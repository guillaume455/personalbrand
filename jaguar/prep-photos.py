#!/usr/bin/env python3
"""The photos of the Jaguar F-Type (dealer's studio series K08673), ready for the reel: 1600 px max, EXIF removed, and
blurred where the brief forbids. Checked by eye: no watermark, logo or company name on the photos kept; the plates are
already blank. Left out on purpose: 15 (the VIN plate), 25 and 26 (the navigation screen shows the dealer's town),
14, 24, 33 (boot, mirror, papers), and 65075185_...jpg, which is not a photo of the car but an insurance document.
Boxes in full-resolution pixels (1200 x 800). Raw photos stay out of the repository (Drive)."""
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

RAW = "/tmp/claude-0/-home-user-personalbrand/a374c73f-4307-5632-a6b9-84584e511937/scratchpad/jag_raw"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
KEEP = {
    1: [(505, 180, 565, 235, 10)],      # 3/4 front; the stock sticker on the windscreen
    3: [], 4: [],                       # rear 3/4, top down, rear lights
    7: [],                              # wheel
    11: [], 13: [(845, 140, 1025, 245, 14)],   # leather interior; the cockpit (the screen blurred)
    31: [],                             # gear selector
    32: [],                             # the dashboard: 139 891 km
}
os.makedirs("assets/img", exist_ok=True)
for n, boxes in KEEP.items():
    im = ImageOps.exif_transpose(Image.open(f"{RAW}/Jaguar-FTYPE-K08673-{n}.jpg")).convert("RGB")
    for x0, y0, x1, y1, r in boxes:
        reg = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(r))
        m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *reg.size), radius=min(reg.size) // 4, fill=255)
        im.paste(reg, (x0, y0), m.filter(ImageFilter.GaussianBlur(5)))
    im.save(f"assets/img/jag-{n:02d}.jpg", quality=92)
    print(n, im.size)
