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

def img_like(p, *words):
    for im in p["images"]:
        if all(w in im["file"] for w in words):
            return im
    return p["images"][0]

# texture tiles (menu + homepage): Natural Black 1B where it exists
for t in D.TEXTURES:
    pool = [p for p in products if p["texture"]["key"] == t["key"]]
    tp = next((p for p in pool if p["color"]["key"] == "Natural Black 1B"), pool[0])
    t["tile"] = tp["images"][0]
    t["product"] = tp

hero_product = find("Body Wave", "Natural Black 1B")
hero = img_like(hero_product, "grey-wall-lamp")
hero_imgs = [find("Body Wave", "Burgundy 530")["images"][0], hero, find("Curly", "Honey Blonde")["images"][0]]
banner_texture = D.TEX["Kinky Straight"]
banner_imgs = [find("Kinky Straight", "Natural Black 1B")["images"][0], find("Kinky Straight", "Ginger 350")["images"][0]]

def banner_for(pool):
    """Three images for a collection banner: different products, first image each."""
    picks, seen = [], set()
    for p in pool:
        if p["handle"] not in seen:
            picks.append(p["images"][0]); seen.add(p["handle"])
        if len(picks) == 3: break
    i = 1
    while len(picks) < 3 and i < len(pool[0]["images"]):
        picks.append(pool[0]["images"][i]); i += 1
    return picks
theater = []
for c in D.COLORS:
    p = find("Body Wave", c["key"])
    cc = color_to_cc[c["key"]]
    theater.append(dict(color=c, product=p, img=p["images"][0], family_slug=cc["slug"], family_name=cc["name"]))

best = [find(*k) for k in [("Body Wave", "Natural Black 1B"), ("Body Wave", "Burgundy 530"), ("Straight", "Natural Black 1B"),
                           ("Kinky Straight", "Natural Black 1B"), ("Loose Deep", "Ginger 350"), ("Curly", "Honey Blonde"),
                           ("Body Wave", "Honey Auburn"), ("Virgin Curl", "Virgin Natural")]]
look_keys = [("Straight", "Red"), ("Loose Deep", "Honey Auburn"), ("Kinky Straight", "Ginger 350"), ("Curly", "Burgundy 530"),
             ("Body Wave", "Honey Blonde"), ("Kinky Curly", "Burgundy 530"), ("Straight", "Jet Black 1"), ("Loose Deep", "Natural Auburn")]
lookbook = []
for k in look_keys:
    p = find(*k)
    lookbook.append(dict(product=p, img=p["images"][1] if len(p["images"]) > 1 else p["images"][0]))
all_tile = [find("Straight", "Red")["images"][0], find("Body Wave", "Honey Blonde")["images"][0], find("Loose Deep", "Ginger 350")["images"][0], find("Kinky Straight", "Burgundy 530")["images"][0]]
story_p = find("Curly", "Natural Black 1B")
story = story_p["images"][0]

home_faq = [
    ("What are Chesed wigs made of?", "Every Chesed wig is 100% unprocessed virgin Remy human hair on a lace front, so you can color, heat-style and wash it like your own hair."),
    ("How do I choose my length?", "Use the length guide: it shows where each length from 10 to 32 inches ends on the body. Waves and curls sit about 2 inches higher than straight hair."),
    ("How do I choose my shade?", "Every shade is shown on the same model in real rooms. The color guide puts all ten side by side, including the ones people mix up, like 1B vs Jet Black."),
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
         version=str(int(time.time())), macros=None)
env.globals.update(G)
env.globals["strands"] = strands
env.globals["reviews"] = D.REVIEWS
env.globals["macros"] = env.get_template("partials/macros.html").module

# Menu: "simple" = text menu that reaches every page; "visual" = the archived Round 3 image mega menu
HEADER = "simple"
env.globals["header_style"] = HEADER
env.globals["nav_textures"] = [dict(t, products=[p for p in products if p["texture"]["key"] == t["key"]]) for t in D.TEXTURES]
SIMPLE_PAGES = ["about", "faq", "shipping", "returns", "contact"]
# home + all-wigs hub + texture and color collections + products + 2 guides + simple pages + site map
env.globals["page_count"] = 2 + len(D.TEXTURES) + len(D.COLOR_COLLECTIONS) + len(products) + 2 + len(SIMPLE_PAGES) + 1

written = []
def render(template, path, **ctx):
    html = env.get_template(template).render(**ctx)
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    written.append(path)

def org_ld():
    return {"@context": "https://schema.org", "@type": "Organization", "name": "Chesed Hair Collection",
            "url": "https://chesedhair.com", "logo": "https://chesedhair.com/favicon.svg"}

