"""DISCO DIWALI story (diya ground, string lights, copper mask: user, 2026-10-24 "in disco diwali branding"): call for stalls (nails, lip balm, press-ons), 2026-10-24. Text-led: no circle photo. Copy is the user's own, lightly cut to fit:
WE ARE LOOKING FOR STALLS / NAILS & PRESS-ONS, LIP BALM (nails and press-ons are one stall, user 2026-10-24) / INTERESTED OR KNOW SOMEONE? LET US KNOW. No contact method was supplied, so NO link pill and no handle.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_call.py -> out/discodiwali/stall_call/story.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_charity_ground as G
B = dd.B; W, H = 1080, 1920
OUT = os.path.join(ROOT, "out", "discodiwali", "stall_call")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
def story():
    parts, els = [G.ground_diya(W, H)], []
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:210px;width:150px;z-index:20">'); els.append(("badge", 40, 210, 150, 142))
    k = .499                                           # copper mask at the approved story position: visible outline 357..1059 x 98..536 (shifted below IG's top bar)
    mvw, mvh = 701, 438; mx, my = 358, 196
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(mx - 157 * k)}px;top:{round(my - 211 * k)}px;width:{round(1680 * k)}px;z-index:6;filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">'); els.append(("mask", mx, my, mvw, mvh))
    def line(tag, txt, top, size, weight, h, stroke=True, color="#fff"):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else f"color:{color};"}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("h1", "We are", 672, 118, 700, 118); line("h2", "looking for", 774, 118, 700, 118); line("h3", "stalls", 900, 170, 700, 190)
    line("k1", "Nails &amp; press-ons", 1150, 92, 700, 92, stroke=False, color=dd.GOLD)
    line("k2", "Lip balm", 1262, 92, 700, 92, stroke=False, color=dd.GOLD)
    line("ask1", "Interested or know someone?", 1440, 50, 700, 54, stroke=False)
    line("ask2", "Let us know", 1502, 50, 400, 54, stroke=False)
    vw = 300; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = 1566
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        inner, els, bottom = story(); print("last element ends at", bottom, "of", H)
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "story.png"), W, H, elements=els, bleed_tags=("plate", "mask", "lights"), crop_tags=("plate",), page_bg="#000",
                       text_pairs=[("h1", "#fff", "#000", 118, True), ("k1", "#FFC700", "#000", 92, True), ("ask1", "#fff", "#000", 50, True)])
asyncio.run(main())
