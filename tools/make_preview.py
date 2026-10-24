"""Compose preview overview images (desktop pages + mobile pages)."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = r"C:\Users\erhan\Documents\ai\biyopet\preview"
CREAM = (253, 251, 246)
GREEN = (15, 59, 41)
MUTED = (95, 114, 105)

font_path = r"C:\Windows\Fonts\segoeuib.ttf"
label_font = ImageFont.truetype(font_path, 22)
small_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)

def load(name):
    return Image.open(os.path.join(BASE, name)).convert("RGB")

def desktop_overview():
    pages = [
        ("index-desktop.png", "Ana Sayfa"),
        ("urunler-desktop.png", "Ürünler"),
        ("hikayemiz-desktop.png", "Hikayemiz"),
        ("iletisim-desktop.png", "İletişim"),
    ]
    target_w = 330
    gap = 34
    top = 120
    thumbs = []
    for name, label in pages:
        im = load(name)
        w = target_w
        h = round(im.height * w / im.width)
        thumbs.append((im.resize((w, h), Image.LANCZOS), label, h))
    max_h = max(h for _, _, h in thumbs)
    width = gap + len(thumbs) * (target_w + gap)
    height = top + max_h + 60
    canvas = Image.new("RGB", (width, height), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.text((gap, 24), "Biyopet — Masaüstü önizleme", font=label_font, fill=GREEN)
    draw.text((gap, 58), "1440 px · tam sayfa görünüm", font=small_font, fill=MUTED)
    x = gap
    for im, label, h in thumbs:
        canvas.paste(im, (x, top))
        draw.rectangle([x - 1, top - 1, x + target_w, top + h], outline=(231, 218, 194))
        draw.text((x, top - 34), label, font=label_font, fill=GREEN)
        x += target_w + gap
    out = os.path.join(BASE, "onizleme-masaustu.png")
    canvas.save(out, "PNG", optimize=True)
    print("saved", out, canvas.size)

def mobile_overview():
    pages = [
        ("index-mobile-hero.png", "Ana Sayfa"),
        ("urunler-mobile-hero.png", "Ürünler"),
        ("iletisim-mobile-hero.png", "İletişim"),
    ]
    gap = 40
    target_h = 1050
    top = 120
    thumbs = []
    for name, label in pages:
        im = load(name)
        h = target_h
        w = round(im.width * h / im.height)
        thumbs.append((im.resize((w, h), Image.LANCZOS), label))
    width = gap + sum(w + gap for im, _ in thumbs for w in [im.width])
    canvas = Image.new("RGB", (width, top + target_h + 54), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.text((gap, 24), "Biyopet — Mobil önizleme", font=label_font, fill=GREEN)
    draw.text((gap, 58), "390 px genişlik · ekran görünümü", font=small_font, fill=MUTED)
    x = gap
    for im, label in thumbs:
        canvas.paste(im, (x, top))
        draw.rectangle([x - 1, top - 1, x + im.width, top + im.height], outline=(231, 218, 194))
        draw.text((x, top - 34), label, font=label_font, fill=GREEN)
        x += im.width + gap
    out = os.path.join(BASE, "onizleme-mobil.png")
    canvas.save(out, "PNG", optimize=True)
    print("saved", out, canvas.size)

desktop_overview()
mobile_overview()
