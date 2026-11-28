"""Extract the reusable NON-PHOTO assets from the user's sponsors_cold PDF (every page is one flattened 1920x1080 image) into the git-ignored
engine/assets/sponsorship/starry/: 30 past-sponsor logo tiles, 5 testimonial logo pills, 7 past-event flyers, 2 'your logo here' mock-ups.
Photos are deliberately NOT extracted: the Starry Night deck keeps every photo slot blank (user, 2026-11-22). Coordinates are in the 2000px-wide
space the pages are displayed in; the factor .96 maps them to the 1920px page raster.  Run: python scratchpad/starry_deck_assets.py <pages_dir>"""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]; OUT = os.path.join(ROOT, "engine", "assets", "sponsorship", "starry"); os.makedirs(OUT, exist_ok=True)
F = .96
def crop(page, x0, y0, x1, y1, name, inset=3):
    im = Image.open(os.path.join(SRC, f"p-{page:02d}.jpg")).convert("RGB")
    box = (round(x0 * F) + inset, round(y0 * F) + inset, round(x1 * F) - inset, round(y1 * F) - inset)
    im.crop(box).save(os.path.join(OUT, name + ".png")); return box
cx = [100, 404, 706, 1009, 1312, 1615]; cy = [236, 400, 563, 727, 892]
n = 0
for r in cy:
    for c in cx:
        n += 1; crop(17, c, r, c + 286, r + 146, f"logo_{n:02d}")
for name, b in {"q_redbull": (154, 926, 263, 988), "q_realmark": (778, 531, 955, 593), "q_leveraged": (1368, 531, 1534, 593), "q_friends": (778, 944, 910, 1006), "q_subway": (1368, 944, 1442, 1006)}.items():
    crop(18, *b, name, inset=2)
tiles = [100, 361, 621, 881, 1141, 1402, 1662]; fy = (740, 1038)
for name, i in {"flyer_dd24": 0, "flyer_sn24": 1, "flyer_paradox": 2, "flyer_punjabi": 3, "flyer_sn25": 5, "flyer_summer": 6}.items():
    crop(11, tiles[i], fy[0], tiles[i] + 240, fy[1], name)
crop(12, 100, 302, 680, 946, "flyer_dd24_big"); crop(13, 100, 323, 517, 844, "flyer_sn24_big"); crop(13, 1021, 323, 1438, 844, "flyer_sn25_big")
crop(28, 1340, 253, 1605, 649, "mock_standee"); crop(28, 1245, 710, 1710, 1020, "mock_card")
print(len(os.listdir(OUT)), "assets ->", OUT)
