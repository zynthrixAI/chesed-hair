"""Render the static preview site from src/ into the repo root.

    python3 src/build.py

Pages use Shopify-style URLs (/collections/<handle>/, /products/<handle>/, /pages/<handle>/)
so the structure carries over to the real store.
"""
import hashlib, json, os, shutil, time
from jinja2 import Environment, FileSystemLoader, select_autoescape
import data as D

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")),
                  autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

_img_v = {}
def img(file, w):
    """Photo address with a short fingerprint of the file, so browsers fetch a photo again when it changes
    (the host tells browsers to keep photos for 7 days)."""
    path = os.path.join(ROOT, "assets", "p", f"{file}-{w}.webp")
    if path not in _img_v:
        _img_v[path] = hashlib.md5(open(path, "rb").read()).hexdigest()[:8] if os.path.exists(path) else "0"
    return f"/assets/p/{file}-{w}.webp?v={_img_v[path]}"
env.globals["img"] = img

products = D.build_products()
D.COLOR_COLLECTIONS[:] = D.make_color_collections(products)
extras = D.build_extras()
soon_kinds = {ec["kind"] for ec in D.EXTRA_COLLECTIONS if ec.get("coming_soon")}
extras = [x for x in extras if x["kind"] not in soon_kinds]   # e.g. hair bundles: "coming soon" for now
for _ec in D.EXTRA_COLLECTIONS:   # count and thumbnail for the menu cards
    _pool = [x for x in extras if x["kind"] == _ec["kind"]]
    _ec["count"] = len(_pool)
    _ec["thumb"] = next((x["images"][0] for x in _pool if not x["placeholder"]), _pool[0]["images"][0] if _pool else dict(file="placeholder", alt=""))
by_handle = {p["handle"]: p for p in products}
fam = {cc["slug"]: cc for cc in D.COLOR_COLLECTIONS}
color_to_cc = {k: cc for cc in D.COLOR_COLLECTIONS for k in cc["colors"]}

def length_photo(key):
    """One length photo with the height of each length line, in % of the photo (18" at 500px of 1200, 30px an inch)."""
    ph = next(c for c in D.LENGTH_PHOTOS if c["key"] == key)
    return dict(ph, file=f"length-{key}", lines=[dict(len=L, y=round((500 + (L - ph["up"] - 18) * 30) / 12, 2)) for L in D.LENGTHS])

def landmarks(curly):
    return D.CURLY_LANDMARKS if curly else D.LANDMARKS

for p in products:
    p["siblings"] = [q for q in products if q["texture"]["key"] == p["texture"]["key"]]
    p["same_color"] = [q for q in products if q["color"]["key"] == p["color"]["key"] and q["handle"] != p["handle"]]
    p["color_collection"] = color_to_cc[p["color"]["key"]]
    p["landmark_for"] = landmarks(p["texture"]["curly"])
    p["length_photo"] = length_photo(D.length_photo_key(p["texture"]))

def find(texture, color):
    return next(p for p in products if p["texture"]["key"] == texture and p["color"]["key"] == color)

POSES = ["1-front", "2-three-quarter", "3-back", "4-side", "5-fingers", "6-lifestyle"]

def pose_img(p, n):
    """A wig's photo by pose (0 front, 1 three-quarter, 2 back, 3 side, 4 fingers, 5 lifestyle), falling back to its first photo.
    The first photo in p["images"] is the cover, so never use list position for a specific pose."""
    return next((im for im in p["images"] if f"-{POSES[n]}" in im["file"]), p["images"][0])

def shot(texture, color, n):
    return pose_img(find(texture, color), n)

def img_like(p, *words):
    for im in p["images"]:
        if all(w in im["file"] for w in words):
            return im
    return p["images"][0]

# texture tiles (menu + homepage): 1B where it exists
for t in D.TEXTURES:
    pool = [p for p in products if p["texture"]["key"] == t["key"]]
    tp = next((p for p in pool if p["color"]["key"] == "1B"), pool[0])
    t["tile"] = pose_img(tp, 1)
    t["product"] = tp

home_textures = [t for t in D.TEXTURES if not t["tile"].get("placeholder")]
NUM = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}
n_tex_word = NUM.get(len(D.TEXTURES), str(len(D.TEXTURES)))

hero_product = find("Body Wave", "1B")
hero = img_like(hero_product, "6-lifestyle")
# the most striking editorial shots: side panes frame the centre one
hero = shot("Body Wave", "530", 1)
hero_imgs = [shot("Straight", "1B", 1),      # the client's favourite leads
             dict(file="banner-curly-burgundy", alt="Long burgundy curly lace front wig on a smiling model in a sage hoodie"),
             dict(file="banner-curly-black", alt="Long black curly lace front wig on a model in an orange knit sweater")]
banner_texture = D.TEX["Kinky Straight"]
banner_imgs = [shot("Kinky Straight", "350", 1), shot("Kinky Straight", "530", 1)]

