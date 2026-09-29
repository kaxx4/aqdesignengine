"""TerraThon WICKET WARS (cricket) RULES, static feed post 1080x1350. Copy is condensed FROM the user-pasted rules page
(ngoaquaterra.com/terrathon/cricket, 2026-09-29); every rule keeps its number, and nothing is added. Six cards + a conduct strip.

Adaptations / known source conflicts (flagged to the user):
  * the site names DigiLocker Aadhaar ID in "Who can play" but "school or college ID" in the header and "Bring", so the WHO card says only
    "IDs are checked" and does not pick an ID type.
  * body copy is sentence case (NeutralFace regular) for legibility at 22px; headers and the conduct strip are caps.
  * "Wide / no ball in the final over: not legal deliveries, 1 run" is kept as the site words it; the poster does not say they are re-bowled.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_rules_cricket.py [cricket|pickleball]
"""
import asyncio, importlib.util, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL
H = 1350
GREEN = "#2FD284"     # TerraThon hero-sticker green (brain/TERRATHON.md sec 4)

import sys
SPORT = sys.argv[1] if len(sys.argv) > 1 else "cricket"
SPORTS = {
    "cricket": dict(
        title="WICKEET WAARS", info=("SAT 3 + SUN 4 OCT  |  TURF XL, NEW ALIPORE  |  ", "REPORT BY 9:45AM"),
        strip=("TEAM REPORTS 20 MIN BEFORE ITS MATCH  |  ", "UMPIRE'S DECISION IS FINAL"), strip2="NO ABUSE. NO VAPES, ALCOHOL OR SIMILAR SUBSTANCES.",
        cta="LINK IN THE BIO", out="terrathon_cricket_rules.png",
        cards=[
            ("WHO CAN PLAY", "Born on or after 1 January 2005. Every player must qualify, not just the captain. IDs are checked, and no ID on time can mean disqualification."),
            ("FORMAT", "One innings each, straight knockout. 5 overs, and the fielding side has 15 minutes to finish. 8 players a team (7 + 1 sub), one jersey colour. Bring your own bats and gloves."),
            ("BOWLING", "Full-arm only, with a run-up. No underarm, standing, sling-action or chucking. At least 4 bowlers a match. One bowler may bowl 2 overs, not back to back."),
            ("POWERPLAY", "One Powerplay over per team, and all runs in it count double. It cannot be the last over. Call it before the bowler is picked, or the second-last over becomes it."),
            ("SCORING", "Wides and no balls give 3 runs and count as a ball. In the final over they are not legal balls and give 1 run. Overthrows are live: every valid run counts."),
            ("CEILING NET", "Ball hits the ceiling net and is caught straight after: the batter is out. If it touches a side-wall net first, then it is caught: not out."),
        ]),
    # PICKLEBALL (rules page pasted 2026-09-29). Registrations are CLOSED on the site, so the pill is not a register CTA.
    # Venue: the site says "Confirming"; the user ruled 11:11 Pick A Court earlier (flagged again to the user).
    "pickleball": dict(
        title="PICKLEE JAAM", info=("FRI 2 OCT  |  11:11 PICK A COURT  |  ", "REPORT BY 11:45AM"),
        strip=("MATCHES RUN 12PM TO 7PM  |  ", "UMPIRE'S DECISION IS FINAL"), strip2="BRING YOUR SCHOOL OR COLLEGE ID AND YOUR ENTRY CONFIRMATION.",
        cta="SEE YOU FRI 2 OCT", out="terrathon_pickleball_rules.png", body=24,
        cards=[
            ("THE GAME", "Doubles, on a court the size of a badminton court. Rallies are short and the serve is underarm."),
            ("WHO CAN PLAY", "Born on or after 1 January 2005. Both players in a pair have to meet this. IDs are checked at the gate."),
            ("FORMAT", "Teams of 2 play single matches to 11 points, with a group stage first. All official international pickleball rules are followed."),
            ("KNOCKOUTS", "After the group stage, all matches are knockouts. Semis and finals are best&nbsp;of&nbsp;3."),
            ("PADDLES", "Bring your own paddle. Limited paddles may be provided on prior request, subject to availability."),
            ("CONDUCT", "Any misconduct, foul language or physical altercation leads to immediate disqualification."),
        ]),
}
CFG = SPORTS[SPORT]
CARDS = CFG["cards"]
CX, CW, CG = 56, 472, 24
CY0, CH, RG = 296, 270, 14


