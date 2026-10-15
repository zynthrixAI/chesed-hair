# Chesed Hair: pick up here

Paused on 15 October 2026. Read this, then [HANDOFF.md](HANDOFF.md) for setup and [PROJECT.md](PROJECT.md) for the full history.

## Where things stand
- **Everything is merged and live.** No open branches or pull requests are waiting.
- **Live preview:** https://lime-deer-681625.hostingersite.com
- **Product names now:**

| Page | Big name on each wig | Line under it |
|---|---|---|
| Color pages (e.g. 350 Wigs) | Style: **Body Wave** | 350 Lace Front Wig |
| Homepage best sellers | Style: **Body Wave** | 1B Lace Front Wig |
| Style pages (e.g. Body Wave Wigs) | Shade: **1B** | Body Wave Lace Front Wig |
| All wigs page | Shade: **1B** | Body Wave Lace Front Wig |

## Done on 15 October 2026
1. Merged pull request 7: color pages lead with the style.
2. Homepage best sellers now lead with the style too (merged without a pull request page, because the GitHub tool was signed out).
3. Saved CLAUDE.md, HANDOFF.md, PROJECT.md and this file to GitHub. They are publicly readable on the preview site; the user chose that.

## Start tomorrow with
1. **Sign the GitHub tool back in** so changes get normal pull request pages:
   `"C:\Program Files\GitHub CLI\gh.exe" auth login` (GitHub.com, then log in with a web browser).
2. **Decide the All wigs page:** lead with the style or keep the shade? To switch it, add `card_lead="texture"` to the All wigs render call in `src/build.py` (the one with `is_hub=True`).
3. **Send the preview to Chesed** for approval.
4. Then work through the "Waiting on Chesed" list in PROJECT.md (reviews, WhatsApp number, prices, shipping, returns, wig details, About page, shade descriptions).

## Things to know
- **Uploading to GitHub needs the user's clear go-ahead.** Claude Code's safety check blocked `git push` until the user said yes. Ask before pushing, or the user can allow `git push` in `/permissions`.
- **Merge only when the user says "merge it."**
