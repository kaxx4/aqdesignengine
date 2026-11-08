"""Four-company Diwali poster v2, following the two references closely: ONE full-bleed illustration on black
(a big open hand catching a sparkler star; spiky stars, grainy orbs, long leaves), a small Bontan-style header
(thin rule, two-line title, tiny logos at the right) and a tiny asterisk burst. Branding is subordinate:
each company is a quiet dark motif inside an orb (wheel / book / leaf / building frame), logos are small,
websites are one muted line. All shapes drawn here; palette from the references (cobalt, teal, orange-red, yellow, pale blue)."""
import asyncio, os, sys, math, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import four_kit as K
from four_kit import *
R = ROOT; CO = f"{R}/scratchpad/co"; b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
COB, TEAL, ORG, YEL, PALE, CREAM, INK = "#1565E8", "#2DD4A8", "#F45B1F", "#F5C400", "#8FD8F0", "#F4EFE0", "#0A0A0A"
DEFS.append('<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="9" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G"/></filter>')
def spray_line(x1, y1, x2, y2, w, c1, c2, g, under=None):
    gid, mid = K._id("g"), K._id("m")
    DEFS.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{g[0]}" y1="{g[1]}" x2="{g[2]}" y2="{g[3]}"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'
                f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-50" y="-50" width="1200" height="1500"><g filter="url(#spk)"><rect x="-50" y="-50" width="1200" height="1500" fill="url(#{gid})"/></g></mask>')
    u = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{under}" stroke-width="{w+16}" stroke-linecap="round"/>' if under else ""
    return u + f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c1}" stroke-width="{w}" stroke-linecap="round"/><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c2}" stroke-width="{w}" stroke-linecap="round" mask="url(#{mid})"/>'
art = []; A = art.append
# --- long leaves (ref 1) behind everything
for x, y, ang, L, w, c1, c2 in [(-20, 210, 22, 380, 34, "#6F5CD6", "#B7A8F5"), (1100, 330, 160, 340, 30, "#C93D12", "#F45B1F"),
                                (-20, 860, -18, 330, 30, "#16805A", "#2DD4A8"), (1100, 760, 200, 300, 28, "#6F5CD6", "#B7A8F5")]:
    d, g = leaf(x, y, ang, L, w, bend=w * .7); A(spray(d, c1, c2, g))
# --- halo + sparkler star (ref 1) with stick running into the hand
A(spray(circle(600, 470, 215), "#12120d", "#3e3d2f", (600, 255, 600, 690)))
A(f'<line x1="600" y1="470" x2="770" y2="930" stroke="#5b3a2e" stroke-width="13" stroke-linecap="round"/>')
A(spray(star(600, 470, 190, 70, 11, 6, pinch=.2), "#F5B700", "#F45B1F", (560, 290, 650, 660)))
A(spray(circle(600, 470, 58), "#FFF2B8", "#F5C400", (600, 420, 600, 530)))
# --- stars + orbs (ref 2)
A(spray(star(230, 300, 140, 40, 7, -10, pinch=.3), COB, PALE, (150, 200, 300, 420)))
A(spray(star(805, 235, 150, 44, 7, 12, pinch=.3), ORG, YEL, (805, 150, 805, 400)))
A(spray(star(400, 880, 95, 28, 6, 0, pinch=.3), TEAL, CREAM, (330, 800, 480, 960)))
A(spray(star(560, 1130, 85, 25, 6, 20, pinch=.3), YEL, ORG, (560, 1060, 560, 1200)))
def orb(cx, cy, r, c1, c2, g): A(spray(circle(cx, cy, r), c1, c2, g))
orb(205, 560, 112, TEAL, CREAM, (150, 480, 280, 650)); orb(905, 470, 98, PALE, CREAM, (840, 380, 960, 560))
orb(170, 1040, 168, TEAL, YEL, (60, 900, 300, 1200)); orb(385, 1165, 80, PALE, CREAM, (330, 1190, 440, 1320))
# quiet company motifs inside the orbs (dark, low contrast)
M = f'fill="none" stroke="{INK}" stroke-opacity=".55" stroke-linecap="round"'
A(f'<g {M} stroke-width="7"><circle cx="205" cy="560" r="64"/><circle cx="205" cy="560" r="8" fill="{INK}" fill-opacity=".55"/>' + "".join(
    f'<line x1="{205+9*math.cos(math.radians(a*30))}" y1="{560+9*math.sin(math.radians(a*30))}" x2="{205+62*math.cos(math.radians(a*30))}" y2="{560+62*math.sin(math.radians(a*30))}" stroke-width="3.5"/>' for a in range(12)) + '</g>')          # MK wheel
