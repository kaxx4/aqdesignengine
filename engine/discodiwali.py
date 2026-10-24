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
TYPOS = ("editorial", "foil", "outline", "vertical", "stack", "minimal", "whisper")   # type treatments for style="photo" announce
# Composition presets for style="photo" announce. mask = (dx, dy, scale, tilt) in reference px / multiplier / degrees; title = (scale, y_ref).
# The edition lines and info stack are placed RELATIVE to the title's real bottom, so every preset keeps the lockup's notch tuck.
LAYOUTS = {"classic": {},
           "mask_hero":   dict(mask=(80, -60, 1.5, 6),   title=(.84, 500)),     # a huge mask bleeding off the right edge, title lower
           "title_hero":  dict(mask=(470, 20, .62, 8),   title=(1.04, 350)),     # the lockup bleeds wide, the mask shrinks to a corner accent
           "mask_behind": dict(mask=(-100, 170, 1.25, -6), title=(.9, 430))}   # the mask sits BEHIND the title: the lockup overprints it
STYLES = ("plate", "diya", "stroke", "blue", "photo")   # plate: beaded celestial corners. diya: navy and gold lotus-diya corners (no string lights). stroke: plain ink ground, red-stroked mask. photo: a real event photo, graded navy, with the soft diya plate SCREEN-blended over it, plus editorial type. blue: full-bleed navy diya pattern under a colour-dodge blue layer and disco beams (blend-mode recipe, scratchpad/dd_blend_lab.py v7)
LAUNCH_KINDS = ("story_launch", "wa_poster", "wa_dp", "story_ref", "poster_ref")   # the launch pack sets every line of type in NeutralFace
KINDS = ("announce", "countdown", "tickets_open", "sold_out", "save_the_date", "teaser_full", "teaser_arch", "teaser_trio", "story_launch", "wa_poster", "wa_dp", "story_ref", "poster_ref")
REQUIRED = {
    "announce":     ("edition", "date", "time", "status", "cta"),
    "countdown":    ("edition", "date", "days", "cta"),
    "tickets_open": ("edition", "headline", "cta"),
    "sold_out":     ("edition", "date", "thanks"),
    "save_the_date": ("edition", "day", "month", "year", "time", "cta"),
    "teaser_full":  ("edition", "date", "line", "photo", "cta"),
    "teaser_arch":  ("edition", "date", "line", "photo", "cta"),
    "teaser_trio":  ("edition", "date", "line", "photos", "cta"),
    "story_launch": ("edition", "status", "photo"),
    "wa_poster":    ("edition", "date", "time", "status", "photo"),
    "wa_dp":        ("edition",),
    "story_ref":    ("edition", "photo"),
    "poster_ref":   ("edition", "status"),
}
OPTIONAL = {"announce": ("note", "photo"), "countdown": ("unit",), "tickets_open": ("detail", "date"), "sold_out": (), "save_the_date": (), "teaser_full": (), "teaser_arch": (), "teaser_trio": (), "story_launch": ("note", "date", "time"), "wa_poster": ("note",), "wa_dp": ("date",), "story_ref": ("dim", "status", "note", "link", "date", "time", "venue", "address"), "poster_ref": ("dim", "note", "link", "photo", "date", "time", "venue")}

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
    allowed = {"story_launch": ("story",), "wa_poster": ("feed",), "wa_dp": ("square",), "story_ref": ("story",), "poster_ref": ("feed",)}.get(kind, ("feed", "story"))
    if canvas not in allowed:
        raise ValueError(f"{kind}: canvas must be one of {allowed}, got {canvas!r}")
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
    def __init__(self, kind, content, canvas, style="plate", mask="asset", typo="editorial", mask_tilt=0, mask_scale=1.0, layout="classic"):
        validate_brief(kind, content, canvas)
        if style not in STYLES:
            raise ValueError(f"style must be one of {STYLES}, got {style!r}")
        if mask not in MASKS:
            raise ValueError(f"mask must be one of {MASKS}, got {mask!r}")
        if typo not in TYPOS:
            raise ValueError(f"typo must be one of {TYPOS}, got {typo!r}")
        self.kind, self.c, self.canvas, self.style, self.mask, self.typo = kind, content, canvas, style, mask, typo
        if kind in ("story_launch", "wa_poster", "story_ref", "poster_ref"):
            style = self.style = "photo"                      # these kinds ARE the photo direction
        if kind == "story_launch":
            # ONE mask placement for every story (user, 2026-10-13: "use story_01 as the reference"): the classic position, no tilt, no scale.
            # Layout presets and mask_tilt/mask_scale are ignored here, because the presets move the mask and the title together.
            layout, mask_tilt, mask_scale = "classic", 0, 1.0
        self.type_scale = 1.14 if kind == "story_launch" else 1.0      # a story is read at a third of the size: its type is scaled up
        self.neutral_only = kind in LAUNCH_KINDS                      # launch pack: ALL type is NeutralFace (user, 2026-10-13)
        self.no_pill = kind in ("story_launch", "wa_poster", "story_ref", "poster_ref")   # no CTA pill: a link sticker goes there (story) / there is no link (WhatsApp)
        if layout not in LAYOUTS:
            raise ValueError(f"layout must be one of {tuple(LAYOUTS)}, got {layout!r}")
        self.layout = layout
        L = LAYOUTS[layout]
        self.mask_dx, self.mask_dy, ms, mt = L.get("mask", (0, 0, 1.0, 0))
        self.mask_tilt = mask_tilt or mt                                  # explicit kwargs win over the preset
        self.mask_scale = mask_scale if mask_scale != 1.0 else ms
        self.title_scale, self.title_yref = L.get("title", (1.0, 390))
        self.W, self.H = core.SIZES[canvas]
        dh = self.H - BASE_H
        self.dy_top, self.dy_title, self.dy_info = (round(dh * .15), round(dh * .62), dh) if dh > 0 else (0, 0, 0)   # only a TALLER canvas shifts
        if kind == "story_launch":                             # the feed composition shifted clear of Instagram's top bar; pill zone left for the sticker
            self.dy_top, self.dy_title, self.dy_info = 130, 150, 150
        if kind == "wa_poster":
            self.dy_info = 24
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
        if self.no_pill:
            return
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
        # TEXT BUDGET RULE (user, 2026-10-13): the more of the canvas a photo owns, the less copy it carries. The sparse typos let more photo through.
        sparse = self.typo in ("minimal", "whisper")
        light = sparse or self.kind == "story_launch"      # a story keeps more photo: its copy sits in one band, not over the whole frame
        P.append(f'<img data-tag="photo" src="{photo_uri(ph)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1;'
                 f'filter:contrast(1.12) saturate(.95) brightness({1.1 if sparse else 1.05 if light else .95})">')
        P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,#0A1E7A,#050A33);'
                 f'mix-blend-mode:multiply;opacity:{.42 if sparse else .45 if light else .6}"></div>')
        plate = "bg_diya_portrait.jpg"
        ex = "mix-blend-mode:screen;"
        if H <= BASE_H:
            self.img(plate, 0, 0, W, H, z=3, tag="plate", extra="object-fit:cover;" + ex)
        else:
            self.img(plate, 0, 0, W, BASE_H, z=3, tag="plate", extra=ex)
            self.img(plate, 0, H - BASE_H, W, BASE_H, z=3, tag="plate",
                     extra=ex + "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
        if sparse:   # a bottom shade so the one line of copy that remains still reads on a bright photo
            P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:4;pointer-events:none;background:linear-gradient(to bottom,rgba(0,0,0,0) 58%,rgba(0,0,0,.72) 100%)"></div>')
        P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:4;pointer-events:none;background:radial-gradient(ellipse 66% 40% at 50% 66%,'
                 f'rgba(0,0,0,{.26 if sparse else .55 if light else .62}),rgba(0,0,0,{.1 if sparse else .22 if light else .3}) 65%,rgba(0,0,0,0) 100%)"></div>')

    def raw(self, label, html, cx, cy, w, h, css="", z=12):
        """A centred block of arbitrary markup with its declared box. For the editorial type, where one line mixes faces."""
        ts = 1.0 if label in ("sub1", "sub2", "cue") else self.type_scale   # the notch tuck and the cue keep their size
        if ts != 1 and label in ("date", "month", "time", "status", "note"):
            mid = S(1105) + self.dy_info                  # just above the date: scaled type spreads its lines DOWN from it,
            cy = round(mid + (cy - mid) * ts)             # otherwise bigger type simply lands on its neighbours
        tf = "translate(-50%,-50%)" + (f" scale({ts})" if ts != 1 else "")
        self.parts.append(f'<div data-tag="{label}" style="position:absolute;left:{cx}px;top:{cy}px;transform:{tf};white-space:nowrap;'
                          f'line-height:1;color:{OFFWHITE};z-index:{z};{css}">{html}</div>')
        self.box(label, cx - w * ts / 2, cy - h * ts / 2, w * ts, h * ts)

    # ---- type treatments for style="photo" -----------------------------------------------------------------------
    GL = "#E8C063"                                              # gold lifted for small type on a photo ground
    FOIL = ("background:linear-gradient(180deg,#FFF6CF 0%,#F0C65A 34%,#A8721A 60%,#F7DC86 82%,#C48A22 100%);-webkit-background-clip:text;"
            "background-clip:text;-webkit-text-fill-color:transparent;color:transparent;")

    def _title_for_layout(self):
        ts, yr = self.title_scale, self.title_yref
        shift = 0 if self.layout == "classic" else self._centre_shift(ts)
        self.title(scale=ts, cx_shift=shift, y_ref=yr)
        # where the lockup really ends and its notch sits, for the edition lines
        self._tcx = S(30) + shift + S(580 * ts) + S(63 * ts)
        self._tbottom = yr + 670 * ts

    def _announce_editorial(self):
        self.base(); self.top_group(); self._title_for_layout()
        if self.typo not in ("vertical", "minimal", "whisper"):
            self._edition_lines()
        getattr(self, "_info_" + self.typo)()

    def _edition_lines(self):
        cx = self._tcx
        b = self._tbottom
        if self.neutral_only:                        # launch pack: the edition name is a real line of type, not a caption (user, 2026-10-13)
            self.raw("sub1", "MASQUERADE SANGEET", cx, S(b - 118) + self.dy_title, S(640), S(52),
                     "font-family:var(--e);font-weight:600;font-size:%dpx;letter-spacing:.34em;text-indent:.34em" % S(46))
        else:
            self.raw("sub1", "MASQUERADE SANGEET", cx, S(b - 108) + self.dy_title, S(560 * min(self.title_scale, 1.0)), S(40),
                     "font-family:var(--e);font-weight:600;font-size:%dpx;letter-spacing:.34em;text-indent:.34em" % S(26))
        if self.neutral_only:                        # NeutralFace is an uppercase face: a small tracked gold EDITION, not a 58px serif word
            self.raw("sub2", "Edition", cx, S(b - 50) + self.dy_title, S(210), S(34),
                     f"font-family:var(--e);font-weight:600;font-size:{S(28)}px;letter-spacing:.42em;text-indent:.42em;color:{self.GL}")
        else:
            self.raw("sub2", "Edition", cx, S(b - 52) + self.dy_title, S(260), S(60),
                     f"font-family:var(--s);font-style:italic;font-size:{S(58)}px;color:{self.GL}")

    def _day_rest(self):
        day, _, rest = self.c["date"].upper().partition(" ")
        return day.rstrip("TH"), rest

    def _info_editorial(self):
        c, di, W, GL = self.c, self.dy_info, self.W, self.GL
        day, rest = self._day_rest()
        self.raw("date", f'<span style="font-family:var(--s);font-style:italic;font-weight:400;font-size:{S(150)}px;color:{OFFWHITE}">{day}</span>'
                         f'<span style="font-family:var(--e);font-weight:700;font-size:{S(54)}px;letter-spacing:.06em;margin-left:{S(18)}px;vertical-align:{S(34)}px">{rest}</span>',
                 W // 2, S(1128) + di, S(820), S(150), "text-shadow:0 2px 24px rgba(0,0,0,.6)")
        rule = f'<span style="display:inline-block;width:{S(120)}px;height:2px;background:{GOLD};vertical-align:middle"></span>'
        self.raw("time", f'{rule}<span style="margin:0 {S(26)}px">{c["time"].upper()}</span>{rule}', W // 2, S(1232) + di, S(760), S(36),
                 f"font-family:var(--m);font-weight:700;font-size:{S(26)}px;letter-spacing:.22em;color:{GL}")
        self.raw("status", c["status"].upper(), W // 2, S(1290) + di, S(700), S(40),
                 f"font-family:var(--e);font-weight:600;font-size:{S(40) if self.neutral_only else S(32)}px;letter-spacing:.2em")
        if c.get("note"):
            self.raw("note", c["note"], W // 2, S(1340) + di, S(420), S(46),
                     f"font-family:var(--s);font-style:italic;font-size:{S(38) if not self.neutral_only else S(28)}px;color:{GL}")
        self.pill("cta", c.get("cta", ""), S(1412) + di, h=S(80))

    def _info_foil(self):
        """A gold-foil italic numeral (a gradient clipped to the glyphs), with the month and year stacked in tracked caps beside it."""
        c, di, W, GL = self.c, self.dy_info, self.W, self.GL
        day, rest = self._day_rest()
        month, _, year = rest.partition(", ")
        self.raw("date", f'<span style="font-family:var(--s);font-style:italic;font-size:{S(250)}px;{self.FOIL}filter:drop-shadow(0 4px 18px rgba(0,0,0,.55))">{day}</span>'
                         f'<span style="display:inline-block;margin-left:{S(30)}px;text-align:left;line-height:1.3;font-family:var(--e);font-weight:700;'
                         f'font-size:{S(46)}px;letter-spacing:.26em;vertical-align:{S(60)}px">{month}<br><span style="color:{GL}">{year}</span></span>',
                 W // 2, S(1148) + di, S(760), S(210))
        if self.neutral_only:      # launch pack: time small, STATUS the big line, note smaller (the reference poster's hierarchy)
            self.raw("time", c["time"].upper(), W // 2, S(1290) + di, S(700), S(34), f"font-family:var(--m);font-weight:700;font-size:{S(26)}px;letter-spacing:.18em;color:{GL}")
            self.raw("status", c["status"], W // 2, S(1340) + di, S(900), S(60), f"font-family:var(--e);font-weight:600;font-size:{S(46)}px")
            if c.get("note"):
                self.raw("note", c["note"], W // 2, S(1388) + di, S(520), S(40), f"font-family:var(--e);font-weight:600;font-size:{S(28)}px")
            self.pill("cta", c.get("cta", ""), S(1420) + di, h=S(76))
            return
        self.raw("time", c["time"].upper() + f'&nbsp;&nbsp;·&nbsp;&nbsp;{c["status"].upper()}', W // 2, S(1262) + di, S(900), S(34),
                 f"font-family:var(--m);font-weight:700;font-size:{S(21)}px;letter-spacing:.18em;color:{GL}")
        self.raw("status", c.get("note") or "Tickets, soon.", W // 2, S(1322) + di, S(480), S(60), f"font-family:var(--s);font-style:italic;font-size:{S(56)}px")
        self.pill("cta", c.get("cta", ""), S(1420) + di, h=S(76))

    def _info_outline(self):
        """Hollow numerals: transparent fill, a hairline stroke, so the photo reads THROUGH the date. The month is solid beside it."""
        c, di, W, GL = self.c, self.dy_info, self.W, self.GL
        day, rest = self._day_rest()
        month, _, year = rest.partition(", ")
        self.raw("date", f'<span style="font-family:var(--d);font-weight:900;font-size:{S(262)}px;-webkit-text-fill-color:transparent;-webkit-text-stroke:3px {OFFWHITE}">{day}</span>',
                 S(282), S(1172) + di, S(400), S(250))
        self.raw("month", f'<span style="font-family:var(--d);font-weight:900;font-size:{S(84)}px;letter-spacing:.02em">{month}</span><br>'
                          f'<span style="font-family:var(--d);font-weight:900;font-size:{S(84)}px;-webkit-text-fill-color:transparent;-webkit-text-stroke:2px {GL}">{year}</span>',
                 S(838), S(1172) + di, S(440), S(200), "line-height:1.02;text-align:left")
        if self.neutral_only:      # launch pack: time small, STATUS the big line, note smaller
            self.raw("time", c["time"].upper(), W // 2, S(1290) + di, S(700), S(34), f"font-family:var(--m);font-weight:700;font-size:{S(26)}px;letter-spacing:.18em;color:{GL}")
            self.raw("status", c["status"], W // 2, S(1338) + di, S(900), S(60), f"font-family:var(--e);font-weight:600;font-size:{S(46)}px")
            if c.get("note"):
                self.raw("note", c["note"], W // 2, S(1384) + di, S(520), S(40), f"font-family:var(--e);font-weight:600;font-size:{S(28)}px")
            self.pill("cta", c.get("cta", ""), S(1414) + di, h=S(76))
            return
        self.raw("time", f'{c["time"].upper()}&nbsp;&nbsp;/&nbsp;&nbsp;{c["status"].upper()}', W // 2, S(1318) + di, S(900), S(34),
                 f"font-family:var(--m);font-weight:700;font-size:{S(21)}px;letter-spacing:.18em;color:{GL}")
        if c.get("note"):
            self.raw("note", c["note"], W // 2, S(1372) + di, S(420), S(46), f"font-family:var(--s);font-style:italic;font-size:{S(40)}px;color:{GL}")
        self.pill("cta", c.get("cta", ""), S(1414) + di, h=S(76))

    def _info_vertical(self):
        """Rail type: the edition and the cause run vertically up both edges; the centre is one italic date line over tracked meta."""
        c, di, W, GL = self.c, self.dy_info, self.W, self.GL
        def rail(label, text, x):
            L, T = S(360), S(26)
            self.raw(label, text, x, S(1262) + di, L, T,
                     f"font-family:var(--m);font-weight:700;font-size:{S(18)}px;letter-spacing:.2em;color:{GL};transform:translate(-50%,-50%) rotate(-90deg)")
            self.elements[-1] = (label, round(x - T / 2), round(S(1262) + di - L / 2), T, L)     # the box as DRAWN: rotated
        rail("railL", c["edition"].upper(), S(58))
        rail("railR", "ALL FOR CHARITY", W - S(58))
        self.raw("date", c["date"], W // 2, S(1160) + di, S(760), S(110),
                 f"font-family:var(--s);font-style:italic;font-size:{S(92)}px;text-shadow:0 2px 24px rgba(0,0,0,.6)")
        self.raw("time", f'<span style="color:{GL}">{c["time"].upper()}</span>', W // 2, S(1244) + di, S(560), S(34),
                 f"font-family:var(--m);font-weight:700;font-size:{S(24)}px;letter-spacing:.3em")
        self.raw("status", c["status"].upper(), W // 2, S(1296) + di, S(700), S(36),
                 f"font-family:var(--e);font-weight:600;font-size:{S(30)}px;letter-spacing:.24em")
        self.pill("cta", c["cta"], S(1408) + di, h=S(80))

    def _info_minimal(self):
        """Three things only: the title, ONE foil date line, the CTA. The photo gets everything else."""
        c, di, W = self.c, self.dy_info, self.W
        self.raw("date", c["date"], W // 2, S(1262) + di, S(900), S(110),
                 f"font-family:var(--s);font-style:italic;font-size:{S(96)}px;{self.FOIL}filter:drop-shadow(0 2px 1px rgba(0,0,0,.95)) drop-shadow(0 0 22px rgba(0,0,0,.75))")
        self.pill("cta", c["cta"], S(1404) + di, h=S(76))

    def _info_whisper(self):
        """The title and one mono line. No pill, no edition, no time: the date and where to go, set small."""
        c, di, W = self.c, self.dy_info, self.W
        self.raw("date", f'{c["date"].upper()}&nbsp;&nbsp;·&nbsp;&nbsp;{c["cta"].upper()}', W // 2, S(1410) + di, S(900), S(36),
                 f"font-family:var(--m);font-weight:700;font-size:{S(26)}px;letter-spacing:.24em;color:{self.GL};text-shadow:0 2px 14px rgba(0,0,0,.8)")

    def _info_stack(self):
        """A heavy NeutralFace line, the numeral solid and the month hollow, over one mono meta line and a serif italic kicker."""
        c, di, W, GL = self.c, self.dy_info, self.W, self.GL
        day, rest = self._day_rest()
        month, _, year = rest.partition(", ")
        self.raw("date", f'<span style="font-family:var(--d);font-weight:900;font-size:{S(200)}px;letter-spacing:.01em">{day}</span>'
                         f'<span style="font-family:var(--d);font-weight:900;font-size:{S(200)}px;margin-left:{S(26)}px;-webkit-text-fill-color:transparent;'
                         f'-webkit-text-stroke:3px {OFFWHITE}">{month[:3]}</span>',
                 W // 2, S(1160) + di, S(760), S(170), "text-shadow:0 4px 28px rgba(0,0,0,.5)")
        self.raw("time", f'{year}&nbsp;&nbsp;·&nbsp;&nbsp;{c["time"].upper()}', W // 2, S(1262) + di, S(700), S(34),
                 f"font-family:var(--m);font-weight:700;font-size:{S(25)}px;letter-spacing:.26em;color:{GL}")
        self.raw("status", c["status"], W // 2, S(1326) + di, S(640), S(60), f"font-family:var(--s);font-style:italic;font-size:{S(54)}px")
        if c.get("note"):
            self.raw("note", c["note"], W // 2, S(1384) + di, S(420), S(44), f"font-family:var(--m);font-weight:700;font-size:{S(22)}px;letter-spacing:.24em;color:{GL}")
        self.pill("cta", c.get("cta", ""), S(1420) + di, h=S(76))

    def _mask_xf(self):
        return f"transform:rotate({self.mask_tilt}deg) scale({self.mask_scale});transform-origin:60% 40%;" if (self.mask_tilt or self.mask_scale != 1.0) else ""

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
            self.img("mask_copper.png", S(370 - 160 * u + self.mask_dx), S(40 - 215 * u + self.mask_dy) + self.dy_top, S(1680 * u), z=6, tag="mask",
                     extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));" + self._mask_xf())
        elif self.style == "stroke":
            # mask_stroked.png is the mask padded by 90px of red stroke on every side (scratchpad/make_mask_stroke.py)
            pad = round(90 * MK * K)
            self.img("mask_stroked.png", S(415 - 190 * MK) - pad, S(-145) + self.dy_top - pad, round(mw * 2180 / 2000), z=6, tag="mask",
                     extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));")
        else:
            if self.kind == "story_launch":
                # fitted so the SILVER mask's visible outline lands on the COPPER mask's story_01 footprint (measured from both alpha channels:
                # copper outline 332,164 to 1028,622 on the 1080 canvas; silver at left 254, top 60, width 832 reproduces it within 3px of height)
                self.img("mask.png", 254, 60, 832, z=6, tag="mask", extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
            else:
                self.img("mask.png", S(415 - 190 * MK + self.mask_dx), S(-145 + self.mask_dy) + self.dy_top, mw, z=6, tag="mask",
                         extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.55));" + self._mask_xf())
        if self.style != "diya":              # the navy diya direction is quiet: the lotus-diya plate carries the light
            self.img("string_lights.png", S(105), S(-150) + self.dy_top, S(1560), z=5, tag="lights")   # z 5 < mask z 6: the mask is IN FRONT of the lights (user, 2026-10-13)
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
    TEXT_TAGS = ("sub1", "sub2", "date", "month", "time", "status", "note", "cue", "edition", "linkpill")
    # Launch-pack type is WHITE with a thin BLACK border, like the reference launch poster (user, 2026-10-13). One !important override on the
    # text elements and everything inside them, so it beats every treatment's inline colour: gold lines, the foil gradient clip and the hollow
    # numerals all become solid white. paint-order puts the fill over the stroke, so the 4px stroke shows as a 2px border OUTSIDE the glyph
    # and never thins the letters, at any type size.
    WHITE_BORDER_CSS = ("".join(f'[data-tag="{t}"],[data-tag="{t}"] *,' for t in TEXT_TAGS).rstrip(",") +
                        "{color:#fff!important;-webkit-text-fill-color:#fff!important;background:none!important;-webkit-background-clip:border-box!important;"
                        "background-clip:border-box!important;-webkit-text-stroke:4px #000!important;paint-order:stroke fill!important;"
                        # NeutralFace ONLY (user, 2026-10-13): forced on every text element so no inline face can survive, the two cuts it ships
                        # (Bold for everything, Regular for the one 'EDITION' word, as in the reference poster), natural spacing, no italics
                        "font-family:var(--d)!important;font-weight:700!important;font-style:normal!important;letter-spacing:.01em!important;"
                        "text-indent:0!important;text-transform:uppercase!important}"
                        '[data-tag="sub2"],[data-tag="sub2"] *{font-weight:400!important}')

    @staticmethod
    def neutralise(html):
        """Re-set every text face in NeutralFace (the brand display face, --d): the serif italic, mono and Eina lines all become NeutralFace.
        NeutralFace is an uppercase face, so the replacements force uppercase; weights map to its two cuts (400 Regular, 700 Bold).
        Safe on the whole document: the base64 image payloads cannot contain these CSS strings."""
        for old, new in (("font-family:var(--s);font-style:italic", "font-family:var(--d);font-style:normal;font-weight:400;text-transform:uppercase"),
                         ("font-family:var(--m)", "font-family:var(--d);text-transform:uppercase"),
                         ("font-family:var(--e);font-weight:600", "font-family:var(--d);font-weight:700;text-transform:uppercase"),
                         ("font-family:var(--e)", "font-family:var(--d);text-transform:uppercase")):
            html = html.replace(old, new)
        return html

    def build(self):
        getattr(self, "_" + self.kind)()
        self.overlays()
        page = B.page(self.W, self.H, GROUND, "".join(self.parts), grain=False)
        if not self.neutral_only:
            return page
        page = self.neutralise(page)                                      # the whole page, so the default .p font rule is NeutralFace too
        return page.replace("</style>", self.WHITE_BORDER_CSS + "</style>", 1)

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

    # ---- launch pack: stories, WhatsApp poster, WhatsApp DP ---------------------------------------------------------
    def _poster_ref(self):
        """The FEED poster REMADE FROM THE USER'S REFERENCE (2026-10-13). Same family as `story_ref`, on the diya plate instead of a photo.
        Measured off the reference after cropping its screenshot frame (7px left/top, 5px right/bottom) and scaling to 1080x1350: badge
        30..297 x 122..370, copper mask outline 343..1035 x 108..560, ball-free title 35..1071 x 461..1012, edition lines centred at x 612,
        status and note at x 540, link pill 316..766 x 1118..1221. The lights are fitted to the reference's bulbs. No disco ball, no date/time."""
        c, W, P = self.c, self.W, self.parts
        P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        if c.get("photo"):
            # photo variant (bulk WhatsApp posters): a real event photo edge to edge, graded exactly like story_ref, in place of the diya plate
            P.append(f'<img data-tag="photo" src="{photo_uri(c["photo"])}" style="position:absolute;inset:0;width:{W}px;height:{self.H}px;object-fit:cover;'
                     f'z-index:1;filter:contrast(1.08) saturate(1.0) brightness(.92)">')
            P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,rgba(8,6,30,.55) 0%,'
                     'rgba(8,6,30,0) 30%,rgba(0,0,0,0) 62%,rgba(0,0,0,.35) 100%)"></div>')
        else:
            self.img("bg_diya_portrait.jpg", 0, 0, W, self.H, z=1, tag="plate", extra="object-fit:cover;")
        if c.get("dim"):
            P.append(f'<div data-tag="dim" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:rgba(0,0,0,{c["dim"]})"></div>')
        self.img("string_lights.png", 160, -53, 1045, z=5, tag="lights")
        k = .4925                                         # copper mask: visible outline 343..1035 x 108..560
        self.img("mask_copper.png", round(343 - 157 * k), round(108 - 211 * k), round(1680 * k), z=6, tag="mask",
                 extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
        self.box("mask", 343, 108, 692, 452)
        self.img("live_badge.png", 30, 122, 267, z=8, tag="badge"); self.box("badge", 30, 122, 267, 248)
        t = .6034                                         # ball-free title lockup: visible outline 35..1071 x 461..1012
        self.img("title_lockup_noball.png", round(35 - 265 * t), round(461 - 401 * t), round(2000 * t), z=9, tag="title")
        self.box("title", 35, 461, 1036, 551)
        self.raw("sub1", "MASQUERADE SANGEET", 612, 917, 520, 44, "font-family:var(--e);font-weight:600;font-size:38px")
        self.raw("sub2", "Edition", 612, 962, 170, 40, "font-family:var(--e);font-weight:400;font-size:37px")
        link = c.get("link", "Link in bio")
        nolink = link is False                            # WhatsApp: nothing to link to, so no pill, and the info lines drop into the freed space
        dy = 62 if nolink else 0
        if c.get("date") or c.get("venue"):               # logistics (user, 2026-10-24): compact block, status/note pulled up to make room
            P.append('<div data-tag="infoshade" style="position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(180deg,'
                     'rgba(0,0,0,0) 52%,rgba(0,0,0,.5) 68%,rgba(0,0,0,.68) 100%)"></div>')
            self.raw("status", c["status"], 540, 1034, 900, 52, "font-family:var(--e);font-weight:600;font-size:44px")
            if c.get("note"):
                self.raw("note", c["note"], 540, 1104, 900, 84, "font-family:var(--e);font-weight:700;font-size:72px")
            if c.get("date"):
                self.raw("when", c["date"], 540, 1186, 900, 46, "font-family:var(--e);font-weight:700;font-size:40px")
            if c.get("time"):
                self.raw("clock", c["time"], 540, 1230, 900, 40, "font-family:var(--e);font-weight:700;font-size:36px")
            if c.get("venue"):
                self.raw("venue", c["venue"], 540, 1286, 960, 40, "font-family:var(--e);font-weight:700;font-size:34px")
            return
        self.raw("status", c["status"], 538, 1030 + dy, 700, 52, "font-family:var(--e);font-weight:600;font-size:44px")
        if c.get("note"):
            self.raw("note", c["note"], 540, 1075 + dy, 350, 34, "font-family:var(--e);font-weight:600;font-size:28px")
        if nolink:
            return
        P.append(f'<div data-tag="linkpill" style="position:absolute;left:316px;top:1118px;width:450px;height:103px;border-radius:22px;'
                 f'border:2px solid rgba(190,150,60,.75);background:rgba(8,6,10,.62);z-index:12;display:flex;align-items:center;justify-content:center;'
                 f'font-family:var(--e);font-weight:600;font-size:56px;line-height:1;text-transform:uppercase">{link}</div>')
        self.box("linkpill", 316, 1118, 450, 103)

    def _story_ref(self):
        """The launch story REMADE FROM THE USER'S REFERENCE IMAGE (2026-10-13, "remake this, same to same"). Every number below was MEASURED off
        that image after scaling it to 1080x1920 and removing its screenshot frame (about 18px left, 25px top); the lights were fitted by
        matching six bulb positions at 0.55x, all within 6px. Differences from `story_launch`, all deliberate: no diya plate (the photo runs
        to the corners), no disco ball on the title (the reference has none; `title_lockup_noball.png` is a derived copy, the original is
        untouched), a 38px WHITE regular EDITION instead of a small gold one, a larger note, no 'photo dim' ellipse, and 'LINK IN BIO' as
        real text in a soft gold-edged pill instead of arrows. The PHOTO is the one thing that cannot be reproduced from the reference: it
        is whichever library photo is passed in `photo`."""
        c, W, P = self.c, self.W, self.parts
        ph = c.get("photo", "05")
        P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        P.append(f'<img data-tag="photo" src="{photo_uri(ph)}" style="position:absolute;inset:0;width:{W}px;height:{self.H}px;object-fit:cover;z-index:1;'
                 f'filter:contrast(1.08) saturate(1.0) brightness(.92)">')
        P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,rgba(8,6,30,.55) 0%,'
                 'rgba(8,6,30,0) 30%,rgba(0,0,0,0) 62%,rgba(0,0,0,.35) 100%)"></div>')
        if c.get("venue") or c.get("date"):               # logistics block: sink the lower third so the info reads on bright photos
            P.append('<div data-tag="infoshade" style="position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(180deg,'
                     'rgba(0,0,0,0) 56%,rgba(0,0,0,.5) 72%,rgba(0,0,0,.68) 100%)"></div>')
        if c.get("dim"):                                   # bright photo (neon pink / purple): sink it so the lockup and type keep their contrast
            P.append(f'<div data-tag="dim" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:rgba(0,0,0,{c["dim"]})"></div>')
        self.img("string_lights.png", 158, -59, 1100, z=5, tag="lights")
        k = .499                                           # copper mask: visible outline 357..1059 x 98..536 on the canvas
        self.img("mask_copper.png", round(358 - 157 * k), round(98 - 211 * k), round(1680 * k), z=6, tag="mask",
                 extra="filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
        self.box("mask", 358, 98, 701, 438)
        self.img("live_badge.png", 45, 124, 264, z=8, tag="badge"); self.box("badge", 45, 124, 264, 250)
        t = .59                                            # title lockup, no ball: visible outline 38..1051 x 480..1018
        self.img("title_lockup_noball.png", round(38 - 265 * t), round(480 - 401 * t), round(2000 * t), z=9, tag="title")
        self.box("title", 38, 480, 1013, 538)
        self.raw("sub1", "MASQUERADE SANGEET", 617, 938, 520, 46,
                 "font-family:var(--e);font-weight:600;font-size:40px")
        self.raw("sub2", "Edition", 617, 981, 180, 42, "font-family:var(--e);font-weight:400;font-size:38px")
        if c.get("status"):
            self.raw("status", c["status"], 543, 1136, 880, 62, "font-family:var(--e);font-weight:600;font-size:52px")
        if c.get("note"):
            big = bool(c.get("date") or c.get("venue"))     # with the logistics block the note is the PRICE: make it a second hero line
            self.raw("note", c["note"], 541, 1234 if big else 1215, 900 if big else 500, 100 if big else 44,
                     f"font-family:var(--e);font-weight:{700 if big else 600};font-size:{88 if big else 38}px")
        # Optional logistics block (user, 2026-10-23: bulk stories mention date, time, location). Supplied facts only. The pill drops below it.
        py = 1314
        sh = 0 if (c.get("status") or c.get("note")) else -90      # status and note dropped: pull the block up under the edition lines
        if c.get("date") or c.get("venue"):
            if c.get("date"):
                self.raw("when", c["date"], 541, 1316 + sh, 960, 54, "font-family:var(--e);font-weight:700;font-size:46px")
            if c.get("time"):
                self.raw("clock", c["time"], 541, 1370 + sh, 960, 50, "font-family:var(--e);font-weight:700;font-size:42px")
            if c.get("venue"):
                self.raw("venue", c["venue"], 541, 1436 + sh, 960, 50, "font-family:var(--e);font-weight:700;font-size:40px")
            if c.get("address"):
                self.raw("address", c["address"], 541, 1484 + sh, 960, 40, "font-family:var(--e);font-weight:400;font-size:32px")
            py = (1546 if c.get("address") else 1500) + sh
        link = c.get("link", "Link in bio")
        P.append(f'<div data-tag="linkpill" style="position:absolute;left:342px;top:{py}px;width:382px;height:82px;border-radius:22px;'
                 f'border:2px solid rgba(222,180,100,.6);background:rgba(236,200,150,.22);z-index:12;display:flex;align-items:center;justify-content:center;'
                 f'font-family:var(--e);font-weight:600;font-size:44px;line-height:1;text-transform:uppercase">{link}</div>')
        self.box("linkpill", 342, py, 382, 82)

    def _story_launch(self):
        """The launch announcement as a story. All the launch information (badge, edition, date, time, status, note) with the CTA pill REMOVED:
        a clear zone is declared at the lower third for Instagram's link sticker, with a small cue above it. The bottom 250px stays empty for
        Instagram's reply bar and the top 200px for its profile bar."""
        if self.c.get("date"):
            self._announce_editorial()
        else:
            self._story_no_date()
        W = self.W
        self.raw("cue", "↓&nbsp;&nbsp;LINK IN BIO&nbsp;&nbsp;↓", W // 2, 1478, S(520), S(34),
                 f"font-family:var(--m);font-weight:700;font-size:{S(24)}px;letter-spacing:.3em;color:{self.GL};text-shadow:0 2px 14px rgba(0,0,0,.8)")
        self.box("linkzone", (W - 640) // 2, 1505, 640, 165)        # reserved for the link sticker: nothing else may enter

    def _story_no_date(self):
        """A launch story WITHOUT the date and time (user, 2026-10-13): title and edition lines as usual, then the status becomes the hero line
        and the note sits under it. Nothing is printed where the date block was, so the lines are re-centred on the space it freed."""
        c, di, W = self.c, self.dy_info, self.W
        self.base(); self.top_group(); self._title_for_layout()
        self._edition_lines()
        # raw(label, html, cx, cy, w, h, css): the status is the hero line where the date block used to start
        self.raw("status", c["status"], W // 2, S(1150) + di, S(900), S(70),
                 f"font-family:var(--e);font-weight:600;font-size:{S(58)}px;letter-spacing:.01em")
        if c.get("note"):
            self.raw("note", c["note"], W // 2, S(1240) + di, S(520), S(44),
                     f"font-family:var(--e);font-weight:600;font-size:{S(36)}px")

    def _wa_poster(self):
        """The same launch information as a WhatsApp-forwardable 4:5 poster. There is no link to point at, so no CTA pill."""
        self._announce_editorial()

    def _wa_dp(self):
        """WhatsApp group DP in the approved design family (user, 2026-10-13: "rebuild the DP to match"). 1080x1080 shown as a CIRCLE r=540, so
        the poster's elements are scaled down and centred: copper mask, ball-free title (tuck of the edition lines kept), white NeutralFace with
        the black border, diya plate. The LIVE badge (ALL FOR CHARITY pill, LIVE logo, AQUATERRA logo) is included at top left (user, 2026-10-14), small enough to sit inside the crop; no date unless one is supplied."""
        W, H, P = self.W, self.H, self.parts
        P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self.img("bg_diya_portrait.jpg", 0, -(1350 - W) // 2, W, 1350, z=1, tag="plate")
        DY = 23                                           # base offset; the badge adds a further 24px under the mask (TY) so the stack stays centred
        TY = 24
        bw = 215                                          # the LIVE badge = ALL FOR CHARITY pill + LIVE logo + AQUATERRA logo, as on the posters
        bx, by = 185, 140 + DY
        self.img("live_badge.png", bx, by, bw, z=8, tag="badge"); self.box("badge", bx, by, bw, round(bw * 1005 / 1061))
        k = .2847                                         # copper mask: visible width 400 (the poster's 692 at 0.58x), shifted right of the badge
        mx, my = 430, 140 + DY
        self.img("mask_copper.png", round(mx - 157 * k), round(my - 211 * k), round(1680 * k), z=6, tag="mask",
                 extra="filter:drop-shadow(0 6px 18px rgba(0,0,0,.6));")
        self.box("mask", mx, my, 400, 263)
        t = .466                                          # ball-free title: visible width 800, left 140
        tx, ty = 140, 330 + DY + TY
        self.img("title_lockup_noball.png", round(tx - 265 * t), round(ty - 401 * t), round(2000 * t), z=9, tag="title")
        self.box("title", tx, ty, 800, 425)
        # The edition lines are NOT tucked into the title's notch here (they are on the posters): at DP size a tucked 33px line is unreadable.
        # They sit as a clear centred pair below the lockup: 46px bold MASQUERADE SANGEET, 40px regular EDITION.
        self.raw("sub1", "MASQUERADE SANGEET", 540, 820 + DY + TY, 560, 54, "font-family:var(--e);font-weight:600;font-size:46px;letter-spacing:.01em")
        self.raw("sub2", "Edition", 540, 874 + DY + TY, 190, 46, "font-family:var(--e);font-weight:400;font-size:40px")
        if self.c.get("date"):
            self.raw("date", self.c["date"], 540, 972, 400, 40, "font-family:var(--e);font-weight:600;font-size:32px")   # optional; sized so its box stays inside the circle at this height

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


async def render_poster(kind, content, canvas, out_png, style="plate", mask="asset", typo="editorial", **opts):
    """Validate, build and render one poster through the full gate stack. Returns the output path."""
    p = Poster(kind, content, canvas, style, mask, typo, **opts)
    html = p.build()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    # ("date","time"): foil's numeral line box is taller than its glyphs; the ink clears the time line (checked by eye)
    ignore_all = [("title", "sub1"), ("title", "sub2"), ("title", "count"), ("title", "headline"),
              ("carpet", "headline"), ("carpet", "detail"), ("carpet", "date"), ("carpet", "cta"), ("carpet", "title"),
              ("carpet", "sub1"), ("carpet", "sub2"), ("banner", "sub2"), ("day", "title"), ("arch", "title"), ("arch", "tagline"), ("arch", "badge"),
              ("title", "tagline"), ("title", "edition"), ("title", "railL"), ("title", "railR"), ("badge", "title"), ("badge", "mask"), ("title", "mask"), ("mask", "badge"), ("mask", "sub1"), ("mask", "sub2"), ("mask", "date"), ("mask", "edition"), ("title", "date"), ("title", "edition"), ("date", "edition"), ("title", "month"), ("title", "time"), ("mask", "title"), ("lights", "mask"), ("title", "sub1"), ("title", "sub2"), ("sub2", "status"), ("status", "note"), ("date", "time"), ("title", "date"), ("f1", "f2"), ("f2", "f3"), ("f1", "f3"), ("f1", "badge"), ("banner", "date"), ("banner", "title")]
    labels = {e[0] for e in p.elements}
    ignore = [pr for pr in ignore_all if pr[0] in labels and pr[1] in labels]
    text_pairs = [(lab, OFFWHITE, GROUND, 40, True) for lab in ("date", "status", "headline", "unit")]
    await B.render(html, out_png, p.W, p.H, elements=p.elements, containers=tuple(l for l in ("cta", "carpet", "arch", "linkpill") if l in labels),
                   collision_ignore=ignore, text_pairs=text_pairs,
                   bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain", "carpet", "banner", "photo"),
                   crop_tags=("plate", "sparkles", "grain", "photo", "arch"), page_bg=GROUND)
    return out_png


DEMO_DATE = "2026-11-10"
DEMO = [
    ("announce", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards",
                      status="Ticket sales open soon", note="More details to follow", cta="Link in bio")),
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
