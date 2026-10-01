"""PHOTOBOOTH stall signage for the TerraThon Mini-Fete, single page A4 LANDSCAPE (297x210mm), TerraThon branding. PDF + 300dpi PNG.
Photo: the user's picture of three printed AQUATERRA photo strips held in a hand (engine/assets/terrathon/photobooth.jpg), cropped to the strips in a tall tilted
orchid frame. It shows real people (school-age, faces visible): flagged to the user. Copy: TERRATHON / PHOTO BOOTH / STRIKE A POSE (my line; the copy pack says
"a photobooth for the evidence"). NOT supplied, so NOT printed: price, hours, prints-per-person, date, venue. No "Mini-Fete" wording. AQ logo bottom-right.
PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; ask the printer for a bleed proof.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_photobooth_sign.py   ->  out/collaterals/photobooth_sign_A4_landscape.pdf + .png
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, CREAM_HALO, WHITE, CARD, INK = "#000000", "#DE68F0", "#F3ECDE", "#F5F5F5", "#F5EEE1", "#0A0A0A"
LOT = "data:image/jpeg;base64," + base64.b64encode(open("engine/assets/terrathon/photobooth.jpg", "rb").read()).decode()
_im, STAR = tt.crop_to_alpha("shuriken.png")
W, H = 1123, 794
rnd = random.Random(13)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(420))


def frame(cls, src, x, y, w, h, deg, pos="50% 50%", z=2):
    return (f'<div class="frame {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({deg}deg);z-index:{z}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>')


HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:297mm 210mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:297mm;height:210mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE}}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:88px}}
.frame{{position:absolute;border:10px solid {ORCHID};border-radius:34px;overflow:hidden;background:#111}}
.col{{position:absolute;left:630px;width:450px;top:0;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:4}}
.t1{{font-weight:400;font-size:34px;letter-spacing:.2em;color:{CREAM_HALO};white-space:nowrap}}
.name{{font-family:'StretchPro';color:{WHITE};letter-spacing:.01em;font-feature-settings:'liga' 1,'dlig' 1;line-height:.98;white-space:nowrap}}
.sub{{font-family:'SigmarOne';color:{ORCHID};letter-spacing:-.01em;line-height:1;white-space:nowrap;margin-top:22px}}
.pill{{margin-top:26px;background:{CARD};color:{INK};border:7px solid {ORCHID};border-radius:999px;font-weight:900;font-size:25px;letter-spacing:.04em;padding:12px 24px 10px;white-space:nowrap}}
.aq{{position:absolute;right:56px;bottom:50px;height:50px;display:block;z-index:4}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
{frame("fa", LOT, 96, 92, 410, 610, -3, "50% 100%", 3)}
<img class="star" src="{STAR}" style="left:34px;top:46px;z-index:5"><img class="star" src="{STAR}" style="right:46px;top:44px;z-index:5"><img class="star" src="{STAR}" style="left:420px;top:640px;z-index:5">
<div class="col"><div class="t1">TERRATHON</div>
<div class="name" id="n1" style="margin-top:20px">PHOTO</div><div class="name" id="n2">B&zwnj;O&zwnj;OTH</div>
<div class="sub" id="sub">STRIKE A POSE</div></div>
<img class="aq" src="{core.LOGO}">
</div></body></html>"""

FIT = """() => {
  const fit = (ids, target, strokeEm) => { ids.forEach(id => { const e = document.getElementById(id); e.style.fontSize = '100px'; });
    const w = Math.max(...ids.map(id => document.getElementById(id).getBoundingClientRect().width)); const px = 100 * target / w;
    ids.forEach(id => { const e = document.getElementById(id); e.style.fontSize = px + 'px'; e.style.webkitTextStroke = (strokeEm * px) + 'px currentColor'; }); return px; };
  return [fit(['n1', 'n2'], 400, 0.04), fit(['sub'], 400, 0.03)];
}"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), out = {}, bad = [];
  const q = s => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
  const frames = q('.frame'), text = q('.col > *'), stars = q('.star'), aq = q('.aq')[0];
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]);
  const issues = [];
  frames.forEach((f, i) => { text.forEach((t, j) => { if (hit(f, t)) issues.push(['frame-text', i, j]); }); if (hit(f, aq)) issues.push(['frame-aq', i]);
    if (f[0] < 20 || f[1] < 20 || f[2] > pr.right - 20 || f[3] > pr.bottom - 20) issues.push(['frame-near-edge', i, f]); });
  stars.forEach((s, i) => { text.forEach((t, j) => { if (hit(s, t)) issues.push(['star-text', i, j]); }); frames.forEach((f, j) => { if (hit(s, f)) issues.push(['star-frame', i, j]); }); });
  text.forEach((t, j) => { if (hit(t, aq)) issues.push(['text-aq', j]); });
  return {issues, frames, text, aq};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        res = await pg.evaluate(CHECK); print("issues", res["issues"]); print("frames", res["frames"]); print("text", res["text"])
        await pg.locator("#page").screenshot(path="out/collaterals/photobooth_sign_A4_landscape.png")
        await pg.pdf(path="out/collaterals/photobooth_sign_A4_landscape.pdf", width="297mm", height="210mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    d = open("out/collaterals/photobooth_sign_A4_landscape.pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
