"""AQ EVENTS TEAM recruitment story for STARRY NIGHT, 1080x1920, AQ house style (cream ground, ink, department hue).

Workflow C (design.py drew style 620d62f101b97c, a diagonal fan of cards on a BLACK ground). Adaptations, per the section 2 precedence ladder:
  * Ground is CREAM, not black: a hard brand rule beats the recipe. The recipe's mechanism (a stacked, overlapping card system with one hero and a pinned badge) is kept as
    ONE big ink 'night sky' slab with a sky hard shadow, a sky-block headline that overlaps the type above it, and a moon sticker pinned across the slab's corner.
  * 'Exactly three flat colours': this piece uses cream, ink, sky (the Events department hue, core.accent_for('events')) plus lemon for the stars. Lemon is the fourth.
  * One serif accent word only: 'starry' (Instrument Serif italic), per section 9.
Facts used: AQ runs Starry Night (a Christmas carnival fundraiser, December 2024 and 2.0 in December 2025). NOT supplied and therefore NOT printed: edition number, date, venue, roles, deadline,
application link. The CTA says LINK IN BIO as the AQ convention; change it if the form lives elsewhere. Run: PYTHONIOENCODING=utf-8 python scratchpad/aq_starry_recruit.py"""
import asyncio, os, sys, importlib.util, random
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["story"]; M = 64
INK, CREAM = core.INK, core.CREAM
SKY = core.accent_for("events"); LEMON = core.ACCENTS[2]
els = []
def box(label, x, y, w, h, html, z=10):
    els.append((label, round(x), round(y), round(w), round(h)))
    return f'<div data-tag="{label}" style="position:absolute;left:{round(x)}px;top:{round(y)}px;width:{round(w)}px;height:{round(h)}px;z-index:{z}">{html}</div>'

