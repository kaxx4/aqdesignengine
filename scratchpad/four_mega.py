"""ONE mega Diwali poster for four companies (feed 1080x1350): AQ, Shikshaq, MK Cycles, Ekavya Vyapaar.
2x2 panels around a shared spray-textured sparkler star; each panel has its own hero, palette, logo and
'Visit us at <site>'. Real facts only: websites; Ekavya Ranges (Ballygunge, under construction) is from ekavya's site.
Style from two user references (grainy spray-gradient shapes on black); every shape drawn here."""
import asyncio, os, sys, base64, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from four_kit import *
R = ROOT; CO = f"{R}/scratchpad/co"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
CREAM, INK = "#F4EFE0", "#0A0A0A"
parts = []; A = parts.append
# ---------- panels
PAN = [dict(k="aq", x=40, y=250, bg="#0B2C40", site="www.ngoaquaterra.com", align="l"),
       dict(k="sh", x=550, y=250, bg="#1B2380", site="www.shikshaq.in", align="r"),
       dict(k="mk", x=40, y=740, bg="#33100C", site="mkcycles.in", align="l"),
       dict(k="ek", x=550, y=740, bg="#14213D", site="ekavyavyapaar.vercel.app", align="r")]
PW, PH = 490, 470
for p in PAN:
    A(f'<rect x="{p["x"]}" y="{p["y"]}" width="{PW}" height="{PH}" rx="32" fill="{p["bg"]}"/>')
    # tiny stars in each panel
    for i in range(14):
        sx = p["x"] + 30 + (i * 137) % (PW - 60); sy = p["y"] + 20 + (i * 71) % 260
        A(f'<circle cx="{sx}" cy="{sy}" r="{1.6 + (i % 3) * .7}" fill="{CREAM}" opacity=".85"/>')
def hc(p): return (p["x"] + (235 if p["align"] == "l" else 255), p["y"] + 150)
def wrap(start, cx, cy, sc):
    parts[start:] = [f'<g transform="translate({cx} {cy}) scale({sc}) translate({-cx} {-cy})">' + "".join(parts[start:]) + '</g>']
# ---------- AQ hero: sparkler with flowing leaves (mint / teal / sky)
cx, cy = hc(PAN[0]); _s = len(parts)
for ang, L, w, c1, c2 in [(-165, 210, 30, "#1B8A5A", "#00E5A0"), (-140, 230, 26, "#0E7C86", "#3DA9FC"), (-118, 210, 24, "#3DA9FC", "#CFEFE3"),
                          (-62, 215, 24, "#0E7C86", "#3DA9FC"), (-40, 230, 28, "#1B8A5A", "#00E5A0"), (-15, 205, 30, "#3DA9FC", "#F4EFE0"),
                          (-90, 170, 18, "#00E5A0", "#F4EFE0"), (-185, 150, 22, "#3DA9FC", "#1B8A5A")]:
    d, g = leaf(cx, cy + 95, ang, L, w, bend=w * .5); A(spray(d, c1, c2, g))
A(f'<line x1="{cx}" y1="{cy-30}" x2="{cx}" y2="{cy+120}" stroke="#7a5a48" stroke-width="9" stroke-linecap="round"/>')
A(spray(star(cx, cy - 40, 86, 30, 9, 10), "#FFC700", "#FF4D2E", (cx, cy - 120, cx + 30, cy + 40)))
A(f'<circle cx="{cx}" cy="{cy-40}" r="24" fill="#FFF2B8"/>')
wrap(_s, cx, cy, 1.0)
# ---------- Shikshaq hero: open book under a flame star
cx, cy = hc(PAN[1]); _s = len(parts)
A(spray(star(cx, cy - 55, 118, 42, 8, 0), "#FF8000", "#FFD27A", (cx, cy - 170, cx, cy + 20)))
A(f'<circle cx="{cx}" cy="{cy-55}" r="28" fill="#FFF4E8"/>')
for x, y, s, c in [(cx - 150, cy - 130, 24, "#EDEEFF"), (cx + 140, cy - 100, 20, "#FFB259"), (cx + 100, cy - 170, 14, "#EDEEFF")]:
    A(flat(sparkle4(x, y, s), c))
