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


def diya_ground(H):
    """The approved blue diya ground (brain/DISCO_DIWALI.md, user 2026-10-14 'i want this blue effect'): black, navy and gold lotus-diya corners fading to black, string lights, gold dust, grain.
    A story stacks TWO plates, the second flipped and faded in, so all four corners carry the pattern (engine format rule 8)."""
    P = ['<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>',
         f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{min(H, dd.BASE_H)}px;object-fit:cover;z-index:1">']
    if H > dd.BASE_H:
        P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - dd.BASE_H}px;width:{W}px;height:{dd.BASE_H}px;object-fit:cover;z-index:1;'
                 'transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%)">')
    P += [f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:170px;top:-40px;width:1100px;z-index:5">',
          f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">',
          f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">']
    return "".join(P)


async def build(H):
    story = H > 1350
    s = Sign(W, H); s.parts = [diya_ground(H)]
    top = 210 if story else 44
    s.parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:{top}px;width:170px;z-index:20">')
    s.els.append(("badge", 40, top, 170, round(170 * 1005 / 1061)))
    s.mask(760, top + 8, 250, 12)
    pw = 1000; px = (W - pw) // 2
    f_sp = await fit("Special", 560, 150); f_inv = await fit("Invitation", pw - 90, 240); f3 = await fit("Rs. 550", pw - 90, 340); fl = 54
    pad = 34; gap = 8
    py = (440 if story else 250)
    room = (790 if story else 745)                             # panel height available: the fee takes what the invitation lines leave
    f3 = min(f3, room - 2 * pad - f_sp - f_inv - fl - 3 * gap)
    ph = pad + f_sp + gap + f_inv + gap + fl + gap + f3 + pad
    print(f"   sizes: special {f_sp}, invitation {f_inv}, label {fl}, fee {f3}; panel {ph}px")
    s.add("panel", px, py, pw, ph, f'<div style="height:{ph}px;border-radius:34px;border:6px solid {GOLD};box-sizing:border-box;background:rgba(0,0,0,.62);box-shadow:0 0 40px rgba(201,151,28,.35),0 16px 40px rgba(0,0,0,.6)"></div>', z=15, declare=False)
    s.els.append(("panel", px, py, pw, ph))
    y = s.text("invite1", "Special", py + pad, f_sp, color=GOLD, x=px, w=pw)
    y = s.text("invite2", "Invitation", y + gap, f_inv, color=GOLD, x=px, w=pw)
    y = s.text("label", "Entry", y + gap, fl, x=px, w=pw, stroke=4, ls=.25)
    y = s.text("fee", "Rs. 550", y + gap, f3, x=px, w=pw, stroke=6)
    iy = py + ph + (50 if story else 24)
    y = s.text("when", "10th November, 2026", iy, 52 if story else 46, stroke=3) + 10
    y = s.text("clock", "4:30 PM onwards", y, 42 if story else 38, stroke=3) + 8
    y = s.text("venue", "60, Chowringhee Banquets", y, 38 if story else 34, stroke=3)
    vw = 240 if story else 190; ly = (1450 if story else 1158)
    end = s.lockup(W // 2, ly, vw)
    s.text("edition", E.EDITION, end + 8, 24 if story else 20, stroke=2, ls=.04)
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
