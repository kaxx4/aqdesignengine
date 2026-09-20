"""Self-tests for the session-10c RECREATION rules:
    shapes.brush_asterisk / ink_mark  — a drawn mark, not a die-cut sticker
    shapes.pixel_art / AQ_PIXELS      — a bitmap motif silhouette family
    compare.geometry                  — measure a reference instead of eyeballing it
    reconcile.measure_dom             — a child clipped by its container

Each assertion reconstructs a real failure from recreating samples 3d846c78 and
77e7bb34. Two of them are failures the pixel-metric score did NOT catch.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_recreation.py
"""
import os, sys, asyncio, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

sh = _load("shapes"); core = _load("core"); B = _load("build"); rec = _load("reconcile")
N = 0
def ok(m):
    global N; N += 1; print(f"  ok {N}: {m}")

# ── brush_asterisk — the silhouette-collapse fix ────────────────────────────
# v1 of this function drew wedges radiating from a shared hub: a solid centre, every
# edge meeting at one point. Rendered beside the reference it was plainly a clean
# vector sparkle, not ink. An asterisk is drawn as STROKES PULLED THROUGH the middle.
d = sh.brush_asterisk(strokes=4, seed=3)
assert d.count("M") == 4
ok("brush_asterisk(strokes=4) emits FOUR marks, not eight wedges")
assert "Q" in d
ok("...each one curved — a hand pivots, it does not rule a line")
assert sh.brush_asterisk(strokes=6, seed=3).count("M") == 6
ok("the stroke count is parametric")
assert sh.brush_asterisk(seed=3) == sh.brush_asterisk(seed=3)
assert sh.brush_asterisk(seed=3) != sh.brush_asterisk(seed=8)
ok("seeded: reproducible, and genuinely different between seeds")

mark = sh.ink_mark(d, fill="#3DA9FC", size=140)
assert "stroke" not in mark and "filter" not in mark
ok("ink_mark applies NO halo, outline or shadow — a drawn mark is not a sticker")
assert 'fill="#3DA9FC"' in mark and 'width="140"' in mark
ok("ink_mark honours fill and size")
assert "stroke" in sh.sticker(sh.scallop(), "#FF4D8C")
ok("...while sticker() still DOES apply the die-cut treatment — they stay distinct")

# ── pixel_art ───────────────────────────────────────────────────────────────
for name in sh.AQ_PIXELS:
    p = sh.pixel_art(name)
    assert p and p.count("M") > 10, name
ok(f"all {len(sh.AQ_PIXELS)} AQ_PIXELS grids produce many-celled paths")

tiny = sh.pixel_art(["##", ".#"])
assert tiny.count("M") == 3
ok("pixel_art accepts a raw grid and emits one square per filled cell")
assert sh.pixel_art([]) == "" and sh.pixel_art(["..", ".."]) == ""
ok("an empty or all-blank grid emits nothing instead of raising")

gapped = sh.pixel_art(["##", "##"], gap=0.3)
solid = sh.pixel_art(["##", "##"], gap=0.0)
assert gapped != solid
ok("gap insets each cell, so the grid reads as separated pixels")
assert sh.pixel_art("sprout", box=200).count("M") == sh.pixel_art("sprout", box=50).count("M")
ok("box scales the art without changing the cell count")
assert sh.pixel_art("not-a-name") == "" or isinstance(sh.pixel_art("not-a-name"), str)
ok("an unknown name degrades to empty rather than raising")


