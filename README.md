# HAVN demo app

Investor demo of the HAVN guest journey (find → hold → unlock → rest → leave) as a single-file mobile web app.

- `src/app.html` – the app (HTML/CSS/JS, `{{IMAGES}}` / `{{QRS}}` placeholders)
- `src/images.json` – base64 renders cropped from `~/dev/havn-deck/img` (interiors3b, src_05, src_06b, src_07b, src_13c)
- `build.py` – builds `dist/artifact.html` (body only, for the Claude artifact) and `dist/index.html` (full document, PWA metas, for hosting or download); needs Pillow + segno
- `dist/icon-*.png`, `dist/manifest.webmanifest` – home-screen icon + manifest for the hosted variant
- `docs/` – GitHub Pages site (havn.rest): `docs/index.html` is the static coming-soon placeholder (logo, claim, no build step); `docs/demo/` is the hosted demo app, written by `build.py` (`docs/sw.js` only unregisters the old root service worker)

Published artifact (V1, 07.10.2026): https://claude.ai/artifact/6vUiX5PxAEVy7gdzrpoVeb
Downloadable copy: ~/Downloads/HAVN App Demo V1.html

Design system: HAVN deck (off-white #F4F2EE, ink #141414, grey #6F6B66, hairline #D6D2CB, vermilion #C9251B, Helvetica Neue light, Georgia wordmark).
Prices and room types follow deck V3.13 (Single €29/2h · €69/night, Double €39/2h · €89/night, Health Pod €19/h, member −20%).
