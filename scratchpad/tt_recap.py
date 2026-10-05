"""TerraThon 2026 POST-EVENT RECAP carousel, 9 slides, feed 1080x1350 (jokey, candid-photo led).

PLACEHOLDER PHOTOS: the real event photos are not supplied yet. Every photo below is a 2024 throwback frame (engine/assets/terrathon/throwback*),
and each photo slide carries a "PLACEHOLDER PHOTO" tag. To go live: change PH (slide -> file) to files in engine/assets/terrathon/day_photos/,
set PLACEHOLDER=False, re-measure each object-position by looking, and rewrite the captions to describe the real frame.
Facts used (user, 2026-10-05): 150+ participants, 3 days, 3 sports. Nothing else numeric is claimed.
Reuses the Slide kit from tt_throwback.py (same look: black ground, orchid frames, shuriken, cream chips, StretchPro + Sigmar One).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_recap.py
"""
import asyncio, base64, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PLACEHOLDER = True
src = open("scratchpad/tt_throwback.py", encoding="utf-8").read().replace("asyncio.run(main())", "")
sys.argv = ["x", "pickleball"]
g = {"__file__": os.path.join(ROOT, "scratchpad", "tt_throwback.py"), "__name__": "ttt"}
exec(compile(src, "tt_throwback.py", "exec"), g)
tt, B, W, H, Slide, rb, photo_slide = g["tt"], g["B"], g["W"], g["H"], g["Slide"], g["rb"], g["photo_slide"]
ORCHID, INK, WHITE, SLAB, GROUND, CTA_FILL, HALO = g["ORCHID"], g["INK"], g["WHITE"], g["SLAB"], g["GROUND"], g["CTA_FILL"], g["CREAM_HALO"]
TOTAL = 9; g["TOTAL"] = 9
DIRS = {"pb": "throwback", "ff": "throwback_fifa"}
def photo_src(n):
    d, f = n.split(":")
    return "data:image/jpeg;base64," + base64.b64encode(open(f"engine/assets/terrathon/{DIRS[d]}/{f}.jpg", "rb").read()).decode()
g["photo_src"] = photo_src

def tag(s):
    if PLACEHOLDER:
        s.parts.append(f'<div class="measure" data-tag="ph" style="position:absolute;left:400px;top:1285px;padding:6px 14px;border-radius:999px;background:#FF4D2E;color:#000;'
                       f'font-family:var(--m);font-weight:700;font-size:16px;z-index:30;white-space:nowrap">PLACEHOLDER PHOTO</div>'); s.el("ph", 400, 1285, 230, 36)

def tpx_of(m, w, size=100): return size * w / m["text_w"]
def stretch(s, tg, txt, tpx, cx, top, color=WHITE, w=940):
    s.parts.append(f'<div class="measure" data-tag="{tg}" style="position:absolute;left:{cx - w / 2}px;width:{w}px;top:{top}px;text-align:center;color:{color};font-family:StretchPro;'
                   f'-webkit-text-stroke:{tt.ST_STROKE * tpx}px {color};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{txt}</div>')
    s.el(tg, cx - w / 2 + 60, top, w - 120, tpx * .82)

