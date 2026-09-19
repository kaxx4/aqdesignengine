"""Recreation — sample 3d846c78, v2.

v1 -> v2, against the acceptance checklist in brain/RECREATION_AUDIT.md:
  1. THE BRUSH MARK WAS A SILHOUETTE COLLAPSE. v1's brush_asterisk drew wedges
     radiating from a shared hub: a solid centre, every edge meeting at one point,
     reading as a clean vector sparkle. The reference mark is four STROKES pulled
     through the middle — tapered at both ends, bowed, crossing rather than
     meeting. shapes.brush_asterisk rewritten; see its docstring.
  2. The mark collided with the footer copy on both cream cards (the gate caught
     the BR one: content 316px in a 285px box). Its size and position are now
     COMPUTED from the free band between the caps block and the footer.
  3. The grid sat centred; the reference sits HIGH, with roughly twice as much
     black below it as above.
  4. Wordmark was "AquaTerra / Kolkata." — the reference stacks the two words of
     the NAME ("Sunday / Script."), so: "Aqua / Terra."
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

# grid, measured off the reference: x 10.5%..89.5%, sitting HIGH
GX0, GX1 = 0.105 * W, 0.895 * W
GUT = 0.026 * W
CW = (GX1 - GX0 - GUT) / 2
CH = CW / 1.45
BR_EXTRA = 0.040 * W
# the reference has ~2x as much black below the grid as above it
SPARE = H - (2 * CH + GUT)
GY0 = SPARE * 0.34
GY1 = GY0 + 2 * CH + GUT

CARD_SHADOW = "0 10px 26px -8px rgba(0,0,0,.85)"

CAPS_L = ["KOLKATA", "STUDENT", "WELFARE", "CLIMATE"]
CAPS_R = ["GROWN", "RUN", "CREW", "AND EDUCATION"]
RHYTHM = ["Log.", "Return.", "Repeat."]
FOOT_1 = "STUDENT-RUN NON-PROFIT BASED IN KOLKATA"
FOOT_2L, FOOT_2R = "558 LOGGED PROJECTS", "@NGO.AQUATERRA"


def card(x, y, w, h, bg, z=6):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{bg};box-shadow:{CARD_SHADOW};z-index:{z};overflow:hidden">')


def caps_card(x, y, w, h, bg, fg, strokes, seed, mark_cx_frac=0.5, z=6):
    pad = w * 0.072
    fs = w * 0.062
    small = w * 0.030
    rows = []
    for i, (l, r) in enumerate(zip(CAPS_L, CAPS_R)):
        parts = ([l] + r.split(" ")) if i == 2 else [l, r]
        spans = "".join(f"<span>{p}</span>" for p in parts)
        rows.append('<div style="display:flex;justify-content:space-between;'
                    f'align-items:baseline">{spans}</div>')
    caps_top = pad * 0.92
    caps_h = fs * 0.98 * 4
    caps = (f'<div style="position:absolute;left:{pad}px;top:{caps_top}px;width:{w-2*pad}px;'
            f'font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:.98;'
            f'letter-spacing:-.005em;color:{fg}">{"".join(rows)}</div>')

    # the mark lives in the FREE BAND between the caps block and the footer, and is
    # sized to it. v1 sized it as a fraction of card width and it struck through the
    # footer copy on both cream cards.
    foot_h = small * 2.4 + pad * 1.1
    band_top = caps_top + caps_h + h * 0.012
    band_h = (h - foot_h) - band_top
    ms = max(24.0, band_h * 0.96)
    mx = w * mark_cx_frac - ms / 2
    my = band_top + (band_h - ms) / 2
    mark = (f'<div style="position:absolute;left:{mx}px;top:{my}px;width:{ms}px;height:{ms}px;'
            f'z-index:2">'
            f'{sh.ink_mark(sh.brush_asterisk(strokes=strokes, R=45, w0=9.0, w1=1.2, seed=seed), fill=fg, size=ms)}'
            f'</div>')

    f1 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*1.52}px;width:{w-2*pad}px;'
          f'font-family:var(--d);font-weight:900;font-size:{small}px;letter-spacing:.012em;'
          f'color:{fg}">{FOOT_1}</div>')
    f2 = (f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.66}px;width:{w-2*pad}px;'
          f'display:flex;justify-content:space-between;font-family:var(--d);font-weight:900;'
          f'font-size:{small}px;letter-spacing:.012em;color:{fg}">'
          f'<span>{FOOT_2L}</span><span>{FOOT_2R}</span></div>')
    return card(x, y, w, h, bg, z) + caps + mark + f1 + f2 + "</div>", (band_top, band_h, ms)


def mark_card(x, y, w, h, bg, fg, z=6):
    pad = w * 0.075
    fs = w * 0.215
    small = w * 0.036
    words = "".join(f"<span>{t}</span>" for t in RHYTHM)
    return (card(x, y, w, h, bg, z)
            + f'<div style="position:absolute;left:{pad}px;top:{h*0.115}px;width:{w-2*pad}px;'
              f'font-family:var(--s);font-size:{fs}px;line-height:.9;letter-spacing:-.012em;'
              f'color:{fg};text-align:center">Aqua<br>Terra.</div>'
            + f'<div style="position:absolute;left:{pad}px;bottom:{pad*0.8}px;width:{w-2*pad}px;'
              f'display:flex;justify-content:space-between;font-family:var(--s);'
              f'font-size:{small}px;color:{fg}">{words}</div>'
            + "</div>")


async def main():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')
    x0, x1 = GX0, GX0 + CW + GUT
    y0, y1 = GY0, GY0 + CH + GUT

    tl, m1 = caps_card(x0, y0, CW, CH, CREAM, BLUE, strokes=4, seed=3, mark_cx_frac=0.50)
    P.append(tl); els.append(("tl", x0, y0, CW, CH))
    P.append(mark_card(x1, y0, CW, CH, BLUE, CREAM)); els.append(("tr", x1, y0, CW, CH))
    P.append(mark_card(x0, y1, CW, CH, ORANGE, INK)); els.append(("bl", x0, y1, CW, CH))
    br, m2 = caps_card(x1, y1, CW + BR_EXTRA, CH, CREAM, INK, strokes=5, seed=11,
                       mark_cx_frac=0.40)
    P.append(br); els.append(("br", x1, y1, CW + BR_EXTRA, CH))

    html = B.page(W, H, INK, "".join(P), grain=False)
    lay.preflight(W, H, els, html=html, page_bg=INK, core=core)
    async with B.session():
        await B.render(html, f"{OUT}/v2.png", W, H, elements=els)
    print(f"  -> {OUT}/v2.png")
    print(f"  cards {CW:.0f}x{CH:.0f} (aspect {CW/CH:.2f}) | "
          f"black above {GY0:.0f} / below {H-GY1:.0f} (ref ~1:2)")
    print(f"  TL mark band {m1[1]:.0f}px -> mark {m1[2]:.0f}px | "
          f"BR band {m2[1]:.0f}px -> mark {m2[2]:.0f}px")

asyncio.run(main())
