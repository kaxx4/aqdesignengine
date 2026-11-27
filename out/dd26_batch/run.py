import asyncio, sys, importlib.util
sys.path.insert(0, "out/dd26_batch")
s = importlib.util.spec_from_file_location("bc", "out/dd26_batch/build_carousel.py")
bc = importlib.util.module_from_spec(s); s.loader.exec_module(bc)
from jobs import JOBS
slug, ver = sys.argv[1], sys.argv[2]
cover_only = len(sys.argv) > 3 and sys.argv[3] == 'cover'
if cover_only:
    async def _noop(*a, **k): return None
    bc.render_slide = _noop; bc.render_type_slide = _noop
asyncio.run(bc.build(JOBS[slug], ver))
