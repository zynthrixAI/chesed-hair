"""Catalog data for the Chesed Hair preview.

Products are shaped like Shopify product objects (handle, title, options,
variants, images, metafields) so the templates port to Liquid with few changes.
Prices, shipping threshold and review counts are PLACEHOLDERS until the client confirms them.
"""
import json, os, re

HERE = os.path.dirname(__file__)
ASSETS_P = os.path.join(HERE, "..", "assets", "p")
POSE_NAMES = {"front": "front view", "three-quarter": "three-quarter view", "back": "back view",
              "side": "side view", "fingers": "fingers through the lengths", "lifestyle": "lifestyle shot",
              "mannequin-front": "front view on a mannequin", "mannequin-back": "back view on a mannequin"}

PRICE = 289.00            # placeholder price (same as the approved preview)
FREE_SHIP = 200.00        # placeholder free-shipping threshold
LENGTHS = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
CURLY_LANDMARKS = ["jawline", "chin", "shoulders", "collarbone", "armpits", "bust", "below the bust",
                   "mid ribs", "waist", "below the waist", "hips", "top of the thighs"]
LANDMARKS = ["chin", "shoulders", "collarbone", "armpits", "bust", "below the bust",
             "mid ribs", "waist", "below the waist", "hips", "top of the thighs", "upper thighs"]

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

