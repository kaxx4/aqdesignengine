"""Companion plate for the REVER marketing deck (CLAUDE.md standing rule, 2026-07-18): "Mirrored Night", philosophy in brain/companion/MIRRORED_NIGHT_PHILOSOPHY.md.

THE SUBTLE REFERENCE. The deck's promise is a campaign shaped like a night: close to a month of build, one evening (10 November), a week of afterglow. The plate draws that
shape as a field survey. One column per half-day, -28 to +7, each a stack of identical mirror-facet tiles; below the axis every column is echoed, dimmer and one step late,
because a collab post lives on two profiles (Rever's and ours). The one crimson tile is Rever, at the crest. It is a SCHEMATIC, not data: heights come from a smooth curve and a
seeded rng, and the plate says so ("schematic, not a count"). No statistic is implied.

Run: python scratchpad/companion_mirrored_night.py   ->  brain/companion/mirrored_night.{png,pdf}   (3600x4500, 4:5)
"""
import math, os, random, sys
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = "/root/.claude/skills/synced/38d67b45-df55-409d-be12-6b62181fe978_87846feb-1ca9-4b65-a508-b752d233935d/canvas-design/canvas-fonts"
OUT = os.path.join(ROOT, "brain", "companion")
W, H = 1200, 1500
GROUND, CREAM, ORCHID, CRIMSON = "#0C0B0E", "#EFE7D4", "#DE68F0", "#BB213C"

ML, MR = 96, 96
X0, X1 = ML, W - MR
COLS = 72                       # half-days, -28 .. +7 (36 days x 2 columns... 35 days = 70 + the event day pair)
T0 = -28.0
PITCH = (X1 - X0) / COLS        # 14
TILE, GAP = 10, 3
VP = TILE + GAP                 # vertical pitch 13
AXIS = 905
rnd = random.Random(1110)


def t_of(i): return T0 + i * 0.5


def height(t):
    """Smooth stack height in tiles: a slow build, the crest on the night, a fast decay."""
    if t < 0:
        return 2 + 23 * (1 - abs(t) / 28.0) ** 1.9
    if t < 1:
        return 50 - 8 * t
    return 2 + 31 * math.exp(-(t - 1) / 2.3)


cols = []
for i in range(COLS):
    t = t_of(i)
    h = height(t)
    h += rnd.uniform(-1.2, 1.2) if abs(t) > 0.01 else 0
    cols.append(max(1, int(round(h))))
PEAK = max(range(COLS), key=lambda i: cols[i])
assert abs(t_of(PEAK)) <= 0.5, "the crest must sit on the night"


def px(i): return X0 + i * PITCH + (PITCH - TILE) / 2


tiles = []
for i, h in enumerate(cols):
    x = px(i)
    for k in range(h):
        y = AXIS - 8 - (k + 1) * VP + GAP
        top = k >= h - 2
        lit = (rnd.random() < (0.93 - 0.55 * (k / max(h, 1)) ** 1.3)) and not top
        if i == PEAK and k == h - 1:
            tiles.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{TILE}" height="{TILE}" fill="{CRIMSON}"/>')
        elif lit:
            tiles.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{TILE}" height="{TILE}" fill="{ORCHID}"/>')
        else:
            tiles.append(f'<rect x="{x + .4:.2f}" y="{y + .4:.2f}" width="{TILE - .8}" height="{TILE - .8}" fill="none" stroke="{CREAM}" stroke-width=".7" opacity=".78"/>')

# the reflection: each column echoed one half-day late, 0.56 as tall, fading with depth, the lit/counted mix kept
refl = []
rr = random.Random(7)
for i in range(1, COLS):
    h = int(round(cols[i - 1] * 0.56))
    x = px(i)
    for k in range(h):
        y = AXIS + 42 + k * VP
        depth = k / 31.0
        op = 0.5 * math.exp(-3.1 * depth) * (0.92 + 0.08 * rr.random())
        if op < .03: continue
        lit = rr.random() < (0.9 - 0.5 * (k / max(h, 1)) ** 1.2)
        if lit:
            refl.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{TILE}" height="{TILE}" fill="{ORCHID}" opacity="{op:.3f}"/>')
        else:
            refl.append(f'<rect x="{x + .4:.2f}" y="{y + .4:.2f}" width="{TILE - .8}" height="{TILE - .8}" fill="none" stroke="{CREAM}" stroke-width=".7" opacity="{op * .8:.3f}"/>')

