"""DISCO DIWALI story (diya ground, string lights, copper mask: user, 2026-10-24 "in disco diwali branding"): sponsor invite (nails, lip balm, press-ons), 2026-10-24. Text-led: no circle photo. Copy is the user's own, lightly cut to fit:
WE ARE LOOKING FOR STALLS / NAILS & PRESS-ONS, LIP BALM (nails and press-ons are one stall, user 2026-10-24) / INTERESTED OR KNOW SOMEONE? LET US KNOW. No contact method was supplied, so NO link pill and no handle.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_sponsor_invite.py -> out/discodiwali/sponsor_invite/story.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_photo_bg as PB, dd_copper as CP
B = dd.B; W, H = 1080, 1920
OUT = os.path.join(ROOT, "out", "discodiwali", "sponsor_invite")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
def story():
    parts, els = [PB.photo_ground(dd, W, H, "14_03", "50% 0%", dim=.76)], []
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:210px;width:150px;z-index:20">'); els.append(("badge", 40, 210, 150, 142))
    ss = 300; sx, sy = 1040 - ss, 230
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sy}px;z-index:12">{CP.diya(ss, 8)}</div>'); els.append(("sticker", sx, sy, ss, round(ss * .72)))
    def line(tag, txt, top, size, weight, h, stroke=True, color="#fff"):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else f"color:{color};"}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("h1", "Sponsor", 470, 190, 700, 190); line("h2", "Disco Diwali", 668, 128, 700, 128)
    line("o1", "We are open to", 880, 50, 400, 54, stroke=False)
    line("o2", "in-kind and monetary", 944, 62, 700, 66, stroke=False)
    line("o3", "sponsorship", 1016, 62, 700, 66, stroke=False)
    line("lab", "What you get in return", 1150, 60, 700, 64, stroke=False, color=dd.GOLD)
    for i, t in enumerate(("Media coverage", "Logos on all creatives and banners", "Google reviews", "Standee or stall on the event day")):
        line(f"g{i}", t, 1246 + i * 76, 46, 700, 50, stroke=False)
    line("g4", "And a lot more", 1246 + 4 * 76 + 6, 46, 700, 50, stroke=False)
    vw = 300; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = 1654
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        inner, els, bottom = story(); print("last element ends at", bottom, "of", H)
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "story.png"), W, H, elements=els, bleed_tags=("plate", "lights"), crop_tags=("plate",), page_bg="#000",
                       text_pairs=[("h1", "#fff", "#000", 190, True), ("lab", "#FFC700", "#000", 60, True), ("g0", "#fff", "#000", 46, True)])
asyncio.run(main())
