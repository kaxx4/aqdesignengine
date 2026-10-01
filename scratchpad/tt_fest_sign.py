"""TERRATHON BY AQUATERRA, the festival's main signage, single page A4 LANDSCAPE (297x210mm), TerraThon branding. PDF + 300dpi PNG.
v2 (user, 2026-10-01): the WHOLE line "TERRATHON BY AQUATERRA" set in StretchPro, centred in the middle (two lines, each fitted to the same width: TERRATHON in white,
BY AQUATERRA in orchid); the real AQ LIVE logo (the aq_live kit sticker) top centre; the real AQ logo (core.LOGO) beside it, as a centred pair along the top; the user-supplied partner strip (Education/Hydration/Dessert/Jersey partners, transparent PNG, partners/partner_strip.png)
across the bottom; the other four kit stickers: pickleball + controller top corners, cricket + carnival at the bottom corners flanking the strip. Doubled letters (RR) are GUARDED with a zero-width non-joiner: unguarded, the StretchPro ligature fuses
them into one stretched glyph and the word reads wrong. No dates, venue or sports names printed.
PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; ask the printer for a bleed proof.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_fest_sign.py   ->  out/collaterals/terrathon_by_aquaterra_sign_A4_landscape.pdf + .png
"""
import asyncio, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, WHITE = "#000000", "#DE68F0", "#F5F5F5"
W, H = 1123, 794
ST = {n: tt.crop_to_alpha(n)[1] for n in ("pickleball_set.png", "cricket_set.png", "aq_live.png", "controller.png", "carnival.png")}
rnd = random.Random(23)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(430))
# corner stickers: (file, height px, rotation deg, css position)
import base64
STRIP = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/partners/partner_strip.png", "rb").read()).decode()   # user-supplied partner lockup (transparent)
CORNERS = [("pickleball_set.png", 170, -6, "left:46px;top:40px"), ("controller.png", 138, 6, "right:48px;top:52px"),
           ("cricket_set.png", 150, 5, "left:50px;top:588px"), ("carnival.png", 146, -5, "right:46px;top:590px")]
corner_html = "".join(f'<img class="stk" src="{ST[n]}" style="height:{h}px;transform:rotate({r}deg);{pos}">' for n, h, r, pos in CORNERS)

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:297mm 210mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:297mm;height:210mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE};text-align:center}}
.specks{{position:absolute;inset:0}}
.stk{{position:absolute;display:block;width:auto;z-index:2}}
.top{{position:absolute;left:0;right:0;top:34px;display:flex;align-items:center;justify-content:center;gap:30px;z-index:3}}
.live{{height:158px;display:block}}
.mid{{position:absolute;left:0;right:0;top:208px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;z-index:2}}
.ln{{font-family:'StretchPro';letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;line-height:1;white-space:nowrap;display:block}}
.strip{{position:absolute;left:50%;bottom:34px;width:780px;transform:translateX(-50%);display:block;z-index:3}}
.aq{{height:54px;display:block}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
{corner_html}
<div class="top"><img class="live" id="live" src="{ST['aq_live.png']}"><img class="aq" id="aq" src="{core.LOGO}"></div>
<div class="mid"><span class="ln" id="l1" style="color:{WHITE}">TER&zwnj;RATHON</span><span class="ln" id="l2" style="color:{ORCHID}">BY AQUATER&zwnj;RA</span></div>
<img class="strip" id="strip" src="{STRIP}">
</div></body></html>"""

FIT = """() => { const out = []; ['l1', 'l2'].forEach(id => { const e = document.getElementById(id);
  const tw = () => { const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().width; };
  e.style.fontSize = '100px'; e.style.webkitTextStroke = '4px currentColor'; let px = 100 * 880 / tw();
  e.style.fontSize = px + 'px'; e.style.webkitTextStroke = (0.04 * px) + 'px currentColor'; px = px * 880 / tw();
  e.style.fontSize = px + 'px'; e.style.webkitTextStroke = (0.04 * px) + 'px currentColor'; out.push([id, Math.round(px), Math.round(tw())]); }); return out; }"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), q = (s) => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
  const named = {live: q('#live')[0], aq: q('#aq')[0], strip: q('#strip')[0], l1: q('#l1')[0], l2: q('#l2')[0]}; q('.stk').forEach((b, i) => named['stk' + i] = b);
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]); const k = Object.keys(named), issues = [];
  k.forEach(n => { const b = named[n]; if (b[0] < 20 || b[1] < 20 || b[2] > pr.right - 20 || b[3] > pr.bottom - 20) issues.push(['near-edge', n, b]); });
  for (let i = 0; i < k.length; i++) for (let j = i + 1; j < k.length; j++) if (hit(named[k[i]], named[k[j]])) issues.push(['overlap', k[i], k[j]]);
  return {issues, named};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    out = "out/collaterals/terrathon_by_aquaterra_sign_A4_landscape"
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        r = await pg.evaluate(CHECK); print("issues", r["issues"]); print(r["named"])
        await pg.locator("#page").screenshot(path=out + ".png")
        await pg.pdf(path=out + ".pdf", width="297mm", height="210mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    d = open(out + ".pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
