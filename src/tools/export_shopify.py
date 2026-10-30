"""Write a Shopify product import file (Products > Import in the Shopify admin) from the catalogue.

    python src/tools/export_shopify.py [out.csv]

Wigs: one product per shade and texture, option "Length" (18" to 32") with Chesed's prices.
Crochet: options as on the preview (Color, Length). Hair bundles are left out while they are hidden.
Photos are fetched by Shopify from the preview site, so it must be live with the same photos.
Wigs with placeholder photos are imported as drafts with no photos.
Tags drive the automatic collections: wig / crochet, texture-<slug>, shade-<slug>, crochet-texture-<slug>, crochet-color-<slug>.
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D

PREVIEW = "https://lime-deer-681625.hostingersite.com"
OUT = sys.argv[1] if len(sys.argv) > 1 else r"D:\Work\Chesed Hair\Shopify\chesed-products.csv"
COLS = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
        "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
        "Variant SKU", "Variant Inventory Tracker", "Variant Inventory Policy", "Variant Fulfillment Service",
        "Variant Price", "Variant Requires Shipping", "Variant Taxable",
        "Image Src", "Image Position", "Image Alt Text", "SEO Title", "SEO Description", "Variant Image", "Status"]

def photo(file):
    return f"{PREVIEW}/assets/p/{file}-1024.webp"

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def product_rows(head, variants, images):
    """Shopify's layout: the first row carries the product, then one row per variant; photos fill the image columns row by row."""
    rows = []
    for i in range(max(len(variants), len(images))):
        r = dict(head) if i == 0 else {"Handle": head["Handle"]}
        if i < len(variants):
            r.update(variants[i])
        if i < len(images):
            r.update({"Image Src": photo(images[i]["file"]), "Image Position": i + 1, "Image Alt Text": images[i].get("alt", "")})
        rows.append(r)
    return rows

def variant(sku, price, *opts):
    v = {"Variant SKU": sku, "Variant Inventory Tracker": "", "Variant Inventory Policy": "continue",
         "Variant Fulfillment Service": "manual", "Variant Price": f"{price:.2f}", "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE"}
    for n, (name, value) in enumerate(opts, 1):
        v[f"Option{n} Name"], v[f"Option{n} Value"] = name, value
    return v

rows = []
for p in D.build_products():
    t, c = p["texture"], p["color"]
    body = (f"<p>{esc(c['blurb'])}</p><p>{esc(t['intro'])}</p>"
            f"<ul><li>Texture: {esc(t['name'])}</li><li>Hair: 100% unprocessed virgin Remy human hair</li>"
            f"<li>Lace: 13x5 lace front</li><li>Cap: one size fits all</li><li>Lengths: 18 to 32 inches</li></ul>")
    head = {"Handle": p["handle"], "Title": p["title"], "Body (HTML)": body, "Vendor": "Chesed Hair", "Type": "Lace Front Wig",
            "Tags": ", ".join(["wig", f"texture-{t['slug']}", f"shade-{c['slug']}", f"family-{c['family']}"]),
            "Published": "FALSE" if p["placeholder"] else "TRUE", "Status": "draft" if p["placeholder"] else "active",
            "SEO Title": f"{p['title']} | Chesed",
            "SEO Description": f"{p['title']} in 100% unprocessed virgin Remy human hair. {c['blurb']} 18 to 32 inches."[:320]}
    variants = [variant(f"{p['handle']}-{v['length']}", v["price"], ("Length", v["title"])) for v in p["variants"]]
    images = [] if p["placeholder"] else p["images"]
    rows += product_rows(head, variants, images)

for x in D.build_extras():
    if x["kind"] != "crochet":
        continue
    names = [o["name"] for o in x["options"]]
    body = f"<p>{esc(x['desc'][0])}</p>" if x["desc"] else ""
    if len(x["desc"]) > 1:
        body += "<ul>" + "".join(f"<li>{esc(line)}</li>" for line in x["desc"][1:]) + "</ul>"
    head = {"Handle": x["handle"], "Title": x["title"], "Body (HTML)": body, "Vendor": "Chesed Hair", "Type": "Crochet Extensions",
            "Tags": ", ".join(["crochet"] + [f"crochet-texture-{s}" for s in x["textures"]] + [f"crochet-color-{s}" for s in x["colors"]]),
            "Published": "TRUE", "Status": "active", "SEO Title": f"{x['title']} | Chesed",
            "SEO Description": f"{x['title']}. Choose your color and length. Crochet & Feather Extensions from Chesed Hair."[:320]}
    color_img = {im["color"]: photo(im["file"]) for im in x["images"] if im.get("color")}
    variants = []
    for v in x["variants"]:
        vals = [v["o"][n] for n in names]
        sku = x["handle"] + "-" + "-".join(s.lower().replace(" ", "-").replace('"', "in") for s in vals)
        r = variant(sku, v["price"], *zip(names, vals))
        if v["o"].get("Color") in color_img:
            r["Variant Image"] = color_img[v["o"]["Color"]]
        variants.append(r)
    rows += product_rows(head, variants, x["images"])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
handles = {r["Handle"] for r in rows}
print(f"Wrote {len(rows)} rows, {len(handles)} products, to {OUT}")
