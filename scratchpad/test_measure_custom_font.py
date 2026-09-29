"""measure_text(extra_css=): a face outside core.FONTS must be measurable.

Bug (TerraThon, 2026-09-29): StretchPro turns a doubled letter into ONE stretched glyph (EE -> 3.9 cap-heights vs 1.32 for a single E).
build.measure_text() only knew core.FONTS, so it measured StretchPro strings in the FALLBACK font, where EE is simply twice E.
"""
import asyncio, base64, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, E)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(E, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build")
face = ("@font-face{font-family:'StretchPro';src:url(data:font/otf;base64,"
        + base64.b64encode(open("engine/assets/fonts/StretchPro.otf", "rb").read()).decode() + ") format('opentype')}")
fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
async def main():
    items = [dict(text="E", font="StretchPro", size=100, weight=400), dict(text="EE", font="StretchPro", size=100, weight=400)]
    async with B.session():
        without = await B.measure_text(items)
        with_css = await B.measure_text(items, extra_css=face)
    r0 = without[1]["text_w"] / without[0]["text_w"]; r1 = with_css[1]["text_w"] / with_css[0]["text_w"]
    check(f"without extra_css the fallback measures EE as ~2x E (got {r0:.2f})", 1.8 < r0 < 2.2)
    check(f"with extra_css the ligature makes EE ~2.95x E (got {r1:.2f})", 2.7 < r1 < 3.2)
    check("the two measurements genuinely differ", abs(r1 - r0) > 0.5)
asyncio.run(main())
if fails:
    print("FAILED:", fails); sys.exit(1)
print("ALL 3 ASSERTIONS PASSED")
