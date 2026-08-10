"""AQ 2026 WORKSHOP CAROUSEL BUILDER — batch mode.

Helper block copied from gen_sunderbans8_carousel_v6.py per brain/CAROUSEL_PLAYBOOK.md
(no frame_border; logo bare with drop-shadow; accent-matched dots; tinted scrims; truthful
index tag). The one change: `spots` are no longer hand-picked — engine/vision.plan_spots
measures each photo's real free zones, per CLAUDE.md §12 (vision.py supersedes manual picking).
"""
import asyncio, base64, os, sys, importlib.util

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core"); B = load("build"); dd = load("doodles"); vision = load("vision")
lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
ROOT = "scratchpad/carousel_2026"


def photo_b64(path):
    ext = "jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "png"
    with open(path, "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()


def logo_pill(x=M, y=48):
    return (f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{x}px;z-index:20;'
            f'height:56px;display:block;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))">')


def dots(n, active, accent="#FFFFFF", x_right=M, y=112):
    out = f'<div style="position:absolute;top:{y}px;right:{x_right}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        c = accent if i == active else "rgba(255,255,255,.35)"
        b = "border:2px solid var(--ink);" if i == active else ""
        out += f'<span style="width:9px;height:9px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"


def footer(loc, date):
    return (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:#FFFFFF;'
            f'text-shadow:0 2px 6px rgba(0,0,0,.5)">@ngo.aquaterra '
            f'<span style="opacity:.75;font-weight:500">&middot; {loc} &middot; {date}</span></div>')


def scrim_bottom(h=260, tint=None):
    layers = 'linear-gradient(to top,rgba(0,0,0,.72),rgba(0,0,0,0))'
    if tint:
        layers = f'linear-gradient(to top,{tint}4D,transparent 65%), ' + layers
    return f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;background:{layers};z-index:10"></div>'


def scrim_top(h=340, tint=None):
    layers = 'linear-gradient(to bottom,rgba(0,0,0,.55),rgba(0,0,0,0))'
    if tint:
        layers = f'linear-gradient(to bottom,{tint}40,transparent 65%), ' + layers
    return f'<div style="position:absolute;top:0;left:0;right:0;height:{h}px;background:{layers};z-index:9"></div>'


def full_bleed_photo(b64):
    return (f'<img src="{b64}" style="position:absolute;inset:0;width:{W}px;height:{H}px;'
            f'object-fit:cover;z-index:1">')


def caption(txt, accent):
    return (f'<div style="position:absolute;bottom:100px;left:{M}px;right:{M}px;z-index:20;'
            f'display:flex;align-items:flex-start;gap:12px">'
            f'<span style="width:18px;height:3px;background:{accent};margin-top:11px;flex:none"></span>'
            f'<span style="font-family:var(--e);font-weight:500;font-size:19px;line-height:1.35;'
            f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">{txt}</span></div>')


def sticker(txt, accent, x, y, rot=-4):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;left:{x}px;top:{y}px;z-index:9;transform:rotate({rot}deg);'
            f'font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{ink};background:{accent};border:2.5px solid var(--ink);border-radius:999px;'
            f'padding:6px 14px;box-shadow:3px 3px 0 var(--ink);white-space:nowrap">{txt}</span>')


def index_tag(page_index, total, accent):
    txt = f"{page_index:02d} / {total:02d}"
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;bottom:140px;right:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:12px;letter-spacing:.08em;color:{ink};background:{accent};'
            f'border:2px solid var(--ink);border-radius:999px;padding:5px 12px;'
            f'box-shadow:2px 2px 0 var(--ink)">{txt}</span>')


def one(kind, x, y, size, fill, rot=0, opacity=1.0, z=8):
    # dd.stamp() per §10 — never the try/except fill= pattern (silently drops colour on the
    # 5 stroke-drawn doodles).
    # The drop-shadow is the craft layer, not decoration: without it a thin stroke laid over a
    # textured wall reads as a scuff mark on the photo rather than as a placed object (caught by
    # the looking gate on learners_den v2).
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'opacity:{opacity};z-index:{z};'
            f'filter:drop-shadow(2px 3px 0 rgba(10,10,10,.85)) drop-shadow(0 0 6px rgba(0,0,0,.35))">'
            f'{dd.stamp(kind, fill, rot=rot, style="clean")}</div>')


def connector(x1, y1, x2, y2, color, opacity=0.5):
    cx1, cy1, cx2, cy2 = x1 + 15, y1 + 15, x2 + 15, y2 + 15
    return (f'<svg style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:7;'
            f'pointer-events:none"><line x1="{cx1}" y1="{cy1}" x2="{cx2}" y2="{cy2}" stroke="{color}" '
            f'stroke-width="2.5" stroke-dasharray="2 8" stroke-linecap="round" opacity="{opacity}"/></svg>')


