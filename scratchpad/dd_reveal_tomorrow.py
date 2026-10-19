"""DISCO DIWALI teaser poster, "REVEAL TOMORROW" (inspo: a giant iOS-style dialog, 'Coming in June / Save', held up in front of the photo).

One 1080x1350 feed poster on the approved diya ground (black, navy and gold lotus-diya corners fading to black, string lights):
the title lockup stays the hero (R2), and a big white dialog card is the hook: LOCATION + DATE REVEALED TOMORROW, a hairline divider,
a blue REMIND ME action row. An eyebrow above it carries the hype line. No date, venue, price or lineup is printed (none is public yet).

Adaptations recorded (CLAUDE.md sec 2 precedence ladder):
  - The inspo's HANDS are a stock photo of a stranger; real-assets-only forbids faking them. The mechanism that is kept: an oversized
    system dialog that states the news in one flat line, with a blue action row, tilted a hair so it reads as held, not pinned.
  - The dialog is a DESIGN DEVICE (no OS marks, our own button copy). Its blue is the only blue on the poster, as in the captcha carousel.
  - Type is NeutralFace throughout (user, 2026-10-13); white with a thin black border on the dark ground, black on the white card.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_reveal_tomorrow.py [vN]"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
BLUE = "#1A73E8"
VER = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = os.path.join(ROOT, "out", "discodiwali", f"reveal_tomorrow_{VER}.png")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
D = "font-family:var(--d);text-transform:uppercase;"


def ground():
    """The approved diya ground: plate, string lights, gold dust and grain (same layer stack as dd_carousel_captcha.bg_layers)."""
    return (f'<div data-tag="plate" style="position:absolute;inset:0;z-index:1;background:#000"></div>'
            f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'
            f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
            f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def build():
    # badge and mask: the approved classic placements (measured for poster_ref)
    bw = 230
    badge = f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:30px;top:96px;width:{bw}px;z-index:20">'
    k = .4925
    mask = (f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(343 - 157 * k)}px;top:{round(108 - 211 * k)}px;width:{round(1680 * k)}px;z-index:6;'
            f'filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">')
    # title lockup: ink bbox is (264..1984, 400..1316) of 2000x1382, so at scale t the ink is 1720t x 916t
    t = .52
    ink_w, ink_h = round(1720 * t), round(916 * t)
    ix, iy = (W - ink_w) // 2, 372
    title = f'<img data-tag="title" src="{dd.uri("title_lockup_noball.png")}" style="position:absolute;left:{round(ix - 264 * t)}px;top:{round(iy - 400 * t)}px;width:{round(2000 * t)}px;z-index:9">'
    bottom = iy + ink_h
    ncx = round(ix + .556 * ink_w)                  # the lockup's notch, where the edition lines tuck
    s1, s2 = round(bottom - 80), round(bottom - 43)
    sub1 = f'<div data-tag="sub1" style="position:absolute;left:{ncx - 215}px;top:{s1}px;width:430px;text-align:center;{D}font-weight:700;font-size:32px;{STROKE}z-index:10">Masquerade Sangeet</div>'
    sub2 = f'<div data-tag="sub2" style="position:absolute;left:{ncx - 135}px;top:{s2}px;width:270px;text-align:center;{D}font-weight:400;font-size:31px;{STROKE}z-index:10">Edition</div>'

    # hype eyebrow
    ey_y = bottom + 48
    eyebrow = f'<div data-tag="eyebrow" style="position:absolute;left:0;width:{W}px;top:{ey_y}px;text-align:center;{D}font-weight:700;font-size:40px;letter-spacing:.14em;{STROKE}z-index:20">The wait is almost over</div>'

    # the dialog card
    CW, CH, CR = 900, 300, 44
    cx0, cy0 = (W - CW) // 2, ey_y + 70
    top_h = 196
    bell = (f'<svg width="46" height="46" viewBox="0 0 46 46" style="margin-right:16px"><path d="M23 5c-7 0-11 5-11 12v8l-4 6h30l-4-6v-8c0-7-4-12-11-12z" fill="{BLUE}"/>'
            f'<path d="M18 36a5 5 0 0 0 10 0z" fill="{BLUE}"/></svg>')
    card = (f'<div data-tag="card" style="position:absolute;left:{cx0}px;top:{cy0}px;width:{CW}px;height:{CH}px;background:#F7F7F7;border-radius:{CR}px;z-index:12;'
            f'transform:rotate(-2deg);box-shadow:0 22px 64px rgba(0,0,0,.7),0 0 90px rgba(214,170,90,.28);overflow:hidden">'
            f'<div style="position:absolute;left:0;top:0;width:{CW}px;height:{top_h}px;display:flex;flex-direction:column;align-items:center;justify-content:center;'
            f'{D}font-weight:900;font-size:66px;line-height:1.04;color:#0a0a0a;text-align:center;white-space:nowrap">'
            f'<span>Location + date</span><span>revealed tomorrow</span></div>'
            f'<div style="position:absolute;left:0;top:{top_h}px;width:{CW}px;height:2px;background:#C9C9CE"></div>'
            f'<div style="position:absolute;left:0;top:{top_h + 2}px;width:{CW}px;height:{CH - top_h - 2}px;display:flex;align-items:center;justify-content:center;'
            f'{D}font-weight:700;font-size:48px;color:{BLUE}">{bell}Remind me</div></div>')
    # rotated bbox: a 900x330 card at 2 degrees draws ~ 900*cos+330*sin wide, 330*cos+900*sin tall
    rw, rh = 900 + 12, 300 + 32
    els = [("badge", 30, 96, bw, round(bw * 1005 / 1061)), ("mask", 266, 4, 827, 629), ("title", ix, iy, ink_w, ink_h),
           ("sub1", ncx - 215, s1, 430, 38), ("sub2", ncx - 135, s2, 270, 36), ("eyebrow", 90, ey_y, 900, 46),
           ("card", cx0 - 6, cy0 - 16, rw, rh)]
    text_pairs = [("card_head", "#0a0a0a", "#F7F7F7", 66, True), ("card_cta", BLUE, "#F7F7F7", 48, True)]
    return ground() + mask + badge + title + sub1 + sub2 + eyebrow + card, els, text_pairs


async def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    inner, els, text_pairs = build()
    html = B.page(W, H, "#000", inner, grain=False)
    async with B.session():
        await B.render(html, OUT, W, H, elements=els, containers=("card",), bleed_tags=("plate",), crop_tags=("plate", "card"), page_bg="#000",
                       text_pairs=text_pairs, collision_ignore=[("title", "sub1"), ("title", "sub2"), ("mask", "title")])
    print("done ->", OUT)
asyncio.run(main())
