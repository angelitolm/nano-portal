# nano-portal

Web de Nano: https://nano.angellm.dev

Estática (HTML + CSS + un poco de JS), sin build ni dependencias, en Vercel.
Nano convierte un Android viejo en una mascota de escritorio que se alterna con un HUD de rendimiento del PC.

## Publicar (Vercel)

1. Vercel → Add New → Project → importa el repo `nano-portal`.
2. Framework Preset **Other**. `vercel.json` ya fija: sin build, salida `public/` (`outputDirectory`), cabeceras de caché y seguridad (CSP estricta: sin scripts ni estilos en línea, sin CDNs ni fuentes externas).
3. Project → Settings → Domains → `nano.angellm.dev`. En Cloudflare DNS crea el CNAME `nano` → `cname.vercel-dns.com`
   en modo **DNS only** (nube gris), si no Vercel no puede emitir el certificado.

Cada push a `main` publica; las otras ramas generan previews.

## Enlace de descarga

Todavía no hay descarga pública de la app ni del agente: los botones muestran «Muy pronto».

- Cuando la haya, cambia `DOWNLOAD_URL` al principio de `public/main.js` (hoy `null`). Activa todos los elementos con
  `data-download` (cabecera, banda final y pie): pone el `href`, quita el estado «Muy pronto» y cambia el texto al de `data-download-text`.
- Como respaldo sin JS, pon la misma URL en los `href` con `data-download` de `public/index.html`.
- Si la URL está en otro dominio, no hace falta tocar la CSP: es un enlace, no un `fetch`.

## Recursos

- `public/assets/favicon.svg`: el logo (los ojos de Nano). Los PNG (`favicon-32.png`, `apple-touch-icon.png`, `og.png` de 1200×630)
  se generan con `python tools/make-assets.py` (Pillow).
- Iconos: Iconsax (variante Bulk, la misma de la app), licencia MIT, en un sprite SVG dentro de `index.html`.
- Las réplicas de la cara y del HUD son HTML/CSS/SVG con datos de ejemplo: no hay capturas de pantalla.

Cabeceras de caché y seguridad en `vercel.json`. Las imágenes de `public/assets/` se cachean un año: si cambias
una, cambia también su nombre. CSS y JS se cachean un día: al cambiarlos, sube el `?v=` de `styles.css` y `main.js` en los HTML.

## Probar en local

```bash
python -m http.server 8765 -d public
```
