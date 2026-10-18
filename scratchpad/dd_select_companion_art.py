"""Companion art for the Disco Diwali selection carousel ("One Chosen Line"). Out: out/discodiwali/carousel/select/companion/one_chosen_line.png"""
import os, glob, random
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/carousel/select/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, CREAM, DIM = (6, 6, 9), (236, 234, 226), (229, 168, 0), (251, 241, 203), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
random.seed(18)
x0, pitch, n, y0 = 120, 62, 14, 260
chosen = 8
for i in range(n):
    y = y0 + i * pitch
    L = random.choice([420, 560, 680, 760, 840])
    if i == chosen:
        cl = 700
        d.rectangle([x0 * S, (y - 22) * S, (x0 + cl) * S, (y + 22) * S], fill=CREAM)
        d.line([x0 * S, (y - 22 - 40) * S, x0 * S, (y + 22) * S], fill=GOLD, width=4 * S)
        d.ellipse([(x0 - 18) * S, (y - 22 - 76) * S, (x0 + 18) * S, (y - 22 - 40) * S], fill=GOLD)
        d.line([(x0 + cl) * S, (y - 22) * S, (x0 + cl) * S, (y + 22 + 40) * S], fill=GOLD, width=4 * S)
        d.ellipse([(x0 + cl - 18) * S, (y + 22 + 40) * S, (x0 + cl + 18) * S, (y + 22 + 76) * S], fill=GOLD)
        d.line([(x0 + 24) * S, y * S, (x0 + cl - 24) * S, y * S], fill=(38, 35, 28), width=4 * S)
    elif abs(i - chosen) == 1:
        continue                                   # leave room for the handles
    else:
        d.line([x0 * S, y * S, (x0 + L) * S, y * S], fill=(70, 69, 66), width=3 * S)
d.text((x0 * S, 120 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((x0 * S, 162 * S), "ONE CHOSEN LINE  /  FOURTEEN, ONE SELECTED", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "one_chosen_line.png"))
