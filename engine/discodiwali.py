"""DISCO DIWALI format module (a fourth shape, like dispatch.py): one skeleton, many posters.

Learned from the 2026 announcement recreation (scratchpad/dd_announce.py, brain/DISCO_DIWALI.md). The poster is
LAYERS, back to front, and the only hand-input is a content dict:

  ground (black) -> beaded plate -> [carpet] -> mask -> string lights -> badge -> title lockup
  -> type stack / hero numeral -> [sold-out banner] -> gold sparkles (screen) -> film grain (screen)

Vertical layout is solved, not typed. A canvas taller than the 1350 feed (story = 1920) gives its extra height to three
anchor groups in fixed shares: TOP (badge, mask, lights) moves 15%, TITLE 62%, INFO (the type stack) 100%, so the
information stays bottom-anchored and the title keeps its breathing room.

Rules (all from the reference, see DISCO_DIWALI.md sec 4; precedence: the format beats core.ACCENTS, CLAUDE.md sec 2):
  R1  ink ground, silver/gold/off-white only. No AQ accents, no cream.
  R2  one hero: the title lockup (or the countdown numeral, which replaces the info stack, never the title).
  R3  the mask and lights never touch the type stack.
  R4  all copy is supplied. Nothing is invented: a price, venue or lineup is printed only if the caller passes it.
  R6  the red carpet ALWAYS fades into black toward its narrow end (user directive, 2026-10-13); it is never a hard-edged slab.
  R5  every kind validates its brief and RAISES with the field named (the dispatch.py contract).

Kinds: announce | countdown | tickets_open | sold_out | save_the_date | teaser_full | teaser_arch | teaser_trio (photo teasers).      Canvases: feed (1080x1350) | story (1080x1920).

CLI:   PYTHONIOENCODING=utf-8 python engine/discodiwali.py            -> renders the demo set to out/discodiwali/
"""
import asyncio, base64, datetime, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_DIR = os.path.join(ROOT, "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)
def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = _load("core"); B = _load("build")

ASSETS = os.path.join(ROOT, "engine", "assets", "disco_diwali") + os.sep
OFFWHITE, GOLD, GROUND = "#F2F2F2", "#C9971C", "#000000"
K = 0.9                      # the reference is 1200x1500; every reference coordinate scales by this onto 1080
S = lambda v: round(v * K)
BASE_H = 1350
MASKS = ("asset", "copper", "red")      # asset: supplied silver mask. copper: supplied copper mask (classier colourway). red: drawn red satin mask
STYLES = ("plate", "diya", "stroke", "blue", "photo")   # plate: beaded celestial corners. diya: navy and gold lotus-diya corners (no string lights). stroke: plain ink ground, red-stroked mask. photo: a real event photo, graded navy, with the soft diya plate SCREEN-blended over it, plus editorial type. blue: full-bleed navy diya pattern under a colour-dodge blue layer and disco beams (blend-mode recipe, scratchpad/dd_blend_lab.py v7)
KINDS = ("announce", "countdown", "tickets_open", "sold_out", "save_the_date", "teaser_full", "teaser_arch", "teaser_trio")
REQUIRED = {
    "announce":     ("edition", "date", "time", "status", "cta"),
    "countdown":    ("edition", "date", "days", "cta"),
    "tickets_open": ("edition", "headline", "cta"),
    "sold_out":     ("edition", "date", "thanks"),
    "save_the_date": ("edition", "day", "month", "year", "time", "cta"),
    "teaser_full":  ("edition", "date", "line", "photo", "cta"),
    "teaser_arch":  ("edition", "date", "line", "photo", "cta"),
    "teaser_trio":  ("edition", "date", "line", "photos", "cta"),
}
OPTIONAL = {"announce": ("note", "photo"), "countdown": ("unit",), "tickets_open": ("detail", "date"), "sold_out": (), "save_the_date": (), "teaser_full": (), "teaser_arch": (), "teaser_trio": ()}

# SVG shader used by style="blue": splits the title lockup into R/G/B copies offset +-3px and screen-blends them back.
BLUE_DEFS = ('<svg width="0" height="0" style="position:absolute"><defs><filter id="ca" x="-4%" y="-4%" width="108%" height="108%" color-interpolation-filters="sRGB">'
             '<feColorMatrix in="SourceGraphic" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r"/>'
             '<feColorMatrix in="SourceGraphic" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>'
             '<feColorMatrix in="SourceGraphic" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b"/>'
             '<feOffset in="r" dx="-3" dy="0" result="ro"/><feOffset in="b" dx="3" dy="0" result="bo"/>'
             '<feBlend in="ro" in2="g" mode="screen" result="rg"/><feBlend in="rg" in2="bo" mode="screen"/></filter></defs></svg>')

_cache = {}
def uri(name):
    if name not in _cache:
        mime = "image/png" if name.endswith(".png") else "image/svg+xml" if name.endswith(".svg") else "image/jpeg"
        _cache[name] = f"data:{mime};base64," + base64.b64encode(open(ASSETS + name, "rb").read()).decode()
    return _cache[name]

PHOTO_DIR = os.path.join(ROOT, "engine", "assets", "img", "events", "unsorted-2026-10-07")
_photo_cache = {}
def photo_path(ref):
    """A real event photo, by file name or by its NN_ prefix (e.g. "03"). Raises if it is not in the library."""
    if os.path.isfile(ref):
        return ref
    cand = os.path.join(PHOTO_DIR, ref)
    if os.path.isfile(cand):
        return cand
    import glob
    hits = sorted(glob.glob(os.path.join(PHOTO_DIR, f"{ref}_*.jpg")))
    if len(hits) == 1:
        return hits[0]
    raise ValueError(f"photo {ref!r} is not in {PHOTO_DIR} (give a file name or a unique NN prefix)")

def photo_uri(ref, max_px=1500):
    """Embed a photo downscaled to max_px on its long side: the library holds 3024x4032 originals."""
    path = photo_path(ref)
    if path not in _photo_cache:
        import io
        from PIL import Image
        im = Image.open(path).convert("RGB")
        im.thumbnail((max_px, max_px))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=86)
        _photo_cache[path] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _photo_cache[path]

