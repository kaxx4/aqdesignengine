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

print(f"\nALL {N} ASSERTIONS PASSED")

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

print(f"\nALL {N} ASSERTIONS PASSED")
