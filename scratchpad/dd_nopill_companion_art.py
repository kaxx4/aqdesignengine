"""Companion art for the Disco Diwali no-pill poster ("Held Open"). Out: out/discodiwali/launch/companion/held_open.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/launch/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fx, fy, fw, fh = 270, 330, 540, 675                                             # a 4:5 poster frame, centred
d.rectangle([fx * S, fy * S, (fx + fw) * S, (fy + fh) * S], outline=OFF, width=S)
d.rounded_rectangle([(fx + 28) * S, (fy + 30) * S, (fx + 120) * S, (fy + 108) * S], radius=8 * S, outline=OFF, width=S)       # the badge
d.arc([(fx + 230) * S, (fy + 24) * S, (fx + fw - 28) * S, (fy + 150) * S], 200, 340, fill=OFF, width=2 * S)                    # the mask
for ly, lw in ((250, 440), (292, 330), (420, 290), (448, 200)):                                                             # title, edition, status, note
    d.line([(fx + 40) * S, (fy + ly) * S, (fx + 40 + lw) * S, (fy + ly) * S], fill=OFF, width=2 * S)
px0, py0, px1, py1 = fx + 120, fy + 530, fx + fw - 120, fy + 590                                                           # where the pill was
def dashed(x0, y0, x1, y1, dash=10, gap=7):
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        L = abs(bx - ax) + abs(by - ay); n = int(L // (dash + gap)) + 1
        for i in range(n):
            t0, t1 = i * (dash + gap) / L, min(1, (i * (dash + gap) + dash) / L)
            d.line([(ax + (bx - ax) * t0) * S, (ay + (by - ay) * t0) * S, (ax + (bx - ax) * t1) * S, (ay + (by - ay) * t1) * S], fill=GOLD, width=2 * S)
dashed(px0, py0, px1, py1)
d.line([px1 * S, ((py0 + py1) / 2) * S, (fx + fw + 70) * S, ((py0 + py1) / 2) * S], fill=GOLD, width=S)                        # hairline to the legend
d.text(((fx + fw + 82) * S, ((py0 + py1) / 2 - 8) * S), "HELD OPEN", font=small, fill=GOLD)
d.text((fx * S, 100 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((fx * S, 142 * S), "HELD OPEN  /  ONE ELEMENT WITHDRAWN", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "held_open.png"))
