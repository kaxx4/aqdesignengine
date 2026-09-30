"""Crop the user's 2026-09-30 photo uploads into square, subject-focused JPEGs for the 8-reasons carousel.
Source zips are NOT in the repo (people photos; public repo). Usage: python scratchpad/tt_reasons8_prep.py <folder holding a/ and b/>
Writes engine/assets/terrathon/carousel_photos/<key>.jpg (git-ignored). Crops are (file, cx, cy) in source fractions; the square is the full short side."""
import os, sys
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()
SRC = sys.argv[1]
OUT = "engine/assets/terrathon/carousel_photos"; os.makedirs(OUT, exist_ok=True)
CROPS = {
    "crftd":      ("a/crftd/09C4452D-47A0-4C17-9246-3895EDAFFCE6.jpg", .50, .66),
    "mini_fete":  ("b/mini fete/WhatsApp Image 2026-09-30 at 10.59.25 PM.jpeg", .50, .56),
    "artily":     ("a/artily/WhatsApp Image 2026-09-30 at 6.49.47 AM.jpeg", .49, .50),
    "cravella":   ("a/cravella/IMG_20260703_202034_301.jpg.jpeg", .50, .58),
    "photobooth": ("a/photobooth/WhatsApp Image 2026-09-30 at 6.11.34 AM.jpeg", .50, .57),
    "lottery":    ("b/lottery/48ce29902ce305ec8dfdead153469d9a.jpg", .50, .50),
}
for key, (f, cx, cy) in CROPS.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f))).convert("RGB")
    s = min(im.size); x0 = min(max(int(cx * im.width - s / 2), 0), im.width - s); y0 = min(max(int(cy * im.height - s / 2), 0), im.height - s)
    sq = im.crop((x0, y0, x0 + s, y0 + s))
    if s > 1400: sq = sq.resize((1400, 1400), Image.LANCZOS)
    sq.save(f"{OUT}/{key}.jpg", quality=90); print(key, im.size, "->", sq.size)
