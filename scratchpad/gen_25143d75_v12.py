import asyncio, os, sys, importlib.util, itertools, math
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); sh = load("shapes")

# ============================================================================
# v10 — DIAGNOSIS FROM THE PARENT SESSION'S BRIEF (confirmed correct by re-
# looking at the reference, see scratchpad/friction5/f2514b.md for the full
# writeup):
#
#   v6 (accepted at 0.169, clean looking gate, "every element present and
#   correctly proportioned") had TWO real defects that "present + proportioned"
#   never asks about:
#
#   1. ARRANGEMENT: v6 used layout.scatter_solve twice (stickers, then pills)
#      which SORTED the pile into two tidy horizontal bands — 3 round stickers
#      in a row above, 5 pills in a row below. The reference INTERLEAVES both
#      families into ONE pile at varied heights/angles (instagram/dribbble/
#      behance pills sit BETWEEN and AMONG the stickers vertically, not below
#      them as a group). Same inventory, different geometry — RECREATION_
#      PROTOCOL.md's "WHEN THE REGION ROWS ARE LYING TO YOU" names this exact
#      failure mode by this exact slug.
#   2. FOOTER: v6's footer is a contained, centred, high-contrast cream line
#      at ~6% of canvas height. The reference's footer is a FULL-BLEED,
#      LOW-CONTRAST (measured: text-stroke gray ~rgb(98) vs bg rgb(32), NOT
#      full CREAM at full opacity) wash that spans margin-to-margin and runs
#      up into/behind the pile's bottom row, occupying ~18% of the canvas
#      height (compare.geometry: rows 10-11 of 11, y 0.818-1.0).
#
# THIS BUILD DOES NOT USE scatter_solve. Per this session's brief and per
# scatter_solve's own docstring (added by a prior session after this same
# lesson): it finds *a* legal layout, not *the reference's*. All 8 pile
# object centers below are read directly off the reference image with a
# fractional grid overlay (scratchpad/_ref_grid.png, 5% gridlines) and cross-
# checked against compare.geometry's 9x11 occupancy table. layout.resolve_label_z
# is still used — that is a z-ORDER fix (which object paints in front), not a
# PLACEMENT solver, and its docstring makes no "authoring vs recreation" claim.
# ============================================================================

W, H = 1200, 628          # judged canvas: linkedin (task-assigned)
M = 42                    # matches the reference's own ~3.5% margin
INK = core.INK; CREAM = core.CREAM
PINK = core.ACCENTS[0]; MINT = core.ACCENTS[1]; TOMATO = core.ACCENTS[3]

SLUG = "25143d758ea743"
OUTV = f"out/versions/{SLUG}"
os.makedirs(OUTV, exist_ok=True)

def rot_bbox(w, h, deg):
    return lay.rotated_bbox(0, 0, w, h, deg)[2:4]  # (rw, rh)

