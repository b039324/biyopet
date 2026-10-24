"""Apply accessibility, copy and progressive-enhancement fixes to the Biyopet pages."""
import io, os, re

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"

def patch(name, replacements):
    path = os.path.join(ROOT, name)
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    for old, new, expected in replacements:
        count = text.count(old)
        if expected is not None and count != expected:
            raise SystemExit(f"{name}: expected {expected} of {old[:60]!r}, found {count}")
        text = text.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("patched", name)

VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
JS_CLASS = VIEWPORT + '\n  <script>document.documentElement.classList.add(\'js\');</script>'

# ---- Tüm sayfalar: JS sınıfı + 15 kg e -> 15 kg ----
for name in ["index.html", "urunler.html", "hikayemiz.html", "iletisim.html", "yasal.html"]:
    patch(name, [
        (VIEWPORT, JS_CLASS, 1),
        ("15 kg e", "15 kg", None),
        ('href="iletisim.html#form">Toptan &amp; bayilik', 'href="iletisim.html?konu=bayilik#form">Toptan &amp; bayilik', None),
    ])

# ---- Ana sayfa ----
patch("index.html", [
    ("<div class=\"stat\"><strong>4</strong><span>Yaş grubu ürünü</span></div>",
     "<div class=\"stat\"><strong>4</strong><span>Ürün çeşidi</span></div>", 1),
    ('<input id="newsletter-email" name="email" type="email" placeholder="E-posta adresiniz" autocomplete="email" required>',
     '<input id="newsletter-email" name="email" type="email" placeholder="E-posta adresiniz" autocomplete="email" aria-describedby="newsletter-status" required>', 1),
])

# ---- Ürünler ----
patch("urunler.html", [
    ('<div class="filter-bar" data-product-filter aria-label="Ürünleri filtrele">',
     '<div class="filter-bar" data-product-filter role="group" aria-label="Ürünleri filtrele">', 1),
    ('<span class="filter-bar__count"><strong data-filter-count>4</strong> ürün gösteriliyor</span>',
     '<span class="filter-bar__count" aria-live="polite"><strong data-filter-count>4</strong> ürün gösteriliyor</span>', 1),
    ('<button class="guide-tab" type="button" role="tab" data-guide-tab="kopek-yetiskin" aria-selected="true">Yetişkin Köpek</button>',
     '<button class="guide-tab" type="button" role="tab" id="guide-tab-kopek-yetiskin" aria-controls="guide-panel-kopek-yetiskin" data-guide-tab="kopek-yetiskin" aria-selected="true" tabindex="0">Yetişkin Köpek</button>', 1),
    ('<button class="guide-tab" type="button" role="tab" data-guide-tab="kopek-yavru" aria-selected="false">Yavru Köpek</button>',
     '<button class="guide-tab" type="button" role="tab" id="guide-tab-kopek-yavru" aria-controls="guide-panel-kopek-yavru" data-guide-tab="kopek-yavru" aria-selected="false" tabindex="-1">Yavru Köpek</button>', 1),
    ('<button class="guide-tab" type="button" role="tab" data-guide-tab="kedi-yetiskin" aria-selected="false">Yetişkin Kedi</button>',
     '<button class="guide-tab" type="button" role="tab" id="guide-tab-kedi-yetiskin" aria-controls="guide-panel-kedi-yetiskin" data-guide-tab="kedi-yetiskin" aria-selected="false" tabindex="-1">Yetişkin Kedi</button>', 1),
    ('<button class="guide-tab" type="button" role="tab" data-guide-tab="kedi-yavru" aria-selected="false">Yavru Kedi</button>',
     '<button class="guide-tab" type="button" role="tab" id="guide-tab-kedi-yavru" aria-controls="guide-panel-kedi-yavru" data-guide-tab="kedi-yavru" aria-selected="false" tabindex="-1">Yavru Kedi</button>', 1),
    ('<div class="guide-panel" data-guide-panel="kopek-yetiskin" role="tabpanel">',
     '<div class="guide-panel" id="guide-panel-kopek-yetiskin" data-guide-panel="kopek-yetiskin" role="tabpanel" aria-labelledby="guide-tab-kopek-yetiskin" tabindex="0">', 1),
    ('<div class="guide-panel" data-guide-panel="kopek-yavru" role="tabpanel" hidden>',
     '<div class="guide-panel" id="guide-panel-kopek-yavru" data-guide-panel="kopek-yavru" role="tabpanel" aria-labelledby="guide-tab-kopek-yavru" tabindex="0" hidden>', 1),
    ('<div class="guide-panel" data-guide-panel="kedi-yetiskin" role="tabpanel" hidden>',
     '<div class="guide-panel" id="guide-panel-kedi-yetiskin" data-guide-panel="kedi-yetiskin" role="tabpanel" aria-labelledby="guide-tab-kedi-yetiskin" tabindex="0" hidden>', 1),
    ('<div class="guide-panel" data-guide-panel="kedi-yavru" role="tabpanel" hidden>',
     '<div class="guide-panel" id="guide-panel-kedi-yavru" data-guide-panel="kedi-yavru" role="tabpanel" aria-labelledby="guide-tab-kedi-yavru" tabindex="0" hidden>', 1),
    ("3–5 ay yeterli olabilir", "yaklaşık 6–9 ay yeterli olabilir", 1),
    ('href="iletisim.html#form">Bayilik Talep Et', 'href="iletisim.html?konu=bayilik#form">Bayilik Talep Et', 4),
    ('href="iletisim.html#form">Teklif Alın', 'href="iletisim.html?konu=bayilik#form">Teklif Alın', 1),
])

