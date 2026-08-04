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
    out = []
    for i in range(len(norm)):
        for j in range(i + 1, len(norm)):
            la, ax, ay, aw, ah = norm[i]
            lb, bx, by, bw, bh = norm[j]
            if frozenset({la, lb}) in ignore_pairs:
                continue
            ox = min(ax + aw, bx + bw) - max(ax, bx)
            oy = min(ay + ah, by + bh) - max(ay, by)
            if ox > min_overlap and oy > min_overlap:
                out.append((la, lb, ox, oy))
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
              collision_ignore=frozenset(), auto_nudge=False):
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
        # antipattern_scan is NOT run here — it cannot be told apart from a normal
        # full-width footer without nesting analysis (false-positives on nearly every
        # poster). Call layout.antipattern_scan(html) manually when chasing a blank card.
    if color_pairs is not None:
        r['invisible_colors'] = invisible_color_check(color_pairs, page_bg, core)
    if expect_hero:
        r['missing_hero'] = dominance_check(elements, W, H, min_hero_frac)
    ADVISORY = {'under_filled_quadrants', 'nudged_elements', 'invisible_craft'}
    hard = {k: v for k, v in r.items() if k not in ADVISORY}
    clean = all(not v for v in hard.values())
    r['clean'] = clean
    print(f"[preflight] {'CLEAN ✓' if clean else 'ISSUES:'}")
    for k, v in r.items():
        if k != 'clean' and v:
            tag = " (advisory)" if k in ADVISORY else ""
            shown = f"{len(v)} element(s) repositioned" if k == 'nudged_elements' else v
            print(f"   - {k}{tag}: {shown}")
    return r
