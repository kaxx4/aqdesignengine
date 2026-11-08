"""Recreation of the user-supplied sparkler illustration (reference 736x736), traced shape by shape in its own
coordinate space: pink fist + brown stick, yellow starburst with cream core and speckled halo, two-tone leaves,
outline loops, squiggles, dots, dust, painterly rough edges. Rendered square at 1080 (aspect preserved)."""
import asyncio, os, sys, math, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED, PINKL, SALMON = "#F2461E", "#F28484", "#F5A58C"
DG, LG, LAV, LAVL, BLUE, BLUEL, PINK = "#1B8C66", "#6CC48A", "#8A86DA", "#C3BFF2", "#1E8DDD", "#9CDDF6", "#EE84C2"
INK = "#0a0a0c"
def crm(pts, closed=False):
    P = (pts[-1:] + pts + pts[:2]) if closed else ([pts[0]] + pts + [pts[-1]])
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + ("Z" if closed else "")
def offs(pts, ws, side=1):
    out = []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        out.append((p[0] - dy / L * ws[i] * side, p[1] + dx / L * ws[i] * side))
    return out
def band(pts, ws, c1, c2=None, side=1, c2frac=1.0):
    """tapered band along a centre line; c2 fills the half on `side` (from the centre line to that edge)"""
    L, Rr = offs(pts, ws, 1), offs(pts, ws, -1)
    s = f'<path d="{crm(L + Rr[::-1], closed=True)}" fill="{c1}"/>'
    if c2:
        E = offs(pts, [w * c2frac for w in ws], side)
        s += f'<path d="{crm(E + pts[::-1], closed=True)}" fill="{c2}"/>'
    return s
def ribbon(pts, w, c1, c2=None, side=1):
    s = f'<path d="{crm(pts)}" fill="none" stroke="{c1}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    if c2: s += f'<path d="{crm(offs(pts,[w*.28]*len(pts),side))}" fill="none" stroke="{c2}" stroke-width="{w*.42}" stroke-linecap="round"/>'
    return s
def loop(pts, c, sw=6): return f'<path d="{crm(pts, closed=True)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'
def blob(pts, c): return f'<path d="{crm(pts, closed=True)}" fill="{c}"/>'
o = []; A = o.append; rnd = random.Random(5)
for _ in range(520):
    x, y = rnd.uniform(0, 736), rnd.uniform(0, 736); A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([.6,.8,1,1.2,1.6])}" fill="#d8d4c4" opacity="{rnd.uniform(.25,.75):.2f}"/>')
A('<defs><radialGradient id="hl" cx="368" cy="190" r="160" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#9a9474" stop-opacity=".8"/><stop offset=".6" stop-color="#7a7458" stop-opacity=".66"/><stop offset=".93" stop-color="#4a4733" stop-opacity=".4"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>')
A('<circle cx="368" cy="190" r="162" fill="url(#hl)"/>')
for _ in range(280):
    a, r = rnd.uniform(0, 6.283), 168 * math.sqrt(rnd.random()); x, y = 368 + r * math.cos(a), 190 + r * math.sin(a)
    A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([.7,1,1.4,2,2.6,3.2])}" fill="{rnd.choice(["#e9e2c4","#f0a640","#cfc9a8","#dcd6b6"])}" opacity="{rnd.uniform(.35,.85):.2f}"/>')
