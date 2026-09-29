"""TerraThon SCHEDULE, static feed graphic (1080x1350). Fri 2 - Sun 4 Oct 2026, three days, Mini-Fete included.

Bespoke build from the TerraThon format constants (tt_events.py): black ground with white flecks, blue shuriken furniture,
cream cards with orchid border (the slab's language), StretchPro title, Sigmar One subtitle (sparingly), NeutralFace body.
All times/venues are from the user's live-site timetable (2026-09-29) and answers: Mini-Fete runs the same hours as cricket,
pickleball is at 11:11 Pick A Court, FIFA is at Battleground Gaming. Fixture draw is on the day (site copy).

Adaptations: stickers per row are the kit's real assets (cricket_set, pickleball_set, controller, carnival), cropped to alpha.
The CTA pill says TURN UP EARLY (registrations may have closed by post day; no invented link).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_schedule.py [story]   (story = 1080x1920, IG safe zones kept clear)
"""
import asyncio, importlib.util, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL

# (sticker, sport, venue, report-by, matches, tag)
DAYS = [
    ("FRI", "02", [("pickleball_set.png", "PICKLEBALL", "11:11 PICK A COURT", "11:45AM", "12PM TO 7PM", None)]),
    ("SAT", "03", [("cricket_set.png", "CRICKET", "TURF XL, NEW ALIPORE", "9:45AM", "10AM TO 4PM", None),
                   ("controller.png", "FIFA", "BATTLEGROUND GAMING", "11:15AM", "11:30AM TO 1:30PM", None),
                   ("carnival.png", "MINI-FETE", "TURF XL, NEW ALIPORE", None, "10AM TO 4PM", "OPEN TO ALL")]),
    ("SUN", "04", [("cricket_set.png", "CRICKET", "TURF XL, NEW ALIPORE", "9:45AM", "10AM TO 2PM", None),
                   ("carnival.png", "MINI-FETE", "TURF XL, NEW ALIPORE", None, "10AM TO 2PM", "OPEN TO ALL")]),
]
CARD_X, CARD_W, COL_W, BORDER = 56, 968, 172, 6


