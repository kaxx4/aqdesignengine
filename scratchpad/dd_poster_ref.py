"""Remake of the user's reference FEED poster (2026-10-13). Writes out/discodiwali/launch/poster_remake.png.  Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_poster_ref.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details soon")
asyncio.run(dd.render_poster("poster_ref", BRIEF, "feed", os.path.join(ROOT, "out", "discodiwali", "launch", "poster_remake.png")))
print("poster remake done")
