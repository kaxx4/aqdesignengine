import os
# GEOMETRIC RECONCILIATION — when eyes are unavailable, catch structural flaws by measuring
# actual element extents in the rendered DOM. Catches: text overflow, off-canvas, element collisions
# beyond the audit whitelist, text-wider-than-container, elements past margins.
import asyncio, importlib.util
def load(n):
    s=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),f"{n}.py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
# engine.py is loaded LAZILY. It imports build.py, and build.py now imports this
# module for measure_dom() — loading it at import time would close that circle.
# measure_dom needs nothing from it; only the Workflow A probe() does.
_ENG = None
def _eng():
    global _ENG
    if _ENG is None:
        _ENG = load("engine")
    return _ENG

W,H=1080,1350; M=64

# ════════════════════════════════════════════════════════════════════════════
# measure_dom — the reusable half of this module  (session 10)
# ════════════════════════════════════════════════════════════════════════════
# THE BUG THIS FIXES. Everything below in probe() measures real rendered extents
# and catches exactly the failure class that hand-maintained (x,y,w,h) tuples
# CANNOT catch: a text block whose true rendered size is not what the author
# guessed. But probe() is welded to Workflow A — it takes an archetype name,
# replays engine.ARCHETYPES, hardcodes 1080x1350 and drives its own browser. So
# for every bespoke Workflow B script (all 44 recreations, and every poster in
# this session) the one check that would have caught the bug was unreachable.
#
# Three real failures in the session-10 batch v1, all invisible to the static
# gate and all caught instantly by this once it could be called:
#   * a 470px numeral was ~100px wider than its declared bbox, so the collision
#     check cleared a sticker that visibly sat on the glyph;
#   * pill labels were wider than their pills and rendered "PLANTAT…" clipped;
#   * a 3-line headline was taller than the colour band it was sized to sit in
#     and spilled across the boundary into the body copy.
#
# measure_dom() is that logic with the Workflow A plumbing removed: give it any
# loaded page and it reports what is ACTUALLY on screen. build.render() calls it
# on every render now, reusing the page it already has, so it costs ~15ms.

