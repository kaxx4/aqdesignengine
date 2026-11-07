"""DISCO DIWALI A3 EVENT SIGNAGE (2026-11-04): the three Summer Sunset print signs the user supplied, rebuilt in Disco Diwali branding.

  title    A3 landscape  - reference: big event title with "AQ's 5th anniversary party" over it  -> the Disco Diwali lockup as hero, the edition line under it
  ticket   A3 landscape  - reference: title small on top, "PLEASE KEEP YOUR TICKET ID NUMBER READY! (SENT WITH CONFIRMATION TEXT AS AP-XXXX)"
  welcome  A3 portrait   - reference: "WELCOME / TO / <title> / 2ND FLOOR ->"

Same system as the stall signs (dd_a3_print.py, approved by the user): beaded celestial ground, string lights, LIVE badge top left, copper stickers
(the mask, the brand's own hero object, plus the sticker set), white display type with a black stroke, and the gold-rule
"BROUGHT TO YOU BY TEAM AQUATERRA" credit line in place of the reference's cream pill (the user rejected the pill as off-brand).

Copy is the user's reference copy. Two values are the user's to confirm and live at the top of this file:
  TICKET_FMT  the reference printed AP-XXXX; the user set Disco Diwali's format to DD26-XXXX (2026-11-07)
  DIRECTION   the reference printed 2ND FLOOR ->; the venue is a rooftop (user, 2026-10-19), the arrow's direction depends on where the sign hangs
300 dpi at A3: scale 3.25 on 1527x1080 / 1080x1527 CSS px. sRGB, no bleed.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_a3_event_signs.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_copper as CP   # noqa: E402
import dd_ground as G    # noqa: E402

TICKET_FMT = "DD26-XXXX"
DIRECTION = "To the rooftop &rarr;"
EDITION = "Masquerade Sangeet Edition"
SCALE = 3.25
OUT = os.path.join(ROOT, "out", "discodiwali", "print_a3_event")
STROKE = "color:#fff;-webkit-text-stroke:{s}px #000;paint-order:stroke fill;"
GOLD, COPPER = dd.GOLD, "#E8955C"


def ground(W, H):
    return G.ground(dd, W, H)          # the blue diya ground (user, 2026-11-07), shared by every A3 sign: scratchpad/dd_ground.py


class Sign:
    def __init__(self, W, H):
        self.W, self.H, self.parts, self.els = W, H, [ground(W, H)], []

    def add(self, tag, x, y, w, h, html, z=20, declare=True):
        self.parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:{z}">{html}</div>')
        if declare:
            self.els.append((tag, x, y, w, h))

    def badge(self, bw=170):
        self.parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:48px;top:44px;width:{bw}px;z-index:20">')
        self.els.append(("badge", 48, 44, bw, round(bw * 1005 / 1061)))

    def mask(self, x, y, w, rot=12):
        h = round(w * 1278 / 1680)
        self.parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);'
                          f'filter:drop-shadow(0 14px 18px rgba(0,0,0,.7));z-index:14">')
        self.els.append(("mask", x, y, w, h))

    def sticker(self, tag, fn, x, y, s, rot):
        self.add(tag, x, y, s, s, getattr(CP, fn)(s, rot, u=tag[:2]), z=13)

    def lockup(self, cx, y, vw, tag="title"):
        """The title lockup WITH its ball; (cx, y) is the visible lockup's top centre, vw its visible width (1717 of the asset's 2000)."""
        t = vw / 1717; vh = round(991 * t); vx = round(cx - vw / 2)
        self.parts.append(f'<img data-tag="{tag}" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
        self.els.append((tag, vx, y, vw, vh))
        return y + vh

    def text(self, tag, txt, y, size, stroke=4, color=None, ls=0, x=0, w=None, h=None):
        w = self.W if w is None else w
        st = f"color:{color};" if color else STROKE.format(s=stroke)
        self.parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;width:{w}px;top:{y}px;text-align:center;font-family:var(--d);font-weight:700;font-size:{size}px;'
                          f'line-height:1;letter-spacing:{ls}em;text-transform:uppercase;white-space:nowrap;{st}text-shadow:0 3px 14px rgba(0,0,0,.8);z-index:20">{txt}</div>')
        self.els.append((tag, x + 40, y, w - 80, h or size))
        return y + (h or size)

    def credit(self):
        fy = self.H - 92
        rule = f'<span style="display:inline-block;width:150px;height:2px;background:{GOLD};vertical-align:middle"></span>'
        self.parts.append(f'<div data-tag="credit" style="position:absolute;left:0;width:{self.W}px;top:{fy}px;text-align:center;font-family:var(--d);font-weight:700;font-size:28px;line-height:1;'
                          f'letter-spacing:.12em;text-transform:uppercase;color:#fff;text-shadow:0 2px 10px #000,0 0 4px #000;z-index:20;white-space:nowrap">'
                          f'{rule}<span style="margin:0 26px;vertical-align:middle">Brought to you by Team AquaTerra</span>{rule}</div>')
        self.els.append(("credit", (self.W - 760) // 2, fy, 760, 30))
        return fy


def title_sign():
    s = Sign(1527, 1080); s.badge()
    s.mask(1150, 40, 320, 14)
    s.sticker("st_star", "star", 50, 430, 200, -12)
    s.sticker("st_diya", "diya", 1250, 470, 230, 6)
    y = s.text("edition_top", "AquaTerra presents", 210, 40, color=GOLD, ls=.14, x=380, w=767)
    end = s.lockup(763, y + 60, 860)
    s.text("edition", EDITION, end + 30, 52, stroke=3)
    s.credit()
    return s


def ticket_sign():
    s = Sign(1527, 1080); s.badge()
    s.mask(1180, 50, 280, 14)
    s.sticker("st_heart", "heart", 60, 790, 190, -10)
    s.sticker("st_star", "star", 1270, 780, 200, 10)
    end = s.lockup(763, 150, 470)
    y = end + 60
    y = s.text("l1", f'Please keep your <span style="color:{GOLD}">ticket ID</span>', y, 84) + 22
    y = s.text("l2", "number ready!", y, 84) + 44
    y = s.text("l3", f'(sent with confirmation text as <span style="color:{COPPER}">{TICKET_FMT}</span>)', y, 42, stroke=3)
    s.credit()
    return s


def welcome_sign():
    s = Sign(1080, 1527); s.badge()
    s.mask(780, 40, 250, 14)
    s.sticker("st_diya", "diya", 40, 1292, 140, -6)
    s.sticker("st_star", "star", 880, 1270, 160, 12)
    y = s.text("welcome", "Welcome", 300, 160) + 24
    y = s.text("to", "to", y, 88, x=390, w=300) + 46
    end = s.lockup(540, y, 700)
    y = s.text("edition", EDITION, end + 26, 44, stroke=3) + 70
    s.text("direction", DIRECTION, y, 74, color=GOLD)
    s.credit()
    return s


async def main():
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    async with B.session(scale=SCALE):
        for name, build in (("01_title", title_sign), ("02_ticket_id", ticket_sign), ("03_welcome", welcome_sign)):
            s = build()
            png = os.path.join(OUT, f"{name}_a3.png")
            await B.render(B.page(s.W, s.H, "#000", "".join(s.parts), grain=False), png, s.W, s.H, elements=s.els, bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", text_pairs=[("text", "#fff", "#000", 42, True), ("gold", GOLD, "#000", 40, True), ("credit", "#fff", "#000", 28, True)])
            im = Image.open(png).convert("RGB"); print(f"[{name}] {im.size}")
            im.save(os.path.join(OUT, f"{name}_a3.pdf"), "PDF", resolution=300)
    print("event signs done ->", OUT)
if __name__ == "__main__":
    asyncio.run(main())
