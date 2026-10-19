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
CANVAS = sys.argv[3] if len(sys.argv) > 3 else "feed"        # feed 1080x1350 | story 1080x1920
STORY = CANVAS == "story"
W, H = (1080, 1920) if STORY else (1080, 1350)
DT = 166 if STORY else 0                     # story: the top group clears Instagram's 200px profile bar
BLUE = "#1A73E8"
VER = sys.argv[1] if len(sys.argv) > 1 else "v1"
MASK = sys.argv[2] if len(sys.argv) > 2 else "corner"       # corner (chosen by user, 2026-10-19) | ref | centre | behind | corner
OUT = os.path.join(ROOT, "out", "discodiwali", f"reveal_tomorrow_{VER}_{MASK}{'_story' if STORY else ''}.png")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
D = "font-family:var(--d);text-transform:uppercase;"


def ground():
    """The approved diya ground: plate, string lights, gold dust and grain (same layer stack as dd_carousel_captcha.bg_layers)."""
    if STORY:      # taller than the plate's 4:5: stack TWO plates, the second flipped and faded in, so all four corners carry beading (DISCO_DIWALI.md rule 8)
        plates = (f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:1350px;z-index:1">'
                  f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - 1350}px;width:{W}px;height:1350px;z-index:1;transform:scaleY(-1);'
                  f'-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%)">')
    else:
        plates = f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'
    return (f'<div data-tag="plate" style="position:absolute;inset:0;z-index:1;background:#000"></div>' + plates +
            f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
            f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def build():
    # badge and mask: the approved classic placements (measured for poster_ref)
    bw = 210
    badge = f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:30px;top:{84 + DT}px;width:{bw}px;z-index:20">'
    # TOP BLOCK, three mask placements (argv[2]): ref = the approved classic (mask up-right), centre = mask centred over the lockup,
    # behind = a big tilted mask that the lockup overprints, corner = a small mask accent with a bigger title.
    # All three keep the lockup's notch tuck for the edition lines, positioned relative to the lockup's own ink box.
    P = dict(ref=dict(k=.4186, mcx=None, mx=None, my=None, tilt=0, t=.5129, ix=None, iy=None),
             centre=dict(k=.5, mcx=585, my=70, tilt=0, t=.5, iy="mask-130"),
             behind=dict(k=.58, mcx=645, my=104, tilt=7, t=.55, iy=350),
             corner=dict(k=.36, mcx=800, my=64, tilt=0, t=.58, iy=330))[MASK]
    k, t = P["k"], P["t"]
    ink_w, ink_h = round(1720 * t), round(916 * t)
    m_w, m_h = round(1408 * k), round(926 * k)
    if MASK == "ref":
        SC = .85
        X = lambda x: round((x - 554) * SC + 545); Y = lambda y: round((y - 108) * SC + 90)
        m_x, m_y, ix, iy = X(343), Y(108) + 24, X(35), Y(461)
    else:
        m_x, m_y = P["mcx"] - m_w // 2, P["my"] + DT
        ix = (W - ink_w) // 2 + 14
        iy = m_y + m_h - 130 if P["iy"] == "mask-130" else P["iy"] + DT
    tilt = P["tilt"]
    mask = (f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(m_x - 156 * k)}px;top:{round(m_y - 210 * k)}px;width:{round(1680 * k)}px;z-index:6;'
            f'transform:rotate({tilt}deg);transform-origin:{round((156 + 704) * k)}px {round((210 + 463) * k)}px;filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">')
    if tilt:    # a tilted mask draws a bigger footprint than its ink box
        import math
        r = math.radians(abs(tilt)); bw2, bh2 = m_w * math.cos(r) + m_h * math.sin(r), m_h * math.cos(r) + m_w * math.sin(r)
        m_x, m_y, m_w, m_h = round(m_x - (bw2 - m_w) / 2), round(m_y - (bh2 - m_h) / 2), round(bw2), round(bh2)
    title = f'<img data-tag="title" src="{dd.uri("title_lockup_noball.png")}" style="position:absolute;left:{round(ix - 264 * t)}px;top:{round(iy - 400 * t)}px;width:{round(2000 * t)}px;z-index:9">'
    bottom = iy + ink_h
    f = ink_w / 1038                                 # the notch tuck, scaled from the reference lockup
    s1w, s2w = round(520 * f), round(320 * f)
    s1x, s1, s2x, s2 = round(ix + 317 * f), round(iy + 456 * f), round(ix + 417 * f), round(iy + 501 * f)
    sub1 = f'<div data-tag="sub1" style="position:absolute;left:{s1x}px;top:{s1}px;width:{s1w}px;text-align:center;{D}font-weight:700;font-size:{round(38 * f)}px;{STROKE}z-index:10">Masquerade Sangeet</div>'
    sub2 = f'<div data-tag="sub2" style="position:absolute;left:{s2x}px;top:{s2}px;width:{s2w}px;text-align:center;{D}font-weight:400;font-size:{round(37 * f)}px;{STROKE}z-index:10">Edition</div>'

    # hype eyebrow
    ey_y = bottom + (60 if STORY else 34)
    eyebrow = f'<div data-tag="eyebrow" style="position:absolute;left:0;width:{W}px;top:{ey_y}px;text-align:center;{D}font-weight:700;font-size:{46 if STORY else 40}px;letter-spacing:.14em;{STROKE}z-index:20">The wait is almost over</div>'

    # the dialog card
    CW, CH, CR = (940, 380, 48) if STORY else (900, 300, 44)
    cx0, cy0 = (W - CW) // 2, ey_y + (84 if STORY else 64)
    top_h = 250 if STORY else 196
    hs, bs = (80, 56) if STORY else (66, 48)      # card headline / action-row type sizes
    bell = (f'<svg width="46" height="46" viewBox="0 0 46 46" style="margin-right:16px"><path d="M23 5c-7 0-11 5-11 12v8l-4 6h30l-4-6v-8c0-7-4-12-11-12z" fill="{BLUE}"/>'
            f'<path d="M18 36a5 5 0 0 0 10 0z" fill="{BLUE}"/></svg>')
    card = (f'<div data-tag="card" style="position:absolute;left:{cx0}px;top:{cy0}px;width:{CW}px;height:{CH}px;background:#F7F7F7;border-radius:{CR}px;z-index:12;'
            f'transform:rotate(-2deg);box-shadow:0 22px 64px rgba(0,0,0,.7),0 0 90px rgba(214,170,90,.28);overflow:hidden">'
            f'<div style="position:absolute;left:0;top:0;width:{CW}px;height:{top_h}px;display:flex;flex-direction:column;align-items:center;justify-content:center;'
            f'{D}font-weight:900;font-size:{hs}px;line-height:1.04;color:#0a0a0a;text-align:center;white-space:nowrap">'
            f'<span>Location + date</span><span>reveal tomorrow</span></div>'
            f'<div style="position:absolute;left:0;top:{top_h}px;width:{CW}px;height:2px;background:#C9C9CE"></div>'
            f'<div style="position:absolute;left:0;top:{top_h + 2}px;width:{CW}px;height:{CH - top_h - 2}px;display:flex;align-items:center;justify-content:center;'
            f'{D}font-weight:700;font-size:{bs}px;color:{BLUE}">{bell}Remind me</div></div>')
    # rotated bbox: a 900x330 card at 2 degrees draws ~ 900*cos+330*sin wide, 330*cos+900*sin tall
    rw, rh = CW + 12, CH + 32
    els = [("badge", 30, 84 + DT, bw, round(bw * 1005 / 1061)), ("mask", m_x, m_y, m_w, m_h), ("title", ix, iy, ink_w, ink_h),
           ("sub1", s1x, s1, s1w, 38), ("sub2", s2x, s2, s2w, 36), ("eyebrow", 90, ey_y, 900, 52),
           ("card", cx0 - 6, cy0 - 16, rw, rh)]
    text_pairs = [("card_head", "#0a0a0a", "#F7F7F7", hs, True), ("card_cta", BLUE, "#F7F7F7", bs, True)]
    return ground() + mask + badge + title + sub1 + sub2 + eyebrow + card, els, text_pairs


async def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    inner, els, text_pairs = build()
    html = B.page(W, H, "#000", inner, grain=False)
    async with B.session():
        await B.render(html, OUT, W, H, elements=els, containers=("card",), bleed_tags=("plate",), crop_tags=("plate", "card"), page_bg="#000",
                       text_pairs=text_pairs, collision_ignore=[("title", "sub1"), ("title", "sub2"), ("mask", "title"), ("badge", "mask")])
    print("done ->", OUT)
asyncio.run(main())
