# Chesed Hair: pick up here

Updated 26 November 2026. These notes are on `main` (brought over from `black-friday` on 23 November); the Black Friday mock-up code stays on the `black-friday` branch only. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Black Friday sale: LIVE (20 November 2026)
- **Live design: Idea 5** (v26, chosen by the client on 20 November): Option 07's giant photo-filled "30%" on the left, three fanned wig cards with sale prices on the right. It replaced Option 07 (v9) on the evening of 20 November.
- **What switches by itself** (New York time):
  - **Until Mon 11/23:** a teaser top bar, and the sale banner with "Sale starts in" (banner live from 20 November, user).
  - **11/23 to 11/30:** the sale top bar, the banner with "Sale ends in", and the pink scrolling band.
  - **From 12/1:** back to normal.
- **How it works in the theme:** see `../chesed-theme/CLAUDE.md`. To preview a state, add `?bf=sale` (or `teaser`, `off`) to any address.
- **Discount:** the automatic discount "Black Friday: 30% off everything" was created 20 November. It's scheduled for 23 Nov 00:00 to 30 Nov 23:59 New York time and applies to all products.
  - It doesn't combine with codes (the spin-wheel codes, CHESED20, and friends50, which someone else scheduled from 20 November): the shopper gets the bigger discount.
  - It combines with shipping discounts.
