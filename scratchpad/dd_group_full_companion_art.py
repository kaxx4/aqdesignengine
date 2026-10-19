"""Companion art for the Disco Diwali "group 1 is full" poster ("Last Seat"). Out: out/discodiwali/launch/group_full_companion/last_seat.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/launch/group_full_companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, SEAT, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (176, 138, 54), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
cols, rows, sz, gap = 12, 14, 44, 18
gw, gh = cols * sz + (cols - 1) * gap, rows * sz + (rows - 1) * gap
x0, y0 = (1080 - gw) // 2, 250
last = (9, 8)                                                         # the marked last seat (col, row)
for r in range(rows):
    for c in range(cols):
        x, y = x0 + c * (sz + gap), y0 + r * (sz + gap)
        if (c, r) == last:
            d.rounded_rectangle([x * S, y * S, (x + sz) * S, (y + sz) * S], radius=8 * S, fill=OFF, outline=GOLD, width=3 * S)
        else:
            d.rounded_rectangle([x * S, y * S, (x + sz) * S, (y + sz) * S], radius=8 * S, fill=SEAT)
pad = 26
d.rectangle([(x0 - pad) * S, (y0 - pad) * S, (x0 + gw + pad) * S, (y0 + gh + pad) * S], outline=GOLD, width=2 * S)
d.text((x0 * S, 110 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((x0 * S, 152 * S), "LAST SEAT  /  EVERY SEAT TAKEN", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "last_seat.png"))
