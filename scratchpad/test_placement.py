"""Self-tests for the session-10b PLACEMENT rules:
    shapes.inner_width / fit_font   — fit a label to the silhouette that holds it
    layout.occlusion_check          — an element buried behind what sits in front
    layout.fit_block                — solve a block's size to the room that remains
    layout.scatter_solve            — place a pile against real constraints

Every assertion reconstructs a failure from the four motif pieces, all of which
passed the pre-existing gate stack and were caught by looking.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_placement.py
"""
import os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

lay = _load("layout"); sh = _load("shapes")
N = 0
def ok(m):
    global N; N += 1; print(f"  ok {N}: {m}")

# ── shapes.fit_font — the BOX-UNITS trap ────────────────────────────────────
# sticker() scales a 0..100 box to `size` px, so label(size=13) inside a 206px
# badge renders at 26.8px. Writing a sensible-looking 13 really asked for 27, and
# "PATHER SATHI" ran out of both ends of its capsule.
assert sh.inner_width("capsule", 200) > sh.inner_width("burst", 200)
ok("a capsule offers more usable width than a starburst at the same diameter")
assert sh.inner_width("burst", 200) > sh.inner_width("star", 200)
ok("...and a burst more than a star, whose waist is narrowest of all")
assert sh.INNER_FRAC["star"] == 0.42
ok("the star fraction matches layout.star_text_width's already-measured waist")
assert 0 < sh.inner_width("not-a-shape", 200) < 200
ok("an unknown family falls back to a conservative fraction, never crashes")

box, fits = sh.fit_font(305, 40, "capsule", 206)
assert fits and box * 206 / 100 < sh.inner_width("capsule", 206) * 1.02
ok("PATHER SATHI (305px at 40px) fits a 206px capsule once fitted")
assert box < 13, box
ok("...at a SMALLER box size than the 13 that was hand-written — the trap, measured")

box2, fits2 = sh.fit_font(372, 40, "burst", 168)
assert not fits2
ok("'291 WORKSHOPS' reports fits=False in a 168px burst instead of shipping 5pt type")
assert box2 >= 5.0
ok("...and still returns a floor value rather than 0, so a caller cannot divide by it")

big, _ = sh.fit_font(100, 40, "capsule", 400)
small, _ = sh.fit_font(400, 40, "capsule", 400)
assert big > small
ok("a shorter label is fitted larger than a longer one at the same diameter")
assert sh.fit_font(0, 40, "capsule", 200)[1] is True
ok("a zero-width measurement degrades safely instead of dividing by zero")

# ── layout.occlusion_check ──────────────────────────────────────────────────
buried = [("badge", (100, 100, 200, 200), 5), ("headline", (0, 0, 900, 400), 20)]
hits = lay.occlusion_check(buried)
assert hits and hits[0][0] == "badge" and hits[0][1] == 0.0
ok("occlusion_check reports a badge fully behind a headline as 0% visible")

assert lay.occlusion_check([("badge", (100, 100, 200, 200), 30),
                            ("headline", (0, 0, 900, 400), 20)]) == []
ok("the same badge IN FRONT is never flagged — z-order is what is being tested")

HALF = [("b", (0, 0, 200, 200), 1), ("c", (100, 0, 200, 200), 9)]
half = lay.occlusion_check(HALF, min_visible=0.6)
assert half and abs(half[0][1] - 0.5) < 0.05, half
ok("a half-covered element measures ~50% visible")
assert lay.occlusion_check(HALF, min_visible=0.4) == []
ok("min_visible sets the tolerance — 50% clears a 40% floor, trips a 60% one")
assert lay.occlusion_check([("solo", (0, 0, 100, 100), 1)]) == []
ok("an element with nothing in front of it is never flagged")
assert lay.occlusion_check([]) == []
ok("occlusion_check tolerates an empty list")

# ── layout.fit_block ────────────────────────────────────────────────────────
# piece C set a headline by eye, it wrapped to one more line than planned, and the
# body copy landed on the footer.
assert lay.fit_block(300, 3, 0.9) == 300 / (3 * 0.9)
ok("fit_block solves size = room / (lines x line-height)")
assert lay.fit_block(300, 3, 0.9, extras=120) < lay.fit_block(300, 3, 0.9)
ok("reserving space for the body copy below shrinks the headline, as it must")
assert lay.fit_block(10000, 2, 0.9, max_size=96) == 96
ok("max_size caps it — a huge canvas does not mean a 900px headline")
assert lay.fit_block(10, 3, 0.9, min_size=24) == 24
assert lay.fit_block(-50, 3) == 24
ok("no room (or negative room) returns min_size instead of a nonsense value")

# ── layout.scatter_solve ────────────────────────────────────────────────────
# six versions of hand-typed coordinates, each fix trading one collision for
# another, is a search being done badly.
W, H = 1080, 1350
items = [(f"s{i}", 160, 160) for i in range(8)]
protect = [(64, 400, 950, 130), (64, 560, 500, 130)]
keep_out = [(0, 0, W, 130), (0, H - 200, W, 200)]
spots, unplaced = lay.scatter_solve(items, W, H, protect=protect, keep_out=keep_out, seed=3)
assert not unplaced, unplaced
ok("scatter_solve places all 8 badges against text + keep-out constraints")
assert len(spots) == len(items) and len({s[0] for s in spots}) == len(items)
ok("every item comes back exactly once")

boxes = {lab: (x, y, 160, 160) for lab, x, y in spots}
for lab, (x, y, w, h) in boxes.items():
    assert x >= 0 and y >= 0 and x + w <= W and y + h <= H, (lab, x, y)
ok("nothing is placed off-canvas")

def inter(a, b):
    ix = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    iy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(0, ix) * max(0, iy)

for lab, bx in boxes.items():
    for k in keep_out:
        assert inter(bx, k) == 0, (lab, "touches keep-out")
ok("the logo band and the footer band are never touched — keep_out is absolute")

for lab, bx in boxes.items():
    for pb in protect:
        assert inter(bx, pb) / (pb[2] * pb[3]) <= 0.31, (lab, "buries protected text")
ok("no protected text box is covered past the threshold")

names = list(boxes)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = boxes[names[i]], boxes[names[j]]
        assert inter(a, b) / (160 * 160) <= 0.19, (names[i], names[j])
ok("no two badges overlap each other past max_pair_overlap")

s1, _ = lay.scatter_solve(items, W, H, protect=protect, keep_out=keep_out, seed=3)
s2, _ = lay.scatter_solve(items, W, H, protect=protect, keep_out=keep_out, seed=3)
assert s1 == s2
ok("the same seed reproduces the same layout — placements are reproducible")
s3, _ = lay.scatter_solve(items, W, H, protect=protect, keep_out=keep_out, seed=4)
assert s1 != s3
ok("a different seed gives a genuinely different arrangement")

# an impossible ask must FAIL HONESTLY rather than stacking things badly
huge = [(f"h{i}", 500, 500) for i in range(9)]
_, un = lay.scatter_solve(huge, W, H, seed=5, tries=200)
assert un, "nine 500px badges cannot fit 1080x1350 without heavy overlap"
ok("an over-dense pile reports what it could NOT place instead of dumping it somewhere")

assert lay.scatter_solve([], W, H) == ([], [])
ok("scatter_solve tolerates an empty item list")

print(f"\nALL {N} ASSERTIONS PASSED")
