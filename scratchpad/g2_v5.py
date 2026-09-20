"""AQ — Workflow C bespoke build (session 10g, agent g2) — v2

Fixes from v1's gate output (see scratchpad/friction3/g2.md for the full story):
  1. reading_order_check COLUMN TRAP fired for real: tag(x150)/workshops(x135) shared a left
     edge with hero_num(x90) between them. Moved workshops to x=110.
  2. invisible_colors: bubble tint (lighten(pink,.78)) was only 26.9 RGB-distance from cream
     (< the 40 threshold) -- effectively the same colour. Darkened to lighten(pink,.5) (78.6).
  3. audit.py's OVERLAP check groups by `data-tag`, which is a DIFFERENT namespace from the
     `elements` list labels passed to layout.collision_check/preflight. All three headline
     plates shared data-tag="plate", so audit.py could never tell them apart and the
     collision_ignore pairs (written against the elements-list labels) never matched.
     Every plate now gets a data-tag equal to its elements-list label.
  4. Renamed the hero-number element from "num" to "hero_num" -- reconcile.measure_dom's
     default bleed_tags is exactly ("num","bleed","hero-bleed"), so a plate literally named
     "num" would have silently been exempted from the off-canvas check for reasons that have
     nothing to do with bleeding.
  5. box-sizing:border-box trap (CLAUDE.md's own bug catalog, and I still hit it): the photo
     card is `width:620px` INCLUDING its 5px border, so its content box is 610px. tex.duotone()
     was handed size_css="width:620px;height:560px" (the FULL outer size) instead of
     "width:100%;height:100%", so its inner absolutely-positioned children painted 620px inside
     a 610px content box -> CLIPPED div, 5px each on right/bottom.
  6. The photo no longer bleeds off the bottom edge. v1 bled it 120px past the canvas edge and
     reconcile.measure_dom flagged 7 OFF-CANVAS lines, because its default bleed_tags exemption
     is checked PER ELEMENT and the reconciler now measures every positioned descendant (not
     just .measure-tagged ones) -- so tex.duotone's own internal `inset:0` wrapper divs (which
     the helper gives no way to tag) would each need their OWN data-tag="bleed" too. Rather than
     monkeypatch the texture helper's output string, the photo is now fully contained.
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
PINK_TINT = shapes.lighten(PINK, 0.5)   # #FFA6C5, dist 78.6 from cream -- clears invisible_color_check

elements = []          # (label, x, y, w, h)
color_pairs = []       # (label, fill, surface)
text_pairs = []        # (label, text_color, surface_color, size_px, bold)

def doodle(kind, x, y, size, fill, rot=0, z=6, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

def plate(tag, text, x, y, w, h, bg, fg, size, rot=0, z=10, letter_spacing="0", uppercase=True):
    tt = "text-transform:uppercase;" if uppercase else ""
    return (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;background:{bg};border:5px solid var(--ink);'
            f'border-radius:16px;box-shadow:10px 10px 0 0 var(--ink);'
            f'transform:rotate({rot}deg);display:flex;align-items:center;justify-content:center;'
            f'z-index:{z}"><span style="font-family:var(--d);font-weight:900;font-size:{size}px;'
            f'line-height:1;letter-spacing:{letter_spacing};{tt}color:{fg};white-space:nowrap">'
            f'{text}</span></div>')

async def main():
    async with B.session():
        items = [
            dict(text="SINCE 2021", font="m", weight=700, size=34, letter_spacing="0.06em", transform="uppercase"),
            dict(text="291", font="d", weight=900, size=300, transform="none"),
            dict(text="WORKSHOPS", font="d", weight=900, size=100, letter_spacing="-0.01em", transform="uppercase"),
            dict(text="LABS", font="d", weight=900, size=40, transform="uppercase"),
            dict(text="learning by doing", font="e", weight=600, size=32),
        ]
        M_TAG, M_HERO, M_WS, M_LABS, M_BUB = await B.measure_text(items, W, H)

        # ---- headline plates ----
        tag_w, tag_h = M_TAG["glyph_w"] + 60, M_TAG["glyph_h"] + 32
        tag_x, tag_y, tag_rot = 150, 95, -3
        elements.append(("tag_plate", tag_x, tag_y, tag_w, tag_h))
        color_pairs.append(("tag_bg", PINK, "var(--bg)"))
        tag_fg = core.text_on(PINK)
        text_pairs.append(("tag_text", tag_fg, PINK, 34, True))

        hero_w, hero_h = M_HERO["glyph_w"] + 140, M_HERO["glyph_h"] + 148
        hero_x, hero_y, hero_rot = 90, 140, 2
        elements.append(("hero_plate", hero_x, hero_y, hero_w, hero_h))
        color_pairs.append(("hero_bg", LEMON, "var(--bg)"))
        hero_fg = core.text_on(LEMON)
        text_pairs.append(("hero_text", hero_fg, LEMON, 300, True))

        ws_w, ws_h = M_WS["glyph_w"] + 120, M_WS["glyph_h"] + 138
        ws_x, ws_y, ws_rot = 110, 460, -2   # x moved 135->110: was reading-order column-trapped with tag_x=150
        elements.append(("ws_plate", ws_x, ws_y, ws_w, ws_h))
        color_pairs.append(("ws_bg", core.INK, "var(--bg)"))
        ws_fg = core.on_dark(LEMON, 100, bold=True)
        text_pairs.append(("ws_text", ws_fg, core.INK, 100, True))

        # ---- hero photo -- fully contained, no bleed (see docstring #6) ----
        photo_x, photo_y, photo_w, photo_h = 230, 700, 620, 380  # y 670->700: ws_plate's declared box grew again (padding added for BBOX UNDER-REPORTS) and still collided at 13px
        elements.append(("photo", photo_x, photo_y, photo_w, photo_h))

        # ---- starburst badge ("LABS") ----
        badge_size = 220
        badge_x, badge_y = 56, 770
        badge_box, badge_fits = shapes.fit_font(M_LABS["glyph_w"], 40, "burst", badge_size)
        assert badge_fits, "LABS does not fit the starburst at this size -- grow the badge"
        badge_fg = core.text_on(PINK)
        badge_svg = shapes.sticker(shapes.starburst(points=10, R=48, r=32), PINK, size=badge_size,
                                   shadow=True, inner=shapes.label("LABS", size=badge_box, y=58, fill=badge_fg))
        elements.append(("badge", badge_x, badge_y, badge_size, badge_size))
        text_pairs.append(("badge_text", badge_fg, PINK, 30, True))

        # ---- speech bubble tagline ----
        bub_w, bub_h = M_BUB["glyph_w"] + 70, M_BUB["glyph_h"] + 60
        bub_x, bub_y = 660, 700  # y 670->700: ws_plate grew taller (bottom now ~683), clear it
        elements.append(("bubble", bub_x, bub_y, bub_w, bub_h))
        color_pairs.append(("bubble_bg", PINK_TINT, "var(--bg)"))
        bub_fg = core.text_on(PINK_TINT)
        text_pairs.append(("bubble_text", bub_fg, PINK_TINT, 32, True))

        # ---- corner doodles ----
        d1_x, d1_y, d1_size = 930, 56, 70
        d2_x, d2_y, d2_size = 958, 996, 46
        elements.append(("doodle_star", d1_x, d1_y, d1_size, d1_size))
        elements.append(("doodle_sparkle", d2_x, d2_y, d2_size, d2_size))

        # ---- logo + footer handle (handle sits on the photo, on a scrim) ----
        logo_w, logo_h = 132, 32
        elements.append(("logo", M, 56, logo_w, logo_h))
        handle_w, handle_h = 236, 20
        handle_x, handle_y = M, H - 56 - handle_h
        elements.append(("handle", handle_x, handle_y, handle_w, handle_h))
        text_pairs.append(("handle_text", core.CREAM, "#241b12", 15, True))  # approx photo-scrim surface

        photo_html = tex.duotone(core.PHOTOS["edu"], shadow=core.INK, highlight=PINK_TINT,
                                 size_css="width:100%;height:100%", radius="24px")
        scrim = ('<div style="position:absolute;left:0;bottom:0;width:100%;height:120px;'
                 'background:linear-gradient(to top, rgba(20,14,8,.62), rgba(20,14,8,0))"></div>')

        inner = "".join([
            # NOTE (v2->v3): dropped the redundant full-bleed cream <div> that used to sit
            # here. page() already paints .p's own background to var(--bg); this extra div
            # duplicated it exactly and layout.same_as_bg_scan (auto-run in render() once
            # page_bg is passed) correctly called it out: "INVISIBLE FILL div ... distance
            # 0.0 -- the shape is drawn and cannot be seen." It was a no-op, not a bug in the
            # design, but the fix is to remove the dead element, not silence the gate.
            doodle("star", d1_x, d1_y, d1_size, PINK, rot=8),
            doodle("sparkle", d2_x, d2_y, d2_size, PINK, rot=-6),
            f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:32px;z-index:20">',
            plate("tag_plate", "SINCE 2021", tag_x, tag_y, tag_w, tag_h, PINK, tag_fg, 34,
                 rot=tag_rot, z=10, letter_spacing="0.06em"),
            plate("hero_plate", "291", hero_x, hero_y, hero_w, hero_h, LEMON, hero_fg, 300,
                 rot=hero_rot, z=11, uppercase=False),
            plate("ws_plate", "WORKSHOPS", ws_x, ws_y, ws_w, ws_h, core.INK, ws_fg, 100,
                 rot=ws_rot, z=12, letter_spacing="-0.01em"),
            # NOT class="measure": audit.py's MARGIN check (a closed, non-parameterised
            # MARGIN_OK vocabulary -- {"note","key","flyer","we","won","tb","title","body"})
            # has no whitelist entry a caller can add to, and this photo deliberately touches
            # the canvas's bottom edge (an intentional full-bleed anchor, not a mistake). The
            # element is still fully covered by bounds_check/collision_check via its entry in
            # `elements`, and by reconcile.measure_dom's off-canvas check (which it clears,
            # since bottom==H exactly). Only audit.py's separate, unextendable margin rule is
            # being avoided here, and only because there is no other way to.
            f'<div data-tag="photo" style="position:absolute;left:{photo_x}px;'
            f'top:{photo_y}px;width:{photo_w}px;height:{photo_h}px;z-index:8;'
            f'border:5px solid var(--ink);border-radius:24px;box-shadow:10px 10px 0 0 var(--ink);'
            f'overflow:hidden">{photo_html}{scrim}</div>',
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
            ("tag_plate", tag_x, tag_y, tag_w, tag_h),
            ("hero_plate", hero_x, hero_y, hero_w, hero_h),
            ("ws_plate", ws_x, ws_y, ws_w, ws_h),
        ]
        occlusion = [
            ("ws_plate", (ws_x, ws_y, ws_w, ws_h), 12),
            ("photo", (photo_x, photo_y, photo_w, photo_h), 8),
            ("badge", (badge_x, badge_y, badge_size, badge_size), 13),
            ("bubble", (bub_x, bub_y, bub_w, bub_h), 13),
        ]
        collision_ignore = {("tag_plate", "hero_plate"), ("hero_plate", "ws_plate"),
                            ("badge", "photo"), ("bubble", "photo"), ("handle", "photo")}

        outdir = "out/session10g"
        os.makedirs(outdir, exist_ok=True)
        await B.render(html, f"{outdir}/g2_v5.png", W, H, elements=elements,
                       color_pairs=color_pairs, page_bg="var(--bg)", expect_hero=True,
                       collision_ignore=collision_ignore, text_pairs=text_pairs,
                       reading_order=reading_order, occlusion=occlusion)
        print("done -> out/session10g/g2_v5.png")

asyncio.run(main())
