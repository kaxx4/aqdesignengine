"""DISCO DIWALI DRESS CODE poster, feed (1080x1350) + story (1080x1920), 2026-10-25. Copy: DRESS CODE / INDO-WESTERN (user-supplied; nothing else printed).
Photo: user-supplied group shot at the photobooth, in a tilted cream PRINT FRAME (user: "something else instead of a circular frame"). Diya ground (the event photo library is spent),
LIVE badge, copper mask sticker (user: "for sticker use the mask") on the frame's top-right corner, lockup footer. No link pill: nothing to link.
Photo consent: four identifiable people, unconfirmed.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_dresscode.py -> out/discodiwali/dresscode/{feed,story}.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_charity_ground as G
B = dd.B; W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "dresscode")
PHOTO = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-dresscode", "01_four-friends-booth.jpg")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
def poster(H):
    story = H > 1350
    parts, els = [G.ground_diya(W, H)], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    pw, ph = (920, 700) if story else (840, 560)
    pad = 26; fw, fh = pw + 2 * pad, ph + 2 * pad + 40
    fx, fy = (W - fw) // 2, (380 if story else 190)
    parts.append(f'<div data-tag="frame" style="position:absolute;left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px;background:#F4EFE0;transform:rotate(-3deg);z-index:10;'
                 f'box-shadow:0 18px 44px rgba(0,0,0,.65);box-sizing:border-box;padding:{pad}px {pad}px {pad + 40}px {pad}px">'
                 f'<img src="{dd.photo_uri(PHOTO)}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block;filter:contrast(1.04) saturate(1.05)"></div>')
    els.append(("frame", fx - 20, fy - 20, fw + 40, fh + 40))
    k = .30 if story else .27
    mvw, mvh = round(1403 * k), round(878 * k)
    mx, my = 1060 - mvw, fy - (mvh // 2) - (10 if story else 20)
    parts.append(f'<img data-tag="sticker" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(mx - 157 * k)}px;top:{round(my - 211 * k)}px;width:{round(1680 * k)}px;'
                 f'z-index:12;filter:drop-shadow(0 8px 22px rgba(0,0,0,.6))">'); els.append(("sticker", mx, my, mvw, mvh))
    def line(tag, txt, top, size, weight, h):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    hy = fy + fh + (70 if story else 60)
    line("h1", "Dress code", hy, 84, 700, 84)
    s2 = 108; line("h2", "Indo-Western", hy + 96, s2, 700, s2)
    y = hy + 96 + s2 + (44 if story else 28)
    vw = 300 if story else 250; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, y, vw, vh))
    return "".join(parts), els, y + vh
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H); print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, bleed_tags=("plate", "lights"), crop_tags=("plate",), page_bg="#000",
                           collision_ignore=[("frame", "sticker"), ("frame", "badge")], text_pairs=[("h2", "#fff", "#000", 108, True)])
asyncio.run(main())
