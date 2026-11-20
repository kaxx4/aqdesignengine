"""Companion art for the Exposure thank-you poster: 'Faceted Light'. Run: python scratchpad/dd_thanks_companion_art.py"""
import glob, math, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.dirname(glob.glob("/root/.claude/skills/synced/*/canvas-design/canvas-fonts/DMMono-Regular.ttf")[0])
S = 2; W, H = 2400 * S, 3000 * S
img = Image.new("RGB", (W, H), (7, 8, 14)); d = ImageDraw.Draw(img)
mono = lambda n: ImageFont.truetype(f"{FD}/DMMono-Regular.ttf", n * S)
serif = ImageFont.truetype(f"{FD}/InstrumentSerif-Italic.ttf", 64 * S)
GOLD = (233, 196, 106); EMBER = (74, 38, 22); DIM = (120, 116, 108); RED = (232, 38, 42)
cx, cy, R = W // 2, 1260 * S, 800 * S
LX, LY = -0.55, -0.6                                # light direction (upper left)
def ladder(t):                                       # 0..1 -> ember..pale gold
    t = max(0, min(1, t)); a = EMBER if t < .5 else (150, 98, 48); b = (150, 98, 48) if t < .5 else (250, 236, 190)
    u = t * 2 if t < .5 else (t - .5) * 2
    return tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
rows, red_cell = 30, (11, 21)
for r in range(rows):
    lat0 = -math.pi / 2 + math.pi * r / rows; lat1 = lat0 + math.pi / rows
    latm = (lat0 + lat1) / 2; n = max(8, round(2 * rows * math.cos(latm)))
    for c in range(n):
        lon = -math.pi + 2 * math.pi * (c + .5) / n
        x, y, z = math.cos(latm) * math.sin(lon), math.sin(latm), math.cos(latm) * math.cos(lon)
        if z < 0: continue                           # front hemisphere only
        px, py = cx + R * x, cy + R * y
        lit = max(0, (x * LX + y * LY) / math.hypot(LX, LY)) * .55 + z * .45
        col = RED if (r, c) == (red_cell[0], red_cell[1] * n // 42) else ladder(lit ** .85)
        wdt = 2 * math.pi * R * math.cos(latm) / n * .86 * max(z, .22)
        hgt = R * (math.sin(lat1) - math.sin(lat0)) * .86
        d.rounded_rectangle([px - wdt / 2, py - hgt / 2, px + wdt / 2, py + hgt / 2], radius=min(wdt, hgt) * .14, fill=col)
# lens-barrel rings
for rad, w in ((R + 70 * S, 2), (R + 190 * S, 2)):
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(70, 68, 66), width=w)
for k in range(180):
    a = math.radians(k * 2 - 90); long = k % 5 == 0
    r0, r1 = R + 70 * S, R + (70 + (34 if long else 16)) * S
    d.line([cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)], fill=(110, 106, 98), width=2 * S if long else S)
stops = ["f/1.4", "f/2", "f/2.8", "f/4", "f/5.6", "f/8", "f/11", "f/16"]
for i, s in enumerate(stops):                       # stepped values on the outer ring, upper arc
    a = math.radians(-160 + i * (140 / 7) * 1.0) ; a = math.radians(-200 + i * 20)
    rr = R + 190 * S; px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
    d.ellipse([px - 7 * S, py - 7 * S, px + 7 * S, py + 7 * S], fill=ladder(1 - i / 7))
    tw = d.textlength(s, font=mono(20)); tx = cx + (rr + 50 * S) * math.cos(a); ty = cy + (rr + 50 * S) * math.sin(a)
    d.text((tx - tw / 2, ty - 10 * S), s, font=mono(20), fill=DIM)
M = 150 * S
d.text((M, M), "PLATE 01", font=mono(24), fill=DIM)
d.text((W - M - d.textlength("EXPOSURE, IN STOPS", font=mono(24)), M), "EXPOSURE, IN STOPS", font=mono(24), fill=DIM)
d.line([M, M + 60 * S, W - M, M + 60 * S], fill=(48, 48, 52), width=S)
phrase = "with thanks, in every facet"
d.text(((W - d.textlength(phrase, font=serif)) / 2, 2560 * S), phrase, font=serif, fill=(236, 228, 206))
d.line([M, H - M - 60 * S, W - M, H - M - 60 * S], fill=(48, 48, 52), width=S)
d.text((M, H - M - 30 * S), "1 / 1", font=mono(20), fill=DIM)
out = os.path.join(ROOT, "sample_outputs", "disco_diwali_thanks_exposure", "companion_faceted_light.png")
img.resize((W // S, H // S), Image.LANCZOS).save(out); print(out)
