"""TerraThon x DISCO DIWALI TICKETS, Rs. 550 (user, 2026-10-01: "a whatsapp graphic that gets your Disco Diwali tickets at 550 at TerraThon cricket Turf XL, and 5 story designs").
`wa`      -> the WhatsApp graphic (feed 4:5 1080x1350), the existing sticker-first DD ticket design (tt_dd_tickets.py: disco ball, diya, ticket) re-copied: GET YOUR TICKETS / DISCO DIWALI / RS. 550 / AT TERRATHON CRICKET / 3RD & 4TH OCT / TURF XL / DD TICKET STALL.
`stories` -> five 1080x1920 story designs: 1 hero disco ball + price, 2 giant price + ticket, 3 where (real DD photo, venue, dates), 4 the night (two real DD photos + diya), 5 want them free? (the Disco Dash tie-in).
Facts: price Rs. 550 (user); the DD ticket stall is at the Mini-Fete, 3rd + 4th Oct 2026, Turf XL, New Alipore (earlier user brief); "at TerraThon cricket Turf XL" is read as the tickets being sold at Turf XL on the TerraThon cricket days, which is where that stall is.
Disco Diwali's OWN date/venue were never supplied and are NOT printed. Photos: the user's three Disco Diwali images (engine/assets/terrathon/dd_photos/), no event date claimed. Story 5 repeats the Disco Dash rule (first 5 finishers win free tickets).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_tickets_set.py [wa|stories]   (default: both)
"""
import asyncio, base64, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = True     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = 1920, 5
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/minigames"
DDP = "engine/assets/terrathon/dd_photos"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


PH = {n: b64(f"{DDP}/{n}.jpg", "image/jpeg") for n in ("decor", "group", "dance")}


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


