# Chesed Hair: pick up here

Updated 20 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com. Pull requests 10 to 15 (the client's homepage feedback, see PROJECT.md) are merged into `main`.
- **Open work:** branch `claude/remove-mannequin-photos` removes the mannequin photos I generated (they are still showing on the live site until it is pushed and merged). It is committed on this PC and **not pushed**; the user has not yet asked for that. Check `git status` and `gh pr list`.
- **GitHub tool:** signed in as zynthrixAI.
- **Mannequin photos:** none on the site right now. The user is preparing them by hand; the source shots are in `D:\Work\Chesed Hair\Images\Mannequin Photos - To Upload`. File naming for adding them is in PROJECT.md.
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, and every automatic crop/cut-out of the mannequin shots. The user was clear they would rather do the photos themselves.

## Start next time with
1. **Send the preview to Chesed** for approval.
2. Work through the "Waiting on Chesed" list in PROJECT.md (photos for Permed Straight, Wet & Wavy, bundles, Burmese Magic; bundle prices; wig lengths).
3. If the user hands over finished mannequin photos, add them as described in PROJECT.md.

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it."**
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first.
- Test pages with headless Chrome or puppeteer-core: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`
