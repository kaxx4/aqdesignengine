"""
Generalized composition decision-layers, usable by ANY archetype/one-off build.
Not tied to a single sample or archetype — these are choices the engine can make
on every generation, widening the decision space instead of hardcoding one look.
"""
import random, re

def pick_fill_mode(rng=None):
    """Badge/sticker fill: solid dominates real reference posters. Translucent/outline
    is a rare accent (<=1 per piece), never the default treatment."""
    rng = rng or random
    return rng.choices(["solid", "solid", "solid", "outline", "translucent"], k=1)[0]

def cluster_positions(n, cx, cy, min_r, max_r, overlap_frac=0.35, rng=None):
    """
    Place n badges as an OVERLAPPING PILE around (cx,cy) — walk outward along a
    loose spiral, each new badge's center placed close enough to the previous
    that their radii guarantee real overlap (overlap_frac of the sum of radii).
    Real sticker-collage references clip/overlap; isolated even spacing reads
    as a "grid of badges", not a pile — this is the fix for that.
    Returns list of (x, y, r) — x,y is the CENTER of each circle (diameter 2r).
    """
    import math
    rng = rng or random
    out = []
    px, py, pr = cx, cy, 0
    for i in range(n):
        r = rng.uniform(min_r, max_r)
        if i == 0:
            x, y = cx, cy
        else:
            dist = (pr + r) * (1 - overlap_frac)
            ang = rng.uniform(0, 2 * math.pi)
            x = px + dist * math.cos(ang)
            y = py + dist * math.sin(ang)
        out.append((x, y, r))
        px, py, pr = x, y, r
    return out

def quadrant_fill_check(W, H, elements, min_frac=0.55):
    """
    LOCAL overlap (one badge pile, one photo stack) must not be paid for by
    starving the REST of the canvas — that's the v2/v3 bespoke_87525f70 regression:
    cramming everything into one corner to get an overlapping cluster raised
    dom_cov (more empty cream) instead of lowering it.
    elements: list of (x, y, w, h) bounding boxes already placed (badges, doodles,
    type blocks, chips — anything with real visual weight).
    Returns list of the quadrants (of 4) that are under-filled, so the caller can
    add a mid-layer object/gap-filler there before finalizing.
    Quadrant is "filled" if elements covering it sum to >= min_frac of a light
    presence check (crude bbox-overlap area, not pixel-exact — good enough to
    catch "nothing was placed here at all").
    """
    hw, hh = W / 2, H / 2
    quads = [(0, 0, hw, hh), (hw, 0, W, hh), (0, hh, hw, H), (hw, hh, W, H)]
    under = []
    for qi, (qx0, qy0, qx1, qy1) in enumerate(quads):
        qarea = (qx1 - qx0) * (qy1 - qy0)
        covered = 0.0
        for (x, y, w, h) in elements:
            ox = max(0, min(qx1, x + w) - max(qx0, x))
            oy = max(0, min(qy1, y + h) - max(qy0, y))
            covered += ox * oy
        if covered / qarea < (1 - min_frac):
            under.append(qi)
    return under

def bounds_check(W, H, elements):
    """
    Canvas is 1080x1350 for feed (NOT ~1700+) — two separate bespoke recreations
    silently lost elements to `overflow:hidden` by assuming a taller canvas.
    Call this on every (x,y,w,h) element list right before rendering; it returns
    a list of (index, x,y,w,h) that clip off-canvas so the bug is caught before
    a render, not discovered after by comparing a blank patch to the reference.
    """
    out = []
    for i, (x, y, w, h) in enumerate(elements):
        if x < 0 or y < 0 or x + w > W or y + h > H:
            out.append((i, x, y, w, h))
    return out


# ---------------------------------------------------------------------------
# The three checks below encode failure classes that recurred across the whole
# session-8 revisit pass. The bespoke one-off scripts BYPASS audit.py's DOM gate
# (that gate only sees `.measure` elements); they hand-maintain (x,y,w,h) tuple
# lists and call bounds_check/quadrant_fill_check on those. So the equivalent
# guards have to live HERE, in the tuple-list world those scripts actually use.
# Per CLAUDE.md: convert each caught visual flaw into an encoded rule.
# ---------------------------------------------------------------------------

def _norm_ignore(ignore_pairs):
    """Accept any sane spelling of an ignore-list and say so when one is nonsense.

    THE BUG THIS FIXES. The contract was `frozenset({a, b})` per pair, documented only
    here — 800 lines from `preflight`, which is where a caller actually looks. Passing
    ("a","b") tuples, the obvious guess, matched nothing: every ignored collision kept
    reporting and NOTHING said the ignore-list was a no-op. It cost a full debug cycle
    to find by reading source. Now tuples, lists and sets all work, and anything that
    cannot be a pair is reported instead of silently dropped.
    """
    out, bad = set(), []
    for item in (ignore_pairs or ()):
        if isinstance(item, (frozenset, set, tuple, list)) and len(item) == 2:
            out.add(frozenset(item))
        else:
            bad.append(item)
    if bad:
        print(f"   [collision_check] IGNORED ENTRIES THAT ARE NOT PAIRS: {bad} "
              f"— expected two labels each, e.g. ('hero','badge')")
    return frozenset(out)