A(spray(circle(cx - 135, cy - 20, 26), "#4351FF", "#F9F5F1", (cx - 160, cy - 40, cx - 110, cy)))
A(f'<path d="M{cx-175} {cy+95} L{cx} {cy+70} L{cx} {cy+175} L{cx-175} {cy+190}Z" fill="#2E3AD6"/><path d="M{cx+175} {cy+95} L{cx} {cy+70} L{cx} {cy+175} L{cx+175} {cy+190}Z" fill="#2E3AD6"/>')
A(spray(f"M{cx-160} {cy+60} L{cx-6} {cy+40} L{cx-6} {cy+150} L{cx-160} {cy+168}Z", "#F9F5F1", "#FFB259", (cx - 160, cy + 40, cx - 6, cy + 168)))
A(spray(f"M{cx+160} {cy+60} L{cx+6} {cy+40} L{cx+6} {cy+150} L{cx+160} {cy+168}Z", "#F9F5F1", "#FFB259", (cx + 160, cy + 40, cx + 6, cy + 168)))
for i in range(4):
    A(f'<line x1="{cx-140}" y1="{cy+78+i*18}" x2="{cx-30}" y2="{cy+66+i*18}" stroke="#2E3AD6" stroke-width="4" stroke-linecap="round"/>'
      f'<line x1="{cx+140}" y1="{cy+78+i*18}" x2="{cx+30}" y2="{cy+66+i*18}" stroke="#2E3AD6" stroke-width="4" stroke-linecap="round"/>')
wrap(_s, cx, cy + 15, .76)
# ---------- MK hero: a bicycle wheel as a diwali chakri (spinning firework)
cx, cy = hc(PAN[2]); _s = len(parts)
A(spray(star(cx, cy, 190, 100, 12, 8, pinch=.2), "#FF4D2E", "#FFC700", (cx - 150, cy + 150, cx + 120, cy - 160)))
ring = circle(cx, cy, 128) + circle(cx, cy, 108)
A(f'<path d="{ring}" fill="#33100C" fill-rule="evenodd" transform="translate(0 0)"/>')
A(spray(circle(cx, cy, 124) + circle(cx, cy, 104), "#F4EFE0", "#FFC700", (cx - 120, cy + 120, cx + 100, cy - 110), extra='fill-rule="evenodd"'))
for i in range(16):
    a = math.radians(i * 22.5)
    A(f'<line x1="{cx+14*math.cos(a):.1f}" y1="{cy+14*math.sin(a):.1f}" x2="{cx+104*math.cos(a):.1f}" y2="{cy+104*math.sin(a):.1f}" stroke="#F4EFE0" stroke-width="3"/>')
A(f'<circle cx="{cx}" cy="{cy}" r="20" fill="#FFC700"/><circle cx="{cx}" cy="{cy}" r="9" fill="#33100C"/>')
for a, c in [(-30, "#FFC700"), (35, "#F4EFE0"), (120, "#FF4D2E"), (200, "#FFC700"), (255, "#F4EFE0")]:
    r1, r2 = 160, 192; aa = math.radians(a)
    A(f'<line x1="{cx+r1*math.cos(aa):.0f}" y1="{cy+r1*math.sin(aa):.0f}" x2="{cx+r2*math.cos(aa):.0f}" y2="{cy+r2*math.sin(aa):.0f}" stroke="{c}" stroke-width="7" stroke-linecap="round"/>')
wrap(_s, cx, cy + 10, .78)
# ---------- Ekavya hero: Ekavya Ranges under construction (concrete frame, crane, first lit floors)
cx, cy = hc(PAN[3]); _s = len(parts)
bx, by, bw = cx - 105, cy - 120, 210
for i in range(5):
    fy = by + 40 + i * 52
    A(f'<rect x="{bx-8}" y="{fy+44}" width="{bw+16}" height="8" fill="#4F7BFF"/>')
for c in range(4):
    A(f'<rect x="{bx + c*(bw-12)/3}" y="{by+40}" width="12" height="260" fill="#0B3FC9"/>')
for i in range(5):
    fy = by + 40 + i * 52
    lit = i >= 3
    for c in range(3):
        wx = bx + 18 + c * ((bw - 12) / 3)
        if lit: A(spray(f"M{wx} {fy+8} h{bw/3-26} v34 h-{bw/3-26}Z", "#F04E17", "#FFC700", (wx, fy + 42, wx + 30, fy + 8)))
A(f'<rect x="{bx-24}" y="{by+296}" width="{bw+48}" height="10" fill="#4F7BFF"/>')
# crane
A(f'<rect x="{bx+bw-6}" y="{by-90}" width="10" height="130" fill="#F04E17"/><rect x="{bx-40}" y="{by-96}" width="{bw+120}" height="9" fill="#F04E17"/>'
  f'<line x1="{bx+bw+4}" y1="{by-90}" x2="{bx+bw+60}" y2="{by-94}" stroke="#F04E17" stroke-width="3"/><line x1="{bx-30}" y1="{by-86}" x2="{bx-30}" y2="{by-30}" stroke="#F4EFE0" stroke-width="3"/>')
