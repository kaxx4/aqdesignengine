"""AQ ENGINE — stylebank: every reference image as a usable STYLE, not just a target.

WHY THIS EXISTS
`training_samples/reference_posters/` is 74 images the engine has been trained AGAINST
— one at a time, as recreation targets. But each of those images is also a STYLE: a
ground, a density, a hero type, a mechanism. Once a reference has been read, that
knowledge should be reachable when someone just says "design something", instead of
being locked inside a one-off recreation script and a paragraph in RECREATION_AUDIT.md.

THE SPLIT THAT MAKES THIS HONEST
  * MEASURED fields (coverage, ground, aspect, palette, bbox) come from the pixels, via
    compare.py. They are recomputed by `python engine/stylebank.py measure` and are
    never hand-typed — the session-10c lesson was that eyeballing a proportion produces
    a confident wrong number.
  * JUDGED fields (mechanism, hero, tags, recipe) need eyes. They are filled in by
    looking at the image and are marked `judged: false` until someone actually has.

`pick()` is the "design something" entry point: an EDUCATED random draw, not a uniform
one. It filters by whatever the caller knows (department, canvas, ground) and then
weights what is left, so the result is always a plausible fit rather than a lottery.
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REFDIR = os.path.join(ROOT, "training_samples", "reference_posters")
BANK = os.path.join(ROOT, "brain", "STYLE_BANK.json")


def _load():
    if not os.path.exists(BANK):
        return {"version": 1, "styles": {}}
    with open(BANK, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(b):
    os.makedirs(os.path.dirname(BANK), exist_ok=True)
    with open(BANK, "w", encoding="utf-8") as f:
        json.dump(b, f, indent=2, ensure_ascii=False)


def _compare():
    import importlib.util
    s = importlib.util.spec_from_file_location("compare", os.path.join(HERE, "compare.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


# ── ground classification, from the pixels ──────────────────────────────────
def _classify_ground(rgb):
    """Name the page ground from its measured colour. Deliberately coarse — the only
    distinction a builder acts on is dark / paper / saturated."""
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # CHROMA IS TESTED FIRST, and that ordering is the whole correctness of this
    # function. Luminance-first called pure red [240,0,0] "dark" (its luminance is 51,
    # under the 70 threshold) and saturated blue [24,48,168] "dark" too. Both are
    # obviously saturated grounds to any eye. The bug was found by cross_check()
    # flagging two judges' recipes as contradicting the measurement — the recipes were
    # right and the classifier was wrong.
    if mx - mn > 60:
        return "saturated"
    if lum < 70:
        return "dark"
    if lum > 200:
        return "paper"
    return "paper" if lum > 150 else "mid"


def measure(verbose=True):
    """Recompute every MEASURED field for every reference. Idempotent; never touches
    judged fields."""
    import numpy as np
    from PIL import Image
    c = _compare()
    bank = _load()
    styles = bank.setdefault("styles", {})
    files = sorted(f for f in os.listdir(REFDIR)
                   if f.lower().endswith((".jpg", ".jpeg", ".png")))
    for fn in files:
        slug = os.path.splitext(fn)[0][:14]
        path = os.path.join(REFDIR, fn)
        im = c._load(path)
        a = c._arrays(im)
        if isinstance(a, tuple):
            a = a[0]
        m = c.content_mask(a, im=im)
        ys, xs = np.nonzero(m)
        H_, W_ = m.shape
        src = Image.open(path)
        bg = c._bg_color(a)
        e = styles.setdefault(slug, {})
        e["file"] = fn
        e["measured"] = {
            "aspect": round(src.size[0] / src.size[1], 3),
            "coverage": round(float(m.mean()), 3),
            "ground_rgb": [int(v) for v in bg],
            "ground": _classify_ground([int(v) for v in bg]),
            "content_bbox": ([round(float(xs.min()) / W_, 3), round(float(ys.min()) / H_, 3),
                              round(float(xs.max()) / W_, 3), round(float(ys.max()) / H_, 3)]
                             if len(xs) else None),
            "centroid": ([round(float(xs.mean()) / W_, 3), round(float(ys.mean()) / H_, 3)]
                         if len(xs) else None),
            "palette": [c._name_color(p[0]) for p in c._palette(a, m, k=5)],
        }
        e.setdefault("judged", False)
        e.setdefault("kind", None)        # poster | mockup | sheet | carousel
        e.setdefault("mechanism", None)   # the ONE reusable move
        e.setdefault("hero", None)        # type | number | photo | shape | pile | grid
        e.setdefault("tags", [])
        e.setdefault("recipe", None)      # one sentence a builder can act on
        e.setdefault("canvas", "feed")
        e.setdefault("depts", [])         # which AQ departments this style suits
    bank["version"] = 1
    _save(bank)
    if verbose:
        n = len(styles)
        judged = sum(1 for v in styles.values() if v.get("judged"))
        print(f"measured {n} styles -> {BANK}")
        print(f"  judged: {judged}/{n}  (run `stylebank.py todo` for what still needs eyes)")
    return bank


# ── the picker ──────────────────────────────────────────────────────────────
def pick(dept=None, canvas=None, ground=None, hero=None, kind="poster",
         judged_only=True, seed=None, n=1):
    """EDUCATED random draw of a style to design in.

    Every filter is a NARROWING, applied only when given, and every one of them falls
    back rather than returning nothing: an over-specified request that matches zero
    styles would otherwise make "design something" fail, which is the one outcome this
    entry point must never produce. Each relaxation is reported in `relaxed`.
    """
    bank = _load()
    styles = [dict(slug=k, **v) for k, v in bank.get("styles", {}).items()]
    if not styles:
        raise RuntimeError("style bank is empty — run `python engine/stylebank.py measure`")

    rng = random.Random(seed)
    relaxed = []

    def _narrow(pool, pred, label):
        got = [s for s in pool if pred(s)]
        if got:
            return got
        relaxed.append(label)
        return pool

    pool = styles
    # An `asset` reference is a drawing VOCABULARY (a sticker sheet, an icon set) with
    # no layout. Handing one to "design something" would produce a page of loose
    # objects and no composition, so it is never a default target — only reachable by
    # asking for it explicitly.
    if kind != "asset":
        pool = [s for s in pool if s.get("kind") != "asset"] or pool
    if judged_only:
        pool = _narrow(pool, lambda s: s.get("judged"), "judged_only")
    if kind:
        pool = _narrow(pool, lambda s: s.get("kind") == kind, f"kind={kind}")
    if canvas:
        pool = _narrow(pool, lambda s: s.get("canvas") == canvas, f"canvas={canvas}")
    if ground:
        pool = _narrow(pool, lambda s: s["measured"]["ground"] == ground, f"ground={ground}")
    if hero:
        pool = _narrow(pool, lambda s: s.get("hero") == hero, f"hero={hero}")
    if dept:
        pool = _narrow(pool, lambda s: dept in (s.get("depts") or []), f"dept={dept}")

    # Weighting, so this is educated rather than uniform:
    #   * a style someone has actually LOOKED at outranks an unjudged one
    #   * a style with a written recipe outranks one without
    #   * mid-density references are safer defaults than the extremes
    def _w(s):
        w = 1.0
        if s.get("judged"):  w *= 3.0
        if s.get("recipe"):  w *= 2.0
        cov = (s.get("measured") or {}).get("coverage") or 0.3
        w *= 1.0 if 0.18 <= cov <= 0.62 else 0.55
        return w

    chosen = []
    avail = list(pool)
    for _ in range(min(n, len(avail))):
        ws = [_w(s) for s in avail]
        s = rng.choices(avail, weights=ws, k=1)[0]
        avail.remove(s)
        s = dict(s); s["relaxed"] = relaxed
        chosen.append(s)
    return chosen[0] if n == 1 else chosen


def brief(style, subject):
    """Turn a chosen style + a subject line into an instruction a builder can act on."""
    m = style.get("measured", {})
    lines = [
        f"STYLE  {style['slug']}  ({style.get('file')})",
        f"  mechanism : {style.get('mechanism') or '(unjudged — open the image)'}",
        f"  hero      : {style.get('hero') or '?'}      kind: {style.get('kind') or '?'}",
        f"  ground    : {m.get('ground')}  {m.get('ground_rgb')}",
        f"  coverage  : {m.get('coverage')}   centroid {m.get('centroid')}",
        f"  palette   : {', '.join(m.get('palette') or [])}",
        f"  canvas    : {style.get('canvas')}",
        f"  recipe    : {style.get('recipe') or '(none written yet)'}",
        "",
        f"SUBJECT  {subject}",
        "",
        "BUILD IT:",
        f"  1. open the reference:  training_samples/reference_posters/{style.get('file')}",
        f"  2. measure it:          compare.geometry(path)   <- build to THESE numbers",
        "  3. bespoke script from core/build/layout/shapes/tex — never engine.py ARCHETYPES",
        "  4. render, then LOOK at the PNG (CLAUDE.md section 3). The score is a proxy.",
    ]
    if style.get("relaxed"):
        lines.insert(1, f"  (filters relaxed to find a match: {', '.join(style['relaxed'])})")
    return "\n".join(lines)


JUDGE_DIR = os.path.join(ROOT, "brain", "style_judgments")

JUDGED_FIELDS = ("kind", "hero", "canvas", "mechanism", "tags", "depts", "recipe")


# ════════════════════════════════════════════════════════════════════════════
# THE JUDGING SCHEMA — lives here, not in whatever prompt asked for the work
# ════════════════════════════════════════════════════════════════════════════
# Two independent judges, given the same instructions, hit the SAME six ambiguities.
# That is a spec defect, not judge error. Each resolution below names the case that
# exposed it, so the next reader can tell a rule from a preference.
#
# It lives in the module because a schema that only exists inside a task prompt gets
# re-invented, slightly differently, every time someone writes a new prompt.
# Read it with:  python engine/stylebank.py schema

KINDS = {
    "poster":   "ONE composition on a flat ground. The layout can be copied directly.",
    "sheet":    "Several finished artefacts shown together (cards, covers, stickers). "
                "Copy the SYSTEM that unites them, not any one item.",
    "mockup":   "The design is shown ON something — a device, printed stock, or a real "
                "scene. Extract ONE screen or mechanism; never copy the frame, the "
                "bezel, the basket or the wood. "
                "(Widened from 'phones/devices/browser chrome': a poster photographed "
                "in a shopping basket and business cards on a wood backdrop are the "
                "same problem — the design is wearing a costume. Both judges hit this.)",
    "asset":    "A VOCABULARY reference with no layout to copy: a sticker sheet, an "
                "icon set, a single illustrated object. Its recipe should describe the "
                "drawing language, and should say plainly that it is not a template. "
                "(Added: two judges both forced such references into poster/sheet and "
                "flagged that neither fit.)",
    "carousel": "A sequence of slides.",
}

# `sheet` and `mockup` BOTH describe business cards photographed on a wood backdrop.
# The tie-break is what the judgment CHANGES for a builder: mockup means "the frame is
# not part of the design, throw it away". That instruction matters more than the count
# of artefacts, so mockup wins whenever a setting has to be discarded.
KIND_TIEBREAK = "If a setting/frame must be discarded to use it, it is a `mockup`, "                 "however many artefacts are in the shot."

HEROES = {
    "type": "words are the mass", "number": "a figure is the mass",
    "photo": "a photograph is the mass", "shape": "a drawn form is the mass",
    "pile": "many small objects read as one mass", "grid": "a repeating structure is the mass",
}

# The two hero tie-breaks judges asked for, both from real cases:
HERO_RULES = """
  * TWO CO-EQUAL ELEMENTS (a giant headline over an equally giant photo). Pick what a
    BUILDER lays down first — the element the other is positioned against. If the photo
    is a full-bleed field and the type sits on it, hero is `photo`.
  * CONTENT-TYPE vs VISUAL-FORM DISAGREE (letters spelled out of 3D keycap objects).
    Pick the VISUAL FORM (`pile`), because the form is what gets rebuilt. The words are
    swappable content; the object-pile is the move.
