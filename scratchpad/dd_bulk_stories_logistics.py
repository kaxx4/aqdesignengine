"""DISCO DIWALI bulk stories (kind story_ref) WITH date, time and location (user, 2026-10-23). Ten stories, one photo each.
Facts are the supplied ones only: Tue 10 Nov 2026, 4:30 PM onwards, 60 Chowringhee Banquets (rooftop), 60 Chowringhee Road, Kolkata 700020.
Outputs out/discodiwali/bulk_logistics/story_NN.png + sheet.png.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories_logistics.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition",
             date="Tue, 10 November 2026", time="4:30 PM onwards", venue="Rooftop, 60 Chowringhee Banquets",
             address="60 Chowringhee Road")
PHOTOS = ["05", "03", "12", "06", "09", "11", "07", "13", "08", "10"]
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_logistics")
    async with dd.B.session():
        for i, ph in enumerate(PHOTOS, 1):
            await dd.render_poster("story_ref", dict(BRIEF, photo=ph), "story", os.path.join(out, f"story_{i:02d}.png"))
    from PIL import Image
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(PHOTOS) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims): sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("done ->", out)
asyncio.run(main())
