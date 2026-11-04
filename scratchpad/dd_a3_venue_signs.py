"""DISCO DIWALI A3 VENUE SIGNAGE SET (2026-11-04). The user's list, every page A3 at 300 dpi, on the approved stall-sign system
(dd_a3_event_signs.Sign: beaded celestial ground, string lights, LIVE badge, copper mask + stickers, gold-rule credit line):

  01 main sign            street / building gate   landscape  lockup, edition, date + time, "on the rooftop"
  02-07 direction signs   LIFT and STAIRS, each with a left, right and up arrow (drawn, not a font glyph, so it prints the same everywhere)
  08 lift lobby queue     "keep your ticket QR ready"
  09 charity banner       "every rupee goes to charity"
  10 photo booth sign     portrait
  11-13 registration lane signs 1, 2, 3   portrait
  14-15 table tents       SCAN HERE / FORM LOOKUP: A3 landscape folded across the middle into a tent, so the top half is printed upside down
                          and both faces read the right way up once folded. A dashed fold line is printed on the fold.

Facts printed are only supplied ones: the edition, 10th November, 4:30 PM onwards, the rooftop (user, 2026-10-19), "all for charity".
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_a3_venue_signs.py
"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_a3_event_signs as E   # noqa: E402
dd, B, CP, Sign, GOLD, COPPER = E.dd, E.B, E.CP, E.Sign, E.GOLD, E.COPPER
OUT = os.path.join(E.ROOT, "out", "discodiwali", "print_a3_venue")
LW, LH = 1527, 1080


def arrow(size, deg):
    """A bold gold arrow, pointing right at deg=0; rotation baked into the svg."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 200 200" style="display:block;overflow:visible">'
            f'<g transform="rotate({deg} 100 100)"><path d="M20 78 H112 V34 L184 100 L112 166 V122 H20 Z" fill="{GOLD}" stroke="#000" stroke-width="8" stroke-linejoin="round"'
            f' style="filter:drop-shadow(0 6px 10px rgba(0,0,0,.7))"/></g></svg>')


def main_sign():
    s = Sign(LW, LH); s.badge()
    s.mask(1150, 40, 320, 14)
    s.sticker("st_star", "star", 50, 470, 200, -12)
    s.sticker("st_diya", "diya", 1250, 520, 230, 6)
    end = s.lockup(763, 190, 740)
    y = s.text("edition", E.EDITION, end + 26, 46, stroke=3, x=330, w=867) + 34
    y = s.text("when", "10th November &middot; 4:30 PM onwards", y, 50, color=GOLD, x=300, w=927) + 26
    s.text("where", "On the rooftop", y, 40, stroke=3, x=430, w=667)
    s.credit()
    return s