async def main():
    async with B.session():
        probe = await B.measure_text([{"text": "EVENTS", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "TEAM", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "NIGHT", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "starry", "font": "s", "size": 100, "weight": 400}], W, H)
        ev100, team100, night100, star100 = (p["text_w"] for p in probe)
        ev_size = 100 * (W - 2 * M) / ev100                # EVENTS spans the full measure
        night_size = 100 * 800 / night100                  # NIGHT fills the slab
        starry_size = 100 * 520 / star100
        sz = await B.measure_text([{"text": "JOIN THE", "font": "d", "size": 92, "weight": 900, "transform": "uppercase", "line_height": .9},
                                   {"text": "EVENTS", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "TEAM", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "NIGHT", "font": "d", "size": night_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "starry", "font": "s", "size": starry_size, "weight": 400, "line_height": .9}], W, H)
        join_h, ev_h, team_h, night_h, starry_h = (s["ink_h"] for s in sz)
        team_w = sz[2]["text_w"]
        parts = []
        # logo + eyebrow
        parts.append(f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:34px;z-index:20">'); els.append(("logo", M, 56, 160, 34))
        eb = core.on_cream(SKY, 18)
        parts.append(box("eyebrow", M, 138, 520, 26, f'<div style="font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;color:{eb};display:flex;align-items:center;gap:10px;white-space:nowrap">'
                         f'<span style="width:12px;height:12px;border-radius:50%;background:{eb}"></span>NOW RECRUITING</div>'))
        # headline
        y = 196
        parts.append(box("join", M, y, 640, join_h, f'<div style="font-family:var(--d);font-weight:900;font-size:92px;line-height:.9;text-transform:uppercase;color:{INK};white-space:nowrap">JOIN THE</div>'))
        y += join_h + 14
        parts.append(box("events", M - 4, y, W - 2 * M + 8, ev_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{INK};white-space:nowrap">EVENTS</div>'))
        y += ev_h + 26
        pad_x, pad_y = 40, 22
        bw, bh = team_w + 2 * pad_x, team_h + 2 * pad_y
        parts.append(box("team", M, y, bw, bh, f'<div style="width:100%;height:100%;background:{SKY};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;box-shadow:10px 10px 0 {INK};box-sizing:border-box;'
                         f'display:flex;align-items:center;justify-content:center"><span style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{INK}">TEAM</span></div>', z=11))
        # the sub-line sits to the right of TEAM, lowercase body
        sx = M + bw + 36
        parts.append(box("sub", sx, y + bh / 2 - 48, W - M - sx, 120, f'<div style="font-family:var(--e);font-weight:500;font-size:34px;line-height:1.18;color:{INK}">come run<br>the night<br>with us</div>'))
        y += bh + 70
        # the night slab
        sy0 = y; sh = 1530 - sy0
        sw = W - 2 * M
        slab_inner = []
        sbox = lambda label, x, yy, w, h, html: (els.append((label, M + x, sy0 + yy, w, h)), f'<div data-tag="{label}" style="position:absolute;left:{x}px;top:{yy}px;width:{w}px;height:{h}px">{html}</div>')[1]
        slab_inner.append(sbox("label", 44, 36, 560, 24, f'<div style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.12em;color:{CREAM};white-space:nowrap">THE CHRISTMAS CARNIVAL FUNDRAISER</div>'))
        ty = 150
        slab_inner.append(sbox("starry", 54, ty, 560, starry_h, f'<div style="font-family:var(--s);font-style:italic;font-size:{starry_size:.0f}px;line-height:.9;color:{LEMON};white-space:nowrap">starry</div>'))
        slab_inner.append(sbox("night", 44, ty + starry_h + 10, 820, night_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{night_size:.0f}px;line-height:.86;text-transform:uppercase;color:{CREAM};white-space:nowrap">NIGHT</div>'))
        # stars: fixed sizes, rejection-placed in the free area (seeded, so it is reproducible)
        keep = [(770, 0, 190, 120), (44, 36, 600, 40), (44, ty - 10, 640, starry_h + 20), (36, ty + starry_h, 850, night_h + 30)]
        rnd = random.Random(7); placed = []
        def free(x, yy, s):
            if x < 28 or yy < 28 or x + s > sw - 28 or yy + s > sh - 28: return False
            for kx, ky, kw, kh in keep + placed:
                if x < kx + kw + 18 and x + s > kx - 18 and yy < ky + kh + 18 and yy + s > ky - 18: return False
            return True
        for kind, s, col in (("star", 120, LEMON), ("star", 84, LEMON), ("sparkle", 100, CREAM), ("star", 64, LEMON), ("sparkle", 70, CREAM), ("star", 52, LEMON), ("sparkle", 56, CREAM)):
            for _ in range(4000):
                x, yy = rnd.randint(28, sw - s - 28), rnd.randint(28, sh - s - 28)
                if free(x, yy, s):
                    placed.append((x, yy, s, s)); rot = rnd.randint(-14, 14)
                    slab_inner.append(sbox(f"dd_{kind}{len(placed)}", x, yy, s, s, dd.stamp(kind, col, rot=rot, style="clean"))); break
        for _ in range(14):                                   # tiny solid dots, the far stars
            r = rnd.choice((4, 5, 7))
            for _ in range(2000):
                x, yy = rnd.randint(28, sw - 2 * r - 28), rnd.randint(28, sh - 2 * r - 28)
                if free(x, yy, 2 * r):
                    placed.append((x, yy, 2 * r, 2 * r))
                    slab_inner.append(f'<div style="position:absolute;left:{x}px;top:{yy}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:{CREAM}"></div>'); break
        els.append(("slab", M, sy0, sw, sh))
        parts.append(f'<div data-tag="slab" style="position:absolute;left:{M}px;top:{sy0}px;width:{sw}px;height:{sh}px;background:{INK};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;'
                     f'box-shadow:14px 14px 0 {SKY},14px 14px 0 5px {INK};box-sizing:border-box;z-index:8"><div style="position:absolute;left:-5px;top:-5px;right:-5px;bottom:-5px">{"".join(slab_inner)}</div></div>')
        # moon sticker pinned across the slab's top-right corner
        ms = 190; mx, my = W - M - ms + 26, sy0 - ms // 2 - 6
        moon = (f'<svg viewBox="0 0 100 100" width="{ms}" height="{ms}" style="display:block;overflow:visible"><defs><mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="68" cy="38" r="38" fill="#000"/></mask></defs>'
                f'<circle cx="50" cy="50" r="46" fill="{LEMON}" stroke="{INK}" stroke-width="3.5" mask="url(#mm)" transform="rotate(-18 50 50)"/></svg>')
        parts.append(box("moon", mx, my, ms, ms, moon, z=15))
        # CTA + handle
        cy0 = sy0 + sh + 70
        cta = f'LINK IN BIO'
        parts.append(box("cta", M, cy0, 360, 78, f'<div style="width:100%;height:100%;background:{SKY};border:4px solid {INK};border-radius:999px;box-shadow:{core.hard_shadow("xl")};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:24px;letter-spacing:.1em;color:{INK}">{cta}</div>', z=12))
        parts.append(box("handle", M + 400, cy0 + 24, 400, 30, f'<div style="font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.05em;color:{INK}">@ngo.aquaterra</div>'))
        html = B.page(W, H, "var(--bg)", f'<div style="position:absolute;inset:0;background:var(--bg)"></div>' + "".join(parts), grain=True)
        tp = [("join/events", INK, "var(--bg)", 92, True), ("sub", INK, "var(--bg)", 34, False), ("eyebrow", eb, "var(--bg)", 18, True),
              ("team", INK, SKY, 200, True), ("cta", INK, SKY, 24, True), ("slab label", CREAM, INK, 17, True), ("night", CREAM, INK, 200, True), ("starry", LEMON, INK, 200, False)]
        slab_kids = ("label", "starry", "night") + tuple(e[0] for e in els if e[0].startswith("dd_"))
        os.makedirs("out/aq_events", exist_ok=True)
        await B.render(html, "out/aq_events/starry_recruit_story.png", W, H, elements=els, text_pairs=tp, containers=("slab",), page_bg="var(--bg)", expect_hero=True,
                       collision_ignore=[("moon", "slab"), ("team", "events"), ("team", "sub")] )
        print("bottom of CTA row:", cy0 + 78, "of", H)
asyncio.run(main())
