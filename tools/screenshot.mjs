/* Full-page screenshots via Chrome DevTools Protocol (no npm deps). */
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const PORT = 9333;
const BASE = "http://127.0.0.1:8099";
const OUT = "C:\\Users\\erhan\\Documents\\ai\\biyopet\\preview";
const userDataDir = path.join(process.env.TEMP || ".", "biyopet-cdp-" + Date.now());

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(
  CHROME,
  [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--hide-scrollbars",
    "--disable-extensions",
    "--mute-audio",
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${userDataDir}`,
    "about:blank",
  ],
  { stdio: "ignore" }
);

function cleanup(code) {
  try { chrome.kill(); } catch {}
  process.exit(code);
}
process.on("SIGINT", () => cleanup(130));

let version;
for (let i = 0; i < 60; i++) {
  try {
    const res = await fetch(`http://127.0.0.1:${PORT}/json/version`);
    if (res.ok) { version = await res.json(); break; }
  } catch {}
  await sleep(250);
}
if (!version) {
  console.error("Chrome DevTools endpoint did not start.");
  cleanup(1);
}

const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
let page = targets.find((t) => t.type === "page");
if (!page) {
  page = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json();
}

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  ws.onopen = resolve;
  ws.onerror = reject;
});

let nextId = 1;
const pending = new Map();
const listeners = new Map();
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(JSON.stringify(msg.error)));
    else resolve(msg.result);
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
    const timer = setTimeout(() => reject(new Error("timeout: " + method)), timeout);
    const fn = (params) => { clearTimeout(timer); resolve(params); };
    if (listeners.has(method)) listeners.get(method).push(fn);
    else listeners.set(method, [fn]);
  });
}

await send("Page.enable");
await send("Runtime.enable");

const inject = `
(() => {
  const style = document.createElement('style');
  style.textContent = \`
    *, *::before, *::after { animation: none !important; }
    .reveal { opacity: 1 !important; transform: none !important; }
    html { scroll-behavior: auto !important; }
  \`;
  document.head.appendChild(style);
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
})();
`;

async function load(url) {
  const loaded = once("Page.loadEventFired");
  await send("Page.navigate", { url });
  await loaded;
  await sleep(700);
  await send("Runtime.evaluate", { expression: inject });
  await sleep(250);
  // lazy-load tüm görsellerin yüklenmesi için sayfayı baştan sona kaydır
  await send("Runtime.evaluate", {
    expression: `(async () => {
      document.documentElement.style.scrollBehavior = 'auto';
      const h = document.documentElement.scrollHeight;
      for (let y = 0; y < h; y += 600) {
        window.scrollTo({ top: y, behavior: 'instant' });
        await new Promise((r) => setTimeout(r, 60));
      }
      window.scrollTo({ top: 0, behavior: 'instant' });
      await new Promise((r) => setTimeout(r, 300));
      await Promise.all([...document.images].map((img) => img.decode().catch(() => {})));
      await new Promise((r) => setTimeout(r, 500));
    })()`,
    awaitPromise: true,
  });
  await sleep(400);
}

async function fullPage(file) {
  const { result } = await send("Runtime.evaluate", {
    expression: "({w: Math.max(document.documentElement.scrollWidth, window.innerWidth), h: Math.max(document.documentElement.scrollHeight, window.innerHeight)})",
    returnByValue: true,
  });
  const width = Math.ceil(result.value.w);
  const height = Math.ceil(result.value.h);
  const shot = await send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: true,
    clip: { x: 0, y: 0, width, height, scale: 1 },
  });
  await fs.writeFile(file, Buffer.from(shot.data, "base64"));
  console.log("saved", file, `${width}x${height}`);
}

async function viewport(file) {
  const shot = await send("Page.captureScreenshot", { format: "png" });
  await fs.writeFile(file, Buffer.from(shot.data, "base64"));
  console.log("saved", file, "viewport");
}

const pages = ["index", "urunler", "hikayemiz", "iletisim", "yasal"];

// Desktop full page + hero viewport
for (const name of pages) {
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 940, deviceScaleFactor: 1, mobile: false });
  await load(`${BASE}/${name}.html`);
  await viewport(path.join(OUT, `${name}-hero.png`));
  await fullPage(path.join(OUT, `${name}-desktop.png`));
}

// Mobile full page + hero viewport
for (const name of ["index", "urunler", "hikayemiz", "iletisim"]) {
  await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await load(`${BASE}/${name}.html`);
  await fullPage(path.join(OUT, `${name}-mobile.png`));

  await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await load(`${BASE}/${name}.html`);
  await viewport(path.join(OUT, `${name}-mobile-hero.png`));
}

ws.close();
cleanup(0);
