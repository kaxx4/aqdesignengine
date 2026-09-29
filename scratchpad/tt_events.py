"""TerraThon event posters from ONE skeleton (Wicket Wars, PickleJam, Soccer Storm).

The three references share the skeleton to the pixel (brain/TERRATHON.md sec 2); only the hero,
title, numbers and CTA change, so the events are DATA and `build()` is the format. Coordinates are
reference px on the 1600-wide design, mapped to the 1080x1350 feed canvas by S = 0.675.

Adaptations (recorded per CLAUDE.md sec 2 rule 4):
  * NeutralFace throughout (user ruling): 400 for labels, 900 for values. NO stretched glyphs (user ruling).
  * Stickers are the user's real files (engine/assets/terrathon), placed at native size (x 1600/1620),
    aligned by their alpha box. The slab hides each hero's lower edge, as in the references.
  * The calendar is DRAWN, with no date (the reference emoji reads "JUL 17").
  * The reference Soccer Storm subtitle reads "A FIFA TOURNMENT" (typo). Set correctly here.
  * The Soccer Storm "bio" reference omits the TERRATHON pill; the other five event posters carry it, so
    it is part of the series and is drawn. Scored against soccer_storm_below.png, which has it.
  * Palette is TerraThon's own. Noto Color Emoji stands in for Apple's.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_events.py [wicket_wars|picklejam|soccer_storm ...]
"""
import asyncio, base64, io, os, random, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core"); B = load("build")
import numpy as np
from PIL import Image

W, H = core.SIZES["feed"]
S = W / 1600.0
NATIVE = 1600 / 1620          # stickers sit 1:1 in the 1620px design
ASSET = "engine/assets/terrathon"

FONT_CSS = (
    "@font-face{font-family:'StretchPro';src:url(data:font/otf;base64,"
    + base64.b64encode(open("engine/assets/fonts/StretchPro.otf", "rb").read()).decode() + ") format('opentype')}"
    "@font-face{font-family:'SigmarOne';src:url(data:font/woff2;base64,"
    + base64.b64encode(open("engine/assets/fonts/SigmarOne-Regular.woff2", "rb").read()).decode() + ") format('woff2')}")
TITLE_W, SUBTITLE_PX = 940, 80    # longest title line width (ref px) and Sigmar One subtitle size

GROUND, ORCHID, CREAM_HALO, SLAB = "#000000", "#DE68F0", "#F3ECDE", "#F9F9F9"
INK, WHITE, CTA_FILL = "#0A0A0A", "#F5F5F5", "#F5EEE1"


def px(v):
    return round(v * S, 1)


SUB_PX, SUB_MAX_W = 88, 1265     # subtitle size / max width, ref px (PickleJam's long sport name shrinks to fit)

EVENTS = {
    "wicket_wars": dict(
        sticker="cricket_set.png", hero_xy=(433, 484), title=("WICKEET", "WAARS"), sub="A CRICKET TOURNAMENT",
        pool="RS. 7,500", winner="RS.4,500", runners="RS.3,000",
        date="3RD & 4TH OCTOBER, 2026", venue="TURF XL",
        fee=[("PARTICIPATION FEE ", "RS. 2,100"), ("FOR A ", "TEAM OF 8")],
        date_dy=0, fee_dy=0, ref="wicket_wars_below"),
    "picklejam": dict(
        sticker="pickleball_set.png", hero_xy=(314, 483), title=("PICKLEE", "JAAM"), sub="A PICKLEBALL TOURNAMENT",
        pool="RS. 5,000", winner="RS.3,000", runners="RS.2,000",
        date="2ND OCTOBER, 2026", venue="11:11 PICK A COURT",
        fee=[("PARTICIPATION FEE ", "RS. 750"), ("FOR A ", "TEAM OF 2")],
        date_dy=6.5, fee_dy=1.5, ref="picklejam_below"),
    "soccer_storm": dict(
        sticker="controller.png", hero_xy=(340, 590), title=("SOCCER", "STOORM"), sub="A FIFA TOURNAMENT",
        pool="RS. 2,500", winner="RS.1,500", runners="RS.1,000",
        date="3RD OCTOBER, 2026", venue="BATTLEGROUND GAMING",
        fee=[("PARTICIPATION FEE ", "RS. 350")],
        date_dy=15.8, fee_dy=10, ref="soccer_storm_below"),
}


