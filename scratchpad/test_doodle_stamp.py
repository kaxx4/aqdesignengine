"""Self-test for doodles.stamp — reproduces the silent colour-drop bug.

BUG (found 2026-08-03, friendship_day carousel): the doodle() helper in CLAUDE.md §6's template
does `try: fn(fill=..) except TypeError: fn(rot=rot)`. The 5 stroke-drawn doodles reject `fill=`,
so the fallback ran and they rendered in their HARD-CODED DEFAULT colour. A pink arrow came out
tomato. No error, no warning — the requested colour was accepted and discarded.
"""
import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
dd = load("doodles")

PINK = "#FF4D8C"; MINT = "#1B8A5A"
n = 0
def ok(cond, msg):
    global n
    assert cond, "FAIL: " + msg
    n += 1
    print(f"  ok {n}: {msg}")

# ── 1. THE HISTORICAL BUG — the old helper shape drops the colour ────────────
def old_helper(kind, fill, rot=0):
    fn = getattr(dd, kind)
    try:    return fn(fill=fill, rot=rot, style="clean")
    except TypeError: return fn(rot=rot, style="clean")

ok(MINT not in old_helper("arrow", MINT), "old helper SILENTLY drops the colour on `arrow`")
ok("#FF4D2E" in old_helper("arrow", MINT), "...and renders arrow's hard-coded tomato default")
ok("#0E7C86" in old_helper("zigzag", PINK), "...a pink zigzag really did come out teal")
ok("#7E5BFF" in old_helper("ring", MINT), "...a mint ring really did come out grape")

# ── 2. THE FIX — every stroke-drawn doodle now takes the colour ──────────────
STROKE = ["ring", "arrow", "squiggle", "zigzag", "spiral"]
for k in STROKE:
    ok(PINK in dd.stamp(k, PINK), f"stamp() applies colour to stroke-drawn `{k}`")

# ── 3. fill-drawn doodles must keep working ──────────────────────────────────
for k in ["star", "heart", "paw", "speech", "leaf", "plus", "dots", "cross"]:
    ok(MINT in dd.stamp(k, MINT), f"stamp() applies colour to fill-drawn `{k}`")

# ── 4. globe has NO colour arg — must not crash, must not fake one ───────────
ok(dd.COLOR_ARG["globe"] is None, "globe is correctly known to have no colour arg")
g = dd.stamp("globe", PINK)
ok(PINK not in g and "<svg" in g, "globe renders its intrinsic AQ colours, never a forced fill")

# ── 5. the map itself is right ───────────────────────────────────────────────
ok(all(dd.COLOR_ARG[k] == "stroke" for k in STROKE), "COLOR_ARG marks all 5 stroke doodles")
ok(dd.COLOR_ARG["star"] == "fill", "COLOR_ARG marks fill doodles as fill")
ok(set(dd.COLOR_ARG) == set(dd.PACK), "every doodle in PACK is classified")

# ── 6. rot / style / seed still thread through ───────────────────────────────
ok("rotate(45deg)" in dd.stamp("star", PINK, rot=45), "rot threads through")
ok(dd.stamp("star", PINK, style="rough") != dd.stamp("star", PINK, style="clean"),
   "style threads through")
ok(dd.stamp("star", PINK, style="rough", seed=1) != dd.stamp("star", PINK, style="rough", seed=9),
   "seed threads through")

print(f"\nALL {n} ASSERTIONS PASSED")