A(spray(star(bx - 30, by - 20, 34, 12, 8, 0), "#FFC700", "#F04E17", (bx - 30, by - 60, bx - 30, by + 20)))
for x, y, s, c in [(cx - 150, cy - 60, 20, "#F4EFE0"), (cx + 150, cy - 10, 16, "#FFC700"), (cx + 128, cy - 150, 12, "#F4EFE0")]:
    A(flat(sparkle4(x, y, s), c))
wrap(_s, cx, cy + 40, .62)
# ---------- shared centre sparkler star
A(spray(star(540, 730, 138, 62, 12, 7, pinch=.22), "#FFC700", "#FF4D2E", (500, 590, 600, 870)))
A(f'<circle cx="540" cy="730" r="40" fill="#FFF2B8"/>')
for x, y, s in [(70, 215, 14), (1010, 220, 16), (60, 1250, 18), (1015, 1255, 14), (120, 1290, 12)]:
    A(flat(sparkle4(x, y, s * 1.6), CREAM))
# ---------- body: titles, logos, urls
def foot(p, logo_html, name):
    right = p["align"] == "r"
    x0 = p["x"] + 26; w = PW - 52; ty = p["y"] + 322
    al = "right" if right else "left"; fl = "flex-end" if right else "flex-start"
    return (f'<div class=chk data-n="{name}" style="position:absolute;left:{x0}px;top:{ty}px;width:{w}px;display:flex;flex-direction:column;align-items:{fl};text-align:{al};z-index:12">'
            f'<div style="height:52px;display:flex;align-items:center">{logo_html}</div>'
            f'<div style="margin-top:12px;font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:#C9C3B5">Visit us at</div>'
            f'<div style="margin-top:4px;font-size:27px;font-weight:700;letter-spacing:-.005em;color:{CREAM}">{p["site"]}</div></div>')
aq_logo = f'<span style="background:{CREAM};border-radius:999px;padding:7px 16px;display:inline-flex"><img src="{core.LOGO}" style="height:30px"></span>'
sh_logo = f'<span style="background:#F9F5F1;border-radius:999px;padding:3px 16px;display:inline-flex"><img src="data:image/svg+xml;base64,{b64(R+"/addons/shikshaq/assets/shikshaq-logo.svg")}" style="height:44px"></span>'
mk_logo = f'<img src="data:image/png;base64,{b64(CO+"/mk_logo_crop.png")}" style="height:50px">'
ek_logo = (f'<span style="display:inline-flex;align-items:center;gap:12px"><img src="data:image/svg+xml;base64,{b64(CO+"/ek_icon.svg")}" style="height:46px">'
           f'<span style="font-weight:800;font-size:23px;letter-spacing:.12em;color:{CREAM}">EKAVYA VYAPAAR</span></span>')
body = (foot(PAN[0], aq_logo, "aq") + foot(PAN[1], sh_logo, "sh") + foot(PAN[2], mk_logo, "mk") + foot(PAN[3], ek_logo, "ek") +
        f'<div class=chk data-n="title" style="position:absolute;left:0;right:0;top:34px;text-align:center;font-weight:800;font-size:134px;line-height:1;letter-spacing:-.035em;color:{CREAM};white-space:nowrap;z-index:12">Happy <span style="font-weight:400">Diwali</span></div>'
        f'<div class=chk data-n="sub" style="position:absolute;left:0;right:0;top:186px;text-align:center;font-size:27px;font-weight:500;color:#C9C3B5;white-space:nowrap;z-index:12">from AQ, Shikshaq, MK Cycles and Ekavya Vyapaar</div>'
        f'<div class=chk data-n="tag" style="position:absolute;left:{PAN[3]["x"]+26}px;top:{PAN[3]["y"]+292}px;text-align:right;width:{PW-52}px;font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.12em;color:#FFC700;text-transform:uppercase;z-index:12">Now building: Ekavya Ranges</div>'
        f'<div class=chk data-n="wish" style="position:absolute;left:0;right:0;top:1252px;text-align:center;font-size:34px;font-weight:600;color:{CREAM};white-space:nowrap;z-index:12">Wishing you light, love and a bright year ahead</div>')
html = page("".join(parts), body)
asyncio.run(shoot(html, f"{R}/out/four/mega_diwali_v3.png"))
