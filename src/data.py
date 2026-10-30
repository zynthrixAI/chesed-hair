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

# Wig prices from Chesed's price sheet ("CHESED WIG List", 24 October 2026): a price per length,
# plus $5 for the coloured shades and an extra for some textures. Chesed asked for the sheet prices times 2,
# rounded up to the next .95. Water Wave wigs were removed: not on the sheet. Curly is not on it either, but came back on 29 October 2026 at the Kinky Curly prices (user).
WIG_LENGTH_PRICE = {18: 69.95, 20: 79.95, 22: 99.95, 24: 99.95, 26: 129.95, 28: 139.95, 30: 149.95, 32: 179.95}
NATURAL_SHADES = {"1", "1B", "Virgin"}          # every other shade costs $5 more
COLOR_EXTRA = 5.00
TEXTURE_EXTRA = {"Loose Deep": 3.50, "Kinky Curly": 4.50, "Virgin Curl": 4.50, "Kinky Straight": 4.50, "Wet & Wavy": 4.50,
                 "Deep Wave": 3.50, "Curly": 4.50}   # Body Wave, Straight, Permed Straight: no extra
# Curly is not on the sheet: priced like Kinky Curly (user, 29 October 2026)
PRICE_MULTIPLIER = 2

def up_to_95(x):
    n = int(x)
    return n + 0.95 if x <= n + 0.95 + 1e-9 else n + 1.95

def wig_price(length, texture, color):
    sheet = WIG_LENGTH_PRICE[length] + (0 if color in NATURAL_SHADES else COLOR_EXTRA) + TEXTURE_EXTRA.get(texture, 0)
    return round(up_to_95(sheet * PRICE_MULTIPLIER), 2)
FREE_SHIP = 100.00        # free US shipping over $100 (client, 22 October 2026)
LENGTHS = [18, 20, 22, 24, 26, 28, 30, 32]   # wigs come in 18" to 32" (client, 22 October 2026; 34" and 36" dropped by Chesed, 30 October 2026)
DEFAULT_LENGTH = 24
# where each length ends on the body; waves and curls sit one step higher.
LANDMARKS = ["bust", "below the bust", "mid ribs", "waist", "below the waist", "hips",
             "top of the thighs", "upper thighs"]
CURLY_LANDMARKS = ["armpits", "bust", "below the bust", "mid ribs", "waist", "below the waist",
                   "hips", "top of the thighs"]

# Length photos (layout C, chosen by Chesed on 24 October 2026): a 5'5" model from behind with a pink line
# and tag for each length. Waves and curls spring up, so their lines sit 2 inches higher.
LENGTH_PHOTOS = [dict(key="straight", label="Straight", up=0), dict(key="wavy", label="Wavy", up=2),
                 dict(key="curly", label="Curly", up=2)]
WAVY_TEXTURES = {"Body Wave", "Loose Deep", "Wet & Wavy"}   # the other curly textures use the curly photo

# Crochet and feather lengths, shown on the same length photos (measured on the photo, 27 October 2026: 18" lands on the bust
# like the wigs). Waves and curls sit about 2 inches higher. Chesed to confirm.
CROCHET_LENGTHS = [12, 14, 16, 18, 22]
CROCHET_DEFAULT_LENGTH = 16
CROCHET_LANDMARKS = ["shoulders", "below the shoulders", "armpits", "bust", "mid ribs"]
CROCHET_CURLY_LANDMARKS = ["neck", "shoulders", "below the shoulders", "armpits", "below the bust"]
CROCHET_LENGTH_PHOTO = {"kinky-straight": "straight", "straight": "straight", "body-wave": "wavy", "wet-and-wavy": "wavy",
                        "water-wave": "wavy", "deep-wave": "curly", "burmese-curly": "curly"}   # crochet texture -> length photo

def crochet_length_photo_key(extra):
    return next((CROCHET_LENGTH_PHOTO[t] for t in extra["textures"] if t in CROCHET_LENGTH_PHOTO), "curly")