def collision_check(elements, min_overlap=12, ignore_pairs=frozenset()):
    """
    Pairwise bbox-overlap detector for the manual element list — the tuple-world
    twin of audit.py's DOM OVERLAP check. Catches the collision class that hit
    samples 26 (thumbsup over the 'volunteer' pill), 27 (badge 7 inside the paw),
    and 32 (sparkle over a speech bubble): a doodle/badge placed on top of text
    or another shape, invisible to bounds_check because nothing left the canvas.

    elements: list of (x,y,w,h) OR (label,x,y,w,h). Labels (when present) are
      echoed back so the caller knows WHICH two things collide.
    min_overlap: ignore <=Npx grazes (borders/intentional tucks); real coverage
      only. Matches audit.py's 12px threshold.
    ignore_pairs: set of frozenset({label_a,label_b}) the caller declares an
      intentional overlap (e.g. a chip tucked under a hero on purpose).

    Returns list of (a, b, ox, oy) for each real collision, a/b being the label
    or index. Empty list == no collisions (the pass condition).
    """
    norm = []
    for i, e in enumerate(elements):
        if len(e) == 5:
            lbl, x, y, w, h = e
        else:
            x, y, w, h = e; lbl = i
        norm.append((lbl, x, y, w, h))
    _ign = _norm_ignore(ignore_pairs)
    # An ignore pair naming a label that was never DECLARED is the loudest available
    # signal that the author built an element and forgot elements.append(). Seen in
    # out/session10f/c2_v3.png: the script whitelisted ("book","card") and
    # ("umbrella","card") while book, umbrella and a lemon star were all missing from
    # `elements` — so collision_check could not see them, preflight printed CLEAN, and
    # the star landed squarely on the words "SIGN-UPS OPEN NOW". The author had
    # clearly thought about those overlaps; they just never entered the gate's world.
    _known = {n[0] for n in norm}
    _ghosts = sorted({str(l) for pr in _ign for l in pr if l not in _known},
                     key=str)
    if _ghosts:
        print(f"   [collision_check] IGNORE PAIRS NAME UNDECLARED ELEMENTS: {_ghosts}"
              f" — these are invisible to every static check. Did you forget"
              f" elements.append() for them?")
    out = []
    for i in range(len(norm)):
        for j in range(i + 1, len(norm)):
            la, ax, ay, aw, ah = norm[i]
            lb, bx, by, bw, bh = norm[j]
            if frozenset({la, lb}) in _ign:
                continue
            ox = min(ax + aw, bx + bw) - max(ax, bx)
            oy = min(ay + ah, by + bh) - max(ay, by)
            if ox > min_overlap and oy > min_overlap:
                out.append((la, lb, ox, oy))
    return out


def cascade_peek_check(stack, min_peek_frac=0.06):
    """
    Repeated-card "deck" compositions (CLAUDE.md/VISUAL_DNA.md §7 repetition-as-composition:
    2022ebef4f's 3x duplicated card at decreasing scale + increasing rotation) have a specific,
    previously-uncaught failure mode: the back repeats are offset in the WRONG DIRECTION and end
    up fully covered by the front card instead of peeking out from behind it. Caught by eye in the
    2022ebef4ffad5 recreation (v3->v4, 2026-09-03): the smaller back cards were nested inside the
    front card's bounds by 88/44px while the frontmost card was ~720px wide, so their edges never
    crossed the front card's edge and the "cascade" rendered as a single flat card.

    stack: list of (x,y,w,h) for one cascade group, ordered BACK-TO-FRONT (index 0 is drawn first
    / furthest back, last index is drawn last / frontmost — matches the z-order convention used
    throughout the bespoke scripts).
    min_peek_frac: each back card must have at least this fraction of its OWN area not covered by
    the union of every card drawn after it (i.e. visibly poking out), or it reads as hidden.

    Returns list of (index, visible_frac) for cards that fail to peek. Empty list == pass.
    Rotation is intentionally ignored (checked on axis-aligned bboxes) — this is a cheap, zero
    false-positive-on-real-bugs check for the "offset too small / wrong sign" class, not a precise
    peek measurement; a rotated card that clears this check by a wide margin is fine.

    Coverage is computed by grid-sampling each card (not by summing pairwise overlap areas) —
    summing double-counts the region where two or more FRONT cards overlap each other on top of
    the card being tested, which made an early version of this check fail correctly-peeking real
    3-card decks. Sampling handles the union correctly with no extra bookkeeping.
    """
    out = []
    GRID = 12
    for i in range(len(stack) - 1):
        x, y, w, h = stack[i]
        if w <= 0 or h <= 0:
            continue
        front = stack[i + 1:]
        visible = 0
        total = 0
        for gx in range(GRID):
            for gy in range(GRID):
                px = x + (gx + 0.5) / GRID * w
                py = y + (gy + 0.5) / GRID * h
                total += 1
                if not any(fx <= px <= fx + fw and fy <= py <= fy + fh for fx, fy, fw, fh in front):
                    visible += 1
        visible_frac = visible / total
        if visible_frac < min_peek_frac:
            out.append((i, round(visible_frac, 3)))
    return out


def collision_nudge(elements, W, H, min_overlap=12, ignore_pairs=frozenset(),
                     max_iters=40, step=6, margin=8):
    """
    AUTO-REPOSITION pass for collision_check hits — the piece §12/§10 flagged as
    still manual ("detection done, reposition still manual"). Given the same
    element list collision_check consumes, push the SECOND element of each
    colliding pair directly away from the first along the vector between their
    centers, a `step`px at a time, re-checking after every nudge, until no pair
    collides or `max_iters` is exhausted. Later/smaller elements (badges,
    doodles, chips) move; earlier/larger ones (hero, background bands) are
    treated as anchors — matches how bespoke scripts append elements in
    z/placement order, hero first.

    Degenerate case (identical centers): nudge along a fixed diagonal so the
    push direction is never undefined.

    Stays within [margin, W-margin] / [margin, H-margin] — never pushes an
    element into an off-canvas position (that's bounds_check's job to catch,
    not this one's job to cause).

    Returns (new_elements, unresolved) — new_elements preserves the input's
    shape (plain or labeled tuples); unresolved is whatever collision_check
    still reports after max_iters, i.e. pairs too cramped to separate within
    the canvas (the caller should treat that as a real design problem, not
    auto-fix it further).
    """
    import math
    labeled = len(elements) > 0 and len(elements[0]) == 5
    cur = list(elements)

    def unpack(e):
        return (e[0], e[1], e[2], e[3], e[4]) if labeled else (None, e[0], e[1], e[2], e[3])

    def repack(lbl, x, y, w, h):
        return (lbl, x, y, w, h) if labeled else (x, y, w, h)

    for _ in range(max_iters):
        hits = collision_check(cur, min_overlap=min_overlap, ignore_pairs=ignore_pairs)
        if not hits:
            break
        la, lb, _, _ = hits[0]
        # map labels/indices back to positions in cur
        idx_a = idx_b = None
        for i, e in enumerate(cur):
            lbl = e[0] if labeled else i
            if lbl == la and idx_a is None:
                idx_a = i
            if lbl == lb and idx_b is None:
                idx_b = i
        if idx_a is None or idx_b is None:
            break
        j = max(idx_a, idx_b)  # move the later-placed element only
        i = idx_a if j == idx_b else idx_b
        _, ax, ay, aw, ah = unpack(cur[i])
        lbl_j, bx, by, bw, bh = unpack(cur[j])
        acx, acy = ax + aw / 2, ay + ah / 2
        bcx, bcy = bx + bw / 2, by + bh / 2
        dx, dy = bcx - acx, bcy - acy
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            dx, dy, dist = 1.0, 1.0, math.sqrt(2)
        ux, uy = dx / dist, dy / dist
        nx = min(max(bx + ux * step, margin), W - margin - bw)
        ny = min(max(by + uy * step, margin), H - margin - bh)
        cur[j] = repack(lbl_j, nx, ny, bw, bh)

    unresolved = collision_check(cur, min_overlap=min_overlap, ignore_pairs=ignore_pairs)
    return cur, unresolved