def days_to_go(date_iso, today=None):
    """Whole days from today to an ISO date. Derived from the supplied date, so it is a fact, not an invention."""
    today = today or datetime.date.today()
    return (datetime.date.fromisoformat(date_iso) - today).days

def validate_brief(kind, content, canvas):
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")
    if canvas not in ("feed", "story"):
        raise ValueError(f"canvas must be 'feed' or 'story', got {canvas!r}")
    for f in REQUIRED[kind]:
        if f not in content or content[f] in (None, ""):
            raise ValueError(f"{kind}: required field {f!r} is missing")
    extra = set(content) - set(REQUIRED[kind]) - set(OPTIONAL[kind])
    if extra:
        raise ValueError(f"{kind}: unknown field(s) {sorted(extra)}; allowed {REQUIRED[kind] + OPTIONAL[kind]}")
    if kind in ("teaser_full", "teaser_arch"):
        photo_path(content["photo"])
    if kind == "teaser_trio":
        if not isinstance(content["photos"], (list, tuple)) or len(content["photos"]) != 3:
            raise ValueError("teaser_trio: 'photos' must be a list of exactly 3 photos")
        for ph in content["photos"]:
            photo_path(ph)
    if kind == "countdown" and not str(content["days"]).isdigit():
        raise ValueError("countdown: 'days' must be a whole number (use days_to_go(iso_date))")

def _fit(text, size, max_w, weight=700):
    """Shrink a size until the estimated width fits. Uppercase grotesque averages ~0.64em a glyph; the DOM gate
    (reconcile.measure_dom) is the real check, this only stops the obvious overflow before it renders."""
    est = lambda s: len(text) * s * (0.66 if weight >= 700 else 0.62)
    while est(size) > max_w and size > 18:
        size -= 2
    return size