def length_photo_key(texture):
    return "straight" if not texture["curly"] else "wavy" if texture["key"] in WAVY_TEXTURES else "curly"

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

TEXTURES = [
    dict(key="Body Wave", name="Body Wave", slug="body-wave", curly=True,
         short="Soft S-shaped waves that swing past the collarbone.",
         intro="Body wave is the easiest texture to wear every day: soft, S-shaped waves with natural movement that look styled from the moment you put the wig on. Each Chesed body wave wig is a lace front unit made from 100% unprocessed virgin Remy human hair, in 10 shades and every length from 18 to 32 inches. Pick a shade, choose your length and wear it straight out of the box, or reset the wave with a wash and air-dry.",
         faq=[("Will the body wave pattern last?", "Yes. The wave is set into the hair, so it returns after washing. Air-dry or diffuse to keep the S-shape defined."),
              ("Can I straighten a body wave wig?", "You can flat iron it with a heat protectant. The wave comes back after the next wash."),
              ("Why does a body wave wig look shorter than its length?", "Length is measured with the hair pulled straight. Waves sit about 2 inches higher on the body."),
              ("Which shade sells best in body wave?", "Natural black (1B) is the everyday choice. Rich wine red (530) and copper ginger (350) are the statement shades.")]),
    dict(key="Curly", name="Curly", slug="curly", curly=True,
         short="Small, dense spiral curls with full volume.",
         intro="Our curly lace front wigs have small, dense spiral curls that look full from root to tip. They are made from 100% unprocessed virgin Remy human hair and come in 9 shades and lengths from 18 to 32 inches. Curly units give the most volume of any Chesed texture, so a shorter length still reads big. Refresh the curls with water and a leave-in conditioner between washes.",
         faq=[("How do I keep the curls defined?", "Wet the hair, apply a leave-in conditioner and let it air-dry. Avoid brushing curls when dry."),
              ("Does a curly wig look shorter?", "Yes. Curls shrink, so a curly wig sits 2 to 4 inches higher than its stretched length."),
              ("Can I wear it straight?", "You can blow it out and flat iron it. The curls return when the hair gets wet."),
              ("How full is a curly wig?", "Curly units look the fullest of all our textures because each curl takes up more space.")]),
    dict(key="Kinky Curly", name="Kinky Curly", slug="kinky-curly", curly=True,
         short="Tight, springy coils that blend with natural 4C hair.",
         intro="Kinky curly wigs have tight, springy coils that match natural 4B and 4C hair, so the hairline blends instead of standing out. This lace front unit is made from 100% unprocessed virgin Remy human hair, currently in rich wine red (530), in lengths from 18 to 32 inches. It is the most natural-looking option if you want a wig that looks like your own hair grown out.",
         faq=[("Will kinky curly blend with my natural hair?", "Yes. The coil pattern is made to match 4B and 4C textures."),
              ("How much does kinky curly shrink?", "A lot. Expect it to sit 4 or more inches higher than its stretched length."),
              ("How do I detangle it?", "Finger-detangle while wet with conditioner, working from the ends up."),
              ("Which colors does kinky curly come in?", "Rich wine red (530) for now. More shades are planned.")]),
    dict(key="Kinky Straight", name="Kinky Straight", slug="kinky-straight", curly=False,
         short="Straight with a natural, blown-out yaki texture.",
         intro="Kinky straight hair looks like natural hair that has been blown out: straight, with a soft yaki texture instead of a glassy shine. That texture is why it blends with relaxed or pressed hair and looks believable up close. Each Chesed kinky straight wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 9 shades and lengths from 18 to 32 inches.",
         faq=[("What is the difference between kinky straight and straight?", "Kinky straight has a coarse, blown-out texture. Straight is smooth and silky."),
              ("Can I curl a kinky straight wig?", "Yes. It holds curls well because of its texture."),
              ("Does it blend with relaxed hair?", "Yes. It is the closest match to relaxed or silk-pressed natural hair."),
              ("Is it frizzy?", "It has a natural texture, not frizz. A light serum smooths flyaways.")]),
    dict(key="Loose Deep", name="Loose Deep Wave", slug="loose-deep-wave", curly=True,
         short="Loose, defined curls between a wave and a curl.",
         intro="Loose deep wave sits between a body wave and a curl: defined, bouncy curls that are looser than a deep wave and fuller than a body wave. It is a strong choice if you want volume without tight curls. Every Chesed loose deep wave wig is a lace front unit made from 100% unprocessed virgin Remy human hair, in 9 shades and lengths from 18 to 32 inches.",
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
         intro="Virgin curl wigs are curly units left in their natural, uncolored state, so the hair has never been processed. That makes them the best base if you plan to dye the wig yourself later. They come in 1B, 1 and Virgin, in lengths from 18 to 32 inches, as lace front units in 100% unprocessed virgin Remy human hair.",
         faq=[("What makes virgin curl different from curly?", "Virgin curl is never colored, so it stays in its natural shade. That makes it the safest base for dyeing."),
              ("Can I dye it?", "Yes. Unprocessed hair takes color best. We recommend a professional colorist."),
              ("Which shades are available?", "1B, 1 and Virgin."),
              ("How do I care for it?", "Treat it like natural curly hair: moisture, gentle detangling, air-drying.")]),
    dict(key="Permed Straight", name="Permed Straight", slug="permed-straight", curly=False,
         only_colors=["1", "1B", "Virgin", "350", "530", "Honey Auburn", "Honey Blonde", "Red"],
         short="Straight with a soft perm texture and extra body.",
         intro="Permed straight falls straight but has a soft perm texture through it, so it looks fuller and more natural than glassy, silky straight hair. It is a good match for relaxed or lightly textured natural hair and keeps its body between washes. Each Chesed permed straight wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 8 shades and lengths from 18 to 32 inches.",
         faq=[("How is permed straight different from straight?", "Straight is smooth and silky. Permed straight has a soft texture and more body, so it looks less flat."),
              ("Can I curl a permed straight wig?", "Yes. Use a heat protectant and a curling iron or wand."),
              ("Does it blend with my natural hair?", "It blends best with relaxed, silk-pressed or lightly textured hair."),
              ("Which shades are available?", "1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde and Red.")]),
    dict(key="Wet & Wavy", name="Wet & Wavy", slug="wet-and-wavy", curly=True,
         only_colors=["1", "1B", "Virgin", "350", "530", "Honey Auburn", "Honey Blonde", "Red"],
         short="Loose, glossy waves that look freshly wet-set.",
         intro="Wet & wavy has loose, flowing waves with a glossy, just-styled finish that looks like freshly wet-set hair. The pattern is defined from root to tip and moves easily. Each Chesed wet & wavy wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 8 shades and lengths from 18 to 32 inches. Refresh the waves with water and a light leave-in conditioner.",
         faq=[("How do I keep the waves defined?", "Wet the hair, add a leave-in conditioner and let it air-dry or diffuse. Avoid brushing when dry."),
              ("Is wet & wavy the same as body wave?", "No. Wet & wavy has a looser, glossier, more water-like pattern. Body wave is a softer S-shape."),
              ("Does it look shorter than its length?", "Yes. The waves take up length, so it sits about 2 inches higher than straight hair."),
              ("Which shades are available?", "1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde and Red.")]),
    # Deep Wave: a style from the client's feedback. Copy and photos are placeholders until Chesed confirms them.
    dict(key="Deep Wave", name="Deep Wave", slug="deep-wave", curly=True,
         only_colors=["1", "1B", "Virgin", "350", "530", "Honey Auburn", "Honey Blonde", "Red"],
         short="Deep, defined waves with full, bouncy volume.",
         intro="Deep wave has deep, defined waves that are tighter than a body wave and looser than a curl, so it looks full and bouncy from root to tip. Each Chesed deep wave wig is a lace front unit in 100% unprocessed virgin Remy human hair, in 8 shades and lengths from 18 to 32 inches. Refresh the pattern with water and a curl cream.",
         faq=[("How is deep wave different from loose deep wave?", "Deep wave has tighter, more defined waves. Loose deep wave is softer and more open."),
              ("How do I keep the waves defined?", "Wet the hair, apply a curl cream and let it air-dry or diffuse. Avoid brushing when dry."),
              ("Does it look shorter than its length?", "Yes. The waves take up length, so it sits 2 to 3 inches higher than straight hair."),
              ("Which shades are available?", "1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde and Red.")]),
]
TEX ={t["key"]: t for t in TEXTURES}