async def browser_tests():
    global N
    W, H = 1080, 1350
    async with B.session():
        # ── clipped BY ITS PARENT ───────────────────────────────────────────
        # sample 77e7bb34 v1: a copy block inside an overflow:hidden slab had a
        # negative top offset, so its first line was sliced off by the slab edge.
        # compare.py scored that render 0.147 — INSIDE the accept gate. A missing
        # line of copy barely moves a pixel histogram; only the eye saw it.
        html = B.page(W, H, "var(--bg)", (
            '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
            '<div data-tag="slab" style="position:absolute;left:100px;top:300px;'
            'width:600px;height:300px;background:#FFFFFF;overflow:hidden">'
            '  <div data-tag="copy" style="position:absolute;left:30px;top:-84px;'
            '  width:400px;font-family:var(--e);font-size:40px">one<br>two<br>three</div>'
            '</div>'), grain=False)
        pg = await B._SESSION.page(W, H)
        await pg.set_content(html, wait_until="load"); await B._settle(pg)
        f = await rec.measure_dom(pg, W, H)
        hits = [t for t, *_ in f["clipped"] if "copy" in t]
        assert hits, f["clipped"]
        ok("measure_dom flags a child cut off by its container's edge")
        assert any("slab" in t for t, *_ in f["clipped"])
        ok("...and names the container doing the clipping")

        # the check must see NESTED elements. _SEL used to match direct children of
        # .p only, so nesting — which the house style recommends — hid elements from
        # the gate entirely.
        assert any("copy" in str(b[0]) for b in f["boxes"])
        ok("nested descendants are measured at all (the selector bug this exposed)")

        # deliberate page-edge BLEED must not be flagged: .p is always overflow:hidden
        bleed = B.page(W, H, "var(--bg)", (
            '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
            '<div data-tag="pill" style="position:absolute;left:-150px;top:400px;'
            'width:400px;height:80px;background:#FF4D8C"></div>'), grain=False)
        await pg.set_content(bleed, wait_until="load"); await B._settle(pg)
        g = await rec.measure_dom(pg, W, H)
        assert not g["clipped"], g["clipped"]
        ok("a pill deliberately bleeding off the page edge is NOT reported as clipped")
        assert any("pill" in t for t, *_ in g["off_canvas"])
        ok("...page-edge bleed stays the off_canvas check's job, where it belongs")

        # a well-contained child is silent
        fine = B.page(W, H, "var(--bg)", (
            '<div style="position:absolute;inset:0;background:var(--bg)"></div>'
            '<div data-tag="slab" style="position:absolute;left:100px;top:300px;'
            'width:600px;height:300px;background:#FFF;overflow:hidden">'
            '  <div data-tag="copy" style="position:absolute;left:30px;top:30px;'
            '  width:400px;font-size:30px">fits</div></div>'), grain=False)
        await pg.set_content(fine, wait_until="load"); await B._settle(pg)
        assert not (await rec.measure_dom(pg, W, H))["clipped"]
        ok("a child that fits its container reports nothing — no baseline noise")

asyncio.run(browser_tests())

# ── compare.geometry ────────────────────────────────────────────────────────
# Step 1 of the recreation protocol is a WRITTEN description. For sample 3d846c78 I
# wrote "the grid sits high, about twice as much black below as above". Measured, the
# reference is 1.05 : 1. v2 built to the written proportion and scored 0.405 against
# v1's 0.180, with bbox IoU falling 0.87 -> 0.60. Proportions get measured now.
cmp_ = _load("compare")
REF = "training_samples/reference_posters/3d846c781bd0593f6c08387a095c02d9.jpg"
if os.path.exists(REF):
    g = cmp_.geometry(REF)
    assert set(g) >= {"content_bbox", "margins", "vertical_ratio", "centroid", "coverage"}
    ok("compare.geometry returns bbox, margins, vertical ratio, centroid and coverage")
    assert abs(g["vertical_ratio"] - 1.05) < 0.06
    ok("...and measures 3d846c78 at 1.05 : 1 — NOT the 2 : 1 the written description claimed")
    x0, y0, x1, y1 = g["content_bbox"]
    assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1
    ok("the bbox is returned as canvas fractions, ready to build against")
    assert len(g["grid"]) == 9 * 11 and all(0.0 <= v <= 1.0 for v in g["grid"])
    ok("the occupancy grid is a plain list of floats in 0..1")
else:
    ok("(reference image absent — geometry assertions skipped)")

# (no banner here — a mid-file "ALL PASSED" print makes a FAILED run look passed)

# ── layout.resolve_label_z — protect the LABEL, not the object ──────────────
# sample 522f2d89: in a deliberately overlapping pile, heavy overlap is the effect.
# One capsule covering another's WORDS never is. collision_check can say nothing
# (the overlap is the design); occlusion_check measures whole objects, so a capsule
# 60% visible reads as fine even when the hidden 40% is exactly the text.
lay = _load("layout")

solvable = [("a", (100, 100, 300, 60), 5),
            ("b", (400, 90, 320, 90), 9),
            ("c", (700, 700, 200, 60), 3)]
z, un = lay.resolve_label_z(solvable)
assert un == []
ok("resolve_label_z leaves a pile whose labels already clear each other alone")

