#!/usr/bin/env python3
"""
HelioFlo Facebook Ad v3 — All Three Ranges
Full-bleed photo hero with floating product PNGs (Solterra-style).
No pricing. No white/cream sections. Coloured backgrounds everywhere.
1080 × 1350 px
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

W, H = 1080, 1350

C_RED   = (181,  69,  27)
C_TEAL  = (  0, 201, 167)
C_GOLD  = (212, 168,  71)
C_WHITE = (255, 255, 255)
C_DARK  = ( 14,  16,  22)
C_MUTED = (160, 155, 145)
C_CREAM = (251, 247, 242)

# Dark saturated card backgrounds
BG_RED  = ( 95,  28,  8)
BG_TEAL = (  0,  72, 60)
BG_GOLD = ( 88,  58,  8)

# Info box backgrounds
IB = [(0, 90, 76), (115, 35, 10), (90, 64, 8), (22, 24, 32)]

F_GB  = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
F_GI  = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
F_HV  = '/System/Library/Fonts/Helvetica.ttc'

BASE = '/Users/pierreliu/HelioFlo'
OUT  = os.path.join(BASE, 'Facebook Ads', 'HelioFlo Ad — All Ranges.png')

# ── Section geometry ──────────────────────────────────────────────────
PHOTO_H = 640     # lifestyle photo with floating products
BAND_H  =  48     # "CHOOSE YOUR BATTERY SYSTEM" dark banner
CARD_H  = 320     # 3 tier cards side-by-side
INFO_H  = 102     # 4 info boxes
CTA_H   = 178     # brand-red CTA
FOOT_H  =  62     # near-black footer strip
# 640+48+320+102+178+62 = 1350 ✓

Y_BAND  = PHOTO_H
Y_CARDS = Y_BAND  + BAND_H
Y_INFO  = Y_CARDS + CARD_H
Y_CTA   = Y_INFO  + INFO_H
Y_FOOT  = Y_CTA   + CTA_H


def tbbox(font, text):
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]

def remove_white(img, thr=234):
    img = img.convert('RGBA')
    data = list(img.getdata())
    img.putdata([(r, g, b, 0) if r >= thr and g >= thr and b >= thr
                 else (r, g, b, a) for r, g, b, a in data])
    return img

def fit_into(img, bw, bh, pad=10):
    iw, ih = img.size
    s = min((bw - pad*2) / iw, (bh - pad*2) / ih)
    return img.resize((int(iw*s), int(ih*s)), Image.LANCZOS)

def load_logo(h=50):
    logo = Image.open(f'{BASE}/brand_assets/HelioFlo_Logo.PNG').convert('RGBA')
    w = int(h * logo.width / logo.height)
    return logo.resize((w, h), Image.LANCZOS)

def shadow_text(draw, xy, text, font, fill, sdist=2, sop=85):
    x, y = xy
    draw.text((x+sdist, y+sdist), text, font=font, fill=(*C_DARK[:3], sop))
    draw.text(xy, text, font=font, fill=fill)

def tick(draw, cx, cy, r, color):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, 255))
    lw = max(2, r // 3)
    draw.line([(cx-r//2+1, cy+1), (cx-r//7, cy+r//2)], fill=C_WHITE, width=lw)
    draw.line([(cx-r//7, cy+r//2), (cx+r//2-1, cy-r//2+2)], fill=C_WHITE, width=lw)


# ════════════════════════════════════════════════════════════════════
# 1. PHOTO HERO  (0 → 640)
# ════════════════════════════════════════════════════════════════════
canvas = Image.new('RGBA', (W, H), C_DARK)

bg = Image.open(f'{BASE}/Facebook Ads/Stock Photos/Solar Panel Home 3.jpg').convert('RGB')
bw, bh = bg.size
# Scale to W=1080, then center-crop height to PHOTO_H
bg = bg.resize((W, int(bh * W / bw)), Image.LANCZOS)
off_y = (bg.height - PHOTO_H) // 2
bg = bg.crop((0, off_y, W, off_y + PHOTO_H))
bg = ImageEnhance.Brightness(bg).enhance(0.80)
bg = ImageEnhance.Color(bg).enhance(1.14)
canvas.alpha_composite(bg.convert('RGBA'), dest=(0, 0))

d = ImageDraw.Draw(canvas)

# ── Composite gradient overlay ────────────────────────────────────────
ov = Image.new('RGBA', (W, PHOTO_H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)

# Left column: dark → transparent (for headline legibility)
for x in range(W):
    t = x / W
    a = int(215 * max(0, 1 - (t / 0.60) ** 1.65))
    od.line([(x, 0), (x, PHOTO_H)], fill=(*C_DARK, a))

# Top band: dark bar (logo + badge area)
for y in range(84):
    a = int(175 * (1 - y / 84) ** 0.5)
    od.line([(0, y), (W, y)], fill=(*C_DARK, a))

# Bottom fade: photo dissolves into the dark band below
for y in range(90):
    yy = PHOTO_H - 90 + y
    a  = int(230 * (y / 90) ** 2.0)
    od.line([(0, yy), (W, yy)], fill=(*C_DARK, a))

canvas.alpha_composite(ov, dest=(0, 0))
d = ImageDraw.Draw(canvas)

# Red accent stripe at very top
d.rectangle([0, 0, W, 4], fill=(*C_RED, 255))

# ── HelioFlo logo ─────────────────────────────────────────────────────
logo = load_logo(50)
canvas.alpha_composite(logo, dest=(28, 16))
d = ImageDraw.Draw(canvas)

# ── Sydney badge ──────────────────────────────────────────────────────
fBadge = ImageFont.truetype(F_HV, 11)
btxt = "SERVICING SYDNEY, NSW"
bw2, bh2 = tbbox(fBadge, btxt)
bpx, bpy = 12, 6
bx1 = W - bw2 - bpx*2 - 28
by1 = 18
d.rounded_rectangle([bx1, by1, bx1+bw2+bpx*2, by1+bh2+bpy*2],
                     radius=9, fill=(*C_TEAL, 230))
d.text((bx1+bpx, by1+bpy), btxt, font=fBadge, fill=C_WHITE)

# ── Headline block ────────────────────────────────────────────────────
fH1  = ImageFont.truetype(F_GB,  68)
fSub = ImageFont.truetype(F_GI,  22)
fEye = ImageFont.truetype(F_HV,  14)
fBen = ImageFont.truetype(F_HV,  13)

tx, ty = 34, 90

# Eyebrow
ey = "SOLAR BATTERY INSTALLATION"
ew, eh = tbbox(fEye, ey)
d.rectangle([tx, ty + eh//2 - 1, tx+10, ty + eh//2 + 1], fill=(*C_TEAL, 220))
d.text((tx+18, ty), ey, font=fEye, fill=(*C_TEAL, 240))
ty += eh + 14

shadow_text(d, (tx, ty), "Power Your Home.", fH1, C_WHITE, sdist=2, sop=100)
_, h1h = tbbox(fH1, "Power Your Home.")
ty += h1h - 2

shadow_text(d, (tx, ty), "Cut Your Bills.", fH1, C_WHITE, sdist=2, sop=100)
_, h2h = tbbox(fH1, "Cut Your Bills.")
ty += h2h + 14

shadow_text(d, (tx, ty), "Professional installation for Sydney homeowners.",
            fSub, (*C_WHITE, 205), sdist=1, sop=50)
_, sh = tbbox(fSub, "x")
ty += sh + 22

# Inline benefit chips
for bc, bt in [(C_TEAL, "Blackout Backup"),
               (C_RED,  "Govt Rebate Eligible"),
               (C_GOLD, "SAA Licensed")]:
    btw, bth = tbbox(fBen, bt)
    pad = 9
    d.rounded_rectangle([tx, ty, tx+btw+pad*2, ty+bth+10],
                         radius=7, fill=(*bc, 50), outline=(*bc, 180), width=1)
    d.text((tx+pad, ty+5), bt, font=fBen, fill=(*C_WHITE, 240))
    tx += btw + pad*2 + 8

# ── 3 product PNGs floating on photo (right side, stacked) ───────────
prods = [
    (f'{BASE}/Solis/Solis Dyness Battery Image.jpg',     C_RED,  "ESSENTIAL"),
    (f'{BASE}/Swatten/ Product Image All-in-One System Three Phase (HV) (10-20) kW.png',
                                                          C_TEAL, "MID-MARKET"),
    (f'{BASE}/EcoFlow/Product Image PO.png',              C_GOLD, "PREMIUM"),
]
fLbl    = ImageFont.truetype(F_HV, 10)
px0     = 618          # left edge of product panel
pw      = W - px0      # 462 px wide
slot_h  = (PHOTO_H - 36) // 3   # ≈ 201 px per product slot

for i, (pp, acc, lbl) in enumerate(prods):
    sy = 18 + i * slot_h
    try:
        pi = Image.open(pp).convert('RGBA')
        pi = remove_white(pi, thr=232)
        pi = fit_into(pi, pw, slot_h, pad=12)
        px = px0 + (pw - pi.width)  // 2
        py = sy  + (slot_h - pi.height) // 2
        canvas.alpha_composite(pi, dest=(int(px), int(py)))
        d = ImageDraw.Draw(canvas)
    except Exception as e:
        print(f"  [warn] {e}")

    # Accent label tab at bottom-right of each slot
    lw2, lh2 = tbbox(fLbl, lbl)
    lx = W - lw2 - 12
    ly = sy + slot_h - lh2 - 8
    d.rectangle([lx-8, ly-3, W, ly+lh2+3], fill=(*acc, 200))
    d.text((lx, ly), lbl, font=fLbl, fill=C_WHITE)

    # Subtle slot separator
    if i > 0:
        d.line([(px0+18, sy), (W-18, sy)], fill=(255, 255, 255, 18))

# Subtle vertical divider between text column and product column
d.line([(px0-6, 86), (px0-6, PHOTO_H-96)], fill=(255, 255, 255, 14))


# ════════════════════════════════════════════════════════════════════
# 2. TIER BAND  (640 → 688)
# ════════════════════════════════════════════════════════════════════
d.rectangle([0, Y_BAND, W, Y_CARDS], fill=(*C_DARK, 255))
d.rectangle([0, Y_BAND, W, Y_BAND+3], fill=(*C_RED, 255))

fBand = ImageFont.truetype(F_GB, 22)
band_txt = "CHOOSE YOUR BATTERY SYSTEM"
bw3, bh3 = tbbox(fBand, band_txt)
d.text(((W - bw3)//2, Y_BAND + (BAND_H - bh3)//2), band_txt, font=fBand, fill=C_WHITE)

# Thin teal accent line at base of band
d.rectangle([0, Y_CARDS-3, W, Y_CARDS], fill=(*C_TEAL, 55))


# ════════════════════════════════════════════════════════════════════
# 3. TIER CARDS  (688 → 1008)  — 3 × 360 px, flush, no gutters
# ════════════════════════════════════════════════════════════════════
CARD_W = W // 3   # 360

TIERS = [
    dict(bg=BG_RED,  acc=C_RED,
         lbl="ESSENTIAL RANGE",
         s1="Start Your",   s2="Solar Journey.",
         sub="Single-Phase  ·  LiFePO4  ·  Entry-Level",
         feats=["LiFePO4 Battery Chemistry",
                "Single-Phase Blackout Backup",
                "Smart App Monitoring",
                "Expandable Up to 50 Units"]),
    dict(bg=BG_TEAL, acc=C_TEAL, rec=True,
         lbl="MID-MARKET RANGE",
         s1="Whole-Home",   s2="Protection.",
         sub="Three-Phase  ·  All-in-One  ·  Most Popular",
         feats=["All-in-One Inverter + Battery",
                "Three-Phase Whole-Home Backup",
                "10-Year Manufacturer Warranty",
                "Federal Rebate Eligible"]),
    dict(bg=BG_GOLD, acc=C_GOLD,
         lbl="PREMIUM RANGE",
         s1="Total Energy", s2="Independence.",
         sub="Three-Phase  ·  EV-Ready  ·  Modular",
         feats=["Three-Phase Blackout Backup",
                "EV-Ready + Smart App Control",
                "Modular Expandable Capacity",
                "Maximum Grid Independence"]),
]

fCL  = ImageFont.truetype(F_HV,  13)
fCS  = ImageFont.truetype(F_GB,  38)
fCsb = ImageFont.truetype(F_HV,  12)
fFt  = ImageFont.truetype(F_HV,  14)
fRec = ImageFont.truetype(F_GB,  10)

for i, td in enumerate(TIERS):
    cx1, cx2 = i * CARD_W, (i+1) * CARD_W
    acc = td['acc']

    d.rectangle([cx1, Y_CARDS, cx2, Y_INFO], fill=(*td['bg'], 255))
    d.rectangle([cx1, Y_CARDS, cx2, Y_CARDS+5], fill=(*acc, 255))

    if i > 0:
        d.line([(cx1, Y_CARDS+5), (cx1, Y_INFO)], fill=(255,255,255,18))

    # MOST POPULAR badge (mid-market)
    if td.get('rec'):
        rt = "★  MOST POPULAR  ★"
        rw, rh = tbbox(fRec, rt)
        rpx, rpy = 10, 4
        rx1 = cx1 + (CARD_W - rw - rpx*2) // 2
        ry1 = Y_CARDS + 8
        d.rounded_rectangle([rx1, ry1, rx1+rw+rpx*2, ry1+rh+rpy*2],
                              radius=6, fill=(*acc, 55))
        d.text((rx1+rpx, ry1+rpy), rt, font=fRec, fill=(*acc, 240))
        ny = ry1 + rh + rpy*2 + 6
    else:
        ny = Y_CARDS + 12

    # Tier label
    lw2, lh2 = tbbox(fCL, td['lbl'])
    d.text((cx1 + (CARD_W-lw2)//2, ny), td['lbl'], font=fCL, fill=(*acc, 215))
    ny += lh2 + 6

    # Big statement (2 lines)
    sw1, sh1 = tbbox(fCS, td['s1'])
    sw2, sh2 = tbbox(fCS, td['s2'])
    d.text((cx1 + (CARD_W-sw1)//2, ny),      td['s1'], font=fCS, fill=C_WHITE)
    d.text((cx1 + (CARD_W-sw2)//2, ny+sh1+2), td['s2'], font=fCS, fill=C_WHITE)
    ny += sh1 + 2 + sh2 + 6

    # Subtitle spec
    sbw, sbh = tbbox(fCsb, td['sub'])
    d.text((cx1 + (CARD_W-sbw)//2, ny), td['sub'], font=fCsb, fill=(*acc, 200))
    ny += sbh + 12

    # Thin divider
    d.rectangle([cx1+14, ny, cx2-14, ny+1], fill=(255,255,255,30))
    ny += 11

    # Feature bullets
    for feat in td['feats']:
        r = 5
        tick(d, cx1+16, ny+9, r, acc)
        d.text((cx1+29, ny), feat, font=fFt, fill=(*C_WHITE, 228))
        ny += tbbox(fFt, feat)[1] + 9


# ════════════════════════════════════════════════════════════════════
# 4. INFO BOXES  (1008 → 1110)
# ════════════════════════════════════════════════════════════════════
BOX_W = W // 4   # 270

INFO_ITEMS = [
    (IB[0], C_TEAL, "SAA ACCREDITED",    "Licensed Installer"),
    (IB[1], C_RED,  "GOVT REBATE",       "Handled End-to-End"),
    (IB[2], C_GOLD, "10-YEAR WARRANTY",  "Manufacturer Backed"),
    (IB[3], C_TEAL, "FREE QUOTE",        "No Obligation"),
]

fIB  = ImageFont.truetype(F_GB,  13)
fIBs = ImageFont.truetype(F_HV,  12)

for i, (bg_col, acc, t1, t2) in enumerate(INFO_ITEMS):
    bx1 = i * BOX_W
    bx2 = bx1 + BOX_W
    d.rectangle([bx1, Y_INFO, bx2, Y_CTA], fill=(*bg_col, 255))
    if i > 0:
        d.line([(bx1, Y_INFO+8), (bx1, Y_CTA-8)], fill=(255,255,255,18))

    mcy = (Y_INFO + Y_CTA) // 2
    tick(d, bx1+20, mcy, 8, acc)

    tx3 = bx1 + 36
    t1w, t1h = tbbox(fIB,  t1)
    t2w, t2h = tbbox(fIBs, t2)
    tot = t1h + 3 + t2h
    ty3 = mcy - tot // 2
    d.text((tx3, ty3),       t1, font=fIB,  fill=C_WHITE)
    d.text((tx3, ty3+t1h+3), t2, font=fIBs, fill=(*C_MUTED, 200))


# ════════════════════════════════════════════════════════════════════
# 5. CTA BAR  (1110 → 1288)
# ════════════════════════════════════════════════════════════════════
d.rectangle([0, Y_CTA, W, Y_FOOT], fill=(*C_RED, 255))
d.rectangle([0, Y_CTA, W, Y_CTA+3], fill=(255, 255, 255, 30))

fCtH = ImageFont.truetype(F_GB, 40)
fCtS = ImageFont.truetype(F_GI, 17)
fPh  = ImageFont.truetype(F_GB, 28)
fBtn = ImageFont.truetype(F_GB, 18)

cy2 = Y_CTA + 16

cta_txt = "Get Your Free Quote Today"
ctw, cth = tbbox(fCtH, cta_txt)
shadow_text(d, ((W-ctw)//2, cy2), cta_txt, fCtH, C_WHITE, sdist=2, sop=80)
cy2 += cth + 6

sub_txt = "No obligation  ·  Government rebates applied  ·  Professional installation"
stw, sth = tbbox(fCtS, sub_txt)
d.text(((W-stw)//2, cy2), sub_txt, font=fCtS, fill=(*C_WHITE, 185))
cy2 += sth + 12

ph_txt = "0414 146 027"
phw, phh = tbbox(fPh, ph_txt)
d.text(((W-phw)//2, cy2), ph_txt, font=fPh, fill=C_CREAM)
cy2 += phh + 12

btn_txt = "GET A FREE QUOTE NOW →"
btw, bth = tbbox(fBtn, btn_txt)
bpx2 = 34
bx1_b = (W - btw - bpx2*2) // 2
d.rounded_rectangle([bx1_b, cy2, bx1_b+btw+bpx2*2, cy2+bth+18], radius=26, fill=C_CREAM)
d.text((bx1_b+bpx2, cy2+9), btn_txt, font=fBtn, fill=C_RED)


# ════════════════════════════════════════════════════════════════════
# 6. FOOTER  (1288 → 1350)
# ════════════════════════════════════════════════════════════════════
d.rectangle([0, Y_FOOT, W, H], fill=(8, 10, 16, 255))
d.rectangle([0, Y_FOOT, W, Y_FOOT+2], fill=(*C_RED, 100))

logo2 = load_logo(38)
lx2 = (W - logo2.width) // 2
ly2 = Y_FOOT + 12
canvas.alpha_composite(logo2, dest=(lx2, ly2))
d = ImageDraw.Draw(canvas)

fURL = ImageFont.truetype(F_HV, 13)
url_txt = "helioflo.com.au   ·   0414 146 027   ·   Sydney, NSW"
uw, uh = tbbox(fURL, url_txt)
d.text(((W-uw)//2, ly2+38+6), url_txt, font=fURL, fill=(*C_MUTED, 175))


# ── Save ─────────────────────────────────────────────────────────────
canvas.convert('RGB').save(OUT, 'PNG', optimize=True)
print(f'Saved → {OUT}')
