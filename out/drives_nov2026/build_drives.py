"""AQ DRIVES CAROUSEL BUILDER, v2 (Nov 2026 batch). ONE shared builder, per-drive content in jobs_drives.py.

Built on the aq-photo-carousel skill helpers (.claude/skills/aq-photo-carousel/scripts/build_carousel.py:
logo, dots, scrims, vision-driven doodles). v2 follows user direction: PHOTO is the focus (large photo
area, no dark dead space, little caption chrome), no closing slide, cooler graphics from the engine's
own vocabulary (shapes.py / tex.py / doodles.py).

MECHANISMS (one per drive, chosen from brain/VISUAL_DNA.md vocabulary; design.py draws were consulted but
returned the same two-slab recipe for three subjects, so the mechanism is assigned per drive by hand):
  tape    cream ground, photo as a tilted card with ink outline + hard shadow, a mint cut-paper plate
          behind it, two torn tape strips, a die-cut starburst sticker.            (876, 902, 905)
  slab    cream ground, photo in a 32px rounded slab, mint slab peeking out offset behind it (notched-
          slab family), staggered word pills overlapping the slab edge on the cover.      (878, 903)
  bleed   full-bleed photo, bottom halftone dot screen (halftone belongs on PHOTOS, so it is legal),
          cream caption slab, staggered word-pill title, sticker swarm (starburst + location chip) and
          vision-placed doodles.                                                          (877, 901, 904)
Not used: duotone / riso photo (children's faces must stay natural) and torn edges (no free edge to tear).

ADAPTATIONS vs the recipes (precedence ladder, CLAUDE.md section 2): hard brand rules win. Welfare mint is
the only structural accent (accent_for('welfare')); a 2nd/3rd hue (lemon pill, sky doodle) is punctuation,
so the "N colours" counts are a target not a ceiling. Display type is NeutralFace caps; no serif used. Hard ink
outline/offset shadow appears on card, pills and stickers only (the craft layer, section 9).

KEPT FROM v1: landscape photos are never cropped to a 4:5 sliver: in `tape` they sit in a card
cropped to 972x900 with a focus point (still 67% of a 16:9 frame) instead of a blurred band; truthful
"N volunteers" sticker; no printed dates; measured exclusion boxes for hair; 'volunteers' never
'unique volunteers'; all copy from drives.json.
"""
import asyncio, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
_r = HERE
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
REPO = _r
_spec = importlib.util.spec_from_file_location(
    "bc", os.path.join(REPO, ".claude/skills/aq-photo-carousel/scripts/build_carousel.py"))
bc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bc)   # also chdirs to REPO
core, B, lay, vision = bc.core, bc.B, bc.lay, bc.vision
sys.path.insert(0, os.path.join(REPO, "engine"))
shapes = bc.load("shapes"); tex = bc.load("tex")
from PIL import Image, ImageOps

W, H, M = bc.W, bc.H, bc.M
SC = 2
MINT = core.accent_for("welfare")
MINTBRIGHT = "#00E5A0"
LEMON = core.ACCENTS[2]
INK = core.INK
OUT_ROOT = os.path.join(REPO, "out/drives_nov2026")
BASE_DIR = os.path.join(OUT_ROOT, "_base")
CAPTION_INK = core.on_cream(MINT, 26)

bc.slide_accent = lambda seed: MINT
bc.ACCENT_ORDER = [1, 2, 4, 1, 6, 2, 4]
bc.DOODLE_EXTRA = {0: MINTBRIGHT, 3: MINTBRIGHT}

CX, CW = 54, 972            # photo card geometry (tape / slab)


def fit_img(src, w, h, focus, out):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ImageOps.fit(im, (w * SC, h * SC), Image.LANCZOS, centering=focus).save(out, quality=90)
    return out


async def tw(text, font, size, weight, ls=0):
    r = (await B.measure_text([dict(text=text, font=font, size=size, weight=weight, letter_spacing=ls)]))[0]
    return r["text_w"]


async def fit_title(lines_html, max_w, max_size=96, min_size=54):
    ws = [await tw(l.replace("&amp;", "&"), "d", 100, 900) for l in lines_html.split("<br>")]
    return max(min_size, min(max_size, int(100 * max_w / max(ws))))


