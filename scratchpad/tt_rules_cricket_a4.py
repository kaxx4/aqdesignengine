"""TerraThon WICKEET WAARS (cricket) RULES, single page A4 PORTRAIT (210x297mm), TerraThon branding. PDF + 300dpi PNG.
Copy is the SAME condensed, user-approved rules copy as the feed post (scratchpad/tt_rules_cricket.py, condensed from the organisers' 19/20-rule text): eight cards, every
rule keeping its substance, nothing added. Same conventions as the feed post: green cards and chips, everything else purple/white, StretchPro title with the doubled-letter
stretch ligatures (WICKEET WAARS is the brand spelling), Sigmar One "THE RULES", info line, conduct strip, AQ logo + "SEE YOU 3 + 4 OCT" pill.
Known gaps carried over from the source (flagged to the user earlier): the "report at least __ minutes before" number in rule 6 was cut off in the pasted text, so it is NOT
printed (the info line's "REPORT BY 9:45AM" is the one time that was confirmed); the prize pool (rule 17) is not on this poster. Body type is 15.5px css ~ 11.5pt on A4.
PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; ask the printer for a bleed proof.

FIFA: arg `fifa` (SOCCER STOORM, the feed post's 5 condensed cards, last one full width; bigger type because there is more room).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_rules_cricket_a4.py [fifa]   ->  out/collaterals/terrathon_cricket_rules_A4_portrait.pdf + .png (terrathon_fifa_rules_A4_portrait with fifa)
"""
import asyncio, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
from playwright.async_api import async_playwright

GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL
GREEN = "#2FD284"
W, H = 794, 1123
_im, STAR = tt.crop_to_alpha("shuriken.png")
FIFA_ARG = "fifa" in sys.argv
if FIFA_ARG:   # copy = the feed post's FIFA config (scratchpad/tt_rules_cricket.py): venue ruled "Battleground Gaming" by the user; controller line removed at the user's request
    TITLE, INFO, STRIP, STRIP2, CTA = "SOCCER STOORM", ("SAT 3 OCT  |  BATTLEGROUNDS, BHOWANIPORE  |  ", "REPORT BY 11:15AM"), ("", "ORGANISERS' DECISIONS ARE FINAL"), "3 PAUSES A MATCH. NO CHEATING, ABUSE OR MATCH-FIXING.", "SEE YOU SAT 3 OCT"
    CARDS = [
        ("WHO CAN PLAY", "Born on or after 1 January 2005, checked by ID. Registration is solo, and every match is 1v1."),
        ("PLATFORM", "PS5, EA SPORTS FC 26. Competitive mode, normal speed, clear weather, injuries and handball off. No custom squads, edited ratings or modified settings."),
        ("FORMAT", "Single elimination: Round of 16, Quarter Finals, Semi Finals, Grand Final. Halves are 6 minutes, then 8 in the semis and final. Tied? Extra Time, then Penalties."),
        ("REPORTING", "Be at the venue 10 minutes before your match. More than 5 minutes late is a loss by walkover, with no refund."),
        ("TEAM DRAW", "On the day, each player draws a chit for their team, and both players must be there. Draws are final unless the organisers say otherwise. The pool: Arsenal, Borussia Dortmund, Bayern Munich, PSG, Real Madrid, FC Barcelona, Al Nassr, Al Hilal, Liverpool, Chelsea, Manchester City, Manchester United, Atl\u00e9tico Madrid.", True),
    ]
    BODY_PX, CHIP_PX, ROWS_N, OUT = 19, 22, 3, "terrathon_fifa_rules_A4_portrait"
else:
    TITLE, INFO, STRIP, STRIP2, CTA = "WICKEET WAARS", ("SAT 3 + SUN 4 OCT  |  TURF XL, NEW ALIPORE  |  ", "REPORT BY 9:45AM"), ("NON-SPORTING APPEALS ARE PENALISED  |  ", "UMPIRE'S DECISION IS FINAL"), "ABUSE MEANS DISQUALIFICATION OR HEAVY PENALTIES. NO VAPES OR ALCOHOL.", "SEE YOU 3 + 4 OCT"
    BODY_PX, CHIP_PX, ROWS_N, OUT = 15.5, 19, 4, "terrathon_cricket_rules_A4_portrait"
    CARDS = [
        ("WHO CAN PLAY", "Born on or after 1 January 2005, verified by a scannable Aadhaar ID. No ID on time can mean disqualification in a dispute."),
        ("FORMAT", "One innings each, straight knockout. 5 overs, finished by the fielding side in 15 minutes; batting-side delays count. 8 players, one jersey colour."),
        ("REPORTING", "Whole team reports before its match. Not ready for the toss within 5 minutes of schedule: 3&#8209;run penalty per minute. Over 15 minutes: walkover."),
        ("EQUIPMENT", "Bring your own bats and safety gear (gloves, guards). Any bat except hollow, scoop or plastic. Ball: Cricket Tennis Ball Heavy Version by Vicky."),
        ("BOWLING", "Full-arm only, with a run-up. No underarm, standing, sling-action or chucking. At least 4 bowlers, and one may bowl 2 overs, not back to back."),
        ("POWERPLAY", "One Powerplay over per team, and all runs count double. Not the last over. Call it before the bowler is picked, or the second-last over becomes it."),
        ("SCORING", "Wides and no balls: 3 runs, and they count as a ball. In the final over: 1 run, not legal balls. Overthrows are live: all valid runs count."),
        ("CEILING NET", "Ball hits the ceiling net and is caught straight after: out. If it touches a side-wall net first, then it is caught: not out."),
    ]
