"""
MARGINALIA — companion art piece to out/teachers_day.png (AQ Teachers Day poster).
Generates a self-contained SVG, then rasterizes it to PNG + PDF via the already-installed
Chromium (matches the AQ engine's own render path in engine/build.py).

Design: brain/../companion/teachers_day/PHILOSOPHY.md. A field of hand-corrected marks — red
crossed-out attempts thinning, band by band, into calm graphite checkmarks, thinning again into
near-silence and a single gold mark that holds. The subject (a teacher's private practice of
marking a student's work, over and over, until it's right) is never named in the piece itself.
"""
import math, random, os

W, H = 1600, 2000
random.seed(7)

PAPER   = "#F2ECDD"
PAPER2  = "#ECE4D2"   # slightly deeper paper tone for the vignette
INK     = "#2B2A28"
RED     = "#A6392B"
RED2    = "#8F3226"
GOLD    = "#C0923A"
FRAME   = "#2B2A28"

FONT_DIR = "/root/.claude/skills/synced/38d67b45-df55-409d-be12-6b62181fe978_87846feb-1ca9-4b65-a508-b752d233935d/canvas-design/canvas-fonts"

def font_face(family, path, style="normal", weight="400"):
    import base64
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (f"@font-face{{font-family:'{family}';src:url(data:font/ttf;base64,{b64}) "
            f"format('truetype');font-style:{style};font-weight:{weight}}}")

FONTS_CSS = "\n".join([
    font_face("InstrumentSerif", os.path.join(FONT_DIR, "InstrumentSerif-Italic.ttf"), "italic"),
    font_face("JetBrainsMono", os.path.join(FONT_DIR, "JetBrainsMono-Regular.ttf")),
    font_face("JetBrainsMonoBold", os.path.join(FONT_DIR, "JetBrainsMono-Bold.ttf"), weight="700"),
])

def jitter(v, amt): return v + random.uniform(-amt, amt)

def checkmark(cx, cy, s, rot, color, sw):
    # a two-segment tick, local box ~24x24 centered on origin, then placed at (cx,cy)
    pts = [(-9,1),(-2,8),(10,-9)]
    return path_from_local(pts, cx, cy, s, rot, color, sw, closed=False)

def cross(cx, cy, s, rot, color, sw):
    a = f'M{-8},{-8} L{8},{8}'
    b = f'M{8},{-8} L{-8},{8}'
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({s:.3f})">'
    return (g + f'<path d="{a}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
              + f'<path d="{b}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round"/></g>')

def scribble(cx, cy, s, rot, color, sw):
    d = "M-14,6 C-9,-10 -4,14 1,-8 C6,-14 11,12 15,-4"
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({s:.3f})">'
    return g + f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'

def loop(cx, cy, s, rot, color, sw):
    d = "M-10,8 C-10,-10 10,-10 10,4 C10,14 -6,14 -4,2 C-2,-8 8,-6 10,4"
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({s:.3f})">'
    return g + f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'

def star(cx, cy, s, color):
    pts = []
    for i in range(10):
        ang = -math.pi/2 + i*math.pi/5
        r = 11 if i % 2 == 0 else 4.6
        pts.append((r*math.cos(ang), r*math.sin(ang)))
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s:.3f})">'
    return g + f'<path d="{d}" fill="{color}" stroke="{FRAME}" stroke-width="0.8"/></g>'

def path_from_local(pts, cx, cy, s, rot, color, sw, closed=False):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + (" Z" if closed else "")
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({s:.3f})">'
    return g + f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'

marks = []

# ---- the field: 14 bands, thinning from agitated correction to a single resolved mark ----
MARGIN = 150
FRAME_IN = 40
top_y, bot_y = 300, 1760
bands = 14
band_h = (bot_y - top_y) / bands

fig_labels = []  # small specimen annotations, sprinkled sparingly

