"""Render the static preview site from src/ into the repo root.

    python3 src/build.py

Pages use Shopify-style URLs (/collections/<handle>/, /products/<handle>/, /pages/<handle>/)
so the structure carries over to the real store.
"""
import json, os, shutil, time
from jinja2 import Environment, FileSystemLoader, select_autoescape
import data as D

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")),
                  autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

products = D.build_products()
D.COLOR_COLLECTIONS[:] = D.make_color_collections(products)
extras = D.build_extras()
for _ec in D.EXTRA_COLLECTIONS:   # count and thumbnail for the menu cards
    _pool = [x for x in extras if x["kind"] == _ec["kind"]]
    _ec["count"] = len(_pool)
    _ec["thumb"] = next((x["images"][0] for x in _pool if not x["placeholder"]), _pool[0]["images"][0])
by_handle = {p["handle"]: p for p in products}
fam = {cc["slug"]: cc for cc in D.COLOR_COLLECTIONS}
color_to_cc = {k: cc for cc in D.COLOR_COLLECTIONS for k in cc["colors"]}

def landmarks(curly):
    return D.CURLY_LANDMARKS if curly else D.LANDMARKS

for p in products:
    p["siblings"] = [q for q in products if q["texture"]["key"] == p["texture"]["key"]]
    p["same_color"] = [q for q in products if q["color"]["key"] == p["color"]["key"] and q["handle"] != p["handle"]]
    p["color_collection"] = color_to_cc[p["color"]["key"]]
    p["landmark_for"] = landmarks(p["texture"]["curly"])

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
hero_imgs = [shot("Straight", "1B", 1), shot("Straight", "530", 1), shot("Straight", "Honey Blonde", 1)]   # the client's favourite (1B) leads; the others match it: sleek straight, same framing, different wigs
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
                           ("Kinky Straight", "1B"), ("Loose Deep", "350"), ("Curly", "Honey Blonde"),
                           ("Body Wave", "Honey Auburn"), ("Virgin Curl", "Virgin")]]
