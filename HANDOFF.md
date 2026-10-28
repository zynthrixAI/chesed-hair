# Chesed Hair: handoff for VS Code

Read this first when continuing the project. For where we paused and what to do next, see [NEXT-SESSION.md](NEXT-SESSION.md). For the full history and the to-do list, see [PROJECT.md](PROJECT.md).

**About the user:** they are not a programmer. Explain things in plain language, without jargon, and show results (screenshots or the live link) rather than code.

## Where things are
- **Project folder:** `D:\Work\Chesed Hair\Website\chesed-hair` (open this folder in VS Code)
- **GitHub:** `github.com/zynthrixAI/chesed-hair`. `main` is what the live site shows.
- **Live preview:** https://lime-deer-681625.hostingersite.com. Hostinger deploys `main` automatically, usually within about 20 seconds of a merge. If it doesn't update, redeploy from the Git section in Hostinger's hPanel.
- **Open work:** see [NEXT-SESSION.md](NEXT-SESSION.md) for branches that are committed but not yet pushed.
- **Shopify theme:** `D:\Work\Chesed Hair\Website\chesed-theme` (separate folder with its own Git history; see its `CLAUDE.md`).
- **Shopify store:** the user's Partners development store `chesed-hair-umskgt0n.myshopify.com` (our workshop; the Chesed theme is its live theme since 28 October, behind the store password). The finished work goes into Chesed's own store, "Chesed Hair Collection", once they give access; no transfer (see PROJECT.md, "Plan change").

