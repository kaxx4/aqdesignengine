"""Story HIGHLIGHT kit: one themed circle cover + 10-15 photo story slides per event.

A FORMAT MODULE (same shape as dispatch.py / discodiwali.py): the only hand-input is an event
name, a year and a list of photo paths. Theme, cover, template order and slide count are decided
here by rule.

  import highlights as H
  await H.build_event("Paradox 2026", "Paradox", "2026", photos, out_dir)

Canvas is the 1080x1920 story. Instagram draws its own UI over the top ~250px and bottom ~250px,
and crops a highlight cover to a circle centred on the canvas, so:
  - the logo sits at y=130 (below the profile bar)
  - everything that must survive on a cover lives inside the central circle (diameter 760)

Six slide templates, cycled by SEQUENCE so no two neighbours match:
  full      full-bleed photo, scrim, event chip + title
  polaroid  tilted white-border photo on the themed ground, hard shadow
  arch      arch-windowed photo over a giant outlined event word
  duo       two offset cards (uses 2 photos)
  strip     three-frame film strip (uses 3 photos)
  round     big circular photo with a ring and a sticker
A slide that wants k photos but has fewer left falls back to a 1-photo template, so a thin folder
yields a SHORTER highlight instead of a padded one (real-assets-only, CLAUDE.md section 9).
"""
import asyncio, base64, io, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)


def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = _load("core"); B = _load("build"); dd = _load("doodles")
A = core.ACCENTS
W, H = core.SIZES["story"]
M = 64
MIN_SLIDES, MAX_SLIDES = 10, 15

# --- THEMES ---------------------------------------------------------------------------------
# ground = canvas colour, disc = cover circle fill, accent = chip/sticker, glyph = doodle on cover.
# A dark ground flips type and outlines to cream.
THEMES = {
    "paradox":        dict(ground=A[4], disc="#F4EFE0", accent=A[2], glyph="burst",     dark=False),
    "terrathon":      dict(ground=A[6], disc="#F4EFE0", accent=A[2], glyph="lightning", dark=False),
    "starry_night":   dict(ground="#0B1030", disc=A[2], accent=A[4], glyph="sparkle",   dark=True),
    "merry_miracles": dict(ground=A[1], disc="#F4EFE0", accent=A[3], glyph="tree",      dark=False),
    "disco_diwali":   dict(ground="#0A0A0A", disc="#C98B3D", accent=A[0], glyph="star", dark=True),
    "anniversary":    dict(ground=A[0], disc="#F4EFE0", accent=A[2], glyph="heart",     dark=False),
    "fundraiser":     dict(ground=A[2], disc="#F4EFE0", accent=A[5], glyph="thumbsup",  dark=False),
    "fete":           dict(ground=A[5], disc="#F4EFE0", accent=A[2], glyph="circle",    dark=False),
    "camp":           dict(ground=A[1], disc="#F4EFE0", accent=A[2], glyph="leaf",      dark=False),
    "afterparty":     dict(ground=A[3], disc="#F4EFE0", accent=A[2], glyph="plus",      dark=False),
}


def theme_for(name):
    n = name.lower()
    for key, words in (("starry_night", ("starry",)), ("disco_diwali", ("disco", "diwali")),
                       ("merry_miracles", ("merry", "miracle")), ("terrathon", ("terrathon",)),
                       ("paradox", ("paradox",)), ("anniversary", ("anniversary", "turns five")),
                       ("camp", ("camp",)), ("afterparty", ("after party", "afterparty", "sunset")),
                       ("fete", ("fete",)), ("fundraiser", ("fundraiser", "fifa", "football",
                                                           "basketball", "binge", "halloween",
                                                           "games"))):
        if any(w in n for w in words):
            return key
    return "fete"


def _ink(t):
    return "#F4EFE0" if t["dark"] else core.INK


def _on(fill):
    return core.text_on(fill)


# --- ASSETS ---------------------------------------------------------------------------------
def img_uri(path, max_px=1500):
    """Photo as a base64 JPEG, EXIF-rotated and capped so a 15-slide batch stays renderable."""
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _photo(uri, x, y, w, h, extra="", focus="50% 35%", z=2):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};'
            f'overflow:hidden;{extra}"><img src="{uri}" style="width:100%;height:100%;object-fit:cover;'
            f'object-position:{focus};display:block"></div>')


def _doodle(kind, x, y, size, fill, rot=0, z=6):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:{z};'
            f'filter:drop-shadow(3px 4px 0 rgba(10,10,10,.9))">{dd.stamp(kind, fill, rot=rot, style="clean")}</div>')


