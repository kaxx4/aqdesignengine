"""HOW EVENTS MAKE THE IMPACT: single feed post (1080x1350). Workflow C, bespoke.

Reuses the helper block of gen_why_we_do_v1.py (marks, logo pill, flecks, measured headline/body, shoot)
by exec'ing everything above its CAROUSEL marker, so the two pieces cannot drift apart.

Mechanism: THE PARTY photo beside THE PROJECT photo with an arrow between, then the real money split.
Adaptations / honesty notes:
  * photos: dd_photos/dance.jpg (Disco Diwali) and the Sundarbans education frame, cropped above its baked caption.
  * money split is the revenue doc's: ~90% events (of which ~80% tickets, ~20% sponsors), ~10% ROOTS, 0% donations.
    The bar shows events 90 / ROOTS 10 and states the 80/20 inside events as text; no derived percentages.
  * outcome numbers are AQ_FACTS figures (500+ projects, 3,500+ children, 25,000+ hours), scoped, not tied to a
    ticket-to-outcome conversion, because no such figure exists.
  * 4 accents on a black ground (sky, grape, mint, cream). The recipe count is a target; sky is the events hue by rule.
"""
import os, sys, asyncio
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
OUT = "out/events_impact"; os.makedirs(OUT, exist_ok=True)
DANCE = b64("engine/assets/terrathon/dd_photos/dance.jpg")
W, H = 1080, 1350

def pill_chip(txt, x, y, w, h=40):
    return (f'<div data-tag="chip" style="position:absolute;left:{x}px;top:{y}px;height:{h}px;padding:0 18px;border-radius:999px;background:{CREAM};'
            f'color:{BLACK};font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.08em;display:flex;align-items:center;white-space:nowrap;z-index:12">{txt}</div>')

