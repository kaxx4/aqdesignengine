"""DISCO DIWALI story: call for a NAILS & PRESS-ONS stall (user, 2026-10-24: "use the photo i used"): the glitter-table crop in the circle, copper star, new photo ground.
Copy: LOOKING FOR / NAILS & PRESS-ONS / STALLS, then INTERESTED OR KNOW SOMEONE? LET US KNOW. No contact supplied, so no pill.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_nails.py -> out/discodiwali/stall_nails/story.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_photo_bg as PB, dd_copper as CP
B = dd.B; W, H = 1080, 1920
OUT = os.path.join(ROOT, "out", "discodiwali", "stall_nails")
PHOTO = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-glitter", "01_glitter-table-crop.jpg")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
def story():
    parts, els = [PB.photo_ground(dd, W, H, "14_08", "50% 30%", dim=.7)], []
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:210px;width:150px;z-index:20">'); els.append(("badge", 40, 210, 150, 142))
    d, cx, cy = 640, 220, 330
    parts.append(f'<div data-tag="circle" style="position:absolute;left:{cx}px;top:{cy}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:8px solid {dd.GOLD};box-sizing:border-box;z-index:10;'
                 f'box-shadow:0 14px 40px rgba(0,0,0,.6)"><img src="{dd.photo_uri(PHOTO)}" style="width:100%;height:100%;object-fit:cover;object-position:50% 50%"></div>'); els.append(("circle", cx, cy, d, d))
    ss = 280; sx, sy = 1040 - ss, 230
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sy}px;z-index:12">{CP.star(ss, -12)}</div>'); els.append(("sticker", sx, sy, ss, ss))
    def line(tag, txt, top, size, weight, h, stroke=True, color="#fff"):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else f"color:{color};"}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("h1", "Looking for", 1010, 96, 700, 96)
    line("h2", "Nails &amp;", 1124, 150, 700, 150); line("h3", "Press-ons", 1272, 150, 700, 150)
    line("h4", "Stalls", 1420, 96, 700, 96)
    line("ask1", "Interested or know someone?", 1560, 46, 700, 50, stroke=False)
    line("ask2", "Let us know", 1616, 46, 400, 50, stroke=False)
    vw = 260; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = 1690
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        inner, els, bottom = story(); print("last element ends at", bottom, "of", H)
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "story.png"), W, H, elements=els, bleed_tags=("plate", "lights"), crop_tags=("plate", "circle"), page_bg="#000",
                       text_pairs=[("h2", "#fff", "#000", 150, True), ("ask1", "#fff", "#000", 46, True)], collision_ignore=[("circle", "sticker")])
asyncio.run(main())
