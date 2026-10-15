# Chesed Hair website: project log

A preview of the Chesed Hair online store (lace front wigs), built by Web Wroughts so Chesed can approve the design before the real Shopify store is built.

- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Code:** https://github.com/zynthrixAI/chesed-hair
- **On this PC:** `C:\Users\syedh\code\chesed-hair`
- **Last updated:** 15 October 2026 (paused; see [NEXT-SESSION.md](NEXT-SESSION.md))

---

## What the site has

- **73 pages:** the homepage, 14 shopping pages ("collections"), 50 wig pages and 8 info pages (About, FAQ, Shipping, Returns, Contact, Color guide, Length guide, All pages).
- **7 textures:** Body Wave, Curly, Kinky Curly, Kinky Straight, Loose Deep Wave, Straight, Virgin Curl.
- **10 shades:** 1, 1B, 99J, 350, 530, Honey Auburn, Honey Blonde, Natural Auburn, Red, Virgin.
- **12 lengths:** 10" to 32".
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

---

## To do

### Our next steps
- [ ] Sign the GitHub tool on this PC back in (`gh auth login`).
- [ ] Decide whether the **All wigs** page should also lead with the style (it currently leads with the shade).
- [ ] Send the preview to Chesed for approval.

### Waiting on Chesed
These are placeholders on the site. Most are marked in **pink** so they're easy to spot.
- [ ] **Reviews:** the three homepage reviews (Jessica L., Monica R., Danielle K.) couldn't be verified and look like sample text from a website theme. Chesed must confirm they are real customers or replace them. Posting fake reviews breaks US advertising (FTC) rules.
- [ ] **WhatsApp number:** until Chesed provides it, tapping the button shows a "preview" notice.
- [ ] **Spin wheel:** the prizes, odds and discount codes.
- [ ] **Price:** currently $289 for every wig and length.
- [ ] **Free shipping threshold:** currently $200.
- [ ] **Processing and delivery times.**
- [ ] **Returns:** how the return label works and how long refunds take.
- [ ] **Wig details:** lace size, density and cap size.
- [ ] **About page:** founder story and photos.
- [ ] **Shade descriptions:** these were written by looking at the photos (e.g. "350 is bright copper orange"); Chesed should check them.

### When this becomes the real Shopify store
- [ ] Rebuild the pages as a Shopify theme. The page templates were written to be close to Shopify's template language.
- [ ] Create the spin-wheel discount codes in Shopify.
- [ ] Connect Judge.me for real reviews.
- [ ] Connect an email platform (e.g. Klaviyo) so the welcome wheel actually sends emails.
- [ ] Remove the "hidden from Google" settings so the store can be found.
