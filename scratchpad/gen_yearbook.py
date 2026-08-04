import asyncio, os, sys, json, base64, importlib.util

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)

def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); T = load("tex")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
INK_ON = core.INK_ON

def snap(v): return round(v / 8) * 8

def b64_img(path, mime="image/png"):
    # file:// <img src> silently fails in Playwright's set_content-rendered page (Chromium
    # blocks local-resource loads from an about:blank origin) — embed as a data: URI instead,
    # same as core._b64 does for the engine's own LOGO/PHOTOS/FONTS. See layout.img_src_check.
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

PEOPLE = [
    dict(name="Maanvi Bhandari", dept="Marketing", superlative="Trendsetter",
         quote="I'm not great at the advice — can I interest you in a sarcastic comment?", img="p01.png"),
    dict(name="Vanshika Saraf", dept="Marketing", superlative="Content Curator",
         quote="Capturing moments and creating memories.", img="p02.png"),
    dict(name="Aadhya Jain", dept="Marketing", superlative="Campus Lore",
         quote="Not everyone's cup of tea — or the plot twist is that she actually does it.", img="p03.png"),
    dict(name="Aryan Ahmed", dept="Social Media", superlative="Impact Catalyst",
         quote="Somehow it always works out.", img="p04.png"),
    dict(name="Asmita Roy", dept="Social Media", superlative="Creative Menace",
         quote="Proof that being chronically online can take you places as well.", img="p05.png"),
    dict(name="Aarav Gupta", dept="Social Media", superlative="Digital Maestro",
         quote="Create what others imagine.", img="p06.png"),
    dict(name="Rajveer Pandey", dept="Social Media", superlative="Mr. Dependable",
         quote="Jack of all trades.", img="p07.png"),
    dict(name="Prishita Biyani", dept="Social Media", superlative="Pragmatic Caretaker",
         quote="Love is shown in what we do.", img="p08.png"),
    dict(name="Aanchal Dubey", dept="Projects", superlative="(Un)reliable Source",
         quote="To catch a bus, you've gotta think like a bus.", img="p09.png"),
    dict(name="Anant Goyal", dept="Projects", superlative="Adulting Hurts",
         quote="The only reward for good work is more work.", img="p10.png"),
]

# Vertical crop anchor per photo (object-position Y%) — riso_photo_wrap defaults to dead center,
# which is wrong whenever a person's face isn't exactly mid-height in their source photo (a
# portrait-oriented source forced into this wide card frame only shows a horizontal BAND of it).
# Only overridden where the default center crop was cutting into a face/chin; everyone else's
# source photo happens to center well already.
OBJECT_POS = {
    "p07.png": "50% 55%",  # center between his face and his hands, now that the taller frame has room for both
    "p08.png": "50% 55%",  # center between her face and her hands/torso
}

# Frame height per photo (default 600px, matching every other card) — object-position only PANS
# the crop window, it can't make the window itself taller. At the default 600px frame, ~49% of
# the source's height is visible (a fairly tight crop). Bumped for these two so more of the body
# is visible alongside the face, not just a closer headshot. panel_h is computed FROM this (see
# build_card), so raising it here automatically keeps the card's bottom margin correct.
FRAME_H = {
    "p07.png": 720,
    "p08.png": 720,
}

DOODLES = ["star", "sparkle", "burst", "zigzag", "spiral", "plus", "lightning"]
PHOTO_DIR = os.path.abspath("scratchpad/yearbook/photos")

def chip(txt, accent, x, y, rot=0, dark_border=False):
    # dark_border: the chip sits on the ink panel, not cream — an ink border/shadow would be
    # invisible against it (exactly the class layout.invisible_color_check guards against for
    # solid fills; a chip's own border needs the same care). Use the cream surface color instead.
    fg = "#0A0A0A" if accent in INK_ON else "#fff"
    edge = "var(--bg)" if dark_border else "var(--ink)"
    return (f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;background:{accent};color:{fg};'
            f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.06em;text-transform:uppercase;'
            f'padding:10px 18px;border-radius:999px;border:3px solid {edge};box-shadow:4px 4px 0 {edge};'
            f'transform:rotate({rot}deg);z-index:11;white-space:nowrap">{txt}</div>')