TEXTURES = [
    dict(key="Body Wave", name="Body Wave", slug="body-wave", curly=True,
         short="Soft S-shaped waves that swing past the collarbone.",
         intro="Body wave is the easiest texture to wear every day: soft, S-shaped waves with natural movement that look styled from the moment you put the wig on. Each Chesed body wave wig is a lace front unit made from 100% unprocessed virgin Remy human hair, in 10 shades and every length from 10 to 32 inches. Pick a shade, choose your length and wear it straight out of the box, or reset the wave with a wash and air-dry.",
         faq=[("Will the body wave pattern last?", "Yes. The wave is set into the hair, so it returns after washing. Air-dry or diffuse to keep the S-shape defined."),
              ("Can I straighten a body wave wig?", "You can flat iron it with a heat protectant. The wave comes back after the next wash."),
              ("Why does a body wave wig look shorter than its length?", "Length is measured with the hair pulled straight. Waves sit about 2 inches higher on the body."),
              ("Which shade sells best in body wave?", "1B is the everyday choice. 530 and 350 are the statement shades.")]),
    dict(key="Curly", name="Curly", slug="curly", curly=True,
         short="Small, dense spiral curls with full volume.",
         intro="Our curly lace front wigs have small, dense spiral curls that look full from root to tip. They are made from 100% unprocessed virgin Remy human hair and come in 9 shades and lengths from 10 to 32 inches. Curly units give the most volume of any Chesed texture, so a shorter length still reads big. Refresh the curls with water and a leave-in conditioner between washes.",
         faq=[("How do I keep the curls defined?", "Wet the hair, apply a leave-in conditioner and let it air-dry. Avoid brushing curls when dry."),
              ("Does a curly wig look shorter?", "Yes. Curls shrink, so a curly wig sits 2 to 4 inches higher than its stretched length."),
              ("Can I wear it straight?", "You can blow it out and flat iron it. The curls return when the hair gets wet."),
              ("How full is a curly wig?", "Curly units look the fullest of all our textures because each curl takes up more space.")]),
    dict(key="Kinky Curly", name="Kinky Curly", slug="kinky-curly", curly=True,
         short="Tight, springy coils that blend with natural 4C hair.",
         intro="Kinky curly wigs have tight, springy coils that match natural 4B and 4C hair, so the hairline blends instead of standing out. This lace front unit is made from 100% unprocessed virgin Remy human hair, currently in 530, in lengths from 10 to 32 inches. It is the most natural-looking option if you want a wig that looks like your own hair grown out.",
         faq=[("Will kinky curly blend with my natural hair?", "Yes. The coil pattern is made to match 4B and 4C textures."),
              ("How much does kinky curly shrink?", "A lot. Expect it to sit 4 or more inches higher than its stretched length."),
              ("How do I detangle it?", "Finger-detangle while wet with conditioner, working from the ends up."),
              ("Which colors does kinky curly come in?", "530 for now. More shades are planned.")]),
    dict(key="Kinky Straight", name="Kinky Straight", slug="kinky-straight", curly=False,
         short="Straight with a natural, blown-out yaki texture.",
         intro="Kinky straight hair looks like natural hair that has been blown out: straight, with a soft yaki texture instead of a glassy shine. That texture is why it blends with relaxed or pressed hair and looks believable up close. Each Chesed kinky straight wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 9 shades and lengths from 10 to 32 inches.",
         faq=[("What is the difference between kinky straight and straight?", "Kinky straight has a coarse, blown-out texture. Straight is smooth and silky."),
              ("Can I curl a kinky straight wig?", "Yes. It holds curls well because of its texture."),
              ("Does it blend with relaxed hair?", "Yes. It is the closest match to relaxed or silk-pressed natural hair."),
              ("Is it frizzy?", "It has a natural texture, not frizz. A light serum smooths flyaways.")]),
    dict(key="Loose Deep", name="Loose Deep Wave", slug="loose-deep-wave", curly=True,
         short="Loose, defined curls between a wave and a curl.",
         intro="Loose deep wave sits between a body wave and a curl: defined, bouncy curls that are looser than a deep wave and fuller than a body wave. It is a strong choice if you want volume without tight curls. Every Chesed loose deep wave wig is a lace front unit made from 100% unprocessed virgin Remy human hair, in 9 shades and lengths from 10 to 32 inches.",
         faq=[("Is loose deep wave the same as body wave?", "No. Loose deep wave has more defined, curlier waves. Body wave is softer and looser."),
              ("How do I keep the pattern?", "Wash, apply a curl cream and let it air-dry or diffuse."),
              ("Does it tangle?", "Less than tighter curls. Detangle wet with a wide-tooth comb."),
              ("Does it look shorter than its length?", "Yes, by about 2 to 3 inches, because the curls take up length.")]),
    dict(key="Straight", name="Straight", slug="straight", curly=False,
         short="Smooth, silky straight hair with natural movement.",
         intro="Our straight lace front wigs are smooth, silky and swing with natural movement. Straight hair shows length most clearly, so it is the best texture for long lengths up to 32 inches. Each wig is made from 100% unprocessed virgin Remy human hair and comes in 9 shades. Wear it sleek, add curls with a wand, or part it however you like.",
         faq=[("Will straight hair stay straight?", "Yes. It is naturally straight, so it dries straight after washing."),
              ("Can I curl it?", "Yes, with a curling iron or wand and a heat protectant."),
              ("Does straight hair show the true length?", "Yes. Straight hair falls at its full measured length."),
              ("Is it shiny?", "It has a natural soft shine, not a synthetic gloss.")]),
    dict(key="Virgin Curl", name="Virgin Curl", slug="virgin-curl", curly=True,
         short="Natural-color curls in untreated virgin hair.",
         intro="Virgin curl wigs are curly units left in their natural, uncolored state, so the hair has never been processed. That makes them the best base if you plan to dye the wig yourself later. They come in 1B, 1 and Virgin, in lengths from 10 to 32 inches, as lace front units in 100% unprocessed virgin Remy human hair.",
         faq=[("What makes virgin curl different from curly?", "Virgin curl is never colored, so it stays in its natural shade. That makes it the safest base for dyeing."),
              ("Can I dye it?", "Yes. Unprocessed hair takes color best. We recommend a professional colorist."),
              ("Which shades are available?", "1B, 1 and Virgin."),
              ("How do I care for it?", "Treat it like natural curly hair: moisture, gentle detangling, air-drying.")]),
    dict(key="Permed Straight", name="Permed Straight", slug="permed-straight", curly=False,
         only_colors=["1", "1B", "Virgin", "350", "530", "Honey Auburn", "Honey Blonde", "Red"],
         short="Straight with a soft perm texture and extra body.",
         intro="Permed straight falls straight but has a soft perm texture through it, so it looks fuller and more natural than glassy, silky straight hair. It is a good match for relaxed or lightly textured natural hair and keeps its body between washes. Each Chesed permed straight wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 8 shades and lengths from 10 to 32 inches.",
         faq=[("How is permed straight different from straight?", "Straight is smooth and silky. Permed straight has a soft texture and more body, so it looks less flat."),
              ("Can I curl a permed straight wig?", "Yes. Use a heat protectant and a curling iron or wand."),
              ("Does it blend with my natural hair?", "It blends best with relaxed, silk-pressed or lightly textured hair."),
              ("Which shades are available?", "1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde and Red.")]),
    dict(key="Wet & Wavy", name="Wet & Wavy", slug="wet-and-wavy", curly=True,
         only_colors=["1", "1B", "Virgin", "350", "530", "Honey Auburn", "Honey Blonde", "Red"],
         short="Loose, glossy waves that look freshly wet-set.",
         intro="Wet & wavy has loose, flowing waves with a glossy, just-styled finish that looks like freshly wet-set hair. The pattern is defined from root to tip and moves easily. Each Chesed wet & wavy wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 8 shades and lengths from 10 to 32 inches. Refresh the waves with water and a light leave-in conditioner.",
         faq=[("How do I keep the waves defined?", "Wet the hair, add a leave-in conditioner and let it air-dry or diffuse. Avoid brushing when dry."),
              ("Is wet & wavy the same as body wave?", "No. Wet & wavy has a looser, glossier, more water-like pattern. Body wave is a softer S-shape."),
              ("Does it look shorter than its length?", "Yes. The waves take up length, so it sits about 2 inches higher than straight hair."),
              ("Which shades are available?", "1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde and Red.")]),
]
TEX = {t["key"]: t for t in TEXTURES}