"""

# `canvas` is FIT FOR PURPOSE, not nearest aspect. Judges defaulted to aspect distance,
# which is a different question and can disagree with the right answer.
CANVAS_RULE = """
  Choose the AQ canvas this MECHANISM works on, not the one closest to the reference's
  aspect ratio. A 2:1 landscape reference is still `linkedin` — AQ has nothing wider —
  and the recipe should then say how the mechanism compresses to 1.91:1.
  feed 1080x1350 | story 1080x1920 | square 1080x1080 | linkedin 1200x628 | li_square 1200x1200
"""

RECIPE_RULE = """
  3-5 sentences of INSTRUCTIONS, not observations. Ground, proportions, what goes where,
  and what the RESTRAINT is (the thing you must NOT add).
  SCOPE: describe ONE extractable move, matching the recreation protocol's standing
  ruling for multi-slide references (CLAUDE.md section 5). A moodboard of eight unrelated
  artefacts gets the ONE mechanism a builder would copy, not a tour of all eight.
"""

# HOW TO JUDGE, not just what to write. A judging agent self-reported this and it is
# the single most useful process finding of the exercise:
JUDGING_PROCESS = """
  ONE IMAGE PER READ CALL. Reading five images in a batch and reasoning about them
  together causes slug-to-image MIS-ATTRIBUTION — a nightclub poster filed under the
  wrong slug, two sticker sheets swapped. It is slower per image and far cheaper
  overall, because the alternative is re-verifying all of them after you notice.
  A confidently-written recipe for the WRONG picture passes every schema check there
  is; only cross_check() catches it, and only when the grounds happen to disagree.

  A UI/website capture is a `mockup` even with no browser chrome — the content card IS
  the device. Judges defaulted these to `poster` and flagged the gap.
