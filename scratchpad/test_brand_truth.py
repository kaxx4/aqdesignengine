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

print(f"\nALL {N} ASSERTIONS PASSED")