COLORS = [
    dict(key="1B", slug="1b", hex="#2A201C", family="black",
         blurb="Soft off-black with a faint warm brown undertone. It is the closest match to most natural hair."),
    dict(key="1", slug="1", hex="#0E0E10", family="black",
         blurb="The deepest, coolest black we make. It is crisp and high-contrast, with no brown at all."),
    dict(key="Virgin", slug="virgin", hex="#2B1D16", family="black",
         blurb="Untreated hair in its natural dark brown-black, with soft espresso tones where light hits."),
    dict(key="530", slug="530", hex="#6E1B2E", family="burgundy",
         blurb="Rich wine red with violet depth. It glows warm on deep skin and reads dark in low light."),
    dict(key="99J", slug="99j", hex="#441A28", family="burgundy",
         blurb="Dark plum, cooler and deeper than burgundy, almost black cherry in shadow."),
    dict(key="350", slug="350", hex="#B4552C", family="ginger",
         blurb="Bright copper orange with lighter tones where the light catches it. It is our boldest warm shade."),
    dict(key="Honey Auburn", slug="honey-auburn", hex="#8D6038", family="auburn",
         blurb="Golden brown with soft honey highlights and slightly darker roots. It is warm, not orange."),
    dict(key="Natural Auburn", slug="natural-auburn", hex="#9E6B3C", family="auburn",
         blurb="A natural reddish brown that warms up in sunlight and stays soft indoors."),
    dict(key="Honey Blonde", slug="honey-blonde", hex="#C99A55", family="honey-blonde",
         blurb="Warm golden blonde from root to tip, buttery rather than ash or platinum."),
    dict(key="Red", slug="red", hex="#B0141F", family="red",
         blurb="True cherry red from root to tip, with no orange and no pink."),
]
COL = {c["key"]: c for c in COLORS}

COLOR_COLLECTIONS = []   # one collection per shade, filled in by make_color_collections() once products exist

# how each shade differs from the ones people mix it up with
COLOR_COMPARE = {
    "1": ("What is the difference between 1 and 1B?", "1 is jet black, cooler and darker. 1B is off-black with a warm brown undertone."),
    "1B": ("What is the difference between 1B and 1?", "1B is off-black with a warm brown undertone. 1 is jet black, cooler and darker."),
    "Virgin": ("How is Virgin different from 1B?", "Virgin is untreated hair in its natural dark brown-black, softer than 1 and a touch warmer than 1B."),
    "530": ("Is 530 the same as red?", "No. 530 is a deep wine red with violet depth. Red is true cherry red, and 99J is darker still."),
    "99J": ("How is 99J different from 530?", "99J is darker and cooler than 530, almost black cherry in shadow."),
    "350": ("Is 350 orange or red?", "Orange-copper. It is brighter and more orange than auburn."),
    "Honey Auburn": ("How is Honey Auburn different from Natural Auburn?", "Honey Auburn is golden brown with honey highlights. Natural Auburn is a more even reddish brown."),
    "Natural Auburn": ("How is Natural Auburn different from Honey Auburn?", "Natural Auburn is an even reddish brown. Honey Auburn is golden, with lighter honey highlights."),
    "Honey Blonde": ("Is honey blonde the same as 613?", "No. Honey blonde is a warm golden shade. 613 is a pale platinum blonde."),
    "Red": ("Is this red or 530?", "True cherry red. For a darker wine shade, see 530."),
}

