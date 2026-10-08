"""STICKER KIT for the REVER x DISCO DIWALI deck, drawn in the TerraThon die-cut treatment (user, 2026-10-08: "do a terrathon style where you generate fresh stickers").

Flat fills in the kit palette (green / blue / orchid / cream, kit-ink details), a darker shade of the same hue for volume, a cream die-cut halo with a hand-cut rough edge
(the feMorphology + turbulence filter from tt_dd_tickets.py). NO text inside any sticker, so every one survives <img> / inline embedding. Original artwork, no photos.
Re-used from tt_dd_tickets.py: disco_ball, diya, ticket, spark.  New here: mask (the masquerade hero), cloche, burger, pin, camera, phone, megaphone, review, shirt,
clock, badge, record, clipboard, psign, heart.

Each builder returns (svg_html, w, h) for a requested width.  Run `python scratchpad/rever_deck_stickers.py` for a contact sheet -> scratchpad/work/stickers_sheet.png.
"""
import importlib.util, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py"))
ddt = importlib.util.module_from_spec(spec); spec.loader.exec_module(ddt)
die_filter, star4, disco_ball, diya, ticket, spark = ddt.die_filter, ddt.star4, ddt.disco_ball, ddt.diya, ddt.ticket, ddt.spark

G, GD, B, BD, BL = "#2FD284", "#1B9A63", "#1E88E5", "#1666B8", "#8FCBFF"
O, OD, OL = "#DE68F0", "#B445C8", "#F4B1FB"
C, K, Y, YD = "#F3ECDE", "#0A0A0A", "#FFC700", "#C79500"
NAVY = "#0A3D8F"
_n = [0]


