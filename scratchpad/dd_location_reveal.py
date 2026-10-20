"""DISCO DIWALI location reveal poster, feed (1080x1350) and story (1080x1920). Inspo: a flat-lay photo of a rounded map card tilted on the ground,
with round white map buttons and a Memoji pin bubble.

Composition, back to front: black ground, the approved navy diya plate with string lights, a map card (the user's own map screenshot, rounded, tilted
-5 degrees, hard shadow and hairline edge) carrying a "3D" button and a compass pill like the inspo, the copper mask lying across its top-right corner, the LIVE
badge top left, then a ROOFTOP tag, the venue and its address, and the DISCO DIWALI lockup (with its ball) as a small footer mark. No pill and no edition line (user).

Facts (all supplied by the user, 2026-10-19): the event is on a ROOFTOP; venue "60, Chowringhee Banquets"; address "60, Chowringhee Road, Bishop Lefroy Rd, Kolkata, West Bengal 700020".
NO date or time (user choice). No price or lineup. The map is the user's real screenshot, never redrawn, so no street label is mine.
Adaptations: the inspo's Memoji pin avatar is dropped (the red venue pin in the screenshot carries the pointing); the map buttons are drawn here with no Apple or Google marks; type is NeutralFace, white with a thin black border.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_location_reveal.py"""
import asyncio, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "location")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
VENUE = ("60, Chowringhee", "Banquets")
ADDR = ("60, Chowringhee Road, Bishop Lefroy Rd,", "Kolkata, West Bengal 700020")
TILT = -5                                   # the screenshot is 1080x508: any card width w keeps its aspect at h = w * 508 / 1080
BLUE = "#1A73E8"
DEFAULT_VARIANT = "below"                             # chosen by the user, 2026-10-19: "ON THE ROOFTOP" below the address
VARIANT = os.environ.get("ROOFTOP", DEFAULT_VARIANT)   # how the rooftop is mentioned: below | tag | plain_above | callout


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_photo_bg as _pb
PHOTO, PHOTO_POS = "07_12", "50% 20%"             # carousel background photo (user, 2026-10-20: "use a photo in the bg of the carousel"); BG=diya restores the plate-only ground


def ground(H):
    if os.environ.get("BG") == "diya":
        return ground_diya(H)
    return _pb.photo_ground(dd, W, H, PHOTO, PHOTO_POS)