# ---- İletişim ----
patch("iletisim.html", [
    ("Formu doldurun ya da doğrudan arayın; en kısa sürede dönüş yapalım.",
     "Formu doldurun ya da doğrudan arayın; size en kısa sürede dönüş yapacağız.", 1),
    ("Formu doldurun, talebinizi ilgili ekibe ileten kadar takip edelim.",
     "Formu doldurun; talebinizi ilgili ekibe ilettikten sonra süreci birlikte takip edelim.", 1),
    ('<div class="map-panel" role="img" aria-label="Biyopet merkez ofis konumu">',
     '<div class="map-panel">', 1),
    ('<span class="map-panel__note">Temsili konum görseli</span>',
     '<span class="map-panel__note">Konum: İstanbul · temsili görsel</span>', 1),
    ('<input id="name" name="name" type="text" autocomplete="name" placeholder="Adınız ve soyadınız" required minlength="2">',
     '<input id="name" name="name" type="text" autocomplete="name" placeholder="Adınız ve soyadınız" aria-describedby="err-name" required minlength="2">', 1),
    ('<p class="field__error" data-error-for="name" aria-live="polite"></p>',
     '<p class="field__error" id="err-name" data-error-for="name" aria-live="polite"></p>', 1),
    ('<input id="email" name="email" type="email" autocomplete="email" placeholder="ornek@eposta.com" required>',
     '<input id="email" name="email" type="email" autocomplete="email" placeholder="ornek@eposta.com" aria-describedby="err-email" required>', 1),
    ('<p class="field__error" data-error-for="email" aria-live="polite"></p>',
     '<p class="field__error" id="err-email" data-error-for="email" aria-live="polite"></p>', 1),
    ('<input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="05xx xxx xx xx">',
     '<input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="05xx xxx xx xx" aria-describedby="err-phone">', 1),
    ('<p class="field__error" data-error-for="phone"></p>',
     '<p class="field__error" id="err-phone" data-error-for="phone"></p>', 1),
    ('<select id="topic" name="topic">',
     '<select id="topic" name="topic" aria-describedby="err-topic">', 1),
    ('<p class="field__error" data-error-for="topic"></p>',
     '<p class="field__error" id="err-topic" data-error-for="topic"></p>', 1),
    ('<textarea id="message" name="message" placeholder="Bize iletmek istedikleriniz..." required minlength="10"></textarea>',
     '<textarea id="message" name="message" placeholder="Bize iletmek istedikleriniz..." aria-describedby="err-message" required minlength="10"></textarea>', 1),
    ('<p class="field__error" data-error-for="message" aria-live="polite"></p>',
     '<p class="field__error" id="err-message" data-error-for="message" aria-live="polite"></p>', 1),
    ('''                <label class="checkbox-field" for="consent">
                  <input id="consent" name="consent" type="checkbox" required>
                  <span><a href="yasal.html#kvkk">KVKK Aydınlatma Metnini</a> okudum, kişisel verilerimin talebimin
                    yanıtlanması amacıyla işlenmesini kabul ediyorum.</span>
                </label>
                <p class="field__error" data-error-for="consent" aria-live="polite"></p>''',
     '''                <div class="checkbox-field">
                  <input id="consent" name="consent" type="checkbox" aria-describedby="err-consent" required>
                  <div class="checkbox-field__body">
                    <label for="consent">Kişisel verilerimin talebimin yanıtlanması amacıyla işlenmesini kabul ediyorum.</label>
                    <a class="checkbox-field__link" href="yasal.html#kvkk">KVKK Aydınlatma Metni’ni okuyun</a>
                  </div>
                </div>
                <p class="field__error" id="err-consent" data-error-for="consent" aria-live="polite"></p>''', 1),
    ('''            <div class="guide__note" style="margin-top:22px">
              <svg aria-hidden="true"><use href="#i-info"/></svg>
              <span>Bu alan önizleme amaçlıdır. Form gönderimi bir sunucuya bağlı değildir; gerçek
                kullanımda e-posta servisi veya CRM entegrasyonu eklenmelidir.</span>
            </div>
''', '', 1),
])

# ---- Hikayemiz ----
patch("hikayemiz.html", [
    ("Özenle seçilmiş hammaddeler ve koruyucu içermeyen formüllerle",
     "Özenle seçilmiş hammaddeler ve dengeli formüllerle", 1),
    ("<div class=\"stat\"><strong>4</strong><span>Yaş grubu ürünü</span></div>",
     "<div class=\"stat\"><strong>4</strong><span>Ürün çeşidi</span></div>", 1),
    ("<div class=\"stat\"><strong>7/24</strong><span>Müşteri desteği hedefi</span></div>",
     "<div class=\"stat\"><strong>4</strong><span>Üretim adımı</span></div>", 1),
])

# ---- Yasal: canlı sayfadaki örnek metin uyarısını kaldır ----
patch("yasal.html", [
    ('''          <div class="guide__note">
            <svg aria-hidden="true"><use href="#i-info"/></svg>
            <span>Bu metinler genel bilgilendirme amacıyla hazırlanmış örnek metinlerdir.
              Yayına almadan önce hukuk danışmanınızla birlikte şirket bilgilerinize ve
              yürürlükteki mevzuata göre uyarlanmalıdır.</span>
          </div>

''', '', 1),
])

print("done")
