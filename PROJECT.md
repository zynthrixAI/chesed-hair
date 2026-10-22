# Chesed Hair website: project log

A preview of the Chesed Hair online store (lace front wigs), built by Web Wroughts so Chesed can approve the design before the real Shopify store is built.

- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Code:** https://github.com/zynthrixAI/chesed-hair
- **On this PC:** `D:\Work\Chesed Hair\Website\chesed-hair`
- **Last updated:** 22 October 2026 (see [NEXT-SESSION.md](NEXT-SESSION.md))

---

## What the site has

- **120 pages:** the homepage, 24 shopping pages ("collections"), 82 wig pages, 5 extension pages and 8 info pages (About, FAQ, Shipping, Returns, Contact, Color guide, Length guide, All pages).
- **11 wig textures:** Body Wave, Curly, Kinky Curly, Kinky Straight, Loose Deep Wave, Straight, Virgin Curl, plus **Permed Straight**, **Wet & Wavy**, **Deep Wave** and **Water Wave** (placeholder photos for now).
- **Two extra categories:** Crochet & Feather Extensions (5 products) and Hair Bundles (coming soon).
- **10 shades:** 1, 1B, 99J, 350, 530, Honey Auburn, Honey Blonde, Natural Auburn, Red, Virgin.
- **10 lengths:** 18" to 36".
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
- **Mannequin photos (open):** the client's studio shots (front and back of each wig on a mannequin) are meant to be the last photos in each wig's gallery. Several automatic attempts (cropping the combined front-and-back picture, centring, background removal) were **rejected**, so **there are no mannequin photos on the site now**. The user will prepare them by hand. The unedited source shots, picked and named per wig, are in `D:\Work\Chesed Hair\Images\Mannequin Photos - To Upload` (98 files, `<handle>-mannequin-front.jpg` / `-back.jpg`, for 49 wigs; Kinky Curly, Permed Straight and Wet & Wavy have none). To add them: save each finished photo as WebP into `assets/p/` as `<handle>-7-mannequin-front-1024.webp` and `-560.webp` (front) and `<handle>-8-mannequin-back-1024.webp` and `-560.webp` (back), then rebuild. `build_products()` in `src/data.py` then puts them in the last two gallery slots (replacing the "fingers" photo); wigs without them keep the six AI photos.

---

## To do

### Our next steps
- [x] GitHub tool signed in (16 October 2026).
- [x] All wigs page leads with the style.
- [ ] Send the preview to Chesed for approval.

