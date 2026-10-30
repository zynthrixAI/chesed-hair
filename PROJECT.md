# Chesed Hair website: project log

A preview of the Chesed Hair online store (lace front wigs and crochet), built by Web Wroughts so Chesed could approve the design. The real store is now being built in Shopify from the same catalogue (see "Shopify store" below).

- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Code:** https://github.com/zynthrixAI/chesed-hair
- **On this PC:** `D:\Work\Chesed Hair\Website\chesed-hair`
- **Shopify theme on this PC:** `D:\Work\Chesed Hair\Website\chesed-theme` (private repo `zynthrixAI/chesed-theme`)
- **Last updated:** 29 October 2026 (see [NEXT-SESSION.md](NEXT-SESSION.md))

---

## What the site has

- **111 pages:** the homepage, 22 shopping pages ("collections"), 74 wig pages, 6 extension pages and 8 info pages (About, FAQ, Shipping, Returns, Contact, Color guide, Length guide, All pages).
- **10 wig textures:** Body Wave, Curly, Kinky Curly, Kinky Straight, Loose Deep Wave, Straight, Virgin Curl, plus **Permed Straight**, **Wet & Wavy** and **Deep Wave** (placeholder photos for now). Water Wave wigs were removed because they are not on Chesed's price sheet; Curly was removed for the same reason and came back on 29 October at the Kinky Curly prices.
- **Two extra categories:** Crochet & Feather Extensions (6 products) and Hair Bundles (coming soon).
- **10 shades:** 1, 1B, 99J, 350, 530, Honey Auburn, Honey Blonde, Natural Auburn, Red, Virgin.
- **10 lengths:** 18" to 36", priced by length from Chesed's price sheet times 2 ($139.95 to $479.95, plus extras for coloured shades and some textures).
- **Web addresses work like Shopify's**, e.g. `/collections/body-wave-wigs/` or `/products/1b-body-wave-lace-front-wig/`, so the move to Shopify is simpler later.
- **Hidden from Google** on purpose, so the preview never competes with the real store.

---

## Everything done so far

All of this is live on the preview unless marked otherwise.

### Building the store (first sessions)
1. **Homepage approved,** then the full store built: homepage, collections, 50 wig pages and guides, all from one catalog file.
2. **Luxury redesign:** black, porcelain and blush colors around Chesed pink; large photo banners; elegant fonts; smooth scrolling.
3. **Motion and effects:** the shade showcase plays through all ten shades as you scroll, the lookbook slides sideways, headings reveal word by word, and photos wipe in.
4. **Round 3 layouts:** full-width two-column sections, an interactive hair length chart, and a reviews carousel.

### Pull request 1: simpler menu
- Menu is now **Shop / Guides / Help / About.** Hovering a texture in Shop shows every wig in it.
- On phones, the menu opens in expandable sections.
- New **All pages** page (`/pages/sitemap/`).
- The old picture menu is saved and can be switched back on.

### Pull request 2: features that help people buy
- **Spin-to-win welcome wheel:** every spin wins a discount, the real odds are shown, and the won code follows the shopper to the bag.
- **Working search** with instant results.
- **Product cards:** "or 4 × $72.25" and a **Quick add** button with a length picker.
- **Wig pages:** a trust row (free shipping, returns, pay in 4, secure checkout) plus spaces for reviews and try-on videos.
- **Homepage:** best sellers moved near the top.

### Pull request 3: polish
- The Shop menu stays one size; collection banners are shorter.
- Smooth opening and closing everywhere, and carousels you can drag with the mouse.
- Shade swatches on wig pages.
- Texture spotlight with a shade switcher, and a story section with חֶסֶד (Chesed).
- **WhatsApp chat button.**
- **New filter on shopping pages:** pick textures and shades, remove them as pills, live count. Opens as a sheet on phones.
- Quick-facts box on collections, a pull quote on wig pages, how-it-works steps on Shipping and Returns, and "On this page" contents on the FAQ and guides.

### Pull request 4: fixes and homepage sections
- Fixed the menu opening by accident when the mouse was near the top of the screen.
- Removed the scrolling row of texture names; the promise ticker stays.
- New expanding shade panels on the homepage.
- The textures section now holds in place and slides sideways as you scroll.
- Newsletter sign-up in the footer sits on one line.

### Pull request 5: works on this Windows PC
- The build tool crashed on Windows because of the ✦ symbol and the Hebrew word. Fixed.
- Tidied up a leftover file that shouldn't have been saved.
- The GitHub tool was installed and signed in, so Claude can open and merge changes from this PC.

### Pull request 6: real shade names and spacing
- **Every shade now uses Chesed's real name:** 1, 1B, 99J, 350, 530, Honey Auburn, Honey Blonde, Natural Auburn, Red, Virgin. Before this they had made-up names like "Ginger 350" and "Jet Black 1".
- Wig names, web addresses and all 238 photo file names were updated.
- Color pages renamed: **1, 1B & Virgin Wigs**, **530 & 99J Wigs** and **350 Wigs** (Auburn, Honey Blonde and Red stayed the same).
- Fixed an FAQ that said 1, 1B and Virgin come in seven textures; they come in six.
- **Smaller gap** between Best sellers and "The wig you'll actually receive."

