"""DISCO DIWALI static WhatsApp poster (1080x1350) with BOTH the date and the location revealed (user, 2026-10-21).

Facts, all supplied by the user: Tuesday 10 November 2026 (weekday derived from the date), 4:30 PM onwards, "Masquerade Sangeet Edition", venue "60, Chowringhee Banquets",
address "60, Chowringhee Road, Bishop Lefroy Rd, Kolkata, West Bengal 700020", ON THE ROOFTOP, ALL FOR CHARITY (the badge). No link pill (WhatsApp), no price, no lineup, no DJ.
The "two days after Diwali / one day before Bhai Dooj" line is DELIBERATELY LEFT OFF: it is unconfirmed against a Kolkata panchang (brain/DISCO_DIWALI.md) and a poster that
states the date and venue as fact should not carry a festival-calendar claim nobody has checked.
Layout, distinct from the reveal slides: photo ground, LIVE badge, a big date block (copper calendar sticker), the user's map screenshot on a tilted card with the copper pin,
venue + address + rooftop, the lockup as a footer mark. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_info.py
"""
import asyncio, datetime, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_copper as cp
import dd_photo_bg as pb
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "wa_info")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
DAY = datetime.date(2026, 11, 10)
WEEKDAY = DAY.strftime("%A")                                  # derived, not typed
TILT = -4


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


def build():
    parts, els = [pb.photo_ground(dd, W, H, "07_06", "50% 35%", dim=.70, bright=.9)], []

    def text(tag, txt, y, size, weight=700, x=0, w=W, align="center", extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;width:{w}px;top:{y}px;text-align:{align};font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                     f'line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, x, y, w, round(size * .88)))

    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:40px;width:150px;z-index:20">'); els.append(("badge", 40, 40, 150, round(150 * 1005 / 1061)))
    # date block
    text("weekday", WEEKDAY, 120, 54, 400, x=250, w=580, extra="letter-spacing:10px;")
    text("date", f"{DAY.day} November", 190, 128, x=40, w=1000)
    text("year", f"{DAY.year}  &middot;  4:30 PM onwards", 330, 54, 700, x=40, w=1000)
    parts.append(f'<div data-tag="sticker_cal" style="position:absolute;left:905px;top:28px;z-index:12">{cp.calendar(135, 10, "wc")}</div>'); els.append(("sticker_cal", 905, 28, 135, 135))
    # map card
    mw = 700; mh = round(mw * 508 / 1080); cx, cy = 540, 610
    bx, by, bw, bh = rot_box(cx, cy, mw, mh, TILT)
    parts.append(f'<div data-tag="card" style="position:absolute;left:{cx - mw // 2}px;top:{cy - mh // 2}px;width:{mw}px;height:{mh}px;border-radius:38px;overflow:hidden;z-index:10;transform:rotate({TILT}deg);'
                 f'box-shadow:0 36px 64px rgba(0,0,0,.65),0 0 0 3px rgba(255,255,255,.55)"><img src="{dd.uri("map_60_chowringhee.jpg")}" style="width:{mw}px;height:{mh}px;object-fit:cover;display:block"></div>')
    els.append(("card", bx, by, bw, bh))
    parts.append(f'<div data-tag="sticker_pin" style="position:absolute;left:{bx - 40}px;top:{by - 30}px;z-index:12">{cp.pin(210, -12, "wp")}</div>'); els.append(("sticker_pin", bx - 40, by - 30, 210, 210))
    y = by + bh + 34
    text("v1", "60, Chowringhee", y, 76); text("v2", "Banquets", y + 70, 76)
    text("addr1", "60, Chowringhee Road, Bishop Lefroy Rd,", y + 158, 28, 400); text("addr2", "Kolkata, West Bengal 700020", y + 192, 28, 400)
    text("roof", "On the rooftop", y + 238, 40)
    vw = 250; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = H - 56 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, y + 238 + 35, vy


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, text_end, lock_top = build()
    print(f"[wa_info] text ends y={text_end}, lockup starts y={lock_top} (gap {lock_top - text_end})")
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "poster.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card"),
                       page_bg="#000", collision_ignore=[("sticker_pin", "card")])
    print("wa info done ->", OUT)
asyncio.run(main())
