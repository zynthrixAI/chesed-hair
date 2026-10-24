# Chesed Hair website: project log

A preview of the Chesed Hair online store (lace front wigs), built by Web Wroughts so Chesed can approve the design before the real Shopify store is built.

- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Code:** https://github.com/zynthrixAI/chesed-hair
- **On this PC:** `D:\Work\Chesed Hair\Website\chesed-hair`
- **Last updated:** 24 October 2026 (see [NEXT-SESSION.md](NEXT-SESSION.md))

---

## What the site has

- **102 pages:** the homepage, 22 shopping pages ("collections"), 65 wig pages, 6 extension pages and 8 info pages (About, FAQ, Shipping, Returns, Contact, Color guide, Length guide, All pages).
- **9 wig textures:** Body Wave, Kinky Curly, Kinky Straight, Loose Deep Wave, Straight, Virgin Curl, plus **Permed Straight**, **Wet & Wavy** and **Deep Wave** (placeholder photos for now). Curly and Water Wave wigs were removed because they are not on Chesed's price sheet.
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

### Lace-free photos (24 October 2026, not merged)
- **Chesed's photo folders:** 17 photos replaced with versions where the wig lace was removed (`Images\Lace Review\No lace`). The old ones were moved to `Final Images\_with lace (old)\` with their names kept; each shade folder still has 6 photos.
- **Website:** the same 17 photos (34 WebP files, 1024 and 560 wide) replaced in `assets/gallery/` on the branch `add-ai-gallery-images`, committed as "Replace 17 gallery images with lace-free versions". Not pushed yet; not for `main`. That branch's `assets/gallery/` photos aren't used by the site's code yet.

---

## To do

### Ours
- [ ] **New shades and types:** add #2, #27, #4/30, Virgin Light, Loose Wave and Chesed's other new wig types once their photos and details arrive.
- [ ] Send Chesed the updated preview.
- [ ] **Branch `add-ai-gallery-images`:** push when the user says so. If its photos should go on the live site, they need adding to `assets/p/` (the folder the site uses) on a branch from `main`.

### Waiting on Chesed
- [ ] **Photos:** Deep Wave, Permed Straight and Wet & Wavy wigs (all shades, plus mannequin front and back); Honey Auburn with more blonde highlights; the 4 bundles.
- [ ] **The 12 shades:** the site has 10. Names of the 2 missing shades and which styles they come in.
- [ ] **Shade names:** approve 1B Natural Black, 1 Jet Black, Virgin Natural Dark Brown, 530 Rich Wine Red, 99J Deep Plum, 350 Copper Ginger, Red Cherry Red. The shade descriptions were written from the photos too.
- [ ] **Deep Wave wigs:** approval of our copy.
- [ ] **Estimated prices** (not on the sheet, shown doubled): 34" and 36" (sheet-level $209.95 and $239.95, so $419.95 and $479.95 for 1B Straight).
- [ ] **Lengths missing from the sheet:** 28" for Kinky Straight and Permed Straight, and every length except 28" for coloured Deep Wave (only Red also has 20"). The site still sells them at the usual price; confirm.
- [ ] **Sheet questions:** Deep Wave 20" Red at $83.45 (every other coloured shade is $5 more); Loose Wave 22"-24" Virgin Light reads $1034.45; Wet & Wavy 20"-22" Virgin Light is at the coloured price; Deep Wave and Loose Wave list only some shades per length.
- [ ] **34" and 36" on the body:** we guessed "mid thigh" and "lower thigh".
- [ ] **Spin wheel:** the prizes, odds and discount codes (not answered yet).
- [ ] **Hair bundles:** prices and plain names for the "TP" shades (Chesed is working on these).
- [ ] **Crochet descriptions:** the 6 listings still use the old store's wording.

### When this becomes the real Shopify store
- [ ] Rebuild the pages as a Shopify theme. The page templates were written to be close to Shopify's template language.
- [ ] Replace the 6 sample reviews with real ones (connect Judge.me).
- [ ] Create the spin-wheel discount codes in Shopify.
- [ ] Connect an email platform (e.g. Klaviyo) so the welcome wheel actually sends emails.
- [ ] Set free shipping over $100 in Shopify's shipping settings.
- [ ] Remove the "hidden from Google" settings so the store can be found.
