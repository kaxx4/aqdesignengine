"""Companion art for the Disco Diwali callout-frames carousel ("Held Frames"). Out: out/discodiwali/carousel/callout/companion/held_frames.png"""
import os, glob, random, math
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/carousel/callout/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD = (6, 6, 9), (236, 234, 226), (232, 192, 99)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 15 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
# frames: (x, y, w, h, bracket x, bracket y, tint)
frames = [(80, 150, 300, 220, 590, 560, (40, 20, 110)), (690, 260, 310, 400, 470, 820, (110, 20, 70)), (80, 880, 330, 250, 650, 1010, (10, 70, 120))]
keep = [(x - 14, y - 14, x + w + 14, y + h + 40) for x, y, w, h, *_ in frames] + [(60, 1195, 640, 1295)]
random.seed(27)
pitch = 30
for gy in range(40, 1350 - 30, pitch):
    for gx in range(40, 1080 - 30, pitch):
        x, y = gx + random.uniform(-5, 5), gy + random.uniform(-5, 5)
        if any(a <= x <= c and b <= y <= e for a, b, c, e in keep):
            continue
        w = (math.sin(x / 150) + math.cos(y / 190) + 2) / 4                 # a slow swell: the crowd breathes
        r = 0.8 + 2.6 * w * random.random()
        v = int(40 + 90 * w)
        d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=(v, v, v + 8))
def bracket(cx, cy, size=46, arm=13):
    x0, y0, x1, y1 = cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=INK)
    for px, py, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(px + dx * arm) * S, py * S, px * S, py * S, px * S, (py + dy * arm) * S], fill=GOLD, width=3 * S, joint="curve")
for n, (x, y, w, h, bx, by, tint) in enumerate(frames, 1):
    mids = [(x + w / 2, y), (x + w / 2, y + h), (x, y + h / 2), (x + w, y + h / 2)]
    sx, sy = min(mids, key=lambda m: (m[0] - bx) ** 2 + (m[1] - by) ** 2)
    d.line([sx * S, sy * S, bx * S, by * S], fill=GOLD, width=2 * S)
    bracket(bx, by)
    for i in range(h * S):                                                    # a vertical gradient: a bright window, not a flat swatch
        t = i / (h * S)
        c = tuple(int(tint[k] * (1.15 - .6 * t) + 25 * (1 - t)) for k in range(3))
        d.line([x * S, y * S + i, (x + w) * S, y * S + i], fill=c)
    d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], outline=GOLD, width=3 * S)
    d.text((x * S, (y + h + 10) * S), f"FIG. {n:02d}", font=small, fill=(150, 148, 140))
d.text((72 * S, 1218 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((72 * S, 1256 * S), "HELD FRAMES  /  3 WINDOWS, 3 MARKS", font=small, fill=(150, 148, 140))
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "held_frames.png"))