"""

DEPTS = ("welfare", "events", "labs", "ops", "content")
# An empty depts list is the HONEST answer for a generic stock reference — a nightclub
# flyer or a K-pop fan event has no natural AQ department. Judges reported assigning
# soft guesses ("events for anything flyer-shaped") and flagged them as lower
# confidence than the rest of the entry. Prefer [] over a stretch.
# An empty depts list is a valid, honest answer. A pure illustration reference with no
# programmatic content should not have a department invented for it.


def schema():
    print(__doc__.strip() + "\n")
    print("kind:")
    print(f"  TIE-BREAK  {KIND_TIEBREAK}")
    for k, v in KINDS.items():
        print(f"  {k:9} {v}")
    print("\nhero:")
    for k, v in HEROES.items():
        print(f"  {k:9} {v}")
    print("  tie-breaks:" + HERO_RULES.rstrip())
    print("\ncanvas:" + CANVAS_RULE.rstrip())
    print("\nrecipe:" + RECIPE_RULE.rstrip())
    print(f"\ndepts: 0-3 of {DEPTS}  (empty is valid and honest)")
    print("\ntags: 4-6 short kebab-case")


GROUND_WORDS = {
    "dark":      ("dark ground", "black ground", "ink ground", "on dark", "dark field"),
    "paper":     ("paper ground", "cream ground", "white ground", "pale ground", "light ground"),
    "saturated": ("saturated ground", "colour ground", "color ground", "accent ground"),
}


def cross_check(verbose=True):
    """Catch a judgment that contradicts what the pixels say — i.e. a judgment written
    about the WRONG IMAGE.

    THE FAILURE MODE THIS CATCHES (self-reported by a judging agent, session 10e). It
    read images five per tool call and reasoned about them together, and mis-attributed
    several slug-to-image pairings — a nightclub poster filed under the wrong slug, two
    sticker sheets swapped. It caught the problem itself by spot-checking, re-verified
    all twenty individually and flagged it. But nothing in the system would have caught
    it otherwise: a confidently-written recipe for the wrong picture passes every schema
    check there is.

    The bank already holds the answer. Ground is MEASURED from the pixels, and a recipe
    almost always states the ground in its first sentence. When those two disagree, the
    judgment is about a different image. Cheap, and it needs no second look.

    Returns [(slug, measured_ground, claimed_ground)]. Empty == no contradictions.
    """
    bank = _load()
    out = []
    for slug, v in bank.get("styles", {}).items():
        if not v.get("judged"):
            continue
        # A MOCKUP's measured ground is the BACKDROP it was photographed on, not the
        # ground of the design inside it — a phone on a yellow table measures yellow
        # while its screen, which is what the recipe describes, is black. Both are
        # correct about different things, so there is nothing to cross-check.
        if v.get("kind") == "mockup":
            continue
        text = ((v.get("recipe") or "") + " " + " ".join(v.get("tags") or [])).lower()
        measured = (v.get("measured") or {}).get("ground")
        claimed = None
        for g, words in GROUND_WORDS.items():
            if any(w in text for w in words):
                claimed = g
                break
        if claimed and measured and claimed != measured:
            # Soft boundaries that are NOT contradictions:
            #   paper vs saturated — a pale tint honestly reads as either.
            #   dark vs saturated when the colour is BOTH — a deep maroon [96,24,0] is
            #     a saturated hue at luminance 26. "Dark ground" and "saturated ground"
            #     are both true of it, so flagging that pair would cry wolf on every
            #     deep brand colour in the corpus.
            rgb = (v.get("measured") or {}).get("ground_rgb") or [0, 0, 0]
            lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
            pair = {claimed, measured}
            if pair == {"dark", "saturated"} and lum < 90:
                continue
            if "dark" in pair:
                out.append((slug, measured, claimed))
    if verbose:
        if out:
            print(f"{len(out)} judgment(s) contradict the measured ground "
                  f"— likely written about the WRONG IMAGE:")
            for slug, m, c in out:
                print(f"  {slug}: pixels say {m}, recipe says {c}")
        else:
            print("no judgment contradicts its measured ground")
    return out


def validate(verbose=True):
    """Report judged entries that fall outside the schema. Never edits anything —
    a judgment made under an older spec is data, not a bug to silently overwrite."""
    bank = _load()
    bad = []
    for slug, v in bank.get("styles", {}).items():
        if not v.get("judged"):
            continue
        if v.get("kind") not in KINDS:
            bad.append((slug, "kind", v.get("kind")))
        if v.get("hero") not in HEROES:
            bad.append((slug, "hero", v.get("hero")))
        for d in (v.get("depts") or []):
            if d not in DEPTS:
                bad.append((slug, "dept", d))
        if not (v.get("recipe") or "").strip():
            bad.append((slug, "recipe", "empty"))
        n = len(v.get("tags") or [])
        if not (3 <= n <= 8):
            bad.append((slug, "tags", f"{n} tags"))
    if verbose:
        if bad:
            print(f"{len(bad)} schema issues:")
            for slug, field, val in bad:
                print(f"  {slug}  {field}={val!r}")
        else:
            print("all judged entries conform to the schema")
    return bad


def merge(verbose=True):
    """Fold every drop-file in brain/style_judgments/ into the bank.

    WHY DROP-FILES AND NOT DIRECT WRITES. Judging 74 references is naturally parallel
    work — several agents, twenty images each. Pointing all of them at STYLE_BANK.json
    means concurrent read-modify-write on one file: the last writer wins and the others'
    work vanishes silently, which is the worst possible failure mode because nothing
    errors. Each judge writes its OWN file instead, and this folds them in afterwards.

    A drop-file is `{"<slug>": {kind, hero, canvas, mechanism, tags, depts, recipe}}`.
    Only the judged fields are taken; measured fields are never overwritten from a
    drop-file, because those come from the pixels and a judge has no business editing
    them.
    """
    bank = _load()
    styles = bank.setdefault("styles", {})
    if not os.path.isdir(JUDGE_DIR):
        if verbose:
            print(f"no drop-files at {JUDGE_DIR}")
        return bank
    taken, skipped, unknown = 0, [], []
    for fn in sorted(os.listdir(JUDGE_DIR)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(JUDGE_DIR, fn), "r", encoding="utf-8") as f:
            drop = json.load(f)
        for slug, fields in drop.items():
            if slug not in styles:
                unknown.append((fn, slug)); continue
            clean = {k: v for k, v in fields.items() if k in JUDGED_FIELDS}
            if not clean.get("mechanism") or not clean.get("recipe"):
                skipped.append((fn, slug)); continue
            styles[slug].update(clean)
            styles[slug]["judged"] = True
            taken += 1
    _save(bank)
    if verbose:
        n = len(styles); j = sum(1 for v in styles.values() if v.get("judged"))
        print(f"merged {taken} judgments -> {j}/{n} judged")
        for fn, slug in skipped:
            print(f"  SKIPPED {slug} from {fn}: no mechanism/recipe (a judgment "
                  f"without a recipe is not usable)")
        for fn, slug in unknown:
            print(f"  UNKNOWN slug {slug} in {fn}")
    return bank


def todo():
    bank = _load()
    out = [k for k, v in bank.get("styles", {}).items() if not v.get("judged")]
    print(f"{len(out)} styles still need eyes:")
    for k in out:
        print(f"  {k}  {bank['styles'][k]['file']}")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "measure"
    if cmd == "measure":
        measure()
    elif cmd == "schema":
        schema()
    elif cmd == "crosscheck":
        cross_check()
    elif cmd == "validate":
        validate()
    elif cmd == "merge":
        merge()
    elif cmd == "todo":
        todo()
    elif cmd == "pick":
        kw = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
        seed = int(kw.pop("seed")) if "seed" in kw else None
        print(brief(pick(seed=seed, **kw), kw.pop("subject", "(no subject given)")))
    else:
        print(__doc__)
