"""ARTILY menu card for the TerraThon Mini-Fete stall, single page A4 portrait (210x297mm), TerraThon branding (the same look as the Crave'lla menu card, scratchpad/tt_cravella_menu.py).
Outputs a vector PDF (print) and a 300dpi PNG (2480x3508). Menu and prices verbatim from the user's FINAL list (2026-10-01): Classic Cold Coffee, Strawberry Matcha, Lime Bomb, Pink Panther
all Rs. 250 (printed once, "ALL RS. 250"), Gondhoraj Mojito Rs. 200. The user's three photos (engine/assets/terrathon/partners/artily/) sit in tilted orchid frames because five items are
too few to fill an A4 on their own; the logo is the partner badge (circle, orchid ring). Handle @artilyindia is the one on the QR poster (not independently verified). Not claimed:
ingredients, sizes, allergens, ordering. The photos are not captioned (the user did not say which drink each shows).
PRINT CAVEAT: a full-bleed black A4 uses a lot of ink and shows paper-edge slips; the artwork keeps a ~12mm safe margin and has no bleed or crop marks. Ask the printer for a bleed proof.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_artily_menu.py   ->  out/collaterals/artily_menu_A4.pdf + .png
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, GREEN, CREAM_HALO, CARD, INK, WHITE = "#000000", "#DE68F0", "#2FD284", "#F3ECDE", "#F5EEE1", "#0A0A0A", "#F5F5F5"
A = "engine/assets/terrathon/partners/artily"
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(p, "rb").read()).decode()
LOGO = b64(f"{A}/logo_circle.png", "image/png")
PHOTOS = [(b64(f"{A}/drink_blue.jpg", "image/jpeg"), "50% 55%", -3), (b64(f"{A}/drink_popsicle.jpg", "image/jpeg"), "70% 45%", 2), (b64(f"{A}/matcha.jpg", "image/jpeg"), "50% 50%", -2)]
_im, STAR = tt.crop_to_alpha("shuriken.png")

FOUR = ["CLASSIC COLD COFFEE", "STRAWBERRY MATCHA", "LIME BOMB", "PINK PANTHER"]
rows = "".join(f'<div class="row"><span class="bul"></span><span class="nm">{n}</span></div>' for n in FOUR)
cardA = f'<section class="card"><div class="shead"><div class="chip">FOUR DRINKS</div><div class="pill">ALL RS. 250</div></div><div class="rows">{rows}</div></section>'
cardB = f'<section class="card"><div class="shead"><div class="chip">THE MOJITO</div><div class="pill">RS. 200</div></div><div class="rows"><div class="row"><span class="bul"></span><span class="nm">GONDHORAJ MOJITO</span></div></div></section>'
photos = "".join(f'<div class="ph" style="transform:rotate({d}deg)"><img src="{src}" style="object-position:{pos}"></div>' for src, pos, d in PHOTOS)

rnd = random.Random(9)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, 794):.0f}" cy="{rnd.uniform(0, 1123):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(330))

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
.logo{{width:118px;height:118px;border-radius:50%;border:6px solid {ORCHID};display:block;margin:12px auto 0;position:relative;z-index:3}}
.title{{font-family:'StretchPro';font-size:68px;line-height:1;color:{WHITE};-webkit-text-stroke:2.8px {WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;margin-top:10px;white-space:nowrap}}
.sub{{font-family:'SigmarOne';font-size:23px;color:{ORCHID};-webkit-text-stroke:.7px {ORCHID};letter-spacing:-.01em;margin-top:6px;white-space:nowrap}}
.info{{font-weight:900;font-size:15px;letter-spacing:.1em;color:{WHITE};margin-top:9px}}
.star{{position:absolute;z-index:1;width:78px}}
.body{{position:relative;z-index:2;flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-between;padding:20px 44px 10px}}
.card{{background:{CARD};border:5px solid {GREEN};border-radius:26px;padding:18px 26px 12px}}
.shead{{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:6px}}
.chip{{background:{ORCHID};color:{INK};font-weight:900;font-size:26px;line-height:1;letter-spacing:.04em;padding:9px 20px 8px;border-radius:999px;white-space:nowrap}}
.pill{{background:{GREEN};color:{INK};font-weight:900;font-size:30px;line-height:1;letter-spacing:.04em;padding:9px 20px 8px;border-radius:999px;white-space:nowrap}}
.row{{display:flex;align-items:center;gap:14px;height:50px;font-weight:400;font-size:29px;letter-spacing:.03em;text-transform:uppercase;color:{INK}}}
.row + .row{{border-top:3px solid rgba(10,10,10,.2)}}
.bul{{flex:none;width:11px;height:11px;border-radius:50%;background:{ORCHID}}}
.photos{{display:flex;justify-content:space-between;align-items:center;padding:8px 6px 0}}
.ph{{width:222px;height:146px;border:8px solid {ORCHID};border-radius:30px;overflow:hidden;background:#111;flex:none}}
.ph img{{width:100%;height:100%;object-fit:cover;display:block}}
.foot{{position:relative;z-index:2;flex:none;display:flex;align-items:center;justify-content:space-between;margin:0 44px;padding:12px 0 38px;border-top:3px solid {ORCHID}}}
.foot img{{height:34px;display:block}}
.hd{{font-weight:900;font-size:17px;letter-spacing:.12em;color:{WHITE}}}
.note{{font-weight:400;font-size:14px;letter-spacing:.1em;color:{WHITE}}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 794 1123" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:40px;top:50px"><img class="star" src="{STAR}" style="right:40px;top:76px">
<div class="head"><div class="kick">TERRATHON MINI-FETE</div><img class="logo" src="{LOGO}"><div class="title">THE MENU</div>
<div class="sub">ARTILY, OUR HYDRATION PARTNER</div><div class="info">3RD + 4TH OCTOBER 2026  |  TURF XL, NEW ALIPORE</div></div>
<div class="body">{cardA}{cardB}<div class="photos">{photos}</div></div>
<div class="foot"><img src="{core.LOGO}"><div class="hd">@ARTILYINDIA</div><div class="note">ALL PRICES IN RS.</div></div>
</div></body></html>"""

CHECK = """() => {
  const pg = document.getElementById('page'), pr = pg.getBoundingClientRect(), bad = [];
  document.querySelectorAll('.page *').forEach(e => {
    const r = e.getBoundingClientRect(); if (!r.width || !r.height || e.closest('svg.specks')) return;
    if (r.right > pr.right + 0.5 || r.left < pr.left - 0.5 || r.bottom > pr.bottom + 0.5) bad.push(['off-page', String(e.className || e.tagName), Math.round(r.right), Math.round(r.bottom)]);
  });
  const cards = [...document.querySelectorAll('.card')], ph = document.querySelector('.photos'), foot = document.querySelector('.foot'), head = document.querySelector('.head');
  const q = e => { const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; };
  const stars = [...document.querySelectorAll('.star')].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
  const title = document.querySelector('.title').getBoundingClientRect();
  return {bad, head: q(head), cards: cards.map(q), photos: q(ph), foot: q(foot), stars, titleX: [Math.round(title.left), Math.round(title.right)], titleW: Math.round(document.querySelector('.title').scrollWidth)};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print("CHECK", await pg.evaluate(CHECK))
        await pg.locator("#page").screenshot(path="out/collaterals/artily_menu_A4.png")
        await pg.pdf(path="out/collaterals/artily_menu_A4.pdf", width="210mm", height="297mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    d = open("out/collaterals/artily_menu_A4.pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
