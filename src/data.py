"""Catalog data for the Chesed Hair preview.

Products are shaped like Shopify product objects (handle, title, options,
variants, images, metafields) so the templates port to Liquid with few changes.
Prices, shipping threshold and review counts are PLACEHOLDERS until the client confirms them.
"""
import json, os, re

HERE = os.path.dirname(__file__)
PICKS = json.load(open(os.path.join(HERE, "picks.json")))

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
              ("Which shade sells best in body wave?", "Natural Black 1B is the everyday choice. Burgundy 530 and Ginger 350 are the statement shades.")]),
    dict(key="Curly", name="Curly", slug="curly", curly=True,
         short="Small, dense spiral curls with full volume.",
         intro="Our curly lace front wigs have small, dense spiral curls that look full from root to tip. They are made from 100% unprocessed virgin Remy human hair and come in 9 shades and lengths from 10 to 32 inches. Curly units give the most volume of any Chesed texture, so a shorter length still reads big. Refresh the curls with water and a leave-in conditioner between washes.",
         faq=[("How do I keep the curls defined?", "Wet the hair, apply a leave-in conditioner and let it air-dry. Avoid brushing curls when dry."),
              ("Does a curly wig look shorter?", "Yes. Curls shrink, so a curly wig sits 2 to 4 inches higher than its stretched length."),
              ("Can I wear it straight?", "You can blow it out and flat iron it. The curls return when the hair gets wet."),
              ("How full is a curly wig?", "Curly units look the fullest of all our textures because each curl takes up more space.")]),
    dict(key="Kinky Curly", name="Kinky Curly", slug="kinky-curly", curly=True,
         short="Tight, springy coils that blend with natural 4C hair.",
         intro="Kinky curly wigs have tight, springy coils that match natural 4B and 4C hair, so the hairline blends instead of standing out. This lace front unit is made from 100% unprocessed virgin Remy human hair, currently in Burgundy 530, in lengths from 10 to 32 inches. It is the most natural-looking option if you want a wig that looks like your own hair grown out.",
         faq=[("Will kinky curly blend with my natural hair?", "Yes. The coil pattern is made to match 4B and 4C textures."),
              ("How much does kinky curly shrink?", "A lot. Expect it to sit 4 or more inches higher than its stretched length."),
              ("How do I detangle it?", "Finger-detangle while wet with conditioner, working from the ends up."),
              ("Which colors does kinky curly come in?", "Burgundy 530 for now. More shades are planned.")]),
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
         intro="Virgin curl wigs are curly units left in their natural, uncolored state, so the hair has never been processed. That makes them the best base if you plan to dye the wig yourself later. They come in Natural Black 1B, Jet Black 1 and Virgin Natural, in lengths from 10 to 32 inches, as lace front units in 100% unprocessed virgin Remy human hair.",
         faq=[("What makes virgin curl different from curly?", "Virgin curl is never colored, so it stays in its natural shade. That makes it the safest base for dyeing."),
              ("Can I dye it?", "Yes. Unprocessed hair takes color best. We recommend a professional colorist."),
              ("Which shades are available?", "Natural Black 1B, Jet Black 1 and Virgin Natural."),
              ("How do I care for it?", "Treat it like natural curly hair: moisture, gentle detangling, air-drying.")]),
]
TEX = {t["key"]: t for t in TEXTURES}

