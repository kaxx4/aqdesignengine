"""
Self-test for the giant_type/cream density-escalation fix (see brain/DECISIONS.md, 2026-09-05).

Real bug: generating a teachers_day poster (giant_type, field="cream", short word + 3 tags +
one body paragraph) got stuck NEEDS-LOOK at fill=0.28 with TL/TR quads at 0.17/0.16 and
`flat_dominant`+`sparse` both firing. Root cause, found by tracing the pipeline:
  1. ARCHETYPE_PROFILES["giant_type"]["max_density"] was 1, so the self-correction loop had only
     ONE escalation step to fix a flat/sparse field — every other archetype had 2-4.
  2. `leftmass` (the one shape living in the TL quadrant) never scaled with `density` at all,
     unlike `rightmass`/`lowmass`, which both grow via `+density*N` — so escalating density did
     nothing for TL specifically.
Fix: `leftmass` now scales with density like its siblings; `max_density` raised 1->2; a new
`midmass` tier (density>=2 only) fills the one collision-safe window beside the title (below the
word's own bounding box, above the tags row) that was otherwise unreachable because the title
div's box spans the full grid width for wrapping purposes even though a short word's glyphs don't.

Each assertion below reconstructs a piece of that failure directly, so a future refactor that
regresses it will fail loudly here rather than needing a human to notice a NEEDS-LOOK on some
unrelated poster months later.
"""
import asyncio, os, sys, importlib.util
ENGINE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng = load("engine"); B = load("build"); pv = load("preview")

CONTENT = dict(
    field="cream", meta="teachers' day · sept 5", word="teachers",
    tags=["mentors", "patience", "gratitude"],
    body="every kid we've reached learned from someone who chose to teach first. sundarban's classrooms run on you.",
    big="thank you for<br>showing up.", band="you taught us this too.",
    footer="@ngo.aquaterra",
)
ACCENT = eng.RULES["accents"][1]

passed = 0
def check(name, cond):
    global passed
    assert cond, f"FAILED: {name}"
    passed += 1
    print(f"  ok  {name}")

# 1. the profile now grants giant_type real escalation headroom (was 1)
check("giant_type max_density raised to >=2",
      eng.ARCHETYPE_PROFILES["giant_type"]["max_density"] >= 2)

# 2. leftmass HTML literally grows with density (the actual root-cause line)
html0 = eng.archetype_giant_type(CONTENT, ACCENT, density=0)
html1 = eng.archetype_giant_type(CONTENT, ACCENT, density=1)
html2 = eng.archetype_giant_type(CONTENT, ACCENT, density=2)
import re
def leftmass_width(html):
    # leftmass is the first absolutely-positioned div at top:120px;left:60px in the markup
    m = re.search(r'top:120px;left:64px;width:(\d+)px', html)
    assert m, "leftmass marker not found in archetype output"
    return int(m.group(1))
w0, w1, w2 = leftmass_width(html0), leftmass_width(html1), leftmass_width(html2)
check(f"leftmass width grows with density ({w0} < {w1} < {w2})", w0 < w1 < w2)

# 3. midmass exists only at density>=2, and never at 0/1 (it targets a specific escalation tier)
check("midmass absent at density=0", "rotate(4deg)" not in html0)
check("midmass absent at density=1", "rotate(4deg)" not in html1)
check("midmass present at density=2", "rotate(4deg)" in html2)

# 4. end-to-end: the real historical content, rendered, actually recovers from the stuck state.
#    (Requires Playwright/Chromium — matches how every other render-based self-test in this repo
#    already works, e.g. the vision/collision suites call into build.render.)
async def render_fill(density):
    inner = eng.ARCHETYPES["giant_type"](CONTENT, ACCENT, density)
    html = B.page(eng.W, eng.H, "var(--bg)", inner, grain=True)
    out = f"/tmp/test_giant_type_density_{density}.png"
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": eng.W, "height": eng.H}, device_scale_factor=2)
        await pg.set_content(html, wait_until="load"); await pg.wait_for_timeout(600)
        await pg.locator(".p").screenshot(path=out); await b.close()
    return pv.critique(out)

async def main():
    global passed
    c1 = await render_fill(1)
    c2 = await render_fill(2)
    # this is the exact historical failure: density=1 alone leaves it sparse (fill<0.32) — the
    # bug wasn't that escalation didn't happen, it's that the one escalation step wasn't enough
    # and there was nowhere further to go.
    check(f"density=1 fill {c1['fill']} still short of the generic sparse bar (documents the stuck state)",
          c1["fill"] < 0.32)
    check(f"density=2 fill {c2['fill']} clears the sparse bar (0.32) the fix was meant to reach",
          c2["fill"] >= 0.32)
    check(f"density=2 TL quad {c2['quads']['TL']} clears quad_min (0.12)", c2["quads"]["TL"] >= 0.12)
    check(f"density=2 TR quad {c2['quads']['TR']} clears quad_min (0.12)", c2["quads"]["TR"] >= 0.12)
    for d in (1, 2):
        try: os.remove(f"/tmp/test_giant_type_density_{d}.png")
        except OSError: pass
    print(f"\n{passed} assertions passed.")

asyncio.run(main())
