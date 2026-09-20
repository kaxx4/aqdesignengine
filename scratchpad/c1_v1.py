"""Workflow C — bespoke fresh poster ("3,756 volunteer turnouts logged since 2021"), welfare dept.

Style drawn by design.py (seed 23): STYLE d252704dc5e5f3 — a 2x2-ish block collage (dark headline
band, checkerboard pattern, cream body-copy block) stitched by torn/tape word-strip labels crossing
the seams, with a starburst anchor. Reference: training_samples/reference_posters/
d252704dc5e5f32f202f854401f845fe.jpg ("Relationship Series / IT'S NOT YOU IT'S ME").

Measured (compare.geometry): content bbox ~0..1 both axes (full bleed, ~0 margin), coverage .789,
centroid (0.517,0.581) -- i.e. genuinely full-bleed, weight sits slightly right-and-below center.
Occupancy grid: the top ~35% of the frame is emptier (the dark block's negative space around the
headline), everything below row 5 (~45% down) is near-saturated (checker + body blocks + tape pile).

THIS IS WORKFLOW C, NOT B: the brief is new AQ content, not element-for-element reproduction. I'm
reusing the reference's MECHANISM (block collage + crossing tape strips + starburst anchor) per the
style's `recipe`, built to AQ's own brand rules, not copying its literal words/colours.

Acceptable adaptations vs. the literal reference:
  - Reference uses serif caps for the whole headline AND the whole body paragraph. AQ's brand fonts
    restrict Instrument Serif to <=1 accent word per piece (CLAUDE.md Sec 9) -- so the headline uses
    NeutralFace (the display font) and the body uses Eina (lowercase), with exactly one word set in
    Instrument Serif italic as the piece's one accent word.
  - Palette: reference is pink/blue/red/purple; AQ substitutes its own department colour (mint,
    core.accent_for('welfare')) as the tape-strip accent, plus lemon as the pattern pair, so the
    department semantic (Sec 9) still holds.
  - Reference's tape strips read as one sentence ("IT'S NOT YOU IT'S ME"); AQ's read the same way
    but say something true about the content ("SHOWING / UP AGAIN / AND AGAIN"), never a fabricated
    number (the truth ladder: only the one supplied count, 3,756, appears as a number).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/c1_v1.py
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); shp = load("shapes")
tex = load("tex")

W, H = core.SIZES["feed"]      # 1080x1350
M = 64
MINT = core.accent_for("welfare")     # #1B8A5A -- fixed by department, not chosen
LEMON = core.ACCENTS[2]
PINK = core.ACCENTS[0]
INK = core.INK
CREAM = core.CREAM
BG2 = "#EDE6D0"

TAPE_TEXT_ON_MINT = core.text_on(MINT)   # measured, not assumed -- prints as #0A0A0A

# ---- block rects (x,y,w,h) ----
BLOCK_A = (0, 0, 820, 760)        # dark headline block
STRIP_STRIPE = (820, 0, 80, 760)  # diagonal stripe column
STRIP_CHECK = (900, 0, 180, 760)  # blue/purple-analog checker column (mint/lemon here)
BLOCK_C = (0, 760, 500, 590)      # bottom-left checkerboard (mint/lemon)
BLOCK_D = (500, 760, 580, 590)    # bottom-right cream body-copy block

elements = []   # (label, x, y, w, h) kept in sync with every placed element


async def main():
    # ---- MEASURE TEXT FIRST (CLAUDE.md Sec 6) ----
    measured = await B.measure_text([
        {"text": "3,756", "font": "d", "weight": 900, "size": 300, "letter_spacing": "-2px"},
        {"text": "VOLUNTEER TURNOUTS", "font": "d", "weight": 900, "size": 38, "letter_spacing": "1px", "transform": "uppercase"},
        {"text": "SHOWING", "font": "d", "weight": 900, "size": 58, "letter_spacing": "0px", "transform": "uppercase"},
        {"text": "UP AGAIN", "font": "d", "weight": 900, "size": 58, "letter_spacing": "0px", "transform": "uppercase"},
        {"text": "AND AGAIN", "font": "d", "weight": 900, "size": 50, "letter_spacing": "0px", "transform": "uppercase"},
        {"text": "since 2021, one number keeps climbing — volunteers who turn up for health "
                  "camps, tree drives and relief work, showing up", "font": "e", "weight": 600,
         "size": 32, "line_height": "1.18", "max_width": 476},
        {"text": "again.", "font": "s", "weight": 400, "size": 46},
    ], W, H)
    hero_m, cap_m, t1_m, t2_m, t3_m, body_m, again_m = measured

    # hero number must fit inside block A minus margins (820-64-48=708)
    hero_fit = min(300, 300 * (708 / max(1, hero_m["glyph_w"])))
    # re-measure at the fitted size only if we had to shrink (keeps this deterministic, no guess)
    if hero_fit < 299:
        [hero_m2] = await B.measure_text([
            {"text": "3,756", "font": "d", "weight": 900, "size": hero_fit, "letter_spacing": "-2px"}], W, H)
        hero_m = hero_m2
    hero_size = hero_fit

    parts = []

    # ================= BLOCK A -- dark headline block =================
    ax, ay, aw, ah = BLOCK_A
    parts.append(f'<div style="position:absolute;left:{ax}px;top:{ay}px;width:{aw}px;height:{ah}px;background:{INK};z-index:1"></div>')

    # logo -- pill on dark ground (never white-inverted, Sec 9)
    logo_pill = (f'<div style="position:absolute;left:{M}px;top:52px;background:{CREAM};'
                 f'border-radius:999px;padding:10px 18px;z-index:10;box-shadow:{core.hard_shadow("sm", CREAM)}">'
                 f'<img src="{core.LOGO}" style="height:26px;display:block"></div>')
    parts.append(logo_pill)
    elements.append(("logo_pill", M, 52, 170, 46))

    eyebrow_y = 122
    parts.append(f'<div style="position:absolute;left:{M}px;top:{eyebrow_y}px;font-family:var(--m);'
                 f'font-weight:700;font-size:16px;letter-spacing:.14em;text-transform:uppercase;'
                 f'color:{CREAM};z-index:10">AQUATERRA &mdash; WELFARE</div>')
    elements.append(("eyebrow", M, eyebrow_y, 340, 20))

    hero_y = 210
    parts.append(f'<div style="position:absolute;left:{M-4}px;top:{hero_y}px;font-family:var(--d);'
                 f'font-weight:900;font-size:{hero_size}px;line-height:.82;letter-spacing:-2px;'
                 f'color:{CREAM};z-index:10">3,756</div>')
    elements.append(("hero_number", M - 4, hero_y, hero_m["glyph_w"] + 8, hero_m["ink_h"]))

    cap_y = hero_y + hero_m["h"] + 26
    parts.append(f'<div style="position:absolute;left:{M}px;top:{cap_y}px;font-family:var(--d);'
                 f'font-weight:900;font-size:38px;letter-spacing:1px;text-transform:uppercase;'
                 f'color:{MINT};z-index:10">VOLUNTEER TURNOUTS</div>')
    elements.append(("caption", M, cap_y, cap_m["ink_w"], cap_m["ink_h"]))

    # ================= PATTERN COLUMN (right) =================
    sx, sy, sw, sh = STRIP_STRIPE
    parts.append(f'<div style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;'
                 f'{tex.stripes(color=PINK, bg=CREAM, width=12, gap=12, angle=32)};z-index:1"></div>')
    cx_, cy_, cw_, ch_ = STRIP_CHECK
    parts.append(f'<div style="position:absolute;left:{cx_}px;top:{cy_}px;width:{cw_}px;height:{ch_}px;'
                 f'{tex.checkerboard(c1=MINT, c2=LEMON, cell=30)};z-index:1"></div>')

    # cream starburst anchor at the seam corner (top-right), overlapping block A / pattern column
    star1_d = shp.starburst(points=10, R=48, r=30)
    star1_size = 260
    star1_cx, star1_cy = 800, 130
    parts.append(shp.ink_mark(star1_d, fill=CREAM, size=star1_size, rot=14).replace(
        '<svg ', f'<svg style="position:absolute;left:{star1_cx - star1_size/2}px;top:{star1_cy - star1_size/2}px;z-index:8" '))
    elements.append(("starburst_seam", star1_cx - star1_size * 0.34, star1_cy - star1_size * 0.34, star1_size * 0.68, star1_size * 0.68))

    # ================= TAPE STRIPS crossing the seam =================
    def tape_strip(text, tm, x, y, rot, fs, pad_x=34, pad_y=18):
        w = tm["glyph_w"] + pad_x * 2
        h = tm["glyph_h"] + pad_y * 2
        html = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
               f'background:{MINT};transform:rotate({rot}deg);transform-origin:center center;'
               f'display:flex;align-items:center;justify-content:center;z-index:15;'
               f'box-shadow:{core.hard_shadow("base")}">'
               f'<span style="font-family:var(--d);font-weight:900;font-size:{fs}px;'
               f'letter-spacing:.01em;color:{TAPE_TEXT_ON_MINT};white-space:nowrap">{text}</span></div>')
        return html, w, h

    t1_html, t1_w, t1_h = tape_strip("SHOWING", t1_m, 48, 672, -4, 58)
    parts.append(t1_html)
    elements.append(("tape_showing", 48, 672, t1_w, t1_h))

    t2_html, t2_w, t2_h = tape_strip("UP AGAIN", t2_m, 560, 726, 3, 58)
    parts.append(t2_html)
    elements.append(("tape_upagain", 560, 726, t2_w, t2_h))

    t3_html, t3_w, t3_h = tape_strip("AND AGAIN", t3_m, 48, 800, -3, 50)
    parts.append(t3_html)
    elements.append(("tape_andagain", 48, 800, t3_w, t3_h))

    # ================= BLOCK C -- bottom-left checkerboard, ink starburst anchor =================
    cxb, cyb, cwb, chb = BLOCK_C
    parts.append(f'<div style="position:absolute;left:{cxb}px;top:{cyb}px;width:{cwb}px;height:{chb}px;'
                 f'{tex.checkerboard(c1=PINK, c2=LEMON, cell=34)};z-index:1"></div>')
    star2_d = shp.starburst(points=11, R=48, r=32)
    star2_size = 230
    star2_cx, star2_cy = 250, 1120
    parts.append(shp.ink_mark(star2_d, fill=INK, size=star2_size, rot=-8).replace(
        '<svg ', f'<svg style="position:absolute;left:{star2_cx - star2_size/2}px;top:{star2_cy - star2_size/2}px;z-index:6" '))
    elements.append(("starburst_anchor", star2_cx - star2_size * 0.34, star2_cy - star2_size * 0.34, star2_size * 0.68, star2_size * 0.68))

    # ================= BLOCK D -- bottom-right cream body block =================
    dx, dy, dw, dh = BLOCK_D
    parts.append(f'<div style="position:absolute;left:{dx}px;top:{dy}px;width:{dw}px;height:{dh}px;background:{BG2};z-index:1"></div>')

    body_x, body_y = dx + 52, dy + 96
    body_w = body_m["w"]
    parts.append(f'<div style="position:absolute;left:{body_x}px;top:{body_y}px;width:{body_w}px;'
                 f'font-family:var(--e);font-weight:600;font-size:32px;line-height:1.18;color:{INK}">'
                 f'since 2021, one number keeps climbing &mdash; volunteers who turn up for health '
                 f'camps, tree drives and relief work, showing up '
                 f'<span style="font-family:var(--s);font-style:italic;font-weight:400;font-size:46px;'
                 f'color:{core.ink_of(MINT)}">again.</span></div>')
    elements.append(("body_copy", body_x, body_y, body_w, body_m["h"] + again_m["h"]))

    footer_y = dy + dh - 66
    parts.append(f'<div style="position:absolute;left:{body_x}px;top:{footer_y}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.08em;color:{INK};z-index:10">@ngo.aquaterra</div>')
    elements.append(("footer", body_x, footer_y, 220, 20))

    # ---- assemble ----
    inner = "".join(parts)
    html = B.page(W, H, INK, inner, grain=True)

    color_pairs = [
        ("starburst_seam", CREAM, INK),
        ("starburst_anchor", INK, PINK),
        ("tape_bg", MINT, INK),
        ("hero_number", CREAM, INK),
        ("caption", MINT, INK),
    ]

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=INK, core=core,
                       expect_hero=True, min_hero_frac=0.10,
                       collision_ignore={("starburst_seam", "logo_pill"),
                                         ("tape_showing", "tape_upagain"),
                                         ("tape_upagain", "tape_andagain"),
                                         ("tape_showing", "caption"),
                                         ("tape_showing", "hero_number"),
                                         ("starburst_anchor", "body_copy")})

    os.makedirs("out/session10f", exist_ok=True)
    with open("out/session10f/c1_v1.html", "w", encoding="utf-8") as f:
        f.write(html)
    async with B.session():
        await B.render(html, "out/session10f/c1_v1.png", W, H, elements=elements,
                       color_pairs=color_pairs, page_bg=INK, expect_hero=True)
    print("done -> out/session10f/c1_v1.png")

asyncio.run(main())