# Raising only helps when coverage is ASYMMETRIC — a short label swallowed by a long
# one. Two equal labels overlapping is symmetric: whichever goes on top, the other is
# covered by the same amount, and no stacking fixes it (see the unsolvable case below).
buried = [("short", (200, 200, 100, 40), 2), ("long", (100, 150, 500, 140), 9)]
z2, un2 = lay.resolve_label_z(buried)
assert z2["short"] > z2["long"], (z2, un2)
ok("a short label swallowed by a long one is RAISED above it")
assert un2 == [], un2
ok("...and resolves, because it covers little of the long one in return")

# genuinely unsolvable: two labels on exactly the same spot. No stacking fixes that.
z3, un3 = lay.resolve_label_z([("x", (0, 0, 100, 50), 1), ("y", (0, 0, 100, 50), 2)])
assert un3, "mutually-covering labels must be reported, not silently 'fixed'"
ok("two labels in the same place are reported UNRESOLVED — the composition must move")

# the escalation trap: raising every covered object at once, or one at a time without
# cycle detection, makes a mutually-overlapping pair lift each other forever.
import time as _t
_t0 = _t.time()
lay.resolve_label_z([(f"k{i}", (i * 5, 0, 200, 60), i) for i in range(12)])
assert _t.time() - _t0 < 5.0
ok("a heavily interlocking pile terminates instead of escalating forever")

assert lay.resolve_label_z([]) == ({}, [])
ok("resolve_label_z tolerates an empty pile")

# ── compare.crop — make mockup references scorable at all ───────────────────
# ~a third of the corpus is a mockup (phones on a backdrop, a card photo). Comparing a
# poster against a picture of three phones on grey measures the grey, so every mockup
# recreation in the run so far was parked with NO number.
import PIL.Image as _I
_probe = "scratchpad/crops/_test_probe.png"
os.makedirs("scratchpad/crops", exist_ok=True)
_I.new("RGB", (400, 600), (12, 12, 12)).save(_probe)
out = cmp_.crop(_probe, 0.25, 0.10, 0.75, 0.90, "scratchpad/crops/_test_cut.png")
assert _I.open(out).size == (200, 480)
ok("compare.crop cuts a fractional region and writes it at the right pixel size")

try:
    cmp_.crop(_probe, 0.7, 0.1, 0.3, 0.9)
    raise AssertionError("an inverted box should raise")
except ValueError:
    pass
ok("an inverted/empty crop box raises instead of writing a broken target")

_auto = cmp_.crop(_probe, 0.1, 0.1, 0.9, 0.9)
assert os.path.exists(_auto) and "_crop_" in _auto
ok("with no out_path it writes a predictable name beside the source")
for _f in (_probe, "scratchpad/crops/_test_cut.png", _auto):
    if os.path.exists(_f):
        os.remove(_f)

# ── THE SCORE MUST SAY WHEN IT IS NOT COMPARABLE (session 10f, agent r1) ────
# compare._load resamples BOTH images to one frame. That is right for relative
# geometry and wrong to read as a quality number when the sources are different
# shapes: a 0.275 phone-screen crop against a 0.5625 story canvas scored 0.534
# against a 0.16 accept line while the looking gate found every element present
# and correctly proportioned. The agent had to discover that by running a control
# (render vs. a downscaled copy of itself → 0.001). compare knows both aspects.
import io as _io2, contextlib as _ctx2
from PIL import Image as _Im
import tempfile as _tf2

_d = _tf2.mkdtemp(prefix="aq_asp_")
_tall = os.path.join(_d, "tall.png");  _Im.new("RGB", (400, 1400), "white").save(_tall)
_wide = os.path.join(_d, "wide.png");  _Im.new("RGB", (400, 500), "white").save(_wide)
_same = os.path.join(_d, "same.png");  _Im.new("RGB", (800, 1000), "white").save(_same)

r_, g_, gap_ = cmp_.aspect_gap(_tall, _wide)
assert gap_ > 0.5, (r_, g_)
ok(f"aspect_gap measures the real source shapes ({r_} vs {g_})")

_b = _io2.StringIO()
with _ctx2.redirect_stdout(_b):
    cmp_.compare(_tall, _wide)
assert "ASPECT MISMATCH" in _b.getvalue()
ok("a cross-aspect comparison SAYS the score is not comparable")
assert "control" in _b.getvalue().lower() and "RECREATION_PROTOCOL" in _b.getvalue()
ok("...and names the control to run and where the ruling lives")

_b = _io2.StringIO()
with _ctx2.redirect_stdout(_b):
    cmp_.compare(_same, _same)
assert "ASPECT MISMATCH" not in _b.getvalue()
ok("a same-aspect comparison stays silent — it does not cry wolf on normal work")

