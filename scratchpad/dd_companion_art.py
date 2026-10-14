"""Companion art piece for the Disco Diwali window carousel ("Stacked Light"). Output: out/discodiwali/carousel/window/companion/stacked_light.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/carousel/window/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD = (6, 6, 8), (236, 234, 226), (201, 151, 28)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
mono = ImageFont.truetype(fonts[0], 15 * S) if fonts else ImageFont.load_default()
big = ImageFont.truetype(fonts[-1], 26 * S) if fonts else ImageFont.load_default()
n, top, step, wtop, shrink = 18, 120 * S, 52 * S, 700 * S, 0.075
for i in range(n):
    y0 = top + i * step; h = 170 * S
    wb = wtop * (1 - shrink); cx = W // 2
    poly = [(cx - wtop / 2, y0), (cx + wtop / 2, y0), (cx + wb / 2, y0 + h), (cx - wb / 2, y0 + h)]
    d.polygon(poly, fill=INK)                       # occlude everything behind
    col = GOLD if i % 6 == 2 else OFF
    d.line(poly + [poly[0]], fill=col, width=2 * S if col == GOLD else S, joint="curve")
    d.line([(cx - wtop / 2, y0 + 30 * S), (cx + wtop / 2, y0 + 30 * S)], fill=col, width=S)      # the title bar rule
    d.text((70 * S, y0 + 6 * S), f"FIG. {i + 1:02d}", font=mono, fill=GOLD if col == GOLD else (130, 128, 122))
d.text((70 * S, 1244 * S), "DISCO DIWALI", font=big, fill=OFF)
d.text((70 * S, 1288 * S), "STACKED LIGHT  /  18 FRAMES, ONE INTERVAL", font=mono, fill=(130, 128, 122))
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "stacked_light.png")); img.save(os.path.join(OUT, "stacked_light.pdf"))
