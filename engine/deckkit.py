"""DECKKIT: the design system behind the AQ sponsorship + stalls decks and brochures (user brief 2026-10-09).

WHY THIS EXISTS. The Disco Diwali sponsorship deck was assembled slide by slide in Figma: nine background colours, four heading
treatments, emoji icons from three different sets, a bar chart that mixed people with rupees. The brief was "make it feel cohesive".
Cohesion cannot be asked of an author slide by slide, so it is encoded here: ONE scaffold, ONE type scale, ONE palette, ONE radius
scale, ONE icon set, ONE chart grammar. A slide is a function that returns content for the scaffold; it cannot choose its own ground,
its own heading size or its own corner radius, because those are not parameters.

THE LANGUAGE (user ruling: "a softer, cleaner variant", rounded corners and frames, NOT TerraThon):
  * cream ground, paper cards read by a 1.5px keyline + a soft shadow (never a hard offset shadow, never a thick outline)
  * radii: frame 28 / card 22 / chip 999. Photos always sit in a 28px frame.
  * one accent family (green #2FD284, blue #1E88E5, lemon #FFC700) = the colours of the die-cut sticker kit, so the stickers belong
  * every ~5th slide is a DARK slide (ink ground, same type scale) for rhythm; nothing else changes
  * titles NeutralFace 900 UPPERCASE, ONE Instrument Serif italic accent word on a lemon highlight (AQ rule: <=1 accent word)
  * labels JetBrains Mono, body Eina, numbers NeutralFace

Everything returns HTML strings. Rendering goes through build.render (the standing gate); nothing here touches the browser.
"""
import base64, html as _html, io, json, os, re
from PIL import Image

import importlib.util as _iu

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)


def _load(n):
    s = _iu.spec_from_file_location(n, os.path.join(_HERE, n + ".py"))
    m = _iu.module_from_spec(s); s.loader.exec_module(m); return m


core = _load("core")
ASSETS = os.path.join(_HERE, "assets", "sponsorship")

# ── tokens ────────────────────────────────────────────────────────────────────────────────────
W, H, M = 1920, 1080, 96
BG, PAPER, INK = "#F4EFE0", "#FBF8F0", "#0A0A0A"
INK2, MUTE, LINE = "#34342F", "#66645B", "rgba(10,10,10,.12)"
GREEN, BLUE, LEMON, TOMATO = "#2FD284", "#1E88E5", "#FFC700", "#FF4D2E"
GREEN_D, BLUE_D = "#14864F", "#1666B8"           # the same hues darkened until they clear 4.5:1 as small type on cream
DARK, DARK2 = "#0B0C0E", "#16181C"               # dark-slide ground and card
CREAM_ON_DARK = "#F4EFE0"
R_FRAME, R_CARD = 28, 22

FOOT_H = 40      # footer band height; content area ends above it


def esc(t): return _html.escape(str(t), quote=False)


# ── images ────────────────────────────────────────────────────────────────────────────────────
_IMG = {}


def uri(path, maxside=1500, q=84):
    """data: URI for an asset (path relative to engine/assets/sponsorship, or absolute). Big photos are shrunk once and cached."""
    p = path if os.path.isabs(path) else os.path.join(ASSETS, path)
    if p in _IMG: return _IMG[p]
    ext = os.path.splitext(p)[1].lower()
    if ext in (".jpg", ".jpeg", ".png") and os.path.getsize(p) > 250_000:
        im = Image.open(p)
        if max(im.size) > maxside: im.thumbnail((maxside, maxside), Image.LANCZOS)
        buf = io.BytesIO()
        if im.mode in ("RGBA", "LA", "P"): im.convert("RGBA").save(buf, "PNG", optimize=True); mime = "image/png"
        else: im.convert("RGB").save(buf, "JPEG", quality=q); mime = "image/jpeg"
        out = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "svg": "image/svg+xml"}[ext[1:]]
        out = f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
    _IMG[p] = out
    return out


