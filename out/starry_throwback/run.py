import asyncio, sys, importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
s = importlib.util.spec_from_file_location("bc", os.path.join(HERE, "build_carousel.py"))
bc = importlib.util.module_from_spec(s); s.loader.exec_module(bc)
from jobs import JOB
ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
asyncio.run(bc.build(JOB, ver))
