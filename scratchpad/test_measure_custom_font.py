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
    tight = [dict(text="E", font="StretchPro", size=100, weight=400, letter_spacing="-0.045em"),
             dict(text="EE", font="StretchPro", size=100, weight=400, letter_spacing="-0.045em")]
    tight_f = [dict(i, features="'liga' 1,'dlig' 1") for i in tight]
    async with B.session():
        a = await B.measure_text(tight, extra_css=face); b = await B.measure_text(tight_f, extra_css=face)
    ra = a[1]["text_w"] / a[0]["text_w"]; rb = b[1]["text_w"] / b[0]["text_w"]
    check(f"non-zero letter-spacing DISABLES the ligature (EE measures {ra:.2f}x, not ~2.95x)", ra < 2.3)
    check(f"features=liga/dlig restores it under tight tracking ({rb:.2f}x)", 2.6 < rb < 3.2)
asyncio.run(main())
if fails:
    print("FAILED:", fails); sys.exit(1)
print("ALL 5 ASSERTIONS PASSED")