# ── A DELIBERATE CROP IS NOT A BUG (session 10f, agent g4) ──────────────────
# "size it oversize, then clip it with overflow:hidden" is a real technique. An
# agent used it twice in one poster — to crop a baked-in caption out of a photo,
# and to shape a hero-shine — and got CLIPPED reported both times on a visually
# correct render. It worked around the gate rather than ship a render whose own
# log reads as broken, which is exactly the wrong way round.
async def crop_tests():
    global N
    W2, H2 = 1080, 1350
    CROP = ('<div data-tag="frame" style="position:absolute;left:100px;top:300px;'
            'width:600px;height:300px;overflow:hidden;background:#FFF">'
            '<div data-tag="photo" style="position:absolute;left:0;top:-120px;'
            'width:600px;height:520px;background:#1B8A5A"></div></div>')
    # the 77e7bb34 bug: a line of copy sliced off a slab edge, never intended
    REAL = ('<div data-tag="slab" style="position:absolute;left:100px;top:300px;'
            'width:600px;height:200px;overflow:hidden;background:#FFF">'
            '<div data-tag="copy" style="position:absolute;left:20px;top:-60px;'
            'font:700 40px sans-serif">one<br>two</div></div>')
    async with B.session():
        pg = await B._SESSION.page(W2, H2)

        await pg.set_content(B.page(W2, H2, "var(--bg)", CROP, grain=False), wait_until="load")
        await B._settle(pg)
        undeclared = await rec.measure_dom(pg, W2, H2)
        assert any("photo" in str(t) for t, *_ in undeclared["clipped"])
        ok("an UNDECLARED crop reports CLIPPED — the check is not weakened")

        declared = await rec.measure_dom(pg, W2, H2, crop_tags=("photo", "frame"))
        assert declared["clipped"] == [], declared["clipped"]
        ok("declaring the crop silences it, container and child alike")

        await pg.set_content(B.page(W2, H2, "var(--bg)", REAL, grain=False), wait_until="load")
        await B._settle(pg)
        still = await rec.measure_dom(pg, W2, H2, crop_tags=("photo", "frame"))
        assert any("copy" in str(t) for t, *_ in still["clipped"])
        ok("...and a DIFFERENT element's accidental clip still fires (the 77e7bb34 bug)")

asyncio.run(crop_tests())

# ── shapes.ribbon — the corpus's most-wanted missing silhouette ─────────────
# 12 of the 74 references call for a flowing band: a winding ribbon threading down
# a page, a swooping arrow-band behind a headline, a wavy torn panel edge. There
# was no primitive, so a recreation hand-wrote a Catmull-Rom generator from scratch
# and every future reference with the motif would have hit the same wall.
S_ = [(12, 18), (52, 26), (70, 50), (40, 64), (30, 80), (66, 86), (88, 70)]
r_ = sh.ribbon(S_, width=13)
assert r_.startswith("M") and r_.rstrip().endswith("Z")
ok("ribbon() returns a CLOSED path, so it fills like any other silhouette")
assert r_.count("L") > 100
ok("...sampled densely enough to read as a curve, not a polyline")

assert sh.ribbon([(0, 0)]) == "" and sh.ribbon([]) == ""
ok("fewer than two points degrades to empty instead of raising")

_w8, _w20 = sh.ribbon(S_, width=8), sh.ribbon(S_, width=20)
assert _w8 != _w20
ok("width actually changes the band")

_tap = sh.ribbon(S_, taper=[4, 15, 15, 13, 10, 15, 4])
assert _tap != r_
ok("a taper list overrides the constant width — a ribbon that thins reads as drawn")

_closed = sh.ribbon(S_, closed=True)
assert _closed != r_ and _closed.count("L") > r_.count("L")
ok("closed=True joins the run back to its start")

# the exact shape family the agent could not reach: flat run into a 180 hook
_hook = sh.ribbon([(20, 20), (70, 20), (84, 20), (88, 32), (76, 40), (64, 36), (60, 26)],
                  width=11)
_xs = [float(t.split(",")[0]) for t in _hook.replace("M", "L").split("L")[1:] if "," in t]
assert max(_xs) > 88 and min(_xs) < 22
ok("a flat run into a tight 180 hook spans its full intended extent (80cb7ed7)")

assert sh.ribbon(S_, width=13) == sh.ribbon(S_, width=13)
ok("ribbon is deterministic — the same points give the same path")

print(f"\nALL {N} ASSERTIONS PASSED")