def _logo(dark_bg, y=130):
    pill = ('background:#F4EFE0;border:2.5px solid #0A0A0A;border-radius:999px;padding:8px 18px;'
            'box-shadow:3px 3px 0 #0A0A0A;') if dark_bg else ''
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;z-index:30;{pill}">'
            f'<img src="{core.LOGO}" style="height:50px;display:block"></div>')


def _chip(txt, fill, x, y, rot=-3, z=30):
    return (f'<span style="position:absolute;left:{x}px;top:{y}px;z-index:{z};transform:rotate({rot}deg);'
            f'font-family:var(--m);font-weight:700;font-size:22px;letter-spacing:.1em;text-transform:uppercase;'
            f'color:{_on(fill)};background:{fill};border:3px solid #0A0A0A;border-radius:999px;'
            f'padding:9px 22px;box-shadow:4px 4px 0 #0A0A0A;white-space:nowrap">{txt}</span>')


def _title(txt, size, color, x, y, w, z=30, align="left", shadow=False):
    sh = "text-shadow:0 4px 18px rgba(0,0,0,.55);" if shadow else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:{z};text-align:{align};'
            f'font-family:var(--d);font-weight:900;font-size:{size}px;line-height:.92;text-transform:uppercase;'
            f'color:{color};{sh}">{txt}</div>')


def _mono(txt, color, x, y, size=20, z=30, align="left", w=None):
    ww = f"width:{w}px;" if w else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{ww}z-index:{z};text-align:{align};'
            f'font-family:var(--m);font-weight:700;font-size:{size}px;letter-spacing:.12em;'
            f'text-transform:uppercase;color:{color}">{txt}</div>')


def _size_for(txt, max_w, start, floor):
    """Width heuristic for NeutralFace caps (~0.62em per glyph). The looking gate is the final
    word; this only keeps a long event name from running off the canvas."""
    s = start
    while s > floor and len(txt) * s * 0.62 > max_w:
        s -= 6
    return s


# --- COVER ----------------------------------------------------------------------------------
def cover_html(key, name, year):
    t = THEMES[key]
    D = 760                                   # disc diameter; IG crops covers to the central circle
    cx, cy = W // 2, H // 2
    disc_ink = _on(t["disc"])
    ring = "#F4EFE0" if t["dark"] else "#0A0A0A"
    words = name.upper().split()
    line1 = " ".join(words[:-1]) if len(words) > 1 else name.upper()
    line2 = words[-1] if len(words) > 1 else ""
    size = _size_for(max(line1, line2, key=len), 600, 112, 56)
    body = f'<div style="position:absolute;inset:0;background:{t["ground"]}"></div>'
    body += _doodle(t["glyph"], 70, 220, 190, t["accent"], rot=-14, z=3)
    body += _doodle(t["glyph"], W - 260, H - 420, 220, t["accent"], rot=12, z=3)
    body += (f'<div style="position:absolute;left:{cx-D//2}px;top:{cy-D//2}px;width:{D}px;height:{D}px;'
             f'border-radius:50%;background:{t["disc"]};border:10px solid {ring};box-shadow:12px 12px 0 {ring};z-index:5"></div>')
    body += _doodle(t["glyph"], cx - 150, cy - 300, 300, t["accent"], rot=-6, z=8)
    body += _title(line1, size, disc_ink, cx - 330, cy + 40, 660, z=9, align="center")
    y = cy + 40 + int(size * .95)
    if line2:
        body += _title(line2, size, disc_ink, cx - 330, y, 660, z=9, align="center")
        y += int(size * .95)
    body += _mono(year, disc_ink, cx - 330, y + 18, 26, z=9, align="center", w=660)
    return B.page(W, H, t["ground"], body, grain=False)


# --- SLIDE TEMPLATES ------------------------------------------------------------------------
def t_full(t, ph, name, year, i, n):
    acc = t["accent"]
    h = (_photo(ph[0], 0, 0, W, H, z=1)
         + f'<div style="position:absolute;left:0;right:0;bottom:0;height:700px;z-index:10;'
           f'background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0))"></div>'
         + f'<div style="position:absolute;left:0;right:0;top:0;height:380px;z-index:10;'
           f'background:linear-gradient(to bottom,rgba(0,0,0,.55),rgba(0,0,0,0))"></div>'
         + _logo(True)
         + _chip(f"{name} {year}", acc, M, 1440)
         + _title(name, _size_for(name, W - 2 * M, 120, 64), "#FFFFFF", M, 1500, W - 2 * M, shadow=True)
         + _mono(f"{i:02d} / {n:02d}", "#FFFFFF", W - M - 200, 1620, 20, w=200, align="right"))
    return h, "#0A0A0A"


