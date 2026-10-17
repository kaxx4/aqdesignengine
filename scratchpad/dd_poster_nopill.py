"""Static Disco Diwali feed poster WITHOUT the link pill (user, 2026-10-17). The approved poster_ref design with link=False: no pill, and the status and
note lines drop into the freed space. No date, time or location (user, 2026-10-14).  Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_poster_nopill.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details soon", link=False)
asyncio.run(dd.render_poster("poster_ref", BRIEF, "feed", os.path.join(ROOT, "out", "discodiwali", "launch", "poster_nopill.png")))
print("poster no-pill done")