- **Screenshots:** `D:\Work\Chesed Hair\Shopify\black-friday-2026\Idea 5 on the store\` (Option 07's are in `Option 07 on the store\`).
- **To do:**
  - **Checked 23 November:** the sale switched on by itself (banner "Sale ends in", sale top bar, discount active). A test cart took 30% off a 24" 1B Body Wave ($229.95 to $160.97).
  - **Card prices were 1 cent low:** Shopify rounds the 30% discount down. Fixed and live on 23 November (the banner now takes off 30% rounded down, like the cart).
  - After 30 November, check that it all switched back and the discount ended.
- **Design history** (branch `black-friday`, on GitHub since 20 November; not for `main`):
  - The v7 to v21 options are in `src/templates/partials/bf_more.html`; Option 07 is v9.
  - That branch's mock-up code shouldn't be merged into `main`.
  - **Option 07 with wigs, 5 ideas (v22 to v26, 20 November, the client chose Idea 5, now live):** same build (`BF=sale BFV=more`, `/?bfv=22`...`26`). Screenshots in `Shopify\black-friday-2026\Desktop\Wig banner ideas\`.

## Product page round (26 November 2026, live)
- **Asked by the user:** a Buy it now button, the countdown everywhere, a visible 30% off on product pages, and a fix for a white gap above the details column.
- **Buy it now:** solid black, above Add to bag (now a see-through button with a pink outline). It adds the item and goes straight to checkout, with a won spin code if the shopper has one.
- **Countdown:** in the sale top bar ("Ends in 4d 16h 24m 39s") and on product pages, ticking every second.
- **Product pages during the sale:** the sale price (rounded like the cart), the old price crossed out, a pink "30% off" tag and "Black Friday price, taken off automatically at checkout". Add to bag, Shop Pay and the sticky bar show the sale price. The won-code note is hidden.
- **Product cards** (shop pages, homepage, search) show "From $97.97 ~~$139.95~~ 30% off" during the sale.
- **Spin to win** (the pop-up and the tab) is hidden during the sale; it comes back by itself.
- **Buy it now on phones:** the bar that slides up at the bottom of the screen once the main buttons scroll away now has Buy it now (black) beside Add to bag (pink outline), half and half on phones (the price is left off there to fit). Coming back from checkout with the back button, the buttons work again (phones keep the page in memory with the button switched off).
- **White gap fixed:** the details column stuck 150px down although the header doesn't stick.
- **Scrolling on laptops (user's design, 26 November):** both columns stay on screen. Scrolling down moves the details (right) to their end first, then the photos (left), then the rest of the page; scrolling up moves the details back first, then the photos. It works from the page's normal scroll (mouse wheel, trackpad, keys). Replaces two earlier tries that day (columns scrolling separately under the mouse, then a normal page).
- **All of it switches off after 30 November** (`html[data-bf]`). Screenshots: `D:\Work\Chesed Hair\Shopify\product-page-2026-11-26\`.

## Length photos with coloured dresses (23 November 2026, live)
- **Client asked** for the black dress on the length photos to change, so the hair ends show.
- **Colours (user):** a different one per photo. Straight is soft ivory cream, Wavy soft sage green, Curly soft powder blue. Each crochet photo matches its wig photo.
- **Made by the user in the Gemini app.** The Ace Data account (Nano Banana, Midjourney) was out of credit, and Claude can't make images itself.
- **Lined up by script:** Gemini widened the frame, so each photo was scaled and cropped back onto the original so the length lines hit the same body points. Script and files: `D:\Work\Chesed Hair\Images\Dress colour\` (`finish.py`, the originals in `1 Give these to Gemini`, before and after images). Crochet Wavy is about 1% smaller, with a 12px bottom strip padded. Gemini made the Wavy hair slightly longer.
- **Code:** same file names (`length-*`, `length-crochet-*` in `assets/p/`). Branch `dress-colour`, merged into `main` on 23 November (user: "merge it"). Theme pushed live with the user's go-ahead.

## Earlier: Black Friday design rounds
- **Ask** (Eunji, 19 November 2026): **30% off the entire site, Monday 11/23 to Monday 11/30.** The user chose:
  - a top bar on every page plus a homepage banner
  - an automatic discount (no code)
  - a teaser top bar from now until 11/23, then the sale switching on and off by itself
- **Status:** the user likes design v5 ("looks good", 19 November) and is waiting for the client's feedback.
  - **Nothing is live.**
  - **The Shopify discount is not created.**
  - Screenshots: `D:\Work\Chesed Hair\Shopify\black-friday-2026\` (`banner-laptop.png`, `banner-phone.png`).
- **Mock-up:** branch `black-friday` in this repo (on GitHub since 20 November; not for merging into `main`).
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
- **Desktop first (user, 19 November):** settle the laptop design before phones.
  - The user kept v3, v4A, v5 and v6 to show the client.
  - **15 more options made, v7 to v21:** `src/templates/partials/bf_more.html`, CSS under `/* Black Friday v7 to v21 */`.
  - Build with `BF=sale BFV=more python src/build.py`, then open `/?bfv=<n>` (or `.claude/home.html?v=<n>`).
  - Screenshots at 1440×900 are in `Shopify\black-friday-2026\Desktop\`. Phone layouts aren't made for these yet.
  - **The screenshots are named "Option 01" to "Option 19" for the client.**
    - Options 01 to 04 are v3, v4A, v5 and v6.
    - Options 05 to 19 are v7 to v21, so the version is the option number plus 2.
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
1. **Every change to chesedhair.com is public.** **How the user wants changes done (26 November 2026):** when they ask for a site change, do it end to end without stopping to ask: make it, check it on a hidden preview (`shopify theme dev`), push it live, check the live page, commit, push to GitHub, update the notes and merge, then report with a screenshot. Ask first only when the request is unclear, or for prices, products, deleting things or anything that costs money.
2. **Read the final handover first:** `D:\Work\Chesed Hair\Documents\Chesed Hair - Final Handover.md` (the whole project, images included, and what the proposal still owes). The client work log is the Claude Doc "Chesed Hair: Work Delivered" (https://claude.ai/artifact/WwPXxErn3hqasxgDgazZxu). Both repos are up to date on GitHub (26 November): the theme on `main`; this repo on `main`. The `black-friday` branch only holds the banner mock-ups now; its copy of the notes is older than `main`'s.
3. **Still owed from the proposal:** up to 5 minutes of AI video. Basic SEO is set up; further SEO work only if the client takes it up as a separate service. The project is now on monthly store management.
4. **Done by the user (29 October):** free shipping over $100, the policies (all 5 live, linked in the footer) and payments. **Georgia sales tax is the client's job**; no tax is charged until they set it up.
5. **Waiting on the client:** `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md` (tax, business details, shipping times, photos, prices). Reviews and star ratings came from the client, confirmed in writing to the user.
6. Textures: 10 in the catalogue, 7 on sale (Permed Straight, Wet & Wavy and Deep Wave are drafts waiting for photos, and hidden on Shopify).
7. Later: menus as Shopify navigation, a reviews app (Judge.me), an email platform for the wheel, a backup app (Rewind).

## Things to know
- **GitHub and merging:** part of the end-to-end routine above (user, 26 November: "streamline this process"). Commit, push and merge without asking each time.
- **Importing a product CSV into Shopify:** Shopify copies each photo from a public web address, and the preview site that used to serve them is gone. Put new photos somewhere public first (for example a temporary folder on webwroughts.com) or upload them in the Shopify admin.
- **Shopify:** Chesed's store is the public site: theme pushes, products, collections and pages there show to shoppers straight away. Change it only for something the user asked for (see the routine above). The `?preview_theme_id=` link only works for someone signed in to the admin.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, the strand length charts (replaced by the length photos), and boxed category cards on the homepage. **Never crop the crochet photos.**
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user wants results shown as screenshots, but **doesn't want to be asked at every step** (26 November). They get frustrated by long experiments that don't land: show a small test first. When there are two reasonable designs, show both as screenshots and recommend one.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The homepage banner is full screen height, so a tall window shows only the banner: use a page that loads the site in an iframe and scrolls it to a section (one is kept at `.claude/shot.html`, not committed: `?u=<path>&w=<width>&h=<height>&s=<css selector>`). The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
