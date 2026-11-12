"""AQ recruitment v4, welfare + HR group (4 pieces, feed 1080x1350).

  welfare_1  style 62f8cc4d3c6135  staggered pills bleeding off both edges; real programme names + edition numbers. Lane welfare, tier T1.
  welfare_2  style a99a4af4caa8fc  numbered photos on dashed leaders round a mixed serif/sans headline. Lane welfare, tier T1.
  welfare_3  style d375fd7dbcf69c  stylised Kolkata map, star markers on curved routes, one torn diagonal headline strip. Lane welfare, tier T3.
  hr_1       style d91402fc3c0f43  dashboard stack: hero figure over a grid of metric cards. Lane hr (teal), tier T2.

ADAPTATIONS (precedence ladder, CLAUDE.md section 2):
  * welfare_1: the reference's avatar+sentence pills became programme-name+edition pills (real AQ names). Pill field sits on cream, not the
    reference's beige-pink; a quarter of the pills are filled mint so the lane colour carries. The slab headline uses one italic serif line (<=1 accent run).
  * welfare_2: recipe's "mixed serif word + bold sans word" is "540+" (NeutralFace) + "drives" (the one Instrument Serif accent word). Photos get the AQ
    ink outline + hard shadow (craft layer) instead of the reference's clean-cut no-shadow product shots. The circular arrow button is replaced by the url pill.
    Each photo carries a short real-fact label because the numbers alone would say nothing.
  * welfare_3: recipe wants a coloured grained ground; this one is the INK ground (so the mint lane colour reads) with a mint land mass, using B.page grain.
    Travel-time tags became real project counts per place (platform psv, merged spelling variants). Map is hand-drawn and NOT to scale; no real cartography.
    Route colour family = lemon; torn labels cream/ink only; the headline strip is the largest element.
  * hr_1: the reference is a mockup of three phones; only the mechanism (hero figure, pill row, card grid, one saturated card) is used, on the cream ground.
    One accent card is teal (the HR lane colour). Colour count exceeds "one saturated" only by the lane chip and series tab.
Companion art piece (CLAUDE.md standing rule) is OUTSTANDING: not produced here, the dispatching session owns it.
"""
import os, sys, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
core, B, V = K.core, K.B, K.V
INK, CREAM, PAPER = K.INK, K.CREAM, K.PAPER
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = K.PINK, K.MINT, K.LEM, K.TOM, K.SKY, K.GRAPE, K.TEAL
t, box = K.t, K.box
only = sys.argv[1:] or ["welfare_1", "welfare_2", "welfare_3", "hr_1"]

def ink_text(fill): return core.text_on(fill)

