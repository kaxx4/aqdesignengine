"""THE PATIENT SPINDLE — companion art piece.
A diagrammatic rotation study: concentric rings + radial spokes (a charkha's
geometry, abstracted into a specimen card), one thread breaking the perfect
repetition to trail off-grid and knot at its end. Clinical mono annotations at
the margins; the only two Gandhi Jayanti resonances left in — 108 (the mala
count) and the date reduced to two numbers — are never spelled out as words.
"""
import asyncio, base64, math, os, sys

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
def b64font(name):
    with open(os.path.join(FONT_DIR, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

MONO = b64font("IBMPlexMono-Regular.ttf")
MONO_B = b64font("IBMPlexMono-Bold.ttf")
SERIF_I = b64font("CrimsonPro-Italic.ttf")

W, H = 1500, 2000
CX, CY = 750, 970
R_OUT = 600
INK = "#1B1712"
CREAM = "#F1EAD9"
GREEN = "#2F6B4F"
TERRA = "#B65B3D"

def ring(r, w, op):
    return f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{INK}" stroke-width="{w}" opacity="{op}"/>'

def spokes():
    out = []
    n = 36
    for i in range(n):
        a = math.radians(i * 360 / n)
        x1, y1 = CX + 34 * math.sin(a), CY - 34 * math.cos(a)
        x2, y2 = CX + R_OUT * math.sin(a), CY - R_OUT * math.cos(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{INK}" stroke-width="1.1" opacity=".38"/>')
    # tick marks just outside the rim, one per spoke — the instrument-dial detail
    for i in range(n):
        a = math.radians(i * 360 / n)
        x1, y1 = CX + (R_OUT + 6) * math.sin(a), CY - (R_OUT + 6) * math.cos(a)
        x2, y2 = CX + (R_OUT + 20) * math.sin(a), CY - (R_OUT + 20) * math.cos(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{INK}" stroke-width="1.4" opacity=".55"/>')
    return "".join(out)

def escaping_thread():
    """The one gesture that breaks the grid: a spoke that keeps going past the rim,
    curves, and ends in a small knot — the human hand among the many even turns."""
    a = math.radians(35)
    hx, hy = CX + 34 * math.sin(a), CY - 34 * math.cos(a)
    rx, ry = CX + R_OUT * math.sin(a), CY - R_OUT * math.cos(a)
    kx, ky = CX + (R_OUT + 168) * math.sin(a + 0.34), CY - (R_OUT + 168) * math.cos(a + 0.34)
    path = (f'M{hx:.1f} {hy:.1f} L{rx:.1f} {ry:.1f} '
            f'Q{rx + (kx - rx) * 0.35:.1f} {ry + (ky - ry) * 0.15:.1f} {kx:.1f} {ky:.1f}')
    return (f'<path d="{path}" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="7.5" fill="{TERRA}"/>'
            f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="7.5" fill="none" stroke="{INK}" stroke-width="1.4"/>')

RINGS = [(R_OUT, 3.2, .82), (460, 1.1, .30), (300, 1.1, .30), (140, 1.1, .30)]

svg = "".join(ring(r, w, o) for r, w, o in RINGS)
svg += spokes()
svg += escaping_thread()
svg += f'<circle cx="{CX}" cy="{CY}" r="15" fill="{INK}"/>'
svg += f'<circle cx="{CX}" cy="{CY}" r="15" fill="none" stroke="{GREEN}" stroke-width="2"/>'

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'PMono';src:url(data:font/ttf;base64,{MONO}) format('truetype');font-weight:400}}
@font-face{{font-family:'PMono';src:url(data:font/ttf;base64,{MONO_B}) format('truetype');font-weight:700}}
@font-face{{font-family:'PSerif';src:url(data:font/ttf;base64,{SERIF_I}) format('truetype');font-style:italic}}
*{{margin:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:{CREAM};position:relative;overflow:hidden;
     font-family:'PMono',monospace}}
.grain{{position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:multiply;opacity:.05;
       background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
.lbl{{position:absolute;font-size:14px;letter-spacing:.16em;text-transform:uppercase;color:{INK};
     opacity:.72;line-height:1.7}}
.lbl b{{font-weight:700}}
.frame{{position:absolute;inset:56px;border:1px solid {INK};opacity:.28}}
.tick{{position:absolute;font-size:11px;letter-spacing:.1em;color:{INK};opacity:.5}}
</style></head><body>
<div class="frame"></div>
<div class="lbl" style="top:96px;left:96px;width:520px">STUDY&nbsp;NO.&nbsp;II<br><b>PATIENT&nbsp;ROTATION</b></div>
<div class="lbl" style="top:96px;right:96px;text-align:right;width:200px">02&nbsp;&middot;&nbsp;10</div>
<svg width="{W}" height="{H}" style="position:absolute;inset:0;z-index:2">{svg}</svg>
<div class="lbl" style="bottom:150px;left:96px;width:520px;opacity:.6;font-size:13px">
ONE&nbsp;CENTRE.&nbsp;EVERY&nbsp;TURN&nbsp;ACCOUNTED&nbsp;FOR.</div>
<div class="lbl" style="bottom:150px;right:96px;text-align:right;width:260px;opacity:.6;font-size:13px">
108&nbsp;TURNS&nbsp;RECORDED</div>
<div style="position:absolute;bottom:96px;left:0;width:{W}px;text-align:center;
     font-family:'PSerif',serif;font-style:italic;font-size:26px;color:{INK};opacity:.68;
     letter-spacing:.01em">spun, not spoken</div>
<div class="grain"></div>
</body></html>"""

async def main():
    from playwright.async_api import async_playwright
    out_html = "scratchpad/canvas_art.html"
    with open(out_html, "w") as f:
        f.write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.goto("file://" + os.path.abspath(out_html))
        await pg.wait_for_timeout(200)
        await pg.screenshot(path="scratchpad/patient_spindle.png")
        await b.close()
    print("done")

asyncio.run(main())