rnd = random.Random(7)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(380))
WIDE = ' style="grid-column:1/-1"'
cards_html = "".join(f'<section class="card"{WIDE if len(c) > 2 else ""}><div class="chip">{c[0]}</div><div class="bd">{c[1]}</div></section>' for c in CARDS)

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:210mm 297mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE}}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:56px;z-index:1}}
.hd{{position:absolute;left:0;right:0;top:30px;text-align:center;z-index:3}}
.t1{{font-weight:400;font-size:26px;letter-spacing:.2em;color:{CREAM_HALO}}}
.ti{{font-family:'StretchPro';color:{WHITE};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};line-height:1;white-space:nowrap;display:block;margin-top:8px}}
.tr{{font-family:'SigmarOne';color:{ORCHID};letter-spacing:{tt.SG_LS}em;line-height:1;white-space:nowrap;display:block;margin-top:6px}}
.info{{font-weight:900;color:{WHITE};line-height:1;white-space:nowrap;display:block;margin-top:14px}} .info b{{color:{ORCHID};font-weight:900}}
.grid{{position:absolute;left:36px;right:36px;top:224px;height:700px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat({ROWS_N},1fr);gap:12px 16px;z-index:3}}
.card{{border:5px solid {GREEN};border-radius:24px;background:{CTA_FILL};color:{INK};padding:10px 16px 8px;overflow:hidden}}
.chip{{display:inline-block;background:{GREEN};color:{INK};font-weight:900;font-size:{CHIP_PX}px;line-height:1;letter-spacing:.03em;padding:6px 13px 5px;border-radius:999px}}
.bd{{font-weight:400;font-size:{BODY_PX}px;line-height:1.17;margin-top:{8 if FIFA_ARG else 6}px}}
.strip{{position:absolute;left:0;right:0;text-align:center;z-index:3;white-space:nowrap}}
.s1{{top:944px;font-weight:900;font-size:17px;color:{WHITE}}} .s1 b{{color:{ORCHID};font-weight:900}}
.s2{{top:976px;font-weight:400;font-size:15.5px;color:{WHITE}}}
.aq{{position:absolute;left:30px;bottom:24px;height:40px;z-index:4}}
.cta{{position:absolute;right:30px;bottom:18px;height:54px;width:300px;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};color:{INK};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:26px;z-index:4}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:16px;top:20px"><img class="star" src="{STAR}" style="right:16px;top:24px">
<div class="hd"><div class="t1">TERRATHON</div><span class="ti" id="ti">{TITLE}</span><span class="tr" id="tr">THE RULES</span><span class="info" id="info">{INFO[0]}<b>{INFO[1]}</b></span></div>
<div class="grid" id="grid">{cards_html}</div>
<div class="strip s1" id="s1">{STRIP[0]}<b>{STRIP[1]}</b></div><div class="strip s2" id="s2">{STRIP2}</div>
<img class="aq" id="aq" src="{core.LOGO}"><div class="cta" id="cta">{CTA}</div>
</div></body></html>"""

FIT = """() => {
  const tw = e => { const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().width; };
  const fit = (id, target, strokeEm, cap) => { const e = document.getElementById(id); e.style.fontSize = '100px'; if (strokeEm) e.style.webkitTextStroke = (strokeEm * 100) + 'px currentColor';
    let px = Math.min(100 * target / tw(e), cap || 1e9); e.style.fontSize = px + 'px'; if (strokeEm) e.style.webkitTextStroke = (strokeEm * px) + 'px currentColor'; return Math.round(px * 10) / 10; };
  return [fit('ti', 640, 0.04), fit('tr', 330, 0.03, 40), fit('info', 700, 0, 19), fit('s1', 700, 0, 17)]; }"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), q = e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const cards = [...document.querySelectorAll('.card')], over = cards.map((c, i) => [i, c.scrollHeight - c.clientHeight, q(c)]).filter(x => x[1] > 0);
  const lines = cards.map(c => { const b = c.querySelector('.bd'); return Math.round(b.getBoundingClientRect().height / parseFloat(getComputedStyle(b).lineHeight)); });
  const nat = cards.map(c => Math.round(c.querySelector('.chip').getBoundingClientRect().height + c.querySelector('.bd').getBoundingClientRect().height + 6 + 18 + 10));
  const boxes = {hd: q(document.querySelector('.hd')), info: q(document.getElementById('info')), grid: q(document.getElementById('grid')), s1: q(document.getElementById('s1')), s2: q(document.getElementById('s2')), aq: q(document.getElementById('aq')), cta: q(document.getElementById('cta'))};
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]); const k = Object.keys(boxes), ov = [], edge = [];
  for (let i = 0; i < k.length; i++) { const b = boxes[k[i]]; if (b[0] < 12 || b[2] > pr.right - 12 || b[3] > pr.bottom - 12) edge.push([k[i], b]); for (let j = i + 1; j < k.length; j++) if (hit(b, boxes[k[j]])) ov.push([k[i], k[j]]); }
  const stars = [...document.querySelectorAll('.star')].map(q), starHit = stars.map((s, i) => [i, hit(s, boxes.hd) && hit(s, [boxes.hd[0] + 80, 0, boxes.hd[2] - 80, 9999])]);
  return {over, lines, nat, boxes, ov, edge, stars};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    out = "out/collaterals/" + OUT
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        r = await pg.evaluate(CHECK)
        print("card overflow", r["over"]); print("lines", r["lines"], "natural heights", r["nat"]); print("boxes", r["boxes"]); print("overlaps", r["ov"], "edge", r["edge"], "stars", r["stars"])
        await pg.locator("#page").screenshot(path=out + ".png")
        await pg.pdf(path=out + ".pdf", width="210mm", height="297mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    d = open(out + ".pdf", "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