def _token_map(core):
    """Build {'--name': '#hex', ...} from core.ROOT's custom-property block, plus
    the ACCENTS list resolved by index so callers passing raw A[i] hex compare too."""
    m = {}
    if core is not None:
        for name, hx in re.findall(r'--([\w]+)\s*:\s*(#[0-9A-Fa-f]{3,6})', core.ROOT):
            m['--' + name] = hx.lower()
    return m


def _to_rgb(hx):
    hx = hx.lstrip('#')
    if len(hx) == 3:
        hx = ''.join(c * 2 for c in hx)
    if len(hx) != 6:
        return None
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def _resolve(color, tokens):
    """Resolve 'var(--x)' -> hex via tokens, or pass through a literal #hex.
    Returns lowercase #hex or None if it can't be resolved (skip, don't guess)."""
    if not isinstance(color, str):
        return None
    color = color.strip()
    mv = re.fullmatch(r'var\(\s*(--[\w]+)\s*\)', color)
    if mv:
        return tokens.get(mv.group(1))
    if re.fullmatch(r'#[0-9A-Fa-f]{3,6}', color):
        return color.lower()
    return None


def same_as_bg_scan(html, page_bg, core=None, thresh=18):
    """AUTO-GATE version of invisible_color_check — scans the HTML itself instead of a
    hand-maintained pairs list.

    WHY: invisible_color_check is OPT-IN (the caller must build `color_pairs`). In the
    showcase5b run a speech bubble was filled with the SAME accent as the page field and
    rendered as an empty outline — the check that exists for exactly this never fired, because
    the bespoke script simply never passed color_pairs. That is the same failure shape as the
    'flat_dominant computed but inert' bug in DECISIONS.md: a check that exists but does not run
    is worth nothing.

    This version needs no cooperation from the caller. It regex-scans every `background:` /
    `background-color:` declaration and flags any that resolves to (near-)exactly the page bg.
    thresh is deliberately TIGHT (18, vs 40 for the manual check) so it stays zero-false-positive
    and is safe to auto-run on every render: a deliberate tone-on-tone layer will normally sit
    further apart than this, while the real bug is an exact token match.

    Skips gradients, `transparent`, `none`, rgba() and named colours rather than guessing.
    Returns a list of (declared_value, resolved_hex, dist). Empty == clean.
    """
    tokens = _token_map(core)
    bgh = _resolve(page_bg, tokens)
    if bgh is None:
        return []
    bgr = _to_rgb(bgh)
    if bgr is None:
        return []
    out, seen = [], set()
    # Scan ONLY element inline style="..." attributes. Scanning the whole document also matched
    # the page container's own `.p{background:X}` rule in the <style> block, which trivially
    # equals the page bg — a guaranteed false positive on every render (caught in self-test).
    decls = []
    for sm in re.finditer(r'style\s*=\s*"([^"]*)"', html or ""):
        st = sm.group(1)
        # Skip FULL-BLEED BACKDROP layers. A div with inset:0 (or 100%x100%) painted in the page
        # colour IS the background field — a deliberate base layer, not an invisible element.
        # Without this the gate fired on almost every real build (caught in regression).
        flat = st.replace(" ", "")
        if "inset:0" in flat or ("width:100%" in flat and "height:100%" in flat):
            continue
        decls.extend(re.findall(r'background(?:-color)?\s*:\s*([^;"\']+)', st))
    for val in decls:
        val = val.strip()
        if any(k in val.lower() for k in ("gradient", "transparent", "none", "rgba", "url(")):
            continue
        h = _resolve(val, tokens)
        if h is None:
            continue
        r = _to_rgb(h)
        if r is None:
            continue
        dist = sum((a - b) ** 2 for a, b in zip(r, bgr)) ** 0.5
        if dist < thresh and val not in seen:
            seen.add(val)
            out.append((val, h, round(dist, 1)))
    return out


_CRAFT_COLOR = re.compile(r'(var\(\s*--[\w]+\s*\)|#[0-9A-Fa-f]{3,6})')


def invisible_craft_scan(html, page_bg, core=None, thresh=18):
    """Flag CRAFT-LAYER strokes (ink outlines, hard-offset shadows) that resolve to the page bg
    and therefore render invisible.

    THE BUG THIS ENCODES (Friendship Day carousel, 2026-08-02). `same_as_bg_scan` guards element
    FILLS, but the AQ craft layer (CLAUDE.md §9: "thick ink outlines · hard-offset ink shadows")
    lives in `border:` and `box-shadow:`, which nothing checked. On the two ink-based slides every
    element carried `border:7px solid var(--ink)` + `box-shadow:12px 12px 0 var(--ink)` against an
    ink page — so the entire outline-and-shadow language silently deleted itself. The slides still
    rendered, still passed every gate, and looked flat and cheap next to the cream ones. Caught by
    eye only; that is exactly the class §8 says to convert into a rule.

    The fix a build should make is NOT to drop the outline but to flip its colour with the field
    (cream outline on ink, ink outline on cream) — i.e. outline colour is a per-slide token, not a
    constant.

    ADVISORY, not a hard fail. Known false positive: an element sitting on a CARD rather than on
    the page (a cream-bordered chip on an accent panel over a cream page reads fine, but resolves
    'border == page bg' here). Element-to-backing-surface is not knowable from the HTML alone, so
    this reports and never flips preflight's `clean`. thresh is tight (18) for the same reason
    same_as_bg_scan is: the real bug is an exact token match.

    Returns list of (property, declared_value, resolved_hex, dist). Empty == clean.
    """
    tokens = _token_map(core)
    bgh = _resolve(page_bg, tokens)
    if bgh is None:
        return []
    bgr = _to_rgb(bgh)
    if bgr is None:
        return []
    out, seen = [], set()
    for sm in re.finditer(r'style\s*=\s*"([^"]*)"', html or ""):
        st = sm.group(1)
        props = [("border", v) for v in re.findall(
            r'border(?:-(?:top|right|bottom|left))?\s*:\s*([^;"\']+)', st)]
        props += [("box-shadow", v) for v in re.findall(r'box-shadow\s*:\s*([^;"\']+)', st)]
        for prop, val in props:
            if any(k in val.lower() for k in ("gradient", "transparent", "none", "rgba", "inset")):
                continue
            m = _CRAFT_COLOR.search(val)
            if not m:
                continue
            h = _resolve(m.group(1), tokens)
            if h is None:
                continue
            rgb = _to_rgb(h)
            if rgb is None:
                continue
            dist = sum((a - b) ** 2 for a, b in zip(rgb, bgr)) ** 0.5
            key = (prop, m.group(1))
            if dist < thresh and key not in seen:
                seen.add(key)
                out.append((prop, m.group(1), h, round(dist, 1)))
    return out