def banner_for(pool):
    """Three images for a collection banner: different products, first image each."""
    picks, seen = [], set()
    pool = [p for p in pool if not p.get("placeholder")] or pool     # real photos first
    spread = [pool[0], pool[len(pool) // 2], pool[-1]] + pool    # first, middle, last: three different looks
    for p in spread:
        if p["handle"] not in seen:
            picks.append(pose_img(p, 1)); seen.add(p["handle"])
        if len(picks) == 3: break
    i = 1
    while len(picks) < 3 and i < len(pool[0]["images"]):
        picks.append(pool[0]["images"][i]); i += 1
    while len(picks) < 3:
        picks.append(picks[-1])
    return picks
theater = []
for c in D.COLORS:
    p = find("Body Wave", c["key"])
    cc = color_to_cc[c["key"]]
    theater.append(dict(color=c, product=p, img=pose_img(p, 1), family_slug=cc["slug"], family_name=cc["name"]))

best = [find(*k) for k in [("Body Wave", "1B"), ("Body Wave", "530"), ("Straight", "1B"),
                           ("Kinky Straight", "1B"), ("Loose Deep", "350"), ("Straight", "Honey Blonde"),
                           ("Body Wave", "Honey Auburn"), ("Virgin Curl", "Virgin")]]
look_keys = [("Straight", "Red"), ("Loose Deep", "Honey Auburn"), ("Kinky Straight", "350"), ("Virgin Curl", "1B"),
             ("Body Wave", "Honey Blonde"), ("Kinky Curly", "530"), ("Straight", "1"), ("Loose Deep", "Natural Auburn")]
lookbook = []
for k in look_keys:
    p = find(*k)
    lookbook.append(dict(product=p, img=pose_img(p, 1)))
all_tile = [shot("Straight", "Red", 1), shot("Body Wave", "Honey Blonde", 1), shot("Loose Deep", "350", 1), shot("Kinky Straight", "530", 1)]
# home: texture spotlight with a shade switcher (every shade of the banner texture)
spotlight = [dict(color=p["color"], img=pose_img(p, 1), url=p["url"], price=p["price"]) for p in products if p["texture"]["key"] == banner_texture["key"]]
spot_start = next(i for i, x in enumerate(spotlight) if x["color"]["key"] == "1B")
story = shot("Body Wave", "Honey Auburn", 5)      # warm, smiling: the "lovingkindness" photo

# FAQs: wig questions on wig pages, crochet questions on crochet pages, a general mix on the homepage and the FAQ page
WIG_FAQ = [
    ("What are Chesed wigs made of?", "Every Chesed wig is 100% unprocessed virgin Remy human hair on a lace front, so you can color, heat-style and wash it like your own hair."),
    ("What lace and cap do the wigs have?", "A 13x5 lace front for a natural hairline, on a cap that is one size fits all."),
    ("How do I choose my length?", "Use the length guide: it shows where each length from 18 to 36 inches ends on the body. Waves and curls sit about 2 inches higher than straight hair."),
    ("How do I choose my shade?", "Every shade is shown on the same model in real rooms. The color guide puts all ten side by side, including the ones people mix up, like 1B vs 1."),
    ("What if the wig isn't right?", "Return or exchange unused wigs within 30 days with the lace uncut. Your first US return label is free."),
]
SHIP_FAQ = [
    ("How fast is shipping?", f"Orders ship within 1 business day by express shipping and usually arrive in 2 to 6 business days. US shipping is free on orders over ${int(D.FREE_SHIP)}."),
    ("Can I cancel my order?", "Email us within 1 hour of ordering. Once an order has shipped it can't be cancelled, but you can return it."),
    ("What is your return policy?", "Return or exchange unused hair within 30 days of receiving it, in its original packaging. Wigs must have the lace uncut. Email us your order number and a few photos to start, and your first US return label is free."),
    ("Can I pay in instalments?", "Yes. Choose Shop Pay at checkout to pay in 4 interest-free payments."),
]
GENERAL_FAQ = [
    ("What is Chesed hair made of?", "Our lace front wigs and our crochet and feather extensions are all human hair. The wigs are 100% unprocessed virgin Remy hair, so you can color, heat-style and wash them like your own."),
    ("Should I choose a wig or crochet extensions?", "A lace front wig is a complete look you put on and take off in minutes. Crochet and feather extensions are installed into your own braids with a crochet needle, for a light, seamless look that stays in day and night. Not sure? Email us and we'll help you choose."),
    ("Can I dye or restyle Chesed hair?", "Our wigs can be dyed, bleached and permed like your own hair. Crochet and feather extensions are already styled and colored, so we don't recommend dyeing them."),
]
home_faq = GENERAL_FAQ[:2] + [
    ("How do I choose my shade and length?", "For wigs, the color guide shows all ten shades on the same model, and the length guide shows where every length from 18 to 36 inches ends on the body. For crochet, each product page shows every color on a model, in lengths from 12 to 22 inches."),
    SHIP_FAQ[0],
    ("What if it isn't right?", "Return or exchange unused hair within 30 days, in its original packaging (wigs with the lace uncut). Your first US return label is free."),
]
crochet_ec = next(ec for ec in D.EXTRA_COLLECTIONS if ec["kind"] == "crochet")
FAQ_PAGE = [("general", "General", GENERAL_FAQ), ("wigs", "Lace front wigs", WIG_FAQ),
            ("crochet", "Crochet & feather extensions", [f for f in crochet_ec["faq"] if "ship" not in f[0].lower()]),
            ("shipping", "Shipping & returns", SHIP_FAQ)]

# crochet on the homepage, the all-wigs page and wig pages
crochet = [x for x in extras if x["kind"] == "crochet"]
crochet_textures = [dict(name=n, url=f"/collections/{crochet_ec['slug']}/?texture={sl}") for sl, n in D.CROCHET_TEXTURES if any(sl in x["textures"] for x in crochet)]
crochet_promo = dict(name=crochet_ec["name"], url=f"/collections/{crochet_ec['slug']}/", img=crochet[0]["images"][0],
                     min_price=min(x["price"] for x in crochet), count=len(crochet), textures=crochet_textures)
for p in products:   # crochet in the same texture first
    p["crochet"] = sorted(crochet, key=lambda x: p["texture"]["slug"] not in x["textures"])[:4]
bundle_ec = next(ec for ec in D.EXTRA_COLLECTIONS if ec["kind"] == "bundle")
home_cats = [dict(name="Lace Front Wigs", url="/collections/wigs/", img=shot("Body Wave", "Honey Blonde", 5),
                  sub=f"{len(D.TEXTURES)} textures, 10 shades, 18 to 36 inches"),
             dict(name=crochet_ec["name"], url=crochet_promo["url"], crop=True,   # crochet photos are model + product side by side: show the model
                  img=dict(file="seamless-burmese-curly-feather-crochet-braid-hair-extensions-4", alt="Model wearing Burmese curly feather crochet extensions"),
                  sub=f"{len(crochet)} handmade styles, 12 to 22 inches"),
             dict(name=bundle_ec["name"], url=f"/collections/{bundle_ec['slug']}/", img=None, soon=bool(bundle_ec.get("coming_soon")),
                  sub="Body wave, straight, deep wave and water wave")]

# ---- strand chart (length visualizer) ----
import math
from markupsafe import Markup
ROW_Y = [40 + k * 25 for k in range(12)]          # landmark rows: chin ... upper thighs
def _strand_path(x, top, y_end, curly):
    if not curly:
        return f"M{x} {top}V{y_end}"
    pts = [f"M{x} {top}"]
    y = top
    while y < y_end:
        y = min(y_end, y + 3)
        pts.append(f"L{x + 5 * math.sin((y - top) / 18 * 2 * math.pi):.1f} {y}")
    return "".join(pts)

def strands(sel=6, hair="#1A1A1C", uid="s", show_curly=False, interactive=True, both=True, lengths=D.LENGTHS):
    W, top, x0, gap = 640, 22, 168, 40
    out = [f'<svg class="strands{" curly" if show_curly else ""}" viewBox="0 0 {W} 340" role="img" aria-label="Chart of where each wig length ends on the body" style="--hair:{hair}" data-strands="{uid}">']
    out.append('<g class="st-guides">')
    for k, lab in enumerate(D.LANDMARKS):
        y = ROW_Y[k]
        out.append(f'<g class="gd" data-k="{k}"><line x1="{x0 - 22}" x2="{W - 8}" y1="{y}" y2="{y}"/><text x="0" y="{y + 4}">{lab.capitalize()}</text></g>')
    out.append(f'<line class="crown" x1="{x0 - 22}" x2="{W - 8}" y1="{top}" y2="{top}"/></g>')
    for i, L in enumerate(lengths):
        x = x0 + i * gap
        ys = ROW_Y[i]
        yc = ROW_Y[i - 1] if i > 0 else ROW_Y[0] - 14
        cls = "st sel" if i == sel else "st"
        attrs = f' data-i="{i}" tabindex="0" role="button" aria-label="{L} inches"' if interactive else ""
        out.append(f'<g class="{cls}" style="--i:{i}"{attrs}><rect class="hit" x="{x - 18}" y="0" width="36" height="340"/>')
        out.append(f'<text class="lab" x="{x}" y="12">{L}"</text>')
        if both or not show_curly:
            out.append(f'<path class="p-s" pathLength="1" d="{_strand_path(x, top, ys, False)}"/><circle class="tip p-s" cx="{x}" cy="{ys}" r="4"/>')
        if both or show_curly:
            out.append(f'<path class="p-c" pathLength="1" d="{_strand_path(x, top, yc, True)}"/><circle class="tip p-c" cx="{x}" cy="{yc}" r="4"/>')
        out.append('</g>')
    out.append('</svg>')
    return Markup("".join(out))

G = dict(length_photos=[length_photo(c["key"]) for c in D.LENGTH_PHOTOS], lengths=D.LENGTHS, default_length=D.DEFAULT_LENGTH, len_landmarks=D.LANDMARKS, len_curly_landmarks=D.CURLY_LANDMARKS,
         textures=D.TEXTURES, color_collections=D.COLOR_COLLECTIONS, colmap=D.COL, free_ship=D.FREE_SHIP,
         version=str(int(time.time())), macros=None, extras=extras, extra_collections=D.EXTRA_COLLECTIONS)
env.globals.update(G)
env.globals["strands"] = strands

# ---- welcome wheel ----
def wheel():
    n, r, cx = len(D.SPIN_PRIZES), 150, 160
    fills = ["#0E0E10", "#EE467C", "#FBFAF9", "#B8295A", "#26262B", "#F7E9EE"]
    inks = ["#FBFAF9", "#0E0E10", "#0E0E10", "#FBFAF9", "#FBFAF9", "#0E0E10"]
    out = [f'<svg class="wheel" viewBox="0 0 320 320" aria-hidden="true"><g id="wheelSpin">']
    for i, pz in enumerate(D.SPIN_PRIZES):
        a0, a1 = (i / n) * 2 * math.pi - math.pi / 2, ((i + 1) / n) * 2 * math.pi - math.pi / 2
        x0, y0, x1, y1 = cx + r * math.cos(a0), cx + r * math.sin(a0), cx + r * math.cos(a1), cx + r * math.sin(a1)
        out.append(f'<path d="M{cx} {cx}L{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{fills[i % 6]}" stroke="#0E0E10" stroke-width="1"/>')
        mid = (i + .5) * 360 / n
        out.append(f'<text transform="rotate({mid:.1f} {cx} {cx}) translate({cx} {cx - r * .62}) rotate({-90 if mid < 180 else 90})" fill="{inks[i % 6]}" text-anchor="middle" dominant-baseline="middle">{pz["label"]}</text>')
    out.append(f'</g><circle cx="{cx}" cy="{cx}" r="22" fill="#FBFAF9" stroke="#0E0E10"/><circle cx="{cx}" cy="{cx}" r="5" fill="#B8295A"/></svg>')
    return Markup("".join(out))
env.globals["wheel"] = wheel
env.globals["whatsapp"] = D.WHATSAPP
env.globals["whatsapp_placeholder"] = D.WHATSAPP_PLACEHOLDER
env.globals["spin_prizes"] = D.SPIN_PRIZES
env.globals["spin_odds"] = ", ".join(f'{p["label"]} {p["weight"]}%' for p in D.SPIN_PRIZES)
assert sum(p["weight"] for p in D.SPIN_PRIZES) == 100
env.globals["reviews"] = D.REVIEWS
env.globals["macros"] = env.get_template("partials/macros.html").module

# Menu: "simple" = text menu that reaches every page; "visual" = the archived Round 3 image mega menu
HEADER = "simple"
env.globals["header_style"] = HEADER
env.globals["nav_textures"] = [dict(t, products=[p for p in products if p["texture"]["key"] == t["key"]]) for t in D.TEXTURES]
NAV_NAMES = {"crochet": "Crochet & Feather", "bundle": "Hair Bundles"}
NAV_BLURBS = {"crochet": "Handmade feather and crochet braid extensions in human hair: body wave, deep wave, water wave, wet & wavy and more.",
              "bundle": "Body wave, straight, deep wave and water wave bundles, from natural darks to bold colors."}
nav_extras = []
for _ec in D.EXTRA_COLLECTIONS:
    _pool = [x for x in extras if x["kind"] == _ec["kind"]]
    _real = [x for x in _pool if not x["placeholder"]]
    nav_extras.append(dict(_ec, nav_name=NAV_NAMES[_ec["kind"]], blurb=NAV_BLURBS[_ec["kind"]], cards=bool(_real), soon=bool(_ec.get("coming_soon")),
                           picks=(_real or _pool)[:6] if _real else _pool))
for _n in nav_extras:
    if _n["kind"] == "crochet":
        _pool = [x for x in extras if x["kind"] == "crochet"]
        _n["textures"] = [dict(name=n, count=c, url=f"/collections/{_n['slug']}/?texture={s}") for s, n in D.CROCHET_TEXTURES if (c := sum(1 for x in _pool if s in x["textures"]))]
        _n["colors"] = [dict(name=n, hex=h, count=c, url=f"/collections/{_n['slug']}/?color={s}") for s, n, h in D.CROCHET_COLORS if (c := sum(1 for x in _pool if s in x["colors"]))]
        _n["picks"] = _n["picks"][:4]
env.globals["nav_extras"] = nav_extras
env.globals["nav_wig_count"] = len(products)
env.globals["wig_feature"] = shot("Body Wave", "530", 1)
SIMPLE_PAGES = ["about", "faq", "shipping", "returns", "contact"]
# home + all-wigs hub + texture, color and extra collections + wigs and extras + 2 guides + simple pages + site map
env.globals["page_count"] = 2 + len(D.TEXTURES) + len(D.COLOR_COLLECTIONS) + len(D.EXTRA_COLLECTIONS) + len(products) + len(extras) + 2 + len(SIMPLE_PAGES) + 1

written = []
def render(template, path, **ctx):
    html = env.get_template(template).render(**ctx)
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(html)
    written.append(path)

def org_ld():
    return {"@context": "https://schema.org", "@type": "Organization", "name": "Chesed Hair Collection",
            "url": "https://chesedhair.com", "logo": "https://chesedhair.com/favicon.svg"}

# HOME
render("index.html", "/", seo_title="Chesed Hair | Human Hair Lace Front Wigs & Crochet Extensions",
       seo_description=f"Lace front wigs in 100% unprocessed virgin Remy human hair, {len(D.TEXTURES)} textures and 10 shades from 18 to 36 inches, plus handmade crochet and feather extensions.",
       canonical="/", body_class="home overlay", page_id="home", hero=hero, hero_product=hero_product, hero_imgs=hero_imgs, banner_imgs=banner_imgs, banner_texture=banner_texture, all_tile=all_tile, theater=theater,
       best=best, home_textures=home_textures, n_tex_word=n_tex_word, n_home_tex_word=NUM.get(len(home_textures), str(len(home_textures))), lookbook=lookbook, story=story, spotlight=spotlight, spot_start=spot_start, home_faq=home_faq, home_cats=home_cats, crochet_promo=crochet_promo, crochet_picks=crochet[:4], jsonld=json.dumps(org_ld()),
       og_image=img(hero['file'], 1024))

# COLLECTIONS
def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://chesedhair.com" + u} for i, (n, u) in enumerate(items)]}

def color_filters(pool):
    out = []
    for c in D.COLORS:
        n = sum(1 for p in pool if p["color"]["key"] == c["key"])
        if n: out.append(dict(value=c["slug"], label=c["key"], hex=c["hex"], count=n))
    return out

def texture_filters(pool):
    out = []
    for t in D.TEXTURES:
        n = sum(1 for p in pool if p["texture"]["key"] == t["key"])
        if n: out.append(dict(value=t["slug"], label=t["name"], hex=None, count=n))
    return out

def crochet_facets(pool):
    tex = [dict(value=s, label=n, hex=None, count=c) for s, n in D.CROCHET_TEXTURES if (c := sum(1 for x in pool if s in x["textures"]))]
    col = [dict(value=s, label=n, hex=h, count=c) for s, n, h in D.CROCHET_COLORS if (c := sum(1 for x in pool if s in x["colors"]))]
    return [dict(key="texture", label="Texture", options=tex), dict(key="color", label="Shade", options=col)]

def facets(pool):
    """Filter groups for a collection: only groups with more than one option. Extras have no texture or shade."""
    if pool and pool[0].get("kind", "wig") == "crochet":
        return crochet_facets(pool)
    if pool and pool[0].get("kind", "wig") != "wig":
        return []
    out = [dict(key="texture", label="Texture", options=texture_filters(pool)),
           dict(key="color", label="Shade", options=color_filters(pool))]
    return [f for f in out if len(f["options"]) > 1]
env.globals["facets"] = facets

def split_intro(text, n=2):
    """First n sentences as the lead, the rest behind Read more."""
    import re as _re
    parts = _re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:n]), " ".join(parts[n:])