# ================= TOP-LEFT
A(loop([(24, 26), (48, 22), (78, 40), (108, 50), (96, 63), (60, 62), (34, 46)], RED, 7))
A(band([(160, 1), (190, 6), (212, 22), (232, 40)], [11, 14, 12, 3], RED))
A(ribbon([(262, 4), (284, 14), (300, 2), (316, 14), (330, 4)], 7, SALMON))
A(band([(-10, 112), (30, 112), (80, 120), (130, 140), (170, 154), (208, 160)], [46, 44, 34, 20, 9, 1], LG, DG, side=-1, c2frac=1))
A(band([(10, 292), (40, 262), (90, 247), (126, 240)], [8, 15, 13, 5], LAV, None))
A(ribbon([(22, 292), (50, 288), (95, 268), (124, 250)], 4, LAVL))
A(blob([(228, 258), (214, 252), (206, 258), (214, 266), (230, 262)], DG))
A(band([(-8, 448), (30, 418), (70, 388), (100, 366), (130, 345), (165, 326), (200, 308), (230, 295)], [6, 8, 9, 13, 17, 21, 16, 2], RED, PINKL, side=-1, c2frac=.55))
A(blob([(-5, 340), (40, 336), (80, 338), (95, 346), (88, 362), (60, 372), (48, 395), (36, 412), (-5, 418)], LG))
A(blob([(-5, 340), (40, 336), (80, 338), (95, 346), (90, 354), (50, 352), (-5, 360)], DG))
A(ribbon([(240, 370), (244, 345), (262, 330), (296, 322)], 12, BLUE, BLUEL))
# ================= TOP-RIGHT
A(ribbon([(418, 2), (404, 16), (394, 30)], 9, BLUEL, BLUE))
A(loop([(462, 0), (468, 20), (456, 40), (441, 34), (437, 14), (447, 0)], LG, 6))
A(ribbon([(533, 75), (552, 62), (575, 52), (580, 30), (576, 12), (592, 0)], 9, DG))
A(band([(568, 92), (596, 66), (630, 36), (662, 8), (672, -4)], [1, 5, 8, 10, 8], BLUE, BLUEL, side=1, c2frac=.6))
A(band([(523, 162), (560, 152), (610, 137), (660, 118), (705, 90), (738, 45), (752, 0)], [2, 14, 24, 32, 38, 46, 40], LAV, LAVL, side=-1, c2frac=.3))
A(f'<path d="M698 116 L742 106 L742 126 Z" fill="{INK}"/>')
A(loop([(684, 0), (690, 20), (702, 24), (716, 12), (708, 0)], RED, 6))
A(band([(590, 233), (625, 244), (665, 262), (705, 286), (746, 310)], [2, 16, 28, 38, 44], LG, DG, side=-1, c2frac=1))
A(band([(693, 245), (712, 245), (746, 247)], [6, 10, 12], RED))
A(ribbon([(533, 252), (554, 258), (562, 248), (576, 262), (589, 274)], 9, DG))
A(ribbon([(589, 312), (606, 322), (622, 342), (648, 354), (670, 368)], 13, BLUE, BLUEL, side=1))
# ================= BOTTOM-LEFT
A(band([(135, 420), (108, 445), (80, 472)], [9, 13, 8], LAV, LAVL, side=-1, c2frac=.6))
A(loop([(0, 500), (22, 488), (44, 492), (50, 506), (30, 520), (-4, 536)], SALMON, 7))
A(band([(-4, 590), (25, 556), (50, 536), (72, 520)], [8, 8, 7, 3], RED))
A(loop([(120, 552), (132, 538), (148, 540), (151, 558), (136, 574), (124, 570)], BLUE, 6))
A(loop([(6, 626), (14, 612), (38, 606), (50, 612), (40, 634), (18, 646), (8, 640)], BLUE, 6))
A(ribbon([(166, 447), (172, 420), (190, 396), (215, 382), (248, 372)], 11, BLUE, BLUEL))
A(loop([(276, 386), (290, 378), (306, 380), (306, 392), (296, 408), (282, 416), (274, 402)], LG, 6))
# big lavender leaf (two legs, notch, light stripe on its right side)
leaf = [(262, 444), (240, 462), (218, 492), (203, 530), (196, 566), (172, 606), (146, 638), (120, 668), (100, 695), (90, 728), (84, 744),
        (150, 744), (152, 676), (160, 696), (176, 744), (200, 744), (190, 716), (183, 676), (190, 650), (205, 614), (226, 578), (240, 530), (252, 484)]
