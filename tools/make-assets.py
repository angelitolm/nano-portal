"""Genera los PNG de public/assets: favicon-32.png, apple-touch-icon.png (180) y og.png (1200x630).

Uso: python tools/make-assets.py   (necesita Pillow; usa Segoe UI si existe, si no la fuente por defecto)
El logo es el mismo que public/assets/favicon.svg: dos ojos cian (#5CE1FF, borde #1E5BFF) sobre un cuadrado oscuro.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "public" / "assets"
BG, TILE, EYE, RIM = (7, 11, 20), (11, 18, 34), (92, 225, 255), (30, 91, 255)
SS = 4  # supersampling para bordes suaves


def eyes(d, ox, oy, s):
    """Dibuja los dos ojos del logo (coordenadas del SVG de 1024) escalados por s y desplazados."""
    for x in (262, 572):
        d.rounded_rectangle([ox + x * s, oy + 386 * s, ox + (x + 190) * s, oy + 676 * s], radius=95 * s, fill=RIM)
        d.rounded_rectangle([ox + x * s, oy + 364 * s, ox + (x + 190) * s, oy + 654 * s], radius=95 * s, fill=EYE)


def icon(size, rounded=True):
    n = size * SS
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = n / 1024
    d.rounded_rectangle([0, 0, n - 1, n - 1], radius=(224 * s) if rounded else 0, fill=TILE)
    eyes(d, 0, 0, s)
    return im.resize((size, size), Image.LANCZOS)


def font(size, bold=False):
    for name in (["segoeuib.ttf"] if bold else []) + ["segoeui.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def glow(size, xy, radius, color, alpha):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([xy[0] - radius, xy[1] - radius, xy[0] + radius, xy[1] + radius], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius / 2.2))


def og():
    W, H = 1200, 630
    im = Image.new("RGBA", (W, H), BG + (255,))
    for xy, r, c, a in (((0, 0), 520, (59, 130, 246), 95), ((W, H), 520, (139, 92, 246), 85), ((0, H), 380, (16, 185, 129), 45)):
        im = Image.alpha_composite(im, glow((W, H), xy, r, c, a))

    # Ojos grandes a la derecha, con brillo cian.
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    s = 0.62 * SS
    ox, oy = 950 * SS - 512 * s, H * SS / 2 - 510 * s
    eyes(ImageDraw.Draw(big), ox, oy, s)
    big = big.resize((W, H), Image.LANCZOS)
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    halo.paste(EYE + (150,), mask=big.split()[3])
    im = Image.alpha_composite(im, halo.filter(ImageFilter.GaussianBlur(18)))
    im = Image.alpha_composite(im, big)

    d = ImageDraw.Draw(im)
    im.alpha_composite(icon(64), (72, 72))
    d.text((152, 104), "Nano", font=font(40, True), fill=(241, 245, 249), anchor="lm")
    d.text((72, 300), "Tu teléfono viejo,", font=font(64, True), fill=(241, 245, 249), anchor="ls")
    d.text((72, 378), "ahora tiene ojos.", font=font(64, True), fill=(167, 139, 250), anchor="ls")
    d.text((72, 452), "Mascota de escritorio + HUD de tu PC", font=font(30), fill=(148, 163, 184), anchor="ls")
    d.text((72, 560), "nano.angellm.dev", font=font(26), fill=(148, 163, 184), anchor="ls")
    im.convert("RGB").save(OUT / "og.png", optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    icon(32).save(OUT / "favicon-32.png", optimize=True)
    icon(180, rounded=False).convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)  # iOS redondea solo
    og()
    for p in sorted(OUT.glob("*.png")):
        with Image.open(p) as i:
            print(p.name, i.size, p.stat().st_size)
