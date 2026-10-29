# Chesed Hair: pick up here

Updated 29 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live store:** www.chesedhair.com (Chesed's store `gvit1g-jv.myshopify.com`) runs the Chesed theme (id 158858969142) since 29 October 2026: 50 active wigs (Curly back since 29 October) and 6 crochet. See "Chesed's own store" and "Curly wigs back" in PROJECT.md. Their old theme "Re-degine Be Yours" is kept unpublished as a fallback.
- **Preview site:** https://lime-deer-681625.hostingersite.com. Everything up to pull request 33 (Curly wigs back, real reviews, spin wheel) is merged and live.
- **Workshop store:** the user's Partners development store `chesed-hair-umskgt0n.myshopify.com` (Chesed theme live there behind the password, but behind the real store since 28 October).
- **Theme folder** `D:\Work\Chesed Hair\Website\chesed-theme` is on GitHub as the private repo `zynthrixAI/chesed-theme` (branch `main`).
- **GitHub tool:** signed in as zynthrixAI. **Shopify CLI:** signed in to the user's Partners account; store tools reach Chesed's store with `SHOPIFY_STORE=gvit1g-jv.myshopify.com`.

## Start next time with
1. **Every change to chesedhair.com is public:** theme pushes need `--allow-live` and the user's go-ahead; show them first.
2. **Both repos are up to date on GitHub** (preview up to pull request 36, 30 October 2026).
3. **Done by the user (29 October):** free shipping over $100, the policies (all 5 live, linked in the footer) and payments. **Georgia sales tax is the client's job**; no tax is charged until they set it up.
4. **Waiting on the client:** `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md` (tax, business details, shipping times, photos, prices). Reviews and star ratings came from the client, confirmed in writing to the user.
5. Textures: 10 in the catalogue, 7 on sale (Permed Straight, Wet & Wavy and Deep Wave are drafts waiting for photos, and hidden on Shopify).
6. Later: menus as Shopify navigation, a reviews app (Judge.me), an email platform for the wheel, a backup app (Rewind).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Importing a product CSV into Shopify:** merge the preview first and check its photos load, because Shopify copies the photos from the preview site.
- **Shopify:** Chesed's store is the public site: theme pushes, products, collections and pages there show to shoppers straight away. **Never change it without the user's say-so.** The `?preview_theme_id=` link only works for someone signed in to the admin.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, the strand length charts (replaced by the length photos), and boxed category cards on the homepage. **Never crop the crochet photos.**
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first. When there are two reasonable designs, show both as screenshots and recommend one.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The homepage banner is full screen height, so a tall window shows only the banner: use a page that loads the site in an iframe and scrolls it to a section (one is kept at `.claude/shot.html`, not committed: `?u=<path>&w=<width>&h=<height>&s=<css selector>`). The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
