#!/usr/bin/env python3
"""Generate one quote page per Sydney suburb."""

import os, re

SUBURBS = [
    # Inner Sydney
    "Sydney CBD", "Surry Hills", "Newtown", "Glebe", "Pyrmont", "Ultimo",
    "Redfern", "Chippendale", "Darlinghurst", "Potts Point", "Elizabeth Bay",
    "Woolloomooloo", "Paddington", "Waterloo", "Zetland", "Erskineville",
    "Alexandria", "Beaconsfield", "Rosebery", "Eastlakes", "Mascot",
    "Eveleigh", "Forest Lodge", "Macdonaldtown", "Camperdown",
    # Eastern Suburbs
    "Bondi", "Bondi Beach", "Bondi Junction", "Coogee", "Randwick",
    "Clovelly", "Bronte", "Tamarama", "Rose Bay", "Double Bay", "Edgecliff",
    "Woollahra", "Vaucluse", "Watsons Bay", "Maroubra", "Matraville",
    "Malabar", "Little Bay", "La Perouse", "Kensington", "Kingsford",
    "Botany", "Hillsdale", "Pagewood", "Daceyville", "Banksmeadow",
    "Chifley", "Philip Bay", "Phillip Bay",
    # Inner West
    "Marrickville", "Leichhardt", "Balmain", "Rozelle", "Annandale",
    "Petersham", "Stanmore", "Enmore", "Tempe", "Sydenham", "St Peters",
    "Dulwich Hill", "Summer Hill", "Ashfield", "Croydon", "Burwood",
    "Strathfield", "Homebush", "Homebush West", "Flemington", "Haberfield",
    "Lilyfield", "Balmain East", "Abbotsford", "Five Dock", "Drummoyne",
    "Canada Bay", "Concord", "Concord West", "Rhodes", "Meadowbank",
    "North Strathfield", "Croydon Park",
    # Lower North Shore
    "North Sydney", "Crows Nest", "St Leonards", "Naremburn", "Waverton",
    "Milsons Point", "Neutral Bay", "Kirribilli", "Cremorne",
    "Cremorne Point", "Mosman", "Spit Junction", "Balmoral",
    "McMahons Point", "Lavender Bay", "Blues Point", "Wollstonecraft",
    "Northbridge", "Castlecrag", "Middle Cove", "Castle Cove",
    "Northwood", "Longueville", "Riverview", "Lane Cove West", "Gore Hill",
    # Upper North Shore
    "Chatswood", "Lane Cove", "Willoughby", "Artarmon", "Lindfield",
    "Killara", "Gordon", "Pymble", "Turramurra", "Wahroonga", "Hornsby",
    "Berowra", "Berowra Heights", "Mount Colah", "Mount Kuring-Gai",
    "Asquith", "Waitara", "Thornleigh", "Pennant Hills", "Cherrybrook",
    "Beecroft", "Cheltenham", "Epping", "Eastwood", "Ryde", "Meadowbank",
    "West Ryde", "Ermington", "Shepherds Bay", "Putney", "Hunters Hill",
    "Gladesville", "North Ryde", "Top Ryde", "Marsfield",
    # Northern Beaches
    "Manly", "Fairlight", "Balgowlah", "Balgowlah Heights", "Seaforth",
    "Dee Why", "Brookvale", "Freshwater", "Curl Curl", "Collaroy",
    "Collaroy Plateau", "Narraweena", "Cromer", "Narrabeen",
    "North Narrabeen", "Warriewood", "Mona Vale", "Newport",
    "Newport Beach", "Bilgola", "Bilgola Plateau", "Avalon Beach",
    "Palm Beach", "Bayview", "Church Point", "Terrey Hills",
    "Belrose", "Davidson", "Frenchs Forest", "Allambie Heights",
    "Beacon Hill", "North Manly", "Manly Vale", "Forestville",
    "Killarney Heights", "Oxford Falls", "Duffys Forest",
    # Hills District
    "Castle Hill", "Kellyville", "Kellyville Ridge", "Rouse Hill",
    "Baulkham Hills", "Winston Hills", "Northmead", "Westmead",
    "Wentworthville", "Pendle Hill", "Girraween", "Glenwood",
    "Stanhope Gardens", "Beaumont Hills", "Box Hill", "Schofields",
    "Riverstone", "Vineyard", "McGraths Hill", "Windsor",
    "Windsor Downs", "Richmond", "North Richmond", "Dural",
    "Glenhaven", "West Pennant Hills", "Carlingford", "Dundas",
    "Dundas Valley", "Telopea", "Oatlands", "Clyde", "Rydalmere",
    "The Ponds", "Parklea", "Quakers Hill", "Acacia Gardens",
    "Pitt Town", "Wilberforce", "Glossodia",
    # Blacktown
    "Blacktown", "Arndell Park", "Bidwill", "Blackett", "Bungarribee",
    "Colebee", "Dean Park", "Dharruk", "Doonside", "Eastern Creek",
    "Glendenning", "Hebersham", "Kings Park", "Lalor Park",
    "Lethbridge Park", "Marayong", "Marsden Park", "Minchinbury",
    "Mount Druitt", "Old Toongabbie", "Prospect", "Rooty Hill",
    "Seven Hills", "Shalvey", "Tregear", "Willmot", "Woodcroft",
    "Wattle Grove",
    # Parramatta
    "Parramatta", "North Parramatta", "Granville", "South Granville",
    "Harris Park", "Merrylands", "Merrylands West", "Guildford",
    "Guildford West", "Auburn", "Lidcombe", "Berala", "Regents Park",
    "Woodville", "Camellia", "Chester Hill", "Villawood",
    "Carramar", "Sefton", "Bass Hill",
    # Penrith
    "Penrith", "Kingswood", "Jamisontown", "Emu Plains", "Emu Heights",
    "Leonay", "Glenmore Park", "Jordan Springs", "Cranebrook",
    "Cambridge Gardens", "Cambridge Park", "Oxley Park", "South Penrith",
    "Colyton", "Claremont Meadows", "Werrington", "Orchard Hills",
    "Regentville", "Mulgoa", "Llandilo", "Berkshire Park",
    # Blue Mountains
    "Blaxland", "Glenbrook", "Lapstone", "Springwood", "Winmalee",
    "Faulconbridge", "Woodford", "Hazelbrook", "Lawson", "Bullaburra",
    "Wentworth Falls", "Leura", "Katoomba", "Linden", "Valley Heights",
    "Yellow Rock",
    # Hawkesbury
    "Kurrajong", "Kurrajong Heights", "Kurmond",
    # South-Western / Bankstown / Canterbury
    "Yagoona", "Bankstown", "Punchbowl", "Wiley Park", "Lakemba",
    "Roselands", "Beverly Hills", "Narwee", "Peakhurst", "Condell Park",
    "Mount Lewis", "Greenacre", "Birrong", "Chullora",
    "Canterbury", "Campsie", "Belmore", "Earlwood", "Kingsgrove",
    # Hurstville / St George
    "Hurstville", "Penshurst", "Mortdale", "Oatley", "Lugarno",
    "Riverwood", "Padstow", "Padstow Heights", "Revesby",
    "Revesby Heights", "Panania", "East Hills", "Milperra",
    "Peakhurst Heights", "Hurstville Grove", "Kyle Bay", "Blakehurst",
    "Carss Park", "Ramsgate", "Ramsgate Beach", "Sans Souci",
    "Dolls Point", "Monterey", "Brighton-Le-Sands", "Kyeemagh",
    "Arncliffe", "Bardwell Park", "Bardwell Valley", "Bexley",
    "Bexley North", "Rockdale", "Kogarah", "Carlton", "Allawah",
    "South Hurstville", "Kogarah Bay",
    # Liverpool / South-West
    "Liverpool", "Casula", "Moorebank", "Chipping Norton", "Lansvale",
    "Carnes Hill", "Prestons", "Edmondson Park", "Middleton Grange",
    "Hoxton Park", "Miller", "Hinchinbrook", "Cecil Hills", "Green Valley",
    "Bonnyrigg", "Bonnyrigg Heights", "Fairfield", "Fairfield East",
    "Fairfield Heights", "Fairfield West", "Cabramatta",
    "Cabramatta West", "Canley Vale", "Canley Heights",
    "Smithfield", "Wetherill Park", "Bossley Park", "Prairiewood",
    "Wakeley", "Edensor Park", "Greenfield Park", "St Johns Park",
    "Yennora", "Lurnea", "Sadleir", "Cartwright", "Busby",
    "Ashcroft", "Holsworthy", "Cecil Park", "Warwick Farm",
    # Sutherland Shire
    "Sutherland", "Cronulla", "Caringbah", "Caringbah South",
    "Miranda", "Gymea", "Gymea Bay", "Kirrawee", "Jannali", "Como",
    "Engadine", "Heathcote", "Waterfall", "Menai", "Illawong",
    "Alfords Point", "Bangor", "Barden Ridge", "Sandy Point",
    "Bonnet Bay", "Woronora", "Woronora Heights", "Loftus",
    "Grays Point", "Kangaroo Point", "Sylvania", "Sylvania Waters",
    "Taren Point", "Burraneer", "Dolans Bay", "Port Hacking",
    "Kurnell", "Bundeena", "Maianbar", "Yowie Bay", "Oyster Bay",
    "Kareela", "Woolooware",
    # Camden / Macarthur / Wollondilly
    "Camden", "Narellan", "Narellan Vale", "Mount Annan",
    "Harrington Park", "Gregory Hills", "Gledswood Hills",
    "Oran Park", "Spring Farm", "Cobbitty", "Elderslie",
    "Kirkham", "Leppington", "Grasmere",
    "Campbelltown", "Minto", "Leumeah", "Glenfield",
    "Macquarie Fields", "Ingleburn", "Raby", "Bow Bowing",
    "Ambarvale", "Rosemeadow", "Blair Athol", "Bradbury",
    "Claymore", "Glen Alpine", "Kentlyn", "Ruse",
    "St Andrews", "St Helens Park", "Woodbine",
    "Appin", "Bargo", "Picton", "Thirlmere", "Tahmoor", "Wilton",
    "Douglas Park", "Buxton",
]

