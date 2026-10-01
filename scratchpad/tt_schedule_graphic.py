"""TerraThon SCHEDULE calendar graphic for WhatsApp, 1080x1350 (4:5). The 'At a glance' timeline of web/terrathon/schedule.html as a poster.
Facts: only the live sport pages (report-by, match windows, venues, fees, prizes, age rule, ID) + the user's 'registrations close 1 Oct'.
Time scale is REAL: a block's height is its duration, so Saturday's cricket/FIFA overlap reads truthfully."""
import asyncio, importlib.util, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
H = 1350
GROUND, ORCHID, GREEN, BLUE, CREAM, INK, WHITE, PANEL = "#000000", tt.ORCHID, "#2FD284", "#0396FF", tt.CREAM_HALO, tt.INK, tt.WHITE, "#0d0d10"
H0, HOURS, PX_H = 9, 10, 72            # 9am to 7pm, 72px per hour
PANEL_TOP = 288
GRID_TOP = PANEL_TOP + 78 + 44 + 14      # day header, then the Mini-Fete banner row, then the hour grid
AX_X, COL_X, GAP = 40, 124, 12
COLW = [258, 340, 298]                   # Saturday is widest: two lanes (cricket + FIFA)
XS = [COL_X, COL_X + COLW[0] + GAP, COL_X + COLW[0] + COLW[1] + 2 * GAP]
DAYS = [("FRI 2 OCT", "PICKLEBALL", XS[0]), ("SAT 3 OCT", "CRICKET + FIFA", XS[1]), ("SUN 4 OCT", "CRICKET", XS[2])]

def y_of(hour): return GRID_TOP + (hour - H0) * PX_H

# (label, col, lane, start, end, colour, sport, window, venue, fee, prize, report_h, report_txt)
BLOCKS = [
    ("pb",  0, None, 12,   19, ORCHID, "PICKLEBALL", "12PM TO 7PM",     "11:11 PICK A COURT", "RS. 750 / TEAM OF 2", "RS. 5,000 PRIZE", 11.75, "REPORT 11:45"),
    ("cr1", 1, "a",  10,   16, GREEN,  "CRICKET",    "10AM TO 4PM",     "TURF XL",            "RS. 2,100 / TEAM",    "RS. 7,500 PRIZE", 9.75,  "REPORT 9:45"),
    ("fifa",1, "b",  11.5, 13.5, BLUE, "FIFA",       "11:30 TO 1:30",   "BATTLEGROUNDS",      "RS. 350 / SOLO",      "RS. 2,500 PRIZE", 11.25, "REPORT 11:15"),
    ("cr2", 2, None, 10,   14, GREEN,  "CRICKET",    "10AM TO 2PM",     "TURF XL",            "RS. 2,100 / TEAM",    "RS. 7,500 PRIZE", 9.75,  "REPORT 9:45"),
]