### Pull request 7: product names on color pages
- On color pages (e.g. 350 Wigs) the big name on each wig is now the **style**: **Body Wave**, with "350 Lace Front Wig" under it.
- On style pages (e.g. Body Wave Wigs) the big name stays the **shade**: **1B**, with "Body Wave Lace Front Wig" under it.
- Merged on 15 October 2026.

### Homepage best sellers lead with the style
- On the homepage, the big name on each best seller is now the **style** (e.g. **Body Wave**, with "1B Lace Front Wig" under it).
- The **All wigs** page still leads with the shade.
- Merged on 15 October 2026 (branch `claude/home-style-names`; no pull request page because the GitHub tool was signed out).

### New photos, crops and the image morph (16 October 2026)
- All 50 wigs now use the new AI gallery: 6 photos per wig (front, three-quarter, back, side, fingers, lifestyle). Old photos deleted.
- Every product photo crops from the top centre.
- Clicking a wig from anywhere morphs the photo into the wig page, and back again (Chrome and Edge).
- All wigs page leads with the style (pull request 8).

### Best photos and a tidier footer (16 October 2026)
- Homepage hero, banners, shade showcase, spotlight, story ("Our name") and collection banners now use the most striking three-quarter and lifestyle shots. Picks are set in `src/build.py` with `shot(texture, color, n)` (0 front, 1 three-quarter, 5 lifestyle). Banners skip placeholder photos.
- Every wig's first photo (cards, wig page, search, bag) is now the bright smiling lifestyle shot; the three-quarter shot is second (the card hover image). Body Wave 1 uses the three-quarter shot because its lifestyle shot has closed eyes. Set in `COVER_POSE` / `COVER_OVERRIDES` in `src/data.py`. In `build.py` use `pose_img(p, n)`, never a list position, to pick a specific pose.
- Footer regrouped: brand and email, wigs by texture and by color (two columns each), more to shop and guides, help.

### One page per shade (16 October 2026)
- The grouped color pages (1, 1B & Virgin; 530 & 99J; Auburn) are gone. Every shade has its own page, e.g. `/collections/1b-wigs/`, `/collections/99j-wigs/`, and the menu, footer and links list the 10 shades separately. 350, Honey Blonde and Red keep their old addresses.
- Shade page copy is generated in `make_color_collections()` in `src/data.py`.
- The Shop menu was redesigned: two-column shades, cards for the extra categories, one footer strip.

### Products from the client's files (16 October 2026)
- **Permed Straight** and **Wet & Wavy** wig styles, 8 shades each (1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde, Red), with pink placeholder photos.
- **Crochet & Feather Extensions:** 21 listings from the Shopify export plus Burmese Magic from the item list. Client photos and real prices. Skipped as duplicates: the second "Water Wave Soft Feather" listing (same title, its color is already in the first) and the repeated "Deep Wave / Small Kinky Curly" listing. The CROCHET tab of the item list matched the export, so only Burmese Magic was new.
- **Hair Bundles:** Body Wave, Straight, Deep Wave, Water Wave from the Bundle tab (shades and lengths from the sheet). Placeholder photos and a placeholder $99 price.
- Wigs with no other shades hide the "Same texture" rail.

### Homepage feedback, round 1 (19 to 20 October 2026; pull requests 10 to 15)
- **Navigation:** the top menu is now **Wigs / Crochet & Feather / Hair Bundles / Guides / Help / About**, so crochet and bundles sit beside wigs instead of hiding under "Shop". Wigs keeps its texture tabs and shade lists. Crochet has its own **by texture** and **by color** lists plus popular products; its links open the crochet page already filtered (`?texture=water-wave`, `?color=blonde`). Bundles lists its four products. Phones get the same three groups. Texture and color families for the extras are worked out in `classify_extra()` in `src/data.py` from each listing's title, options and details, so a few may need correcting.
- **Crochet page filters:** Texture and Shade filters, like wigs. Cards carry `data-texture` and `data-color` (space separated, a product can have several).
- **Homepage banner:** photo 1 is the client's favourite (1B Straight). Photos 2 and 3 are two curly photos the client supplied (burgundy in the middle, black on the right): `banner-curly-burgundy` and `banner-curly-black` in `assets/p/`, set in `hero_imgs` in `src/build.py`.
- **Banner heading:** "100% Virgin Remy Human Hair" is a bold rose label (`.hero-badge`) above the headline.
- **Shade theater:** the scroll-driven behaviour was removed; you click a swatch to change shade.
- **Textures section ("Seven textures. One standard."):** now a plain 4-column grid of cards (2 columns on phones) instead of a pinned sideways scroll with a fade. Section is `.texg` in `index.html`.
- **Photos no longer cropped:** the wig photos are 2:3 and are now shown in full in the product gallery, shop cards, lookbook, spotlight, "on deep skin" and description photos (`.card-wig`, `.g-wig` and friends in `style.css`).
- **Product page photos:** the original layout (first photo large, the rest in pairs). Clicking any photo opens a popup gallery with arrows, thumbnails, swipe and keyboard support (the lightbox in `main.js`, works on wigs and extras). Two redesigns (a thumbnail rail, then a full-width frame with a blurred backdrop) were tried and **rejected by the client**; do not bring them back.
- **Mannequin photos:** the automatic crops and cut-outs of the client's studio shots were **rejected**; the user then edited them by hand (see pull request 19).

