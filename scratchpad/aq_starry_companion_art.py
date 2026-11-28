"""Companion art, plate 03 of 'Faceted Light' (philosophy: sample_outputs/disco_diwali_thanks_exposure/companion_philosophy.md). A star chart: a grid of points whose
brightness is set by distance from one light, one red exception. Run: python scratchpad/aq_starry_companion_art.py"""
import glob, math, os, random
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.dirname(glob.glob("/root/.claude/skills/synced/*/canvas-design/canvas-fonts/DMMono-Regular.ttf")[0])
S = 2; W, H = 2400 * S, 3000 * S
img = Image.new("RGB", (W, H), (7, 8, 14)); d = ImageDraw.Draw(img)
mono = lambda n: ImageFont.truetype(f"{FD}/DMMono-Regular.ttf", n * S)
serif = ImageFont.truetype(f"{FD}/InstrumentSerif-Italic.ttf", 64 * S)
DIM = (120, 116, 108); RED = (232, 38, 42)
def ladder(t):
    t = max(0, min(1, t)); a, b = ((74, 38, 22), (150, 98, 48)) if t < .5 else ((150, 98, 48), (250, 236, 190)); u = t * 2 if t < .5 else (t - .5) * 2
    return tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
M = 150 * S
x0, x1, y0, y1 = M, W - M, 330 * S, 2480 * S
cols, rows = 24, 31
sx, sy = (x1 - x0) / (cols - 1), (y1 - y0) / (rows - 1)
lx, ly = x0 + (x1 - x0) * .72, y0 + (y1 - y0) * .22          # the one light
maxd = math.hypot(x1 - x0, y1 - y0)
rnd = random.Random(11)
ring = Image.new("RGB", (W, H), (7, 8, 14)); rd = ImageDraw.Draw(ring)       # contour rings around the light, CLIPPED to the chart area
for k in (1, 2, 3, 4):
    rr = k * 330 * S; rd.ellipse([lx - rr, ly - rr, lx + rr, ly + rr], outline=(52, 52, 58), width=S)
box = (int(x0 - 30 * S), int(y0 - 30 * S), int(x1 + 30 * S), int(y1 + 30 * S)); img.paste(ring.crop(box), box[:2])
for r in range(rows):
    for c in range(cols):
        x, y = x0 + c * sx, y0 + r * sy
        dist = math.hypot(x - lx, y - ly) / maxd
        t = 1 - dist * 1.35
        size = (5 + 15 * max(t, 0) ** 1.4) * S
        col = RED if (r, c) == (19, 6) else ladder(t)
        if (r, c) == (19, 6): size = 15 * S
        # a four-point star, drawn as a rotated square pair, identical shape everywhere (only size and colour carry the data)
        d.polygon([(x, y - size), (x + size * .28, y - size * .28), (x + size, y), (x + size * .28, y + size * .28), (x, y + size), (x - size * .28, y + size * .28), (x - size, y), (x - size * .28, y - size * .28)], fill=col)
d.text((M, M), "PLATE 03", font=mono(24), fill=DIM)
t = "STAR CHART, ONE LIGHT"; d.text((W - M - d.textlength(t, font=mono(24)), M), t, font=mono(24), fill=DIM)
d.line([M, M + 60 * S, W - M, M + 60 * S], fill=(48, 48, 52), width=S)
p = "for the ones who run the night"; d.text(((W - d.textlength(p, font=serif)) / 2, 2600 * S), p, font=serif, fill=(236, 228, 206))
d.line([M, H - M - 60 * S, W - M, H - M - 60 * S], fill=(48, 48, 52), width=S)
d.text((M, H - M - 30 * S), "3 / 3", font=mono(20), fill=DIM)
out = os.path.join(ROOT, "sample_outputs", "aq_starry_recruit", "companion_faceted_light_03.png")
img.resize((W // S, H // S), Image.LANCZOS).save(out); print(out)