_PATTERN_FN = ("repeating-linear-gradient", "repeating-radial-gradient",
               "repeating-conic-gradient", "conic-gradient", "radial-gradient")

def wash_scan(html, W=1080, H=1350, lo=0.05, hi=0.34, min_area_frac=0.22):
    """Flag large PATTERNED decoration rendered at low opacity — the 'faint wash'
    defect.

    THE BUG THIS ENCODES (Friendship Day, 2026-08-02; catalogued in CLAUDE.md §10
    with a written rule but, until now, NO automated guard). Rings, hatch and
    checker 'fields' were laid across big areas at .13-.26 opacity to add
    richness. At that alpha a pattern does not read as texture — it reads as
    DIRT on the paper, and worse, body copy sitting on top of it loses its
    counters and smears. The piece looks smudged rather than crafted, and every
    numeric gate passes because nothing is off-canvas, colliding or invisible.

    The fix is never 'nudge the alpha' — it is the house rule: decoration is
    SOLID, lives inside a shape with an edge, and carries the ink outline and
    hard shadow like any other object (engine/tex.py). If a texture has to be
    whispered to be bearable, cut it.

    Scoped deliberately so it does not cry wolf:
      * only PATTERN backgrounds (repeating-*/conic/radial gradients). A flat
        low-alpha colour layer is a photo scrim, which is legitimate craft
        (CAROUSEL_PLAYBOOK) and is left alone.
      * only opacity strictly inside (lo, hi). Below `lo` it is invisible rather
        than dirty; at/above `hi` it is a deliberate, visible field.
      * only when the element covers >= `min_area_frac` of the canvas, because
        the damage is proportional to how much copy it can sit under. A small
        textured chip is fine.

    ADVISORY. A halftone screen over a PHOTO is the one legitimate large
    low-alpha pattern in the house style, and whether a div sits over an image
    is not knowable from the HTML string alone — so this reports and never flips
    preflight's `clean`, per the standing 'no noisy check in the auto-gate' rule.

    Returns list of (opacity, area_frac, pattern_fn, snippet). Empty == clean.
    """
    out = []
    canvas = float(W * H) or 1.0
    for sm in re.finditer(r'style\s*=\s*"([^"]*)"', html or ""):
        st = sm.group(1)
        low = st.lower()
        fn = next((f for f in _PATTERN_FN if f in low), None)
        if fn is None:
            continue
        om = re.search(r'(?:^|[;\s])opacity\s*:\s*([0-9.]+)', low)
        if not om:
            continue
        try:
            op = float(om.group(1))
        except ValueError:
            continue
        if not (lo < op < hi):
            continue
        # area: explicit w/h, or inset:0 which means "the whole parent"
        if re.search(r'inset\s*:\s*0', low):
            frac = 1.0
        else:
            wm = re.search(r'(?:^|[;\s])width\s*:\s*([0-9.]+)px', low)
            hm = re.search(r'(?:^|[;\s])height\s*:\s*([0-9.]+)px', low)
            if not (wm and hm):
                continue
            frac = (float(wm.group(1)) * float(hm.group(1))) / canvas
        if frac >= min_area_frac:
            out.append((op, round(frac, 3), fn, st[:70]))
    return out


def invisible_color_check(pairs, page_bg, core=None, thresh=40):
    """
    Flag any fill/stroke color that is ~identical to the surface it sits on —
    the 'shape is technically drawn but invisible' bug that hit sample 21 (an
    oval badge whose background WAS the page bg, so only its white text showed)
    and sample 24 (a near-black text stroke on a black page, so the intended
    bubble-outline never appeared).

    pairs: list of (label, fill_color, surface_color) — surface_color is what's
      DIRECTLY BEHIND this element (usually the page bg, but pass the card color
      if the element sits on a card). Colors may be '#hex' or 'var(--token)'.
    page_bg: default surface for pairs given as (label, fill_color) 2-tuples.
    core: the loaded core module (for var()->hex); pass yours, no re-import.
    thresh: RGB euclidean distance under which two colors read as 'the same'
      (40 ~= imperceptible-to-slight on a 0..441 scale). Unresolvable colors
      (named colors, gradients, rgba) are skipped, never guessed.

    Returns list of (label, fill_hex, surface_hex, dist) that are too close.
    Empty == every shape has real contrast with its backing.
    """
    tokens = _token_map(core)
    out = []
    for p in pairs:
        if len(p) == 3:
            lbl, fill, surf = p
        else:
            lbl, fill = p; surf = page_bg
        fh, sh = _resolve(fill, tokens), _resolve(surf, tokens)
        if fh is None or sh is None:
            continue
        fr, sr = _to_rgb(fh), _to_rgb(sh)
        if fr is None or sr is None:
            continue
        dist = sum((a - b) ** 2 for a, b in zip(fr, sr)) ** 0.5
        if dist < thresh:
            out.append((lbl, fh, sh, round(dist, 1)))
    return out


def css_var_check(html, core=None):
    """
    Catch references to CSS custom properties that were never defined — the
    sample-32 bug where speech-bubble tails used `border-top:...var(--_c)` (a
    typo'd/undefined var), so every tail rendered transparent and invisible.

    Scans `html` for every `var(--x)` reference and every `--x:` definition
    (inline + whatever core.ROOT defines), and returns the sorted list of
    referenced-but-never-defined property names. Empty == all vars resolve.
    """
    defined = set(re.findall(r'(--[\w]+)\s*:', html))
    if core is not None:
        defined |= set('--' + n for n in re.findall(r'--([\w]+)\s*:', core.ROOT))
    referenced = set(re.findall(r'var\(\s*(--[\w]+)', html))
    return sorted(referenced - defined)


