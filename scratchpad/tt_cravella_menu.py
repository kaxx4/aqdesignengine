"""CRAVE'LLA menu card for the TerraThon Mini-Fete stall, single page A4 portrait (210x297mm), in TERRATHON branding (user, 2026-10-01: "use the terrathon
branding"; replaces the first plum-and-cream version, which is in git history). Outputs a vector PDF (print) and a 300dpi PNG (2480x3508).
Look: black ground + white flecks, blue shuriken, StretchPro title with ligature guard, Sigmar One sub (sparingly), NeutralFace caps, cream cards with GREEN
borders and ORCHID chips, green price pills (the series' rules-post language). Crave'lla's real logo is the partner badge (circle, orchid ring); AQ logo in the footer.
Menu and prices verbatim from the user's list; a group whose items share a price shows it ONCE ("ALL RS. 299"). "Asscai Bowl" printed as ACAI (flagged).
Not claimed: ingredients, allergens, sizes, ordering. PRINT CAVEAT: a full-bleed black A4 uses a lot of ink and shows paper-edge slips; the artwork keeps a ~12mm
safe margin and has no bleed or crop marks. Ask the printer for a bleed proof (or say so and a white-ground variant can be made).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_cravella_menu.py   ->  out/collaterals/cravella_menu_A4.pdf + .png
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, GREEN, CREAM_HALO, CARD, INK, WHITE = "#000000", "#DE68F0", "#2FD284", "#F3ECDE", "#F5EEE1", "#0A0A0A", "#F5F5F5"
LOGO = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/partners/cravella/logo_circle.png", "rb").read()).decode()
_im, STAR = tt.crop_to_alpha("shuriken.png")

SECTIONS = [   # FINAL menu (user, 2026-10-01), items and prices verbatim; a group's shared price is printed once
    dict(title="ACAI BOWL", price="RS. 299", cols=1, items=["Granola Greek Yoghurt Bowl"]),
    dict(title="TIRAMISU", price="RS. 299", cols=1, items=["Classic Tiramisu"]),
    dict(title="BROWNIES + CHEESECAKES", price="ALL RS. 150", cols=2, rows=3, items=["Belgian Chocolate Chunk", "Cookie Dough", "Biscoff", "Blueberry Cheesecake", "Nutella Cheesecake", "Biscoff Cheesecake"]),
    dict(title="COOKIE TIN", price=None, cols=1, items=[("Midnight Cookie Tin", "RS. 500"), ("Triple Chocolate Cookie Tin", "RS. 700")]),
]


def section_html(sec):
    pill = f'<div class="pill">{sec["price"]}</div>' if sec["price"] else ""
    cells = ""
    for it in sec["items"]:
        if isinstance(it, tuple):
            cells += f'<div class="cell priced"><span class="nm">{it[0]}</span><span class="dots"></span><span class="pr">{it[1]}</span></div>'
        else:
            cells += f'<div class="cell"><span class="bul"></span><span class="nm">{it}</span></div>'
    flow = f' style="grid-template-rows:repeat({sec["rows"]},auto);grid-auto-flow:column"' if sec.get("rows") else ""
    return f'<section class="card"><div class="shead"><div class="chip">{sec["title"]}</div>{pill}</div><div class="grid c{sec["cols"]}"{flow}>{cells}</div></section>'


rnd = random.Random(7)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, 794):.0f}" cy="{rnd.uniform(0, 1123):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(330))

# measured in the browser: StretchPro title with the doubled-letter ligature guard (no doubled letters in THE MENU, so the guard is a no-op here)
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:210mm 297mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;background:{GROUND};color:{INK};font-family:'NeutralFace',sans-serif;display:flex;flex-direction:column}}
.specks{{position:absolute;inset:0;z-index:0}}
.head{{position:relative;z-index:2;text-align:center;padding:26px 0 0}}
.kick{{font-weight:400;font-size:19px;letter-spacing:.16em;color:{CREAM_HALO}}}
.logo{{width:136px;height:136px;border-radius:50%;border:6px solid {ORCHID};display:block;margin:12px auto 0;position:relative;z-index:3}}
.title{{font-family:'StretchPro';font-size:72px;line-height:1;color:{WHITE};-webkit-text-stroke:2.8px {WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;margin-top:10px;white-space:nowrap}}
.sub{{font-family:'SigmarOne';font-size:23px;color:{ORCHID};-webkit-text-stroke:.7px {ORCHID};letter-spacing:-.01em;margin-top:6px;white-space:nowrap}}
.info{{font-weight:900;font-size:15px;letter-spacing:.1em;color:{WHITE};margin-top:9px}}
.star{{position:absolute;z-index:1;width:78px}}
.body{{position:relative;z-index:2;flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-between;padding:22px 44px 12px}}
.duo{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}}
.duo .chip{{font-size:20px;padding:8px 14px 7px}} .duo .pill{{font-size:21px;padding:8px 14px 7px}} .duo .cell{{font-size:19px}} .duo .shead{{gap:8px}}
.c2 .cell{{font-size:19px;letter-spacing:0}}
.duo .card{{display:flex;flex-direction:column}}
.card{{background:{CARD};border:5px solid {GREEN};border-radius:26px;padding:18px 24px 18px}}
.shead{{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:12px}}
.chip{{background:{ORCHID};color:{INK};font-weight:900;font-size:24px;line-height:1;letter-spacing:.04em;padding:9px 20px 8px;border-radius:999px;white-space:nowrap}}
.pill{{background:{GREEN};color:{INK};font-weight:900;font-size:26px;line-height:1;letter-spacing:.04em;padding:9px 20px 8px;border-radius:999px;white-space:nowrap}}
.grid{{display:grid;gap:14px 24px}} .c1{{grid-template-columns:1fr}} .c2{{grid-template-columns:1fr 1fr}}
.cell{{display:flex;align-items:center;gap:10px;font-weight:400;font-size:21px;line-height:1.18;letter-spacing:.02em;text-transform:uppercase;color:{INK}}}
.bul{{flex:none;width:8px;height:8px;border-radius:50%;background:{ORCHID}}}
.priced .nm{{flex:none}} .dots{{flex:1 1 0;border-bottom:2px dotted rgba(10,10,10,.35);transform:translateY(4px);min-width:10px}}
.pr{{font-weight:900;font-size:25px;letter-spacing:.04em;white-space:nowrap}}
.foot{{position:relative;z-index:2;flex:none;display:flex;align-items:center;justify-content:space-between;margin:0 44px;padding:14px 0 46px;border-top:3px solid {ORCHID}}}
.foot img{{height:34px;display:block}}
.hd{{font-weight:900;font-size:17px;letter-spacing:.12em;color:{WHITE}}}
.note{{font-weight:400;font-size:14px;letter-spacing:.1em;color:{WHITE}}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 794 1123" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:40px;top:50px"><img class="star" src="{STAR}" style="right:40px;top:76px">
<div class="head"><div class="kick">TERRATHON MINI-FETE</div><img class="logo" src="{LOGO}"><div class="title">THE MENU</div>
<div class="sub">CRAVE&rsquo;LLA, OUR DESSERT PARTNER</div><div class="info">3RD + 4TH OCTOBER 2026  |  TURF XL, NEW ALIPORE</div></div>
<div class="body"><div class="duo">{section_html(SECTIONS[0])}{section_html(SECTIONS[1])}</div>{section_html(SECTIONS[2])}{section_html(SECTIONS[3])}</div>
<div class="foot"><img src="{core.LOGO}"><div class="hd">@CRAVELLA_KOLKATA</div><div class="note">ALL PRICES IN RS.</div></div>
</div></body></html>"""

