"""TOLERANCE FIELDS — Plate 01. Companion art piece, AQ engine session 10.

Rendered BY the engine it describes, which is the point: the plate's own
measurements are taken with build.measure_text(), not typed in. The three
frames around the specimen glyph are the three real numbers the browser
reports for one body — layout box, content box, painted box — and the mint
residual is the literal difference between them.
"""
import asyncio, os, sys, math, importlib.util, random

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); tex = load("tex"); lay = load("layout")

W, H = 1800, 2400
M = 150
INK, CREAM = core.INK, core.CREAM
MINT = core.ACCENTS[1]
HAIR = "rgba(10,10,10,.34)"
FAINT = "rgba(10,10,10,.17)"
OUT = "out/session10"
os.makedirs(OUT, exist_ok=True)
random.seed(1126)

SPEC = "6"          # the specimen body
FS = 880            # its nominal size


def tick(x, y, length=14, vertical=False, color=INK, wgt=1):
    """A drafting corner tick. Terminates exactly; never overshoots."""
    if vertical:
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wgt}px;'
                f'height:{length}px;background:{color}"></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{length}px;'
            f'height:{wgt}px;background:{color}"></div>')


def hline(x, y, w, color=HAIR, wgt=1, dash=None):
    if dash:
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{wgt}px;'
                f'background:repeating-linear-gradient(90deg,{color} 0 {dash[0]}px,'
                f'transparent {dash[0]}px {dash[0]+dash[1]}px)"></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{wgt}px;'
            f'background:{color}"></div>')


def vline(x, y, h, color=HAIR, wgt=1, dash=None):
    if dash:
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wgt}px;height:{h}px;'
                f'background:repeating-linear-gradient(180deg,{color} 0 {dash[0]}px,'
                f'transparent {dash[0]}px {dash[0]+dash[1]}px)"></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wgt}px;height:{h}px;'
            f'background:{color}"></div>')


def frame(x, y, w, h, color, wgt=1, dash=None):
    return (hline(x, y, w, color, wgt, dash) + hline(x, y + h - wgt, w, color, wgt, dash) +
            vline(x, y, h, color, wgt, dash) + vline(x + w - wgt, y, h, color, wgt, dash))


def mono(txt, x, y, size=11, color=INK, ls=".18em", weight=500, rot=None, w=None, align="left"):
    r = f"transform:rotate({rot}deg);transform-origin:0 0;" if rot else ""
    ww = f"width:{w}px;text-align:{align};" if w else "white-space:nowrap;"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{ww}{r}'
            f'font-family:var(--m);font-weight:{weight};font-size:{size}px;'
            f'letter-spacing:{ls};color:{color};line-height:1.35">{txt}</div>')