VOCAB = ["star", "sparkle", "circle", "ring", "plus", "zigzag", "burst", "lightning",
         "spiral", "dots", "speech", "cross", "squiggle", "leaf", "thumbsup", "heart"]
# BLUE-GREEN BIASED ROTATION (user direction, 2026-08-08: "more blue green across all pages").
# Was [4,0,2,5,3,1,6] — sky,pink,lemon,grape,tomato,mint,teal — an even spread across the wheel.
# Now weighted to the cool half: sky / teal / mint / mintbright carry the rotation, grape sits
# between blue and violet as a cool bridge, and ONE warm rung (lemon) is kept deliberately.
# Dropping warm entirely would flatten the whole batch into a single hue and lose the
# punctuation the brand rule asks for — one warm rung in seven keeps the blue-greens reading as
# a choice rather than as a colour cast.
ACCENT_ORDER = [4, 6, 1, 5, 4, 6, 2]
MINTBRIGHT = "#00E5A0"          # in core's tokens but not in ACCENTS; earns its place here
# doodle fills get the extra bright mint so the cool range has a high-key note against dark photos
DOODLE_EXTRA = {2: MINTBRIGHT}  # rung 2 (mint) brightens to mintbright for doodles only
SIZES = [26, 34, 44, 60, 80]


# LARGE-AREA colour is cool-only. slide_accent drives the scrim tint, the active dot, the caption
# rule, the index tag and the type slide's 600x300 field — all big or structural. The one warm rung
# in ACCENT_ORDER is punctuation and must never be handed a large field: a full lemon block on a
# type slide (sentence_secrets v-bg1 slide 3) read as a warm poster, straight against the brief.
# Warm survives only where it is small — doodles and stickers, below.
COOL_ORDER = [4, 6, 1, 5, 6, 4, 1]      # sky, teal, mint, grape, teal, sky, mint


def slide_accent(seed):
    return A[COOL_ORDER[seed % len(COOL_ORDER)]]


def filler_from_vision(photo_path, slide_seed, n=4, exclude=None):
    """Doodle scatter whose POSITIONS are measured (vision) and whose kind/colour/size/rotation
    are derived from slide_seed. Returns (html, bboxes)."""
    spots, info = vision.plan_spots_relaxed(photo_path, W, H, n=n, exclude=exclude,
                                            seed=slide_seed, want=2)
    html, boxes, pts = "", [], []
    for i, s in enumerate(spots):
        kind = VOCAB[(slide_seed * 3 + i * 5) % len(VOCAB)]
        rung = (slide_seed + i) % len(ACCENT_ORDER)
        accent = DOODLE_EXTRA.get(rung, A[ACCENT_ORDER[rung]])
        # size floor of 44: below that a doodle on a busy photo reads as a speck, not punctuation
        size = max(44, min(s["size"], SIZES[(slide_seed + i * 2) % len(SIZES)]))
        rot = ((slide_seed * 37 + i * 53) % 60) - 30
        # Colour: the brand ACCENT is the intent — accept it whenever it clears the local contrast
        # bar, and only fall back otherwise. Handing the full list to pick_visible ranks purely by
        # luminance delta, which picked near-black ink on every bright wall; a thin dark stroke on
        # textured concrete then reads as dirt (§10: decoration must never read as dirt).
        _, ok = vision.pick_visible([accent], s["lum"], core=core, min_delta=42)
        fill = accent if ok else ("#FFFFFF" if s["dark_bg"] else "#0A0A0A")
        html += one(kind, s["x"], s["y"], size, fill, rot=rot)
        boxes.append((f"doodle{i}", s["x"], s["y"], size, size))
        pts.append((s["x"], s["y"]))
    if len(pts) >= 2:
        html += connector(pts[0][0], pts[0][1], pts[1][0], pts[1][1], slide_accent(slide_seed))
    return html, boxes


# Reserved boxes where decoration must never land. These are TIGHT around the actual UI, not
# full-width bands: background_grid only keeps free regions that TOUCH THE TOP EDGE, so a
# full-width top exclude severs every candidate region from the top and starves the photo to
# zero spots (measured: free_fraction 0.004). Exclude the logo and the dots, not the whole strip.
EXCLUDE = [(40, 30, 380, 100),          # logo wordmark
           (840, 90, 200, 55),          # carousel dots
           (0, H - 300, W, 300)]        # caption + index tag + footer scrim