def asset(i):
    """Resolve an image id (int) or filename to its file in engine/assets/sponsorship."""
    if isinstance(i, int):
        for ext in ("jpg", "png"):
            p = os.path.join(ASSETS, f"img_{i:03d}.{ext}")
            if os.path.exists(p): return p
        raise FileNotFoundError(f"img_{i:03d}")
    return i if os.path.isabs(i) else os.path.join(ASSETS, i)


def photo(i, focus="50% 50%", r=R_FRAME, extra="", tag="photo", alt=""):
    """A photo in a rounded frame filling its grid cell. ALWAYS this, so every picture in every deck has the same corner and keyline."""
    return (f'<div class="ph" data-tag="{tag}" role="img" aria-label="{esc(alt)}" style="background-image:url({uri(asset(i))});'
            f'background-position:{focus};border-radius:{r}px;{extra}"></div>')


def crop_uri(path, box, maxside=1200):
    """data URI of a crop (fractions x0,y0,x1,y1) of an asset. Used to lift a poster out of an Instagram screenshot."""
    im = Image.open(asset(path)).convert("RGB"); w, h = im.size
    im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if max(im.size) > maxside: im.thumbnail((maxside, maxside), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


_TRIM = {}


def logo_uri(path, pad=.04, flat=False):
    """A logo trimmed to its ink. Source logos carry big transparent or white margins (a mark could fill 30% of its tile). Trims by the alpha
    box when there is real alpha, else by the non-white box. Pair with mix-blend-mode:multiply on a light tile to drop any white that remains."""
    p = asset(path)
    if (p, flat) in _TRIM: return _TRIM[(p, flat)]
    im = Image.open(p).convert("RGBA"); a = im.getchannel("A")
    if a.getextrema()[0] < 250: bb = a.point(lambda v: 255 if v > 24 else 0).getbbox()
    else:
        import numpy as np
        px = np.asarray(im.convert("RGB")).astype(int); m = (px.min(2) < 238)
        ys, xs = np.where(m); bb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else None
    if bb:
        w, h = im.size; px_ = int((bb[2] - bb[0]) * pad) + 2; py_ = int((bb[3] - bb[1]) * pad) + 2
        im = im.crop((max(0, bb[0] - px_), max(0, bb[1] - py_), min(w, bb[2] + px_), min(h, bb[3] + py_)))
    if max(im.size) > 700: im.thumbnail((700, 700), Image.LANCZOS)
    if flat:                      # for a LIGHT tile: composite on white so antialiased edge pixels cannot show a dark fringe
        bgw = Image.new("RGBA", im.size, "white"); bgw.alpha_composite(im); im = bgw.convert("RGB")
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    _TRIM[(p, flat)] = "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    return _TRIM[(p, flat)]


# ── icons: ONE set (24px grid, 1.8 stroke, round). Replaces the three emoji sets in the source deck. ──────────────
_ICON = {
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "heart": '<path d="M12 20s-7.5-4.6-9.2-9.4A5 5 0 0 1 12 7.3a5 5 0 0 1 9.2 3.3C19.5 15.4 12 20 12 20z"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.2c2.6.2 4.5 2.2 4.5 4.8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "megaphone": '<path d="M3 10v4a1 1 0 0 0 1 1h3l8 4V5L7 9H4a1 1 0 0 0-1 1z"/><path d="M18.5 9a4 4 0 0 1 0 6"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 0 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "coffee": '<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10.5h1.5a2.5 2.5 0 0 1 0 5H17M8 3v2M12 3v2"/>',
    "news": '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/>',
    "pencil": '<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12"/><path d="M12 8C10 3.5 6 4.5 7.2 7.2 8 8 12 8 12 8zM12 8c2-4.5 6-3.5 4.8-.8C16 8 12 8 12 8z"/>',
    "utensils": '<path d="M6 3v7a2 2 0 0 0 4 0V3M8 10v11M17 3c-2 2-3 5-3 8h3v10"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "music": '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
    "star": '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.6 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>',
    "ticket": '<path d="M3 8a2 2 0 0 0 2-2h14a2 2 0 0 0 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 0-2 2H5a2 2 0 0 0-2-2v-3a2 2 0 0 0 0-4z"/><path d="M14 6v12" stroke-dasharray="2 2.5"/>',
    "camera": '<path d="M4 8h3l1.5-2.5h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    "sparkle": '<path d="M12 3c.6 4.2 2.8 6.4 7 7-4.2.6-6.4 2.8-7 7-.6-4.2-2.8-6.4-7-7 4.2-.6 6.4-2.8 7-7z"/><path d="M19 17v4M17 19h4"/>',
    "store": '<path d="M4 9l1.5-5h13L20 9"/><path d="M4 9a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0A2.7 2.7 0 0 0 20 9M5.5 12.5V20h13v-7.5M10 20v-4h4v4"/>',
    "school": '<path d="M3 21h18M5 21V10l7-5 7 5v11"/><path d="M10 21v-6h4v6M12 2.5v3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "sprout": '<path d="M12 21V11M12 11c0-4 3-6 7-6 0 4-3 6-7 6zM12 14c0-3-2-5-6-5 0 3 2 5 6 5z"/>',
    "paw": '<circle cx="6.5" cy="10" r="2"/><circle cx="10" cy="6" r="2"/><circle cx="14" cy="6" r="2"/><circle cx="17.5" cy="10" r="2"/><path d="M12 12c-3 0-5 3-5 5.2 0 1.6 1.3 2.3 2.7 2 1-.2 1.6-.6 2.3-.6s1.3.4 2.3.6c1.4.3 2.7-.4 2.7-2C17 15 15 12 12 12z"/>',
    "pulse": '<path d="M12 20s-7.5-4.6-9.2-9.4A5 5 0 0 1 12 7.3a5 5 0 0 1 9.2 3.3C19.5 15.4 12 20 12 20z"/><path d="M6 12h3l1.5-3 3 6 1.5-3H18"/>',
    "shirt": '<path d="M8 3L3 6l2 4 3-1v12h8V9l3 1 2-4-5-3c-1 2-2.4 2.6-4 2.6S9 5 8 3z"/>',
    "box": '<path d="M3 7.5L12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "insta": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r=".8"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "id": '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.5-1.8 1.7-2.5 3-2.5s2.5.7 3 2.5M14.5 10h4M14.5 13h3"/>',
    "wand": '<path d="M4 20L15 9M14 5l1-2 1 2 2 1-2 1-1 2-1-2-2-1zM18 12l.7-1.4.7 1.4 1.4.7-1.4.7-.7 1.4-.7-1.4-1.4-.7z"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5M3 17.5l9 5 9-5" opacity=".6"/>',
}


def icon(name, size=32, color="currentColor", sw=1.8):
    return (f'<svg class="ic" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICON[name]}</svg>')


# ── type helpers ──────────────────────────────────────────────────────────────────────────────
def title(text, size=84, color=None):
    """Heading. `*word*` marks THE one accent word (Instrument Serif italic on a lemon highlight). Newlines become <br>."""
    t = esc(text).replace("\n", "<br>")
    t = re.sub(r"\*(.+?)\*", r'<em>\1</em>', t, count=1)
    c = f"color:{color};" if color else ""
    return f'<h1 class="t" data-tag="title" style="font-size:{size}px;{c}">{t}</h1>'


def eyebrow(text, dot=GREEN):
    return f'<div class="eb" data-tag="eyebrow"><i style="background:{dot}"></i>{esc(text)}</div>'


def lede(text, size=32, width=None, color=None):
    w = f"max-width:{width}px;" if width else ""
    c = f"color:{color};" if color else ""
    return f'<p class="lede" style="font-size:{size}px;{w}{c}">{esc(text)}</p>'


def chip(text, bg=GREEN, fg=None, size=20):
    fg = fg or core.text_on(bg)
    return f'<span class="chip" style="background:{bg};color:{fg};font-size:{size}px">{esc(text)}</span>'


def chip_o(text, size=20, dark=False):
    """Outline chip, for secondary labels."""
    c = CREAM_ON_DARK if dark else INK
    return f'<span class="chip" style="border:1.5px solid {c};color:{c};font-size:{size}px;background:transparent">{esc(text)}</span>'


def card(inner, cls="", style="", dark=False):
    return f'<div class="card{" dk" if dark else ""} {cls}" data-tag="card" style="{style}">{inner}</div>'


def kpi(value, label, ic=None, tone=GREEN, size=84, dark=False):
    """A stat tile: icon in a tinted disc at the TOP, big number + label anchored at the BOTTOM, so a row of tiles lines up whatever the
    label length. ONE grammar for every number in every deck."""
    ico = (f'<span class="disc" style="background:{tone};color:{core.text_on(tone)}">{icon(ic, 30, "currentColor")}</span>' if ic else "<span></span>")
    return card(f'{ico}<div><div class="kv" style="font-size:{size}px">{esc(value)}</div><div class="kl">{esc(label)}</div></div>', "kpi", dark=dark)


# ── chart grammar ─────────────────────────────────────────────────────────────────────────────
def donut(slices, size=560, thick=120, center=None, dark=False):
    """slices: [(label, pct, colour)]. Percent labels sit ON the ring; the legend is HTML beside it, never inside the SVG."""
    import math
    pie = thick >= size / 2 - 8                      # thick == the radius draws a PIE (no hole), anything less a donut
    if pie: thick = size / 2 - 4
    r = size / 2 - thick / 2 - 4; cx = cy = size / 2; circ = 2 * math.pi * r
    tot = sum(p for _, p, _ in slices); off = 0; arcs = ""; labels = ""
    gap = 5
    for lab, p, col in slices:
        frac = p / tot; ln = max(0, frac * circ - gap)
        arcs += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{thick}" '
                 f'stroke-dasharray="{ln:.2f} {circ - ln:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        mid = (off + frac * circ / 2) / circ * 2 * math.pi - math.pi / 2
        lr = (size / 2) * .62 if pie else r
        lx, ly = cx + lr * math.cos(mid), cy + lr * math.sin(mid)
        labels += (f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" font-family="NeutralFace" font-weight="900" '
                   f'font-size="{34 if frac > .09 else 26}" fill="{core.text_on(col)}">{round(p)}%</text>')
        off += frac * circ
    mid_txt = ""
    if center:
        mid_txt = (f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-family="NeutralFace" font-weight="900" font-size="64" '
                   f'fill="{CREAM_ON_DARK if dark else INK}">{esc(center[0])}</text>'
                   f'<text x="{cx}" y="{cy + 34}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="17" '
                   f'letter-spacing="2" fill="{CREAM_ON_DARK if dark else MUTE}">{esc(center[1])}</text>')
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">{arcs}{labels}{mid_txt}</svg>'


def funnel(stages, width=1100, dark=False):
    """Exclusivity funnel: stages [(big, label, colour)]. Each bar is centred and narrower than the last, joined by trapezoid links,
    so the SHAPE says 'fewer and fewer get through' before a word is read. Widths are STYLISED (the real ratio 2,500:500 would leave a sliver you cannot write in)."""
    n = len(stages); bh = 150; gapv = 46; ww = width
    ws = [s[3] * ww for s in stages]           # 4th element = the bar's width as a fraction of the funnel (stylised, not a to-scale ratio)
    h = n * bh + (n - 1) * gapv
    out = ""
    for i, (big, lab, col, _) in enumerate(stages):
        w = ws[i]; x = (ww - w) / 2; y = i * (bh + gapv)
        out += (f'<g><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bh}" rx="26" fill="{col}"/>'
                f'<text x="{ww / 2}" y="{y + 86}" text-anchor="middle" font-family="NeutralFace" font-weight="900" font-size="76" '
                f'fill="{core.text_on(col)}">{esc(big)}</text>'
                f'<text x="{ww / 2}" y="{y + 126}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="20" '
                f'letter-spacing="2" fill="{core.text_on(col)}">{esc(lab)}</text></g>')
        if i < n - 1:
            w2 = ws[i + 1]; x2 = (ww - w2) / 2; y0 = y + bh; y1 = y0 + gapv
            link = CREAM_ON_DARK if dark else INK
            out += (f'<path d="M{x + 40:.1f},{y0 + 4} L{x + w - 40:.1f},{y0 + 4} L{x2 + w2 - 40:.1f},{y1 - 4} L{x2 + 40:.1f},{y1 - 4}Z" '
                    f'fill="{link}" opacity=".10"/>')
    return f'<svg viewBox="0 0 {ww} {h}" width="{ww}" height="{h}">{out}</svg>'


def hbars(rows, width=720, bar_h=46, gap=26, dark=False):
    """Horizontal bars with the value written at the bar end. rows: [(label, sublabel, value, display, colour)]. ONE unit per chart (caller's job)."""
    top = max(r[2] for r in rows); out = ""; lab_w = 230; vw = width - lab_w - 120
    for i, (lab, sub, v, disp, col) in enumerate(rows):
        y = i * (bar_h + gap); w = max(18, v / top * vw)
        tc = CREAM_ON_DARK if dark else INK
        out += (f'<text x="0" y="{y + bar_h / 2 - 4}" font-family="Eina01" font-weight="600" font-size="24" fill="{tc}">{esc(lab)}</text>'
                f'<text x="0" y="{y + bar_h / 2 + 20}" font-family="JetBrains Mono" font-weight="700" font-size="15" letter-spacing="1.5" '
                f'fill="{CREAM_ON_DARK if dark else MUTE}">{esc(sub)}</text>'
                f'<rect x="{lab_w}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="{bar_h / 2}" fill="{col}"/>'
                f'<text x="{lab_w + w + 16:.1f}" y="{y + bar_h / 2 + 11}" font-family="NeutralFace" font-weight="900" font-size="34" fill="{tc}">{esc(disp)}</text>')
    h = len(rows) * (bar_h + gap) - gap
    return f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}">{out}</svg>'


