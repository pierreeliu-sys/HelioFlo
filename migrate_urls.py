#!/usr/bin/env python3
"""
Migrate all pages to clean URL folder structure and fix all internal links.
- payment.html      → payment/index.html
- privacy.html      → privacy/index.html
- complaints.html   → complaints/index.html
- Product Pages/basic-batteries.html      → basic-batteries/index.html
- Product Pages/recommended-batteries.html → recommended-batteries/index.html
- Product Pages/premium-batteries.html    → premium-batteries/index.html
- Product Pages/solar-inverters.html      → solar-inverters/index.html
Also patches index.html links in place.
"""
import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))


def rpath(*parts):
    return os.path.join(BASE, *parts)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Replacement tables ────────────────────────────────────────────────────────

# Applied to root-level pages moving INTO a subfolder (payment, privacy, complaints)
ROOT_TO_SUB = [
    # assets — prepend ../
    ('href="styles.css"',           'href="../styles.css"'),
    ('href="favicon.svg"',          'href="../brand_assets/favicon.svg"'),
    ('src="brand_assets/',          'src="../brand_assets/'),
    ('href="brand_assets/',         'href="../brand_assets/'),
    ('src="Accreditation/',         'src="../Accreditation/'),
    ('href="Accreditation/',        'href="../Accreditation/'),
    # internal page links → clean absolute URLs
    ('href="index.html#why"',       'href="/#why"'),
    ('href="index.html#products"',  'href="/#products"'),
    ('href="index.html#process"',   'href="/#process"'),
    ('href="index.html#contact"',   'href="/#contact"'),
    ('href="index.html#faq"',       'href="/#faq"'),
    ('href="index.html#services"',  'href="/#contact"'),
    ('href="index.html"',           'href="/"'),
    ('href="payment.html"',         'href="/payment"'),
    ('href="privacy.html"',         'href="/privacy"'),
    ('href="complaints.html"',      'href="/complaints"'),
]

# Applied to Product Pages moving to root-level subfolders (same ../ depth)
PRODUCT_PAGE = [
    # internal page links
    ('href="../index.html#why"',      'href="/#why"'),
    ('href="../index.html#products"', 'href="/#products"'),
    ('href="../index.html#process"',  'href="/#process"'),
    ('href="../index.html#contact"',  'href="/#contact"'),
    ('href="../index.html#faq"',      'href="/#faq"'),
    ('href="../index.html"',          'href="/"'),
    ('href="../payment.html"',        'href="/payment"'),
    ('href="../privacy.html"',        'href="/privacy"'),
    ('href="../complaints.html"',     'href="/complaints"'),
    # cross-links between product pages
    ('href="basic-batteries.html"',        'href="/basic-batteries"'),
    ('href="recommended-batteries.html"',  'href="/recommended-batteries"'),
    ('href="premium-batteries.html"',      'href="/premium-batteries"'),
    ('href="solar-inverters.html"',        'href="/solar-inverters"'),
]

# Applied to index.html in place
INDEX_FIXES = [
    ('href="payment.html"',                               'href="/payment"'),
    ('href="privacy.html"',                               'href="/privacy"'),
    ('href="complaints.html"',                            'href="/complaints"'),
    ('href="Product Pages/basic-batteries.html"',         'href="/basic-batteries"'),
    ('href="Product Pages/recommended-batteries.html"',   'href="/recommended-batteries"'),
    ('href="Product Pages/premium-batteries.html"',       'href="/premium-batteries"'),
    ('href="Product Pages/solar-inverters.html"',         'href="/solar-inverters"'),
]


def apply(content, rules):
    for old, new in rules:
        content = content.replace(old, new)
    return content


# ── Migrate root pages to subfolders ─────────────────────────────────────────

for fname, folder in [
    ("payment.html",    "payment"),
    ("privacy.html",    "privacy"),
    ("complaints.html", "complaints"),
]:
    src  = rpath(fname)
    dest = rpath(folder, "index.html")
    html = read(src)
    html = apply(html, ROOT_TO_SUB)
    write(dest, html)
    os.remove(src)
    print(f"  {fname} → {folder}/index.html")


# ── Migrate Product Pages to root-level subfolders ───────────────────────────

product_map = {
    "basic-batteries.html":        "basic-batteries",
    "recommended-batteries.html":  "recommended-batteries",
    "premium-batteries.html":      "premium-batteries",
    "solar-inverters.html":        "solar-inverters",
}

for fname, folder in product_map.items():
    src  = rpath("Product Pages", fname)
    dest = rpath(folder, "index.html")
    html = read(src)
    html = apply(html, PRODUCT_PAGE)
    write(dest, html)
    os.remove(src)
    print(f"  Product Pages/{fname} → {folder}/index.html")

# Remove Product Pages folder if empty
pp = rpath("Product Pages")
if os.path.isdir(pp) and not any(
    f for f in os.listdir(pp) if not f.startswith(".")
):
    shutil.rmtree(pp)
    print("  Removed empty 'Product Pages/' folder")

# ── Patch index.html in place ────────────────────────────────────────────────

idx = rpath("index.html")
html = read(idx)
html = apply(html, INDEX_FIXES)
write(idx, html)
print("  index.html links patched")

print("\nDone. All pages migrated to clean URL structure.")