# axis: hairline, a tick per column, a longer tick per day, a labelled tick per week
axis = [f'<line x1="{X0}" y1="{AXIS}" x2="{X1}" y2="{AXIS}" stroke="{CREAM}" stroke-width=".8" opacity=".9"/>']
for i in range(COLS + 1):
    x = X0 + i * PITCH
    t = t_of(i)
    day = abs(t - round(t)) < 1e-6
    wk = day and int(round(t)) % 7 == 0
    ln = 9 if wk else (5 if day else 2.5)
    axis.append(f'<line x1="{x:.2f}" y1="{AXIS - ln / 2 + (ln / 2 if False else 0)}" x2="{x:.2f}" y2="{AXIS + ln / 2}" stroke="{CREAM}" stroke-width=".7" opacity="{.95 if wk else .55}"/>')
labels = []
for d in (-28, -21, -14, -7, 0, 7):
    i = int(round((d - T0) / 0.5))
    x = X0 + i * PITCH
    s = "0" if d == 0 else (f"+{d}" if d > 0 else f"−{abs(d)}")
    labels.append(f'<text x="{x:.2f}" y="{AXIS + 24}" text-anchor="middle" class="m" fill="{CREAM}" opacity=".7">{s}</text>')

# left ruler in the margin (one tick per five tiles above the axis), and registration furniture
ruler = [f'<line x1="{ML - 22}" y1="{AXIS}" x2="{ML - 22}" y2="{AXIS - 50 * VP}" stroke="{CREAM}" stroke-width=".6" opacity=".4"/>']
for k in range(0, 51):
    ln = 8 if k % 10 == 0 else (5 if k % 5 == 0 else 2.5)
    y = AXIS - 8 - k * VP
    ruler.append(f'<line x1="{ML - 22 - ln}" y1="{y}" x2="{ML - 22}" y2="{y}" stroke="{CREAM}" stroke-width=".6" opacity=".55"/>')


