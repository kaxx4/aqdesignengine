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

# (no banner here — a mid-file "ALL PASSED" print made a FAILED run look passed)

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

assert sb.validate(verbose=False, advisory=False) == []
ok("every judged entry currently conforms to the HARD schema (enums, non-empty recipe)")

# an asset must never be handed to "design something"
for s_ in range(40):
    assert sb.pick(seed=s_).get("kind") != "asset"
ok("pick() never returns an `asset` — it has no layout to build")
assert sb.pick(kind="asset", seed=1).get("kind") == "asset"
ok("...but asking for one explicitly still works")

# (no banner here — a mid-file "ALL PASSED" print made a FAILED run look passed)

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

# ── THE CROSS-ASPECT BRIEF (session 10f) ────────────────────────────────────
# `measured.coverage/centroid/content_bbox` are fractions OF THE REFERENCE IMAGE.
# brief() printed them under "build to THESE numbers" even when the style was judged
# onto a canvas in a completely different shape — 17 of 74 entries, worst case a
# 0.667 portrait judged `linkedin` at 1.911 (a 2.9x swing). The builder was handed
# one frame's proportions as instructions for another, with nothing saying so.

assert sb.CANVAS_ASPECT["feed"] == 1080 / 1350 and sb.CANVAS_ASPECT["linkedin"] == 1200 / 628
ok("canvas aspects are derived from the real pixel sizes, not typed as decimals")

_portrait = {"slug": "x", "canvas": "linkedin", "measured": {"aspect": 0.667}}
sh = sb.canvas_shift(_portrait)
assert sh and sh["direction"] == "wider" and sh["ratio"] > 2.5
ok("a 0.667 portrait judged linkedin is reported as a 2.9x WIDER shift (4939a628d6deb2)")

_same = {"slug": "x", "canvas": "feed", "measured": {"aspect": 0.80}}
assert sb.canvas_shift(_same) is None
ok("a feed-aspect reference judged feed reports no shift — the check does not cry wolf")

_near = {"slug": "x", "canvas": "feed", "measured": {"aspect": 0.95}}
assert sb.canvas_shift(_near) is None, "19% is inside tolerance; the numbers still transfer"
ok("a 19% aspect gap stays inside tolerance — proportions transfer, no warning")

# the caller's canvas WINS over the style's own — a relaxed draw can hand you a
# style judged for another frame entirely, and design.py passes --canvas through.
assert sb.canvas_shift(_same, canvas="linkedin") is not None
ok("an explicitly requested canvas overrides the style's judged one")

_b = sb.brief(_portrait, "a subject")
assert "RE-PROPORTION" in _b and "DOES NOT TRANSFER" in _b
ok("the brief for a cross-aspect style carries an explicit RE-PROPORTION block")
assert "build to THESE numbers" not in _b
ok("...and STOPS saying 'build to THESE numbers', which was the wrong instruction")

_ok_brief = sb.brief(_same, "a subject")
assert "build to THESE numbers" in _ok_brief and "RE-PROPORTION" not in _ok_brief
ok("a same-frame style still says 'build to THESE numbers' — guidance is not blanket-weakened")

# CANVAS_RULE told judges to write the compression into the recipe. Nothing checked it,
# so a majority of the cross-aspect entries never mention the frame. Now it is reported.
# Assert the CHECK, not the current contents of the bank. An earlier draft of this
# test asserted that validate() currently returns flags — which passed only while the
# bank was still broken, and failed the moment the recipes were repaired. That is the
# same "encode the bug, not the rule" mistake session 10e found pinned in
# test_layout_rules.py. What must hold is: a cross-aspect recipe that ignores its own
# frame IS flagged, and one that addresses it is NOT.
import copy as _cp2
_before = _cp2.deepcopy(sb._load())
try:
    _b2 = sb._load()
    _tgt = next(k for k, v in _b2["styles"].items()
                if v.get("kind") == "poster" and v["measured"]["aspect"] > 1.15)
    _b2["styles"][_tgt]["canvas"] = "story"          # 0.562 — a real shift from >1.15
    _b2["styles"][_tgt]["recipe"] = "Paper ground. One big headline. Restraint: nothing else."
    sb._save(_b2)
    _flags = [x for x in sb.validate(verbose=False) if x[1] == "recipe/canvas"]
    assert any(s == _tgt for s, _, _ in _flags), _flags
    ok("a cross-aspect recipe that never mentions its frame IS flagged")

    _b2 = sb._load()
    _b2["styles"][_tgt]["recipe"] += (" Re-proportioned for the taller frame: the row "
                                      "becomes a stack of three, bleeding off both sides.")
    sb._save(_b2)
    assert not [x for x in sb.validate(verbose=False)
                if x[1] == "recipe/canvas" and x[0] == _tgt]
    ok("...and the same entry clears once the recipe says how it re-proportions")
