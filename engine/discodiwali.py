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

Kinds: announce | countdown | tickets_open | sold_out | save_the_date.      Canvases: feed (1080x1350) | story (1080x1920).

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
MASKS = ("asset", "red")      # asset: the supplied jewelled mask. red: the drawn red satin mask (mask_red.svg)
STYLES = ("plate", "stroke")   # plate: beaded celestial corners (the reference). stroke: plain ink ground, red-stroked mask
KINDS = ("announce", "countdown", "tickets_open", "sold_out", "save_the_date")
REQUIRED = {
    "announce":     ("edition", "date", "time", "status", "cta"),
    "countdown":    ("edition", "date", "days", "cta"),
    "tickets_open": ("edition", "headline", "cta"),
    "sold_out":     ("edition", "date", "thanks"),
    "save_the_date": ("edition", "day", "month", "year", "time", "cta"),
}
OPTIONAL = {"announce": ("note",), "countdown": ("unit",), "tickets_open": ("detail", "date"), "sold_out": (), "save_the_date": ()}

_cache = {}
def uri(name):
    if name not in _cache:
        mime = "image/png" if name.endswith(".png") else "image/svg+xml" if name.endswith(".svg") else "image/jpeg"
        _cache[name] = f"data:{mime};base64," + base64.b64encode(open(ASSETS + name, "rb").read()).decode()
    return _cache[name]

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
        if self.style == "stroke":
            return                          # no sequin plate: the ground is plain ink, sparkles and grain still lay over it
        if H <= BASE_H:
            self.img("bg_beaded_portrait.jpg", 0, 0, W, H, z=1, tag="plate", extra="object-fit:cover;")
        else:
            # Taller than the plate's 4:5: cropping it to 9:16 loses the corner clusters and leaves a dead black middle.
            # Stack TWO plates instead, the second flipped and faded in from above, so all four corners carry beading.
            self.img("bg_beaded_portrait.jpg", 0, 0, W, BASE_H, z=1, tag="plate")
            self.img("bg_beaded_portrait.jpg", 0, H - BASE_H, W, BASE_H, z=1, tag="plate",
                     extra="transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);"
                           "mask-image:linear-gradient(to top,transparent 0%,#000 45%);")

    def top_group(self):
        MK = .48
        mw = S(2000 * MK)
        if self.mask == "red":
            # drawn mask: body 920 units wide in a 1260x810 artboard; 0.87 ref-px/unit matches the asset mask's 800px body
            u = .87
            self.img("mask_red.svg", S(415 - 40 * u), S(-150) + self.dy_top, S(1260 * u), z=6, tag="mask",
                     extra="transform:rotate(-7deg);transform-origin:40% 55%;filter:drop-shadow(0 8px 24px rgba(0,0,0,.6));")
        elif self.style == "stroke":
            # mask_stroked.png is the mask padded by 90px of red stroke on every side (scratchpad/make_mask_stroke.py)
            pad = round(90 * MK * K)
            self.img("mask_stroked.png", S(415 - 190 * MK) - pad, S(-145) + self.dy_top - pad, round(mw * 2180 / 2000), z=6, tag="mask",
                     extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.6));")
        else:
            self.img("mask.png", S(415 - 190 * MK), S(-145) + self.dy_top, mw, z=6, tag="mask",
                     extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.55));")
        self.img("string_lights.png", S(105), S(-150) + self.dy_top, S(1560), z=7, tag="lights")
        bw = S(293)
        self.img("live_badge.png", S(45), S(48) + self.dy_top, bw, z=8, tag="badge")
        self.box("badge", S(45), S(48) + self.dy_top, bw, round(bw * 1005 / 1061))

    def title(self, scale=1.0, cx_shift=0):
        TK = .676 * scale
        tw = S(2000 * TK)
        tx = S(30 - 265 * TK) + cx_shift
        ty = S(390 - 320 * TK) + self.dy_title
        self.img("title_lockup.png", tx, ty, tw, z=9, tag="title")
        self.box("title", S(30) + cx_shift, S(390) + self.dy_title, S(1160 * scale), S(670 * scale))

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
              ("carpet", "sub1"), ("carpet", "sub2"), ("banner", "sub2"), ("day", "title"), ("banner", "date"), ("banner", "title")]
    labels = {e[0] for e in p.elements}
    ignore = [pr for pr in ignore_all if pr[0] in labels and pr[1] in labels]
    text_pairs = [(lab, OFFWHITE, GROUND, 40, True) for lab in ("date", "status", "headline", "unit")]
    await B.render(html, out_png, p.W, p.H, elements=p.elements, containers=tuple(l for l in ("cta", "carpet") if l in labels),
                   collision_ignore=ignore, text_pairs=text_pairs,
                   bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain", "carpet", "banner"),
                   crop_tags=("plate", "sparkles", "grain"), page_bg=GROUND)
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

async def _demo():
    out = os.path.join(ROOT, "out", "discodiwali")
    async with B.session():
        for canvas in ("feed", "story"):
            for kind, content in DEMO:
                await render_poster(kind, content, canvas, os.path.join(out, f"{kind}_{canvas}.png"))
        for kind, content in DEMO:
            await render_poster(kind, content, "feed", os.path.join(out, f"{kind}_feed_stroke.png"), style="stroke")
        for kind, content in DEMO[:1] + DEMO[4:]:
            await render_poster(kind, content, "feed", os.path.join(out, f"{kind}_feed_red.png"), style="stroke", mask="red")
    print("demo set done ->", out)

if __name__ == "__main__":
    asyncio.run(_demo())