_MEASURE_JS = """els => els.map(e => {
  const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
  // AN SVG's `className` IS AN SVGAnimatedString, NOT A STRING. It is truthy, so it
  // won every `||` here and the tag serialized as `{}` — real reports read
  // "OFF-CANVAS {}" and "UNTRACKED {}", naming nothing you could act on.
  const _tag = (el) => {
    const c = el.className;
    return el.dataset.tag || (typeof c === "string" && c) ||
           (c && c.baseVal) || el.tagName.toLowerCase();
  };
  return { tag: _tag(e),
           x: Math.round(r.x), y: Math.round(r.y),
           w: Math.round(r.width), h: Math.round(r.height),
           right: Math.round(r.right), bottom: Math.round(r.bottom),
           sw: e.scrollWidth, cw: e.clientWidth,
           sh: e.scrollHeight, ch: e.clientHeight,
           ox: cs.overflowX, oy: cs.overflowY,
           fixedW: /\d/.test(e.style.width || ""),
           fixedH: /\d/.test(e.style.height || ""),
           // Does this element's OWN TEXT actually reach the surface? Sample a few
           // points across its box and ask the browser what is painted there. A
           // point "hits" when elementFromPoint returns this element or something
           // inside it. See buried_text in measure_dom for why this exists.
           txt: (e.textContent || "").trim().slice(0, 40),
           // "Has own text" was the whole test, so a buried IMAGE was invisible to the
           // check: a fade layer landed above build.logo()'s hardcoded z-index:20 and
           // the wordmark vanished completely, with nothing reported (session 10f,
           // agent f62f8). A logo is content, not decoration. An <img>/<svg> counts,
           // and so does anything the author tagged `logo`.
           ownText: [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())
                    // CASE MATTERS: an SVG element's tagName is the lowercase "svg",
                    // not "SVG", because it lives in the SVG namespace. The first
                    // version of this compared against "SVG" and therefore matched
                    // nothing — every doodle stayed invisible to the check while
                    // looking fixed. Verified against a real render, not assumed.
                    || ["img", "svg"].includes(e.tagName.toLowerCase())
                    // ...and the WRAPPER an author positions. A doodle is placed as a
                    // div containing one svg; the div has no text and is not itself an
                    // svg, so checking only the leaf missed the element that actually
                    // went missing (session 10f, agent f2514).
                    || (e.children.length === 1 &&
                        ["img", "svg"].includes(e.children[0].tagName.toLowerCase()))
                    || (e.dataset.tag || "").toLowerCase().includes("logo"),
           hit: (() => {
             if (r.width < 2 || r.height < 2) return null;
             // OPACITY IS THE WHOLE POINT. elementFromPoint reports GEOMETRIC
             // stacking, not visual coverage — and a headline at the house's tight
             // line-height hit-tests ABOVE its own border box, so it "covered" a
             // label 27px higher while being completely transparent there. The v1
             // of this check called that buried and was wrong (agent c2, c2_v5).
             // So: walk the whole stack at each point, top down, and only call it
             // buried if something OPAQUE sits above this element.
             const opaque = (n) => {
               const s = getComputedStyle(n);
               if (parseFloat(s.opacity || "1") < 0.5) return false;
               if (s.backgroundImage && s.backgroundImage !== "none") return true;
               const m = (s.backgroundColor || "").match(/rgba?\\(([^)]+)\\)/);
               if (!m) return false;
               const p = m[1].split(",").map(parseFloat);
               return p.length < 4 || p[3] >= 0.9;
             };
             // A 3x3 GRID, not the old 5-point X. Judging "is half of this word
             // covered" needs vertical resolution: with points only at .3/.5/.7 a
             // label sliced across its middle blocked 2 of 5 and passed. Nine points
             // put three full rows under the question, so a bottom-half cover reads
             // as 6/9 while a corner tuck stays at 1/9.
             const pts = [[.2,.2],[.5,.2],[.8,.2],
                          [.2,.5],[.5,.5],[.8,.5],
                          [.2,.8],[.5,.8],[.8,.8]];
             let seen = 0, ok = 0, top = null;
             for (const [fx, fy] of pts) {
               const px = r.x + r.width * fx, py = r.y + r.height * fy;
               if (px < 0 || py < 0 || px > innerWidth || py > innerHeight) continue;
               seen++;
               const stack = document.elementsFromPoint(px, py);
               let blocked = null;
               for (const t of stack) {
                 if (t === e || e.contains(t) || t.contains(e)) break;  // reached us
                 if (opaque(t)) { blocked = t; break; }
               }
               if (!blocked) { ok++; }
               else if (!top) {
                 top = _tag(blocked);
               }
             }
             return seen ? { seen, ok, top } : null;
           })(),
           // What is ACTUALLY painted behind this element's own background? Walk the
           // stack below it and take the first opaque thing. See invisible_fill.
           behind: (() => {
             const cs2 = getComputedStyle(e);
             const own = cs2.backgroundColor || "";
             const m = own.match(/rgba?\\(([^)]+)\\)/);
             if (!m) return null;
             const p = m[1].split(",").map(parseFloat);
             if (p.length >= 4 && p[3] < 0.9) return null;   // not an opaque fill
             if ((cs2.backgroundImage || "none") !== "none") return null;
             if (r.width < 4 || r.height < 4) return null;
             const stack = document.elementsFromPoint(r.x + r.width / 2,
                                                      r.y + r.height / 2);
             let past = false;
             for (const t of stack) {
               if (t === e) { past = true; continue; }
               if (!past) continue;                          // above us; not the backing
               if (e.contains(t)) continue;                  // our own child
               const s3 = getComputedStyle(t);
               if ((s3.backgroundImage || "none") !== "none") return null;
               const m3 = (s3.backgroundColor || "").match(/rgba?\\(([^)]+)\\)/);
               if (!m3) continue;
               const q = m3[1].split(",").map(parseFloat);
               if (q.length >= 4 && q[3] < 0.9) continue;    // see through it
               return { own: own, behind: s3.backgroundColor, tag: _tag(t) };
             }
             return null;
           })(),
           clip: (() => {
             // nearest ancestor that actually CLIPS, and its rect
             let p = e.parentElement;
             while (p && p !== document.body) {
               const cs2 = getComputedStyle(p);
               // The page root .p is ALWAYS overflow:hidden, and bleeding off the
               // canvas edge is a deliberate AQ move (the staggered-pill field bleeds
               // 28 pills on purpose). Treating .p as a clipping parent reported every
               // one of them as lost content. Page-edge bleed is the off_canvas
               // check's job, which has its own bleed whitelist; this check is only
               // about a child cut off by a CARD or SLAB.
               if (p.classList && p.classList.contains("p")) { return null; }
               if (cs2.overflowX === "hidden" || cs2.overflowY === "hidden" ||
                   cs2.overflowX === "clip"   || cs2.overflowY === "clip") {
                 const pr = p.getBoundingClientRect();
                 return { x: Math.round(pr.x), y: Math.round(pr.y),
                          r: Math.round(pr.right), b: Math.round(pr.bottom),
                          tag: _tag(p) };
               }
               p = p.parentElement;
             }
             return null;
           })() };
})"""