# name: the shade in words, shown instead of the number (client, 22 October 2026). Chesed to approve the wording.
COLORS = [
    dict(key="1B", name="Natural Black", slug="1b", hex="#2A201C", family="black",
         blurb="Soft off-black with a faint warm brown undertone. It is the closest match to most natural hair."),
    dict(key="1", name="Jet Black", slug="1", hex="#0E0E10", family="black",
         blurb="The deepest, coolest black we make. It is crisp and high-contrast, with no brown at all."),
    dict(key="Virgin", name="Natural Dark Brown", slug="virgin", hex="#2B1D16", family="black",
         blurb="Untreated hair in its natural dark brown-black, with soft espresso tones where light hits."),
    dict(key="530", name="Rich Wine Red", slug="530", hex="#6E1B2E", family="burgundy",
         blurb="Rich wine red with violet depth. It glows warm on deep skin and reads dark in low light."),
    dict(key="99J", name="Deep Plum", slug="99j", hex="#441A28", family="burgundy",
         blurb="Dark plum, cooler and deeper than burgundy, almost black cherry in shadow."),
    dict(key="350", name="Copper Ginger", slug="350", hex="#B4552C", family="ginger",
         blurb="Bright copper orange with lighter tones where the light catches it. It is our boldest warm shade."),
    dict(key="Honey Auburn", name="Honey Auburn", slug="honey-auburn", hex="#8D6038", family="auburn",
         blurb="Golden brown with soft honey highlights and slightly darker roots. It is warm, not orange."),
    dict(key="Natural Auburn", name="Natural Auburn", slug="natural-auburn", hex="#9E6B3C", family="auburn",
         blurb="A natural reddish brown that warms up in sunlight and stays soft indoors."),
    dict(key="Honey Blonde", name="Honey Blonde", slug="honey-blonde", hex="#C99A55", family="honey-blonde",
         blurb="Warm golden blonde from root to tip, buttery rather than ash or platinum."),
    dict(key="Red", name="Cherry Red", slug="red", hex="#B0141F", family="red",
         blurb="True cherry red from root to tip, with no orange and no pink."),
]
# what shoppers read: the name first, the number in brackets ("Rich Wine Red (530)"); shades already in words stay as they are
# (user, 30 October 2026). Web addresses keep the number.
for c in COLORS:
    c["label"] = c["name"] if c["key"] in (c["name"], "Red") else f"{c['name']} ({c['key']})"
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
        key, lab = c["key"], c["label"]
        q, a = COLOR_COMPARE[key]
        out.append(dict(
            slug=c["slug"], name=f"{lab} Wigs", label=key, shade=lab, h1=f"{lab} Wigs", colors=[key],
            title=f"{lab} Lace Front Wigs | Chesed Hair",
            intro=f"{c['blurb']} Shop {lab} lace front wigs in {tl}, made from 100% unprocessed virgin Remy human hair, in lengths from 18 to 32 inches.",
            faq=[(f"Which textures come in {lab}?", f"{tl.capitalize()}."), (q, a),
                 (f"Can I dye {lab}?", "Virgin is the best base for color because it has never been processed. We recommend a professional colorist for any color change."),
                 (f"How do I keep {lab} looking its best?", "Wash in cool water with sulfate-free shampoo and conditioner, and store the wig on a stand.")]))
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
# the client's cap and lace pictures, shown last in every wig's gallery (square, so they get the full width)
CAP_IMAGES = [dict(file="wig-cap-one-size", alt="One size fits all cap: 3-panel design, adjustable band, side and top and bottom security combs", info=True),
              dict(file="wig-cap-secure-fit", alt="13 by 5 inch pre-plucked HD lace and the 6x secure fit cap with elastic band and 4 security combs", info=True)]

