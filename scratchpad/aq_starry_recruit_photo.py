"""AQ EVENTS TEAM recruitment story for STARRY NIGHT, PHOTO version (user-supplied DJ-mixer photo), 1080x1920, AQ house style (cream ground, ink, department hue).

Workflow C (design.py drew style 620d62f101b97c, a diagonal fan of cards on a BLACK ground). Adaptations, per the section 2 precedence ladder:
  * Ground is CREAM, not black: a hard brand rule beats the recipe. The recipe's mechanism (a stacked, overlapping card system with one hero and a pinned badge) is kept as
    ONE big ink 'night sky' slab with a sky hard shadow, a sky-block headline that overlaps the type above it, and a moon sticker pinned across the slab's corner.
  * 'Exactly three flat colours': this piece uses cream, ink, sky (the Events department hue, core.accent_for('events')) plus lemon for the stars. Lemon is the fourth.
  * One serif accent word only: 'starry' (Instrument Serif italic), per section 9.
Facts used: AQ runs Starry Night (a Christmas carnival fundraiser, December 2024 and 2.0 in December 2025). NOT supplied and therefore NOT printed: edition number, date, venue, roles, deadline,
application link. The CTA says LINK IN BIO as the AQ convention; change it if the form lives elsewhere. Photo version: the ink night-sky slab is replaced by a framed, tilted photo card of the user's DJ-mixer photo (hands on a mixer, no faces), cropped so the 'Pioneer DJ' brand mark along the
photo's bottom edge is OUT of frame; a starry-night sticker and the moon are pinned to the card. Run: PYTHONIOENCODING=utf-8 python scratchpad/aq_starry_recruit_photo.py"""
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
        # the photo card
        import base64, io, math
        from PIL import Image
        im = Image.open(os.path.join("engine", "assets", "img", "events", "starry-night-recruit", "dj_mixer.jpg")).convert("RGB"); im.thumbnail((1500, 2250))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=88); photo_uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        cy_top = y; ch = 640; cw = W - 2 * M - 20; cx0 = M + 4; TILT = -2.5
        parts.append(f'<div data-tag="photo" style="position:absolute;left:{cx0}px;top:{cy_top}px;width:{cw}px;height:{ch}px;box-sizing:border-box;background:{INK};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;'
                     f'box-shadow:14px 14px 0 {SKY},14px 14px 0 5px {INK};overflow:hidden;transform:rotate({TILT}deg);z-index:8">'
                     f'<img src="{photo_uri}" style="width:100%;height:100%;object-fit:cover;object-position:50% 58%;filter:brightness(1.18) contrast(1.06) saturate(1.1);display:block"></div>')
        a_ = math.radians(abs(TILT)); bw_ = cw * math.cos(a_) + ch * math.sin(a_); bh_ = cw * math.sin(a_) + ch * math.cos(a_)
        els.append(("photo", round(cx0 + cw / 2 - bw_ / 2), round(cy_top + ch / 2 - bh_ / 2), round(bw_), round(bh_)))
        sy0, sh = cy_top, ch
        # starry-night sticker pinned over the card's bottom-left corner (ink tag, serif accent word 'starry')
        tw, th = 400, 196; tx, ty = M - 18, cy_top + ch - th + 44
        parts.append(box("tag", tx, ty, tw, th, f'<div style="width:100%;height:100%;background:{INK};border:5px solid {CREAM};border-radius:{core.RADII["outer"]}px;box-shadow:0 0 0 4px {INK},10px 10px 0 4px {INK};box-sizing:border-box;'
                         f'transform:rotate(4deg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0"><span style="font-family:var(--s);font-style:italic;font-size:96px;line-height:.9;color:{LEMON};margin-bottom:16px">starry</span>'
                         f'<span style="font-family:var(--d);font-weight:900;font-size:76px;line-height:.9;text-transform:uppercase;color:{CREAM}">NIGHT</span></div>', z=16))
        # mono label above the card's top-left
        parts.append(box("label", M, cy_top - 44, 620, 24, f'<div style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.12em;color:{INK};white-space:nowrap">THE CHRISTMAS CARNIVAL FUNDRAISER</div>'))
        # moon sticker across the card's top-right corner
        ms = 190; mx, my = W - M - ms + 40, cy_top - ms // 2 - 14
        moon = (f'<svg viewBox="0 0 100 100" width="{ms}" height="{ms}" style="display:block;overflow:visible"><defs><mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="68" cy="38" r="38" fill="#000"/></mask></defs>'
                f'<circle cx="50" cy="50" r="46" fill="{LEMON}" stroke="{INK}" stroke-width="3.5" mask="url(#mm)" transform="rotate(-18 50 50)"/></svg>')
        parts.append(box("moon", mx, my, ms, ms, moon, z=15))
        # loose stars on the cream, in measured free zones
        for lbl, kind, sx_, sy_, sz, col, rot in (("dd_star1", "star", 880, 52, 76, LEMON, -10), ("dd_star2", "star", 860, cy_top + ch + 70, 88, LEMON, 12), ("dd_sparkle1", "sparkle", 720, cy_top + ch + 44, 64, INK, 0)):
            parts.append(box(lbl, sx_, sy_, sz, sz, dd.stamp(kind, col, rot=rot, style="clean"), z=14))
        y = cy_top + ch + 60
        # CTA + handle
        cy0 = y + 20
        cta = f'LINK IN BIO'
        parts.append(box("cta", M, cy0, 360, 78, f'<div style="width:100%;height:100%;background:{SKY};border:4px solid {INK};border-radius:999px;box-shadow:{core.hard_shadow("xl")};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:24px;letter-spacing:.1em;color:{INK}">{cta}</div>', z=12))
        parts.append(box("handle", M + 400, cy0 + 24, 230, 30, f'<div style="font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.05em;color:{INK}">@ngo.aquaterra</div>'))
        html = B.page(W, H, "var(--bg)", f'<div style="position:absolute;inset:0;background:var(--bg)"></div>' + "".join(parts), grain=True)
        tp = [("join/events", INK, "var(--bg)", 92, True), ("sub", INK, "var(--bg)", 34, False), ("eyebrow", eb, "var(--bg)", 18, True),
              ("team", INK, SKY, 200, True), ("cta", INK, SKY, 24, True), ("tag NIGHT", CREAM, INK, 76, True), ("tag starry", LEMON, INK, 96, False), ("label", INK, "var(--bg)", 17, True)]
        os.makedirs("out/aq_events", exist_ok=True)
        await B.render(html, "out/aq_events/starry_recruit_photo_story.png", W, H, elements=els, text_pairs=tp, containers=(), page_bg="var(--bg)", expect_hero=True,
                       collision_ignore=[("moon", "photo"), ("tag", "photo"), ("team", "events"), ("team", "sub"), ("moon", "sub"), ("moon", "label")] )
        print("bottom of CTA row:", cy0 + 78, "of", H)
asyncio.run(main())
