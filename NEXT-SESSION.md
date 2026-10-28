# Chesed Hair: pick up here

Updated 29 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Preview site:** https://lime-deer-681625.hostingersite.com. Everything up to pull request 27 (crochet on the homepage, general FAQs, Hair Bundles hidden) is merged and live.
- **Shopify store, in progress:** the real store is being built in the user's Partners development store `chesed-hair-umskgt0n.myshopify.com` as our workshop. **Plan changed on 28 October:** no transfer; we'll update Chesed's own store, "Chesed Hair Collection", once they give us access (see "Plan change" in PROJECT.md). Products, collections, shade and texture details, info pages and the theme "Chesed" are in. **Since 28 October the Chesed theme is the live theme on the dev store** (Horizon is unpublished), so the client sees our design with just the store address and password. See "Shopify store" in PROJECT.md and the theme's own [CLAUDE.md](../chesed-theme/CLAUDE.md).
- **Theme folder** `D:\Work\Chesed Hair\Website\chesed-theme` is on GitHub as the private repo `zynthrixAI/chesed-theme` (branch `main`).
- **GitHub tool:** signed in as zynthrixAI. **Shopify CLI:** signed in to the user's Partners account, with store access for the tools.

## Start next time with
1. **Chesed's own store (`gvit1g-jv.myshopify.com`) is ready to launch.** Products, collections, details, pages, spin-wheel codes, redirects, real reviews and the theme "Chesed" (id 158858969142, **unpublished**) are in; see "Chesed's own store" in PROJECT.md. **Launch only when the user says "publish it"**: then follow "Launch day" in PROJECT.md (publish the theme, unpublish and redirect their 8 old collections, delete test1, check the live site).
2. **Nothing from 28 to 29 October is on GitHub yet:** both repos have local commits. Ask before `git push`.
3. **The user does in the admin:** paste the policies (`D:\Work\Chesed Hair\Shopify\policies-to-paste.html`), the free shipping over $100 rate, payments and Apple/Google Pay, two-step sign-in. Georgia sales tax waits on the client.
4. **Waiting on the client:** `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md` (star ratings, tax, business details, shipping times, photos, prices).
5. The dev store's live theme doesn't have the 28 to 29 October theme changes (pushing to it was blocked); push only with the user's go-ahead.
6. Later: menus as Shopify navigation, a reviews app (Judge.me), an email platform for the wheel, a backup app (Rewind).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Shopify:** on the dev store the Chesed theme is live, so `shopify theme push` changes what the client sees straight away (behind the store password); show the user before pushing. The `?preview_theme_id=` link only works for someone signed in to the admin; everyone else gets the live theme (that is why the client saw Shopify's default Horizon theme on 28 October). On Chesed's own store the theme stays unpublished until the user says to publish. Store data changes (products, collections, pages) go straight to the dev store, which isn't public. **Never change Chesed's own store without the user's say-so**, and back it up first.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, the strand length charts (replaced by the length photos), and boxed category cards on the homepage. **Never crop the crochet photos.**
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first. When there are two reasonable designs, show both as screenshots and recommend one.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The homepage banner is full screen height, so a tall window shows only the banner: use a page that loads the site in an iframe and scrolls it to a section (one is kept at `.claude/shot.html`, not committed: `?u=<path>&w=<width>&h=<height>&s=<css selector>`). The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
