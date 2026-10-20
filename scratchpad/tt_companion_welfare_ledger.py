"""Companion art piece (standing rule, CLAUDE.md): LEDGER OF SMALL LIGHTS. See brain/companion/LEDGER_OF_SMALL_LIGHTS_PHILOSOPHY.md.
A specimen plate of 558 die-cut four-point marks, one per logged project, drawn from the real table (tt_welfare_stats.py).
Rule: one column per welfare pillar, marks stack from the baseline in date order, colour is the ERA (2021-22 blue, 2023-24 green, 2025-26 orchid),
a half-row gap separates each year inside a column. The subtle reference is the welfare record itself: the tall column is children and education,
the short ones are the work that is rarer but exists. Nothing is invented: every mark is a row.
Run: python scratchpad/tt_companion_welfare_ledger.py  ->  brain/companion/welfare_ledger.png"""
import importlib.util, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("st", "scratchpad/tt_welfare_stats.py"); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)

W, H = 2400, 3000
BLACK, CREAM, ORCHID, GREEN, BLUE = (0, 0, 0), (243, 236, 222), (222, 104, 240), (47, 210, 132), (20, 138, 218)
PER, PITCH, MARK, GAP = 6, 34, 30, 100           # marks per row, pitch px, mark px, gap between columns
COLW = PER * PITCH
GRIDW = 7 * COLW + 6 * GAP
MX, BASE = (W - GRIDW) // 2, 2420

base = Image.open("engine/assets/terrathon/shuriken.png").convert("RGBA")
ys, xs = np.where(np.array(base)[..., 3] > 20); base = base.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
def recolor(im, dst):
    a = np.array(im).astype(int); d = np.sqrt(((a[..., :3] - np.array(BLUE)) ** 2).sum(-1)); m = (d < 70) & (a[..., 3] > 20)
    a[..., :3][m] = np.clip(np.array(dst) + (a[..., :3][m] - np.array(BLUE)) * 0.5, 0, 255)
    return Image.fromarray(a.astype(np.uint8))
SPR = {k: v.resize((MARK, round(MARK * v.height / v.width)), Image.LANCZOS) for k, v in {"blue": base, "green": recolor(base, GREEN), "orchid": recolor(base, ORCHID)}.items()}
era = lambda y: "blue" if y <= 2022 else "green" if y <= 2024 else "orchid"

canvas = Image.new("RGBA", (W, H), BLACK + (255,)); d = ImageDraw.Draw(canvas)
rnd = random.Random(5)
for _ in range(900):
    x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice([1, 1, 1.5, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(rnd.uniform(35, 140))))

mono = ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Medium.ttf", 24)
mono_s = ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Medium.ttf", 20)
bold = ImageFont.truetype("engine/assets/fonts/JetBrainsMono-Bold.ttf", 28)
LABEL = dict(children="CHILDREN", health="HEALTH", women="WOMEN", elderly="ELDERLY", community="COMMUNITY", environment="ENVIRON", animals="ANIMALS")

top_y = BASE
for i, p in enumerate(st.PILLARS):
    rows = sorted(st.pstat(p)["rows"], key=lambda r: (r["year"], r["month"]))
    x0 = MX + i * (COLW + GAP)
    r_i, c_i, last_year = 0, 0, None
    for r in rows:
        if last_year is not None and r["year"] != last_year:                     # new year: finish the row, drop a half-row gap
            if c_i: r_i += 1; c_i = 0
            r_i += 0.5
        last_year = r["year"]
        sp = SPR[era(r["year"])]
        cx, cy = x0 + c_i * PITCH + PITCH / 2, BASE - 20 - r_i * PITCH - PITCH / 2
        canvas.alpha_composite(sp, (round(cx - sp.width / 2), round(cy - sp.height / 2)))
        c_i += 1
        if c_i == PER: c_i = 0; r_i += 1
    top = BASE - 20 - (r_i + (1 if c_i else 0)) * PITCH
    top_y = min(top_y, top)
    d.text((x0, BASE + 38), LABEL[p], font=mono, fill=CREAM + (235,), anchor="la")
    d.text((x0, BASE + 74), f"{len(rows):03d}", font=bold, fill=CREAM + (235,), anchor="la")
    d.line([x0, BASE, x0 + COLW, BASE], fill=CREAM + (200,), width=2)

d.text((MX, 190), "PLATE 09", font=bold, fill=CREAM + (235,), anchor="lm")
d.text((MX, 246), "ONE MARK = ONE LOGGED PROJECT. 2021 TO 2026.", font=mono, fill=CREAM + (200,), anchor="lm")
lx = W - MX
for j, (k, lab) in enumerate((("blue", "2021-22"), ("green", "2023-24"), ("orchid", "2025-26"))):
    y = 190 + j * 40
    d.text((lx - 40, y), lab, font=mono_s, fill=CREAM + (210,), anchor="rm")
    canvas.alpha_composite(SPR[k], (lx - 28, y - SPR[k].height // 2))
d.text((MX, H - 200), f"{st.N} PROJECTS.  {st.VOLS:,} VOLUNTEER TURNOUTS.", font=mono, fill=CREAM + (235,), anchor="lm")
d.text((MX, H - 150), "36 FUNDRAISER AND MISC ROWS NOT SHOWN", font=mono_s, fill=CREAM + (150,), anchor="lm")
d.text((lx, H - 200), "AQUATERRA", font=bold, fill=CREAM + (235,), anchor="rm")

os.makedirs("brain/companion", exist_ok=True)
out = "brain/companion/welfare_ledger.png"; canvas.convert("RGB").save(out); print("done", out, "top of tallest column y =", int(top_y))
