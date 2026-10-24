"""DISCO DIWALI PHASE 2 ticket poster, feed 1080x1350 and story 1080x1920 (user, 2026-10-24): "generate for phase 2 650".

Facts printed, all supplied: PHASE TWO, RS. 650 PER SPOT, ALL FOR CHARITY (the badge), the edition. The line under the headline is NEXT UP, true by definition and not a claim
(phase 2 follows phase 1). NOT printed because not supplied: a DATE, a sale TIME, a slot count (never invent scarcity), a ticket link (no LINK IN BIO pill). Same family as
scratchpad/dd_phase1.py and dd_early_birds.py: photo ground (event photo 07_05), hero = the price, a copper ticket plus bolt and note, the lockup as a footer mark.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_phase2.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_copper as cp
import dd_photo_bg as pb
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "phase2")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


def build(H):
    dy = (H - 1350) // 2
    parts, els = [pb.photo_ground(dd, W, H, "07_05", "50% 40%", dim=.70, bright=.9)], []

    def text(tag, txt, y, size, weight=700, x=0, w=W, align="center", extra="", rot=0):
        rt = f";transform:rotate({rot}deg)" if rot else ""
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;width:{w}px;top:{y + dy}px;text-align:{align};font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                     f'line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20{rt}">{txt}</div>'); els.append((tag, x, y + dy, w, round(size * .88)))

    def sticker(tag, svg, x, y, w, h, z=12):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + dy}px;z-index:{z}">{svg}</div>'); els.append((tag, x, y + dy, w, h))

    by = 215 if H > 1350 else 40                              # absolute: a story keeps the top 200px clear and the badge above the headline
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:{by}px;width:150px;z-index:20">')
    els.append(("badge", 40, by, 150, round(150 * 1005 / 1061)))
    text("h1", "Phase", 200, 150, x=60, w=470, align="left", rot=-4)
    text("h2", "two", 350, 150, x=60, w=470, align="left", rot=-4)
    text("when", "Next up", 575, 96, x=0, w=W)
    text("price", "RS. 650", 690, 250, x=0, w=W)
    text("per", "per spot", 925, 74, 400, x=250, w=580, extra="letter-spacing:6px;")
    sticker("ticket", cp.ticket(360, -10, "e2"), 680, 130, 360, 360, 13)
    sticker("bolt", cp.bolt(190, 12, "e3"), 40, 960, 190, 190, 13)
    sticker("note", cp.note(150, -10, "e4"), 905, 975, 150, 150, 13)
    text("sub", "Masquerade Sangeet Edition", 1050, 38, 400, x=250, w=580)
    vw = 270; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = 1350 - 62 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy + dy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy + dy, vw, vh))
    return "".join(parts), els, vy


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, vy = build(H)
            print(f"[{name}] lockup top y={vy}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000")
    print("phase 2 done ->", OUT)
asyncio.run(main())
