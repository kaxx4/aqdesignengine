"""Companion art for the Disco Diwali bulk stories ("Constant Frame"). Frame colours are sampled from the ten real story renders.
Out: out/discodiwali/bulk_hall/companion/constant_frame.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BULK = os.path.join(ROOT, "out/discodiwali/bulk_hall"); OUT = os.path.join(BULK, "companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fw, fh, gap = 170, 302, 28
x0 = (1080 - (5 * fw + 4 * gap)) // 2; y0 = 340
def mean(im):
    return tuple(int(v) for v in im.resize((1, 1), Image.LANCZOS).getpixel((0, 0)))
for n in range(10):
    st = Image.open(os.path.join(BULK, f"story_{n + 1:02d}.png")).convert("RGB").resize((90, 160))
    top, bot = mean(st.crop((0, 0, 90, 60))), mean(st.crop((0, 100, 90, 160)))
    top, bot = tuple(int(c * .95) for c in top), tuple(int(c * .65) for c in bot)
    x = x0 + (n % 5) * (fw + gap); y = y0 + (n // 5) * (fh + 70)
    for i in range(fh * S):                                          # the sampled gradient: warm top, cooler floor
        t = i / (fh * S)
        d.line([x * S, y * S + i, (x + fw) * S, y * S + i], fill=tuple(int(top[k] * (1 - t) + bot[k] * t) for k in range(3)))
    # the constant skeleton: identical coordinates in every frame
    d.rounded_rectangle([(x + 12) * S, (y + 20) * S, (x + 56) * S, (y + 58) * S], radius=5 * S, outline=OFF, width=S)       # the badge
    d.arc([(x + 70) * S, (y + 14) * S, (x + fw - 12) * S, (y + 70) * S], 200, 340, fill=OFF, width=2 * S)                    # the mask
    for ly, lw in ((92, 140), (112, 96), (190, 120), (204, 86)):
        d.line([(x + 14) * S, (y + ly) * S, (x + 14 + lw) * S, (y + ly) * S], fill=OFF, width=2 * S)                        # title and status bars
    d.rounded_rectangle([(x + 40) * S, (y + 238) * S, (x + fw - 40) * S, (y + 268) * S], radius=6 * S, outline=GOLD, width=S)  # the pill
    d.rectangle([x * S, y * S, (x + fw) * S, (y + fh) * S], outline=GOLD, width=2 * S)
    d.text((x * S, (y + fh + 14) * S), f"NO. {n + 1:02d}", font=small, fill=DIM)
d.text((x0 * S, 100 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((x0 * S, 142 * S), "CONSTANT FRAME  /  ONE STRUCTURE, TEN LIGHTS", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "constant_frame.png"))
