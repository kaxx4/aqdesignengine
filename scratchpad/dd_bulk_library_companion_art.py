"""Companion art for bulk stories set 2 ("Two Rows"): set 1 above, set 2 below, colours sampled from the real story renders.
Out: out/discodiwali/bulk_library/companion/two_rows.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/bulk_library/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fw, fh, gap = 84, 150, 14
x0 = (1080 - (10 * fw + 9 * gap)) // 2
def mean(im): return tuple(int(v) for v in im.resize((1, 1), Image.LANCZOS).getpixel((0, 0)))
def row(folder, y, label):
    d.text((x0 * S, (y - 34) * S), label, font=small, fill=DIM)
    for n in range(10):
        st = Image.open(os.path.join(ROOT, "out/discodiwali", folder, f"story_{n + 1:02d}.png")).convert("RGB").resize((90, 160))
        top = tuple(int(c * .95) for c in mean(st.crop((0, 0, 90, 60)))); bot = tuple(int(c * .65) for c in mean(st.crop((0, 100, 90, 160))))
        x = x0 + n * (fw + gap)
        for i in range(fh * S):
            t = i / (fh * S)
            d.line([x * S, y * S + i, (x + fw) * S, y * S + i], fill=tuple(int(top[k] * (1 - t) + bot[k] * t) for k in range(3)))
        d.rounded_rectangle([(x + 8) * S, (y + 12) * S, (x + 30) * S, (y + 32) * S], radius=3 * S, outline=OFF, width=S)
        d.rounded_rectangle([(x + 18) * S, (y + 118) * S, (x + fw - 18) * S, (y + 132) * S], radius=3 * S, outline=GOLD, width=S)
        d.rectangle([x * S, y * S, (x + fw) * S, (y + fh) * S], outline=GOLD, width=2 * S)
row("bulk_hall", 480, "SET 01")
row("bulk_library", 790, "SET 02")
d.text((x0 * S, 130 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((x0 * S, 172 * S), "TWO ROWS  /  TWENTY NIGHTS, ONE STRUCTURE", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "two_rows.png"))
