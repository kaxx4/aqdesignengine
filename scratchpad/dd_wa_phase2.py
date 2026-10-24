"""DISCO DIWALI WhatsApp posters (poster_ref, link=False) with phase-opening line, date, time, venue (user, 2026-10-24). Three posters.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_phase2.py   -> out/discodiwali/wa_phase2/poster_NN.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Phase opens tomorrow, 6 PM", note="@ Rs. 550", link=False,
             date="Tue, 10 November 2026", time="4:30 PM onwards", venue="Rooftop, 60 Chowringhee Banquets")
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "wa_phase2")
    async with dd.B.session():
        for i, ph in enumerate([os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14", f) for f in ("08_boy-on-shoulders-stage-lights-portrait.jpg", "04_pink-ceiling-chandelier-phone.jpg", "06_blue-room-crowd-faces.jpg")], 1):
            await dd.render_poster("poster_ref", dict(BRIEF, photo=ph, dim=(.3 if i == 2 else 0)), "feed", os.path.join(out, f"poster_{i:02d}.png"))
    print("done ->", out)
asyncio.run(main())
