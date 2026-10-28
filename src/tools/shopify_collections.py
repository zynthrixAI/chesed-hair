"""Create the shopping pages (automatic collections) in the Shopify store and show them in the online store.

    python src/tools/shopify_collections.py

Uses the Shopify command-line tool (`shopify store auth` must have been run once for the store).
Each collection fills itself from the product tags written by export_shopify.py. Collections that already
exist (same handle) are left alone, so the script is safe to run again.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

from shopify_api import gql

def tag_rule(tag):
    return {"column": "TAG", "relation": "EQUALS", "condition": tag}

products = D.build_products()
n_tex = sum(1 for t in D.TEXTURES if any(p["texture"]["key"] == t["key"] and not p["placeholder"] for p in products))   # textures on sale (wigs with photos)
cols = [dict(handle="wigs", title="Lace Front Wigs", rules=[tag_rule("wig")],
             body=f"Every Chesed wig in one place: {n_tex} textures and 10 shades of lace front wigs in 100% unprocessed virgin Remy human hair, each available from 18 to 36 inches. All of them are shown on the same model, so you can compare textures and shades fairly. Filter by texture and shade below to narrow it down.",
             seo=f"Lace Front Wigs in {n_tex} Textures & 10 Colors | Chesed")]
for t in D.TEXTURES:
    cols.append(dict(handle=f"{t['slug']}-wigs", title=f"{t['name']} Wigs", rules=[tag_rule(f"texture-{t['slug']}")], body=t["intro"],
                     seo=f"{t['name']} Lace Front Wigs | Chesed"))
for cc in D.make_color_collections(products):
    cols.append(dict(handle=f"{cc['slug']}-wigs", title=cc["h1"], rules=[tag_rule(f"shade-{D.COL[k]['slug']}") for k in cc["colors"]],
                     body=cc["intro"], seo=cc["title"]))
for ec in D.EXTRA_COLLECTIONS:
    if ec["kind"] == "crochet":
        cols.append(dict(handle=ec["slug"], title=ec["h1"], rules=[tag_rule("crochet")], body=ec["intro"], seo=ec["title"]))

pub = next(p["id"] for p in gql("{ publications(first: 20) { nodes { id name } } }")["publications"]["nodes"] if p["name"] == "Online Store")
have = {c["handle"] for c in gql("{ collections(first: 100) { nodes { handle } } }")["collections"]["nodes"]}

CREATE = """mutation($input: CollectionInput!) { collectionCreate(input: $input) { collection { id handle productsCount { count } } userErrors { field message } } }"""
PUBLISH = """mutation($id: ID!, $pub: ID!) { publishablePublish(id: $id, input: [{publicationId: $pub}]) { userErrors { message } } }"""
for c in cols:
    if c["handle"] in have:   # keep the intro in step with the catalogue
        cid = next(n["id"] for n in gql("query($q: String) { collections(first: 1, query: $q) { nodes { id } } }", {"q": f"handle:{c['handle']}"})["collections"]["nodes"])
        gql("mutation($c: CollectionInput!) { collectionUpdate(input: $c) { userErrors { message } } }",
            {"c": {"id": cid, "descriptionHtml": f"<p>{c['body']}</p>"}}, mutation=True)
        print(f"exists   {c['handle']} (intro updated)")
        continue
    r = gql(CREATE, {"input": {"title": c["title"], "handle": c["handle"], "descriptionHtml": f"<p>{c['body']}</p>",
                               "ruleSet": {"appliedDisjunctively": True, "rules": c["rules"]},
                               "seo": {"title": c["seo"], "description": c["body"][:155].rsplit(" ", 1)[0] + "…"}}}, mutation=True)["collectionCreate"]
    if r["userErrors"]:
        print(f"ERROR    {c['handle']}: {r['userErrors']}")
        continue
    gql(PUBLISH, {"id": r["collection"]["id"], "pub": pub}, mutation=True)
    print(f"created  {c['handle']}")

# Order: the preview's order (texture, then shade), so menus and pages list shades and textures the same way
from shopify_api import ids, store_handle
prod_ids = ids("products")
col_nodes = {c["handle"]: c["id"] for c in gql("{ collections(first: 100) { nodes { id handle } } }")["collections"]["nodes"]}
SORT = "mutation($c: CollectionInput!) { collectionUpdate(input: $c) { userErrors { message } } }"
REORDER = "mutation($id: ID!, $moves: [MoveInput!]!) { collectionReorderProducts(id: $id, moves: $moves) { userErrors { message } } }"
for c in cols:
    members = [p["handle"] for p in products if any(r["condition"] in (["wig", f"texture-{p['texture']['slug']}", f"shade-{p['color']['slug']}"]) for r in c["rules"])]
    if c["rules"][0]["condition"] == "crochet":
        members = [x["handle"] for x in D.build_extras() if x["kind"] == "crochet"]
    if not members or c["handle"] not in col_nodes:
        continue
    cid = col_nodes[c["handle"]]
    gql(SORT, {"c": {"id": cid, "sortOrder": "MANUAL"}}, mutation=True)
    moves = [{"id": prod_ids[store_handle(h)], "newPosition": str(i)} for i, h in enumerate(members)]
    for i in range(0, len(moves), 250):
        r = gql(REORDER, {"id": cid, "moves": moves[i:i + 250]}, mutation=True)["collectionReorderProducts"]
        if r["userErrors"]:
            print(f"ERROR order {c['handle']}: {r['userErrors']}")
    print(f"ordered  {c['handle']} ({len(members)})")
