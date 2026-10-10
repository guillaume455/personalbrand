#!/usr/bin/env python3
"""The five photos of the Porsche (June 2014), ready for the reel: upright, 1600 px max, EXIF and GPS removed, and
blurred where the brief forbids: the plates, and the garage signs (name, phone number, flag) that would identify the
seller of 2014. Boxes are in full-resolution pixels (3264 x 2448). Raw photos stay out of the repository (Drive)."""
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

RAW = "/tmp/claude-0/-home-user-personalbrand/a374c73f-4307-5632-a6b9-84584e511937/scratchpad/p997_raw"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BLUR = {
    "20140606_174128": [(200, 1380, 510, 1630, 40), (950, 0, 3264, 480, 60)],             # plate; signage over the door
    "20140606_174224": [(400, 1400, 660, 1640, 40), (1150, 0, 2330, 760, 60), (1000, 330, 1330, 430, 40)],
    "20140606_174216": [(0, 0, 300, 760, 60)],                                           # the dealer's flag
    "20140606_174140": [],
    "20140607_183242": [(1150, 790, 1330, 920, 25)],                                     # the far front plate
}
os.makedirs("assets/img", exist_ok=True)
for name, boxes in BLUR.items():
    im = ImageOps.exif_transpose(Image.open(f"{RAW}/{name}.jpg")).convert("RGB")
    for x0, y0, x1, y1, r in boxes:
        reg = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(r))
        m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *reg.size), radius=min(reg.size) // 4, fill=255)
        im.paste(reg, (x0, y0), m.filter(ImageFilter.GaussianBlur(8)))
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(f"assets/img/{name}.jpg", quality=90)          # no exif= : the EXIF (GPS included) is not written
    print(name, im.size)
