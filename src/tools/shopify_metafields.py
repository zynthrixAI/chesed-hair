"""Store the shade and texture details in Shopify, so the theme can show them and Chesed can edit them in the admin.

    python src/tools/shopify_metafields.py

Each shade and texture lives once, on its collection (namespace "chesed"):
  texture collections: short (one line), curly, length_photo (straight / wavy / curly), faq
  shade collections:   shade_key (e.g. 1B), shade_name (e.g. Natural Black), hex, blurb, faq
  all wigs, crochet:   faq
Each wig points at its texture and shade collections (product metafields chesed.texture and chesed.shade).
Safe to run again: definitions that exist are kept and values are overwritten.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
from shopify_api import gql, ids

DEFS = [("COLLECTION", "short", "Texture: one-line description", "single_line_text_field"),
        ("COLLECTION", "curly", "Texture: curly (waves and curls sit higher)", "boolean"),
        ("COLLECTION", "length_photo", "Texture: length photo (straight, wavy or curly)", "single_line_text_field"),
        ("COLLECTION", "shade_key", "Shade: code, e.g. 1B", "single_line_text_field"),
        ("COLLECTION", "shade_name", "Shade: name in words, e.g. Natural Black", "single_line_text_field"),
        ("COLLECTION", "shade_label", "Shade: what shoppers read, e.g. Natural Black (1B)", "single_line_text_field"),
        ("COLLECTION", "hex", "Shade: swatch color", "color"),
        ("COLLECTION", "blurb", "Shade: description", "multi_line_text_field"),
        ("COLLECTION", "faq", "Questions and answers", "json"),
        ("PRODUCT", "texture", "Wig texture (collection)", "collection_reference"),
        ("PRODUCT", "shade", "Wig shade (collection)", "collection_reference")]

CREATE_DEF = """mutation($d: MetafieldDefinitionInput!) { metafieldDefinitionCreate(definition: $d) { createdDefinition { id } userErrors { code message } } }"""
for owner, key, name, typ in DEFS:
    r = gql(CREATE_DEF, {"d": {"ownerType": owner, "namespace": "chesed", "key": key, "name": name, "type": typ,
                               "access": {"storefront": "PUBLIC_READ"}}}, mutation=True)["metafieldDefinitionCreate"]
    errs = [e for e in r["userErrors"] if e["code"] != "TAKEN"]
    print(f"definition {owner.lower()}.{key}: {'error ' + str(errs) if errs else 'ok'}")

def faq(items):
    return json.dumps([{"q": q, "a": a} for q, a in items])

col_ids, prod_ids = ids("collections"), ids("products")
values = []   # (owner handle kind, handle, key, type, value)
def put(owner_id, key, typ, value):
    values.append({"ownerId": owner_id, "namespace": "chesed", "key": key, "type": typ, "value": value})

for t in D.TEXTURES:
    cid = col_ids[f"{t['slug']}-wigs"]
    put(cid, "short", "single_line_text_field", t["short"])
    put(cid, "curly", "boolean", "true" if t["curly"] else "false")
    put(cid, "length_photo", "single_line_text_field", D.length_photo_key(t))
    put(cid, "faq", "json", faq(t["faq"]))
products = D.build_products()
for cc in D.make_color_collections(products):
    c = D.COL[cc["colors"][0]]
    cid = col_ids[f"{cc['slug']}-wigs"]
    put(cid, "shade_key", "single_line_text_field", c["key"])
    put(cid, "shade_name", "single_line_text_field", c["name"])
    put(cid, "shade_label", "single_line_text_field", c["label"])
    put(cid, "hex", "color", c["hex"])
    put(cid, "blurb", "multi_line_text_field", c["blurb"])
    put(cid, "faq", "json", faq(cc["faq"]))
put(col_ids["wigs"], "faq", "json", faq(D.WIG_FAQ))
crochet_ec = next(ec for ec in D.EXTRA_COLLECTIONS if ec["kind"] == "crochet")
put(col_ids[crochet_ec["slug"]], "faq", "json", faq(crochet_ec["faq"]))
for p in products:
    put(prod_ids[p["handle"]], "texture", "collection_reference", col_ids[f"{p['texture']['slug']}-wigs"])
    put(prod_ids[p["handle"]], "shade", "collection_reference", col_ids[f"{p['color']['slug']}-wigs"])

SET = """mutation($m: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $m) { metafields { id } userErrors { field message } } }"""
for i in range(0, len(values), 25):
    r = gql(SET, {"m": values[i:i + 25]}, mutation=True)["metafieldsSet"]
    if r["userErrors"]:
        sys.exit(f"metafieldsSet failed: {r['userErrors']}")
print(f"set {len(values)} values")
