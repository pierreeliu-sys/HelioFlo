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


def make_page(suburb):
    title = f"Solar Battery Installation {suburb}"
    desc  = (
        f"Get a free solar battery installation quote in {suburb}, Sydney. "
        "HelioFlo installs premium LiFePO4 home batteries with federal rebates available."
    )

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
  <title>HelioFlo | {title}</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="../brand_assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../styles.css">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: {CREAM}; font-family: var(--font-sans, system-ui, sans-serif); }}

    /* ── Nav ── */
    .s-nav {{
      background: {CREAM2};
      border-bottom: 1px solid rgba(0,0,0,0.08);
      padding: 0 40px;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .s-nav__logo {{ height: 26px; }}
    .s-nav__back {{
      font-size: 0.78rem;
      font-weight: 600;
      color: {INK};
      text-decoration: none;
      opacity: 0.45;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: opacity 0.15s;
    }}
    .s-nav__back:hover {{ opacity: 1; color: {TEAL}; }}

    /* ── Page wrapper ── */
    .s-main {{
      padding: 36px 20px 52px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .s-eyebrow {{
      font-size: 0.67rem;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: {GOLD};
      margin-bottom: 10px;
    }}
    .s-h1 {{
      font-size: clamp(1.5rem, 4vw, 2.1rem);
      font-weight: 800;
      letter-spacing: -0.025em;
      line-height: 1.15;
      text-align: center;
      margin-bottom: 24px;
      max-width: 580px;
    }}
    .s-h1__label {{
      display: block;
      color: {RED};
      font-size: 0.72em;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .s-h1__suburb {{ color: {TEAL}; }}

    /* ── Form card ── */
    .s-card {{
      width: 100%;
      max-width: 720px;
      background: {CREAM2};
      border-radius: 14px;
      border: 1px solid rgba(0,0,0,0.07);
      border-top: 3px solid {TEAL};
      box-shadow: 0 4px 28px rgba(0,0,0,0.07);
      overflow: hidden;
    }}

    /* ── Card header band ── */
    .s-card__head {{
      background: {INK};
      padding: 16px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .s-card__head-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: rgba(255,255,255,0.9);
      letter-spacing: 0.01em;
    }}
    .s-card__head-badges {{
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }}
    .s-badge {{
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .s-badge--teal {{ background: {TEAL}; color: {INK}; }}
    .s-badge--gold {{ background: {GOLD}; color: {INK}; }}

    /* ── Form body ── */
    .s-card__body {{ padding: 24px 28px 28px; }}

    /* ── Compact form overrides ── */
    .s-form .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .s-form .form-field {{ margin-bottom: 10px; }}
    .s-form .form-field:last-of-type {{ margin-bottom: 0; }}
    .s-form label {{
      display: block;
      font-size: 0.72rem;
      font-weight: 600;
      color: {INK};
      opacity: 0.7;
      margin-bottom: 4px;
      letter-spacing: 0.02em;
    }}
    .s-form .required-star {{ color: {GOLD}; opacity: 1; }}
    .s-form input,
    .s-form select {{
      width: 100%;
      height: 38px;
      padding: 0 11px;
      font-size: 0.86rem;
      color: {INK};
      background: #fff;
      border: 1px solid rgba(0,0,0,0.14);
      border-radius: 7px;
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
      appearance: none;
      -webkit-appearance: none;
    }}
    .s-form select {{
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%231a1a1a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 10px center;
      padding-right: 28px;
    }}
    .s-form input:focus,
    .s-form select:focus {{
      border-color: {TEAL};
      box-shadow: 0 0 0 3px rgba(0,201,167,0.13);
    }}
    .s-form textarea {{
      width: 100%;
      padding: 9px 11px;
      font-size: 0.86rem;
      color: {INK};
      background: #fff;
      border: 1px solid rgba(0,0,0,0.14);
      border-radius: 7px;
      outline: none;
      resize: vertical;
      min-height: 68px;
      transition: border-color 0.15s, box-shadow 0.15s;
      font-family: inherit;
    }}
    .s-form textarea:focus {{
      border-color: {TEAL};
      box-shadow: 0 0 0 3px rgba(0,201,167,0.13);
    }}

    /* ── Submit row ── */
    .s-form__foot {{
      margin-top: 18px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .s-submit {{
      flex-shrink: 0;
      padding: 11px 28px;
      background: {TEAL};
      color: {INK};
      font-size: 0.88rem;
      font-weight: 700;
      letter-spacing: 0.01em;
      border: none;
      border-radius: 9999px;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
    }}
    .s-submit:hover {{ background: #00b394; transform: translateY(-1px); }}
    .s-submit:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; }}
    .s-form-note {{
      font-size: 0.75rem;
      color: #999;
      line-height: 1.4;
    }}

    /* ── Footer ── */
    .s-footer {{
      background: {INK};
      color: rgba(255,255,255,0.32);
      text-align: center;
      padding: 16px 24px;
      font-size: 0.73rem;
      letter-spacing: 0.01em;
    }}
    .s-footer a {{
      color: rgba(255,255,255,0.32);
      text-decoration: none;
      margin: 0 6px;
      transition: color 0.15s;
    }}
    .s-footer a:hover {{ color: {TEAL}; }}

    @media (max-width: 580px) {{
      .s-nav {{ padding: 0 16px; }}
      .s-main {{ padding: 28px 12px 40px; }}
      .s-card__head {{ padding: 14px 18px; flex-wrap: wrap; }}
      .s-card__body {{ padding: 18px 18px 22px; }}
      .s-form .form-row {{ grid-template-columns: 1fr; gap: 0; }}
    }}
  </style>
</head>
<body>

  <nav class="s-nav">
    <a href="/">
      <img src="../brand_assets/HelioFlo_Logo.svg" alt="HelioFlo" class="s-nav__logo">
    </a>
    <a href="/" class="s-nav__back">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
      Main site
    </a>
  </nav>

  <main class="s-main">
    <p class="s-eyebrow">SAA-Accredited &middot; Sydney, NSW</p>
    <h1 class="s-h1">
      <span class="s-h1__label">Solar Battery Installation</span>
      <span class="s-h1__suburb">{suburb}</span>
    </h1>

    <div class="s-card">
      <div class="s-card__head">
        <span class="s-card__head-title">Get a free quote</span>
        <div class="s-card__head-badges">
          <span class="s-badge s-badge--teal">No obligation</span>
          <span class="s-badge s-badge--gold">Federal rebate eligible</span>
        </div>
      </div>
      <div class="s-card__body">
        <form class="s-form" id="suburb-form" action="#" method="post" novalidate>
          <div class="form-row">
            <div class="form-field">
              <label for="first-name">First name <span class="required-star">*</span></label>
              <input id="first-name" name="first_name" type="text" placeholder="Alex" autocomplete="given-name" required>
            </div>
            <div class="form-field">
              <label for="last-name">Last name</label>
              <input id="last-name" name="last_name" type="text" placeholder="Johnson" autocomplete="family-name">
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="email">Email <span class="required-star">*</span></label>
              <input id="email" name="email" type="email" placeholder="alex@example.com" autocomplete="email" required>
            </div>
            <div class="form-field">
              <label for="phone">Phone <span class="required-star">*</span></label>
              <input id="phone" name="phone" type="tel" placeholder="04XX XXX XXX" autocomplete="tel" required>
            </div>
          </div>
          <div class="form-field">
            <label for="address">Address</label>
            <input id="address" name="address" type="text" placeholder="e.g. 12 Smith St, {suburb}" autocomplete="off">
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="property">Property type</label>
              <select id="property" name="property">
                <option value="" disabled selected>Select type</option>
                <option value="house">House</option>
                <option value="townhouse">Townhouse</option>
                <option value="apartment">Apartment</option>
                <option value="business">Business</option>
              </select>
            </div>
            <div class="form-field">
              <label for="interest">Interested in</label>
              <select id="interest" name="interest">
                <option value="" disabled selected>Select a service</option>
                <option value="inverter-battery">Inverter + Battery bundle</option>
                <option value="battery-only">Battery only</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="build-type">Build type</label>
              <select id="build-type" name="build_type">
                <option value="" disabled selected>Select type</option>
                <option value="existing">Existing</option>
                <option value="new-build">New Build</option>
              </select>
            </div>
            <div class="form-field">
              <label for="electricity-bill">Quarterly bill</label>
              <select id="electricity-bill" name="electricity_bill">
                <option value="" disabled selected>Select range</option>
                <option value="under-300">Under $300</option>
                <option value="301-600">$301 – $600</option>
                <option value="601-900">$601 – $900</option>
                <option value="above-900">Above $900</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="install-period">Installation timeframe</label>
              <select id="install-period" name="install_period">
                <option value="" disabled selected>Select timeframe</option>
                <option value="0-1m">0 – 1 month</option>
                <option value="1-3m">1 – 3 months</option>
                <option value="4-6m">4 – 6 months</option>
                <option value="researching">Just researching</option>
              </select>
            </div>
            <div class="form-field">
              <label for="message">Anything else? <span style="font-weight:400;opacity:0.6;">(optional)</span></label>
              <textarea id="message" name="message" placeholder="Tell us about your home…"></textarea>
            </div>
          </div>
          <div class="s-form__foot">
            <button type="submit" class="s-submit" id="suburb-submit">Send Quote Request</button>
            <p class="s-form-note">No spam, ever. We'll only contact you about your enquiry.</p>
          </div>
        </form>
      </div>
    </div>
  </main>

  <footer class="s-footer">
    <p>
      &copy; 2026 HelioFlo. All rights reserved.
      <a href="/privacy">Privacy Policy</a>
      <a href="/complaints">Complaints Policy</a>
      <a href="tel:0414146027">0414 146 027</a>
      <a href="mailto:hello@helioflo.com">hello@helioflo.com</a>
    </p>
  </footer>

  <script>
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
        fbq('track', 'Lead');
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
    base = os.path.dirname(os.path.abspath(__file__))

    # Remove old suburbs/ flat-file directory
    old_dir = os.path.join(base, "suburbs")
    if os.path.isdir(old_dir):
        import shutil
        shutil.rmtree(old_dir)
        print(f"Removed old {old_dir}/")

    for suburb in SUBURBS:
        slug     = slugify(suburb)
        out_dir  = os.path.join(base, slug)
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(make_page(suburb))

    print(f"Generated {len(SUBURBS)} suburb pages as /<slug>/index.html")
    print("Sample URLs:")
    for s in SUBURBS[:5]:
        print(f"  /{slugify(s)}/")


if __name__ == "__main__":
    main()