for i in range(bands):
    t = i / (bands - 1)  # 0 at top (chaos) -> 1 near bottom (order)
    y0 = top_y + i * band_h
    count = max(1, round(13 * (1 - t) ** 1.4))
    size = 1.05 + t * 0.55
    if i == bands - 1:
        count = 0  # last band left empty; the single gold mark sits below it, alone
    xs = []
    usable_w = W - 2*MARGIN
    if count == 1:
        xs = [W/2]
    else:
        for k in range(count):
            xs.append(MARGIN + usable_w * (k + 0.5) / count)
    for x in xs:
        cx = jitter(x, usable_w / max(count,1) * 0.22 * (1 - t*0.6))
        cy = jitter(y0 + band_h/2, band_h*0.28*(1 - t*0.5))
        rot = jitter(0, 30 * (1 - t) + 4)
        s = size * random.uniform(0.85, 1.15)
        sw = 2.6 - t*0.7
        if t < 0.22:
            kind = random.choices(["cross","scribble"], weights=[0.6,0.4])[0]
            col = random.choice([RED, RED2])
        elif t < 0.45:
            kind = random.choices(["cross","check","scribble"], weights=[0.35,0.4,0.25])[0]
            col = RED if kind != "check" else INK
        elif t < 0.75:
            kind = random.choices(["check","loop"], weights=[0.75,0.25])[0]
            col = INK
        else:
            kind = "check"
            col = INK
            rot *= 0.3
        if kind == "check": marks.append(checkmark(cx, cy, s*1.3, rot, col, sw))
        elif kind == "cross": marks.append(cross(cx, cy, s*1.15, rot, col, sw))
        elif kind == "scribble": marks.append(scribble(cx, cy, s*1.0, rot, col, sw))
        elif kind == "loop": marks.append(loop(cx, cy, s*1.05, rot, col, sw))

# a few sparse specimen annotations, set in the quiet margin strip between the frame and the
# mark field (x<MARGIN or x>W-MARGIN) so they can never collide with a mark's jittered position —
# an annotation sitting on top of the thing it annotates is the one failure this piece can't afford.
for n, (fx, fy, anchor) in enumerate([
    (FRAME_IN+30, 460, "start"), (W-FRAME_IN-30, 620, "end"),
    (FRAME_IN+30, 900, "start"), (W-FRAME_IN-30, 1120, "end"),
]):
    fig_labels.append(f'<text x="{fx}" y="{fy}" font-family="JetBrainsMono" font-size="13" '
                       f'letter-spacing="0.06em" fill="{INK}" text-anchor="{anchor}" opacity="0.42">fig. {7+n*6}</text>')

# the single resolved mark — gold, alone, centered in generous silence
gold_y = bot_y + 55
marks.append(star(W/2, gold_y, 2.1, GOLD))
marks.append(f'<circle cx="{W/2}" cy="{gold_y}" r="34" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.55"/>')

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
<style>{FONTS_CSS}</style>
<radialGradient id="vig" cx="50%" cy="42%" r="75%">
<stop offset="60%" stop-color="{PAPER}"/><stop offset="100%" stop-color="{PAPER2}"/>
</radialGradient>
</defs>

<rect width="{W}" height="{H}" fill="url(#vig)"/>

<!-- ledger frame -->
<rect x="{FRAME_IN}" y="{FRAME_IN}" width="{W-2*FRAME_IN}" height="{H-2*FRAME_IN}" fill="none" stroke="{FRAME}" stroke-width="1.6"/>
<rect x="{FRAME_IN+10}" y="{FRAME_IN+10}" width="{W-2*FRAME_IN-20}" height="{H-2*FRAME_IN-20}" fill="none" stroke="{FRAME}" stroke-width="0.75" opacity="0.55"/>

<!-- header -->
<text x="{MARGIN}" y="150" font-family="JetBrainsMonoBold" font-size="15" letter-spacing="0.22em" fill="{INK}">A TAXONOMY OF CORRECTIONS</text>
<text x="{W-MARGIN}" y="150" font-family="JetBrainsMono" font-size="15" letter-spacing="0.14em" fill="{INK}" text-anchor="end" opacity="0.75">PLATE VII</text>
<line x1="{MARGIN}" y1="178" x2="{W-MARGIN}" y2="178" stroke="{INK}" stroke-width="1" opacity="0.4"/>

{''.join(fig_labels)}
{''.join(marks)}

<!-- footer -->
<line x1="{MARGIN}" y1="{H-160}" x2="{W-MARGIN}" y2="{H-160}" stroke="{INK}" stroke-width="1" opacity="0.4"/>
<text x="{W/2}" y="{H-108}" font-family="InstrumentSerif" font-style="italic" font-size="34" fill="{INK}" text-anchor="middle">again, until it holds.</text>
<text x="{W/2}" y="{H-70}" font-family="JetBrainsMono" font-size="12" letter-spacing="0.16em" fill="{INK}" text-anchor="middle" opacity="0.5">COLLECTED MARKS &#183; UNCOUNTED HOURS</text>
</svg>'''

out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, "marginalia.svg"), "w") as f:
    f.write(svg)
print("wrote", os.path.join(out_dir, "marginalia.svg"), f"({len(marks)} marks)")
