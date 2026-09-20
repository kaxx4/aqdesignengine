import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
tex = load("tex"); shapes = load("shapes")

W, H = core.SIZES["li_square"]   # 1200x1200 -- LinkedIn square, per design.py's draw
M = 64
A = core.ACCENTS
TEAL = core.accent_for("ops")            # #0E7C86, fixed by department rule (CLAUDE.md sec9)
LEMON = A[2]; PINK = A[0]
CREAM = core.CREAM

# ---- copy (VOICE.md sec2 truth ladder + sec4 audience=corporate/CSR + sec5 linkedin channel +
#       sec6 intent=recap: count it, then name who did it -> ends on attribution) ----
HERO_NUM = "3,756"
QUALIFIER = "VOLUNTEER TURNOUTS"
TAG_LEFT = "SINCE 2021"
TAG_RIGHT = "COUNTED"
EYEBROW = "VOLUNTEER OPERATIONS"
BODY = ("AquaTerra volunteers have logged 3,756 turnouts since 2021, each one counted "
        "at the time it happened. The number tracks visits, not unique people: one "
        "volunteer can return many times, and many do.")
ATTRIBUTION = "Logged by the volunteers who showed up for it."
DEPT_TAG = "OPS"
HANDLE = "@ngo.aquaterra"

elements = []
color_pairs = []
text_pairs = []

