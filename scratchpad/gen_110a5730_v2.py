"""RECREATION -- 110a5730e3710b ("Sociosphere" 3-phone app mockup), iteration 2.

v1 (scratchpad/gen_110a5730_v1.py) failed the static gate before any looking-gate review:
  - off_canvas on card3 (I deliberately let it bleed 60px past H=1350 to mimic the
    reference's own frame-clipped 4th card -- reconcile.measure_dom correctly caught this
    as a real bug: CLAUDE.md's "deliberate full-bleed stays the off_canvas check's job",
    i.e. bleeding past the canvas edge is never sanctioned, even to imitate a clipped
    reference element. Fixed here by ending card3 flush at its visible extent instead.
  - off_canvas on c3_title at y=1438 (>H) -- caused by a real layout-budget bug: body text
    measured with `max_width` returns the WHOLE wrapped block's height in one number, and
    v1 multiplied that by 2 assuming it was a per-line height. That silently doubled every
    body-copy block and pushed everything below it off the canvas.
  - MARGIN breaches on both headlines and both category pills -- side-effect of the same
    cascading overflow.
Fixed: correct body-block height usage, tightened the whole vertical budget so header +
2 full cards + a genuine (on-canvas) peek of card3 fit in 1350px, and the "All"/badge
overlap (by-design, per the reference) is now declared to preflight via collision_ignore
instead of being reported as a bug.
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); shapes = load("shapes")

W, H = core.SIZES["feed"]
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
        ]
        m = await B.measure_text(items, W, H)
        head_flow = m[0]["h"]
        title_h = m[2]["ink_h"]
        body1_h, body2_h = m[5]["h"], m[6]["h"]        # whole wrapped block, NOT per-line

        inner_parts = []
        inner_parts.append(f'<div style="position:absolute;inset:0;background:{TOMATO}"></div>')

        # ---- top row: logo pill (real wordmark, never inverted -- a cream chip on the dark ground) ----
        LOGO_Y = 44
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{LOGO_Y}px;width:160px;height:44px;'
            f'border-radius:22px;background:{CREAM};display:flex;align-items:center;padding-left:14px;'
            f'box-sizing:border-box;z-index:20"><img src="{core.LOGO}" style="height:22px;display:block"></div>')
        E("logo_pill", M, LOGO_Y, 160, 44)
        inner_parts.append(search_icon(W - M - 28, LOGO_Y + 8, WHITE, 28))
        E("search_icon", W - M - 28, LOGO_Y + 8, 28, 28)

        # ---- headline, two lines, declared PER-LINE ----
        HEAD_Y = 108
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
        PILL_Y = HEAD2_Y + m[1]["h"] + 26
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
        p3_w = W - M - p3_x
        inner_parts.append(pill(p3_x, PILL_Y, p3_w, PILL_H, INK, WHITE, "Field notes", 24, right_flush=True))
        E("pill_clipped", p3_x, PILL_Y, p3_w, PILL_H)

        # ---- card 1: white, photo card ----
        C1_Y = PILL_Y + PILL_H + 28
        IMG_PAD = 16
        IMG_H = 220
        TXT_X = M + 28
        t1_y = C1_Y + IMG_PAD + IMG_H + 22
        b1_y = t1_y + title_h + 10
        by1_y = b1_y + body1_h + 16
        CARD1_H = by1_y + 26 + 20 - C1_Y
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
        rd1_y = by1_y + 30
        inner_parts.append(read_row(TXT_X, rd1_y, INK))
        E("c1_read", TXT_X, rd1_y, 90, 22)

        # ---- card 2: lavender, squiggle motif -- the pattern-break card ----
        C2_Y = C1_Y + CARD1_H + 24
        t2_y = C2_Y + 150
        b2_y = t2_y + title_h + 10
        by2_y = b2_y + body2_h + 14
        CARD2_H = by2_y + 30 + 18 - C2_Y
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C2_Y}px;width:{CARD_W}px;height:{CARD2_H}px;'
            f'border-radius:26px;background:{LAVENDER};box-shadow:0 10px 22px rgba(0,0,0,.22);'
            f'overflow:hidden;z-index:10"></div>')
        E("card2_bg", M, C2_Y, CARD_W, CARD2_H)
        inner_parts.append(
            f'<div style="position:absolute;left:{M+30}px;top:{C2_Y-20}px;width:420px;height:224px;'
            f'z-index:11;opacity:.95">{dd.stamp("squiggle", TOMATO, rot=-8)}</div>')
        E("card2_squiggle", M + 30, C2_Y - 20, 420, 224)
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
        rd2_y = by2_y + 30
        inner_parts.append(read_row(TXT_X, rd2_y, WHITE))
        E("c2_read", TXT_X, rd2_y, 90, 22)

        # ---- card 3: white, text-only, a genuine ON-CANVAS peek (title only, no bleed) ----
        C3_Y = C2_Y + CARD2_H + 24
        NAV_H = 28
        CARD3_H = (H - NAV_H - 8) - C3_Y
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C3_Y}px;width:{CARD_W}px;height:{CARD3_H}px;'
            f'border-radius:26px;background:{WHITE};box-shadow:0 10px 22px rgba(0,0,0,.22);z-index:9"></div>')
        E("card3_bg", M, C3_Y, CARD_W, CARD3_H)
        t3_y = C3_Y + 26
        inner_parts.append(
            f'<div class="measure" data-tag="c3_title" style="position:absolute;left:{TXT_X}px;top:{t3_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:30px;color:{INK};z-index:11">Classroom notes</div>')
        E("c3_title", TXT_X, t3_y, m[4]["ink_w"], title_h)

        # ---- bottom-nav hint -- a flat bar fully ON canvas (never bleeds past H) ----
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
        # Every text/photo element below is drawn INSIDE its own card -- that overlap is the
        # entire point (containment, not collision). collision_check has no notion of nesting,
        # so each parent/child pair has to be declared by hand or it reads as a false collision.
        CONTAINMENT_IGNORE = {
            ("pill_all", "badge"),
            ("card1_bg", "card1_photo"), ("card1_bg", "c1_title"), ("card1_bg", "c1_body"),
            ("card1_bg", "c1_byline"), ("card1_bg", "c1_read"),
            ("card2_bg", "card2_squiggle"), ("card2_bg", "c2_title"), ("card2_bg", "c2_body"),
            ("card2_bg", "c2_byline"), ("card2_bg", "c2_read"), ("card2_squiggle", "c2_title"),
            ("card3_bg", "c3_title"),
        }
        pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=TOMATO, core=core,
                            expect_hero=False, collision_ignore=CONTAINMENT_IGNORE)
        print("PREFLIGHT CLEAN:", pf["clean"])
        if not pf["clean"]:
            print({k: v for k, v in pf.items() if k != "clean" and v})

        slug = "110a5730e3710b"
        outdir = f"out/versions/{slug}"
        os.makedirs(outdir, exist_ok=True)
        await B.render(html, f"{outdir}/v2.png", W, H, elements=els, color_pairs=color_pairs,
                        page_bg=TOMATO, expect_hero=False, collision_ignore=CONTAINMENT_IGNORE)
        print("done -> ", f"{outdir}/v2.png")
        print("C3_Y", C3_Y, "CARD3_H", CARD3_H, "bottom", C3_Y + CARD3_H)

asyncio.run(main())