def build_products():
    products = []
    for style, t in TEX.items():
        for color, c in COL.items():
            handle = f"{c['slug']}-{t['slug']}-lace-front-wig"
            title = f"{c['label']} {t['name']} Lace Front Wig"
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
            images = images + CAP_IMAGES
            products.append(dict(
                kind="wig", placeholder=placeholder,
                handle=handle, title=title, texture=t, color=c, price=wig_price(LENGTHS[0], style, color),
                images=images, url=f"/products/{handle}/",
                options=["Length"], variants=[dict(length=l, title=f'{l}"', price=wig_price(l, style, color), landmark=LANDMARKS[i]) for i, l in enumerate(LENGTHS)],
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
         intro="Handmade feather and crochet braid hair extensions in human hair, in textures from body wave and deep wave to water wave and wet & wavy. Pick your shade and length on each product page. Packs, weights and lengths vary by style, so check the details on the page.",
         faq=[("What are feather crochet extensions?", "They are hair extensions made to be installed with a crochet technique, so the finished look is seamless and light."),
              ("How many packs do I need for a full head?", "It depends on the style and the length you choose. Some listings offer a 3-pack full-head option. Ask us if you are not sure."),
              ("Can I dye or restyle them?", "They can be, but it is not recommended, because the hair is already styled and colored."),
              ("How long do they last?", "With care they can last up to a year. Textured styles need regular upkeep."),
              ("How do I choose a color and length?", "Each style comes in six colors, from natural black to honey blonde and ruby wine, and in lengths from 12 to 22 inches. Pick a color on the product page to see it on a model."),
              ("How fast will it ship, and can I return it?", "Orders ship within 1 business day and usually arrive in 2 to 6 business days. Unused extensions in their original packaging can be returned or exchanged within 30 days.")]),
    dict(kind="bundle", slug="hair-bundles", name="Hair Bundles", h1="Hair Bundles", noun="bundle", coming_soon=True, hidden=True,   # client: "coming soon", then hidden until the bundles arrive (27 October 2026)
         title="Human Hair Bundles | Chesed Hair",
         intro="Chesed hair bundles are coming soon: body wave, straight, deep wave and water wave, from natural darks to bold colors and blondes. In the meantime, shop our lace front wigs and crochet & feather extensions.",
         faq=[("Which bundle textures do you carry?", "Body wave, straight, deep wave and water wave."),
              ("How do I choose a shade?", "Dark shades (1, 1B, Virgin) are the natural blacks. The color bundles and blonde shades are lighter and bolder."),
              ("How many bundles do I need?", "Most people use 3 to 4 bundles for a full head. Longer lengths may need more."),
              ("Can I color or style them?", "Details to be confirmed by Chesed.")]),
]
EXTRA_BY_KIND = {c["kind"]: c for c in EXTRA_COLLECTIONS}