async def main():
    async with B.session():
        lp, lbox = logo_pill()
        # ---- photo pair ----
        LW, GUT, RW, PH_H = 628, 16, 436, 600
        left = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{LW}px;height:{PH_H}px;overflow:hidden;z-index:2">'
                f'<img src="{DANCE}" style="width:100%;height:100%;object-fit:cover;object-position:42% 40%"></div>')
        right = (f'<div data-tag="photo" style="position:absolute;left:{LW + GUT}px;top:0;width:{RW}px;height:{PH_H}px;overflow:hidden;z-index:2">'
                 f'<img src="{PH["edu"]}" style="position:absolute;left:-120px;top:-130px;width:670px;height:837px"></div>')
        c1 = pill_chip("THE PARTY", 24, PH_H - 64, 150); c2 = pill_chip("THE PROJECT", LW + GUT + 24, PH_H - 64, 190)
        badge = (f'<div data-tag="badge" style="position:absolute;left:{LW + GUT // 2 - 56}px;top:244px;width:112px;height:112px;border-radius:50%;background:{MINT_B};'
                 f'border:6px solid {BLACK};display:flex;align-items:center;justify-content:center;z-index:14">'
                 f'<svg width="60" height="60" viewBox="0 0 60 60"><path d="M8 30 H46 M32 14 L48 30 L32 46" fill="none" stroke="{BLACK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
        els = [("logo", *lbox), ("photo", 0, 0, LW, PH_H), ("photo", LW + GUT, 0, RW, PH_H),
               ("chipL", 24, PH_H - 64, 150, 40), ("chipR", LW + GUT + 24, PH_H - 64, 190, 40), ("badge", LW + GUT // 2 - 56, 244, 112, 112)]

        # ---- headline ----
        lines = [("THE DANCE FLOOR", "THE DANCE FLOOR"), ("FUNDS THE FIELD WORK.", mark("FUNDS THE FIELD WORK."))]
        h, he, yb, s = await headline(lines, 88, M, 650, W - 2 * M - 30)
        els += he

        # ---- event pills ----
        names = ["PARADOX", "DISCO DIWALI", "STARRY NIGHT", "TERRATHON"]
        ms = await B.measure_text([dict(text=n, font="m", size=16, weight=700, letter_spacing=1.6) for n in names])
        px = M; py = yb + 22; pills = ""
        for n, m in zip(names, ms):
            w = int(m["text_w"]) + 36
            pills += (f'<div data-tag="pill" style="position:absolute;left:{px}px;top:{py}px;height:38px;width:{w}px;border:2px solid {CREAM};border-radius:999px;color:{CREAM};'
                      f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.1em;display:flex;align-items:center;justify-content:center;white-space:nowrap;z-index:10">{n}</div>')
            els.append((f"pill_{n}", px, py, w, 38)); px += w + 14

        # ---- the real money split ----
        by = py + 38 + 74
        lab = (f'<div style="position:absolute;left:{M}px;top:{by - 34}px;font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;color:{MINT_B};z-index:10;white-space:nowrap">'
               f'WHERE AQ&#39;S MONEY COMES FROM</div>')
        els.append(("barlab", M, by - 34, 420, 22))
        BW = W - 2 * M; w1 = round(BW * .9)
        bar = (f'<div data-tag="bar" style="position:absolute;left:{M}px;top:{by}px;width:{BW}px;height:64px;border-radius:14px;overflow:hidden;display:flex;z-index:10">'
               f'<div style="width:{w1}px;background:{A[4]};color:{BLACK};font-family:var(--d);font-weight:900;font-size:30px;display:flex;align-items:center;padding-left:24px;white-space:nowrap">EVENTS ~90%</div>'
               f'<div style="flex:1;background:{A[5]}"></div></div>')
        els.append(("bar", M, by, BW, 64))
        rl = (f'<div style="position:absolute;right:{M}px;top:{by + 72}px;font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.08em;color:{core.on_dark(A[5], 15)};z-index:10;white-space:nowrap">ROOTS (CLOTHING BRAND) ~10%</div>')
        els.append(("rootslab", W - M - 262, by + 72, 262, 20))
        cap, cape, cy = await body(["of event money, ~80% is tickets and ~20% sponsors.", "0% is individual donations. students earn what they give."], 26, M, by + 76, lh=1.32, tag="cap")
        els += cape

        # ---- what it funded ----
        fy = cy + 38
        lead = (f'<div style="position:absolute;left:{M}px;top:{fy}px;font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;color:{MINT_B};z-index:10;white-space:nowrap">'
                f'WHAT THAT HAS FUNDED SO FAR</div>')
        els.append(("lead", M, fy, 420, 22))
        stats = [("500+", "projects since june 2021", A[0]), ("3,500+", "children, through workshops", A[2]), ("25,000+", "volunteer hours, logged", MINT_B)]
        sm = await B.measure_text([dict(text=n, font="d", size=70, weight=900) for n, _, _ in stats])
        sx = M; sh = ""; colw = (W - 2 * M) // 3
        for (n, l, col), m in zip(stats, sm):
            sh += (f'<div data-tag="num" style="position:absolute;left:{sx}px;top:{fy + 32}px;font-family:var(--d);font-weight:900;font-size:70px;line-height:.9;color:{col};white-space:nowrap;z-index:10">{n}</div>'
                   f'<div data-tag="lab" style="position:absolute;left:{sx}px;top:{fy + 32 + 70}px;font-family:var(--e);font-size:21px;color:{CREAM};white-space:nowrap;z-index:10">{l}</div>')
            els += [(f"s_{n}", sx, fy + 32, m["text_w"], 63), (f"sl_{n}", sx, fy + 102, colw - 14, 28)]
            sx += colw
        f, fe = foot(W, H, right="")
        els += fe
        tp = TP + [("bar", BLACK, A[4], 30, True), ("pill", CREAM, BLACK, 16, True), ("chip", BLACK, CREAM, 17, True), ("roots", core.on_dark(A[5], 15), BLACK, 15, True)]
        await shoot("events_impact", W, H, wrap(W, H, 31, left, right, lp, c1, c2, badge, h, pills, lab, bar, rl, cap, lead, sh, f), els, tp)

asyncio.run(main())