# Selector note: `.p [data-tag]` only sees explicitly tagged nodes, which is how
# the old probe under-reported. We measure every positioned descendant instead,
# so an untagged element cannot hide from the check by simply not opting in.
# Selector note. This used to be `.p > div, .p > span, .p > img` plus the tagged
# nodes — DIRECT CHILDREN ONLY. So the moment a build nested anything (a label inside
# a pill, a copy block inside a slab) that element was never measured at all, and the
# nesting the house style actively RECOMMENDS was the thing that hid elements from the
# gate. Sample 77e7bb34 lost a whole line of copy off the top of its slab and nothing
# fired. Now every positioned descendant is measured.
_SEL = ".p [data-tag], .p [class*=measure], .p div, .p span, .p img, .p svg"

# An auto-sized block only gets reported when it overshoots its line box by BOTH
# of these. Measured across the corpus: a normal AQ headline at line-height
# .86-.92 overshoots 7-9%, which is just how tight leading paints — flagging it
# would fire on essentially every poster and teach everyone to ignore the gate.
# A genuine "your bbox is a lie" case (line-height .78 at 470px) overshoots 32%.
def _rgb_tuple(css):
    """(r,g,b) from a computed `rgb()`/`rgba()` string, else None."""
    import re as _re
    m = _re.match(r"rgba?\(([^)]+)\)", (css or "").strip())
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split(",")]
    try:
        return tuple(int(float(p)) for p in parts[:3])
    except ValueError:
        return None


_SPILL_MIN_RATIO = 1.20
_SPILL_MIN_PX = 24