### Client feedback, round 2 (22 October 2026)
Feedback came in a Google Doc ("Website Updates"). Merged as pull requests 16 (mannequin photos removed) and 17:
- **Wig lengths are 18" to 36"** (was 10" to 32"). Lengths and where they end on the body are set once in `LENGTHS`, `LANDMARKS` and `CURLY_LANDMARKS` in `src/data.py` and passed to the script through `window.CHESED`. Wig pages open on 24" (`DEFAULT_LENGTH`).
- **Wig details:** 13x5 lace front, one size fits all cap, density removed.
- **Shades in words:** each shade has a `name` in `COLORS` (1B Natural Black, 1 Jet Black, Virgin Natural Dark Brown, 530 Rich Wine Red, 99J Deep Plum, 350 Copper Ginger, Red Cherry Red; the auburns and Honey Blonde keep their names). The wig page "Shade" label, the swatch pop-ups and the homepage shade sections show the name. Product titles and web addresses still use the number.
- **"Worn by you"** (try-on videos and review placeholder) removed from wig and extension pages, with the star-rating placeholder.
- **Crochet & Feather:** Kinky Curly and Loose Wave taken out of the menu and filters (`CROCHET_TEXTURES`). The "20 extensions / 10 lengths" boxes replaced with "Human hair, handmade" and the lowest price. Products "Lightweight Ripple Deep Curl" and "Highlight #4/30/530 Water Wave" removed (the importer skips them too).
- **Hair Bundles: coming soon.** `coming_soon=True` on the bundle collection in `src/data.py`: the bundle page shows a coming-soon note, the menu says "Coming soon", and the 4 bundle product pages are no longer built.
- **Free shipping over $100** (`FREE_SHIP`), used everywhere including the bag's progress bar.
- **About page:** the story from chesedhair.com (meaning of Chesed, why you'll love it, care and versatility, ethical commitment). Founder story and photos still to come.
- **Deep Wave and Water Wave wigs** added as drafts (8 shades each, same as Permed Straight, with "Photo coming soon" pictures and copy we wrote).
- **Not done yet: the length picture (reminder).** The client wants a body picture showing where each length ends, like their Amazon listing, but nicer. Two tries so far: a drawn back-view figure whose hair grows (rejected as worse), and an AI photo of a model from behind with a length ruler (on hold). Come back to this.

**Follow-up (22 October 2026, branch `claude/cap-photos-live-crochet`):**
- **Cap pictures on every wig:** the client's "One size fits all" and "6X secure fit guard" pictures (`wig-cap-one-size`, `wig-cap-secure-fit` in `assets/p/`) are the last two photos in every wig's gallery, full width so they aren't cropped. Set in `CAP_IMAGES` in `src/data.py`; they are kept out of shop cards and the "on deep skin" photos.
- **Crochet & Feather: only the 5 listings that were live in Shopify** (Wet & Wavy, Kinky Straight, Burmese Curly, Body Wave, Deep Wave). The client said the 14 drafts were tests. Burmese Magic (only on the item list) was removed too. The importer skips drafts and Burmese Magic.

**Wig prices (23 October 2026, branch `claude/wig-prices`):** from Chesed's price sheet ("CHESED WIG Selling Price", JK Trading, 1 September 2026). Set in `WIG_LENGTH_PRICE`, `COLOR_EXTRA` and `TEXTURE_EXTRA` in `src/data.py`.
- Per length: 18" $69.95, 20" $79.95, 22" and 24" $99.95, 26" $129.95, 28" $139.95, 30" $149.95, 32" $189.95, 34" $219.95, 36" $249.95. The sheet's bands overlap ("18-20", "20-22", "22-24"); the user chose the lower band, so 20" = $79.95 and 22" = $99.95.
- Plus $5 for every shade except 1, 1B and Virgin. Plus $3.50 for Loose Deep; $4.50 for Kinky Curly, Virgin Curl, Kinky Straight and Wet & Wavy.
- The wig page price, "or 4 payments", Add to bag and the sticky bar follow the chosen length; quick add uses each length's price; cards show "From" the 18" price.
- **Our estimates, for Chesed to confirm:** 28", 34" and 36" (not on the sheet), and the extras for Curly (+$4.50), Water Wave (+$4.50), Deep Wave (+$3.50) and Permed Straight (+$0).

**Mannequin photos (23 October 2026, branch `claude/wig-prices`):** the user's hand-edited mannequin photos (`D:\Work\Chesed Hair\Images\Mannequin Image Edit Preview`, named `<Texture> - <Shade> - Front/Back.png`, transparent, 1000x1000) are on all 49 wigs that have studio shots. Saved on the pearl background as `<handle>-7-mannequin-front` and `-8-mannequin-back` in `assets/p/`; they replace the "fingers" photo and sit side by side, square and uncropped (`.g-mq`). **Three Body Wave files had the wrong shade name** (checked against the original studio shots): the file named 530 is 350, the one named 99J is 530, and the one named 350 is 99J. They were placed on the right wigs, and the files in the folder were renamed to match (23 October 2026).

**Chesed's answers (23 October 2026, branches `claude/photo-versions` and `claude/client-answers`):**
- **Photos refresh straight away:** every photo address carries a fingerprint of the file (`img()` in `src/build.py`), because Hostinger tells browsers to keep photos for 7 days and replaced photos kept showing the old version.
- **Crochet photos from Amazon:** `src/tools/import_amazon_crochet.py` reads `D:\Work\Chesed Hair\Images\Assets - Chesed Hair\Amazon-...\Amazon` and gives each crochet product its six colour photos (square model-plus-product shots) and the info slides (size chart, knotless loop, human hair, feather crochet, packs, crochet vs bulk). Choosing a colour puts that colour's photo first (`showColor` in `main.js`). Crochet galleries show square photos whole on white (`.g-x`).
- **Burmese Magic is back** (6 crochet products), with the same lengths, colours and prices as Burmese Curly.
- **Reviews:** the user asked for demo reviews. Six sample reviews in `REVIEWS` (`src/data.py`), each tagged "Sample" in pink, with a note that they are replaced by real reviews before launch.
- **WhatsApp button removed** (not needed). **About page:** founder story and photos not needed; the note is gone.
- **Shipping and returns follow LUVME's terms** (client's choice): ships within 1 business day, express delivery in 2 to 6 business days, cancel within 1 hour; 30-day returns and exchanges for unused hair with the lace uncut, approval by email with photos, one free US return label per order, refunds within 2 business days of checking the return, exchanges ship within 3 business days. On the Shipping and Returns pages, wig and crochet pages, and the FAQ.

