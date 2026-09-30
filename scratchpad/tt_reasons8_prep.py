"""Prepare the user's 2026-09-30 photo uploads for the 8-reasons carousel.
Source zips are NOT in the repo (people photos; public repo).
Usage: python scratchpad/tt_reasons8_prep.py <folder holding a/ and b/> [key=folder_of_photos ...]
  e.g. ... dd_tickets=/path/to/disco_diwali period_pain=/path/to/period_pain   (every image in the folder becomes one collage cell)
Writes engine/assets/terrathon/carousel_photos/<key>_<n>.jpg (git-ignored) + focus.json (object-position per file).
A reason with several photos becomes a COLLAGE inside its circle (tt_carousel.photo_list); cell order = file order:
2 photos = side by side, 3 = one tall + two stacked, 4 = 2x2. Order the files so the strongest, tallest photo is first."""
import glob, json, os, sys
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()
SRC = sys.argv[1]
OUT = "engine/assets/terrathon/carousel_photos"; os.makedirs(OUT, exist_ok=True)
for f in glob.glob(f"{OUT}/*"): os.remove(f)
# key -> [(file, focus "x% y%")]: focus is where the subject sits, so object-fit:cover keeps it in the circle
PLAN = {
    "crftd": [("a/crftd/09C4452D-47A0-4C17-9246-3895EDAFFCE6.jpg", "50% 66%"), ("a/crftd/IMG_6030.HEIC", "70% 70%")],
    "mini_fete": [("b/mini fete/WhatsApp Image 2026-09-30 at 10.59.25 PM.jpeg", "50% 55%"),
                  ("b/mini fete/WhatsApp Image 2026-09-30 at 10.59.23 PM.jpeg", "40% 75%"),
                  ("b/mini fete/WhatsApp Image 2026-09-30 at 10.59.27 PM.jpeg", "40% 75%")],
    "artily": [("a/artily/WhatsApp Image 2026-09-30 at 6.49.46 AM.jpeg", "50% 45%"),      # portrait popsicle drink: the tall cell
               ("a/artily/WhatsApp Image 2026-09-30 at 6.49.47 AM.jpeg", "49% 50%"),      # the branded ARTILY can
               ("a/artily/WhatsApp Image 2026-09-30 at 6.49.45 AM.jpeg", "32% 50%")],
    "cravella": [("a/cravella/IMG_20260703_202034_301.jpg.jpeg", "55% 60%"), ("a/cravella/20260929_151102.jpg.jpeg", "50% 30%")],
    "photobooth": [("a/photobooth/WhatsApp Image 2026-09-30 at 6.11.34 AM.jpeg", "50% 57%")],
    "lottery": [("b/lottery/48ce29902ce305ec8dfdead153469d9a.jpg", "50% 50%")],
}
for arg in sys.argv[2:]:                         # extra reasons whose photos arrive later: key=folder
    key, folder = arg.split("=", 1)
    PLAN[key] = [(p, "50% 50%") for p in sorted(glob.glob(os.path.join(folder, "*"))) if os.path.isfile(p)]
focus = {}
for key, items in PLAN.items():
    for n, (f, fc) in enumerate(items, 1):
        path = f if os.path.isabs(f) else os.path.join(SRC, f)
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        if max(im.size) > 1600: im.thumbnail((1600, 1600), Image.LANCZOS)
        name = f"{key}_{n}.jpg"; im.save(f"{OUT}/{name}", quality=90); focus[name] = fc; print(name, im.size)
json.dump(focus, open(f"{OUT}/focus.json", "w"), indent=1)
