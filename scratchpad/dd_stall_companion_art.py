"""Companion art piece for the Disco Diwali stall story (CLAUDE.md standing rule). Philosophy: out/discodiwali/stall_call/companion/philosophy.md ("Ordinal Light").
Subtle reference only: a plan of 108 bays, a small lamp in each, ONE bay unlit (open). Palette: AQ cream, AQ ink, one tomato signal used once.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_companion_art.py"""
import asyncio, base64, math, os
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "discodiwali", "stall_call", "companion")
FONTS = [d for d, _, f in os.walk("/root/.claude/skills") if "InstrumentSerif-Italic.ttf" in f][0]
CREAM, INK, SIG = "#F4EFE0", "#0A0A0A", "#FF4D2E"
W, H = 2160, 2700
COLS, ROWS, CELL, GAP = 9, 12, 150, 22
GW, GH = COLS * CELL + (COLS - 1) * GAP, ROWS * CELL + (ROWS - 1) * GAP
GX, GY = (W - GW) // 2 + 20, 350
OPEN = (5, 6)                                    # column F, row 07 (0-indexed)
s = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>']
LETTERS = "ABCDEFGHI"
for c in range(COLS):
    x = GX + c * (CELL + GAP) + CELL / 2
    col = SIG if c == OPEN[0] else INK
    s.append(f'<text x="{x}" y="{GY - 44}" text-anchor="middle" class="m" fill="{col}">{LETTERS[c]}</text>')
for r in range(ROWS):
    y = GY + r * (CELL + GAP) + CELL / 2 + 8
    col = SIG if r == OPEN[1] else INK
    s.append(f'<text x="{GX - 52}" y="{y}" text-anchor="end" class="m" fill="{col}">{r + 1:02d}</text>')
for r in range(ROWS):
    for c in range(COLS):
        x = GX + c * (CELL + GAP); y = GY + r * (CELL + GAP)
        cx, cy = x + CELL / 2, y + CELL / 2
        is_open = (c, r) == OPEN
        k = r * COLS + c
        flame = 22 + 14 * (0.5 + 0.5 * math.sin(k * 0.61)) + 6 * math.cos(k * 1.7)     # systematic, never random
        lean = 5 * math.sin(k * 0.37)
        stroke = SIG if is_open else INK
        s.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="6" fill="none" stroke="{INK}" stroke-width="{2 if not is_open else 2}" {"stroke-dasharray=\"3 7\"" if is_open else ""} stroke-opacity="{1 if not is_open else .9}"/>')
        bowl = f'M{cx-26},{cy+8} A26,26 0 0 0 {cx+26},{cy+8} Z'
        if is_open:
            s.append(f'<path d="{bowl}" fill="none" stroke="{SIG}" stroke-width="3"/>')
        else:
            s.append(f'<path d="{bowl}" fill="{INK}"/>')
            tip = flame + 14
            s.append(f'<path d="M{cx},{cy-3} C{cx-12},{cy-10} {cx-6},{cy-tip*.62} {cx+lean},{cy-tip} C{cx+6+lean*.5},{cy-tip*.62} {cx+12},{cy-10} {cx},{cy-3} Z" fill="{INK}"/>')
# header, footer
s.append(f'<text x="{GX}" y="190" class="m" fill="{INK}">PLATE 10 / 11</text>')
s.append(f'<text x="{GX + GW}" y="190" text-anchor="end" class="m" fill="{INK}">BAYS 107 / 108</text>')
s.append(f'<line x1="{GX}" y1="226" x2="{GX + GW}" y2="226" stroke="{INK}" stroke-width="2"/>')
fy = GY + GH + 130
s.append(f'<line x1="{GX}" y1="{fy - 78}" x2="{GX + GW}" y2="{fy - 78}" stroke="{INK}" stroke-width="2"/>')
s.append(f'<text x="{GX}" y="{fy + 62}" class="serif" fill="{INK}">one bay open</text>')
s.append(f'<text x="{GX + GW}" y="{fy + 8}" text-anchor="end" class="m" fill="{INK}">SURVEYED AT DUSK</text>')
s.append(f'<text x="{GX + GW}" y="{fy + 50}" text-anchor="end" class="m" fill="{SIG}">F · 07</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(s) + "</svg>"
b64 = lambda f: base64.b64encode(open(os.path.join(FONTS, f), "rb").read()).decode()
html = f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:IS;src:url(data:font/ttf;base64,{b64("InstrumentSerif-Italic.ttf")})}}
@font-face{{font-family:DM;src:url(data:font/ttf;base64,{b64("DMMono-Regular.ttf")})}}
html,body{{margin:0;background:{CREAM}}} .m{{font-family:DM;font-size:26px;letter-spacing:.22em}} .serif{{font-family:IS;font-style:italic;font-size:150px}}
</style>{svg}'''
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(OUT, "ordinal_light.png")); await b.close()
    print("done", GX, GY, GW, GH, "grid bottom", GY + GH, "footer", fy)
asyncio.run(main())
