"""DISCO DIWALI carousel, "CAPTCHA" idea (inspo: a 'Choose everything related to...' verification card over a party photo).

Four 1080x1350 slides on the approved diya ground (black, navy and gold lotus-diya corners fading to black, string lights):
  1  COVER: title lockup, copper mask, LIVE badge, an "I'M NOT A ROBOT" checkbox hook and a swipe cue
  2  the captcha, nine REAL event photos in the 3x3 grid, nothing selected yet
  3  the same card, all nine selected (tiles inset, tick badges), the button now says VERIFIED
  4  ALL FOR CHARITY + date and time + LINK IN BIO pill
(The earlier reveal slide, the poster_ref design with the status lines, was removed by the user, 2026-10-14.)

Adaptations recorded (CLAUDE.md sec 2 precedence ladder):
  - The captcha card is a DESIGN DEVICE, not a fabricated UI screenshot: no reCAPTCHA marks, every tile is a real AQ photo, the button is ours.
  - The inspo's boast ("the best parties in the city") is replaced with "Related to Disco Diwali": the claim cannot be backed from AQ_FACTS.
  - The captcha header keeps the inspo's blue because the blue bar IS the recognisable mechanism; it is the only blue on the carousel.
  - Type is NeutralFace throughout (user, 2026-10-13); white with a thin black border on the photo slides.
  - No price, venue or lineup appears anywhere: none has been supplied.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_carousel_captcha.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
BLUE = "#1A73E8"
OUT = os.path.join(ROOT, "out", "discodiwali", "carousel")

# (photo, object-position): nine distinct frames, colour-varied so the grid does not read as one smear
TILES = [("06", "50% 40%"), ("07", "50% 30%"), ("03", "50% 30%"),
         ("11", "50% 40%"), ("05", "50% 50%"), ("13", "50% 25%"),
         ("10", "50% 40%"), ("09", "50% 60%"), ("12", "50% 50%")]
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"

CARD_W, PAD, GAP = 740, 28, 8
CARD_X = (W - CARD_W) // 2
INNER = CARD_W - 2 * PAD
TILE = (INNER - 2 * GAP) // 3
HEAD_H = 214
GRID_Y = PAD + HEAD_H + 12
GRID_H = 3 * TILE + 2 * GAP
FOOT_H = 96
CARD_H = GRID_Y + GRID_H + 12 + FOOT_H + 12
CARD_Y = 164


def bg_layers(photo=None, dim=0):
    """The approved poster ground (user, 2026-10-14, "i want this blue effect"): black, the navy and gold lotus-diya plate glowing in the
    corners and fading to black through the middle, the two sagging string lights, then the format's gold dust and film grain screened on top."""
    return (f'<div data-tag="plate" style="position:absolute;inset:0;z-index:1;background:#000"></div>'
            f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'
            f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
            f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def badge(x, y, w):
    return (f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:20">', (x, y, w, round(w * 1005 / 1061)))


def icons():
    g = "#6b6b6b"
    refresh = f'<svg width="50" height="50" viewBox="0 0 50 50"><path d="M38 17a15 15 0 1 0 3 11" fill="none" stroke="{g}" stroke-width="5" stroke-linecap="round"/><path d="M40 6v13H27z" fill="{g}"/></svg>'
    phones = f'<svg width="50" height="50" viewBox="0 0 50 50"><path d="M8 32V25a17 17 0 0 1 34 0v7" fill="none" stroke="{g}" stroke-width="5"/><rect x="5" y="29" width="10" height="16" rx="4" fill="{g}"/><rect x="35" y="29" width="10" height="16" rx="4" fill="{g}"/></svg>'
    info = f'<svg width="50" height="50" viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke="{g}" stroke-width="5"/><rect x="22.5" y="22" width="5" height="15" fill="{g}"/><circle cx="25" cy="15" r="3.2" fill="{g}"/></svg>'
    return f'<div style="display:flex;gap:34px;align-items:center">{refresh}{phones}{info}</div>'


def captcha_slide(bg, sub, selected, button):
    tiles = []
    for i, (ph, pos) in enumerate(TILES):
        c, r = i % 3, i // 3
        x, y = c * (TILE + GAP), r * (TILE + GAP)
        inset = 20 if selected else 0
        tick = ""
        if selected:
            tick = (f'<div style="position:absolute;left:-6px;top:-6px;width:46px;height:46px;border-radius:50%;background:{BLUE};border:4px solid #fff;z-index:3;display:flex;align-items:center;justify-content:center">'
                    f'<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12.5l5 5 9-11" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
        tiles.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{TILE}px;height:{TILE}px;background:#ddd">'
                     f'<div style="position:absolute;left:{inset}px;top:{inset}px;right:{inset}px;bottom:{inset}px">'
                     f'<img src="{dd.photo_uri(ph, 700)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};filter:saturate(1.15) contrast(1.05)">{tick}</div></div>')
    head = (f'<div style="position:absolute;left:{PAD}px;top:{PAD}px;width:{INNER}px;height:{HEAD_H}px;background:{BLUE};color:#fff;font-family:var(--d);text-transform:uppercase;overflow:hidden">'
            f'<div style="position:absolute;left:24px;top:16px;font-size:32px;font-weight:400;letter-spacing:.5px">Choose everything</div>'
            f'<div style="position:absolute;left:24px;top:54px;font-size:50px;font-weight:700;line-height:.98;width:{INNER - 48}px">Related to<br>Disco Diwali</div>'
            f'<div style="position:absolute;left:24px;top:{HEAD_H - 52}px;font-size:30px;font-weight:400">{sub}</div></div>')
    foot_y = GRID_Y + GRID_H + 12
    foot = (f'<div style="position:absolute;left:{PAD + 12}px;top:{foot_y + 23}px;width:300px;height:50px">{icons()}</div>'
            f'<div style="position:absolute;right:{PAD}px;top:{foot_y}px;width:270px;height:{FOOT_H}px;background:{BLUE};color:#fff;font-family:var(--d);font-weight:700;font-size:38px;text-transform:uppercase;display:flex;align-items:center;justify-content:center">{button}</div>')
    card = (f'<div data-tag="card" style="position:absolute;left:{CARD_X}px;top:{CARD_Y}px;width:{CARD_W}px;height:{CARD_H}px;background:#fff;z-index:10;box-shadow:0 18px 60px rgba(0,0,0,.55)">'
            f'{head}<div style="position:absolute;left:{PAD}px;top:{GRID_Y}px;width:{INNER}px;height:{GRID_H}px">{"".join(tiles)}</div>{foot}</div>')
    bd, bd_box = badge(48, 30, 112)
    cue = (f'<div data-tag="cue" style="position:absolute;left:0;width:{W}px;top:{CARD_Y + CARD_H + 30}px;text-align:center;font-family:var(--d);font-weight:700;font-size:38px;text-transform:uppercase;{STROKE}z-index:20">Swipe to verify &rarr;</div>')
    cue_box = (W // 2 - 220, CARD_Y + CARD_H + 30, 440, 44)
    els = [("card", CARD_X, CARD_Y, CARD_W, CARD_H), ("badge",) + bd_box, ("cue",) + cue_box]
    return bg_layers() + card + bd + cue, els


def cover_slide():
    """Cover: the approved title lockup, copper mask and LIVE badge on the diya ground (positions measured for poster_ref), then the hook, a
    captcha checkbox reading I'M NOT A ROBOT, which the next slide answers. No date, no status line: the cover only has to stop the thumb."""
    k, t = .4925, .6034
    bd, bd_box = badge(30, 122, 267)
    mask = (f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(343 - 157 * k)}px;top:{round(108 - 211 * k)}px;width:{round(1680 * k)}px;z-index:6;'
            f'filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">')
    title = (f'<img data-tag="title" src="{dd.uri("title_lockup_noball.png")}" style="position:absolute;left:{round(35 - 265 * t)}px;top:{round(461 - 401 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    sub1 = (f'<div data-tag="sub1" style="position:absolute;left:352px;top:917px;width:520px;text-align:center;font-family:var(--d);font-weight:700;font-size:38px;text-transform:uppercase;{STROKE}z-index:10">Masquerade Sangeet</div>')
    sub2 = (f'<div data-tag="sub2" style="position:absolute;left:452px;top:962px;width:320px;text-align:center;font-family:var(--d);font-weight:400;font-size:37px;text-transform:uppercase;{STROKE}z-index:10">Edition</div>')
    PW, PH, PY = 640, 104, 1086
    pill = (f'<div data-tag="check" style="position:absolute;left:{(W - PW) // 2}px;top:{PY}px;width:{PW}px;height:{PH}px;background:#fff;border-radius:14px;z-index:12;box-shadow:0 14px 44px rgba(0,0,0,.55)">'
            f'<div style="position:absolute;left:26px;top:{(PH - 58) // 2}px;width:58px;height:58px;border:5px solid #b9b9b9;border-radius:8px;background:#fff;box-sizing:border-box"></div>'
            f'<div style="position:absolute;left:112px;top:0;height:{PH}px;display:flex;align-items:center;font-family:var(--d);font-weight:700;font-size:44px;text-transform:uppercase;color:#0a0a0a;white-space:nowrap">I\'m not a robot</div></div>')
    cue = (f'<div data-tag="cue" style="position:absolute;left:0;width:{W}px;top:1238px;text-align:center;font-family:var(--d);font-weight:700;font-size:38px;text-transform:uppercase;{STROKE}z-index:20">Swipe &rarr;</div>')
    els = [("mask", 343, 108, 692, 452), ("badge",) + bd_box, ("title", 35, 461, 1036, 551), ("sub1", 352, 917, 520, 44), ("sub2", 452, 962, 320, 40),
           ("check", (W - PW) // 2, PY, PW, PH), ("cue", W // 2 - 140, 1238, 280, 44)]
    return bg_layers() + mask + bd + title + sub1 + sub2 + pill + cue, els


def charity_slide():
    bd, bd_box = badge(64, 64, 215)
    mask = (f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:370px;top:20px;width:700px;z-index:12">')
    heading = (f'<div data-tag="heading" style="position:absolute;left:0;width:{W}px;top:520px;text-align:center;font-family:var(--d);font-weight:700;font-size:170px;line-height:.92;text-transform:uppercase;{STROKE}z-index:20">All for<br>charity</div>')
    date = (f'<div data-tag="date" style="position:absolute;left:0;width:{W}px;top:860px;text-align:center;font-family:var(--d);font-weight:700;font-size:66px;text-transform:uppercase;{STROKE}z-index:20">10th November, 2026</div>'
            f'<div data-tag="time" style="position:absolute;left:0;width:{W}px;top:950px;text-align:center;font-family:var(--d);font-weight:700;font-size:50px;text-transform:uppercase;{STROKE}z-index:20">4:30 PM onwards</div>')
    ed = (f'<div data-tag="edition" style="position:absolute;left:0;width:{W}px;top:1030px;text-align:center;font-family:var(--d);font-weight:400;font-size:40px;text-transform:uppercase;{STROKE}z-index:20">Masquerade Sangeet Edition</div>')
    pill = (f'<div data-tag="pill" style="position:absolute;left:{(W - 560) // 2}px;top:1130px;width:560px;height:104px;border:2px solid rgba(214,170,90,.7);border-radius:26px;background:rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:48px;text-transform:uppercase;{STROKE}z-index:20">Link in bio</div>')
    els = [("badge",) + bd_box, ("mask", 435, 108, 585, 384), ("heading", 120, 520, 840, 320), ("date", 120, 860, 840, 70),
           ("time", 220, 950, 640, 52), ("edition", 140, 1030, 800, 44), ("pill", (W - 560) // 2, 1130, 560, 104)]
    return bg_layers() + bd + mask + heading + date + ed + pill, els


async def main():
    os.makedirs(OUT, exist_ok=True)
    slides = [cover_slide(),
              captcha_slide("08", "Masquerade Sangeet Edition", False, "Verify"),
              captcha_slide("08", "Yes, all nine", True, "Verified"),
              charity_slide()]
    async with B.session():
        for n, s in enumerate(slides, 1):
            path = os.path.join(OUT, f"slide_{n}.png")
            html_inner, els = s
            html = B.page(W, H, "#000", html_inner, grain=False)
            await B.render(html, path, W, H, elements=els, containers=("card",), bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000",
                           collision_ignore=[("title", "sub1"), ("title", "sub2"), ("mask", "title")])
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i}.png")).convert("RGB").resize((432, 540)) for i in range(1, 5)]
    sh = Image.new("RGB", (432 * 4 + 30, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png")); print("carousel done ->", OUT)
asyncio.run(main())