# Textures and colour families for the crochet extensions and bundles (read from each listing's title, options and details),
# so the menu and the collection page can filter them the way wigs are filtered.
# Kinky Curly and Loose Wave were dropped from the menu and filters: the client says they don't carry them (22 October 2026).
CROCHET_TEXTURES = [("body-wave", "Body Wave"), ("deep-wave", "Deep Wave"), ("water-wave", "Water Wave"),
                    ("wet-and-wavy", "Wet & Wavy"), ("straight", "Straight"), ("kinky-straight", "Kinky Straight"),
                    ("burmese-curly", "Burmese Curly")]
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
# Sample reviews for the preview (the client asked for demo reviews, 23 October 2026). Each one is tagged
# "Sample" on the page. Replace them with real customer reviews (Judge.me on Shopify) before launch.
REVIEWS = [   # real reviews from Chesed's TikTok Shop and Amazon customers (client, 29 October 2026); no star ratings were supplied
    dict(name="Danielle P.", stars=5, product='Body Wave Lace Front Wig, 22"', text="The lace was so thin it vanished at my hairline. I wore it to a wedding and got asked who my stylist was."),
    dict(name="Nia S.", stars=5, product='Kinky Curly Lace Front Wig, 18"', text="The curls are bouncy and defined right out of the box. I only needed a little water and leave-in to refresh them."),
    dict(name="Camille B.", stars=4.5, product="Wet & Wavy Feather Crochet", text="Installed in under an hour with the pre-made loops. The waves look so natural that my coworkers thought it was my hair."),
    dict(name="Renee A.", stars=5, product='Straight Lace Front Wig, 26"', text="Silky straight with no shedding. It holds a style with minimal heat and the cap fits snug without pinching."),
    dict(name="Tiana M.", stars=5, product="Deep Wave Feather Crochet", text="Soft, light, and it doesn’t smell like plastic the way other brands do. I’m already planning my second order."),
    dict(name="Shanice W.", stars=4.5, product='Loose Deep Wave Lace Front Wig, 20"', text="The density is perfect: full but not bulky. I trimmed the baby hairs myself and it looks like my own scalp."),
    dict(name="Imani K.", stars=5, product="Kinky Straight Feather Crochet", text="It blends so well with my natural texture. I’ve washed it three times and it still looks brand new."),
    dict(name="Gabrielle H.", stars=5, product='Virgin Curl Lace Front Wig, 16"', text="I took the shorter length because the guide said curls shrink, and it landed exactly where I wanted."),
    dict(name="Alicia R.", stars=4.5, product="Body Wave Feather Crochet", text="Great for a protective style. It’s lightweight, my edges feel comfortable, and it still looks fresh at week three."),
    dict(name="Brooklyn D.", stars=5, product="Burmese Curly Feather Crochet", text="The curls stay full all day and don’t tangle at the ends. The loops made installing it so easy, even as a beginner."),
]
REVIEWS_SOURCE = "From our customers on TikTok Shop and Amazon."