async def main():
    # ---------- 1. MEASURE every string first (build.measure_text, never guess) ----------
    items = [
        {"text": "AQUATERRA", "font": "m", "size": 24, "weight": 700, "letter_spacing": "0.16em", "transform": "uppercase"},
        {"text": "find us online", "font": "m", "size": 13, "weight": 500, "letter_spacing": "0.12em", "transform": "uppercase"},
        {"text": "LINKEDIN", "font": "d", "size": 26, "weight": 900},
        {"text": "INSTAGRAM", "font": "d", "size": 26, "weight": 900},
        {"text": "DRIBBBLE", "font": "d", "size": 26, "weight": 900},
        {"text": "BEHANCE", "font": "d", "size": 26, "weight": 900},
        {"text": "FACEBOOK", "font": "d", "size": 26, "weight": 900},
        {"text": "hello@aquaterra.ngo", "font": "e", "size": 60, "weight": 600},
    ]
    m = await B.measure_text(items, W, H)
    (wm1, wm2, m_link, m_insta, m_drib, m_beh, m_fb, m_foot) = m

    # ---------- 2. sizes — UNCHANGED from v6. v6's SCALE/area_ratio (0.918) and
    # gyration_ratio (0.95) were already inside RECREATION_PROTOCOL's tolerance
    # band and the accepted checklist marked "sizes correct" — the defect was
    # arrangement, not scale. Re-deriving sizes from scratch would risk
    # re-breaking something that already worked. ----------
    SCALE = 1.22
    PILL_H = round(62 * SCALE)
    PAD = round(30 * SCALE)
    pill_specs = {
        "linkedin":  ("LINKEDIN",  m_link["text_w"]  * SCALE + 2*PAD, -13),
        "instagram": ("INSTAGRAM", m_insta["text_w"] * SCALE + 2*PAD,   6),
        "dribbble":  ("DRIBBBLE",  m_drib["text_w"]  * SCALE + 2*PAD,   7),
        "behance":   ("BEHANCE",   m_beh["text_w"]   * SCALE + 2*PAD,   9),
        "facebook":  ("FACEBOOK",  m_fb["text_w"]    * SCALE + 2*PAD,   8),
    }
    PILL_FONT = round(26 * SCALE)
    sticker_specs = {
        "hand":  {"size": round(185*SCALE), "rot": -8},
        "tongue":{"size": round(215*SCALE), "rot": 2},
        "heart": {"size": round(180*SCALE), "rot": -3},
    }

    # ---------- 3. HEADER band (measured, fixed position — unchanged from v6;
    # the accepted checklist marked the header correct) ----------
    wm_x, wm_y = M, 34
    wm1_w, wm1_h = wm1["text_w"], wm1["ink_h"]
    wm2_y = wm_y + wm1_h + 8
    wm2_w, wm2_h = wm2["text_w"], wm2["ink_h"]
    dot_x = wm_x + wm2_w + 12
    dot_y = wm2_y + wm2_h/2 - 9
    dot_size = 18
    dot_color = core.on_dark(PINK, dot_size, bold=True)

    wm_block = (wm_x, wm_y, max(wm1_w, wm2_w + 12 + dot_size), (wm2_y + wm2_h) - wm_y)

    CROSS = 54
    cross_x, cross_y = W - M - CROSS, 38
    cross_color = core.outline_of(INK)
    cross_box = (cross_x, cross_y, CROSS, CROSS)

    # ---------- 4. FOOTER — REBUILT. compare.geometry on the reference puts the
    # footer band at y 0.818-1.0 (18.2% of canvas height), spanning the full
    # content width (x 0.035-0.967, i.e. margin to margin, NOT centred/narrower
    # like v6). Direct pixel sampling of the reference
    # (scratchpad/_ref_bottom_full.png + a gray histogram) found the footer
    # text stroke sits at ~rgb(98) against a ~rgb(32) background — a LOW-
    # CONTRAST wash, not full-opacity cream (which the pile objects' outlines
    # actually use). Rendered here as CREAM text at reduced opacity so it
    # reads as the same atmospheric wash, sized to fill the full margin-to-
    # margin width (drives the font size UP to "giant", matching the
    # reference's mechanism), and positioned so its top edge runs up behind
    # the pile's lowest row (matching "runs through the bottom of the pile").
    #
    # KNOWN GATE BLIND SPOT (flagging per this session's brief, not fixing —
    # engine/*.py is off-limits): layout.text_contrast_check evaluates the
    # DECLARED colour pair (CREAM vs INK, ~17:1, passes easily) and has no way
    # to see the CSS opacity that actually makes this low-contrast on the
    # rendered page. The check is correctly silent here (nothing is actually
    # illegible - the wash is a deliberate atmospheric effect, not body copy)
    # but it means "low contrast" as a compositional choice is invisible to
    # the whole static gate stack; only the looking gate catches whether a
    # wash reads as a wash. See friction report.
    foot_avail_w = W - 2*M
    foot_size = 60
    scale_to_fit = foot_avail_w / m_foot["text_w"]
    foot_size = 60 * scale_to_fit
    foot_w = m_foot["text_w"] * (foot_size/60.0)
    foot_h = m_foot["ink_h"] * (foot_size/60.0)
    # target: bounding footprint (with typical descender room) ~18% of H
    target_footprint = 0.18 * H
    if foot_h < target_footprint * 0.75:
        # ink_h alone (cap-height to baseline) under-reports the full glyph
        # box for a lowercase string with descenders/ascenders; measure_text's
        # own docs (CLAUDE.md §6) say ink_h is the CONTENT box, not the total
        # glyph box — scale up modestly to approximate the descender room a
        # string like "hello@aquaterra.ngo" (g, @) actually needs.
        adjust = (target_footprint * 0.82) / foot_h
        foot_size *= adjust
        foot_w = m_foot["text_w"] * (foot_size/60.0)
        foot_h = m_foot["ink_h"] * (foot_size/60.0)
    foot_x = M
    foot_y = H - 34 - foot_h   # small bottom margin, matches ref's ~5.5% bottom margin
    foot_box = (foot_x, foot_y - foot_h*0.35, foot_w, foot_h * 1.55)  # generous box: includes ascender/descender room the ink_h box misses, for the gate's own bookkeeping

    # ---------- 5. THE PILE — hand-placed from the reference, NOT scatter_solve.
    # Centers read off scratchpad/_ref_grid.png (5% gridlines) and cross-checked
    # against compare.geometry's 9x11 occupancy grid; rotations kept from the
    # step-1 written inventory (already close to the reference by eye in v6 —
    # that part was never the problem). Values are (center_x_frac, center_y_frac)
    # as a FRACTION OF THE FULL CANVAS, matching how compare.geometry itself
    # reports fractions, so the two are directly comparable when re-scored.
    #
    # The reference's actual vertical interleave, top to bottom by object TOP
    # edge: instagram (topmost) -> hand -> dribbble -> behance/tongue (mid) ->
    # heart -> linkedin/facebook (bottom row). v6's mistake was grouping all
    # 3 stickers into one visual row above all 5 pills; here instagram sits
    # ABOVE the hand sticker's midline, dribbble is level with hand's lower
    # half, behance sits BELOW tongue's top edge tucked into its own gap, and
    # facebook/heart sit at the pile's bottom edge running into the footer —
    # exactly the tangle-vs-grid distinction RECREATION_PROTOCOL calls out.
    # v10->v11->v12 REFINEMENT HISTORY:
    # v10 (first pass, 5%-grid read): score 0.225 (worse than v6's 0.169).
    # v11 (2%-grid re-read): 0.215. Both still flagged REGION UNDER-filled at
    # row7/col7 (x 0.667-0.778, y 0.545-0.636, ref coverage 0.96 vs ours 0.04-
    # 0.08) — a real, large gap, not noise.
    # v12: re-measured with a 1%-grid, labels burned INTO each crop (the 2%
    # pass had gridline labels cropped off outside the visible frame, which
    # silently produced WRONG numbers for "heart" — see friction report).
    # That exposed a genuine mistake: "heart" (the broken-heart sticker) is
    # NOT at the far right (x~0.88) as the two coarser reads both said — it
    # sits at x~0.62-0.855 (center ~0.74), well left of where two independent
    # coarse reads put it. The far-right space (x 0.86-0.97) in the reference
    # is empty pile-wise; only the top-right CROSS ornament (a separate,
    # already-correct element) lives out there. Moving "heart" left is what
    # closes the row7/col7 gap: FACEBOOK's right edge + heart's left edge
    # jointly cover it, matching the reference.
    pile_centers = {
        # stickers
        "hand":      (0.220, 0.475),
        "tongue":    (0.400, 0.655),
        "heart":     (0.740, 0.645),
        # pills — deliberately interleaved with the stickers' vertical range,
        # not grouped below them
        "linkedin":  (0.220, 0.745),
        "instagram": (0.420, 0.430),
        "dribbble":  (0.655, 0.440),
        "behance":   (0.540, 0.500),
        "facebook":  (0.575, 0.660),
    }

    unrot = {}        # label -> (w, h, rot)  the CSS/box size the div actually gets
    for key, (txt, w, rot) in pill_specs.items():
        unrot[key] = (w, PILL_H, rot)
    for key, spec in sticker_specs.items():
        unrot[key] = (spec["size"], spec["size"], spec["rot"])

    pile_boxes = {}   # label -> (x,y,w,h,rot)  UNROTATED div box (top-left + size)
    for key, (fx, fy) in pile_centers.items():
        w, h, rot = unrot[key]
        cx, cy = fx * W, fy * H
        pile_boxes[key] = (cx - w/2, cy - h/2, w, h, rot)

    # sanity: nothing may clip off-canvas or collide with the header/cross/
    # footer keepout zones — checked here (a raw print, not a gate) before
    # ever rendering, so a bad hand-measurement is caught before spending a
    # render+look cycle on it.
    def rect_overlap(a, b):
        ax, ay, aw, ah = a; bx, by, bw, bh = b
        return not (ax+aw < bx or bx+bw < ax or ay+ah < by or by+bh < ay)
    for key, (x, y, w, h, rot) in pile_boxes.items():
        rw, rh = rot_bbox(w, h, rot)
        cx, cy = x + w/2, y + h/2
        rx, ry = cx - rw/2, cy - rh/2
        if rx < 0 or ry < 0 or rx+rw > W or ry+rh > H:
            print(f"WARNING pre-check: {key} rotated bbox off-canvas: {(rx,ry,rw,rh)}")
        if rect_overlap((rx, ry, rw, rh), wm_block):
            print(f"WARNING pre-check: {key} overlaps header keepout")
        if rect_overlap((rx, ry, rw, rh), cross_box):
            print(f"WARNING pre-check: {key} overlaps cross keepout")

    # ---------- 6. z-order: protect each object's LABEL, not the object
    # (resolve_label_z) — a z-ORDER fix, not a placement solver, kept from v6.
    # Front-to-back read off the reference: tongue sits most in front (its
    # peel-corner detail is only visible because it is drawn ON TOP of
    # whatever it touches), then heart, then the pill chain, hand furthest
    # back (linkedin's top edge tucks slightly under it in the reference).
    z_seed = {"hand": 10, "linkedin": 11, "instagram": 12, "dribbble": 13,
              "behance": 14, "facebook": 15, "heart": 18, "tongue": 20}
    label_boxes = {}
    for key, (x, y, w, h, rot) in pile_boxes.items():
        if key in sticker_specs:
            pad = w * 0.16
            label_boxes[key] = (x+pad, y+pad, w-2*pad, h-2*pad)
        else:
            label_boxes[key] = (x, y, w, h)
    rlz_items = [(k, label_boxes[k], z_seed[k]) for k in pile_boxes]
    new_z, unresolved = lay.resolve_label_z(rlz_items, min_visible=0.80)
    if unresolved:
        print("resolve_label_z: UNRESOLVED (composition must move, not just re-stack):", unresolved)

    # ---------- 7. build the HTML ----------
    parts = []
    illustration_boxes = []

    parts.append(f'<div style="position:absolute;left:{wm_x}px;top:{wm_y}px;font-family:var(--m);'
                 f'font-weight:700;font-size:24px;letter-spacing:0.16em;text-transform:uppercase;'
                 f'color:{CREAM};z-index:20">AQUATERRA</div>')
    parts.append(f'<div style="position:absolute;left:{wm_x}px;top:{wm2_y}px;font-family:var(--m);'
                 f'font-weight:500;font-size:13px;letter-spacing:0.12em;text-transform:uppercase;'
                 f'color:{CREAM};opacity:.72;z-index:20">find us online</div>')
    parts.append(f'<div style="position:absolute;left:{dot_x}px;top:{dot_y}px;width:{dot_size}px;'
                 f'height:{dot_size}px;z-index:20">{dd.stamp("circle", dot_color)}</div>')

    parts.append(f'<div style="position:absolute;left:{cross_x}px;top:{cross_y}px;width:{CROSS}px;'
                 f'height:{CROSS}px;z-index:20">{dd.stamp("plus", cross_color)}</div>')

    color_pairs = [("wordmark", CREAM, INK), ("tagline", CREAM, INK), ("dot", dot_color, INK),
                   ("cross", cross_color, INK)]

    # footer FIRST in DOM / lowest z among content (z=3, still above the .p
    # page background at z=0 but below every pile object at z>=10) so the
    # pile's bottom row paints OVER it where they meet, matching the
    # reference (the pile is drawn after/on top of the footer line there).
    parts.append(f'<div style="position:absolute;left:{foot_x}px;top:{foot_y}px;width:{foot_w+4}px;'
                 f'font-family:var(--e);font-weight:600;font-size:{foot_size:.1f}px;color:{CREAM};'
                 f'opacity:0.4;white-space:nowrap;z-index:3">hello@aquaterra.ngo</div>')
    color_pairs.append(("footer_text", CREAM, INK))

    for key in ["hand", "linkedin", "tongue", "instagram", "dribbble", "behance", "facebook", "heart"]:
        if key not in pile_boxes:
            continue
        x, y, w, h, rot = pile_boxes[key]
        z = new_z[key]
        if key in sticker_specs:
            path = sh.scallop(lobes=14 if key != "heart" else 16, r=46)
            svg = sh.sticker(path, CREAM, size=int(w), halo=True, shadow=False, rot=rot,
                             outline=INK, detail="inner",
                             inner=sh.text_on_arc("DRAG ME • DRAG ME • DRAG ME • DRAG ME • ",
                                                   r=37, size=6.2, fill=INK, box=100, start="2%"))
            parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                         f'z-index:{z}">{svg}</div>')
            color_pairs.append((f"{key}_sticker_fill", CREAM, INK))
            ill = w * 0.34
            ix, iy = x + w/2 - ill/2, y + h/2 - ill/2
            if key == "hand":
                inner_svg = dd.stamp("thumbsup", MINT)
            elif key == "tongue":
                inner_svg = dd.stamp("heart", PINK)
            else:  # heart+lightning combo -> the reference's broken heart
                # z-index:4 stacking-context bug from v1 (see brain/RECREATION_
                # AUDIT.md): explicit z-index on BOTH wrappers, never rely on
                # DOM order when one sibling has a transform.
                inner_svg = (f'<div style="position:absolute;inset:0;z-index:1">{dd.stamp("heart", TOMATO)}</div>'
                            f'<div style="position:absolute;inset:0;z-index:2;transform:scale(0.72) translate(8px,-4px)">'
                            f'{dd.stamp("lightning", INK)}</div>')
            parts.append(f'<div style="position:absolute;left:{ix}px;top:{iy}px;width:{ill}px;'
                         f'height:{ill}px;z-index:{z+1}">{inner_svg}</div>')
            illustration_boxes.append((f"{key}_illustration", ix, iy, ill, ill))
        else:
            parts.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'transform:rotate({rot}deg);z-index:{z};display:flex;align-items:center;'
                f'justify-content:center;background:{CREAM};border:4px solid {INK};'
                f'border-radius:999px;box-sizing:border-box">'
                f'<span style="font-family:var(--d);font-weight:900;font-size:{PILL_FONT}px;color:{INK};'
                f'white-space:nowrap">{pill_specs[key][0]}</span></div>')
            color_pairs.append((f"{key}_pill_fill", CREAM, INK))

    inner = "".join(parts)
    html = B.page(W, H, INK, inner, grain=False)

    # ---------- 8. gate list ----------
    elements = [("wordmark_l1", wm_x, wm_y, wm1_w, wm1_h),
                ("wordmark_l2", wm_x, wm2_y, wm2_w, wm2_h),
                ("wordmark_dot", dot_x, dot_y, dot_size, dot_size),
                ("cross", cross_x, cross_y, CROSS, CROSS),
                ("footer", foot_box[0], foot_box[1], foot_box[2], foot_box[3])]
    for key, (x, y, w, h, rot) in pile_boxes.items():
        rw, rh = rot_bbox(w, h, rot)
        cx, cy = x + w/2, y + h/2
        elements.append((key, cx - rw/2, cy - rh/2, rw, rh))
    elements.extend(illustration_boxes)

    pile_keys = list(pile_boxes.keys())
    illu_keys = [lbl for lbl, *_r in illustration_boxes]
    all_keys = pile_keys + illu_keys
    collision_ignore = set(itertools.combinations(all_keys, 2))  # the pile OVERLAPS by design
    # the footer deliberately runs UNDER the pile's bottom row (that IS the
    # reference's mechanism) — declare it, don't let a real design choice
    # report as an accidental "doodle dropped over text" bug.
    for k in all_keys:
        collision_ignore.add((k, "footer"))
        collision_ignore.add(("footer", k))

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=INK,
                       core=core, expect_hero=False,
                       collision_ignore=collision_ignore)

    async with B.session():
        issues = await B.render(html, f"{OUTV}/v12.png", W, H, elements=elements,
                                color_pairs=color_pairs, page_bg=INK,
                                collision_ignore=collision_ignore)
    print("render issues:", issues)
    print("done -> ", f"{OUTV}/v12.png")

asyncio.run(main())
