"""Companion art for bulk stories set 3 ("Edge of the Frame"): ten slits over one wide band, colours sampled from the real renders.
Out: out/discodiwali/bulk_crops/companion/edge_of_the_frame.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/bulk_crops/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
def mean(im): return tuple(int(v) for v in im.resize((1, 1), Image.LANCZOS).getpixel((0, 0)))
cols = []
for n in range(10):
    st = Image.open(os.path.join(ROOT, "out/discodiwali/bulk_crops", f"story_{n + 1:02d}.png")).convert("RGB").resize((90, 160))
    cols.append((tuple(int(c * .95) for c in mean(st.crop((0, 0, 90, 60)))), tuple(int(c * .65) for c in mean(st.crop((0, 100, 90, 160))))))
bx0, bx1, by, bh = 80, 1000, 560, 300                                    # the wide band: the one scene
for x in range(bx0 * S, bx1 * S):
    t = (x - bx0 * S) / ((bx1 - bx0) * S); i = min(9, int(t * 10)); a, b = cols[i], cols[min(9, i + 1)]; f = t * 10 - i
    c = tuple(int((a[0][k] * (1 - f) + b[0][k] * f) * .55) for k in range(3))
    d.line([x, by * S, x, (by + bh) * S], fill=c)
d.rectangle([bx0 * S, by * S, bx1 * S, (by + bh) * S], outline=(90, 88, 82), width=S)
pos = [.06, .13, .24, .34, .47, .55, .64, .78, .86, .94]                  # uneven stations along the band
sw, sh, sy = 56, 190, 880
for n, (p, (top, bot)) in enumerate(zip(pos, cols)):
    cx = bx0 + p * (bx1 - bx0)
    x0 = cx - sw / 2
    d.line([cx * S, (by + bh) * S, cx * S, sy * S], fill=GOLD, width=S)
    for i in range(sh * S):
        t = i / (sh * S)
        d.line([x0 * S, sy * S + i, (x0 + sw) * S, sy * S + i], fill=tuple(int(top[k] * (1 - t) + bot[k] * t) for k in range(3)))
    d.rectangle([x0 * S, sy * S, (x0 + sw) * S, (sy + sh) * S], outline=GOLD, width=2 * S)
    d.text((x0 * S, (sy + sh + 12) * S), f"{n + 1:02d}", font=small, fill=DIM)
d.text((bx0 * S, 130 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((bx0 * S, 172 * S), "EDGE OF THE FRAME  /  ONE SCENE, TEN STATIONS", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "edge_of_the_frame.png"))