class Slide:
    def __init__(self, idx, seed):
        self.idx, self.els, self.parts = idx, [], []
        rnd = random.Random(seed)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
        self.parts += [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
                       f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    def el(self, l, x, y, w, h): self.els.append((l, x, y, w, h))
    def add(self, html): self.parts.append(html)

    async def title(self, big, sub, big_w=780, sub_w=800, top=100):
        top += OY
        big = re.sub(r'([A-Z])(?=\1)', '\\1\u200c', big).replace("'", "\u2019")   # ZWNJ stops StretchPro's doubled-letter ligature (LL, EE) from stretching
        m = await B.measure_text([dict(text=big, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                                  dict(text=sub, font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        tpx = 100 * big_w / m[0]["text_w"]; spx = 50 * min(1.0, sub_w / m[1]["text_w"])
        self.text("t1", "TERRATHON", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
        self.add(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - big_w - 20) / 2}px;width:{big_w + 20}px;top:{top}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{big}</div>')
        self.el("t2", (W - big_w) / 2, top + 4, big_w, tpx * .82)
        sy = top + tpx * 1.05
        self.add(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - sub_w - 20) / 2}px;width:{sub_w + 20}px;top:{sy}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">{sub}</div>')
        self.el("t3", (W - sub_w) / 2, sy + 2, sub_w, spx * .82)
        return sy + spx + 20

    def text(self, tag, txt, x, y, w, size, weight=400, color=WHITE, align="center", z=6):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:{color};font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1.05;white-space:nowrap;z-index:{z}">{txt}</div>')
        self.el(tag, x, y, w, size * .85)

    def star(self, tag, x, y, size=104, z=8):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = size * im.height / im.width
        self.add(f'<img src="{src}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{hh}px;z-index:{z}">'); self.el(tag, x, y, size, hh)

    def logo_badge(self, tag, x, y, size, ring=10, z=9):
        self.add(f'<img class="measure" data-tag="{tag}" src="{LOGO}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;box-sizing:border-box;border:{ring}px solid {ORCHID};z-index:{z}">'); self.el(tag, x, y, size, size)

    def chip(self, tag, txt, x, y, w, deg=-3, size=40, z=9):
        h = size + 40
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:6px solid {ORCHID};border-radius:999px;'
                 f'background:{CTA_FILL};display:flex;align-items:center;justify-content:center;white-space:nowrap;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;color:{INK};z-index:{z}">{txt}</div>')
        self.el(tag, *rb(x, y, w, h, deg))

    def frame(self, tag, src, x, y, w, h, deg, pos="50% 50%", z=4):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:{z}">'
                 f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>'); self.el(tag, *rb(x, y, w, h, deg))

    def box(self, tag, x, y, w, h, inner, pad="16px 22px"):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:32px;background:{CTA_FILL};'
                 f'padding:{pad};color:{INK};font-family:var(--d);z-index:6;overflow:hidden">{inner}</div>'); self.el(tag, x, y, w, h)

    def footer(self, cta=None):
        ly = H - FOOT - 27 - 56
        self.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); self.el("logo", 27, ly, 320, 56)
        if cta:
            cw, chh = 480, 70; cx, cy = W - 27 - cw, H - FOOT - 13 - chh; self.el("cta", cx, cy, cw, chh)
            self.add(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:30px;color:{INK}">{cta}</div>')
        else:
            tw, th = 150, 50; tx, ty = W - 27 - tw, H - FOOT - 27 - th; self.el("idx", tx, ty, tw, th)
            self.add(f'<div class="measure" data-tag="idx" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:26px;color:{INK}">{self.idx:02d} / {TOTAL:02d}</div>')

    def html(self): return B.page(W, H, GROUND, "".join(self.parts), grain=False)


def head_row(chip, price=None, price_px=40):
    p = (f'<div style="background:{GREEN};color:{INK};font-weight:900;font-size:{price_px}px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{price}</div>' if price else "")
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:16px"><div style="background:{ORCHID};color:{INK};font-weight:900;font-size:30px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{chip}</div>{p}</div>')


def rows_html(rows, rh, size, price_col=False):
    out = ""
    for i, r in enumerate(rows):
        name, price = (r if isinstance(r, tuple) else (r, None))
        sep = f"border-top:3px solid rgba(10,10,10,.22);" if i else ""
        pr = (f'<div style="font-weight:900;font-size:{size}px;white-space:nowrap">{price}</div>' if price else "")
        out += f'<div style="height:{rh}px;{sep}display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:{size}px;line-height:1.08;font-weight:400"><div>{name}</div>{pr}</div>'
    return out


_s2 = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py")); ddm = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(ddm)
DK = "#0A0A0A"


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, x, y, w, h)


def slab(s, tag, x, y, w, h, deg=-1.25):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>'); s.el(tag, *rb(x, y, w, h, deg))


def rows_in(s, sx, sy, sw, sh, rows, tag="row"):
    tot = sum(z for _, z, _c in rows) + (len(rows) - 1) * 20; y = sy + (sh - tot) / 2 - 4
    for i, (txt, z, col) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="{tag}{i}" style="position:absolute;left:{sx + 36}px;width:{sw - 72}px;top:{y}px;text-align:center;color:{col};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>'); s.el(f"{tag}{i}", sx + 36, y, sw - 72, z * .85); y += z + 20
    return [("slab", f"{tag}{i}") for i in range(len(rows))]


async def build():
    out = []
    BOT = H - FOOT - 150
    # ---- 1 HERO: disco ball + price slab ----
    s = Slide(1, 401)
    ty = await s.title("DISCO DIWALI", "GET YOUR TICKETS", big_w=700, sub_w=700, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    bw = 700; ball, bh = ddm.disco_ball(bw, "b1"); svg_sticker(s, "ball", ball, (W - bw) / 2, ty + 10, bw, bh)
    sy = ty + 10 + bh + 30; sh = BOT - sy + 20
    slab(s, "slab", 100, sy, 880, sh)
    ign = rows_in(s, 100, sy, 880, sh, [("RS. 550", 120, INK), ("AT TERRATHON, TURF XL", 38, "#0E7C86")])
    s.footer(cta="DD TICKET STALL"); out.append(("1", s, ign + [("slab", "ball"), ("star_tl", "t1"), ("star_tr", "t1")]))
    # ---- 2 GIANT PRICE + ticket ----
    s = Slide(2, 402)
    ty = await s.title("RS. 550", "DISCO DIWALI TICKETS", big_w=740, sub_w=800, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    tw_ = 900; tk, tkh = ddm.ticket(tw_, "t2"); svg_sticker(s, "tkt", tk, (W - tw_) / 2, ty + 40, tw_, tkh, -7)
    dy_ = ty + 40 + tkh + 90
    dw = 330; dya, dyh = ddm.diya(dw, "d2"); svg_sticker(s, "diya", dya, 70, dy_, dw, dyh, -6)
    s.text("w1", "AT THE DD TICKET STALL", 430, dy_ + 20, 600, 38, 900, WHITE, align="left")
    s.text("w2", "TURF XL, NEW ALIPORE", 430, dy_ + 80, 600, 34, 400, WHITE, align="left")
    s.text("w3", "3RD + 4TH OCT", 430, dy_ + 130, 600, 36, 900, ORCHID, align="left")
    s.footer(cta="DD TICKET STALL"); out.append(("2", s, [("star_tl", "t1"), ("star_tr", "t1"), ("tkt", "t3")]))
    # ---- 3 WHERE: real DD photo + venue ----
    s = Slide(3, 403)
    ty = await s.title("FIND US", "AT TERRATHON CRICKET", big_w=620, sub_w=860, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    fh = int((BOT - ty) * 0.52); s.frame("frame", PH["decor"], 90, ty + 20, 900, fh, -2, "50% 55%")
    py_ = ty + 20 + fh + 50
    s.chip("c1", "DD TICKET STALL", 120, py_, 560, deg=-2, size=36)
    s.text("v1", "TURF XL, NEW ALIPORE", 40, py_ + 120, W - 80, 52, 900, WHITE)
    s.text("v2", "3RD + 4TH OCT", 40, py_ + 188, W - 80, 46, 900, ORCHID)
    s.text("v3", "RS. 550", 40, py_ + 252, W - 80, 54, 900, WHITE)
    s.footer(cta="DD TICKET STALL"); out.append(("3", s, [("star_tl", "t1"), ("star_tr", "t1"), ("frame", "c1")]))
    # ---- 4 THE NIGHT: two real DD photos ----
    s = Slide(4, 404)
    ty = await s.title("DISCO DIWALI", "BE THERE", big_w=700, sub_w=420, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    fh = int((BOT - ty) * 0.62)
    s.frame("f1", PH["dance"], 50, ty + 30, 560, fh, -4, "50% 45%", z=4); s.frame("f2", PH["group"], 470, ty + 30 + fh * 0.30, 560, int(fh * 0.78), 3.5, "50% 40%", z=5)
    dya, dyh = ddm.diya(260, "d4"); svg_sticker(s, "diya", dya, 70, ty + 30 + fh - 40, 260, dyh, -8, z=9)
    s.chip("c1", "TICKETS RS. 550", 330, ty + 30 + fh + 90, 560, deg=-2, size=40)
    s.footer(cta="DD TICKET STALL"); out.append(("4", s, [("star_tl", "t1"), ("star_tr", "t1"), ("f1", "f2"), ("f1", "diya"), ("f2", "diya"), ("f2", "c1"), ("f1", "c1"), ("diya", "c1"), ("f2", "star_tr")]))
    # ---- 5 WANT THEM FREE? ----
    s = Slide(5, 405)
    ty = await s.title("WANT THEM FREE?", "WIN THEM AT DISCO DASH", big_w=700, sub_w=780, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    tk, tkh = ddm.ticket(520, "t5"); svg_sticker(s, "tkt", tk, 40, ty + 30, 520, tkh, -9)
    ball, bh = ddm.disco_ball(440, "b5"); svg_sticker(s, "ball", ball, W - 40 - 440, ty + 20, 440, bh, 6)
    sy = ty + 30 + max(tkh, bh) + 60; sh = 360
    slab(s, "slab", 84, sy, 912, sh)
    ign = rows_in(s, 84, sy, 912, sh, [("FIRST 5 TO FINISH ALL 9", 46, INK), ("MINI-FETE GAMES WIN", 46, INK), ("FREE DISCO DIWALI TICKETS", 36, "#0E7C86")])
    s.chip("c1", "OR BUY AT RS. 550", 220, sy + sh + 60, 640, deg=-2, size=40)
    s.footer(cta="DD TICKET STALL"); out.append(("5", s, ign + [("slab", "tkt"), ("slab", "ball"), ("star_tl", "t1"), ("star_tr", "t1"), ("tkt", "ball")]))
    return out


async def stories():
    res = await build()
    outdir = "out/collaterals/stories"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 40, True), ("idx", INK, CTA_FILL, 26, True), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s, ign in res:
            out = f"{outdir}/dd_tickets_story_{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=False,
                           collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "f1", "f2"))
            print("done", out)


async def wa():
    c = dict(head=("GET YOUR TICKETS", "DISCO DIWALI"), price="RS. 550", tag="AT TERRATHON CRICKET", date="3RD & 4TH OCT", venue="TURF XL", cta="DD TICKET STALL")
    os.makedirs("out/collaterals", exist_ok=True)
    async with ddm.B.session():
        await ddm.build(c, "out/collaterals/dd_tickets_550_whatsapp.png")
    print("done out/collaterals/dd_tickets_550_whatsapp.png")


async def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("wa", "both"): await wa()
    if which in ("stories", "both"): await stories()

asyncio.run(main())