def rotated_bbox(x, y, w, h, deg):
    """The AXIS-ALIGNED box a rotated element actually occupies.

    THE BUG THIS ENCODES (session 10, found by reconcile_boxes). Rotation is in
    almost every AQ piece — tilted stickers, tape, chips, signs. A bespoke script
    writes `transform:rotate(-9deg)` on a 168px sticker and then appends the
    tuple (x, y, 168, 168), because that is the width it typed. The browser draws
    a 192x192 footprint: 168*(cos9 + sin9). Every collision and bounds check then
    runs against a box 14% too small, and a neighbour gets cleared into the
    sticker's corner. At 45deg the error peaks at 41%.

    Returns (x, y, w, h) re-centred and grown, so it drops straight into an
    elements list:  els.append(("stk", *lay.rotated_bbox(x, y, d, d, rot)))
    """
    import math
    r = math.radians(deg)
    c, s_ = abs(math.cos(r)), abs(math.sin(r))
    nw, nh = w * c + h * s_, w * s_ + h * c
    return (x - (nw - w) / 2.0, y - (nh - h) / 2.0, nw, nh)


def scatter_solve(items, W, H, protect=(), keep_out=(), zones=None, margin=28,
                  max_pair_overlap=0.18, max_protect_cover=0.30, seed=1, tries=600):
    """Place a pile of objects so the pile reads as designed instead of as a mess.

    THE BUG THIS ENCODES (session 10b, sticker swarm). Ten badges were positioned by
    typing coordinates. Every fix moved one badge onto something else: the first pass
    buried DOG FEEDS under a headline, the second buried the word "UP.", the third put
    two badges on the body copy and hid a fourth behind another badge. FIVE iterations,
    each one trading one collision for another, because a human (or a model) picking
    ten positions against ten constraints by eye is doing a search badly.

    vision.plan_spots() already solves exactly this for photographs — measure the
    image, return safe spots. There was simply no equivalent for vector layouts, so
    every bespoke script hand-placed its pile. This is that equivalent.

    Constraints, all hard unless noted:
      * stay `margin` px inside the canvas
      * overlap no OTHER placed item by more than `max_pair_overlap` of its own area
        (a little overlap is the motif — a pile that never touches is a grid)
      * cover no `protect` box by more than `max_protect_cover` (headline lines, body
        copy — text you must still be able to read)
      * never intersect a `keep_out` box at all (the logo, the footer)

    items:   [(label, w, h)] — use the ROTATED footprint (layout.rotated_bbox)
    protect: [(x,y,w,h)] text boxes — may be partly covered, never buried
    keep_out:[(x,y,w,h)] absolute no-go
    zones:   optional [(x,y,w,h)] to bias placement into; defaults to the whole canvas

    Returns (placements, unplaced) where placements is [(label, x, y)]. Anything that
    could not be placed within `tries` comes back in `unplaced` rather than being
    dropped somewhere bad — an honest failure the caller must resolve by removing an
    item or giving it more room.
    """
    rng = random.Random(seed)
    zones = list(zones) if zones else [(margin, margin, W - 2 * margin, H - 2 * margin)]

    def inter(a, b):
        ix = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
        iy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
        return max(0.0, ix) * max(0.0, iy)

    # biggest first: the hard-to-place objects get the free space, which is what a
    # designer does by hand and what makes greedy placement actually converge
    order = sorted(range(len(items)), key=lambda i: -items[i][1] * items[i][2])
    placed, out, unplaced = [], {}, []

    for i in order:
        lab, w, h = items[i]
        best, best_score = None, None
        for _ in range(tries):
            zx, zy, zw, zh = zones[rng.randrange(len(zones))]
            x = rng.uniform(zx, max(zx, zx + zw - w))
            y = rng.uniform(zy, max(zy, zy + zh - h))
            x = min(max(x, margin), W - margin - w)
            y = min(max(y, margin), H - margin - h)
            box = (x, y, w, h)
            area = max(1.0, w * h)

            if any(inter(box, k) > 0 for k in keep_out):
                continue
            worst_pair = max((inter(box, pb) / area for pb in placed), default=0.0)
            if worst_pair > max_pair_overlap:
                continue
            bad_text = False
            cover_pen = 0.0
            for pb in protect:
                frac = inter(box, pb) / max(1.0, pb[2] * pb[3])
                if frac > max_protect_cover:
                    bad_text = True
                    break
                cover_pen += frac
            if bad_text:
                continue

            # among legal spots prefer: a LITTLE contact with a neighbour (the pile
            # should interlock), little text coverage, away from dead corners
            contact = 0.0 if not placed else worst_pair
            cx, cy = x + w / 2, y + h / 2
            centre_pull = ((cx - W / 2) ** 2 + (cy - H / 2) ** 2) ** 0.5 / (W + H)
            score = cover_pen * 3.0 + centre_pull * 0.7 - min(contact, 0.10) * 4.0
            if best_score is None or score < best_score:
                best, best_score = box, score
        if best is None:
            unplaced.append(lab)
        else:
            placed.append(best)
            out[lab] = (best[0], best[1])

    return ([(items[i][0], *out[items[i][0]]) for i in order if items[i][0] in out],
            unplaced)


def reading_order_check(parts, align_tol=24, band_tol=0.35):
    """One SENTENCE broken across several placed boxes must scan in its own order.

    `parts`: (label, x, y, w, h) in the order the words are meant to be READ.

    THE BUG. A welfare poster set "showing up again and again" as three chips:
    SHOWING at x=70, UP AGAIN at x=830, AND AGAIN at x=70. Each chip was legible,
    nothing collided, no quadrant was dead, and the pixel critique was happy — but
    SHOWING and AND AGAIN shared a left edge, so they read as a COLUMN and the eye
    went showing -> and again -> up again. The sentence came apart.

    A Sonnet agent iterated this piece twice. It fixed the empty quadrant (which
    preview.critique names in numbers) and never touched this (which only the eye
    catches), so it is exactly the class section 8 exists to convert into a rule.

    Two failures, both narrow on purpose — this is opt-in and must not cry wolf:
      INVERTED — a later part sits entirely above an earlier one. Unambiguous.
      COLUMN TRAP — parts i and i+2 are left-aligned with each other while i+1 is
        not, and i+1 sits vertically between them. Alignment then beats sequence,
        which is the failure above.
    A normal left-aligned stack passes (all three share the edge, so i+1 is aligned
    too). A clean diagonal stagger passes (i and i+2 are not aligned). Returns a
    list of strings; empty means pass.
    """
    out = []
    P = [_wh(p) for p in parts]
    for i in range(len(P) - 1):
        (la, xa, ya, wa, ha), (lb, xb, yb, wb, hb) = P[i], P[i + 1]
        if yb + hb <= ya:
            out.append(f"READING ORDER INVERTED: '{lb}' sits entirely ABOVE '{la}', "
                       f"but is read after it")
    for i in range(len(P) - 2):
        (la, xa, ya, wa, ha) = P[i]
        (lb, xb, yb, wb, hb) = P[i + 1]
        (lc, xc, yc, wc, hc) = P[i + 2]
        aligned_ac = abs(xa - xc) <= align_tol
        aligned_ab = abs(xa - xb) <= align_tol
        between = ya < yb + hb and yb < yc + hc          # i+1 falls between i and i+2
        if aligned_ac and not aligned_ab and between:
            out.append(
                f"COLUMN TRAP: '{la}' and '{lc}' share a left edge (x={xa} / x={xc}) "
                f"with '{lb}' (x={xb}) between them — they will read as a column, so "
                f"the sentence scans '{la}' -> '{lc}' -> '{lb}'")
    return out


