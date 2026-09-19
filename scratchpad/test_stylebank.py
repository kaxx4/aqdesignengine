"""Self-tests for engine/stylebank.py — the reference corpus as a STYLE BANK.

The bank's whole value is that "design something" never has to invent a composition
from nothing. So the properties that matter are: it always returns SOMETHING, the
measured fields are never hand-typed, and an over-specified request degrades instead
of failing.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_stylebank.py
"""
import os, sys, json, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

sb = _load("stylebank"); core = _load("core")
N = 0
def ok(m):
    global N; N += 1; print(f"  ok {N}: {m}")

bank = sb._load()
S = bank.get("styles", {})
assert S, "bank is empty — run `python engine/stylebank.py measure`"
ok(f"bank loads and holds {len(S)} styles")

# every reference image on disk is represented
refs = [f for f in os.listdir(sb.REFDIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
assert len(S) == len(refs), (len(S), len(refs))
ok("every reference image on disk has a bank entry")

# ── measured fields are MEASURED ────────────────────────────────────────────
for k, v in S.items():
    m = v.get("measured") or {}
    assert 0.0 <= m.get("coverage", -1) <= 1.0, k
    assert m.get("ground") in ("paper", "dark", "saturated", "mid"), (k, m.get("ground"))
    assert len(m.get("ground_rgb") or []) == 3, k
    assert m.get("aspect", 0) > 0, k
ok("every entry carries a valid measured coverage, ground, ground_rgb and aspect")

for k, v in S.items():
    bb = v["measured"].get("content_bbox")
    if bb:
        x0, y0, x1, y1 = bb
        assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1, (k, bb)
ok("content bboxes are ordered canvas fractions")

# the ground classifier does what it claims on known inputs
assert sb._classify_ground([0, 0, 0]) == "dark"
assert sb._classify_ground([244, 239, 224]) == "paper"
assert sb._classify_ground([255, 77, 46]) == "saturated"
ok("_classify_ground names ink, cream and a saturated accent correctly")

# measure() must be idempotent and must NOT clobber judged work
before = json.dumps(S.get(sorted(S)[0], {}).get("mechanism"))
sb.measure(verbose=False)
after = sb._load()["styles"][sorted(S)[0]].get("mechanism")
assert json.dumps(after) == before
ok("re-running measure() preserves judged fields (it is safe to re-run any time)")

# ── the picker ──────────────────────────────────────────────────────────────
p = sb.pick(seed=1)
assert p and "slug" in p and "measured" in p
ok("pick() returns a style")

a = sb.pick(seed=42); b = sb.pick(seed=42)
assert a["slug"] == b["slug"]
ok("the same seed draws the same style — briefs are reproducible")
seen = {sb.pick(seed=s)["slug"] for s in range(25)}
assert len(seen) > 2, seen
ok("different seeds genuinely spread across the bank")

# THE PROPERTY THAT MATTERS MOST: "design something" must never come back empty.
over = sb.pick(dept="nonexistent-dept", ground="chartreuse", hero="hologram",
               canvas="billboard", kind="fresco", seed=5)
assert over and over.get("slug")
ok("an impossible request still returns a style rather than failing")
assert over.get("relaxed"), "it must SAY which filters it had to drop"
ok("...and reports exactly which filters it relaxed to get there")

dark = sb.pick(ground="dark", seed=2)
assert dark["measured"]["ground"] == "dark" or "ground=dark" in dark.get("relaxed", [])
ok("a satisfiable filter is honoured")

judged_pick = sb.pick(judged_only=True, seed=9)
assert judged_pick.get("judged") or "judged_only" in judged_pick.get("relaxed", [])
ok("judged_only prefers styles someone has actually looked at")

# weighting: judged + written recipe should dominate a large sample
picks = [sb.pick(seed=s)["slug"] for s in range(60)]
judged_share = sum(1 for s in picks if S[s].get("judged")) / len(picks)
assert judged_share > 0.9, judged_share
ok(f"judged styles dominate the draw ({judged_share:.0%} of 60) — educated, not uniform")

# ── the brief ───────────────────────────────────────────────────────────────
txt = sb.brief(sb.pick(seed=3), "126 return visits to one partner")
for must in ("STYLE", "SUBJECT", "mechanism", "ground", "coverage", "compare.geometry"):
    assert must in txt, must
ok("brief() names the style, the subject, the measured numbers and the next step")
assert "126 return visits" in txt
ok("...and carries the subject through verbatim")
assert "engine.py" in txt and "never" in txt.lower()
ok("...and repeats the Workflow B rule so a builder cannot drift into ARCHETYPES")

# ── department colour is a RULE, not a preference ───────────────────────────
assert core.accent_for("welfare") == core.ACCENTS[1]
assert core.accent_for("events") == core.ACCENTS[4]
ok("a brief's department colour comes from core.accent_for, not from the style")

print(f"\nALL {N} ASSERTIONS PASSED")

# ── schema (added after two independent judges hit the same six ambiguities) ─
assert set(sb.KINDS) == {"poster", "sheet", "mockup", "asset", "carousel"}
ok("the kind enum includes `asset` — a vocabulary reference is not a poster")
assert "mockup" in sb.KIND_TIEBREAK and "discard" in sb.KIND_TIEBREAK.lower()
ok("sheet-vs-mockup has an explicit tie-break (the frame gets discarded)")
assert "VISUAL FORM" in sb.HERO_RULES and "co-equal" in sb.HERO_RULES.lower()
ok("hero has tie-breaks for co-equal elements and content-vs-form")
assert "not the one closest to the reference" in sb.CANVAS_RULE
ok("canvas is specified as fit-for-purpose, NOT nearest aspect")
assert "ONE extractable move" in sb.RECIPE_RULE
ok("recipe scope matches the recreation protocol's one-mechanism ruling")

assert sb.validate(verbose=False) == []
ok("every judged entry currently conforms to the schema")

# an asset must never be handed to "design something"
for s_ in range(40):
    assert sb.pick(seed=s_).get("kind") != "asset"
ok("pick() never returns an `asset` — it has no layout to build")
assert sb.pick(kind="asset", seed=1).get("kind") == "asset"
ok("...but asking for one explicitly still works")

print(f"\nALL {N} ASSERTIONS PASSED")

# ── cross_check: catch a judgment written about the WRONG IMAGE ─────────────
# A judging agent self-reported mis-attributing slug-to-image while reading 5 images
# per call. A confident recipe for the wrong picture passes every schema check there
# is, so the only defence is comparing the judgment against the MEASURED pixels.
assert sb.cross_check(verbose=False) == []
ok("no judgment in the bank contradicts its measured ground")

import copy as _copy
_orig = _copy.deepcopy(sb._load())
try:
    _b = sb._load()
    _t = [k for k, v in _b["styles"].items()
          if v.get("kind") == "poster" and v["measured"]["ground"] == "paper"][0]
    _b["styles"][_t]["recipe"] = "Dark ground. A giant headline in paper fills the frame."
    sb._save(_b)
    assert any(h[0] == _t for h in sb.cross_check(verbose=False))
    ok("an injected wrong-image recipe IS caught")
finally:
    sb._save(_orig)
assert sb.cross_check(verbose=False) == []
ok("...and the bank restores cleanly afterwards")

# the classifier bug cross_check exposed: chroma must be tested BEFORE luminance
assert sb._classify_ground([240, 0, 0]) == "saturated"
assert sb._classify_ground([24, 48, 168]) == "saturated"
ok("pure red and saturated blue classify as saturated, not dark (chroma before luminance)")
assert sb._classify_ground([40, 40, 44]) == "dark"
ok("...while a low-chroma near-black is still dark")

# soft boundaries must not cry wolf
assert not any(h[0] == "77e7bb34144e08" for h in sb.cross_check(verbose=False))
ok("a deep maroon is both saturated AND dark — that pair is not flagged")

assert "ONE IMAGE PER READ CALL" in sb.JUDGING_PROCESS
ok("the one-image-per-call rule is encoded in the module, not just in a prompt")

print(f"\nALL {N} ASSERTIONS PASSED")