async def measure_dom(page, W, H, margin=64, bleed_tags=("num", "bleed", "hero-bleed"),
                      crop_tags=()):
    """Measure the REAL rendered geometry of a loaded page and report what the
    static tuple gate structurally cannot see.

    Returns {'clipped': [...], 'spilling': [...], 'off_canvas': [...]}.

      clipped   — content is larger than its box AND the box hides overflow, so
                  characters are genuinely lost ("PLANTAT…"). Never legitimate.
      spilling  — content is larger than its box and overflow is visible, so it
                  escapes and lands on whatever is next to it. This is what a
                  headline sized by guesswork does.
      off_canvas— the element's painted box leaves the canvas. ADVISORY: full
                  bleed is a real AQ move, so tags in `bleed_tags` are exempt
                  and the rest are reported, not failed.
    """
    els = await page.eval_on_selector_all(_SEL, _MEASURE_JS)
    _buried_raw = []
    out = {"clipped": [], "spilling": [], "off_canvas": [], "boxes": [],
           "buried_text": [], "invisible_fill": []}
    for e in els:
        if e["cw"] == 0 and e["ch"] == 0:
            continue                                   # not laid out; nothing to say
        out["boxes"].append((e["tag"], e["x"], e["y"],
                             max(e["w"], e["sw"]), max(e["h"], e["sh"])))
        over_x = e["sw"] > e["cw"] + 4
        over_y = e["sh"] > e["ch"] + 4
        if over_x or over_y:
            hides = ("hidden" in (e["ox"], e["oy"])) or ("clip" in (e["ox"], e["oy"]))
            axis = "width" if over_x else "height"
            got, box = (e["sw"], e["cw"]) if over_x else (e["sh"], e["ch"])
            declared = e["fixedW"] if over_x else e["fixedH"]
            rec = (e["tag"], axis, got, box)
            if hides and e["tag"] in crop_tags:
                # ...unless the author says the clipping IS the technique. A frame
                # that deliberately crops an oversize child is overflow:hidden with
                # taller content BY DESIGN, so the container reports here too.
                pass
            elif hides:
                # content larger than a box that hides overflow: characters are
                # GONE. There is no design in which that is intended.
                out["clipped"].append(rec)
            elif declared:
                # the author wrote an explicit width/height and the content does
                # not fit it. Also unambiguous — the assertion was simply wrong.
                out["spilling"].append(rec)
            elif box and (got - box) >= _SPILL_MIN_PX and got / box >= _SPILL_MIN_RATIO:
                # auto-sized: a tight line-height ALWAYS makes glyphs paint past
                # the line box, so small overshoot here is normal typography and
                # flagging it would make this gate noise. Only a large overshoot
                # matters, and what it means is specific: any hand-written
                # (x,y,w,h) tuple for this element under-reports its real size,
                # so the static collision check will clear things that visibly
                # sit on it. (Session 10: a 470px numeral measured 484px tall in
                # a 367px line box; a sticker was cleared onto the glyph.)
                out["spilling"].append(rec)
        # CLIPPED BY ITS PARENT — content lost at a container edge.
        #
        # THE BUG THIS ENCODES (sample 77e7bb34, session 10c). A copy block was
        # positioned inside an overflow:hidden slab with a top offset that computed
        # NEGATIVE, so its first line ("it's time") was sliced off by the slab's edge.
        # Nothing caught it: the element is not bigger than its own box (so the
        # scroll checks say nothing), it is well inside the canvas (so the off-canvas
        # check says nothing), and compare.py scored the piece 0.147 — inside the
        # accept threshold — because a missing line of copy barely moves a pixel
        # histogram. Only the looking gate saw it.
        #
        # An element cut off by its container is never intended, so this is reported
        # unconditionally alongside `clipped`.
        # CROPPING ON PURPOSE. "size it oversize, then clip it with overflow:hidden"
        # is a real technique — an agent used it twice in one poster, to crop a baked
        # caption out of a photo and to shape a hero-shine — and got CLIPPED reported
        # both times on a visually correct render. It worked around the gate rather
        # than ship a render whose own log reads as broken, which is the wrong way
        # round (session 10f, agent g4). Same contract as bleed_tags: say so and the
        # gate believes you.
        cl = e.get("clip")
        if cl and e["tag"] in crop_tags:
            cl = None
        if cl:
            over = []
            if e["x"] < cl["x"] - 1:      over.append(("left",   cl["x"] - e["x"]))
            if e["y"] < cl["y"] - 1:      over.append(("top",    cl["y"] - e["y"]))
            if e["right"] > cl["r"] + 1:  over.append(("right",  e["right"] - cl["r"]))
            if e["bottom"] > cl["b"] + 1: over.append(("bottom", e["bottom"] - cl["b"]))
            for side, px in over:
                out["clipped"].append((f'{e["tag"]} (by {cl["tag"]})', side, int(px), 0))

        # BURIED TEXT — type that is painted, laid out, the right colour, inside its
        # box and on the canvas, and still cannot be seen because something opaque is
        # in front of it.
        #
        # THE BUG THIS ENCODES (session 10f, agent c1's v1). A body-copy paragraph had
        # no z-index; a sibling background rectangle had `z-index:1`. In CSS any
        # explicit z-index on a positioned element paints above `z-index:auto`
        # REGARDLESS of DOM order, so the opaque cream rectangle buried the whole
        # paragraph. preflight printed CLEAN. render()'s auto-gates printed CLEAN.
        # Playwright's own is_visible() and bounding_box() both reported it present,
        # because by every DOM measure it WAS. Only reading the PNG caught it.
        #
        # So the question has to be asked of the compositor, not the layout engine:
        # hit-test points across the box and see what is actually on top. That catches
        # this cause and every other one — paint order, a later sibling, a stacking
        # context — without needing to model any of them.
        #
        # Only elements with their OWN text are tested. A decorative div legitimately
        # sits behind things; a word does not.
        # INVISIBLE FILL, measured against what is REALLY behind the element.
        #
        # layout.same_as_bg_scan answers this statically by comparing every declared
        # background against the PAGE background, and calls itself zero-false-positive.
        # It is not: a cream badge sitting on a full-bleed teal panel is plainly
        # visible, and got "FILL SAME AS PAGE BG" on every render. TWO independent
        # agents reported that (session 10f, c3 and g3), which makes it a spec defect
        # rather than bad luck — a static scan cannot know an element's real backing
        # surface, and guessing the page ground is wrong the moment anything is
        # layered, which is most AQ posters.
        #
        # The browser knows exactly. This compares an element's own opaque fill with
        # the first opaque thing painted underneath it.
        bh = e.get("behind")
        if bh and bh.get("own") and bh.get("behind"):
            ca, cb = _rgb_tuple(bh["own"]), _rgb_tuple(bh["behind"])
            if ca and cb:
                dist = sum((x - y) ** 2 for x, y in zip(ca, cb)) ** 0.5
                if dist < 18:
                    out["invisible_fill"].append(
                        (e["tag"], bh["own"], bh["behind"], bh["tag"], round(dist, 1)))

        hit = e.get("hit")
        # PARTIAL BURIAL IS STILL ILLEGIBLE. This required ok == 0 — every sampled
        # point covered — so a plate whose label had its bottom 40% sliced off by an
        # overlapping sibling passed with 2 of 5 points clear, and shipped: "SINCE
        # 2021" cut through the middle of its letters (session 10f, g2_v6). You
        # cannot read the top half of a word.
        #
        # The threshold has to leave room for the real AQ move it must not flag: a
        # sticker tucked over a headline's corner covers about one point in five and
        # is deliberate. A majority blocked is not a tuck, it is a cut.
        if e.get("ownText") and hit and hit["seen"]:
            _blocked = hit["seen"] - hit["ok"]
            if _blocked and _blocked >= hit["seen"] * 0.6:
                _buried_raw.append(
                    ((e["tag"], ((e.get("txt") or "").strip() or "<image>")[:40],
                      hit.get("top") or "?", f'{_blocked}/{hit["seen"]}'),
                     (e["x"], e["y"], e["w"], e["h"])))

        if e["tag"] in bleed_tags:
            continue
        if e["right"] > W + 2 or e["bottom"] > H + 2 or e["x"] < -2 or e["y"] < -2:
            out["off_canvas"].append((e["tag"], e["x"], e["y"], e["right"], e["bottom"]))
    # ONE LINE PER OBJECT. A doodle is a positioned div containing an svg that
    # carries its own class, so the wrapper and the child reported the same burial
    # twice under different names. Keep the box the AUTHOR positioned (the outer one)
    # and drop anything nested inside it blamed on the same occluder.
    for i, (row, bx) in enumerate(_buried_raw):
        inner = False
        for j, (row2, bx2) in enumerate(_buried_raw):
            if i == j or row[2] != row2[2]:
                continue
            # A doodle svg is width:100%/height:100% of its wrapper, so the two
            # boxes are IDENTICAL and a strict `bigger` test never fired. On a tie,
            # keep whichever came first — querySelectorAll yields DOM order, so the
            # parent the author positioned precedes the child it contains.
            a1, a2 = bx[2] * bx[3], bx2[2] * bx2[3]
            bigger = a2 > a1 or (a2 == a1 and j < i)
            inside = (bx[0] >= bx2[0] - 2 and bx[1] >= bx2[1] - 2 and
                      bx[0] + bx[2] <= bx2[0] + bx2[2] + 2 and
                      bx[1] + bx[3] <= bx2[1] + bx2[3] + 2)
            if bigger and inside:
                inner = True
                break
        if not inner:
            out["buried_text"].append(row)
    return out