def make_color_collections(products):
    """One collection page per shade, with the textures that shade actually comes in."""
    out = []
    for c in COLORS:
        texs = [t["name"].lower() for t in TEXTURES if any(p["texture"]["key"] == t["key"] and p["color"]["key"] == c["key"] for p in products)]
        if not texs:
            continue
        tl = texs[0] if len(texs) == 1 else ", ".join(texs[:-1]) + " and " + texs[-1]
        key = c["key"]
        q, a = COLOR_COMPARE[key]
        out.append(dict(
            slug=c["slug"], name=f"{key} Wigs", label=key, h1=f"{key} Wigs", colors=[key],
            title=f"{key} Lace Front Wigs | Chesed Hair",
            intro=f"{c['blurb']} Shop {key} lace front wigs in {tl}, made from 100% unprocessed virgin Remy human hair, in lengths from 10 to 32 inches.",
            faq=[(f"Which textures come in {key}?", f"{tl.capitalize()}."), (q, a),
                 (f"Can I dye {key}?", "Virgin is the best base for color because it has never been processed. We recommend a professional colorist for any color change."),
                 (f"How do I keep {key} looking its best?", "Wash in cool water with sulfate-free shampoo and conditioner, and store the wig on a stand.")]))
    return out


def gallery_images(handle, color, texture_name):
    """The gallery photos for a wig, in order: front, three-quarter, back, side, fingers, lifestyle, then the real mannequin photos, front and back (where the client supplied them); build_products puts them in the last slots."""
    found = sorted(f for f in os.listdir(ASSETS_P) if f.startswith(handle + "-") and f.endswith("-1024.webp"))
    images = []
    for f in found:
        pose = f[len(handle) + 1:-len("-1024.webp")]          # e.g. "1-front"
        order, _, name = pose.partition("-")
        images.append((int(order), dict(
            file=f[:-len("-1024.webp")],
            mannequin=name.startswith("mannequin"),
            alt=f"{color} {texture_name.lower()} lace front wig {'' if name.startswith('mannequin') else 'on model, '}{POSE_NAMES.get(name, name.replace('-', ' '))}",
        )))
    return [im for _, im in sorted(images, key=lambda x: x[0])]

# Which photo leads each wig's gallery (and its card): the bright, smiling lifestyle shot, with exceptions below.
# The rest follow in their original order: front, three-quarter, back, side, fingers.
COVER_POSE = "6-lifestyle"
COVER_OVERRIDES = {("Body Wave", "1"): "2-three-quarter"}   # (texture, shade) -> pose

def cover_first(images, texture, color):
    pose = COVER_OVERRIDES.get((texture, color), COVER_POSE)
    lead = [im for im in images if f"-{pose}" in im["file"]]
    return lead + [im for im in images if im not in lead] if lead else images

PLACEHOLDER_IMG = "placeholder"   # assets/p/placeholder-1024.webp: pink "photo coming soon" stand-in

def build_products():
    products = []
    for style, t in TEX.items():
        for color, c in COL.items():
            handle = f"{c['slug']}-{t['slug']}-lace-front-wig"
            title = f"{color} {t['name']} Lace Front Wig"
            images = gallery_images(handle, color, t["name"])
            mannequin = [im for im in images if im.get("mannequin")]
            images = cover_first([im for im in images if not im.get("mannequin")], t["key"], color)
            if mannequin and images:        # the real mannequin photos (front, then back) take the last slots in the gallery
                images = images[:-1] + mannequin
            placeholder = False
            if not images and color in t.get("only_colors", []):
                images = [dict(file=PLACEHOLDER_IMG, alt=f"Photo coming soon: {title}", placeholder=True)]
                placeholder = True
            if not images:
                continue
            products.append(dict(
                kind="wig", placeholder=placeholder,
                handle=handle, title=title, texture=t, color=c, price=PRICE,
                images=images, url=f"/products/{handle}/",
                options=["Length"], variants=[dict(length=l, title=f'{l}"', price=PRICE, landmark=LANDMARKS[i]) for i, l in enumerate(LENGTHS)],
            ))
    # sort: texture order then color order
    tix = {t["key"]: i for i, t in enumerate(TEXTURES)}
    cix = {c["key"]: i for i, c in enumerate(COLORS)}
    products.sort(key=lambda p: (tix[p["texture"]["key"]], cix[p["color"]["key"]]))
    return products

