# Chesed Hair: pick up here

Updated 22 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Two branches are committed on this PC and not pushed** (the user has not asked yet). Check `git status` and `gh pr list`.
  - `claude/remove-mannequin-photos`: removes the mannequin photos we generated. They are still on the live site, and the client noticed "a weird outline" around them.
  - `claude/new-styles-coming-soon`: the client's round 2 feedback (see "Client feedback, round 2" in PROJECT.md). This includes lengths 18" to 36", shade names, 13x5 lace and one-size cap, the reviews section removed, crochet fixes, bundles "coming soon", free shipping over $100, the About story, and new Deep Wave and Water Wave wigs.
- **GitHub tool:** signed in as zynthrixAI.
- **Mannequin photos:** none on the site. The user is preparing them by hand; the source shots are in `D:\Work\Chesed Hair\Images\Mannequin Photos - To Upload`. File naming is in PROJECT.md.

## Start next time with
1. **Reminder: the length picture still needs fixing.** The client wants a body picture showing where each length ends (like their Amazon listing, but nicer). A drawn figure was rejected; an AI photo of a model from behind with a length ruler is on hold. Ask the user how they want to continue.
2. Push and open pull requests for the two branches when the user says so.
3. Send Chesed the list of what they need to send ("What Chesed needs to send" in PROJECT.md).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it."**
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, and the drawn back-view length figure.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe.