def chip_flow(txt, accent, rot=0, dark_border=False):
    # non-absolute twin of chip() for use inside a flex-flow container (the ink panel), where
    # normal document flow — not manual (x,y) — is what guarantees no overlap.
    fg = "#0A0A0A" if accent in INK_ON else "#fff"
    edge = "var(--bg)" if dark_border else "var(--ink)"
    return (f'<div style="display:inline-block;background:{accent};color:{fg};'
            f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.06em;text-transform:uppercase;'
            f'padding:10px 18px;border-radius:999px;border:3px solid {edge};box-shadow:4px 4px 0 {edge};'
            f'transform:rotate({rot}deg);white-space:nowrap">{txt}</div>')

def doodle(kind, x, y, size, accent, rot=0, z=15):
    fn = getattr(dd, kind, dd.star)
    try: inner = fn(fill=accent, rot=rot)
    except TypeError:
        try: inner = fn(stroke=accent, rot=rot)
        except TypeError: inner = fn(rot=rot)
    return f'<div style="position:absolute;top:{snap(y)}px;left:{snap(x)}px;width:{size}px;height:{size}px;z-index:{z}">{inner}</div>'

def photo_wrap(src, tint, object_pos="50% 50%"):
    # riso_photo_wrap hardcodes object-position:center — fine when a face happens to sit at
    # mid-height, wrong otherwise (see OBJECT_POS above). Same halftone/tint treatment, with a
    # controllable crop anchor.
    return (f'<div style="position:relative;width:100%;height:100%;overflow:hidden">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{object_pos};'
            f'filter:grayscale(1) contrast(1.2) brightness(1.05)">'
            f'<div style="position:absolute;inset:0;background:{tint};mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;background-image:radial-gradient(#00000055 1.2px,transparent 1.6px);'
            f'background-size:5px 5px;mix-blend-mode:multiply;opacity:.4"></div></div>')

