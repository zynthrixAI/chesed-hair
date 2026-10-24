"""Crochet & feather photos from Chesed's Amazon folder -> assets/p/ and src/extras.json.

Each style folder has one subfolder per colour (with a square "thumb" photo: model and product)
and info slides (size chart, human hair, feather crochet, packs, pack comparisons). The gallery is
the six colour photos, then the slides. Burmese Magic (only live on Amazon) is added back here.
Run once after the Amazon folder changes:  python src/tools/import_amazon_crochet.py
"""
import glob, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
AMZ = r"D:\Work\Chesed Hair\Images\Assets - Chesed Hair\Amazon-20261022T201515Z-1-001\Amazon"
OUT_P = os.path.join(REPO, "assets", "p")
EXTRAS = os.path.join(REPO, "src", "extras.json")

STYLES = {  # Amazon folder -> (handle, colour subfolder prefix)
    "Wet and Wavy": ("seamless-wet-and-wavy-feather-crochet-braid-hair-extensions", "WW"),
    "Kinky Straight": ("seamless-kinky-straight-feather-crochet-braid-hair-extensions", "Kinky"),
    "Burmese Curl": ("seamless-burmese-curly-feather-crochet-braid-hair-extensions", "Burmese"),
    "Body Wave": ("seamless-body-wave-feather-crochet-braid-hair-extensions", "BW"),
    "Deep Wave": ("seamless-deep-wave-feather-crochet-braid-hair-extensions", "DW"),
    "Magic Burmese Curl": ("seamless-burmese-magic-feather-crochet-braid-hair-extensions", "BMC"),
}
COLORS = ["Natural Black", "Black", "Honey Blonde", "Honey Auburn", "Brown Auburn", "Ruby Wine"]   # the option order on the site
SLIDES = [("slide1-chart*", "Size chart: strands per pack for each length"), ("slide2*", "Knotless crochet loop, pre-separated and pre-made"),
          ("slide3*", "100% human hair, soft and natural unprocessed virgin Remy"), ("slide4*", "Feather crochet: dye, bleach and perm, tangle and shed free, feathered ends, washable"),
          ("slide5*", "Wet and wavy texture"), ("slide_pack_comparison1*", "How many packs: 1 pack, 2 packs or 3 packs for a full head"),
          ("slide_pack_comparison2*", "Crochet hair compared with bulk hair")]


def save(src, base):
    im = Image.open(src).convert("RGBA")
    flat = Image.new("RGB", im.size, (255, 255, 255))
    flat.paste(im, (0, 0), im)
    for w in (1024, 560):
        flat.resize((w, round(flat.height * w / flat.width)), Image.LANCZOS).save(os.path.join(OUT_P, f"{base}-{w}.webp"), "WEBP", quality=84, method=6)


products = json.load(open(EXTRAS, encoding="utf-8"))
by_handle = {p["handle"]: p for p in products}

# Burmese Magic Curl: same lengths, colours and prices as Burmese Curl
if STYLES["Magic Burmese Curl"][0] not in by_handle:
    ref = by_handle[STYLES["Burmese Curl"][0]]
    bm = json.loads(json.dumps(ref))
    bm.update(handle=STYLES["Magic Burmese Curl"][0], title="Seamless Burmese Magic Curl Feather Crochet Braid Hair Extensions",
              status="active", source="Amazon folder (Magic Burmese Curl)")
    bm["desc"] = [d.replace("Burmese Curly", "Burmese Magic Curl").replace("Burmese Curl", "Burmese Magic Curl") for d in bm["desc"]]
    products.insert(products.index(ref) + 1, bm)
    by_handle[bm["handle"]] = bm

for folder, (handle, prefix) in STYLES.items():
    p = by_handle[handle]
    for old in glob.glob(os.path.join(OUT_P, f"{handle}-*.webp")):
        os.remove(old)
    images, n = [], 0
    for color in COLORS:
        thumbs = glob.glob(os.path.join(AMZ, folder, f"{prefix} {color}", "*thumb*"))
        if not thumbs:
            print("no photo:", folder, color)
            continue
        n += 1
        save(thumbs[0], f"{handle}-{n}")
        images.append(dict(file=f"{handle}-{n}", alt=f"{p['title']} in {color}", color=color))
    for pattern, alt in SLIDES:
        found = sorted(glob.glob(os.path.join(AMZ, folder, pattern)))
        if found:
            n += 1
            save(found[0], f"{handle}-{n}")
            images.append(dict(file=f"{handle}-{n}", alt=alt))
    p["images"] = images
    print(folder, len(images), "photos")

json.dump(products, open(EXTRAS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
