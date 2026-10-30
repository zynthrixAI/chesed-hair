"""Create or update the info pages and guides in the Shopify store, and write their theme templates.

    python src/tools/shopify_pages.py [theme folder]

Pages: About, FAQ, Shipping, Returns, Contact (text from PAGES in src/data.py), the length guide and the color guide
(text from the preview's guide templates). Each page uses its own template (templates/page.<handle>.json in the theme),
which holds the line under the heading and, for Shipping and Returns, the how-it-works steps.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
from shopify_api import gql

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(SRC)), "chesed-theme")

def guide_text(name):
    """The guide's own words: the toc-body of the preview template, without the shop button."""
    t = open(os.path.join(SRC, "templates", name), encoding="utf-8").read()
    body = t.split('<div class="toc-body">', 1)[1]
    return re.sub(r"\s*<p><a class=\"btn rose\".*", "", body, flags=re.S).strip()

pages = []   # (handle, title, seo title, body, template json)
for handle, seo, h1, lede, body in D.PAGES:
    main = {"type": "main-page", "settings": {"lede": lede or "", "toc": handle == "faq"}}
    if handle in D.PAGE_STEPS:
        main["blocks"] = {f"s{i}": {"type": "step", "settings": {"icon": ic, "heading": h, "text": tx.replace(f"${int(D.FREE_SHIP)}", "$[free_ship]")}}
                          for i, (ic, h, tx) in enumerate(D.PAGE_STEPS[handle])}
        main["block_order"] = list(main["blocks"])
    pages.append((handle, h1, seo, body, {"sections": {"main": main}, "order": ["main"]}))
pages.append(("wig-length-guide", "Wig Length Chart: 18 to 32 Inches", "Wig Length Chart, 18-32 Inch on a Model | Chesed",
              guide_text("length_guide.html"), {"sections": {"main": {"type": "main-length-guide", "settings": {}}}, "order": ["main"]}))
pages.append(("wig-color-guide", "Wig Colors on Deep Skin", "Wig Color Chart: 10 Shades on Deep Skin | Chesed",
              guide_text("color_guide.html"), {"sections": {"main": {"type": "main-color-guide", "settings": {"texture": "body-wave-wigs"}}}, "order": ["main"]}))

have = {p["handle"]: p["id"] for p in gql("{ pages(first: 100) { nodes { id handle } } }")["pages"]["nodes"]}
CREATE = "mutation($p: PageCreateInput!) { pageCreate(page: $p) { page { id } userErrors { message } } }"
UPDATE = "mutation($id: ID!, $p: PageUpdateInput!) { pageUpdate(id: $id, page: $p) { page { id } userErrors { message } } }"
for handle, title, seo, body, tpl in pages:
    json.dump(tpl, open(os.path.join(THEME, "templates", f"page.{handle}.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    fields = {"title": title, "body": body, "templateSuffix": handle, "isPublished": True,
              "metafields": [{"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": seo}]}
    if handle in have:
        r = gql(UPDATE, {"id": have[handle], "p": fields}, mutation=True)["pageUpdate"]
    else:
        r = gql(CREATE, {"p": {**fields, "handle": handle}}, mutation=True)["pageCreate"]
    print(f"{'updated' if handle in have else 'created'}  {handle}" + (f"  ERROR {r['userErrors']}" if r["userErrors"] else ""))