def footer(loc, dark_bg):
    col = "#FFFFFF" if dark_bg else INK
    sh = "text-shadow:0 2px 6px rgba(0,0,0,.55);" if dark_bg else ""
    return (f'<div style="position:absolute;bottom:40px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:{col};{sh}">@ngo.aquaterra '
            f'<span style="opacity:.75;font-weight:500">&middot; {loc}</span></div>')


def ink_dots(n, active, y=62):
    out = f'<div style="position:absolute;top:{y}px;right:{M}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        c = MINT if i == active else "rgba(10,10,10,.22)"
        b = f"border:2px solid {INK};" if i == active else ""
        out += f'<span style="width:10px;height:10px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"


def starburst_sticker(n, x, y, size=220, rot=-9):
    """Die-cut starburst with the TRUE volunteer count. Label is HTML over the svg (text fits by construction)."""
    ink = core.text_on(MINT)
    svg = shapes.sticker(shapes.starburst(14, 48, 38), MINT, size=size, shadow=True, rot=rot, detail="none")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:24">{svg}'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;'
            f'justify-content:center;transform:rotate({rot}deg);color:{ink}">'
            f'<span style="font-family:var(--d);font-weight:900;font-size:{round(size*.30)}px;line-height:.9">{n}</span>'
            f'<span style="font-family:var(--m);font-weight:700;font-size:{round(size*.06)}px;'
            f'letter-spacing:.06em;margin-top:3px">volunteers</span></div></div>')


def pill(text, accent, x, y, fs, rot):
    fg = core.text_on(accent)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;background:{accent};color:{fg};'
            f'border:4px solid {INK};border-radius:14px;padding:6px 22px;box-shadow:6px 6px 0 {INK};'
            f'font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:1;text-transform:uppercase;'
            f'white-space:nowrap;transform:rotate({rot}deg);z-index:22">{text}</div>')


async def pills_block(title_html, x0, bottom_y, max_w):
    """Staggered word pills stacked UP from bottom_y. Returns (html, boxes, top_y)."""
    words = title_html.replace("<br>", " ").replace("&amp;", "&").split()
    fs = 70
    while True:
        ws = [await tw(w, "d", fs, 900) for w in words]
        if max(ws) + 52 + 8 + 52 <= max_w or fs <= 44:
            break
        fs -= 4
    accents = [MINT, "#FFFFFF" if False else core.CREAM, LEMON]
    html, boxes = "", []
    h = fs + 12 + 8
    y = bottom_y - h
    for i, w_ in reversed(list(enumerate(words))):
        wpx = ws[i] + 44 + 8
        x = x0 + (i % 3) * 30
        html += pill(w_, accents[i % 3], x, y, fs, -2 if i % 2 == 0 else 2)
        boxes.append((f"pill{i}", x, y, wpx + 6, h + 6))
        y -= h + 14
    return html, boxes, y + h + 14


def caption_slab(txt, bottom, max_w=820):
    return (f'<div style="position:absolute;left:{M}px;bottom:{bottom}px;z-index:21;max-width:{max_w}px;'
            f'background:{core.CREAM};color:{INK};border:3px solid {INK};border-radius:22px;'
            f'padding:12px 20px;box-shadow:4px 4px 0 {INK};font-family:var(--e);font-weight:500;'
            f'font-size:21px;line-height:1.3">{txt}</div>')