def t_polaroid(t, ph, name, year, i, n):
    ink = _ink(t)
    rot = -4 if i % 2 else 4
    fw, fh = 820, 1020
    x, y = (W - fw) // 2, 390
    h = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{fw}px;height:{fh+120}px;z-index:4;'
         f'transform:rotate({rot}deg);background:#FFFFFF;border:5px solid #0A0A0A;box-shadow:14px 14px 0 #0A0A0A">'
         f'<div style="position:absolute;left:34px;top:34px;width:{fw-68}px;height:{fh-34}px;overflow:hidden;'
         f'border:3px solid #0A0A0A"><img src="{ph[0]}" style="width:100%;height:100%;object-fit:cover;'
         f'object-position:50% 35%;display:block"></div>'
         f'<div style="position:absolute;left:34px;top:{fh+10}px;width:{fw-68}px;text-align:center;'
         f'font-family:var(--m);font-weight:700;font-size:26px;letter-spacing:.12em;text-transform:uppercase;'
         f'color:#0A0A0A">{name} &middot; {year}</div></div>')
    h += _doodle(t["glyph"], 70, 250, 150, t["accent"], rot=-12)
    h += _doodle("sparkle", W - 230, 1560, 140, t["accent"], rot=10)
    h += _logo(t["dark"])
    h += _mono(f"{i:02d} / {n:02d}", ink, W - M - 200, 150, 22, w=200, align="right")
    return h, t["ground"]


def t_arch(t, ph, name, year, i, n):
    ink = _ink(t)
    word = name.upper().split()[0]
    sz = _size_for(word, W - 2 * M, 300, 120)
    h = (f'<div style="position:absolute;left:0;top:380px;width:{W}px;z-index:3;text-align:center;'
         f'font-family:var(--d);font-weight:900;font-size:{sz}px;line-height:.9;'
         f'-webkit-text-stroke:3px {ink};color:transparent">{word}</div>')
    aw, ah = 760, 1100
    h += (f'<div style="position:absolute;left:{(W-aw)//2}px;top:520px;width:{aw}px;height:{ah}px;z-index:4;'
          f'border-radius:{aw//2}px {aw//2}px 40px 40px;overflow:hidden;border:6px solid #0A0A0A;'
          f'box-shadow:14px 14px 0 #0A0A0A"><img src="{ph[0]}" style="width:100%;height:100%;'
          f'object-fit:cover;object-position:50% 30%;display:block"></div>')
    h += _chip(year, t["accent"], 120, 1560, rot=-5, z=8)
    h += _doodle("star", W - 250, 1500, 150, t["accent"], rot=14, z=8)
    h += _logo(t["dark"])
    h += _mono(f"{i:02d} / {n:02d}", ink, W - M - 200, 150, 22, w=200, align="right")
    return h, t["ground"]


def t_duo(t, ph, name, year, i, n):
    ink = _ink(t)
    cw, ch = 700, 680
    h = (f'<div style="position:absolute;left:70px;top:300px;width:{cw}px;height:{ch}px;z-index:4;'
         f'transform:rotate(-3deg);border:6px solid #0A0A0A;box-shadow:12px 12px 0 #0A0A0A;overflow:hidden">'
         f'<img src="{ph[0]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 35%;display:block"></div>'
         f'<div style="position:absolute;left:{W-cw-70}px;top:{300+ch-100}px;width:{cw}px;height:{ch}px;z-index:5;'
         f'transform:rotate(3deg);border:6px solid #0A0A0A;box-shadow:12px 12px 0 #0A0A0A;overflow:hidden">'
         f'<img src="{ph[1]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 35%;display:block"></div>')
    h += _chip(f"{name} {year}", t["accent"], 90, 1610, rot=-3)
    h += _doodle(t["glyph"], W - 260, 190, 170, t["accent"], rot=12)
    h += _logo(t["dark"])
    h += _mono(f"{i:02d} / {n:02d}", ink, W - M - 200, 1620, 22, w=200, align="right")
    return h, t["ground"]


