"""TerraThon Mini-Fete MARKETING CAROUSEL: "7 reasons to show up" (feed 1080x1350 AND story 1080x1920 from one brief).

Structure taken from the Paradox "13 reasons why" template (training_samples/terrathon/paradox_13_reasons_template.png):
cover -> one slide per reason (circular photo + headline + one-line wink) -> close. LOOK is TerraThon's (user ruling: black vibes):
black ground, the tilted white slab with orchid border, the four shuriken, the real sticker kit. The template's photo circle is TUCKED
behind the slab exactly like the event posters' hero.

User rulings folded in (2026-09-29): no sponsor strip; footer is JUST the AQ logo and "ALL FOR CHARITY"; photo circles are left BLANK
(a blue sticker disk) for the user to fill: drop a JPG/PNG named after the slide key into engine/assets/terrathon/carousel_photos/
(e.g. mini_games.jpg) and re-run; the disk becomes that photo. CTA is the WhatsApp group (link in bio / caption, never on the image).

Adaptations (CLAUDE.md sec 2 rule 4): NeutralFace throughout, no stretched glyphs; drawn dateless calendar not needed here; stories keep
the top ~250px and bottom ~260px free of key content (Instagram UI); copy is DRAFT for the user's approval.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_carousel.py [feed|story ...]
"""
import asyncio, base64, importlib.util, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B = tt.core, tt.B
GROUND, ORCHID, CREAM_HALO, SLAB, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL
BLUE = "#0396FF"
PHOTO_DIR = "engine/assets/terrathon/carousel_photos"

DATE, VENUE = "3RD & 4TH OCTOBER, 2026", "TURF XL, NEW ALIPORE"
REASONS = [   # key, headline, tagline  (DRAFT copy; vendor facts confirmed by the user 2026-09-29)
    ("mini_games", "MINI-GAMES", "WIN STUFF. TALK TRASH."),
    ("photobooth", "PHOTOBOOTH", "POSE NOW. REGRET NEVER."),
    ("artily", "ARTILY", "SIP BOBA. LOSE MINI-GAMES WITH DIGNITY."),
    ("cravella", "CRAVE'LLA", "DESSERTS AND BROWNIES. NO FURTHER QUESTIONS."),
    ("crftd", "CRFTD ORDERS", "PRE-ORDER DIY T-SHIRTS AND CUSTOM ORDERS."),
    ("lottery", "LOTTERY AT LOCATION", "LUCK HAS A STALL TOO."),
    ("dd_tickets", "DD TICKET STALL", "YOUR PASS TO THE PARTY IS ONE STALL AWAY."),
]
N = len(REASONS)

# layout per canvas: everything in canvas px. story keeps Instagram's UI zones clear (top 250, bottom 260).
LAYOUT = {
    "feed":  dict(W=1080, H=1350, disk_cy=420, disk_d=560, slab_top=640, slab_h=430, strip_y=1100, foot_y=1235,
                  cover_head_y=52, cover_hero_top=290, cover_hero_h=540, cover_slab_top=744, cover_slab_h=340, cover_strip_y=1112),
    "story": dict(W=1080, H=1920, disk_cy=640, disk_d=680, slab_top=930, slab_h=470, strip_y=1440, foot_y=1585,
                  cover_head_y=280, cover_hero_top=600, cover_hero_h=700, cover_slab_top=1188, cover_slab_h=340, cover_strip_y=1556),
}


def photo_src(key):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = f"{PHOTO_DIR}/{key}.{ext}"
        if os.path.exists(p):
            mime = "image/png" if ext == "png" else "image/webp" if ext == "webp" else "image/jpeg"
            return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
    return None


