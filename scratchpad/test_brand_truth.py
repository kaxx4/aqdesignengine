"""Self-tests for the session-10 brand-truth layer in engine/core.py.

Every assertion below reconstructs a REAL defect found by reading the live site
(vercelaq-main/frontend/src/styles/tokens.css) against what the poster engine
was actually emitting. A rule you cannot demonstrate catching its bug is not
done — CLAUDE.md §8 step 3.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_brand_truth.py
"""
import os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = _load("core")
N = 0
def ok(msg):
    global N; N += 1; print(f"  ok {N}: {msg}")

PINK, MINT, LEMON, TOMATO, SKY, GRAPE, TEAL = core.ACCENTS
CREAM, INK, PAPER = core.CREAM, core.INK, core.PAPER

# ── 1. THE BUG: white on pink ────────────────────────────────────────────────
# core.text_on() read a hand-kept INK_ON set and returned WHITE for pink. White
# on #FF4D8C measures 3.14:1 — below the 4.5:1 AA floor for normal text. Ink on
# the same pink is 6.31:1. The engine shipped the failing pairing for 44 posters.
assert abs(core.contrast(PAPER, PINK) - 3.14) < 0.02, core.contrast(PAPER, PINK)
ok("historical: white on pink is 3.14:1 — genuinely below the AA floor")
assert abs(core.contrast(INK, PINK) - 6.31) < 0.02
ok("historical: ink on the same pink is 6.31:1 — twice as legible")
assert core.text_on(PINK) == INK, "regression: text_on(pink) must be ink"
ok("text_on(pink) now returns ink, not white")

# the same bug, on the other three accents it affected
for nm, hexv in (("mint", MINT), ("tomato", TOMATO), ("grape", GRAPE)):
    assert core.text_on(hexv) == INK, nm
ok("text_on fixed for mint / tomato / grape too (all four the old set got wrong)")

# and it did NOT overcorrect: teal genuinely wants paper
assert core.contrast(INK, TEAL) < core.contrast(PAPER, TEAL)
assert core.text_on(TEAL) == PAPER
ok("teal still takes paper — ink on it is 4.00:1, the fix did not overcorrect")

# the choice is MEASURED, so it is right for colours outside ACCENTS too
assert core.text_on("#FFFFFF") == INK and core.text_on("#000000") == PAPER
ok("text_on generalises to non-palette colours (it measures, not looks up)")

# every accent can carry SOME legible text
for h in core.ACCENTS:
    assert core.text_on_passes(h), h
ok("every one of the 7 accents clears AA with its correct text colour")

# non-colour input must not explode — bespoke scripts pass var(--x) constantly
for junk in ("var(--bg)", "linear-gradient(red,blue)", None, 42):
    assert core.text_on(junk) == INK
ok("text_on falls back to ink for var()/gradient/None/garbage instead of raising")

# ── 2. THE BUG: accent-coloured type on the cream page ───────────────────────
# Not one accent clears 4.5:1 on #F4EFE0, so accent small-type on the page
# ground was ALWAYS illegible. The engine had no guard and no darker partner.
for h in core.ACCENTS:
    assert core.contrast(h, CREAM) < 4.5, f"{h} unexpectedly passes on cream"
ok("confirmed: all 7 raw accents FAIL 4.5:1 as type on cream (the gap)")

for h in core.ACCENTS:
    v = core.ink_of(h)
    assert v != h, f"{h} has no ink partner"
    assert core.contrast(v, CREAM) >= 4.5, (h, v, core.contrast(v, CREAM))
    assert core.contrast(v, PAPER) >= 4.5, (h, v)
ok("every ink_of() partner clears 4.5:1 on BOTH cream and white")

assert core.ink_of("#123456") == "#123456"
ok("ink_of passes unknown colours through — never invents a brand value")

# the partners are dark fills, so type ON them must be paper
for h in core.ACCENTS:
    assert core.text_on(core.ink_of(h)) == PAPER
ok("text on an ink-variant fill resolves to paper (the site's --on-pink-ink branch)")

# ── 3. THE BUG: department colour was an arbitrary rotation index ────────────
# generate(name, archetype, content, accent_idx) picked the hue by INDEX, so a
# welfare poster could come out grape while the site teaches welfare = mint.
assert core.accent_for("welfare") == MINT
assert core.accent_for("events") == SKY
assert core.accent_for("labs") == LEMON
assert core.accent_for("content") == GRAPE
assert core.accent_for("ops") == TEAL
ok("accent_for() pins each department to the hue the website teaches")

assert core.accent_for("  WELFARE  ") == MINT
ok("accent_for is case/whitespace tolerant (CSV categories are messy)")
assert core.accent_for("not-a-dept") == PINK
assert core.accent_for(None) == PINK
ok("unknown/None department falls back to pink rather than raising")

assert core.DEPT_SITE_TEAL == "#12909C" and core.DEPT["ops"] == "#0E7C86"
ok("the site/engine teal DRIFT is recorded as data, not silently reconciled")

