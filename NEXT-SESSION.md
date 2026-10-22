# Chesed Hair: pick up here

Updated 23 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com. Everything up to pull request 20 is merged and live. Check `git status` and `gh pr list` for anything newer.
- **GitHub tool:** signed in as zynthrixAI.
- **On the site now:** wig lengths 18" to 36" with Chesed's prices, shade names in words, the client's cap pictures and the user's hand-edited mannequin photos on every wig that has them, 6 crochet products with their Amazon photos, bundles "coming soon", 6 sample reviews (tagged "Sample"), and shipping and returns modelled on LUVME.

## Start next time with
1. **Length picture.** The user is choosing between four layouts made from three AI back-view photos (straight, wavy, curly): A lines on the hair, B ruler beside each photo, C pink tags plus a size table, D one photo with Straight/Wavy/Curly tabs. Our suggestion: C for the length guide and homepage, D on wig pages. The test page is `lenvar.html` with photos `lc-straight.jpg`, `lc-wave.jpg`, `lc-curly.jpg` in the previous session's scratchpad (`C:\Users\syedh\AppData\Local\Temp\claude\d--Work-Chesed-Hair-Website-chesed-hair\24392e20-6bc0-440a-923c-2e18f2d28ee1\scratchpad`). If they are gone, regenerate the three photos (Black model from behind, black fitted mini dress, blush backdrop, head to above the knees) and line them up so shoulders and hem match. When the user picks, save the photos into `assets/p/` and build it into the length guide, wig pages and homepage.
2. **Send Chesed the updated preview** and the "Waiting on Chesed" list in PROJECT.md.

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, and the drawn back-view length figure.
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