A(blob(leaf, LAV))
A(band([(262, 444), (246, 492), (232, 545), (214, 590), (196, 628), (186, 668), (188, 720), (196, 744)], [1, 8, 12, 13, 12, 10, 8, 6], LAVL, None, side=-1))
A(f'<path d="M148 672 L128 748 L156 748 Z" fill="{INK}"/>')
A(ribbon([(237, 640), (228, 656), (244, 668), (241, 690), (232, 706), (241, 724)], 11, BLUE, BLUEL, side=-1))
A(band([(94, 654), (74, 688), (48, 714), (30, 744)], [7, 11, 12, 9], DG))
# ================= BOTTOM-RIGHT
A(band([(518, 366), (545, 372), (585, 384), (630, 399), (680, 424), (746, 470)], [2, 7, 11, 11, 9, 7], RED))
A(band([(520, 372), (545, 406), (585, 430), (630, 446), (670, 470), (712, 512), (746, 548)], [3, 17, 30, 34, 31, 26, 13], RED, PINKL, side=-1, c2frac=.55))
A(f'<path d="M700 420 Q730 440 746 470 L746 430Z" fill="{INK}"/>')
A(ribbon([(658, 368), (690, 378), (714, 395), (733, 420)], 10, BLUE, BLUEL))
A(ribbon([(473, 468), (483, 490), (480, 510), (500, 525), (505, 548), (510, 562)], 10, DG))
A(band([(562, 490), (580, 515), (610, 545), (640, 580), (680, 614), (746, 640)], [2, 16, 27, 33, 31, 28], LG, DG, side=-1, c2frac=1))
A(band([(622, 568), (650, 618), (690, 660)], [8, 11, 1], LG))
A(loop([(548, 583), (562, 583), (574, 605), (580, 632), (588, 654), (578, 657), (566, 640), (560, 612), (550, 596)], BLUE, 6))
A(band([(610, 646), (622, 662), (638, 696), (662, 720), (690, 746)], [9, 11, 12, 11, 8], RED))
A(band([(580, 702), (588, 722), (592, 746)], [8, 9, 6], SALMON))
A(loop([(464, 692), (466, 680), (478, 684), (482, 716), (490, 746), (482, 746), (470, 718)], RED, 6))
# dots
for x, y, r, c in [(141, 39, 6, LAVL), (161, 77, 8, LAVL), (191, 68, 4.5, LAVL), (60, 183, 6, "#F5A02A"), (101, 208, 6, "#F5A02A"), (5, 215, 8, LAVL), (22, 227, 4, LAVL),
                   (509, 3, 7, LAVL), (536, 17, 5, LAVL), (510, 34, 7, LAVL), (655, 69, 8, LAVL), (625, 11, 4, LAVL), (661, 192, 6, "#F5A02A"), (621, 216, 6, "#F5A02A"),
                   (183, 365, 6, LAVL), (210, 362, 7, LAVL), (228, 439, 7, LAVL), (250, 433, 4, LAVL), (95, 518, 5, "#F5A02A"), (86, 598, 8, "#F5A02A"), (164, 483, 4, "#F5A02A"),
                   (512, 401, 7, "#F5A02A"), (492, 427, 4, LAVL), (522, 437, 7, LAVL), (451, 495, 4, "#F5A02A"), (487, 570, 5, LAVL), (522, 594, 8, LAVL), (534, 663, 5, "#F5A02A"),
                   (631, 496, 5, LAVL), (662, 500, 4, LAVL), (676, 530, 8, LAVL), (704, 701, 9, LAVL), (626, 403, 3, "#F5A02A"), (320, 60, 3, "#d6d2b8")]:
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
# ================= starburst (tips read off the reference)
cx, cy = 372, 185
tips = [(-171, 130), (-135, 102), (-125, 164), (-89, 110), (-68, 83), (-44, 163), (-16, 111), (21, 140), (43, 99), (77, 157), (106, 141), (135, 109), (159, 152)]
pts = []
for i, (a, r) in enumerate(tips):
    r = r * 1.04
    pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    na = (a + tips[(i + 1) % len(tips)][0] + (360 if i == len(tips) - 1 else 0)) / 2
    pts.append((cx + 72 * math.cos(math.radians(na)), cy + 72 * math.sin(math.radians(na))))