SUBURBS = sorted(set(SUBURBS))

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzdtD0egYjC7Pg_g59ojkqeVsbfKjvCy8OB3Y6GVi7agO4OiBnBfKxcgosy0IpqUqDWSg/exec"
PIXEL_ID   = "994518709733202"

# Brand colours
CREAM  = "#F0E6D0"
CREAM2 = "#FFFCF7"
TEAL   = "#00C9A7"
GOLD   = "#D4A847"
RED    = "#B5451B"
INK    = "#1a1a1a"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


SERIF  = "Georgia, 'Times New Roman', serif"
SANS   = "Helvetica, Arial, sans-serif"

CHECK_SVG = (
    "<svg width='14' height='14' viewBox='0 0 24 24' fill='none' "
    "stroke='currentColor' stroke-width='2.5' stroke-linecap='round' "
    "stroke-linejoin='round'><polyline points='20 6 9 17 4 12'/></svg>"
)
CARET_SVG = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='12' height='12' viewBox='0 0 24 24' fill='none' "
    "stroke='%231a1a1a' stroke-width='2.5' stroke-linecap='round' "
    "stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E\")"
)


def make_page(suburb):
    title = f"Solar Battery Installation {suburb}"
    desc  = (
        f"Get a free solar battery installation quote in {suburb}, Sydney. "
        "HelioFlo installs premium LiFePO4 home batteries — federal rebates available."
    )
    slug = slugify(suburb)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{PIXEL_ID}');
  fbq('track', 'PageView');
  fbq('track', 'ViewContent', {{content_name: '{title}', content_category: 'Suburb Landing Page'}});
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"
  /></noscript>
  <!-- End Meta Pixel Code -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Solar Battery Installation {suburb} | HelioFlo</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="../../brand_assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../styles.min.css">
  <style>
    /* ════════ SUBURB PAGE — VIDEO HERO + FORM ════════ */

    /* Video hero */
    .suburb-hero {{
      position: relative;
      height: 100vh;
      min-height: 560px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    .suburb-hero__vid {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 0;
    }}
    .suburb-hero__scrim {{
      position: absolute;
      inset: 0;
      background: linear-gradient(
        160deg,
        rgba(26,20,16,0.72) 0%,
        rgba(26,20,16,0.55) 60%,
        rgba(26,20,16,0.70) 100%
      );
      z-index: 1;
    }}
    .suburb-hero__inner {{
      position: relative;
      z-index: 2;
      text-align: center;
      padding: 0 24px;
      max-width: 820px;
    }}
    .suburb-hero__eyebrow {{
      font-family: var(--font-sans);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 24px;
    }}
    .suburb-hero__h1 {{
      font-family: var(--font-serif);
      line-height: 1.05;
      margin-bottom: 36px;
    }}
    .suburb-hero__service {{
      display: block;
      font-style: italic;
      font-weight: 400;
      font-size: clamp(1.4rem, 2.8vw, 2.2rem);
      color: rgba(255,255,255,0.78);
      letter-spacing: -0.01em;
      margin-bottom: 8px;
    }}
    .suburb-hero__name {{
      display: block;
      font-style: normal;
      font-weight: 700;
      font-size: clamp(3.2rem, 8vw, 6rem);
      color: var(--teal);
      letter-spacing: -0.04em;
      line-height: 0.9;
    }}
    .suburb-hero__cta {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 1rem 2.2rem;
      background: var(--teal);
      color: #fff;
      font-family: var(--font-sans);
      font-size: 0.95rem;
      font-weight: 700;
      border-radius: 999px;
      text-decoration: none;
      box-shadow: 0 14px 36px rgba(0,201,167,0.32);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .suburb-hero__cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 18px 44px rgba(0,201,167,0.42);
    }}

    /* Quote form section */
    .suburb-form-section {{
      background: var(--cream);
      padding: 80px 0;
    }}
    .suburb-form-wrap {{
      width: min(680px, calc(100% - 2rem));
      margin: 0 auto;
      background: #fff;
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }}
    .sform-hdr {{
      background: var(--dark-surface);
      padding: 24px 36px;
      border-bottom: 3px solid var(--teal);
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .sform-hdr__title {{
      font-family: var(--font-serif);
      font-style: italic;
      font-size: 1.3rem;
      color: #fff;
      font-weight: 400;
    }}
    .sform-hdr__badges {{
      display: flex;
      gap: 8px;
    }}
    .sbadge {{
      font-family: var(--font-sans);
      font-size: 0.62rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 9px;
      border-radius: 4px;
    }}
    .sbadge--teal {{ background: var(--teal); color: var(--dark); }}
    .sbadge--gold {{ background: var(--gold); color: var(--dark); }}
    .sform-body {{ padding: 32px 36px 36px; }}
    .sfg {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .sff {{ display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; }}
    .sff label {{
      font-family: var(--font-sans);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .sff .req {{ color: var(--gold); }}
    .sff input,
    .sff select {{
      font-family: var(--font-sans);
      font-size: 0.875rem;
      color: var(--text);
      background: var(--cream);
      border: 1px solid var(--border);
      border-radius: 8px;
      height: 42px;
      padding: 0 12px;
      outline: none;
      appearance: none;
      -webkit-appearance: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .sff select {{
      background-image: {CARET_SVG};
      background-color: var(--cream);
      background-repeat: no-repeat;
      background-position: right 10px center;
      padding-right: 30px;
    }}
    .sff input:focus,
    .sff select:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0,201,167,0.14);
      background: #fff;
    }}
    .sff textarea {{
      font-family: var(--font-sans);
      font-size: 0.875rem;
      color: var(--text);
      background: var(--cream);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
      min-height: 72px;
      resize: vertical;
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .sff textarea:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0,201,167,0.14);
      background: #fff;
    }}
    .sform-foot {{
      margin-top: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .sbtn-submit {{
      font-family: var(--font-sans);
      font-size: 0.9rem;
      font-weight: 700;
      color: #fff;
      background: linear-gradient(135deg, var(--teal) 0%, #009E85 100%);
      border: none;
      border-radius: 999px;
      padding: 14px 36px;
      cursor: pointer;
      box-shadow: 0 10px 28px rgba(0,201,167,0.28);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .sbtn-submit:hover {{ transform: translateY(-2px); box-shadow: 0 16px 36px rgba(0,201,167,0.38); }}
    .sbtn-submit:disabled {{ opacity: 0.55; cursor: not-allowed; transform: none; }}
    .sform-note {{
      font-family: var(--font-sans);
      font-size: 0.73rem;
      color: var(--muted);
      line-height: 1.5;
    }}

    @media (max-width: 600px) {{
      .sfg {{ grid-template-columns: 1fr; }}
      .sform-body {{ padding: 24px 20px 28px; }}
      .sform-hdr {{ padding: 20px 20px; }}
    }}
  </style>
</head>
<body>

  <!-- ═══ HEADER (matches landing page) ═══ -->
  <header class="site-header" id="site-header">
    <div class="container header-row">
      <a href="/" aria-label="HelioFlo home">
        <img src="../../brand_assets/HelioFlo_Logo.svg" alt="HelioFlo" class="brand-logo">
      </a>
      <nav id="main-nav" class="main-nav" role="navigation" aria-label="Main navigation">
        <a href="/#why">Why HelioFlo</a>
        <a href="/#products">Products</a>
        <a href="/#process">Process</a>
        <a href="/#faq">FAQ</a>
        <a href="#quote" class="btn btn-nav btn-sm">Get a Free Quote</a>
      </nav>
      <div class="header-end">
        <a href="tel:0414146027" class="header-phone">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 0118 1.18 2 2 0 0120 3.17v3a2 2 0 01-1.64 1.95 13 13 0 00-5.5 2.38 13 13 0 00-3.63 3.63 13 13 0 00-2.38 5.5A2 2 0 016.84 22a19.79 19.79 0 01-3.07-8.63 2 2 0 012-2.18h3a2 2 0 011.95 1.64z"/></svg>
          0414 146 027
        </a>
        <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <!-- ═══ VIDEO HERO ═══ -->
  <section class="suburb-hero">
    <video class="suburb-hero__vid" autoplay muted loop playsinline>
      <source src="../../brand_assets/solar-bg.mp4" type="video/mp4">
    </video>
    <div class="suburb-hero__scrim"></div>
    <div class="suburb-hero__inner">
      <p class="suburb-hero__eyebrow">SAA-Accredited &middot; Sydney, NSW</p>
      <h1 class="suburb-hero__h1">
        <span class="suburb-hero__service">Solar Battery Installation</span>
        <span class="suburb-hero__name">{suburb}</span>
      </h1>
      <a href="#quote" class="suburb-hero__cta">Get a Free Quote</a>
    </div>
  </section>

  <!-- ═══ QUOTE FORM ═══ -->
  <section class="suburb-form-section" id="quote">
    <div class="suburb-form-wrap">
      <div class="sform-hdr">
        <span class="sform-hdr__title">Get a free quote</span>
        <div class="sform-hdr__badges">
          <span class="sbadge sbadge--teal">No obligation</span>
          <span class="sbadge sbadge--gold">Rebate eligible</span>
        </div>
      </div>
      <div class="sform-body">
        <form id="suburb-form" action="#" method="post" novalidate>
          <div class="sfg">
            <div class="sff">
              <label>First name <span class="req">*</span></label>
              <input name="first_name" type="text" placeholder="Alex" autocomplete="given-name" required>
            </div>
            <div class="sff">
              <label>Last name</label>
              <input name="last_name" type="text" placeholder="Johnson" autocomplete="family-name">
            </div>
          </div>
          <div class="sfg">
            <div class="sff">
              <label>Email <span class="req">*</span></label>
              <input name="email" type="email" placeholder="alex@example.com" autocomplete="email" required>
            </div>
            <div class="sff">
              <label>Phone <span class="req">*</span></label>
              <input name="phone" type="tel" placeholder="04XX XXX XXX" autocomplete="tel" required>
            </div>
          </div>
          <div class="sff">
            <label>Address</label>
            <input name="address" type="text" placeholder="e.g. 12 Smith St, {suburb}" autocomplete="off">
          </div>
          <div class="sfg">
            <div class="sff">
              <label>Property type</label>
              <select name="property">
                <option value="" disabled selected>Select</option>
                <option value="house">House</option>
                <option value="townhouse">Townhouse</option>
                <option value="apartment">Apartment</option>
                <option value="business">Business</option>
              </select>
            </div>
            <div class="sff">
              <label>Interested in</label>
              <select name="interest">
                <option value="" disabled selected>Select</option>
                <option value="inverter-battery">Inverter + Battery</option>
                <option value="battery-only">Battery only</option>
              </select>
            </div>
          </div>
          <div class="sfg">
            <div class="sff">
              <label>Build type</label>
              <select name="build_type">
                <option value="" disabled selected>Select</option>
                <option value="existing">Existing</option>
                <option value="new-build">New Build</option>
              </select>
            </div>
            <div class="sff">
              <label>Quarterly electricity bill</label>
              <select name="electricity_bill">
                <option value="" disabled selected>Select</option>
                <option value="under-300">Under $300</option>
                <option value="301-600">$301 – $600</option>
                <option value="601-900">$601 – $900</option>
                <option value="above-900">Above $900</option>
              </select>
            </div>
          </div>
          <div class="sfg">
            <div class="sff">
              <label>Installation timeframe</label>
              <select name="install_period">
                <option value="" disabled selected>Select</option>
                <option value="0-1m">0 – 1 month</option>
                <option value="1-3m">1 – 3 months</option>
                <option value="4-6m">4 – 6 months</option>
                <option value="researching">Just researching</option>
              </select>
            </div>
            <div class="sff">
              <label>Anything else? <span style="font-weight:400;opacity:0.6;">(optional)</span></label>
              <textarea name="message" placeholder="Tell us about your home…"></textarea>
            </div>
          </div>
          <div class="sform-foot">
            <button type="submit" class="sbtn-submit" id="suburb-submit">Send Quote Request</button>
            <p class="sform-note">No spam. We'll only contact you about your enquiry.</p>
          </div>
        </form>
      </div>
    </div>
  </section>

  <!-- ═══ FOOTER (matches landing page) ═══ -->
  <footer class="site-footer">
    <div class="footer-accent"></div>
    <div class="container footer-main">
      <a href="/" aria-label="HelioFlo home" class="footer-brand">
        <img src="../../brand_assets/HelioFlo_Logo.svg" alt="HelioFlo" class="footer-logo">
      </a>
      <nav class="footer-nav" aria-label="Footer navigation">
        <a href="/#why">Why HelioFlo</a>
        <a href="/#products">Products</a>
        <a href="/#process">Our Process</a>
        <a href="/#faq">FAQ</a>
        <a href="/payment">Payment Terms</a>
      </nav>
      <div class="footer-contact">
        <a href="tel:0414146027">0414 146 027</a>
        <a href="mailto:hello@helioflo.com">hello@helioflo.com</a>
      </div>
    </div>
    <div class="footer-accred">
      <div class="container footer-accred-logos">
        <img src="../../Accreditation/SAA%20Accreditation.jpg" alt="SAA Accredited Installer">
        <img src="../../Accreditation/New%20Energy%20Tech%20Accreditation.webp" alt="New Energy Tech Approved Seller">
        <img src="../../Accreditation/Powerwall%20Certified%20Accreditation.jpg" alt="Powerwall Certified Installer">
      </div>
    </div>
    <div class="container footer-bottom">
      <p>&copy; 2026 HelioFlo. All rights reserved.</p>
      <div class="footer-legal">
        <a href="/privacy">Privacy Policy</a>
        <a href="/complaints">Complaints Policy</a>
      </div>
    </div>
  </footer>

  <script>
    // Header scroll state (matches landing page)
    const header = document.getElementById('site-header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', onScroll, {{ passive: true }});
    onScroll();

    // Mobile nav toggle
    const navToggle = document.querySelector('.nav-toggle');
    const mainNav   = document.querySelector('.main-nav');
    navToggle?.addEventListener('click', () => {{
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      mainNav.classList.toggle('is-open');
      navToggle.classList.toggle('is-open');
    }});

    // Form submit
    const SCRIPT_URL = '{SCRIPT_URL}';
    document.getElementById('suburb-form').addEventListener('submit', async function(e) {{
      e.preventDefault();
      const btn  = document.getElementById('suburb-submit');
      const form = e.target;
      btn.textContent = 'Sending...';
      btn.disabled = true;

      const payload = {{
        timestamp:        new Date().toLocaleString('en-AU'),
        source:           'Suburb Page – {suburb}',
        first_name:       form.first_name.value,
        last_name:        form.last_name.value,
        email:            form.email.value,
        phone:            form.phone.value,
        address:          form.address.value,
        property:         form.property.value,
        interest:         form.interest.value,
        build_type:       form.build_type.value,
        electricity_bill: form.electricity_bill.value,
        install_period:   form.install_period.value,
        message:          form.message.value,
      }};

      try {{
        await fetch(SCRIPT_URL, {{ method: 'POST', mode: 'no-cors', body: JSON.stringify(payload) }});
        fbq('track', 'Lead', {{value: 150.00, currency: 'AUD'}});
        fbq('track', 'Schedule');
        btn.textContent = 'Request sent. We\\'ll be in touch soon!';
      }} catch {{
        btn.textContent = 'Something went wrong. Please try again.';
        btn.disabled = false;
      }}
    }});

    document.addEventListener('click', function(e) {{
      var a = e.target.closest('a');
      if (!a || !a.href) return;
      if (a.href.indexOf('tel:')    === 0) fbq('track', 'Contact', {{contact_method: 'phone'}});
      if (a.href.indexOf('mailto:') === 0) fbq('track', 'Contact', {{contact_method: 'email'}});
    }});
  </script>

</body>
</html>
"""


def main():
    import shutil
    base = os.path.dirname(os.path.abspath(__file__))

    # Remove old root-level suburb folders
    slugs = {slugify(s) for s in SUBURBS}
    non_suburb = {
        "brand_assets", "accreditation", "payment", "privacy", "complaints",
        "basic-batteries", "recommended-batteries", "premium-batteries",
        "solar-inverters", "suburbs", ".git", ".github",
    }
    for entry in os.listdir(base):
        entry_lower = entry.lower()
        if (os.path.isdir(os.path.join(base, entry))
                and entry_lower not in non_suburb
                and entry_lower in slugs):
            shutil.rmtree(os.path.join(base, entry))
            print(f"  Removed old /{entry}/")

    # Generate into suburbs/{slug}/index.html
    suburbs_dir = os.path.join(base, "suburbs")
    for suburb in SUBURBS:
        slug     = slugify(suburb)
        out_dir  = os.path.join(suburbs_dir, slug)
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(make_page(suburb))

    print(f"Generated {len(SUBURBS)} suburb pages as /suburbs/<slug>/index.html")
    print("Sample URLs:")
    for s in SUBURBS[:5]:
        print(f"  /suburbs/{slugify(s)}/")


if __name__ == "__main__":
    main()
