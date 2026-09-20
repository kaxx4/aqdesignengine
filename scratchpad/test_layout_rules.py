"""REBUILT 2026-08-03. The original file was cited in CLAUDE.md §8/§12 as "21 assertions, each
reconstructs a real failure" but was missing from the repo entirely — found during the
friendship_day session. This rebuild restores that contract: every assertion reconstructs a
documented historical bug from the §10 catalog, so each rule can be demonstrated catching the
thing it exists for.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_layout_rules.py
Companions: test_collision_nudge.py · test_invisible_craft.py · test_doodle_stamp.py
"""
import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\Code\AquaTerra\AQ_CODEBASE")
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
# ignore_pairs USED to require frozenset({a,b}) exactly, and a plain tuple — the obvious
# guess — silently matched nothing while the collision kept firing. This assertion used
# to PIN THAT FOOTGUN IN PLACE by asserting the tuple failed. A test that documents a
# footgun as expected behaviour is a test that prevents the fix: when a Sonnet agent lost
# a full debug cycle to it and the API was corrected, this test failed, correctly, for
# asserting the old broken contract. Worth remembering — encode the RULE, not the bug.
_pair = [("doodle", 0, 0, 200, 200), ("headline", 100, 100, 200, 200)]
ok(lay.collision_check(_pair, ignore_pairs={frozenset({"doodle", "headline"})}) == [],
   "by-design overlaps can be whitelisted via ignore_pairs (tags-on-hero, sign piles)")
ok(lay.collision_check(_pair, ignore_pairs={("doodle", "headline")}) == [],
   "a TUPLE now whitelists too — the silent no-op is fixed")
ok(lay.collision_check(_pair, ignore_pairs=[["doodle", "headline"]]) == [],
   "...and a list of lists, and a set: any spelling of a PAIR works")
ok(lay.collision_check(_pair, ignore_pairs={"doodle"}) != [],
   "an entry that is not a pair is REPORTED, not silently dropped")

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

# ══ cascade_peek_check — "deck offset hides the back cards" (2022ebef4ffad5, 2026-09-03) ════
buggy_stack = [(170 + 88, 470 + 96, 590, 459), (170 + 44, 470 + 48, 648, 504), (170, 470, 720, 560)]
ok(lay.cascade_peek_check(buggy_stack) != [],
   "2022ebef4ffad5 v3 (actual coords): back cards offset DOWN-RIGHT and shrunk end up nested "
   "fully inside the frontmost card's bounds -- the 'cascade' rendered as one flat card. Caught.")
fixed_stack = [(170 + 30, 560 + -110, 612, 476), (170 + 15, 560 + -55, 662, 515), (170, 560, 720, 560)]
ok(lay.cascade_peek_check(fixed_stack) == [],
   "v4 fix: back cards offset UP so their top edge crosses the frontmost card's top edge -- "
   "each one visibly peeks out. Passes.")
ok(lay.cascade_peek_check([(0, 0, 100, 100)]) == [],
   "a single-card 'stack' (nothing behind it to hide) trivially passes")

# ── READING ORDER (session 10f, from out/session10f/c1_v3.png) ───────────────
# "showing up again and again" set as three chips at x=48 / x=560 / x=48. Every
# chip legible, nothing colliding, no dead quadrant, pixel critique happy — but
# chips 1 and 3 shared a left edge, so they read as a COLUMN and the sentence
# scanned "showing -> and again -> up again". A Sonnet agent iterated the piece
# TWICE, fixed the empty quadrant the metrics named, and never saw this.
REAL = [("SHOWING", 48, 672, 560, 80),      # the exact coordinates from c1_v3.py
        ("UP AGAIN", 560, 726, 500, 80),
        ("AND AGAIN", 48, 800, 520, 72)]
_ro = lay.reading_order_check(REAL)
ok(len(_ro) == 1 and "COLUMN TRAP" in _ro[0],
   "the real c1_v3 chip placement is caught as a column trap")
ok("SHOWING" in _ro[0] and "AND AGAIN" in _ro[0] and "UP AGAIN" in _ro[0],
   "...and the message names all three, in the order they will actually be read")

# it must not fire on the two placements that are CORRECT, or nobody will use it
ok(lay.reading_order_check([("a", 48, 100, 400, 80), ("b", 48, 190, 400, 80),
                            ("c", 48, 280, 400, 80)]) == [],
   "a plain left-aligned three-line stack passes — all three share the edge")
ok(lay.reading_order_check([("a", 48, 100, 400, 80), ("b", 300, 200, 400, 80),
                            ("c", 560, 300, 400, 80)]) == [],
   "a clean diagonal stagger passes — chips 1 and 3 are not aligned")
ok(lay.reading_order_check(REAL[:2]) == [],
   "two chips alone cannot form a column trap (it needs three)")

# the unambiguous half
_inv = lay.reading_order_check([("first", 48, 600, 300, 80), ("second", 48, 100, 300, 80)])
ok(len(_inv) == 1 and "INVERTED" in _inv[0],
   "a part read second but placed entirely above the first is an inversion")
ok(lay.reading_order_check([("first", 48, 100, 300, 80), ("second", 48, 300, 300, 80)]) == [],
   "...and the same two in the right order do not fire")

# bare (x,y,w,h) boxes are accepted like every other check in this module
ok(lay.reading_order_check([(48, 672, 560, 80), (560, 726, 500, 80),
                            (48, 800, 520, 72)]) != [],
   "unlabelled boxes still work — labels are for the message, not the logic")

# and it is a HARD FAIL in preflight, because a scrambled sentence is not taste
_pf = lay.preflight(1080, 1350, [(48, 672, 560, 80)], reading_order=REAL)
ok(_pf["clean"] is False and _pf["reading_order"],
   "preflight fails on a column trap — opt-in, so it never fires unasked")
ok(lay.preflight(1080, 1350, [(48, 672, 560, 80)])["clean"] is True,
   "...and a build that declares no sentence is unaffected")

# ── IGNORE PAIRS NAMING UNDECLARED ELEMENTS (session 10f, from c2_v3.png) ───
# The script whitelisted ("book","card") and ("umbrella","card") while book,
# umbrella and a lemon star were all missing from `elements`. collision_check
# therefore could not see them, preflight printed CLEAN, and the star landed on
# the words "SIGN-UPS OPEN NOW". The author had thought about those overlaps —
# they just never entered the gate's world, and nothing said so.
import io as _io, contextlib as _ctx

def _say(els, ign):
    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        lay.collision_check(els, ignore_pairs=ign)
    return buf.getvalue()

_E = [("card", 200, 600, 700, 700), ("envelope", 0, 1300, 1080, 300)]
_out = _say(_E, {("book", "card"), ("umbrella", "card"), ("card", "envelope")})
ok("UNDECLARED" in _out and "book" in _out and "umbrella" in _out,
   "an ignore pair naming an undeclared label is reported (the c2_v3 star bug)")
ok("card" not in _out.split("UNDECLARED")[1].split("]")[0],
   "...and a label that IS declared is not named in that warning")
ok(_say(_E, {("card", "envelope")}) == "",
   "a build whose ignore pairs all name real elements says nothing")
ok(_say(_E, set()) == "",
   "no ignore pairs at all is silent — the check cannot fire unasked")

print(f"\nALL {n} ASSERTIONS PASSED")