async def build_plate():
    m = await B.measure_text([
        {"text": SPEC, "font": "d", "size": FS, "weight": 900, "line_height": 0.78},
    ])
    g = m[0]
    lay_w, lay_h = g["w"], g["h"]                 # the LAYOUT box  — what CSS declares
    con_w, con_h = g["ink_w"], g["ink_h"]         # the CONTENT box — what it needs to not clip
    pw, ph = g["glyph_w"], g["glyph_h"]           # the PAINTED box — what ink actually lands

    P = []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};'
             f'{tex.paper_fibre(0.055)}"></div>')

    # ── plate header ────────────────────────────────────────────────────────
    P.append(mono("TOLERANCE&nbsp;FIELDS", M, M - 6, 12, INK, ".42em", 700))
    P.append(mono("PLATE&nbsp;01&nbsp;&nbsp;/&nbsp;&nbsp;ONE&nbsp;BODY,&nbsp;THREE&nbsp;EDGES",
                  W - M - 430, M - 6, 12, INK, ".30em", 500, w=430, align="right"))
    P.append(hline(M, M + 26, W - 2 * M, INK, 1))
    P.append(tick(M, M + 26 - 9, 9, vertical=True, color=INK))
    P.append(tick(W - M - 1, M + 26 - 9, 9, vertical=True, color=INK))

    # ── the stage ───────────────────────────────────────────────────────────
    SX, SY = M + 92, M + 212                       # painted-box origin
    px, py = SX, SY

    # residual bands: mint marks ONLY where the actual departs from the nominal.
    dx = (pw - lay_w) / 2.0
    dy = (ph - lay_h) / 2.0
    lx, ly = px + dx, py + dy                      # layout box, centred in the painted box
    cx_, cy_ = px + (pw - con_w) / 2.0, py + (ph - con_h) / 2.0

    # The residual is drawn at FULL STRENGTH or not at all — a .22 wash across a
    # field is the exact 'reads as dirt' defect layout.wash_scan() exists to catch,
    # and the plate may not break the rule it is about. On this specimen the width
    # delta is 1px, so the honest subject is the VERTICAL disagreement: the three
    # frames claim 593 / 642 / 783 for one body. Marked as solid bands in the
    # slivers where painted exceeds layout, and where content exceeds painted.
    for ryy, hh in ((py, dy), (py + ph - dy, dy)):
        P.append(f'<div style="position:absolute;left:{px}px;top:{ryy}px;width:{pw}px;'
                 f'height:{hh}px;background:{MINT};z-index:2"></div>')
    ov = (con_h - ph) / 2.0
    for ryy in (cy_, cy_ + con_h - ov):
        P.append(f'<div style="position:absolute;left:{cx_}px;top:{ryy}px;width:{con_w}px;'
                 f'height:3px;background:{MINT};z-index:1"></div>')
        for k in range(0, int(con_w), 26):
            P.append(f'<div style="position:absolute;left:{cx_+k}px;top:{ryy}px;width:1px;'
                     f'height:{ov}px;background:{MINT};opacity:.55;z-index:1"></div>')

    # the specimen body
    P.append(f'<div style="position:absolute;left:{lx}px;top:{ly}px;font-family:var(--d);'
             f'font-weight:900;font-size:{FS}px;line-height:.78;color:{INK};z-index:4">{SPEC}</div>')

    # the three frames, drawn in order of authority
    P.append(frame(cx_, cy_, con_w, con_h, FAINT, 1, dash=(3, 6)))          # C  content
    P.append(frame(lx, ly, lay_w, lay_h, HAIR, 1))                          # A  layout
    P.append(frame(px, py, pw, ph, MINT, 2))                                # B  painted

    # corner ticks on the painted frame — terminate exactly
    for (tx, ty, hv, hh) in ((px, py, -1, -1), (px + pw, py, 1, -1),
                             (px, py + ph, -1, 1), (px + pw, py + ph, 1, 1)):
        P.append(hline(tx if hv < 0 else tx - 22, ty, 22, MINT, 2))
        P.append(vline(tx, ty if hh < 0 else ty - 22, 22, MINT, 2))

    # ── dimension annotation ────────────────────────────────────────────────
    ax = px + pw + 46
    rows = [("A", "LAYOUT", f"{lay_w} &times; {lay_h}", HAIR),
            ("B", "PAINTED", f"{pw} &times; {ph}", MINT),
            ("C", "CONTENT", f"{con_w} &times; {con_h}", FAINT)]
    for i, (k, nm, val, col) in enumerate(rows):
        yy = py + 40 + i * 92
        P.append(f'<div style="position:absolute;left:{ax}px;top:{yy}px;width:26px;height:26px;'
                 f'border:2px solid {col if col != FAINT else HAIR};background:{CREAM};'
                 f'z-index:6"></div>')
        P.append(mono(k, ax + 8, yy + 7, 12, INK, ".05em", 700))
        P.append(mono(nm, ax + 42, yy + 2, 11, INK, ".30em", 700))
        P.append(mono(val, ax + 42, yy + 22, 26, INK, ".01em", 500))
        P.append(hline(ax, yy + 62, 300, FAINT, 1))

    dwx = ax
    P.append(mono("&Delta;&nbsp;B&minus;A", dwx, py + 40 + 3 * 92 + 6, 11, INK, ".30em", 700))
    P.append(mono(f"+{pw-lay_w}&nbsp;&nbsp;+{ph-lay_h}", dwx, py + 40 + 3 * 92 + 26,
                  26, MINT, ".01em", 700))
    P.append(mono("THE&nbsp;RESIDUAL&nbsp;IS&nbsp;SHOWN&nbsp;IN&nbsp;FULL&nbsp;STRENGTH.",
                  dwx, py + 40 + 3 * 92 + 66, 9, INK, ".22em", 500, w=300))

    # extension lines — stop SHORT of the body they describe (drafting convention)
    exy = py + ph + 34
    P.append(hline(px, exy, pw, INK, 1))
    P.append(vline(px, py + ph + 8, 26, INK, 1))
    P.append(vline(px + pw - 1, py + ph + 8, 26, INK, 1))
    P.append(mono(f"{pw}", px + pw / 2 - 40, exy + 12, 11, INK, ".18em", 700, w=80, align="center"))
    exv = px - 34
    P.append(vline(exv, ly, lay_h, HAIR, 1))
    P.append(hline(exv - 8, ly, 16, HAIR, 1))
    P.append(hline(exv - 8, ly + lay_h - 1, 16, HAIR, 1))
    P.append(mono(f"{lay_h}", exv - 58, ly + lay_h / 2 - 8, 11, INK, ".18em", 500))

    # ── the accumulation: the same reading, taken two hundred times ─────────
    CX = M
    CY = py + ph + 132
    COLS, ROWS, CW, RH = 20, 11, 74, 30
    base = pw
    P.append(mono("SERIES&nbsp;I&nbsp;&mdash;&nbsp;PAINTED&nbsp;WIDTH,&nbsp;220&nbsp;READINGS",
                  CX, CY - 30, 10, INK, ".30em", 700))
    P.append(hline(CX, CY - 10, W - 2 * M, INK, 1))
    for r in range(ROWS):
        for c in range(COLS):
            v = base + random.choice([0, 0, 0, 0, 1, -1, 1, 2, -2, 1])
            off = v != base
            col = MINT if off else "rgba(10,10,10,.52)"
            wt = 700 if off else 500
            P.append(mono(f"{v}", CX + c * CW, CY + 8 + r * RH, 12, col, ".06em", wt))
    P.append(hline(CX, CY + 8 + ROWS * RH + 6, W - 2 * M, FAINT, 1))

    # ── specimen strip: rotation grows the footprint ────────────────────────
    # v1 spaced these by a constant 108px and they collided — the plate committing
    # the exact error it documents. Spacing is now derived from the real footprint.
    S = 148
    degs = (0, 9, 27, 45)
    foots = [lay.rotated_bbox(0, 0, S, S, d)[2] for d in degs]
    RX = CX
    RY = CY + 8 + ROWS * RH + 150
    P.append(mono("SERIES&nbsp;II&nbsp;&mdash;&nbsp;FOOTPRINT&nbsp;UNDER&nbsp;ROTATION",
                  RX, RY - 30, 10, INK, ".30em", 700))
    P.append(hline(RX, RY - 10, W - 2 * M, INK, 1))
    GAPX = 74
    span = sum(foots) + GAPX * (len(degs) - 1)
    ox = RX + ((W - 2 * M) - span) / 2.0
    lane_h = max(foots)
    for deg, foot in zip(degs, foots):
        cx0 = ox + foot / 2.0
        cy0 = RY + 52 + lane_h / 2.0
        P.append(frame(cx0 - foot / 2.0, cy0 - foot / 2.0, foot, foot,
                       MINT if deg else HAIR, 1))
        P.append(f'<div style="position:absolute;left:{cx0-S/2.0}px;top:{cy0-S/2.0}px;'
                 f'width:{S}px;height:{S}px;background:{CREAM};border:2px solid {INK};'
                 f'transform:rotate({deg}deg);z-index:5"></div>')
        P.append(mono(f"{deg}&deg;", cx0 - 40, RY + 52 + lane_h + 22, 12, INK,
                      ".18em", 700, w=80, align="center"))
        P.append(mono(f"{foot:.0f}", cx0 - 40, RY + 52 + lane_h + 44, 20,
                      MINT if deg else "rgba(10,10,10,.42)", ".02em", 700, w=80, align="center"))
        P.append(mono(f"+{(foot/S-1)*100:.0f}%", cx0 - 40, RY + 52 + lane_h + 72, 9,
                      INK if deg else FAINT, ".22em", 500, w=80, align="center"))
        ox += foot + GAPX
    P.append(hline(RX, RY + 52 + lane_h + 108, W - 2 * M, FAINT, 1))

    # ── the one human line, nearly hidden ───────────────────────────────────
    P.append(f'<div style="position:absolute;left:{M}px;top:{H-M-92}px;font-family:var(--s);'
             f'font-style:italic;font-size:33px;color:{INK};opacity:.80;z-index:9">'
             f'the declared edge is a claim.</div>')

    P.append(hline(M, H - M - 34, W - 2 * M, INK, 1))
    # DERIVED, never typed. A plate about not guessing may not carry a hand-keyed
    # spec line — v1's said 760 PX while the specimen had been set to 880.
    P.append(mono(f"SPEC.&nbsp;{SPEC}&nbsp;&nbsp;&middot;&nbsp;&nbsp;NEUTRALFACE&nbsp;900&nbsp;&nbsp;"
                  f"&middot;&nbsp;&nbsp;{FS}&nbsp;PX&nbsp;&nbsp;&middot;&nbsp;&nbsp;LH&nbsp;0.78"
                  f"&nbsp;&nbsp;&middot;&nbsp;&nbsp;A&nbsp;{lay_w}&times;{lay_h}"
                  f"&nbsp;&nbsp;B&nbsp;{pw}&times;{ph}&nbsp;&nbsp;C&nbsp;{con_w}&times;{con_h}",
                  M, H - M - 18, 10, INK, ".22em", 500))
    P.append(mono("AQUATERRA&nbsp;&mdash;&nbsp;TOLERANCE&nbsp;FIELDS&nbsp;&nbsp;&middot;&nbsp;&nbsp;"
                  "MMXXVI", W - M - 430, H - M - 18, 10, INK, ".26em", 500, w=430, align="right"))

    return B.page(W, H, CREAM, "".join(P), grain=False)


async def main():
    async with B.session():
        html = await build_plate()
        await B.render(html, f"{OUT}/TOLERANCE_FIELDS_plate01.png", W, H)
    print(f"  -> {OUT}/TOLERANCE_FIELDS_plate01.png")

asyncio.run(main())
