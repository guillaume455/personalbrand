#!/usr/bin/env python3
"""Prepare Guillaume's photos (Drive, folder of the Mini) for the reel: EXIF orientation, max 1600 px, plates
blurred (boxes in relative coordinates x0, y0, x1, y1 measured on each photo). Usage: python3 prep-photos.py <raw dir>"""
import os, sys
from PIL import Image, ImageOps, ImageFilter

RAW = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/img")
PLATES = {
    "1.jpg": [(.10, .69, .25, .81)],
    "2.jpg": [(.70, .45, .89, .61)],
    "20170225_154834.jpg": [(.62, .31, .74, .42)],
    "20170225_160734.jpg": [(.36, .58, .60, .70)],
    "20170408_135132.jpg": [(.65, .68, .77, .79)],
    "20190228_165907.jpg": [(.55, .44, .69, .62)],
    "20190228_165935.jpg": [(.33, .72, .57, .85)],
    "snapchat.jpg": [(.64, .67, .91, .82)],
    "austin1.jpg": [], "austin2.jpg": [], "avant-plq.jpg": [], "avant-orl.jpg": [], "3.jpg": [], "4.jpg": [],
    "20190228_170039.jpg": [], "20190228_170102.jpg": [],
}
for f, boxes in PLATES.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(RAW, f))).convert("RGB")
    im.thumbnail((1600, 1600), Image.LANCZOS)
    w, h = im.size
    for x0, y0, x1, y1 in boxes:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(max(w, h) / 90)), b)
    im.save(os.path.join(OUT, f.replace(".jpg", ".jpg")), quality=90)
    print(f, im.size)