# ---------------------------------------------------------------------------------- layouts
async def render_bleed(drive, role, idx, total, spec, out_png, seed):
    base = fit_img(os.path.join(HERE, "_src", str(drive["post_id"]), spec["file"]), W, H,
                   spec.get("focus", (0.5, 0.4)), os.path.join(BASE_DIR, f'{drive["post_id"]}_{idx}.jpg'))
    ex = bc.EXCLUDE + list(spec.get("exclude") or [])
    ex = [e for e in ex if e != (0, H - 300, W, 300)] + [(0, H - 380, W, 380)]
    fillers, fboxes = bc.filler_from_vision(base, seed, n=3, exclude=ex)
    el = list(fboxes)
    halftone = (f'<div style="position:absolute;left:0;right:0;bottom:0;height:420px;z-index:10;'
                f'background:linear-gradient(to top,rgba(0,0,0,.62),rgba(0,0,0,0));"></div>'
                f'<div style="position:absolute;left:0;right:0;bottom:0;height:300px;z-index:11;'
                f'{tex.halftone(color="#0A0A0A", size=7, opacity=.5)}'
                f'-webkit-mask-image:linear-gradient(to top,#000,transparent);'
                f'mask-image:linear-gradient(to top,#000,transparent)"></div>')
    inner = bc.full_bleed_photo(bc.photo_b64(base)) + bc.scrim_top(220) + halftone
    inner += bc.logo_pill() + bc.dots(total, idx - 1, accent=MINT, y=70) + fillers
    el.append(("logo", M, 48, 260, 56))
    if role == "cover":
        sub_h = (await B.measure_text([dict(text=drive["subhead"], font="e", size=21, weight=500,
                                            max_width=780)]))[0]["h"] + 24 + 6
        inner += caption_slab(drive["subhead"], 84, 820)
        el.append(("subhead", M, H - 84 - sub_h, 820, sub_h))
        phtml, pbox, ptop = await pills_block(drive["title_html"], M, H - 84 - sub_h - 22, 960)
        inner += phtml; el += pbox
        sx, sy = spec.get("stick", (W - M - 215, 120))
        inner += starburst_sticker(drive["volunteers"], sx, sy)
        el.append(("sticker", sx, sy, 220, 220))
        if drive.get("swarm"):
            chip = drive["loc"].upper()
            cw = await tw(chip, "m", 13, 700, 1.0) + 36
            cx_, cy_ = W - M - round(cw), sy + 235
            inner += bc.sticker(chip, LEMON, cx_, cy_, rot=3)
            el.append(("chip", cx_, cy_, round(cw), 34))
    else:
        c = (await B.measure_text([dict(text=spec["cap"], font="e", size=21, weight=500, max_width=780)]))[0]
        inner += caption_slab(spec["cap"], 84)
        el.append(("caption", M, H - 84 - c["h"] - 30, 820, c["h"] + 30))
    inner += footer(drive["loc"], True)
    el.append(("footer", M, H - 58, 420, 20))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    ign = {("sticker", "chip"), ("chip", "sticker")}
    await B.render(html, out_png, W, H, elements=el, page_bg="var(--bg)", collision_ignore=ign,
                   text_pairs=[("footer", "#FFFFFF", "#101010", 13, True)])