async def render_cover(proj, photo, out_dir, total, seed=0):
    accent = slide_accent(seed)
    fillers, fboxes = filler_from_vision(photo, seed, n=4, exclude=EXCLUDE)
    inner = (full_bleed_photo(photo_b64(photo))
             + scrim_top(340, tint=accent) + scrim_bottom(500, tint=accent)
             + logo_pill()
             + (f'<div style="position:absolute;top:120px;left:{M}px;z-index:20;font-family:var(--m);'
                f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:{accent};'
                f'display:flex;align-items:center;gap:10px;text-shadow:0 2px 6px rgba(0,0,0,.5)">'
                f'<span style="width:10px;height:10px;border-radius:50%;background:{accent}"></span>'
                f'{proj["loc"].upper()} &middot; {proj["date_label"]}</div>')
             + (f'<div style="position:absolute;bottom:230px;left:{M}px;right:{M}px;z-index:20;'
                f'font-family:var(--d);font-weight:900;font-size:{proj.get("title_size",78)}px;line-height:.92;'
                f'text-transform:uppercase;color:#FFFFFF;text-shadow:0 4px 14px rgba(0,0,0,.55)">'
                f'{proj["title_html"]}</div>')
             + (f'<div style="position:absolute;bottom:150px;left:{M}px;right:{M}px;z-index:20;'
                f'display:flex;align-items:flex-start;gap:12px">'
                f'<span style="width:18px;height:3px;background:{accent};margin-top:11px;flex:none"></span>'
                f'<span style="font-family:var(--e);font-weight:500;font-size:20px;line-height:1.35;'
                f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">'
                f'{proj["subhead"]}</span></div>')
             + fillers + footer(proj["loc"], proj["date_label"]))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    lay.preflight(W, H, [b for b in fboxes], html=html, page_bg="var(--bg)", core=core)
    await B.render(html, f"{out_dir}/1_cover.png", W, H)


async def render_slide(proj, photo, idx, total, out_dir, cap, seed, stick=None, extra_exclude=None):
    accent = slide_accent(seed)
    # extra_exclude: per-photo no-go boxes. vision's skin veto protects faces, but HAIR is dark
    # and smooth, so it scores as low-busy background and a doodle can land on a child's head
    # (caught on smile_notes_mba 01.jpg). Until that's a measured rule, name the box explicitly.
    ex = EXCLUDE + list(extra_exclude or [])
    fillers, fboxes = filler_from_vision(photo, seed, n=4, exclude=ex)
    inner = (full_bleed_photo(photo_b64(photo))
             + scrim_bottom(280 if cap else 170, tint=accent)
             + logo_pill() + dots(total, idx - 1, accent=accent) + fillers)
    if stick:
        # stickers go in the guaranteed-dark bottom scrim band (playbook rule 3) — never
        # fought into a cluttered sky pocket where they clip the edge or a shoulder
        inner += sticker(stick, A[ACCENT_ORDER[(seed + 3) % 7]], M, H - 250, rot=-3)
    inner += index_tag(idx, total, accent)
    if cap:
        inner += caption(cap, accent)
    inner += footer(proj["loc"], proj["date_label"])
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    lay.preflight(W, H, [b for b in fboxes], html=html, page_bg="var(--bg)", core=core)
    await B.render(html, f"{out_dir}/{idx+1}_slide.png", W, H)


