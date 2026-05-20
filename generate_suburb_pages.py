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
  <link rel="icon" href="../brand_assets/favicon.svg" type="image/svg+xml">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --red:   {RED};
      --teal:  {TEAL};
      --gold:  {GOLD};
      --ink:   {INK};
      --cream: {CREAM};
      --white: {CREAM2};
      --serif: {SERIF};
      --sans:  {SANS};
      --border: rgba(0,0,0,0.09);
    }}

    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--sans);
      background: var(--cream);
      color: var(--ink);
      -webkit-font-smoothing: antialiased;
    }}

    /* ════════════════════════════════════════
       HEADER
    ════════════════════════════════════════ */
    .hdr {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--ink);
      border-bottom: 3px solid var(--red);
      padding: 0 48px;
      height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }}
    .hdr__logo {{ height: 30px; flex-shrink: 0; }}
    .hdr__nav {{
      display: flex;
      align-items: center;
      gap: 28px;
      flex: 1;
      justify-content: center;
    }}
    .hdr__nav a {{
      font-family: var(--sans);
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.55);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .hdr__nav a:hover {{ color: #fff; }}
    .hdr__right {{
      display: flex;
      align-items: center;
      gap: 20px;
      flex-shrink: 0;
    }}
    .hdr__phone {{
      font-family: var(--sans);
      font-size: 0.82rem;
      font-weight: 600;
      color: rgba(255,255,255,0.6);
      text-decoration: none;
      letter-spacing: 0.02em;
      transition: color 0.15s;
    }}
    .hdr__phone:hover {{ color: #fff; }}
    .hdr__cta {{
      font-family: var(--sans);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--ink);
      background: var(--teal);
      padding: 9px 20px;
      border-radius: 9999px;
      text-decoration: none;
      transition: background 0.15s, transform 0.1s;
    }}
    .hdr__cta:hover {{ background: #00b394; transform: translateY(-1px); }}

    /* ════════════════════════════════════════
       HERO SPLIT LAYOUT
    ════════════════════════════════════════ */
    .hero {{
      display: grid;
      grid-template-columns: 52% 48%;
      min-height: calc(100vh - 68px);
      align-items: start;
    }}

    /* LEFT PANEL */
    .hero__left {{
      padding: 64px 56px 64px 64px;
      display: flex;
      flex-direction: column;
    }}
    .hero__eyebrow {{
      font-family: var(--sans);
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 20px;
    }}
    .hero__h1 {{
      font-family: var(--serif);
      margin-bottom: 32px;
      line-height: 1;
    }}
    .hero__h1-service {{
      display: block;
      font-style: italic;
      font-weight: 400;
      font-size: clamp(1.4rem, 2.6vw, 2rem);
      color: var(--red);
      letter-spacing: -0.01em;
      margin-bottom: 6px;
    }}
    .hero__h1-suburb {{
      display: block;
      font-style: normal;
      font-weight: 700;
      font-size: clamp(3rem, 6vw, 5rem);
      color: var(--teal);
      letter-spacing: -0.035em;
      line-height: 0.92;
    }}
    .hero__sub {{
      font-family: var(--serif);
      font-size: 1rem;
      color: rgba(26,26,26,0.62);
      line-height: 1.7;
      max-width: 400px;
      margin-bottom: 40px;
    }}

    /* Trust list */
    .trust {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0;
      margin-bottom: 44px;
    }}
    .trust li {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--serif);
      font-size: 0.9rem;
      font-weight: 400;
      color: var(--ink);
      padding: 11px 0;
      border-bottom: 1px solid var(--border);
    }}
    .trust li:first-child {{ border-top: 1px solid var(--border); }}
    .trust__icon {{
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--teal);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      color: var(--ink);
    }}

    /* Accreditations */
    .accred {{
      display: flex;
      gap: 16px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .accred img {{
      height: 44px;
      object-fit: contain;
      opacity: 0.65;
      filter: grayscale(0.2);
    }}

    /* RIGHT PANEL */
    .hero__right {{
      background: var(--white);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      min-height: calc(100vh - 68px);
    }}

    /* Form card header */
    .form-hdr {{
      background: var(--ink);
      padding: 22px 32px;
      border-bottom: 3px solid var(--teal);
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .form-hdr__title {{
      font-family: var(--serif);
      font-style: italic;
      font-size: 1.25rem;
      color: #fff;
      font-weight: 400;
    }}
    .form-hdr__badges {{
      display: flex;
      gap: 8px;
    }}
    .badge {{
      font-family: var(--sans);
      font-size: 0.62rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 9px;
      border-radius: 4px;
    }}
    .badge--teal {{ background: var(--teal); color: var(--ink); }}
    .badge--gold {{ background: var(--gold); color: var(--ink); }}

    /* Form body */
    .form-body {{ padding: 28px 32px 32px; flex: 1; }}

    /* Form grid */
    .fg {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .ff {{ display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; }}
    .ff--full {{ grid-column: 1 / -1; }}
    .ff label {{
      font-family: var(--sans);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: rgba(26,26,26,0.55);
    }}
    .ff .req {{ color: var(--gold); }}
    .ff input,
    .ff select {{
      font-family: var(--sans);
      font-size: 0.875rem;
      color: var(--ink);
      background: #fff;
      border: 1px solid rgba(0,0,0,0.15);
      border-radius: 6px;
      height: 40px;
      padding: 0 12px;
      outline: none;
      appearance: none;
      -webkit-appearance: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .ff select {{
      background-image: {CARET_SVG};
      background-repeat: no-repeat;
      background-position: right 10px center;
      padding-right: 30px;
    }}
    .ff input:focus,
    .ff select:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0,201,167,0.14);
    }}
    .ff textarea {{
      font-family: var(--sans);
      font-size: 0.875rem;
      color: var(--ink);
      background: #fff;
      border: 1px solid rgba(0,0,0,0.15);
      border-radius: 6px;
      padding: 10px 12px;
      min-height: 64px;
      resize: vertical;
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .ff textarea:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0,201,167,0.14);
    }}

    /* Submit row */
    .form-foot {{
      margin-top: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .btn-submit {{
      font-family: var(--sans);
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--ink);
      background: var(--teal);
      border: none;
      border-radius: 9999px;
      padding: 13px 32px;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
      flex-shrink: 0;
    }}
    .btn-submit:hover {{ background: #00b394; transform: translateY(-1px); }}
    .btn-submit:disabled {{ opacity: 0.55; cursor: not-allowed; transform: none; }}
    .form-note {{
      font-family: var(--sans);
      font-size: 0.73rem;
      color: #aaa;
      line-height: 1.45;
    }}

    /* ════════════════════════════════════════
       FOOTER
    ════════════════════════════════════════ */
    .ftr {{
      background: var(--ink);
      border-top: 3px solid var(--red);
    }}
    .ftr__inner {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 48px 24px;
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: start;
      gap: 32px;
    }}
    .ftr__logo {{ height: 26px; opacity: 0.7; }}
    .ftr__links {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px 20px;
      justify-content: center;
      align-items: center;
    }}
    .ftr__links a {{
      font-family: var(--sans);
      font-size: 0.78rem;
      color: rgba(255,255,255,0.4);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .ftr__links a:hover {{ color: var(--teal); }}
    .ftr__contact {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      text-align: right;
    }}
    .ftr__contact a {{
      font-family: var(--sans);
      font-size: 0.78rem;
      color: rgba(255,255,255,0.4);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .ftr__contact a:hover {{ color: #fff; }}
    .ftr__copy {{
      grid-column: 1 / -1;
      border-top: 1px solid rgba(255,255,255,0.08);
      padding-top: 16px;
      font-family: var(--sans);
      font-size: 0.72rem;
      color: rgba(255,255,255,0.25);
      text-align: center;
    }}

    /* ════════════════════════════════════════
       RESPONSIVE
    ════════════════════════════════════════ */
    @media (max-width: 900px) {{
      .hdr {{ padding: 0 24px; }}
      .hdr__nav {{ display: none; }}
      .hero {{ grid-template-columns: 1fr; }}
      .hero__left {{ padding: 40px 24px 36px; }}
      .hero__right {{ border-left: none; border-top: 1px solid var(--border); min-height: auto; }}
      .hero__h1-suburb {{ font-size: clamp(2.4rem, 10vw, 3.8rem); }}
      .ftr__inner {{ grid-template-columns: 1fr; padding: 24px; text-align: center; }}
      .ftr__links {{ justify-content: center; }}
      .ftr__contact {{ text-align: center; }}
    }}
    @media (max-width: 480px) {{
      .hdr {{ padding: 0 16px; height: 60px; }}
      .hdr__logo {{ height: 26px; }}
      .hero__left {{ padding: 32px 16px 28px; }}
      .form-hdr {{ padding: 18px 20px; }}
      .form-body {{ padding: 20px 20px 24px; }}
      .fg {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- ═══ HEADER ═══ -->
  <header class="hdr">
    <a href="/"><img src="../brand_assets/HelioFlo_Logo.svg" alt="HelioFlo" class="hdr__logo"></a>
    <nav class="hdr__nav">
      <a href="/#why">Why HelioFlo</a>
      <a href="/#products">Products</a>
      <a href="/#process">Our Process</a>
      <a href="/#faq">FAQ</a>
    </nav>
    <div class="hdr__right">
      <a href="tel:0414146027" class="hdr__phone">0414 146 027</a>
      <a href="#quote-form" class="hdr__cta">Get a Quote</a>
    </div>
  </header>

  <!-- ═══ HERO ═══ -->
  <main class="hero">

    <!-- LEFT: Headline + Trust -->
    <section class="hero__left">
      <p class="hero__eyebrow">SAA-Accredited &middot; Sydney, NSW</p>
      <h1 class="hero__h1">
        <span class="hero__h1-service">Solar Battery Installation</span>
        <span class="hero__h1-suburb">{suburb}</span>
      </h1>
      <p class="hero__sub">
        HelioFlo installs premium LiFePO4 battery systems for homeowners across {suburb} and Greater Sydney.
        Federal government rebates apply — no hidden fees, same-week quotes.
      </p>
      <ul class="trust">
        <li>
          <span class="trust__icon">{CHECK_SVG}</span>
          SAA Accredited Installer
        </li>
        <li>
          <span class="trust__icon">{CHECK_SVG}</span>
          Licensed &amp; Fully Insured
        </li>
        <li>
          <span class="trust__icon">{CHECK_SVG}</span>
          5-Year Workmanship Warranty
        </li>
        <li>
          <span class="trust__icon">{CHECK_SVG}</span>
          Federal Rebate — Cheaper Home Batteries Program
        </li>
        <li>
          <span class="trust__icon">{CHECK_SVG}</span>
          Same-week Quotes &middot; 48-hr Proposal
        </li>
      </ul>
      <div class="accred">
        <img src="../Accreditation/SAA%20Accreditation.jpg" alt="SAA Accredited">
        <img src="../Accreditation/New%20Energy%20Tech%20Accreditation.webp" alt="New Energy Tech">
        <img src="../Accreditation/Powerwall%20Certified%20Accreditation.jpg" alt="Powerwall Certified">
      </div>
    </section>

    <!-- RIGHT: Form -->
    <aside class="hero__right" id="quote-form">
      <div class="form-hdr">
        <span class="form-hdr__title">Get a free quote</span>
        <div class="form-hdr__badges">
          <span class="badge badge--teal">No obligation</span>
          <span class="badge badge--gold">Rebate eligible</span>
        </div>
      </div>
      <div class="form-body">
        <form id="suburb-form" action="#" method="post" novalidate>
          <div class="fg">
            <div class="ff">
              <label>First name <span class="req">*</span></label>
              <input name="first_name" type="text" placeholder="Alex" autocomplete="given-name" required>
            </div>
            <div class="ff">
              <label>Last name</label>
              <input name="last_name" type="text" placeholder="Johnson" autocomplete="family-name">
            </div>
          </div>
          <div class="fg">
            <div class="ff">
              <label>Email <span class="req">*</span></label>
              <input name="email" type="email" placeholder="alex@example.com" autocomplete="email" required>
            </div>
            <div class="ff">
              <label>Phone <span class="req">*</span></label>
              <input name="phone" type="tel" placeholder="04XX XXX XXX" autocomplete="tel" required>
            </div>
          </div>
          <div class="ff">
            <label>Address</label>
            <input name="address" type="text" placeholder="e.g. 12 Smith St, {suburb}" autocomplete="off">
          </div>
          <div class="fg">
            <div class="ff">
              <label>Property type</label>
              <select name="property">
                <option value="" disabled selected>Select</option>
                <option value="house">House</option>
                <option value="townhouse">Townhouse</option>
                <option value="apartment">Apartment</option>
                <option value="business">Business</option>
              </select>
            </div>
            <div class="ff">
              <label>Interested in</label>
              <select name="interest">
                <option value="" disabled selected>Select</option>
                <option value="inverter-battery">Inverter + Battery</option>
                <option value="battery-only">Battery only</option>
              </select>
            </div>
          </div>
          <div class="fg">
            <div class="ff">
              <label>Build type</label>
              <select name="build_type">
                <option value="" disabled selected>Select</option>
                <option value="existing">Existing</option>
                <option value="new-build">New Build</option>
              </select>
            </div>
            <div class="ff">
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
          <div class="fg">
            <div class="ff">
              <label>Installation timeframe</label>
              <select name="install_period">
                <option value="" disabled selected>Select</option>
                <option value="0-1m">0 – 1 month</option>
                <option value="1-3m">1 – 3 months</option>
                <option value="4-6m">4 – 6 months</option>
                <option value="researching">Just researching</option>
              </select>
            </div>
            <div class="ff">
              <label>Anything else? <span style="font-weight:400;opacity:0.6;">(optional)</span></label>
              <textarea name="message" placeholder="Tell us about your home…"></textarea>
            </div>
          </div>
          <div class="form-foot">
            <button type="submit" class="btn-submit" id="suburb-submit">Send Quote Request</button>
            <p class="form-note">No spam. We'll only contact you about your enquiry.</p>
          </div>
        </form>
      </div>
    </aside>

  </main>

  <!-- ═══ FOOTER ═══ -->
  <footer class="ftr">
    <div class="ftr__inner">
      <img src="../brand_assets/HelioFlo_Logo.svg" alt="HelioFlo" class="ftr__logo">
      <div class="ftr__links">
        <a href="/#why">Why HelioFlo</a>
        <a href="/#products">Products</a>
        <a href="/#process">Our Process</a>
        <a href="/#faq">FAQ</a>
        <a href="/payment">Payment Terms</a>
        <a href="/privacy">Privacy Policy</a>
        <a href="/complaints">Complaints Policy</a>
      </div>
      <div class="ftr__contact">
        <a href="tel:0414146027">0414 146 027</a>
        <a href="mailto:hello@helioflo.com">hello@helioflo.com</a>
      </div>
      <p class="ftr__copy">&copy; 2026 HelioFlo. All rights reserved. Servicing Sydney, NSW.</p>
    </div>
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