# =============================================================== welfare_1: pills
def welfare_1():
    progs = [("tails and treats", "53"), ("sharbat seva", "33"), ("grow green", "26"), ("wear and share", "22"),
             ("food for all", "17"), ("book basket", "16"), ("wear & write", "15"), ("respect and reach", "8"),
             ("smile notes campaign", ""), ("cookie pass on drive", ""), ("colours of durga", "")]
    dots = [MINT, LEM, SKY, PINK, MINT, TOM, GRAPE]
    rows = []; y0, pitch, ph = 204, 88, 70; nrows = 11
    els = []
    for r in range(nrows):
        seq = []
        for i in range(9):
            k = (r * 3 + i * 4 + (r // 2)) % len(progs)
            seq.append((progs[k], k + r + i))
        pills = ""
        for (name, num), s in seq:
            filled = (s % 4 == 0)
            bg = MINT if filled else PAPER
            fg = ink_text(MINT) if filled else INK
            dot = "" if filled else f'<span style="width:34px;height:34px;border-radius:50%;background:{dots[s % len(dots)]};border:3px solid {INK};flex:none"></span>'
            tag = (f'<span style="font-family:var(--m);font-weight:700;font-size:22px;background:{INK};color:{LEM};border-radius:999px;padding:3px 12px">{num}</span>' if num else "")
            pills += (f'<div style="display:flex;align-items:center;gap:14px;height:{ph}px;box-sizing:border-box;padding:0 {14 if num else 28}px 0 {14 if not filled else 28}px;'
                      f'border:3px solid {INK};border-radius:999px;background:{bg};box-shadow:4px 4px 0 {INK};white-space:nowrap;flex:none;'
                      f'font-family:var(--e);font-weight:600;font-size:28px;color:{fg}">{dot}{name}{tag}</div>')
        off = -(120 + (r * 173) % 330)
        rows.append(f'<div data-tag="row" style="position:absolute;left:{off}px;top:{y0 + r * pitch}px;display:flex;gap:20px;z-index:3">{pills}</div>')
    # slab
    sw, sh, sx, sy, rot = 880, 372, 100, 520, -5
    slab = (f'<div data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;background:{INK};border-radius:22px;'
            f'box-shadow:0 0 0 8px {CREAM},14px 14px 0 8px {INK};transform:rotate({rot}deg);z-index:12;padding:36px 44px">'
            f'<div style="font-family:var(--d);text-transform:uppercase;font-weight:900;font-size:104px;line-height:.92;color:{CREAM};letter-spacing:-.01em">53 rounds<br>of biscuits.</div>'
            f'<div style="font-family:var(--s);font-style:italic;font-size:50px;line-height:1.05;color:{core.on_dark(MINT, 50)};margin-top:14px">no dog has left a review.</div>'
            f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.05em;color:{core.on_dark(LEM, 16)};margin-top:14px">tails and treats, edition 53 &nbsp;/&nbsp; since january 2022</div></div>')
    els += [("slab",) + (sx - 20, sy - 30, sw + 40, sh + 60)]
    inner = [K.logo(), K.lane_chip("welfare"), K.series_tab(), *rows, slab,
             t("applications are open.", 64, 1172, 20, color=INK, font="m", weight=700, ls=.04, tag="ask", z=22),
             K.url_pill(y=1206)]
    html = K.page("".join(inner))
    return K.render("welfare_1", html, elements=[("logo", 64, 48, 190, 40)], text_pairs=[("slab_h", CREAM, INK, 104, True), ("ask", INK, "var(--bg)", 20, True)],
                    bleed_tags=("row",), containers=())

# =============================================================== welfare_2: numbered photos
def welfare_2():
    shots = [  # n, key, x, y, w, h, rot, caption, fx, fy, badge side
        (1, "sharbat_cup", 70, 196, 250, 310, -4, "sharbat seva: 33 editions, up to 20 L a round", .5, .5, "r"),
        (2, "bananas_group", 392, 214, 310, 230, 3, "food for all: 5,400 bananas in one round", .6, .5, "l"),
        (3, "plant", 760, 190, 250, 320, 4, "grow green: 26 editions, 100 saplings in one round", .5, .45, "l"),
        (4, "old_age", 62, 890, 250, 240, -3, "respect and reach (old age home): 8 editions", .5, .5, "r"),
        (5, "books", 368, 910, 290, 210, 2, "book basket: 16 editions", .5, .55, "l"),
        (6, "clothes_pile", 712, 884, 290, 250, -2, "wear and share: 22 editions", .5, .5, "l")]
    P = []
    grid = "".join(box(150 + i * 130, 160, 2, 1010, "background:#E4DDC8;", z=1) for i in range(7))
    P.append(grid)
    for n, key, x, y, w, h, rot, cap, fx, fy, side in shots:
        im = K.cover(K.PH[key], w, h, fx, fy)
        bx = w - 22 if side == "r" else -24
        leader = (f'<svg style="position:absolute;left:{(w - 52) if side == "r" else 8}px;top:-34px;z-index:5" width="60" height="60" viewBox="0 0 60 60">'
                  f'<path d="{"M12 8 C 40 4, 46 30, 40 52" if side == "r" else "M52 8 C 22 4, 14 30, 20 52"}" stroke="{INK}" stroke-width="3" stroke-dasharray="5 5" fill="none" stroke-linecap="round"/></svg>')
        badge = (f'<div style="position:absolute;left:{bx}px;top:-34px;width:46px;height:46px;border-radius:50%;background:{MINT};border:3px solid {INK};box-shadow:3px 3px 0 {INK};'
                 f'font-family:var(--m);font-weight:700;font-size:22px;line-height:40px;text-align:center;color:{ink_text(MINT)};z-index:6">{n}</div>')
        label = (f'<div style="position:absolute;left:10px;top:{h - 14}px;width:{w - 10}px;background:{PAPER};border:3px solid {INK};box-shadow:4px 4px 0 {INK};border-radius:12px;'
                 f'padding:6px 10px;box-sizing:border-box;font-family:var(--e);font-weight:600;font-size:17px;line-height:21px;color:{INK};z-index:4">{cap}</div>')
        P.append(f'<div data-tag="shot" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:3">'
                 f'<img src="{K.uri(im)}" style="width:{w}px;height:{h}px;border:4px solid {INK};box-sizing:border-box;border-radius:14px;box-shadow:6px 6px 0 {INK};display:block;object-fit:cover">{leader}{badge}{label}</div>')
    P += [t("this is what", 64, 604, 22, color=INK, font="m", weight=700, ls=.08, upper=True, tag="eyebrow", z=8),
          t("540+", 56, 624, 170, color=INK, font="d", weight=900, ls=-.02, upper=True, lh=170, tag="hero", z=8),
          t("drives", 506, 590, 206, color=core.on_cream(MINT, 206), font="s", italic=True, lh=214, tag="serif", z=8),
          t("look like. mostly bananas.", 520, 806, 36, color=INK, font="e", weight=500, tag="sub", z=8)]
    P += [K.logo(), K.lane_chip("welfare"), K.series_tab(), K.url_pill(y=1206)]
    html = K.page("".join(P))
    return K.render("welfare_2", html, elements=[("logo", 64, 48, 190, 40)], bleed_tags=(),
                    text_pairs=[("hero", INK, "var(--bg)", 196, True), ("sub", INK, "var(--bg)", 40, False), ("serif", core.on_cream(MINT, 206), "var(--bg)", 206, True)])

# =============================================================== welfare_3: map
def _counts():
    c = collections.Counter()
    for l in open("scratchpad/welfare_projects_2026-10-19.psv"):
        p = l.rstrip("\n").split("|")
        if len(p) < 2: continue
        n = p[1].lower()
        for k in ["salt lake", "howrah", "lake town", "beleghata", "science city", "bhawanipore", "new alipore", "ballygunge", "sundarban", "sunderban", "tetultala"]:
            if k in n: c[k] += 1
    c["sunderbans"] = c["sundarban"] + c["sunderban"]
    return c

def star_svg(cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * .46
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    p = " ".join(pts)
    return (f'<polygon points="{p}" fill="{CREAM}" stroke="{CREAM}" stroke-width="{r * .34:.1f}" stroke-linejoin="round"/>'
            f'<polygon points="{p}" fill="{fill}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')

def torn(w, h, seed, amp=5):
    rnd = random.Random(seed); pts = []
    n = max(6, w // 28)
    for i in range(n + 1): pts.append((w * i / n, rnd.uniform(0, amp)))
    for i in range(n, -1, -1): pts.append((w * i / n, h - rnd.uniform(0, amp)))
    return "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts) + ")"

def welfare_3():
    c = _counts()
    dests = [  # name, tag, starx, stary, size, colour, labelx, labely
        ("lake town", c["lake town"], 400, 262, 54, SKY, 450, 236),
        ("salt lake", c["salt lake"], 900, 300, 62, PINK, 610, 350),
        ("beleghata", c["beleghata"], 960, 520, 46, TOM, 690, 470),
        ("howrah", c["howrah"], 98, 540, 58, GRAPE, 150, 450),
        ("science city", c["science city"], 950, 890, 54, LEM, 600, 850),
        ("bhawanipore", c["bhawanipore"], 100, 1030, 50, TOM, 60, 1084),
        ("new alipore", c["new alipore"], 380, 1130, 52, GRAPE, 430, 1090),
        ("sunderbans", c["sunderbans"], 950, 1140, 54, PINK, 770, 972)]
    if "salt lake" not in c: pass
    anchor = (470, 960, 72)
    # --- background svg: land, river, roads, routes, stars
    land = "M-20 175 L1100 175 L1100 1360 L-20 1360 Z"
    river = "M200 175 C 250 350, 150 520, 220 700 S 330 950, 420 1100 S 560 1260, 640 1360"
    svg = [f'<svg style="position:absolute;left:0;top:0;z-index:2" width="1080" height="1350" viewBox="0 0 1080 1350">',
           f'<path d="{land}" fill="{MINT}"/>']
    # district outlines, roads
    for d in ["M-20 330 C 200 300, 420 380, 620 330 S 960 260, 1100 300", "M-20 780 C 220 840, 420 760, 640 820 S 960 900, 1100 840",
              "M620 175 C 600 400, 700 560, 640 760 S 700 1000, 760 1360", "M1000 175 C 960 380, 1040 560, 990 760",
              "M330 175 C 360 330, 340 440, 400 560 S 460 700, 420 820", "M-20 1180 C 200 1200, 420 1150, 640 1220 S 960 1260, 1100 1230"]:
        svg.append(f'<path d="{d}" stroke="{CREAM}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    svg.append(f'<ellipse cx="780" cy="470" rx="90" ry="44" fill="{INK}" stroke="{CREAM}" stroke-width="5" transform="rotate(-18 780 470)"/>')   # a lake
    svg.append(f'<path d="{river}" stroke="{CREAM}" stroke-width="64" fill="none" stroke-linecap="round"/><path d="{river}" stroke="{INK}" stroke-width="52" fill="none" stroke-linecap="round"/>')
    svg.append(f'<path d="M640 1300 C 700 1290, 780 1320, 860 1360" stroke="{INK}" stroke-width="30" fill="none"/>')
    # routes
    ax, ay, ar = anchor
    for name, n, sx, sy, sz, col, lx, ly in dests:
        mx, my = (sx + ax) / 2, (sy + ay) / 2
        dx, dy = sx - ax, sy - ay
        nx, ny = -dy * .22, dx * .22
        svg.append(f'<path d="M{ax} {ay} Q {mx + nx:.0f} {my + ny:.0f} {sx} {sy}" stroke="{LEM}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    for name, n, sx, sy, sz, col, lx, ly in dests: svg.append(star_svg(sx, sy, sz, col))
    svg.append(star_svg(ax, ay, ar, LEM)); svg.append("</svg>")
    P = [box(0, 0, 1080, 1350, f"background:{INK};", z=0), "".join(svg)]
    # labels
    els = []
    def label(text, tag, x, y, seed):
        w = int(len(text) * 19.5 + 40); h1 = 50
        tg = f"{tag} projects" if tag != "" else ""
        tw = int(len(tg) * 15 + 30)
        out = (f'<div data-tag="lbl" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:9;filter:drop-shadow(5px 5px 0 {INK})">'
               f'<div style="width:{w}px;height:{h1}px;background:{CREAM};clip-path:{torn(w, h1, seed)};font-family:var(--d);font-weight:900;font-size:30px;line-height:{h1}px;'
               f'text-align:center;text-transform:uppercase;color:{INK}">{text}</div>'
               f'<div style="margin:6px 0 0 {w - tw - 8}px;width:{tw}px;height:38px;background:{INK};border:3px solid {CREAM};box-sizing:border-box;font-family:var(--m);font-weight:700;'
               f'font-size:15px;line-height:32px;text-align:center;color:{CREAM};letter-spacing:.04em">{tg}</div></div>')
        els.append((text, x, y, w, 104))
        return out
    for i, (name, n, sx, sy, sz, col, lx, ly) in enumerate(dests): P.append(label(name, n, lx, ly, i + 3))
    P.append(label("kolkata", 558, 610, 940 if False else 860, 99).replace("projects", "logged") if False else "")
    # headline strip
    sw, sh, sx0, sy0 = 1240, 250, -80, 615
    strip = (f'<div data-tag="strip" style="position:absolute;left:{sx0}px;top:{sy0}px;width:{sw}px;height:{sh}px;transform:rotate(-7deg);z-index:14;filter:drop-shadow(10px 10px 0 {INK})">'
             f'<div style="width:{sw}px;height:{sh}px;background:{CREAM};clip-path:{torn(sw, sh, 41, 12)}"></div>'
             f'<div style="position:absolute;left:104px;top:14px;white-space:nowrap;font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:124px;line-height:1;color:{INK};letter-spacing:-.01em">205 places.</div>'
             f'<div style="position:absolute;left:108px;top:140px;white-space:nowrap;font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:58px;line-height:1;color:{INK}">the map is a suggestion.</div>'
             f'<div style="position:absolute;left:110px;top:206px;white-space:nowrap;font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.04em;color:{INK}">205 distinct locations across 558 logged projects, june 2021 to september 2026</div></div>')
    els.append(("strip", 60, 560, 980, 360))
    P += [strip, K.logo_pill(dark=True), K.lane_chip("welfare", y=122), K.series_tab(), K.url_pill(y=1206, bg=INK, fg=LEM)]
    html = B.page(1080, 1350, INK, "".join(P), grain=True)
    # kolkata label placed after (anchor)
    return K.render("welfare_3", html, elements=els, bleed_tags=("strip",),
                    text_pairs=[("strip", INK, CREAM, 150, True)], crop_tags=("lbl",))

# =============================================================== hr_1: dashboard
def hr_1():
    P = [K.logo(), K.lane_chip("hr"), K.series_tab()]
    P.append(t("students on the roster, all aged 14 to 19", 64, 190, 20, color=INK, font="m", weight=700, ls=.05, upper=True, tag="eyebrow", z=8))
    P.append(t(f'1,400<span style="color:{core.on_cream(TEAL, 258)}">+</span>', 64, 242, 258, color=INK, font="d", weight=900, ls=-.02, upper=True, lh=250, tag="hero", z=8))
    P.append(t("all of them students. all of this, too.", 64, 522, 38, color=INK, font="d", weight=900, ls=0, upper=True, tag="head", z=8))
    # pill row
    def ppill(x, txt, bg, fg):
        w = int(len(txt) * 13 + 56)
        return t(txt, x, 590, 20, color=fg, font="m", weight=700, ls=.03, tag="pill", z=9,
                 extra=f"background:{bg};border:3px solid {INK};border-radius:999px;box-shadow:4px 4px 0 {INK};padding:9px 22px;"), w
    p1, w1 = ppill(64, "applications are open.", INK, LEM)
    p2, w2 = ppill(64 + w1 + 24, "link in bio.", PAPER, INK)
    P += [p1, p2]
    cards = [("540+", "drives, workshops and events since 2021", PAPER), ("8", "sundarbans trips", PAPER), ("4,000+", "saplings", PAPER),
             ("15,000+", "bananas. we counted.", PAPER), ("0", "donations. students earn what they spend", PAPER), ("0", "fees to join. no experience needed", TEAL)]
    cw, ch, gx, gy, x0, y0 = 464, 150, 24, 22, 64, 668
    for i, (num, cap, bg) in enumerate(cards):
        x = x0 + (i % 2) * (cw + gx); y = y0 + (i // 2) * (ch + gy)
        fg = ink_text(bg) if bg != PAPER else INK
        P.append(K.doodle(['burst','leaf','tree','heart','circle','plus'][i], x + cw - 84, y + 20, 56, [SKY, MINT, MINT, PINK, LEM, PAPER][i], rot=[8,-10,6,-8,0,0][i], z=9))
        P.append(f'<div data-tag="card" style="position:absolute;left:{x}px;top:{y}px;width:{cw}px;height:{ch}px;box-sizing:border-box;background:{bg};border:3px solid {INK};border-radius:28px;'
                 f'box-shadow:6px 6px 0 {INK};z-index:6;padding:16px 26px">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:80px;line-height:80px;color:{fg};text-transform:uppercase">{num}</div>'
                 f'<div style="font-family:var(--m);font-weight:700;font-size:16px;line-height:20px;letter-spacing:.03em;color:{fg};margin-top:8px;width:410px">{cap}</div></div>')
    P.append(K.url_pill(y=1206))
    html = K.page("".join(P))
    return K.render("hr_1", html, elements=[("logo", 64, 48, 190, 40)], text_pairs=[("hero", INK, "var(--bg)", 258, True), ("card_teal", ink_text(TEAL), TEAL, 84, True)])

for n in only: globals()[n]()
