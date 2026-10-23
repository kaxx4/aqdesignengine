"""Companion art for the Gen Z carousel: seven strata of identical rings, one hue each.
Subtle reference: seven countries, one generation, different rhythms that briefly align."""
import math, glob
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample, then downscale
W, H = 1600 * S, 2000 * S
CREAM, INK = (244, 239, 224), (10, 10, 10)
HUES = ["#FF4D2E", "#3DA9FC", "#FFC700", "#FF4D8C", "#7E5BFF", "#1B8A5A", "#0E7C86"]
LABELS = ["I", "II", "III", "IV", "V", "VI", "VII"]
mono = glob.glob("/root/.claude/skills/synced/*/canvas-design/canvas-fonts/DMMono-Regular.ttf")[0]
F = ImageFont.truetype(mono, 17 * S)


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
ML, MR, MT, MB = 200 * S, 160 * S, 220 * S, 260 * S
cols, rows = 46, 7
strata_h = (H - MT - MB) / rows
gap = 28 * S
cw = (W - ML - MR) / cols
r = cw * 0.30

for k in range(rows):
    top = MT + k * strata_h
    base = top + strata_h - gap
    d.line([(ML, base), (W - MR, base)], fill=INK, width=2 * S)
    for c in range(cols):
        x = ML + c * cw + cw / 2
        t = c / (cols - 1)
        phase = math.sin(t * math.pi * (2.2 + 0.45 * k) + k * 0.9) * (1 - t)
        conv = math.exp(-((t - 0.78) / 0.09) ** 2)
        level = 0.46 + 0.34 * phase * (1 - conv) + 0.31 * conv
        n = max(1, int(level * (strata_h - gap) / (cw * 0.9)))
        for j in range(n):
            y = base - r - 4 * S - j * cw * 0.9
            d.ellipse([x - r, y - r, x + r, y + r], outline=INK, width=2 * S, fill=rgb(HUES[k]))
    d.text((ML - 70 * S, base - 22 * S), LABELS[k], font=F, fill=INK)

xa = ML + 0.78 * (W - ML - MR)
d.line([(xa, MT - 40 * S), (xa, H - MB + 20 * S)], fill=INK, width=1 * S)
d.text((xa - 60 * S, MT - 80 * S), "t = 0.78", font=F, fill=INK)
d.text((ML, H - MB + 70 * S), "seven instruments  /  one score", font=F, fill=INK)
d.text((ML, MT - 80 * S), "convergent instruments", font=F, fill=INK)

img = img.resize((W // S, H // S), Image.LANCZOS)
img.save("out/genz_protests/companion/convergent_instruments.png")
print("ok")