# ── 4. craft scales ──────────────────────────────────────────────────────────
assert core.radius_inside(32, 10) == 22 and core.radius_inside(22, 8) == 14
ok("radius_inside reproduces the site's concentric 32/22/14 spine")
assert core.radius_inside(10, 40) == 0
ok("radius_inside clamps at 0 instead of going negative")

assert core.hard_shadow("base") == "2px 2px 0 0 #0A0A0A"
assert core.hard_shadow("lg") == "3px 3px 0 0 #0A0A0A"
ok("hard_shadow emits the site's 1.5/2/3/4 hard-offset scale")
assert "0 0 0 2px #F4EFE0" in core.keyline() and "0 0 0 4px #0A0A0A" in core.keyline()
ok("keyline() is the paper-gap-then-ink-ring sticker treatment (site rule 4)")
assert core.keyline(ring_bg="#FF4D8C").startswith("0 0 0 2px #FF4D8C")
ok("keyline's first ring follows the surface the sticker actually sits on")

# ── 5. THE BUG: ink outline on an ink field = invisible craft layer ──────────
# friendship_day lost its ENTIRE craft layer this way. outline_of makes the
# outline colour a function of the surface instead of a constant.
assert core.outline_of(CREAM) == INK
assert core.outline_of("#0A0A0A") == CREAM
assert core.outline_of(MINT) == CREAM     # mint is dark enough to need a light line
assert core.outline_of(LEMON) == INK
ok("outline_of flips to cream on dark fields — the friendship_day craft bug")
assert core.outline_of("var(--bg)") == INK
ok("outline_of tolerates var() input")

# ── TYPE ON A DARK GROUND (session 10f) ─────────────────────────────────────
# on_cream() took a `ground=` argument, which invites `on_cream(a, 16, ground=INK)`
# for a dark-ground poster. Its only fallback was ink_of(), which DARKENS — so on a
# dark ground it walked the wrong way, failed again, and hit a hardcoded `else INK`.
# It returned #0A0A0A ON #0A0A0A: contrast 1.00:1, invisible. The catalog's oldest
# failure class, emitted by the helper that exists to prevent it.

TEAL = core.ACCENTS[6]
assert round(core.contrast(TEAL, INK), 2) == 4.00
ok("MEASURED: teal on ink is 4.00:1 — the one accent that fails small type there")

_was_the_bug = core.on_cream(TEAL, 16, ground=INK)
assert _was_the_bug != INK, "the exact historical return value"
assert core.contrast(_was_the_bug, INK) >= core.AA_NORMAL
ok("on_cream(teal, 16, ground=INK) no longer returns ink-on-ink")

assert core.on_dark(TEAL, 16) == _was_the_bug
ok("on_dark() is the named entry point for it, and agrees with on_cream(ground=INK)")

# the tint must be the SMALLEST step that passes — the department hue has to survive
_r, _g, _b = core._chan(core.on_dark(TEAL, 16))
assert _b > _r and _g > _r, "still teal, not a grey or a wash"
ok("...and the lightened partner keeps the hue (blue+green still dominate red)")
assert core.contrast(core.on_dark(TEAL, 16), INK) < 6.0, "no bigger a jump than needed"
ok("...tinting stops at the first value that clears the floor, not the brightest")

for a in core.ACCENTS:
    got = core.on_dark(a, 16)
    assert core.contrast(got, INK) >= core.AA_NORMAL, (a, got)
ok("every accent is legible as small type on ink after on_dark()")

# accents may still shout: display type keeps the raw accent under the 3.0 floor
assert core.on_dark(TEAL, 48) == TEAL
ok("at 48px bold teal clears the large-text floor and is returned untouched")

# the cream path must not have shifted while generalising
assert core.on_cream(core.ACCENTS[1], 16) == core.ink_of(core.ACCENTS[1])
assert core.on_cream(core.ACCENTS[1], 48) == core.ACCENTS[1]
ok("on_cream's own behaviour is unchanged — small darkens, display shouts")

# direction is MEASURED from the ground, not assumed
assert core.on_ground(TEAL, CREAM, 16) == core.ink_of(TEAL)   # light ground -> darken
assert core.on_ground(TEAL, INK, 16) != core.ink_of(TEAL)     # dark ground  -> lighten
ok("on_ground picks the direction by measuring the ground, both ways")

# a ground no accent can serve returns the winning NEUTRAL, never a fixed INK
_on_grape = core.on_ground(core.ACCENTS[0], core.ACCENTS[5], 16)
assert _on_grape == core.text_on(core.ACCENTS[5])
ok("when no accent can clear the floor, the neutral that WINS on that ground is used")

assert core.on_ground(TEAL, "var(--bg)", 16) == TEAL
ok("on_ground never guesses at a var()/gradient ground — it returns the accent unchanged")

print(f"\nALL {N} ASSERTIONS PASSED")
