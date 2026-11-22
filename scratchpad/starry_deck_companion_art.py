"""Companion art, plate 04 of 'Faceted Light' (philosophy: sample_outputs/disco_diwali_thanks_exposure/companion_philosophy.md): thirty-six small mirror-balls, one per slide of the
Starry Night deck, all lit from one source; the single red facet-ball is slide 09, the slide that was rebuilt around a new event. Run: python scratchpad/starry_deck_companion_art.py"""
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
    t = max(0, min(1, t)); a, b = ((EMBER, (150, 98, 48)) if t < .5 else ((150, 98, 48), (250, 236, 190))); u = t * 2 if t < .5 else (t - .5) * 2
    return tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
def sphere(cx, cy, R, rows, tint, red=False):
    for r in range(rows):
        lat0 = -math.pi / 2 + math.pi * r / rows; lat1 = lat0 + math.pi / rows; latm = (lat0 + lat1) / 2
        n = max(8, round(2 * rows * math.cos(latm)))
        for c in range(n):
            lon = -math.pi + 2 * math.pi * (c + .5) / n
            x, y, z = math.cos(latm) * math.sin(lon), math.sin(latm), math.cos(latm) * math.cos(lon)
            if z < 0: continue
            lit = max(0, (x * -.55 + y * -.6) / math.hypot(.55, .6)) * .55 + z * .45
            col = RED if (red and (r + c) % 3 == 0) else ladder(lit ** .85 * tint)
            wdt = 2 * math.pi * R * math.cos(latm) / n * .86 * max(z, .22); hgt = R * (math.sin(lat1) - math.sin(lat0)) * .86
            px, py = cx + R * x, cy + R * y
            d.rounded_rectangle([px - wdt / 2, py - hgt / 2, px + wdt / 2, py + hgt / 2], radius=min(wdt, hgt) * .14, fill=col)
M = 150 * S; cols = 6; cell = (W - 2 * M) / cols; top = 400 * S; R = 118 * S
for i in range(36):
    r_, c_ = divmod(i, cols); cx = M + cell * (c_ + .5); cy = top + cell * (r_ + .5)
    sphere(cx, cy, R, 12, 1.0 - .04 * abs(i - 8) / 8 * 3, red=(i == 8))
    t = f"{i + 1:02d}"; d.text((cx - d.textlength(t, font=mono(18)) / 2, cy + R + 26 * S), t, font=mono(18), fill=DIM)
d.text((M, M), "PLATE 04", font=mono(24), fill=DIM)
t = "THIRTY-SIX SLIDES, ONE LIGHT"; d.text((W - M - d.textlength(t, font=mono(24)), M), t, font=mono(24), fill=DIM)
d.line([M, M + 60 * S, W - M, M + 60 * S], fill=(48, 48, 52), width=S)
p = "an outline, before the pictures"; d.text(((W - d.textlength(p, font=serif)) / 2, 2650 * S), p, font=serif, fill=(236, 228, 206))
d.line([M, H - M - 60 * S, W - M, H - M - 60 * S], fill=(48, 48, 52), width=S)
d.text((M, H - M - 30 * S), "4 / 4", font=mono(20), fill=DIM)
out = os.path.join(ROOT, "sample_outputs", "starry_night_deck", "companion_faceted_light_04.png")
img.resize((W // S, H // S), Image.LANCZOS).save(out); print(out)
