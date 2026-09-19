"""Self-tests for the session-10 MEASURED-LAYOUT gates:
    layout.contains_check      — content that does not fit the shape it belongs to
    layout.rotated_bbox        — the footprint a rotated element really occupies
    build.measure_text         — ask the font instead of guessing
    reconcile.measure_dom      — clipped / oversize / off-canvas, from the real DOM
    reconcile.reconcile_boxes  — declared bboxes vs. what the browser drew

Every assertion reconstructs a failure from the session-10 batch, all three of
which passed the entire pre-existing static gate stack and were caught by eye.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_measured_layout.py
"""
import os, sys, asyncio, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = _load("core"); lay = _load("layout"); B = _load("build"); rec = _load("reconcile")
N = 0
def ok(m):
    global N; N += 1; print(f"  ok {N}: {m}")

# ── contains_check — "PLANTAT" hanging off its pill ─────────────────────────
# A bar was sized from DATA (26 projects -> 120px) while its label was sized
# from TEXT (212px), and the two were sibling divs so nothing related them.
hits = lay.contains_check([("bar-label", (70, 100, 212, 40), (64, 96, 120, 60))])
assert hits and hits[0][1] == "right" and hits[0][2] == 98
ok("contains_check catches a 212px label overhanging a 120px pill by 98px")

assert lay.contains_check([("bar-label", (70, 100, 90, 40), (64, 96, 180, 60))]) == []
ok("a label that genuinely fits is not flagged")

# the second half of the same bug: a headline taller than its colour band
assert lay.contains_check([("headline", (64, 168, 900, 281), (0, 0, 1200, 392))]) == \
       [("headline", "bottom", 57)]
ok("catches a 281px headline at y=168 crossing a 392px band edge")

assert len(lay.contains_check([("x", (0, 0, 100, 100), (10, 10, 50, 50))])) == 4
ok("reports every side that overhangs, not just the first")
assert lay.contains_check([("x", (64, 10, 100, 20), (60, 6, 110, 30))], pad=12)
ok("pad enforces required slack inside the outer box")
assert lay.contains_check([]) == []
ok("contains_check tolerates an empty pair list")

# it must be a HARD fail — clipped copy is never an intended design
r = lay.preflight(1080, 1350, [(0, 0, 100, 100)],
                  contains=[("lbl", (70, 100, 212, 40), (64, 96, 120, 60))])
assert r["not_contained"] and r["clean"] is False
ok("wired into preflight as a HARD FAIL (unlike the advisory density checks)")

# ── rotated_bbox — the 168px sticker that draws 192px ───────────────────────
x, y, w, h = lay.rotated_bbox(100, 100, 168, 168, -9)
assert abs(w - 192.2) < 0.5 and abs(h - 192.2) < 0.5
ok("rotated_bbox: a 168px sticker at -9deg really occupies 192px (browser agrees)")
assert abs(x - 87.9) < 0.5
ok("...and it re-centres the origin, so the box drops straight into an element list")

for d in (0, 90, 180, -180):
    _, _, w2, h2 = lay.rotated_bbox(0, 0, 168, 168, d)
    assert abs(w2 - 168) < 0.01 and abs(h2 - 168) < 0.01, d
ok("square multiples of 90deg are unchanged — no phantom growth")

_, _, w3, _ = lay.rotated_bbox(0, 0, 168, 168, 45)
assert abs(w3 / 168 - 1.414) < 0.01
ok("the error peaks at 45deg (41% larger) — worth a rule, not a habit")

_, _, w4, h4 = lay.rotated_bbox(0, 0, 300, 100, 90)
assert abs(w4 - 100) < 0.01 and abs(h4 - 300) < 0.01
ok("a non-square element swaps axes correctly at 90deg")

# ── reconcile_boxes — CLAUDE.md §10's "discipline" row, mechanised ──────────
measured = [("hero", 52, 214, 743, 363), ("stk", 800, 240, 192, 192)]
declared = [("hero", 52, 214, 731, 336), ("stk", 800, 240, 168, 168)]
res = rec.reconcile_boxes(measured, declared)
labels = {r0[0] for r0 in res["under_reported"]}
assert labels == {"hero", "stk"}
ok("reconcile_boxes catches BOTH under-reported boxes (glyph overflow + rotation)")

assert rec.reconcile_boxes(measured, [("hero", 52, 214, 743, 363),
                                      ("stk", 800, 240, 192, 192)])["under_reported"] == []
ok("correct declarations produce no noise")

res2 = rec.reconcile_boxes([("ghost", 670, 168, 346, 206)], [("hero", 52, 214, 731, 336)])
assert res2["untracked"] and res2["untracked"][0][0] == "ghost"
ok("an element with NO declared bbox is reported as untracked — the silent half")

tiny = rec.reconcile_boxes([("chip", 10, 10, 40, 20)], [])
assert tiny["untracked"] == []
ok("sub-60px elements are below the floor — chips do not spam the report")

