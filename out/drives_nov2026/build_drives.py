"""AQ DRIVES CAROUSEL BUILDER (Nov 2026 batch) - ONE shared builder, per-drive content in jobs_drives.py.

Built on the aq-photo-carousel skill helpers (.claude/skills/aq-photo-carousel/scripts/build_carousel.py:
logo, dots, scrims, vision-driven doodles, truthful index tag). What this file adds, each as a RULE:

  * welfare accent: every large/structural colour is core.accent_for('welfare') (mint). The skill's
    cool rotation is overridden; doodles keep a small contrasting rung (lemon/sky) as punctuation.
  * BASE-IMAGE COMPOSITION: every slide's photo is pre-composed with PIL into a 1080x1350 (2x) base so
    vision.plan_spots measures what is really on screen. Two fits:
      - "cover": object-fit cover with a per-photo focus (centering) so faces/subject stay clear of the
        bottom text zone. Narrow phone portraits (dogs) are focused so the subject sits in the upper
        part of the frame, above the cover title.
      - "band":  LANDSCAPE photos are NOT cropped to a 4:5 sliver (a 16:9 frame would lose 55% of
        its width and upscale 2x). They run full-width as a band over a blurred, darkened copy of
        themselves, so every face survives.
  * no dates on slides: the JSON gives a *posted* date, not the date the drive happened, so printing
    one would assert a fact the data does not hold.
  * 'volunteers' never 'unique volunteers'.
  * the closer is a cream type slide (AQUATERRA + @ngo.aquaterra), sized from MEASURED text.
"""
import asyncio, json, os, sys, importlib.util, math

HERE = os.path.dirname(os.path.abspath(__file__))
_r = HERE
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
REPO = _r
_spec = importlib.util.spec_from_file_location(
    "bc", os.path.join(REPO, ".claude/skills/aq-photo-carousel/scripts/build_carousel.py"))
bc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bc)   # also chdirs to REPO
core, B, lay, vision = bc.core, bc.B, bc.lay, bc.vision
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

W, H, M = bc.W, bc.H, bc.M
SC = 2                                       # base images at 2x, like the PNG output
MINT = core.accent_for("welfare")            # semantic dept colour (A[1])
MINTBRIGHT = "#00E5A0"
OUT_ROOT = os.path.join(REPO, "out/drives_nov2026")
BASE_DIR = os.path.join(OUT_ROOT, "_base")

# --- override the skill's cool rotation: large areas = welfare mint, punctuation = small contrast rung
bc.slide_accent = lambda seed: MINT
bc.ACCENT_ORDER = [1, 2, 4, 1, 6, 2, 4]      # mint, lemon, sky, mint, teal, lemon, sky
bc.DOODLE_EXTRA = {0: MINTBRIGHT, 3: MINTBRIGHT}


def accent_text_on_dark(size=15):
    return core.on_dark(MINT, size)


