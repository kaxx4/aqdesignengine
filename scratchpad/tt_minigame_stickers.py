"""TerraThon Mini-Fete MINI-GAME STICKERS (user, 2026-10-01: "use stickers instead of pictures because we don't have them. Make your own stickers if required").
Nine flat vector stickers drawn in the kit's die-cut style: green silhouettes with cream detail, a cream die-cut halo (feMorphology dilate of the whole silhouette), and kit-blue / orchid
accents. Original artwork, no photos. Each is written to engine/assets/terrathon/minigames/<slug>.svg (240x240 viewBox, no text so it survives <img> embedding).
Slugs: headphones, cup_flip, jenga, darts, tongue, pushup, plank, aim_cup, coin_drop.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_minigame_stickers.py   (writes the svgs and a contact sheet out/collaterals/minigame_stickers_sheet.png)
"""
import os, asyncio
G, B, O, C, K, Y = "#2FD284", "#1E88E5", "#DE68F0", "#F3ECDE", "#0A0A0A", "#FFC700"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "engine", "assets", "terrathon", "minigames")

def stroke(d, col, w, extra=""): return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def rect(x, y, w, h, r, fill, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'
def circ(x, y, r, fill, extra=""): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'
def poly(pts, fill, extra=""): return f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="2" stroke-linejoin="round" {extra}/>'

GD, BL, OL, YD = "#1B9A63", "#8FCBFF", "#F4B1FB", "#C79500"
def line(x1, y1, x2, y2, col, w): return stroke(f"M{x1},{y1} L{x2},{y2}", col, w)
S = {}
# 1 GUESS THE SENTENCE WITH HEADPHONES: shaded headphones, sound waves, a bubble with a question mark
S["headphones"] = (stroke("M54,168 C54,70 186,70 186,168", GD, 26) + stroke("M54,168 C54,70 186,70 186,168", G, 18) + stroke("M70,128 C84,92 156,92 170,128", C, 5)
    + rect(30, 132, 52, 88, 24, GD) + rect(30, 128, 52, 88, 24, G) + rect(158, 132, 52, 88, 24, GD) + rect(158, 128, 52, 88, 24, G)
    + rect(44, 148, 24, 56, 12, C) + rect(172, 148, 24, 56, 12, C) + circ(56, 176, 7, G) + circ(184, 176, 7, G)
    + stroke("M12,150 Q4,172 12,194 M228,150 Q236,172 228,194", B, 7)
    + rect(116, 8, 112, 70, 26, OL) + rect(112, 4, 112, 70, 26, O) + poly("140,66 134,98 166,68", O)
    + stroke("M150,28 a15,15 0 1 1 24,12 q-9,6 -9,17", K, 9) + circ(166, 63, 5.5, K))
# 2 FLIP THE CUP: cup mid-flip inside a circular arrow, water drops flying off
S["cup_flip"] = ('<g transform="rotate(158 120 122)">' + poly("80,70 160,70 148,200 92,200", GD) + poly("84,70 156,70 145,196 95,196", G)
    + rect(72, 56, 96, 20, 10, C) + rect(104, 112, 32, 14, 7, C) + rect(100, 140, 40, 14, 7, C) + '</g>'
    + stroke("M46,150 C20,70 90,16 160,32 C196,40 214,84 204,122", B, 12) + poly("186,120 224,118 206,150", B)
    + circ(76, 206, 8, BL) + circ(112, 224, 6, BL) + circ(166, 214, 7, BL) + circ(40, 60, 7, O) + circ(214, 40, 6, O))
# 3 JENGA WITH DARES: wooden tower with grain, one blue block mid-pull, a dare card
def jrow(y, flip):
    if not flip: return rect(44, y, 152, 42, 9, GD) + rect(44, y, 152, 38, 9, G) + stroke(f"M70,{y+12} H110 M130,{y+22} H168", GD, 4)
    return "".join(rect(44 + i * 52, y + 3, 48, 38, 9, GD) + rect(44 + i * 52, y, 48, 38, 9, B if (i == 2 and y == 132) else G) for i in range(3))
S["jenga"] = (jrow(188, False) + jrow(144, True) + jrow(100, False) + jrow(56, True)
    + rect(200, 100, 44, 20, 8, B, 'transform="rotate(-8 222 110)"') + poly("34,8 70,8 70,44 34,44", O, 'transform="rotate(-10 52 26)"') + stroke("M52,18 V30", K, 8) + circ(52, 38, 4, K))
# 4 DARTS: board with spokes and rings, dart with striped flights
S["darts"] = (circ(112, 130, 98, GD) + circ(112, 130, 92, G) + circ(112, 130, 66, C) + circ(112, 130, 44, G) + circ(112, 130, 22, O) + circ(112, 130, 7, C)
    + "".join(line(112 + 66 * __import__("math").cos(a * 0.5236), 130 + 66 * __import__("math").sin(a * 0.5236), 112 + 92 * __import__("math").cos(a * 0.5236), 130 + 92 * __import__("math").sin(a * 0.5236), GD, 4) for a in range(12))
    + stroke("M116,126 L192,52", K, 16) + stroke("M116,126 L192,52", B, 10)
    + poly("186,24 232,16 224,62 210,44", O) + poly("200,60 232,52 226,84", OL) + stroke("M206,30 L218,50", C, 4)
    + stroke("M214,96 L236,104 M208,112 L226,128", B, 6))
# 5 TONGUE TWISTERS: a bubble with a tongue tied in a knot
S["tongue"] = (rect(14, 22, 212, 138, 44, G) + poly("68,154 54,214 118,158", G)
    + stroke("M48,98 C58,48 108,52 106,94 C104,134 64,124 78,92 C90,58 142,56 148,92 C152,118 176,122 192,84", O, 20) + stroke("M48,98 C58,48 108,52 106,94", OL, 5)
    + circ(192, 84, 13, O) + stroke("M192,76 V92", K, 5) + circ(36, 40, 5, C) + circ(210, 140, 5, C))
# 6 PUSH UP CHALLENGE: athletic figure side-on, far limbs shaded, sweat and an up arrow
S["pushup"] = (rect(10, 202, 220, 16, 8, O) + stroke("M104,150 V202", GD, 22) + stroke("M60,128 L206,176", GD, 34)
    + stroke("M82,150 V202", G, 22) + stroke("M60,126 L204,172", G, 32) + stroke("M204,172 L222,202", G, 22) + rect(204, 194, 30, 14, 7, C)
    + circ(46, 100, 25, G) + stroke("M32,84 Q46,72 62,82", K, 6) + rect(52, 62, 34, 14, 7, B, 'transform="rotate(-18 69 69)"')
    + stroke("M138,70 V30 M116,48 L138,26 L160,48", B, 12) + circ(22, 66, 5, BL) + circ(14, 86, 4, BL))
# 7 PLANK CHALLENGE: forearm plank with a stopwatch
S["plank"] = (rect(10, 202, 220, 16, 8, O) + stroke("M56,160 H112", GD, 22) + stroke("M52,150 L196,176", GD, 34)
    + stroke("M52,146 L194,170", G, 32) + stroke("M194,170 L220,202", G, 22) + rect(204, 194, 30, 14, 7, C) + stroke("M60,160 H112", G, 22)
    + circ(44, 126, 25, G) + stroke("M30,112 Q44,100 60,110", K, 6)
    + circ(176, 62, 42, B) + circ(176, 62, 30, C) + stroke("M176,62 V42 M176,62 L192,72", K, 7) + rect(164, 8, 24, 12, 4, B) + rect(206, 24, 14, 10, 4, B, 'transform="rotate(40 213 29)"')
    + "".join(line(176 + 24 * __import__("math").sin(t * 0.5236), 62 - 24 * __import__("math").cos(t * 0.5236), 176 + 28 * __import__("math").sin(t * 0.5236), 62 - 28 * __import__("math").cos(t * 0.5236), K, 3) for t in range(12)))
# 8 AIM THE CUP: striped cup, ball flying in along a dotted arc
S["aim_cup"] = (poly("110,118 214,118 198,230 126,230", GD) + poly("114,118 210,118 195,226 129,226", G) + rect(100, 104, 124, 22, 11, C)
    + rect(132, 150, 60, 14, 7, C) + rect(136, 180, 52, 14, 7, C)
    + stroke("M20,206 C34,40 160,10 170,74", B, 10, 'stroke-dasharray="2 22"') + circ(172, 70, 24, O) + stroke("M156,62 C164,52 178,52 186,60", OL, 6) + circ(34, 34, 6, Y) + circ(220, 40, 6, Y) + circ(214, 76, 4, C))
# 9 COIN DROP: glass jar with a coin stack, a coin dropping in
S["coin_drop"] = (rect(56, 100, 128, 132, 26, "#C9F3E3") + rect(56, 100, 128, 132, 26, "none", f'stroke="{G}" stroke-width="9"') + rect(46, 88, 148, 22, 11, C)
    + rect(94, 92, 52, 10, 5, K) + "".join(rect(72, 200 - i * 20, 96, 16, 8, Y) + rect(72, 208 - i * 20, 96, 6, 3, YD) for i in range(3))
    + circ(120, 40, 32, Y) + circ(120, 40, 32, "none", f'stroke="{YD}" stroke-width="5"') + circ(120, 40, 20, "none", f'stroke="{YD}" stroke-width="5"') + stroke("M120,28 L124,38 L134,38 L126,44 L129,54 L120,48 L111,54 L114,44 L106,38 L116,38 Z", YD, 3)
    + stroke("M64,18 V50 M176,18 V50 M92,6 V30 M148,6 V30", B, 8))

HALO = f'<filter id="h" x="-15%" y="-15%" width="130%" height="130%"><feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/><feFlood flood-color="{C}"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
def svg(slug): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 264 264" width="264" height="264"><defs>{HALO}</defs><g filter="url(#h)">{S[slug]}</g></svg>'

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug in S: open(os.path.join(OUT, slug + ".svg"), "w").write(svg(slug))
    from playwright.async_api import async_playwright
    cells = "".join(f'<div style="display:inline-block;width:300px;text-align:center;color:#fff;font:14px sans-serif">{svg(s)}<div>{s}</div></div>' for s in S)
    async def main():
        async with async_playwright() as pw:
            br = await pw.chromium.launch(); pg = await br.new_page(viewport={"width": 960, "height": 980})
            await pg.set_content(f'<body style="background:#000;margin:10px">{cells}</body>'); await pg.screenshot(path=os.path.join(ROOT, "out", "collaterals", "minigame_stickers_sheet.png")); await br.close()
    os.makedirs(os.path.join(ROOT, "out", "collaterals"), exist_ok=True); asyncio.run(main()); print("ok")