ground = rec.reconcile_boxes([("bg", 0, 0, 1080, 1350)], [], canvas=(1080, 1350))
assert ground["untracked"] == []
ok("the page ground itself is excluded from untracked")

assert rec.reconcile_boxes([], []) == {"under_reported": [], "untracked": []}
ok("reconcile_boxes tolerates empty input")

assert rec.format_reconcile({"under_reported": [("hero", (731, 336), (743, 363))],
                             "untracked": []})[0].startswith("BBOX UNDER-REPORTS hero")
ok("format_reconcile prints a line that names the element and both sizes")


async def browser_tests():
    global N
    async with B.session():
        # ── measure_text: the three numbers, and which one to use ───────────
        m = await B.measure_text([
            {"text": "126", "font": "d", "size": 430, "weight": 900,
             "line_height": 0.78, "letter_spacing": "-.045em"},
            {"text": "PLANTATION DRIVE", "font": "m", "size": 19, "weight": 700,
             "letter_spacing": ".05em"},
        ])
        hero, label = m
        assert hero["ink_h"] > hero["h"], (hero["ink_h"], hero["h"])
        ok("measure_text: content box exceeds the layout box at line-height < 1")
        assert hero["glyph_w"] > hero["w"], (hero["glyph_w"], hero["w"])
        ok("...and the PAINTED width exceeds the layout width — this is what put "
           "a sticker on the numeral")
        assert hero["h"] < hero["glyph_h"] < hero["ink_h"]
        ok("glyph_h sits between the two CSS boxes: the em box reserves descender "
           "space digits never use")
        assert hero["lines"] == 1 and label["lines"] == 1
        ok("line counts are reported")
        assert 190 < label["w"] < 240, label["w"]
        ok("a mono label measures ~212px at 19px — the number the pill needed")

        multi = await B.measure_text([{"text": "A<br>B<br>C", "font": "d", "size": 100,
                                       "weight": 900, "line_height": 0.86}])
        assert multi[0]["lines"] == 3
        ok("multi-line text reports its real line count")
        assert multi[0]["glyph_w"] is None
        ok("glyph metrics are None for multi-line (honest: the canvas API is per-line)")

        # ── measure_dom: clipped vs oversize vs off-canvas ───────────────────
        W, H = 1080, 1350
        html = B.page(W, H, "var(--bg)", (
            '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
            # genuinely clipped: content larger than a box that hides overflow
            '<div data-tag="clipme" style="position:absolute;left:60px;top:60px;'
            'width:120px;height:40px;overflow:hidden;font-family:var(--m);font-size:19px;'
            'white-space:nowrap">PLANTATION DRIVE</div>'
            # explicit height the content does not fit -> the author asserted wrong
            '<div data-tag="spillme" style="position:absolute;left:60px;top:200px;'
            'width:400px;height:40px;font-family:var(--e);font-size:30px;line-height:1.5">'
            'one two three four five six seven eight nine ten</div>'
            # a normal tight-leading headline: must NOT be flagged
            '<div data-tag="normal" style="position:absolute;left:60px;top:500px;'
            'width:800px;font-family:var(--d);font-size:92px;line-height:.92">ONE<br>TWO</div>'
            # off canvas
            '<div data-tag="gone" style="position:absolute;left:1000px;top:1300px;'
            'width:300px;height:200px;background:#FF4D8C"></div>'), grain=False)
        pg = await B._SESSION.page(W, H)
        await pg.set_content(html, wait_until="load")
        await B._settle(pg)
        f = await rec.measure_dom(pg, W, H)

        assert any(t == "clipme" for t, *_ in f["clipped"]), f["clipped"]
        ok("measure_dom flags text clipped by an overflow:hidden box (characters lost)")
        assert any(t == "spillme" for t, *_ in f["spilling"]), f["spilling"]
        ok("...and content that does not fit an EXPLICIT height the author declared")
        assert not any(t == "normal" for t, *_ in f["spilling"]), f["spilling"]
        ok("...but NOT a normal tight-leading headline — the gate stays quiet on "
           "ordinary typography, so its warnings keep meaning something")
        assert any(t == "gone" for t, *_ in f["off_canvas"]), f["off_canvas"]
        ok("measure_dom flags an element whose painted box leaves the canvas")
        assert f["boxes"], "boxes must be returned for reconcile_boxes"
        ok("measure_dom returns real boxes for reconciliation against the tuples")

        clean_html = B.page(W, H, "var(--bg)",
                            '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
                            '<div data-tag="ok" style="position:absolute;left:64px;top:64px;'
                            'width:400px;font-family:var(--e);font-size:24px">fine</div>', grain=False)
        await pg.set_content(clean_html, wait_until="load")
        await B._settle(pg)
        g = await rec.measure_dom(pg, W, H)
        assert not g["clipped"] and not g["spilling"] and not g["off_canvas"]
        ok("a clean page reports nothing at all — no baseline noise")

asyncio.run(browser_tests())
print(f"\nALL {N} ASSERTIONS PASSED")