def direction_sign(word, deg):
    s = Sign(LW, LH); s.badge()
    s.mask(1180, 50, 270, 14)
    end = s.lockup(763, 120, 400)
    row_y, a = end + 110, 280
    ws = 220 if word == "Lift" else 200
    tw = round(ws * (2.2 if word == "Lift" else 3.55))          # measured-by-eye widths of LIFT / STAIRS in NeutralFace 700, checked on the render
    gap = 50; total = a + gap + tw; x0 = (LW - total) // 2
    if deg == 0:      # arrow after the word
        tx, ax = x0, x0 + tw + gap
    else:
        ax, tx = x0, x0 + a + gap
    s.add("arrow", ax, row_y + (ws - a) // 2, a, a, arrow(a, deg), z=21)
    s.text("word", word, row_y, ws, x=tx - 20, w=tw + 40)
    s.text("to", "To Disco Diwali &middot; Rooftop", row_y + ws + 70, 46, color=GOLD, x=330, w=867)
    s.sticker("st_l", "star", 50, 820, 150, -12)
    s.sticker("st_r", "heart", 1330, 820, 150, 10)
    s.credit()
    return s


def queue_sign():
    s = Sign(LW, LH); s.badge()
    s.mask(1180, 50, 270, 14)
    s.sticker("st_l", "star", 50, 800, 170, -12)
    s.sticker("st_r", "diya", 1290, 830, 190, 6)
    end = s.lockup(763, 140, 440)
    y = s.text("l1", "Please keep your", end + 70, 96) + 24
    y = s.text("l2", f'<span style="color:{GOLD}">ticket QR</span> ready', y, 112) + 46
    s.text("l3", "Open it on your phone before you reach the desk", y, 38, stroke=3, x=200, w=1127)
    s.credit()
    return s


def charity_banner():
    s = Sign(LW, LH); s.badge()
    s.mask(1180, 50, 270, 14)
    s.sticker("st_heart", "heart", 60, 760, 220, -10)
    s.sticker("st_diya", "diya", 1250, 790, 230, 6)
    end = s.lockup(763, 130, 400)
    y = s.text("l1", "Every rupee", end + 80, 124) + 24
    s.text("l2", f'goes to <span style="color:{GOLD}">charity</span>', y, 124)
    s.credit()
    return s


def photobooth_sign():
    s = Sign(1080, 1527); s.badge()
    s.mask(780, 40, 250, 14)
    s.sticker("st_cam", "camera", 400, 250, 280, -8)
    y = s.text("l1", "Photo", 560, 200) + 20
    y = s.text("l2", "Booth", y, 200) + 50
    end = s.lockup(540, y, 400)
    s.text("edition", E.EDITION, end + 24, 40, stroke=3)
    s.sticker("st_l", "star", 40, 1040, 150, -12)
    s.sticker("st_r", "heart", 890, 1040, 150, 10)
    s.credit()
    return s


def lane_sign(n):
    s = Sign(1080, 1527); s.badge()
    s.mask(780, 40, 250, 14)
    end = s.lockup(540, 300, 440)
    y = s.text("eyebrow", "Registration", end + 60, 64, color=GOLD, ls=.08) + 30
    y = s.text("lane", "Lane", y, 150) + 10
    s.text("num", str(n), y, 560, stroke=8, h=560, x=290, w=500)
    s.sticker("st_l", "star", 40, 1270, 150, -12)
    s.sticker("st_r", "diya", 890, 1240, 150, 6)
    s.credit()
    return s


def tent(word, sub):
    """A3 landscape folded at y=540 into a tent: two identical faces, the top one rotated 180 degrees."""
    s = Sign(LW, LH)
    lw = 340; t = lw / 1717; ly = 50; wy = ly + round(991 * t) + 28
    def face(tag):
        return (f'<div style="position:absolute;left:0;top:0;width:{LW}px;height:540px">'
                f'<img src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(763 - lw / 2 - 265 * t)}px;top:{round(ly - 320 * t)}px;width:{round(2000 * t)}px">'
                f'<div style="position:absolute;left:0;width:{LW}px;top:{wy}px;text-align:center;font-family:var(--d);font-weight:700;font-size:120px;line-height:1;'
                f'text-transform:uppercase;white-space:nowrap;color:#fff;-webkit-text-stroke:5px #000;paint-order:stroke fill;text-shadow:0 3px 14px rgba(0,0,0,.8)">{word}</div>'
                f'<div style="position:absolute;left:0;width:{LW}px;top:{wy + 140}px;text-align:center;font-family:var(--d);font-weight:700;font-size:36px;line-height:1;'
                f'text-transform:uppercase;white-space:nowrap;color:{GOLD};text-shadow:0 3px 14px rgba(0,0,0,.8)">{sub}</div></div>')
    s.add("top_face", 0, 0, LW, 540, f'<div style="position:relative;height:540px;transform:rotate(180deg)">{face("t")}</div>', z=20)
    s.add("bot_face", 0, 540, LW, 540, f'<div style="position:relative;height:540px">{face("b")}</div>', z=20)
    s.parts.append(f'<div data-tag="fold" style="position:absolute;left:0;top:539px;width:{LW}px;height:0;border-top:2px dashed rgba(201,151,28,.8);z-index:22"></div>')
    return s


PAGES = [("01_main_gate", main_sign)]
for word in ("Lift", "Stairs"):
    for tag, deg in (("left", 180), ("right", 0), ("up", -90)):
        PAGES.append((f"0{len(PAGES) + 1}_{word.lower()}_{tag}", lambda w=word, d=deg: direction_sign(w, d)))
PAGES += [("08_lift_queue", queue_sign), ("09_charity", charity_banner), ("10_photobooth", photobooth_sign)]
PAGES += [(f"{11 + i}_lane_{i + 1}", lambda n=i + 1: lane_sign(n)) for i in range(3)]
PAGES += [("14_tent_scan_here", lambda: tent("Scan here", "Show your ticket QR")),
          ("15_tent_form_lookup", lambda: tent("Form lookup", "No QR? We&rsquo;ll find your registration"))]


async def main():
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    only = os.environ.get("ONLY")
    pages = []
    async with B.session(scale=E.SCALE):
        for name, build in PAGES:
            if only and only not in name:
                continue
            s = build()
            png = os.path.join(OUT, f"{name}_a3.png")
            print(f"--- {name}")
            await B.render(B.page(s.W, s.H, "#000", "".join(s.parts), grain=False), png, s.W, s.H, elements=s.els, bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", collision_ignore=[("top_face", "bot_face")],
                           text_pairs=[("text", "#fff", "#000", 38, True), ("gold", GOLD, "#000", 40, True), ("credit", "#fff", "#000", 28, True)])
            im = Image.open(png).convert("RGB"); im.save(os.path.join(OUT, f"{name}_a3.pdf"), "PDF", resolution=300); pages.append(im)
    print("venue signs done ->", OUT, len(pages), "pages")
asyncio.run(main())
