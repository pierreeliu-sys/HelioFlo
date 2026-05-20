#!/usr/bin/env python3
"""
HelioFlo Gallery Image Editor — logo-only version
Color grade + HelioFlo PNG logo composited bottom-left.
"""

from PIL import Image, ImageDraw, ImageEnhance
import os

LOGO_SRC = '/Users/pierreliu/HelioFlo/brand_assets/HelioFlo_Logo.PNG'
SRC_DIR  = '/Users/pierreliu/HelioFlo/Gallery/Unedited'
OUT_DIR  = '/Users/pierreliu/HelioFlo/Gallery/Edited'
os.makedirs(OUT_DIR, exist_ok=True)


def apply_grade(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Sharpness(img).enhance(1.18)
    warm = Image.new('RGB', img.size, (255, 235, 210))
    img  = Image.blend(img, warm, 0.035)
    return img


def make_gradient(W: int, H: int, ratio: float = 0.32) -> Image.Image:
    """Subtle dark bottom gradient to lift logo off the photo."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw  = ImageDraw.Draw(layer)
    y0 = int(H * (1 - ratio))
    for y in range(y0, H):
        t = (y - y0) / max(H - y0, 1)
        a = int(165 * (t ** 0.70))
        draw.line([(0, y), (W, y)], fill=(8, 8, 12, a))
    return layer


def composite_logo(base: Image.Image, logo_src: Image.Image) -> Image.Image:
    """Paste the HelioFlo PNG logo at the bottom-left of base (RGBA)."""
    W, H = base.size

    # Scale logo so its width ≈ 22% of image width, max 300px
    logo_w = min(300, int(W * 0.22))
    logo_h = int(logo_w * logo_src.height / logo_src.width)
    logo   = logo_src.resize((logo_w, logo_h), Image.LANCZOS)

    # Padding
    pad_x = int(W * 0.040)
    pad_y = int(H * 0.038)

    x = pad_x
    y = H - logo_h - pad_y

    base.alpha_composite(logo, dest=(x, y))
    return base


jobs = [
    ('HelioFlo Installation 1.jpeg', 'HelioFlo Installation 1 — Professional.jpeg'),
    ('HelioFlo Installation 2.jpeg', 'HelioFlo Installation 2 — Care.jpeg'),
    ('HelioFlo Installation 3.jpeg', 'HelioFlo Installation 3 — Excellence.jpeg'),
    ('HelioFlo Installation 4.jpeg', 'HelioFlo Installation 4 — Excellence.jpeg'),
]

logo_src = Image.open(LOGO_SRC).convert('RGBA')

for src_name, dst_name in jobs:
    src = os.path.join(SRC_DIR, src_name)
    dst = os.path.join(OUT_DIR, dst_name)
    print(f'  {src_name}')

    img = Image.open(src).convert('RGB')
    img = apply_grade(img)
    W, H = img.size

    img_rgba = img.convert('RGBA')
    grad     = make_gradient(W, H, ratio=0.32)
    img_rgba = Image.alpha_composite(img_rgba, grad)
    img_rgba = composite_logo(img_rgba, logo_src)

    img_rgba.convert('RGB').save(dst, 'JPEG', quality=93, subsampling=0)
    print(f'    → {dst_name}')

print('Done.')
