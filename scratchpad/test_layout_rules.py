"""REBUILT 2026-08-03. The original file was cited in CLAUDE.md §8/§12 as "21 assertions, each
reconstructs a real failure" but was missing from the repo entirely — found during the
friendship_day session. This rebuild restores that contract: every assertion reconstructs a
documented historical bug from the §10 catalog, so each rule can be demonstrated catching the
thing it exists for.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_layout_rules.py
Companions: test_collision_nudge.py · test_invisible_craft.py · test_doodle_stamp.py
"""
import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); lay = load("layout")

W, H = 1080, 1350
INK = "#0A0A0A"; CREAM = "#F4EFE0"
n = 0
def ok(cond, msg):
    global n
    assert cond, "FAIL: " + msg
    n += 1
    print(f"  ok {n:2d}: {msg}")

# ══ bounds_check — "Element clips off-canvas" (samples 6, 9, 10) ══════════════
ok(lay.bounds_check(W, H, [(40, 40, 200, 200)]) == [],
   "bounds_check passes an element fully inside the canvas")
ok(lay.bounds_check(W, H, [(950, 40, 200, 200)]) != [],
   "sample 9/10: element running off the RIGHT edge is caught")
ok(lay.bounds_check(W, H, [(40, 1250, 200, 200)]) != [],
   "sample 6: element running off the BOTTOM is caught (feed is 1350, not taller)")
ok(lay.bounds_check(W, H, [(-30, 40, 200, 200)]) != [],
   "negative origin (off the LEFT edge) is caught")

# ══ collision_check — "Doodle/badge dropped over text" (samples 26, 27, 32) ═══
ok(lay.collision_check([(0, 0, 100, 100), (200, 200, 100, 100)]) == [],
   "collision_check passes two well-separated elements")
ok(lay.collision_check([(0, 0, 200, 200), (100, 100, 200, 200)]) != [],
   "sample 26: a genuine overlap is caught")
ok(lay.collision_check([(0, 0, 100, 100), (95, 0, 100, 100)]) == [],
   "a 5px graze is BELOW min_overlap=12 and correctly tolerated (no false positive)")
hit = lay.collision_check([("doodle", 0, 0, 200, 200), ("headline", 100, 100, 200, 200)])
ok(hit and any("doodle" in str(h) and "headline" in str(h) for h in hit),
   "labels are echoed so the report names WHICH two elements collided")
# NOTE: ignore_pairs takes a set of frozenset({a,b}) — an unordered PAIR, not a tuple.
# A plain tuple silently fails to match and the collision still fires (verified below).
ok(lay.collision_check([("doodle", 0, 0, 200, 200), ("headline", 100, 100, 200, 200)],
                       ignore_pairs={frozenset({"doodle", "headline"})}) == [],
   "by-design overlaps can be whitelisted via ignore_pairs (tags-on-hero, sign piles)")
ok(lay.collision_check([("doodle", 0, 0, 200, 200), ("headline", 100, 100, 200, 200)],
                       ignore_pairs={("doodle", "headline")}) != [],
   "a TUPLE in ignore_pairs does NOT whitelist — it must be a frozenset (API footgun)")

# ══ invisible_color_check — "fill == surface" (samples 21, 24) ════════════════
ok(lay.invisible_color_check([("badge", "var(--bg)")], "var(--bg)", core) != [],
   "sample 21: a badge filled with the PAGE BG is invisible and is caught")
ok(lay.invisible_color_check([("badge", "var(--pink)")], "var(--bg)", core) == [],
   "a pink badge on cream has real contrast and passes")
ok(lay.invisible_color_check([("stroke", "#0A0A0A", "#0C0C0C")], "var(--bg)", core) != [],
   "sample 24: a near-ink stroke on a near-ink surface is caught via the 3-tuple surface arg")
ok(lay.invisible_color_check([("grad", "linear-gradient(red,blue)")], "var(--bg)", core) == [],
   "gradients are SKIPPED, never guessed at")
ok(lay.invisible_color_check([("named", "rebeccapurple")], "var(--bg)", core) == [],
   "named colours are SKIPPED, never guessed at")

# ══ css_var_check — "var(--typo) renders transparent" (sample 32) ═════════════
ok(lay.css_var_check('<div style="color:var(--ink)">x</div>', core) == [],
   "css_var_check passes a var that core actually defines")
ok(lay.css_var_check('<div style="color:var(--inkk)">x</div>', core) != [],
   "sample 32: a typo'd var (--inkk) is caught — it would render transparent")

# ══ same_as_bg_scan — the AUTO gate (showcase5b) ══════════════════════════════
ok(lay.same_as_bg_scan('<div style="background:var(--bg)">x</div>', "var(--bg)", core) != [],
   "showcase5b: an element background equal to the page bg is caught automatically")
ok(lay.same_as_bg_scan('<div style="position:absolute;inset:0;background:var(--bg)"></div>',
                       "var(--bg)", core) == [],
   "a full-bleed inset:0 BACKDROP layer is the field itself — correctly exempt")

# ══ star_text_width — "text overflows a star's waist" (samples 19, 44) ════════
ok(lay.star_text_width(400) < 400,
   "sample 44: star_text_width returns LESS than the star's diameter (the waist, not the box)")
ok(lay.star_text_width(400) < lay.star_text_width(600),
   "the safe width scales with the star")

# ══ dominance_check — "hero far too small" (sample 42) ════════════════════════
ok(lay.dominance_check([(0, 0, 100, 100)], W, H) != [],
   "sample 42: a layout whose largest element reaches no hero scale is flagged (opt-in)")
ok(lay.dominance_check([(0, 0, 700, 700)], W, H) == [],
   "a genuine hero passes dominance_check")

# ══ img_src_check ════════════════════════════════════════════════════════════
ok(lay.img_src_check('<img src="data:image/png;base64,AAAA">') == [],
   "a real embedded data-URI image passes")
ok(lay.img_src_check('<img src="">') != [], "an empty img src is caught")

# ══ preflight — the bundle, and what is HARD vs ADVISORY ═════════════════════
r = lay.preflight(W, H, [("a", 40, 40, 200, 200), ("b", 600, 600, 300, 300)],
                  html='<div style="color:var(--ink)">x</div>', page_bg="var(--bg)", core=core)
ok(r["clean"] is True, "preflight reports CLEAN on a genuinely clean build")
r2 = lay.preflight(W, H, [("a", 950, 40, 200, 200)], html=None)
ok(r2["clean"] is False and r2["off_canvas"], "preflight FAILS clean on a hard bug (off-canvas)")
ok("under_filled_quadrants" in r and r["clean"] is True,
   "under_filled_quadrants is ADVISORY — reported, but never flips clean")

print(f"\nALL {n} ASSERTIONS PASSED")
