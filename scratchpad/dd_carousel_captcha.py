"""DISCO DIWALI carousel, "CAPTCHA" idea (inspo: a 'Choose everything related to...' verification card over a party photo).

Four 1080x1350 slides on a BLACK ground lit by the blue-style effects (screened blue light, disco beams, RGB-split title):
  1  the captcha, nine REAL event photos in the 3x3 grid, nothing selected yet
  2  the same card, all nine selected (tiles inset, tick badges), the button now says VERIFIED
  3  the reveal: the approved poster_ref design (RGB-split title lockup, copper mask, LIVE badge) on the black + blue ground
  4  ALL FOR CHARITY + date and time + LINK IN BIO pill

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


def blue_layers(W=W, H=H):
    """The blue-style recipe (blend-mode lab v7) re-cut for a BLACK ground. Colour-dodge needs something to burn, so on pure ink the blue
    light is SCREENed instead: a hot glow in the top right corner and the same repeating-conic disco beams
    (radial-masked so they fade before the type zone). Every layer is tagged plate: deliberate full bleed."""
    def lay(css, z):
        return f'<div data-tag="plate" style="position:absolute;inset:0;z-index:{z};pointer-events:none;{css}"></div>'
    beam_mask = "radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.45) 34%,transparent 66%)"
    return (lay("background:radial-gradient(circle at 88% 4%,rgba(61,123,255,.62) 0%,rgba(20,60,220,0) 40%);mix-blend-mode:screen", 2)
            + lay("background:repeating-conic-gradient(from 188deg at 88% -6%,rgba(120,175,255,.95) 0deg 3deg,transparent 3deg 10deg);"
                  f"-webkit-mask-image:{beam_mask};mask-image:{beam_mask};mix-blend-mode:screen;opacity:.62", 3))


def bg_layers(photo=None, dim=0):
    """Black ground, the blue light and beams, then the format's own gold dust and film grain screened over everything."""
    return (f'<div data-tag="plate" style="position:absolute;inset:0;z-index:1;background:#000"></div>' + blue_layers()
            + f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


class BluePoster(dd.Poster):
    """poster_ref on the black + blue ground: swaps the diya plate for the blue layers and RGB-splits the title lockup."""
    def img(self, name, *a, **k):
        if name == "bg_diya_portrait.jpg":
            self.parts.append(dd.BLUE_DEFS + '<div data-tag="plate" style="position:absolute;inset:0;z-index:1;background:#000"></div>' + blue_layers(self.W, self.H))
            return
        if name == "title_lockup_noball.png":
            k["extra"] = k.get("extra", "") + "filter:url(#ca);"
        return super().img(name, *a, **k)


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
    slides = [captcha_slide("08", "Masquerade Sangeet Edition", False, "Verify"),
              captcha_slide("08", "Yes, all nine", True, "Verified"),
              None, charity_slide()]
    dd.Poster = BluePoster
    async with B.session():
        for n, s in enumerate(slides, 1):
            path = os.path.join(OUT, f"slide_{n}.png")
            if s is None:
                await dd.render_poster("poster_ref", dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon",
                                                          note="More details to follow", link=False), "feed", path)
                continue
            html_inner, els = s
            html = B.page(W, H, "#000", html_inner, grain=False)
            await B.render(html, path, W, H, elements=els, containers=("card",), bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000")
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i}.png")).convert("RGB").resize((432, 540)) for i in range(1, 5)]
    sh = Image.new("RGB", (432 * 4 + 30, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png")); print("carousel done ->", OUT)
asyncio.run(main())
