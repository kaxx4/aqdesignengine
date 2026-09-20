import asyncio, os, sys, importlib.util, math
# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
B = load("build"); core = load("core")

W, H = 1600, 1580
RED = "#E8341F"
CREAM = "#F4EFE0"
TEAL = "#0E5A63"
INK = "#0A0A0A"

# --- the cascade: one card shape, repeated under a strict rule ---
# ratio: each repeat is 0.895x the previous. rotation: +5.5deg per repeat. offset: fixed vector.
N = 9
BASE_W, BASE_H = 620, 760
RATIO = 0.895
ROT_STEP = 5.5
DX, DY = 34, -30
CX, CY = W / 2 - BASE_W / 2 + 40, 560

cards = []
for i in range(N):
    sc = RATIO ** i
    w, h = BASE_W * sc, BASE_H * sc
    x = CX + DX * i - (BASE_W - w) * 0.15
    y = CY + DY * i + (i * 6)
    rot = -ROT_STEP * (N - 1) / 2 + ROT_STEP * i
    shadow_off = 10
    cards.append((x, y, w, h, rot, i))

svg_cards = []
# draw back-to-front so later (i large) sits on top, matching a fanned hand held from the left
for x, y, w, h, rot, i in cards:
    ccx, ccy = x + w / 2, y + h / 2
    op = 1.0
    svg_cards.append(
        f'<g transform="rotate({rot:.2f} {ccx:.1f} {ccy:.1f})">'
        f'<rect x="{x+7:.1f}" y="{y+9:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" '
        f'fill="{INK}" opacity="0.16"/>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="14" '
        f'fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>'
        f'<line x1="{x+w*0.14:.1f}" y1="{y+h*0.16:.1f}" x2="{x+w*0.62:.1f}" y2="{y+h*0.16:.1f}" '
        f'stroke="{INK}" stroke-width="2" opacity="0.5"/>'
        f'<line x1="{x+w*0.14:.1f}" y1="{y+h*0.22:.1f}" x2="{x+w*0.42:.1f}" y2="{y+h*0.22:.1f}" '
        f'stroke="{INK}" stroke-width="2" opacity="0.28"/>'
        f'</g>'
    )

# a single glint punctuating the top-right register (the composition's only ornament)
glint_cx, glint_cy = W - 210, 300
def sparkle(cx, cy, r):
    return (f'<path d="M{cx} {cy-r} Q{cx+r*0.16} {cy-r*0.16} {cx+r} {cy} '
            f'Q{cx+r*0.16} {cy+r*0.16} {cx} {cy+r} Q{cx-r*0.16} {cy+r*0.16} {cx-r} {cy} '
            f'Q{cx-r*0.16} {cy-r*0.16} {cx} {cy-r} Z" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>')

# fixed reference marks (systematic/diagram feel) — tick row at the far right margin
ticks = "".join(
    f'<line x1="{W-64}" y1="{240+i*26}" x2="{W-64-(14 if i%4==0 else 8)}" y2="{240+i*26}" '
    f'stroke="{INK}" stroke-width="1.6" opacity="0.55"/>' for i in range(20)
)

# teal horizon field the cascade's lowest tip touches with zero gap — no dead space, no collision
last_x, last_y, last_w, last_h, last_rot, _ = cards[-1]
horizon_y = last_y + last_h * 0.985

caption = (f'<text x="120" y="{H-96}" font-family="JetBrains Mono, monospace" font-size="19" '
           f'letter-spacing="3.2" fill="{CREAM}" font-weight="700">FIG. 09 — ONE RULE, REPEATED</text>'
           f'<text x="120" y="{H-64}" font-family="JetBrains Mono, monospace" font-size="13" '
           f'letter-spacing="1.6" fill="{CREAM}" opacity="0.72">SCALE ×0.895 · ROTATE +5.5° · OFFSET (34,-30) PER STEP</text>')

mark = (f'<text x="120" y="150" font-family="JetBrains Mono, monospace" font-size="15" '
        f'letter-spacing="4" fill="{INK}" opacity="0.62">CASCADE DISCIPLINE</text>'
        f'<text x="120" y="176" font-family="JetBrains Mono, monospace" font-size="12" '
        f'letter-spacing="2.4" fill="{INK}" opacity="0.4">N=09 · NO GAP · NO COLLISION</text>')

svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
       f'<rect width="{W}" height="{H}" fill="{RED}"/>'
       f'<rect x="0" y="{horizon_y:.1f}" width="{W}" height="{H-horizon_y:.1f}" fill="{TEAL}"/>'
       f'<rect x="0" y="{horizon_y:.1f}" width="{W}" height="3" fill="{INK}" opacity="0.5"/>'
       + mark + ticks
       + "".join(svg_cards)
       + sparkle(glint_cx, glint_cy, 26)
       + sparkle(glint_cx - 54, glint_cy + 64, 12)
       + caption
       + f'<rect x="26" y="26" width="{W-52}" height="{H-52}" fill="none" stroke="{CREAM}" stroke-width="1.2" opacity="0.35"/>'
       + '</svg>')

inner = f'<div style="position:absolute;inset:0">{svg}</div>'
html = B.page(W, H, RED, inner, grain=True)

async def main():
    os.makedirs("scratchpad/proof", exist_ok=True)
    await B.render(html, "scratchpad/proof/cascade_discipline.png", W, H)
    print("done")
asyncio.run(main())