### Pull requests 16 and 17: client feedback, round 2 (22 October 2026)
Feedback came in a Google Doc ("Website Updates").
- **Generated mannequin photos removed** (pull request 16).
- **Wig lengths are 18" to 36"** (was 10" to 32"). Lengths and where they end on the body are set once in `LENGTHS`, `LANDMARKS` and `CURLY_LANDMARKS` in `src/data.py` and passed to the script through `window.CHESED`. Wig pages open on 24" (`DEFAULT_LENGTH`).
- **Wig details:** 13x5 lace front, one size fits all cap, density removed.
- **Shades in words:** each shade has a `name` in `COLORS` (1B Natural Black, 1 Jet Black, Virgin Natural Dark Brown, 530 Rich Wine Red, 99J Deep Plum, 350 Copper Ginger, Red Cherry Red; the auburns and Honey Blonde keep their names). The wig page "Shade" label, the swatch pop-ups and the homepage shade sections show the name. Product titles and web addresses still use the number.
- **"Worn by you"** (try-on videos and review placeholder) removed from wig and extension pages, with the star-rating placeholder.
- **Crochet & Feather:** Kinky Curly and Loose Wave taken out of the menu and filters (`CROCHET_TEXTURES`). The "extensions / lengths" count boxes replaced with "Human hair, handmade" and the lowest price.
- **Hair Bundles: coming soon.** `coming_soon=True` on the bundle collection in `src/data.py`: the bundle page shows a coming-soon note, the menu says "Coming soon", and the bundle product pages are not built.
- **Free shipping over $100** (`FREE_SHIP`), used everywhere including the bag's progress bar.
- **About page:** the story from chesedhair.com (meaning of Chesed, why you'll love it, care and versatility, ethical commitment).
- **Deep Wave and Water Wave wigs** added (8 shades each, same as Permed Straight, with "Photo coming soon" pictures and copy we wrote).

### Pull request 18: cap pictures and live crochet only (22 October 2026)
- **Cap pictures on every wig:** the client's "One size fits all" and "6X secure fit guard" pictures (`wig-cap-one-size`, `wig-cap-secure-fit` in `assets/p/`) are the last two photos in every wig's gallery, full width so they aren't cropped. Set in `CAP_IMAGES` in `src/data.py`; kept out of shop cards and the "on deep skin" photos.
- **Crochet & Feather: only the listings that were live in Shopify.** The client said the drafts were tests. `src/tools/import_extras.py` skips drafts.

### Pull request 19: wig prices and mannequin photos (23 October 2026)
- **Wig prices** from Chesed's price sheet ("CHESED WIG Selling Price", JK Trading, 1 September 2026), in `WIG_LENGTH_PRICE`, `COLOR_EXTRA` and `TEXTURE_EXTRA` in `src/data.py`:
  - Per length: 18" $69.95, 20" $79.95, 22" and 24" $99.95, 26" $129.95, 28" $139.95, 30" $149.95, 32" $189.95, 34" $219.95, 36" $249.95. The sheet's bands overlap ("18-20", "20-22", "22-24"); the user chose the lower band, so 20" = $79.95 and 22" = $99.95.
  - Plus $5 for every shade except 1, 1B and Virgin. Plus $3.50 for Loose Deep; $4.50 for Kinky Curly, Virgin Curl, Kinky Straight and Wet & Wavy.
  - **Our estimates** (not on the sheet): 28", 34" and 36", and the extras for Curly (+$4.50), Water Wave (+$4.50), Deep Wave (+$3.50) and Permed Straight (+$0).
  - The wig page price, "or 4 payments", Add to bag and the sticky bar follow the chosen length; quick add uses each length's price; cards show "From" the 18" price.
- **Mannequin photos:** the user's hand-edited photos (`D:\Work\Chesed Hair\Images\Mannequin Image Edit Preview`, named `<Texture> - <Shade> - Front/Back.png`, transparent, 1000x1000) are on all 49 wigs that have studio shots. Saved on the pearl background as `<handle>-7-mannequin-front` and `-8-mannequin-back` in `assets/p/`; they replace the "fingers" photo and sit side by side, square and uncropped (`.g-mq`). Three Body Wave files had the wrong shade name (530, 99J and 350 were rotated); they were placed on the right wigs and the files renamed. Wigs without mannequin photos: Kinky Curly, Permed Straight, Wet & Wavy, Deep Wave, Water Wave.

### Pull request 20: Chesed's answers (23 October 2026)
- **Photos refresh straight away:** every photo address carries a fingerprint of the file (`img()` in `src/build.py`), because Hostinger tells browsers to keep photos for 7 days.
- **Crochet photos from Amazon:** `src/tools/import_amazon_crochet.py` reads `D:\Work\Chesed Hair\Images\Assets - Chesed Hair\Amazon-...\Amazon` and gives each crochet product its six colour photos (square model-plus-product shots) and the info slides (size chart, knotless loop, human hair, feather crochet, packs, crochet vs bulk). Choosing a colour puts that colour's photo first (`showColor` in `main.js`). Crochet galleries show square photos whole on white (`.g-x`).
- **6 crochet products:** Wet & Wavy, Kinky Straight, Burmese Curly, Body Wave, Deep Wave and **Burmese Magic** (back, with the same lengths, colours and prices as Burmese Curly).
- **Sample reviews:** the user asked for demo reviews. Six sample reviews in `REVIEWS` (`src/data.py`), each tagged "Sample" in pink, with a note that they are replaced by real reviews before launch.
- **WhatsApp button removed** (not needed). **About page:** no founder story or photos (not needed).
- **Shipping and returns follow LUVME's terms** (client's choice): ships within 1 business day, express delivery in 2 to 6 business days, cancel within 1 hour; 30-day returns and exchanges for unused hair with the lace uncut, approval by email with photos, one free US return label per order, refunds within 2 business days of checking the return, exchanges ship within 3 business days. On the Shipping and Returns pages, wig and crochet pages, and the FAQ.

