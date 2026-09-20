import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
sh = load("shapes"); tex = load("tex")

W, H = core.SIZES["li_square"]     # 1200x1200 — LinkedIn square, per design.py's draw
M = 64
ACCENT = core.accent_for("ops")            # "#0E7C86" teal — fixed by department, never rotated
ACCENT_INK = core.ink_of(ACCENT)           # "#0E6E77" — legible small-type partner on cream
INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
PANEL_H = 560                              # ~46.7% of 1200 — re-solved for a square frame from
                                            # the reference's 45%-top-block mechanism (1.556:1 ref
                                            # does not transfer its fractions directly, per design.py's
                                            # own re-proportion warning)

elements = []   # (label, x, y, w, h) — kept in sync with every div below

async def main():
    # ---- MEASURE TEXT FIRST (CLAUDE.md section 6) ----
    items = [
        {"text": "3,756", "font": "d", "size": 168, "weight": 900},
        {"text": "volunteer turnouts", "font": "e", "size": 30, "weight": 600, "transform": "lowercase"},
        {"text": "since 2021", "font": "m", "size": 20, "weight": 700, "transform": "lowercase"},
        {"text": "ops log", "font": "m", "size": 20, "weight": 700, "transform": "lowercase"},
        {"text": "Every turnout is logged the day it happens, not tallied at year end. "
                  "Some of this count is one volunteer, back again.",
         "font": "e", "size": 34, "weight": 600, "max_width": 520, "line_height": 1.28},
        {"text": "ops · aquaterra", "font": "m", "size": 17, "weight": 700, "transform": "lowercase"},
        {"text": "@ngo.aquaterra", "font": "m", "size": 17, "weight": 700},
    ]
    m = await B.measure_text(items, W, H)
    (num_m, lab_m, tag1_m, tag2_m, body_m, dept_m, foot_m) = m
    print("MEASURED:", m)

    # ---- central stat pill, sized from the MEASURED numeral + label ----
    pill_w = max(num_m["glyph_w"], lab_m["ink_w"]) + 160
    pill_h = num_m["ink_h"] + lab_m["h"] + 90
    pill_x = (W - pill_w) / 2
    pill_y = 150
    elements.append(("stat_pill", pill_x, pill_y, pill_w, pill_h))

    num_x = pill_x + (pill_w - num_m["glyph_w"]) / 2
    num_y = pill_y + 38
    elements.append(("hero_num", num_x, num_y, num_m["glyph_w"], num_m["glyph_h"]))

    lab_x = pill_x + (pill_w - lab_m["ink_w"]) / 2
    lab_y = num_y + num_m["glyph_h"] + 14
    elements.append(("hero_label", lab_x, lab_y, lab_m["ink_w"], lab_m["h"]))

    # ---- two small badges tucked at the pill's shoulders (reference mechanism) ----
    tag1_w, tag1_h = tag1_m["ink_w"] + 44, 48
    tag1_x = pill_x - tag1_w * 0.45
    tag1_y = pill_y + 14
    elements.append(("tag_since", tag1_x, tag1_y, tag1_w, tag1_h))

    tag2_d = 110  # circular badge diameter
    tag2_x = pill_x + pill_w - tag2_d * 0.55
    tag2_y = pill_y - tag2_d * 0.22
    elements.append(("tag_ops", tag2_x, tag2_y, tag2_d, tag2_d))

    # ---- logo, top-left on the dark panel: pill treatment (house rule, section 9) ----
    logo_w, logo_h = 176, 56
    elements.append(("logo_pill", M, 40, logo_w, logo_h))

    # ---- body copy, right margin, below the torn seam ----
    body_w = 520
    body_x = W - M - body_w
    body_y = 700
    elements.append(("body", body_x, body_y, body_w, body_m["h"]))

    # ---- dept tag bottom-left / handle bottom-right ----
    dept_x, dept_y = M, H - 70
    elements.append(("dept_tag", dept_x, dept_y, dept_m["ink_w"], dept_m["h"]))
    foot_x = W - M - foot_m["ink_w"]
    foot_y = H - 70
    elements.append(("footer", foot_x, foot_y, foot_m["ink_w"], foot_m["h"]))

    # ================= build the HTML =================
    grid_bg = tex.grid_lines(color=INK, step=48, width=2, opacity=0.35)
    panel = (f'<div style="position:absolute;top:0;left:0;width:{W}px;height:{PANEL_H}px;'
             f'background:{ACCENT};{tex.torn("bottom")};z-index:1">'
             f'<div style="position:absolute;inset:0;{grid_bg}"></div>'
             f'</div>')

    logo_pill = (f'<div style="position:absolute;left:{M}px;top:40px;width:{logo_w}px;height:{logo_h}px;'
                 f'background:{PAPER};border-radius:{core.RADII["pill"]}px;'
                 f'border:4px solid {INK};box-shadow:{core.hard_shadow("base")};'
                 f'display:flex;align-items:center;justify-content:center;z-index:20">'
                 f'<img src="{core.LOGO}" style="height:28px"></div>')

    pill = (f'<div style="position:absolute;left:{pill_x}px;top:{pill_y}px;width:{pill_w}px;height:{pill_h}px;'
            f'background:{CREAM};border-radius:{core.RADII["pill"]}px;border:6px solid {INK};'
            f'box-shadow:{core.hard_shadow("xl")};z-index:10"></div>')
    hero_num = (f'<div style="position:absolute;left:{pill_x}px;top:{num_y}px;width:{pill_w}px;'
                f'font-family:var(--d);font-weight:900;font-size:168px;line-height:0.86;text-align:center;'
                f'color:{INK};z-index:12">3,756</div>')
    hero_label = (f'<div style="position:absolute;left:{pill_x}px;top:{lab_y}px;width:{pill_w}px;'
                  f'font-family:var(--e);font-weight:600;font-size:30px;text-align:center;'
                  f'text-transform:lowercase;color:{ACCENT_INK};z-index:12">volunteer turnouts</div>')

    tag_since = (f'<div style="position:absolute;left:{tag1_x}px;top:{tag1_y}px;width:{tag1_w}px;height:{tag1_h}px;'
                 f'background:{core.ACCENTS[2]};border-radius:10px;border:4px solid {INK};'
                 f'box-shadow:{core.hard_shadow("base")};transform:rotate(-7deg);'
                 f'display:flex;align-items:center;justify-content:center;z-index:15">'
                 f'<span style="font-family:var(--m);font-weight:700;font-size:20px;'
                 f'text-transform:lowercase;color:{core.ink_of(core.ACCENTS[2])}">since 2021</span></div>')

    tag_ops = (f'<div style="position:absolute;left:{tag2_x}px;top:{tag2_y}px;width:{tag2_d}px;height:{tag2_d}px;'
               f'z-index:15;transform:rotate(9deg)">{dd.stamp("burst", core.ACCENTS[0], rot=0)}'
               f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
               f'transform:rotate(-9deg)"><span style="font-family:var(--m);font-weight:700;font-size:15px;'
               f'text-transform:lowercase;color:{core.ink_of(core.ACCENTS[0])}">ops log</span></div></div>')

    body = (f'<div style="position:absolute;left:{body_x}px;top:{body_y}px;width:{body_w}px;'
            f'font-family:var(--e);font-weight:600;font-size:34px;line-height:1.28;text-align:right;'
            f'color:{INK}">Every turnout is logged the day it happens, not tallied at year end. '
            f'Some of this count is one volunteer, back again.</div>')

    dept_tag = (f'<span style="position:absolute;left:{dept_x}px;top:{dept_y}px;font-family:var(--m);'
                f'font-weight:700;font-size:17px;letter-spacing:.04em;text-transform:lowercase;'
                f'color:{ACCENT_INK};z-index:20">ops · aquaterra</span>')
    footer = (f'<span style="position:absolute;left:{foot_x}px;top:{foot_y}px;font-family:var(--m);'
              f'font-weight:700;font-size:17px;letter-spacing:.04em;color:{core.INK}88;z-index:20">'
              f'@ngo.aquaterra</span>')

    inner = "".join([
        f'<div style="position:absolute;inset:0;background:{CREAM}"></div>',
        panel, tag_since, tag_ops, pill, hero_num, hero_label, logo_pill,
        body, dept_tag, footer,
    ])
    html = B.page(W, H, CREAM, inner, grain=True)

    color_pairs = [
        ("panel_bg", ACCENT, CREAM),
        ("pill_bg", CREAM, ACCENT),
        ("tag_since_bg", core.ACCENTS[2], ACCENT),
        ("tag_ops_bg", core.ACCENTS[0], ACCENT),
    ]
    text_pairs = [
        ("hero_num", INK, CREAM, 168, True),
        ("hero_label", ACCENT_INK, CREAM, 30, True),
        ("tag_since_txt", core.ink_of(core.ACCENTS[2]), core.ACCENTS[2], 20, True),
        ("tag_ops_txt", core.ink_of(core.ACCENTS[0]), core.ACCENTS[0], 15, True),
        ("body", INK, CREAM, 34, True),
        ("dept_tag", ACCENT_INK, CREAM, 17, True),
        ("footer", INK, CREAM, 17, True),
    ]
    contains = [
        ("hero_num_in_pill", (num_x, num_y, num_m["glyph_w"], num_m["glyph_h"]), (pill_x, pill_y, pill_w, pill_h)),
        ("hero_label_in_pill", (lab_x, lab_y, lab_m["ink_w"], lab_m["h"]), (pill_x, pill_y, pill_w, pill_h)),
    ]

    # manual pre-render checks that build.render()'s internal preflight call never
    # reaches (it always passes html=None to layout.preflight — see friction notes):
    wash = lay.wash_scan(html, W, H)
    craft = lay.invisible_craft_scan(html, ACCENT, core)  # panel is the ink-outline backing for the tags
    anti = lay.antipattern_scan(html)
    print("[manual] wash_scan:", wash)
    print("[manual] invisible_craft_scan (against panel):", craft)
    print("[manual] antipattern_scan:", anti)

    os.makedirs("out/session10g", exist_ok=True)
    await B.render(html, "out/session10g/g3_v1.png", W, H, elements=elements,
                    color_pairs=color_pairs, page_bg=CREAM, expect_hero=True,
                    text_pairs=text_pairs, contains=contains,
                    collision_ignore={("stat_pill", "tag_since"), ("stat_pill", "tag_ops")})
    print("done")

asyncio.run(main())
