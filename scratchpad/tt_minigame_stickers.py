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

S = {}
# 1 GUESS THE SENTENCE WITH HEADPHONES: headphones + an orchid speech bubble holding a question mark
S["headphones"] = (stroke("M58,160 C58,76 182,76 182,160", G, 20) + rect(36, 134, 46, 78, 20, G) + rect(158, 134, 46, 78, 20, G)
    + rect(52, 152, 14, 42, 7, C) + rect(174, 152, 14, 42, 7, C)
    + rect(132, 14, 92, 62, 22, O) + poly("150,70 146,96 176,72", O)
    + stroke("M162,36 a14,14 0 1 1 22,11 q-8,6 -8,15", K, 8) + circ(176, 66, 5, K))
# 2 FLIP THE CUP: a tipping cup with a blue arrow curling over it
S["cup_flip"] = ('<g transform="rotate(-24 120 140)">' + poly("78,84 162,84 148,206 92,206", G) + rect(70, 74, 100, 20, 10, C, f'stroke="{C}"')
    + rect(100, 122, 40, 16, 8, C) + '</g>' + stroke("M52,104 C40,40 130,14 184,52", B, 14) + poly("196,58 160,62 180,30", B)
    + circ(204, 150, 8, O) + circ(34, 170, 6, O))
# 3 JENGA WITH DARES: a block tower with one block pulled out and a dare burst
blocks = ""
for i, y in enumerate((178, 130, 82)):
    if i % 2 == 0:
        blocks += rect(52, y, 136, 40, 8, G) + stroke(f"M92,{y+6} V{y+34} M132,{y+6} V{y+34}", C, 5)
    else:
        blocks += rect(52, y, 40, 40, 8, G) + rect(100, y, 40, 40, 8, G) + rect(148, y, 40, 40, 8, B if i == 1 else G)
S["jenga"] = (blocks + rect(150, 30, 70, 40, 8, G, 'transform="rotate(14 185 50)"')
    + poly("34,24 44,52 70,40 52,66 76,86 46,84 30,110 26,80 0,70 28,56", O, 'transform="translate(2 -4) scale(.9)"')
    + stroke("M44,52 V62", K, 6) + circ(44, 72, 3.5, K))
# 4 DARTS: a dartboard with a dart in the bullseye
S["darts"] = (circ(112, 128, 92, G) + circ(112, 128, 68, C) + circ(112, 128, 46, G) + circ(112, 128, 24, O) + circ(112, 128, 8, C)
    + stroke("M118,122 L200,40", B, 12) + poly("196,18 232,16 226,52 214,36", O) + poly("198,46 224,20 232,28 206,54", O))
# 5 TONGUE TWISTERS: a green speech bubble with a wavy twist and an orchid tongue
S["tongue"] = (rect(22, 30, 196, 124, 40, G) + poly("70,150 56,206 112,152", G)
    + stroke("M56,88 C76,58 92,118 112,88 S148,58 168,88 S190,108 192,90", C, 11)
    + '<path d="M132,146 C128,206 194,206 190,146 Z" fill="%s"/>' % O + stroke("M161,160 V186", K, 5))
# 6 PUSH UP CHALLENGE: side-on figure mid push-up
S["pushup"] = (rect(14, 196, 212, 14, 7, O) + circ(46, 98, 24, G) + stroke("M70,122 L196,170", G, 30) + stroke("M96,134 V196", G, 22) + stroke("M196,170 L214,196", G, 20)
    + stroke("M120,56 V28 M100,40 L120,22 L140,40", B, 12))
# 7 PLANK CHALLENGE: horizontal body on forearms plus a blue stopwatch
S["plank"] = (rect(14, 196, 212, 14, 7, O) + circ(44, 120, 24, G) + stroke("M70,138 L190,166", G, 30) + stroke("M84,150 L70,196 H110", G, 22) + stroke("M190,166 L212,196", G, 20)
    + circ(176, 56, 40, B) + circ(176, 56, 28, C) + stroke("M176,56 V38 M176,56 L190,64", K, 7) + rect(164, 8, 24, 12, 4, B))
# 8 AIM THE CUP: a cup with a ball arcing in along a dashed path
S["aim_cup"] = (poly("120,120 204,120 190,226 134,226", G) + rect(112, 110, 100, 20, 10, C) + rect(142, 158, 40, 16, 8, C)
    + stroke("M22,200 C40,40 150,20 162,96", B, 10, 'stroke-dasharray="4 20"') + circ(164, 78, 22, O) + stroke("M150,70 C160,62 170,62 178,70", C, 5))
# 9 COIN DROP: coins falling into a glass jar
S["coin_drop"] = (rect(60, 100, 120, 128, 22, G) + rect(52, 90, 136, 20, 10, C) + rect(76, 170, 88, 14, 7, Y) + rect(76, 190, 88, 14, 7, Y) + rect(82, 150, 76, 14, 7, Y)
    + circ(120, 50, 30, Y) + circ(120, 50, 19, Y, 'stroke="#B98A00" stroke-width="5"') + stroke("M76,22 V50 M164,22 V50", B, 9))

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