CHECK = """() => {
  const pg = document.getElementById('page'), pr = pg.getBoundingClientRect(), bad = [];
  document.querySelectorAll('.page *').forEach(e => {
    const r = e.getBoundingClientRect(); if (!r.width || !r.height || e.closest('svg.specks')) return;
    if (r.right > pr.right + 0.5 || r.left < pr.left - 0.5 || r.bottom > pr.bottom + 0.5) bad.push(['off-page', String(e.className || e.tagName), Math.round(r.right), Math.round(r.bottom)]);
  });
  const body = document.querySelector('.body'), foot = document.querySelector('.foot'), cards = [...document.querySelectorAll('.card')];
  const gaps = cards.slice(1).map((c, i) => Math.round(c.getBoundingClientRect().top - cards[i].getBoundingClientRect().bottom));
  const head = document.querySelector('.head').getBoundingClientRect();
  return {bad, headBottom: Math.round(head.bottom), cardGaps: gaps, firstCardTop: Math.round(cards[0].getBoundingClientRect().top),
          lastCardBottom: Math.round(cards[cards.length-1].getBoundingClientRect().bottom), footTop: Math.round(foot.getBoundingClientRect().top), pageH: Math.round(pr.height),
          cellWrap: [...document.querySelectorAll('.cell .nm')].filter(n => n.getBoundingClientRect().height > 30).map(n => n.textContent),
          titleW: Math.round(document.querySelector('.title').getBoundingClientRect().width)};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print("CHECK", await pg.evaluate(CHECK))
        await pg.locator("#page").screenshot(path="out/collaterals/cravella_menu_A4.png")
        await pg.pdf(path="out/collaterals/cravella_menu_A4.pdf", width="210mm", height="297mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    from PIL import Image
    print("png", Image.open("out/collaterals/cravella_menu_A4.png").size)
    d = open("out/collaterals/cravella_menu_A4.pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