def ground_diya(H):
    """Black, the diya plate (two plates on a tall canvas, the second flipped and faded in, format rule 8), string lights, gold dust, grain."""
    plate = lambda top, extra="": (f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{top}px;width:{W}px;height:1350px;'
                                   f'object-fit:cover;z-index:1;{extra}">')
    p = '<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>' + plate(0)
    if H > 1350:
        p += plate(H - 1350, "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
    p += (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
          f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
          f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return p


def map_card(cx, cy, MAP_W, callout=False):
    MAP_H = round(MAP_W * 508 / 1080)
    left, top = cx - MAP_W // 2, cy - MAP_H // 2
    three_d = (f'<div style="position:absolute;left:30px;top:30px;width:92px;height:92px;border-radius:50%;background:#fff;box-shadow:0 8px 22px rgba(0,0,0,.35);'
               f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:40px;color:#0a0a0a">3D</div>')
    nav = (f'<div style="position:absolute;right:30px;bottom:30px;width:96px;height:176px;border-radius:48px;background:#fff;box-shadow:0 8px 22px rgba(0,0,0,.35);'
           f'display:flex;flex-direction:column;align-items:center;justify-content:space-evenly">'
           f'<svg width="46" height="46" viewBox="0 0 46 46"><path d="M5 12l12-4 12 4 12-4v26l-12 4-12-4-12 4z" fill="#0a0a0a"/><path d="M17 8v26M29 12v26" stroke="#fff" stroke-width="3"/></svg>'
           f'<svg width="46" height="46" viewBox="0 0 46 46"><path d="M40 6L6 20l14 4 4 14z" fill="{BLUE}"/></svg></div>')
    call = ""
    if callout:                       # a black map-annotation pill sitting just above the red venue pin of the screenshot (pin head at ~525,198 of 1080x508)
        k = MAP_W / 1080
        call = (f'<div style="position:absolute;left:{round(525 * k - 95)}px;top:{round(190 * k - 62)}px;width:190px;height:56px;border-radius:28px;background:#0a0a0a;border:2px solid rgba(214,170,90,.85);'
                f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:30px;letter-spacing:5px;text-indent:5px;color:#fff;text-transform:uppercase">Rooftop</div>')
    card = (f'<div data-tag="card" style="position:absolute;left:{left}px;top:{top}px;width:{MAP_W}px;height:{MAP_H}px;border-radius:44px;overflow:hidden;z-index:10;'
            f'transform:rotate({TILT}deg);box-shadow:0 40px 70px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.55)">'
            f'<img src="{dd.uri("map_60_chowringhee.jpg")}" style="width:{MAP_W}px;height:{MAP_H}px;object-fit:cover;display:block">{three_d}{nav}{call}</div>')
    return card, rot_box(cx, cy, MAP_W, MAP_H, TILT)


def poster(H):
    """Top: the LIVE badge. Middle: the map card with the copper mask on its top-right corner, then the reveal copy. Footer: the DISCO DIWALI lockup
    (with its ball) as a small mark, like the reference chat slide. No pill and no edition line (user, 2026-10-19)."""
    story = H > 1350
    card_w = 960                                              # 960 wide: the card is the hero, its tilted box spans ~995px
    card_top = 470 if story else 200                          # top of the card's tilted bounding box
    card_h = round(card_w * 508 / 1080)
    cy = card_top + (rot_box(0, 0, card_w, card_h, TILT)[3] + 1) // 2
    vsize = 90 if story else 84
    parts, els = [ground(H)], []
    # LIVE badge top left (story keeps the top 200px clear of the profile bar)
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # map card, then the copper mask lying across its top-right corner (the placement the user preferred)
    card, box = map_card(540, cy, card_w, callout=(VARIANT == "callout")); parts.append(card); els.append(("card",) + box)
    mw = 330
    mx, my = 730, box[1] - 62
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{mx}px;top:{my}px;width:{mw}px;z-index:12;transform:rotate(10deg);'
                 f'filter:drop-shadow(0 12px 26px rgba(0,0,0,.65))">'); els.append(("mask", mx + 30, my + 40, 276, 196))
    # reveal copy
    y = box[1] + box[3] + (34 if story else 24)
    def line(tag, txt, top, size, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 70, top, 940, h))
    if VARIANT == "tag":
        tag_w, tag_h = 300, 58                                # ROOFTOP tag: a gold-edged pill above the venue
        parts.append(f'<div data-tag="rooftop" style="position:absolute;left:{(W - tag_w) // 2}px;top:{y}px;width:{tag_w}px;height:{tag_h}px;box-sizing:border-box;border:2px solid rgba(214,170,90,.8);'
                     f'border-radius:29px;background:rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:32px;'
                     f'letter-spacing:8px;text-indent:8px;text-transform:uppercase;{STROKE}z-index:20">Rooftop</div>'); els.append(("rooftop", (W - tag_w) // 2, y, tag_w, tag_h))
        y += tag_h + 14
    elif VARIANT == "plain_above":
        line("rooftop", "Rooftop", y, 36, 400, 38, "letter-spacing:9px;"); y += 52
    else:
        y += 6
    line("venue1", VENUE[0], y, vsize, 700, vsize); y += vsize - 4
    line("venue2", VENUE[1], y, vsize, 700, vsize); y += vsize + 14
    line("addr1", ADDR[0], y, 30, 400, 32); y += 38
    line("addr2", ADDR[1], y, 30, 400, 32)
    if VARIANT == "below":
        y += 52; line("rooftop", "On the rooftop", y, 38, 700, 40)
    # footer mark: the lockup with its ball, centred, visible box 265..1982 x 320..1311 of the 2000x1382 asset
    vw = 400 if story else 300
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    vy = (1420 if story else H - 64 - vh)
    vy = max(vy, y + 32 + 40)
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, (f"{name}.png" if VARIANT == DEFAULT_VARIANT else f"var_{VARIANT}_{name}.png")), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card"),
                           page_bg="#000", collision_ignore=[("mask", "card"), ("card", "badge")])
    print("location reveal done ->", OUT)
asyncio.run(main())