look_keys = [("Straight", "Red"), ("Loose Deep", "Honey Auburn"), ("Kinky Straight", "350"), ("Curly", "530"),
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

home_faq = [
    ("What are Chesed wigs made of?", "Every Chesed wig is 100% unprocessed virgin Remy human hair on a lace front, so you can color, heat-style and wash it like your own hair."),
    ("How do I choose my length?", "Use the length guide: it shows where each length from 10 to 32 inches ends on the body. Waves and curls sit about 2 inches higher than straight hair."),
    ("How do I choose my shade?", "Every shade is shown on the same model in real rooms. The color guide puts all ten side by side, including the ones people mix up, like 1B vs 1."),
    ("What if the wig isn't right?", "Return unworn wigs within 30 days with the lace uncut."),
]

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

G = dict(textures=D.TEXTURES, color_collections=D.COLOR_COLLECTIONS, colmap=D.COL, free_ship=D.FREE_SHIP,
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
NAV_BLURBS = {"crochet": "Handmade feather and crochet braid extensions in human hair: body wave, deep wave, water wave, kinky curly and more.",
              "bundle": "Body wave, straight, deep wave and water wave bundles, from natural darks to bold colors."}
nav_extras = []
for _ec in D.EXTRA_COLLECTIONS:
    _pool = [x for x in extras if x["kind"] == _ec["kind"]]
    _real = [x for x in _pool if not x["placeholder"]]
    nav_extras.append(dict(_ec, nav_name=NAV_NAMES[_ec["kind"]], blurb=NAV_BLURBS[_ec["kind"]], cards=bool(_real),
                           picks=(_real or _pool)[:6] if _real else _pool))
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
render("index.html", "/", seo_title="Chesed Hair | Human Hair Lace Front Wigs",
       seo_description=f"Lace front wigs in 100% unprocessed virgin Remy human hair. {len(D.TEXTURES)} textures, 10 shades, 10 to 32 inches, all shown on the same model.",
       canonical="/", body_class="home overlay", page_id="home", hero=hero, hero_product=hero_product, hero_imgs=hero_imgs, banner_imgs=banner_imgs, banner_texture=banner_texture, all_tile=all_tile, theater=theater,
       best=best, home_textures=home_textures, n_tex_word=n_tex_word, lookbook=lookbook, story=story, spotlight=spotlight, spot_start=spot_start, home_faq=home_faq, jsonld=json.dumps(org_ld()),
       og_image=f"/assets/p/{hero['file']}-1024.webp")

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

def facets(pool):
    """Filter groups for a collection: only groups with more than one option. Extras have no texture or shade."""
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
col_related = [dict(label=cc["name"], url=f"/collections/{cc['slug']}-wigs/", hex=D.COL[cc["colors"][0]]["hex"]) for cc in D.COLOR_COLLECTIONS]

hub = dict(h1="Lace Front Wigs", intro=f"Every Chesed wig in one place: {len(D.TEXTURES)} textures and 10 shades of lace front wigs in 100% unprocessed virgin Remy human hair, each available from 10 to 32 inches. All of them are shown on the same model, so you can compare textures and shades fairly. Filter by texture and shade below to narrow it down.",
           products=products, filters=texture_filters(products), filter_key="texture", filter_label="Texture", image=None,
           faq=home_faq, related_heading="Shop by color", related=col_related,
           banner=[shot("Straight", "Red", 1), shot("Body Wave", "530", 1), shot("Loose Deep", "Honey Blonde", 1)])
render("collection.html", "/collections/wigs/", seo_title=f"Lace Front Wigs in {len(D.TEXTURES)} Textures & 10 Colors | Chesed",
       seo_description="Shop all Chesed lace front wigs: body wave, curly, kinky curly, kinky straight, loose deep wave, straight, permed straight, wet & wavy and virgin curl, in 10 shades, 10 to 32 inches.",
       canonical="/collections/wigs/", body_class="shop overlay", page_id="hub", c=hub, is_hub=True, card_lead="texture",
       jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Lace Front Wigs", "/collections/wigs/")])))

TEX_TITLES = {"permed-straight": "Permed Straight Lace Front Wigs | Chesed", "wet-and-wavy": "Wet & Wavy Lace Front Wigs | Chesed",
              "body-wave": "Body Wave Lace Front Wigs, 10-32 Inch | Chesed", "curly": "Curly Lace Front Wigs, 10-32 Inch | Chesed",
              "kinky-curly": "Kinky Curly Lace Front Wigs | Chesed Hair", "kinky-straight": "Kinky Straight Wigs, Yaki Texture | Chesed",
              "loose-deep-wave": "Loose Deep Wave Lace Front Wigs | Chesed", "straight": "Silky Straight Lace Front Wigs | Chesed",
              "virgin-curl": "Virgin Curl Human Hair Wigs | Chesed Hair"}
for t in D.TEXTURES:
    pool = [p for p in products if p["texture"]["key"] == t["key"]]
    c = dict(h1=f"{t['name']} Wigs", intro=t["intro"], products=pool, filters=color_filters(pool), filter_key="color",
             filter_label="Color", image=t["tile"], faq=t["faq"], related_heading="Other textures", banner=banner_for(pool),
             related=[r for r in tex_related if r["label"] != t["name"]] + col_related)
    url = f"/collections/{t['slug']}-wigs/"
    render("collection.html", url, seo_title=TEX_TITLES[t["slug"]], seo_description=t["intro"][:155].rsplit(" ", 1)[0] + "…",
           canonical=url, body_class="shop overlay", page_id=t["slug"], c=c, is_hub=False,
           jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Wigs", "/collections/wigs/"), (c["h1"], url)])))

for cc in D.COLOR_COLLECTIONS:
    pool = [p for p in products if p["color"]["key"] in cc["colors"]]
    img_p = pool[0]
    c = dict(h1=cc["h1"], intro=cc["intro"], products=pool, filters=texture_filters(pool), filter_key="texture",
             filter_label="Texture", image=img_p["images"][0], faq=cc["faq"], related_heading="Other colors", banner=banner_for(pool),
             related=[r for r in col_related if r["label"] != cc["name"]] + tex_related)
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
           seo_description=f"{p['title']} in 100% unprocessed virgin Remy human hair. {p['color']['blurb']} 10 to 32 inches.",
           canonical=p["url"], body_class="shop pdp-page", page_id=p["handle"], p=p, og_type="product",
           og_image=f"/assets/p/{p['images'][0]['file']}-1024.webp",
           jsonld=json.dumps([ld, breadcrumb_ld([("Home", "/"), (f"{p['texture']['name']} Wigs", f"/collections/{p['texture']['slug']}-wigs/"), (p["title"], p["url"])])]))

# EXTRA COLLECTIONS (crochet & feather extensions, hair bundles)
for ec in D.EXTRA_COLLECTIONS:
    pool = [x for x in extras if x["kind"] == ec["kind"]]
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
           og_image=f"/assets/p/{x['images'][0]['file']}-1024.webp",
           jsonld=json.dumps([ld, breadcrumb_ld([("Home", "/"), (x["collection"]["name"], f"/collections/{x['collection']['slug']}/"), (x["title"], x["url"])])]))

# PAGES
render("length_guide.html", "/pages/wig-length-guide/", seo_title="Wig Length Chart, 10-32 Inch on a Model | Chesed",
       seo_description="See where every wig length from 10 to 32 inches ends on the body, for straight and curly textures.",
       canonical="/pages/wig-length-guide/", body_class="shop", page_id="lg", lengths=D.LENGTHS, landmarks=D.LANDMARKS, curly_landmarks=D.CURLY_LANDMARKS,
       page=dict(h1="Wig Length Chart: 10 to 32 Inches", lede="Where each length ends on the body, for straight and for curly textures."))
render("color_guide.html", "/pages/wig-color-guide/", seo_title="Wig Color Chart: 10 Shades on Deep Skin | Chesed",
       seo_description="All 10 Chesed wig colors on the same model: 1, 1B, Virgin, 530, 99J, 350, Honey Auburn, Natural Auburn, Honey Blonde and Red.",
       canonical="/pages/wig-color-guide/", body_class="shop", page_id="cg", theater=theater,
       page=dict(h1="Wig Colors on Deep Skin", lede="All ten shades on the same model, so you can compare them fairly."))

simple_pages = [
    ("about", "About Chesed Hair", "About Chesed Hair", "Chesed means lovingkindness.",
     "<p>Chesed is the Hebrew word for a deep, unconditional love. We named the brand after it because that's how hair should be made: with care for the woman who wears it and the people who make it.</p><p>Every Chesed unit starts as 100% unprocessed virgin Remy human hair, sourced and made without exploited labor.</p><p class='ph-note'>Founder story and photos to come from Chesed.</p>"),
    ("faq", "Wig FAQ: Lace, Fit, Shipping | Chesed Hair", "Frequently Asked Questions", "Choosing, wearing and caring for your wig.",
     "".join(f"<h2 id='q{i + 1}'>{q}</h2><p>{a}</p>" for i, (q, a) in enumerate(home_faq)) + "<p class='ph-note'>Shipping, lace, density and cap-size answers will be added once Chesed confirms the details.</p>"),
    ("shipping", "Shipping | Chesed Hair", "Shipping", None, "<p class='ph-note'>Processing times, carriers and international rates to be confirmed by Chesed.</p>"),
    ("returns", "Returns | Chesed Hair", "Returns", None, "<p class='ph-note'>Full return policy to be confirmed by Chesed.</p>"),
    ("contact", "Contact | Chesed Hair", "Contact", None, "<p>Email <a href='mailto:info@chesedhair.com'>info@chesedhair.com</a>. We reply within <span class='ph'>X</span> business days.</p>"),
]
PAGE_STEPS = {
    "shipping": [("bag", "You order", "Pay in full or in 4 with Shop Pay. You get a confirmation email right away."),
                 ("box", "We pack and ship", "Your wig ships within <span class='ph'>X</span> business days, with tracking."),
                 ("home", "It arrives", f"Free US shipping on orders over ${int(D.FREE_SHIP)}. Delivery times <span class='ph'>to confirm</span>.")],
    "returns": [("chat", "Tell us within 30 days", "Email us with your order number. We'll reply with a return label <span class='ph'>(to confirm)</span>."),
                ("box", "Send it back", "Unworn, with the lace uncut and the wig in its original packaging."),
                ("card", "Get your refund", "Refunded to your original payment once it arrives <span class='ph'>(timing to confirm)</span>.")],
}
TOC_PAGES = {"faq"}
for handle, title, h1, lede, body in simple_pages:
    render("page.html", f"/pages/{handle}/", seo_title=title, seo_description=lede or h1, canonical=f"/pages/{handle}/",
           body_class="shop", page_id=handle, page=dict(h1=h1, lede=lede, body=body, steps=PAGE_STEPS.get(handle),
           toc=[(f"q{i + 1}", q) for i, (q, _) in enumerate(home_faq)] if handle in TOC_PAGES else None))

assert [h for h, *_ in simple_pages] == SIMPLE_PAGES

render("sitemap.html", "/pages/sitemap/", seo_title="All Pages | Chesed Hair", seo_description="Every page on the Chesed Hair site, from collections and wigs to guides and help.",
       canonical="/pages/sitemap/", body_class="shop", page_id="sitemap",
       page=dict(h1="All Pages", lede="Every collection, wig, guide and help page in one place."))

# search index for the header search overlay
idx = [dict(t="All wigs", u="/collections/wigs/", k="Collection", s="lace front wigs all shop")]
idx += [dict(t=f"{t['name']} Wigs", u=f"/collections/{t['slug']}-wigs/", k="Texture", s=t["short"]) for t in D.TEXTURES]
idx += [dict(t=cc["name"], u=f"/collections/{cc['slug']}-wigs/", k="Color", s=" ".join(cc["colors"])) for cc in D.COLOR_COLLECTIONS]
idx += [dict(t=p["title"], u=p["url"], k="Wig", s=f"{p['color']['family']} {p['texture']['short']}", i=f"/assets/p/{p['images'][0]['file']}-560.webp", p=p["price"]) for p in products]
idx += [dict(t=ec["name"], u=f"/collections/{ec['slug']}/", k="Collection", s=ec["name"].lower() + " hair") for ec in D.EXTRA_COLLECTIONS]
idx += [dict(t=x["title"], u=x["url"], k=x["collection"]["name"], s=x["kind"] + " hair extensions bundles", i=f"/assets/p/{x['images'][0]['file']}-560.webp", p=x["price"]) for x in extras]
idx += [dict(t="Length Guide", u="/pages/wig-length-guide/", k="Guide", s="inches length chart how long"),
        dict(t="Color Guide", u="/pages/wig-color-guide/", k="Guide", s="shade colour chart compare")]
idx += [dict(t=h1, u=f"/pages/{h}/", k="Help", s=lede or "") for h, _, h1, lede, _ in simple_pages]
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
json.dump(idx, open(os.path.join(ROOT, "assets", "search.json"), "w", encoding="utf-8"), separators=(",", ":"))

assert len(written) == env.globals["page_count"], (len(written), env.globals["page_count"])
print(f"Wrote {len(written)} pages")