COLORS = [
    dict(key="Natural Black 1B", slug="natural-black-1b", hex="#2A201C", family="black",
         blurb="Soft off-black with a faint warm brown undertone. It is the closest match to most natural hair."),
    dict(key="Jet Black 1", slug="jet-black-1", hex="#0E0E10", family="black",
         blurb="The deepest, coolest black we make. It is crisp and high-contrast, with no brown at all."),
    dict(key="Virgin Natural", slug="virgin-natural", hex="#2B1D16", family="black",
         blurb="Untreated hair in its natural dark brown-black, with soft espresso tones where light hits."),
    dict(key="Burgundy 530", slug="burgundy-530", hex="#6E1B2E", family="burgundy",
         blurb="Rich wine red with violet depth. It glows warm on deep skin and reads dark in low light."),
    dict(key="99J Plum", slug="99j-plum", hex="#441A28", family="burgundy",
         blurb="Dark plum, cooler and deeper than burgundy, almost black cherry in shadow."),
    dict(key="Ginger 350", slug="ginger-350", hex="#B4552C", family="ginger",
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

COLOR_COLLECTIONS = [
    dict(slug="black", name="Black Wigs", h1="Black Wigs", colors=["Natural Black 1B", "Jet Black 1", "Virgin Natural"],
         title="Black Wigs: 1B, Jet Black & Virgin | Chesed",
         intro="Three blacks, three different looks. Natural Black 1B is soft off-black with a warm undertone, the closest match to most natural hair. Jet Black 1 is the deepest, coolest black. Virgin Natural is untreated hair in its own dark brown-black. Every black wig is a lace front unit in 100% unprocessed virgin Remy human hair, in every texture and length from 10 to 32 inches.",
         faq=[("What is the difference between 1B and 1?", "1B is off-black with a warm brown undertone. 1 is jet black, cooler and darker."),
              ("Which black looks most natural?", "Natural Black 1B for most people. Virgin Natural is the softest."),
              ("Can I dye a black wig?", "Virgin Natural is the best base for color because it has never been processed."),
              ("Do black wigs come in every texture?", "Yes, all seven textures.")]),
    dict(slug="burgundy", name="Burgundy & 99J Wigs", h1="Burgundy & 99J Wigs", colors=["Burgundy 530", "99J Plum"],
         title="Burgundy 530 & 99J Plum Wigs | Chesed Hair",
         intro="Burgundy 530 is a rich wine red with violet depth. 99J Plum is darker and cooler, almost black cherry in shadow. Both glow on deep skin and soften into a dark shade indoors, which makes them the easiest bold colors to wear daily. Shop burgundy lace front wigs in 100% unprocessed virgin Remy human hair, from 10 to 32 inches.",
         faq=[("What is the difference between 530 and 99J?", "530 is a brighter wine red. 99J is a darker, cooler plum."),
              ("Does burgundy fade?", "Wash in cool water with a color-safe shampoo to keep the shade rich."),
              ("Which textures come in burgundy?", "Burgundy 530 comes in six textures. 99J Plum is in body wave."),
              ("Is burgundy good for dark skin?", "Yes. It is one of the most flattering bold shades on deep skin.")]),
    dict(slug="auburn", name="Auburn Wigs", h1="Auburn Wigs", colors=["Honey Auburn", "Natural Auburn"],
         title="Honey & Natural Auburn Wigs | Chesed Hair",
         intro="Auburn sits between brown and red. Honey Auburn is golden brown with soft honey highlights. Natural Auburn is a natural reddish brown that warms up in sunlight. Both add warmth without going full red. Every auburn wig is a lace front unit in 100% unprocessed virgin Remy human hair, from 10 to 32 inches.",
         faq=[("What is the difference between honey auburn and natural auburn?", "Honey Auburn has golden highlights. Natural Auburn is a more even reddish brown."),
              ("Is auburn orange?", "No. Both shades are brown-based, warm but not orange."),
              ("Which textures come in auburn?", "Body wave, curly, kinky straight, loose deep wave and straight."),
              ("Will auburn suit deep skin?", "Yes. Warm browns flatter warm undertones especially well.")]),
    dict(slug="ginger", name="Ginger Wigs", h1="Ginger Wigs", colors=["Ginger 350"],
         title="Ginger 350 Lace Front Wigs | Chesed Hair",
         intro="Ginger 350 is our boldest warm shade: bright copper orange with lighter tones where the light catches it. It turns heads in daylight and glows under warm lamps. Shop ginger lace front wigs in body wave, curly, kinky straight, loose deep wave and straight, made from 100% unprocessed virgin Remy human hair, from 10 to 32 inches.",
         faq=[("Is ginger 350 orange or red?", "Orange-copper. It is brighter and more orange than auburn."),
              ("How do I keep ginger bright?", "Use color-safe shampoo and cool water."),
              ("Which textures come in ginger?", "Body wave, curly, kinky straight, loose deep wave and straight."),
              ("Does ginger suit dark skin?", "Yes. It is one of the most popular bold shades on deep skin.")]),
    dict(slug="honey-blonde", name="Honey Blonde Wigs", h1="Honey Blonde Wigs", colors=["Honey Blonde"],
         title="Honey Blonde Lace Front Wigs | Chesed Hair",
         intro="Honey Blonde is warm golden blonde from root to tip: buttery rather than ash or platinum, so it looks soft against deep skin instead of harsh. Shop honey blonde lace front wigs in body wave, curly, kinky straight, loose deep wave and straight, made from 100% unprocessed virgin Remy human hair, from 10 to 32 inches.",
         faq=[("Is honey blonde the same as 613?", "No. Honey blonde is a warm golden shade. 613 is a pale platinum blonde."),
              ("Will honey blonde look brassy?", "It is meant to be warm. A purple shampoo once a month keeps it golden, not orange."),
              ("Which textures come in honey blonde?", "Body wave, curly, kinky straight, loose deep wave and straight."),
              ("Does honey blonde suit deep skin?", "Yes. Warm blondes flatter deep skin more than ash blondes.")]),
    dict(slug="red", name="Red Wigs", h1="Red Wigs", colors=["Red"],
         title="Red Lace Front Wigs, 10-32 Inch | Chesed",
         intro="Our Red is true cherry red from root to tip, with no orange and no pink. It is the most saturated shade in the range, made for statement looks. Shop red lace front wigs in body wave, curly, kinky straight, loose deep wave and straight, made from 100% unprocessed virgin Remy human hair, from 10 to 32 inches.",
         faq=[("Will red fade quickly?", "All bright reds fade a little. Cool water and color-safe shampoo keep it vivid."),
              ("Is this red or burgundy?", "True red. For a darker wine shade, see Burgundy 530."),
              ("Which textures come in red?", "Body wave, curly, kinky straight, loose deep wave and straight."),
              ("Does red suit dark skin?", "Yes. A true red reads rich and vivid on deep skin.")]),
]

POSE_ORDER = ["Straight-On Front", "Fingers Through Lengths", "Head Tilt Fingers Through Roots",
              "Smile Fingers Through Hair", "Three-Quarter Hand Through Lengths", "Both Hands in Hair",
              "Chin Up Hand Behind Head", "Smile Hand at Temple"]

def build_products():
    groups = {}
    for p in PICKS:
        groups.setdefault((p["style"], p["color"]), []).append(p)
    products = []
    for (style, color), picks in groups.items():
        t, c = TEX[style], COL[color]
        handle = f"{c['slug']}-{t['slug']}-lace-front-wig"
        title = f"{color} {t['name']} Lace Front Wig"
        def pose_of(p): return p["new"].split(" - ")[2]
        picks = sorted(picks, key=lambda p: (POSE_ORDER.index(pose_of(p)) if pose_of(p) in POSE_ORDER else 99, p["new"]))
        images = []
        for i, p in enumerate(picks):
            parts = p["new"].rsplit(".", 1)[0].split(" - ")
            scene = " - ".join(parts[2:])
            images.append(dict(
                src=p["src"],
                file=f"{handle}-{slug(scene)}",
                alt=f"{color} {t['name'].lower()} lace front wig on model, {parts[2].lower()}, {parts[3].lower()}",
            ))
        products.append(dict(
            handle=handle, title=title, texture=t, color=c, price=PRICE,
            images=images, url=f"/products/{handle}/",
            options=["Length"], variants=[dict(length=l, title=f'{l}"', price=PRICE, landmark=LANDMARKS[i]) for i, l in enumerate(LENGTHS)],
        ))
    # sort: texture order then color order
    tix = {t["key"]: i for i, t in enumerate(TEXTURES)}
    cix = {c["key"]: i for i, c in enumerate(COLORS)}
    products.sort(key=lambda p: (tix[p["texture"]["key"]], cix[p["color"]["key"]]))
    return products

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