class Poster:
    """One poster under construction. Layers append in z-order; `box` keeps the declared bbox beside every element."""
    def __init__(self, kind, content, canvas, style="plate", mask="asset"):
        validate_brief(kind, content, canvas)
        if style not in STYLES:
            raise ValueError(f"style must be one of {STYLES}, got {style!r}")
        if mask not in MASKS:
            raise ValueError(f"mask must be one of {MASKS}, got {mask!r}")
        self.kind, self.c, self.canvas, self.style, self.mask = kind, content, canvas, style, mask
        self.W, self.H = core.SIZES["feed" if canvas == "feed" else "story"]
        dh = self.H - BASE_H
        self.dy_top, self.dy_title, self.dy_info = round(dh * .15), round(dh * .62), dh
        self.parts, self.elements = [], []

    def box(self, label, x, y, w, h):
        self.elements.append((label, round(x), round(y), round(w), round(h)))

    def img(self, name, x, y, w, h=None, z=1, extra="", tag=""):
        hh = f"height:{h}px;" if h else ""
        self.parts.append(f'<img src="{uri(name)}" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;'
                          f'width:{w}px;{hh}z-index:{z};{extra}">')

    def line(self, label, text, cy, size, weight=700, cx=None, max_w=None, extra="", z=12, ink_h=1.1, plain=None):
        cx = self.W // 2 if cx is None else cx
        max_w = max_w or self.W - 2 * 60
        # measure the VISIBLE text: `text` may carry inline markup (the clock svg), which is not type and must not shrink it
        size = _fit(plain if plain is not None else text, size, max_w, weight)
        stroke = f"-webkit-text-stroke:{max(1, size // 28)}px {OFFWHITE};" if weight >= 700 else ""
        self.parts.append(
            f'<div data-tag="{label}" style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);white-space:nowrap;'
            f'font-family:var(--e);font-weight:{weight};font-size:{size}px;line-height:1;color:{OFFWHITE};text-transform:uppercase;'
            f'letter-spacing:.01em;{stroke}z-index:{z};{extra}">{text}</div>')
        w = min(len(plain if plain is not None else text) * size * .62, max_w)
        self.box(label, cx - w / 2, cy - size * ink_h / 2, w, size * ink_h)
        return size

    def pill(self, label, text, cy, w=S(498), h=S(112)):
        x = (self.W - w) // 2
        self.parts.append(
            f'<div data-tag="{label}" style="position:absolute;left:{x}px;top:{cy - h // 2}px;width:{w}px;height:{h}px;'
            f'border:2px solid {GOLD};border-radius:{S(24)}px;background:#050505;z-index:12;display:flex;align-items:center;'
            f'justify-content:center;font-family:var(--e);font-weight:700;font-size:{_fit(text.upper(), S(58), w - 40)}px;'
            f'color:{OFFWHITE};text-transform:uppercase;line-height:1;-webkit-text-stroke:2px {OFFWHITE}">{text}</div>')
        self.box(label, x, cy - h // 2, w, h)

    # ---- shared layers ----------------------------------------------------------------------------
    def base(self):
        W, H = self.W, self.H
        self.parts.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        if self.style == "stroke" or self.kind == "teaser_full":
            return                          # no sequin plate: the ground is plain ink, sparkles and grain still lay over it
        if self.style == "blue":
            self._blue_base()
            return
        if self.style == "photo":
            self._photo_base()
            return
        plate = "bg_diya_portrait.jpg" if self.style == "diya" else "bg_beaded_portrait.jpg"
        if H <= BASE_H:
            self.img(plate, 0, 0, W, H, z=1, tag="plate", extra="object-fit:cover;")
        else:
            # Taller than the plate's 4:5: cropping it to 9:16 loses the corner clusters and leaves a dead black middle.
            # Stack TWO plates instead, the second flipped and faded in from above, so all four corners carry beading.
            self.img(plate, 0, 0, W, BASE_H, z=1, tag="plate")
            self.img(plate, 0, H - BASE_H, W, BASE_H, z=1, tag="plate",
                     extra="transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);"
                           "mask-image:linear-gradient(to top,transparent 0%,#000 45%);")

    def _blue_base(self):
        """Layered blend recipe, back to front: ink, FULL-SCREEN navy diya pattern, a blue layer colour-DODGED over it (burns the gold,
        blooms the lotus), disco beams SCREENed from the top right through a radial mask, then a dim ellipse over the type zone so the
        pattern still lives in the corners. Every layer is tagged plate: deliberate full bleed."""
        W, H, P = self.W, self.H, self.parts
        def lay(css, z):
            P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:{z};pointer-events:none;{css}"></div>')
        P.append(BLUE_DEFS)
        P.append(f'<img data-tag="plate" src="{uri("pattern_diya_navy.jpg")}" style="position:absolute;left:{-(H - W) // 2}px;top:0;'
                 f'width:{H}px;height:{H}px;object-fit:cover;z-index:1;filter:brightness(.7) saturate(1.15)">')
        lay("background:radial-gradient(circle at 82% 10%,#3D7BFF 0%,rgba(20,60,220,0) 58%),linear-gradient(165deg,#1038FF,#001060 70%);"
            "mix-blend-mode:color-dodge;opacity:.6", 2)
        mask = "radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.5) 50%,transparent 90%)"
        lay("background:repeating-conic-gradient(from 188deg at 88% -6%,rgba(120,175,255,.95) 0deg 3deg,transparent 3deg 10deg);"
            f"-webkit-mask-image:{mask};mask-image:{mask};mix-blend-mode:screen;opacity:.75", 3)
        cy = round(64 * 100 / 100)                                  # dim ellipse centre, % of height
        lay(f"background:radial-gradient(ellipse 62% 44% at 50% {cy}%,rgba(0,0,0,.86),rgba(0,0,0,.55) 62%,rgba(0,0,0,.05) 100%)", 4)

    def _photo_base(self):
        """Back to front: ink, a real event photo graded dark, a navy multiply so the photo and the plate share one hue, the soft diya plate
        SCREEN-blended on top (its black centre drops out, so the photo shows through the middle while the gold lotus corners glow), then a
        gentle dim under the type. The raw tiled pattern is NOT used here: it is for edge cases only (user, 2026-10-13)."""
        W, H, P = self.W, self.H, self.parts
        ph = self.c.get("photo", "03")
        P.append(f'<img data-tag="photo" src="{photo_uri(ph)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1;'
                 f'filter:contrast(1.12) saturate(.9) brightness(.95)">')
        P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,#0A1E7A,#050A33);'
                 f'mix-blend-mode:multiply;opacity:.6"></div>')
        plate = "bg_diya_portrait.jpg"
        ex = "mix-blend-mode:screen;"
        if H <= BASE_H:
            self.img(plate, 0, 0, W, H, z=3, tag="plate", extra="object-fit:cover;" + ex)
        else:
            self.img(plate, 0, 0, W, BASE_H, z=3, tag="plate", extra=ex)
            self.img(plate, 0, H - BASE_H, W, BASE_H, z=3, tag="plate",
                     extra=ex + "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
        P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:4;pointer-events:none;background:radial-gradient(ellipse 66% 40% at 50% 66%,'
                 f'rgba(0,0,0,.62),rgba(0,0,0,.3) 65%,rgba(0,0,0,0) 100%)"></div>')

    def raw(self, label, html, cx, cy, w, h, css="", z=12):
        """A centred block of arbitrary markup with its declared box. For the editorial type, where one line mixes faces."""
        self.parts.append(f'<div data-tag="{label}" style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);white-space:nowrap;'
                          f'line-height:1;color:{OFFWHITE};z-index:{z};{css}">{html}</div>')
        self.box(label, cx - w / 2, cy - h / 2, w, h)

    def _announce_editorial(self):
        """Editorial type for style="photo": tracked small caps, a serif italic accent, one big date, mono meta between gold rules."""
        c, di, W = self.c, self.dy_info, self.W
        GL = "#E8C063"                                          # gold lifted for small type on a photo ground
        self.base(); self.top_group(); self.title()
        cx = S(673)
        self.raw("sub1", "MASQUERADE SANGEET", cx, S(952) + self.dy_title, S(560), S(40),
                 "font-family:var(--e);font-weight:600;font-size:%dpx;letter-spacing:.34em;text-indent:.34em" % S(26))
        self.raw("sub2", "Edition", cx, S(1008) + self.dy_title, S(260), S(60),
                 f"font-family:var(--s);font-style:italic;font-size:{S(58)}px;color:{GL}")
        date = c["date"].upper()
        day, _, rest = date.partition(" ")
        self.raw("date", f'<span style="font-family:var(--s);font-style:italic;font-weight:400;font-size:{S(150)}px;color:{OFFWHITE}">{day.rstrip("TH")}</span>'
                         f'<span style="font-family:var(--e);font-weight:700;font-size:{S(54)}px;letter-spacing:.06em;margin-left:{S(18)}px;vertical-align:{S(34)}px">{rest}</span>',
                 W // 2, S(1128) + di, S(820), S(150), "text-shadow:0 2px 24px rgba(0,0,0,.6)")
        rule = f'<span style="display:inline-block;width:{S(120)}px;height:2px;background:{GOLD};vertical-align:middle"></span>'
        meta = f'{c["time"].upper()}'
        self.raw("time", f'{rule}<span style="margin:0 {S(26)}px">{meta}</span>{rule}', W // 2, S(1232) + di, S(760), S(36),
                 f"font-family:var(--m);font-weight:700;font-size:{S(26)}px;letter-spacing:.22em;color:{GL}")
        self.raw("status", c["status"].upper(), W // 2, S(1290) + di, S(700), S(40),
                 f"font-family:var(--e);font-weight:600;font-size:{S(32)}px;letter-spacing:.2em")
        if c.get("note"):
            self.raw("note", c["note"], W // 2, S(1334) + di, S(420), S(46),
                     f"font-family:var(--s);font-style:italic;font-size:{S(38)}px;color:{GL}")
        self.pill("cta", c["cta"], S(1412) + di, h=S(80))

    def top_group(self):
        MK = .48
        mw = S(2000 * MK)
        if self.mask == "red":
            # drawn mask: body 920 units wide in a 1260x810 artboard; 0.87 ref-px/unit matches the asset mask's 800px body
            u = .87
            self.img("mask_red.svg", S(415 - 40 * u), S(-150) + self.dy_top, S(1260 * u), z=6, tag="mask",
                     extra="transform:rotate(-7deg);transform-origin:40% 55%;filter:drop-shadow(0 8px 24px rgba(0,0,0,.6));")
        elif self.mask == "copper":
            # copper_mask.png content spans x160-1560, y215-1135 of a 1680x1278 asset; 0.55 ref-px per asset-px
            u = .55
            self.img("mask_copper.png", S(370 - 160 * u), S(40 - 215 * u) + self.dy_top, S(1680 * u), z=6, tag="mask",
                     extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
        elif self.style == "stroke":
            # mask_stroked.png is the mask padded by 90px of red stroke on every side (scratchpad/make_mask_stroke.py)
            pad = round(90 * MK * K)
            self.img("mask_stroked.png", S(415 - 190 * MK) - pad, S(-145) + self.dy_top - pad, round(mw * 2180 / 2000), z=6, tag="mask",
                     extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));")
        else:
            self.img("mask.png", S(415 - 190 * MK), S(-145) + self.dy_top, mw, z=6, tag="mask",
                     extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.55));")
        if self.style != "diya":              # the navy diya direction is quiet: the lotus-diya plate carries the light
            self.img("string_lights.png", S(105), S(-150) + self.dy_top, S(1560), z=7, tag="lights")
        self.badge()

    def badge(self):
        bw = S(293)
        self.img("live_badge.png", S(45), S(48) + self.dy_top, bw, z=8, tag="badge")
        self.box("badge", S(45), S(48) + self.dy_top, bw, round(bw * 1005 / 1061))

    def title(self, scale=1.0, cx_shift=0, y_ref=390):
        TK = .676 * scale
        tw = S(2000 * TK)
        tx = S(30 - 265 * TK) + cx_shift
        ty = S(y_ref - 320 * TK) + self.dy_title
        self.img("title_lockup.png", tx, ty, tw, z=9, tag="title", extra="filter:url(#ca);" if self.style == "blue" else "")
        self.box("title", S(30) + cx_shift, S(y_ref) + self.dy_title, S(1160 * scale), S(670 * scale))

    def edition(self, y_sub=950, y_ed=1000):
        e = self.c["edition"]
        a, _, b = e.rpartition(" ")            # "Masquerade Sangeet Edition" -> bold "Masquerade Sangeet" / light "Edition"
        cx = S(673)
        self.line("sub1", a, S(y_sub) + self.dy_title, S(46), cx=cx, max_w=S(620))
        self.line("sub2", b, S(y_ed) + self.dy_title, S(44), weight=400, cx=cx, max_w=S(300))

    def overlays(self):
        self.img("sparkles.png", 0, 0, self.W, self.H, z=14, tag="sparkles", extra="mix-blend-mode:screen;object-fit:cover;")
        self.img("grain.png", 0, 0, self.W, self.H, z=15, tag="grain", extra="mix-blend-mode:screen;object-fit:cover;opacity:.9;")

    @staticmethod
    def clock(size):
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 40 40" style="display:inline-block;vertical-align:middle;'
                f'margin-right:{S(16)}px;-webkit-text-stroke:0"><circle cx="20" cy="20" r="18" fill="#EEE" stroke="#999" stroke-width="2"/>'
                f'<path d="M20 9v11l6 5" stroke="#222" stroke-width="3" fill="none" stroke-linecap="round"/></svg>')

    # ---- kinds ------------------------------------------------------------------------------------
    def build(self):
        getattr(self, "_" + self.kind)()
        self.overlays()
        return B.page(self.W, self.H, GROUND, "".join(self.parts), grain=False)

    def _announce(self):
        if self.style == "photo":
            return self._announce_editorial()
        c, di = self.c, self.dy_info
        self.base(); self.top_group(); self.title(); self.edition()
        self.line("date", c["date"], S(1090) + di, S(76))
        self.line("time", f'{self.clock(S(60))}{c["time"]}', S(1168) + di, S(60), plain="xx" + c["time"])
        self.line("status", c["status"], S(1232) + di, S(60))
        if c.get("note"):
            self.line("note", c["note"], S(1302) + di, S(34))
        self.pill("cta", c["cta"], S(1386) + di)

    def _countdown(self):
        c, di = self.c, self.dy_info
        self.base(); self.top_group(); self.title(); self.edition()
        n = str(c["days"])
        self.line("count", n, S(1128) + di, S(190) if len(n) < 3 else S(160), weight=700, z=12, ink_h=.9)
        unit = c.get("unit") or ("day to go" if n == "1" else "days to go")
        self.line("unit", unit, S(1250) + di, S(54))
        self.line("date", c["date"], S(1306) + di, S(38), weight=400)
        self.pill("cta", c["cta"], S(1386) + di, h=S(96))

    def _tickets_open(self):
        c, di = self.c, self.dy_info
        self.base()
        cw = self.W
        ch = round(cw * 1429 / 2000)
        self.img("red_carpet.png", 0, self.H - ch, cw, z=3, tag="carpet", extra="-webkit-mask-image:linear-gradient(to top,#000 0%,#000 32%,rgba(0,0,0,.55) 58%,transparent 92%);mask-image:linear-gradient(to top,#000 0%,#000 32%,rgba(0,0,0,.55) 58%,transparent 92%);")
        self.box("carpet", 0, self.H - ch, cw, ch)
        self.top_group(); self.title(); self.edition()
        self.line("headline", c["headline"], S(1085) + di, S(86))
        y = 1160
        if c.get("detail"):
            self.line("detail", c["detail"], S(y) + di, S(52)); y += 62
        if c.get("date"):
            self.line("date", c["date"], S(y) + di, S(44), weight=400)
        self.pill("cta", c["cta"], S(1386) + di)

    def _save_the_date(self):
        c, di = self.c, self.dy_info
        self.base(); self.top_group(); self.title(); self.edition()
        self.line("day", str(c["day"]), S(1190) + di, S(250), cx=S(330), max_w=S(420), ink_h=.9)
        self.line("month", c["month"], S(1148) + di, S(70), cx=S(800), max_w=S(430))
        self.line("year", str(c["year"]), S(1222) + di, S(70), cx=S(800), max_w=S(430))
        self.line("time", c["time"], S(1292) + di, S(40), weight=400, cx=S(800), max_w=S(470))
        self.pill("cta", c["cta"], S(1386) + di)

    # ---- photo teasers: real event photos in the Disco Diwali branding ----------------------------------------
    def _centre_shift(self, scale):
        """cx_shift that centres a title scaled by `scale` on the canvas (its content is 1160 ref-px wide at scale 1)."""
        return S((1200 - 1160 * scale) / 2 - 30)

    def _teaser_info(self, date_y=1215, edition_y=1275):
        c, di = self.c, self.dy_info
        self.line("date", c["date"], S(date_y) + di, S(62))
        self.line("edition", c["edition"], S(edition_y) + di, S(34), weight=400)
        self.pill("cta", c["cta"], S(1386) + di, h=S(96))

    def _photo_tag(self, name, ref, x, y, w, h, z, extra="", filt="contrast(1.06) saturate(.92) brightness(.78)"):
        self.parts.append(f'<img data-tag="{name}" src="{photo_uri(ref)}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                          f'object-fit:cover;z-index:{z};filter:{filt};{extra}">')

    def _teaser_full(self):
        c, di = self.c, self.dy_info
        self.parts.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self._photo_tag("photo", c["photo"], 0, 0, self.W, self.H, 1)
        # warm copper wash (multiply) + a vignette that sinks the photo into ink where the type sits
        self.parts.append('<div style="position:absolute;inset:0;background:#8a4a2a;mix-blend-mode:multiply;opacity:.35;z-index:2"></div>')
        self.parts.append('<div style="position:absolute;inset:0;z-index:3;background:linear-gradient(to bottom,rgba(0,0,0,.55) 0%,rgba(0,0,0,.05) 26%,'
                          'rgba(0,0,0,.55) 52%,rgba(0,0,0,.92) 72%,#000 100%);pointer-events:none"></div>')
        self.badge()
        TS = .78
        self.title(scale=TS, cx_shift=self._centre_shift(TS), y_ref=585)
        self.line("tagline", c["line"], S(1150) + di, S(54), max_w=self.W - 2 * 70)
        self._teaser_info(date_y=1222, edition_y=1280)

    def _teaser_arch(self):
        c, di = self.c, self.dy_info
        self.base(); self.badge()
        aw, ah = S(700), S(900) + self.dy_title
        ax, ay = (self.W - aw) // 2, S(70) + self.dy_top
        self.parts.append(f'<div data-tag="arch" style="position:absolute;left:{ax}px;top:{ay}px;width:{aw}px;height:{ah}px;border-radius:{aw // 2}px {aw // 2}px {S(16)}px {S(16)}px;'
                          f'border:3px solid {GOLD};overflow:hidden;z-index:4;box-shadow:0 0 60px rgba(201,151,28,.25)">'
                          f'<img src="{photo_uri(c["photo"])}" style="width:100%;height:100%;object-fit:cover;filter:contrast(1.1) saturate(1) brightness(1.15)">'
                          f'<div style="position:absolute;inset:0;background:#8a4a2a;mix-blend-mode:multiply;opacity:.2"></div>'
                          f'<div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0) 40%,rgba(0,0,0,.9) 100%);pointer-events:none"></div></div>')
        self.box("arch", ax, ay, aw, ah)
        TS = .6
        self.title(scale=TS, cx_shift=self._centre_shift(TS), y_ref=760)
        self.line("tagline", c["line"], S(1170) + di, S(40), max_w=self.W - 2 * 70)
        self.line("date", c["date"], S(1232) + di, S(56))
        self.line("edition", c["edition"], S(1290) + di, S(30), weight=400)
        self.pill("cta", c["cta"], S(1395) + di, h=S(90))

    def _teaser_trio(self):
        import math
        c, di = self.c, self.dy_info
        self.base(); self.badge()
        f = 1 + .45 * (self.H - BASE_H) / BASE_H               # frames grow with the extra height instead of leaving a dead middle
        fw, fh = round(S(300) * f), round(S(380) * f)
        lift = round((self.dy_title - self.dy_top) * .4)       # and drift toward the title as it moves down
        spec = [(S(60), S(345), -6), (S(450), S(300), 2), (S(810 - 40 * (f - 1) * 4), S(355), -4)]   # below the badge, loosely stacked
        for i, ((x, y, rot), ph) in enumerate(zip(spec, c["photos"])):
            y += self.dy_top + lift
            self.parts.append(f'<div data-tag="f{i + 1}" style="position:absolute;left:{x}px;top:{y}px;width:{fw}px;height:{fh}px;transform:rotate({rot}deg);'
                              f'background:#EDE6D8;padding:{S(14)}px {S(14)}px {S(58)}px;z-index:{4 + i};box-shadow:0 18px 40px rgba(0,0,0,.65)">'
                              f'<img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;filter:contrast(1.06) saturate(.92) brightness(.85)"></div>')
            r = math.radians(abs(rot))
            bw, bh = fw * math.cos(r) + fh * math.sin(r), fw * math.sin(r) + fh * math.cos(r)
            self.box(f"f{i + 1}", x + (fw - bw) / 2, y + (fh - bh) / 2, bw, bh)
        TS = .55
        self.title(scale=TS, cx_shift=self._centre_shift(TS), y_ref=770)
        self.line("tagline", c["line"], S(1170) + di, S(38), max_w=self.W - 2 * 70)
        self.line("date", c["date"], S(1232) + di, S(54))
        self.line("edition", c["edition"], S(1288) + di, S(30), weight=400)
        self.pill("cta", c["cta"], S(1395) + di, h=S(90))

    def _sold_out(self):
        c, di = self.c, self.dy_info
        self.base(); self.top_group(); self.title(); self.edition()
        bw = round(self.W * 1.04)
        bh = round(bw * 470 / 2000)
        by = S(1225) + di - bh // 2
        self.parts.append(f'<img src="{uri("sold_out_banner.png")}" data-tag="banner" style="position:absolute;left:{(self.W - bw) // 2}px;'
                          f'top:{by}px;width:{bw}px;height:{bh}px;transform:rotate(-5deg);z-index:11;'
                          f'box-shadow:0 14px 34px rgba(0,0,0,.6);border-radius:4px">')
        self.box("banner", (self.W - bw) // 2, by + 30, bw, bh - 30)
        self.line("date", c["date"], S(1415) + di, S(44))
        self.line("thanks", c["thanks"], S(1462) + di, S(36), max_w=self.W - 2 * 60)


async def render_poster(kind, content, canvas, out_png, style="plate", mask="asset"):
    """Validate, build and render one poster through the full gate stack. Returns the output path."""
    p = Poster(kind, content, canvas, style, mask)
    html = p.build()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    ignore_all = [("title", "sub1"), ("title", "sub2"), ("title", "count"), ("title", "headline"),
              ("carpet", "headline"), ("carpet", "detail"), ("carpet", "date"), ("carpet", "cta"), ("carpet", "title"),
              ("carpet", "sub1"), ("carpet", "sub2"), ("banner", "sub2"), ("day", "title"), ("arch", "title"), ("arch", "tagline"), ("arch", "badge"),
              ("title", "tagline"), ("title", "edition"), ("title", "date"), ("f1", "f2"), ("f2", "f3"), ("f1", "f3"), ("f1", "badge"), ("banner", "date"), ("banner", "title")]
    labels = {e[0] for e in p.elements}
    ignore = [pr for pr in ignore_all if pr[0] in labels and pr[1] in labels]
    text_pairs = [(lab, OFFWHITE, GROUND, 40, True) for lab in ("date", "status", "headline", "unit")]
    await B.render(html, out_png, p.W, p.H, elements=p.elements, containers=tuple(l for l in ("cta", "carpet", "arch") if l in labels),
                   collision_ignore=ignore, text_pairs=text_pairs,
                   bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain", "carpet", "banner", "photo"),
                   crop_tags=("plate", "sparkles", "grain", "photo", "arch"), page_bg=GROUND)
    return out_png


DEMO_DATE = "2026-11-10"
DEMO = [
    ("announce", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards",
                      status="Ticket sales open soon", note="More details soon", cta="Link in bio")),
    ("countdown", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", days=days_to_go(DEMO_DATE), cta="Link in bio")),
    ("tickets_open", dict(edition="Masquerade Sangeet Edition", headline="Tickets are live", date="10th November, 2026", cta="Link in bio")),
    ("sold_out", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", thanks="Thank you for the love")),
    ("save_the_date", dict(edition="Masquerade Sangeet Edition", day="10", month="November", year="2026", time="4:30 PM Onwards", cta="Link in bio")),
]

TEASERS = [
    ("teaser_full", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", line="Lights. Music. Masks.",
                         photo="03", cta="Link in bio"), "diya", "copper"),
    ("teaser_full", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", line="Ticket sales open soon",
                         photo="05", cta="Link in bio"), "diya", "copper"),
    ("teaser_arch", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", line="Save the date",
                         photo="12", cta="Link in bio"), "diya", "copper"),
    ("teaser_trio", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", line="The dance floor is waiting",
                         photos=["07", "08", "09"], cta="Link in bio"), "diya", "copper"),
]