## Tools on this PC (Windows 11)
- **Python 3.14** with Jinja2 installed. Use `python`, not `python3`.
- **Git**, with name `Claude <noreply@anthropic.com>` set for this repo only (matches every earlier commit).
- **GitHub CLI**, at `"C:\Program Files\GitHub CLI\gh.exe"` (may not be on the PATH). Signed in as zynthrixAI again on 16 October 2026. If it signs out, run `gh auth login` in a normal PowerShell window (it can't be run inside Claude Code).
- **Shopify CLI 4.9** (`npm install -g @shopify/cli`). Two sign-ins, both run by the user in a normal PowerShell window because they open a browser: `shopify auth login` (themes) and `shopify store auth --store=chesed-hair-umskgt0n.myshopify.com --scopes=read_products,write_products,write_publications,read_content,write_content,write_online_store_navigation,read_themes,write_themes,read_files,write_files,write_discounts` (store data for the tools below).
- **Not installed:** Playwright. Check pages in a browser instead.

## Commands
Build every page (writes 102 pages into the repo root, plus `assets/search.json`):
```bash
python src/build.py
```

Preview locally, then open http://127.0.0.1:8000:
```bash
python -m http.server 8000 --bind 127.0.0.1
```

## How the code is laid out
| Path | What it is |
|---|---|
| `src/data.py` | The catalog and settings: `TEXTURES` (9 wig styles), `COLORS` (the 10 shades, with `name` in words), `LENGTHS` and `LANDMARKS`, wig prices (`WIG_LENGTH_PRICE`, `COLOR_EXTRA`, `TEXTURE_EXTRA`, `PRICE_MULTIPLIER`), `LENGTH_PHOTOS`, `FREE_SHIP`, `CAP_IMAGES`, `REVIEWS` (samples), `SPIN_PRIZES`, the FAQs (`GENERAL_FAQ`, `WIG_FAQ`, `SHIP_FAQ`, `HOME_FAQ`, `FAQ_PAGE`), the info page text (`PAGES`, `PAGE_STEPS`), and `wheel_svg()` / `length_photo()`. The preview and the Shopify tools both read it |
| `src/tools/export_shopify.py` | Shopify product import file (CSV) from the catalogue. Photos are fetched from the preview site, so it must be live |
| `src/tools/shopify_api.py` | Runs Admin API queries through the Shopify CLI (`shopify store execute`). Query and variables go through files: the CLI's Windows wrapper mangles quotes and `< >` on the command line |
| `src/tools/shopify_collections.py` | Creates the automatic collections and sets their product order. Safe to run again |
| `src/tools/shopify_metafields.py` | Writes the shade and texture details onto their collections and links each wig to them. Safe to run again |
| `src/tools/shopify_pages.py` | Creates or updates the info pages and guides, and writes their templates into the theme folder |
| `src/tools/theme_snippets.py` | Copies the stylesheet, fonts, non-product photos, spin wheel, length photos and sample reviews into the theme. Run it after changing `assets/css/style.css` or those partials |
| `src/extras.json` | The crochet and feather extensions and hair bundles. Made by `src/tools/import_extras.py` (client's CSV and item list; drafts skipped), then `src/tools/import_amazon_crochet.py` (crochet photos from the Amazon folder, adds Burmese Magic) |
| `src/build.py` | Renders every page. Also sets the homepage picks (`best`, `look_keys`, hero) and `HEADER` (`"simple"` or `"visual"` menu) |
| `src/templates/` | Jinja templates: `index`, `collection`, `product`, `page`, guides, `sitemap` |
| `src/templates/partials/` | Header, footer, search, spin wheel, cart, and `macros.html` (the product card) |
| `assets/css/style.css` | The only stylesheet |
| `assets/js/main.js` | The only script |
| `src/templates/partials/length_photos.html` | The length photos (straight, wavy, curly with pink length tags) and the size table, used on the homepage, length guide and wig pages |
| `assets/p/` | Product photos as WebP, 1024px and 560px. Wigs: `<handle>-1-front`, `-2-three-quarter`, `-3-back`, `-4-side`, `-5-fingers`, `-6-lifestyle` (6 per wig, read straight from this folder). `-7-mannequin-front` and `-8-mannequin-back` on the 49 wigs that have them (they take the last two slots and replace `-5-fingers`), then the two cap pictures `wig-cap-one-size` and `wig-cap-secure-fit`. Extras: `<handle>-<n>` (crochet: 6 colour photos, then info slides). `placeholder` is the pink stand-in photo |
| Everything else in the root | **Built output.** Never edit it by hand: change `src/`, rebuild, and commit both |

### Useful details
- **Handles** are `<shade slug>-<texture slug>-lace-front-wig`, e.g. `350-loose-deep-wave-lace-front-wig`. Renaming a shade means renaming its photos in `assets/p/` and deleting the old built folders under `products/` and `collections/`, because the build doesn't remove pages it no longer makes.
- **Collection URLs** are `/collections/<slug>-wigs/`. Color slugs are the shade slugs: `1`, `1b`, `virgin`, `530`, `99j`, `350`, `honey-auburn`, `natural-auburn`, `honey-blonde`, `red`.
- **Product card** (`macros.product_card`) takes `lead="color"` (default) or `lead="texture"`. Color collections pass `card_lead="texture"` from `build.py`.
- **Stylesheet and script links** get a `?v=` number from the file's modified time. After a fresh clone, a rebuild changes that number on every page. That change is harmless.
- **Photo links** are written with `img(file, width)` (in `build.py`), which adds `?v=` plus a fingerprint of the photo. Use it for every photo.
- **Prices:** each wig variant's price comes from `wig_price(length, texture, shade)` in `src/data.py`: Chesed's sheet price times 2 (`PRICE_MULTIPLIER`), rounded up to the next .95. Wig pages read the per-length prices from `data-prices` so the price follows the chosen length.
- **Hair Bundles** are switched off with `coming_soon=True` in `EXTRA_COLLECTIONS`; remove it to bring the bundle pages back.

### Photo folders on this PC
- **Chesed's studio photos:** `D:\Work\Chesed Hair\Images\Final Images\<Style>\<shade folder>\`, six per shade (`<Style> - <Shade> - <n> <Shot>`; shade folders use HA, HB, NA for Honey Auburn, Honey Blonde, Natural Auburn).
- **Lace-free versions:** 17 photos were replaced with lace-free versions on 24 October 2026 (from `Images\Lace Review\No lace`). The old photos are in `Final Images\_with lace (old)\`.
- **Branch `add-ai-gallery-images`:** 300 AI model photos for 7 styles in `assets/gallery/<handle>/` (WebP, 1024 and 560), including the 17 lace-free versions. The site's code doesn't use this folder yet, and the branch is older than `main` (it still has Curly photos). Don't merge it into `main` without the user's say-so.

## Workflow
1. Start each change on a **new branch from the latest `main`** (`git fetch` first).
2. Edit `src/` or `assets/`, then run `python src/build.py`.
3. Check the pages in a browser at about 1440px wide and at phone width (about 390px).
4. Commit the source **and** the built pages, push, and open a PR into `main` with `gh pr create`.
5. Ask before `git push`: Claude Code's safety check blocks pushes until the user gives a clear go-ahead.
6. Explain the change to the user in plain words. Merge only when they say **"merge it"**: `gh pr merge <n> --rebase`.
7. After merging, check the live site picked it up. Tell the user to press Ctrl + Shift + R if they still see the old version.

## Rules
- **Every page stays `noindex`.** Keep `robots.txt` and the noindex tags until this becomes the real store.
- **Don't commit** `src/__pycache__/` or `.claude/`. Both are in `.gitignore`.
- **Hostinger serves the whole repo root,** so anything committed is publicly reachable on the preview site.
- **CLAUDE.md, HANDOFF.md, NEXT-SESSION.md and PROJECT.md are committed in the repo** (they were meant to be local only, but are tracked). Keep them updated as the project moves on, and keep them free of anything private.
- **Placeholders** that Chesed must confirm are marked in pink on the pages (now mainly the "Sample" reviews and the spin wheel). See PROJECT.md for the list.

## Gotchas
- **Shopify CLI on Windows:** run the tools with `PYTHONIOENCODING=utf-8` (the console can't print some characters). `shopify store execute` needs `--allow-mutations` for changes; the tools add it.
- **Product counts in Shopify** include drafts in the admin, but shoppers only see active products.
- **Wig photos are 2:3.** Frame them 2:3 (or `object-fit:contain`); 4:5 or square frames cut the bottom of the hair off.
- **Class-name collisions broke things twice:** `.sm` vs `.link.sm` (now `.smenu`), and `.trust` vs the homepage strip (now `.pdp-trust`). Search the CSS for a class name before adding a new one.
- **Hidden dropdowns:** never set `visibility:visible` inside a hidden panel. Use `inherit`, or the hidden panel catches mouse hovers and opens the menu.
- **The sticky filter bar** has a `backdrop-filter`, which traps `position:fixed` children. It's turned off on phones for that reason.
- **Windows build:** files must be written with `encoding="utf-8"` (the ✦ symbol and the Hebrew חֶסֶד crash cp1252). Already fixed in `build.py`; keep it that way for any new file writes.
- **Line-ending warnings** ("LF will be replaced by CRLF") come from the PC's Git settings and are harmless.
- **GitHub's merge sometimes returns error 500.** Wait a moment and retry.
- **Browsers keep photos for 7 days** (Hostinger sends `max-age=604800`). Every photo address is written with `img(file, width)` in `src/build.py`, which adds `?v=` plus a fingerprint of the file, so a replaced photo shows straight away. Never write `/assets/p/...webp` by hand in a template.