# Welcome wheel (email popup). Every spin wins; weights are the real odds and are shown to shoppers.
# Placeholder prizes and codes: Chesed sets the final offers and creates the codes in Shopify.
# The codes exist in Chesed's store as one-use-per-customer discounts; min is the order needed for the dollar codes.
SPIN_PRIZES = [
    dict(label="10% off", code="WELCOME10", pct=10, amt=0, min=0, weight=35),
    dict(label="$20 off", code="SAVE20", pct=0, amt=20, min=100, weight=25),
    dict(label="15% off", code="WELCOME15", pct=15, amt=0, min=0, weight=20),
    dict(label="$40 off", code="SAVE40", pct=0, amt=40, min=150, weight=10),
    dict(label="20% off", code="WELCOME20", pct=20, amt=0, min=0, weight=7),
    dict(label="$60 off", code="SAVE60", pct=0, amt=60, min=200, weight=3),
]

# WhatsApp chat button. Placeholder: Chesed's WhatsApp Business number, digits only with country code.
WHATSAPP = "10000000000"
WHATSAPP_PLACEHOLDER = True

# FAQs: wig questions on wig pages, crochet questions on crochet pages, a general mix on the homepage and the FAQ page
WIG_FAQ = [
    ("What are Chesed wigs made of?", "Every Chesed wig is 100% unprocessed virgin Remy human hair on a lace front, so you can color, heat-style and wash it like your own hair."),
    ("What lace and cap do the wigs have?", "A 13x5 lace front for a natural hairline, on a cap that is one size fits all."),
    ("How do I choose my length?", "Use the length guide: it shows where each length from 18 to 32 inches ends on the body. Waves and curls sit about 2 inches higher than straight hair."),
    ("How do I choose my shade?", "Every shade is shown on the same model in real rooms. The color guide puts all ten side by side, including the ones people mix up, like 1B vs 1."),
    ("What if the wig isn't right?", "Return or exchange unused wigs within 30 days with the lace uncut. Your first US return label is free."),
]
SHIP_FAQ = [
    ("How fast is shipping?", f"Orders ship within 1 business day by express shipping and usually arrive in 2 to 6 business days. US shipping is free on orders over ${int(FREE_SHIP)}."),
    ("Can I cancel my order?", "Email us within 1 hour of ordering. Once an order has shipped it can't be cancelled, but you can return it."),
    ("What is your return policy?", "Return or exchange unused hair within 30 days of receiving it, in its original packaging. Wigs must have the lace uncut. Email us your order number and a few photos to start, and your first US return label is free."),
    ("Can I pay in instalments?", "Yes. Choose Shop Pay at checkout to pay in 4 interest-free payments."),
]
GENERAL_FAQ = [
    ("What is Chesed hair made of?", "Our lace front wigs and our crochet and feather extensions are all human hair. The wigs are 100% unprocessed virgin Remy hair, so you can color, heat-style and wash them like your own."),
    ("Should I choose a wig or crochet extensions?", "A lace front wig is a complete look you put on and take off in minutes. Crochet and feather extensions are installed into your own braids with a crochet needle, for a light, seamless look that stays in day and night. Not sure? Email us and we'll help you choose."),
    ("Can I dye or restyle Chesed hair?", "Our wigs can be dyed, bleached and permed like your own hair. Crochet and feather extensions are already styled and colored, so we don't recommend dyeing them."),
]
HOME_FAQ = GENERAL_FAQ[:2] + [
    ("How do I choose my shade and length?", "For wigs, the color guide shows all ten shades on the same model, and the length guide shows where every length from 18 to 32 inches ends on the body. For crochet, each product page shows every color on a model, in lengths from 12 to 22 inches."),
    SHIP_FAQ[0],
    ("What if it isn't right?", "Return or exchange unused hair within 30 days, in its original packaging (wigs with the lace uncut). Your first US return label is free."),
]


