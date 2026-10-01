"""TerraThon Mini-Fete: the single-slide WHATSAPP marketing graphic with ALL the pointers (Tue 29 Sep). 1080x1350 (4:5).
Seven pointer pills + date/venue + OPEN TO ALL + a QR code made from the user's real group link (decoded and verified) + footer AQ logo and ALL FOR CHARITY.
Copy is DRAFT for the user's approval; every fact is one the user gave."""
import asyncio, base64, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
H = 1350
STORY = False     # main(story=True) renders 1080x1920 with Instagram's safe zones
OY = 0
POINTS = [("DISCO DASH", "WIN FREE DD TICKETS"), ("PHOTOBOOTH", "POSE NOW"), ("ARTILY", "BOBA"), ("CRAVE'LLA", "DESSERTS + BROWNIES"),
          ("CRFTD ORDERS", "T-SHIRT ORDERS TAKEN"), ("LOTTERY", "AT LOCATION"), ("DD TICKET STALL", "RS. 550  |  DISCO DIWALI 10TH NOV")]

async def main(story=False):
    global H, OY
    H = 1920 if story else 1350; OY = 250 if story else 0
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    def img(name, label, x, y, w, z=3):
        im, src = tt.crop_to_alpha(name); h = w * im.height / im.width; el(label, x, y, w, h)
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">', h
    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>', f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']
    m = await B.measure_text([dict(text="MINI-FEETE", font="StretchPro", size=100, weight=400, letter_spacing="-0.02em", features=tt.ST_FEAT),
                              dict(text="7 REASONS TO SHOW UP", font="SigmarOne", size=60, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    # title block
    tpx = 100 * 760 / m[0]["text_w"]; spx = 60 * min(1.0, 760 / m[1]["text_w"])
    parts.append(f'<div class="measure" data-tag="t1" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{70 + OY}px;text-align:center;color:{CREAM_HALO};font-family:var(--d);font-weight:400;font-size:44px;line-height:1;white-space:nowrap;z-index:6">TERRATHON</div>')
    parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{126 + OY}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{0.03 * tpx}px {WHITE};'
                 f'letter-spacing:-0.02em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">MINI-FEETE</div>')
    parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 800) / 2}px;width:800px;top:{126 + OY + tpx * 1.08}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">7 REASONS TO SHOW UP</div>')
    el("t1", (W - 300) / 2, 72 + OY, 300, 36); el("t2", (W - 760) / 2, 128 + OY, 760, tpx * .8); el("t3", (W - 760) / 2, 126 + OY + tpx * 1.08 + 4, 760, spx * .8)
    y0 = 126 + OY + tpx * 1.08 + spx + 40      # start of the pointer grid
    # 7 pointer pills in two columns + the carnival sticker in the 8th cell
    pw, ph, gx, gy = 470, (132 if story else 108), 24, (28 if story else 20)
    x0 = (W - (2 * pw + gx)) / 2
    for i, (a, b) in enumerate(POINTS):
        col, row = i % 2, i // 2
        full = i == len(POINTS) - 1                      # DD ticket stall: the payoff, full width
        x, y, w_ = (x0, y0 + row * (ph + gy), 2 * pw + gx) if full else (x0 + col * (pw + gx), y0 + row * (ph + gy), pw)
        el(f"pill{i}", x, y, w_, ph)
        parts.append(f'<div class="measure" data-tag="pill{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w_}px;height:{ph}px;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{INK};font-family:var(--d);white-space:nowrap;z-index:6">'
                     f'<div style="font-weight:900;font-size:34px;line-height:1.05">{a}</div><div style="font-weight:400;font-size:22px;line-height:1.1;margin-top:2px">{b}</div></div>')
    yb = y0 + 4 * (ph + gy) + 6
    # date / venue / open to all
    parts.append(f'<div class="measure" data-tag="dv" style="position:absolute;left:{(W - 900) / 2}px;width:900px;top:{yb}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:400;font-size:34px;line-height:1;white-space:nowrap;z-index:6">'
                 f'3RD &amp; 4TH OCTOBER, 2026  |  TURF XL, NEW ALIPORE</div>')
    parts.append(f'<div class="measure" data-tag="oa" style="position:absolute;left:{(W - 900) / 2}px;width:900px;top:{yb + 46}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:40px;line-height:1;white-space:nowrap;z-index:6">OPEN TO ALL  |  ALL FOR CHARITY</div>')
    el("dv", (W - 860) / 2, yb + 3, 860, 30); el("oa", (W - 720) / 2, yb + 48, 720, 34)
    # footer: logo left, QR right
    qy = H - (300 if story else 40) - 220
    cs, chh = img("carnival.png", "carnival", 60, yb + (96 if story else 108), 205 if story else 235); parts.append(cs)
    qsrc = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/qr_whatsapp_group.png", "rb").read()).decode()
    el("qr", W - 40 - 220, qy, 220, 220)
    parts.append(f'<div class="measure" data-tag="qr" style="position:absolute;left:{W - 40 - 220}px;top:{qy}px;width:220px;height:220px;background:#fff;border:6px solid {ORCHID};border-radius:22px;z-index:8;display:flex;align-items:center;justify-content:center">'
                 f'<img src="{qsrc}" style="width:186px;height:186px;display:block"></div>')
    parts.append(f'<div class="measure" data-tag="qrl" style="position:absolute;left:{W - 40 - 220 - 330}px;width:310px;top:{qy + 78}px;text-align:right;color:{WHITE};font-family:var(--d);font-weight:900;font-size:30px;line-height:1.1;z-index:6">SCAN TO JOIN THE <span style="color:{ORCHID}">WHATSAPP GROUP</span></div>')
    el("qrl", W - 40 - 220 - 330, qy + 78, 310, 70)
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{qy + (196 if story else 150)}px;height:56px;z-index:9">'); el("logo", 27, qy + (196 if story else 150), 320, 56)
    for lab, x, y, z in (("star_tl", 40, 60 + OY, 5), ("star_tr", 940, 70 + OY, 5)):
        s, _ = img("shuriken.png", lab, x, y, 100, z); parts.append(s)
    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("pill", INK, CTA_FILL, 34, True), ("sub", ORCHID, GROUND, 60, True), ("small", WHITE, GROUND, 30, False)]
    os.makedirs("out/collaterals/stories", exist_ok=True)
    async with B.session():
        await B.render(html, ("out/collaterals/stories/whatsapp_all_pointers_story.png" if story else "out/collaterals/whatsapp_all_pointers.png"), W, H, elements=els, text_pairs=text_pairs, page_bg=GROUND, expect_hero=True, margin=12)
    print("done")
import sys
asyncio.run(main(story="story" in sys.argv[1:]))