def build_card(i, person, total):
    accent = A[i % len(A)]
    tick_accent = A[(i + 3) % len(A)]
    doodle_kind = DOODLES[i % len(DOODLES)]
    fg_on_accent = "#0A0A0A" if accent in INK_ON else "#fff"
    img_path = os.path.join(PHOTO_DIR, person["img"])
    img_uri = b64_img(img_path, "image/png")

    # Dense, ink-panel treatment: the photo up top, then a solid ink block (same move
    # stacked_zones uses) carries name + chips + quote — no bland flat-cream gap, real
    # color/weight in the lower half instead of empty margin.
    frame_x, frame_y, frame_w, frame_h = M, 120, W - 2 * M, FRAME_H.get(person["img"], 600)
    panel_x, panel_y, panel_w = M, frame_y + frame_h + 28, W - 2 * M
    panel_h = H - panel_y - M  # bottom margin matches the side margins regardless of frame_h
    pad = 44

    # Content inside the panel is a CENTERED FLEX COLUMN, not manually-positioned absolute
    # children. A fixed-height panel with absolutely-positioned children left a large dead void
    # below a short quote (all the panel's slack pooled in one spot, because the quote box was
    # sized for the longest possible quote, not the actual one) — flex + justify-content:center
    # distributes whatever slack exists evenly above/below instead, and CSS normal flow makes
    # child-vs-child collision structurally impossible, so name/chips/quote don't need manual
    # (x,y) bookkeeping or a collision_ignore entry between each other.
    elements = [
        ("photo_frame", frame_x, frame_y, frame_w, frame_h),
        ("kicker", M, 56, 380, 24),
        ("index_chip", W - M - 150, 44, 150, 40),
        ("panel", panel_x, panel_y, panel_w, panel_h),
        ("panel_doodle", panel_x + panel_w - 96, panel_y + panel_h - 96, 72, 72),
    ]

    color_pairs = [
        ("panel", "var(--ink)", "var(--bg)"),
        ("dept_chip", accent, "var(--ink)"),
        ("superlative_chip", tick_accent, "var(--ink)"),
        ("index_chip_bg", "var(--ink)", "var(--bg)"),
    ]

    photo = photo_wrap(img_uri, accent + "55", object_pos=OBJECT_POS.get(person["img"], "50% 50%"))

    panel_content = "".join([
        f'<div style="font-family:var(--d);font-weight:900;font-size:68px;line-height:1.04;'
        f'text-transform:uppercase;color:{accent}">{person["name"]}</div>',
        f'<div style="display:flex;gap:16px;flex-wrap:wrap">'
        f'{chip_flow(person["dept"], accent, rot=-2, dark_border=True)}'
        f'{chip_flow(person["superlative"], tick_accent, rot=1.5, dark_border=True)}</div>',
        f'<div style="font-family:var(--s);font-style:italic;font-size:30px;line-height:1.36;'
        f'color:var(--bg)">&ldquo;{person["quote"]}&rdquo;</div>',
    ])

    inner = "".join([
        f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
        # kicker + index (top row)
        f'<span style="position:absolute;top:56px;left:{M}px;font-family:var(--m);font-weight:700;font-size:14px;'
        f'letter-spacing:.14em;text-transform:uppercase;color:var(--ink);z-index:20">3-month reflection &middot; 2025</span>',
        f'<div style="position:absolute;top:44px;right:{M}px;background:var(--ink);color:var(--bg);'
        f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.08em;padding:8px 16px;'
        f'border-radius:999px;z-index:20">{i+1:02d} / {total:02d}</div>',
        # photo frame — thick outline, offset shadow, halftone riso photo (craft layer)
        f'<div style="position:absolute;left:{frame_x}px;top:{frame_y}px;width:{frame_w}px;height:{frame_h}px;'
        f'border-radius:24px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden;z-index:5">{photo}</div>',
        doodle(doodle_kind, frame_x + frame_w - 56, frame_y - 34, 84, tick_accent, rot=-8, z=16),
        # ink panel carrying name + chips + quote, vertically centered
        f'<div style="position:absolute;left:{panel_x}px;top:{panel_y}px;width:{panel_w}px;height:{panel_h}px;'
        f'background:var(--ink);border-radius:24px;box-shadow:10px 10px 0 rgba(10,10,10,0.28);z-index:4;'
        f'display:flex;flex-direction:column;justify-content:center;gap:30px;'
        f'padding:{pad}px;box-sizing:border-box">{panel_content}</div>',
        doodle(DOODLES[(i + 2) % len(DOODLES)], panel_x + panel_w - 96, panel_y + panel_h - 96, 72, accent, rot=6, z=12),
    ])

    html = B.page(W, H, "var(--bg)", inner, grain=True)
    return html, elements, color_pairs