### Pull request 22: length photos and doubled prices (24 October 2026)
- **Length photos (layout C, chosen by Chesed):** three photos of a 5'5" model from behind (straight, wavy, curly) with a pink line and tag for each length, then a size table (length, centimeters, where straight and wavy/curly hair ends). On the length guide and the homepage; on phones, Straight / Wavy / Curly buttons show one photo at a time and the table scrolls sideways. Photos: `length-straight`, `length-wavy`, `length-curly` in `assets/p/`. Code: `partials/length_photos.html`, `LENGTH_PHOTOS` in `src/data.py`, `length_photo()` in `src/build.py`.
- **Wig pages:** the "Every length, side by side" section shows the photo for that wig's texture (wavy: Body Wave, Loose Deep, Wet & Wavy, Water Wave; curly: the other curly textures). Tapping a length on the photo picks it, like the length buttons. The old strand charts are gone.
- **Prices:** Chesed's corrected sheet ("CHESED WIG List", 24 October 2026) times 2, rounded up to the next .95 (`PRICE_MULTIPLIER`, `up_to_95()` in `src/data.py`). E.g. 18" Straight in 1B $139.95, 24" Body Wave in 530 $209.95, 32" Kinky Curly in Red $378.95. The sheet's 32" price is now $179.95 (was $189.95), and 28" is now on the sheet. 632 of the sheet's 633 rows for our shades and textures match the site; the odd one out is Deep Wave 20" in Red, which the sheet prices like a natural shade ($83.45).
- **Burmese Magic** feather crochet renamed **Burmese Magic Curl** (Chesed). Web address unchanged.
- **New on Chesed's sheet, not on the site yet** (no photos): shades #2, #27, #4/30 and Virgin Color (Light), and a **Loose Wave** texture. Chesed also says more wig types are coming.

