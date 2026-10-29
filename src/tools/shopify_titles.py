"""Bring the wig titles in Shopify in step with the catalogue (title, search title and search description).
Only these three fields change; web addresses, photos, prices and descriptions stay as they are. Safe to run again.

    SHOPIFY_STORE=gvit1g-jv.myshopify.com python src/tools/shopify_titles.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D
from shopify_api import gql

Q = "query($q: String) { products(first: 1, query: $q) { nodes { id handle title seo { title } } } }"
UPD = "mutation($p: ProductUpdateInput!) { productUpdate(product: $p) { userErrors { field message } } }"
for p in D.build_products():
    c = p["color"]
    seo = {"title": f"{p['title']} | Chesed",
           "description": f"{p['title']} in 100% unprocessed virgin Remy human hair. {c['blurb']} 18 to 36 inches."[:320]}
    n = gql(Q, {"q": f"handle:{p['handle']}"})["products"]["nodes"]
    if not n or n[0]["handle"] != p["handle"]:
        print(f"missing  {p['handle']}"); continue
    if n[0]["title"] == p["title"] and n[0]["seo"]["title"] == seo["title"]:
        print(f"same     {p['title']}"); continue
    e = gql(UPD, {"p": {"id": n[0]["id"], "title": p["title"], "seo": seo}}, mutation=True)["productUpdate"]["userErrors"]
    print(f"{'ERROR ' + str(e) if e else 'renamed'}  {n[0]['title']} -> {p['title']}")