def reconcile_boxes(measured, declared, tol=16, min_size=60, canvas=None):
    """Compare what the gate was TOLD against what the browser actually drew.

    THE BUG THIS ENCODES. CLAUDE.md §10 lists "stale bbox tuple hides a real
    off-canvas/collision" with a guard column that reads, in full: "discipline".
    It is the only entry in the catalogue whose guard is a human promise, and it
    has cost real bugs every time — a bespoke script moves an element's CSS,
    forgets the matching elements.append(), and every static check then runs
    against a layout that no longer exists and cheerfully reports CLEAN.

    This is that promise, mechanised. Two distinct failures, both real:

      under_reported — a declared box is materially smaller than the element the
                       browser drew, so collision_check clears neighbours that
                       visibly sit on it. (Session 10: a 430px numeral declared
                       336px tall, painted 443px; a sticker was cleared onto it.)
      untracked      — a substantial element exists in the render with NO
                       declared box anywhere near it, so the static gate never
                       considered it at all. This is the silent half of the bug:
                       not a wrong box, an absent one.

    Matching is positional (nearest origin within `tol`), because tuples carry no
    identity. That is a real limitation: heavily overlapping elements can match
    the wrong partner. So both lists are ADVISORY — they tell you where to look,
    they do not fail a build.

    measured: [(tag,x,y,w,h)] from measure_dom()['boxes']
    declared: the element list handed to preflight — (x,y,w,h) or (label,x,y,w,h)
    """
    out = {"under_reported": [], "untracked": []}
    dec = [(e[0] if len(e) == 5 else "", *e[-4:]) for e in (declared or [])]
    cw, ch = canvas if canvas else (None, None)
    for tag, x, y, w, h in measured:
        if w < min_size or h < min_size:
            continue                                  # chips/labels: too small to matter here
        if cw and w >= cw - 2 and h >= ch - 2:
            continue                                  # the page ground itself
        best, bestd = None, 1e9
        for d in dec:
            dist = abs(d[1] - x) + abs(d[2] - y)
            if dist < bestd:
                best, bestd = d, dist
        if best is None or bestd > tol * 4:
            out["untracked"].append((tag, x, y, w, h))
            continue
        if w > best[3] + tol or h > best[4] + tol:
            out["under_reported"].append(
                (best[0] or tag, (best[3], best[4]), (w, h)))
    return out


