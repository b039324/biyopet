/* Functional smoke tests via Chrome DevTools Protocol. */
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9334;
const BASE = "http://127.0.0.1:8099";
const userDataDir = path.join(process.env.TEMP || ".", "biyopet-test-" + Date.now());
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--hide-scrollbars", "--disable-extensions", "--mute-audio",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${userDataDir}`, "about:blank",
], { stdio: "ignore" });

function cleanup(code) { try { chrome.kill(); } catch {} process.exit(code); }

let version;
for (let i = 0; i < 60; i++) {
  try {
    const res = await fetch(`http://127.0.0.1:${PORT}/json/version`);
    if (res.ok) { version = await res.json(); break; }
  } catch {}
  await sleep(250);
}
if (!version) { console.error("Chrome did not start"); cleanup(1); }

const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = targets.find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

let nextId = 1;
const pending = new Map();
const listeners = new Map();
const consoleErrors = [];
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(JSON.stringify(msg.error)));
    else resolve(msg.result);
  } else if (msg.method === "Runtime.exceptionThrown") {
    consoleErrors.push(msg.params.exceptionDetails.text + " " + (msg.params.exceptionDetails.exception?.description || ""));
  } else if (msg.method === "Log.entryAdded" && msg.params.entry.level === "error") {
    consoleErrors.push(msg.params.entry.text);
  } else if (msg.method && listeners.has(msg.method)) {
    const arr = listeners.get(msg.method);
    listeners.delete(msg.method);
    arr.forEach((fn) => fn(msg.params));
  }
};
function send(method, params = {}) {
  const id = nextId++;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}
function once(method, timeout = 20000) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("timeout " + method)), timeout);
    const fn = (params) => { clearTimeout(timer); resolve(params); };
    if (listeners.has(method)) listeners.get(method).push(fn);
    else listeners.set(method, [fn]);
  });
}
async function evaluate(expression) {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + " " + (r.exceptionDetails.exception?.description || ""));
  return r.result.value;
}
async function load(url, width = 1440, height = 940, mobile = false) {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile });
  const loaded = once("Page.loadEventFired");
  await send("Page.navigate", { url });
  await loaded;
  await sleep(800);
  await evaluate(`(async()=>{document.documentElement.style.scrollBehavior='auto';const h=document.documentElement.scrollHeight;for(let y=0;y<h;y+=600){window.scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,60));}window.scrollTo({top:0,behavior:'instant'});await new Promise(r=>setTimeout(r,300));await Promise.all([...document.images].map(img=>img.decode().catch(()=>{})));await new Promise(r=>setTimeout(r,500));})()`);
}

await send("Page.enable");
await send("Runtime.enable");
await send("Log.enable");

const results = [];
const check = (name, pass, detail = "") => results.push({ name, pass, detail });

// ---- Ana sayfa ----
await load(`${BASE}/index.html`);
check("Ana sayfa: yatay taşma yok", await evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
  await evaluate("document.documentElement.scrollWidth + '/' + window.innerWidth"));
check("Ana sayfa: tüm görseller yüklü", await evaluate("[...document.images].every(i => i.complete && i.naturalWidth > 0)"),
  await evaluate("JSON.stringify([...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.currentSrc||i.src))"));
check("Ana sayfa: reveal animasyonları tamam", await evaluate("document.querySelectorAll('.reveal:not(.is-visible)').length === 0"),
  await evaluate("document.querySelectorAll('.reveal:not(.is-visible)').length"));
await evaluate("document.querySelectorAll('.faq__item')[1].querySelector('summary').click()");
check("SSS: tek açık öğe davranışı",
  await evaluate("document.querySelectorAll('.faq__item')[1].open === true && document.querySelectorAll('.faq__item')[0].open === false"));
await evaluate("(() => { const f = document.getElementById('newsletter-form'); const i = document.getElementById('newsletter-email'); i.value = 'gecersiz'; f.requestSubmit(); })()");
check("Bülten: geçersiz e-posta uyarısı", (await evaluate("document.getElementById('newsletter-status').textContent")).includes("geçerli"));
await evaluate("(() => { const f = document.getElementById('newsletter-form'); const i = document.getElementById('newsletter-email'); i.value = 'test@example.com'; f.requestSubmit(); })()");
check("Bülten: geçerli e-posta kaydı", (await evaluate("document.getElementById('newsletter-status').textContent")).includes("Teşekkürler"));