def length_photo(key, lengths=None):
    """One length photo with the height of each length line, in % of the photo (18" at 500px of 1200, 30px an inch).
    Wigs by default; pass CROCHET_LENGTHS for crochet."""
    ph = next(c for c in LENGTH_PHOTOS if c["key"] == key)
    return dict(ph, file=f"length-{key}", lines=[dict(len=L, y=round((500 + (L - ph["up"] - 18) * 30) / 12, 2)) for L in lengths or LENGTHS])


def wheel_svg():
    """The spin wheel as SVG markup."""
    import math
    n, r, cx = len(SPIN_PRIZES), 150, 160
    fills = ["#0E0E10", "#EE467C", "#FBFAF9", "#B8295A", "#26262B", "#F7E9EE"]
    inks = ["#FBFAF9", "#0E0E10", "#0E0E10", "#FBFAF9", "#FBFAF9", "#0E0E10"]
    out = [f'<svg class="wheel" viewBox="0 0 320 320" aria-hidden="true"><g id="wheelSpin">']
    for i, pz in enumerate(SPIN_PRIZES):
        a0, a1 = (i / n) * 2 * math.pi - math.pi / 2, ((i + 1) / n) * 2 * math.pi - math.pi / 2
        x0, y0, x1, y1 = cx + r * math.cos(a0), cx + r * math.sin(a0), cx + r * math.cos(a1), cx + r * math.sin(a1)
        out.append(f'<path d="M{cx} {cx}L{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{fills[i % 6]}" stroke="#0E0E10" stroke-width="1"/>')
        mid = (i + .5) * 360 / n
        out.append(f'<text transform="rotate({mid:.1f} {cx} {cx}) translate({cx} {cx - r * .62}) rotate({-90 if mid < 180 else 90})" fill="{inks[i % 6]}" text-anchor="middle" dominant-baseline="middle">{pz["label"]}</text>')
    out.append(f'</g><circle cx="{cx}" cy="{cx}" r="22" fill="#FBFAF9" stroke="#0E0E10"/><circle cx="{cx}" cy="{cx}" r="5" fill="#B8295A"/></svg>')
    return "".join(out)