def format_reconcile(res):
    lines = []
    for label, dec, real in res.get("under_reported", []):
        lines.append(f"BBOX UNDER-REPORTS {label}: declared {dec[0]}x{dec[1]}, "
                     f"drawn {real[0]}x{real[1]} — the static gate is checking a smaller box")
    for tag, x, y, w, h in res.get("untracked", []):
        lines.append(f"UNTRACKED {tag} at ({x},{y}) {w}x{h} — no declared bbox, "
                     f"so no gate ever considered it")
    return lines


def suppress_handled(flaws, declared, tol=8):
    """Drop OVERSIZE reports the author has already accounted for.

    THE NOISE THIS REMOVES (found by a Sonnet agent running the manual cold, session
    10e). `spilling`/OVERSIZE fires whenever glyphs paint past their line box — which a
    line-height below 1 ALWAYS causes, and every AQ headline uses one. So it printed on
    essentially every hero numeral, including renders where the author had read
    measure_text()'s docstring and correctly sized the bbox off `ink_h`. The check
    cannot tell "already handled" from "genuine bug" on its own.

    But the CALLER knows: if they passed an element list whose declared box already
    covers the painted extent, they have handled it. Only what remains is worth a line.
    A gate that cries wolf on every clean run is how people learn to skim past the
    warnings that matter.
    """
    if not declared:
        return flaws
    boxes = [(e[-2], e[-1]) for e in declared]     # (w, h) of every declared element
    out = dict(flaws)
    keep = []
    for rec in flaws.get("spilling", []):
        tag, axis, got, box = rec
        i = 0 if axis == "width" else 1
        if any(b[i] + tol >= got for b in boxes):
            continue                                # someone declared a box this big
        keep.append(rec)
    out["spilling"] = keep
    return out


