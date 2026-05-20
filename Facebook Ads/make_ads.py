#!/usr/bin/env python3
"""
HelioFlo Facebook Ad Generator
1080×1080 ads for Essential, Mid-Market, and Premium battery ranges.
Brand: Uluru Red #B5451B · Spinifex Gold #D4A847 · Electric Teal #00C9A7
Typography: Georgia (headlines) · Helvetica (body/UI)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

# ── Canvas ──────────────────────────────────────────────────────────
W, H = 1080, 1080

# ── Brand colours ────────────────────────────────────────────────────
C_RED   = (220,  38,  38)   # Essential accent
C_TEAL  = (  0, 201, 167)   # Mid-Market accent  (Electric Teal)
C_GOLD  = (212, 168,  71)   # Premium accent     (Spinifex Gold)
C_WHITE = (255, 255, 255)
C_DARK  = ( 10,  12,  18)
C_MUTED = (155, 163, 178)

# ── Font paths ───────────────────────────────────────────────────────
F_GB  = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
F_GBI = '/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf'
F_GI  = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
F_HV  = '/System/Library/Fonts/Helvetica.ttc'

BASE = '/Users/pierreliu/HelioFlo'
OUT  = os.path.join(BASE, 'Facebook Ads')


# ── Helpers ──────────────────────────────────────────────────────────

def tbbox(font, text):
    """Return (w, h) of rendered text using font metrics (no Draw needed)."""
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]

def shadow(draw, xy, text, font, fill, sdist=2, sop=180):
    x, y = xy
    draw.text((x+sdist, y+sdist), text, font=font, fill=(*C_DARK[:3], sop))
    draw.text(xy, text, font=font, fill=fill)

def rr(draw, xy, rad, fill=None, outline=None, ow=2):
    draw.rounded_rectangle(xy, radius=rad, fill=fill, outline=outline, width=ow)

def remove_white(img, thr=245):
    img = img.convert('RGBA')
    d   = list(img.getdata())
    img.putdata([(r,g,b,0) if r>=thr and g>=thr and b>=thr else (r,g,b,a) for r,g,b,a in d])
    return img

def fit(img, bw, bh, pad=20):
    iw, ih = img.size
    s  = min((bw-pad*2)/iw, (bh-pad*2)/ih)
    return img.resize((int(iw*s), int(ih*s)), Image.LANCZOS)

def prep_bg():
    bg = Image.open(f'{BASE}/Facebook Ads/Stock Photos/Solar Panel Home 3.jpg').convert('RGB')
    w, h = bg.size
    s    = min(w, h)
    bg   = bg.crop(((w-s)//2,(h-s)//2,(w+s)//2,(h+s)//2)).resize((W,H), Image.LANCZOS)
    bg   = bg.filter(ImageFilter.GaussianBlur(radius=9))
    bg   = ImageEnhance.Brightness(bg).enhance(0.28)
    return bg.convert('RGBA')

def load_logo(height=58):
    logo = Image.open(f'{BASE}/brand_assets/HelioFlo_Logo.PNG').convert('RGBA')
    lw   = int(height * logo.width / logo.height)
    return logo.resize((lw, height), Image.LANCZOS)

def left_vignette(w, h):
    """Dark-left → transparent-right gradient panel for text legibility."""
    layer = Image.new('RGBA', (w, h), (0,0,0,0))
    d     = ImageDraw.Draw(layer)
    for x in range(w):
        a = int(215 * max(0, 1-(x/(w*0.80))**1.9))
        d.line([(x,0),(x,h)], fill=(*C_DARK, a))
    return layer

def draw_tick(draw, cx, cy, r, color):
    """Filled circle with a white tick."""
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, 215))
    lw = max(2, r//3)
    draw.line([(cx-r//2+1, cy+1), (cx-r//7, cy+r//2)], fill=C_WHITE, width=lw)
    draw.line([(cx-r//7,   cy+r//2), (cx+r//2-1, cy-r//2+1)], fill=C_WHITE, width=lw)

# ── Core render ──────────────────────────────────────────────────────

def make_ad(tier, accent, h1, h2, tagline, feats, prod_paths, outfile):
    canvas = prep_bg()

    # Section heights
    HDR   = 108          # header bar
    BAR   =  16          # accent stripe
    BOT_S = H - 108 - 228   # bottom of content = 744
    STRIP = 108          # trust strip
    CTA   = 228          # cta bar
    # Content 124 → 744 = 620px tall

    CONTENT_TOP = HDR + BAR          # 124
    CONTENT_BOT = BOT_S              # 744
    CONT_H      = CONTENT_BOT - CONTENT_TOP   # 620
    LEFT_W      = 548                # left text column

    # ── Header ──────────────────────────────────────────
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, W, HDR], fill=(*C_DARK, 228))

    canvas.alpha_composite(load_logo(58), dest=(38, 25))

    # Badge
    fb   = ImageFont.truetype(F_HV, 15)
    btxt = "GOVERNMENT REBATE ELIGIBLE"
    bw, bh = tbbox(fb, btxt)
    px, py = 20, 6
    bx1 = W - bw - px*2 - 34
    bry = 32
    rr(d, [bx1, bry, bx1+bw+px*2, bry+bh+py*2], rad=14, fill=(*accent, 230))
    d.text((bx1+px, bry+py), btxt, font=fb, fill=C_WHITE)

    # ── Accent stripe ────────────────────────────────────
    d.rectangle([0, HDR, W, HDR+BAR], fill=(*accent, 255))

    # ── Left text panel ──────────────────────────────────
    canvas.alpha_composite(left_vignette(LEFT_W, CONT_H), dest=(0, CONTENT_TOP))
    d = ImageDraw.Draw(canvas)

    # Fonts
    fTr  = ImageFont.truetype(F_HV,  18)
    fH1  = ImageFont.truetype(F_GB,  58)
    fH2  = ImageFont.truetype(F_GBI, 65)
    fTag = ImageFont.truetype(F_GI,  23)
    fFt  = ImageFont.truetype(F_HV,  21)
    fSt  = ImageFont.truetype(F_HV,  16)
    fCtH = ImageFont.truetype(F_GB,  44)
    fBtn = ImageFont.truetype(F_HV,  23)
    fURL = ImageFont.truetype(F_HV,  17)

    mx = 46
    my = CONTENT_TOP + 34

    # Tier label
    draw_tick(d, mx+7, my+8, 8, accent)
    d.text((mx+22, my), tier.upper(), font=fTr, fill=(*accent, 255))
    _, trh = tbbox(fTr, tier)
    my += trh + 14

    # Thin accent rule
    d.rectangle([mx, my, mx+68, my+3], fill=(*accent, 210))
    my += 16

    # Headline
    shadow(d, (mx, my), h1, fH1, C_WHITE)
    _, h1h = tbbox(fH1, h1)
    my += h1h + 2

    shadow(d, (mx, my), h2, fH2, accent)
    _, h2h = tbbox(fH2, h2)
    my += h2h + 18

    # Tagline
    d.text((mx, my), tagline, font=fTag, fill=(*C_MUTED, 215))
    _, tgh = tbbox(fTag, tagline)
    my += tgh + 24

    # Divider rule
    d.rectangle([mx, my, mx+210, my+1], fill=(255,255,255,45))
    my += 16

    # Feature list
    for feat in feats:
        draw_tick(d, mx+9, my+10, 9, accent)
        d.text((mx+26, my), feat, font=fFt, fill=(*C_WHITE, 235))
        _, fh = tbbox(fFt, feat)
        my += fh + 12

    # ── Right product panel ──────────────────────────────
    rp_x = LEFT_W
    rp_w = W - LEFT_W
    n    = len(prod_paths)

    for i, pp in enumerate(prod_paths):
        slot_y = CONTENT_TOP + i * (CONT_H // n)
        slot_h = CONT_H // n

        pimg = Image.open(pp).convert('RGBA')
        # Remove white/near-white background
        pimg = remove_white(pimg, thr=246)

        pimg = fit(pimg, rp_w, slot_h, pad=28)
        dx = rp_x + (rp_w - pimg.width)  // 2
        dy = slot_y + (slot_h - pimg.height) // 2
        canvas.alpha_composite(pimg, dest=(dx, dy))

    d = ImageDraw.Draw(canvas)

    # Vertical separator between columns
    d.line([(LEFT_W, CONTENT_TOP+20), (LEFT_W, CONTENT_BOT-20)],
           fill=(255,255,255,25), width=1)

    # ── Trust strip ──────────────────────────────────────
    st = CONTENT_BOT
    d.rectangle([0, st, W, st+STRIP], fill=(*C_DARK, 242))
    d.rectangle([0, st, W, st+2],     fill=(*accent, 160))

    sigs = [("SAA Accredited", "Licensed Installer"),
            ("Federal Rebate", "Handled End-to-End"),
            ("5-Year Warranty", "Workmanship Guaranteed")]
    col  = W // 3
    for i, (s1, s2) in enumerate(sigs):
        cx  = i*col + col//2
        s1w, _ = tbbox(fFt, s1)
        s2w, _ = tbbox(fSt, s2)
        d.text((cx-s1w//2, st+14), s1, font=fFt, fill=C_WHITE)
        d.text((cx-s2w//2, st+44), s2, font=fSt, fill=(*C_MUTED, 190))
        if i < 2:
            d.line([(i+1)*col, st+14, (i+1)*col, st+STRIP-14],
                   fill=(255,255,255,30))

    # ── CTA bar ──────────────────────────────────────────
    ct = st + STRIP
    d.rectangle([0, ct, W, H], fill=(7, 9, 15, 255))
    d.rectangle([0, ct, W, ct+3], fill=(*accent, 255))

    # Headline
    ctxt = "Get a Free Quote Today"
    ctw, _ = tbbox(fCtH, ctxt)
    shadow(d, ((W-ctw)//2, ct+22), ctxt, fCtH, C_WHITE, sdist=2)

    # Phone button
    btn = "0414 146 027"
    bw, bh = tbbox(fBtn, btn)
    bpad = 36
    bx1  = (W - bw - bpad*2) // 2
    by1  = ct + 90
    rr(d, [bx1, by1, bx1+bw+bpad*2, by1+bh+24], rad=28, fill=(*accent, 255))
    d.text((bx1+bpad, by1+12), btn, font=fBtn, fill=C_WHITE)

    # Sub-line
    sub  = "helioflo.com.au   ·   Servicing Sydney, NSW"
    subw, _ = tbbox(fURL, sub)
    d.text(((W-subw)//2, by1+bh+48), sub, font=fURL, fill=(*C_MUTED, 155))

    # Save
    canvas.convert('RGB').save(outfile, 'PNG', optimize=True)
    print(f'  saved → {os.path.basename(outfile)}')


# ── Tier definitions ─────────────────────────────────────────────────

TIERS = [
    dict(
        tier    = 'Essential Range',
        accent  = C_RED,
        h1      = 'Start Storing',
        h2      = 'Solar Energy.',
        tagline = 'Entry-level LiFePO4 storage for every home.',
        feats   = ['LiFePO4 Battery Chemistry',
                   'Single-Phase Blackout Backup',
                   'Expandable — Up to 50 Units'],
        prods   = [f'{BASE}/Solis/Solis Dyness Battery Image.jpg',
                   f'{BASE}/Solis/Solis Inverter Image.webp'],
        out     = f'{OUT}/HelioFlo Ad — Essential Range.png',
    ),
    dict(
        tier    = 'Mid-Market Range',
        accent  = C_TEAL,
        h1      = 'Whole-Home',
        h2      = 'Three-Phase Backup.',
        tagline = 'All-in-one integrated system for three-phase homes.',
        feats   = ['All-in-One Inverter & Battery',
                   'Three-Phase Whole-Home Support',
                   "10-Year Manufacturer's Warranty"],
        prods   = [f'{BASE}/Swatten/ Product Image All-in-One System Three Phase (HV) (10-20) kW.png'],
        out     = f'{OUT}/HelioFlo Ad — Mid-Market Range.png',
    ),
    dict(
        tier    = 'Premium Range',
        accent  = C_GOLD,
        h1      = 'Maximum Energy',
        h2      = 'Independence.',
        tagline = 'For large homes, EV owners & high-demand properties.',
        feats   = ['Three-Phase Blackout Backup',
                   'Smart EV-Ready & App Control',
                   'Modular Expandable Capacity'],
        prods   = [f'{BASE}/EcoFlow/Product Image PO.png'],
        out     = f'{OUT}/HelioFlo Ad — Premium Range.png',
    ),
]

print('Generating HelioFlo Facebook Ads...')
for t in TIERS:
    print(f'\n  [{t["tier"]}]')
    make_ad(t['tier'], t['accent'], t['h1'], t['h2'],
            t['tagline'], t['feats'], t['prods'], t['out'])
print('\nDone.')