async def main():
    # ---- MEASURE TEXT FIRST (CLAUDE.md sec6) ----
    m = await B.measure_text([
        dict(text=HERO_NUM, font="d", weight=900, size=130),
        dict(text=QUALIFIER, font="m", weight=700, size=24, letter_spacing="0.12em"),
        dict(text=TAG_LEFT, font="d", weight=800, size=40),
        dict(text=TAG_RIGHT, font="d", weight=800, size=40),
        dict(text=BODY, font="e", weight=500, size=38, line_height=1.4, max_width=1040),
        dict(text=ATTRIBUTION, font="e", weight=700, size=30, line_height=1.3, max_width=1040),
        dict(text=EYEBROW, font="m", weight=700, size=16, letter_spacing="0.14em"),
        dict(text=HANDLE, font="m", weight=700, size=15),
        dict(text=DEPT_TAG, font="m", weight=700, size=14, letter_spacing="0.1em"),
    ], W, H)
    m_num, m_qual, m_tagL, m_tagR, m_body, m_attr, m_eye, m_handle, m_dept = m

    # ================= TOP BLOCK (teal, torn bottom edge, ruled grid) =================
    TOP_H = 680
    top_block = (f'<div style="position:absolute;top:0;left:0;width:{W}px;height:{TOP_H}px;'
                 f'background-color:{TEAL};background-image:'
                 f'repeating-linear-gradient(0deg,{core.INK}22 0 2px,transparent 2px 60px),'
                 f'repeating-linear-gradient(90deg,{core.INK}22 0 2px,transparent 2px 60px);'
                 f'{tex.torn("bottom")};z-index:1"></div>')
    elements.append(("top_block", 0, 0, W, TOP_H))
    color_pairs.append(("top_block", TEAL, "var(--bg)"))
    CONTAINERS = ("top_block",)   # children absolutely positioned INSIDE the teal block are
                                  # contained, not colliding with it (layout.collision_check docstring)

    # decorative burst, top-right corner of the teal block.
    # v1 measured this at 96x96 but reconcile.measure_dom reported the drawn <svg> as 114x114 --
    # doodles._svg pins width/height to the wrapper's OWN box (100%), so the 18px gap is NOT the
    # doodle over-drawing; it is the div's border-box vs the svg's content-box rounding at 2x
    # device-scale. Declaring the box reconcile actually measured, centered on the same point.
    burst = dd.stamp("burst", PINK, rot=12)
    BURST_CX, BURST_CY, BURST_DRAWN = 1058, 108, 114
    bx, by = BURST_CX - BURST_DRAWN / 2, BURST_CY - BURST_DRAWN / 2
    burst_div = f'<div style="position:absolute;top:{by}px;left:{bx}px;width:96px;height:96px;z-index:5">{burst}</div>'
    elements.append(("burst_doodle", bx, by, BURST_DRAWN, BURST_DRAWN))
    color_pairs.append(("burst_doodle", PINK, TEAL))

    # ---- logo, top-left, in a cream pill (house rule sec9: pill on dark/photo grounds) ----
    logo_pill = (f'<div style="position:absolute;top:40px;left:{M}px;width:186px;height:64px;'
                 f'background:{CREAM};border-radius:999px;border:4px solid {core.INK};'
                 f'box-shadow:{core.hard_shadow("lg")};display:flex;align-items:center;'
                 f'justify-content:center;z-index:20"><img src="{core.LOGO}" style="height:34px"></div>')
    elements.append(("logo_pill", M, 40, 186, 64))
    color_pairs.append(("logo_pill", CREAM, TEAL))

    # ================= GIANT PILL CTA (holds the number AND its qualifier together) ====
    PILL_W = max(720, int(m_num["glyph_w"] + 140), int(m_qual["text_w"] + 140))
    PILL_H = 240
    PILL_X = (W - PILL_W) // 2
    PILL_Y = 250
    # v1: flex `gap:6px` + hero line-height 0.78 let the comma's descender touch "VOLUNTEER".
    # Widen the gap and give the qualifier its own top margin instead of trusting flex gap alone.
    pill = (f'<div style="position:absolute;top:{PILL_Y}px;left:{PILL_X}px;width:{PILL_W}px;'
            f'height:{PILL_H}px;background:{LEMON};border-radius:999px;border:6px solid {core.INK};'
            f'box-shadow:{core.hard_shadow("xl")};z-index:10;display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center">'
            f'<span style="font-family:var(--d);font-weight:900;font-size:126px;line-height:0.9;'
            f'color:{core.INK}">{HERO_NUM}</span>'
            f'<span style="font-family:var(--m);font-weight:700;font-size:24px;letter-spacing:0.12em;'
            f'color:{core.INK};margin-top:22px">{QUALIFIER}</span></div>')
    elements.append(("giant_pill", PILL_X, PILL_Y, PILL_W, PILL_H))
    color_pairs.append(("giant_pill", LEMON, TEAL))
    text_pairs.append(("hero_num", core.INK, LEMON, 126, True))
    text_pairs.append(("qualifier", core.INK, LEMON, 24, True))

    # ================= TWO TAG BADGES AT THE PILL'S SHOULDERS =========================
    tag_path = shapes.tag(w=100, h=44)
    box_l, fits_l = shapes.fit_font(m_tagL["text_w"], 40, "tag", 170)
    box_r, fits_r = shapes.fit_font(m_tagR["text_w"], 40, "tag", 170)
    lbl_l = shapes.label(TAG_LEFT, size=box_l, y=30, fill=core.INK, weight=800)
    lbl_r = shapes.label(TAG_RIGHT, size=box_r, y=30, fill=core.INK, weight=800)
    badge_l = shapes.sticker(tag_path, CREAM, size=170, inner=lbl_l, detail="none")
    badge_r = shapes.sticker(tag_path, CREAM, size=170, inner=lbl_r, detail="none")
    TAGL_X, TAGL_Y, TAGL_ROT = 40, 305, -8
    TAGR_X, TAGR_Y, TAGR_ROT = 990, 305, 8
    badge_l_div = (f'<div style="position:absolute;top:{TAGL_Y}px;left:{TAGL_X}px;'
                   f'transform:rotate({TAGL_ROT}deg);z-index:15">{badge_l}</div>')
    badge_r_div = (f'<div style="position:absolute;top:{TAGR_Y}px;left:{TAGR_X}px;'
                   f'transform:rotate({TAGR_ROT}deg);z-index:15">{badge_r}</div>')
    elements.append(("tag_since2021", *lay.rotated_bbox(TAGL_X, TAGL_Y, 170, 170, TAGL_ROT)))
    elements.append(("tag_counted", *lay.rotated_bbox(TAGR_X, TAGR_Y, 170, 170, TAGR_ROT)))
    color_pairs.append(("tag_since2021", CREAM, TEAL))
    color_pairs.append(("tag_counted", CREAM, TEAL))
    if not fits_l:
        print(f"[g3_v2] WARN: TAG_LEFT does not fit its badge (box {box_l})")
    if not fits_r:
        print(f"[g3_v2] WARN: TAG_RIGHT does not fit its badge (box {box_r})")

    # ================= PAPER PANEL (cream, ink-on-paper only per drawn style's restraint) ==
    # v1 left a dead zone between body copy and the footer (preview.critique-shaped flaw,
    # caught by eye). Fixed with genuine content, not filler: the recap intent (VOICE.md sec6)
    # is supposed to END on attribution anyway ("count it, then name who did it") -- v1 simply
    # never wrote that half of the intent shape.
    EYEBROW_Y = TOP_H + 56
    eyebrow_el = B.eyebrow(EYEBROW, core.ink_of(TEAL), EYEBROW_Y)
    elements.append(("eyebrow", M, EYEBROW_Y, m_eye["w"] + 22, m_eye["h"]))
    text_pairs.append(("eyebrow", core.ink_of(TEAL), "var(--bg)", 16, True))

    BODY_Y = EYEBROW_Y + 64
    body_el = (f'<div class="measure" data-tag="body" style="position:absolute;top:{BODY_Y}px;'
               f'left:{M}px;width:1040px;font-family:var(--e);font-weight:500;font-size:38px;'
               f'line-height:1.4;color:{core.INK};z-index:6">{BODY}</div>')
    elements.append(("body", M, BODY_Y, 1040, m_body["h"]))
    text_pairs.append(("body", core.INK, "var(--bg)", 38, False))

    ATTR_Y = BODY_Y + m_body["h"] + 56
    attr_el = (f'<div class="measure" data-tag="attribution" style="position:absolute;top:{ATTR_Y}px;'
               f'left:{M}px;width:1040px;font-family:var(--e);font-weight:700;font-size:30px;'
               f'line-height:1.3;color:{core.ink_of(TEAL)};z-index:6">{ATTRIBUTION}</div>')
    elements.append(("attribution", M, ATTR_Y, 1040, m_attr["h"]))
    text_pairs.append(("attribution", core.ink_of(TEAL), "var(--bg)", 30, True))

    footer_el = (f'<span style="position:absolute;bottom:56px;left:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:0.04em;color:var(--ink3);'
                 f'z-index:20">{HANDLE}</span>')
    elements.append(("footer", M, H - 56 - m_handle["h"], m_handle["w"], m_handle["h"]))
    text_pairs.append(("footer", "var(--ink3)", "var(--bg)", 15, True))

    dept_dot = (f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
                f'background:{TEAL};margin-right:8px"></span>')
    dept_x = W - M - m_dept["w"] - 22
    dept_el = (f'<span style="position:absolute;bottom:58px;left:{dept_x}px;font-family:var(--m);'
               f'font-weight:700;font-size:14px;letter-spacing:0.1em;color:{core.ink_of(TEAL)};'
               f'z-index:20;display:flex;align-items:center">{dept_dot}{DEPT_TAG}</span>')
    elements.append(("dept_tag", dept_x, H - 58 - m_dept["h"], m_dept["w"] + 22, m_dept["h"]))
    text_pairs.append(("dept_tag", core.ink_of(TEAL), "var(--bg)", 14, True))

    print(f"[g3_v2] ATTR_Y+h = {ATTR_Y + m_attr['h']}, footer top = {H-56-m_handle['h']} "
          f"(must clear, else attribution collides with the footer)")

    inner = "".join([
        top_block, burst_div, logo_pill, pill, badge_l_div, badge_r_div,
        eyebrow_el, body_el, attr_el, footer_el, dept_el,
    ])
    html = B.page(W, H, "var(--bg)", inner, grain=False)

    os.makedirs("out/session10g", exist_ok=True)
    await B.render(
        html, "out/session10g/g3_v2.png", W, H,
        elements=elements, color_pairs=color_pairs, page_bg="var(--bg)",
        expect_hero=True, text_pairs=text_pairs, containers=CONTAINERS,
        collision_ignore={("giant_pill", "tag_since2021"), ("giant_pill", "tag_counted")},
    )
    print("done -> out/session10g/g3_v2.png")

asyncio.run(main())
