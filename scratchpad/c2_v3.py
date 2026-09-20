"""
c2_v3 — fixes from v2's preflight/reconcile output:
  * DOUBLE ROTATION bug found here: both doodles.stamp(rot=..) and shapes.sticker(rot=..) already
    bake the rotation into the returned SVG's own inline `transform:rotate()` style. v2's at()/
    doodle()/stick() helpers ALSO put `transform:rotate()` on the wrapping div, on top of that --
    every rotated doodle/sticker was rendering at 2x its intended tilt, and rotated_bbox()'s
    footprint math (computed for the single angle I *thought* I was applying) no longer matched
    the true rendered box, which is what OVERSIZE was actually reporting, not a rotated_bbox bug.
    Fixed by rotating ONLY at the outer wrapper and passing rot=0 into stamp()/sticker() itself.
  * headline flow: measure_text's own docstring says "flow the NEXT element off `h`" -- true for
    normal document flow, but for an ABSOLUTELY positioned layout (this whole engine) there is no
    next-sibling auto-flow, so `h` doesn't protect anything. Flowing off `ink_h` instead (the true
    painted extent) is what actually prevents two manually-positioned headline lines overlapping.
  * card()'s hatch overlay div had no declared width, so it defaulted to the SVG's own explicit
    width=w -- 10px wider than the card's box-sizing:border-box CONTENT area (w minus the 5px
    border on each side). Exactly CLAUDE.md's catalogued "border eats content width" bug, just
    reached through a plain hatch overlay instead of a pill.
  * repositioned stickers/text that were genuinely colliding (star inside the headline's safety
    bbox, cloud into the tagline, tree into leaf) instead of widening the ignore-list; kept
    ignore-list entries only for overlaps the reference itself has (cascade cards, a prop grazing
    the deck/envelope seam).
"""
import asyncio, os, sys, importlib.util
# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["story"]
M = 64
A = core.ACCENTS
SKY = core.accent_for("events")
MINT = A[1]; LEMON = A[2]; TOMATO = A[3]; GRAPE = A[5]; TEAL = A[6]
INK = core.INK
WHITE = "#FFFFFF"
elements = []

def at(label, x, y, w, h, inner, z=6, rot=0):
    if rot:
        bx, by, bw, bh = lay.rotated_bbox(x, y, w, h, rot)
    else:
        bx, by, bw, bh = x, y, w, h
    elements.append((label, bx, by, bw, bh))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean", label=None):
    # rot applied ONLY here (outer div) -- dd.stamp gets rot=0, else it double-rotates (see header note)
    return at(label or f"dd_{kind}", x, y, size, size,
              f'<div style="width:100%;height:100%">{dd.stamp(kind, fill, style=style)}</div>', z=z, rot=rot)

def stick(label, path_d, fill, x, y, size, z=15, rot=0, inner="", shadow=True):
    # same double-rotation trap as doodle() -- rot applied only at the wrapper, rot=0 into sticker()
    return at(label, x, y, size, size,
              S.sticker(path_d, fill, size=size, shadow=shadow, outline=INK, inner=inner),
              z=z, rot=rot)

BOOK_D = ("M50 18 C36 10 16 12 8 20 L8 82 C16 74 36 72 50 80 "
          "C64 72 84 74 92 82 L92 20 C84 12 64 10 50 18 Z")
BOOK_INNER = (f'<path d="M50 18 L50 80" fill="none" stroke="{INK}" stroke-width="3" opacity=".55"/>'
              f'<path d="M16 30 L42 36 M16 42 L42 46 M16 54 L40 56" fill="none" stroke="{INK}" stroke-width="2.5" opacity=".45"/>'
              f'<path d="M58 36 L84 30 M60 46 L84 42 M60 56 L82 54" fill="none" stroke="{INK}" stroke-width="2.5" opacity=".45"/>')