async def main(story=False):
    H = 1920 if story else 1350                  # story: Instagram UI zones (top ~250, bottom ~270) kept clear
    OY = 192 if story else 0                     # title block drop
    ROW_H = 140 if story else 118
    GAP = 32 if story else 24
    Y0 = 470 if story else 322
    FOOT = 270 if story else 0                   # footer lift off the bottom edge
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    def sticker(name, label, x, y, hh, z=4):
        im, src = tt.crop_to_alpha(name); k = min(hh / im.height, 92 / im.width); w = im.width * k; hh = im.height * k
        return f'<img src="{src}" style="height:{hh}px;width:{w:.1f}px;display:block;flex:none">', w
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    m = await B.measure_text([dict(text="SCHEDULE", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="2ND TO 4TH OCTOBER", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 640 / m[0]["text_w"]; spx = 50 * min(1.0, 700 / m[1]["text_w"])
    parts.append(f'<div class="measure" data-tag="t1" style="position:absolute;left:{(W - 420) / 2}px;width:420px;top:{58 + OY}px;text-align:center;color:{CREAM_HALO};font-family:var(--d);font-weight:400;font-size:44px;line-height:1;z-index:6">TERRATHON</div>')
    parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 700) / 2}px;width:700px;top:{112 + OY}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">SCHEDULE</div>')
    parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{112 + OY + tpx * 1.05}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">2ND TO 4TH OCTOBER</div>')
    el("t1", (W - 300) / 2, 60 + OY, 300, 36); el("t2", (W - 640) / 2, 116 + OY, 640, tpx * .82); el("t3", (W - 700) / 2, 112 + OY + tpx * 1.05 + 2, 700, spx * .82)

    y = Y0
    for di, (dn, dd_, rows) in enumerate(DAYS):
        ch = len(rows) * ROW_H + 2 * BORDER
        el(f"card{di}", CARD_X, y, CARD_W, ch)
        col = (f'<div style="width:{COL_W}px;flex:none;background:{ORCHID};display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK};'
               f'font-family:var(--d);border-radius:26px 0 0 26px;border-right:4px solid {INK}">'
               f'<div style="font-weight:900;font-size:58px;line-height:.95">{dn}</div>'
               f'<div style="font-weight:900;font-size:30px;line-height:1;margin-top:8px">{dd_} OCT</div></div>')
        body = ""
        for ri, (stk, sport, venue, rep, mt, tag) in enumerate(rows):
            sh = 96 if story else 84
            simg, sw = sticker(stk, sport, 0, 0, sh)
            chip = ""
            rep_html = (f'<div style="font-weight:400;font-size:22px;line-height:1.1;margin-top:4px">REPORT BY <span style="font-weight:900">{rep}</span></div>' if rep
                        else f'<div style="font-weight:900;font-size:22px;line-height:1.1;margin-top:4px;color:{INK}">OPEN TO ALL</div>')
            sep = "" if ri == len(rows) - 1 else f"border-bottom:3px solid {INK};"
            body += (f'<div style="height:{ROW_H}px;box-sizing:border-box;{sep}display:flex;align-items:center;padding:0 22px 0 18px;gap:16px;color:{INK};font-family:var(--d)">'
                     f'<div style="width:96px;flex:none;display:flex;justify-content:center">{simg}</div>'
                     f'<div style="flex:1 1 0;min-width:0;white-space:nowrap"><div style="font-weight:900;font-size:40px;line-height:1">{sport}{chip}</div>'
                     f'<div style="font-weight:400;font-size:23px;line-height:1.1;margin-top:5px">{venue}</div></div>'
                     f'<div style="flex:none;text-align:right;white-space:nowrap"><div style="font-weight:900;font-size:31px;line-height:1">{mt}</div>{rep_html}</div></div>')
        parts.append(f'<div class="measure" data-tag="card{di}" style="position:absolute;left:{CARD_X}px;top:{y}px;width:{CARD_W}px;height:{ch}px;box-sizing:border-box;'
                     f'border:{BORDER}px solid {ORCHID};border-radius:32px;background:{CTA_FILL};display:flex;z-index:6">{col}<div style="flex:1 1 0;min-width:0">{body}</div></div>')
        y += ch + GAP
    yb = y - GAP + 36

    parts.append(f'<div class="measure" data-tag="note1" style="position:absolute;left:{(W - 1040) / 2}px;width:1040px;white-space:nowrap;top:{yb}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:30px;line-height:1;z-index:6">'
                 f'TURN UP AT THE <span style="color:{ORCHID}">REPORTING TIME</span>, NOT THE MATCH TIME</div>')
    parts.append(f'<div class="measure" data-tag="note2" style="position:absolute;left:{(W - 1040) / 2}px;width:1040px;white-space:nowrap;top:{yb + 48}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:400;font-size:22px;line-height:1;z-index:6">'
                 f'FIXTURES ARE DRAWN ON THE DAY. A SQUAD NOT THERE WHEN CALLED FORFEITS.</div>')
    el("note1", (W - 960) / 2, yb + 4, 960, 30); el("note2", (W - 900) / 2, yb + 50, 900, 22)

    ly = H - FOOT - 27 - 56
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); el("logo", 27, ly, 320, 56)
    cx, cw, ch2 = W - 27 - 380, 380, 70; cy = H - FOOT - 13 - ch2
    el("cta", cx, cy, cw, ch2)
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch2}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                 f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:32px;color:{INK}">TURN UP EARLY</div>')
    for lab, x, yy, sz in (("star_tl", 44, 56 + OY, 100), ("star_tr", 936, 66 + OY, 100)):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = sz * im.height / im.width; el(lab, x, yy, sz, hh)
        parts.append(f'<img src="{src}" class="measure" data-tag="{lab}" style="position:absolute;left:{x}px;top:{yy}px;width:{sz}px;height:{hh}px;z-index:5">')

    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("card", INK, CTA_FILL, 33, True),
                  ("chip", INK, ORCHID, 20, True), ("daycol", INK, ORCHID, 58, True), ("note", WHITE, GROUND, 24, False), ("cta", INK, CTA_FILL, 32, True)]
    out = "out/collaterals/stories/terrathon_schedule_story.png" if story else "out/collaterals/terrathon_schedule.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    async with B.session():
        await B.render(html, out, W, H, elements=els, text_pairs=text_pairs,
                       containers=("card0", "card1", "card2"), page_bg=GROUND, expect_hero=False, margin=12)
    print("done", out)

import sys
asyncio.run(main(story="story" in sys.argv[1:]))
