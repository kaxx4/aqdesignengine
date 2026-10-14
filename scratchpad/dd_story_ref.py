"""Remake of the user's reference story (2026-10-13). Writes out/discodiwali/launch/story_remake.png.  Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_story_ref.py [photo]"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
PHOTO = sys.argv[1] if len(sys.argv) > 1 else "05"
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details to follow", photo=PHOTO)
asyncio.run(dd.render_poster("story_ref", BRIEF, "story", os.path.join(ROOT, "out", "discodiwali", "launch", "story_remake.png")))
print("remake done")