A(f'<g fill="{INK}" fill-opacity=".62"><path d="M850 458 L902 470 L902 530 L850 520Z"/><path d="M958 458 L906 470 L906 530 L958 520Z"/></g><g stroke="{PALE}" stroke-width="3" stroke-linecap="round" stroke-opacity=".9">' + "".join(f'<line x1="{858}" y1="{470+i*13}" x2="{894}" y2="{476+i*13}"/><line x1="{950}" y1="{470+i*13}" x2="{914}" y2="{476+i*13}"/>' for i in range(3)) + '</g>')      # Shikshaq book
for ang, L in [(-150, 85), (-115, 100), (-80, 95), (-45, 85), (-20, 70)]:
    d, _ = leaf(170, 1135, ang, L, 14, 4); A(f'<path d="{d}" fill="{INK}" fill-opacity=".5"/>')                                                       # AQ leaves
for r_ in range(3):
    for c_ in range(3):
        A(f'<rect x="{355+c_*24}" y="{1135+r_*20}" width="16" height="12" fill="{INK}" fill-opacity=".5"/>')                                        # Ekavya building frame
# --- open hand (ref 2): fingers as separated capsules, black gaps, spray teal at the tips
hand = []
fingers = [((598, 985), (580, 765), 60), ((664, 975), (660, 700), 62), ((730, 980), (745, 712), 62), ((795, 1010), (830, 800), 58)]
palm = "M545 1380 L545 1070 Q545 970 640 960 L760 960 Q850 975 850 1080 L850 1380Z"
hand.append(spray(palm, COB, TEAL, (700, 1250, 700, 960), extra=f'stroke="{INK}" stroke-width="10" stroke-linejoin="round"'))
for (x1, y1), (x2, y2), w in fingers:
    hand.append(spray_line(x1, y1, x2, y2, w, COB, TEAL, (x1, y1 + 60, x2, y2), under=INK))
hand.append(spray_line(575, 1115, 478, 975, 64, COB, TEAL, (575, 1115, 478, 955), under=INK))
for d_ in ["M585 1110 Q650 1060 715 1090", "M600 1190 Q690 1150 790 1175"]:
    hand.append(f'<path d="{d_}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
A('<g transform="rotate(16 700 1330)">' + "".join(hand) + '</g>')
body_art = f'<g filter="url(#rough)">{"".join(art)}</g>'
# --- thin asterisk burst bottom-left (ref 2)
bx, by = 105, 1240
body_art += "".join(f'<line x1="{bx+14*math.cos(math.radians(i*15))}" y1="{by+14*math.sin(math.radians(i*15))}" x2="{bx+(52 if i%2==0 else 40)*math.cos(math.radians(i*15))}" y2="{by+(52 if i%2==0 else 40)*math.sin(math.radians(i*15))}" stroke="{CREAM}" stroke-width="3" stroke-linecap="round"/>' for i in range(24))
body_art += f'<line x1="40" y1="36" x2="1040" y2="36" stroke="{CREAM}" stroke-width="2"/>'
# --- header (ref 2): title left, tiny logos right; URLs one muted line
sh = f'<img src="data:image/svg+xml;base64,{b64(R+"/addons/shikshaq/assets/shikshaq-logo.svg")}" style="height:30px">'
pill = lambda inner: f'<span style="background:{CREAM};border-radius:999px;padding:5px 12px;display:inline-flex;align-items:center">{inner}</span>'
logos = (pill(f'<img src="{core.LOGO}" style="height:22px">') + pill(sh) +
         f'<img src="data:image/png;base64,{b64(CO+"/mk_logo_crop.png")}" style="height:36px">' +
         f'<img src="data:image/svg+xml;base64,{b64(CO+"/ek_icon.svg")}" style="height:36px">')
body = (f'<div class=chk data-n="t1" style="position:absolute;left:40px;top:58px;font-weight:800;font-size:58px;line-height:1;letter-spacing:-.02em;color:{TEAL};z-index:12;white-space:nowrap">HAPPY DIWALI</div>'
        f'<div class=chk data-n="t2" style="position:absolute;left:40px;top:122px;font-weight:800;font-size:30px;line-height:1;letter-spacing:-.005em;color:{CREAM};z-index:12;white-space:nowrap">AQ · SHIKSHAQ · MK CYCLES · EKAVYA</div>'
        f'<div class=chk data-n="logos" style="position:absolute;right:40px;top:62px;display:flex;align-items:center;gap:14px;z-index:12">{logos}</div>'
        f'<div class=chk data-n="urls" style="position:absolute;left:176px;width:380px;bottom:34px;text-align:left;line-height:1.45;font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.04em;color:#a39e8c;z-index:12;white-space:nowrap">VISIT US AT<br>NGOAQUATERRA.COM · SHIKSHAQ.IN<br>MKCYCLES.IN · EKAVYAVYAPAAR.VERCEL.APP</div>')
html = K.page(body_art, body)
asyncio.run(K.shoot(html, f"{R}/out/four/mega2_final.png"))
