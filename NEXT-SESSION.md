# Chesed Hair: pick up here

Updated 22 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Merged and live:** pull requests 16 (generated mannequin photos removed) and 17 (client feedback round 2). See PROJECT.md.
- **Open work:** branch `claude/client-answers` (built on `claude/photo-versions`): photo fingerprints, Amazon crochet photos, Burmese Magic back, sample reviews, WhatsApp removed, shipping and returns from LUVME. Check `git status` and `gh pr list` to see whether it has been pushed and merged.
- **GitHub tool:** signed in as zynthrixAI.
- **Mannequin photos:** on all 49 wigs that have studio shots (branch `claude/wig-prices`). See PROJECT.md for the three Body Wave files that had the wrong shade name.

## Start next time with
1. **Length picture:** the client liked a "How to measure" chart with three back-view photos (straight, wave, curly) and length lines. A test with three AI photos is in the scratchpad (`len3.html`, photos `lc-*.jpg`); the user has not said yes yet. If they do, copy the photos into `assets/p/` and build it into the length guide, wig pages and homepage.
2. Push and merge `claude/client-answers` when the user says so.
3. Send Chesed the list of what they need to send ("What Chesed needs to send" in PROJECT.md).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it."**
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, and the drawn back-view length figure.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe.