async def _demo():
    out = os.path.join(ROOT, "out", "discodiwali")
    async with B.session():
        for canvas in ("feed", "story"):
            for kind, content in DEMO:
                await render_poster(kind, content, canvas, os.path.join(out, f"{kind}_{canvas}.png"))
        for kind, content in DEMO:
            await render_poster(kind, content, "feed", os.path.join(out, f"{kind}_feed_stroke.png"), style="stroke")
        for kind, content in DEMO:
            await render_poster(kind, content, "feed", os.path.join(out, f"{kind}_feed_diya.png"), style="diya", mask="copper")
        for kind, content in DEMO[:1] + DEMO[4:]:
            await render_poster(kind, content, "feed", os.path.join(out, f"{kind}_feed_red.png"), style="stroke", mask="red")
        tdir = os.path.join(out, "teasers")
        for i, (kind, content, st, mk) in enumerate(TEASERS, 1):
            for canvas in ("story", "feed"):
                await render_poster(kind, content, canvas, os.path.join(tdir, f"t{i}_{kind}_{canvas}.png"), style=st, mask=mk)
        pdir = os.path.join(out, "photo")
        for ph in ("03", "05", "12"):
            for canvas in ("feed", "story"):
                await render_poster("announce", dict(DEMO[0][1], photo=ph), canvas, os.path.join(pdir, f"announce_{ph}_{canvas}.png"), style="photo", mask="copper")
        bdir = os.path.join(out, "blue")
        for kind, content in DEMO:
            for canvas in ("feed", "story"):
                await render_poster(kind, content, canvas, os.path.join(bdir, f"{kind}_{canvas}.png"), style="blue", mask="copper")
        for i, (kind, content, st, mk) in enumerate(TEASERS, 1):
            await render_poster(kind, content, "story", os.path.join(bdir, f"t{i}_{kind}_story.png"), style="blue", mask="copper")
    print("demo set done ->", out)

if __name__ == "__main__":
    asyncio.run(_demo())
