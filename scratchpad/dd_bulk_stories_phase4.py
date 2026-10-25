"""DISCO DIWALI bulk stories (kind story_ref) WITH date, time and location (user, 2026-10-23). Ten stories, one photo each.
Facts are the supplied ones only: Tue 10 Nov 2026, 4:30 PM onwards, 60 Chowringhee Banquets (rooftop), 60 Chowringhee Road, Kolkata 700020.
Outputs out/discodiwali/bulk_phase4/story_NN.png + sheet.png.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories_logistics.py
"""
import glob, asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Phase 1 is today, 6 PM", note="@ Rs. 550")
EV = os.path.join(ROOT, "engine", "assets", "img", "events")
U = lambda n: os.path.join(EV, "unsorted-2026-10-07", n)
S = lambda n: os.path.join(EV, "summer-aq-turns-five", n)
HALL = sorted(glob.glob(os.path.join(EV, "disco-diwali-hall-2026-10-14", "*.jpg")))
PHOTOS = HALL + [U("12_dark-crowd-star-balloons.jpg")]       # the library is nearly spent: the hall set was last used two batches ago
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_phase4")
    async with dd.B.session():
        for i, ph in enumerate(PHOTOS, 1):
            await dd.render_poster("story_ref", dict(BRIEF, bignote=True, photo=ph, dim=(.15 if i == 10 else .38)), "story", os.path.join(out, f"story_{i:02d}.png"))
    from PIL import Image
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(PHOTOS) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims): sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("done ->", out)
asyncio.run(main())