def _wh(p):
    """(label,x,y,w,h) from a labelled or bare box; labels default to their index."""
    if len(p) == 5:
        return (str(p[0]), p[1], p[2], p[3], p[4])
    return ("?", p[0], p[1], p[2], p[3])


def occlusion_check(items, min_visible=0.45):
    """Flag an element so covered by the things in front of it that it reads as a
    mistake rather than as depth.

    THE BUG THIS ENCODES (session 10b, sticker swarm). Interleaving badges in front
    of and behind a headline is the whole motif — a pile only reads as depth when
    some of it is behind. But a "DOG FEEDS" tag placed behind the word SHOWING came
    out ~85% covered, so it read as a red smear with three stray letters, not as a
    sticker. Nothing could catch it: collision_check treats that overlap as intended
    (it IS intended), and bounds/contains have nothing to say about z-order.

    This is the general form of cascade_peek_check, which solved exactly this for
    repeated-card decks and was never generalised past them.

    items: [(label, (x,y,w,h), z), ...] — z is the CSS z-index.
    Anything with a higher z is treated as opaque cover. Returns
    [(label, visible_fraction), ...] for elements below `min_visible`.

    APPROXIMATE BY DESIGN, and one caveat matters more than the rest: a TEXT
    element's bbox is mostly air. A headline box reports 100% coverage of whatever
    sits behind it while its glyph strokes might cover only a third, so this
    over-reports against type. Tolerable here — the numbers still RANK the badges
    correctly, and a badge sitting wholly inside a headline's box is worth looking
    at even when some of it peeks between letters. It also unions coverage on a
    coarse grid rather than clipping polygons, and cannot know a cover is
    translucent. So: "look at this one", never a hard fail.
    """
    out = []
    norm = [(lab, tuple(box[-4:]), z) for lab, box, z in items]
    for lab, (x, y, w, h), z in norm:
        if w <= 0 or h <= 0:
            continue
        covers = [b for _l, b, zz in norm if zz > z]
        if not covers:
            continue
        # 24x24 sample grid over the element: cheap, stable, and accurate to ~2%
        N = 24
        hidden = 0
        for i in range(N):
            px = x + (i + 0.5) * w / N
            for j in range(N):
                py = y + (j + 0.5) * h / N
                for (cx, cy, cw, ch) in covers:
                    if cx <= px <= cx + cw and cy <= py <= cy + ch:
                        hidden += 1
                        break
        visible = 1.0 - hidden / float(N * N)
        if visible < min_visible:
            out.append((lab, round(visible, 3)))
    return out


def resolve_label_z(items, min_visible=0.80, max_passes=6):
    """Re-order a pile's z so that every object's OWN LABEL stays readable.

    THE BUG THIS ENCODES (sample 522f2d89, and the sticker swarm before it). In a
    deliberately overlapping pile, heavy overlap is the whole effect — the objects are
    SUPPOSED to cover each other. What is never intended is one object covering
    another's TEXT. collision_check can say nothing here (the overlap is the design);
    occlusion_check measures whole objects, so a capsule 60% visible reads as fine even
    when the 40% hidden is exactly the part with the words on it.

    So the thing to protect is not the object, it is the label box inside it.

    Given [(key, label_box, z)] this raises the z of any object whose label is covered
    below `min_visible`, just far enough to clear whatever covers it, and repeats until
    stable. Raising rather than lowering keeps the pile's existing depth relationships
    as intact as possible — the alternative, pushing coverers down, cascades.

    Returns (new_z_by_key, unresolved_keys). `unresolved` is honest: two labels can sit
    exactly on top of each other, and no z-order fixes that — the composition has to
    move. Callers should act on it rather than shipping an unreadable label.
    """
    z = {k: zz for k, _b, zz in items}
    boxes = {k: tuple(b[-4:]) for k, b, _z in items}
    keys = [k for k, _b, _z in items]

    def _vis(k):
        cur = [(kk, boxes[kk], z[kk]) for kk in keys]
        hit = occlusion_check([(kk, b, zv) for kk, b, zv in cur], min_visible=min_visible)
        return {h[0]: h[1] for h in hit}

    # Raise ONE object per pass — the worst-covered — and re-measure.
    #
    # Two traps here, both hit while writing this:
    #   * raising EVERY covered object at once makes a mutually-overlapping pair lift
    #     each other forever: a goes above b, b goes above a, both climb.
    #   * raising one at a time still cycles on such a pair, because whichever ends up
    #     on top leaves the other covered. That case is genuinely UNSOLVABLE by
    #     z-order — if two label boxes materially overlap, no stacking makes both
    #     readable and the composition itself has to move. So a key that has already
    #     been raised once and is covered again is declared unresolved and frozen,
    #     which both breaks the cycle and reports the truth.
    raised, stuck = set(), set()
    for _ in range(max_passes * max(1, len(keys))):
        covered = {k: v for k, v in _vis(None).items() if k not in stuck}
        if not covered:
            break
        k = min(covered, key=lambda kk: covered[kk])
        if k in raised:
            stuck.add(k)
            continue
        above = [z[kk] for kk in keys if kk != k and z[kk] > z[k]
                 and _overlaps(boxes[k], boxes[kk])]
        if not above:
            stuck.add(k)
            continue
        newz = max(above) + 1
        if newz == z[k]:
            stuck.add(k)
            continue
        z[k] = newz
        raised.add(k)
    return z, sorted(_vis(None))


def _overlaps(a, b):
    ix = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    iy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return ix > 0 and iy > 0


