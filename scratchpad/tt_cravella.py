"""TerraThon x CRAVE'LLA stall carousel (6 slides, feed 1080x1350): introduces the stall as OUR DESSERT PARTNER and shows its Mini-Fete menu.
Real assets only (user, 2026-10-01): logo + two photos, copied to engine/assets/terrathon/partners/cravella/ (logo masked to a circle).
Facts: stall at the TerraThon Mini-Fete, 3rd and 4th Oct 2026, Turf XL, New Alipore (brain/TERRATHON.md 5b); Crave'lla = desserts and brownies, a
photobooth etc. are other stalls (user-confirmed 5f); handle @cravella_kolkata (partner file + the logo labels in the photo). Menu and prices verbatim
from the user's FINAL menu (2026-10-01; replaces the first, longer list); where every item in a group shares a price it is printed ONCE ("ALL RS. 299"). Not claimed: a founding year, ingredients,
ordering links, or that stall sales go to charity (only the fete is "all for charity" in the copy pack, and this deck does not say it).
Spelling flag: the user wrote "Asscai Bowl"; printed here as ACAI BOWL (flagged back to the user).

Look: TerraThon's (black ground, shuriken, cream cards with green borders, orchid highlights, StretchPro title, Sigmar One sub).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_cravella.py [story]   (story = 1080x1920, out/collaterals/stories/cravella_story_NN.png)
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = "story" in sys.argv[1:]     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = (1920 if STORY else 1350), 6
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/partners/cravella"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


LOGO = b64(f"{A}/logo_circle.png", "image/png")
PH_TIRA = b64(f"{A}/tiramisu.jpg", "image/jpeg")
PH_TINS = b64(f"{A}/cookie_tins.jpg", "image/jpeg")


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
        self.text("t1", "TERRATHON MINI-FETE", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
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


async def build():
    slides = []
    # 1 COVER
    s = Slide(1, 21)
    ty = await s.title("CRAVE'LLA", "OUR DESSERT PARTNER", big_w=780, sub_w=760, top=104)
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    ls = 780 if STORY else 700; lx, lyy = (W - ls) / 2, ty + 24
    s.logo_badge("logo_big", lx, lyy, ls, ring=14)
    s.star("star_bl", lx - 40, lyy + ls - 150, 116, z=10); s.star("star_br", lx + ls - 80, lyy + 10, 104, z=10)
    s.chip("chip", "DESSERTS + BROWNIES", (W - 640) / 2, lyy + ls - 30, 640, deg=-2.5, size=40)
    s.text("info", "AT THE MINI-FETE  |  3RD + 4TH OCT  |  TURF XL, NEW ALIPORE", 40, lyy + ls + 96, W - 80, 27, 900)
    s.footer(); slides.append((s, ("logo_big", "chip"), ("logo_big", "star_bl"), ("logo_big", "star_br"), ("star_bl", "chip")))
    # 2 INTRO
    s = Slide(2, 22)
    ty = await s.title("MEET THE STALL", "CRAVE'LLA, OUR DESSERT PARTNER", big_w=760, sub_w=860, top=96)
    fy = ty + 14; fh = 690 + EXTRA
    s.frame("frame", PH_TIRA, 84, fy, 912, fh, -1.25, "50% 92%")
    s.logo_badge("badge", 40, fy - 40, 170, ring=8)
    s.star("star_tr", W - 130, fy - 36, 104)
    cy0 = fy + fh + 54; cw, ch, g = 296, 220, 12
    for i, (hd, body) in enumerate((("WHAT", "DESSERTS, BROWNIES AND COOKIE TINS"), ("WHEN", "SAT 3 + SUN 4 OCT, 2026"), ("WHERE", "TURF XL, NEW ALIPORE"))):
        x = 84 + i * (cw + g)
        s.box(f"fact{i}", x, cy0, cw, ch, f'<div style="display:inline-block;background:{ORCHID};font-weight:900;font-size:24px;line-height:1;padding:7px 16px 6px;border-radius:999px">{hd}</div>'
                                          f'<div style="font-weight:900;font-size:27px;line-height:1.12;margin-top:14px">{body}</div>', pad="16px 18px")
    s.footer(); slides.append((s, ("frame", "badge"), ("frame", "star_tr"), ("badge", "star_tr")))
    # 3 MENU 1
    s = Slide(3, 23)
    ty = await s.title("THE MENU", "ACAI + TIRAMISU", big_w=620, sub_w=560, top=96)
    RH, sz = 150 + (30 if STORY else 0), 44
    hA = 26 + 56 + 32 + RH * 1 + 22; hB = 26 + 56 + 32 + RH * 1 + 22
    top = ty + 20 + (1160 + OY + EXTRA - ty - 20 - (hA + hB + 26)) / 2
    s.box("boxA", 56, top, 968, hA, head_row("ACAI BOWL", "RS. 299") + f'<div style="margin-top:14px">{rows_html(["GRANOLA GREEK YOGHURT BOWL"], RH, sz)}</div>', pad="26px 26px 22px")
    s.box("boxB", 56, top + hA + 26, 968, hB, head_row("TIRAMISU", "RS. 299") + f'<div style="margin-top:14px">{rows_html(["CLASSIC TIRAMISU"], RH, sz)}</div>', pad="26px 26px 22px")
    s.star("star_tl", 30, 60 + OY); s.star("star_tr", W - 30 - 104, 74 + OY)
    s.text("note", "CRAVE'LLA STALL, TURF XL  |  3RD + 4TH OCT", 40, 1196 + OY + EXTRA, W - 80, 24, 400)
    s.footer(); slides.append((s,))
    # 4 MENU 2
    s = Slide(4, 24)
    ty = await s.title("THE MENU", "BROWNIES + CHEESECAKES", big_w=620, sub_w=800, top=96)
    left = ["BELGIAN CHOCOLATE CHUNK", "COOKIE DOUGH", "BISCOFF"]
    right = ["BLUEBERRY CHEESECAKE", "NUTELLA CHEESECAKE", "BISCOFF CHEESECAKE"]
    RH, sz = 190 + (30 if STORY else 0), 38; hC = 26 + 56 + 32 + RH * 3 + 22
    col = lambda rws: f'<div style="flex:1 1 0;min-width:0">{rows_html(rws, RH, sz)}</div>'
    top = ty + 20 + (1160 + OY + EXTRA - ty - 20 - hC) / 2
    s.box("boxC", 56, top, 968, hC, head_row("BROWNIES + CHEESECAKES", "ALL RS. 150", 44) + f'<div style="display:flex;gap:34px;margin-top:14px">{col(left)}{col(right)}</div>', pad="26px 26px 22px")
    s.star("star_tl", 30, 60 + OY); s.star("star_tr", W - 30 - 104, 74 + OY)
    s.text("note", "CRAVE'LLA STALL, TURF XL  |  3RD + 4TH OCT", 40, 1196 + OY + EXTRA, W - 80, 24, 400)
    s.footer(); slides.append((s,))
    # 5 MENU 3 (cookie tins + photo)
    s = Slide(5, 25)
    ty = await s.title("THE MENU", "COOKIE TIN", big_w=620, sub_w=480, top=96)
    fy, fh = ty + 24, 840 + EXTRA
    s.frame("frame", PH_TINS, 56, fy, 470, fh, -2, "50% 62%")
    s.star("star_c", 30, fy + fh - 80, 110)
    tins = [("MIDNIGHT COOKIE TIN", "RS. 500"), ("TRIPLE CHOCOLATE COOKIE TIN", "RS. 700")]
    rh = (fh - 26 - 56 - 32 - 22 - 12) // 2
    inner = head_row("COOKIE TIN") + '<div style="margin-top:14px">'
    for i, (nm, pr) in enumerate(tins):
        sep = "border-top:3px solid rgba(10,10,10,.22);" if i else ""
        inner += f'<div style="height:{rh}px;{sep}display:flex;flex-direction:column;justify-content:center;gap:8px"><div style="font-size:31px;line-height:1.1">{nm}</div><div style="font-weight:900;font-size:58px;line-height:1;color:{INK}">{pr}</div></div>'
    inner += "</div>"
    s.box("boxD", 560, fy + 6, 464, fh - 12, inner, pad="26px 24px 22px")
    s.star("star_tr", W - 30 - 104, 70 + OY, 104)
    s.text("note", "CRAVE'LLA STALL, TURF XL  |  3RD + 4TH OCT", 40, fy + fh + 54, W - 80, 24, 400)
    s.footer(); slides.append((s, ("frame", "star_c"), ("frame", "boxD")))
    # 6 CLOSER
    s = Slide(6, 26)
    ty = await s.title("SEE YOU THERE", "CRAVE'LLA, OUR DESSERT PARTNER", big_w=800, sub_w=880, top=96)
    ls = 540 if STORY else 340; s.logo_badge("logo_big", (W - ls) / 2, ty + 20, ls, ring=12)
    s.star("star_l", 110, ty + 90, 110); s.star("star_r", W - 110 - 110, ty + 150, 110)
    sx, sy, sw, sh = 84, ty + 20 + ls + (70 if STORY else 50), 912, (420 if STORY else 330)
    s.add(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(-1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>')
    s.el("slab", *rb(sx, sy, sw, sh, -1.25))
    k = 8 if STORY else 0
    rows = [("3RD & 4TH OCTOBER, 2026", 900, 46 + k), ("TURF XL, NEW ALIPORE", 900, 46 + k), ("DESSERTS, BROWNIES, COOKIE TINS AND MORE", 400, 28 + k // 2), ("OPEN TO ALL AT THE MINI-FETE", 400, 28 + k // 2)]
    ty2 = sy + (72 if STORY else 52)
    for i, (txt, wt, sz) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 40}px;width:{sw - 80}px;top:{ty2}px;text-align:center;color:{INK};font-family:var(--d);font-weight:{wt};font-size:{sz}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>')
        s.el(f"row{i}", sx + 40, ty2, sw - 80, sz * .85); ty2 += sz + ((34 if i == 1 else 22) if STORY else (24 if i == 1 else 16))
    s.footer(cta="@CRAVELLA_KOLKATA"); slides.append((s, ("logo_big", "star_l"), ("logo_big", "star_r")) + tuple(("slab", f"row{i}") for i in range(4)) + (("logo_big", "slab"),))
    return slides


async def main():
    slides = await build()
    outdir = "out/collaterals/stories" if STORY else "out/collaterals/cravella_stall"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("card", INK, CTA_FILL, 31, False), ("chip", INK, ORCHID, 30, True),
                  ("price", INK, GREEN, 40, True), ("idx", INK, CTA_FILL, 26, True), ("note", WHITE, GROUND, 24, False), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for s, *ign in slides:
            out = f"{outdir}/cravella_story_{s.idx:02d}.png" if STORY else f"{outdir}/slide_{s.idx:02d}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",) if s.idx == 6 else (), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "logo_big", "badge"))
            print("done", out)

asyncio.run(main())
