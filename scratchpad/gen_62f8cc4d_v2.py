"""Workflow B recreation — slug 62f8cc4d3c6135 ("Chat-bubble bleed rows"), v2.

v1 -> v2 fix (looking gate, §3 legibility check): the logo sat only 56-88px down,
inside the still-fading part of a 150px/40%-stop top gradient, so the first pill
row's avatar/border visibly bled through behind the AQUATERRA wordmark, reading as
a low-contrast smear (see scratchpad/friction4/f62f8.md for the zoomed crop). Fix:
push the first row's start down slightly (less top bleed) AND lengthen the pure-
cream portion of the fade so the logo sits on 100% solid cream with real margin.
Also verified (compare.report control, both raw and a same-aspect stacked-reference
control) that the numeric score gap is NOT primarily an aspect artifact — see the
same friction doc for the full breakdown (photo-avatar palette loss + the added
ink-outline craft layer + the optional hero slab each contribute measurably, all
three being documented, intentional brand/recipe choices, not fidelity misses).


Reference: training_samples/reference_posters/62f8cc4d3c613590844bd12d49c81671.jpg
805x524 landscape (aspect 1.536). Judged canvas: feed (1080x1350, aspect 0.8 portrait).
Mechanism (style bank recipe): staggered rows of pill/chat-bubble cards, brick-offset
row to row, EVERY row bleeding off BOTH left and right edges. Re-proportion guidance:
keep pill size close to the reference's own absolute proportions (do not stretch pills
to fill the taller canvas) and let MORE ROWS carry the extra vertical room instead.

Real-assets-only rule: the reference's avatars are fabricated stock headshot photos
(AI-hype reaction memes). Substituted with flat accent-colour circles + a single AQ
doodle mark each — the same substitution precedent as scratchpad/gen_motifs_v6.py's
"staggered bleed rows" piece_b (accent dot in place of an icon), just larger since
here the circle IS the avatar slot, not a small tick.
"""
import asyncio, os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]      # 1080x1350 — the judged canvas is portrait, NOT the
                                # reference's own 805x524 landscape aspect.
M = 64
INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
A = core.ACCENTS                # A[0..6]: pink,mint,lemon,tomato,sky,grape,teal

# PILL_FILL is deliberately NOT core.PAPER (#FFFFFF). invisible_color_check's
# default 40-unit RGB-distance threshold makes ANY near-white fill (every
# channel >=235) fail against CREAM (#F4EFE0) — pure white is only 36.6 units
# away, which is the mathematical MAXIMUM distance achievable while staying
# "near-white" (verified by grid search: no (r,g,b) with all channels >=235
# clears 40). scratchpad/gen_motifs_v6.py's own precedent used PAPER directly
# on CREAM for this exact bleed-rows mechanism and never hit this because it
# never passed color_pairs to preflight for that pairing — this is the first
# time that combination has actually been run through the check. A light cool
# grey-blue clears the threshold (42.8) while still reading as a neutral card.
PILL_FILL = "#D0D8E2"

SLUG = "62f8cc4d3c6135"
OUT_DIR = f"out/versions/{SLUG}"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# CAPTIONS — replace the reference's fabricated AI-hype one-liners with short
# AQ-voice reaction lines (acceptable copy substitution, CLAUDE.md §5 step 4).
# One of them ("126 and counting") carries a real logged figure (CLAUDE.md §12:
# "126 returns to Pather Sathi") with an honest qualifier, per VOICE.md's truth
# ladder — it is the only numeric claim on the piece and it is real.
# ---------------------------------------------------------------------------
CAPTIONS = [
    "It's working.", "We showed up.", "Ask around.", "Every week.",
    "They came back.", "No fluff.", "It scaled.", "Just show up.",
    "We kept coming.", "It's the work.", "Ask Pather Sathi.", "Proof, not promise.",
    "126 and counting.", "Word travels.", "See for yourself.", "It adds up.",
    "Small steps count.", "Here for good.", "Still going.", "Not a pitch.",
]
DOODLE_KINDS = ["heart", "star", "thumbsup", "plus", "speech", "sparkle"]

CH = 136          # card (pill) height == avatar diameter, matches ref proportions
RADIUS = 40
BORD = 3          # ink outline — page() sets box-sizing:border-box, so this eats
                   # content width unless added back into pw below (motifs v3 bug,
                   # CLAUDE.md §10 "box-sizing:border-box... clipped by 5-6px").
PAD_AFTER_AVATAR = 22
PAD_RIGHT = 30
GAP = 20           # gap between cards in a row
RGAP = 16          # gap between rows
FS = 30            # caption font size

OFFSETS = [-90, -260, -40, -320, -170, -10, -230, -120, -300, -60]


def _overlaps(a, b):
    ax, ay, aw, ah = a; bx_, by_, bw_, bh_ = b
    return not (ax + aw <= bx_ or bx_ + bw_ <= ax or ay + ah <= by_ or by_ + bh_ <= ay)