star_d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
A(f'<clipPath id="sc"><path d="{star_d}"/></clipPath><path d="{star_d}" fill="#FBBE0E" stroke="#FBBE0E" stroke-width="2" stroke-linejoin="round"/>')
A('<g clip-path="url(#sc)">' + "".join(f'<circle cx="{rnd.uniform(228,505):.1f}" cy="{rnd.uniform(50,342):.1f}" r="{rnd.choice([.9,1.3,1.8,2.5,3.2])}" fill="{rnd.choice(["#E8541C","#ee7a1c","#E8541C","#f6d24a"])}" opacity=".85"/>' for _ in range(230)) + '</g>')
A(f'<circle cx="372" cy="184" r="33" fill="#F2E6A4"/>')
# ================= stick + fist (traced from a 3x zoom: fist coordinates are zoom units, group scaled by 1/3)
A(f'<path d="M363 250 L371 250 L369 430 L362 430Z" fill="#4E2A22"/>')
sil = "M225 105 Q225 70 260 68 L628 50 Q652 50 648 76 L640 106 Q622 150 548 166 L560 200 L738 520 L722 622 L642 802 L598 978 L175 978 L150 802 L70 562 L58 520 L230 335Z"
fist = f'<path d="{sil}" fill="{PINK}"/>'
lines = ["M368 170 L548 164", "M410 176 L410 214", "M232 340 L440 186 Q462 178 470 200 L500 302", "M205 455 L545 318 Q572 312 576 340 L586 482",
         "M262 515 L575 493 Q602 496 598 522 Q572 642 540 700 Q530 718 500 721", "M330 625 L466 617 L470 668", "M386 628 Q440 650 480 690 Q492 706 498 722", "M498 722 Q524 790 562 920"]
for d in lines: fist += f'<path d="{d}" fill="none" stroke="#150c10" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
A(f'<g transform="translate(230 410) scale(0.33333)">{fist}</g>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 736 736" width="736" height="736"><defs><filter id="rf" x="-3%" y="-3%" width="106%" height="106%">'
       '<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter>'
       '<filter id="gr"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="8"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.25"/></filter></defs>'
       f'<rect width="736" height="736" fill="{INK}"/><g filter="url(#rf)">{"".join(o)}</g><rect width="736" height="736" filter="url(#gr)" opacity=".22"/></svg>')
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for size, out in [(736, "sparkler_recreation_736.png"), (1080, "sparkler_recreation_1080.png")]:
            pg = await b.new_page(viewport={"width": size, "height": size})
            await pg.set_content(f'<body style="margin:0;background:#000">{svg.replace("width=\"736\" height=\"736\"", f"width=\"{size}\" height=\"{size}\"", 1)}</body>')
            await pg.wait_for_timeout(300); await pg.screenshot(path=f"{ROOT}/out/four/{out}"); await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image
ref = Image.open("/tmp/claude-0/-home-user/789e1244-ae70-5b86-bc19-5e0a334e997b/images/1.jpg").convert("RGB").resize((736, 736))
mine = Image.open(f"{ROOT}/out/four/sparkler_recreation_736.png").convert("RGB")
sb = Image.new("RGB", (1472, 736)); sb.paste(ref, (0, 0)); sb.paste(mine, (736, 0)); sb.save(f"{ROOT}/out/four/_sparkler_compare.png")