**What Chesed needs to send:**
- [ ] **Deep Wave and Water Wave wigs:** which shades each comes in, the price, lengths, approval of our copy, and photos for every shade (front, three-quarter, back, side, close-up, lifestyle, plus mannequin front and back).
- [ ] **"Missing notes: Straight, Deep Wave, Water Wave":** confirm these are wig styles. Straight is already on the site.
- [ ] **The 12 shades:** the site has 10. Names of the 2 missing shades, which styles they come in, and photos.
- [ ] **Prices we estimated:** 28" ($139.95), 34" ($219.95), 36" ($249.95), and the extras for Curly, Water Wave, Deep Wave and Permed Straight.
- [ ] **Honey Auburn:** new photos with more blonde highlights.
- [ ] **Shade names:** approve the names we wrote (e.g. "Rich Wine Red" for 530), listed above.
- [ ] **Body positions for 34" and 36":** we guessed "mid thigh" and "lower thigh".
- [x] **Crochet & Feather:** answered: only the 5 live listings stay (see the follow-up above). (The two Shopify drafts "Lightweight Ripple Deep Curl" and "Highlight #4/30/530 Water Wave" were removed at the client's request, 22 October 2026; the importer skips them too.)
- [ ] **Length chart picture (ours to fix):** the client liked a "How to measure" chart with three back-view photos (straight, wave, curly) and length lines. A test with three AI photos and lines for 18" to 36" was shown to the user (23 October 2026); waiting for the go-ahead before building it into the length guide, wig pages and homepage.

### Waiting on Chesed
These are placeholders on the site. Most are marked in **pink** so they're easy to spot.
- [ ] **Spin wheel:** the prizes, odds and discount codes.
- [ ] **Real reviews:** the homepage shows 6 sample reviews (tagged "Sample") until real ones come in.
- [ ] **Bundle prices and "TP" shade names:** Chesed will provide them.
- [ ] **Price:** wigs use Chesed's price sheet (see above). Bundles are "coming soon" (placeholder $99 when they return).
- [ ] **New photos needed:** Permed Straight, Wet & Wavy, Deep Wave and Water Wave wigs, Honey Auburn (more blonde highlights), and the 4 bundles.
- [ ] **Check the item list:** the "TP" shades (TP27, TP30...) in the bundle tab need a plain-language name. The 5 extension listings still use the old store's descriptions and are missing a return policy.
- [ ] **Copy for the two new wig styles and the two new categories** was written by us. Chesed should check it.
- [ ] **Shade descriptions:** these were written by looking at the photos (e.g. "350 is bright copper orange"); Chesed should check them.

### When this becomes the real Shopify store
- [ ] Rebuild the pages as a Shopify theme. The page templates were written to be close to Shopify's template language.
- [ ] Create the spin-wheel discount codes in Shopify.
- [ ] Connect Judge.me for real reviews.
- [ ] Connect an email platform (e.g. Klaviyo) so the welcome wheel actually sends emails.
- [ ] Remove the "hidden from Google" settings so the store can be found.
