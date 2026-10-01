"""TERRATHON BY AQUATERRA, the festival's main signage, single page A4 LANDSCAPE (297x210mm), TerraThon branding. PDF + 300dpi PNG.
Elements: giant TERRATHON (StretchPro; the doubled R is GUARDED with a zero-width non-joiner so it reads TERRATHON (unguarded, the RR ligature becomes one stretched R and the word reads TEFATHON from across a room)), "BY" in Sigmar One + the real AQ logo (core.LOGO), a row of the
kit's REAL stickers (pickleball set, cricket set, AQ LIVE, controller, carnival) and the blue shuriken furniture, black ground with flecks.
Facts: only the name and the "by AquaTerra" line. NO dates, venue, prizes or sports names are printed (not asked for; the sticker row hints at the three sports + the
Mini-Fete without naming them). PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; ask the printer for a bleed proof.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_fest_sign.py   ->  out/collaterals/terrathon_by_aquaterra_sign_A4_landscape.pdf + .png
"""
import asyncio, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, CREAM_HALO, WHITE = "#000000", "#DE68F0", "#F3ECDE", "#F5F5F5"
W, H = 1123, 794
_im, STAR = tt.crop_to_alpha("shuriken.png")
ST = {n: tt.crop_to_alpha(n)[1] for n in ("pickleball_set.png", "cricket_set.png", "aq_live.png", "controller.png", "carnival.png")}
rnd = random.Random(23)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(430))
# (sticker, height px, rotation deg)
ROW = [("pickleball_set.png", 158, -6), ("cricket_set.png", 186, 5), ("aq_live.png", 232, -4), ("controller.png", 158, 6), ("carnival.png", 186, -5)]
row_html = "".join(f'<img class="stk" src="{ST[n]}" style="height:{h}px;transform:rotate({r}deg)">' for n, h, r in ROW)

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:297mm 210mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:297mm;height:210mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE};text-align:center}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:74px;z-index:1}}
.title{{position:absolute;left:0;right:0;top:120px;font-family:'StretchPro';color:{WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;line-height:1;white-space:nowrap;z-index:2}}
.by{{position:absolute;left:0;right:0;top:310px;display:flex;align-items:center;justify-content:center;gap:34px;z-index:2}}
.by .b{{font-family:'SigmarOne';color:{ORCHID};-webkit-text-stroke:1.4px {ORCHID};letter-spacing:-.01em;font-size:84px;line-height:1}}
.by img{{height:122px;display:block}}
.row{{position:absolute;left:52px;right:52px;bottom:60px;display:flex;align-items:flex-end;justify-content:space-between;z-index:2}}
.stk{{display:block;width:auto}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:30px;top:22px"><img class="star" src="{STAR}" style="right:34px;top:30px">
<div class="title" id="title">TER&zwnj;RATHON</div>
<div class="by"><div class="b">BY</div><img src="{core.LOGO}"></div>
<div class="row" id="row">{row_html}</div>
</div></body></html>"""

FIT = """() => { const e = document.getElementById('title'); const tw = () => { const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().width; };
  e.style.fontSize = '100px'; e.style.webkitTextStroke = '4px currentColor'; const px = 100 * 1020 / tw();
  e.style.fontSize = px + 'px'; e.style.webkitTextStroke = (0.04 * px) + 'px currentColor'; const px2 = px * 1020 / tw();
  e.style.fontSize = px2 + 'px'; e.style.webkitTextStroke = (0.04 * px2) + 'px currentColor'; return [px, px2, tw()]; }"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), q = (s) => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
  const title = q('#title')[0], by = q('.by')[0], stk = q('.stk'), stars = q('.star');
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]); const issues = [];
  stk.forEach((s, i) => { if (hit(s, by)) issues.push(['stk-by', i]); if (hit(s, title)) issues.push(['stk-title', i]); if (s[0] < 20 || s[2] > pr.right - 20 || s[3] > pr.bottom - 20) issues.push(['stk-edge', i, s]);
    stk.forEach((t, j) => { if (j > i && hit(s, t)) issues.push(['stk-stk', i, j]); }); });
  stars.forEach((s, i) => { if (hit(s, title)) issues.push(['star-title', i, s, title]); if (hit(s, by)) issues.push(['star-by', i]); stk.forEach((t, j) => { if (hit(s, t)) issues.push(['star-stk', i, j]); }); });
  if (hit(title, by)) issues.push(['title-by']);
  return {issues, title, by, stk, stars};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    out = "out/collaterals/terrathon_by_aquaterra_sign_A4_landscape"
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        r = await pg.evaluate(CHECK); print("issues", r["issues"]); print("title", r["title"], "by", r["by"]); print("stk", r["stk"])
        await pg.locator("#page").screenshot(path=out + ".png")
        await pg.pdf(path=out + ".pdf", width="297mm", height="210mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    d = open(out + ".pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
