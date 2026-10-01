"""CRAVE'LLA stall signage for the TerraThon Mini-Fete, single page A4 LANDSCAPE (297x210mm), TerraThon branding. Outputs a vector PDF and a 300dpi PNG.
Requested contents (user, 2026-10-01): Crave'lla logo and name, "dessert partner", the AQ LIVE logo (kit sticker engine/assets/terrathon/aq_live.png, used as-is),
and the AQ logo (core.LOGO, the real colored wordmark). Look: black ground + white flecks, blue shuriken, StretchPro name with the doubled-letter guard,
Sigmar One sub (sparingly), NeutralFace caps, orchid ring on the logo. No dates, venue or "Mini-Fete" on this version (user, 2026-10-01); only the name, the partner line and the logos.
PRINT CAVEAT: full-bleed black A4; ~12mm safe margin kept, no bleed or crop marks. Ask the printer for a bleed proof or a white-ground variant.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_cravella_sign.py   ->  out/collaterals/cravella_sign_A4_landscape.pdf + .png
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, CREAM_HALO, WHITE = "#000000", "#DE68F0", "#F3ECDE", "#F5F5F5"
LOGO = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/partners/cravella/logo_circle.png", "rb").read()).decode()
_im, STAR = tt.crop_to_alpha("shuriken.png")
_im, AQLIVE = tt.crop_to_alpha("aq_live.png")
W, H = 1123, 794
rnd = random.Random(11)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(420))

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:297mm 210mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:297mm;height:210mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE}}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:92px}}
.logo{{position:absolute;left:62px;top:{(H - 470) / 2}px;width:470px;height:470px;border-radius:50%;border:12px solid {ORCHID};display:block}}
.col{{position:absolute;left:560px;width:520px;top:0;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.t1{{font-weight:400;font-size:46px;letter-spacing:.2em;color:{CREAM_HALO};white-space:nowrap}}
.name{{font-family:'StretchPro';color:{WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;line-height:1;white-space:nowrap;margin-top:22px}}
.sub{{font-family:'SigmarOne';color:{ORCHID};letter-spacing:-.01em;line-height:1;white-space:nowrap;margin-top:26px}}
.info{{font-weight:900;font-size:24px;letter-spacing:.1em;color:{WHITE};margin-top:26px;white-space:nowrap}}
.aq{{position:absolute;left:66px;bottom:58px;height:54px;display:block}}
.live{{position:absolute;right:56px;bottom:50px;width:250px;display:block;transform:rotate(-6deg)}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:40px;top:38px"><img class="star" src="{STAR}" style="right:46px;top:44px">
<img class="logo" src="{LOGO}">
<div class="col"><div class="t1">TERRATHON</div>
<div class="name" id="name">CRAVE&rsquo;L&zwnj;LA</div><div class="sub" id="sub">OUR DESSERT PARTNER</div>
</div>
<img class="aq" src="{core.LOGO}"><img class="live" src="{AQLIVE}" style="right:44px">
</div></body></html>"""

FIT = """() => {
  const fit = (id, target, strokeEm) => { const e = document.getElementById(id); e.style.fontSize = '100px'; const w = e.getBoundingClientRect().width;
    const px = 100 * target / w; e.style.fontSize = px + 'px'; if (strokeEm) e.style.webkitTextStroke = (strokeEm * px) + 'px currentColor'; return px; };
  return [fit('name', 505, 0.04), fit('sub', 505, 0.03)];
}"""

CHECK = """() => {
  const pg = document.getElementById('page'), pr = pg.getBoundingClientRect(), bad = [];
  const boxes = {};
  document.querySelectorAll('.page > *:not(svg), .col > *').forEach(e => {
    const r = e.getBoundingClientRect(); if (!r.width) return;
    boxes[String(e.className || e.id)] = [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
    if (r.right > pr.right - 20 || r.left < 20 || r.bottom > pr.bottom - 20 || r.top < 0) bad.push(['near-edge', String(e.className), Math.round(r.right), Math.round(r.bottom)]);
  });
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]);
  const keys = Object.keys(boxes).filter(k => k !== 'col'), overlaps = [];
  for (let i = 0; i < keys.length; i++) for (let j = i + 1; j < keys.length; j++) if (hit(boxes[keys[i]], boxes[keys[j]])) overlaps.push([keys[i], keys[j]]);
  return {bad, overlaps, boxes};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        res = await pg.evaluate(CHECK); print("bad", res["bad"]); print("overlaps", res["overlaps"]); print(res["boxes"])
        await pg.locator("#page").screenshot(path="out/collaterals/cravella_sign_A4_landscape.png")
        await pg.pdf(path="out/collaterals/cravella_sign_A4_landscape.pdf", width="297mm", height="210mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    from PIL import Image
    print("png", Image.open("out/collaterals/cravella_sign_A4_landscape.png").size)
    d = open("out/collaterals/cravella_sign_A4_landscape.pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
