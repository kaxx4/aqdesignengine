"""Six extra die-cut stickers for the REVER marketing deck, in the same TerraThon treatment as rever_deck_stickers.py (flat fills, a darker shade for volume, cream halo
with a hand-cut edge, NO text inside any of them). They cover what the marketing plan talks about and the first kit did not: a podcast mic, a broadcast chat,
a schoolhouse, and the Instagram outcomes (views, shares, follows). Generic drawings: no Instagram or WhatsApp logos.

Each returns (svg_html, w, h) for a requested width. `python scratchpad/rever_marketing_stickers.py` writes a contact sheet to scratchpad/work/marketing_stickers_sheet.png.
"""
import importlib.util, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("rever_deck_stickers", os.path.join(ROOT, "scratchpad", "rever_deck_stickers.py"))
stk = importlib.util.module_from_spec(_s); _s.loader.exec_module(stk)
wrap, rect, circ, path, poly, stroke, line, star4, ellipse = stk.wrap, stk.rect, stk.circ, stk.path, stk.poly, stk.stroke, stk.line, stk.star4, stk.ellipse
G, GD, B, BD, BL, O, OD, OL, C, K, Y = stk.G, stk.GD, stk.B, stk.BD, stk.BL, stk.O, stk.OD, stk.OL, stk.C, stk.K, stk.Y


def mic(width=240, seed=31):
    grille = "".join(line(92, y, 148, y, BL, 6) for y in (40, 62, 84, 106))
    art = (rect(78, 20, 84, 132, 42, BD) + rect(78, 14, 84, 132, 42, B) + grille + rect(78, 120, 84, 12, 0, OD, 'opacity="0"')
           + stroke("M50,104 C50,158 82,186 120,186 C158,186 190,158 190,104", O, 15) + line(120, 186, 120, 210, O, 15) + rect(74, 206, 92, 18, 9, OD) + rect(74, 202, 92, 18, 9, O)
           + star4(212, 36, 16, Y, 0, .3) + star4(28, 50, 12, G, 0, .3))
    return wrap(art, (0, 0, 240, 236), width, seed)


def chat(width=300, seed=32):
    big = "M44,36 H176 a28,28 0 0 1 28,28 V116 a28,28 0 0 1 -28,28 H104 L66,182 V144 H44 a28,28 0 0 1 -28,-28 V64 a28,28 0 0 1 28,-28 Z"
    art = (path(big, GD, 'transform="translate(5 8)"') + path(big, G) + circ(72, 90, 10, C) + circ(110, 90, 10, C) + circ(148, 90, 10, C)
           + f'<g transform="translate(112 112) scale(.74)">' + path(big, OD, 'transform="translate(5 8)"') + path(big, O)
           + rect(46, 62, 112, 11, 5, C) + rect(46, 92, 76, 11, 5, C) + '</g>'
           + star4(226, 34, 16, Y, 0, .3) + star4(14, 190, 12, B, 0, .3))
    return wrap(art, (0, 10, 250, 250), width, seed)


def school(width=300, seed=33):
    art = (rect(24, 112, 192, 104, 12, "#7FB6EC") + rect(24, 106, 192, 104, 12, BL) + path("M10,116 L120,40 L230,116 Z", OD, 'transform="translate(0 6)"') + path("M10,112 L120,36 L230,112 Z", O)
           + rect(98, 142, 44, 68, 10, B) + circ(132, 178, 4, C) + "".join(rect(x, 134, 32, 30, 8, C) for x in (40, 168)) + "".join(rect(x + 14, 134, 4, 30, 0, B) for x in (40, 168))
           + circ(120, 80, 14, C) + stroke("M120,80 V70 M120,80 H128", K, 4) + line(120, 36, 120, 4, K, 5) + path("M122,6 L158,18 L122,30 Z", G)
           + star4(222, 40, 16, Y, 0, .3) + star4(22, 70, 12, G, 0, .3))
    return wrap(art, (0, 0, 240, 226), width, seed)


def eye(width=300, seed=34):
    d = "M14,112 C54,46 186,46 226,112 C186,178 54,178 14,112 Z"
    art = (path(d, "#CDBFA0", 'transform="translate(0 9)"') + path(d, "#FFFFFF") + circ(120, 112, 46, BD) + circ(120, 112, 42, B) + circ(120, 112, 26, K) + circ(106, 98, 10, "#fff") + circ(134, 126, 5, "#fff")
           + stroke("M30,112 C62,70 176,70 210,112", O, 7, 'opacity=".9"') + star4(214, 40, 16, Y, 0, .3) + star4(24, 170, 12, G, 0, .3))
    return wrap(art, (0, 20, 240, 190), width, seed)


def plane(width=280, seed=35):
    art = (path("M18,108 L224,26 L118,142 Z", BL) + path("M224,26 L168,206 L118,142 Z", BD) + path("M224,26 L168,206 L118,142 Z", B, 'transform="translate(-4 -4)"')
           + path("M118,142 L100,198 L152,164 Z", OD) + stroke("M12,196 C40,180 60,176 84,184", O, 7, 'stroke-dasharray="1 14"') + star4(36, 40, 16, Y, 0, .3) + star4(216, 196, 12, G, 0, .3))
    return wrap(art, (0, 10, 240, 210), width, seed)


def follow(width=280, seed=36):
    art = (circ(100, 80, 42, GD) + circ(100, 74, 42, G) + path("M24,206 C24,140 62,114 100,114 C138,114 176,140 176,206 Z", GD, 'transform="translate(0 6)"') + path("M24,206 C24,140 62,114 100,114 C138,114 176,140 176,206 Z", G)
           + circ(182, 160, 36, OD, 'transform="translate(3 5)"') + circ(182, 160, 36, O) + line(182, 142, 182, 178, C, 9) + line(164, 160, 200, 160, C, 9)
           + star4(40, 60, 12, Y, 0, .3) + star4(214, 60, 16, B, 0, .3))
    return wrap(art, (0, 10, 240, 220), width, seed)


KIT = dict(mic=mic, chat=chat, school=school, eye=eye, plane=plane, follow=follow)

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    tiles = ""
    for name, fn in KIT.items():
        svg, w, h = fn(width=300)
        tiles += f'<div style="width:380px;height:330px;display:flex;align-items:center;justify-content:center;position:relative">{svg}<span style="position:absolute;left:8px;bottom:4px;color:#888;font:14px monospace">{name}</span></div>'
    p = os.path.join(ROOT, "scratchpad", "work", "marketing_stickers_sheet.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(f'<html><body style="margin:0;background:#000"><div style="display:flex;flex-wrap:wrap;width:{380 * 3}px">{tiles}</div></body></html>')
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1140, "height": 700}); pg.goto("file://" + p); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(ROOT, "scratchpad", "work", "marketing_stickers_sheet.png"), full_page=True); b.close()
    print("sheet written")
