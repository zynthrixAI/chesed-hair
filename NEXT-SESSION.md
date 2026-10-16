# Chesed Hair: pick up here

Updated 16 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Open work:** branch `claude/new-ai-images` holds the new photos, the top-centre crops, the image morph and the new products from the client's files. It is committed on this PC and may not be pushed or merged yet; check `git status` and `gh pr list`.
- **GitHub tool:** signed in as zynthrixAI.
- **Wig card names:** color pages, homepage best sellers and the All wigs page lead with the style (e.g. **Body Wave**, then "1B Lace Front Wig"). Style pages lead with the shade.

## Start next time with
1. Check whether the `claude/new-ai-images` pull request is open and merged. Merge only when the user says "merge it".
2. **Send the preview to Chesed** for approval.
3. Work through the "Waiting on Chesed" list in PROJECT.md. New items: photos for Permed Straight, Wet & Wavy, the bundles and Burmese Magic; bundle prices; wig lengths (the item list starts at 18").

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Ask before `git push`.
- **Merge only when the user says "merge it."**
- Deleting lots of files at once is blocked by Claude Code's safety check until the user says yes.
- Test pages with headless Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --screenshot=out.png --window-size=1440,1500 --virtual-time-budget=6000 http://127.0.0.1:8000/...`
