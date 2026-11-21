"""DISCO DIWALI sponsor thank-you poster: title sponsor EXPOSURE (Exposure Institute), feed 1080x1350 and story 1080x1920.

Built on the charity poster skeleton (dd_charity.py): event photo ground, string lights, LIVE badge top left, copper HEART sticker top right (a thank-you
heart), THANK YOU as the hero, the edition-free "to our title sponsor" line, the sponsor's OWN logo, the DISCO DIWALI lockup as a footer mark. No pill, no link.
Adaptations: the logo is the user's supplied JPG (white ground), so it sits on a cream plaque and is MULTIPLY-blended so its white becomes the plaque's cream and
its colours stay untouched (a sponsor logo is never recoloured). The plaque is the one card in the format; the logo needs a light surface (grey and black type).
Facts: sponsor name and role supplied by the user. No amount, no date, no venue. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_thanks_exposure.py"""
import asyncio, base64, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
import dd_photo_bg as _pb, dd_copper as _cp
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "thanks_exposure")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
PHOTO, PHOTO_POS = "14_04", "50% 30%"
LOGO = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, "engine", "assets", "sponsors", "exposure_logo.jpg"), "rb").read()).decode()
LOGO_AR = 161 / 670
TILT = -3


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


def poster(H):
    story = H > 1350
    sq = H < 1350
    parts, els = [_pb.photo_ground(dd, W, H, PHOTO, PHOTO_POS)], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    hs = 250 if not story else 260
    if sq: hs = 210
    sx, sy_ = 1040 - hs, (60 if not story else 220)
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sy_}px;z-index:12">{_cp.heart(hs, 10)}</div>'); els.append(("sticker", sx, sy_, hs, round(hs * .9)))

    def line(tag, txt, top, fsize, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    size = 215 if story else 200
    hy = 520 if story else 300
    if sq:                                   # square: ONE headline line, so the sponsor stack fits 1080
        size, hy = 148, 262
        line("head1", "Thank you", hy, size, 700, size)
        sub_y = hy + size + 14
    else:
        line("head1", "Thank", hy, size, 700, size)
        line("head2", "you", hy + round(size * .96), size, 700, size)
        sub_y = hy + round(size * .96) * 2 + 20
    line("sub", "to our title sponsor", sub_y, 44, 400, 46)
    # sponsor plaque
    pad = 30
    lw = 800 if story else (620 if sq else 720)
    lh = round(lw * LOGO_AR)
    pw, ph = lw + 2 * pad, lh + 2 * pad
    cx = W // 2
    py = sub_y + 46 + (50 if story else (26 if sq else 36))
    parts.append(f'<div data-tag="plaque" style="position:absolute;left:{cx - pw // 2}px;top:{py}px;width:{pw}px;height:{ph}px;box-sizing:border-box;background:#F4EFE0;border:5px solid #D9B25F;'
                 f'border-radius:20px;box-shadow:12px 14px 0 rgba(0,0,0,.7);transform:rotate({TILT}deg);z-index:15">'
                 f'<img data-tag="logo" src="{LOGO}" style="position:absolute;left:{pad - 5}px;top:{pad - 5}px;width:{lw}px;height:{lh}px;mix-blend-mode:multiply"></div>')
    els.append(("plaque",) + rot_box(cx, py + ph / 2, pw, ph, TILT))
    nm_y = py + ph + (46 if story else (30 if sq else 36))
    line("name", "Exposure Institute", nm_y, 40, 700, 42)
    vw = 300 if story else (190 if sq else 250)
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    vy = 1450 if story else H - 52 - vh   # story: ends above Instagram's reply-bar zone (y>=1670)
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920), ("square", 1080)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            tp = [("headline", "#fff", "#1a1020", 200, True), ("sub", "#fff", "#1a1020", 44, False), ("name", "#fff", "#1a1020", 40, True)]
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(("plaque", "logo") and ()), bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", collision_ignore=[], text_pairs=tp)
    print("done ->", OUT)
asyncio.run(main())