async def render_card(drive, role, idx, total, spec, out_png, seed, kind):
    slab = kind == "slab"
    CY = 150
    CH = 800 if role == "cover" else 980
    img = fit_img(os.path.join(HERE, "_src", str(drive["post_id"]), spec["file"]), CW, CH,
                  spec.get("focus", (0.5, 0.4)), os.path.join(BASE_DIR, f'{drive["post_id"]}_{idx}.jpg'))
    el = []
    rad = 32 if slab else 22
    rot = 0 if slab else (-1.2 if idx % 2 else 1.0)
    plate_rot = 0 if slab else -rot * 1.4
    inner = (f'<div style="position:absolute;inset:0;{tex.paper_fibre(opacity=.05)}"></div>')
    # plate: solid mint cut paper behind the card (offset = the notched-slab / riso-misregister move)
    off = 22 if slab else 16
    inner += tex.cutpaper(CX + off, CY + off, CW, CH, MINT, rot=plate_rot, z=3, shadow=0, radius=f"{rad}px",
                          outline=None)
    inner += (f'<img src="{bc.photo_b64(img)}" style="position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;'
              f'height:{CH}px;object-fit:cover;border:{3 if slab else 4}px solid {INK};border-radius:{rad}px;'
              f'transform:rotate({rot}deg);z-index:5;'
              f'{"" if slab else f"box-shadow:8px 8px 0 {INK};"}">')
    el.append(("card", CX, CY, CW, CH))
    if not slab:
        inner += tex.tape(CX + 50, CY - 24, 150, 44, rot=-9, color="#F2E9C9", z=30)
        inner += tex.tape(CX + CW - 200, CY - 20, 150, 44, rot=8, color="#F2E9C9", z=30)
    inner += bc.logo_pill() + ink_dots(total, idx - 1)
    el.append(("logo", M, 48, 260, 56))
    ty = CY + CH + 48
    if role == "cover":
        fs = await fit_title(drive["title_html"], 760)
        n = drive["title_html"].count("<br>") + 1
        th = round(n * fs * 0.92)
        inner += (f'<div style="position:absolute;top:{ty}px;left:{M}px;z-index:20;font-family:var(--d);'
                  f'font-weight:900;font-size:{fs}px;line-height:.92;text-transform:uppercase;color:{INK}">'
                  f'{drive["title_html"]}</div>')
        for k, l in enumerate(drive["title_html"].split("<br>")):
            lw = await tw(l.replace("&amp;", "&"), "d", fs, 900)
            el.append((f"title{k}", M, ty + round(k * fs * .92), round(lw), round(fs * .92)))
        sy_ = ty + th + 14
        sm = (await B.measure_text([dict(text=drive["subhead"], font="e", size=19, weight=500, max_width=760)]))[0]
        inner += (f'<div style="position:absolute;top:{sy_}px;left:{M}px;width:760px;z-index:20;display:flex;gap:12px">'
                  f'<span style="width:18px;height:4px;background:{MINT};border:2px solid {INK};margin-top:10px;flex:none"></span>'
                  f'<span style="font-family:var(--e);font-weight:500;font-size:19px;line-height:1.35;color:{INK}">'
                  f'{drive["subhead"]}</span></div>')
        el.append(("subhead", M + 30, sy_, 730, sm["h"]))
        sx, sy = (W - M - 215, CY + CH - 170)
        inner += starburst_sticker(drive["volunteers"], sx, sy)
        el.append(("sticker", sx, sy, 220, 220))
    else:
        c = (await B.measure_text([dict(text=spec["cap"], font="e", size=28, weight=500, max_width=720)]))[0]
        inner += (f'<div style="position:absolute;top:{ty}px;left:{M}px;width:720px;z-index:20;display:flex;gap:14px">'
                  f'<span style="width:22px;height:5px;background:{MINT};border:2px solid {INK};margin-top:15px;flex:none"></span>'
                  f'<span style="font-family:var(--e);font-weight:500;font-size:28px;line-height:1.3;color:{INK}">'
                  f'{spec["cap"]}</span></div>')
        el.append(("caption", M + 36, ty, 684, c["h"]))
    # doodles in the cream zone, right of the text (text is held to 760px)
    for i, (dx, dy, sz) in enumerate([(870, ty - 6, 84), (960, ty + 96, 50)]):
        kind_ = bc.VOCAB[(seed * 3 + i * 5) % len(bc.VOCAB)]
        rung = (seed + i) % len(bc.ACCENT_ORDER)
        col = bc.DOODLE_EXTRA.get(rung, bc.A[bc.ACCENT_ORDER[rung]])
        if col == MINT: col = MINTBRIGHT
        inner += bc.one(kind_, dx, dy, sz, col, rot=((seed * 29 + i * 47) % 60) - 30)
        el.append((f"doodle{i}", dx, dy, sz, sz))
    inner += footer(drive["loc"], False)
    el.append(("footer", M, H - 58, 420, 20))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    ign = {("sticker", "card")}
    await B.render(html, out_png, W, H, elements=el, page_bg="var(--bg)", collision_ignore=ign,
                   containers=(),
                   text_pairs=[("caption", INK, "#F4EFE0", 28, False), ("footer", INK, "#F4EFE0", 13, True)])


async def build(drive, only=None):
    d = os.path.join(OUT_ROOT, f'{drive["post_id"]}_{drive["slug"]}')
    os.makedirs(d, exist_ok=True)
    photos = [drive["cover"]] + drive["slides"]
    total = len(photos)
    for i, p in enumerate(photos, start=1):
        if only and i not in only:
            continue
        role = "cover" if i == 1 else "slide"
        out = os.path.join(d, f"slide_{i}.png")
        if drive["style"] == "bleed":
            await render_bleed(drive, role, i, total, p, out, drive["seed"] + i)
        else:
            await render_card(drive, role, i, total, p, out, drive["seed"] + i, drive["style"])
    with open(os.path.join(d, "caption.txt"), "w") as f:
        f.write(drive["caption"].strip() + "\n")
    print(f'  -> {d} ({total} slides, {drive["style"]})')


async def main(ids=None, only=None):
    sys.path.insert(0, HERE)
    from jobs_drives import DRIVES
    async with B.session():
        for dr in DRIVES:
            if ids and str(dr["post_id"]) not in ids:
                continue
            await build(dr, only=only)


if __name__ == "__main__":
    ids = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] != "all" else None
    only = {int(x) for x in sys.argv[2].split(",")} if len(sys.argv) > 2 else None
    asyncio.run(main(ids, only))