def format_measure(flaws, name=""):
    """One-line-per-flaw rendering for the render gate's console output."""
    lines = []
    for tag, axis, got, box in flaws.get("clipped", []):
        if box == 0:
            lines.append(f"CLIPPED {tag}: {got}px past its container's {axis} edge "
                         f"— content is cut off")
        else:
            lines.append(f"CLIPPED {tag}: {axis} {got}px inside a {box}px box "
                         f"— characters are lost")
    for tag, axis, got, box in flaws.get("spilling", []):
        lines.append(f"OVERSIZE {tag}: real {axis} {got}px vs {box}px box "
                     f"— a hand-written bbox here under-reports by {got-box}px")
    for tag, own, behind, btag, dist in flaws.get("invisible_fill", []):
        lines.append(f"INVISIBLE FILL {tag}: its background {own} is the same as the "
                     f"'{btag}' painted directly behind it ({behind}, distance {dist}) "
                     f"— the shape is drawn and cannot be seen")
    for tag, txt, top, seen in flaws.get("buried_text", []):
        lines.append(f"BURIED (advisory) {tag}: \"{txt}\" is painted but not visible — "
                     f"an opaque '{top}' covers it at {seen} sampled points. "
                     f"If that is not intended, raise this element above '{top}' or move "
                     f"one of them. A repeated-card DECK legitimately hides the back "
                     f"copies' own text and will report here")
    for tag, x, y, r, b in flaws.get("off_canvas", []):
        lines.append(f"OFF-CANVAS {tag}: box ({x},{y})-({r},{b})")
    return lines


