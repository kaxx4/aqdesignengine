"""Self-test for layout.invisible_craft_scan — reproduces the exact historical bug.

BUG (Friendship Day carousel v1, 2026-08-02): on the two ink-based slides every element carried
`border:7px solid var(--ink)` + `box-shadow:12px 12px 0 var(--ink)` against an ink page. The whole
AQ craft layer (CLAUDE.md §9 "thick ink outlines · hard-offset ink shadows") rendered invisible.
Every existing gate passed. Only the looking gate caught it.
"""
import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); lay = load("layout")

INK = "#0A0A0A"; CREAM = "#F4EFE0"
n = 0
def ok(cond, msg):
    global n
    assert cond, "FAIL: " + msg
    n += 1
    print(f"  ok {n}: {msg}")

# ── 1. THE HISTORICAL BUG, verbatim from v1's punch box ───────────────────────
bug = ('<div style="background:#FF4D8C;border:7px solid var(--ink);'
       'box-shadow:12px 12px 0 var(--ink);padding:12px">wish them</div>')
hits = lay.invisible_craft_scan(bug, "var(--ink)", core)
ok(len(hits) == 2, "catches BOTH the ink border and the ink hard-shadow on an ink page")
ok({h[0] for h in hits} == {"border", "box-shadow"}, "reports which property vanished")

# ── 2. THE FIX must pass — cream outline on an ink field ──────────────────────
fixed = (f'<div style="background:#FF4D8C;border:7px solid {CREAM};'
         f'box-shadow:12px 12px 0 {CREAM};padding:12px">wish them</div>')
ok(lay.invisible_craft_scan(fixed, "var(--ink)", core) == [],
   "the fix (outline colour flips with the field) is clean")

# ── 3. The SAME markup on a cream page was never a bug — must not fire ────────
ok(lay.invisible_craft_scan(bug, "var(--bg)", core) == [],
   "ink outline on a CREAM page is correct and stays silent")

# ── 4. literal hex must resolve the same as a var() token ─────────────────────
lit = f'<div style="border:6px solid {INK};box-shadow:8px 8px 0 {INK}"></div>'
ok(len(lay.invisible_craft_scan(lit, INK, core)) == 2, "literal #hex resolves like var(--ink)")

# ── 5. things it must never guess at (skip, don't fabricate) ──────────────────
ok(lay.invisible_craft_scan('<div style="border:2px solid rgba(0,0,0,.4)"></div>', INK, core) == [],
   "rgba() is skipped, not guessed")
ok(lay.invisible_craft_scan('<div style="border:2px solid black"></div>', INK, core) == [],
   "named colours are skipped, not guessed")
ok(lay.invisible_craft_scan('<div style="box-shadow:inset 0 0 4px #0A0A0A"></div>', INK, core) == [],
   "inset shadows are not the hard-offset craft layer")
ok(lay.invisible_craft_scan(bug, None, core) == [], "unresolvable page_bg -> skip, never crash")

# ── 6. it is ADVISORY — must never flip preflight's `clean` ───────────────────
els = [("a", 40, 40, 200, 200), ("b", 400, 400, 200, 200)]
r = lay.preflight(1080, 1440, els, html=bug, page_bg="var(--ink)", core=core)
ok(r["invisible_craft"], "preflight surfaces invisible_craft")
ok(r["clean"] is True, "but it is ADVISORY — a known-FP check never flips clean")

print(f"\nALL {n} ASSERTIONS PASSED")
