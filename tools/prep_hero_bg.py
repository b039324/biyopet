"""Ürünler ve Hikayemiz sayfa başlıkları için arka plan görsellerini hazırla.

Kaynak: assets/img/bg/kaynak/*.jpg|png
Çıktı:  assets/img/bg/*.webp + *.jpg  (masaüstü 1920 px, mobil 1080 px)
"""
from PIL import Image, ImageFilter
import os

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"
SRC = os.path.join(ROOT, "assets", "img", "bg", "kaynak")
OUT = os.path.join(ROOT, "assets", "img", "bg")

JOBS = {
    "urunler-hero": "urunler-hero-kaynak.jpg",
    "hikayemiz-hero": "hikayemiz-hero-kaynak.png",
}

DESKTOP = (1920, 823)
MOBILE = (1080, 760)


def cover_crop(im: Image.Image, size, focus=(0.55, 0.45)) -> Image.Image:
    """Hedef orana göre, odak noktasını merkez alarak kırp ve yeniden boyutlandır."""
    target_w, target_h = size
    target_ratio = target_w / target_h
    ratio = im.width / im.height
    if ratio > target_ratio:
        # kaynak daha geniş: sağdan/soldan kırp
        crop_h = im.height
        crop_w = round(crop_h * target_ratio)
        x = round(im.width * focus[0] - crop_w / 2)
        x = max(0, min(x, im.width - crop_w))
        box = (x, 0, x + crop_w, im.height)
    else:
        crop_w = im.width
        crop_h = round(crop_w / target_ratio)
        y = round(im.height * focus[1] - crop_h / 2)
        y = max(0, min(y, im.height - crop_h))
        box = (0, y, im.width, y + crop_h)
    return im.crop(box).resize((target_w, target_h), Image.LANCZOS)


def save_pair(im: Image.Image, base: str) -> None:
    im.save(os.path.join(OUT, base + ".webp"), "WEBP", quality=82, method=6)
    im.save(os.path.join(OUT, base + ".jpg"), "JPEG", quality=84, optimize=True, progressive=True)


for base, source in JOBS.items():
    src = os.path.join(SRC, source)
    im = Image.open(src).convert("RGB")

    desktop = cover_crop(im, DESKTOP, focus=(0.62, 0.5))
    # hafif netleştirme (özellikle küçük kaynak büyütüldüğünde)
    desktop = desktop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
    save_pair(desktop, base)

    mobile = cover_crop(im, MOBILE, focus=(0.55, 0.42))
    mobile = mobile.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=3))
    save_pair(mobile, base + "-mobil")

    print(base, "kaynak", im.size, "masaüstü", desktop.size, "mobil", mobile.size)

for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p):
        print(f, round(os.path.getsize(p) / 1024), "KB")
