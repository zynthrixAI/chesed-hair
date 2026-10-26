# Chesed Hair: pick up here

Updated 27 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Preview site:** https://lime-deer-681625.hostingersite.com. Everything up to pull request 27 (crochet on the homepage, general FAQs, Hair Bundles hidden) is merged and live.
- **Shopify store, in progress:** the real store is being built in the user's Partners development store `chesed-hair-umskgt0n.myshopify.com` and will be transferred to Chesed when finished. Products, collections, shade and texture details, info pages and the theme "Chesed" (unpublished) are in. See "Shopify store" in PROJECT.md and the theme's own [CLAUDE.md](../chesed-theme/CLAUDE.md).
- **Branch `claude/shopify-tools`** (this repo, on this PC, not pushed): the Shopify tools in `src/tools/` and the move of FAQs, page text, the wheel drawing and length lines into `src/data.py`. The preview builds exactly as before. Ask before pushing.
- **Theme folder** `D:\Work\Chesed Hair\Website\chesed-theme` has its own Git history, not on GitHub yet.
- **GitHub tool:** signed in as zynthrixAI. **Shopify CLI:** signed in to the user's Partners account, with store access for the tools.

## Start next time with
1. Get the store password from the user (Online Store → Preferences → Password protection), run `shopify theme dev` (see the theme's CLAUDE.md) and check every page at 1440px and phone width. Nothing in the theme has been seen in a browser yet.
2. Fix what's off, push the theme, and show the user screenshots plus the preview link.
3. Then: menus as Shopify navigation, payments and shipping settings, Judge.me reviews, spin-wheel discount codes.

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Shopify:** the theme stays unpublished until the user says to publish. Store data changes (products, collections, pages) go straight to the dev store, which isn't public.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, the strand length charts (replaced by the length photos), and boxed category cards on the homepage. **Never crop the crochet photos.**
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first. When there are two reasonable designs, show both as screenshots and recommend one.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The homepage banner is full screen height, so a tall window shows only the banner: use a page that loads the site in an iframe and scrolls it to a section (one is kept at `.claude/shot.html`, not committed: `?u=<path>&w=<width>&h=<height>&s=<css selector>`). The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
