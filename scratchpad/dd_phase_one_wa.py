"""DISCO DIWALI "PHASE ONE SOLD OUT" WhatsApp poster, feed 1080x1350 (user, 2026-10-25). v2: it must follow the STORY's idea (v1 had its own layout and a
ball lockup at the top, which the user rejected): kind poster_ref with `stamp` = the story_ref layout (badge top left, copper mask top right, ball-free title and edition lines,
the PHASE ONE / SOLD OUT band across the title, date / time / venue under it) on photo 09, no pill.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_phase_one_wa.py -> out/discodiwali/phase_one_sold_out/wa.png"""
import asyncio, glob, importlib.util, os, sys, tempfile
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
LIB = os.path.join(ROOT, "engine/assets/img/events/disco-diwali-2026-10-21")
def crop45(nn, tmp):
    im = Image.open(glob.glob(os.path.join(LIB, f"{nn}_*.jpg"))[0]).convert("RGB"); w, h = im.size
    cw, ch = (round(h * 4 / 5), h) if w / h > .8 else (w, round(w * 5 / 4))
    x0, y0 = (w - cw) // 2, (h - ch) // 2; out = os.path.join(tmp, f"{nn}.jpg"); im.crop((x0, y0, x0 + cw, y0 + ch)).save(out, quality=92); return out
async def main():
    out = os.path.join(ROOT, "out/discodiwali/phase_one_sold_out"); os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        async with dd.B.session():
            await dd.render_poster("poster_ref", dict(edition="Masquerade Sangeet Edition", status="Phase one sold out", date="Tue, 10 Nov 2026", time="4:30 PM onwards",
                venue="60, Chowringhee Banquets, Rooftop", stamp="phase_one_sold_out_banner.png", photo=crop45("09", tmp), link=False), "feed", os.path.join(out, "wa.png"))
    print("wa ->", out)
asyncio.run(main())
