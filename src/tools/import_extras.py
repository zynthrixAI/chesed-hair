"""One-off importer: client CSV + item list -> src/extras.json and photos in assets/p/.
Run from the repo root:  python <this file>
"""
import csv, collections, html, io, json, os, re, sys, urllib.request, zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

REPO = r"C:\Users\syedh\code\chesed-hair"
DOCS = r"D:\Work\Chesed Hair\Documents"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dl")
os.makedirs(CACHE, exist_ok=True)
OUT_P = os.path.join(REPO, "assets", "p")

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and")).strip("-")

# ---------- crochet / feather extensions from the Shopify export ----------
TITLES = {  # CSV row order -> clean title. Missing index = skipped duplicate.
    0: "Seamless Wet & Wavy Feather Crochet Braid Hair Extensions",
    1: "Deep Curly Handmade Hair Extensions",
    2: "Seamless Kinky Straight Feather Crochet Braid Hair Extensions",
    3: "Seamless Burmese Curly Feather Crochet Braid Hair Extensions",
    4: "Seamless Body Wave Feather Crochet Braid Hair Extensions",
    5: "Seamless Deep Wave Feather Crochet Braid Hair Extensions",
    # 6 removed: client asked to drop it (a Shopify draft), 22 October 2026
    7: "Water Wave Micro-Ring Hair Extensions",
    8: "Lightweight Natural Black Human Hair Extensions",
    9: "Handmade Feather Human Hair Extensions",
    10: "Water Wave Soft Feather Human Hair Extensions",
    # 11 skipped: same title as 10, and its only color (Deep Brown #2) is already in 10
    12: "Multi-Color Deep Wave Feather Crochet Braid Hair Extensions",
    13: "Multi-Color Kinky Curly Crochet Braid Hair Extensions",
    14: "Soft Deep Wave Feather Crochet Braid Hair Extensions",
    15: "Kinky Curly Micro-Ring Loop Hair, Highlight #4/27/30",
    16: "Soft Natural Black Straight Feather Crochet Braid Hair Extensions",
    17: "Invisible Water Wave Brown Highlight Feather Crochet Hair Extensions",
    18: "Deep Wave Feather Crochet Braid Human Hair Extensions",
    19: "Multi-Color Water Wave Crochet Braid Hair Extensions",
    20: "Soft Kinky Curly Feather Crochet Braid Hair Extensions",
    # 21 removed: client asked to drop it (a Shopify draft), 22 October 2026
    # 22 skipped: identical options and prices to 18
}
OPT_NAME = {"Hair Length": "Length", "Colors": "Color", "Hair Color": "Color", "Color": "Color",
            "Hair Texture": "Texture", "Pack(S)": "Pack"}
OPT_ORDER = ["Texture", "Color", "Pack", "Length"]
JUNK = re.compile(r"\s*\((?:HOT|sale|Hot Sale|Limited Stock|Influencer Length|Influencer Recommend)\)\s*", re.I)

def clean_val(v):
    v = v.replace("\ufffd", "").replace("\u00a0", " ")
    v = JUNK.sub("", v)
    v = re.sub(r"''|′′|\"|”|″", '"', v).strip()
    v = re.sub(r"(\d)\s*$", r"\1", v)
    if re.fullmatch(r"\d+", v):                      # "26" that lost its inch mark
        v += '"'
    return re.sub(r"\s+", " ", v)

def parse_text(body):
    """Product detail lines from the old listing, minus its shipping and returns boilerplate."""
    t = re.sub(r"<img[^>]*>", "", body)
    t = re.sub(r"</?(br|p|div|li|tr|td|th|h\d)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\ufffd", "").replace("\u00a0", " ")
    lines = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
    lines = [l for l in lines if l]
    return lines

