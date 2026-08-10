"""Self-test for vision.plan_spots_relaxed (CLAUDE.md §8 step 3).

Each assertion reproduces the real bug found in the 2026 workshop carousel batch (2026-08-07):
plan_spots returned [] on dense indoor photos, so slides rendered with NO doodles at all and
every gate still said CLEAN — the craft layer vanished silently.
"""
import os, sys, importlib.util

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


vision = load("vision")
W, H = 1080, 1350
SRC = "scratchpad/carousel_2026"
n_pass = 0


def check(label, cond):
    global n_pass
    assert cond, f"FAIL: {label}"
    n_pass += 1
    print(f"  ok  {label}")


# ── the exact photo that rendered with zero doodles in learners_den v1 ────────────────
dense = f"{SRC}/learners_den_art/src_images/06.jpg"

# The historical condition was BOTH things at once: a full-width top exclude band AND the
# strict default percentile. That combination is what returned [] and shipped a bare slide.
FULL_TOP = [(0, 0, W, 190), (0, H - 320, W, 320)]

# 1. reproduce the original bug exactly
strict = vision.plan_spots(dense, W, H, n=4, seed=1, busy_pctl=45, exclude=FULL_TOP)
check("baseline: original exclude+percentile combo starves this photo", len(strict) == 0)

# 2. the fix: the ladder recovers usable spots on the same photo (tight excludes)
spots, info = vision.plan_spots_relaxed(dense, W, H, n=4, seed=1)
check("relaxed ladder recovers >=2 spots", len(spots) >= 2)
check("ladder reports the rung it used", info["busy_pctl"] >= 45)
check("ladder reports not-starved when it succeeds", info["starved"] is False)

# 3. failure is REPORTED, never silent: an impossible exclude must set starved=True
blanket = [(0, 0, W, H)]
spots2, info2 = vision.plan_spots_relaxed(dense, W, H, n=4, seed=1, exclude=blanket)
check("fully-excluded photo yields no spots", len(spots2) == 0)
check("fully-excluded photo is flagged starved", info2["starved"] is True)

# 4. the root cause of the batch bug: a FULL-WIDTH top exclude severs every candidate region
#    from the top edge, which background_grid requires — starving an otherwise-fine photo.
full_top = [(0, 0, W, 190)]
tight = [(40, 30, 380, 100), (840, 90, 200, 55)]
a, _ = vision.plan_spots_relaxed(dense, W, H, n=4, seed=1, exclude=full_top)
b, _ = vision.plan_spots_relaxed(dense, W, H, n=4, seed=1, exclude=tight)
check("full-width top exclude starves the photo", len(a) < len(b))
check("tight UI-shaped excludes preserve spots", len(b) >= 2)

# 5. subject safety is NOT traded away by relaxing: every returned spot still clears the
#    skin veto and still carries real measured clearance
for s in spots:
    check(f"spot at ({s['x']},{s['y']}) has real clearance", s["clearance_px"] > 0)
    check(f"spot at ({s['x']},{s['y']}) is on canvas",
          0 <= s["x"] and 0 <= s["y"] and s["x"] + s["size"] <= W and s["y"] + s["size"] <= H)

# 6. determinism — same seed, same plan (batch output must be reproducible)
again, _ = vision.plan_spots_relaxed(dense, W, H, n=4, seed=1)
check("same seed reproduces the same spots",
      [(s["x"], s["y"]) for s in again] == [(s["x"], s["y"]) for s in spots])

print(f"\n{n_pass} assertions passed")