def stroke(d, col, w, extra=""): return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def rect(x, y, w, h, r, fill, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'
def circ(x, y, r, fill, extra=""): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'
def poly(pts, fill, extra=""): return f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="2" stroke-linejoin="round" {extra}/>'
def path(d, fill, extra=""): return f'<path d="{d}" fill="{fill}" {extra}/>'
def line(x1, y1, x2, y2, col, w): return stroke(f"M{x1},{y1} L{x2},{y2}", col, w)


def wrap(art, vb, width, seed, halo=11, rough=7):
    """Die-cut a drawing: returns (svg, w, h). vb = (x, y, w, h) in drawing units."""
    _n[0] += 1
    fid = f"rds{_n[0]}"
    h = width * vb[3] / vb[2]
    svg = (f'<svg width="{width:.1f}" height="{h:.1f}" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" overflow="visible" style="display:block">'
           f'<defs>{die_filter(fid, seed, halo, rough)}</defs><g filter="url(#{fid})">{art}</g></svg>')
    return svg, width, h


def _clip(cid, d): return f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'


# ---------------------------------------------------------------- the masquerade mask (hero)
_MASK = ("M160,52 C120,24 54,32 20,84 C6,108 12,130 34,140 C70,160 116,160 138,134 C148,124 154,120 160,120 "
         "C166,120 172,124 182,134 C204,160 250,160 286,140 C308,130 314,108 300,84 C266,32 200,24 160,52 Z")


def mask(width=420, main=O, dark=OD, accent=G, plume=True, seed=3, flip=False):
    _n[0] += 1; u = f"mk{_n[0]}"
    feather = lambda ox, oy, ex, ey, wd, col, sp: (
        f'<path d="M{ox},{oy} Q{(ox+ex)/2 - wd},{(oy+ey)/2 - wd*.2} {ex},{ey} Q{(ox+ex)/2 + wd*.2},{(oy+ey)/2 + wd} {ox},{oy} Z" fill="{col}"/>'
        + stroke(f"M{ox},{oy} L{ex},{ey}", sp, 5))
    pl = ""
    if plume:
        pl = (feather(240, 66, 318, -74, 70, accent, GD if accent == G else BD)
              + feather(252, 74, 376, -14, 64, B if accent == G else G, BD if accent == G else GD)
              + feather(260, 84, 372, 52, 54, C, "#BDB49C"))
    body = (_clip(u, _MASK) + path(_MASK, dark)
            + f'<g clip-path="url(#{u})">' + path(_MASK, main) + f'<ellipse cx="160" cy="176" rx="190" ry="34" fill="{dark}"/>'
            + stroke("M40,70 C70,48 100,40 128,44", C, 7, 'opacity=".85"') + '</g>'
            + f'<g transform="translate(160 96) scale(.9) translate(-160 -96)">' + stroke(_MASK, C, 5, 'stroke-dasharray="1 15"') + '</g>'
            + path("M48,92 C72,66 124,70 142,108 C114,128 66,126 48,92 Z", K) + path("M272,92 C248,66 196,70 178,108 C206,128 254,126 272,92 Z", K)
            + circ(76, 90, 7, C) + circ(244, 90, 7, C)
            + stroke("M44,70 C70,38 124,40 150,82", accent, 8) + stroke("M276,70 C250,38 196,40 170,82", accent, 8)
            + poly("160,66 178,90 160,114 142,90", accent) + poly("160,76 169,90 160,104 151,90", C)
            + "".join(circ(x, y, 6, C) for x, y in [(52, 128), (82, 146), (120, 150), (200, 150), (238, 146), (268, 128)]))
    s = f'<g transform="translate(320 0) scale(-1 1)">{pl}{body}</g>' if flip else pl + body
    vb = (-10, -96, 400, 300) if plume else (0, 10, 320, 190)
    return wrap(s, vb, width, seed, 11, 7)


# ---------------------------------------------------------------- food
def cloche(width=300, seed=5):
    d = "M26,186 C26,100 68,62 120,62 C172,62 214,100 214,186 Z"
    art = (ellipse(120, 204, 110, 22, B) + ellipse(120, 194, 110, 22, C) + ellipse(120, 190, 96, 14, BL)
           + path(d, GD) + path("M34,182 C34,108 72,70 118,70 C158,70 192,92 203,142 C206,156 206,170 206,182 Z", G)
           + stroke("M56,142 C58,112 76,92 100,84", C, 9) + circ(120, 50, 15, C) + rect(104, 58, 32, 10, 5, GD) + circ(116, 46, 5, "#fff", 'opacity=".7"')
           + stroke("M84,30 q-14,-14 0,-28 q14,-14 0,-28", B, 7, 'transform="translate(0 28)"') + stroke("M150,30 q-14,-14 0,-28", B, 7, 'transform="translate(0 24)"')
           + star4(206, 42, 20, O, 0, .3) + star4(30, 90, 12, Y, 0, .3))
    return wrap(art, (0, -24, 240, 270), width, seed)


def ellipse(cx, cy, rx, ry, fill, extra=""): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def burger(width=300, seed=8):
    bun_top = "M24,116 C24,64 68,40 120,40 C172,40 216,64 216,116 Z"
    art = (path("M30,178 H210 Q210,210 180,212 H60 Q30,210 30,178 Z", YD) + path("M30,172 H210 Q210,202 180,204 H60 Q30,202 30,172 Z", Y)
           + rect(22, 140, 196, 36, 18, "#7A3F1D") + rect(22, 140, 196, 26, 16, "#9A5128")
           + path("M18,126 q14,-14 28,0 t28,0 t28,0 t28,0 t28,0 t28,0 t28,0 V142 H18 Z", G)
           + rect(30, 118, 180, 12, 6, O)
           + path(bun_top, YD) + path("M30,112 C30,66 70,46 120,46 C160,46 196,62 208,100 C210,106 210,110 210,112 Z", Y)
           + "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="{C}" transform="rotate({r} {x} {y})"/>' for x, y, r in [(74, 70, -20), (112, 58, 8), (150, 68, 24), (96, 92, 12), (138, 92, -14), (178, 92, 20)])
           + star4(214, 40, 18, G, 0, .3))
    return wrap(art, (0, 20, 240, 210), width, seed)


# ---------------------------------------------------------------- the rest of the kit
def pin(width=260, seed=4):
    d = "M120,14 C70,14 38,52 38,94 C38,150 120,226 120,226 C120,226 202,150 202,94 C202,52 170,14 120,14 Z"
    art = (ellipse(120, 228, 64, 10, BL) + path(d, GD) + path("M120,14 C70,14 38,52 38,94 C38,128 70,172 100,200 C86,160 78,120 92,70 C100,44 116,28 140,18 C132,15 126,14 120,14 Z", G)
           + path("M120,14 C170,14 202,52 202,94 C202,150 120,226 120,226 C150,170 160,100 120,14 Z", GD, 'opacity=".55"')
           + circ(120, 94, 46, C) + star4(120, 94, 34, O, 0, .36) + circ(120, 94, 8, C)
           + star4(204, 30, 16, Y, 0, .3) + star4(30, 150, 12, B, 0, .3))
    return wrap(art, (0, 0, 240, 244), width, seed)


def camera(width=300, seed=6):
    art = (rect(76, 54, 76, 34, 10, BD) + rect(76, 50, 76, 34, 10, B) + circ(54, 62, 12, O) + rect(168, 62, 40, 20, 7, Y)
           + rect(20, 78, 200, 126, 26, BD) + rect(20, 72, 200, 126, 26, B) + rect(20, 100, 200, 14, 0, C, 'opacity=".9"')
           + circ(120, 140, 50, C) + circ(120, 140, 42, O) + circ(120, 140, 32, K) + circ(120, 140, 22, BL) + circ(110, 130, 7, "#fff") + circ(130, 150, 4, "#fff")
           + circ(190, 98, 7, O) + star4(214, 40, 18, G, 0, .3) + star4(24, 36, 12, O, 0, .3))
    return wrap(art, (0, 20, 240, 200), width, seed)


def phone(width=230, seed=9):
    art = (rect(62, 8, 116, 224, 26, OD) + rect(62, 4, 116, 224, 26, O) + rect(72, 20, 96, 192, 16, C) + rect(104, 12, 32, 6, 3, OD)
           + rect(72, 20, 96, 192, 16, K, 'opacity="0"') + circ(120, 108, 34, G) + poly("108,90 108,126 140,108", C)
           + rect(84, 164, 72, 8, 4, K) + rect(84, 182, 48, 8, 4, BL) + circ(92, 36, 8, B)
           + path("M206,62 C186,48 186,30 198,24 C206,20 212,26 212,26 C212,26 218,20 226,24 C238,30 236,48 216,62 Z", B, 'transform="translate(-6 8)"')
           + star4(32, 70, 16, Y, 0, .3) + star4(204, 170, 14, G, 0, .3))
    return wrap(art, (10, 0, 240, 244), width, seed)


def megaphone(width=300, seed=10):
    art = (path("M62,96 L176,40 L176,176 L62,124 Z", OD) + path("M62,92 L176,36 L176,166 L62,120 Z", O) + ellipse(176, 102, 20, 66, OL) + ellipse(178, 102, 12, 44, OD)
           + rect(30, 90, 46, 36, 12, BD) + rect(30, 86, 46, 36, 12, B) + path("M72,122 H106 L116,188 Q116,200 104,200 H88 Q76,200 74,188 Z", BD) + path("M72,118 H104 L112,182 Q112,194 100,194 H88 Q76,194 74,182 Z", B)
           + stroke("M204,60 q26,42 0,84", G, 9) + stroke("M226,38 q40,64 0,128", G, 9) + star4(40, 40, 18, Y, 0, .3) + star4(212, 200, 14, O, 0, .3))
    return wrap(art, (10, 10, 250, 210), width, seed)


def _star5(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * .46
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return poly(" ".join(pts), fill)


def review(width=330, seed=12):
    art = (rect(12, 40, 216, 124, 42, BD) + rect(12, 34, 216, 124, 42, B) + poly("62,150 48,202 108,156", B)
           + "".join(_star5(46 + i * 37, 98, 19, YD) + _star5(46 + i * 37, 95, 18, Y) for i in range(5))
           + star4(222, 28, 18, G, 0, .3) + star4(14, 190, 12, O, 0, .3))
    return wrap(art, (0, 10, 240, 205), width, seed)


def shirt(width=290, seed=13):
    body = "M70,34 L102,22 Q120,46 138,22 L170,34 L226,84 L198,118 L174,100 L174,208 L66,208 L66,100 L42,118 L14,84 Z"
    art = (path(body, OD, 'transform="translate(0 6)"') + path(body, O) + path("M66,100 L66,208 L100,208 L100,40 L70,34 Z", OL, 'opacity=".45"')
           + stroke("M102,22 Q120,46 138,22", C, 9) + stroke("M26,100 L48,118 M214,100 L192,118", C, 7)
           + circ(120, 128, 32, C) + circ(120, 128, 26, G) + path("M104,120 q8,-12 20,-6 q8,6 2,16 q-6,10 -16,6 q-10,-4 -6,-16 Z", B) + path("M126,138 q10,-4 12,6 q-8,6 -12,-6 Z", C)
           + star4(222, 36, 16, Y, 0, .3) + star4(24, 196, 12, G, 0, .3))
    return wrap(art, (0, 10, 240, 214), width, seed)


def clock(width=260, seed=14):
    art = (circ(60, 40, 26, O) + circ(180, 40, 26, O) + circ(120, 130, 92, BD) + circ(120, 126, 92, B) + circ(120, 126, 78, C)
           + "".join(line(120 + 62 * math.sin(t * .5236), 126 - 62 * math.cos(t * .5236), 120 + 70 * math.sin(t * .5236), 126 - 70 * math.cos(t * .5236), K, 6) for t in range(12))
           + stroke("M120,126 L120,80", K, 9) + stroke("M120,126 L156,146", K, 9) + circ(120, 126, 9, O)
           + path("M120,126 L120,48 A78,78 0 0 1 160,60 Z", G, 'opacity=".55"')
           + stroke("M62,214 L50,236 M178,214 L190,236", B, 9) + star4(222, 90, 14, Y, 0, .3))
    return wrap(art, (0, 4, 240, 244), width, seed)


def badge(width=230, seed=15):
    art = (stroke("M82,-6 L120,58 M158,-6 L120,58", B, 16) + rect(104, 44, 32, 24, 7, BD)
           + rect(48, 62, 144, 176, 22, "#CDBFA0") + rect(48, 56, 144, 176, 22, C)
           + circ(120, 112, 30, G) + path("M78,176 C78,146 162,146 162,176 V178 H78 Z", G) + circ(120, 112, 30, "none", f'stroke="{GD}" stroke-width="0"')
           + rect(74, 190, 92, 10, 5, K) + rect(86, 208, 68, 8, 4, BL) + rect(48, 100, 0, 0, 0, K) + star4(190, 60, 14, O, 0, .3))
    return wrap(art, (20, -10, 200, 262), width, seed)


def record(width=300, seed=16):
    ring = "".join(circ(110, 136, r, "none", f'stroke="#2C2C30" stroke-width="3"') for r in (80, 68, 56, 44))
    art = (circ(110, 136, 98, K) + ring + circ(110, 136, 32, G) + star4(110, 136, 22, C, 0, .4) + circ(110, 136, 6, K)
           + stroke("M44,86 C56,58 80,44 108,42", "#fff", 7, 'opacity=".6"')
           + stroke("M214,26 L170,112", BD, 12) + stroke("M214,26 L170,112", B, 8) + rect(150, 100, 34, 22, 6, O, 'transform="rotate(28 167 111)"') + circ(214, 26, 12, O)
           + path("M18,64 V24 L48,16 V56", "none", f'stroke="{O}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"') + circ(14, 66, 10, O) + circ(44, 58, 10, O)
           + star4(222, 190, 16, Y, 0, .3))
    return wrap(art, (0, 0, 250, 244), width, seed)


def clipboard(width=250, seed=17):
    chk = lambda y: stroke(f"M82,{y} l10,10 l18,-20", G, 9) + rect(124, y - 6, 52, 10, 5, K) + rect(124, y + 10, 36, 8, 4, BL)
    art = (rect(40, 30, 160, 204, 24, BD) + rect(40, 24, 160, 204, 24, B) + rect(56, 50, 128, 164, 12, C)
           + chk(92) + chk(140) + chk(188) + rect(86, 10, 68, 38, 14, OD) + rect(86, 6, 68, 38, 14, O) + circ(120, 22, 8, C)
           + star4(210, 40, 16, Y, 0, .3) + star4(24, 200, 12, G, 0, .3))
    return wrap(art, (10, 0, 230, 244), width, seed)


def psign(width=230, seed=18):
    art = (rect(106, 140, 28, 92, 10, BL) + rect(44, 14, 152, 152, 32, BD) + rect(44, 8, 152, 152, 32, B) + rect(56, 20, 128, 128, 22, "none", f'stroke="{C}" stroke-width="5"')
           + rect(86, 40, 22, 90, 5, C) + path("M100,40 H128 A28,28 0 0 1 128,96 H100 Z", C) + path("M108,56 H126 A12,12 0 0 1 126,80 H108 Z", B)
           + star4(204, 20, 16, O, 0, .3) + star4(30, 190, 12, G, 0, .3))
    return wrap(art, (10, 0, 220, 240), width, seed)


def heart(width=200, seed=19):
    d = "M120,208 C40,152 24,110 24,76 C24,44 48,26 74,26 C98,26 112,40 120,58 C128,40 142,26 166,26 C192,26 216,44 216,76 C216,110 200,152 120,208 Z"
    art = (path(d, OD) + path(d, O, 'transform="translate(-4 -6)"') + stroke("M52,76 C52,60 62,50 78,50", C, 9, 'opacity=".9"') + star4(214, 30, 16, Y, 0, .3))
    return wrap(art, (0, 10, 240, 210), width, seed)


def calendar(width=240, seed=20):
    art = (rect(24, 44, 192, 176, 28, "#CDBFA0") + rect(24, 38, 192, 176, 28, C) + path("M24,66 a28,28 0 0 1 28,-28 H188 a28,28 0 0 1 28,28 V92 H24 Z", O)
           + rect(62, 14, 16, 44, 8, B) + rect(162, 14, 16, 44, 8, B)
           + "".join(rect(46 + i * 48, 112 + j * 34, 30, 22, 6, K if (i, j) != (2, 1) else G) for i in range(4) for j in range(3)) + star4(222, 44, 16, Y, 0, .3))
    return wrap(art, (10, 0, 240, 230), width, seed)


KIT = dict(mask=mask, cloche=cloche, burger=burger, pin=pin, camera=camera, phone=phone, megaphone=megaphone, review=review, shirt=shirt, clock=clock,
           badge=badge, record=record, clipboard=clipboard, psign=psign, heart=heart, calendar=calendar)


def sheet():
    import asyncio
    tiles = []
    for name, fn in KIT.items():
        svg, w, h = fn(width=300) if name != "mask" else mask(width=340)
        tiles.append(f'<div style="width:380px;height:330px;display:flex;align-items:center;justify-content:center;position:relative">{svg}'
                     f'<span style="position:absolute;left:8px;bottom:4px;color:#888;font:14px monospace">{name}</span></div>')
    for name, fn in dict(disco=lambda width: disco_ball(width), diya=lambda width: diya(width), ticket=lambda width: ticket(width)).items():
        svg, h = fn(300)
        tiles.append(f'<div style="width:380px;height:330px;display:flex;align-items:center;justify-content:center">{svg}</div>')
    html = f'<html><body style="margin:0;background:#000"><div style="display:flex;flex-wrap:wrap;width:{380*5}px">{"".join(tiles)}</div></body></html>'
    return html


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    html = sheet(); p = os.path.join(ROOT, "scratchpad", "work", "stickers_sheet.html"); open(p, "w").write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1900, "height": 1650}); pg.goto("file://" + p); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(ROOT, "scratchpad", "work", "stickers_sheet.png"), full_page=True); b.close()
    print("sheet written")
