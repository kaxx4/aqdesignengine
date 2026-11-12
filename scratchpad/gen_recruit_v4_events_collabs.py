"""AQ recruitment v4, EVENTS + COLLABS lanes. Four pieces, four different skeletons (none are the v2/v3 formats).

  events_1  style 091944e282ce11  date-pill rows on a black band       T1  (events, sky)
  events_2  style eaad68d6305fba  3 extruded plates + photo + burst    T4  (events, sky)
  collabs_1 style d536b66c9aaa00  listing cards with rotated tags      T3  (collabs, pink)
  collabs_2 style 620d62f101b97c  diagonal fan of cards on black       T4  (collabs, pink)

ADAPTATIONS (CLAUDE.md s2 ladder): cream ground not white (events_1, collabs_1, events_2); display type stays NeutralFace
uppercase; event dates are ONLY ones in brain/DISCO_DIWALI.md / TERRATHON.md / K.FACTS (month+year for the older editions,
no invented days). The reference's 'IN OCTOBER 2024' status bar became 'EVENTS WE RAN' / '2024 TO 2026'. The colour count is
exceeded on events_1 (six accents rotating, as the recipe itself asks) and collabs_2 holds to pink/lemon/tomato + photos.
collabs_1: the reference is a phone mockup; only the mechanism (outlined listing cards, mono detail column, thumbnail,
rotated status tag) is used. Status tags carry real numbers only. No college partner is named anywhere.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
from recruit_kit import INK, CREAM, PAPER, PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL, core, dd
from PIL import Image, ImageOps

W = 1080
def tx(c): return core.text_on(c)
def T(s, x, y, size, **kw): return K.t(s, x, y, size, **kw)

def mono_photo(rel, w, h, fx=.5, fy=.5, contrast=1.1, tint=None):
    im = K.cover(K.PH[rel], w, h, fx=fx, fy=fy)
    g = K.mono(im, contrast=contrast)
    if tint:
        d = ImageOps.colorize(ImageOps.grayscale(g), black=INK, white=tint, mid=None)
        return d
    return g

def burst(cx, cy, r, fill, pts=14, z=12, rot=0, inner=.82, sw=5):
    P = []
    for i in range(pts * 2):
        a = math.pi * i / pts + math.radians(rot); rr = r if i % 2 == 0 else r * inner
        P.append(f"{r + rr*math.cos(a):.1f},{r + rr*math.sin(a):.1f}")
    return (f'<svg style="position:absolute;left:{cx-r}px;top:{cy-r}px;z-index:{z};filter:drop-shadow(6px 6px 0 #0A0A0A)" width="{2*r}" height="{2*r}" viewBox="0 0 {2*r} {2*r}">'
            f'<polygon points="{" ".join(P)}" fill="{fill}" stroke="#0A0A0A" stroke-width="{sw}" stroke-linejoin="round"/></svg>')

def spark(x, y, s, col, rot=0, z=14):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;z-index:{z}">{dd.stamp("sparkle", col, rot=rot)}</div>')

# =============================================================== events_1
def events_1():
    P = [K.logo(), K.lane_chip("events"), K.series_tab()]
    E = []
    bx, by, bw, bh = 64, 176, 952, 990
    P.append(K.box(bx, by, bw, bh, f"background:{INK};border-radius:46px;", z=2))
    # headline card
    cx, cy, cw, ch = 88, 200, 904, 250
    P.append(K.box(cx, cy, cw, ch, f"background:{SKY};border:5px solid {INK};border-radius:38px;box-shadow:0 7px 0 0 #fff2;", z=4))
    P.append(T("SOMEONE HAD TO", cx + 40, cy + 34, 84, font="d", weight=900, lh=88, tag="h1", upper=True, z=6, ls=-.01))
    P.append(T("BOOK THE DJ.", cx + 40, cy + 132, 84, font="d", weight=900, lh=88, tag="h2", upper=True, z=6, ls=-.01))
    P.append(spark(cx + cw - 130, cy - 44, 62, LEM, 0)); P.append(spark(cx + cw - 64, cy - 22, 32, LEM, 20))
    P.append(spark(cx - 44, cy + 118, 76, MINT, 0, z=14))
    # status bar: white pill + pink pill
    sy = 466
    P.append(K.box(88, sy, 640, 68, f"background:{PAPER};border:5px solid {INK};border-radius:34px;", z=4))
    P.append(K.box(100, sy + 11, 46, 46, f"background:{INK};border-radius:50%;", z=5))
    P.append(T("→", 108, sy + 14, 30, color=PAPER, font="e", weight=700, tag="arr", z=6, lh=38))
    P.append(T("EVENTS WE RAN", 168, sy + 11, 38, font="d", weight=900, lh=46, tag="stat", upper=True, z=6))
    P.append(K.box(690, sy, 302, 68, f"background:{PINK};border:5px solid {INK};border-radius:34px;", z=5))
    P.append(T("2024 TO 2026", 716, sy + 14, 32, font="d", weight=900, lh=40, tag="yrs", upper=True, z=6))
    rows = [("OCT", "2024", "DISCO DIWALI 1.0", "", LEM, MINT),
            ("DEC", "2024", "STARRY NIGHT", "", PINK, SKY),
            ("JUN", "2025", "PARADOX 3.0", "", MINT, LEM),
            ("OCT", "2025", "DISCO DIWALI 2.0", "550 registrations", PAPER, TOM),
            ("OCT", "2026", "TERRATHON, 2 TO 4 OCT", "", SKY, MINT),
            ("NOV", "2026", "DISCO DIWALI MASQUERADE SANGEET, 10 NOV", "", PINK, LEM)]
    y = 556; rh = 74; gap = 10
    for i, (mo, yr, name, sub, dc, ec) in enumerate(rows):
        yy = y + i * (rh + gap)
        P.append(K.box(88, yy, 270, rh, f"background:{dc};border:5px solid {INK};border-radius:37px;", z=4))
        P.append(T(mo, 120, yy + 12, 44, color=tx(dc), font="d", weight=900, lh=48, tag=f"mo{i}", upper=True, z=6))
        P.append(T(yr, 232, yy + 29, 20, color=tx(dc), font="m", weight=700, lh=24, tag=f"yr{i}", z=6, upper=False))
        P.append(K.box(300, yy, 692, rh, f"background:{ec};border:5px solid {INK};border-radius:37px;", z=5))
        size = 30 if len(name) < 30 else 23
        P.append(T(name, 350, yy + (14 if size == 30 else 20), size, color=tx(ec), font="d", weight=900, lh=40 if size == 30 else 34, tag=f"ev{i}", upper=True, z=7))
        if sub: P.append(T(sub, 650, yy + 24, 16, color=tx(ec), font="m", weight=700, lh=22, tag="sub", z=7, upper=False))
        E.append((f"row{i}", 88, yy, 904, rh))
    P.append(T("the next one needs someone too. applications are open.", 88, 1098, 21, color=CREAM, font="m", weight=700, lh=30, tag="ask", z=6, upper=False, w=900))
    P.append(spark(930, 1030, 62, LEM, 12, z=14))
    P.append(K.url_pill(y=1190))
    html = K.page("".join(P))
    return html, E + [("band", bx, by, bw, bh), ("url", 64, 1190, 952, 84)], [("ask", CREAM, INK, 21, True)]

# =============================================================== events_2
def events_2():
    P = [K.box(0, 0, W, 1350, f"background:{CREAM};", z=0)]
    # curved line accent (solid, outlined) behind the plates and photo
    path = "M-40 760 C 180 560, 320 820, 520 700 S 900 480, 1130 640"
    for sw, col in ((44, INK), (32, PINK)):
        P.append(f'<svg style="position:absolute;left:0;top:0;z-index:1" width="{W}" height="1350" viewBox="0 0 {W} 1350"><path d="{path}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linecap="round"/></svg>')
    P += [K.logo(), K.lane_chip("events"), K.series_tab()]
    P.append(T("on the events team, you are also a:", 64, 172, 30, font="e", weight=600, lh=38, tag="kick", z=8, upper=False))
    E = []
    plates = [("VENDOR.", SKY, 80, 224, 700, 150, -3), ("SPONSOR.", PINK, 190, 372, 760, 150, 2), ("DJ.", LEM, 120, 520, 500, 150, -2)]
    for i, (s, c, x, y, w, h, r) in enumerate(plates):
        P.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};border:6px solid {INK};box-shadow:16px 16px 0 0 {INK};'
                 f'transform:rotate({r}deg);z-index:{6+i}"></div>')
        P.append(f'<div class="measure" data-tag="plate{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg);z-index:{16+i};'
                 f'font-family:var(--d);font-weight:900;font-size:122px;line-height:{h}px;text-align:center;color:{INK};text-transform:uppercase;letter-spacing:-.01em">{s}</div>')
        E.append((f"plate{i}", x, y, w, h))
    # hero photo, B&W, arch, bleeding off the bottom
    px, py, pw, ph_ = 190, 690, 700, 700
    g = mono_photo("dd_booth", pw, ph_, fx=.42, contrast=1.15)
    P.append(f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph_}px;border:6px solid {INK};border-radius:350px 350px 0 0;overflow:hidden;z-index:4;background:{INK}">'
             f'<img src="{K.uri(g)}" style="width:100%;height:100%;display:block"></div>')
    E.append(("photo", px, py, pw, ph_))
    # sunburst badge
    bcx, bcy, br = 190, 1030, 128
    P.append(burst(bcx, bcy, br, TOM, pts=16, z=20, rot=8))
    P.append(T("10+", bcx - br, bcy - 78, 92, color=INK, font="d", weight=900, w=2 * br, lh=92, extra="text-align:center;", tag="b1", z=22, upper=True))
    P.append(T("SMALL BUSINESSES", bcx - 80, bcy + 14, 22, color=INK, font="d", weight=900, w=160, lh=24, extra="text-align:center;", tag="b2", z=22, upper=True))
    P.append(T("DISCO DIWALI 2.0", bcx - 80, bcy + 68, 14, color=INK, font="m", weight=700, w=160, lh=18, extra="text-align:center;", tag="b3", z=22, upper=True))
    E.append(("badge", bcx - br, bcy - br, 2 * br, 2 * br))
    # speech bubble
    sx, sy, sw_, sh = 690, 720, 340, 170
    P.append(f'<svg style="position:absolute;left:{sx-30}px;top:{sy}px;z-index:20;filter:drop-shadow(6px 6px 0 #0A0A0A)" width="{sw_+30}" height="{sh+40}" viewBox="0 0 {sw_+30} {sh+40}">'
             f'<path d="M{30+40} 3 H{30+sw_-40} Q{30+sw_-3} 3 {30+sw_-3} 43 V{sh-43} Q{30+sw_-3} {sh-3} {30+sw_-40} {sh-3} H80 L8 {sh+34} L40 {sh-8} Q33 {sh-10} 33 {sh-43} V43 Q33 3 70 3 Z" fill="{PAPER}" stroke="#0A0A0A" stroke-width="6" stroke-linejoin="round"/></svg>')
    P.append(T("yes, we argued about balloons.", sx + 22, sy + 30, 36, font="e", weight=700, w=sw_ - 44, lh=44, tag="bub", z=22, upper=False, extra="text-align:center;"))
    E.append(("bubble", sx, sy, sw_, sh))
    P.append(spark(930, 960, 70, LEM, 10, z=21))
    P.append(K.url_pill(y=1190))
    return K.page("".join(P)), E + [("url", 64, 1190, 952, 84)], [("bub", INK, PAPER, 36, True), ("kick", INK, CREAM, 30, True)]

# =============================================================== collabs_1
def collabs_1():
    P = [K.logo(), K.lane_chip("collabs"), K.series_tab()]
    P.append(T("THE OTHER SIDE OF THE TABLE WAS A FOUNDATION.", 64, 176, 60, font="d", weight=900, w=952, lh=60, tag="head", z=8, upper=True))
    cards = [
        ("AQ x VISHWAJAGRITI x EMAMI", [("WHERE", "Science City"), ("WHAT", "stationery kits"), ("HOSTED", "30 kids")], "emami", "300 KITS", PINK, 1.2),
        ("CRFTD AT NOVUS", [("WHERE", "a school fest"), ("WHAT", "blank T-shirts, sprayed"), ("WALK-INS", "300")], "tee_novus", "300 WALK-INS", LEM, -1.0),
        ("CRFTD AT MORPHEUS", [("WHERE", "a school fest"), ("WHAT", "a Crftd stall"), ("WALK-INS", "300, 350")], "tee_morpheus", "300 + 350", SKY, .8),
        ("DISCO DIWALI 2.0", [("WHERE", "a party"), ("WHAT", "small businesses"), ("REGISTERED", "550")], "dd_booth", "10+ BUSINESSES", MINT, -.8),
    ]
    y = 336; ch = 206; gap = 14
    E = []
    for i, (title, det, ph, tag, tc, rot) in enumerate(cards):
        cy = y + i * (ch + gap)
        thumb = K.cover(K.PH[ph], 210, 150, fx=.5, fy=.4)
        inner = (T(title, 0, 22 if len(title) > 20 else 20, 30 if len(title) > 20 else 36, font="d", weight=900, w=590, lh=40, tag=f"t{i}", z=5, upper=True, extra="text-align:center;") +
                 "".join(T(k, 36, 84 + j * 36, 16, color="#555", font="m", weight=700, lh=22, tag=f"k{i}{j}", z=5, upper=False) +
                         T(v, 190, 84 + j * 36, 16, font="m", weight=700, lh=22, tag=f"v{i}{j}", z=5, upper=False) for j, (k, v) in enumerate(det)) +
                 f'<img src="{K.uri(thumb)}" style="position:absolute;left:{952-36-210}px;top:46px;width:210px;height:150px;border:4px solid {INK};border-radius:14px;object-fit:cover;z-index:4">')
        P.append(f'<div style="position:absolute;left:64px;top:{cy}px;width:952px;height:{ch}px;background:{PAPER};border:5px solid {INK};border-radius:30px;box-shadow:8px 8px 0 0 {INK};'
                 f'transform:rotate({rot}deg);z-index:{4+i}">{inner}</div>')
        tw = int(len(tag) * 21 + 44)
        P.append(f'<div class="measure" data-tag="tag{i}" style="position:absolute;left:{1016-tw}px;top:{cy-14}px;width:{tw}px;height:44px;background:{tc};border:4px solid {INK};'
                 f'transform:rotate({-6 if i%2==0 else 5}deg);z-index:{30+i};font-family:var(--d);font-weight:900;font-size:25px;line-height:36px;text-align:center;color:{tx(tc)};text-transform:uppercase;box-shadow:4px 4px 0 0 {INK}">{tag}</div>')
        E.append((f"card{i}", 64, cy, 952, ch))
    P.append(K.footer(color=INK))
    return K.page("".join(P)), E, [("head", INK, CREAM, 60, True)]

# =============================================================== collabs_2
def collabs_2():
    P = [K.box(0, 0, W, 1350, f"background:{INK};", z=0), K.logo_pill(64, 48, dark=True), K.lane_chip("collabs"), K.series_tab()]
    E = []
    def card(x, y, w, h, rot, bg, inner="", z=5, pad=0):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border:6px solid {PAPER if bg==INK else INK};transform:rotate({rot}deg);z-index:{z};overflow:hidden;box-shadow:10px 10px 0 0 #000">{inner}</div>')
    def label(s, x, y, col, rot, z):
        w = int(len(s) * 15 + 36)
        return (f'<div class="measure" data-tag="lab" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:40px;background:{col};border:3px solid {INK};z-index:{z};transform:rotate({rot}deg);'
                f'font-family:var(--m);font-weight:700;font-size:17px;line-height:34px;text-align:center;color:{INK}">{s}</div>'), w
    # accent card (behind), headline card (front)
    acc = T("300 STATIONERY KITS. 30 KIDS HOSTED. A FOUNDATION, AT SCIENCE CITY.", 0, 0, 34, font="d", weight=900, w=270, lh=38, tag="acc", z=2, upper=True)
    P.append(card(600, 212, 420, 330, 3, LEM, f'<div style="position:absolute;left:130px;top:44px;width:270px">{acc}</div>', z=4))
    head = "".join(T(s, 0, i * 70, 66, color=INK, font="d", weight=900, lh=68, tag=f"h{i}", z=3, upper=True) for i, s in enumerate(["SCHOOLS.", "NGOs.", "A FOUNDATION", "OR TWO."]))
    P.append(card(64, 196, 610, 360, -3, PINK, f'<div style="position:absolute;left:30px;top:30px">{head}</div>', z=9))
    # photo cards cascading down and right
    e = K.cover(K.PH["emami"], 560, 330, fx=.5, fy=.45)
    P.append(card(120, 530, 560, 330, 2, INK, f'<img src="{K.uri(e)}" style="width:100%;height:100%;display:block;object-fit:cover">', z=7))
    n = K.cover(K.PH["tee_novus"], 390, 480, fx=.5, fy=.35)
    P.append(card(620, 590, 390, 480, -2, INK, f'<img src="{K.uri(n)}" style="width:100%;height:100%;display:block;object-fit:cover">', z=8))
    d = K.cover(K.PH["dd_booth"], 440, 290, fx=.45, fy=.5)
    P.append(card(150, 860, 440, 290, -3, INK, f'<img src="{K.uri(d)}" style="width:100%;height:100%;display:block;object-fit:cover">', z=6))
    for s, x, y, c, r in (("A FOUNDATION", 140, 826, LEM, -3), ("A SCHOOL FEST", 720, 1040, PINK, -2), ("A PARTY, SMALL BUSINESSES", 170, 1140, PAPER, 2)):
        h, w = label(s, x, y, c, r, 25); P.append(h); E.append(("lab" + s[:4], x, y, w, 40))
    # pin badge at the seam of emami + novus cards
    P.append(burst(650, 660, 86, TOM, pts=12, z=30, rot=4, sw=5))
    P.append(T("HELLO.", 580, 641, 30, color=INK, font="d", weight=900, w=160, lh=44, extra="text-align:center;", tag="hello", z=32, upper=True))
    # ellipse callout
    P.append(f'<div style="position:absolute;left:548px;top:1112px;width:460px;height:120px;border-radius:50%;background:{PINK};border:6px solid {INK};z-index:26;box-shadow:8px 8px 0 0 #000"></div>')
    P.append(T("APPLICATIONS ARE OPEN.", 548, 1150, 28, color=INK, font="d", weight=900, w=460, lh=44, extra="text-align:center;", tag="open", z=27, upper=True))
    P.append(K.footer(color=PAPER))
    E += [("head", 64, 196, 610, 360), ("acc", 600, 212, 420, 330), ("emami", 120, 530, 560, 330), ("novus", 620, 590, 390, 480), ("dd", 150, 860, 440, 290), ("ellipse", 548, 1112, 460, 120), ("hello", 570, 580, 160, 160)]
    return K.page("".join(P)), E, [("open", INK, PINK, 31, True), ("footer", PAPER, INK, 15, True)]

IGN = {"events_2": [("plate0","plate1"),("plate1","plate2"),("badge","photo"),("bubble","photo"),("photo","url")],
       "collabs_1": [("card%d"%i,"card%d"%(i+1)) for i in range(3)],
       "collabs_2": [("head","acc"),("head","emami"),("emami","novus"),("emami","hello"),("novus","hello"),("dd","ellipse"),("labA FO","emami"),("labA SC","novus"),("dd","emami"),("novus","acc"),("h0","h1"),("h1","h2"),("h2","h3")]}
CONT = {"events_1": ("band",)}
if __name__ == "__main__":
    which = sys.argv[1:] or ["events_1", "events_2", "collabs_1", "collabs_2"]
    for n in which:
        html, E, tp = globals()[n]()
        K.render(n, html, elements=E, text_pairs=tp, bleed_tags=("photo",) if n == "events_2" else (),
                 collision_ignore=IGN.get(n, ()), containers=CONT.get(n, ()))
