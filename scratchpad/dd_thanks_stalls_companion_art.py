"""Companion art for the stalls thank-you poster: 'Faceted Light', plate 02, five spheres, one per stall, each lit from the same source. Reuses the philosophy in
sample_outputs/disco_diwali_thanks_exposure/companion_philosophy.md. Run: python scratchpad/dd_thanks_stalls_companion_art.py"""
import glob, math, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.dirname(glob.glob("/root/.claude/skills/synced/*/canvas-design/canvas-fonts/DMMono-Regular.ttf")[0])
S = 2; W, H = 2400 * S, 3000 * S
img = Image.new("RGB", (W, H), (7, 8, 14)); d = ImageDraw.Draw(img)
mono = lambda n: ImageFont.truetype(f"{FD}/DMMono-Regular.ttf", n * S)
serif = ImageFont.truetype(f"{FD}/InstrumentSerif-Italic.ttf", 64 * S)
EMBER = (74, 38, 22); DIM = (120, 116, 108); RED = (232, 38, 42)
def ladder(t):
    t = max(0, min(1, t)); a = EMBER if t < .5 else (150, 98, 48); b = (150, 98, 48) if t < .5 else (250, 236, 190)
    u = t * 2 if t < .5 else (t - .5) * 2
    return tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
def sphere(cx, cy, R, rows, red=None):
    for r in range(rows):
        lat0 = -math.pi / 2 + math.pi * r / rows; lat1 = lat0 + math.pi / rows; latm = (lat0 + lat1) / 2
        n = max(8, round(2 * rows * math.cos(latm)))
        for c in range(n):
            lon = -math.pi + 2 * math.pi * (c + .5) / n
            x, y, z = math.cos(latm) * math.sin(lon), math.sin(latm), math.cos(latm) * math.cos(lon)
            if z < 0: continue
            lit = max(0, (x * -.55 + y * -.6) / math.hypot(.55, .6)) * .55 + z * .45
            col = RED if red == (r, c * 42 // n) else ladder(lit ** .85)
            wdt = 2 * math.pi * R * math.cos(latm) / n * .86 * max(z, .22); hgt = R * (math.sin(lat1) - math.sin(lat0)) * .86
            px, py = cx + R * x, cy + R * y
            d.rounded_rectangle([px - wdt / 2, py - hgt / 2, px + wdt / 2, py + hgt / 2], radius=min(wdt, hgt) * .14, fill=col)
R = 270 * S
spots = [(640, 640), (1760, 900), (640, 1470), (1760, 1730), (1200, 2200)]   # a loose zigzag, centred
red = {0: None, 1: None, 2: (7, 15), 3: None, 4: None}
for i, (x, y) in enumerate(spots):
    sphere(x * S, y * S, R, 16, red[i])
    rr = R + 36 * S; d.ellipse([x * S - rr, y * S - rr, x * S + rr, y * S + rr], outline=(70, 68, 66), width=2)
    d.text((x * S - 40 * S, y * S + rr + 24 * S), f"STALL 0{i + 1}", font=mono(20), fill=DIM)
M = 150 * S
d.text((M, M), "PLATE 02", font=mono(24), fill=DIM)
t = "FIVE STALLS, ONE LIGHT"; d.text((W - M - d.textlength(t, font=mono(24)), M), t, font=mono(24), fill=DIM)
d.line([M, M + 60 * S, W - M, M + 60 * S], fill=(48, 48, 52), width=S)
d.line([M, H - M - 60 * S, W - M, H - M - 60 * S], fill=(48, 48, 52), width=S)
d.text((M, H - M - 30 * S), "2 / 2", font=mono(20), fill=DIM)
p = "every one of you, lit"; d.text(((W - d.textlength(p, font=serif)) / 2, H - M - 190 * S), p, font=serif, fill=(236, 228, 206))
out = os.path.join(ROOT, "sample_outputs", "disco_diwali_thanks_stalls", "companion_faceted_light_02.png")
img.resize((W // S, H // S), Image.LANCZOS).save(out); print(out)