def fit_block(available_h, line_count, line_height=0.9, max_size=200, min_size=24,
              extras=0):
    """The largest font size at which `line_count` lines still fit `available_h`.

    THE BUG THIS ENCODES (session 10b, piece C). A headline was set at a size picked
    by eye, wrapped to one more line than expected, and pushed the body copy down
    onto the footer. The available space was knowable the whole time — it is just
    (footer top - photo bottom) - the gaps. Solve for the size instead of nudging it.

    `extras` is any fixed height below the block that must also fit (body copy, a
    kicker, the gaps between them).
    """
    room = available_h - extras
    if room <= 0 or line_count <= 0:
        return min_size
    return max(min_size, min(max_size, room / (line_count * line_height)))


def contains_check(pairs, pad=0):
    """Flag content that does not actually fit the shape it is supposed to sit in.

    THE BUG THIS ENCODES (session 10, batch v1). A pill-shaped bar was sized from
    its DATA (`width = 120px` for a count of 26) while its label was sized from
    its TEXT, so "PLANTATION DRIVE" rendered as "PLANTAT" hanging off a short
    pill. Same defect, different axis: a three-line headline was positioned over
    a 392px colour band that its own line-height made 448px tall, so the last
    word straddled the band edge onto the page.

    Neither is visible to any existing gate. bounds_check only knows the canvas;
    collision_check treats the label and its pill as two elements that are SUPPOSED
    to overlap; and reconcile.measure_dom can only see containment the DOM actually
    expresses. Label and shape were siblings positioned by coordinate, so nothing
    related them.

    THE PREFERRED FIX IS STRUCTURAL: nest the label INSIDE the shape's div. Then
    the browser enforces containment and measure_dom reports it for free. Use this
    check for the cases nesting cannot express — a rotated sticker over a slab, a
    caption that must stay within a photo, type fitted to a band it is not a child
    of.

    pairs: [(label, inner(x,y,w,h), outer(x,y,w,h)), ...]
    pad:   required slack inside the outer box, in px.
    Returns [(label, side, overhang_px), ...]. Empty == clean.
    """
    out = []
    for label, inner, outer in pairs:
        ix, iy, iw, ih = inner[-4:]
        ox, oy, ow, oh = outer[-4:]
        for side, over in (("left",   (ox + pad) - ix),
                           ("top",    (oy + pad) - iy),
                           ("right",  (ix + iw) - (ox + ow - pad)),
                           ("bottom", (iy + ih) - (oy + oh - pad))):
            if over > 0.5:
                out.append((label, side, round(over, 1)))
    return out


def star_text_width(diameter, waist_frac=0.42):
    """
    A 5/6-point star's usable text band is its narrow horizontal WAIST, not its
    full bounding box — text sized to the box overflows past the points and gets
    clipped by the clip-path (samples 19 and 44, both star badges). Constrain the
    inner text element to this width and let it wrap. Returns an int px width.
    """
    return int(diameter * waist_frac)


def dominance_check(elements, W, H, min_hero_frac=0.12):
    """
    The static cousin of metrics.VDR: 'every layout has a HERO slot' (DECISIONS.md)
    and VDR<0.05 == no hero (weak). Recurring miss where a substituted hero doodle
    was scaled far too small for the reference's dominant element — sample 42 (a mic
    that filled ~55% of the reference became a small globe, leaving a dead gap), and
    the general 'scale UP existing elements before adding filler' lesson.

    Call this ONLY when the piece is meant to have a single dominant element (heroes,
    number_hero, giant_type, podcast-cover, etc.) — scatter collages legitimately have
    no hero. Returns [] if some element's bbox area is >= min_hero_frac of the canvas,
    else [("no hero", largest_frac)] so the caller knows to grow the intended hero.
    Accepts (x,y,w,h) or (label,x,y,w,h).
    """
    canvas = W * H
    largest = 0.0
    for e in elements:
        x, y, w, h = e[-4:]
        largest = max(largest, (w * h) / canvas)
    if largest < min_hero_frac:
        return [("no hero", round(largest, 3))]
    return []


def antipattern_scan(html, wide_px=480):
    """
    Precise lint for the DECISIONS.md rendering gotcha (sample 2022ebef): a
    position:absolute child anchored with `bottom:Npx` silently fails to paint once
    it is WIDE, inside a rotated overflow:hidden parent — a blank-card bug with NO
    error. The discriminating factor is WIDTH ("width 300 renders, width 760
    vanishes"), NOT the ambient rotate/overflow:hidden (page() adds overflow:hidden
    to every .p, and footers routinely use bottom:, so co-occurrence alone is pure
    noise). So we flag only the real shape: a single element whose OWN style pairs
    `bottom:Npx` with a `width:` >= wide_px. Narrow bottom-anchored footers are not
    flagged; wide bottom-anchored cards/SVGs are.

    Returns [] or one 'verify this' warning per offending style. Re-anchor with
    `top:` and eyeball the element in the render.
    """
    out = []
    for style in re.findall(r'style\s*=\s*"([^"]*)"', html):
        if re.search(r'(^|;)\s*bottom\s*:\s*\d', style) is None:
            continue
        wm = re.search(r'(^|;)\s*width\s*:\s*(\d+)\s*px', style)
        if wm and int(wm.group(2)) >= wide_px:
            out.append(f"HEURISTIC: a bottom-anchored element is {wm.group(2)}px wide — wide "
                       f"bottom-anchored children inside a rotated overflow:hidden parent can "
                       f"render BLANK (Chromium, no error). Re-anchor with top: and verify in "
                       f"the render. See brain/DECISIONS.md sample 2022ebef.")
    return out


def img_src_check(html):
    """
    Catch `<img src="file://...">` (or any non-data:/non-http(s): src) — it renders as a
    silently BROKEN image with zero console error surfaced to any existing gate. Proven
    empirically (session 9, HR yearbook carousel): Chromium refuses local-resource loads from a
    page whose origin is about:blank/data (`build.render` uses Playwright's `page.set_content`,
    which never navigates to a file:// origin), logging only
    "Not allowed to load local resource" to the browser console — invisible to bounds_check,
    collision_check, css_var_check, and invisible_color_check alike, all of which inspect CSS/
    layout, never whether an <img> actually resolved. A halftone/tint wrapper around a failed
    photo (tex.riso_photo_wrap) then renders as a flat tinted field with nothing behind it —
    reads as "fine" to every existing check.
    core._b64(path, mime) (already used for LOGO/PHOTOS/FONTS) is the fix: embed the image as a
    data: URI instead of referencing it by path. This check is the guard so a bespoke script that
    forgets to do that fails LOUD, before render, instead of shipping a blank photo.
    Returns [] (pass) or the list of offending src values.
    """
    bad = []
    for src in re.findall(r'<img[^>]+src\s*=\s*"([^"]*)"', html):
        if not (src.startswith("data:") or src.startswith("http://") or src.startswith("https://")):
            bad.append(src)
    return bad


