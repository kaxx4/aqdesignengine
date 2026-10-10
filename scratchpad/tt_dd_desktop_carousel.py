"""DISCO DIWALI "desktop diary" carousel (user, 2026-10-10), 5 slides, feed 1080x1350 + story 1080x1920 (arg: story).
Mechanism from the user's reference (a Mac desktop as a diary): a menu bar, photo-thumbnail icons with captions and folders scattered
around the screen, a central Photo Booth window holding one big photo with a camera bar, and an iOS-style alert dialog (title, quote,
Options / Close) overlapping it, with a cursor on the camera button. Dressed in TerraThon (black ground, orchid-bordered cream UI).
Slides: 1 desktop cover / 2-4 one photo window each (dance, decor, group) with an alert caption / 5 closer (alert + stickers).
TEASER: tickets are NOT on sale and the user wants no ticket talk; no date, venue, price, link in bio. Photos: real DD photos.
Adaptations: Portuguese captions -> English AQ-voice lines; wallpaper -> TerraThon black starfield; menu bar clock omitted (no time/date).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_desktop_carousel.py [story]  -> out/collaterals/dd_desktop[_story]/
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("fc", os.path.join(ROOT, "scratchpad", "tt_dd_folder_carousel.py"))
fc = importlib.util.module_from_spec(sp); sp.loader.exec_module(fc)
B, W, H, OY = fc.B, fc.W, fc.H, fc.DY
FOOT, Slide, PH, rb = fc.FOOT, fc.Slide, fc.PH, fc.rb
ORCHID, CTA_FILL, INK, WHITE, GROUND = fc.ORCHID, fc.CTA_FILL, fc.INK, fc.WHITE, fc.GROUND
LEMON, GREEN, BLUE_T = fc.LEMON, fc.GREEN, "#0A7BE0"
EXTRA = 200 if fc.STORY else 0
STORY = fc.STORY

CAM = (f'<svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="{ORCHID}" stroke="{INK}" stroke-width="4"/>'
       f'<rect x="26" y="36" width="48" height="32" rx="7" fill="#fff"/><rect x="40" y="30" width="20" height="9" rx="3" fill="#fff"/>'
       f'<circle cx="50" cy="52" r="10" fill="{ORCHID}"/><circle cx="50" cy="52" r="5" fill="#fff"/></svg>')
WIFI = (f'<svg width="40" height="30" viewBox="0 0 40 30" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round">'
        f'<path d="M3,12 Q20,-2 37,12"/><path d="M10,19 Q20,10 30,19"/><circle cx="20" cy="25" r="2.5" fill="{INK}"/></svg>')
BATT = (f'<svg width="52" height="28" viewBox="0 0 52 28"><rect x="2" y="2" width="42" height="24" rx="7" fill="none" stroke="{INK}" stroke-width="3.5"/>'
        f'<rect x="6" y="6" width="22" height="16" rx="3" fill="{INK}"/><rect x="46" y="9" width="4" height="10" rx="2" fill="{INK}"/></svg>')

CROPS = {  # (photo key, background-size %, background-position)
    "decor": ("decor", 160, "20% 60%"), "dance": ("dance", 230, "55% 30%"), "people": ("group", 200, "30% 40%"),
    "lights": ("dance", 300, "70% 0%"), "cassette": ("decor", 260, "10% 90%"), "blocks": ("decor", 320, "100% 65%")}


def menubar(s):
    y = OY
    s.add(f'<div class="measure" data-tag="mbar" style="position:absolute;left:0;top:{y}px;width:{W}px;height:68px;background:{CTA_FILL};border-bottom:5px solid {ORCHID};z-index:3"></div>')
    s.el("mbar", 0, y, W, 68)
    im, src = fc.tt.crop_to_alpha("shuriken.png")
    s.add(f'<img src="{src}" style="position:absolute;left:24px;top:{y + 12}px;width:46px;z-index:4">')
    s.add(f'<div style="position:absolute;left:84px;top:{y + 18}px;font-family:var(--d);font-weight:900;font-size:28px;color:{INK};z-index:4;white-space:nowrap">DISCO DIWALI</div>')
    s.add(f'<div style="position:absolute;right:28px;top:{y + 18}px;display:flex;gap:18px;align-items:center;z-index:4">{WIFI}{BATT}</div>')


def thumb(s, tag, key, x, y, label, w=150, h=130, z=5):
    k, z_, pos = CROPS[key]
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {CTA_FILL};border-radius:22px;'
          f'background:url({PH[k]}) {pos}/{z_}% auto no-repeat;box-shadow:0 0 0 4px {ORCHID};z-index:{z}"></div>')
    s.add(f'<div style="position:absolute;left:{x - 25}px;top:{y + h + 18}px;width:{w + 50}px;text-align:center;font-family:var(--d);font-weight:400;font-size:24px;line-height:1.1;color:{WHITE};z-index:{z}">{label}</div>')
    s.el(tag, x - 25, y - 4, w + 50, h + 18 + 56)


def folder_icon(s, tag, x, y, label, w=130, k="x"):
    fh = w * .8
    s.folder(tag, x, y, w, k, z=5)
    s.add(f'<div style="position:absolute;left:{x - 30}px;top:{y + fh + 14}px;width:{w + 60}px;text-align:center;font-family:var(--d);font-weight:400;font-size:24px;line-height:1.1;color:{WHITE};z-index:5">{label}</div>')
    s.els[-1] = (tag, x - 30, y, w + 60, fh + 14 + 30)


def window(s, tag, x, y, w, photo_h, key, pos="50% 50%", title="DISCO DIWALI BOOTH", z=6):
    bar, foot = 60, 96
    h = bar + photo_h + foot + 12
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:30px;background:{CTA_FILL};overflow:hidden;z-index:{z}">'
          f'<div style="height:{bar}px;display:flex;align-items:center;padding:0 22px;gap:11px;position:relative;border-bottom:3px solid rgba(10,10,10,.15)">'
          f'<div style="width:20px;height:20px;border-radius:50%;background:{ORCHID}"></div><div style="width:20px;height:20px;border-radius:50%;background:{LEMON}"></div><div style="width:20px;height:20px;border-radius:50%;background:{GREEN}"></div>'
          f'<div style="position:absolute;left:0;right:0;text-align:center;font-family:var(--d);font-weight:900;font-size:26px;color:{INK}">{title}</div></div>'
          f'<img src="{PH[key]}" style="width:100%;height:{photo_h}px;object-fit:cover;object-position:{pos};display:block">'
          f'<div style="height:{foot}px;position:relative;display:flex;align-items:center;padding:0 24px">'
          f'<div style="width:60px;height:60px;border-radius:12px;border:4px solid {INK};background:url({PH[key]}) center/cover"></div>'
          f'<div style="position:absolute;left:{w / 2 - 56}px;top:{foot / 2 - 50 - 3}px">{CAM}</div>'
          f'<div style="margin-left:auto;border:3px solid {INK};border-radius:999px;padding:5px 26px;font-family:var(--d);font-weight:400;font-size:22px;color:{INK}">VIDEO</div></div></div>')
    s.el(tag, x, y, w, h)
    return h, (x + w / 2 - 6 + 18, y + h - foot / 2 + 10)       # window height, cursor spot beside the camera


def alert(s, tag, x, y, w, title, body, hi="close", z=9, bh=76):
    h = 150 + bh + (0)
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:36px;background:{CTA_FILL};overflow:hidden;z-index:{z}">'
          f'<div style="height:{h - bh - 12}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:0 24px;text-align:center">'
          f'<div style="font-family:var(--d);font-weight:900;font-size:34px;line-height:1;color:{INK}">{title}</div>'
          f'<div style="font-family:var(--d);font-weight:400;font-size:28px;line-height:1.1;color:{INK}">{body}</div></div>'
          f'<div style="height:{bh}px;border-top:3px solid rgba(10,10,10,.18);display:flex;font-family:var(--d);font-size:30px;color:{BLUE_T}">'
          f'<div style="flex:1;display:flex;align-items:center;justify-content:center;border-right:3px solid rgba(10,10,10,.18);font-weight:400">Options</div>'
          f'<div style="flex:1;display:flex;align-items:center;justify-content:center;font-weight:900">Close</div></div></div>')
    s.el(tag, x, y, w, h)
    return h


async def build():
    out = []
    # ---------- 1 DESKTOP COVER ----------
    s = Slide(1, 601); menubar(s)
    t0 = OY + 120
    thumb(s, "th1", "decor", 60, t0, "THE DECOR")
    thumb(s, "th2", "dance", 465, t0 - 30, "THE DANCE<br>FLOOR")
    thumb(s, "th3", "people", 870, t0, "THE PEOPLE")
    thumb(s, "th4", "lights", 60, t0 + 320, "THE LIGHTS")
    folder_icon(s, "fo1", 910, t0 + 410, "OUTFITS", k="c1")
    wy = t0 + 280
    wh, cur = window(s, "win", 250, wy, 580, 400, "dance", "55% 40%")
    ad = alert(s, "alt", 60, wy + wh - 325, 430, "DISCO DIWALI", "Something is loading...")
    s.cursor("cur", cur[0], cur[1], z=12)
    by = wy + wh + 90
    thumb(s, "th5", "cassette", 90, by, "THE VIBES")
    folder_icon(s, "fo2", 475, by + 6, "DISCO DIWALI", k="c2")
    thumb(s, "th6", "blocks", 830, by, "THE BLOCKS")
    s.footer(); s.allow("win", "alt"); s.allow("win", "cur"); s.allow("alt", "cur"); s.allow("alt", "th4")
    out.append(("1", s))
    # ---------- 2-4 PHOTO WINDOWS ----------
    pts = [("2", "dance", "DANCE FLOOR", "Zero skill required.", "55% 40%"),
           ("3", "decor", "DISCO DECOR", "Balls, blocks and a cassette.", "50% 60%"),
           ("4", "group", "YOUR PEOPLE", "Dressed in their best.", "50% 45%")]
    for n, key, ttl, body, pos in pts:
        s = Slide(int(n), 610 + int(n)); menubar(s)
        wy = OY + 120
        wh, cur = window(s, "win", 70, wy, 940, 700 + EXTRA // 2, key, pos)
        s.cursor("cur", cur[0], cur[1], z=12)
        alert(s, "alt", 40, wy + wh - 325, 520, ttl, body)
        fy = wy + wh + 50
        folder_icon(s, "fo", 880, fy - 10, "DISCO DIWALI", k=f"d{n}")
        s.star("star", 760, fy - 6, 90)
        s.footer(); s.allow("win", "alt"); s.allow("win", "cur"); s.allow("alt", "cur")
        out.append((n, s))
    # ---------- 5 CLOSER ----------
    s = Slide(5, 605); menubar(s)
    t0 = OY + 120
    thumb(s, "th1", "decor", 60, t0, "THE DECOR"); thumb(s, "th2", "dance", 465, t0 - 30, "THE DANCE<br>FLOOR"); thumb(s, "th3", "people", 870, t0, "THE PEOPLE")
    ball, bh = fc.ddm.disco_ball(300, "b5"); fc.svg_sticker(s, "ball", ball, 700, t0 + 300, 300, bh, 6)
    dy, dyh = fc.ddm.diya(280, "d5"); fc.svg_sticker(s, "diya", dy, 90, t0 + 330, 280, dyh, -8)
    ay = t0 + 300 + bh + 80
    alert(s, "alt", 190, ay, 700, "DISCO DIWALI", "Save this folder. More soon.", bh=90)
    s.cursor("cur", 640, ay + 150 + 90 - 40, z=12)
    s.footer(cta="STAY TUNED"); s.allow("alt", "cur")
    out.append(("5", s))
    return out


async def main():
    res = await build()
    outdir = "out/collaterals/dd_desktop" + ("_story" if STORY else ""); os.makedirs(outdir, exist_ok=True)
    text_pairs = [("ui", INK, CTA_FILL, 28, True), ("cap", WHITE, GROUND, 24, False), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s in res:
            out = f"{outdir}/dd_desktop_{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("win",), page_bg=GROUND, expect_hero=False,
                           collision_ignore=set(map(tuple, s.ign)), margin=12, bleed_tags=("mbar",), crop_tags=("win", "th1", "th2", "th3", "th4", "th5", "th6"))
            print("done", out)

asyncio.run(main())
