"""TerraThon PICKLEBALL THROWBACK carousel (7 slides, feed 1080x1350). Real photos from the user's zip (dd68314d-pickleball.zip,
HEIC -> JPEG, downscaled copies in engine/assets/terrathon/throwback/). IMG_6018 was a cricket turf, not pickleball, so it is unused.

Look: TerraThon's (black ground + white flecks, blue shuriken furniture, orchid-bordered frames, cream chips, StretchPro title,
Sigmar One sub sparingly, NeutralFace body). Photos sit in tilted orchid-bordered frames, the slab language, with a shuriken tucked on a
frame corner. Every caption describes THAT photo. No year, score, name or count is invented; the only facts are PickleJam's own
(2nd Oct, 11:11 Pick A Court, Rs. 750 per team of 2, pool Rs. 5,000, report 11:45am, matches 12pm to 7pm, registrations close 1 Oct).
The index tag ("02 / 07") is the truthful carousel position. CTA reads LINK IN THE BIO (registrations are open until 1 Oct).

Adaptation: the source photos are 9:16, cropped to the frame with a per-photo object-position (measured by looking).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_throwback.py
"""
import asyncio, base64, importlib.util, io, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
H = 1350
PHOTOS = "engine/assets/terrathon/throwback"
TOTAL = 7


def photo_src(n):
    return "data:image/jpeg;base64," + base64.b64encode(open(f"{PHOTOS}/IMG_{n}.jpg", "rb").read()).decode()


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

    def frame(self, tag, n, x, y, w, h, deg, pos="50% 50%", z=4):
        self.parts.append(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);'
                          f'border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:{z}">'
                          f'<img src="{photo_src(n)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>')
        self.el(tag, *rb(x, y, w, h, deg))

    def star(self, tag, x, y, size=120, z=8):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = size * im.height / im.width
        self.parts.append(f'<img src="{src}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{hh}px;z-index:{z}">')
        self.el(tag, x, y, size, hh)

    def chip(self, tag, txt, x, y, w, deg=-3, size=46, z=9):
        h = size + 44
        self.parts.append(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);'
                          f'border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;white-space:nowrap;'
                          f'font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;color:{INK};z-index:{z}">{txt}</div>')
        self.el(tag, *rb(x, y, w, h, deg))

    def text(self, tag, txt, x, y, w, size, weight=400, color=WHITE, align="center", z=6, lh=1.05):
        self.parts.append(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:{color};font-family:var(--d);'
                          f'font-weight:{weight};font-size:{size}px;line-height:{lh};white-space:nowrap;z-index:{z}">{txt}</div>')
        self.el(tag, x, y, w, size * 0.85)

    def footer(self, cta=None):
        ly = H - 27 - 56
        self.parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); self.el("logo", 27, ly, 320, 56)
        if cta:
            cw, chh = 400, 70; cx, cy = W - 27 - cw, H - 13 - chh
            self.parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                              f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:32px;color:{INK}">{cta}</div>')
            self.el("cta", cx, cy, cw, chh)
        else:
            tw, th = 150, 50; tx, ty = W - 27 - tw, H - 27 - th
            self.parts.append(f'<div class="measure" data-tag="idx" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                              f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:26px;color:{INK}">{self.idx:02d} / {TOTAL:02d}</div>')
            self.el("idx", tx, ty, tw, th)

    def html(self):
        return B.page(W, H, GROUND, "".join(self.parts), grain=False)


def photo_slide(idx, n, pos, chip_txt, sub, chip_w, deg=-1.25, flip=False):
    s = Slide(idx, 100 + idx)
    fx, fy, fw, fh = 84, 96, 912, 1010
    s.frame("frame", n, fx, fy, fw, fh, deg, pos)
    s.star("star_c", fx - 44 if not flip else fx + fw - 90, fy + fh - 96, 128)
    s.star("star_t", W - 27 - 120 if not flip else 27, 40, 100, z=8)
    s.chip("chip", chip_txt, 215 if not flip else W - 215 - chip_w, fy + fh - 92, chip_w, deg=-3 if not flip else 3)
    s.text("sub", sub, 60, fy + fh + 66, W - 120, 32, 400)
    s.footer()
    return s, ("frame_star", "star_c")