async def main():
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    def img(name, label, x, y, w, z=5):
        im, src = tt.crop_to_alpha(name); h = w * im.height / im.width; el(label, x, y, w, h)
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>', f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    m = await B.measure_text([dict(text="TERRATHON", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="THE SCHEDULE", font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 640 / m[0]["text_w"]; spx = 100 * min(0.72, 560 / m[1]["text_w"])
    parts.append(f'<div class="measure" data-tag="t1" style="position:absolute;left:{(W - 640) / 2}px;width:640px;top:{52 - .14 * tpx}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">TERRATHON</div>')
    parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 700) / 2}px;width:700px;top:{158}px;text-align:center;color:{ORCHID};font-family:SigmarOne;-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">THE SCHEDULE</div>')
    parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:250px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:400;font-size:30px;line-height:1;white-space:nowrap;z-index:6">2ND TO 4TH OCTOBER, 2026  |  KOLKATA</div>')
    el("t1", (W - 640) / 2, 54, 640, .7 * tpx); el("t2", (W - 560) / 2, 162, 560, spx * .8); el("t3", (W - 640) / 2, 252, 640, 26)

    # calendar panel
    px0, py0, pw, ph = 24, PANEL_TOP, W - 48, GRID_TOP - PANEL_TOP + HOURS * PX_H + 22
    el("panel", px0, py0, pw, ph)
    parts.append(f'<div class="measure" data-tag="panel" style="position:absolute;left:{px0}px;top:{py0}px;width:{pw}px;height:{ph}px;border:3px solid #2b2b33;border-radius:30px;background:{PANEL};z-index:2"></div>')
    for h in range(H0, H0 + HOURS + 1, 2):
        y = y_of(h); lab = f"{h if h <= 12 else h - 12}{'AM' if h < 12 else 'PM'}"
        parts.append(f'<div style="position:absolute;left:{AX_X}px;width:70px;text-align:right;top:{y - 11}px;font-family:var(--d);font-size:17px;color:#b9b9c2;line-height:1;z-index:4">{lab}</div>')
    for h in range(H0, H0 + HOURS + 1):
        parts.append(f'<div style="position:absolute;left:{COL_X - 6}px;width:{sum(COLW) + 2 * GAP + 12}px;top:{y_of(h)}px;border-top:1px solid #1f1f26;z-index:3"></div>')
    for ci, (name, sub, x) in enumerate(DAYS):
        parts.append(f'<div class="measure" data-tag="day{x}" style="position:absolute;left:{x}px;width:{COLW[ci]}px;top:{py0 + 18}px;font-family:var(--d);color:{WHITE};z-index:6;line-height:1"><div style="font-weight:900;font-size:30px">{name}</div><div style="font-weight:400;font-size:17px;color:#b9b9c2;margin-top:6px;letter-spacing:.04em">{sub}</div></div>')
        el(f"day{x}", x, py0 + 20, 250, 56)
        parts.append(f'<div style="position:absolute;left:{x - 6}px;top:{GRID_TOP}px;height:{HOURS * PX_H}px;border-left:2px dashed #2b2b33;z-index:3"></div>')

    for ci in (1, 2):
        x, w = XS[ci], COLW[ci] - 8
        by = py0 + 78
        el(f"mf{ci}", x, by, w, 44)
        parts.append(f'<div class="measure" data-tag="mf{ci}" style="position:absolute;left:{x}px;top:{by}px;width:{w}px;height:44px;border:4px solid {ORCHID};border-radius:999px;background:{tt.CTA_FILL};color:{INK};display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:17px;white-space:nowrap;z-index:6">MINI-FETE  |  TURF XL</div>')
    for lab, col, lane, s, e, colr, sport, win, ven, fee, prize, rep_h, rep_txt in BLOCKS:
        cx = DAYS[col][2]; half = lane is not None; cw = COLW[col] - 8
        w = (cw - 8) / 2 if half else cw
        x = cx + (0 if lane != "b" else (cw - 8) / 2 + 8)
        y = y_of(s) + 2; h = (e - s) * PX_H - 4
        ry = y_of(rep_h)
        # report-by marker: dotted line + label, kept inside the block's lane
        parts.append(f'<div style="position:absolute;left:{x}px;width:{w}px;top:{ry}px;border-top:3px dotted {CREAM};z-index:5"></div>')
        parts.append(f'<div class="measure" data-tag="{lab}_rep" style="position:absolute;left:{x}px;top:{ry - 26}px;font-family:var(--d);font-size:{15 if half else 17}px;color:{CREAM};background:{PANEL};padding:0 6px 0 0;line-height:1;white-space:nowrap;z-index:6">{rep_txt}</div>')
        el(f"{lab}_rep", x, ry - 24, 120 if half else 150, 18)
        big, small = (34, 19) if not half else (25, 15)
        body = f'<div style="font-weight:900;font-size:{big}px;line-height:1;white-space:nowrap">{sport}</div><div style="font-weight:400;font-size:{small}px;line-height:1.2;margin-top:8px;white-space:nowrap">{win}</div><div style="font-weight:400;font-size:{small}px;line-height:1.2;margin-top:4px;white-space:nowrap">{ven}</div>'
        if h > 150:
            body += f'<div style="margin-top:auto;font-weight:900;font-size:{small}px;line-height:1.25;white-space:nowrap">{fee}<br>{prize}</div>'
        else:
            body += f'<div style="margin-top:auto;font-weight:900;font-size:{small}px;line-height:1.25;white-space:nowrap">{fee}<br>{prize}</div>'
        el(lab, x, y, w, h)
        parts.append(f'<div class="measure" data-tag="{lab}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:22px;border:4px solid {CREAM};background:{colr};color:{INK};padding:{12 if not half else 9}px {14 if not half else 9}px;display:flex;flex-direction:column;overflow:hidden;font-family:var(--d);z-index:5">{body}</div>')

    # footer
    fy = py0 + ph + 22
    parts.append(f'<div class="measure" data-tag="note1" style="position:absolute;left:40px;width:{W - 80}px;top:{fy}px;text-align:center;color:{WHITE};font-family:var(--d);font-weight:900;font-size:22px;line-height:1;white-space:nowrap;z-index:6">MINI-FETE: 3RD + 4TH OCT, TURF XL. OPEN TO ALL. ALL FOR CHARITY.</div>')
    n2 = "REPORT BY THE TIME SHOWN. CARRY YOUR SCHOOL OR COLLEGE ID. BORN ON OR AFTER 1 JAN 2005."
    nm = await B.measure_text([dict(text=n2, font="d", size=100, weight=400)]); n2fs = min(20, 100 * 980 / nm[0]["text_w"])
    parts.append(f'<div class="measure" data-tag="note2" style="position:absolute;left:40px;width:{W - 80}px;top:{fy + 36}px;text-align:center;color:#b9b9c2;font-family:var(--d);font-weight:400;font-size:{n2fs}px;line-height:1;white-space:nowrap;z-index:6">{n2}</div>')
    el("note1", 40, fy, W - 80, 24); el("note2", 40, fy + 36, W - 80, 22)
    ly = 1350 - 26 - 56
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); el("logo", 27, ly, 320, 56)
    cm = await B.measure_text([dict(text="REGISTER AT NGOAQUATERRA.COM/TERRATHON", font="d", size=100, weight=900)])
    cfs = min(26, 100 * 590 / cm[0]["text_w"]); cwid = 640
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{W - 27 - cwid}px;top:{ly - 4}px;width:{cwid}px;height:64px;border:6px solid {ORCHID};border-radius:999px;background:{tt.CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:{cfs}px;white-space:nowrap;color:{INK}">REGISTER AT NGOAQUATERRA.COM/TERRATHON</div>'); el("cta", W - 27 - cwid, ly - 4, cwid, 64)
    parts.append(img("shuriken.png", "star_l", 32, 60, 96) + img("shuriken.png", "star_r", 952, 84, 96))

    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    tp = [("head", WHITE, GROUND, 96, True), ("small", WHITE, GROUND, 22, False), ("cta", INK, tt.CTA_FILL, 24, True),
          ("pb", INK, ORCHID, 19, False), ("cr", INK, GREEN, 19, False), ("fifa", INK, BLUE, 16, False)]
    os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        inside = {("panel", l) for l, *_ in els if l != "panel"}
        await B.render(html, "out/collaterals/schedule_calendar_whatsapp.png", W, H, elements=els, text_pairs=tp, containers=("panel",), page_bg=GROUND, expect_hero=True, margin=12, collision_ignore=inside)
    print("done")
asyncio.run(main())