# HOME
render("index.html", "/", seo_title="Chesed Hair | Human Hair Lace Front Wigs",
       seo_description="Lace front wigs in 100% unprocessed virgin Remy human hair. 7 textures, 10 shades, 10 to 32 inches, all shown on the same model.",
       canonical="/", body_class="home overlay", page_id="home", hero=hero, hero_product=hero_product, hero_imgs=hero_imgs, banner_imgs=banner_imgs, banner_texture=banner_texture, all_tile=all_tile, theater=theater,
       best=best, lookbook=lookbook, story=story, home_faq=home_faq, jsonld=json.dumps(org_ld()),
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

tex_related = [dict(label=t["name"], url=f"/collections/{t['slug']}-wigs/") for t in D.TEXTURES]
col_related = [dict(label=cc["name"], url=f"/collections/{cc['slug']}-wigs/", hex=D.COL[cc["colors"][0]]["hex"]) for cc in D.COLOR_COLLECTIONS]

hub = dict(h1="Lace Front Wigs", intro="Every Chesed wig in one place: 7 textures and 10 shades of lace front wigs in 100% unprocessed virgin Remy human hair, each available from 10 to 32 inches. All of them are shown on the same model, so you can compare textures and shades fairly. Filter by texture below, or shop by color from the menu.",
           products=products, filters=texture_filters(products), filter_key="texture", filter_label="Texture", image=None,
           faq=home_faq, related_heading="Shop by color", related=col_related,
           banner=[find("Straight", "Red")["images"][0], find("Body Wave", "Natural Black 1B")["images"][0], find("Loose Deep", "Honey Auburn")["images"][0]])
render("collection.html", "/collections/wigs/", seo_title="Lace Front Wigs in 7 Textures & 10 Colors | Chesed",
       seo_description="Shop all Chesed lace front wigs: body wave, curly, kinky curly, kinky straight, loose deep wave, straight and virgin curl, in 10 shades, 10 to 32 inches.",
       canonical="/collections/wigs/", body_class="shop overlay", page_id="hub", c=hub, is_hub=True,
       jsonld=json.dumps(breadcrumb_ld([("Home", "/"), ("Lace Front Wigs", "/collections/wigs/")])))

TEX_TITLES = {"body-wave": "Body Wave Lace Front Wigs, 10-32 Inch | Chesed", "curly": "Curly Lace Front Wigs, 10-32 Inch | Chesed",
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
           canonical=url, body_class="shop overlay", page_id=cc["slug"], c=c, is_hub=False,
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

# PAGES
render("length_guide.html", "/pages/wig-length-guide/", seo_title="Wig Length Chart, 10-32 Inch on a Model | Chesed",
       seo_description="See where every wig length from 10 to 32 inches ends on the body, for straight and curly textures.",
       canonical="/pages/wig-length-guide/", body_class="shop", page_id="lg", lengths=D.LENGTHS, landmarks=D.LANDMARKS, curly_landmarks=D.CURLY_LANDMARKS,
       page=dict(h1="Wig Length Chart: 10 to 32 Inches", lede="Where each length ends on the body, for straight and for curly textures."))
render("color_guide.html", "/pages/wig-color-guide/", seo_title="Wig Color Chart: 10 Shades on Deep Skin | Chesed",
       seo_description="All 10 Chesed wig colors on the same model: 1B, Jet Black, Virgin Natural, Burgundy 530, 99J, Ginger 350, Honey Auburn, Natural Auburn, Honey Blonde and Red.",
       canonical="/pages/wig-color-guide/", body_class="shop", page_id="cg", theater=theater,
       page=dict(h1="Wig Colors on Deep Skin", lede="All ten shades on the same model, so you can compare them fairly."))

simple_pages = [
    ("about", "About Chesed Hair", "About Chesed Hair", "Chesed means lovingkindness.",
     "<p>Chesed is the Hebrew word for a deep, unconditional love. We named the brand after it because that's how hair should be made: with care for the woman who wears it and the people who make it.</p><p>Every Chesed unit starts as 100% unprocessed virgin Remy human hair, sourced and made without exploited labor.</p><p class='ph-note'>Founder story and photos to come from Chesed.</p>"),
    ("faq", "Wig FAQ: Lace, Fit, Shipping | Chesed Hair", "Frequently Asked Questions", "Choosing, wearing and caring for your wig.",
     "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in home_faq) + "<p class='ph-note'>Shipping, lace, density and cap-size answers will be added once Chesed confirms the details.</p>"),
    ("shipping", "Shipping | Chesed Hair", "Shipping", None, f"<p>Free US shipping on orders over ${int(D.FREE_SHIP)}.</p><p class='ph-note'>Processing times, carriers and international rates to be confirmed by Chesed.</p>"),
    ("returns", "Returns | Chesed Hair", "Returns", None, "<p>Return unworn wigs within 30 days with the lace uncut.</p><p class='ph-note'>Full return policy to be confirmed by Chesed.</p>"),
    ("contact", "Contact | Chesed Hair", "Contact", None, "<p>Email <a href='mailto:info@chesedhair.com'>info@chesedhair.com</a>. We reply within <span class='ph'>X</span> business days.</p>"),
]
for handle, title, h1, lede, body in simple_pages:
    render("page.html", f"/pages/{handle}/", seo_title=title, seo_description=lede or h1, canonical=f"/pages/{handle}/",
           body_class="shop", page_id=handle, page=dict(h1=h1, lede=lede, body=body))

assert [h for h, *_ in simple_pages] == SIMPLE_PAGES

render("sitemap.html", "/pages/sitemap/", seo_title="All Pages | Chesed Hair", seo_description="Every page on the Chesed Hair site, from collections and wigs to guides and help.",
       canonical="/pages/sitemap/", body_class="shop", page_id="sitemap",
       page=dict(h1="All Pages", lede="Every collection, wig, guide and help page in one place."))

assert len(written) == env.globals["page_count"], (len(written), env.globals["page_count"])
print(f"Wrote {len(written)} pages")