finally:
    sb._save(_before)

assert sb.validate(verbose=False) == []
ok("the bank as it stands is clean on BOTH the hard schema and the advisories")

# canvas_shift must stay silent for kinds whose measured aspect is not the design's
_mockup_shift = {"slug": "m", "kind": "mockup", "canvas": "story",
                 "measured": {"aspect": 1.018}}
assert sb.canvas_shift(_mockup_shift) is None
ok("canvas_shift says nothing about a mockup — 1.018 is the PHOTO, not the design")
assert sb.canvas_shift(dict(_mockup_shift, kind="poster")) is not None
ok("...while the identical numbers on a poster do report a shift")

# ── WHAT THE MEASURED NUMBERS ACTUALLY DESCRIBE (session 10f) ───────────────
# "build to THESE numbers" was honest for only 25 of the 74 entries. For a `sheet`
# the fractions describe a page of twelve artefacts; for a `mockup` they describe a
# photograph of a phone on a table; for the tbh website screenshot they describe a
# whole page scroll. All three were being printed as build targets.

assert set(sb.MEASURED_SCOPE) == {"sheet", "mockup", "asset", "carousel"}
ok("every non-poster kind declares what its measured numbers really describe")
assert "poster" not in sb.MEASURED_SCOPE
ok("...and `poster` does not — a single design in its own frame IS the target")

_mock = {"slug": "m", "kind": "mockup", "canvas": "feed",
         "measured": {"aspect": 0.80, "coverage": 0.55}}
_t = sb.brief(_mock, "s")
assert "THE PHOTOGRAPH" in _t and "compare.crop" in _t
ok("a mockup's brief says the numbers measure the photo, and names compare.crop")
assert "build to THESE numbers" not in _t and "build to these" not in _t
ok("...and never calls a backdrop's coverage a build target, even at a matching aspect")

assert "WHOLE SHEET" in sb.brief(dict(_mock, kind="sheet"), "s")
ok("a sheet's brief says the numbers measure the sheet, not one artefact")

_poster = dict(_mock, kind="poster")
assert "build to THESE numbers" in sb.brief(_poster, "s")
ok("a same-frame poster keeps the direct instruction — the warning is targeted, not blanket")

_n = sum(1 for v in S.values() if v.get("kind") == "poster" and sb.canvas_shift(v) is None)
assert 0 < _n < len(S), _n
ok(f"{_n} of {len(S)} bank entries are same-frame posters whose numbers ARE targets")

# brief() must not require pick()'s injected slug
_noslug = {k: v for k, v in _poster.items() if k != "slug"}
_noslug["file"] = "abcdef1234567890.jpg"
assert "abcdef12345678" in sb.brief(_noslug, "s")
ok("brief() works on a style read straight out of the bank (no injected slug)")

# ── THE ACCEPTANCE LIST MUST BE VISIBLE, AND MUST BE THE REAL ONE ───────────
# A judging agent reported `_REPROP_WORDS` as a hidden acceptance test: it could be
# failed by a recipe that plainly DID address its frame, with no way to know why.
# Publishing a hand-retyped copy would only swap an invisible contract for one free
# to drift — and the first draft of that fix drifted immediately ("square" in the
# prose, "squar" in the code). So the rule PRINTS the tuple.
_printed = sb.RECIPE_RULE
for _w in sb._REPROP_WORDS:
    assert _w in _printed, _w
ok("every enforced re-proportion word appears in the published RECIPE_RULE")
assert "hidden acceptance test" in _printed
ok("...and the rule says plainly that the list is part of the contract")
assert "DOES NOT COUNT AGAINST" in _printed
ok("the sentence budget no longer competes with the re-proportioning requirement")

print(f"\nALL {N} ASSERTIONS PASSED")
