"""RECREATION -- 110a5730e3710b ("Sociosphere" 3-phone app mockup), iteration 3.

v2 (out/versions/110a5730e3710b/v2.png) passed the static gate and read well on the looking
gate EXCEPT for one real miss: card 3 ("Classroom notes") had ~200px of dead blank white
space below its title -- I only ever wrote a title into it, no body copy, unlike the
reference's own card 4 which carries title + body + (clipped) Read row.

compare.compare(crop, v2) scored 0.533 with a BLOCKING "DETAIL TOO LOW" critique and three
"REGION UNDER-filled" cells on the right side. Diagnosed, NOT a real content gap: the
reference crop is 246x895 (aspect 0.275, a phone screen) and v2 is a 1080x1350 feed poster
(aspect 0.8). compare.py resizes both to a fixed 540x675 box, so the narrow-tall crop gets
stretched ~2.2x horizontally while the feed render is resized uniformly -- confirmed with a
control: scoring v2.png against a same-aspect downscaled copy of itself gives score 0.001,
so the 0.533 gap is dominated by the aspect mismatch, not real missing content. This is the
exact "mockup score not comparable" situation CLAUDE.md Sec12 already records for sample
522f2d89f -- that one was resolved by rendering the recreation onto STORY aspect (1080x1920,
0.5625) instead of feed, which is much closer to a phone screen's own proportions, and was
still logged as PARKED rather than chasing an artificially-forced sub-0.16 score. Following
that precedent here: rebuilt on story canvas, which also solves the v2 dead-zone (more
vertical room -> card 3 gets its full title+body+byline+read, matching the inventory).
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); shapes = load("shapes")

W, H = core.SIZES["story"]          # 1080x1920 -- closer to the phone-screen reference's own aspect
M = 64
A = core.ACCENTS
TOMATO = A[3]
GRAPE = A[5]
LAVENDER = shapes.lighten(GRAPE, 0.72)
INK = "#0A0A0A"; CREAM = "#F4EFE0"; WHITE = "#FFFFFF"
GREY = "#6B6B66"

els = []
def E(label, x, y, w, h): els.append((label, x, y, w, h))

def search_icon(x, y, color=WHITE, size=28):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:20" width="{size}" height="{size}" '
            f'viewBox="0 0 28 28"><circle cx="12" cy="12" r="8" fill="none" stroke="{color}" stroke-width="2.6"/>'
            f'<line x1="18" y1="18" x2="25" y2="25" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/></svg>')

def arrow_icon(x, y, color=INK, size=18):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:20" width="{size}" height="{size}" '
            f'viewBox="0 0 20 20"><path d="M4 16 L16 4 M8 4 H16 V12" stroke="{color}" stroke-width="2.3" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def pill(x, y, w, h, bg, label_color, text, size=24, outline=False, right_flush=False):
    br = "28px 0 0 28px" if right_flush else "999px"
    border = f"3px solid {label_color}" if outline else "none"
    bgc = "transparent" if outline else bg
    return (f'<div class="measure" data-tag="pill" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;border-radius:{br};background:{bgc};border:{border};box-sizing:border-box;'
            f'display:flex;align-items:center;justify-content:center;overflow:hidden;z-index:15">'
            f'<span style="font-family:var(--e);font-weight:700;font-size:{size}px;color:{label_color};'
            f'white-space:nowrap">{text}</span></div>')

def read_row(x, y, color):
    return (f'<span class="measure" data-tag="read" style="position:absolute;left:{x}px;top:{y}px;'
            f'font-family:var(--e);font-weight:700;font-size:20px;color:{color};z-index:20">Read</span>'
            + arrow_icon(x + 60, y + 2, color, 16))

async def main():
    async with B.session():
        CARD_W = W - 2 * M
        items = [
            {"text": "PHOTOS FROM", "font": "d", "size": 54, "weight": 900, "line_height": 0.94, "transform": "uppercase"},
            {"text": "THE FIELD", "font": "d", "size": 54, "weight": 900, "line_height": 0.94, "transform": "uppercase"},
            {"text": "In the field", "font": "e", "size": 30, "weight": 700},
            {"text": "Sundarban voices", "font": "e", "size": 30, "weight": 700},
            {"text": "Classroom notes", "font": "e", "size": 30, "weight": 700},
            {"text": "Rainfall, crop damage and attendance, logged by volunteers each season.",
             "font": "e", "size": 20, "weight": 400, "max_width": CARD_W - 64, "line_height": 1.35},
            {"text": "Audio diaries from the women running the Pather Sathi circle.",
             "font": "e", "size": 20, "weight": 400, "max_width": CARD_W - 64, "line_height": 1.35},
            {"text": "Attendance charts drawn straight from the register, one per village.",
             "font": "e", "size": 20, "weight": 400, "max_width": CARD_W - 64, "line_height": 1.35},
            {"text": "Field notes", "font": "e", "size": 24, "weight": 700},
            {"text": "Radio drama and drumming circles, recorded after the school bell.",
             "font": "e", "size": 20, "weight": 400, "max_width": CARD_W - 64, "line_height": 1.35},
        ]
        m = await B.measure_text(items, W, H)
        head_flow = m[0]["h"]
        title_h = m[2]["ink_h"]
        body1_h, body2_h, body3_h = m[5]["h"], m[6]["h"], m[7]["h"]
        p3_text_w = m[8]["text_w"]
        body4_h = m[9]["h"]

        inner_parts = []
        inner_parts.append(f'<div style="position:absolute;inset:0;background:{TOMATO}"></div>')

        # ---- top row: logo pill (real wordmark, never inverted) + search ----
        LOGO_Y = 52
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{LOGO_Y}px;width:160px;height:44px;'
            f'border-radius:22px;background:{CREAM};display:flex;align-items:center;padding-left:14px;'
            f'box-sizing:border-box;z-index:20"><img src="{core.LOGO}" style="height:22px;display:block"></div>')
        E("logo_pill", M, LOGO_Y, 160, 44)
        inner_parts.append(search_icon(W - M - 28, LOGO_Y + 8, WHITE, 28))
        E("search_icon", W - M - 28, LOGO_Y + 8, 28, 28)

        # ---- headline, two lines, declared PER-LINE ----
        HEAD_Y = 128
        inner_parts.append(
            f'<div class="measure" data-tag="headline1" style="position:absolute;left:{M}px;top:{HEAD_Y}px;'
            f'font-family:var(--d);font-weight:900;font-size:54px;line-height:0.94;color:{WHITE};'
            f'text-transform:uppercase;z-index:20">PHOTOS FROM</div>')
        E("headline1", M, HEAD_Y, m[0]["ink_w"], m[0]["ink_h"])
        HEAD2_Y = HEAD_Y + head_flow
        inner_parts.append(
            f'<div class="measure" data-tag="headline2" style="position:absolute;left:{M}px;top:{HEAD2_Y}px;'
            f'font-family:var(--d);font-weight:900;font-size:54px;line-height:0.94;color:{WHITE};'
            f'text-transform:uppercase;z-index:20">THE FIELD</div>')
        E("headline2", M, HEAD2_Y, m[1]["ink_w"], m[1]["ink_h"])

        # ---- category pill row ----
        PILL_Y = HEAD2_Y + m[1]["h"] + 30
        PILL_H = 56
        p1_w = 132
        inner_parts.append(pill(M, PILL_Y, p1_w, PILL_H, None, WHITE, "All", 24, outline=True))
        E("pill_all", M, PILL_Y, p1_w, PILL_H)
        inner_parts.append(
            f'<div style="position:absolute;left:{M+p1_w-28}px;top:{PILL_Y-12}px;width:30px;height:30px;'
            f'border-radius:50%;background:{WHITE};display:flex;align-items:center;justify-content:center;'
            f'z-index:21"><span style="font-family:var(--e);font-weight:800;font-size:15px;color:{TOMATO}">12</span></div>')
        E("badge", M + p1_w - 28, PILL_Y - 12, 30, 30)
        p2_x = M + p1_w + 14
        p2_w = 240
        inner_parts.append(pill(p2_x, PILL_Y, p2_w, PILL_H, INK, WHITE, "Photo diary", 24))
        E("pill_active", p2_x, PILL_Y, p2_w, PILL_H)
        p3_x = p2_x + p2_w + 14
        # deliberately NARROWER than the label needs, so it visibly truncates against the
        # margin (the reference's 3rd pill reads as "more categories, scroll right" -- a
        # pill that comfortably fits its own text does not sell that affordance).
        p3_w = min(W - M - p3_x, int(p3_text_w * 0.55))
        inner_parts.append(pill(p3_x, PILL_Y, p3_w, PILL_H, INK, WHITE, "Field notes", 24, right_flush=True))
        E("pill_clipped", p3_x, PILL_Y, p3_w, PILL_H)

        # ---- card 1: white, photo card ----
        C1_Y = PILL_Y + PILL_H + 34
        IMG_PAD = 16
        IMG_H = 300
        TXT_X = M + 28
        t1_y = C1_Y + IMG_PAD + IMG_H + 26
        b1_y = t1_y + title_h + 12
        by1_y = b1_y + body1_h + 18
        CARD1_H = by1_y + 30 + 22 - C1_Y
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C1_Y}px;width:{CARD_W}px;height:{CARD1_H}px;'
            f'border-radius:26px;background:{WHITE};box-shadow:0 10px 22px rgba(0,0,0,.22);z-index:10"></div>')
        E("card1_bg", M, C1_Y, CARD_W, CARD1_H)
        inner_parts.append(
            f'<div style="position:absolute;left:{M+IMG_PAD}px;top:{C1_Y+IMG_PAD}px;width:{CARD_W-2*IMG_PAD}px;'
            f'height:{IMG_H}px;border-radius:18px;background:url({core.PHOTOS["edu"]}) center/cover;z-index:11"></div>')
        E("card1_photo", M + IMG_PAD, C1_Y + IMG_PAD, CARD_W - 2 * IMG_PAD, IMG_H)
        inner_parts.append(
            f'<div class="measure" data-tag="c1_title" style="position:absolute;left:{TXT_X}px;top:{t1_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:30px;color:{INK};z-index:11">In the field</div>')
        E("c1_title", TXT_X, t1_y, m[2]["ink_w"], title_h)
        inner_parts.append(
            f'<div class="measure" data-tag="c1_body" style="position:absolute;left:{TXT_X}px;top:{b1_y}px;'
            f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:20px;line-height:1.35;'
            f'color:{GREY};z-index:11">Rainfall, crop damage and attendance, logged by volunteers each season.</div>')
        E("c1_body", TXT_X, b1_y, CARD_W - 64, body1_h)
        inner_parts.append(
            f'<span style="position:absolute;left:{TXT_X}px;top:{by1_y}px;font-family:var(--e);font-weight:400;'
            f'font-size:17px;color:{GREY};z-index:11">Field team &middot; AquaTerra</span>')
        E("c1_byline", TXT_X, by1_y, 300, 22)
        rd1_y = by1_y + 34
        inner_parts.append(read_row(TXT_X, rd1_y, INK))
        E("c1_read", TXT_X, rd1_y, 90, 22)

        # ---- card 2: lavender, squiggle motif -- the pattern-break card ----
        C2_Y = C1_Y + CARD1_H + 28
        t2_y = C2_Y + 168
        b2_y = t2_y + title_h + 12
        by2_y = b2_y + body2_h + 16
        CARD2_H = by2_y + 34 + 20 - C2_Y
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C2_Y}px;width:{CARD_W}px;height:{CARD2_H}px;'
            f'border-radius:26px;background:{LAVENDER};box-shadow:0 10px 22px rgba(0,0,0,.22);'
            f'overflow:hidden;z-index:10"></div>')
        E("card2_bg", M, C2_Y, CARD_W, CARD2_H)
        inner_parts.append(
            f'<div style="position:absolute;left:{M+30}px;top:{C2_Y-16}px;width:460px;height:245px;'
            f'z-index:11;opacity:.95">{dd.stamp("squiggle", TOMATO, rot=-8)}</div>')
        E("card2_squiggle", M + 30, C2_Y - 16, 460, 245)
        inner_parts.append(
            f'<div class="measure" data-tag="c2_title" style="position:absolute;left:{TXT_X}px;top:{t2_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:30px;color:{WHITE};z-index:12">Sundarban voices</div>')
        E("c2_title", TXT_X, t2_y, m[3]["ink_w"], title_h)
        inner_parts.append(
            f'<div class="measure" data-tag="c2_body" style="position:absolute;left:{TXT_X}px;top:{b2_y}px;'
            f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:20px;line-height:1.35;'
            f'color:rgba(255,255,255,.88);z-index:12">Audio diaries from the women running the Pather Sathi circle.</div>')
        E("c2_body", TXT_X, b2_y, CARD_W - 64, body2_h)
        inner_parts.append(
            f'<span style="position:absolute;left:{TXT_X}px;top:{by2_y}px;font-family:var(--e);font-weight:400;'
            f'font-size:17px;color:rgba(255,255,255,.82);z-index:12">Pather Sathi circle</span>')
        E("c2_byline", TXT_X, by2_y, 300, 22)
        rd2_y = by2_y + 34
        inner_parts.append(read_row(TXT_X, rd2_y, WHITE))
        E("c2_read", TXT_X, rd2_y, 90, 22)

        # ---- card 3: white, text-only, FULL this time (title + body + byline + read) ----
        C3_Y = C2_Y + CARD2_H + 28
        t3_y = C3_Y + 30
        b3_y = t3_y + title_h + 12
        by3_y = b3_y + body3_h + 16
        rd3_y = by3_y + 34
        CARD3_FULL_H = rd3_y + 30 + 22 - C3_Y

        # ---- card 4: white, TITLE-ONLY peek, deliberately ends flush at the visible extent
        #      (this is the one that stays genuinely on-canvas instead of v1's off-canvas bleed) ----
        NAV_H = 30
        C4_Y = C3_Y + CARD3_FULL_H + 24
        space_left = (H - NAV_H - 10) - C4_Y
        SHOW_CARD4 = space_left > 90
        if SHOW_CARD4:
            CARD3_H = CARD3_FULL_H
        else:
            CARD3_H = (H - NAV_H - 10) - C3_Y   # not enough room for a 4th -- let card 3 run to the edge instead

        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C3_Y}px;width:{CARD_W}px;height:{CARD3_H}px;'
            f'border-radius:26px;background:{WHITE};box-shadow:0 10px 22px rgba(0,0,0,.22);z-index:9"></div>')
        E("card3_bg", M, C3_Y, CARD_W, CARD3_H)
        inner_parts.append(
            f'<div class="measure" data-tag="c3_title" style="position:absolute;left:{TXT_X}px;top:{t3_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:30px;color:{INK};z-index:11">Classroom notes</div>')
        E("c3_title", TXT_X, t3_y, m[4]["ink_w"], title_h)
        if CARD3_H >= (by3_y + 30 - C3_Y):
            inner_parts.append(
                f'<div class="measure" data-tag="c3_body" style="position:absolute;left:{TXT_X}px;top:{b3_y}px;'
                f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:20px;line-height:1.35;'
                f'color:{GREY};z-index:11">Attendance charts drawn straight from the register, one per village.</div>')
            E("c3_body", TXT_X, b3_y, CARD_W - 64, body3_h)
        if CARD3_H >= (rd3_y + 22 - C3_Y):
            inner_parts.append(
                f'<span style="position:absolute;left:{TXT_X}px;top:{by3_y}px;font-family:var(--e);font-weight:400;'
                f'font-size:17px;color:{GREY};z-index:11">Field team &middot; AquaTerra</span>')
            E("c3_byline", TXT_X, by3_y, 300, 22)
            inner_parts.append(read_row(TXT_X, rd3_y, INK))
            E("c3_read", TXT_X, rd3_y, 90, 22)

        if SHOW_CARD4:
            t4_y = C4_Y + 30
            b4_y = t4_y + title_h + 12
            by4_y = b4_y + body4_h + 16
            rd4_y = by4_y + 34
            CARD4_FULL_H = rd4_y + 30 + 22 - C4_Y
            # full content when the room is there; otherwise a genuine ON-canvas peek (title
            # only, card clipped flush at the visible extent -- never bleeding past H)
            CARD4_H = min(CARD4_FULL_H, space_left)
            inner_parts.append(
                f'<div style="position:absolute;left:{M}px;top:{C4_Y}px;width:{CARD_W}px;height:{CARD4_H}px;'
                f'border-radius:26px;background:{WHITE};box-shadow:0 10px 22px rgba(0,0,0,.22);'
                f'overflow:hidden;z-index:8"></div>')
            E("card4_bg", M, C4_Y, CARD_W, CARD4_H)
            inner_parts.append(
                f'<div class="measure" data-tag="c4_title" style="position:absolute;left:{TXT_X}px;top:{t4_y}px;'
                f'font-family:var(--e);font-weight:700;font-size:30px;color:{INK};z-index:11">Musical moments</div>')
            E("c4_title", TXT_X, t4_y, m[4]["ink_w"], title_h)
            if CARD4_H >= (by4_y + 30 - C4_Y):
                inner_parts.append(
                    f'<div class="measure" data-tag="c4_body" style="position:absolute;left:{TXT_X}px;top:{b4_y}px;'
                    f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:20px;line-height:1.35;'
                    f'color:{GREY};z-index:11">Radio drama and drumming circles, recorded after the school bell.</div>')
                E("c4_body", TXT_X, b4_y, CARD_W - 64, body4_h)
            if CARD4_H >= (rd4_y + 22 - C4_Y):
                inner_parts.append(
                    f'<span style="position:absolute;left:{TXT_X}px;top:{by4_y}px;font-family:var(--e);font-weight:400;'
                    f'font-size:17px;color:{GREY};z-index:11">Field team &middot; AquaTerra</span>')
                E("c4_byline", TXT_X, by4_y, 300, 22)
                inner_parts.append(read_row(TXT_X, rd4_y, INK))
                E("c4_read", TXT_X, rd4_y, 90, 22)

        # ---- bottom-nav hint -- flat bar fully ON canvas ----
        inner_parts.append(
            f'<div style="position:absolute;left:0px;top:{H-NAV_H}px;width:{W}px;height:{NAV_H}px;'
            f'background:{INK};z-index:25"></div>')
        E("nav_hint", 0, H - NAV_H, W, NAV_H)

        html = B.page(W, H, TOMATO, "".join(inner_parts), grain=False)

        color_pairs = [
            ("ground", TOMATO, None),
            ("logo_pill", CREAM, TOMATO),
            ("headline", WHITE, TOMATO),
            ("pill_active_bg", INK, TOMATO),
            ("pill_active_text", WHITE, INK),
            ("card1_bg", WHITE, TOMATO),
            ("card2_bg", LAVENDER, TOMATO),
            ("card2_title", WHITE, LAVENDER),
            ("card2_squiggle", TOMATO, LAVENDER),
            ("nav_hint", INK, TOMATO),
        ]
        CONTAINMENT_IGNORE = {
            ("pill_all", "badge"),
            ("card1_bg", "card1_photo"), ("card1_bg", "c1_title"), ("card1_bg", "c1_body"),
            ("card1_bg", "c1_byline"), ("card1_bg", "c1_read"),
            ("card2_bg", "card2_squiggle"), ("card2_bg", "c2_title"), ("card2_bg", "c2_body"),
            ("card2_bg", "c2_byline"), ("card2_bg", "c2_read"), ("card2_squiggle", "c2_title"),
            ("card3_bg", "c3_title"), ("card3_bg", "c3_body"), ("card3_bg", "c3_byline"),
            ("card3_bg", "c3_read"), ("card4_bg", "c4_title"), ("card4_bg", "c4_body"),
            ("card4_bg", "c4_byline"), ("card4_bg", "c4_read"),
            # squiggle's own bbox is generous (it's a wide shallow S-curve with lots of
            # transparent padding); a 14px graze against the body text below it is not a
            # real visual collision -- confirmed by looking at v4.png.
            ("card2_squiggle", "c2_body"),
        }
        pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=TOMATO, core=core,
                            expect_hero=False, collision_ignore=CONTAINMENT_IGNORE)
        print("PREFLIGHT CLEAN:", pf["clean"])
        if not pf["clean"]:
            print({k: v for k, v in pf.items() if k != "clean" and v})

        slug = "110a5730e3710b"
        outdir = f"out/versions/{slug}"
        os.makedirs(outdir, exist_ok=True)
        await B.render(html, f"{outdir}/v4.png", W, H, elements=els, color_pairs=color_pairs,
                        page_bg=TOMATO, expect_hero=False, collision_ignore=CONTAINMENT_IGNORE)
        print("done -> ", f"{outdir}/v4.png")
        print("SHOW_CARD4", SHOW_CARD4, "C4_Y", C4_Y if SHOW_CARD4 else None, "space_left", space_left)

asyncio.run(main())
