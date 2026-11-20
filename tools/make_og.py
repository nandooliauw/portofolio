#!/usr/bin/env python3
"""Generate the 1200x630 social preview card (assets/og.png).

Text is fixed content for this site, not scraped data, so the script is the
single source: edit the strings here and re-run.

    python tools/make_og.py
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 15, 20)
PANEL = (17, 24, 35)
LINE = (30, 42, 58)
TEXT = (219, 230, 243)
DIM = (143, 161, 184)
ACCENT = (74, 168, 255)

MONO = [r"C:\Windows\Fonts\consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
SANS = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\Arial Bold.ttf"]
SANS_REG = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\Arial.ttf"]


def font(paths, size):
    for path in paths:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> int:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    # subtle grid of dots, same family as the site's panels
    for x in range(40, W, 40):
        for y in range(40, H, 40):
            draw.point((x, y), fill=(23, 31, 42))

    draw.rounded_rectangle([(36, 36), (W - 36, H - 36)], radius=18, outline=LINE, width=2)
    draw.rectangle([(36, 36), (44, H - 36)], fill=ACCENT)

    draw.text((86, 96), "FERNANDO ISKANDAR", font=font(MONO, 20), fill=DIM)
    draw.text((86, 150), "Frontend engineer", font=font(SANS, 58), fill=TEXT)
    draw.text((86, 220), "& security tooling", font=font(SANS, 58), fill=ACCENT)

    draw.text(
        (86, 320),
        "4+ years building product interfaces and the internal tools",
        font=font(SANS_REG, 26),
        fill=DIM,
    )
    draw.text(
        (86, 358),
        "that check them. Open-source Python: headerhawk, loghawk.",
        font=font(SANS_REG, 26),
        fill=DIM,
    )

    for index, label in enumerate(("github.com/nandoofr298", "linkedin.com/in/nandooliauw", "Bekasi, Indonesia")):
        x = 86 + index * 340
        draw.rounded_rectangle([(x, 452), (x + 8, 460)], radius=2, fill=ACCENT)
        draw.text((x + 18, 448), label, font=font(MONO, 17), fill=DIM)

    os.makedirs("assets", exist_ok=True)
    image.save("assets/og.png", "PNG", optimize=True)
    print(f"wrote assets/og.png ({image.width}x{image.height}, {os.path.getsize('assets/og.png')} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