# FAQ page sections: (anchor, heading, questions)
FAQ_PAGE = [("general", "General", GENERAL_FAQ), ("wigs", "Lace front wigs", WIG_FAQ),
            ("crochet", "Crochet & feather extensions", [f for f in EXTRA_BY_KIND["crochet"]["faq"] if "ship" not in f[0].lower()]),
            ("shipping", "Shipping & returns", SHIP_FAQ)]

# Info pages: (handle, SEO title, heading, lede, body HTML) and the how-it-works steps on Shipping and Returns
PAGES = [
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
    ("shipping", "Shipping | Chesed Hair", "Shipping", "Ships within 24 hours. Arrives in 2 to 6 business days.", "<h2>Processing</h2><p>Orders ship within 1 business day (24 hours) of payment, Monday to Friday. You get a confirmation email when you order and a tracking link when it ships.</p><h2>Delivery</h2><p>Every order ships by express shipping and usually arrives in 2 to 6 business days. Allow 2 to 3 extra days around weekends, holidays and busy periods.</p><h2>Shipping cost</h2><p>Free US shipping on orders over ${fs}.</p><h2>Cancelling an order</h2><p>Email us within 1 hour of placing your order to cancel it. Once an order has shipped it can't be cancelled, but you can return it.</p><h2>Questions about your delivery</h2><p>Email <a href='mailto:chesedhaircollection@gmail.com'>chesedhaircollection@gmail.com</a> with your order number. If there is a problem or delay we'll email you.</p>".replace("{fs}", str(int(FREE_SHIP)))),
    ("returns", "Returns | Chesed Hair", "Returns & Exchanges", "30 days to return or exchange unused hair.", "<h2>30-day returns and exchanges</h2><p>You can return or exchange unused hair within 30 days of receiving it.</p><h2>What we can accept</h2><ul><li>Hair in its original condition: not worn, washed, cut, dyed, bleached or styled.</li><li>Lace untouched: not cut or trimmed.</li><li>Original packaging, with any tags.</li></ul><p>Hair touches the scalp, so for hygiene we can't accept used items.</p><h2>How to start a return</h2><p>Email <a href='mailto:chesedhaircollection@gmail.com'>chesedhaircollection@gmail.com</a> with your order number, the reason and a few photos of the item. Once we approve it we'll send the return address. Returns sent without approval can't be refunded.</p><h2>Return shipping</h2><p>Each US order gets one free prepaid return label. After that, return shipping is paid by you. If we sent the wrong item or it arrived damaged, we cover the return.</p><h2>Refunds</h2><p>We refund to your original payment method within 2 business days of receiving and checking your return. Card refunds can take up to 10 business days to show; Shop Pay instalments and PayPal usually take about 3.</p><h2>Exchanges</h2><p>Same steps as a return. Your new item ships within 3 business days of your return arriving.</p>"),
    ("contact", "Contact | Chesed Hair", "Contact", None, "<p>Email <a href='mailto:chesedhaircollection@gmail.com'>chesedhaircollection@gmail.com</a>. We reply within 1 business day.</p>"),
]
PAGE_STEPS = {
    "shipping": [("bag", "You order", "Pay in full or in 4 with Shop Pay. You get a confirmation email right away."),
                 ("box", "We pack and ship", "Your order ships within 1 business day, with tracking."),
                 ("home", "It arrives", f"Express delivery in 2 to 6 business days. Free US shipping on orders over ${int(FREE_SHIP)}.")],
    "returns": [("chat", "Tell us within 30 days", "Email us your order number, the reason and a few photos. Once approved, we send the return address and a free US label."),
                ("box", "Send it back", "Unused, with the lace uncut and the hair in its original packaging."),
                ("card", "Get your refund", "Refunded to your original payment within 2 business days of it arriving.")],
}
