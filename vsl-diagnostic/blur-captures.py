#!/usr/bin/env python3
"""Anonymise the listing screenshots: blur the dealer names, logos, plates and the leboncoin account name.
Sources: the raw screenshots sent by Guillaume (not versioned). Output: assets/img/*.png
Usage: python3 blur-captures.py <folder of raw screenshots>"""
import sys
from PIL import Image, ImageFilter, ImageDraw

SRC = sys.argv[1]
JOBS = {
    "1.webp": ("annonce-audi.png", [
        (1785, 12, 1935, 98),      # compte leboncoin (avatar + pseudo)
        (1375, 370, 1475, 495),    # logo du garage
        (1488, 345, 1705, 395),    # nom du garage
        (895, 525, 1070, 575),     # plaque, photo du haut
        (80, 690, 165, 790),       # plaque, grande photo
        (1170, 830, 1250, 890),    # plaque, photo du bas
    ]),
    "3.webp": ("annonce-ford.png", [
        (1375, 110, 1495, 215),    # logo du garage
        (1500, 62, 1695, 112),     # nom du garage
        (900, 300, 1070, 355),     # plaque arrière
        (684, 640, 785, 695),      # plaque, photo du bas
        (90, 300, 150, 350),       # plaque avant
    ]),
    "2.webp": ("lacentrale-accueil.png", []),
    "4.webp": ("portrait.png", []),
    "5.webp": ("bandeau-signature.png", []),
}
for src, (dst, boxes) in JOBS.items():
    img = Image.open(f"{SRC}/{src}").convert("RGBA")
    for box in boxes:
        region = img.crop(box).filter(ImageFilter.GaussianBlur(14)).filter(ImageFilter.GaussianBlur(14))
        mask = Image.new("L", region.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, *region.size), radius=12, fill=255)
        img.paste(region, box[:2], mask)
    img.save(f"assets/img/{dst}")
    print(dst, img.size, len(boxes), "zone(s) floutée(s)")