env.globals["split_intro"] = split_intro

tex_related = [dict(label=t["name"], url=f"/collections/{t['slug']}-wigs/") for t in D.TEXTURES]
crochet_pill = dict(label=crochet_ec["name"], url=f"/collections/{crochet_ec['slug']}/")
col_related = [dict(label=cc["name"], url=f"/collections/{cc['slug']}-wigs/", hex=D.COL[cc["colors"][0]]["hex"]) for cc in D.COLOR_COLLECTIONS]

hub = dict(h1="Lace Front Wigs", intro=f"Every Chesed wig in one place: {len(D.TEXTURES)} textures and 10 shades of lace front wigs in 100% unprocessed virgin Remy human hair, each available from 18 to 36 inches. All of them are shown on the same model, so you can compare textures and shades fairly. Filter by texture and shade below to narrow it down.",
           products=products, filters=texture_filters(products), filter_key="texture", filter_label="Texture", image=None,
           faq=WIG_FAQ, related_heading="Shop by color", related=col_related + [crochet_pill], also=crochet_promo,
           banner=[shot("Straight", "Red", 1), shot("Body Wave", "530", 1), shot("Loose Deep", "Honey Blonde", 1)])
render("collection.html", "/collections/wigs/", seo_title=f"Lace Front Wigs in {len(D.TEXTURES)} Textures & 10 Colors | Chesed",
       seo_description="Shop all Chesed lace front wigs: body wave, kinky curly, kinky straight, loose deep wave, straight, permed straight, wet & wavy, deep wave and virgin curl, in 10 shades, 18 to 36 inches.",
       canonical="/collections/wigs/", body_class="shop overlay", page_id="hub", c=hub, is_hub=True, card_lead="texture",
       jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Lace Front Wigs", "/collections/wigs/")])))

TEX_TITLES = {"permed-straight": "Permed Straight Lace Front Wigs | Chesed", "wet-and-wavy": "Wet & Wavy Lace Front Wigs | Chesed",
              "deep-wave": "Deep Wave Lace Front Wigs | Chesed",
              "body-wave": "Body Wave Lace Front Wigs, 18-36 Inch | Chesed",
              "kinky-curly": "Kinky Curly Lace Front Wigs | Chesed Hair", "kinky-straight": "Kinky Straight Wigs, Yaki Texture | Chesed",
              "loose-deep-wave": "Loose Deep Wave Lace Front Wigs | Chesed", "straight": "Silky Straight Lace Front Wigs | Chesed",
              "virgin-curl": "Virgin Curl Human Hair Wigs | Chesed Hair"}
for t in D.TEXTURES:
    pool = [p for p in products if p["texture"]["key"] == t["key"]]
    c = dict(h1=f"{t['name']} Wigs", intro=t["intro"], products=pool, filters=color_filters(pool), filter_key="color",
             filter_label="Color", image=t["tile"], faq=t["faq"], related_heading="Other textures", banner=banner_for(pool),
             related=[r for r in tex_related if r["label"] != t["name"]] + col_related + [crochet_pill])
    url = f"/collections/{t['slug']}-wigs/"
    render("collection.html", url, seo_title=TEX_TITLES[t["slug"]], seo_description=t["intro"][:155].rsplit(" ", 1)[0] + "…",
           canonical=url, body_class="shop overlay", page_id=t["slug"], c=c, is_hub=False,
           jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Wigs", "/collections/wigs/"), (c["h1"], url)])))

for cc in D.COLOR_COLLECTIONS:
    pool = [p for p in products if p["color"]["key"] in cc["colors"]]
    img_p = pool[0]
    c = dict(h1=cc["h1"], intro=cc["intro"], products=pool, filters=texture_filters(pool), filter_key="texture",
             filter_label="Texture", image=img_p["images"][0], faq=cc["faq"], related_heading="Other colors", banner=banner_for(pool),
             related=[r for r in col_related if r["label"] != cc["name"]] + tex_related + [crochet_pill])
    url = f"/collections/{cc['slug']}-wigs/"
    render("collection.html", url, seo_title=cc["title"], seo_description=cc["intro"][:155].rsplit(" ", 1)[0] + "…",
           canonical=url, body_class="shop overlay", page_id=cc["slug"], c=c, is_hub=False, card_lead="texture",
           jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Wigs", "/collections/wigs/"), (c["h1"], url)])))

# PRODUCTS
for p in products:
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["title"], "brand": {"@type": "Brand", "name": "Chesed Hair"},
          "image": [f"https://chesedhair.com/assets/p/{im['file']}-1024.webp" for im in p["images"]],
          "description": f"{p['color']['blurb']} {p['texture']['short']}", "color": p["color"]["key"],
          "offers": [{"@type": "Offer", "name": f'{v["length"]} inch', "price": f'{v["price"]:.2f}', "priceCurrency": "USD",
                      "availability": "https://schema.org/InStock", "url": f"https://chesedhair.com{p['url']}?length={v['length']}"} for v in p["variants"]]}
    render("product.html", p["url"], seo_title=f"{p['title']} | Chesed",
           seo_description=f"{p['title']} in 100% unprocessed virgin Remy human hair. {p['color']['blurb']} 18 to 36 inches.",
           canonical=p["url"], body_class="shop pdp-page", page_id=p["handle"], p=p, og_type="product",
           og_image=img(p['images'][0]['file'], 1024),
           jsonld=json.dumps([ld, breadcrumb_ld([("Home", "/"), (f"{p['texture']['name']} Wigs", f"/collections/{p['texture']['slug']}-wigs/"), (p["title"], p["url"])])]))

# EXTRA COLLECTIONS (crochet & feather extensions, hair bundles)
for ec in D.EXTRA_COLLECTIONS:
    pool = [x for x in extras if x["kind"] == ec["kind"]]
    if ec.get("coming_soon"):
        c = dict(h1=ec["h1"], intro=ec["intro"], products=[], kind=ec["kind"], noun=ec["noun"], coming_soon=True, faq=[], filters=[],
                 banner=[shot("Straight", "1B", 5), shot("Body Wave", "530", 1), shot("Straight", "Honey Blonde", 1)], related_heading="Shop now",
                 related=[dict(label="All wigs", url="/collections/wigs/")] + [dict(label=o["name"], url=f"/collections/{o['slug']}/") for o in D.EXTRA_COLLECTIONS if not o.get("coming_soon")])
        url = f"/collections/{ec['slug']}/"
        render("collection.html", url, seo_title=ec["title"], seo_description=ec["intro"][:155].rsplit(" ", 1)[0] + "…",
               canonical=url, body_class="shop overlay", page_id=ec["slug"], c=c, is_hub=False,
               jsonld=json.dumps(breadcrumb_ld([("Home", "/"), (c["h1"], url)])))
        continue
    real = [x for x in pool if not x["placeholder"]] or pool
    opt_name, label = ("Color", "shades") if ec["kind"] == "bundle" else ("Length", "lengths")
    facts = dict(options=len({v for x in pool for o in x["options"] if o["name"] == opt_name for v in o["values"]}), options_label=label,
                 min_price=min(x["price"] for x in pool), price_ph=any(x["price_placeholder"] for x in pool))
    banner = []
    for x in real:
        if len(banner) < 3 and x["images"][0]["file"] not in [b["file"] for b in banner]:
            banner.append(x["images"][0])
    while len(banner) < 3:
        banner.append(banner[-1] if banner else dict(file="placeholder", alt=""))
    c = dict(h1=ec["h1"], intro=ec["intro"], products=pool, kind=ec["kind"], noun=ec["noun"], facts=facts, filters=[], filter_key="",
             filter_label="", image=banner[0], faq=ec["faq"], related_heading="Keep exploring", banner=banner,
             related=[dict(label="All wigs", url="/collections/wigs/")] + [dict(label=o["name"], url=f"/collections/{o['slug']}/") for o in D.EXTRA_COLLECTIONS if o["kind"] != ec["kind"]] + tex_related)
    url = f"/collections/{ec['slug']}/"
    render("collection.html", url, seo_title=ec["title"], seo_description=ec["intro"][:155].rsplit(" ", 1)[0] + "…",
           canonical=url, body_class="shop overlay", page_id=ec["slug"], c=c, is_hub=False,
           jsonld=json.dumps(breadcrumb_ld([("Home", "/"), (c["h1"], url)])))

for x in extras:
    lo, hi = min(v["price"] for v in x["variants"]), max(v["price"] for v in x["variants"])
    ld = {"@context": "https://schema.org", "@type": "Product", "name": x["title"], "brand": {"@type": "Brand", "name": "Chesed Hair"},
          "image": [f"https://chesedhair.com/assets/p/{im['file']}-1024.webp" for im in x["images"]],
          "description": f"{x['title']} from Chesed Hair.",
          "offers": {"@type": "AggregateOffer", "lowPrice": f"{lo:.2f}", "highPrice": f"{hi:.2f}", "priceCurrency": "USD",
                     "offerCount": len(x["variants"]), "availability": "https://schema.org/InStock"}}
    render("extra.html", x["url"], seo_title=f"{x['title']} | Chesed",
           seo_description=f"{x['title']}. Choose your options and add to bag. {x['collection']['name']} from Chesed Hair.",
           canonical=x["url"], body_class="shop pdp-page", page_id=x["handle"], p=x, og_type="product",
           og_image=img(x['images'][0]['file'], 1024),
           jsonld=json.dumps([ld, breadcrumb_ld([("Home", "/"), (x["collection"]["name"], f"/collections/{x['collection']['slug']}/"), (x["title"], x["url"])])]))

# PAGES
render("length_guide.html", "/pages/wig-length-guide/", seo_title="Wig Length Chart, 18-36 Inch on a Model | Chesed",
       seo_description="See where every wig length from 18 to 36 inches ends on the body, for straight and curly textures.",
       canonical="/pages/wig-length-guide/", body_class="shop", page_id="lg", lengths=D.LENGTHS, landmarks=D.LANDMARKS, curly_landmarks=D.CURLY_LANDMARKS,
       page=dict(h1="Wig Length Chart: 18 to 36 Inches", lede="Where each length ends on the body, for straight and for curly textures."))
render("color_guide.html", "/pages/wig-color-guide/", seo_title="Wig Color Chart: 10 Shades on Deep Skin | Chesed",
       seo_description="All 10 Chesed wig colors on the same model: 1, 1B, Virgin, 530, 99J, 350, Honey Auburn, Natural Auburn, Honey Blonde and Red.",
       canonical="/pages/wig-color-guide/", body_class="shop", page_id="cg", theater=theater,
       page=dict(h1="Wig Colors on Deep Skin", lede="All ten shades on the same model, so you can compare them fairly."))

simple_pages = [
    ("about", "About Chesed Hair", "About Chesed Hair", "Chesed means lovingkindness.",
     # story text from chesedhair.com (client asked for it, 22 October 2026)
     "<h2>More than a name</h2><p>\"Chesed\" is a Hebrew word meaning <b>lovingkindness</b>: a deep, unconditional love.</p>"
     "<p>It reflects our belief that beauty should come from a place of care, intention, and authenticity.</p><p>We don't just create products. We create with purpose.</p>"
     "<h2>Effortless from start to finish</h2><ul><li>Instant volume with a soft, natural flow</li><li>Easy installation, easy removal</li>"
     "<li>Designed for everyday wear and long-lasting comfort</li><li>Moves like real hair, because it is</li></ul>"
     "<h2>Care and versatility</h2><p>Chesed hair can be dyed, bleached and permed.</p>"
     "<h2>Our ethical commitment</h2><p>We believe beauty should never come at the cost of people.</p>"
     "<p>Our products are created in hygienic facilities that meet high ethical standards, <b>with no labor exploitation.</b></p>"
     ""),
    ("faq", "FAQ: Wigs, Crochet, Shipping & Returns | Chesed Hair", "Frequently Asked Questions", "Choosing, wearing and caring for your wig or crochet extensions.",
     "".join(f"<h2 id='{key}'>{name}</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in items) for key, name, items in FAQ_PAGE)),
    # shipping and returns follow LUVME's terms, as the client asked (23 October 2026)
    ("shipping", "Shipping | Chesed Hair", "Shipping", "Ships within 24 hours. Arrives in 2 to 6 business days.", "<h2>Processing</h2><p>Orders ship within 1 business day (24 hours) of payment, Monday to Friday. You get a confirmation email when you order and a tracking link when it ships.</p><h2>Delivery</h2><p>Every order ships by express shipping and usually arrives in 2 to 6 business days. Allow 2 to 3 extra days around weekends, holidays and busy periods.</p><h2>Shipping cost</h2><p>Free US shipping on orders over ${fs}.</p><h2>Cancelling an order</h2><p>Email us within 1 hour of placing your order to cancel it. Once an order has shipped it can't be cancelled, but you can return it.</p><h2>Questions about your delivery</h2><p>Email <a href='mailto:info@chesedhair.com'>info@chesedhair.com</a> with your order number. If there is a problem or delay we'll email you.</p>".replace("{fs}", str(int(D.FREE_SHIP)))),
    ("returns", "Returns | Chesed Hair", "Returns & Exchanges", "30 days to return or exchange unused hair.", "<h2>30-day returns and exchanges</h2><p>You can return or exchange unused hair within 30 days of receiving it.</p><h2>What we can accept</h2><ul><li>Hair in its original condition: not worn, washed, cut, dyed, bleached or styled.</li><li>Lace untouched: not cut or trimmed.</li><li>Original packaging, with any tags.</li></ul><p>Hair touches the scalp, so for hygiene we can't accept used items.</p><h2>How to start a return</h2><p>Email <a href='mailto:info@chesedhair.com'>info@chesedhair.com</a> with your order number, the reason and a few photos of the item. Once we approve it we'll send the return address. Returns sent without approval can't be refunded.</p><h2>Return shipping</h2><p>Each US order gets one free prepaid return label. After that, return shipping is paid by you. If we sent the wrong item or it arrived damaged, we cover the return.</p><h2>Refunds</h2><p>We refund to your original payment method within 2 business days of receiving and checking your return. Card refunds can take up to 10 business days to show; Shop Pay instalments and PayPal usually take about 3.</p><h2>Exchanges</h2><p>Same steps as a return. Your new item ships within 3 business days of your return arriving.</p>"),
    ("contact", "Contact | Chesed Hair", "Contact", None, "<p>Email <a href='mailto:info@chesedhair.com'>info@chesedhair.com</a>. We reply within 1 business day.</p>"),
]
PAGE_STEPS = {
    "shipping": [("bag", "You order", "Pay in full or in 4 with Shop Pay. You get a confirmation email right away."),
                 ("box", "We pack and ship", "Your order ships within 1 business day, with tracking."),
                 ("home", "It arrives", f"Express delivery in 2 to 6 business days. Free US shipping on orders over ${int(D.FREE_SHIP)}.")],
    "returns": [("chat", "Tell us within 30 days", "Email us your order number, the reason and a few photos. Once approved, we send the return address and a free US label."),
                ("box", "Send it back", "Unused, with the lace uncut and the hair in its original packaging."),
                ("card", "Get your refund", "Refunded to your original payment within 2 business days of it arriving.")],
}
TOC_PAGES = {"faq"}
for handle, title, h1, lede, body in simple_pages:
    render("page.html", f"/pages/{handle}/", seo_title=title, seo_description=lede or h1, canonical=f"/pages/{handle}/",
           body_class="shop", page_id=handle, page=dict(h1=h1, lede=lede, body=body, steps=PAGE_STEPS.get(handle),
           toc=[(key, name) for key, name, _ in FAQ_PAGE] if handle in TOC_PAGES else None))

assert [h for h, *_ in simple_pages] == SIMPLE_PAGES

render("sitemap.html", "/pages/sitemap/", seo_title="All Pages | Chesed Hair", seo_description="Every page on the Chesed Hair site, from collections and wigs to guides and help.",
       canonical="/pages/sitemap/", body_class="shop", page_id="sitemap",
       page=dict(h1="All Pages", lede="Every collection, wig, guide and help page in one place."))

# search index for the header search overlay
idx = [dict(t="All wigs", u="/collections/wigs/", k="Collection", s="lace front wigs all shop")]
idx += [dict(t=f"{t['name']} Wigs", u=f"/collections/{t['slug']}-wigs/", k="Texture", s=t["short"]) for t in D.TEXTURES]
idx += [dict(t=cc["name"], u=f"/collections/{cc['slug']}-wigs/", k="Color", s=" ".join(cc["colors"])) for cc in D.COLOR_COLLECTIONS]
idx += [dict(t=p["title"], u=p["url"], k="Wig", s=f"{p['color']['family']} {p['texture']['short']}", i=img(p['images'][0]['file'], 560), p=p["price"]) for p in products]
idx += [dict(t=ec["name"], u=f"/collections/{ec['slug']}/", k="Collection", s=ec["name"].lower() + " hair") for ec in D.EXTRA_COLLECTIONS]
idx += [dict(t=x["title"], u=x["url"], k=x["collection"]["name"], s=x["kind"] + " hair extensions bundles", i=img(x['images'][0]['file'], 560), p=x["price"]) for x in extras]
idx += [dict(t="Length Guide", u="/pages/wig-length-guide/", k="Guide", s="inches length chart how long"),
        dict(t="Color Guide", u="/pages/wig-color-guide/", k="Guide", s="shade colour chart compare")]
idx += [dict(t=h1, u=f"/pages/{h}/", k="Help", s=lede or "") for h, _, h1, lede, _ in simple_pages]
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
json.dump(idx, open(os.path.join(ROOT, "assets", "search.json"), "w", encoding="utf-8"), separators=(",", ":"))

assert len(written) == env.globals["page_count"], (len(written), env.globals["page_count"])
print(f"Wrote {len(written)} pages")
