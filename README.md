# Chesed Hair: website preview

Static HTML preview of the Chesed Hair store, used for client approval before the Shopify build.

## How it's built
- `src/data.py`: the catalog (textures, colors, 50 products), shaped like Shopify product data.
- `src/templates/`: Jinja templates, one per page type plus shared partials. Jinja syntax is close to Shopify Liquid, so these port across.
- `python3 src/build.py` renders every page into the repo root with Shopify-style URLs:
  `/collections/<handle>/`, `/products/<handle>/`, `/pages/<handle>/`.
- Product photos live in `assets/p/` as WebP (1024 px and 560 px).

## Deploy
Hostinger pulls `main` and serves the repo root. Commit the rendered pages along with the sources.

## Preview rules
- Every page carries `noindex`; `robots.txt` and `.htaccess` block search engines. Keep them until this becomes the real store.
- Placeholders: price ($289), free-shipping threshold ($200), shipping times, lace size, density and cap size. They are marked in pink on the pages.
- Cart, checkout, Shop Pay and email signup are front-end only. Nothing is charged or stored.