def details_from(lines):
    out = []
    if "PRODUCT DETAILS" in lines:
        i = lines.index("PRODUCT DETAILS") + 1
        seg = []
        while i < len(lines) and not lines[i].startswith("PURCHASE INFO") and lines[i] != "PRODUCT DESCRIPTION":
            seg.append(lines[i]); i += 1
        # key / value pairs
        keep = {"Package", "Hair Texture", "Hair Length", "Hair Quality", "Weight", "Color", "Last For", "Can Be Dyed/Restyled"}
        k = 0
        while k < len(seg) - 1:
            if seg[k] in keep or seg[k].startswith("Hair Quality"):
                out.append((seg[k].replace("Hair Quality", "Hair quality"), seg[k + 1])); k += 2
            else:
                k += 1
    desc = []
    if "PRODUCT DESCRIPTION" in lines:
        i = lines.index("PRODUCT DESCRIPTION") + 1
        while i < len(lines) and not lines[i].isupper():
            desc.append(lines[i]); i += 1
    return out, desc

rows = list(csv.DictReader(open(os.path.join(DOCS, "products_export_1.csv"), encoding="utf-8-sig")))
P = collections.OrderedDict()
for r in rows:
    P.setdefault(r["Handle"], []).append(r)

products, dl = [], []
used = set()
for idx, (h, rs) in enumerate(P.items()):
    if idx not in TITLES:
        continue
    r0 = rs[0]
    title = TITLES[idx]
    handle = slug(title)
    assert handle not in used, handle
    used.add(handle)
    names = [r0[f"Option{k} Name"] for k in (1, 2, 3) if r0[f"Option{k} Name"]]
    onames = [OPT_NAME[n] for n in names]
    variants, seen = [], set()
    for r in rs:
        vals = [clean_val(r[f"Option{k} Value"]) for k in (1, 2, 3) if r0[f"Option{k} Name"]]
        if not vals or not r["Variant Price"] or tuple(vals) in seen:
            continue
        seen.add(tuple(vals))
        v = dict(o=dict(zip(onames, vals)), price=float(r["Variant Price"]))
        variants.append(v)
    order = [n for n in OPT_ORDER if n in onames]
    options = []
    for n in order:
        vals = []
        for v in variants:
            if v["o"][n] not in vals:
                vals.append(v["o"][n])
        if n == "Length":
            vals.sort(key=lambda x: int(re.match(r"\d+", x).group()))
        options.append(dict(name=n, values=vals))
    lines = parse_text(r0["Body (HTML)"])
    details, desc = details_from(lines)
    imgs, seen_u = [], set()
    for r in sorted((x for x in rs if x["Image Src"]), key=lambda x: int(x["Image Position"] or 0)):
        u = r["Image Src"].split("?")[0]
        if u in seen_u or "machine-made-vs" in u:
            continue
        seen_u.add(u); imgs.append(r["Image Src"])
    imgs = imgs[:8]
    files = []
    for n, u in enumerate(imgs, 1):
        files.append(f"{handle}-{n}")
        dl.append((u, f"{handle}-{n}"))
    products.append(dict(kind="crochet", handle=handle, title=title, status=r0["Status"], options=options, variants=variants,
                         images=[dict(file=f, alt=f"{title}, photo {i + 1}") for i, f in enumerate(files)],
                         details=details, desc=desc, source=h))