# Crochet / feather extensions and hair bundles, imported from the client's product export and item list
# (see src/extras.json). They are not wigs, so they live in their own collections.
EXTRA_COLLECTIONS = [
    dict(kind="crochet", slug="crochet-braid-extensions", name="Crochet & Feather Extensions", h1="Crochet & Feather Extensions", noun="extension",
         title="Crochet & Feather Hair Extensions | Chesed Hair",
         intro="Handmade feather and crochet braid hair extensions in human hair, in textures from body wave and deep wave to kinky curly and wet & wavy. Pick your shade and length on each product page. Packs, weights and lengths vary by style, so check the details on the page.",
         faq=[("What are feather crochet extensions?", "They are hair extensions made to be installed with a crochet technique, so the finished look is seamless and light."),
              ("How many packs do I need for a full head?", "It depends on the style and the length you choose. Some listings offer a 3-pack full-head option. Ask us if you are not sure."),
              ("Can I dye or restyle them?", "They can be, but it is not recommended, because the hair is already styled and colored."),
              ("How long do they last?", "With care they can last up to a year. Textured styles need regular upkeep.")]),
    dict(kind="bundle", slug="hair-bundles", name="Hair Bundles", h1="Hair Bundles", noun="bundle",
         title="Human Hair Bundles | Chesed Hair",
         intro="Chesed hair bundles in body wave, straight, deep wave and water wave. Choose from natural darks, bold colors and blonde shades, in lengths from 10 inches up. Photos, prices and hair details are placeholders until Chesed confirms them.",
         faq=[("Which bundle textures do you carry?", "Body wave, straight, deep wave and water wave."),
              ("How do I choose a shade?", "Dark shades (1, 1B, Virgin) are the natural blacks. The color bundles and blonde shades are lighter and bolder."),
              ("How many bundles do I need?", "Most people use 3 to 4 bundles for a full head. Longer lengths may need more."),
              ("Can I color or style them?", "Details to be confirmed by Chesed.")]),
]
EXTRA_BY_KIND = {c["kind"]: c for c in EXTRA_COLLECTIONS}

# Textures and colour families for the crochet extensions and bundles (read from each listing's title, options and details),
# so the menu and the collection page can filter them the way wigs are filtered.
CROCHET_TEXTURES = [("body-wave", "Body Wave"), ("deep-wave", "Deep Wave"), ("water-wave", "Water Wave"), ("loose-wave", "Loose Wave"),
                    ("wet-and-wavy", "Wet & Wavy"), ("straight", "Straight"), ("kinky-straight", "Kinky Straight"),
                    ("kinky-curly", "Kinky Curly"), ("burmese-curly", "Burmese Curly")]
CROCHET_COLORS = [("black", "Black", "#1A1614"), ("brown", "Brown", "#4A2F22"), ("auburn", "Auburn", "#9A4F2B"),
                  ("blonde", "Blonde", "#D9B26A"), ("burgundy", "Burgundy & Red", "#6E1B2E"),
                  ("highlight", "Highlights & Ombre", "linear-gradient(135deg,#4A2F22 0 33%,#B4552C 33% 66%,#D9B26A 66%)")]

def _texture_slugs(text):
    t = text.lower().replace("&", "and")
    found = [s for s, kw in (("wet-and-wavy", "wet and wavy"), ("burmese-curly", "burmese"), ("kinky-straight", "kinky straight"),
                              ("kinky-curly", "kinky curly"), ("deep-wave", "deep wave"), ("water-wave", "water wave"),
                              ("body-wave", "body wave"), ("loose-wave", "loose wave")) if kw in t]
    if "straight" in t.replace("kinky straight", ""):
        found.append("straight")
    return found