async def main():
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']
    m = await B.measure_text([dict(text=CFG["title"], font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="THE RULES", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 800 / m[0]["text_w"]; spx = 50 * min(1.0, 500 / m[1]["text_w"])
    parts.append(f'<div class="measure" data-tag="t1" style="position:absolute;left:{(W - 420) / 2}px;width:420px;top:38px;text-align:center;color:{CREAM_HALO};font-family:var(--d);font-weight:400;font-size:40px;line-height:1;z-index:6">TERRATHON</div>')
    parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 820) / 2}px;width:820px;top:88px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{CFG["title"]}</div>')
    parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 560) / 2}px;width:560px;top:{88 + tpx * 1.05}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">THE RULES</div>')
    el("t1", (W - 300) / 2, 40, 300, 34); el("t2", (W - 800) / 2, 92, 800, tpx * .82); el("t3", (W - 360) / 2, 88 + tpx * 1.05 + 2, 360, spx * .82)
    iy = 88 + tpx * 1.05 + spx + 26
    parts.append(f'<div class="measure" data-tag="info" style="position:absolute;left:{(W - 1000) / 2}px;width:1000px;top:{iy}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:27px;line-height:1;white-space:nowrap;z-index:6">'
                 f'{CFG["info"][0]}<span style="color:{ORCHID}">{CFG["info"][1]}</span></div>')
    el("info", (W - 960) / 2, iy + 2, 960, 24)
    for lab, x, y in (("star_tl", 24, 46), ("star_tr", W - 24 - 104, 58)):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = 104 * im.height / im.width; el(lab, x, y, 104, hh)
        parts.append(f'<img src="{src}" class="measure" data-tag="{lab}" style="position:absolute;left:{x}px;top:{y}px;width:104px;height:{hh}px;z-index:5">')
    for i, (head, body) in enumerate(CARDS):
        acc = GREEN
        x = CX + (i % 2) * (CW + CG); y = CY0 + (i // 2) * (CH + RG)
        el(f"card{i}", x, y, CW, CH)
        parts.append(f'<div class="measure" data-tag="card{i}" style="position:absolute;left:{x}px;top:{y}px;width:{CW}px;height:{CH}px;box-sizing:border-box;border:6px solid {acc};border-radius:30px;background:{CTA_FILL};'
                     f'padding:16px 20px;color:{INK};font-family:var(--d);z-index:6;overflow:hidden">'
                     f'<div style="display:inline-block;background:{acc};color:{INK};font-weight:900;font-size:26px;line-height:1;padding:7px 16px 6px;border-radius:999px">{head}</div>'
                     f'<div style="font-weight:400;font-size:{CFG.get("body", 22)}px;line-height:1.22;margin-top:12px">{body}</div></div>')
    sy = CY0 + 3 * CH + 2 * RG + 24
    parts.append(f'<div class="measure" data-tag="strip1" style="position:absolute;left:{(W - 1000) / 2}px;width:1000px;top:{sy}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:24px;line-height:1;white-space:nowrap;z-index:6">'
                 f'{CFG["strip"][0]}<span style="color:{ORCHID}">{CFG["strip"][1]}</span></div>')
    parts.append(f'<div class="measure" data-tag="strip2" style="position:absolute;left:{(W - 1000) / 2}px;width:1000px;top:{sy + 38}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:400;font-size:22px;line-height:1;white-space:nowrap;z-index:6">'
                 f'{CFG["strip2"]}</div>')
    el("strip1", (W - 960) / 2, sy + 2, 960, 24); el("strip2", (W - 700) / 2, sy + 40, 700, 20)
    ly = H - 27 - 56
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); el("logo", 27, ly, 320, 56)
    cw, chh = 400, 70; cx, cy = W - 27 - cw, H - 13 - chh; el("cta", cx, cy, cw, chh)
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                 f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:32px;color:{INK}">{CFG["cta"]}</div>')
    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("card", INK, CTA_FILL, 23, False), ("chip", INK, GREEN, 26, True),
                  ("info", WHITE, GROUND, 27, True), ("strip", WHITE, GROUND, 22, False), ("cta", INK, CTA_FILL, 32, True)]
    out = "out/collaterals/" + CFG["out"]; os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, page_bg=GROUND, expect_hero=False, margin=12)
    print("done", out)

asyncio.run(main())