async def render_type_slide(proj, idx, total, out_dir, kicker, hero, body, seed):
    """A cream typographic slide, for events with too few photographs to carry a whole carousel.

    WHY THIS EXISTS: two 2026 workshops had 1 and 3 usable photos. The alternatives were to pad
    with near-duplicate frames or to fabricate imagery — the real-assets-only rule (§9) forbids
    the second and the looking gate rejects the first. A type slide built from the row's OWN
    key_statistic is honest content, on-brand, and needs no photograph.

    All decoration here is SOLID + ink-outlined + hard-shadowed (§10: never a low-opacity wash),
    and every element is bbox-tracked so preflight can actually see it.
    """
    accent = slide_accent(seed)
    el = []

    KICK_Y, HERO_Y, FS, LH = 214, 268, 104, 0.94
    lines = hero.count("<br>") + 1
    # Space by MEASURED ELEMENT HEIGHT, never by a guessed constant — the §10 bug where a stacked
    # plate spaced by a fixed offset clips its own text. Body position follows the hero's real
    # line count, so a 2-line and a 4-line hero both breathe.
    hero_h = int(lines * FS * LH)
    BODY_Y = HERO_Y + hero_h + 58

    inner = f'<div style="position:absolute;inset:0;background:var(--bg)"></div>'

    inner += (f'<div style="position:absolute;top:{KICK_Y}px;left:{M}px;z-index:6;'
              f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.18em;'
              f'text-transform:uppercase;color:var(--ink)">{kicker}</div>')
    el.append(("kicker", M, KICK_Y, 460, 22))

    # the hero: the row's real statistic, set as the dominant element
    inner += (f'<div style="position:absolute;top:{HERO_Y}px;left:{M}px;right:{M}px;z-index:6;'
              f'font-family:var(--d);font-weight:900;font-size:{FS}px;line-height:{LH};'
              f'text-transform:uppercase;color:var(--ink)">{hero}</div>')
    el.append(("hero", M, HERO_Y, W - 2 * M, hero_h))

    inner += (f'<div style="position:absolute;top:{BODY_Y}px;left:{M}px;right:{M + 120}px;'
              f'z-index:6;display:flex;align-items:flex-start;gap:14px">'
              f'<span style="width:26px;height:4px;background:{accent};margin-top:13px;flex:none;'
              f'border:2px solid var(--ink)"></span>'
              f'<span style="font-family:var(--e);font-weight:500;font-size:23px;line-height:1.45;'
              f'color:var(--ink)">{body}</span></div>')
    el.append(("body", M, BODY_Y, W - 2 * M - 120, 120))

    # The accent field moved from top-right to the BOTTOM band: at top it sat in the hero's
    # column and wide statistics ran straight over it. Down here it anchors the empty lower half
    # instead, and nothing overlaps it.
    FIELD_Y = H - 470
    inner += (f'<div style="position:absolute;top:{FIELD_Y}px;right:0;width:600px;height:300px;'
              f'background:{accent};border-left:5px solid var(--ink);border-top:5px solid var(--ink);'
              f'border-bottom:5px solid var(--ink);z-index:2"></div>')
    el.append(("accent_field", W - 600, FIELD_Y, 600, 300))

    # doodles in the free lower-left field; hand-placed because there is no photograph to run
    # vision over, so the empty zone is known by construction rather than by measurement
    # every spot must end before the accent field's left edge (W-600); the 4th one started at
    # W-520 and preflight correctly flagged it sitting inside the block
    spots = [(M, FIELD_Y + 24, 96, 6), (M + 172, FIELD_Y + 132, 60, 2),
             (M + 286, FIELD_Y + 20, 72, 4), (M + 360, FIELD_Y + 152, 46, 0)]
    for i, (sx, sy, sz, ai) in enumerate(spots):
        kind = VOCAB[(seed * 3 + i * 5) % len(VOCAB)]
        rung = (seed + ai) % len(ACCENT_ORDER)
        col = DOODLE_EXTRA.get(rung, A[ACCENT_ORDER[rung]])
        inner += one(kind, sx, sy, sz, col, rot=((seed * 29 + i * 47) % 60) - 30)
        el.append((f"doodle{i}", sx, sy, sz, sz))

    inner += logo_pill()
    el.append(("logo", M, 48, 300, 56))
    inner += dots(total, idx - 1, accent=accent)
    inner += index_tag(idx, total, accent)
    inner += (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
              f'font-weight:700;font-size:13px;letter-spacing:.06em;color:var(--ink)">@ngo.aquaterra '
              f'<span style="opacity:.6;font-weight:500">&middot; {proj["loc"]} &middot; '
              f'{proj["date_label"]}</span></div>')
    el.append(("footer", M, H - 70, 460, 20))

    html = B.page(W, H, "var(--bg)", inner, grain=False)
    # No collision_ignore: on this layout nothing is SUPPOSED to overlap, so every pair must be
    # a genuine failure. (v1 whitelisted hero/accent_field and thereby hid the real overlap.)
    lay.preflight(W, H, el, html=html, color_pairs=[("accent_field", accent, "var(--bg)")],
                  page_bg="var(--bg)", core=core)
    await B.render(html, f"{out_dir}/{idx+1}_slide.png", W, H)


async def build(proj, version="v1"):
    # photodir defaults to the slug, but the two can differ when the download folder was named
    # before the carousel slug was chosen
    src = f"{ROOT}/{proj.get('photodir', proj['slug'])}/src_images"
    out_dir = f"out/versions/{proj['slug']}_carousel/{version}"
    os.makedirs(out_dir, exist_ok=True)
    picks = proj["picks"]
    types = proj.get("type_slides", [])
    total = 1 + len(proj["slides"]) + len(types)   # cover + photo slides + type slides
    base_seed = proj.get("seed", 0)
    await render_cover(proj, f"{src}/{picks[0]}", out_dir, total, seed=base_seed)
    extra = proj.get("extra_exclude", {})
    i = 0
    for i, (fn, cap, stick) in enumerate(proj["slides"], start=1):
        await render_slide(proj, f"{src}/{fn}", i, total, out_dir, cap, base_seed + i, stick,
                           extra_exclude=extra.get(fn))
    for j, (kicker, hero, body) in enumerate(types, start=i + 1):
        await render_type_slide(proj, j, total, out_dir, kicker, hero, body, base_seed + j)
    print(f"  -> {out_dir}  ({total} slides)")
