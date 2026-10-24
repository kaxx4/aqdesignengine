"""DISCO DIWALI WhatsApp posters (poster_ref, link=False) with phase-opening line, date, time, venue (user, 2026-10-24). Three posters.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_phase.py   -> out/discodiwali/wa_phase/poster_NN.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Phase opens tomorrow, 6 PM", note="@ Rs. 550", link=False,
             date="Tue, 10 November 2026", time="4:30 PM onwards", venue="Rooftop, 60 Chowringhee Banquets")
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "wa_phase")
    async with dd.B.session():
        for i, ph in enumerate(["05", "09", "06"], 1):
            await dd.render_poster("poster_ref", dict(BRIEF, photo=ph), "feed", os.path.join(out, f"poster_{i:02d}.png"))
    print("done ->", out)
asyncio.run(main())