// ---- Ürünler ----
await load(`${BASE}/urunler.html`);
const visible = () => evaluate("[...document.querySelectorAll('[data-product]')].filter(c => !c.classList.contains('is-hidden')).length");
check("Filtre: başlangıçta 4 ürün", (await visible()) === 4);
await evaluate("document.querySelector('[data-filter=\"kopek\"]').click()");
check("Filtre: Köpek = 2", (await visible()) === 2, await evaluate("document.querySelector('[data-filter-count]').textContent"));
await evaluate("document.querySelector('[data-filter=\"yavru\"]').click()");
check("Filtre: Yavru = 2", (await visible()) === 2);
await evaluate("document.querySelector('[data-filter=\"all\"]').click()");
check("Filtre: Tümü = 4", (await visible()) === 4);
check("Ürünler: tüm görseller yüklü", await evaluate("[...document.images].every(i => i.complete && i.naturalWidth > 0)"));
check("Ürünler: anchored section mevcut", await evaluate("['kopek-yetiskin','kopek-yavru','kedi-yetiskin','kedi-yavru'].every(id => !!document.getElementById(id))"));
await evaluate("document.querySelector('[data-guide-tab=\"kedi-yavru\"]').click()");
check("Besleme: sekme geçişi",
  await evaluate("document.querySelector('[data-guide-panel=\"kedi-yavru\"]').hidden === false && document.querySelector('[data-guide-panel=\"kopek-yetiskin\"]').hidden === true"));
check("Ürünler: yatay taşma yok", await evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
  await evaluate("document.documentElement.scrollWidth + '/' + window.innerWidth"));

// ---- Mobil menü ----
await load(`${BASE}/index.html`, 390, 844, true);
check("Mobil: yatay taşma yok", await evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
  await evaluate("document.documentElement.scrollWidth + '/' + window.innerWidth"));
check("Mobil: menü başlangıçta kapalı", await evaluate("!document.getElementById('nav-links').classList.contains('is-open')"));
await evaluate("document.getElementById('nav-toggle').click()");
check("Mobil: menü açılıyor",
  await evaluate("document.getElementById('nav-links').classList.contains('is-open') && document.getElementById('nav-toggle').getAttribute('aria-expanded') === 'true'"));
await evaluate("document.body.click()");
check("Mobil: dışına tıklayınca kapanıyor", await evaluate("!document.getElementById('nav-links').classList.contains('is-open')"));

// ---- İletişim ----
await load(`${BASE}/iletisim.html`);
await evaluate("document.getElementById('contact-form').requestSubmit()");
check("Form: boş gönderim engellendi",
  (await evaluate("document.getElementById('form-status').textContent")).length > 0 &&
  await evaluate("document.querySelector('[data-error-for=\"name\"]').textContent.length > 0"));
check("Form: onay kutusu hatası görünür", await evaluate("document.querySelector('[data-error-for=\"consent\"]').textContent.length > 0"));
await evaluate(`(() => {
  const f = document.getElementById('contact-form');
  f.elements.namedItem('name').value = 'Ayşe Yılmaz';
  f.elements.namedItem('email').value = 'ayse@example.com';
  f.elements.namedItem('message').value = 'Merhaba, bayilik hakkında bilgi almak istiyorum.';
  f.elements.namedItem('consent').checked = true;
  f.requestSubmit();
})()`);
check("Form: geçerli gönderim başarılı", (await evaluate("document.getElementById('form-status').textContent")).includes("Mesajınız alındı"));
check("Form: başarıdan sonra alanlar temiz", (await evaluate("document.getElementById('contact-form').elements.namedItem('name').value")) === "");
check("İletişim: yatay taşma yok", await evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")); 
check("İletişim: anchor hedefi var", await evaluate("!!document.getElementById('form')"));

// ---- Bayilik ön seçimi ----
await load(`${BASE}/iletisim.html?konu=bayilik#form`);
check("Form: bayilik konusu ön seçili", (await evaluate("document.getElementById('topic').value")) === "bayilik");

// ---- Besleme sekmeleri ARIA ----
await load(`${BASE}/urunler.html`);
check("Besleme: tab/panel ARIA bağlantısı",
  await evaluate("['kopek-yetiskin','kopek-yavru','kedi-yetiskin','kedi-yavru'].every(k => { const t = document.getElementById('guide-tab-' + k); return t && t.getAttribute('aria-controls') === 'guide-panel-' + k && !!document.getElementById(t.getAttribute('aria-controls')); })"));

// ---- Yasal sayfa ----
await load(`${BASE}/yasal.html`);
check("Yasal: üç bölüm mevcut", await evaluate("['kvkk','gizlilik','cerez'].every(id => !!document.getElementById(id))"));

// ---- Konsol hataları ----
check("Konsol hatası yok", consoleErrors.length === 0, consoleErrors.join(" | ").slice(0, 300));

console.log("\n=== SITE TEST RESULTS ===");
for (const r of results) console.log(`${r.pass ? "PASS" : "FAIL"}  ${r.name}${r.detail ? "  [" + r.detail + "]" : ""}`);
const failed = results.filter((r) => !r.pass).length;
console.log(`\n${results.length - failed}/${results.length} passed`);
await fs.writeFile(path.join("C:\\Users\\erhan\\Documents\\ai\\biyopet\\preview", "test-results.json"), JSON.stringify(results, null, 2));
ws.close();
cleanup(failed ? 2 : 0);
