"""Recreation — sample 3d846c78, "Sunday Script" 2x2 brand-card sheet.
Composition description + acceptance checklist: brain/RECREATION_AUDIT.md.

Mechanism: two card layouts printed in four colourways, diagonal pairs matching.
Recognition lives in the JUSTIFIED caps block and the brush mark, not the wordmark.
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
BLUE = core.ACCENTS[4]        # sky, standing in for the reference ultramarine
ORANGE = core.ACCENTS[3]      # tomato, standing in for the reference orange

# ── grid: measured off the reference as fractions of the frame ───────────────
# cards span x 11%..89%, y 29%..72%; the grid sits HIGH, with roughly twice as
# much black below it as above. Card aspect ~1.45:1, small equal gutters.
GX0, GX1 = 0.105 * W, 0.895 * W
GY0 = 0.285 * H
GUT = 0.026 * W
CW = (GX1 - GX0 - GUT) / 2
CH = CW / 1.45
GY1 = GY0 + 2 * CH + GUT
# the reference's bottom-right card is wider and breaks the grid's right edge
BR_EXTRA = 0.040 * W

CARD_SHADOW = "0 10px 26px -8px rgba(0,0,0,.85)"   # the only soft shadow in the piece

CAPS_L = ["KOLKATA", "STUDENT", "WELFARE", "CLIMATE"]
CAPS_R = ["GROWN", "RUN", "CREW", "AND EDUCATION"]
WORDMARK = ("AquaTerra", ".")
RHYTHM = ["Log.", "Return.", "Repeat."]
FOOT_1 = "STUDENT-RUN NON-PROFIT BASED IN KOLKATA"
FOOT_2L, FOOT_2R = "558 LOGGED PROJECTS", "@NGO.AQUATERRA"


def card(x, y, w, h, bg, z=6):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{bg};box-shadow:{CARD_SHADOW};z-index:{z};overflow:hidden">')


def caps_card(x, y, w, h, bg, fg, ast_size, ast_cx, seed, z=6):
    """The 'information' layout: justified caps block, brush mark, two footer lines.

    Justification is done with flex space-between per LINE, not text-align:justify —
    a justified single line collapses to left-aligned in CSS (justify only stretches
    lines that are followed by another line), which would silently kill the whole
    effect the reference is built on.
    """
    pad = w * 0.072
    fs = w * 0.062
    small = w * 0.030
    rows = []
    for i, (l, r) in enumerate(zip(CAPS_L, CAPS_R)):
        # line 3 justifies to THREE words in the reference — keep that rhythm
        parts = ([l] + r.split(" ")) if i == 2 else [l, r]
        spans = "".join(f'<span>{p}</span>' for p in parts)
        rows.append(f'<div style="display:flex;justify-content:space-between;'
                    f'align-items:baseline">{spans}</div>')
    caps = (f'<div style="position:absolute;left:{pad}px;top:{pad*0.92}px;width:{w-2*pad}px;'
            f'font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:.98;'
            f'letter-spacing:-.005em;color:{fg}">{"".join(rows)}</div>')

    ay = pad * 0.92 + fs * 4.15
    mark = (f'<div style="position:absolute;left:{ast_cx - ast_size/2}px;top:{ay}px;'
            f'width:{ast_size}px;height:{ast_size}px;z-index:2">'
            f'{sh.ink_mark(sh.brush_asterisk(arms=8, R=45, w0=7.6, w1=1.5, seed=seed), fill=fg, size=ast_size)}'
            f'</div>')

    f1 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*1.52}px;width:{w-2*pad}px;'
          f'font-family:var(--d);font-weight:900;font-size:{small}px;letter-spacing:.012em;'
          f'color:{fg}">{FOOT_1}</div>')
    f2 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.66}px;width:{w-2*pad}px;'
          f'display:flex;justify-content:space-between;font-family:var(--d);font-weight:900;'
          f'font-size:{small}px;letter-spacing:.012em;color:{fg}">'
          f'<span>{FOOT_2L}</span><span>{FOOT_2R}</span></div>')
    return card(x, y, w, h, bg, z) + caps + mark + f1 + f2 + "</div>"


def mark_card(x, y, w, h, bg, fg, z=6):
    """The 'wordmark' layout: serif name high in the card, three words along the base."""
    pad = w * 0.075
    fs = w * 0.185
    small = w * 0.036
    words = "".join(f'<span>{t}</span>' for t in RHYTHM)
    return (card(x, y, w, h, bg, z)
            + f'<div style="position:absolute;left:{pad}px;top:{h*0.135}px;width:{w-2*pad}px;'
              f'font-family:var(--s);font-size:{fs}px;line-height:.92;letter-spacing:-.012em;'
              f'color:{fg};text-align:center">{WORDMARK[0]}<br>Kolkata{WORDMARK[1]}</div>'
            + f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.8}px;width:{w-2*pad}px;'
              f'display:flex;justify-content:space-between;font-family:var(--s);'
              f'font-size:{small}px;color:{fg}">{words}</div>'
            + "</div>")


async def main():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')

    x0, x1 = GX0, GX0 + CW + GUT
    y0, y1 = GY0, GY0 + CH + GUT

    P.append(caps_card(x0, y0, CW, CH, CREAM, BLUE, CW * 0.30, CW * 0.50, seed=3))
    els.append(("tl", x0, y0, CW, CH))
    P.append(mark_card(x1, y0, CW, CH, BLUE, CREAM))
    els.append(("tr", x1, y0, CW, CH))
    P.append(mark_card(x0, y1, CW, CH, ORANGE, INK))
    els.append(("bl", x0, y1, CW, CH))
    # the reference's BR card is wider and breaks the grid's right edge
    P.append(caps_card(x1, y1, CW + BR_EXTRA, CH, CREAM, INK, CW * 0.40, CW * 0.40, seed=9))
    els.append(("br", x1, y1, CW + BR_EXTRA, CH))

    html = B.page(W, H, INK, "".join(P), grain=False)
    lay.preflight(W, H, els, html=html, page_bg=INK, core=core)
    async with B.session():
        await B.render(html, f"{OUT}/v1.png", W, H, elements=els)
    print(f"  -> {OUT}/v1.png")
    print(f"  grid: cards {CW:.0f}x{CH:.0f} (aspect {CW/CH:.2f}), "
          f"black above {GY0:.0f}px / below {H-GY1:.0f}px")

asyncio.run(main())