async def slide(kind, canvas, out, idx=None):
    L = LAYOUT[canvas]; W, H = L["W"], L["H"]
    els = []
    def el(label, x, y, w, h): els.append((label, x, y, w, h))

    def sticker(name, label, x, y, w_px, z):
        im, src = tt.crop_to_alpha(name)
        h_px = w_px * im.height / im.width
        el(label, x, y, w_px, h_px)
        return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;'
                f'width:{w_px}px;height:{h_px}px;z-index:{z}">'), h_px

    # ground
    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * H / 1350)))
    parts = [f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    slab_top, slab_h = (L["cover_slab_top"], L["cover_slab_h"]) if kind == "cover" else (L["slab_top"], L["slab_h"])
    SX, SW = 47, 986

    # ---- measure the strings we fit ----
    items = []
    if kind == "point":
        _, head, tag = REASONS[idx]
        items = [dict(text=head, font="d", size=100, weight=900)]
    elif kind == "close":
        items = [dict(text="WHATSAPP GROUP", font="d", size=96, weight=900)]
    m = await B.measure_text(items) if items else []

    # ---- hero ----
    if kind == "point":
        key = REASONS[idx][0]; D = L["disk_d"]; cx = W / 2; cy = L["disk_cy"]
        ph = photo_src(key)
        inner = (f'<img src="{ph}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;display:block">' if ph
                 else f'<div style="width:100%;height:100%;border-radius:50%;background:{BLUE}"></div>')
        parts.append(f'<div class="measure" data-tag="hero" style="position:absolute;left:{cx - D / 2}px;top:{cy - D / 2}px;width:{D}px;height:{D}px;'
                     f'border-radius:50%;border:14px solid {CREAM_HALO};background:{CREAM_HALO};z-index:3;overflow:hidden">{inner}</div>')
        el("hero", cx - D / 2, cy - D / 2, D, D)
    elif kind == "cover":
        h, hh = sticker("carnival.png", "hero", 0, 0, 1, 3)   # measure only
        ch = L["cover_hero_h"]; im, src = tt.crop_to_alpha("carnival.png"); w_px = ch * im.width / im.height
        els.pop()
        x = (W - w_px) / 2; y = L["cover_hero_top"]
        s, _ = sticker("carnival.png", "hero", x, y, w_px, 3); parts.append(s)
    else:   # close
        im, src = tt.crop_to_alpha("smiley.png"); ch = L["cover_hero_h"] * 0.95; w_px = ch * im.width / im.height
        x = (W - w_px) / 2; y = slab_top - ch + ch * 0.14
        s, _ = sticker("smiley.png", "hero", x, y, w_px, 3); parts.append(s)

    # ---- stars (constant furniture), pill ----
    star, sw = "shuriken.png", 100
    for lab, x, y, z in (("star_tl", 42, 53 if kind != "point" else 53, 5), ("star_tr", 946, slab_top - 330, 5),
                         ("star_ml", 19, slab_top - 52, 9), ("star_br", 970, slab_top + slab_h - 60, 9)):
        if canvas == "story" and lab == "star_tl": y = 270
        s, _ = sticker(star, lab, x, y, sw, z); parts.append(s)
    pw, ph_, px_, py_ = 254, 81, 809, 53 if canvas == "feed" else 270
    if kind != "cover":
      el("fest_pill", px_, py_, pw, ph_)
      parts.append(f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{px_}px;top:{py_}px;width:{pw}px;height:{ph_}px;'
                   f'border:6px solid {ORCHID};border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;z-index:7;'
                   f'font-family:var(--d);font-weight:900;font-size:31px;color:{INK}">TERRATHON</div>')

    # ---- cover header: centred, measured ----
    if kind == "cover":
        hy = L["cover_head_y"]
        hm = await B.measure_text([dict(text="7 REASONS", font="d", size=124, weight=900), dict(text="TO SHOW UP", font="d", size=80, weight=400)])
        w1, w2 = hm[0]["text_w"], hm[1]["text_w"]
        parts.append(f'<div class="measure" data-tag="c_head1" style="position:absolute;left:{(W - w1) / 2}px;top:{hy}px;font-family:var(--d);font-weight:900;'
                     f'font-size:124px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">7 REASONS</div>'
                     f'<div class="measure" data-tag="c_head2" style="position:absolute;left:{(W - w2) / 2}px;top:{hy + 118}px;font-family:var(--d);font-weight:400;'
                     f'font-size:80px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">TO SHOW UP</div>')
        el("c_head1", (W - w1) / 2, hy + 10, w1, 100); el("c_head2", (W - w2) / 2, hy + 128, w2, 64)

    # ---- slab with content (flex-centred: no border-offset arithmetic) ----
    if kind == "cover":
        body = (f'<div style="font-weight:900;font-size:60px;line-height:1">TERRATHON</div>'
                f'<div style="font-weight:900;font-size:118px;line-height:1">MINI-FETE</div>'
                f'<div style="font-weight:400;font-size:38px;line-height:1.15;margin-top:8px">{DATE}</div>')
    elif kind == "point":
        head_px = 100 * min(1.0, 840 / m[0]["text_w"]); head_px = min(head_px, 104)
        body = (f'<div style="font-weight:900;font-size:{head_px}px;line-height:1">{head.replace("&", "&amp;")}</div>'
                f'<div style="font-weight:400;font-size:40px;line-height:1.15;margin-top:18px;max-width:800px;text-wrap:balance">{tag}</div>')
    else:
        cf = 96 * min(1.0, 800 / m[0]["text_w"])
        body = (f'<div style="font-weight:900;font-size:{cf}px;line-height:1">JOIN THE</div>'
                f'<div style="font-weight:900;font-size:{cf}px;line-height:1">WHATSAPP GROUP</div>'
                f'<div style="font-weight:400;font-size:40px;line-height:1.15;margin-top:16px">LINK IN BIO</div>')
    el("slab", SX - 6, slab_top - 12, SW + 12, slab_h + 24)
    parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{slab_top}px;width:{SW}px;height:{slab_h}px;'
                 f'transform:rotate(-1.25deg);background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;display:flex;flex-direction:column;'
                 f'align-items:center;justify-content:center;text-align:center;font-family:var(--d);color:{INK};white-space:nowrap">{body}</div>')

    # ---- strip under the slab ----
    strip = {"cover": "SWIPE FOR THE 7", "point": f"{DATE}  |  {VENUE}", "close": f"{DATE}  |  {VENUE}"}[kind]
    sfs = 34 if kind == "point" or kind == "close" else 44
    sm = await B.measure_text([dict(text=strip, font="d", size=sfs, weight=400)])
    sw_ = sm[0]["text_w"]
    if sw_ > 960: sfs *= 960 / sw_; sw_ = 960
    SY_ = L["cover_strip_y"] if kind == "cover" else L["strip_y"]
    parts.append(f'<div class="measure" data-tag="strip" style="position:absolute;left:{(W - sw_) / 2}px;top:{SY_}px;font-family:var(--d);'
                 f'font-weight:400;font-size:{sfs}px;line-height:1;color:{WHITE};white-space:nowrap;z-index:6">{strip.replace("&", "&amp;")}</div>')
    el("strip", (W - sw_) / 2, SY_ + 2, sw_, sfs * 0.81)

    # ---- footer: AQ logo + ALL FOR CHARITY ----
    fy = L["foot_y"]
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{fy + 6}px;height:56px;z-index:9">')
    el("logo", 27, fy + 6, 320, 56)
    cw, chh, cx_ = 337, 67, 720
    el("cta", cx_, fy, cw, chh)
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx_}px;top:{fy}px;width:{cw}px;height:{chh}px;border:6px solid {ORCHID};'
                 f'border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);'
                 f'font-weight:900;font-size:26px;color:{INK}">ALL FOR CHARITY</div>')

    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("strip", WHITE, GROUND, 30, False), ("slab", INK, SLAB, 40, False),
                  ("cta", INK, CTA_FILL, 26, True), ("pill", INK, "#FFFFFF", 31, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND,
                   expect_hero=True, collision_ignore={("hero", "slab"), ("star_ml", "slab"), ("star_br", "slab"), ("star_tr", "hero")}, margin=12)


async def main(canvases):
    async with B.session():
        for canvas in canvases:
            d = f"out/versions/terrathon_carousel/{canvas}"; os.makedirs(d, exist_ok=True)
            await slide("cover", canvas, f"{d}/00_cover.png")
            for i, (key, _, _) in enumerate(REASONS):
                await slide("point", canvas, f"{d}/{i + 1:02d}_{key}.png", idx=i)
            await slide("close", canvas, f"{d}/{N + 1:02d}_close.png")
            print("done", canvas)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or ["feed", "story"]))
