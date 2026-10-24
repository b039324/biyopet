"""Kullanıcıdan gelen şeffaf zeminli orijinal ambalaj görsellerini optimize et.

Kaynaklar: assets/img/kaynak/*.png (şeffaf zemin, gölgesiz)
Çıktı:     assets/img/opt/*-620.webp|png, *-1100.webp|png
"""
from PIL import Image
import numpy as np
import os, re, io

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"
SRC = os.path.join(ROOT, "assets", "img", "kaynak")
OUT = os.path.join(ROOT, "assets", "img", "opt")
os.makedirs(OUT, exist_ok=True)

NAMES = [
    "urun-kopek-yetiskin-kuzu-pirinc",
    "urun-kedi-yetiskin-tavuklu",
    "urun-kopek-yavru-kuzu-pirinc",
    "urun-kedi-yavru-tavuklu",
]


def trim(im: Image.Image, pad: int = 12) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    return im.crop((max(0, l - pad), max(0, t - pad),
                    min(im.width, r + pad), min(im.height, b + pad)))


def fit_height(im: Image.Image, target_h: int) -> Image.Image:
    ratio = target_h / im.height
    return im.resize((round(im.width * ratio), target_h), Image.LANCZOS)


sizes = {}
for name in NAMES:
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGBA")
    # kaynaklarda zemine yayılmış çok düşük alfalı (1-4) sis/piksel gürültüsünü temizle
    a = np.array(im)
    alpha = a[:, :, 3]
    alpha = np.where(alpha < 10, 0, alpha).astype(np.uint8)
    im = Image.fromarray(np.dstack([a[:, :, :3], alpha]), "RGBA")
    im = trim(im)
    big = fit_height(im, 1100)
    big.save(os.path.join(OUT, name + "-1100.webp"), "WEBP", quality=90, method=6)
    big.save(os.path.join(OUT, name + "-1100.png"), "PNG", optimize=True)
    small = fit_height(im, 620)
    small.save(os.path.join(OUT, name + "-620.webp"), "WEBP", quality=88, method=6)
    small.save(os.path.join(OUT, name + "-620.png"), "PNG", optimize=True)
    sizes[name] = {"1100": big.size, "620": small.size}
    print(name, im.size, "->", big.size, small.size)

# HTML width/height değerlerini üretilen gerçek boyutlarla güncelle
for html_name in ["index.html", "urunler.html", "hikayemiz.html"]:
    path = os.path.join(ROOT, html_name)
    text = io.open(path, encoding="utf-8").read()
    changed = 0
    for name, dims in sizes.items():
        for key in ("1100", "620"):
            w, h = dims[key]
            pattern = re.compile(
                r'(assets/img/opt/' + re.escape(name) + "-" + key + r'\.png" width=")\d+(" height=")\d+'
            )
            text, n = pattern.subn(lambda m: f"{m.group(1)}{w}{m.group(2)}{h}", text)
            changed += n
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print(html_name, "dimension updates:", changed)