async def build_all():
    S = []
    # 1 COVER
    s = Slide(1, 7)
    m = await B.measure_text([dict(text="THE AFTERMATH", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                              dict(text="TERRATHON 2026", font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    tp = tpx_of(m[0], 900); sp = 50 * min(1.0, 700 / m[1]["text_w"])
    s.text("t1", "ALLEGEDLY, WE HAD FUN", (W - 700) / 2, 34, 700, 36, 400, HALO)
    stretch(s, "t2", "THE AFTERMATH", tp, W / 2, 100)
    s.parts.append(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - 760) / 2}px;width:760px;top:{100 + tp * 1.08}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                   f'-webkit-text-stroke:{tt.SG_STROKE * sp}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{sp}px;line-height:1;white-space:nowrap;z-index:6">TERRATHON 2026</div>'); s.el("t3", (W - 700) / 2, 100 + tp * 1.08, 700, sp * .82)
    fy = 100 + tp * 1.08 + sp + 50
    s.frame("frame", "pb:IMG_6057", 110, fy, 860, 1220 - 60 - fy + 40, -1.25, "50% 100%")
    s.star("star_c", 60, 1010, 128); s.star("star_t", W - 27 - 130, 330, 110)
    s.chip("chip", "SWIPE FOR THE EVIDENCE", 250, 1090, 640, deg=-2.5, size=38)
    s.footer(); tag(s)
    S.append((s, ("frame", "star_c"), ("frame", "chip"), ("frame", "star_t"), ("t3", "frame"), ("frame", "ph"), ("star_t", "t3"), ("star_t", "t2"), ("star_c", "chip")))
    # 2 NUMBERS
    s = Slide(2, 102)
    m = await B.measure_text([dict(text="150+", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
    s.text("k", "THE RECEIPTS", (W - 500) / 2, 70, 500, 46, 400, HALO)
    np_ = tpx_of(m[0], 860, 100); stretch(s, "big", "150+", np_, W / 2, 150)
    s.text("kk", "PARTICIPANTS WHO SHOWED UP AND SHOWED OFF", 40, 150 + np_ + 20, W - 80, 34, 900, ORCHID)
    ty = 150 + np_ + 90
    for i, (txt, sub, x, dg) in enumerate([("3 DAYS", "OF CONTROLLED CHAOS", 70, -2), ("3 SPORTS", "ZERO REGRETS (SOME)", 560, 2)]):
        w_, h_ = 450, 300
        s.parts.append(f'<div class="measure" data-tag="tile{i}" style="position:absolute;left:{x}px;top:{ty + i * 40}px;width:{w_}px;height:{h_}px;box-sizing:border-box;transform:rotate({dg}deg);background:{SLAB};'
                       f'border:18px solid {ORCHID};border-radius:52px;z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;color:{INK};font-family:var(--d)">'
                       f'<div style="font-weight:900;font-size:72px;line-height:1;white-space:nowrap">{txt}</div><div style="font-weight:400;font-size:26px;line-height:1;white-space:nowrap">{sub}</div></div>')
        s.el(f"tile{i}", *rb(x, ty + i * 40, w_, h_, dg))
    s.frame("frame", "ff:IMG-20241019-WA0021", 150, 900, 780, 300, -1.5, "50% 45%")
    s.star("star_a", 90, 1100, 120); s.star("star_b", W - 150, 130, 110); tag(s)
    s.footer()
    S.append((s, ("star_b", "big"), ("star_b", "kk"), ("frame", "star_a"), ("frame", "ph"), ("tile1", "frame"), ("tile0", "frame"), ("kk", "tile0"), ("kk", "tile1")))
    # 3-4,6,8 single photo slides ; 5,7 collages
    singles = {3: ("pb:IMG_5997", "50% 72%", "EYES ON THE BALL", "ALSO EYES ON THE SNACKS, LET'S BE HONEST", 600, False),
               4: ("ff:IMG_3789", "50% 55%", "'ONE QUICK MATCH'", "FAMOUS LAST WORDS", 600, False),
               6: ("ff:IMG_5870", "50% 45%", "SCOREBOARD HAS FEELINGS", "NO, WE WILL NOT BE TAKING QUESTIONS", 760, True),
               8: ("pb:IMG_6026", "50% 78%", "MAIN CHARACTER ENERGY", "THE OVERHEAD, THE CONFIDENCE, THE GLORY", 700, False)}
    for idx, (n, pos, chip, sub, cw, flip) in singles.items():
        s, _ = photo_slide(idx, n, pos, chip, sub, cw, deg=1.25 if flip else -1.25, flip=flip); tag(s)
        S.append((s, ("frame", "star_c"), ("frame", "chip"), ("frame", "star_t"), ("frame", "ph")))
    def collage(idx, frames, chip):
        s = Slide(idx, 100 + idx)
        for t_, n, x, y, w, h, dg, ps in frames: s.frame(t_, n, x, y, w, h, dg, ps)
        s.star("star_a", 470, 80, 110); s.star("star_b", 22, 690, 120); s.star("star_c", W - 150, 1020, 110)
        s.chip("chip", chip, 400, 1150, 620, deg=-3, size=40); s.footer(); tag(s)
        return (s, ("fa", "star_a"), ("fa", "star_b"), ("fb", "star_a"), ("fa", "fb"), ("fa", "fc"), ("fb", "fc"), ("fc", "chip"), ("fb", "star_c"), ("fc", "star_c"),
                ("fc", "star_b"), ("fa", "chip"), ("fb", "chip"), ("star_c", "chip"), ("fa", "ph"))
    c5 = collage(5, [("fa", "pb:IMG_6046", 50, 110, 470, 620, -3, "50% 80%"), ("fb", "pb:IMG_6048", 560, 170, 470, 620, 3, "50% 80%"), ("fc", "pb:IMG_6059", 250, 830, 560, 400, -1.25, "50% 73%")], "ZERO CHILL, FULL CARDIO")
    c7 = collage(7, [("fa", "ff:IMG_3796", 50, 110, 470, 620, -3, "50% 50%"), ("fb", "ff:IMG_5861", 560, 170, 470, 620, 3, "50% 60%"), ("fc", "ff:IMG_3791", 250, 830, 560, 400, -1.25, "50% 50%")], "THUMBS SORE, EGOS SORER")
    order = {x[0].idx: x for x in S}; order[5], order[7] = c5, c7
    S = [order[i] for i in range(1, 9) if i in order]
    # 9 CLOSER
    s = Slide(9, 109)
    m = await B.measure_text([dict(text="BACK NEXT YEAR", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
    tp = tpx_of(m[0], 900); stretch(s, "t2", "BACK NEXT YEAR", tp, W / 2, 96)
    im, srcimg = tt.crop_to_alpha("carnival.png"); ph = 470; pw = ph * im.width / im.height
    s.parts.append(f'<img src="{srcimg}" class="measure" data-tag="hero" style="position:absolute;left:{(W - pw) / 2}px;top:300px;width:{pw}px;height:{ph}px;z-index:4">'); s.el("hero", (W - pw) / 2, 300, pw, ph)
    s.star("star_tl", 60, 330, 110); s.star("star_tr", W - 170, 400, 110)
    sx, sy, sw, sh = 84, 810, 912, 400
    s.parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(-1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>')
    s.el("slab", *rb(sx, sy, sw, sh, -1.25))
    ty = sy + 60
    for i, (txt, wt, sz) in enumerate([("THANK YOU, 150+ OF YOU", 900, 52), ("3 DAYS. 3 SPORTS. ALL FOR CHARITY.", 400, 36), ("TAG YOURSELF IN THE COMMENTS", 400, 36), ("(WE KNOW YOU WILL ANYWAY)", 400, 30)]):
        s.parts.append(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 40}px;width:{sw - 80}px;top:{ty}px;text-align:center;color:{INK};font-family:var(--d);font-weight:{wt};font-size:{sz}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>')
        s.el(f"row{i}", sx + 40, ty, sw - 80, sz * .85); ty += sz + 34
    s.footer(cta="@NGO.AQUATERRA")
    S.append((s, ("hero", "star_tl"), ("hero", "star_tr"), ("hero", "slab")) + tuple(("slab", f"row{i}") for i in range(4)))
    return S

async def main():
    slides = await build_all(); outdir = "out/collaterals/terrathon_recap"; os.makedirs(outdir, exist_ok=True)
    tp_ = [("head", WHITE, GROUND, 96, True), ("chip", INK, CTA_FILL, 42, True), ("idx", INK, CTA_FILL, 26, True), ("row", INK, SLAB, 36, True), ("cta", INK, CTA_FILL, 28, True)]
    async with B.session():
        for s, *ign in slides:
            out = f"{outdir}/slide_{s.idx:02d}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=tp_, containers=("slab",) if s.idx == 9 else (), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "fa", "fb", "fc"))
            print("done", out)
asyncio.run(main())
