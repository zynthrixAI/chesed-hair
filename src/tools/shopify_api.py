"""Run Admin API GraphQL against the Shopify store through the Shopify command-line tool.

Needs `shopify store auth --store=<store> --scopes=...` once (it opens a browser). Set SHOPIFY_STORE to use another store.
"""
import json, os, shutil, subprocess, sys, tempfile

STORE = os.environ.get("SHOPIFY_STORE", "chesed-hair-umskgt0n.myshopify.com")
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