def b64_file(name):
    with open(f"{ASSET}/{name}", "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def crop_to_alpha(name):
    im = Image.open(f"{ASSET}/{name}").convert("RGBA")
    ys, xs = np.where(np.array(im)[..., 3] > 20)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    buf = io.BytesIO(); im.save(buf, "PNG")
    return im, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


async def build(ev, cta_text, out):
    els = []

    def el(label, x, y, w, h):
        els.append((label, x, y, w, h))

    def sticker(name, label, x0, y0, z):
        im, src = crop_to_alpha(name)
        w, h = px(im.width * NATIVE), px(im.height * NATIVE)
        el(label, px(x0), px(y0), w, h)
        return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{px(x0)}px;'
                f'top:{px(y0)}px;width:{w}px;height:{h}px;z-index:{z}">')

    # ground + flecks
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    ground = (f'<div style="position:absolute;inset:0;background:{GROUND}"></div>'
              f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>')

    # header
    HB = f'position:absolute;left:{px(420)}px;width:{px(760)}px;text-align:center;color:{WHITE};z-index:6;white-space:nowrap;line-height:1'
    emo = "font-family:'Noto Color Emoji';font-weight:400"
    hdr = (
        f'<div class="measure" data-tag="pp_label" style="{HB};top:{px(104)}px;font-family:var(--d);font-weight:400;font-size:{px(113.5)}px">PRIZE POOL:</div>'
        f'<div class="measure" data-tag="pp_value" style="{HB};top:{px(212)}px;font-family:var(--d);font-weight:900;font-size:{px(113.5)}px">'
        f'<span style="{emo};font-size:{px(84)}px;vertical-align:.02em;margin-right:{px(12)}px">💸</span>{ev["pool"]}</div>'
        f'<div class="measure" data-tag="winner" style="{HB};top:{px(338)}px;font-family:var(--d);font-weight:400;font-size:{px(50)}px">'
        f'WINNER<span style="{emo};font-size:{px(40)}px">🥇</span>: <b style="font-weight:900">{ev["winner"]}</b></div>'
        f'<div class="measure" data-tag="runners" style="{HB};top:{px(392)}px;font-family:var(--d);font-weight:400;font-size:{px(50)}px">'
        f'RUNNERS UP<span style="{emo};font-size:{px(40)}px">🥈</span>: <b style="font-weight:900">{ev["runners"]}</b></div>')
    el("pp_label", px(420), px(104), px(760), px(103)); el("pp_value", px(420), px(212), px(760), px(103))
    el("winner", px(420), px(338), px(760), px(50)); el("runners", px(420), px(392), px(760), px(50))

    # fest pill
    fx, fy, fw, fh = px(1198), px(78), px(377), px(120)
    el("fest_pill", fx, fy, fw, fh)
    fest = (f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px;'
            f'border:{px(9)}px solid {ORCHID};border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;'
            f'z-index:7;font-family:var(--d);font-weight:900;font-size:{px(46)}px;color:{INK}">TERRATHON</div>')

    # hero + stars (the fourth star sits over the slab corner)
    hero = sticker(ev["sticker"], "hero", *ev["hero_xy"], 3)
    stars = (sticker("shuriken.png", "star_tr", 1346, 257, 5) + sticker("shuriken.png", "star_ul", 163, 484, 5)
             + sticker("shuriken.png", "star_rm", 1343, 813, 5) + sticker("shuriken.png", "star_ll", 28, 1010, 9))

    # info rows: measured, then placed so the group is centred on x=800 (canvas centre)
    FS = px(49)
    date_dy, fee_dy = ev["date_dy"], ev["fee_dy"]
    m = await B.measure_text([
        dict(text=ev["date"], font="d", size=FS, weight=400),
        dict(text=ev["venue"], font="d", size=FS, weight=400),
        dict(text="📍", font="'Noto Color Emoji'", size=px(62), weight=400),
        dict(text=ev["sub"], font="SigmarOne", size=px(SUBTITLE_PX), weight=400),
        dict(text=ev["title"][0], font="StretchPro", size=100, weight=400),
        dict(text=ev["title"][1], font="StretchPro", size=100, weight=400)], extra_css=FONT_CSS)
    cal_w, ic_gap, grp_gap = px(84), px(6), px(80)
    dw, vw, pw = m[0]["text_w"], m[1]["text_w"], m[2]["text_w"]
    # subtitle: full size unless the sport name is long; then it shrinks to SUB_MAX_W (never crowds the slab border)
    sub_px = px(SUBTITLE_PX) * min(1.0, px(SUB_MAX_W) / m[3]["text_w"])
    title_px = 100 * px(TITLE_W) / max(m[4]["text_w"], m[5]["text_w"])          # StretchPro size that makes the longer line TITLE_W wide
    cap = 0.699 * title_px

    # slab + title
    SX, SY, SW, SH = px(70), px(1095), px(1472), px(506)
    el("slab", SX - px(6), SY - px(10), SW + px(12), SH + px(20))
    l1, l2 = ev["title"]
    slab = (f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;'
            f'transform:rotate(-1.25deg);background:{SLAB};border:{px(28)}px solid {ORCHID};border-radius:{px(70)}px;z-index:8">'
            f'<div style="position:absolute;left:{px(30)}px;top:{px(70) - 0.14 * title_px}px;font-family:StretchPro;color:{INK};'
            f'font-size:{title_px}px;line-height:1;white-space:nowrap">{l1}</div>'
            f'<div style="position:absolute;left:{px(30)}px;top:{px(70) + cap + px(30) - 0.14 * title_px}px;font-family:StretchPro;color:{INK};'
            f'font-size:{title_px}px;line-height:1;white-space:nowrap">{l2}</div>'
            f'<div style="position:absolute;left:{px(34)}px;top:{px(304)}px;font-family:SigmarOne;font-weight:400;color:{INK};'
            f'font-size:{sub_px}px;line-height:1;white-space:nowrap">{ev["sub"]}</div></div>')

    total = cal_w + ic_gap + dw + grp_gap + pw + ic_gap + vw
    x = (W - total) / 2
    ry = 1671 + date_dy
    LBL = f'font-family:var(--d);font-weight:400;font-size:{FS}px;line-height:1;color:{WHITE};white-space:nowrap'
    cal = (f'<svg class="measure" data-tag="cal" style="position:absolute;left:{x}px;top:{px(1648 + date_dy)}px;z-index:6" '
           f'width="{cal_w}" height="{px(84)}" viewBox="0 0 84 84"><rect x="6" y="14" width="72" height="64" rx="10" fill="{CREAM_HALO}"/>'
           f'<rect x="6" y="14" width="72" height="20" rx="8" fill="{ORCHID}"/>'
           f'<rect x="20" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/><rect x="56" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/>'
           f'<rect x="18" y="44" width="14" height="12" rx="3" fill="{INK}"/><rect x="38" y="44" width="14" height="12" rx="3" fill="{INK}"/>'
           f'<rect x="58" y="44" width="10" height="12" rx="3" fill="{INK}"/></svg>')
    el("cal", x, px(1648 + date_dy), cal_w, px(84))
    dx = x + cal_w + ic_gap
    date = f'<div class="measure" data-tag="date" style="position:absolute;left:{dx}px;top:{px(ry)}px;{LBL}">{ev["date"].replace("&", "&amp;")}</div>'
    el("date", dx, px(ry + 4), dw, FS)
    px_pin = dx + dw + grp_gap
    pin = (f'<span class="measure" data-tag="pin" style="position:absolute;left:{px_pin}px;top:{px(1646 + date_dy)}px;{emo};'
           f'font-size:{px(62)}px;line-height:1;z-index:6">📍</span>')
    el("pin", px_pin, px(1646 + date_dy), pw, px(74))
    vx = px_pin + pw + ic_gap
    venue = f'<div class="measure" data-tag="venue" style="position:absolute;left:{vx}px;top:{px(ry)}px;{LBL}">{ev["venue"]}</div>'
    el("venue", vx, px(ry + 4), vw, FS)
    fees = ""
    for i, (lab, val) in enumerate(ev["fee"]):
        top = 1751 + fee_dy + i * 52
        fees += (f'<div class="measure" data-tag="fee{i}" style="position:absolute;left:{px(400)}px;width:{px(800)}px;text-align:center;'
                 f'top:{px(top)}px;{LBL}">{lab}<b style="font-weight:900">{val}</b></div>')
        el(f"fee{i}", px(400), px(top), px(800), px(52))
    info = cal + date + pin + venue + fees

    # footer
    lh = px(83)
    logo = f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{px(40)}px;top:{px(1888)}px;height:{lh}px;z-index:9">'
    el("logo", px(40), px(1888), px(475), lh)
    cx, cy, cw, ch = px(1068), px(1880), px(500), px(100)
    el("cta", cx, cy, cw, ch)
    cta = (f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;'
           f'border:{px(9)}px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;'
           f'z-index:9;font-family:var(--d);font-weight:900;font-size:{px(44)}px;color:{INK}">{cta_text}</div>')

    html = B.page(W, H, GROUND, f'<style>{FONT_CSS}</style>' + ground + hdr + fest + hero + stars + slab + info + logo + cta, grain=False)
    text_pairs = [("prize", WHITE, GROUND, 96, True), ("info", WHITE, GROUND, 40, False),
                  ("title", INK, SLAB, 100, True), ("cta", INK, CTA_FILL, 34, True), ("pill", INK, "#FFFFFF", 36, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND,
                   expect_hero=True, collision_ignore={("hero", "slab"), ("star_ll", "slab")}, margin=12)


async def main(names):
    async with B.session():
        for n in names:
            ev = EVENTS[n]
            os.makedirs(f"out/versions/terrathon_{n}", exist_ok=True)
            out = f"out/versions/terrathon_{n}/v{VERSION}.png"
            await build(ev, "LINK BELOW" if ev["ref"].endswith("below") else "LINK IN THE BIO", out)
            print("done", out)

VERSION = int(os.environ.get("TT_V", "1"))
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or list(EVENTS)))
