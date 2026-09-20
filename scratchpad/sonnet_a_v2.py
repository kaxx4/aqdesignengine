"""
WORKFLOW B (bespoke primitives) -- but NOT a reference recreation. v2.

Fresh-content brief: "AquaTerra ran 120 distribution drives since 2021. The
poster should make that number feel like sustained effort, not a statistic."

v1 looking-gate findings (out/sonnet_test/A.png), per CLAUDE.md section 3:
  - preview.critique: flat_dominant (cream >52%), fill=0.36 (borderline sparse),
    TR quadrant fill=0.10 (near-dead).
  - By eye: the grid was centered inside its own column and left a ~150px dead
    strip on the right (grid was sized off the HEIGHT budget, so the width
    budget went unused); the top-right quadrant had nothing in it but the small
    date chip.
v2 fixes, in the order CLAUDE.md's craft rule prefers (scale existing elements
up before adding filler):
  1. grid now SPREADS to fill the full available width exactly (extra
     horizontal gap absorbs the slack instead of sitting outside the grid as
     empty margin) -- same cell count/size, no new object.
  2. headline block tightened a little (smaller sizes, tighter gaps) to buy
     back vertical room for the grid without shrinking it.
  3. ONE new element, thematically justified rather than pure filler: a small
     "plus" (aid-cross) doodle in the top-right dead zone below the date chip
     -- relief/aid iconography, not a random shape.
"""
import asyncio, os, sys, importlib.util

# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core")
B = load("build")
dd = load("doodles")
lay = load("layout")

W, H = core.SIZES["feed"]          # 1080x1350 -- feed is NOT taller than this
M = 64
A = core.ACCENTS                    # A[0..6]: pink,mint,lemon,tomato,sky,grape,teal
INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER

HERO = core.DEPT["welfare"]         # mint -- relief/distribution reads as welfare dept
YEAR_ACCENTS = [A[1], A[4], A[2], A[5], A[3]]     # mint, sky, lemon, grape, tomato
YEARS = ["2021", "2022", "2023", "2024", "2025"]

OUT_DIR = "out/sonnet_test"
os.makedirs(OUT_DIR, exist_ok=True)