### Pull request 24: only the wigs on Chesed's sheet (24 October 2026)
- **Curly and Water Wave wigs removed** (17 wigs, their 2 shopping pages and their photos), because they are not on Chesed's price sheet (user, 24 October 2026). The homepage best sellers and lookbook now use Straight Honey Blonde and Virgin Curl 1B instead. Water Wave crochet and bundles are separate products and stay.
- **34" and 36" estimates updated** to $30 a step above the new 32" price: $209.95 and $239.95 before doubling, so 1B Straight is $419.95 and $479.95.
- **Lengths kept as they are:** the sheet leaves out some lengths (28" for Kinky Straight and Permed Straight; most lengths for coloured Deep Wave), which look like gaps in the sheet. Every wig still offers 18" to 36"; asked Chesed to confirm.

### Lace-free photos (24 to 26 October 2026)
- **Chesed's photo folders:** 17 photos replaced with versions where the wig lace was removed (`Images\Lace Review\No lace`). The old ones were moved to `Final Images\_with lace (old)\` with their names kept; each shade folder still has 6 photos.
- **Website:** the same 17 photos (34 WebP files, 1024 and 560 wide) replaced in `assets/gallery/` on the branch `add-ai-gallery-images`, committed as "Replace 17 gallery images with lace-free versions". Not pushed yet; not for `main`. That branch's `assets/gallery/` photos aren't used by the site's code yet.
- **On the site (pull request 26, merged 26 October 2026):** 15 of the 17 copied into `assets/p/` (the 2 Curly ones are skipped because Curly wigs were removed). The `add-ai-gallery-images` branch was already on GitHub.

### Pull request 27: crochet on the homepage, general FAQs, Hair Bundles hidden (26 to 27 October 2026, merged)
- **Homepage:** a "Shop by category" list under the banner (two rows, Lace Front Wigs and Crochet & Feather, photos shown whole; `CATS_STYLE = "index"` in `src/build.py`. The boxed cards were rejected; a "split" band option is kept but not used), and a crochet section ("Feather-light, made by hand": 4 crochet products and texture links) after the wig textures. The banner says "Wigs & crochet" and has Shop wigs / Shop crochet buttons. Set in `home_cats` and `crochet_promo` in `src/build.py`. **Never crop the crochet photos** (client).
- **Hair Bundles hidden** (27 October 2026) until the bundles arrive: `hidden=True` in `EXTRA_COLLECTIONS` (`src/data.py`) removes the page, menu, footer, search and site map entries. Remove it (and `coming_soon` when they are ready) to bring them back.
- **All wigs page:** an "Also from Chesed" crochet strip (`also` in the hub). Wig shopping pages list Crochet & Feather in "Keep exploring".
- **Wig pages:** "You might also like: Crochet & feather extensions", same texture first (`p["crochet"]`).
- **FAQs:** `GENERAL_FAQ`, `WIG_FAQ`, `SHIP_FAQ` and `HOME_FAQ` in `src/data.py` (moved there from `build.py` on 27 October so Shopify reads them too). Homepage: a general mix. FAQ page: General, Lace front wigs, Crochet & feather, Shipping & returns (`FAQ_PAGE`). All wigs page: wig questions. Crochet pages: crochet questions plus choosing a color and length, and shipping and returns (`EXTRA_COLLECTIONS` in `src/data.py`).

### Shopify store (27 October 2026, in progress, not live)
The user builds in their own Shopify Partners development store and transfers it to Chesed when it's finished.
- **Store:** `chesed-hair-umskgt0n.myshopify.com` (password-protected, as development stores are). Admin login is the user's Partners account.
- **Products:** imported from a CSV made by `src/tools/export_shopify.py` (saved to `D:\Work\Chesed Hair\Shopify\chesed-products.csv`): 65 wigs (option Length, 10 lengths at the site's prices) and 6 crochet (Color, Length). Photos were fetched from the preview site. The 24 Permed Straight, Wet & Wavy and Deep Wave wigs are **drafts** (no photos yet). Hair Bundles left out. Tags: `wig`/`crochet`, `texture-<slug>`, `shade-<slug>`, `family-<family>`, `crochet-texture-<slug>`, `crochet-color-<slug>`.
- **Collections:** 21 automatic collections by tag, same addresses as the preview (`/collections/body-wave-wigs` etc.), products in the preview's order. `src/tools/shopify_collections.py`.
- **Shade and texture details** live once on their collection, in fields (metafields, namespace `chesed`): textures have `short`, `curly`, `length_photo`, `faq`; shades have `shade_key`, `shade_name`, `hex`, `blurb`, `faq`; All wigs and crochet have `faq`. Each wig points at its texture and shade collection (`chesed.texture`, `chesed.shade`). Chesed can edit these in the admin. `src/tools/shopify_metafields.py`.
- **Pages:** About, FAQ, Shipping, Returns, Contact, the length guide and the color guide, with the preview's text (`PAGES`, `PAGE_STEPS`, `FAQ_PAGE` in `src/data.py`). Each uses its own template. `src/tools/shopify_pages.py`.
- **Theme "Chesed"** (id 188679127198; live on the dev store since 28 October): built from Shopify's Skeleton theme in `chesed-theme`. Homepage sections, header and footer, shopping pages with filters, wig and crochet pages, info pages, guides, bag, search, 404. The bag is Shopify's real cart (`/cart.js`); search reads `/collections/all?view=search-index`. See that folder's `CLAUDE.md`.
- **Shared pieces:** `src/tools/theme_snippets.py` copies the stylesheet, fonts, non-product photos, spin wheel, length photos and sample reviews from the preview into the theme. The spin wheel drawing and length-line positions moved to `src/data.py` (`wheel_svg`, `length_photo`).
- **Textures without wigs on sale are hidden on Shopify** (27 October, user): Permed Straight, Wet & Wavy and Deep Wave are left out of the menus, footer and links, and the texture count says 6. They come back by themselves when their wigs are made active. The All wigs intro counts the same way (`shopify_collections.py`).
- **Footer line on both sites:** "Lace front wigs and crochet extensions in 100% human hair."
- **Checked in a browser (27 October):** every page type at 1440px and phone width matches the preview; adding a wig puts the chosen length in Shopify's cart. No Liquid errors; theme check passes. Theme code is in the private repo `zynthrixAI/chesed-theme`.

### Crochet lengths, email, checks (27 October 2026)
- **Crochet and feather lengths** (12" to 22") on the same length photos: on every crochet page ("Every length, side by side", tap a length to pick it) and in a new section of the length guide. Where each length ends was measured on the photo (12" shoulders, 14" below the shoulders, 16" armpits, 18" bust, 22" mid ribs; waves and curls one step higher). `CROCHET_LENGTHS`, `CROCHET_LANDMARKS`, `CROCHET_CURLY_LANDMARKS`, `CROCHET_LENGTH_PHOTO` in `src/data.py`. **Chesed to confirm.**
- **Contact email** is now chesedhaircollection@gmail.com everywhere (site, Shopify pages and theme settings).
- **Bag add-ons removed** (the "Complete the install" wig cap and edge brush were placeholders).
- **Order confirmation email** for Shopify: `chesed-theme/notifications/order-confirmation.liquid`, pasted by hand into Settings → Notifications.
- **Order confirmation email updated (28 October)** against Shopify's own default template, so nothing Shopify shows is lost: pending payment, pay on fulfilment and "action needed" messages, estimated delivery, the delivery note, gift cards, the PO number, Shopify's product title order, and the line photo. Theme repo commit e929d48, pushed 28 October.
- **Checks by agents:** security (no secrets anywhere; fixed text escaping in the script, added security headers on the preview, notes files hidden from the public preview), speed (smaller photos for phones, banner photos lazy-loaded), mobile (no sideways scrolling at 360px; bigger tap targets; readable sticky price; a "swipe" hint under the length tables).

### Plan change: update Chesed's own store instead of transferring (28 October 2026)
- **Chesed already has a Shopify store, "Chesed Hair Collection".** Web Wroughts has collaborator access to it, but the Shopify CLI can't reach it (it isn't in the Web Wroughts Partners organisation list). **No changes to it until the user says so.**
- **Why not transfer the dev store:** a transfer hands over a second, separate store. It doesn't replace or merge into their existing one, so Chesed would have to move their domain, apps, customers, orders and payment setup across themselves. Too much hassle for the client.
- **Decided:** ask Chesed for access to their store and update it in place. The dev store stays as our workshop and reference.
- **Steps once access is granted** (each needs the user's go-ahead):
  1. Look only: list their products, collections, pages, menus, apps and theme.
  2. Back up: export products (and customers and orders) as CSV, duplicate their current theme, and save a full read-only snapshot to files on this PC.
  3. Upload the Chesed theme unpublished.
  4. Merge products carefully: update existing ones in place (same handle), no duplicates.
  5. Add the collections, pages and shade and texture details.
  6. Publish only after the user (and Chesed) approve the preview.
  7. Remove the Shopify CLI connector app from their store.
- **Shopify backups:** Shopify has no store-wide restore point or undo. Themes can be duplicated (and theme files keep older versions); products, customers and orders can be exported as CSV. A backup app such as Rewind is worth suggesting to Chesed before launch. Our theme is safe in Git.

### Chesed theme live on the dev store (28 October 2026)
- The client opened the dev store on their MacBook and saw Shopify's default **Horizon** theme ("Welcome to our store", "Browse our latest products") with our wig photos. Not a caching problem: Horizon was the live theme, and the `?preview_theme_id=` link only shows the Chesed theme to someone signed in to the admin.
- **Fix:** the user published the **Chesed** theme on the dev store. It is now live there (behind the store password); Horizon is unpublished and kept as a fallback. Chesed's own store is untouched.
- From now on `shopify theme push` to the dev store changes what the client sees straight away.

### Chesed's own store: access, backup, theme uploaded (28 October 2026)
- **Store:** `gvit1g-jv.myshopify.com` (admin address `admin.shopify.com/store/chesedgirls`, site www.chesedhair.com). The Shopify CLI reaches it: themes through the user's normal sign-in, store data through `shopify store auth` (read-only scopes for now). In PowerShell, put the `--scopes` list in quotes, or the commas become spaces and the sign-in fails.
- **What was there:** no wigs; 23 crochet products (5 active, 18 drafts); 8 collections; Contact and privacy pages; menus with an ambassador program link (UpPromote app) and TikTok; 53 customers, 3 orders; discount code Anasia10 (active). Live theme "Re-degine Be Yours" (id 150027173942), plus older copies.
- **Backup:** `D:\Work\Chesed Hair\Shopify\backups\chesed-store-2026-10-28\` (not in any repo: it has customer data). Their live theme's files, every product, collection, page, menu, discount, customer and order as JSON, all 528 images, and the privacy policy page; see its README. The user also duplicated the live theme in the admin ("Copy of Re-degine Be Yours") and exported the orders CSV.
- **Decisions (user):** update their 5 active crochet products in place and keep their web addresses (Burmese Magic Curl is added as new); archive the 18 drafts; contact email chesedhaircollection@gmail.com.
- **Chesed theme uploaded unpublished** (id 158858969142). Their live theme is unchanged.
- **Store data merged (user chose "everything now", so it all shows on their live site in the old design too):**
  - The 5 crochet products updated in place (titles, descriptions, type "Crochet Extensions", tags, our Amazon photos with each colour linked to its photo, options renamed Color / Length). Same addresses, variants, SKUs and prices. The script is kept in the backup folder (`update_crochet.py`). Their addresses are mapped in `STORE_HANDLES` in `src/tools/shopify_api.py`, so the tools find them.
  - The 18 crochet drafts archived.
  - The 65 wigs (41 active, 24 drafts) and Burmese Magic Curl imported by the user from `D:\Work\Chesed Hair\Shopify\chesed-store-import-wigs-and-burmese-magic.csv` (made from `export_shopify.py` without the 5 existing crochet).
  - Collections, shade and texture details and pages added with the usual tools (`SHOPIFY_STORE=gvit1g-jv.myshopify.com`). Their 8 old collections are left as they were. Their Contact page now has our text.
- **Theme:** "Ambassadors" (UpPromote sign-up) in the header, phone menu and footer, a TikTok link in the footer, and the spin wheel switched off (theme settings `ambassador_url`, `tiktok_url`, `spin_wheel`). Checked in the preview on their store. Not yet uploaded to the dev store (its theme is live there; needs the user's go-ahead).
- **One email everywhere: chesedhaircollection@gmail.com** (user). The store's sender and contact emails already used it. Changed: the "Email Us" link in their CONNECT menu, and the footer of their live theme "Re-degine Be Yours" (only `sections/footer-group.json` was uploaded). Their privacy policy uses chesedhaircollection@gmail.com too (checked on the live site, 29 October).
- **Policies for their store** (29 October): refund, shipping and contact information drafted in `D:\Work\Chesed Hair\Shopify\policies-for-chesed-store.md` for the user to paste into Settings → Policies (no competitor named anywhere). Terms of service from Shopify's template; legal notice only if they sell to the EU. Client to confirm the public address and phone, the legal business name, international shipping and SMS.
- **Spin wheel back on** (29 October, client approved the wheel): codes WELCOME10/15/20 and SAVE20/40/60 created in Chesed's store as one-use-per-customer discounts; SAVE20 needs $100+, SAVE40 $150+, SAVE60 $200+ (`min` in `SPIN_PRIZES`, shown in the small print and the won line). On Shopify the wheel's form is Shopify's own customer form, posted into a hidden frame, so each email is saved in Customers as a subscriber tagged `spin-wheel` and `spin-<code>` (a scripted post is blocked by the store's bot protection). Theme setting `spin_wheel` is on. The preview site still saves nothing.
- **Launch audit (29 October)** by an agent: preview pages, links, images, prices and checkout all fine. Done after it: sample reviews hidden (`show_reviews` off; never show made-up reviews on the live store), policy links and "Your Privacy Choices" in the footer legal row, page titles no longer repeat "Chesed". **Their ambassador program is discontinued** (af.uppromote.com page says so, the app is uninstalled), so `ambassador_url` is blank and the link is hidden. Client questions: `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md`. Copy-ready policies: `policies-to-paste.html` in the same folder (the first paste showed raw `**`).
- **Done with the user's go-ahead (29 October):** the 3 empty texture collections unpublished (Permed Straight, Wet & Wavy, Deep Wave: republish when their wigs get photos); crochet compare-at prices cleared (150 variants); redirects /pages/our-story, why-chesed, our-team, careers → /pages/about, /pages/reviews → /, /pages/live-chat and book-appointment → /pages/contact; the ambassador link removed from their main menu and **the ambassador program removed from our theme entirely** (setting and links). Script: `backups/chesed-store-2026-10-28/prelaunch_fixes.py`.
- **Reviews (29 October):** 10 real reviews from Chesed's TikTok Shop and Amazon customers (user), in `REVIEWS` in `src/data.py`, with the line "From our customers on TikTok Shop and Amazon" (`REVIEWS_SOURCE`). Star ratings from the client (29 October; 4.5 shows as a half star), confirmed by Chesed in writing to the user. Homepage section on again (`show_reviews`). The sample reviews are gone.
- **Launched 29 October 2026 (user: "publish it"):** the Chesed theme is the live theme on www.chesedhair.com (their old theme "Re-degine Be Yours" and its copy are kept unpublished as a fallback). Their 7 old collections unpublished and redirected (lace-front-wigs and our-best-sellers → /collections/wigs; crochet-braid-hair-extensions, body-wave-hair, deep-wave-hair → /collections/crochet-braid-extensions; straight-hair → /collections/straight-wigs; frontpage → /), test1 deleted. Script: `backups/chesed-store-2026-10-28/launch.py`. Checked: every page type loads with no Liquid errors, old addresses redirect, all 6 crochet pages work.
- **Their store's preview link works for anyone** (the store has no password): `https://gvit1g-jv.myshopify.com?preview_theme_id=158858969142`.


### Curly wigs back, on the preview and Chesed's store (29 October 2026, pull request 33)
- **Curly wigs back** (user): 9 shades (1, 1B, Virgin, 350, 530, Honey Auburn, Honey Blonde, Natural Auburn, Red), their photos restored from history, and the 1B and 350 side photos now lace-free (from the `add-ai-gallery-images` branch). **Priced like Kinky Curly** (`TEXTURE_EXTRA["Curly"] = 4.50`; Curly is not on Chesed's sheet). Water Wave stays removed.
- **Chesed's store:** the user imported `D:\Work\Chesed Hair\Shopify\chesed-store-import-curly-wigs.csv` before the preview was live, so every photo failed; they were added again (`backups/chesed-store-2026-10-28/curly_photos_fix.py`: retries failed photos one at a time and puts them in order). **Merge and wait for the preview before importing a CSV.** Then `shopify_collections.py` (Curly page) and `shopify_metafields.py` on their store, and `curly-wigs` added to the theme's texture list.
- **Homepage crochet category photo** was blank on Chesed's store (their crochet products keep their old addresses): `templates/index.json` now uses their Burmese Curly address, and `home-categories.liquid` falls back to the collection's first product.


### Shade names for shoppers, deep-skin carousel (30 October 2026, pull request 37, live on both sites)
- **Shades read name first, number in brackets** (user): Natural Black (1B), Jet Black (1), Natural Dark Brown (Virgin), Rich Wine Red (530), Deep Plum (99J), Copper Ginger (350); Red is **Cherry Red**; Honey Auburn, Natural Auburn and Honey Blonde unchanged. `label` on each shade in `COLORS` (`src/data.py`), used in wig titles, shade pages, cards, menus, footer, filters, homepage, color guide and search chips. **Web addresses keep the number.** The big decorative numbers in the homepage shade panels stay numbers. Names still need Chesed's approval (client sheet item 3.2).
- **Shopify:** new field `chesed.shade_label` on the shade collections (the theme shows it, falling back to `shade_key`); `shopify_collections.py` keeps shade page titles in step; new `src/tools/shopify_titles.py` renames the wigs (title, search title and description only). Run on Chesed's store on 30 October: 53 wigs renamed, 10 shade pages renamed.
- **Wig pages: "on deep skin" photos are a carousel** (`.rail.scene-grid` with arrows, 4 across on desktop) instead of a grid that left one photo alone on a second row.

### Client work log and handover (30 October 2026)
- **Client work log** for Chesed, as a Claude Doc ("Chesed Hair: Work Delivered", https://claude.ai/artifact/WwPXxErn3hqasxgDgazZxu, export to Google Docs or PDF). Measured against the signed proposal (`D:\Work\Chesed Hair\Documents\New folder\Chesed Hair - Launch Proposal Revised.pdf`). Part 1 is the paid Launch Package and where each item stands; Part 2 is only the work beyond it. **5,437 images were made in total** (user). The image tools are not named in client documents (user).
- **Still owed from the proposal:** up to 5 minutes of AI video (the video spaces were removed at the client's request; to be planned with them). Basic SEO is set up (user, 30 October 2026); further SEO (keyword map, Search Console, GA4, Merchant Center, a reviews app) only if the client takes it up as a separate service.
- **Final handover:** `D:\Work\Chesed Hair\Documents\Chesed Hair - Final Handover.md` (not in this repo).

### Client answers: lengths, menu, Anasia10, address (30 October 2026, pull request 40)
- **Wigs 18" to 32"** (Chesed dropped 34" and 36"): `LENGTHS`, prices, landmarks and every "18 to 36 inches" line. On Chesed's store: 148 variants deleted (34" and 36" on all 74 wigs, drafts too) and the wording fixed on the wigs, 21 collections, the FAQ and the length guide (script kept in the session only; the 28 October backup has the old variants). Theme pushed live (17 files).
- **Menu:** the shade lists in the Wigs menu are one column, because the shade names with numbers ran into each other in two.
- **Anasia10 switched off**; the ambassador program stays off (nothing about it is left on the site). **10 shades is final** (no 12).
- **New public address and phone:** 1364 Buford Business Blvd, Suite 700, Buford, GA 30518; +1 (678) 765-8833. Changed by the user in the Contact information policy and Store details; the privacy policy is Shopify's automatic one and points to the contact page.
- **Crochet length photos** (client: the black hair on a black dress was hard to read and looked like the wig photos): the user made honey blonde versions of the three length photos in Gemini (black dress kept, user's choice), checked to line up with the originals (wavy shifted 10px). Files `length-crochet-<photo>-*.webp`; `length_photo(key, CROCHET_LENGTHS)` picks them. Live on both sites 30 October. Sources in `D:\Work\Chesed Hair\Images\crochet-length-*.png`.
- **Product pages: compact length band** (user, pull request 41): no padding above or below the "Every length, side by side" band; it uses the photo's own pink (#E9CDCA) and the photo's sides fade out, so the photo merges in. Length guide and homepage unchanged. Live on both sites 30 October.

---

## To do

### Ours
- [ ] **New shades and types:** add #2, #27, #4/30, Virgin Light, Loose Wave and Chesed's other new wig types once their photos and details arrive.
- [x] **Shopify theme:** checked every page in a browser; live on www.chesedhair.com since 29 October 2026.
- [x] **Curly wigs back** (29 October, at the Kinky Curly prices).
- [ ] Bring the workshop (dev) store's theme up to date, if it's still needed (only with the user's go-ahead).
- [ ] **AI video** from the proposal (up to 5 minutes), planned with the client.
- [ ] **SEO optimization**, only if the client takes it up (basic SEO is done).

### Waiting on Chesed
The full list sent to the client: `D:\Work\Chesed Hair\Shopify\what-we-need-from-chesed.md`. Main points:
- [ ] **Georgia sales tax** (the client sets it up; no tax is charged until then).
- [ ] **Business details:** legal business name (address and phone answered 30 October).
- [ ] **Shipping:** Standard and Express times; international shipping or not.
- [ ] **Photos:** Deep Wave, Permed Straight and Wet & Wavy wigs (all shades, plus mannequin front and back); Kinky Curly mannequin; Honey Auburn with more blonde highlights; the 4 bundles.
- [ ] **Shade names:** approve 1B Natural Black, 1 Jet Black, Virgin Natural Dark Brown, 530 Rich Wine Red, 99J Deep Plum, 350 Copper Ginger, Red Cherry Red. The shade descriptions were written from the photos too.
- [ ] **Deep Wave wigs:** approval of our copy.
- [ ] **Estimated prices:** **Curly** (priced like Kinky Curly).
- [ ] **Lengths missing from the sheet:** 28" for Kinky Straight and Permed Straight, and most lengths of coloured Deep Wave. The site sells them at the usual price; confirm.
- [ ] **Sheet questions:** Deep Wave 20" Red at $83.45; Loose Wave 22"-24" Virgin Light reads $1034.45; Wet & Wavy 20"-22" Virgin Light is at the coloured price.
- [ ] **Crochet lengths on the body:** our measurements, to confirm.
- [ ] **Spin wheel:** whether the shared codes should expire.
- [ ] **Price-drop alerts** (Watchlyst) or not. (Ambassador program off, Anasia10 off: answered 30 October.)
- [ ] **Hair bundles:** prices, plain names for the "TP" shades, photos.
- [ ] **Crochet descriptions:** the 6 listings still use the old store's wording.

### Shopify store
- [x] Products, collections, shade and texture details, info pages, theme, on Chesed's store; launched 29 October 2026.
- [x] Free shipping over $100, policies and payments (the user, 29 October).
- [x] Spin-wheel discount codes (29 October).
- [x] Real reviews with star ratings (from the client, 29 October).
- [x] Order confirmation email (theme repo; the user pasted it in).
- [ ] Menus as Shopify navigation, so Chesed can edit them (they're built into the theme for now).
- [ ] Connect the theme repo to the store (Shopify's GitHub integration), so changes deploy from GitHub.
- [ ] A reviews app (e.g. Judge.me) so new reviews come in on their own.
- [ ] Connect an email platform (e.g. Klaviyo) so the welcome wheel actually sends emails.
- [x] Two-step sign-in on the user's Shopify account (authenticator app, 30 October).
- [ ] Suggest a backup app (e.g. Rewind) to Chesed.
- [ ] Remove the Shopify CLI connector app from Chesed's store when the work is finished.
