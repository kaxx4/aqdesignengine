"""Companion art piece (standing rule, CLAUDE.md): HALO FIELD. See brain/companion/HALO_FIELD_PHILOSOPHY.md.
A specimen plate of 130 die-cut four-point marks. Rule: scale swells to the centre, rotation steps 6 deg per column, colour changes by phase band
(blue outer, green middle, orchid core). The subtle reference is TerraThon: the shuriken, the cream die-cut halo, the -1.25 deg slab, all for charity."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H = 2400, 3000
BLACK, CREAM, ORCHID = (0, 0, 0), (243, 236, 222), (222, 104, 240)
GREEN, BLUE = (47, 210, 132), (20, 138, 218)
COLS, ROWS = 10, 13
MX, MY, CELLW, CELLH = 150, 200, 210, 180
GRIDW, GRIDH = COLS * CELLW, ROWS * CELLH            # 2100 x 2470

base = Image.open("engine/assets/terrathon/shuriken.png").convert("RGBA")
ys, xs = np.where(np.array(base)[..., 3] > 20); base = base.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
base = base.resize((base.width * 3, base.height * 3), Image.LANCZOS)             # work large, downsample cleanly per mark

def recolor(im, dst):
    a = np.array(im).astype(int); d = np.sqrt(((a[..., :3] - np.array(BLUE)) ** 2).sum(-1)); m = (d < 70) & (a[..., 3] > 20)
    a[..., :3][m] = np.clip(np.array(dst) + (a[..., :3][m] - np.array(BLUE)) * 0.5, 0, 255)
    return Image.fromarray(a.astype(np.uint8))
VARIANT = {"blue": base, "green": recolor(base, GREEN), "orchid": recolor(base, ORCHID)}

canvas = Image.new("RGBA", (W, H), BLACK + (255,))
rnd = random.Random(11); d = ImageDraw.Draw(canvas)
for _ in range(950):                                                             # the dust
    x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice([1, 1, 1.5, 2]); a = int(rnd.uniform(40, 150))
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

cx, cy = (COLS - 1) / 2, (ROWS - 1) / 2
for row in range(ROWS):
    for col in range(COLS):
        nx, ny = (col - cx) / cx, (row - cy) / cy
        dist = min(1.0, math.hypot(nx * 0.9, ny))                                 # 0 at the centre, 1 at the far edge
        size = CELLH * (0.40 + 0.62 * (1 - dist ** 1.35))
        phase = "orchid" if dist < 0.30 else "green" if dist < 0.62 else "blue"
        rot = (col - cx) * 6.0 + (row - cy) * 1.5
        sp = VARIANT[phase].rotate(-rot, resample=Image.BICUBIC, expand=True)
        k = size / max(sp.width, sp.height) * 1.02
        sp = sp.resize((max(2, int(sp.width * k)), max(2, int(sp.height * k))), Image.LANCZOS)
        px, py = MX + col * CELLW + CELLW / 2 - sp.width / 2, MY + row * CELLH + CELLH / 2 - sp.height / 2
        canvas.alpha_composite(sp, (int(px), int(py)))

# reference markers: column indices along the top, row letters down the left. thin, exact.
mono = ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Medium.ttf", 24)
for col in range(COLS):
    t = f"{col + 1:02d}"; x = MX + col * CELLW + CELLW / 2
    d.text((x, MY - 62), t, font=mono, fill=CREAM + (150,), anchor="mm")
    d.line([(x, MY - 34), (x, MY - 18)], fill=CREAM + (110,), width=2)
for row in range(ROWS):
    t = "ABCDEFGHIJKLM"[row]; y = MY + row * CELLH + CELLH / 2
    d.text((MX - 62, y), t, font=mono, fill=CREAM + (150,), anchor="mm")
    d.line([(MX - 34, y), (MX - 18, y)], fill=CREAM + (110,), width=2)
    d.line([(W - MX + 18, y), (W - MX + 34, y)], fill=CREAM + (110,), width=2)      # mirrored tick: the plate is symmetric about its centre line
d.text((MX, 92), "PLATE 07", font=ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Bold.ttf", 30), fill=CREAM + (235,), anchor="lm")
d.text((W - MX, 92), "N = 130   STEP = 6.0 DEG / COL   3 PHASES", font=mono, fill=CREAM + (150,), anchor="rm")

# the one tilted label: the slab, a museum label at -1.25 deg
lw, lh = 1240, 190
lab = Image.new("RGBA", (lw + 60, lh + 60), (0, 0, 0, 0)); ld = ImageDraw.Draw(lab)
ld.rounded_rectangle([30, 30, 30 + lw, 30 + lh], radius=46, fill=ORCHID + (255,)); ld.rounded_rectangle([46, 46, 30 + lw - 16, 30 + lh - 16], radius=32, fill=(249, 249, 249, 255))
f1 = ImageFont.truetype("engine/assets/fonts/NeutralFace-Bold.otf", 64); f2 = ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Medium.ttf", 26)
ld.text((90, 30 + lh / 2 - 26), "ALL FOR CHARITY", font=f1, fill=(10, 10, 10, 255), anchor="lm")
ld.text((90, 30 + lh / 2 + 44), "FOUR-POINT MARK, DIE-CUT, CREAM MARGIN. AQ / 03-04.10.26", font=f2, fill=(10, 10, 10, 200), anchor="lm")
lab = lab.rotate(1.25, resample=Image.BICUBIC, expand=True)
canvas.alpha_composite(lab, (int((W - lab.width) / 2), MY + GRIDH + 50))

os.makedirs("out/collaterals/companion", exist_ok=True)
canvas.convert("RGB").save("out/collaterals/companion/terrathon_halo_field.png", optimize=True)
print("done", canvas.size)
