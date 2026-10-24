# Chesed Hair: pick up here

Updated 24 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com. Everything up to pull request 22 is merged and live. Check `git status` and `gh pr list` for anything newer.
- **Pull request 22** (see PROJECT.md): length photos (layout C) on the length guide, homepage and wig pages; wig prices doubled from Chesed's corrected sheet; Burmese Magic Curl rename.
- **GitHub tool:** signed in as zynthrixAI.

## Start next time with
1. Send Chesed the preview and the "Waiting on Chesed" list in PROJECT.md (sheet questions, estimated prices).
2. Add the new shades and wig types when Chesed sends photos.

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it"** (they also say "push and merge").
- **Rejected designs, do not redo:** the thumbnail-rail and blurred-backdrop product galleries, the sideways-scrolling textures section, every automatic crop or cut-out of the mannequin shots, the drawn back-view length figure, and the strand length charts (replaced by the length photos).
- **Photos:** always write photo addresses with `img(file, width)` in templates and `build.py`. Hostinger tells browsers to keep photos for 7 days, so a photo replaced under the same name only shows up because of the fingerprint `img()` adds.
- **Check photo names against the content.** Three of the user's hand-edited Body Wave files had the wrong shade name; compare new photos with the originals before adding them.
- The user prefers to see results (screenshots) before anything is pushed, and gets frustrated by long experiments that don't land: show a small test first.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`. The window can't go narrower than about 500px, so for phone width put the page in a 390px-wide iframe. The welcome spin wheel pops up over screenshots, and headings animate in, so a missing heading in a screenshot is usually just timing.