def map_svg(mp, height=820, pin_fill=GREEN, dark=False):
    """The school-reach map rebuilt as clean vector: silhouette, river, parks, NUMBERED pins. Names live in an HTML legend beside it
    (the source map printed 18 tiny labels on the map itself, which is why it read as unreadable). mp = scratchpad/sponsorship_private/map.json."""
    w, h = mp["w"], mp["h"]
    land = "#EAE2CC" if not dark else "#1E2025"
    outline = INK if not dark else CREAM_ON_DARK
    s = f'<svg viewBox="0 0 {w} {h}" height="{height}" width="{height * w / h:.0f}">'
    s += f'<path d="{mp["outline"][0]}" fill="{land}" stroke="{outline}" stroke-width="7" stroke-linejoin="round"/>'
    for d in mp["river"]: s += f'<path d="{d}" fill="#7CC4F2" stroke="#4BA3DC" stroke-width="3" stroke-linejoin="round"/>'
    for d in mp["parks"]: s += f'<path d="{d}" fill="#BFE3C0" opacity=".9"/>'
    for p in mp["pins"]:
        x, y = p["x"], p["y"]
        s += (f'<g><circle cx="{x}" cy="{y}" r="36" fill="{pin_fill}" stroke="{INK}" stroke-width="6"/>'
              f'<text x="{x}" y="{y + 1}" text-anchor="middle" dominant-baseline="central" font-family="NeutralFace" font-weight="900" '
              f'font-size="{40 if p["n"] < 10 else 34}" fill="{INK}">{p["n"]}</text></g>')
    return s + "</svg>"