def build_cover(total):
    # Cover slide: the giant title as the one hero move, but backed by real content instead of
    # empty cream — a clustered pile of the actual team's headshots (this IS a yearbook; the
    # faces are the point) up top, and a roster strip of all 10 names/accents at the bottom so
    # the cover previews exactly what the carousel contains.
    hero_accent = A[0]
    tick_accent = A[3]
    content_w = W - 2 * M

    title_y = 620
    rule_y = title_y + 300
    meta_y = rule_y + 52
    roster_y = 1080
    footer_y = 1234

    # photo pile — ALL 10 team photos now (was 6), bigger and more overlapping, spanning the
    # whole upper band instead of one quadrant. "More happening" = more of the actual team
    # visible up front, not more abstract decoration.
    cluster = lay.cluster_positions(10, 640, 380, 58, 92, overlap_frac=0.46,
                                     rng=__import__("random").Random(11))
    pile_people = PEOPLE
    pile_html = ""
    pile_elements = []
    for j, ((cx, cy, r), pperson) in enumerate(zip(cluster, pile_people)):
        d = int(r * 2)
        x, y = int(cx - r), int(cy - r)
        img_uri = b64_img(os.path.join(PHOTO_DIR, pperson["img"]), "image/png")
        tint = A[j % len(A)] + "55"
        photo = photo_wrap(img_uri, tint, object_pos=OBJECT_POS.get(pperson["img"], "50% 50%"))
        pile_html += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
                       f'border-radius:50%;border:5px solid var(--ink);box-shadow:6px 6px 0 var(--ink);'
                       f'overflow:hidden;z-index:{6+j}">{photo}</div>')
        pile_elements.append((f"pile_{j}", x, y, d, d))

    # scattered confetti dots behind/around the pile — small, varied accent colors, low-key
    # energy filler (the sanctioned "more doodles" move, not a new kind of element)
    confetti_specs = [
        (140, 250, 14, A[1]), (200, 560, 10, A[5]), (900, 150, 12, A[6]),
        (940, 520, 16, A[2]), (300, 130, 10, A[4]), (860, 340, 10, A[0]),
    ]
    confetti_html = "".join(
        f'<div style="position:absolute;left:{cx}px;top:{cy}px;width:{cd}px;height:{cd}px;'
        f'border-radius:50%;background:{cc};border:2.5px solid var(--ink);z-index:5"></div>'
        for cx, cy, cd, cc in confetti_specs
    )

    # roster strip — one small chip per person, same accent rotation the cards use, so the
    # cover previews the whole set instead of just naming a count. All 10 first names don't fit
    # on one row at a legible size (measured: ~1080px needed vs ~950px available) — wrap to two
    # rows of 5 rather than silently truncating the roster (a cover reading "10 profiles" should
    # actually preview all 10, not 8).
    roster_html = ""
    roster_elements = []
    row_h = 56
    for k, p in enumerate(PEOPLE):
        row, col = divmod(k, 5)
        a = A[k % len(A)]
        label = p["name"].split()[0]
        w_est = 26 + len(label) * 11
        rx = M + col * 190
        ry = roster_y + row * row_h
        roster_html += chip(label, a, rx, ry, rot=(-2 if k % 2 == 0 else 1.5))
        roster_elements.append((f"roster_{k}", rx, ry, w_est, 48))

    elements = [
        ("kicker", M, 68, 380, 24),
        *pile_elements,
        ("badge", M, title_y - 62, 420, 44),
        ("doodle_sparkle", 60, 480, 54, 54),
        ("doodle_star", 940, 660, 58, 58),
        ("doodle_zigzag", 940, 1010, 60, 60),
        ("title", M, title_y, content_w, 300),
        ("rule", M, rule_y, content_w, 3),
        ("meta", M, meta_y, content_w, 30),
        *roster_elements,
        ("footer_rule", M, footer_y, content_w, 1),
        ("footer_index", M, footer_y + 22, 260, 24),
        ("footer_doodle", W - M - 44, footer_y + 8, 44, 44),
    ]
    color_pairs = [("rule", "var(--ink)", "var(--bg)"), ("badge", hero_accent, "var(--bg)")]

    inner = "".join([
        f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
        f'<span style="position:absolute;top:68px;left:{M}px;font-family:var(--m);font-weight:700;font-size:14px;'
        f'letter-spacing:.14em;text-transform:uppercase;color:var(--ink);z-index:20">3-month reflection &middot; 2025</span>',
        f'<div style="position:absolute;top:56px;right:{M}px;background:var(--ink);color:var(--bg);'
        f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.08em;padding:8px 16px;'
        f'border-radius:999px;z-index:20">COVER</div>',
        confetti_html,
        pile_html,
        doodle("burst", 640 + 92 - 16, 380 - 92 - 16, 68, hero_accent, rot=-6, z=20),
        doodle("sparkle", 60, 480, 54, A[5], rot=12, z=20),
        doodle("star", 940, 660, 58, A[2], rot=-14, z=20),
        doodle("zigzag", 940, 1010, 60, A[6], rot=4, z=20),
        # energetic stat badge, tucked beside the title
        chip("10 people &middot; 1 quarter &middot; 0 chill", hero_accent, M, title_y - 62, rot=-2),
        # giant title, one accent glyph, a slight tilt for energy
        f'<div style="position:absolute;left:{M}px;top:{title_y}px;width:{content_w}px;font-family:var(--d);'
        f'font-weight:900;font-size:120px;line-height:0.96;text-transform:uppercase;color:var(--ink);z-index:12;'
        f'transform:rotate(-1.2deg);transform-origin:left center">'
        f'the<br>team<span style="color:{hero_accent}">.</span></div>',
        f'<div style="position:absolute;left:{M}px;top:{rule_y}px;width:{content_w}px;height:3px;background:var(--ink);opacity:.85;z-index:10"></div>',
        f'<div style="position:absolute;left:{M}px;top:{meta_y}px;width:{content_w}px;font-family:var(--s);'
        f'font-style:italic;font-size:30px;color:var(--ink);z-index:12">a 3-month reflection, ten people, one chaotic quarter.</div>',
        roster_html,
        f'<div style="position:absolute;left:{M}px;top:{footer_y}px;width:{content_w}px;height:1px;background:rgba(10,10,10,0.18);z-index:10"></div>',
        f'<span style="position:absolute;left:{M}px;top:{footer_y+22}px;font-family:var(--m);font-weight:700;'
        f'font-size:13px;letter-spacing:.1em;color:var(--ink);opacity:.6;z-index:12">{total:02d} profiles follow &rarr;</span>',
        doodle("arrow", W - M - 44, footer_y + 4, 44, tick_accent, rot=90, z=12),
    ])
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    cover_ignore = frozenset(frozenset({a[0], b[0]}) for i2, a in enumerate(pile_elements)
                              for b in pile_elements[i2+1:])
    cover_ignore |= frozenset(frozenset({"kicker", e[0]}) for e in pile_elements)
    # "title" is tracked as its FULL two-line bounding box for bounds_check purposes, but "THE"
    # (line 1) is short — doodle_star sits at x940+ in the box's empty right margin, nowhere
    # near the actual glyphs. Confirmed by eye, not guessed. See layout.collision_check's own
    # docstring: this is the same class of intentional-overlap-with-a-container exception.
    cover_ignore |= {frozenset({"doodle_star", "title"})}
    return html, elements, color_pairs, cover_ignore

