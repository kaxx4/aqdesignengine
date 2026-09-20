"""RECREATION -- 110a5730e3710b ("Sociosphere" 3-phone app mockup), iteration 1.

Reference is a MOCKUP (three overlapping phone screenshots on a lavender backdrop). Per
CLAUDE.md Sec5 step0 / RECREATION_PROTOCOL, picked ONE screen (the front-centre, tallest,
most-complete phone) and cropped it before measuring:
    compare.crop(ref, 0.345, 0.088, 0.678, 1.0) -> scratchpad/crops/110a5730_mid.png (246x895)
Full element inventory written to brain/RECREATION_AUDIT.md under
"## Sample 110a5730e3710b" BEFORE this script was written.

This is a UI-mockup reference, not a sticker-pile reference -- shapes.py's die-cut
silhouette/sticker() treatment (built for badge piles) does not apply here; the reference's
own vocabulary is plain rounded-rect cards, pills and flat UI iconography, so that is what
is built (see friction notes for why sticker() was NOT used).

Built at feed 1080x1350 (Workflow B mockup precedent: one mechanism -> one feed poster).
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
M = 48
A = core.ACCENTS                                   # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
TOMATO = A[3]                                      # reference ground measured ~rgb(255,84,45) == AQ tomato
GRAPE = A[5]
LAVENDER = shapes.lighten(GRAPE, 0.72)              # soft tint, not raw grape -- reference card is pale lavender
INK = "#0A0A0A"; CREAM = "#F4EFE0"; WHITE = "#FFFFFF"
GREY = "#6B6B66"

els = []
def E(label, x, y, w, h): els.append((label, x, y, w, h))

def search_icon(x, y, color=WHITE, size=28):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:20" width="{size}" height="{size}" '
            f'viewBox="0 0 28 28"><circle cx="12" cy="12" r="8" fill="none" stroke="{color}" stroke-width="2.6"/>'
            f'<line x1="18" y1="18" x2="25" y2="25" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/></svg>')

def arrow_icon(x, y, color=INK, size=20):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:20" width="{size}" height="{size}" '
            f'viewBox="0 0 20 20"><path d="M4 16 L16 4 M8 4 H16 V12" stroke="{color}" stroke-width="2.3" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def pill(x, y, w, h, bg, label_color, text, size=24, outline=False, right_flush=False):
    br = "32px 0 0 32px" if right_flush else "999px"
    border = f"3px solid {label_color}" if outline else "none"
    bgc = "transparent" if outline else bg
    return (f'<div class="measure" data-tag="pill" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;border-radius:{br};background:{bgc};border:{border};box-sizing:border-box;'
            f'display:flex;align-items:center;justify-content:center;overflow:hidden;z-index:15">'
            f'<span style="font-family:var(--e);font-weight:700;font-size:{size}px;color:{label_color};'
            f'white-space:nowrap">{text}</span></div>')

def read_row(x, y, color):
    return (f'<span style="position:absolute;left:{x}px;top:{y}px;font-family:var(--e);font-weight:700;'
            f'font-size:22px;color:{color};z-index:20">Read</span>' + arrow_icon(x + 68, y + 3, color, 18))

async def main():
    async with B.session():
        # ---- measure everything before laying anything out ----
        CARD_W = W - 2 * M
        items = [
            {"text": "PHOTOS FROM", "font": "d", "size": 66, "weight": 900, "line_height": 0.94, "transform": "uppercase"},
            {"text": "THE FIELD", "font": "d", "size": 66, "weight": 900, "line_height": 0.94, "transform": "uppercase"},
            {"text": "In the field", "font": "e", "size": 34, "weight": 700},
            {"text": "Sundarban voices", "font": "e", "size": 34, "weight": 700},
            {"text": "Classroom notes", "font": "e", "size": 34, "weight": 700},
            {"text": "Volunteers return each season to log rainfall, crop damage and", "font": "e",
             "size": 22, "weight": 400, "max_width": CARD_W - 64},
        ]
        m = await B.measure_text(items, W, H)
        head1_h, head2_h = m[0]["ink_h"], m[1]["ink_h"]
        title_h = m[2]["ink_h"]
        body_h = m[5]["ink_h"]

        inner_parts = []
        # ---- 1. full-bleed ground ----
        inner_parts.append(f'<div style="position:absolute;inset:0;background:{TOMATO}"></div>')

        # ---- 2. top row: logo pill (never white-inverted -- real wordmark on a cream chip) + search ----
        LOGO_Y = 48
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{LOGO_Y}px;width:172px;height:48px;'
            f'border-radius:24px;background:{CREAM};display:flex;align-items:center;padding-left:16px;'
            f'box-sizing:border-box;z-index:20"><img src="{core.LOGO}" style="height:24px;display:block"></div>')
        E("logo_pill", M, LOGO_Y, 172, 48)
        inner_parts.append(search_icon(W - M - 30, LOGO_Y + 10, WHITE, 30))
        E("search_icon", W - M - 30, LOGO_Y + 10, 30, 30)

        # ---- 3. headline, two lines, declared PER-LINE (not one bbox) ----
        HEAD_Y = 130
        inner_parts.append(
            f'<div class="measure" data-tag="headline1" style="position:absolute;left:{M}px;top:{HEAD_Y}px;'
            f'font-family:var(--d);font-weight:900;font-size:66px;line-height:0.94;color:{WHITE};'
            f'text-transform:uppercase;z-index:20">PHOTOS FROM</div>')
        E("headline1", M, HEAD_Y, m[0]["ink_w"], head1_h)
        HEAD2_Y = HEAD_Y + m[0]["h"]
        inner_parts.append(
            f'<div class="measure" data-tag="headline2" style="position:absolute;left:{M}px;top:{HEAD2_Y}px;'
            f'font-family:var(--d);font-weight:900;font-size:66px;line-height:0.94;color:{WHITE};'
            f'text-transform:uppercase;z-index:20">THE FIELD</div>')
        E("headline2", M, HEAD2_Y, m[1]["ink_w"], head2_h)

        # ---- 4. category pill row ----
        PILL_Y = HEAD2_Y + head2_h + 40
        PILL_H = 64
        p1_w = 148
        inner_parts.append(pill(M, PILL_Y, p1_w, PILL_H, None, WHITE, "All", 26, outline=True))
        E("pill_all", M, PILL_Y, p1_w, PILL_H)
        # small round badge, top-right of the "All" pill
        inner_parts.append(
            f'<div style="position:absolute;left:{M+p1_w-30}px;top:{PILL_Y-14}px;width:34px;height:34px;'
            f'border-radius:50%;background:{WHITE};display:flex;align-items:center;justify-content:center;'
            f'z-index:21"><span style="font-family:var(--e);font-weight:800;font-size:17px;color:{TOMATO}">12</span></div>')
        E("badge", M + p1_w - 30, PILL_Y - 14, 34, 34)
        p2_x = M + p1_w + 16
        p2_w = 268
        inner_parts.append(pill(p2_x, PILL_Y, p2_w, PILL_H, INK, WHITE, "Photo diary", 26))
        E("pill_active", p2_x, PILL_Y, p2_w, PILL_H)
        p3_x = p2_x + p2_w + 16
        p3_w = W - M - p3_x                          # stops flush at the margin -- "cut by frame"
        inner_parts.append(pill(p3_x, PILL_Y, p3_w, PILL_H, INK, WHITE, "Field notes", 26, right_flush=True))
        E("pill_clipped", p3_x, PILL_Y, p3_w, PILL_H)

        # ---- 5. card 1: white, photo card ----
        C1_Y = PILL_Y + PILL_H + 44
        IMG_H = 320
        CARD1_H = IMG_H + 32 + title_h + 16 + body_h + 20 + 26 + 28
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C1_Y}px;width:{CARD_W}px;height:{CARD1_H}px;'
            f'border-radius:28px;background:{WHITE};box-shadow:0 10px 24px rgba(0,0,0,.22);z-index:10"></div>')
        E("card1_bg", M, C1_Y, CARD_W, CARD1_H)
        IMG_PAD = 20
        inner_parts.append(
            f'<div style="position:absolute;left:{M+IMG_PAD}px;top:{C1_Y+IMG_PAD}px;width:{CARD_W-2*IMG_PAD}px;'
            f'height:{IMG_H}px;border-radius:20px;background:url({core.PHOTOS["edu"]}) center/cover;z-index:11"></div>')
        E("card1_photo", M + IMG_PAD, C1_Y + IMG_PAD, CARD_W - 2 * IMG_PAD, IMG_H)
        TXT_X = M + 32
        t1_y = C1_Y + IMG_PAD + IMG_H + 28
        inner_parts.append(
            f'<div class="measure" data-tag="c1_title" style="position:absolute;left:{TXT_X}px;top:{t1_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:34px;color:{INK};z-index:11">In the field</div>')
        E("c1_title", TXT_X, t1_y, m[2]["ink_w"], title_h)
        b1_y = t1_y + title_h + 14
        inner_parts.append(
            f'<div class="measure" data-tag="c1_body" style="position:absolute;left:{TXT_X}px;top:{b1_y}px;'
            f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:22px;line-height:1.35;'
            f'color:{GREY};z-index:11">Volunteers return each season to log rainfall, crop damage and '
            f'classroom attendance across six Sundarban villages.</div>')
        E("c1_body", TXT_X, b1_y, CARD_W - 64, body_h * 2)
        by1_y = b1_y + body_h * 2 + 12
        inner_parts.append(
            f'<span style="position:absolute;left:{TXT_X}px;top:{by1_y}px;font-family:var(--e);font-weight:400;'
            f'font-size:19px;color:{GREY};z-index:11">Field team &middot; AquaTerra</span>')
        E("c1_byline", TXT_X, by1_y, 320, 24)
        rd1_y = by1_y + 34
        inner_parts.append(read_row(TXT_X, rd1_y, INK))
        E("c1_read", TXT_X, rd1_y, 100, 26)
        CARD1_H = rd1_y + 40 - C1_Y                    # reconcile declared height to actual content

        # ---- 6. card 2: lavender, squiggle motif -- the pattern-break card ----
        C2_Y = C1_Y + CARD1_H + 28
        CARD2_H = 380
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C2_Y}px;width:{CARD_W}px;height:{CARD2_H}px;'
            f'border-radius:28px;background:{LAVENDER};box-shadow:0 10px 24px rgba(0,0,0,.22);'
            f'overflow:hidden;z-index:10"></div>')
        E("card2_bg", M, C2_Y, CARD_W, CARD2_H)
        # squiggle motif -- engine's own doodle vocabulary (dd.stamp), not a hand-rolled shape;
        # reference's cursive double-loop has no exact catalog match, closest is "squiggle" scaled up
        inner_parts.append(
            f'<div style="position:absolute;left:{M+40}px;top:{C2_Y-30}px;width:520px;height:280px;'
            f'z-index:11;opacity:.95">{dd.stamp("squiggle", TOMATO, rot=-8)}</div>')
        E("card2_squiggle", M + 40, C2_Y - 30, 520, 280)
        t2_y = C2_Y + 190
        inner_parts.append(
            f'<div class="measure" data-tag="c2_title" style="position:absolute;left:{TXT_X}px;top:{t2_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:34px;color:{WHITE};z-index:12">Sundarban voices</div>')
        E("c2_title", TXT_X, t2_y, m[3]["ink_w"], title_h)
        b2_y = t2_y + title_h + 14
        inner_parts.append(
            f'<div class="measure" data-tag="c2_body" style="position:absolute;left:{TXT_X}px;top:{b2_y}px;'
            f'width:{CARD_W-64}px;font-family:var(--e);font-weight:400;font-size:22px;line-height:1.35;'
            f'color:rgba(255,255,255,.88);z-index:12">Audio diaries from women running the Pather Sathi '
            f'circle, in their own words.</div>')
        E("c2_body", TXT_X, b2_y, CARD_W - 64, body_h * 2)
        by2_y = C2_Y + CARD2_H - 66
        inner_parts.append(
            f'<span style="position:absolute;left:{TXT_X}px;top:{by2_y}px;font-family:var(--e);font-weight:400;'
            f'font-size:19px;color:rgba(255,255,255,.82);z-index:12">Pather Sathi circle</span>')
        E("c2_byline", TXT_X, by2_y, 320, 24)
        rd2_y = C2_Y + CARD2_H - 32 - 26
        inner_parts.append(read_row(TXT_X, rd2_y, WHITE))
        E("c2_read", TXT_X, rd2_y, 100, 26)

        # ---- 7. card 3: white, text-only, clipped by the canvas bottom (mirrors reference) ----
        C3_Y = C2_Y + CARD2_H + 28
        CARD3_H = H - C3_Y + 60                        # deliberately runs past the canvas edge
        inner_parts.append(
            f'<div style="position:absolute;left:{M}px;top:{C3_Y}px;width:{CARD_W}px;height:{CARD3_H}px;'
            f'border-radius:28px;background:{WHITE};box-shadow:0 10px 24px rgba(0,0,0,.22);z-index:9"></div>')
        E("card3_bg", M, C3_Y, CARD_W, H - C3_Y)         # bbox declared only to the VISIBLE extent
        t3_y = C3_Y + 28
        inner_parts.append(
            f'<div class="measure" data-tag="c3_title" style="position:absolute;left:{TXT_X}px;top:{t3_y}px;'
            f'font-family:var(--e);font-weight:700;font-size:34px;color:{INK};z-index:11">Classroom notes</div>')
        E("c3_title", TXT_X, t3_y, m[4]["ink_w"], title_h)

        # ---- 8. bottom-nav hint, flat bar fully on-canvas (reference's own frame clips its nav;
        #          reproduced as a visible hint rather than an off-canvas element, which
        #          layout.bounds_check would otherwise flag as a genuine clipping bug) ----
        NAV_H = 30
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
        pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=TOMATO, core=core,
                            expect_hero=False)
        print("PREFLIGHT CLEAN:", pf["clean"])

        slug = "110a5730e3710b"
        outdir = f"out/versions/{slug}"
        os.makedirs(outdir, exist_ok=True)
        await B.render(html, f"{outdir}/v1.png", W, H, elements=els, color_pairs=color_pairs,
                        page_bg=TOMATO, expect_hero=False)
        print("done -> ", f"{outdir}/v1.png")

asyncio.run(main())
