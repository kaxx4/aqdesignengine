"""audit margin= : a series with a tighter safe area than AQ's 64px default must be able to say so.

Bug (TerraThon, 2026-09-29): build.render() hardcoded margin=M, and audit.py separately hardcoded a
36px BOTTOM safe zone that ignored `margin` entirely. The TerraThon footer sits 13px from the bottom
edge and its logo 27px from the left by design, so a correct poster could never report clean.
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, E)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(E, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); audit = load("audit")
W, H = 1080, 1350
def html_with(x, y):
    box = (f'<div class="measure" data-tag="foot" style="position:absolute;left:{x}px;top:{y}px;width:200px;height:60px;'
           f'background:#0E7C86"></div>')
    return B.page(W, H, "#F4EFE0", box, grain=False)
fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
async def main():
    # element 20px from the left edge and 20px from the bottom edge
    h = html_with(20, H - 80)
    d = await audit.audit(h, "t_default", canvas=(W, H))
    check("default margin (64/36) flags an element 20px from the edges", any("foot" in i for i in d))
    d = await audit.audit(h, "t_tight", canvas=(W, H), margin=12)
    check("margin=12 accepts the same element on BOTH the side and the bottom", not any("foot" in i for i in d))
    d = await audit.audit(html_with(4, H - 80), "t_too_tight", canvas=(W, H), margin=12)
    check("margin=12 still flags an element 4px from the left edge", any("foot" in i for i in d))
    d = await audit.audit(html_with(100, H - 6), "t_bottom", canvas=(W, H), margin=12)
    check("margin=12 still flags an element whose bottom is 6px from the canvas edge", any("foot" in i for i in d))
asyncio.run(main())
if fails:
    print("FAILED:", fails); sys.exit(1)
print("ALL 4 ASSERTIONS PASSED")
