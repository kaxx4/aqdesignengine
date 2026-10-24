"""DISCO DIWALI "PHASE 1 SOLD OUT": one story (1080x1920) and one WhatsApp poster (1080x1350), 2026-10-24. Built on story_ref / poster_ref (the approved photo-ground family)
with the new `banner` option: PHASE 1 as the hero line, the speckled SOLD OUT banner (sold_out_banner.png) crossing under it, no link pill (nothing to click). Only supplied fact: phase 1 is sold out.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_phase1_sold_out.py -> out/discodiwali/phase1_sold_out/{story,whatsapp}.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
OUT = os.path.join(ROOT, "out", "discodiwali", "phase1_sold_out")
BASE = dict(edition="Masquerade Sangeet Edition", status="Phase 1", banner=True)
async def main():
    async with dd.B.session():
        await dd.render_poster("story_ref", dict(BASE, photo=os.path.join(HALL, "05_boys-crowd-green-light.jpg"), dim=.2), "story", os.path.join(OUT, "story.png"))
        await dd.render_poster("poster_ref", dict(BASE, photo=os.path.join(HALL, "03_girls-dancing-yellow-top.jpg"), dim=.15, link=False), "feed", os.path.join(OUT, "whatsapp.png"))
    print("done ->", OUT)
asyncio.run(main())
