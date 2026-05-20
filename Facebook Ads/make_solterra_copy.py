#!/usr/bin/env python3
"""
HelioFlo Facebook Ad — Solterra-Style (Design System v2)
Applies: 8px grid, negative tracking on display text, pill CTA button,
single-accent discipline, surface-ladder for card tints.
1080 × 1350 px  |  Meta Feed 4:5
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, textwrap

W, H = 1080, 1350

# ── Brand colours ─────────────────────────────────────────────────────
C_RED   = (181,  69,  27)   # Uluru Red — THE single accent (CTA only)
C_TEAL  = (  0, 201, 167)   # Electric Teal — Mid-Market tier only
C_GOLD  = (212, 168,  71)   # Spinifex Gold — Premium tier only
C_WHITE = (255, 255, 255)
C_DARK  = ( 20,  16,  26)   # Near-black (#14101A)
C_BODY  = ( 60,  56,  66)   # Body text
C_MUTED = (140, 135, 125)   # Secondary / muted text
C_CREAM = (255, 252, 247)   # Surface level 0 (canvas)

# Card header bars — deeper, distinct from accent
HDR_RED  = (145,  42,  14)
HDR_TEAL = (  0, 115,  95)
HDR_GOLD = (138,  90,   8)

# Card content tints — surface ladder Level 1 (very pale)
TINT_RED  = (255, 246, 242)
TINT_TEAL = (240, 255, 252)
TINT_GOLD = (255, 253, 238)

# Info box backgrounds (dark, distinct per personality)
IB = [(0, 92, 76), (26, 30, 20), (96, 66, 8), (136, 20, 8)]

F_GB = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
F_GI = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
F_HV = '/System/Library/Fonts/Helvetica.ttc'

BASE = '/Users/pierreliu/HelioFlo'
OUT  = os.path.join(BASE, 'Facebook Ads', 'HelioFlo Ad — Solterra Style.png')

# ── Section heights (8px grid) ────────────────────────────────────────
HERO_H = 480   # ÷8 = 60 ✓
BAND_H =  48   # ÷8 =  6 ✓
CARD_H = 344   # ÷8 = 43 ✓
INFO_H = 288   # ÷8 = 36 ✓
CTA_H  =  80   # ÷8 = 10 ✓
FOOT_H = 110   # remainder (1350 is not ÷8)
# 480+48+344+288+80+110 = 1350 ✓

Y_BAND  = HERO_H
Y_CARDS = Y_BAND  + BAND_H    # 528
Y_INFO  = Y_CARDS + CARD_H    # 872
Y_CTA   = Y_INFO  + INFO_H    # 1160
Y_FOOT  = Y_CTA   + CTA_H     # 1240

# ── Spacing tokens — 8px base grid ───────────────────────────────────
SP = {'xs': 4, 'sm': 8, 'md': 16, 'lg': 24, 'xl': 32, 'xxl': 48}


def tbbox(font, text):
    bb = font.getbbox(text)
    return bb[2]-bb[0], bb[3]-bb[1]


def remove_white(img, thr=232):
    img = img.convert('RGBA')
    d   = list(img.getdata())
    img.putdata([(r,g,b,0) if r>=thr and g>=thr and b>=thr else (r,g,b,a)
                 for r,g,b,a in d])
    return img


def fit_into(img, bw, bh, pad=8):
    iw, ih = img.size
    s = min((bw-pad*2)/iw, (bh-pad*2)/ih)
    return img.resize((int(iw*s), int(ih*s)), Image.LANCZOS)


def load_logo(h=52):
    logo = Image.open(f'{BASE}/brand_assets/HelioFlo_Logo.PNG').convert('RGBA')
    w = int(h * logo.width / logo.height)
    return logo.resize((w, h), Image.LANCZOS)


def tracked_text(draw, x, y, text, font, fill, tracking=-2):
    """Negative letter-spacing via char-by-char rendering (size × −0.04)."""
    cx = x
    for char in text:
        draw.text((cx, y), char, font=font, fill=fill)
        w, _ = tbbox(font, char)
        cx += w + tracking
    return cx - x  # total rendered width


def pill_button(draw, cx, cy, text, font, bg, fg, pad_h=12, pad_v=32):
    """Draw a horizontally centered pill button. Returns bounding box."""
    tw, th = tbbox(font, text)
    bw = tw + pad_v * 2
    bh = th + pad_h * 2
    x1 = cx - bw // 2
    y1 = cy - bh // 2
    draw.rounded_rectangle([x1, y1, x1+bw, y1+bh], radius=9999, fill=bg)
    draw.text((x1 + pad_v, y1 + pad_h), text, font=font, fill=fg)
    return x1, y1, x1+bw, y1+bh


def tick_circle(draw, cx, cy, r, color):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, 255))
    lw = max(2, r//3)
    draw.line([(cx-r//2+1, cy+1), (cx-r//7, cy+r//2)], fill=C_WHITE, width=lw)
    draw.line([(cx-r//7, cy+r//2), (cx+r//2-1, cy-r//2+2)], fill=C_WHITE, width=lw)


def draw_badge_circle(draw, cx, cy, r, bg_col, lines, line_font):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*bg_col, 230))
    draw.ellipse([cx-r+4, cy-r+4, cx+r-4, cy+r-4],
                 fill=(0,0,0,0), outline=(255,255,255,80), width=1)
    total_h = sum(tbbox(line_font, l)[1] for l in lines) + 2*(len(lines)-1)
    y0 = cy - total_h//2
    for l in lines:
        lw, lh = tbbox(line_font, l)
        draw.text((cx-lw//2, y0), l, font=line_font, fill=C_WHITE)
        y0 += lh + 2


# ═══════════════════════════════════════════════════════════════════
# 1. HERO  (0 → 480)
# ═══════════════════════════════════════════════════════════════════
canvas = Image.new('RGBA', (W, H), C_CREAM)

# Photo — scale to full width, center-crop to HERO_H
bg = Image.open(f'{BASE}/Facebook Ads/Stock Photos/Solar Panel Home 3.jpg').convert('RGB')
bw0, bh0 = bg.size
bg = bg.resize((W, int(bh0*W/bw0)), Image.LANCZOS)
oy = (bg.height - HERO_H) // 2
bg = bg.crop((0, oy, W, oy+HERO_H))
bg = ImageEnhance.Brightness(bg).enhance(0.88)
bg = ImageEnhance.Color(bg).enhance(1.10)
canvas.alpha_composite(bg.convert('RGBA'), dest=(0, 0))

# Cream gradient overlay — left two-thirds for text legibility
ov = Image.new('RGBA', (W, HERO_H), (0,0,0,0))
ovd = ImageDraw.Draw(ov)
for x in range(W):
    t = x / W
    a = int(242 * max(0, 1 - (t/0.52)**2.0))
    ovd.line([(x,0),(x,HERO_H)], fill=(*C_CREAM, a))
canvas.alpha_composite(ov, dest=(0,0))

d = ImageDraw.Draw(canvas)

# 4px brand-red accent stripe at very top
d.rectangle([0, 0, W, 4], fill=(*C_RED, 255))

# HelioFlo logo — 24px from left (8px grid: SP['lg'])
logo = load_logo(48)
canvas.alpha_composite(logo, dest=(SP['lg'], SP['md']))
d = ImageDraw.Draw(canvas)

# ── Fonts: three weights only (400 / 600 — no 500) ───────────────
fEye = ImageFont.truetype(F_HV,  16)   # 400 weight eyebrow
fH1  = ImageFont.truetype(F_GB,  56)   # 600 weight display, 56px
fBod = ImageFont.truetype(F_HV,  18)   # 400 weight body, 18px
fAcc = ImageFont.truetype(F_GI,  16)   # italic accent

TRACK_H1 = -2   # 56px × −0.04 = −2.24 → −2px per character gap

tx = SP['lg']   # 24px left margin
ty = 80

# Eyebrow (400 weight, no tracking at 16px)
ey_txt = "GOING SOLAR IN 2025?"
d.text((tx, ty), ey_txt, font=fEye, fill=C_BODY)
_, eyh = tbbox(fEye, ey_txt)
ty += eyh + SP['sm']   # 8px gap

# Display headline — negative tracking, 1.10 line-height (display tight)
for line, col in [("POWER YOUR HOME", C_DARK),
                  ("WITH SOLAR", C_DARK),
                  ("BATTERY STORAGE", C_RED)]:
    tracked_text(d, tx, ty, line, fH1, col, tracking=TRACK_H1)
    _, lh = tbbox(fH1, line)
    ty += int(lh * 1.10)

# Red accent dash separator
ty += SP['sm']
d.rectangle([tx, ty, tx+40, ty+4], fill=(*C_RED, 200))
ty += SP['md']   # 16px

# Body copy — 18px, 26px line-height (≈1.44), ≤55 chars/line
body_lines = textwrap.fill(
    "Take control of rising energy costs with HelioFlo's "
    "premium solar battery systems — safe, efficient, "
    "and built to save you more.",
    width=40
).split('\n')

for bl in body_lines:
    d.text((tx, ty), bl, font=fBod, fill=C_BODY)
    ty += 26   # 26px line-height (nearest even number to 18×1.44=25.9)

# Italic note — accent red, subdued alpha
ty += SP['xs']
d.text((tx, ty), "  — stable, efficient, affordable", font=fAcc,
       fill=(*C_RED, 185))

# ── Two hero product images — right of frame ──────────────────────
hero_prods = [
    (f'{BASE}/Solis/Solis Inverter Image.webp',       "ALL-IN-ONE"),
    (f'{BASE}/Solis/Solis Dyness Battery Image.jpg',  "BATTERY"),
]
px0    = 560
prod_w = (W - px0) // 2   # ≈260 px each
fPL    = ImageFont.truetype(F_HV, 13)
zh_prod = HERO_H - SP['xxl']   # 432px product zone height

for i, (pp, lbl) in enumerate(hero_prods):
    zx = px0 + i * prod_w
    try:
        pi = Image.open(pp).convert('RGBA')
        pi = remove_white(pi, thr=228)
        pi = fit_into(pi, prod_w, zh_prod, pad=SP['md'])
        canvas.alpha_composite(pi, dest=(int(zx+(prod_w-pi.width)//2),
                                         int(SP['sm']+(zh_prod-pi.height)//2)))
        d = ImageDraw.Draw(canvas)
    except Exception as e:
        print(f"  [warn] hero prod {i}: {e}")

    lw2, _ = tbbox(fPL, lbl)
    d.text((zx+(prod_w-lw2)//2, HERO_H-SP['xl']), lbl, font=fPL, fill=C_BODY)

# Subtle divider between the two products
d.line([(px0+prod_w, SP['md']), (px0+prod_w, HERO_H-SP['xxl'])],
        fill=(*C_MUTED, 40))


# ═══════════════════════════════════════════════════════════════════
# 2. TIER BANNER  (480 → 528)
# ═══════════════════════════════════════════════════════════════════
d.rectangle([0, Y_BAND, W, Y_CARDS], fill=(*C_DARK, 255))

fBand = ImageFont.truetype(F_GB, 20)
band_txt = "CHOOSE THE BATTERY SYSTEM THAT FITS YOUR HOME"
bw2, bh2 = tbbox(fBand, band_txt)

# Red dot prefix (single accent)
icon_r  = 6
icon_cx = (W - bw2) // 2 - icon_r - SP['sm']
icon_cy = Y_BAND + BAND_H // 2
d.ellipse([icon_cx-icon_r, icon_cy-icon_r, icon_cx+icon_r, icon_cy+icon_r],
          fill=(*C_RED, 255))
d.text(((W-bw2)//2, Y_BAND+(BAND_H-bh2)//2), band_txt, font=fBand, fill=C_WHITE)


# ═══════════════════════════════════════════════════════════════════
# 3. TIER CARDS  (528 → 872)  — 3 × 360 px wide
# ═══════════════════════════════════════════════════════════════════
CARD_W  = W // 3    # 360
HDR_H   = 56        # 56÷8=7 ✓
TEXT_W  = 176       # left text column per card
IMG_COL = CARD_W - TEXT_W   # 184px right column

TIERS = [
    dict(
        hdr=HDR_RED,  tint=TINT_RED,  acc=C_RED,
        name="ESSENTIAL",
        price="$4,990",
        ph="Single Phase",
        cap="5–10 kWh Battery",
        feats=["Ideal for single-phase homes",
               "Reliable blackout backup",
               "Expandable capacity"],
        img=f'{BASE}/Solis/Solis Dyness Battery Image.jpg',
    ),
    dict(
        hdr=HDR_TEAL, tint=TINT_TEAL, acc=C_TEAL,
        name="MID-MARKET",
        price="$9,990",
        ph="Three Phase",
        cap="10–20 kWh Battery",
        feats=["More power for growing homes",
               "Whole-home backup power",
               "Best performance & value"],
        img=f'{BASE}/Swatten/ Product Image All-in-One System Three Phase (HV) (10-20) kW.png',
    ),
    dict(
        hdr=HDR_GOLD, tint=TINT_GOLD, acc=C_GOLD,
        name="PREMIUM",
        price="$14,990",
        ph="Three Phase",
        cap="20–30 kWh Battery",
        feats=["Full energy independence",
               "Ideal for high-demand homes",
               "EV-ready charging"],
        img=f'{BASE}/EcoFlow/Product Image PO.png',
    ),
]

fCN  = ImageFont.truetype(F_GB,  20)  # tier name header (600 weight)
fCPr = ImageFont.truetype(F_GB,  48)  # price (600 weight, 48px ÷8=6 ✓)
fCSp = ImageFont.truetype(F_HV,  14)  # phase spec (400 weight)
fCCp = ImageFont.truetype(F_GB,  14)  # capacity accent (600 weight)
fCFt = ImageFont.truetype(F_HV,  13)  # feature bullets (400 weight)

for i, td in enumerate(TIERS):
    cx1 = i * CARD_W
    cx2 = cx1 + CARD_W
    acc = td['acc']

    # Hairline card divider
    if i > 0:
        d.line([(cx1, Y_CARDS), (cx1, Y_INFO)], fill=(200, 195, 190, 255))

    # Coloured header bar
    d.rectangle([cx1, Y_CARDS, cx2, Y_CARDS+HDR_H], fill=(*td['hdr'], 255))
    nw, nh = tbbox(fCN, td['name'])
    d.text((cx1+(CARD_W-nw)//2, Y_CARDS+(HDR_H-nh)//2),
           td['name'], font=fCN, fill=C_WHITE)

    # Pale tint content background (surface ladder — no harsh dark)
    d.rectangle([cx1, Y_CARDS+HDR_H, cx2, Y_INFO], fill=(*td['tint'], 255))

    # ── Left text column — 16px padding (8px grid) ───────────────
    cy = Y_CARDS + HDR_H + SP['md']   # 16px top
    lx = cx1 + SP['md']               # 16px left

    # Price — 48px, 600 weight
    _, ph2 = tbbox(fCPr, td['price'])
    d.text((lx, cy), td['price'], font=fCPr, fill=C_DARK)
    cy += ph2 + SP['xs']   # 4px

    # Phase spec
    d.text((lx, cy), td['ph'], font=fCSp, fill=C_BODY)
    _, sph = tbbox(fCSp, td['ph'])
    cy += sph + SP['xs']   # 4px

    # Capacity — tier accent colour
    d.text((lx, cy), td['cap'], font=fCCp, fill=(*acc, 255))
    _, cph = tbbox(fCCp, td['cap'])
    cy += cph + SP['sm']   # 8px

    # 1px accent hairline rule
    d.rectangle([lx, cy, lx+TEXT_W-SP['md'], cy+1], fill=(*acc, 100))
    cy += SP['sm']   # 8px

    # Feature bullets — 8px item gap
    for feat in td['feats']:
        tick_circle(d, lx+6, cy+7, 5, acc)
        d.text((lx+SP['md'], cy), feat, font=fCFt, fill=C_DARK)
        _, fh = tbbox(fCFt, feat)
        cy += fh + SP['sm']

    # ── Right product image column ────────────────────────────────
    img_x1 = cx1 + TEXT_W
    img_x2 = cx2
    img_y1 = Y_CARDS + HDR_H + SP['sm']
    img_y2 = Y_INFO  - SP['sm']
    iw2 = img_x2 - img_x1
    ih2 = img_y2 - img_y1

    try:
        pi = Image.open(td['img']).convert('RGBA')
        pi = remove_white(pi, thr=230)
        pi = fit_into(pi, iw2, ih2, pad=SP['sm'])
        canvas.alpha_composite(pi, dest=(int(img_x1+(iw2-pi.width)//2),
                                          int(img_y1+(ih2-pi.height)//2)))
        d = ImageDraw.Draw(canvas)
    except Exception as e:
        print(f"  [warn] card img {i}: {e}")


# ═══════════════════════════════════════════════════════════════════
# 4. INFO BOXES  (872 → 1160)  — 4 × 270 px
# ═══════════════════════════════════════════════════════════════════
BOX_W = W // 4   # 270

fIH  = ImageFont.truetype(F_GB,  14)  # box header (600)
fIP  = ImageFont.truetype(F_HV,  13)  # body paragraph (400)
fIB  = ImageFont.truetype(F_GB,  13)  # bold bullet label (600)
fIBd = ImageFont.truetype(F_GB,  10)  # badge micro text

BOXES = [
    dict(
        bg=IB[0], acc=C_TEAL,
        header="A TRUSTED CHOICE",
        items=["SAA Accredited Installer",
               "5-Star Customer Reviews",
               "10-Year Workmanship Warranty",
               "Federal Rebates Handled",
               "Reliable Backup Power"],
        badge=["10 YEAR", "WARRANTY"],
    ),
    dict(
        bg=IB[1], acc=C_TEAL,
        header="INSTALLATION NOTE",
        body=("This battery system must be paired\n"
              "with a new or existing solar PV\n"
              "system to ensure optimal\n"
              "performance and energy savings."),
        has_photo=True,
    ),
    dict(
        bg=IB[2], acc=C_GOLD,
        header="BE PREPARED",
        intro="Protect your home from:",
        items=["Power outages & blackouts",
               "Rising electricity bills",
               "Grid instability & uncertainty"],
        footer="Keep your family powered\nwith reliable energy, 24/7.",
    ),
    dict(
        bg=IB[3], acc=C_RED,
        header="DON'T MISS OUT!",
        body=("Government STC rebates are\n"
              "decreasing. Lock in the best\n"
              "rebate rate now and upgrade\n"
              "your home energy system today!"),
        badge=["ACT", "NOW!"],
    ),
]

for i, ib in enumerate(BOXES):
    bx1 = i * BOX_W
    bx2 = bx1 + BOX_W
    acc = ib['acc']

    d.rectangle([bx1, Y_INFO, bx2, Y_CTA], fill=(*ib['bg'], 255))
    if i > 0:
        d.line([(bx1, Y_INFO+SP['sm']), (bx1, Y_CTA-SP['sm'])],
               fill=(255, 255, 255, 18))

    iy = Y_INFO + SP['md']   # 16px top
    ix = bx1 + SP['md']      # 16px left

    # Dot icon + header
    ic_r = 6
    d.ellipse([ix, iy+2, ix+ic_r*2, iy+2+ic_r*2], fill=(*acc, 255))
    _, hh = tbbox(fIH, ib['header'])
    d.text((ix+ic_r*2+SP['sm'], iy), ib['header'], font=fIH, fill=C_WHITE)
    iy += hh + SP['sm']   # 8px

    # 1px accent hairline
    d.rectangle([ix, iy, bx2-SP['md'], iy+1], fill=(*acc, 110))
    iy += SP['sm']   # 8px

    if 'body' in ib:
        for line in ib['body'].split('\n'):
            d.text((ix, iy), line, font=fIP, fill=(*C_WHITE, 210))
            iy += tbbox(fIP, "Ay")[1] + SP['xs']   # 4px tight gap
        iy += SP['sm']

    if 'intro' in ib:
        d.text((ix, iy), ib['intro'], font=fIB, fill=(*C_WHITE, 230))
        iy += tbbox(fIB, ib['intro'])[1] + SP['sm']   # 8px

    if 'items' in ib:
        for item in ib['items']:
            tick_circle(d, ix+5, iy+6, 4, acc)
            d.text((ix+SP['md'], iy), item, font=fIP, fill=(*C_WHITE, 215))
            iy += tbbox(fIP, "Ay")[1] + SP['sm']   # 8px gap
        iy += SP['xs']

    if 'footer' in ib:
        for line in ib['footer'].split('\n'):
            d.text((ix, iy), line, font=fIB, fill=(*C_WHITE, 230))
            iy += tbbox(fIB, "Ay")[1] + SP['xs']

    # Circular badge (box 1 and box 4)
    if 'badge' in ib:
        badge_cx = bx2 - SP['xxl']     # 48px from right edge
        badge_cy = Y_CTA - SP['xxl']   # 48px above CTA bar
        bg_col   = acc if i == 0 else C_RED
        draw_badge_circle(d, badge_cx, badge_cy, 38, bg_col, ib['badge'], fIBd)

    # Small photo inset (box 2 only)
    if ib.get('has_photo'):
        try:
            sp = Image.open(
                f'{BASE}/Facebook Ads/Stock Photos/Solar Panel Home 3.jpg'
            ).convert('RGB')
            sp = ImageEnhance.Brightness(sp).enhance(0.72)
            tw2 = BOX_W - SP['xl']    # 270-32=238px
            th2 = 88                   # 88÷8=11 ✓
            sw2, sh2 = sp.size
            sc = max(tw2/sw2, th2/sh2)
            sp = sp.resize((int(sw2*sc), int(sh2*sc)), Image.LANCZOS)
            sp = sp.crop(((sp.width-tw2)//2, (sp.height-th2)//2,
                           (sp.width+tw2)//2, (sp.height+th2)//2))
            py2 = Y_CTA - th2 - SP['md']   # 16px above CTA
            canvas.alpha_composite(sp.convert('RGBA'), dest=(bx1+SP['md'], py2))
            d = ImageDraw.Draw(canvas)
        except Exception as e:
            print(f"  [warn] info photo: {e}")


# ═══════════════════════════════════════════════════════════════════
# 5. CTA BAR  (1160 → 1240)  — 80px, Uluru Red
# ═══════════════════════════════════════════════════════════════════
d.rectangle([0, Y_CTA, W, Y_FOOT], fill=(*C_RED, 255))

# Primary pill button — white bg, red text (single accent per design system)
fCTA = ImageFont.truetype(F_GB, 20)
cta_txt = "GET YOUR FREE SOLAR QUOTE TODAY  →"
pill_button(d, W//2, Y_CTA + CTA_H//2, cta_txt, fCTA,
            bg=C_WHITE, fg=C_RED, pad_h=12, pad_v=SP['xl'])


# ═══════════════════════════════════════════════════════════════════
# 6. FOOTER  (1240 → 1350)  — near-black
# ═══════════════════════════════════════════════════════════════════
d.rectangle([0, Y_FOOT, W, H], fill=(*C_DARK, 255))
d.rectangle([0, Y_FOOT, W, Y_FOOT+2], fill=(*C_RED, 180))

logo2 = load_logo(40)
ly2   = Y_FOOT + (FOOT_H - logo2.height) // 2
canvas.alpha_composite(logo2, dest=(SP['lg'], ly2))
d = ImageDraw.Draw(canvas)

# Divider after logo — 16px gap on each side
sep_x = SP['lg'] + logo2.width + SP['md']
d.line([(sep_x, Y_FOOT+SP['md']), (sep_x, H-SP['md'])],
        fill=(255, 255, 255, 22))

fFt1 = ImageFont.truetype(F_HV, 13)   # 400 muted label
fFt2 = ImageFont.truetype(F_GB, 28)   # 600 phone number
fFt3 = ImageFont.truetype(F_HV, 15)   # 400 URL

# "Contact HelioFlo | Call / Text" — left section
ct_txt = "Contact HelioFlo   |   Call / Text"
_, cth2 = tbbox(fFt1, ct_txt)
d.text((sep_x+SP['md'], Y_FOOT+(FOOT_H-cth2)//2), ct_txt,
       font=fFt1, fill=(*C_MUTED, 195))

# Phone number — large, centered
ph_txt = "0414 146 027"
phw, phh = tbbox(fFt2, ph_txt)
d.text(((W-phw)//2, Y_FOOT+(FOOT_H-phh)//2), ph_txt, font=fFt2, fill=C_WHITE)

# URL — right aligned, 24px margin
url_txt = "helioflo.com.au"
uw, uh = tbbox(fFt3, url_txt)
d.text((W-uw-SP['lg'], Y_FOOT+(FOOT_H-uh)//2), url_txt,
       font=fFt3, fill=(*C_MUTED, 200))


# ── Save ──────────────────────────────────────────────────────────────
canvas.convert('RGB').save(OUT, 'PNG', optimize=True)
print(f'Saved → {OUT}')