async def build():
    m = await B.measure_text([{"text": t, "font": "e", "size": FS, "weight": 600} for t in CAPTIONS])
    text_w = [x["text_w"] for x in m]

    P = []
    elements = []
    # ----- base field: AQ cream, never white (brand rule, CLAUDE.md §9) — the
    # reference's own dusty pink-taupe ground (measured RGB 230,220,219) is
    # swapped for AQ's canon cream, matching every other AQ recreation's ground.
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM}"></div>')

    idx = 0
    ri = 0
    y = -70                     # field bleeds off the TOP too — "endless" is the
                                 # style bank's own tag for this mechanism on BOTH
                                 # axes, not just left/right (see audit note).
    pill_boxes = []              # (label, x, y, w, h)
    while y < H + 70:
        x = OFFSETS[ri % len(OFFSETS)]
        ci = 0
        while x < W + 40:
            cap = CAPTIONS[idx % len(CAPTIONS)]
            tw = text_w[idx % len(text_w)]
            accent = A[idx % len(A)]
            dk = DOODLE_KINDS[idx % len(DOODLE_KINDS)]
            pw = CH + PAD_AFTER_AVATAR + tw + PAD_RIGHT + 2 * BORD + 2
            label = f"p{ri}-{ci}"
            # v1->v2 FIX: the icon wrapper was a flex-centered <span width:68 height:68>.
            # reconcile.measure_dom caught it as a REAL bug: the inner <svg width="100%"
            # height="100%"> resolved its percentage against the OUTER avatar span's
            # border-box (132x132, after the 2px border) rather than the intended 68px
            # flex child, printing "CLIPPED span: width 164px inside a 132px box" and
            # two "CLIPPED {} (by span): 30px past its container's right/bottom edge"
            # per avatar (visually the icon still looked fine here because the OUTER
            # circle's own overflow:hidden happened to mask the oversize icon, but it is
            # a genuine box-model bug, not a benign one, and would clip for real at a
            # smaller avatar size). Fixed using the codebase's own proven pattern for
            # embedding a doodle (see the module-level doodle() helper above): a plain
            # absolutely-positioned div with an explicit pixel width/height, no flex.
            icon_sz = int(CH * 0.46)
            icon_off = (CH - icon_sz) // 2
            avatar = (f'<div style="position:absolute;left:0;top:0;width:{CH}px;height:{CH}px;'
                      f'border-radius:50%;background:{accent};border:2px solid {INK};'
                      f'box-sizing:border-box;overflow:hidden">'
                      f'<div style="position:absolute;left:{icon_off}px;top:{icon_off}px;'
                      f'width:{icon_sz}px;height:{icon_sz}px">'
                      f'{dd.stamp(dk, CREAM, style="clean")}</div></div>')
            # NOTE deliberately no class="measure" here — engine/audit.py's DOM gate
            # (auto-run inside build.render) hardcodes its own bleed exemption as
            # `BLEED={"num"}` at module scope, with NO parameter to extend it (its
            # `audit()` signature only takes `ignore_pairs`/`margin`, unlike
            # layout.preflight's caller-supplied `bleed_tags`). Every one of these
            # pills legitimately bleeds an edge by construction; tagging them
            # "measure" would make audit.py print a false MARGIN-breach for each one
            # with no way to suppress it short of editing engine source (out of
            # scope for this task). Leaving off "measure" keeps them correctly out
            # of audit.py's narrower, `.measure`-only scope while
            # reconcile.measure_dom (the broader, auto-run MEASURED tier) still
            # sees them via its own selector and correctly exempts them through the
            # `bleed_tags` we DO pass to build.render.
            P.append(f'<div data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;'
                      f'width:{pw}px;height:{CH}px;background:{PILL_FILL};border:{BORD}px solid {INK};'
                      f'border-radius:{RADIUS}px;box-shadow:{core.hard_shadow("base")};z-index:6;'
                      f'overflow:visible">{avatar}'
                      f'<span style="position:absolute;left:{CH+PAD_AFTER_AVATAR}px;top:0;height:{CH}px;'
                      f'display:flex;align-items:center;font-family:var(--e);font-weight:600;'
                      f'font-size:{FS}px;color:{INK};white-space:nowrap">{cap}</span></div>')
            pill_boxes.append((label, x, y, pw, CH))
            x += pw + GAP
            idx += 1
            ci += 1
        y += CH + RGAP
        ri += 1

    # Every pill this loop places bleeds SOME edge (left/right always, by
    # construction of the while-conditions above; the first/last row also
    # bleed top/bottom) — bounds_check would otherwise HARD-FAIL every one of
    # them, exactly the false-positive CLAUDE.md's own bleed_tags mechanism
    # exists for. Confirm which ACTUALLY cross an edge and only exempt those
    # (rather than blanket-exempting every pill, which would let a genuine
    # off-canvas bug in an interior pill slip through unseen).
    bleed_labels = [label for (label, ex, ey, ew, eh) in pill_boxes
                    if ex < 0 or ex + ew > W or ey < 0 or ey + eh > H]
    elements.extend(pill_boxes)

    # ----- pinned ink slab (recipe: optional enhancement — see audit note) -----
    slab_text = "126 CAME BACK."
    sub_text = "RETURN VISITS TO PATHER SATHI · 2021–2026"
    m2 = await B.measure_text([{"text": slab_text, "font": "d", "size": 92, "weight": 900,
                                "line_height": .88, "max_width": 700}])
    bw, bh = 748, m2[0]["h"] + 118
    bx, by = (W - bw) / 2, H * 0.42 - bh / 2
    rot = -2.4
    P.append(f'<div class="measure" data-tag="band" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;'
              f'background-color:{INK};border-radius:{core.RADII["outer"]}px;'
              f'transform:rotate({rot}deg);z-index:30;overflow:hidden;padding:40px 44px;'
              f'box-shadow:{core.hard_shadow("xl")},{core.keyline(ring_bg=CREAM, gap=9, ring=3)}">'
              f'<div style="font-family:var(--d);font-weight:900;font-size:92px;line-height:.88;'
              f'letter-spacing:-.02em;color:{CREAM}">{slab_text}</div>'
              f'<div style="font-family:var(--m);font-weight:700;font-size:15px;margin-top:20px;'
              f'letter-spacing:.1em;color:{A[2]}">{sub_text}</div></div>')
    slab_box = lay.rotated_bbox(bx, by, bw, bh, rot)
    elements.append(("band", *slab_box))

    # Any pill genuinely overlapping the slab is intentional (recipe: "pin one
    # rotated ink slab over the field... reads as laid over the pills") — declare
    # each such PAIR explicitly rather than a blanket ignore, so collision_check
    # still catches any pill-vs-pill or pill-vs-logo/footer bug it would
    # otherwise find.
    ignore_pairs = set()
    for (label, ex, ey, ew, eh) in pill_boxes:
        if _overlaps((ex, ey, ew, eh), slab_box):
            ignore_pairs.add(frozenset({label, "band"}))

    # ----- fades so the logo/footer sit on a clean patch of the busy field -----
    # v1 used a 150px/40%-stop fade (60px solid), which left the logo (top:56,
    # height:32 -> spans y56-88) sitting in the fade's own translucent 33% zone,
    # so the first pill row visibly bled through behind the wordmark (real
    # legibility miss caught by the looking gate, not any static check — no gate
    # in §7 checks logo-over-background contrast). Widened to a 190px/60%-stop
    # fade (114px fully solid) so both the logo and the footer sit on 100% cream.
    P.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:190px;'
              f'background:linear-gradient(180deg,{CREAM} 60%,transparent);z-index:50"></div>')
    P.append(f'<div style="position:absolute;left:0;bottom:0;width:{W}px;height:190px;'
              f'background:linear-gradient(0deg,{CREAM} 60%,transparent);z-index:50"></div>')

    # B.logo() hardcodes z-index:20 (build.py, cannot edit engine source) — the
    # widened top fade above is z-index:50, so with the logo at its own z-index it
    # rendered COMPLETELY INVISIBLE (fully opaque cream painted over it, not just
    # faded) the first time this was tried. Wrapping it in a full-canvas
    # position:absolute div at z-index:60 lifts it into a stacking context above
    # the fade while an inset:0 wrapper keeps the <img>'s own top/left anchored
    # exactly where build.logo() put them.
    P.append(f'<div style="position:absolute;inset:0;z-index:60;pointer-events:none">{B.logo()}</div>')
    elements.append(("logo", M, 56, 160, 32))
    footer_txt = "REAL VOICES · REAL WORK"
    P.append(f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);'
              f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{INK};z-index:60">'
              f'@ngo.aquaterra</span>')
    P.append(f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);'
              f'font-weight:700;font-size:14px;letter-spacing:.08em;color:{INK};opacity:.6;'
              f'z-index:60">{footer_txt}</span>')
    elements.append(("footer_l", M, H - 70, 260, 20))
    elements.append(("footer_r", W - M - 260, H - 70, 260, 20))

    html = B.page(W, H, CREAM, "".join(P), grain=False)

    color_pairs = [("field_bg", CREAM, None), ("pill_fill", PILL_FILL, CREAM),
                   ("slab_bg", INK, CREAM)] + [(f"accent{i}", A[i], PILL_FILL) for i in range(7)]

    return html, elements, color_pairs, bleed_labels, ignore_pairs, len(pill_boxes)


async def main():
    html, elements, color_pairs, bleed_labels, ignore_pairs, n_pills = await build()

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=CREAM,
                        core=core, expect_hero=False, bleed_tags=tuple(bleed_labels),
                        collision_ignore=ignore_pairs)
    print(f"preflight bleed-exempt pills: {len(bleed_labels)} / {n_pills}   "
          f"slab-overlap ignore pairs: {len(ignore_pairs)}")

    out = f"{OUT_DIR}/v2.png"
    await B.render(html, out, W, H, elements=elements, color_pairs=color_pairs,
                    page_bg=CREAM, expect_hero=False,
                    bleed_tags=tuple(bleed_labels), collision_ignore=ignore_pairs)
    print("rendered", out)

asyncio.run(main())
