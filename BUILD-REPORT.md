# Nano portal: build report

## Structure
- `public/index.html`: the landing page (Spanish). It has an inline SVG sprite with the gradients, the clip paths, Nano's face symbols (`f-neutral`, `f-feliz`, `f-enojado`, `f-guino`, `f-dormido`, `f-furioso`, `f-estresado`, `f-guns`) and the Iconsax Bulk icons. The icons were converted from the app's own `ic_iconsax_*.xml` drawables, so they match the app.
- `public/styles.css`: tokens from `docs/design/nano-ui.md` and the Hallmark stamp. Sections in order: hero, HUD replica, bento, ink timeline, privacy and requirements, the "Próximamente" card, the download band, the footer and the 404 page.
- `public/main.js`:
  - `DOWNLOAD_URL = null` at the top. A non-null value activates every `[data-download]`.
  - A live clock in the HUD (the visitor's own time).
  - The flip cards: `<button aria-pressed>`, the hidden face gets `aria-hidden`, and each card flips back on its own after 15 s, as in the app.
  - Header scroll state, parallax and reveal on scroll, all gated by `html.motion`.
- `public/404.html`: Nano asleep.
- `public/assets/`: `favicon.svg` (two cyan eyes on a dark rounded square), `favicon-32.png`, `apple-touch-icon.png` (180), and `og.png` (1200×630).
- `vercel.json`: Voltia's headers, without the `latest.json` rewrite. The CSP `connect-src` is tightened to `'self'` because the page makes no fetch.
- `tools/make-assets.py`: Pillow script that generates the PNGs.
- `README.md`: mirrors Voltia's. It covers the Vercel setup with `outputDirectory: public`, the domain `nano.angellm.dev`, the Cloudflare CNAME `nano` → `cname.vercel-dns.com` (DNS only), how to switch the download on, and local preview.

## Decisions
- **Architecture copied from Voltia:** no build step, system fonts, no inline style or script, no CDNs. Motion uses only transform and opacity, is gated by `html.motion`, and `prefers-reduced-motion` switches every animation and transition off. The hero face then stays on neutral and all content is visible.
- **Hero face:**
  - It is an SVG built from `<use>` layers.
  - An 18 s CSS cycle runs neutral → feliz → neutral → guiño → FURIOSO (with the cartoon pistols and the BANG flash) → neutral, with blinks and gaze shifts.
  - Fills are presentation attributes inside the sprite, because document CSS cannot reach into `<use>` shadow trees with descendant selectors.
- **Colour and contrast:**
  - Small coloured text uses lighter tints (`#60A5FA`, `#A78BFA`, `#34D399`), all ≥ 6:1 on `#070B14`.
  - The button gradient uses `#2563EB` → `#7C3AED`, so white text clears 5:1.
  - `#64748B` is used only for decoration.
- **Download:**
  - The header and footer links go to `#descargar`.
  - The band button is `aria-disabled` and has no href.
  - All three are marked `data-download` with a `data-download-text` label for when `DOWNLOAD_URL` is set.
  - No URL was invented.
- **Demo data only:**
  - The PC is "MI-PC" and the processes are game.exe, obs64.exe, chrome.exe, discord.exe and explorer.exe.
  - The token is "481 207".
  - Nothing from the private screenshots was used: no PC name, IP or real process list.
- **Claims:**
  - Android 8.0+ comes from minSdk 26 in the spec.
  - Price and Windows version were not claimed, because the spec doesn't state them.
  - For the Gemini voice feature (v2), the page promises to explain later what it sends, rather than claiming "no cloud".
- **Hallmark:** Voltia's product-rail macrostructure was kept on purpose, because the brief asked for the same structure. The brief also explicitly asked for a phone replica, which overrides Hallmark's rule against redrawn chrome.

## Verification
- The page was served with a local Python server that adds the `vercel.json` CSP header. There were no console errors and no CSP violations.
- At 375 px, `scrollWidth` equals 375, so there is no horizontal scroll.
- Flip cards with the keyboard: Enter on the first card and Space on the second (after Tab) both flipped, and `aria-pressed` and `aria-hidden` were updated.
- Reduced motion: a headless Chrome capture with `--force-prefers-reduced-motion` shows everything revealed and the face on neutral.
- The local servers were stopped at the end.

## Screenshots
All in `C:\Users\angel\AppData\Local\Temp\claude\14e89112a5e2c253\49644eff-0b80-4a38-89c2-3e6d845ad074\scratchpad\shots\` (scratchpad, not committed):
- `desktop-1366.png`: full page, reduced motion
- `desktop-hero.png`
- `desktop-hero-furioso.png`: test copy with the FURIOSO frame forced
- `crop-hud.png`
- `crop-bento.png`
- `desktop-404.png`
- `mobile-375-hero.jpg`
- `mobile-375-hud.jpg`
- `mobile-375-flipped.png`
- `mobile-375-bento.jpg`
- `mobile-375-steps.jpg`
- `mobile-375-final.jpg`

## Left to do
- Set `DOWNLOAD_URL` and the `href`s once there is a public APK or agent build.
- Bump `?v=` on `styles.css` and `main.js` after any change.
- The phone-battery back face's Iconsax battery outline is drawn at 40 % opacity, so on the gradient it reads mainly as the bolt. It's cosmetic.
- No Lighthouse run was done.
