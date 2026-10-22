"""Companion art for bulk stories set 4 ("Early Bird"): ten ticket stubs in a row, each coloured from the mean of its real story render
(top sky, bottom shade), a perforation notch on both sides and a gold rule where the price line sits. Out: out/discodiwali/bulk_info/companion/early_bird.png"""
import os, glob
SOLD = os.environ.get("VARIANT") == "soldout"; D = "bulk_soldout" if SOLD else "bulk_info"   # VARIANT=soldout renders the "Sold Out" strip
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, f"out/discodiwali/{D}/companion"); os.makedirs(OUT, exist_ok=True)
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); big = ImageFont.truetype(fonts[-1], 64 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fw, fh, gap = 84, 300, 14
x0 = (1080 - (10 * fw + 9 * gap)) // 2; y = 520
def mean(im): return tuple(int(v) for v in im.resize((1, 1), Image.LANCZOS).getpixel((0, 0)))
d.text((x0 * S, 330 * S), "SOLD OUT" if SOLD else "EARLY BIRD", font=big, fill=OFF)
d.text((x0 * S, (y - 34) * S), "EARLY BIRD: GONE" if SOLD else "TEN STORIES, TEN PHOTOS, ONE PRICE LINE", font=small, fill=DIM)
for n in range(10):
    st = Image.open(os.path.join(ROOT, "out/discodiwali", D, f"story_{n + 1:02d}.png")).convert("RGB").resize((90, 160))
    top = tuple(int(c * .95) for c in mean(st.crop((0, 0, 90, 60)))); bot = tuple(int(c * .6) for c in mean(st.crop((0, 100, 90, 160))))
    x = x0 + n * (fw + gap)
    for i in range(fh * S):
        t = i / (fh * S)
        d.line([x * S, y * S + i, (x + fw) * S, y * S + i], fill=tuple(int(top[k] * (1 - t) + bot[k] * t) for k in range(3)))
    for yy in (y + 190, ):
        d.ellipse([(x - 7) * S, (yy - 7) * S, (x + 7) * S, (yy + 7) * S], fill=INK); d.ellipse([(x + fw - 7) * S, (yy - 7) * S, (x + fw + 7) * S, (yy + 7) * S], fill=INK)
        d.line([(x + 10) * S, yy * S, (x + fw - 10) * S, yy * S], fill=GOLD, width=S)
img.save(os.path.join(OUT, "sold_out.png" if SOLD else "early_bird.png")); print("companion ->", OUT)
