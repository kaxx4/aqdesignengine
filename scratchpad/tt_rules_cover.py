"""TerraThon RULES cover, static feed post 1080x1350. Opener for the three rules posts (tt_rules_cricket.py). Swipe order is
chronological: 02 PickleJam (Fri 2), 03 Wicket Wars (Sat 3 + Sun 4), 04 Soccer Storm (Sat 3). The 02/03/04 tags are the real slide positions
in that order; if the carousel is ordered differently, edit ORDER.
Facts only from the site/the user: dates, venues (user rulings: 11:11 Pick A Court, Turf XL, Battleground Gaming), report-by times, and the
site's own line "Turn up at the reporting time, not the match time". Real sport stickers from the kit; green boxes, purple everything else.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_rules_cover.py
"""
import asyncio, importlib.util, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL
GREEN = "#2FD284"
H = 1350
ORDER = [  # (sticker, name, meta, slide tag)
    ("pickleball_set.png", "PICKLEJAM", "FRI 2 OCT  |  REPORT BY 11:45AM", "02"),
    ("cricket_set.png", "WICKET WARS", "SAT 3 + SUN 4 OCT  |  REPORT BY 9:45AM", "03"),
    ("controller.png", "SOCCER STORM", "SAT 3 OCT  |  REPORT BY 11:15AM", "04"),
]


async def main():
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']
    m = await B.measure_text([dict(text="RULES", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="READ BEFORE YOU REPORT", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 780 / m[0]["text_w"]; spx = 50 * min(1.0, 800 / m[1]["text_w"])
    parts.append(f'<div class="measure" data-tag="t1" style="position:absolute;left:{(W - 700) / 2}px;width:700px;top:52px;text-align:center;color:{CREAM_HALO};font-family:var(--d);font-weight:400;font-size:46px;line-height:1;white-space:nowrap;z-index:6">TERRATHON 2026</div>')
    parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 800) / 2}px;width:800px;top:112px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">RULES</div>')
    sy = 112 + tpx * 1.02
    parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 860) / 2}px;width:860px;top:{sy}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">READ BEFORE YOU REPORT</div>')
    el("t1", (W - 460) / 2, 56, 460, 38); el("t2", (W - 780) / 2, 116, 780, tpx * .82); el("t3", (W - 800) / 2, sy + 2, 800, spx * .82)
    for lab, x, y in (("star_tl", 30, 60), ("star_tr", W - 30 - 110, 74)):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = 110 * im.height / im.width; el(lab, x, y, 110, hh)
        parts.append(f'<img src="{src}" class="measure" data-tag="{lab}" style="position:absolute;left:{x}px;top:{y}px;width:110px;height:{hh}px;z-index:5">')
    cy0 = sy + spx + 56; ch, gap = 226, 28; cx, cw = 56, 968
    for i, (stk, name, meta, tag) in enumerate(ORDER):
        y = cy0 + i * (ch + gap)
        im, src = tt.crop_to_alpha(stk); k = min(160 / im.height, 150 / im.width); sw, sh = im.width * k, im.height * k
        el(f"card{i}", cx, y, cw, ch)
        parts.append(f'<div class="measure" data-tag="card{i}" style="position:absolute;left:{cx}px;top:{y}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:34px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;gap:26px;padding:0 30px 0 26px;color:{INK};font-family:var(--d);z-index:6">'
                     f'<div style="width:160px;flex:none;display:flex;justify-content:center"><img src="{src}" style="width:{sw:.1f}px;height:{sh:.1f}px;display:block"></div>'
                     f'<div style="flex:1 1 0;min-width:0;white-space:nowrap"><div style="font-weight:900;font-size:60px;line-height:1">{name}</div>'
                     f'<div style="font-weight:400;font-size:25px;line-height:1.1;margin-top:12px">{meta}</div></div>'
                     f'<div style="flex:none;background:{GREEN};color:{INK};font-weight:900;font-size:34px;line-height:1;padding:12px 20px 11px;border-radius:999px">{tag} &rarr;</div></div>')
    ny = cy0 + 3 * ch + 2 * gap + 34
    parts.append(f'<div class="measure" data-tag="note" style="position:absolute;left:{(W - 1000) / 2}px;width:1000px;top:{ny}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:28px;line-height:1;white-space:nowrap;z-index:6">'
                 f'TURN UP AT THE <span style="color:{ORCHID}">REPORTING TIME</span>, NOT THE MATCH TIME</div>')
    el("note", (W - 940) / 2, ny + 2, 940, 26)
    ly = H - 27 - 56
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); el("logo", 27, ly, 320, 56)
    cw2, chh = 470, 70; px_, py_ = W - 27 - cw2, H - 13 - chh; el("cta", px_, py_, cw2, chh)
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{px_}px;top:{py_}px;width:{cw2}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                 f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:32px;color:{INK}">SWIPE FOR THE RULES</div>')
    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("card", INK, CTA_FILL, 56, True), ("tag", INK, GREEN, 34, True),
                  ("note", WHITE, GROUND, 28, True), ("cta", INK, CTA_FILL, 32, True)]
    out = "out/collaterals/terrathon_rules_cover.png"; os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, page_bg=GROUND, expect_hero=False, margin=12)
    print("done", out)

asyncio.run(main())
