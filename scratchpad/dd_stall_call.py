"""DISCO DIWALI "LAST CALL FOR STALLS" story (1080x1920), for stall owners who showed interest.

Same skeleton as dd_charity.py (photo ground, string lights, small LIVE badge top left, copper mask top right, NeutralFace stroked headline, lockup with ball as the mark).
Facts printed, all supplied: Disco Diwali, Masquerade Sangeet Edition, 10th November 2026. NOT printed: any deadline (by design), apply route, fee, venue.
A link-sticker zone (640x165 at y=1505, the launch pack's) is declared and left clear for the native Instagram link sticker, so the apply route is added in-app.
No deadline is printed, by design (user, 2026-10-21). Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_call.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_photo_bg as _pb
B = dd.B
W, H = 1080, 1920
OUT = os.path.join(ROOT, "out", "discodiwali", "stall_call")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GOLD = "color:#E8C26A;-webkit-text-stroke:3px #000;paint-order:stroke fill;"


def poster():
    parts, els = [_pb.photo_ground(dd, W, H, "07_03", "50% 55%")], []
    def put(html, tag, box): parts.append(html); els.append((tag,) + box)
    put(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:210px;width:150px;z-index:20">', "badge", (40, 210, 150, 142))
    mw = 470; mh = round(mw * 1278 / 1680)
    put(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{1040 - mw}px;top:170px;width:{mw}px;z-index:6">', "mask", (1040 - mw, 170, mw, mh))
    def line(tag, txt, top, fsize, weight, extra=STROKE):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;'
                     f'line-height:1;text-transform:uppercase;white-space:nowrap;{extra}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, fsize))
    size = 146
    line("head1", "Last call", 640, size, 700)
    line("head2", "for stalls", 640 + round(size * .96), size, 700)
    y = 640 + round(size * .96) * 2 + 28
    line("sub", "Disco Diwali &middot; Masquerade Sangeet Edition", y, 38, 400); y += 70
    line("date", "10th November 2026", y, 52, 700, GOLD); y += 80
    vw = 400; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = max(y + 60, 1120)
    put(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">', "title", (vx, vy, vw, vh))
    line("cue", "Stall owners, apply here &darr;", 1450, 34, 700, GOLD)
    els.append(("linkzone", 220, 1505, 640, 165))
    return "".join(parts), els


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els = poster()
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "story.png"), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000", collision_ignore=[])
    print("done ->", OUT)
asyncio.run(main())