async def build_all():
    slides = []
    # 1. COVER
    s = Slide(1, 7)
    m = await B.measure_text([dict(text="THROWBACK", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="PICKLEBALL EDITION", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 780 / m[0]["text_w"]; spx = 50 * min(1.0, 700 / m[1]["text_w"])
    s.text("t1", "TERRATHON", (W - 420) / 2, 58, 420, 44, 400, CREAM_HALO)
    s.parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 800) / 2}px;width:800px;top:112px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                   f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">THROWBACK</div>'); s.el("t2", (W - 780) / 2, 116, 780, tpx * .82)
    s.parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{112 + tpx * 1.05}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                   f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">PICKLEBALL EDITION</div>'); s.el("t3", (W - 700) / 2, 112 + tpx * 1.05 + 2, 700, spx * .82)
    fy = 112 + tpx * 1.05 + spx + 46
    s.frame("frame", "6057", 110, fy, 860, 1220 - fy - 60, -1.25, "50% 100%")
    s.star("star_tl", 22, 70, 108); s.star("star_tr", W - 22 - 108, 84, 108); s.star("star_c", 110 - 50, 1220 - 60 - 90, 120)
    s.chip("chip", "SWIPE FOR THE REWIND", 300, 1220 - 60 - 30, 640, deg=-2.5, size=38)
    s.footer()
    slides.append((s, ("frame", "star_c"), ("frame", "chip")))
    # 2-4. single photos
    for idx, n, pos, chip, sub, cw, flip in ((2, "5997", "50% 72%", "EYES ON THE BALL", "LOW, FAST AND LOCKED IN", 600, False),
                                             (3, "6026", "50% 78%", "MID-AIR, UNBOTHERED", "THE OVERHEAD, CAUGHT ON CAMERA", 660, True),
                                             (4, "6085", "50% 72%", "SUN'S OUT, PADDLES OUT", "A WIDE SHOT OF A GOOD DAY", 660, False)):
        s, _ = photo_slide(idx, n, pos, chip, sub, cw, deg=-1.25 if not flip else 1.25, flip=flip)
        slides.append((s, ("frame", "star_c"), ("frame", "chip"), ("frame", "star_t")))
    # 5. COLLAGE (three frames)
    s = Slide(5, 105)
    s.frame("fa", "6046", 50, 110, 470, 620, -3, "50% 80%")
    s.frame("fb", "6048", 560, 170, 470, 620, 3, "50% 80%")
    s.frame("fc", "6059", 250, 830, 560, 400, -1.25, "50% 73%")
    s.star("star_a", 470, 80, 110); s.star("star_b", 22, 690, 120); s.star("star_c", W - 150, 1020, 110)
    s.chip("chip", "TEAMS OF TWO", 590, 1150, 420, deg=-3, size=40)
    s.footer()
    slides.append((s, ("fa", "star_a"), ("fa", "star_b"), ("fb", "star_a"), ("fa", "fb"), ("fa", "fc"), ("fb", "fc"), ("fc", "chip"), ("fb", "star_c"), ("fc", "star_c"), ("fc", "star_b"), ("fa", "chip"), ("fb", "chip"), ("star_c", "chip")))
    # 6. one more photo
    s, _ = photo_slide(6, "6060", "50% 88%", "READY FOR THE RETURN", "EVERY POINT STARTS LIKE THIS", 640, deg=-1.25)
    slides.append((s, ("frame", "star_c"), ("frame", "chip"), ("frame", "star_t")))
    # 7. CTA
    s = Slide(7, 107)
    m = await B.measure_text([dict(text="YOUR TURN", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="PICKLEJAM IS BACK", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tpx = 100 * 800 / m[0]["text_w"]; spx = 50 * min(1.0, 700 / m[1]["text_w"])
    s.parts.append(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - 940) / 2}px;width:940px;top:96px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                   f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">YOUR TURN</div>'); s.el("t2", (W - 800) / 2, 100, 800, tpx * .82)
    s.parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{96 + tpx * 1.05}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                   f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">PICKLEJAM IS BACK</div>'); s.el("t3", (W - 700) / 2, 96 + tpx * 1.05 + 2, 700, spx * .82)
    im, src = tt.crop_to_alpha("pickleball_set.png"); ph = 440; pw = ph * im.width / im.height
    s.parts.append(f'<img src="{src}" class="measure" data-tag="hero" style="position:absolute;left:{(W - pw) / 2}px;top:330px;width:{pw}px;height:{ph}px;z-index:4">'); s.el("hero", (W - pw) / 2, 330, pw, ph)
    s.star("star_tl", 60, 330, 110); s.star("star_tr", W - 60 - 110, 400, 110)
    sx, sy, sw, sh = 84, 800, 912, 430
    s.parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(-1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>')
    s.el("slab", *rb(sx, sy, sw, sh, -1.25))
    rows = [("2ND OCTOBER, 2026", 900, 46), ("11:11 PICK A COURT", 900, 46), ("RS. 750 PER TEAM OF 2  |  POOL RS. 5,000", 400, 30), ("REPORT BY 11:45AM  |  MATCHES 12PM TO 7PM", 400, 30), ("REGISTRATIONS CLOSE 1ST OCTOBER", 900, 30)]
    ty = sy + 52
    for i, (txt, wt, sz) in enumerate(rows):
        s.parts.append(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 40}px;width:{sw - 80}px;top:{ty}px;text-align:center;color:{INK};font-family:var(--d);font-weight:{wt};font-size:{sz}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>')
        s.el(f"row{i}", sx + 40, ty, sw - 80, sz * .85); ty += sz + (26 if i == 1 else 18)
    s.footer(cta="LINK IN THE BIO")
    slides.append((s, ("hero", "star_tl"), ("hero", "star_tr")) + tuple(("slab", f"row{i}") for i in range(5)) + (("hero", "slab"),))
    return slides


async def main():
    slides = await build_all()
    outdir = "out/collaterals/throwback_pickleball"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", WHITE, GROUND, 32, False), ("chip", INK, CTA_FILL, 42, True), ("idx", INK, CTA_FILL, 26, True), ("row", INK, SLAB, 46, True), ("cta", INK, CTA_FILL, 32, True)]
    async with B.session():
        for s, *ign in slides:
            out = f"{outdir}/slide_{s.idx:02d}.png"
            containers = ("slab",) if s.idx == 7 else ()
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=containers, page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "fa", "fb", "fc"))
            print("done", out)

asyncio.run(main())
