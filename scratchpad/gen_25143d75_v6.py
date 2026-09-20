import asyncio, os, sys, importlib.util, itertools, math
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); sh = load("shapes")

W, H = 1200, 628          # judged canvas: linkedin (task-assigned, NOT feed)
M = 42                    # matches the reference's own measured ~3.5% margin (compare.geometry)
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

    # ---------- 2. derive sizes from the measurements ----------
    # v2->v3: compare.compare() on v2 scored 0.31 with a BLOCKING "CONTENT TOO SMALL (0.68x
    # reference coverage)" critique (RECREATION_PROTOCOL decision table: scale the whole
    # composition up about the centroid, do not add new elements). area_ratio 0.675 -> need
    # roughly 1/sqrt(0.675) = 1.22x linear scale. Also CENTROID OFF by (+0.07,-0.05): shift
    # the pile left/down.
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

    # footer text: shrink to fit inside the margins if the first guess overflows
    foot_size = 60
    if m_foot["text_w"] * (foot_size/60.0) > (W - 2*M):
        foot_size = int(60 * (W - 2*M) / m_foot["text_w"])
    foot_w = m_foot["text_w"] * (foot_size/60.0)
    foot_h = m_foot["ink_h"] * (foot_size/60.0)

    # ---------- 3. HEADER band (measured, fixed position) ----------
    wm_x, wm_y = M, 34
    wm1_w, wm1_h = wm1["text_w"], wm1["ink_h"]
    wm2_y = wm_y + wm1_h + 8
    wm2_w, wm2_h = wm2["text_w"], wm2["ink_h"]
    dot_x = wm_x + wm2_w + 12
    dot_y = wm2_y + wm2_h/2 - 9
    dot_size = 18
    # on_dark(): the dark-ground contrast decision, MEASURED not eyeballed (see friction doc
    # for the full table). Pink clears AA_NORMAL raw (6.31:1) so on_dark returns it unchanged.
    dot_color = core.on_dark(PINK, dot_size, bold=True)

    wm_block = (wm_x, wm_y, max(wm1_w, wm2_w + 12 + dot_size), (wm2_y + wm2_h) - wm_y)

    CROSS = 54
    cross_x, cross_y = W - M - CROSS, 38
    # outline_of(): the craft-layer-on-dark-field decision (CLAUDE.md bug catalog row
    # "ink outline + hard shadow on an INK field -> invisible"). The reference's ornament
    # is a thin CREAM line on black; outline_of(INK) confirms CREAM is the only legible choice.
    cross_color = core.outline_of(INK)
    cross_box = (cross_x, cross_y, CROSS, CROSS)

    foot_x = (W - foot_w) / 2
    foot_y = H - 46 - foot_h
    foot_box = (foot_x, foot_y - 6, foot_w, foot_h + 12)

    # ---------- 4. THE PILE — scatter_solve, not hand-typed coordinates ----------
    sticker_items = []
    pill_items = []
    unrot = {}        # label -> (w, h, rot)  the CSS/box size the div actually gets
    for key, (txt, w, rot) in pill_specs.items():
        rw, rh = rot_bbox(w, PILL_H, rot)
        pill_items.append((key, rw, rh))
        unrot[key] = (w, PILL_H, rot)
    for key, spec in sticker_specs.items():
        s = spec["size"]; rot = spec["rot"]
        rw, rh = rot_bbox(s, s, rot)
        sticker_items.append((key, rw, rh))
        unrot[key] = (s, s, rot)
    pile_items = sticker_items + pill_items

    # v3->v4: score dropped to 0.219 (no more blocking critique) but the pile still reads as
    # two SEPARATE flanking pill-clusters either side of a sticker row, rather than the
    # reference's tangled single pile (RECREATION_PROTOCOL rule 5: "the engine separates by
    # instinct; reference piles overlap — recreating one requires allow_occlusion intent, not
    # nudging"). scatter_solve's score function only REWARDS contact up to 10% overlap and
    # never penalises full separation, so with a roomy zone it happily spreads out. Tightening
    # the zone forces more of the interleaving the reference actually has.
    # v4->v5: v4's interleaving looked right by eye but the SCORE got WORSE (0.219 -> 0.232):
    # `compare.geometry` on the reference shows row5/col7 (x 67-78%, y 36-45%) is genuinely
    # EMPTY there, and both v3 and v4 kept dropping the LINKEDIN pill into exactly that dead
    # cell. Hard-block it with a keep_out box instead of hoping a different seed avoids it, and
    # duplicate a bottom-half sub-zone in the zones list so scatter_solve samples the
    # bottom band (where the reference is genuinely dense, rows 8-9) more often than a single
    # uniform zone would.
    # v5 first pass over-constrained the solver: a tight zone + a keep_out block + a bottom
    # bias together left no legal spot for 2 of 8 items and scatter_solve HONESTLY reported
    # them unplaced (better than silently overlapping past the limit — but 2 missing pills is
    # a real miss, not an acceptable outcome). Widened the zone back and shrank the dead-zone
    # block to just the worst cell instead of a generous margin around it.
    # v5 SECOND finding: scatter_solve's max_pair_overlap is ONE global ceiling for every
    # pair, but a sticker can absorb far more overlap than a pill can (a sticker's "Drag me"
    # ring repeats itself 4x and its illustration is redundant with the sticker's own
    # silhouette; a pill's ENTIRE box is its one-shot, non-redundant label — the exact
    # "LINKEDIN" -> "LINKED" clipping the previous attempt hit). One knob cannot serve both
    # tolerances at once. Fix: run scatter_solve TWICE — stickers first (looser overlap,
    # they can tangle), then pills with the now-placed stickers passed as `protect` (so a
    # pill MAY dip into a sticker's outer ring up to max_protect_cover, matching the
    # reference's interleaving) while pill-vs-pill overlap stays low enough that no label
    # can be clipped by a sibling pill.
    zone = (int(W*0.05), int(H*0.29), int(W*0.88), int(H*0.55))
    dead_zone_keepout = (int(W*0.68), int(H*0.36), int(W*0.16), int(H*0.10))  # row5/col7 only
    bottom_bias = (int(W*0.05), int(H*0.50), int(W*0.88), int(H*0.34))
    keep_out = [wm_block, cross_box, foot_box, dead_zone_keepout]

    stk_placements, stk_unplaced = lay.scatter_solve(
        sticker_items, W, H, protect=[], keep_out=keep_out, zones=[zone],
        margin=10, max_pair_overlap=0.22, seed=23, tries=1500)
    stk_rw = {l: (rw, rh) for l, rw, rh in sticker_items}
    sticker_boxes_for_protect = []
    for label, rx, ry in stk_placements:
        sticker_boxes_for_protect.append((rx, ry, *stk_rw[label]))

    # v5->v6: max_protect_cover=0.45 let a sticker bury 45% of a pill's label — "INSTAGRAM"
    # rendered as "?AM" behind the pink heart sticker, and resolve_label_z correctly flagged
    # it UNRESOLVED. A pill dipping into a sticker's outer scallop RING (redundant "Drag me"
    # text) is the reference's actual mechanism; a pill buried past its own OUTER EDGE into
    # the sticker's illustrated centre is not. 0.45 was sized for "may touch", not "may hide
    # half the word" — dropped hard.
    pill_placements, pill_unplaced = lay.scatter_solve(
        pill_items, W, H, protect=sticker_boxes_for_protect, max_protect_cover=0.20,
        keep_out=keep_out, zones=[zone, bottom_bias],
        margin=8, max_pair_overlap=0.17, seed=29, tries=5000)

    placements = stk_placements + pill_placements
    unplaced = stk_unplaced + pill_unplaced
    if unplaced:
        print("UNPLACED (scatter_solve could not fit):", unplaced)

    rot_wh = {label: (rw, rh) for label, rw, rh in pile_items}
    pile_boxes = {}   # label -> (x,y,w,h) UNROTATED div box, center-converted
    for label, rx, ry in placements:
        rw, rh = rot_wh[label]
        cx, cy = rx + rw/2, ry + rh/2
        w, h, rot = unrot[label]
        pile_boxes[label] = (cx - w/2, cy - h/2, w, h, rot)

    # ---------- 5. z-order: protect each object's LABEL, not the object (resolve_label_z) ----------
    # Reference: the "tongue" sticker is the front-most (its peel-corner sits on top of
    # everything it overlaps). Seed that ordering, then let resolve_label_z fix any burial
    # scatter_solve's placement introduces.
    z_seed = {"hand": 10, "linkedin": 11, "instagram": 12, "dribbble": 13,
              "behance": 14, "facebook": 15, "heart": 16, "tongue": 20}
    label_boxes = {}
    for key, (x, y, w, h, rot) in pile_boxes.items():
        if key in sticker_specs:
            # the part that MUST stay legible is the centre illustration + ring text,
            # not the outer scalloped rim -> shrink the protected box to the inner ~68%
            pad = w * 0.16
            label_boxes[key] = (x+pad, y+pad, w-2*pad, h-2*pad)
        else:
            label_boxes[key] = (x, y, w, h)   # a pill's label IS the whole pill
    rlz_items = [(k, label_boxes[k], z_seed[k]) for k in pile_boxes]
    new_z, unresolved = lay.resolve_label_z(rlz_items, min_visible=0.80)
    if unresolved:
        print("resolve_label_z: UNRESOLVED (composition must move, not just re-stack):", unresolved)

    # ---------- 6. build the HTML ----------
    parts = []
    # NOTE v1->v2: the page() frame already paints .p's background to INK; this extra
    # full-bleed div duplicated it and reconcile.measure_dom correctly flagged it as an
    # "INVISIBLE FILL" (same colour as what's already behind it) — removed, not a real bug,
    # just a redundant div. See friction doc.

    illustration_boxes = []   # filled below, appended to the gate `elements` list

    # header wordmark (typographic — the reference has no pill/card behind its wordmark
    # either; see AQ ADAPTATION note in brain/RECREATION_AUDIT.md)
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

    text_shadow = f"2px 2px 0 {INK}"  # matte ink text needs no shadow on cream; kept for pills below
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
            # centre illustration — SEPARATE top-level element (never nested inside the
            # sticker's own <svg>: CLAUDE.md bug catalog, "doodles builder inside a bespoke
            # art svg inherits the PARENT viewBox and renders 2-3x oversized").
            ill = w * 0.34
            ix, iy = x + w/2 - ill/2, y + h/2 - ill/2
            if key == "hand":
                inner_svg = dd.stamp("thumbsup", MINT)
            elif key == "tongue":
                inner_svg = dd.stamp("heart", PINK)
            else:  # heart+lightning combo -> the reference's broken heart
                # FOUND WHILE BUILDING v1 (not a documented bug anywhere in CLAUDE.md/DECISIONS.md):
                # build.page()'s global rule `.dood{position:absolute;z-index:4}` means every
                # doodle SVG carries z-index:4 INSIDE whatever local stacking context contains it.
                # A wrapper div with NO transform does not itself form a stacking context, so its
                # child .dood escapes upward and competes at z=4 in the OUTER shared context. A
                # sibling wrapper that DOES have a `transform` (or opacity<1, filter, etc.) forms
                # ITS OWN stacking context, so its z-index:4 child is trapped inside it and the
                # whole subtree participates in the outer context at the WRAPPER's own z-index
                # (auto/0 here) — 0 < 4, so it painted BELOW the other doodle regardless of DOM
                # order. First attempt (no explicit z-index on either wrapper) rendered the
                # lightning bolt completely invisible under the heart. Fix: give every wrapper
                # that stacks more than one doodle an EXPLICIT z-index, so stacking-context
                # isolation can never silently reorder them again.
                inner_svg = (f'<div style="position:absolute;inset:0;z-index:1">{dd.stamp("heart", TOMATO)}</div>'
                            f'<div style="position:absolute;inset:0;z-index:2;transform:scale(0.72) translate(8px,-4px)">'
                            f'{dd.stamp("lightning", INK)}</div>')
            parts.append(f'<div style="position:absolute;left:{ix}px;top:{iy}px;width:{ill}px;'
                         f'height:{ill}px;z-index:{z+1}">{inner_svg}</div>')
            illustration_boxes.append((f"{key}_illustration", ix, iy, ill, ill))
        else:
            txt, _w0, _rot0 = pill_specs[key][0], w, rot
            parts.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'transform:rotate({rot}deg);z-index:{z};display:flex;align-items:center;'
                f'justify-content:center;background:{CREAM};border:4px solid {INK};'
                f'border-radius:999px;box-sizing:border-box">'
                f'<span style="font-family:var(--d);font-weight:900;font-size:{PILL_FONT}px;color:{INK};'
                f'white-space:nowrap">{pill_specs[key][0]}</span></div>')
            color_pairs.append((f"{key}_pill_fill", CREAM, INK))

    parts.append(f'<div style="position:absolute;left:{foot_x}px;top:{foot_y}px;width:{foot_w+4}px;'
                 f'font-family:var(--e);font-weight:600;font-size:{foot_size}px;color:{CREAM};'
                 f'white-space:nowrap;z-index:20">hello@aquaterra.ngo</div>')
    color_pairs.append(("footer_text", CREAM, INK))

    inner = "".join(parts)
    html = B.page(W, H, INK, inner, grain=False)

    # ---------- 7. gate list ----------
    elements = [("wordmark_l1", wm_x, wm_y, wm1_w, wm1_h),
                ("wordmark_l2", wm_x, wm2_y, wm2_w, wm2_h),
                ("wordmark_dot", dot_x, dot_y, dot_size, dot_size),
                ("cross", cross_x, cross_y, CROSS, CROSS),
                ("footer", foot_x, foot_y, foot_w, foot_h)]
    for key, (x, y, w, h, rot) in pile_boxes.items():
        rw, rh = rot_bbox(w, h, rot)
        cx, cy = x + w/2, y + h/2
        elements.append((key, cx - rw/2, cy - rh/2, rw, rh))
    elements.extend(illustration_boxes)

    # v4 found a real gap here: collision_check flagged ('tongue','heart_illustration') even
    # though the two STICKERS themselves (tongue/heart) were correctly in collision_ignore and
    # do not visually overlap at all (confirmed by eye) — a circular sticker's declared bbox is
    # its bounding SQUARE, so two adjacent circles' square corners can overlap on paper with
    # zero real ink touching. An illustration nested inside a sticker inherits that same false-
    # positive risk against every OTHER pile item, not just its own parent, so it needs the
    # same blanket ignore as the stickers/pills themselves.
    pile_keys = list(pile_boxes.keys())
    illu_keys = [lbl for lbl, *_r in illustration_boxes]
    all_keys = pile_keys + illu_keys
    collision_ignore = set(itertools.combinations(all_keys, 2))  # the pile OVERLAPS by design

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=INK,
                       core=core, expect_hero=False,   # a scatter pile has no single hero (layout.dominance_check docstring)
                       collision_ignore=collision_ignore)

    async with B.session():
        issues = await B.render(html, f"{OUTV}/v6.png", W, H, elements=elements,
                                color_pairs=color_pairs, page_bg=INK,
                                collision_ignore=collision_ignore)
    print("render issues:", issues)
    print("done -> ", f"{OUTV}/v6.png")

asyncio.run(main())
