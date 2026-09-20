"""
c2_v1 — Workflow C bespoke build, story canvas (1080x1920).

Brief from `python design.py "monsoon reading camp - sign-ups open" --dept events --canvas story --seed 41`:
  style drawn: 2022ebef4ffad5 (training_samples/reference_posters/2022ebef4ffad554b42b3d6c5c6c914a.jpg)
  mechanism: three identical event cards cascade-stacked (offset AWAY from the front card) tucked
  into a half-open envelope, ringed by object stickers, on a grainy solid ground.
  dept accent (events, core.accent_for): #3DA9FC (sky)

Reference measured (compare.geometry): content bbox x .056-.991 y .090-.964, vertical ratio 2.54:1,
centroid (.500,.535), coverage .500. Reference native pixels 736x1308 (aspect .5626) which is
within rounding of story's own aspect .5625 -- so this reference's OWN pixel geometry is used
directly (scaled x1.4674) instead of reusing the feed-shaped adaptation in
scratchpad/gen_2022ebef4ffad5_v5.py (that script targeted 1080x1350, a different aspect ratio,
so its absolute numbers don't transfer even though the mechanism does).

Adaptations (real-assets-only rule, CLAUDE.md §9): the reference's stock/joke stickers (bath-water
bottle, disco ball, cocktails, elephant head) are swapped for content-true flat SVG marks: an open
book + umbrella (reading camp / monsoon) built as custom silhouettes via shapes.py, plus
doodles.py's leaf/tree/star/zigzag for the Sundarban-programme palette. Envelope flap colours swap
from the reference's grape/teal to sky/mint (events dept + a derived secondary). Fake "$100 cover /
DJ booth" swapped for real CTA copy (free, ages, sign-up channel).
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

W, H = core.SIZES["story"]           # 1080 x 1920 -- NOT the feed 1080x1350
M = 64
A = core.ACCENTS
SKY = core.accent_for("events")      # #3DA9FC -- fixed by department, not a free choice
MINT = A[1]; LEMON = A[2]; TOMATO = A[3]; GRAPE = A[5]; TEAL = A[6]
INK = core.INK
elements = []  # (label, x, y, w, h) -- every element that has real visual weight

def at(label, x, y, w, h, inner, z=6, rot=0):
    elements.append((label, x, y, w, h))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return at(f"dd_{kind}", x, y, size, size,
              f'<div style="width:100%;height:100%">{dd.stamp(kind, fill, rot=rot, style=style)}</div>', z=z)

# ── custom silhouettes (no book/umbrella/rain-cloud in doodles.py -- built here, per template's
#    "inline the path inside art SVGs" rule) ──────────────────────────────────────────────────
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
    """Interior detail for each cascade card: a seated kid + open book + rain ticks overhead --
    the content-true replacement for v5's dancing-figures row, same register (ink line art,
    stroke-only, no fill) so the card reads as the same FAMILY of drawing."""
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
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="position:absolute;left:0;top:0">' + "".join(figs) + '</svg>')

def card(w, h):
    hatch_svg = (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;'
                 f'left:0;top:0" xmlns="http://www.w3.org/2000/svg">'
                 f'{S.hatch(w - 150, h - 110, 120, 96, step=13, color=INK, sw=2.5, angle=45)}</svg>')
    return (f'<div style="width:100%;height:100%;background:#FFFFFF;border:5px solid {INK};'
            f'box-sizing:border-box;overflow:hidden;position:relative">'
            f'<div style="position:absolute;top:20px;left:24px;right:24px;font-family:var(--d);'
            f'font-weight:900;line-height:.92;text-transform:uppercase;color:{INK};z-index:3">'
            f'<div style="font-size:{int(h*0.135)}px">SIGN-UPS</div>'
            f'<div style="font-size:{int(h*0.135)}px;color:{core.on_cream(SKY, size_px=int(h*0.135))}">OPEN</div></div>'
            f'<div style="position:absolute;top:16px;right:20px;width:110px;height:2px;background:{INK};opacity:.25"></div>'
            f'<div style="position:absolute;top:24px;right:20px;width:76px;height:2px;background:{INK};opacity:.25"></div>'
            f'<div style="position:absolute;opacity:.35">{hatch_svg}</div>'
            f'<div style="position:absolute;left:26px;right:26px;bottom:20px;height:{int(h*0.36)}px">'
            f'{reading_row(w-52, int(h*0.36), 3)}</div></div>')

async def main():
    async with B.session():
        # ---- measure every string BEFORE sizing anything around it (CLAUDE.md §6) ----
        probe = await B.measure_text([
            {"text": "MONSOON", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
            {"text": "READING CAMP", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
        ], W, H)
        mon_w100, camp_w100 = probe[0]["text_w"], probe[1]["text_w"]
        mon_size = 100 * (940 / mon_w100)
        camp_size = 100 * (880 / camp_w100)
        sized = await B.measure_text([
            {"text": "MONSOON", "font": "d", "size": mon_size, "weight": 900, "transform": "uppercase", "line_height": 0.86},
            {"text": "READING CAMP", "font": "d", "size": camp_size, "weight": 900, "transform": "uppercase", "line_height": 0.9},
        ], W, H)
        mon_ink_h, mon_glyph_h = sized[0]["ink_h"], sized[0]["glyph_h"]
        camp_ink_h, camp_glyph_h = sized[1]["ink_h"], sized[1]["glyph_h"]

        # ---- header block ----
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
        headline = (f'<div style="position:absolute;top:{y_mon}px;left:0;right:0;text-align:center;'
                    f'z-index:70;color:{INK};font-family:var(--d);font-weight:900;'
                    f'text-transform:uppercase">'
                    f'<div style="font-size:{mon_size:.0f}px;line-height:.86">MONSOON</div>'
                    f'<div style="font-size:{camp_size:.0f}px;line-height:.9;margin-top:6px">READING CAMP</div>'
                    f'</div>')
        # bbox off the TRUE painted glyph box (ink_h/glyph_h), never a guess (CLAUDE.md §6)
        elements.append(("headline_1", 70, y_mon, 940, mon_ink_h))
        y_camp = y_mon + int(mon_ink_h * 0.86) + 6
        elements.append(("headline_2", 100, y_camp, 880, camp_ink_h))
        y_header_end = y_camp + camp_ink_h

        tagline_y = y_header_end + 30
        tagline = (f'<div style="position:absolute;top:{tagline_y}px;left:0;right:0;text-align:center;'
                   f'z-index:70;color:{core.ink_of(SKY)};font-family:var(--m);font-weight:700;'
                   f'font-size:21px;letter-spacing:.1em">FREE &middot; SIGN-UPS OPEN NOW</div>')
        elements.append(("tagline", 200, tagline_y, 680, 30))
        header_bottom = tagline_y + 40

        # ---- cascade cards (identical, per the recipe's "three identical event cards") ----
        CW, CH = 620, 600
        CX = (W - CW) // 2
        CY = header_bottom + 70
        deck = [(0.85, 6, 26, -95, 3), (0.92, -3, 13, -47, 4), (1.0, 3, 0, 0, 5)]
        card_html = ""
        deck_stack = []
        for sc, rot, dx, dy, z in deck:
            w, h = int(CW * sc), int(CH * sc)
            x, y = CX + dx, CY + dy
            deck_stack.append((x, y, w, h))
            card_html += at("card", x, y, w, h, card(w, h), z=z, rot=rot)
        cascade_bottom = CY + CH   # frontmost card's true extent (rot ignored on purpose, small angle)

        # ---- ring of stickers (content-true replacements for the reference's stock props) ----
        cloud = at("cloud", CX + CW - 60, CY - 150, 220, 150,
                   S.sticker(CLOUD_D, "#EAF6FF", size=220, shadow=True, outline=INK), z=16)
        drop1 = at("drop1", CX + CW + 20, CY + 10, 46, 46,
                   f'<svg viewBox="0 0 100 100" width="46" height="46"><path d="{S.pixel_art("drop")}" '
                   f'fill="{core.ink_of(SKY)}"/></svg>', z=16, rot=-8)
        drop2 = at("drop2", CX + CW - 20, CY + 70, 34, 34,
                   f'<svg viewBox="0 0 100 100" width="34" height="34"><path d="{S.pixel_art("drop")}" '
                   f'fill="{TEAL}"/></svg>', z=16, rot=10)

        book = at("book", M - 6, cascade_bottom - 250, 200, 176,
                  S.sticker(BOOK_D, "#FFFFFF", size=200, shadow=True, outline=INK, inner=BOOK_INNER), z=18, rot=-6)

        umbrella = at("umbrella", CX + CW - 130, cascade_bottom - 60, 210, 190,
                      S.sticker(UMBRELLA_D, TOMATO, size=210, shadow=True, outline=INK, inner=UMBRELLA_INNER), z=17, rot=4)

        tree = doodle("tree", M + 10, cascade_bottom + 40, 130, MINT, z=15)
        star = doodle("star", W - M - 150, CY - 40, 90, LEMON, z=16, rot=-10)
        leaf = doodle("leaf", CX - 90, CY + 260, 90, MINT, z=15, rot=18)

        # ---- envelope (half-open, tucked under the cascade -- matches the recipe's mechanism) ----
        env_top = cascade_bottom - 10
        env_h = 470
        envelope = at("envelope", 0, env_top, W, env_h,
                      f'<svg width="{W}" height="{env_h}" viewBox="0 0 {W} {env_h}" xmlns="http://www.w3.org/2000/svg">'
                      f'<polygon points="0,0 {W},0 {W},{env_h} 0,{env_h}" fill="{SKY}"/>'
                      f'<polygon points="0,0 {W//2},{int(env_h*0.5)} {W},0" fill="{TEAL}"/>'
                      f'<line x1="0" y1="0" x2="{W//2}" y2="{int(env_h*0.5)}" stroke="{INK}" stroke-width="4" opacity="0.4"/>'
                      f'<line x1="{W}" y1="0" x2="{W//2}" y2="{int(env_h*0.5)}" stroke="{INK}" stroke-width="4" opacity="0.4"/>'
                      f'</svg>', z=8)

        rsvp_y = env_top + 40
        rsvp = (f'<div style="position:absolute;left:{M}px;top:{rsvp_y}px;z-index:80;color:{INK};'
                f'font-family:var(--m)">'
                f'<div style="font-weight:900;font-size:34px">SIGN UP NOW</div>'
                f'<div style="font-weight:600;font-size:16px;margin-top:8px">dm @ngo.aquaterra to reserve a spot</div>'
                f'<div style="font-size:12px;opacity:.7;margin-top:12px">WALK-INS ALSO <b>WELCOME</b></div></div>')
        elements.append(("rsvp", M, rsvp_y, 460, 100))

        tags = (f'<div style="position:absolute;right:{M}px;top:{rsvp_y+40}px;z-index:80;color:{INK};'
                f'font-family:var(--m);text-align:right;font-weight:800;font-size:15px;'
                f'letter-spacing:.03em;white-space:nowrap">SUNDARBAN &middot; KHIDIRPUR &middot; KOLKATA</div>')
        elements.append(("tags", W - M - 340, rsvp_y + 40, 340, 24))

        handle = (f'<div style="position:absolute;bottom:56px;left:{M}px;z-index:80;color:{INK};'
                  f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.05em">@ngo.aquaterra</div>')
        elements.append(("handle", M, H - 70, 260, 24))

        inner = (f'<div style="position:absolute;inset:0;background:{SKY}"></div>'
                 + envelope + cloud + drop1 + drop2 + tree + leaf
                 + card_html + book + umbrella + star
                 + logo + ages + welcome + headline + tagline + rsvp + tags + handle)
        html = B.page(W, H, SKY, inner, grain=True)

        color_pairs = [("field", SKY, SKY), ("envelope_top", SKY, SKY), ("envelope_fold", TEAL, TEAL)]
        pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=SKY, core=core,
                           expect_hero=True, cascade_stacks=[deck_stack])

        os.makedirs("out/session10f", exist_ok=True)
        await B.render(html, "out/session10f/c2_v1.png", W, H)
        print("done, clean =", pf["clean"])

asyncio.run(main())
