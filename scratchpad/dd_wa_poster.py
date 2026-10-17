"""WhatsApp poster in the approved feed layout (poster_ref with link="Link below"). Writes out/discodiwali/launch/whatsapp_poster_v2.png.  Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_poster.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details to follow", link="Link below")
asyncio.run(dd.render_poster("poster_ref", BRIEF, "feed", os.path.join(ROOT, "out", "discodiwali", "launch", "whatsapp_poster_v2.png")))
print("whatsapp poster done")