# ---------- the item list ----------
z = zipfile.ZipFile(os.path.join(DOCS, "TalkFile_ITEM LIST.xlsx.xlsx"))
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ss = ["".join(t.text or "" for t in si.iter(M + "t")) for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
def sheet(n):
    out = {}
    for row in ET.fromstring(z.read(f"xl/worksheets/{n}.xml")).iter(M + "row"):
        for c in row.findall(M + "c"):
            v = c.find(M + "v")
            if v is not None:
                out[c.get("r")] = ss[int(v.text)].strip() if c.get("t") == "s" else v.text
    return out
s1 = sheet("sheet1")

def color_label(c):
    c = c.replace("#", "").strip()
    m = {"RED": "Red", "HONEY AUBURN": "Honey Auburn", "HONEY BLOND HL": "Honey Blonde HL", "TPRED": "TPRed", "VIRGIN": "Virgin"}
    if c.upper() in m:
        return m[c.upper()]
    if re.fullmatch(r"[0-9/]+B?", c) or c.upper().startswith("TP"):
        return ("#" + c) if not c.upper().startswith("TP") else c.upper()
    return c.title()

def bundle(title_row, name, last_len_row, cols):
    colors = []
    for col in cols:
        v = s1.get(f"{col}{title_row}")
        if v:
            colors.append(color_label(v))
    lens = []
    r = title_row + 1
    while r <= last_len_row:
        v = s1.get(f"A{r}")
        if v:
            lens.append(v.replace('"', ""))
        r += 1
    return name, colors, [f'{l}"' for l in lens]

from string import ascii_uppercase as AZ
B = [bundle(3, "Body Wave", 14, AZ[1:22]), bundle(18, "Straight", 29, AZ[1:22]),
     bundle(33, "Deep Wave", 41, AZ[1:11]), bundle(45, "Water Wave", 53, AZ[1:12])]
BUNDLE_PRICE = 99.00   # placeholder until Chesed sends bundle prices
for name, colors, lens in B:
    title = f"{name} Hair Bundle"
    variants = [dict(o={"Color": c, "Length": l}, price=BUNDLE_PRICE) for c in colors for l in lens]
    products.append(dict(kind="bundle", handle=slug(title), title=title, status="active", placeholder_price=True,
                         options=[dict(name="Color", values=colors), dict(name="Length", values=lens)],
                         variants=variants, images=[dict(file="placeholder", alt="Photo coming soon", placeholder=True)],
                         details=[("Texture", name), ("Lengths", f"{lens[0]} to {lens[-1]}"), ("Shades", f"{len(colors)} shades")], desc=[], source="item list: Bundle"))

# Burmese Magic crochet: on the item list but not in the export.
# Kept: the client sent its Amazon photos (23 October 2026); photos come from import_amazon_crochet.py.
bm_colors = ["Natural", "Natural Black", "Brown Auburn", "Honey Auburn", "Honey Blonde HL", "Ruby Red", "Salt & Pepper"]
bm_lens = ['12"', '14"', '16"', '18"', '22"']
ref = next(p for p in products if p["handle"].startswith("seamless-burmese-curly"))
bm_price = {l: min(v["price"] for v in ref["variants"] if v["o"].get("Length") == l) for l in bm_lens}
products.append(dict(kind="crochet", handle="seamless-burmese-magic-feather-crochet-braid-hair-extensions",
                     title="Seamless Burmese Magic Curl Feather Crochet Braid Hair Extensions", status="active",
                     options=[dict(name="Color", values=bm_colors), dict(name="Length", values=bm_lens)],
                     variants=[dict(o={"Color": c, "Length": l}, price=bm_price[l]) for c in bm_colors for l in bm_lens],
                     images=[dict(file="placeholder", alt="Photo coming soon", placeholder=True)],
                     details=[], desc=[], source="item list: Crochet"))

# Only listings that were live in Shopify go on the site; drafts were tests (client, 22 October 2026)
products = [p for p in products if p["kind"] != "crochet" or p["status"] == "active"]
# then run src/tools/import_amazon_crochet.py for the crochet photos (Amazon set)
json.dump(products, open(os.path.join(REPO, "src", "extras.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(products), "products;", len(dl), "images to fetch")

# ---------- photos ----------
def fetch(item):
    u, base = item
    cache = os.path.join(CACHE, base + ".bin")
    if not os.path.exists(cache):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        open(cache, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    im = Image.open(cache).convert("RGB")
    for w in (1024, 560):
        k = im.copy()
        if k.width > w:
            k = k.resize((w, round(k.height * w / k.width)), Image.LANCZOS)
        k.save(os.path.join(OUT_P, f"{base}-{w}.webp"), "WEBP", quality=82, method=6)
    return base, im.size

with ThreadPoolExecutor(8) as ex:
    for base, size in ex.map(fetch, dl):
        pass
print("photos done")
