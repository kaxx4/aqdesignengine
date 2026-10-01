"""CRAVE'LLA menu card for the TerraThon Mini-Fete stall, single page A4 portrait (210x297mm). Outputs a vector PDF (print) and a 300dpi PNG (2480x3508).
Palette is Crave'lla's own (sampled from their logo: plum #5F2036, cream, gold tin accent for rules only, never text) on warm paper, never white (AQ rule).
Type: NeutralFace caps for section heads and prices, Eina for item names (AQ body face). Logo = the user's real file (circle). AQ logo in the footer.
Menu and prices verbatim from the user's list (2026-10-01); a group whose items share a price shows it ONCE on the header ("ALL RS. 299").
"Asscai Bowl" is printed as Acai (flagged to the user). Not claimed: ingredients, allergens, sizes, ordering. Prices are in rupees.
Print caveat: sRGB, no bleed or crop marks; the artwork keeps a 12mm safe margin, but ask the printer for a borderless/bleed proof before a run.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_cravella_menu.py   ->  out/collaterals/cravella_menu_A4.pdf + .png
"""
import asyncio, base64, importlib.util, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

PLUM, PLUM_DK, CREAM, PAPER, GOLD, INK = "#5F2036", "#3F0C19", "#FAE0BE", "#F9EEDC", "#C9A24B", "#2A1218"
LOGO = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/partners/cravella/logo_circle.png", "rb").read()).decode()

SECTIONS = [
    dict(title="ACAI BOWL", price="RS. 299", cols=1, items=["Granola Greek Yoghurt"]),
    dict(title="TIRAMISU", price="ALL RS. 299", cols=2, rows=2, items=["Classic Tiramisu", "Brownie Tiramisu", "Mocha Leopard Tiramisu", "Tiramisu Tub"]),
    dict(title="BROWNIES + CHEESECAKES", price="ALL RS. 150", cols=2, rows=5, items=["Classic Chocolate Chunk", "Biscoff Crunch Brownie", "Cheesecake Brownie", "Cookie Dough Brownie", "Nutella Cheesecake",
                                                                            "Biscoff Cheesecake", "Blueberry Cheesecake", "Brownie Cheesecake", "Basque Cheesecake"]),
    dict(title="COOKIE TINS", price=None, cols=2, items=[("OG Cookie Tin", "RS. 500"), ("Biscoff Crunch Tin", "RS. 500"), ("Midnight Crunch Tin", "RS. 500"), ("Triple Chocolate Cookie Tin", "RS. 700")]),
]


def section_html(sec):
    pill = f'<div class="pill">{sec["price"]}</div>' if sec["price"] else ""
    cells = ""
    for it in sec["items"]:
        if isinstance(it, tuple):
            cells += f'<div class="cell priced"><span class="nm">{it[0]}</span><span class="dots"></span><span class="pr">{it[1]}</span></div>'
        else:
            cells += f'<div class="cell"><span class="bul"></span><span class="nm">{it}</span></div>'
    return (f'<section><div class="shead"><span class="rule"></span><h2>{sec["title"]}</h2><span class="rule"></span>{pill}</div>'
            f'<div class="grid c{sec["cols"]}"' + (f' style="grid-template-rows:repeat({sec["rows"]},auto);grid-auto-flow:column"' if sec.get("rows") else "") + f'>{cells}</div></section>')


def scallop(n=29, r=14):
    w = 210 * 96 / 25.4
    step = w / n
    cs = "".join(f'<circle cx="{step * (i + .5):.1f}" cy="0" r="{r}" fill="{PLUM}"/>' for i in range(n))
    return f'<svg class="scal" viewBox="0 0 {w:.1f} {r}" preserveAspectRatio="none" width="100%" height="{r}">{cs}</svg>'


HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
@page {{ size:210mm 297mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{PAPER}}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;background:{PAPER};color:{INK};font-family:'Eina01',sans-serif;display:flex;flex-direction:column}}
.head{{background:{PLUM};color:{CREAM};text-align:center;padding:30px 0 26px;position:relative}}
.logo{{width:176px;height:176px;border-radius:50%;border:5px solid {CREAM};display:block;margin:0 auto}}
.kick{{font-family:'NeutralFace';font-weight:900;font-size:16px;letter-spacing:.22em;margin-top:16px}}
.sub{{font-family:'NeutralFace';font-weight:400;font-size:14px;letter-spacing:.14em;margin-top:6px;opacity:.95}}
.scal{{display:block;margin-top:-1px}}
.body{{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-evenly;padding:6px 46px 4px}}
.shead{{display:flex;align-items:center;gap:14px;margin-bottom:12px}}
.rule{{flex:1 1 0;height:2px;background:{GOLD}}}
h2{{font-family:'NeutralFace';font-weight:900;font-size:25px;letter-spacing:.1em;color:{PLUM};white-space:nowrap}}
.pill{{font-family:'NeutralFace';font-weight:900;font-size:19px;letter-spacing:.06em;background:{PLUM};color:{CREAM};padding:6px 16px 5px;border-radius:999px;white-space:nowrap}}
.grid{{display:grid;gap:9px 28px}}
.c1{{grid-template-columns:1fr}} .c2{{grid-template-columns:1fr 1fr}} .c3{{grid-template-columns:1fr 1fr 1fr}}
.cell{{display:flex;align-items:center;gap:9px;font-size:17px;line-height:1.2;font-weight:600;color:{INK}}}
.bul{{flex:none;width:8px;height:8px;border-radius:50%;background:{PLUM}}}
.priced .nm{{flex:none}} .dots{{flex:1 1 0;border-bottom:2px dotted {GOLD};transform:translateY(5px);min-width:10px}}
.pr{{font-family:'NeutralFace';font-weight:900;font-size:18px;color:{PLUM};letter-spacing:.05em;white-space:nowrap}}
.foot{{flex:none;display:flex;align-items:center;justify-content:space-between;padding:12px 46px 46px;border-top:2px solid {GOLD};margin:0 46px;padding-left:0;padding-right:0}}
.foot img{{height:34px;display:block}}
.hd{{font-family:'NeutralFace';font-weight:900;font-size:16px;letter-spacing:.12em;color:{PLUM}}}
.note{{font-family:'NeutralFace';font-weight:400;font-size:13px;letter-spacing:.1em;color:{INK}}}
</style></head><body><div class="page" id="page">
<div class="head"><img class="logo" src="{LOGO}"><div class="kick">OUR DESSERT PARTNER AT TERRATHON</div><div class="sub">MINI-FETE  |  3RD + 4TH OCTOBER 2026  |  TURF XL, NEW ALIPORE</div></div>
{scallop()}
<div class="body">{"".join(section_html(s) for s in SECTIONS)}</div>
<div class="foot"><img src="{core.LOGO}"><div class="hd">@CRAVELLA_KOLKATA</div><div class="note">ALL PRICES IN RS.</div></div>
</div></body></html>"""

CHECK = """() => {
  const pg = document.getElementById('page'), pr = pg.getBoundingClientRect(), bad = [];
  document.querySelectorAll('.page *').forEach(e => {
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
    if (r.right > pr.right + 0.5 || r.left < pr.left - 0.5 || r.bottom > pr.bottom + 0.5) bad.push(['off-page', e.className || e.tagName, Math.round(r.right), Math.round(r.bottom)]);
    if (e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible') bad.push(['clipped', e.className || e.tagName]);
  });
  const body = document.querySelector('.body'), foot = document.querySelector('.foot'), last = body.lastElementChild.getBoundingClientRect();
  return {bad, bodyBottom: Math.round(last.bottom), footTop: Math.round(foot.getBoundingClientRect().top), pageH: Math.round(pr.height),
          cellOverflow: [...document.querySelectorAll('.cell')].filter(c => c.scrollWidth > c.clientWidth + 1).map(c => c.textContent)};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        res = await pg.evaluate(CHECK); print("CHECK", res)
        await pg.locator("#page").screenshot(path="out/collaterals/cravella_menu_A4.png")
        await pg.pdf(path="out/collaterals/cravella_menu_A4.pdf", width="210mm", height="297mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    from PIL import Image
    print("png", Image.open("out/collaterals/cravella_menu_A4.png").size)

asyncio.run(main())