def t_strip(t, ph, name, year, i, n):
    ink = _ink(t)
    fw, fh, gap = 640, 400, 36
    x = (W - fw) // 2
    sh = "#F4EFE0" if t["dark"] else "#0A0A0A"
    h = (f'<div style="position:absolute;left:{x-36}px;top:290px;width:{fw+72}px;height:{3*fh+2*gap+72}px;'
         f'z-index:3;background:#0A0A0A;border:5px solid {sh};border-radius:24px;box-shadow:12px 12px 0 {sh}"></div>')
    for k in range(3):
        h += _photo(ph[k], x, 326 + k * (fh + gap), fw, fh, extra="border:4px solid #F4EFE0;border-radius:6px", z=4)
    for k in range(4):                               # sprocket holes either side of the strip
        for side in (x - 22, x + fw + 8):
            h += (f'<span style="position:absolute;left:{side}px;top:{330 + k * 330}px;width:14px;height:34px;'
                  f'border-radius:4px;background:{t["ground"]};z-index:5"></span>')
    h += _chip(f"{name} {year}", t["accent"], 100, 1690, rot=-3)
    h += _logo(t["dark"])
    h += _mono(f"{i:02d} / {n:02d}", ink, W - M - 200, 150, 22, w=200, align="right")
    return h, t["ground"]


def t_round(t, ph, name, year, i, n):
    ink = _ink(t)
    d = 860
    x, y = (W - d) // 2, 420
    sh = "#F4EFE0" if t["dark"] else "#0A0A0A"
    h = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;z-index:4;border-radius:50%;'
         f'overflow:hidden;border:8px solid #0A0A0A;box-shadow:14px 14px 0 {sh}">'
         f'<img src="{ph[0]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 35%;display:block"></div>')
    h += _doodle(t["glyph"], x - 30, y + d - 200, 230, t["accent"], rot=-10, z=8)
    h += _title(name, _size_for(name, W - 2 * M, 100, 56), ink, M, 1400, W - 2 * M, z=8, align="center")
    h += _chip(year, t["accent"], W // 2 - 70, 1560, rot=-3, z=8)
    h += _logo(t["dark"])
    h += _mono(f"{i:02d} / {n:02d}", ink, W - M - 200, 150, 22, w=200, align="right")
    return h, t["ground"]


TEMPLATES = {"full": (t_full, 1), "polaroid": (t_polaroid, 1), "arch": (t_arch, 1),
             "duo": (t_duo, 2), "strip": (t_strip, 3), "round": (t_round, 1)}
# No two neighbours match and the 1-photo / multi-photo rhythm alternates.
SEQUENCE = ["full", "polaroid", "duo", "arch", "full", "strip", "round", "polaroid",
            "full", "duo", "arch", "round", "full", "strip", "polaroid"]


def plan(n_photos):
    """Template list for n_photos. Returns (templates, photos_left). Stops at MAX_SLIDES or when
    the photos run out; a multi-photo template with too few photos left degrades to a 1-photo one."""
    out, left = [], n_photos
    for kind in SEQUENCE:
        if len(out) >= MAX_SLIDES or left <= 0:
            break
        if TEMPLATES[kind][1] > left:
            kind = "polaroid"
        out.append(kind)
        left -= TEMPLATES[kind][1]
    return out, left


def slides_html(key, name, year, photos):
    t = THEMES[key]
    kinds, _ = plan(len(photos))
    uris = [img_uri(p) for p in photos]
    pages, c = [], 0
    for idx, kind in enumerate(kinds, 1):
        fn, k = TEMPLATES[kind]
        body, ground = fn(t, uris[c:c + k], name, year, idx, len(kinds))
        c += k
        bg = f'<div style="position:absolute;inset:0;background:{ground}"></div>'
        pages.append((kind, B.page(W, H, ground, bg + body, grain=False)))
    return pages


async def build_event(key_or_name, name, year, photos, out_dir, theme=None):
    """Render cover + slides for ONE event into out_dir. Returns the list of files written."""
    key = theme or (key_or_name if key_or_name in THEMES else theme_for(key_or_name))
    os.makedirs(out_dir, exist_ok=True)
    written = []
    async with B.session():
        p = os.path.join(out_dir, "00_cover.png")
        await B.render(cover_html(key, name, year), p, W, H)
        written.append(p)
        for n, (kind, html) in enumerate(slides_html(key, name, year, photos), 1):
            p = os.path.join(out_dir, f"{n:02d}_{kind}.png")
            await B.render(html, p, W, H)
            written.append(p)
    return written


if __name__ == "__main__":
    # smoke test on real AQ photos shipped in the repo
    src = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
    ph = sorted(os.path.join(src, f) for f in os.listdir(src) if f.endswith(".jpg"))
    out = os.path.join(ROOT, "out", "highlights_test", "disco_diwali")
    print(asyncio.run(build_event("Disco Diwali 2.0", "Disco Diwali", "2025", ph, out)))