async def probe(name, archetype, content, accent_idx):
    eng=_eng()
    accent=eng.RULES["accents"][accent_idx]
    # rebuild final html at the density it converged to — replay generate's density logic quickly
    from playwright.async_api import async_playwright
    # brute: try densities 0..4, pick first that passes preview (mirror engine)
    prof=eng.ARCHETYPE_PROFILES.get(archetype,dict(fill_min=0.34,max_density=3))
    import importlib.util as u
    sp=u.spec_from_file_location("pv","preview.py");pv=u.module_from_spec(sp);sp.loader.exec_module(pv)
    density=0; html=None
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for it in range(prof["max_density"]+1):
            inner=eng.ARCHETYPES[archetype](content,accent,density)
            html=eng.B.page(W,H,"var(--bg)",inner,grain=False)
            pg=await b.new_page(viewport={"width":W,"height":H},device_scale_factor=2)
            await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(500)
            await pg.locator(".p").screenshot(path=f"out/{name}.png")
            crit=pv.critique(f"out/{name}.png")
            arch_ok = crit["fill"]>=prof["fill_min"] and crit["contrast"]>=eng.RULES["contrast_min"] and all(v>=eng.RULES["quad_min"] for v in crit["quads"].values())
            if arch_ok: await pg.close(); break
            await pg.close()
            if crit["fill"]<prof["fill_min"]: density=min(density+1,prof["max_density"])
            else: break
        # now measure extents on final
        pg=await b.new_page(viewport={"width":W,"height":H})
        await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(500)
        els=await pg.eval_on_selector_all(".p [data-tag], .p [class*=measure]",
          """els=>els.map(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
             return{tag:e.dataset.tag||'',x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),
             right:Math.round(r.right),bottom:Math.round(r.bottom),
             sw:e.scrollWidth,cw:e.clientWidth}})""")
        await b.close()
    # Measure against the canvas this piece was actually rendered at. These were the
    # literals 1080 and 1350, so probe() reported a phantom bottom overflow on every
    # element below y=1330 of a story poster. probe() is Workflow-A-only legacy and
    # Workflow A is feed-only today, which is the sole reason it never bit.
    pW, pH = W, H
    flaws=[]
    for e in els:
        if e['right']>pW-20: flaws.append(f"{e['tag']} overflows RIGHT edge (right={e['right']})")
        if e['bottom']>pH-20: flaws.append(f"{e['tag']} overflows BOTTOM (bottom={e['bottom']})")
        if e['x']<M-20: flaws.append(f"{e['tag']} breaches LEFT margin (x={e['x']})")
        if e['sw']>e['cw']+4: flaws.append(f"{e['tag']} TEXT WIDER than container (scroll {e['sw']}>{e['cw']})")
    return flaws

async def main():
    cases=[
      ("C1_paradox","giant_type",dict(meta="annual fest · nov",word="paradox",tags=["6 teams","1 night","0 chill"],big="the brief<br>drops soon.",band="pick a lane.",body="two months, one dangerously ambitious student fest.",footer="@ngo.aquaterra → brief in bio"),2),
      ("C4_ways","radial_orbit",dict(meta="the departments",top="one org,",kicker="6 teams",number="6",label="depts",big="find your<br>people.",orbit=[("events",3),("social",5),("welfare",1),("startups",4),("hr",0),("collabs",6)],chips=["there's a spot for you","no experience needed"],footer="@ngo.aquaterra → apply in bio"),2),
      ("C5_merch","giant_type",dict(meta="drop 03 · limited",word="roots",tags=["tees","totes","caps"],big="wear the cause.<br>fund the drive.",band="100% profit → drives.",body="streetwear designed by students.",footer="@ngo.aquaterra → shop in bio"),2),
      ("C7_saturday","giant_type",dict(meta="this week",word="saturday",tags=["6am","topsia","show up"],big="that's the<br>whole plan.",band="bring a friend.",body="food drive at dawn.",footer="@ngo.aquaterra"),1),
      ("C8_members","number_hero",dict(meta="milestone · 2026",kicker="we just hit",number="1.2k",label='teenagers.<br>one <span style="font-family:var(--s);font-style:italic;text-transform:none;color:var(--grape)">city.</span>',chips=["and counting","welfare·climate·education"],band="run entirely by students.",body="1,200 members across six departments.",footer="@ngo.aquaterra"),3),
    ]
    for name,arch,content,acc in cases:
        flaws=await probe(name,arch,content,acc)
        print(f"\n{name} ({arch}):")
        if flaws:
            for f in flaws: print(f"   ⚠ {f}")
        else: print("   ✓ no geometric flaws (extents clean)")

# This module is now IMPORTED by build.py for measure_dom(), so the Workflow A
# demo below must not run on import — it used to fire asyncio.run() at module
# level, which blew up inside any already-running event loop.
if __name__ == "__main__":
    asyncio.run(main())