# ── scaffold ──────────────────────────────────────────────────────────────────────────────────
CSS = f"""
.s{{position:relative;width:{W}px;height:{H}px;background:{BG};overflow:hidden;font-family:var(--e);color:{INK};
    display:flex;flex-direction:column;padding:78px {M}px {FOOT_H + 48}px}}
.s.dk{{background:{DARK};color:{CREAM_ON_DARK}}}
.hd{{display:flex;flex-direction:column;gap:20px;flex:none}}
.eb{{display:flex;align-items:center;gap:12px;font:700 19px var(--m);letter-spacing:.14em;text-transform:uppercase;color:{INK2}}}
.dk .eb{{color:#C9C4B3}}
.eb i{{width:13px;height:13px;border-radius:50%;display:block}}
h1.t{{font-family:var(--d);font-weight:900;text-transform:uppercase;line-height:.94;letter-spacing:-.012em;margin:0}}
h1.t em{{font-family:var(--s);font-style:italic;font-weight:400;text-transform:none;letter-spacing:0;
    background:linear-gradient(transparent 58%,{LEMON} 58%,{LEMON} 92%,transparent 92%);padding:0 .08em;margin:0 -.04em}}
.dk h1.t em{{background:linear-gradient(transparent 58%,#B8860B 58%,#B8860B 92%,transparent 92%);color:{CREAM_ON_DARK}}}
.lede{{font-family:var(--e);line-height:1.34;color:{INK2};margin:0}}
.dk .lede{{color:#D8D3C2}}
.bd{{flex:1;min-height:0;display:flex;margin-top:40px;position:relative}}
.ft{{position:absolute;left:{M}px;right:{M}px;bottom:36px;height:{FOOT_H}px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
    font:700 15px var(--m);letter-spacing:.12em;text-transform:uppercase;color:{MUTE}}}
.dk .ft{{color:#A7A292}}
.ft img{{height:30px;display:block}}
.ft .mid{{display:flex;align-items:center;gap:18px}}
.ft .pg{{justify-self:end}}
.ft .dot{{width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.6}}
.card{{background:{PAPER};border:1.5px solid {LINE};border-radius:{R_CARD}px;box-shadow:0 18px 38px -26px rgba(10,10,10,.34);padding:30px 34px}}
.card.dk{{background:{DARK2};border-color:rgba(244,239,224,.14);box-shadow:none;color:{CREAM_ON_DARK}}}
.chip{{display:inline-flex;align-items:center;gap:10px;padding:10px 22px;border-radius:999px;font-family:var(--e);font-weight:600;white-space:nowrap}}
.ph{{background-size:cover;background-repeat:no-repeat;width:100%;height:100%;box-shadow:0 0 0 1.5px {LINE},0 18px 38px -26px rgba(10,10,10,.4)}}
.kpi{{display:flex;flex-direction:column;justify-content:space-between;gap:18px;min-height:0}}
.kv{{font-family:var(--d);font-weight:900;line-height:.95;letter-spacing:-.01em}}
.kl{{font:600 24px/1.25 var(--e);color:{INK2};margin-top:10px}}
.dk .kl,.card.dk .kl{{color:#D8D3C2}}
.disc{{width:60px;height:60px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}}
.cap{{position:absolute;left:18px;bottom:18px;background:rgba(244,239,224,.92);color:{INK};font:600 18px var(--e);padding:8px 18px;border-radius:999px}}
.frame{{position:relative}}
.mono{{font-family:var(--m);font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
ul.ck{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}}
ul.ck li{{display:flex;gap:14px;align-items:flex-start;font:400 25px/1.28 var(--e);color:{INK2}}}
ul.ck li svg{{flex:none;margin-top:3px}}
"""


def page(inner):
    """Full HTML document for one slide (one .s). Same embedded fonts as the engine."""
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{core.FONTS}{core.ROOT}'
            f'*{{margin:0;box-sizing:border-box}}body{{background:{BG}}}{CSS}</style></head><body>{inner}</body></html>')


def footer(n, total, deck_label, dark=False):
    return (f'<div class="ft"><img src="{core.LOGO}" alt="AquaTerra">'
            f'<div class="mid"><span>{esc(deck_label)}</span></div><span class="pg">{n:02d} / {total:02d}</span></div>')


def slide(body, head=None, n=1, total=1, deck_label="", dark=False, body_style="", cls=""):
    """The ONLY scaffold. head = (eyebrow, title_html, optional lede_html). Body fills the rest of the frame."""
    hd = ""
    if head:
        hd = f'<div class="hd">{"".join(head)}</div>'
    bd = f'<div class="bd" style="{body_style}">{body}</div>' if body is not None else ""
    return page(f'<section class="s p{" dk" if dark else ""} {cls}">{hd}{bd}{footer(n, total, deck_label, dark)}</section>')