def preflight(W, H, elements, html=None, color_pairs=None, page_bg=None, core=None,
              expect_hero=False, min_hero_frac=0.12, quad_min_frac=0.35,
              collision_ignore=frozenset(), auto_nudge=False, cascade_stacks=None,
              contains=None, occlusion=None, reading_order=None):
    """
    ONE pre-render gate that runs every static check the session-8 revisit pass
    turned into a rule. The pass showed the recurring bugs slipped through because
    each build called only a SUBSET of the checks by hand (usually just bounds +
    quadrant). Running them uniformly, every time, is the actual confidence lever:
    no generation can silently skip a failure class again.

    Pass what you have; each check is skipped if its inputs are absent:
      elements     : list of (x,y,w,h) or (label,x,y,w,h) — always run bounds +
                     collision + quadrant on these.
      html         : final inner/page HTML string -> css_var_check + antipattern_scan.
      color_pairs  : list of (label,fill) or (label,fill,surface) -> invisible_color_check
                     (needs page_bg + core to resolve var() tokens).
      expect_hero  : True only for single-dominant-element layouts -> dominance_check.
      contains      : list of (label, inner_box, outer_box) -> contains_check. Declares
                     "this content must fit inside that shape" for relationships the DOM
                     does not express. HARD FAIL — clipped copy is never intended.
      cascade_stacks: list of repeated-card "deck" groups, each a list of (x,y,w,h) ordered
                     back-to-front -> cascade_peek_check per group (opt-in, advisory: rotation
                     is ignored so it can under-flag a rotated design that clears the bbox check
                     without actually reading as flat — never over-flag one, per the docstring).
      auto_nudge   : if True and collisions are found, run collision_nudge on `elements`
                     before scoring collisions/quadrants/hero — r['nudged_elements'] carries
                     the repositioned list back to the caller (None if nothing moved) so a
                     bespoke script can adopt the fixed positions instead of hand-repositioning.
                     Any pair collision_nudge can't separate within the canvas still fails
                     `clean` via r['collisions'].

    Returns dict: {'clean': bool, '<check>': [issues...], ...} and prints a one-line
    verdict + any issues. `clean` is True iff every HARD-FAIL check passed. The
    hard-fail checks are genuine, zero-false-positive bugs: off-canvas, collisions,
    undefined vars, invisible colors, and (opt-in) missing hero. `under_filled_quadrants`
    is ADVISORY only — its inverted-threshold density signal is noisy and the post-render
    pixel critique (preview.py) judges density far more accurately, so it is reported but
    never flips `clean`. The rotate/overflow blank-card heuristic is deliberately NOT in
    this bundle (false-positives on normal footers) — call antipattern_scan manually.
    """
    r = {}
    r['nudged_elements'] = None
    if auto_nudge and collision_check(elements, ignore_pairs=collision_ignore):
        elements, _ = collision_nudge(elements, W, H, ignore_pairs=collision_ignore)
        r['nudged_elements'] = elements
    # legacy checks want plain (x,y,w,h); collision_check keeps labels for readable output
    plain = [e[-4:] for e in elements]
    r['off_canvas'] = bounds_check(W, H, plain)
    r['collisions'] = collision_check(elements, ignore_pairs=collision_ignore)
    r['under_filled_quadrants'] = quadrant_fill_check(W, H, plain, min_frac=quad_min_frac)  # advisory
    if html is not None:
        r['undefined_css_vars'] = css_var_check(html, core)
        r['broken_img_src'] = img_src_check(html)
        if page_bg is not None:
            # ADVISORY (see invisible_craft_scan): catches the craft layer deleting itself when
            # an ink outline/hard shadow lands on an ink field. Cannot be a hard fail because an
            # element's true backing surface isn't knowable from the HTML.
            r['invisible_craft'] = invisible_craft_scan(html, page_bg, core)
        # ADVISORY: large patterned decoration at low alpha reads as dirt and smears
        # through body copy (friendship_day). Can't tell a halftone-over-photo from a
        # wash-over-paper in a string, so it reports and never blocks.
        r['faint_wash'] = wash_scan(html, W, H)
        # antipattern_scan is NOT run here — it cannot be told apart from a normal
        # full-width footer without nesting analysis (false-positives on nearly every
        # poster). Call layout.antipattern_scan(html) manually when chasing a blank card.
    if color_pairs is not None:
        r['invisible_colors'] = invisible_color_check(color_pairs, page_bg, core)
    if expect_hero:
        r['missing_hero'] = dominance_check(elements, W, H, min_hero_frac)
    if occlusion is not None:
        r['occluded'] = occlusion_check(occlusion)
    if contains is not None:
        r['not_contained'] = contains_check(contains)
    if reading_order:
        # HARD FAIL: a sentence that scans in the wrong order is not a taste call,
        # it is copy the reader assembles incorrectly. Opt-in, so it only ever runs
        # on boxes the author has declared to be one sentence.
        r['reading_order'] = reading_order_check(reading_order)
    if cascade_stacks:
        hidden = []
        for gi, stack in enumerate(cascade_stacks):
            hidden.extend((gi, i, frac) for i, frac in cascade_peek_check(stack))
        r['cascade_hidden'] = hidden
    ADVISORY = {'under_filled_quadrants', 'nudged_elements', 'invisible_craft',
                'cascade_hidden', 'faint_wash', 'occluded'}
    hard = {k: v for k, v in r.items() if k not in ADVISORY}
    clean = all(not v for v in hard.values())
    r['clean'] = clean
    print(f"[preflight] {'CLEAN ✓' if clean else 'ISSUES:'}")
    # A check that fires on EVERY composition carries no signal. under_filled_quadrants
    # flagging all four quadrants is exactly that: measured across the session-10
    # batches it printed on essentially every clean run, which is how a reader learns
    # to skim past advisory lines that DO matter. Still returned, just not printed.
    _noise = {'under_filled_quadrants'}
    for k, v in r.items():
        if k in _noise and isinstance(v, list) and len(v) >= 4:
            continue
        if k != 'clean' and v:
            tag = " (advisory)" if k in ADVISORY else ""
            shown = f"{len(v)} element(s) repositioned" if k == 'nudged_elements' else v
            print(f"   - {k}{tag}: {shown}")
    return r
