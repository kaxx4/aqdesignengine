"""AQ — Workflow C bespoke build (session 10g, agent g2)

Brief drawn by design.py:
    python design.py "291 workshops run since 2021" --dept labs --canvas square --seed 19
Style drawn: eaad68d6305fba (eaad68d6305fbaca52c0a830906bc783.jpg) -- "The Design Flow" podcast
poster. Mechanism: a 2-3 plate extruded/shadow-block headline (each word its own flat-colour
plate, hard offset ink shadow, tilted, overlapping) sitting above a bleeding hero photo, pinned
by a starburst badge + a speech-bubble tagline.

REAL CONTENT (per CLAUDE.md / brain/VOICE.md truth ladder): "291 workshops" is COUNTED off
welfare_projects_rows.csv (already validated + shipped in brain/DECISIONS.md session 10 --
"558 logged projects, 291 workshops ..."). Qualifier "since 2021" travels with the number.
No other stat is invented. Department = labs -> core.accent_for('labs') = lemon #FFC700 (fixed
by rule, not a preference).

RE-PROPORTION NOTE: the drawn style's own judged canvas is SQUARE and the reference file itself
is a 736x736 square JPEG -- design.py printed NO "RE-PROPORTION" warning because target==style
canvas, so there was nothing to re-solve. See scratchpad/friction3/g2.md for whether that
absence of guidance is itself a finding.

DATA BUG FOUND (report it, don't patch engine/*): brain/STYLE_BANK.json's `measured.ground` for
this slug says "dark" / ground_rgb [0,0,0]. The actual reference image is a warm YELLOW ground
with a pink swoosh -- not dark at all. `engine/stylebank.py crosscheck` printed "no judgment
contradicts its measured ground" and did NOT catch this. Built to what the eye + the recipe text
(which correctly says "Warm flat ground") actually show, using AQ's own canon cream ground
(brand law, CLAUDE.md SS9: bg is cream, never a borrowed hue) rather than the mis-measured value.
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
shapes = load("shapes"); tex = load("tex")

W, H = core.SIZES["square"]; M = 64
A = core.ACCENTS
LEMON = core.accent_for("labs")     # #FFC700 -- fixed by rule, not chosen
PINK  = A[0]                        # #FF4D8C -- secondary punctuation accent
PINK_TINT = shapes.lighten(PINK, 0.78)

elements = []          # (label, x, y, w, h) -- true declared bbox, kept in sync by hand
color_pairs = []       # (label, fill, surface)
text_pairs = []        # (label, text_color, surface_color, size_px, bold)

def doodle(kind, x, y, size, fill, rot=0, z=6, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

def plate(text, x, y, w, h, bg, fg, size, rot=0, z=10, letter_spacing="0", uppercase=True):
    tt = "text-transform:uppercase;" if uppercase else ""
    return (f'<div class="measure" data-tag="plate" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;background:{bg};border:5px solid var(--ink);'
            f'border-radius:16px;box-shadow:10px 10px 0 0 var(--ink);'
            f'transform:rotate({rot}deg);display:flex;align-items:center;justify-content:center;'
            f'z-index:{z}"><span style="font-family:var(--d);font-weight:900;font-size:{size}px;'
            f'line-height:1;letter-spacing:{letter_spacing};{tt}color:{fg};white-space:nowrap">'
            f'{text}</span></div>')

async def main():
    # ---- 0. measure every string BEFORE sizing anything around it ----
    async with B.session():
        items = [
            dict(text="SINCE 2021", font="m", weight=700, size=34, letter_spacing="0.06em", transform="uppercase"),
            dict(text="291", font="d", weight=900, size=300, transform="none"),
            dict(text="WORKSHOPS", font="d", weight=900, size=100, letter_spacing="-0.01em", transform="uppercase"),
            dict(text="LABS", font="d", weight=900, size=40, transform="uppercase"),
            dict(text="learning by doing", font="e", weight=600, size=32),
        ]
        M_TAG, M_291, M_WS, M_LABS, M_BUB = await B.measure_text(items, W, H)

        # ---- 1. headline plates: size the plate to the MEASURED glyph box ----
        tag_w, tag_h = M_TAG["glyph_w"] + 60, M_TAG["glyph_h"] + 32
        tag_x, tag_y, tag_rot = 150, 95, -3
        elements.append(("tag", tag_x, tag_y, tag_w, tag_h))
        color_pairs.append(("tag_bg", PINK, "var(--bg)"))
        tag_fg = core.text_on(PINK)
        text_pairs.append(("tag_text", tag_fg, PINK, 34, True))

        num_w, num_h = M_291["glyph_w"] + 140, M_291["glyph_h"] + 100
        num_x, num_y, num_rot = 90, 140, 2
        elements.append(("num", num_x, num_y, num_w, num_h))
        color_pairs.append(("num_bg", LEMON, "var(--bg)"))
        num_fg = core.text_on(LEMON)
        text_pairs.append(("num_text", num_fg, LEMON, 300, True))

        ws_w, ws_h = M_WS["glyph_w"] + 120, M_WS["glyph_h"] + 90
        ws_x, ws_y, ws_rot = 135, 460, -2
        elements.append(("workshops", ws_x, ws_y, ws_w, ws_h))
        color_pairs.append(("ws_bg", core.INK, "var(--bg)"))
        ws_fg = core.on_dark(LEMON, 100, bold=True)
        text_pairs.append(("ws_text", ws_fg, core.INK, 100, True))

        # ---- 2. hero photo, bleeding off the bottom edge ----
        photo_x, photo_y, photo_w, photo_vis_h = 230, 640, 620, 440
        photo_css_h = 560   # true CSS height -- extends 120px past the canvas edge on purpose
        elements.append(("photo", photo_x, photo_y, photo_w, photo_vis_h))

        # ---- 3. starburst badge ("LABS") ----
        badge_size = 220
        badge_x, badge_y = 56, 770
        badge_box, badge_fits = shapes.fit_font(M_LABS["glyph_w"], 40, "burst", badge_size)
        assert badge_fits, "LABS does not fit the starburst at this size -- grow the badge"
        badge_fg = core.text_on(PINK)
        badge_svg = shapes.sticker(shapes.starburst(points=10, R=48, r=32), PINK, size=badge_size,
                                   shadow=True, inner=shapes.label("LABS", size=badge_box, y=58, fill=badge_fg))
        elements.append(("badge", badge_x, badge_y, badge_size, badge_size))
        text_pairs.append(("badge_text", badge_fg, PINK, 30, True))

        # ---- 4. speech bubble tagline ----
        bub_w, bub_h = M_BUB["glyph_w"] + 70, M_BUB["glyph_h"] + 60
        bub_x, bub_y = 660, 660
        elements.append(("bubble", bub_x, bub_y, bub_w, bub_h))
        color_pairs.append(("bubble_bg", PINK_TINT, "var(--bg)"))
        bub_fg = core.text_on(PINK_TINT)
        text_pairs.append(("bubble_text", bub_fg, PINK_TINT, 32, True))

        # ---- 5. corner doodles (varied size, secondary accent only) ----
        d1_x, d1_y, d1_size = 930, 56, 70
        d2_x, d2_y, d2_size = 958, 996, 46
        elements.append(("doodle_star", d1_x, d1_y, d1_size, d1_size))
        elements.append(("doodle_sparkle", d2_x, d2_y, d2_size, d2_size))

        # ---- 6. logo + footer handle (handle sits on the photo bleed) ----
        logo_w, logo_h = 132, 32
        elements.append(("logo", M, 56, logo_w, logo_h))
        handle_w, handle_h = 236, 20
        handle_x, handle_y = M, H - 56 - handle_h
        elements.append(("handle", handle_x, handle_y, handle_w, handle_h))
        text_pairs.append(("handle_text", core.CREAM, "#241b12", 15, True))  # approx photo-scrim surface

        # ---- assemble HTML ----
        photo_html = tex.duotone(core.PHOTOS["edu"], shadow=core.INK, highlight=PINK_TINT,
                                 size_css=f"width:{photo_w}px;height:{photo_css_h}px", radius="24px")
        scrim = ('<div style="position:absolute;left:0;bottom:0;width:100%;height:140px;'
                 'background:linear-gradient(to top, rgba(20,14,8,.62), rgba(20,14,8,0));'
                 'border-radius:0 0 24px 24px"></div>')

        inner = "".join([
            f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
            doodle("star", d1_x, d1_y, d1_size, PINK, rot=8),
            doodle("sparkle", d2_x, d2_y, d2_size, PINK, rot=-6),
            f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:32px;z-index:20">',
            plate("SINCE 2021", tag_x, tag_y, tag_w, tag_h, PINK, tag_fg, 34, rot=tag_rot,
                 z=10, letter_spacing="0.06em"),
            plate("291", num_x, num_y, num_w, num_h, LEMON, num_fg, 300, rot=num_rot, z=11,
                 uppercase=False),
            plate("WORKSHOPS", ws_x, ws_y, ws_w, ws_h, core.INK, ws_fg, 100, rot=ws_rot, z=12,
                 letter_spacing="-0.01em"),
            f'<div style="position:absolute;left:{photo_x}px;top:{photo_y}px;width:{photo_w}px;'
            f'height:{photo_css_h}px;z-index:8;border:5px solid var(--ink);border-radius:24px;'
            f'box-shadow:10px 10px 0 0 var(--ink);overflow:hidden">{photo_html}{scrim}</div>',
            f'<div style="position:absolute;left:{badge_x}px;top:{badge_y}px;width:{badge_size}px;'
            f'height:{badge_size}px;z-index:13">{badge_svg}</div>',
            f'<div class="measure" data-tag="bubble" style="position:absolute;left:{bub_x}px;'
            f'top:{bub_y}px;width:{bub_w}px;height:{bub_h}px;background:{PINK_TINT};'
            f'border:5px solid var(--ink);border-radius:26px 26px 26px 4px;'
            f'box-shadow:8px 8px 0 0 var(--ink);display:flex;align-items:center;'
            f'justify-content:center;z-index:13"><span style="font-family:var(--e);font-weight:600;'
            f'font-size:32px;color:{bub_fg}">learning by doing</span></div>',
            f'<span style="position:absolute;left:{handle_x}px;bottom:56px;font-family:var(--m);'
            f'font-weight:700;font-size:15px;letter-spacing:.06em;color:{core.CREAM};z-index:20">'
            f'@ngo.aquaterra</span>',
        ])
        html = B.page(W, H, "var(--bg)", inner, grain=True)

        reading_order = [
            ("tag", tag_x, tag_y, tag_w, tag_h),
            ("num", num_x, num_y, num_w, num_h),
            ("workshops", ws_x, ws_y, ws_w, ws_h),
        ]
        occlusion = [
            ("workshops", (ws_x, ws_y, ws_w, ws_h), 12),
            ("photo", (photo_x, photo_y, photo_w, photo_vis_h), 8),
            ("badge", (badge_x, badge_y, badge_size, badge_size), 13),
            ("bubble", (bub_x, bub_y, bub_w, bub_h), 13),
        ]
        collision_ignore = {("tag", "num"), ("num", "workshops"), ("badge", "photo"),
                            ("bubble", "photo"), ("handle", "photo")}

        slug = "eaad68d6305fba"
        outdir = f"out/session10g"
        os.makedirs(outdir, exist_ok=True)
        await B.render(html, f"{outdir}/g2_v1.png", W, H, elements=elements,
                       color_pairs=color_pairs, page_bg="var(--bg)", expect_hero=True,
                       collision_ignore=collision_ignore, text_pairs=text_pairs,
                       reading_order=reading_order, occlusion=occlusion)
        print("done -> out/session10g/g2_v1.png")

asyncio.run(main())