async def main():
    out_dir = "out/versions/yearbook_hr_2025"
    os.makedirs(out_dir, exist_ok=True)
    total = len(PEOPLE)
    all_clean = True

    html, elements, color_pairs, cover_ignore = build_cover(total)
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                        page_bg="var(--bg)", core=core, expect_hero=True,
                        collision_ignore=cover_ignore)
    if not pf["clean"]:
        all_clean = False
    await B.render(html, f"{out_dir}/card_00_cover.png", W, H)
    print(f"[cover     ] {'THE TEAM':20s} -> {out_dir}/card_00_cover.png  clean={pf['clean']}")

    # panel is a background CONTAINER for these — real, intentional nesting, not a collision
    # (the same pattern layout.collision_check's own docstring calls out: "a chip tucked under
    # a hero on purpose").
    panel_children = frozenset({frozenset({"panel", "panel_doodle"})})

    for i, person in enumerate(PEOPLE):
        html, elements, color_pairs = build_card(i, person, total)
        pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                            page_bg="var(--bg)", core=core, expect_hero=True,
                            collision_ignore=panel_children)
        if not pf["clean"]:
            all_clean = False
        out_path = f"{out_dir}/card_{i+1:02d}.png"
        await B.render(html, out_path, W, H)
        print(f"[{i+1:02d}/{total:02d}] {person['name']:20s} -> {out_path}  clean={pf['clean']}")
    print("ALL CLEAN" if all_clean else "SOME ISSUES — see per-card preflight output above")

asyncio.run(main())
