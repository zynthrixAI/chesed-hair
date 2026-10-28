"""Run Admin API GraphQL against the Shopify store through the Shopify command-line tool.

Needs `shopify store auth --store=<store> --scopes=...` once (it opens a browser). Set SHOPIFY_STORE to use another store.
"""
import json, os, shutil, subprocess, sys, tempfile

STORE = os.environ.get("SHOPIFY_STORE", "chesed-hair-umskgt0n.myshopify.com")
CLI = shutil.which("shopify")

# Chesed's own store kept its old web addresses for the 5 crochet products that were on sale (updated in place, 28 Oct 2026)
STORE_HANDLES = {"gvit1g-jv.myshopify.com": {
    f"seamless-{k}-feather-crochet-braid-hair-extensions": f"chesed-hair-seamless-{v}-handmade-feather-crochet-braid-natural-black-human-hair-extensions"
    for k, v in {"wet-and-wavy": "wet-wavy", "kinky-straight": "kinky-straight", "burmese-curly": "burmese-curly",
                 "body-wave": "body-wave", "deep-wave": "deep-wave"}.items()}}
STORE_HANDLES["gvit1g-jv.myshopify.com"]["seamless-deep-wave-feather-crochet-braid-hair-extensions"] += "-copy"

def store_handle(handle):
    """Our catalogue handle -> the handle the product has in this store."""
    return STORE_HANDLES.get(STORE, {}).get(handle, handle)

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
    if not out.lstrip().startswith("{") or '"error"' in out[:20]:
        sys.exit(f"Shopify CLI failed:\n{r.stdout[-3000:]}\n{r.stderr[-1500:]}")
    return json.loads(out)

def ids(kind):
    """handle -> id for every product or collection (kind "products" or "collections")."""
    out, after = {}, None
    while True:
        page = gql("query($a: String) { %s(first: 250, after: $a) { nodes { id handle } pageInfo { hasNextPage endCursor } } }" % kind, {"a": after})[kind]
        out.update({n["handle"]: n["id"] for n in page["nodes"]})
        if not page["pageInfo"]["hasNextPage"]:
            return out
        after = page["pageInfo"]["endCursor"]