def cross(cx, cy, r=7):
    return (f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{CREAM}" stroke-width=".7" opacity=".7"/>'
            f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="{CREAM}" stroke-width=".7" opacity=".7"/>')


furn = [cross(ML - 22, 70), cross(W - MR + 22, 70), cross(ML - 22, H - 70), cross(W - MR + 22, H - 70)]
furn.append(f'<circle cx="{W - MR - 18}" cy="118" r="13" fill="none" stroke="{CREAM}" stroke-width=".7" opacity=".7"/>'
            f'<circle cx="{W - MR - 18}" cy="118" r="2" fill="{CREAM}" opacity=".7"/>'
            f'<line x1="{W - MR - 40}" y1="118" x2="{W - MR + 4}" y2="118" stroke="{CREAM}" stroke-width=".6" opacity=".6"/>'
            f'<line x1="{W - MR - 18}" y1="96" x2="{W - MR - 18}" y2="140" stroke="{CREAM}" stroke-width=".6" opacity=".6"/>')

# phase brackets under the reflection
BY = 1384
def bracket(i0, i1, label, anchor="middle"):
    xa, xb = X0 + i0 * PITCH + 2, X0 + i1 * PITCH - 2
    return (f'<path d="M{xa:.1f},{BY - 6} V{BY} H{xb:.1f} V{BY - 6}" fill="none" stroke="{CREAM}" stroke-width=".7" opacity=".7"/>'
            f'<text x="{(xa + xb) / 2:.1f}" y="{BY + 24}" text-anchor="middle" class="m" fill="{CREAM}" opacity=".78">{label}</text>')


iN = int(round((0 - T0) / 0.5)); iN1 = iN + 2
brackets = bracket(0, iN, "before · close to a month") + bracket(iN, iN1, "") + bracket(iN1, COLS, "after · the week")
night_x = X0 + (iN + 1) * PITCH
brackets += f'<text x="{night_x:.1f}" y="{BY + 24}" text-anchor="middle" class="m" fill="{CREAM}" opacity=".95" style="letter-spacing:.2em">10.11.26</text>'
# the date label sits under its own short bracket; the 'after' bracket label is nudged right of it by its own span (checked below)

html = f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:'DMMono';src:url('file://{FONTS}/DMMono-Regular.ttf')}}
@font-face{{font-family:'InstrumentSerif';font-style:italic;src:url('file://{FONTS}/InstrumentSerif-Italic.ttf')}}
@font-face{{font-family:'Jura';src:url('file://{FONTS}/Jura-Light.ttf')}}
html,body{{margin:0;background:{GROUND}}}
.m{{font-family:'DMMono';font-size:8.6px;letter-spacing:.16em;text-transform:lowercase}}
.t{{font-family:'Jura';font-size:10.5px;letter-spacing:.34em;text-transform:lowercase}}
.s{{font-family:'InstrumentSerif';font-style:italic;font-size:30px;letter-spacing:.005em}}
</style>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0"/></filter></defs>
<rect width="{W}" height="{H}" fill="{GROUND}"/>
<rect width="{W}" height="{H}" filter="url(#g)" opacity=".045"/>
{''.join(furn)}
<text x="{ML}" y="122" class="t" fill="{CREAM}" opacity=".85">plate 14</text>
<text x="{ML}" y="142" class="t" fill="{CREAM}" opacity=".5">mirrored night</text>
<text x="{ML}" y="300" class="s" fill="{CREAM}" opacity=".92">every post,</text>
<text x="{ML}" y="336" class="s" fill="{CREAM}" opacity=".92">seen twice.</text>
{''.join(ruler)}
{''.join(refl)}
{''.join(tiles)}
{''.join(axis)}
{''.join(labels)}
{brackets}
<text x="{ML}" y="{H - 62}" class="m" fill="{CREAM}" opacity=".5">aquaterra × rever · disco diwali 2026</text>
<text x="{X1}" y="{H - 62}" text-anchor="end" class="m" fill="{CREAM}" opacity=".5">schematic, not a count</text>
</svg>"""

os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(ROOT, "scratchpad", "work"); os.makedirs(tmp, exist_ok=True)
hp = os.path.join(tmp, "mirrored_night.html"); open(hp, "w").write(html)
png = os.path.join(OUT, "mirrored_night.png")
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=3)
    pg.goto("file://" + hp); pg.wait_for_timeout(700)
    # overlap / bounds audit of every text node against the canvas and each other
    boxes = pg.evaluate("""()=>[...document.querySelectorAll('text')].map(t=>{const r=t.getBoundingClientRect();return [t.textContent,r.left,r.top,r.right,r.bottom]})""")
    pg.screenshot(path=png); b.close()
bad = []
for n, l, t, r, bt in boxes:
    if not n.strip(): continue
    if l < 60 or r > W - 60 or t < 60 or bt > H - 40: bad.append(("MARGIN", n, round(l), round(t), round(r), round(bt)))
for a in range(len(boxes)):
    for c in range(a + 1, len(boxes)):
        A, B_ = boxes[a], boxes[c]
        if A[1] < B_[3] and B_[1] < A[3] and A[2] < B_[4] and B_[2] < A[4] and A[0].strip() and B_[0].strip():
            bad.append(("OVERLAP", A[0], B_[0]))
print("text audit:", bad or "clean", "| tiles:", len(tiles), "above,", len(refl), "reflected | crest col", PEAK, "h", cols[PEAK])
im = Image.open(png).convert("RGB"); print(im.size)
im.save(os.path.join(OUT, "mirrored_night.pdf"), resolution=300)
im.save(png, optimize=True)
