"""DISCO DIWALI "PHASE ONE SOLD OUT" story (2026-10-25, user: "create a sold out story for Phase One"). One story_ref story with the sold-out band on top:
the approved stamp layout (band centred on y 960, date / time / venue below it, LINK IN BIO pill) with the band text changed to PHASE ONE / SOLD OUT. The band is built by
scratchpad/make_early_bird_banner.py from the user's SOLD OUT band: `... <jpg> "PHASE ONE" "SOLD OUT" phase_one_sold_out_banner.png`. Its small line NEXT PHASE OPENS SOON is the
user's own wording from the early-bird band; no phase-two date or price is printed. Photo 09 of engine/assets/img/events/disco-diwali-2026-10-21 (chevron backdrop, balloon arch).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_phase_one_story.py   ->  out/discodiwali/phase_one_sold_out/story.png"""
import asyncio, glob, importlib.util, os, sys, tempfile
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
LIB = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-2026-10-21")
PHOTO = os.environ.get("PHOTO", "09")
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Phase one sold out", date="Tue, 10 Nov 2026", time="4:30 PM onwards",
             venue="60, Chowringhee Banquets, Rooftop", stamp="phase_one_sold_out_banner.png")
def crop916(nn, tmp):
    im = Image.open(glob.glob(os.path.join(LIB, f"{nn}_*.jpg"))[0]).convert("RGB"); w, h = im.size
    cw, ch = (w, round(w * 16 / 9)) if w / h < 9 / 16 else (round(h * 9 / 16), h)
    x0 = (w - cw) // 2; y0 = (h - ch) // 2
    out = os.path.join(tmp, f"{nn}.jpg"); im.crop((x0, y0, x0 + cw, y0 + ch)).save(out, quality=92); return out
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "phase_one_sold_out"); os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        async with dd.B.session():
            await dd.render_poster("story_ref", dict(BRIEF, photo=crop916(PHOTO, tmp)), "story", os.path.join(out, "story.png"))
    print("phase one story ->", out)
asyncio.run(main())
