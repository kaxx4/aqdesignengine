import asyncio, os, base64, random, math

FONTDIR = "/root/.claude/skills/synced/38d67b45-df55-409d-be12-6b62181fe978_87846feb-1ca9-4b65-a508-b752d233935d/canvas-design/canvas-fonts"
def b64font(name, mime="font/ttf"):
    with open(os.path.join(FONTDIR, name), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

MONO_R = b64font("IBMPlexMono-Regular.ttf")
MONO_B = b64font("IBMPlexMono-Bold.ttf")
SER_I  = b64font("CrimsonPro-Italic.ttf")
SER_R  = b64font("CrimsonPro-Regular.ttf")

W, H = 1600, 2000
CREAM = "#F4EFE0"
INK = "#0A0A0A"
TOMATO = "#FF4D2E"
PAPER2 = "#EDE6D0"

random.seed(7)

# ---- build the tally field: rows of small numbered case-marks, density building toward the seal ----
rows = 26
cols = 14
mL, mR, mT = 90, 90, 130
cell_w = (W - mL - mR) / cols
cell_h = 66
tallies = []
n = 0
seal_cx, seal_cy, seal_r = W*0.66, mT + rows*cell_h*0.52, 300

for r in range(rows):
    for c in range(cols):
        cx = mL + c*cell_w + cell_w/2
        cy = mT + r*cell_h + cell_h/2
        d = math.hypot(cx-seal_cx, cy-seal_cy)
        # thin the field near the seal so it reads as a break in the grid, not overlap
        if d < seal_r*1.08:
            continue
        n += 1
        rot = random.uniform(-7, 7)
        # tally mark: a short case-file glyph — a small numbered rect tick, alternating weight
        heavy = (r*cols+c) % 7 == 0
        col = INK if not heavy else TOMATO
        op = 0.9 if heavy else random.uniform(0.22, 0.42)
        num = f"{n:03d}"
        tallies.append(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f})" opacity="{op:.2f}">'
                        f'<rect x="-13" y="-17" width="26" height="34" rx="3" fill="none" stroke="{col}" stroke-width="{2.4 if heavy else 1.4}"/>'
                        f'<line x1="-8" y1="-4" x2="8" y2="-4" stroke="{col}" stroke-width="1.1"/>'
                        f'<text x="0" y="12" font-family="IBMPlexMono" font-size="7.5" fill="{col}" text-anchor="middle" letter-spacing="0.5">{num}</text>'
                        f'</g>')

tally_svg = "".join(tallies)

# ---- the seal: oversized stamp breaking the grid, off-center, single hot accent ----
seal_rot = -9
teeth = 14
pts = []
for i in range(teeth*2):
    ang = i * math.pi / teeth
    rad = seal_r if i % 2 == 0 else seal_r*0.84
    pts.append(f"{seal_r+rad*math.cos(ang):.1f},{seal_r+rad*math.sin(ang):.1f}")
star_pts = " ".join(pts)

seal_svg = f'''
<g transform="translate({seal_cx-seal_r:.1f},{seal_cy-seal_r:.1f}) rotate({seal_rot} {seal_r} {seal_r})">
  <polygon points="{star_pts}" fill="{TOMATO}" stroke="{INK}" stroke-width="10"/>
  <circle cx="{seal_r}" cy="{seal_r}" r="{seal_r*0.62:.1f}" fill="none" stroke="{CREAM}" stroke-width="3" stroke-dasharray="4 7"/>
  <text x="{seal_r}" y="{seal_r-56}" font-family="IBMPlexMono" font-weight="700" font-size="28" fill="{CREAM}" text-anchor="middle" letter-spacing="4">VERDICT</text>
  <text x="{seal_r}" y="{seal_r+34}" font-family="IBMPlexMono" font-weight="700" font-size="82" fill="{CREAM}" text-anchor="middle">7/10</text>
  <text x="{seal_r}" y="{seal_r+80}" font-family="IBMPlexMono" font-size="15" fill="{CREAM}" text-anchor="middle" letter-spacing="3" opacity="0.85">CASE CLOSED</text>
</g>
'''

# ---- registration marks + case-file header (administrative typography) ----
header = f'''
<text x="{mL}" y="86" font-family="IBMPlexMono" font-weight="700" font-size="15" fill="{INK}" letter-spacing="6">DOCKET NO. 0001 — LATENT JUDGES</text>
<text x="{W-mR}" y="86" font-family="IBMPlexMono" font-size="15" fill="{INK}" text-anchor="end" letter-spacing="3" opacity="0.7">EXHIBIT A / STUDY LOG, UNVERIFIED</text>
<line x1="{mL}" y1="104" x2="{W-mR}" y2="104" stroke="{INK}" stroke-width="2"/>
'''

crossmarks = ""
for (x,y) in [(50,50),(W-50,50),(50,H-50),(W-50,50-0),(50,H-50),(W-50,H-50)]:
    pass
for (x,y) in [(46,46),(W-46,46),(46,H-46),(W-46,H-46)]:
    crossmarks += (f'<line x1="{x-14}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{INK}" stroke-width="1.4"/>'
                   f'<line x1="{x}" y1="{y-14}" x2="{x}" y2="{y+14}" stroke="{INK}" stroke-width="1.4"/>')

# ---- footer: the one human signature-like flourish, italic, used exactly once ----
footer = f'''
<line x1="{mL}" y1="{H-140}" x2="{W-mR}" y2="{H-140}" stroke="{INK}" stroke-width="1.4" opacity="0.5"/>
<text x="{mL}" y="{H-96}" font-family="CrimsonPro" font-style="italic" font-size="30" fill="{INK}">ruled, without appeal.</text>
<text x="{W-mR}" y="{H-96}" font-family="IBMPlexMono" font-size="13" fill="{INK}" text-anchor="end" letter-spacing="2" opacity="0.6">FILED — AQUATERRA REGISTRAR</text>
'''

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'IBMPlexMono';src:url('{MONO_R}') format('truetype');font-weight:400}}
@font-face{{font-family:'IBMPlexMono';src:url('{MONO_B}') format('truetype');font-weight:700}}
@font-face{{font-family:'CrimsonPro';src:url('{SER_I}') format('truetype');font-style:italic}}
@font-face{{font-family:'CrimsonPro';src:url('{SER_R}') format('truetype')}}
*{{margin:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};position:relative;overflow:hidden}}
</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{CREAM}"/>
  <rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{INK}" stroke-width="2.5"/>
  {header}
  {tally_svg}
  {seal_svg}
  {crossmarks}
  {footer}
</svg>
</body></html>'''

OUT_DIR = "/home/user/aqdesignengine/out/final/latent_judges_exam_prep/companion"
os.makedirs(OUT_DIR, exist_ok=True)
with open(f"{OUT_DIR}/docket_art_source.html", "w") as f:
    f.write(html)

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html, wait_until="load")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f"{OUT_DIR}/docket_aesthetic.png")
        await b.close()

asyncio.run(main())
print("done")