def _color_slug(v):
    v = v.lower()
    if any(k in v for k in ("+", "ombre", "salt", "highlight", "each color", "of each")): return "highlight"
    if "auburn" in v: return "auburn"
    if any(k in v for k in ("blonde", "hondy", "#27")): return "blonde"
    if any(k in v for k in ("burgundy", "ruby", "wine", "red", "#530", "99j")): return "burgundy"
    if "brown" in v or v.strip("# ").startswith(("4", "2")): return "brown"
    if "black" in v or "#1b" in v or v.strip("# ") == "natural": return "black"
    return None

def classify_extra(title, options, details):
    tex, col = set(_texture_slugs(title)), set()
    for o in options:
        for v in o["values"]:
            if o["name"] == "Color" or (o["name"] == "Texture" and "#" in v):
                c = _color_slug(v)
                if c: col.add(c)
            elif o["name"] == "Texture":
                tex.update(_texture_slugs(v))
    for k, v in details:
        if k == "Hair Texture": tex.update(_texture_slugs(v))
        if k == "Color":
            for part in v.replace(",", ";").split(";"):
                c = _color_slug(part)
                if c: col.add(c)
    if "multi-color" in title.lower() or "highlight" in title.lower(): col.add("highlight")
    if "natural black" in title.lower(): col.add("black")
    return [s for s, _ in CROCHET_TEXTURES if s in tex], [s for s, *_ in CROCHET_COLORS if s in col]

def build_extras():
    raw = json.load(open(os.path.join(HERE, "extras.json"), encoding="utf-8"))
    out = []
    for r in raw:
        col = EXTRA_BY_KIND[r["kind"]]
        prices = [v["price"] for v in r["variants"]]
        out.append(dict(
            kind=r["kind"], collection=col, handle=r["handle"], title=r["title"], url=f"/products/{r['handle']}/",
            price=min(prices), price_from=len(set(prices)) > 1, price_placeholder=r.get("placeholder_price", False),
            images=r["images"], placeholder=bool(r["images"][0].get("placeholder")), options=r["options"], variants=r["variants"],
            details=r.get("details", []), desc=r.get("desc", []),
        ))
        out[-1]["textures"], out[-1]["colors"] = classify_extra(r["title"], r["options"], r.get("details", []))
    return out

# Reviews shown on chesedhair.com (homepage "What Our Customers Say", scraped Oct 2026).
# confirmed=False: they appear to be static theme testimonials. Chesed must confirm they are
# real customers before launch (FTC rule on fake reviews). Replace with Judge.me on Shopify.
REVIEWS = [
    dict(name="Jessica L.", stars=5, product="Hair extensions", confirmed=False,
         text="I was honestly surprised by the quality of the hair extensions. They feel incredibly soft, blend perfectly with my natural hair, and hold curls really well. The packaging was beautiful and delivery was fast. I'll definitely be ordering again!"),
    dict(name="Monica R.", stars=5, product="Wig", confirmed=False,
         text="I ordered a wig for a special event and it exceeded my expectations. The hairline looks very natural and the density is perfect — not too heavy, not too thin. I received so many compliments. Highly recommend Chesed Hair!"),
    dict(name="Danielle K.", stars=5, product="Hair extensions", confirmed=False,
         text="The customer service was amazing from start to finish. They helped me choose the right length and texture for my hair type. The quality is truly premium and it looks so natural. Worth every penny!"),
]

# Welcome wheel (email popup). Every spin wins; weights are the real odds and are shown to shoppers.
# Placeholder prizes and codes: Chesed sets the final offers and creates the codes in Shopify.
SPIN_PRIZES = [
    dict(label="10% off", code="WELCOME10", pct=10, amt=0, weight=35),
    dict(label="$20 off", code="SAVE20", pct=0, amt=20, weight=25),
    dict(label="15% off", code="WELCOME15", pct=15, amt=0, weight=20),
    dict(label="$40 off", code="SAVE40", pct=0, amt=40, weight=10),
    dict(label="20% off", code="WELCOME20", pct=20, amt=0, weight=7),
    dict(label="$60 off", code="SAVE60", pct=0, amt=60, weight=3),
]

# WhatsApp chat button. Placeholder: Chesed's WhatsApp Business number, digits only with country code.
WHATSAPP = "10000000000"
WHATSAPP_PLACEHOLDER = True