async def main():
    elements = []
    P = []

    # ---------- background ----------
    P.append('<div style="position:absolute;inset:0;background:var(--bg)"></div>')

    # ---------- logo (top-left) ----------
    P.append(B.logo())
    elements.append(("logo", M, 56, 190, 32))

    # ---------- eyebrow, BELOW the logo (not the same row -- avoids collision) ----------
    eyebrow_color = core.on_cream(HERO, size_px=18, bold=True)
    EYEBROW_Y = 112
    P.append(B.eyebrow("FOOD & RELIEF DISTRIBUTION", eyebrow_color, EYEBROW_Y))
    elements.append(("eyebrow", M, EYEBROW_Y, 440, 26))

    # ---------- date-range chip, top-right ----------
    chip_html = B.chip("2021 \u2192 2026", "var(--bg2)", fg=INK, rot=-4)
    CHIP_W, CHIP_Y = 190, 52
    P.append(f'<div style="position:absolute;top:{CHIP_Y}px;right:{M}px;z-index:20">{chip_html}</div>')
    elements.append(("chip", W - M - CHIP_W, CHIP_Y, CHIP_W, 54))

    # ---------- NEW: aid-cross doodle filling the TR dead zone below the chip ----------
    # v1's preview.critique flagged TR fill=0.10 (near dead_quadrant's <0.10 floor).
    # A "plus" reads as an aid/relief cross here -- thematic, not random filler.
    DOOD_SIZE = 118
    dood_x, dood_y = W - M - DOOD_SIZE - 18, CHIP_Y + 74
    P.append(
        f'<div style="position:absolute;left:{dood_x}px;top:{dood_y}px;'
        f'width:{DOOD_SIZE}px;height:{DOOD_SIZE}px;z-index:8">'
        f'{dd.stamp("plus", A[3], rot=-8)}</div>')
    elements.append(("aid_doodle", dood_x, dood_y, DOOD_SIZE, DOOD_SIZE))

    # ---------- measure the headline block BEFORE placing anything (measure, don't guess) ----------
    NUM_SIZE, SUB_SIZE, ITAL_SIZE = 300, 36, 40
    metrics = await B.measure_text([
        {"text": "120", "font": "d", "size": NUM_SIZE, "weight": 900,
         "line_height": 0.78, "transform": "none"},
        {"text": "DISTRIBUTION DRIVES", "font": "d", "size": SUB_SIZE, "weight": 900,
         "transform": "uppercase", "letter_spacing": "0.01em"},
        {"text": "one at a time.", "font": "s", "size": ITAL_SIZE, "weight": 400},
    ])
    num_m, sub_m, ital_m = metrics

    TOP_Y = 160
    num_x, num_y = M, TOP_Y
    P.append(
        f'<div style="position:absolute;top:{num_y}px;left:{num_x}px;'
        f'font-family:var(--d);font-weight:900;font-size:{NUM_SIZE}px;line-height:.78;'
        f'color:{HERO};text-shadow:9px 9px 0 {INK};z-index:10">120</div>')
    elements.append(("numeral", num_x, num_y, num_m["ink_w"] + 12, num_m["ink_h"] + 12))

    sub_y = num_y + num_m["ink_h"] + 18
    P.append(
        f'<div style="position:absolute;top:{sub_y}px;left:{num_x}px;'
        f'font-family:var(--d);font-weight:900;font-size:{SUB_SIZE}px;'
        f'letter-spacing:.01em;text-transform:uppercase;color:{INK};z-index:10">'
        f'DISTRIBUTION DRIVES</div>')
    elements.append(("subhead", num_x, sub_y, sub_m["ink_w"], sub_m["ink_h"]))

    ital_color = core.on_cream(HERO, size_px=ITAL_SIZE, bold=False)
    ital_y = sub_y + sub_m["ink_h"] + 6
    P.append(
        f'<div style="position:absolute;top:{ital_y}px;left:{num_x}px;'
        f'font-family:var(--s);font-style:italic;font-weight:400;font-size:{ITAL_SIZE}px;'
        f'color:{ital_color};z-index:10">one at a time.</div>')
    elements.append(("italic", num_x, ital_y, ital_m["ink_w"], ital_m["ink_h"]))

    # ---------- the tally grid: 120 cells, 12 cols x 10 rows, 2 rows per year band ----------
    FOOTER_RESERVE = 104
    grid_top = ital_y + ital_m["ink_h"] + 34
    grid_avail_h = H - FOOTER_RESERVE - grid_top

    COLS, ROWS, VGAP = 12, 10, 8
    LABEL_W, LABEL_GAP = 78, 14
    grid_w_avail = W - 2 * M - LABEL_W - LABEL_GAP
    cell = (grid_avail_h - (ROWS - 1) * VGAP) / ROWS   # height is the binding budget
    cell = max(24, min(cell, (grid_w_avail - (COLS - 1) * 6) / COLS))  # never wider than the page allows
    # spend ALL the width budget as horizontal gap, rather than leaving it as dead
    # margin beside the grid (v1's bug) -- same cell size, no new object.
    hgap = (grid_w_avail - COLS * cell) / (COLS - 1)
    grid_w = COLS * cell + (COLS - 1) * hgap
    grid_h = ROWS * cell + (ROWS - 1) * VGAP
    grid_x = M + LABEL_W + LABEL_GAP
    grid_y = grid_top

    print(f"[layout] measured num_ink_h={num_m['ink_h']} sub_ink_h={sub_m['ink_h']} "
          f"ital_ink_h={ital_m['ink_h']} grid_top={grid_top:.0f} grid_avail_h={grid_avail_h:.0f} "
          f"cell={cell:.1f} hgap={hgap:.1f} grid_w={grid_w:.0f} grid_h={grid_h:.0f} "
          f"grid_right={grid_x+grid_w:.0f} grid_bottom={grid_y+grid_h:.0f}")

    n = 0
    for row in range(ROWS):
        year_i = row // 2
        color = YEAR_ACCENTS[year_i]
        y = grid_y + row * (cell + VGAP)
        if row % 2 == 0:
            P.append(
                f'<div style="position:absolute;left:{M}px;top:{y + cell - 10:.1f}px;'
                f'width:{LABEL_W}px;font-family:var(--m);font-weight:700;font-size:15px;'
                f'letter-spacing:.04em;color:var(--ink3);text-align:right;z-index:10">'
                f'{YEARS[year_i]}</div>')
            elements.append((f"ylabel{year_i}", M, y, LABEL_W, cell * 2 + VGAP))
        for col in range(COLS):
            x = grid_x + col * (cell + hgap)
            P.append(
                f'<div style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;'
                f'width:{cell:.1f}px;height:{cell:.1f}px;background:{color};'
                f'border:3px solid {INK};border-radius:6px;'
                f'box-shadow:{core.hard_shadow("sm")};z-index:6"></div>')
            elements.append((f"cell{n}", x, y, cell, cell))
            n += 1
    assert n == 120, f"expected 120 cells, built {n}"

    # ---------- footer ----------
    P.append(B.cta("\u00b7 one drive at a time, since 2021"))
    elements.append(("footer", M, H - 74, 460, 22))

    inner = "".join(P)
    html = B.page(W, H, "var(--bg)", inner, grain=True)

    pf = lay.preflight(W, H, elements, html=html, page_bg="var(--bg)", core=core,
                        expect_hero=True)
    if not pf["clean"]:
        print("!! preflight NOT clean -- see issues above -- fix before trusting the render")

    async with B.session():
        await B.render(html, f"{OUT_DIR}/A.png", W, H)
    print("done ->", f"{OUT_DIR}/A.png")


asyncio.run(main())
