"""DISCO DIWALI "PHASE ONE SOLD OUT" WhatsApp poster, feed 1080x1350 (user, 2026-10-25: "create the wa poster as well"). Same band, photo (09) and facts as
dd_phase_one_story.py: lockup top, band across the middle (scale 0.40, centre y 760, so the title stays clear), date / time / venue under it. No pill (WhatsApp has no link).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_phase_one_wa.py -> out/discodiwali/phase_one_sold_out/wa.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_photo_bg as _pb
B = dd.B; W, H = 1080, 1350
PHOTO = "21_09"                      # 09 of engine/assets/img/events/disco-diwali-2026-10-21 (see dd_photo_bg.find)
STROKE = "color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke fill;"
async def main():
    parts, els = [_pb.photo_ground(dd, W, H, PHOTO, "50% 50%", dim=.62)], []
    parts.append(f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">')
    parts.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:6;mix-blend-mode:screen;opacity:.45;pointer-events:none">')
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:40px;width:150px;z-index:20">'); els.append(("badge", 40, 40, 150, 142))
    vw = 560; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2 + 60; vy = 70
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">'); els.append(("title", vx, vy, vw, vh))
    kb, cy = .40, 760
    bx, by, bw, bh = round(540 - 1400 * kb), round(cy - 771 * kb), round(2800 * kb), round(1547 * kb)
    parts.append(f'<img data-tag="banner" src="{dd.uri("phase_one_sold_out_banner.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:30;filter:drop-shadow(0 10px 28px rgba(0,0,0,.55))">'); els.append(("banner", bx, by, bw, bh))
    for tag, txt, top, fs, wt in (("date", "Tue, 10 Nov 2026", 1118, 46, 700), ("time", "4:30 PM onwards", 1174, 40, 400), ("venue", "60, Chowringhee Banquets, Rooftop", 1226, 34, 700)):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{wt};font-size:{fs}px;line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">{txt}</div>')
        els.append((tag, 40, top, 1000, fs))
    out = os.path.join(ROOT, "out/discodiwali/phase_one_sold_out"); os.makedirs(out, exist_ok=True)
    async with B.session():
        await B.render(B.page(W, H, "#000", "".join(parts), grain=False), os.path.join(out, "wa.png"), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000",
                       collision_ignore=[("banner", "title"), ("banner", "date"), ("banner", "time"), ("banner", "venue")])
    print("wa ->", out)
asyncio.run(main())
