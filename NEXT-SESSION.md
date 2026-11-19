# Chesed Hair: pick up here

Updated 19 November 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Open job: Black Friday sale (waiting on the client)
- **Ask** (Eunji, 19 November 2026): **30% off the entire site, Monday 11/23 to Monday 11/30.** The user chose:
  - a top bar on every page plus a homepage banner
  - an automatic discount (no code)
  - a teaser top bar from now until 11/23, then the sale switching on and off by itself
- **Status:** the user likes design v5 ("looks good", 19 November) and is waiting for the client's feedback.
  - **Nothing is live.**
  - **The Shopify discount is not created.**
  - Screenshots: `D:\Work\Chesed Hair\Shopify\black-friday-2026\` (`banner-laptop.png`, `banner-phone.png`).
- **Mock-up:** branch `black-friday` in this repo (local only, not pushed).
  - `BF=sale python src/build.py` shows the sale; `BF=teaser` shows the teaser top bar only.
  - **Rebuild with plain `python src/build.py` before committing**, so the built pages stay the normal site.
  - Code: `bf`, `bf_img`, `bf_side`, `bf_deal` in `src/build.py`; the `bfx` hero, the pink `bf-band` marquee and the countdown in `src/templates/index.html`; the teaser and sale top bar in `partials/announcement.html`; CSS under `/* Black Friday (mock-up) */` at the end of `assets/css/style.css`.
- **Design v5, as approved:**
  - Black banner with a huge pink outlined "BLACK FRIDAY" across the back.
  - Three photos layered like a magazine spread: 1B Loose Deep in the middle, Honey Blonde Body Wave and 530 Curly behind (phones show only the middle one).
  - A giant "**30%** off" over the main photo, and a turning pink "7 days" seal.
  - A live countdown to 30 November 23:59 New York time on the left.
  - An example price on the right, 24" Natural Black Loose Deep ~~$236.95~~ $165.86, plus the shop buttons.
  - A pink top bar on every page, and the scrolling band under the banner turned pink.
  - The site's own fonts only.
- **Client feedback on v5 (19 November):** too busy because of the layout. **v6 made** (`BF=sale BFV=6 python src/build.py`; CSS under `/* Black Friday v6 */`):
  - the same black and pink, but only one photo (1B Loose Deep), centred
  - "Black" to its left and "Friday" to its right
  - "30% off" across the photo
  - the dates on the bottom left; the countdown and buttons on the bottom right
  - no seal, no side photos, no outlined word, no example price
  - waiting on the user and client. Screenshots of v1 to v6 are in `Shopify\black-friday-2026\`.
- **Rejected by the user, do not redo:**
  - v1, just text on the normal banner ("too simple, can't tell it's a banner").
  - v2, a copy of the client's reference image with glitter corners, tilted black ribbons, a script "Sale" and heavy fonts ("keep it in our theme and style").
  - v3, the normal banner plus a seal and a pink band ("no visible difference from the live one").
  - v4, one photo beside a black or pink panel with a huge 30% ("too basic").
- **To do once the client approves** (show the user first; push live only on their go-ahead):
  1. Port v5 to the theme:
     - a new homepage section, or a sale mode for `sections/home-hero.liquid`
     - the top bar in `sections/header.liquid`
     - the pink marquee
     - the countdown script
     - `theme_snippets.py` for the CSS
  2. **Date switching:** teaser until 23 November 00:00, sale until 30 November 23:59, then back to normal, all in New York time (the store's time zone). Shopify caches pages, so a Liquid date check alone can lag. Also switch it in the browser with JavaScript.
  3. **Discount:** create the automatic 30% discount on all products for the same dates (`discountAutomaticBasicCreate`; needs the `write_discounts` scope).
     - Decide with the user whether the spin-wheel codes and CHESED20 can be used on top of it. CHESED20 is active and was made by someone else.
     - Check the example price matches Shopify's rounding.
  4. After 30 November: check the banner has gone and the discount has ended.

## Where things stand
- **Live store:** www.chesedhair.com (Chesed's store `gvit1g-jv.myshopify.com`) runs the Chesed theme (id 158858969142) since 29 October 2026: 50 active wigs (Curly back since 29 October) and 6 crochet. See "Chesed's own store" and "Curly wigs back" in PROJECT.md. Their old theme "Re-degine Be Yours" is kept unpublished as a fallback.
- **Preview site** (lime-deer-681625.hostingersite.com): **deleted 17 November 2026** (it was only a design demo). Changes now go straight to the live store, www.chesedhair.com. This repo stays the source of the catalogue, the shared theme pieces and the Shopify tools; build locally (`python src/build.py`, `python -m http.server`) to try a change before pushing the theme.
- **Workshop store:** the user's Partners development store `chesed-hair-umskgt0n.myshopify.com` (Chesed theme live there behind the password, but behind the real store since 28 October).
- **Theme folder** `D:\Work\Chesed Hair\Website\chesed-theme` is on GitHub as the private repo `zynthrixAI/chesed-theme` (branch `main`).
- **GitHub tool:** signed in as zynthrixAI. **Shopify CLI:** signed in to the user's Partners account; store tools reach Chesed's store with `SHOPIFY_STORE=gvit1g-jv.myshopify.com`.

## Start next time with
1. **Every change to chesedhair.com is public:** theme pushes need `--allow-live` and the user's go-ahead; show them first.
2. **Read the final handover first:** `D:\Work\Chesed Hair\Documents\Chesed Hair - Final Handover.md` (the whole project, images included, and what the proposal still owes). The client work log is the Claude Doc "Chesed Hair: Work Delivered" (https://claude.ai/artifact/WwPXxErn3hqasxgDgazZxu). Both repos are up to date on GitHub apart from the notes commits.
3. **Still owed from the proposal:** up to 5 minutes of AI video. Basic SEO is set up; further SEO work only if the client takes it up as a separate service. The project is now on monthly store management.
4. **Done by the user (29 October):** free shipping over $100, the policies (all 5 live, linked in the footer) and payments. **Georgia sales tax is the client's job**; no tax is charged until they set it up.
5. **Waiting on the client:** `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md` (tax, business details, shipping times, photos, prices). Reviews and star ratings came from the client, confirmed in writing to the user.
6. Textures: 10 in the catalogue, 7 on sale (Permed Straight, Wet & Wavy and Deep Wave are drafts waiting for photos, and hidden on Shopify).
7. Later: menus as Shopify navigation, a reviews app (Judge.me), an email platform for the wheel, a backup app (Rewind).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Importing a product CSV into Shopify:** Shopify copies each photo from a public web address, and the preview site that used to serve them is gone. Put new photos somewhere public first (for example a temporary folder on webwroughts.com) or upload them in the Shopify admin.
- **Shopify:** Chesed's store is the public site: theme pushes, products, collections and pages there show to shoppers straight away. **Never change it without the user's say-so.** The `?preview_theme_id=` link only works for someone signed in to the admin.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, the strand length charts (replaced by the length photos), and boxed category cards on the homepage. **Never crop the crochet photos.**
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first. When there are two reasonable designs, show both as screenshots and recommend one.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The homepage banner is full screen height, so a tall window shows only the banner: use a page that loads the site in an iframe and scrolls it to a section (one is kept at `.claude/shot.html`, not committed: `?u=<path>&w=<width>&h=<height>&s=<css selector>`). The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
