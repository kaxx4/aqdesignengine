"""DISCO DIWALI "SPECIAL INVITATION" v2 (user, 2026-11-07: 'SPECIAL INVITATION and Rs.550 highlighted, reduce the Disco Diwali text and place it at the footer').
The invitation line and the fee are the hero: a gold-framed panel, SPECIAL INVITATION in gold, ENTRY label + a giant RS. 550 in white, both measured to fill the panel (v3: full-width panel, 'Entry' split off as a small label so the fee can run ~2x larger). The date, time and venue sit
under the panel. The lockup (with ball) is shrunk to a footer mark with the edition line beneath it. Built on the Sign primitives (beaded celestial ground, string lights, LIVE badge,
copper mask) at feed 1080x1350 and story 1080x1920 (top 200 and bottom 250 clear for Instagram's bars). Supplied facts only: 10th November 2026, 4:30 PM onwards, 60 Chowringhee
Banquets, Rs. 550 entry. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_invite2.py -> out/discodiwali/invite2/{feed,story}.png"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_a3_event_signs as E   # noqa: E402
dd, B, Sign, GOLD = E.dd, E.B, E.Sign, E.GOLD
OUT = os.path.join(E.ROOT, "out", "discodiwali", "invite2")
FEE = os.environ.get("FEE", "Entry Rs. 550")
W = 1080


async def fit(text, width, cap):
    m = await B.measure_text([dict(text=text.upper(), font="d", size=100, weight=700)], W=W, H=1350)
    return min(cap, int(100 * width / m[0]["text_w"]))


async def build(H):
    story = H > 1350
    s = Sign(W, H)
    top = 210 if story else 44
    s.parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:{top}px;width:170px;z-index:20">')
    s.els.append(("badge", 40, top, 170, round(170 * 1005 / 1061)))
    s.mask(700, top + 8, 320, 12)
    pw = 1000; px = (W - pw) // 2
    f1 = await fit("Special invitation", pw - 90, 140); f3 = await fit("Rs. 550", pw - 90, 340); fl = 60
    pad = 40; gap = 10
    ph = pad + f1 + gap + fl + gap + f3 + pad
    py = (520 if story else 330)
    s.add("panel", px, py, pw, ph, f'<div style="height:{ph}px;border-radius:34px;border:6px solid {GOLD};box-sizing:border-box;background:rgba(0,0,0,.62);box-shadow:0 0 40px rgba(201,151,28,.35),0 16px 40px rgba(0,0,0,.6)"></div>', z=15, declare=False)
    s.els.append(("panel", px, py, pw, ph))
    y = s.text("invite", "Special invitation", py + pad, f1, color=GOLD, x=px, w=pw)
    y = s.text("label", "Entry", y + gap, fl, x=px, w=pw, stroke=4, ls=.25)
    y = s.text("fee", "Rs. 550", y + gap, f3, x=px, w=pw, stroke=6)
    iy = py + ph + (60 if story else 34)
    y = s.text("when", "10th November, 2026", iy, 56 if story else 50, stroke=3) + 12
    y = s.text("clock", "4:30 PM onwards", y, 46 if story else 40, stroke=3) + 10
    y = s.text("venue", "60, Chowringhee Banquets", y, 42 if story else 36, stroke=3)
    vw = 270 if story else 220; ly = (1440 if story else 1128)
    end = s.lockup(W // 2, ly, vw)
    s.text("edition", E.EDITION, end + 10, 26 if story else 22, stroke=2, ls=.04)
    return s, (y, ly)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            s, (info_end, ly) = await build(H)
            print(f"[{name}] info ends y={info_end}, lockup starts y={ly}")
            await B.render(B.page(W, H, "#000", "".join(s.parts), grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=s.els, bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", containers=("panel",), text_pairs=[("text", "#fff", "#000", 40, True), ("gold", GOLD, "#000", 80, True)])
    print("done ->", OUT)
asyncio.run(main())
