"""Recreation — sample 3d846c78, v3. Built to MEASURED geometry.

v2 -> v3. v2 scored 0.405, WORSE than v1's 0.18, because my step-1 written
description contained two eyeballed proportions that were simply wrong:

  "the grid sits HIGH, about twice as much black below as above"
      measured: 1.05 : 1 — essentially centred. v2 moved it to 0.51 : 1 and bbox
      IoU fell 0.87 -> 0.60.
  "the bottom-right card is visibly WIDER and breaks the grid's right edge"
      measured: the occupancy grid is symmetric; BR is wider by ~1% of frame, not 4%.

Both are now taken from compare.geometry() instead of from looking:
    content bbox  x 0.109..0.896   y 0.298..0.717
    centroid (0.502, 0.508)   coverage 0.309

Also fixed: the brush marks were too light to read as the reference's loaded brush,
and the BR mark was SMALLER than the TL one when the reference has it larger.
"""
import asyncio, os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); lay = load("layout"); sh = load("shapes")

W, H = core.SIZES["feed"]
SLUG = "3d846c781bd059"
OUT = f"out/versions/{SLUG}"
os.makedirs(OUT, exist_ok=True)
INK, CREAM = core.INK, core.CREAM
BLUE, ORANGE = core.ACCENTS[4], core.ACCENTS[3]

# ── MEASURED off the reference (compare.geometry), not estimated ─────────────
BX0, BX1 = 0.109 * W, 0.896 * W
BY0, BY1 = 0.298 * H, 0.717 * H
GUT = 0.024 * W
CW = (BX1 - BX0 - GUT) / 2
CH = (BY1 - BY0 - GUT) / 2
BR_EXTRA = 0.012 * W          # measured: BR is wider by ~1% of frame, not 4%

CARD_SHADOW = "0 10px 26px -8px rgba(0,0,0,.85)"
CAPS_L = ["KOLKATA", "STUDENT", "WELFARE", "CLIMATE"]
CAPS_R = ["GROWN", "RUN", "CREW", "AND EDUCATION"]
RHYTHM = ["Log.", "Return.", "Repeat."]
FOOT_1 = "STUDENT-RUN NON-PROFIT BASED IN KOLKATA"
FOOT_2L, FOOT_2R = "558 LOGGED PROJECTS", "@NGO.AQUATERRA"


def card(x, y, w, h, bg, z=6):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{bg};box-shadow:{CARD_SHADOW};z-index:{z};overflow:hidden">')


def caps_card(x, y, w, h, bg, fg, strokes, seed, mark_cx=0.5, mark_scale=1.0, z=6):
    pad = w * 0.072
    fs = w * 0.063
    small = w * 0.0305
    rows = []
    for i, (l, r) in enumerate(zip(CAPS_L, CAPS_R)):
        parts = ([l] + r.split(" ")) if i == 2 else [l, r]
        spans = "".join(f"<span>{p}</span>" for p in parts)
        rows.append('<div style="display:flex;justify-content:space-between;'
                    f'align-items:baseline">{spans}</div>')
    caps_top = pad * 0.90
    caps_h = fs * 0.98 * 4
    caps = (f'<div style="position:absolute;left:{pad}px;top:{caps_top}px;width:{w-2*pad}px;'
            f'font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:.98;'
            f'letter-spacing:-.005em;color:{fg}">{"".join(rows)}</div>')

    foot_h = small * 2.4 + pad * 1.05
    band_top = caps_top + caps_h + h * 0.008
    band_h = (h - foot_h) - band_top
    ms = max(24.0, band_h * 1.04 * mark_scale)
    mx = w * mark_cx - ms / 2
    my = band_top + (band_h - ms) / 2
    # w0 is the brush's loaded width at the belly of the pull. v2 used 9.0 and the
    # marks read as thin scratches next to the reference's inked strokes.
    mark = (f'<div style="position:absolute;left:{mx}px;top:{my}px;width:{ms}px;height:{ms}px;'
            f'z-index:2">'
            f'{sh.ink_mark(sh.brush_asterisk(strokes=strokes, R=46, w0=13.5, w1=1.3, seed=seed), fill=fg, size=ms)}'
            f'</div>')

    f1 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*1.48}px;width:{w-2*pad}px;'
          f'font-family:var(--d);font-weight:900;font-size:{small}px;letter-spacing:.012em;'
          f'color:{fg}">{FOOT_1}</div>')
    f2 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.62}px;width:{w-2*pad}px;'
          f'display:flex;justify-content:space-between;font-family:var(--d);font-weight:900;'
          f'font-size:{small}px;letter-spacing:.012em;color:{fg}">'
          f'<span>{FOOT_2L}</span><span>{FOOT_2R}</span></div>')
    return card(x, y, w, h, bg, z) + caps + mark + f1 + f2 + "</div>", ms


def mark_card(x, y, w, h, bg, fg, z=6):
    pad = w * 0.075
    fs = w * 0.225
    small = w * 0.036
    words = "".join(f"<span>{t}</span>" for t in RHYTHM)
    return (card(x, y, w, h, bg, z)
            + f'<div style="position:absolute;left:{pad}px;top:{h*0.10}px;width:{w-2*pad}px;'
              f'font-family:var(--s);font-size:{fs}px;line-height:.9;letter-spacing:-.012em;'
              f'color:{fg};text-align:center">Aqua<br>Terra.</div>'
            + f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.78}px;width:{w-2*pad}px;'
              f'display:flex;justify-content:space-between;font-family:var(--s);'
              f'font-size:{small}px;color:{fg}">{words}</div>'
            + "</div>")


async def main():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')
    x0, x1 = BX0, BX0 + CW + GUT
    y0, y1 = BY0, BY0 + CH + GUT
    # BR shares the measured right edge and gains its extra width to the LEFT
    br_x, br_w = x1 - BR_EXTRA, CW + BR_EXTRA

    tl, m1 = caps_card(x0, y0, CW, CH, CREAM, BLUE, strokes=4, seed=3,
                       mark_cx=0.50, mark_scale=0.92)
    P.append(tl); els.append(("tl", x0, y0, CW, CH))
    P.append(mark_card(x1, y0, CW, CH, BLUE, CREAM)); els.append(("tr", x1, y0, CW, CH))
    P.append(mark_card(x0, y1, CW, CH, ORANGE, INK)); els.append(("bl", x0, y1, CW, CH))
    br, m2 = caps_card(br_x, y1, br_w, CH, CREAM, INK, strokes=5, seed=11,
                       mark_cx=0.40, mark_scale=1.18)
    P.append(br); els.append(("br", br_x, y1, br_w, CH))

    html = B.page(W, H, INK, "".join(P), grain=False)
    lay.preflight(W, H, els, html=html, page_bg=INK, core=core)
    async with B.session():
        await B.render(html, f"{OUT}/v3.png", W, H, elements=els)
    print(f"  -> {OUT}/v3.png")
    print(f"  cards {CW:.0f}x{CH:.0f} (aspect {CW/CH:.2f}) | "
          f"bbox x {x0/W:.3f}..{(br_x+br_w)/W:.3f}  y {y0/H:.3f}..{(y1+CH)/H:.3f}")
    print(f"  marks TL {m1:.0f}px / BR {m2:.0f}px (BR larger, as the reference)")

asyncio.run(main())