# ----------------------------------------------------------------------------- base images
def compose_base(src, fit, focus, role, out):
    """Pre-compose the photo into the slide's 1080x1350 base (saved at 2x)."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    cw, ch = W * SC, H * SC
    if fit == "cover":
        base = ImageOps.fit(im, (cw, ch), Image.LANCZOS, centering=focus)
    elif fit == "band":
        bg = ImageOps.fit(im, (cw, ch), Image.LANCZOS, centering=(0.5, 0.5)).filter(ImageFilter.GaussianBlur(60))
        bg = ImageEnhance.Brightness(bg).enhance(0.42)
        bh = round(cw * im.height / im.width)
        band = im.resize((cw, bh), Image.LANCZOS)
        if role == "cover":           # title block owns the bottom ~520px
            avail_top, avail_bot = 150 * SC, (H - 540) * SC
        else:                         # caption + footer own the bottom ~290px
            avail_top, avail_bot = 150 * SC, (H - 300) * SC
        y = avail_top + max(0, (avail_bot - avail_top - bh) // 2)
        base = bg
        base.paste(band, (0, y))
    else:
        raise ValueError(fit)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.save(out, quality=90)
    return out


# ----------------------------------------------------------------------------- text helpers
def footer(loc):
    return (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:#FFFFFF;'
            f'text-shadow:0 2px 6px rgba(0,0,0,.5)">@ngo.aquaterra '
            f'<span style="opacity:.75;font-weight:500">&middot; {loc}</span></div>')


async def fit_title(lines_html, max_size=88, min_size=54):
    """Largest display size at which EVERY title line fits the 952px measure (measured, not guessed)."""
    lines = lines_html.split("<br>")
    res = await B.measure_text([dict(text=l.replace("&amp;", "&"), font="d", size=100, weight=900)
                                for l in lines])
    widest = max(r["text_w"] for r in res)
    return max(min_size, min(max_size, int(100 * (W - 2 * M) / widest)))


async def measure_block(text, font, size, weight, max_w, ls=0):
    r = (await B.measure_text([dict(text=text, font=font, size=size, weight=weight,
                                    max_width=max_w, letter_spacing=ls)]))[0]
    return r


# ----------------------------------------------------------------------------- slides
async def render_photo(drive, role, base_img, idx, total, out_png, seed, cap=None, extra_exclude=None):
    accent = MINT
    ex = bc.EXCLUDE + list(extra_exclude or [])
    if role == "cover":
        ex.append((40, 112, 760, 40))      # the kicker line is real UI: doodles must not land on it
    fillers, fboxes = bc.filler_from_vision(base_img, seed, n=4, exclude=ex)
    el = list(fboxes)
    inner = bc.full_bleed_photo(bc.photo_b64(base_img))
    if role == "cover":
        inner += bc.scrim_top(340, tint=accent) + bc.scrim_bottom(560, tint=accent)
    else:
        inner += bc.scrim_bottom(300 if cap else 170, tint=accent)
    inner += bc.logo_pill() + bc.dots(total, idx - 1, accent=accent) + fillers
    el.append(("logo", M, 48, 260, 56))
    if not fboxes:
        # RULE (vision starved a busy street photo to 0 spots): never ship a slide with no craft
        # layer. Fall back to a TRUTHFUL sticker (the volunteer count from the data), placed in a
        # known-safe strip: above the title on the right of a cover, in the dark scrim band on a slide.
        sx, sy = (W - M - 190, 900) if role == "cover" else (M, H - 250)
        inner += bc.sticker(f'{drive["volunteers"]} volunteers', MINT, sx, sy, rot=-3)
        el.append(("sticker", sx, sy, 190, 36))

    if role == "cover":
        loc = drive["loc"].upper()
        vol = f'{drive["volunteers"]} VOLUNTEERS'
        inner += (f'<div style="position:absolute;top:120px;left:{M}px;z-index:20;font-family:var(--m);'
                  f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;'
                  f'color:{MINTBRIGHT};display:inline-flex;align-items:center;gap:10px;'
                  f'background:rgba(8,12,10,.62);padding:7px 14px 7px 12px;border-radius:999px;margin-left:-12px">'
                  f'<span style="width:10px;height:10px;border-radius:50%;background:{accent}"></span>'
                  f'{loc} &middot; {vol}</div>')
        el.append(("kicker", M - 12, 112, 700, 38))
        size = await fit_title(drive["title_html"])
        nlines = drive["title_html"].count("<br>") + 1
        sub = await measure_block(drive["subhead"], "e", 20, 500, 820)
        sub_h = sub["h"]
        sub_bottom = 150
        title_bottom = sub_bottom + sub_h + 30
        title_h = round(nlines * size * 0.92)
        title_y = H - title_bottom - title_h
        inner += (f'<div style="position:absolute;bottom:{title_bottom}px;left:{M}px;right:{M}px;z-index:20;'
                  f'font-family:var(--d);font-weight:900;font-size:{size}px;line-height:.92;'
                  f'text-transform:uppercase;color:#FFFFFF;text-shadow:0 4px 14px rgba(0,0,0,.55)">'
                  f'{drive["title_html"]}</div>')
        # per-line boxes (a multi-line headline as ONE box is ~60% air)
        for k, l in enumerate(drive["title_html"].split("<br>")):
            lw = (await B.measure_text([dict(text=l.replace("&amp;", "&"), font="d", size=size, weight=900)]))[0]
            el.append((f"title{k}", M, title_y + round(k * size * 0.92), round(lw["text_w"]), round(size * 0.92)))
        inner += (f'<div style="position:absolute;bottom:{sub_bottom}px;left:{M}px;right:{M}px;z-index:20;'
                  f'display:flex;align-items:flex-start;gap:12px">'
                  f'<span style="width:18px;height:3px;background:{accent};margin-top:11px;flex:none"></span>'
                  f'<span style="font-family:var(--e);font-weight:500;font-size:20px;line-height:1.35;'
                  f'color:rgba(255,255,255,.94);text-shadow:0 2px 6px rgba(0,0,0,.45);max-width:820px">'
                  f'{drive["subhead"]}</span></div>')
        el.append(("subhead", M + 30, H - sub_bottom - sub_h, round(sub["text_w"]) if sub["lines"] == 1 else 820, sub_h))
    else:
        inner += bc.index_tag(idx, total, accent)
        el.append(("index", W - M - 90, H - 140 - 26, 90, 26))
        if cap:
            inner += bc.caption(cap, accent)
            c = await measure_block(cap, "e", 19, 500, 820)
            el.append(("caption", M + 30, H - 100 - c["h"], 820, c["h"]))
    inner += footer(drive["loc"])
    el.append(("footer", M, H - 70, 420, 20))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    await B.render(html, out_png, W, H, elements=el, page_bg="var(--bg)",
                   text_pairs=[("footer", "#FFFFFF", "#101010", 13, True)])


async def render_closer(drive, idx, total, out_png, seed):
    accent = MINT
    el = []
    hero_txt = "AQUATERRA"
    r = await B.measure_text([dict(text=hero_txt, font="d", size=100, weight=900)])
    fs = min(190, int(100 * (W - 2 * M) / r[0]["text_w"]))
    hr = (await B.measure_text([dict(text=hero_txt, font="d", size=fs, weight=900)]))[0]
    KICK_Y, HERO_Y = 290, 344
    hero_h = round(fs * 0.92)
    inner = ""   # page ground is already var(--bg); an explicit cream div on it is an invisible fill
    kick = f'{drive["loc"].upper()} &middot; {drive["volunteers"]} VOLUNTEERS'
    inner += (f'<div style="position:absolute;top:{KICK_Y}px;left:{M}px;z-index:6;font-family:var(--m);'
              f'font-weight:700;font-size:15px;letter-spacing:.18em;text-transform:uppercase;'
              f'color:var(--ink)">{kick}</div>')
    kw = (await B.measure_text([dict(text=kick, font="m", size=15, weight=700, letter_spacing=2.7)]))[0]
    el.append(("kicker", M, KICK_Y, round(kw["text_w"]), 22))
    inner += (f'<div style="position:absolute;top:{HERO_Y}px;left:{M}px;z-index:6;font-family:var(--d);'
              f'font-weight:900;font-size:{fs}px;line-height:.92;text-transform:uppercase;'
              f'color:var(--ink)">{hero_txt}</div>')
    el.append(("hero", M, HERO_Y, round(hr["text_w"]), hero_h))
    body = f'{drive["volunteers"]} volunteers showed up. come once, decide after.'
    BODY_Y = HERO_Y + hero_h + 52
    bm = await measure_block(body, "e", 26, 500, 760)
    inner += (f'<div style="position:absolute;top:{BODY_Y}px;left:{M}px;width:760px;z-index:6;'
              f'display:flex;align-items:flex-start;gap:14px">'
              f'<span style="width:26px;height:4px;background:{accent};margin-top:14px;flex:none;'
              f'border:2px solid var(--ink)"></span>'
              f'<span style="font-family:var(--e);font-weight:500;font-size:26px;line-height:1.4;'
              f'color:var(--ink)">{body}</span></div>')
    el.append(("body", M + 40, BODY_Y, 720, bm["h"]))
    FIELD_Y, FIELD_W, FIELD_H = H - 600, 640, 380
    inner += (f'<div style="position:absolute;top:{FIELD_Y}px;right:0;width:{FIELD_W}px;height:{FIELD_H}px;'
              f'background:{accent};border-left:5px solid var(--ink);border-top:5px solid var(--ink);'
              f'border-bottom:5px solid var(--ink);z-index:2"></div>')
    el.append(("accent_field", W - FIELD_W, FIELD_Y, FIELD_W, FIELD_H))
    ink = core.text_on(accent)
    inner += (f'<div style="position:absolute;top:{FIELD_Y + 5}px;right:0;width:{FIELD_W - 5}px;height:{FIELD_H - 10}px;'
              f'z-index:5;display:flex;flex-direction:column;justify-content:center;gap:14px;padding-left:44px;'
              f'box-sizing:border-box">'
              f'<span style="font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.18em;'
              f'text-transform:uppercase;color:{ink}">follow along</span>'
              f'<span style="font-family:var(--m);font-weight:700;font-size:40px;color:{ink}">@ngo.aquaterra</span>'
              f'</div>')
    hm = (await B.measure_text([dict(text="@ngo.aquaterra", font="m", size=40, weight=700)]))[0]
    assert 44 + hm["text_w"] < FIELD_W - 20, "handle does not fit its block"
    spots = [(M, FIELD_Y + 40, 110, 0), (M + 130, FIELD_Y + 250, 64, 2), (M + 210, FIELD_Y + 50, 72, 4),
             (M + 290, FIELD_Y + 230, 50, 1)]   # every spot ends before the block's left edge (W-640=440)
    for i, (sx, sy, sz, ai) in enumerate(spots):
        kind = bc.VOCAB[(seed * 3 + i * 5) % len(bc.VOCAB)]
        rung = (seed + ai) % len(bc.ACCENT_ORDER)
        col = bc.DOODLE_EXTRA.get(rung, bc.A[bc.ACCENT_ORDER[rung]])
        if col == MINT:
            col = MINTBRIGHT
        inner += bc.one(kind, sx, sy, sz, col, rot=((seed * 29 + i * 47) % 60) - 30)
        el.append((f"doodle{i}", sx, sy, sz, sz))
    inner += bc.logo_pill() + bc.dots(total, idx - 1, accent=accent) + bc.index_tag(idx, total, accent)
    el.append(("logo", M, 48, 260, 56))
    inner += (f'<div style="position:absolute;bottom:52px;left:{M}px;z-index:20;font-family:var(--m);'
              f'font-weight:700;font-size:13px;letter-spacing:.06em;color:var(--ink)">@ngo.aquaterra '
              f'<span style="opacity:.6;font-weight:500">&middot; {drive["loc"]}</span></div>')
    el.append(("footer", M, H - 70, 420, 20))
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    await B.render(html, out_png, W, H, elements=el, page_bg="var(--bg)",
                   color_pairs=[("accent_field", accent, "var(--bg)", True)],
                   containers=("accent_field",),
                   text_pairs=[("body", core.INK, "var(--bg)", 26, False),
                               ("kicker", core.INK, "var(--bg)", 15, True),
                               ("handle", ink, accent, 40, True)])


async def build(drive, only=None):
    d = os.path.join(OUT_ROOT, f'{drive["post_id"]}_{drive["slug"]}')
    os.makedirs(d, exist_ok=True)
    photos = [drive["cover"]] + drive["slides"]
    total = len(photos) + 1
    seed = drive["seed"]
    for i, p in enumerate(photos, start=1):
        if only and i not in only:
            continue
        role = "cover" if i == 1 else "slide"
        base = compose_base(os.path.join(HERE, "_src", str(drive["post_id"]), p["file"]),
                            p.get("fit", "cover"), p.get("focus", (0.5, 0.5)), role,
                            os.path.join(BASE_DIR, f'{drive["post_id"]}_{i}.jpg'))
        await render_photo(drive, role, base, i, total, os.path.join(d, f"slide_{i}.png"), seed + i,
                           cap=p.get("cap"), extra_exclude=p.get("exclude"))
    if not only or total in only:
        await render_closer(drive, total, total, os.path.join(d, f"slide_{total}.png"), seed + total)
    with open(os.path.join(d, "caption.txt"), "w") as f:
        f.write(drive["caption"].strip() + "\n")
    print(f'  -> {d} ({total} slides)')


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
