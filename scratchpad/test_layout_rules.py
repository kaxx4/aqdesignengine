"""REBUILT 2026-08-03. The original file was cited in CLAUDE.md §8/§12 as "21 assertions, each
reconstructs a real failure" but was missing from the repo entirely — found during the
friendship_day session. This rebuild restores that contract: every assertion reconstructs a
documented historical bug from the §10 catalog, so each rule can be demonstrated catching the
thing it exists for.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_layout_rules.py
Companions: test_collision_nudge.py · test_invisible_craft.py · test_doodle_stamp.py
"""
import os, sys, importlib.util
# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

# ── TEXT THAT IS THERE BUT CANNOT BE READ (session 10f, from 110a5730 v4) ───
# A recreation put white 30px copy on a lavender card and DECLARED the pair
# honestly: ("card2_title", WHITE, LAVENDER) was right there in color_pairs.
# invisible_color_check ran on that exact pair and passed it, because its question
# is "is this the SAME colour as its backing" — an RGB distance — and #FFFFFF vs
# #DAD1FF are plainly different colours. They are also 1.44:1. core.text_on()
# would have returned ink at 13.71:1. The engine knew; nothing asked.
shapes_m = load("shapes")
LAV = shapes_m.lighten(core.ACCENTS[5], 0.72)
WHITE_ = "#FFFFFF"

ok(round(core.contrast(WHITE_, LAV), 2) == 1.44,
   "MEASURED: white on that lavender is 1.44:1 — barely above invisible")
ok(lay.invisible_color_check([("card2_title", WHITE_, LAV)], "#FF4D2E", core) == [],
   "invisible_color_check passes it — distance is the wrong question for legibility")

_tc = lay.text_contrast_check([("card2_title", WHITE_, LAV, 30, True)], core=core)
ok(len(_tc) == 1 and _tc[0][3] == 1.44,
   "text_contrast_check catches it and reports the real ratio")
ok(_tc[0][5] == core.text_on(LAV) == "#0A0A0A",
   "...and hands back the colour core.text_on would have chosen (13.71:1)")

# the WCAG large-text split must be honoured, or it will be wrong about every hero
ok(lay.text_contrast_check([("num", core.ACCENTS[1], core.CREAM, 500, True)], core=core) == [],
   "a 500px mint numeral on cream (3.78:1) passes the 3.0 large-text floor")
_small = lay.text_contrast_check([("lbl", core.ACCENTS[1], core.CREAM, 20, True)], core=core)
ok(len(_small) == 1 and _small[0][4] == core.AA_NORMAL,
   "...and the SAME mint at 20px fails the 4.5 floor — the on_cream rule, enforced")

ok(lay.text_contrast_check([("a", core.INK, core.CREAM, 16)], core=core) == [] and
   lay.text_contrast_check([("b", "#FFFFFF", core.INK, 16)], core=core) == [],
   "the two normal AQ combinations do not fire")
ok(lay.text_contrast_check([("c", "var(--nope)", "#FFF", 16)], core=core) == [],
   "an unresolvable colour is SKIPPED, never guessed (same contract as its sibling)")
ok(lay.text_contrast_check([("d", WHITE_, LAV)], core=None) == [],
   "without core it returns nothing rather than inventing a contrast model")

_pf2 = lay.preflight(1080, 1350, [(0, 0, 100, 100)],
                     text_pairs=[("card2_title", WHITE_, LAV, 30, True)], core=core)
ok(_pf2["clean"] is False and _pf2["unreadable_text"],
   "preflight HARD-FAILS on unreadable copy — opt-in, so it never fires unasked")

# ── CONTAINMENT IS NOT COLLISION (session 10f, from agent r1) ───────────────
# A UI-mockup recreation with four cards had to hand-list one ignore pair per
# child. A forgotten pair is indistinguishable from a real bug; a typo'd one
# silently whitelists nothing. Declaring the CARD once says what was meant.
CARD = [("card", 80, 180, 400, 300), ("title", 104, 204, 300, 40),
        ("body", 104, 260, 340, 80), ("stray", 300, 150, 120, 120)]

_bare = lay.collision_check(CARD)
ok(len(_bare) == 4, "without containers, every child of the card is reported (4 pairs)")

_held = lay.collision_check(CARD, containers=("card",))
ok(len(_held) == 2, "declaring the card drops the two contained children")
ok(all("card" not in (a, b) or "stray" in (a, b) for a, b, _, _ in _held),
   "...and the card is only cleared against things actually INSIDE it")
ok(any({a, b} == {"card", "stray"} for a, b, _, _ in _held),
   "a doodle hanging OFF the card's edge is still a collision")
ok(any({a, b} == {"title", "stray"} for a, b, _, _ in _held),
   "...and siblings inside a container are still checked against each other")

# the containment test is geometric, not by name — a child must really be inside
_out = [("card", 80, 180, 400, 300), ("title", 40, 204, 300, 40)]
ok(lay.collision_check(_out, containers=("card",)) != [],
   "a 'child' that pokes outside its container is NOT silently forgiven")

_g = _say([("card", 80, 180, 400, 300)], set())
ok(_g == "", "no containers declared, nothing said")
_buf = _io.StringIO()
with _ctx.redirect_stdout(_buf):
    lay.collision_check(CARD, containers=("panel",))
ok("CONTAINERS NOT IN THE ELEMENT LIST" in _buf.getvalue() and "panel" in _buf.getvalue(),
   "a container that was never declared is reported, not silently ignored")

_pf3 = lay.preflight(1080, 1350, CARD, containers=("card",))
ok(len(_pf3["collisions"]) == 2,
   "preflight carries containers through to the collision check")

# ── DOUBLE ROTATION (session 10f, agent c2) ─────────────────────────────────
# doodles.stamp(rot=) and shapes.sticker(rot=) BAKE the angle into the svg they
# return. Wrapping one in a div that also rotates draws it at the SUM. Every
# rotated doodle in two versions came out at twice its intended angle, and
# rotated_bbox — computed for the angle the author thought they applied — then
# under-reported the real footprint by an amount that looks like rounding.
dd_m = load("doodles")
_star = dd_m.stamp("star", "#FFC700", rot=10)

_bug = f'<div style="position:absolute;transform:rotate(10deg)">{_star}</div>'
_hits = lay.double_rotation_scan(_bug)
ok(len(_hits) == 1 and _hits[0] == (10.0, 10.0, 20.0),
   "the c2 bug is caught, and the report shows the SUM that was actually drawn")

_ok_wrap = f'<div style="position:absolute;left:10px">{_star}</div>'
ok(lay.double_rotation_scan(_ok_wrap) == [],
   "the §6 template's own pattern (unrotated wrapper) does not fire")

_counter = ('<div style="transform:rotate(12deg)">'
            '<span style="transform:rotate(-12deg)">level</span></div>')
_c = lay.double_rotation_scan(_counter)
ok(len(_c) == 1 and _c[0][2] == 0.0,
   "deliberate counter-rotation reports a SUM OF ZERO — the tell that it was meant")

ok(lay.double_rotation_scan('<div style="transform:rotate(0deg)">x</div>') == [],
   "a 0deg transform is not a rotation and does not fire")
ok(lay.double_rotation_scan("<div>plain</div>") == [],
   "html with no transforms at all is silent")

_pf4 = lay.preflight(1080, 1350, [("s", 100, 100, 90, 90)], html=_bug, core=core)
ok(_pf4["clean"] is True and _pf4["double_rotation"],
   "preflight reports it as ADVISORY — counter-rotation is legal, so it cannot block")

print(f"\nALL {n} ASSERTIONS PASSED")