UMBRELLA_D = ("M6 62 A44 44 0 0 1 94 62 L86 62 L79 70 L71 62 L63 70 L55 62 L47 70 "
              "L39 62 L31 70 L23 62 L15 70 L6 62 Z")
UMBRELLA_INNER = (f'<path d="M50 18 L50 62 M50 30 A32 32 0 0 1 82 60 M50 30 A32 32 0 0 0 18 60" '
                   f'fill="none" stroke="{INK}" stroke-width="2.5" opacity=".5"/>'
                   f'<path d="M50 62 L50 92" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                   f'<path d="M42 92 a8 8 0 1 0 16 0" fill="none" stroke="{INK}" stroke-width="5"/>')
CLOUD_D = ("M15 62 C13 46 28 34 44 38 C48 22 74 20 82 38 C97 39 97 60 84 63 L20 63 C16 63 15 63 15 62 Z")

def reading_row(w, h, n=3):
    figs = []
    gap = w / n
    for i in range(n):
        cx = int(gap * i + gap / 2)
        figs.append(
            f'<g transform="translate({cx-30},0)">'
            f'<circle cx="30" cy="14" r="12" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M30 26 L30 52 C30 58 20 60 8 58" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M30 52 C30 58 40 60 52 58" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<rect x="14" y="58" width="32" height="22" fill="none" stroke="{INK}" stroke-width="3.5" rx="1"/>'
            f'<line x1="30" y1="58" x2="30" y2="80" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M4 -6 L-2 4 M14 -10 L10 2 M24 -12 L22 0" stroke="{INK}" stroke-width="3" '
            f'stroke-linecap="round" opacity=".5"/>'
            f'</g>')
    return (f'<svg width="100%" height="100%" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid meet" style="position:absolute;left:0;top:0">' + "".join(figs) + '</svg>')

def card(w, h):
    # content box of a box-sizing:border-box div with a 5px border is w-10 / h-10 -- give the
    # hatch overlay THAT box (via inset:0 + width/height:100%), not the outer w/h (v2's bug).
    hatch_svg = (f'<svg width="100%" height="100%" viewBox="0 0 {w-10} {h-10}" '
                 f'style="position:absolute;inset:0" xmlns="http://www.w3.org/2000/svg">'
                 f'{S.hatch(w - 160, h - 120, 120, 96, step=13, color=INK, sw=2.5, angle=45)}</svg>')
    fs = int(h * 0.10)
    return (f'<div style="width:100%;height:100%;background:{WHITE};border:5px solid {INK};'
            f'box-sizing:border-box;overflow:hidden;position:relative">'
            f'<div style="position:absolute;top:20px;left:26px;right:26px;font-family:var(--d);'
            f'font-weight:900;line-height:.95;text-transform:uppercase;color:{INK};z-index:3">'
            f'<div style="font-size:{fs}px">SIGN-UPS</div>'
            f'<div style="font-size:{fs}px;color:{core.ink_of(SKY)}">OPEN</div></div>'
            f'<div style="position:absolute;top:16px;right:20px;width:110px;height:2px;background:{INK};opacity:.25"></div>'
            f'<div style="position:absolute;top:24px;right:20px;width:76px;height:2px;background:{INK};opacity:.25"></div>'
            f'<div style="position:absolute;opacity:.35">{hatch_svg}</div>'
            f'<div style="position:absolute;left:26px;right:26px;bottom:20px;height:{int(h*0.34)}px">'
            f'{reading_row(w-62, int(h*0.34), 3)}</div></div>')

async def main():
    async with B.session():
        probe = await B.measure_text([
            {"text": "MONSOON", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
            {"text": "READING CAMP", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
        ], W, H)
        mon_w100, camp_w100 = probe[0]["text_w"], probe[1]["text_w"]
        mon_size = 100 * (900 / mon_w100)
        camp_size = 100 * (840 / camp_w100)
        sized = await B.measure_text([
            {"text": "MONSOON", "font": "d", "size": mon_size, "weight": 900, "transform": "uppercase", "line_height": 0.86},
            {"text": "READING CAMP", "font": "d", "size": camp_size, "weight": 900, "transform": "uppercase", "line_height": 0.9},
        ], W, H)
        mon_ink_h = sized[0]["ink_h"]
        camp_ink_h = sized[1]["ink_h"]

        logo = f'<img src="{core.LOGO}" style="position:absolute;top:50px;left:{M}px;height:34px;z-index:80">'
        elements.append(("logo", M, 50, 140, 34))

        ages = (f'<div style="position:absolute;top:50px;right:{M}px;z-index:80;color:{INK};'
                f'font-family:var(--m);text-align:right">'
                f'<div style="font-weight:900;font-size:24px;letter-spacing:.02em">AGES 6-14</div>'
                f'<div style="font-size:13px;margin-top:2px;opacity:.75">sundarbans + kolkata</div></div>')
        elements.append(("ages", W - M - 220, 50, 220, 54))

        welcome = (f'<div style="position:absolute;top:126px;left:0;right:0;text-align:center;'
                   f'z-index:70;color:{INK};font-family:var(--m);font-weight:700;font-size:22px;'
                   f'letter-spacing:.16em">WELCOME TO THE</div>')
        elements.append(("welcome", 240, 126, 600, 30))

        y_mon = 168
        y_camp = y_mon + mon_ink_h + 10
        headline = (f'<div style="position:absolute;top:{y_mon}px;left:0;right:0;text-align:center;'
                    f'z-index:70;color:{INK};font-family:var(--d);font-weight:900;'
                    f'text-transform:uppercase">'
                    f'<div style="font-size:{mon_size:.0f}px;line-height:.86">MONSOON</div>'
                    f'<div style="font-size:{camp_size:.0f}px;line-height:.9;margin-top:8px">READING CAMP</div>'
                    f'</div>')
        elements.append(("headline_1", 90, y_mon, 900, mon_ink_h))
        elements.append(("headline_2", 120, y_camp, 840, camp_ink_h))
        header_end = y_camp + camp_ink_h

        tagline_y = header_end + 34
        tagline = (f'<div style="position:absolute;top:{tagline_y}px;left:0;right:0;text-align:center;'
                   f'z-index:70;color:{core.ink_of(SKY)};font-family:var(--m);font-weight:700;'
                   f'font-size:21px;letter-spacing:.1em">FREE &middot; SIGN-UPS OPEN NOW</div>')
        elements.append(("tagline", 200, tagline_y, 680, 30))
        header_bottom = tagline_y + 38

        CW, CH = 620, 600
        CX = (W - CW) // 2
        CY = header_bottom + 180
        deck = [(0.85, 6, 26, -95, 3), (0.92, -3, 13, -47, 4), (1.0, 3, 0, 0, 5)]
        card_html = ""
        deck_stack = []
        for sc, rot, dx, dy, z in deck:
            w, h = int(CW * sc), int(CH * sc)
            x, y = CX + dx, CY + dy
            deck_stack.append((x, y, w, h))
            card_html += at("card", x, y, w, h, card(w, h), z=z, rot=rot)
        cascade_bottom = CY + CH

        cloud = stick("cloud", CLOUD_D, "#EAF6FF", CX + CW - 60, CY - 200, 190, z=16)
        drop1 = at("drop1", CX + CW + 40, CY - 30, 40, 40,
                   f'<svg viewBox="0 0 100 100" width="40" height="40"><path d="{S.pixel_art("drop")}" '
                   f'fill="{core.ink_of(SKY)}"/></svg>', z=16, rot=-8)
        drop2 = at("drop2", CX + CW - 30, CY - 130, 30, 30,
                   f'<svg viewBox="0 0 100 100" width="30" height="30"><path d="{S.pixel_art("drop")}" '
                   f'fill="{TEAL}"/></svg>', z=16, rot=10)

        book = stick("book", BOOK_D, WHITE, M - 20, cascade_bottom - 470, 190, rot=-6, inner=BOOK_INNER)
        umbrella = stick("umbrella", UMBRELLA_D, TOMATO, CX + CW - 40, cascade_bottom + 20, 200, rot=5, inner=UMBRELLA_INNER)

        tree = doodle("tree", M + 6, cascade_bottom - 190, 130, MINT, z=15)
        star = doodle("star", CX + CW - 250, CY - 260, 78, LEMON, z=14, rot=-10)
        leaf = doodle("leaf", CX - 100, CY + 400, 84, MINT, z=13, rot=18)

        env_top = cascade_bottom - 10
        env_h = 480
        envelope = at("envelope", 0, env_top, W, env_h,
                      f'<svg width="{W}" height="{env_h}" viewBox="0 0 {W} {env_h}" xmlns="http://www.w3.org/2000/svg">'
                      f'<polygon points="0,0 {W},0 {W},{env_h} 0,{env_h}" fill="{WHITE}"/>'
                      f'<polygon points="0,0 {W//2},{int(env_h*0.5)} {W},0" fill="{TEAL}"/>'
                      f'<line x1="0" y1="0" x2="{W//2}" y2="{int(env_h*0.5)}" stroke="{INK}" stroke-width="4" opacity="0.4"/>'
                      f'<line x1="{W}" y1="0" x2="{W//2}" y2="{int(env_h*0.5)}" stroke="{INK}" stroke-width="4" opacity="0.4"/>'
                      f'</svg>', z=8)

        rsvp_y = env_top + 60
        rsvp = (f'<div style="position:absolute;left:{M}px;top:{rsvp_y}px;z-index:80;color:{INK};'
                f'font-family:var(--m)">'
                f'<div style="font-weight:900;font-size:36px">SIGN UP NOW</div>'
                f'<div style="font-weight:600;font-size:16px;margin-top:10px">dm @ngo.aquaterra to reserve a spot</div>'
                f'<div style="font-size:12px;opacity:.7;margin-top:14px">WALK-INS ALSO <b>WELCOME</b></div></div>')
        elements.append(("rsvp", M, rsvp_y, 460, 110))

        tags_y = env_top + env_h - 60
        tags = (f'<div style="position:absolute;right:{M}px;top:{tags_y}px;z-index:80;color:{INK};'
                f'font-family:var(--m);text-align:right;font-weight:800;font-size:15px;'
                f'letter-spacing:.03em;white-space:nowrap">SUNDARBAN &middot; KHIDIRPUR &middot; KOLKATA</div>')
        elements.append(("tags", W - M - 340, tags_y, 340, 24))

        handle = (f'<div style="position:absolute;bottom:56px;left:{M}px;z-index:80;color:{INK};'
                  f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.05em">@ngo.aquaterra</div>')
        elements.append(("handle", M, H - 70, 260, 24))

        inner = (f'<div style="position:absolute;inset:0;background:{SKY}"></div>'
                 + envelope + cloud + drop1 + drop2 + tree + leaf
                 + card_html + book + umbrella + star
                 + logo + ages + welcome + headline + tagline + rsvp + tags + handle)
        html = B.page(W, H, SKY, inner, grain=True)

        color_pairs = [("envelope_body", WHITE, SKY), ("envelope_fold", TEAL, WHITE)]
        IGNORE = {("card", "card"), ("card", "envelope"),
                  ("cloud", "card"), ("drop1", "card"), ("drop2", "card"),
                  ("book", "card"), ("umbrella", "card"),
                  ("umbrella", "envelope"), ("dd_tree", "envelope")}
        pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=SKY, core=core,
                           expect_hero=True, cascade_stacks=[deck_stack], collision_ignore=IGNORE)

        os.makedirs("out/session10f", exist_ok=True)
        await B.render(html, "out/session10f/c2_v3.png", W, H)
        print("done, clean =", pf["clean"])

asyncio.run(main())
