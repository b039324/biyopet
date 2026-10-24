"""Ürünler ve Hikayemiz sayfalarına arka plan görseli ekle."""
import io, os

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"

PAGES = {
    "urunler.html": "urunler-hero",
    "hikayemiz.html": "hikayemiz-hero",
}

for page, base in PAGES.items():
    path = os.path.join(ROOT, page)
    text = io.open(path, encoding="utf-8").read()
    old = '    <section class="page-hero">\n      <div class="container">'
    new = (
        '    <section class="page-hero page-hero--media">\n'
        '      <div class="page-hero__media" aria-hidden="true">\n'
        '        <picture>\n'
        f'          <source media="(max-width: 820px)" srcset="assets/img/bg/{base}-mobil.webp" type="image/webp">\n'
        f'          <source media="(max-width: 820px)" srcset="assets/img/bg/{base}-mobil.jpg" type="image/jpeg">\n'
        f'          <source srcset="assets/img/bg/{base}.webp" type="image/webp">\n'
        f'          <img src="assets/img/bg/{base}.jpg" alt="" width="1920" height="823" fetchpriority="high" decoding="async">\n'
        '        </picture>\n'
        '      </div>\n'
        '      <div class="container">'
    )
    if old not in text:
        raise SystemExit(f"{page}: beklenen page-hero bloğu bulunamadı")
    text = text.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("updated", page)
