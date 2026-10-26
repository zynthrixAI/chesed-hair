"""Create the shopping pages (automatic collections) in the Shopify store and show them in the online store.

    python src/tools/shopify_collections.py [store.myshopify.com]

Uses the Shopify command-line tool (`shopify store auth` must have been run once for the store).
Each collection fills itself from the product tags written by export_shopify.py. Collections that already
exist (same handle) are left alone, so the script is safe to run again.
"""
import json, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D

STORE = sys.argv[1] if len(sys.argv) > 1 else "chesed-hair-umskgt0n.myshopify.com"
CLI = shutil.which("shopify")

def gql(query, variables=None, mutation=False):
    """Query and variables go through files: the Windows wrapper of the CLI mangles quotes and < > on the command line."""
    with tempfile.TemporaryDirectory() as tmp:
        qf, vf = os.path.join(tmp, "q.graphql"), os.path.join(tmp, "v.json")
        open(qf, "w", encoding="utf-8").write(query)
        cmd = [CLI, "store", "execute", "-s", STORE, "--query-file", qf, "-j"]
        if variables:
            json.dump(variables, open(vf, "w", encoding="utf-8"))
            cmd += ["--variable-file", vf]
        if mutation:
            cmd.append("--allow-mutations")
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    out = r.stdout[r.stdout.find("\n{") + 1:] if "\n{" in r.stdout else r.stdout
    if not out.lstrip().startswith("{"):
        sys.exit(f"Shopify CLI failed:\n{r.stdout}\n{r.stderr}")
    return json.loads(out)

def tag_rule(tag):
    return {"column": "TAG", "relation": "EQUALS", "condition": tag}

products = D.build_products()
cols = [dict(handle="wigs", title="Lace Front Wigs", rules=[tag_rule("wig")],
             body=f"Every Chesed wig in one place: {len(D.TEXTURES)} textures and 10 shades of lace front wigs in 100% unprocessed virgin Remy human hair, each available from 18 to 36 inches.",
             seo=f"Lace Front Wigs in {len(D.TEXTURES)} Textures & 10 Colors | Chesed")]
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
    if c["handle"] in have:
        print(f"exists   {c['handle']}")
        continue
    r = gql(CREATE, {"input": {"title": c["title"], "handle": c["handle"], "descriptionHtml": f"<p>{c['body']}</p>",
                               "ruleSet": {"appliedDisjunctively": True, "rules": c["rules"]},
                               "seo": {"title": c["seo"], "description": c["body"][:155].rsplit(" ", 1)[0] + "…"}}}, mutation=True)["collectionCreate"]
    if r["userErrors"]:
        print(f"ERROR    {c['handle']}: {r['userErrors']}")
        continue
    gql(PUBLISH, {"id": r["collection"]["id"], "pub": pub}, mutation=True)
    print(f"created  {c['handle']}")
