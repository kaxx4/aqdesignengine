"""SHIKSHAQ - the Shikshaq design language as an engine FORMAT MODULE.

WHAT THIS IS. Shikshaq (shikshaq.in, a Kolkata tuition-teacher directory plus a past-paper
library) is a SECOND BRAND on the AQ rails. It is not AQ: the ground is warm bone, the voice is
a heavy display grotesk in mixed weights, depth is a hairline ring (never AQ's thick outline and
hard offset shadow), and colour is two MODES (teachers = orange, papers = indigo) plus a tinted
palette per subject. So when someone says "design something for Shikshaq", NONE of AQ's palette,
fonts, doodles or craft layer applies. This module is the one entry point that carries the
Shikshaq language, so it is applied the same way every time and a flaw is fixed once, here.

Read brain/SHIKSHAQ.md first. It is the operator doc (what the language IS, which surface gets
which treatment, the page recipes, the gate list). This file is the code behind it.

THE ENCODED RULES  (each one is a flaw caught by eye, now a check or a default)
-------------------------------------------------------------------------------------------
S1  GROUND IS WARM BONE, NEVER WHITE OR GREY.  page #F9F5F1, card #FCFAF7, muted #F0EAE2.
    White appears only as type on a saturated fill and as a sticker keyline.
S2  TOKENS ARE VERIFIED, NOT TRUSTED.  verify_tokens() recomputes every hex from the vendored
    snapshot of the site's own index.css / subject-palette.ts, so a drifted value is a failing
    assertion instead of a quietly off-brand poster. (The Node addon's copy had drifted: it
    still carried the pre-2026-11-06 text ramp and an orange-deep that the site had changed.)
S3  TWO MODES, ONE SWITCH.  teachers = orange #FF8000, papers = indigo #4351FF.  MODES carries
    action / hover / tint / deep / text-on-fill.  Text on ORANGE is INK (6.5:1), white is 2.5:1.
S4  CATEGORY COLOUR IS DATA.  subject_palette() is the site's own generator (aliases, keyword
    scan, the contrast-picked badge text).  Never hand-pick a subject colour.
S5  FILL IS THE SEPARATOR.  Panels are 30px-rounded, gap 0, and differ by fill.  Edges are
    RING + a crisp 1px drop, never a wide blur.  No thick outline in a grid of comparable items.
S6  CONTRAST IS MEASURED PER ELEMENT against the surface actually painted behind it (gate).
S7  EVERY NUMBER TRACES TO A FACT.  FACTS carries what was read off the live data, dated.  A
    digit that is not a fact is a hard failure in copy_gate(), and facts older than 14 days warn.
S8  NO DASHES in copy (em or en).  The site's rule; copy_gate() enforces it.
S9  NO HORIZONTAL OVERFLOW.  A page that is 425px wide in a 390px viewport (a scroller inside a
    grid cell forcing the column open) shipped in the first demo build; the gate now measures it
    and names the culprits.  Fix: min-width:0 on the grid item.
S10 AT MOST ONE SATURATED-ON-SATURATED SEAM per page, never the same hue twice.  (The live home
    places indigo directly above orange once.  The design docs say "never adjacent"; the site
    does it once on purpose, so that is what is encoded.)

HOW TO USE
    import shikshaq as sk                       # engine/ is on sys.path in every bespoke script
    html = sk.doc(body, kind="poster", W=1080, H=1350)
    res  = sk.render_sync(html, "out/x.png", 1080, 1350, kind="poster")   # gate runs on the DOM
    python engine/shikshaq.py scaffold poster my_poster      # a starter that already passes
    python engine/shikshaq.py selftest | css | facts | gate <file.html>
"""
import asyncio, base64, colorsys, io, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "engine", "assets", "shikshaq")
SOURCE = os.path.join(ASSETS, "source")


class ShikshaqError(Exception):
    """A brief or copy that breaks a rule the language treats as hard."""


# ═════════════════════════════════════════════════════════════════════════════
# 1. COLOUR MATH
# ═════════════════════════════════════════════════════════════════════════════
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def hsl_to_hex(h, s, l):
    """CSS Color 4 conversion, the same one src/lib/subject-palette.ts uses."""
    s, l = s / 100.0, l / 100.0
    a = s * min(l, 1 - l)

    def f(n):
        k = (n + h / 30.0) % 12
        return l - a * max(-1, min(k - 3, min(9 - k, 1)))

    return rgb_to_hex((255 * f(0), 255 * f(8), 255 * f(4)))


def hex_to_hsl(hx):
    r, g, b = [c / 255.0 for c in hex_to_rgb(hx)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def lum(hx):
    def ch(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(hx)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ═════════════════════════════════════════════════════════════════════════════
# 2. TOKENS  (values mirror src/index.css; verify_tokens() proves it)
# ═════════════════════════════════════════════════════════════════════════════
C = {
    # ground: all warm, never white or grey
    "page": "#F9F5F1", "card": "#FCFAF7", "muted": "#F0EAE2", "band": "#F2ECE4",
    "hairline": "#E7DFD5", "hairline_raised": "#E4DCD2", "hairline_strong": "#D8CFC4",
    # text ramp (darkened 2026-11-06 at the owner's request)
    "ink": "#1F1F1F", "prose": "#4A443E", "text2": "#6F675F", "text3": "#776F67", "text4": "#8A8279",
    "panel": "#1B1A18",                       # near-black: footer, nav pill, dark CTA, teacher header
    # mode: teachers
    "orange": "#FF8000", "orange_hover": hsl_to_hex(30, 100, 44),
    "orange_tint": "#FFF4E8", "orange_deep": hsl_to_hex(30, 100, 32),
    # mode: papers
    "indigo": "#4351FF", "indigo_hover": hsl_to_hex(235, 85, 56),
    "indigo_tint": "#EDEEFF", "indigo_deep": hsl_to_hex(235.7, 67.2, 51),
    # fixed accents
    "mint": "#E3F7EC", "mint_solid": "#34B268", "peach": "#FCECDE",
    "whatsapp": "#25D366", "whatsapp_text": "#0B3D1F",
    "destructive": hsl_to_hex(0, 72, 42), "white": "#FFFFFF",
}

MODES = {
    "teachers": {"action": C["orange"], "hover": C["orange_hover"], "tint": C["orange_tint"],
                 "deep": C["orange_deep"], "on": C["ink"], "name": "teachers"},
    "papers":   {"action": C["indigo"], "hover": C["indigo_hover"], "tint": C["indigo_tint"],
                 "deep": C["indigo_deep"], "on": C["white"], "name": "papers"},
}
# Which accent a piece of content takes. Semantic, like AQ's accent_for(dept): never a rotation index.
PILLAR_MODE = {"teachers": "teachers", "papers": "papers", "tips": "mint", "trust": "mint"}

RADII = {"slab": 30, "photo": 24, "card": 20, "tile": 13, "ctl": 12, "pill": 9999}
SIZES = {"feed": (1080, 1350), "story": (1080, 1920), "square": (1080, 1080),
         "mobile": (390, 844), "tablet": (768, 1024), "desktop": (1280, 800)}

# ---- the eight-subject generator (src/lib/subject-palette.ts, ported 1:1) ----------------
SUBJECT_SEEDS = {
    "maths": (28, 85, 65), "science": (145, 55, 45), "english": (180, 45, 50),
    "commerce": (220, 60, 55), "computer": (280, 50, 55), "hindi": (0, 65, 55),
    "history": (35, 55, 50), "geography": (160, 50, 45),
}
_TINT_L, _TEXT_S, _TEXT_L, _META_S, _META_L = 93, 45, 26, 28, 34
FALLBACK_PALETTE = {"tint": C["muted"], "solid": "#7B736B", "text": C["ink"], "meta": "#7B736B",
                    "badge": C["white"]}

_ALIASES = {
    "maths": "maths", "math": "maths", "mathematics": "maths",
    "science": "science", "sci": "science", "physics": "science", "phy": "science",
    "chemistry": "science", "chem": "science", "biology": "science", "bio": "science",
    "environmental science": "science", "evs": "science", "home science": "science",
    "english": "english", "eng": "english",
    "commerce": "commerce", "commercial studies": "commerce", "economics": "commerce",
    "econ": "commerce", "eco": "commerce", "accounts": "commerce", "accountancy": "commerce",
    "accounting": "commerce", "acc": "commerce", "business studies": "commerce", "bst": "commerce",
    "computer": "computer", "computers": "computer", "cs": "computer", "it": "computer",
    "hindi": "hindi",
    "history": "history", "hist": "history", "civics": "history", "history and civics": "history",
    "social studies": "history", "sst": "history",
    "geography": "geography", "geo": "geography",
}
_KEYWORDS = [("computer", "computer"), ("comput", "computer"), ("coding", "computer"),
             ("geograph", "geography"), ("histor", "history"), ("civics", "history"),
             ("social studies", "history"), ("hindi", "hindi"), ("math", "maths"),
             ("english", "english"), ("commerc", "commerce"), ("econom", "commerce"),
             ("account", "commerce"), ("business", "commerce"), ("physics", "science"),
             ("chemist", "science"), ("biolog", "science"), ("scien", "science")]


def _norm(s):
    s = s.strip().lower().replace("&", " and ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def subject_family(subject):
    """Raw subject string -> palette family or None. Comma combos resolve on the first member."""
    if not subject:
        return None
    key = _norm(str(subject).split(",")[0])
    if not key:
        return None
    if key in _ALIASES:
        return _ALIASES[key]
    for needle, fam in _KEYWORDS:
        if needle in key:
            return fam
    return None


def palette_from_seed(seed):
    h, s, l = seed
    solid = hsl_to_hex(h, s, l)
    wc, dc = contrast(solid, C["white"]), contrast(solid, C["ink"])
    # The site picks badge text by MEASURING: white if it clears 4.5, else whichever is higher.
    badge = C["white"] if wc >= 4.5 else (C["ink"] if dc > wc else C["white"])
    return {"tint": hsl_to_hex(h, s, _TINT_L), "solid": solid, "text": hsl_to_hex(h, _TEXT_S, _TEXT_L),
            "meta": hsl_to_hex(h, _META_S, _META_L), "badge": badge}


def subject_palette(subject):
    fam = subject_family(subject)
    return palette_from_seed(SUBJECT_SEEDS[fam]) if fam else dict(FALLBACK_PALETTE)


def palette_from_key(key):
    """Decorative, stable colour for a thing with no subject (a paper cover, a school tile).
    The same hash the site uses, so a cover keeps its colour across the site and the poster."""
    k = (key or "").strip()
    if not k:
        return dict(FALLBACK_PALETTE)
    h = 0
    for ch in k:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    names = list(SUBJECT_SEEDS)
    return palette_from_seed(SUBJECT_SEEDS[names[h % len(names)]])


def text_on(fill):
    """Ink or white, whichever MEASURES higher on this fill."""
    return C["ink"] if contrast(fill, C["ink"]) >= contrast(fill, C["white"]) else C["white"]


# ═════════════════════════════════════════════════════════════════════════════
# 3. TOKEN VERIFICATION against the vendored snapshot of the site's own source
# ═════════════════════════════════════════════════════════════════════════════
def _css_vars():
    p = os.path.join(SOURCE, "index.css")
    txt = io.open(p, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"--([a-z0-9-]+):\s*([^;]+);", txt):
        out.setdefault(m.group(1), m.group(2).strip())
    return out


def _as_hex(v):
    v = v.strip()
    if v.startswith("#") and len(v) == 7:
        return v.upper()
    m = re.match(r"^([\d.]+)\s+([\d.]+)%\s+([\d.]+)%$", v)
    if m:
        return hsl_to_hex(*[float(x) for x in m.groups()])
    return None


def _near(a, b, tol=1):
    return all(abs(x - y) <= tol for x, y in zip(hex_to_rgb(a), hex_to_rgb(b)))


def verify_tokens():
    """Recompute every token from the vendored source. Returns a list of mismatches (empty = pass).
    If the site changes a colour, refresh engine/assets/shikshaq/source/ and this names the drift."""
    v = _css_vars()
    pairs = {
        "page": "background", "card": "card", "muted": "muted", "hairline": "border",
        "ink": "foreground", "text2": "text-secondary", "text3": "text-tertiary", "text4": "text-quaternary",
        "prose": "text-prose", "panel": "panel-dark", "orange": "brand", "orange_hover": "brand-hover",
        "orange_tint": "brand-subtle", "orange_deep": "brand-deep", "indigo": "brand-blue",
        "indigo_hover": "brand-blue-hover", "indigo_tint": "brand-blue-subtle",
        "indigo_deep": "brand-blue-deep", "mint": "mint", "mint_solid": "mint-solid",
        "peach": "peach-tint", "whatsapp": "whatsapp", "whatsapp_text": "whatsapp-text",
        "destructive": "destructive", "band": "warm-band", "hairline_raised": "warm-hairline-raised",
        "hairline_strong": "warm-hairline-strong",
    }
    bad = []
    for ours, theirs in pairs.items():
        if theirs not in v:
            bad.append(f"{ours}: source has no --{theirs}")
            continue
        src = _as_hex(v[theirs])
        if src is None:
            bad.append(f"{ours}: cannot read --{theirs} = {v[theirs]!r}")
        elif not _near(C[ours], src):
            bad.append(f"{ours}: engine {C[ours]} but the site's --{theirs} is {src}")
    # subject seeds, read from the TypeScript source
    ts = io.open(os.path.join(SOURCE, "subject-palette.ts"), encoding="utf-8").read()
    for fam, (h, s, l) in SUBJECT_SEEDS.items():
        m = re.search(fam + r":\s*\{\s*h:\s*([\d.]+),\s*s:\s*([\d.]+),\s*l:\s*([\d.]+)", ts)
        if not m:
            bad.append(f"seed {fam}: not found in subject-palette.ts")
        elif tuple(float(x) for x in m.groups()) != (h, s, l):
            bad.append(f"seed {fam}: engine {(h, s, l)} but the site has {tuple(float(x) for x in m.groups())}")
    for name, val in (("TINT_L", _TINT_L), ("TEXT_S", _TEXT_S), ("TEXT_L", _TEXT_L), ("META_S", _META_S), ("META_L", _META_L)):
        m = re.search(r"const " + name + r"\s*=\s*([\d.]+)", ts)
        if not m or float(m.group(1)) != val:
            bad.append(f"{name}: engine {val} but the site has {m.group(1) if m else 'nothing'}")
    return bad


# ═════════════════════════════════════════════════════════════════════════════
# 4. FACTS + COPY GATE  (the truth ladder: a number that is not a fact is not used)
# ═════════════════════════════════════════════════════════════════════════════
FACTS = {
    "asOf": "2026-11-27",
    "source": "shikshaqkanitest production deployment (same Supabase project as shikshaq.in), "
              "read in a real browser. Re-read before publishing: counts move weekly.",
    "teachers": 157, "papers": None, "commission": 0, "free_questions": 2,
    # OWNER RULING 2026-11-27: the paper count is ASKED EACH TIME. The site disagrees with itself, so no figure is
    # hardcoded. need("papers") raises until confirm("papers", N) (or env SHIKSHAQ_PAPERS) records the owner's answer.
    "papers_candidates": {"655": "home hero, About, Auth", "661": "Browse cross-sell card"},
    "subject_teachers": {"Maths": 61, "English": 43, "Hindi": 34, "Chemistry": 32, "Biology": 30,
                         "Accounts": 26, "Computers": 11, "Psychology": 6},
    "board_teachers": {"ICSE": 155, "CBSE": 149, "IGCSE": 55, "IB": 38, "State": 75},
    "paper_subjects": {"Maths": 616, "History & Civics": 21, "English": 18, "History": 4,
                       "Economics": 1, "Applied Mathematics": 1},
    "city": "Kolkata", "site": "shikshaq.in", "classes": "IV to XII", "boards_papers": ["ICSE", "CBSE", "ISC"],
    "sample_papers": [
        {"board": "ICSE", "year": 2026, "subject": "Maths", "cls": "X", "questions": 41, "marks": 106},
        {"board": "ISC", "year": 2026, "subject": "Maths", "cls": "XI", "questions": 48},
        {"board": "ISC", "year": 2026, "subject": "Maths", "cls": "XII", "questions": 54},
    ],
    # Disagreements found between surfaces. A figure on this list needs one source chosen before use.
    "known_inconsistencies": [
        "papers: 655 on the home hero, About and Auth; 661 on the Browse cross-sell card (2026-11-27). Owner ruled: ASK EACH TIME.",
        "papers: the admin database holds far more rows than the 655 the public site counts as live.",
    ],
}

PAPERS_ASK = ("the paper count is ASKED EACH TIME (owner ruling, 2026-11-27): the site shows 655 on the home hero, About and "
              "Auth and 661 on the Browse card. Ask the owner which to use, or read the live site, then "
              "sk.confirm('papers', N) (or set SHIKSHAQ_PAPERS=N). Do not guess.")


def need(key):
    """A fact that must be CONFIRMED before use. Raises (naming the question to ask) instead of returning a stale figure."""
    v = FACTS.get(key)
    if v is None:
        raise ShikshaqError(PAPERS_ASK if key == "papers" else f"fact {key!r} is not confirmed: ask the owner or read the live site")
    return v


def confirm(key, value, source="owner, this session"):
    """Record an answer for a fact that is asked each time. It lasts for this process only."""
    FACTS[key] = value
    FACTS.setdefault("confirmed", {})[key] = source
    return value


if os.environ.get("SHIKSHAQ_PAPERS"):
    confirm("papers", int(os.environ["SHIKSHAQ_PAPERS"]), "env SHIKSHAQ_PAPERS")


_BANNED = [
    (re.compile(r"[\u2014\u2013]"), "em or en dash (site rule: none in copy)"),
    (re.compile(r"\b(guarantee[ds]?|cheapest|best (teacher|tutor)s?|top[- ]rated|number one)\b|#1|(?<![\w.])100\s*%", re.I),
     "unprovable superlative"),
    (re.compile(r"\b(thousands|lakhs?|millions?|trusted by|loved by|most popular|everyone)\b", re.I),
     "unsourced social proof"),
    (re.compile(r"\b(ai[- ]powered|revolutionary|game[- ]chang\w+|unlock|supercharge)\b", re.I), "brand-voice cliche"),
    (re.compile(r"\btoppers?\b", re.I), "unsourced claim about toppers"),
]


def _fact_numbers(facts):
    ok = set()

    def add(v):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            ok.add(str(int(v)) if float(v).is_integer() else str(v)); ok.add(f"{int(v):,}")
        elif isinstance(v, dict):
            for x in v.values(): add(x)
        elif isinstance(v, list):
            for x in v: add(x)
    for k in ("teachers", "papers", "commission", "free_questions", "subject_teachers",
              "board_teachers", "paper_subjects"):
        add(facts.get(k))
    for p in facts.get("sample_papers", []):
        for k in ("year", "questions", "marks"):
            add(p.get(k))
    return ok


def copy_gate(strings, facts=None, extra_ok=(), today=None):
    """Hard-fail copy rules. Returns (errors, warnings). strings: an iterable of visible strings.
    A digit must trace to a fact, a class numeral in context ("Class 10"), or `extra_ok`."""
    facts = facts or FACTS
    errors, warns = [], []
    ok = _fact_numbers(facts) | {str(x) for x in extra_ok}
    for s in strings:
        if not s:
            continue
        for rx, why in _BANNED:
            if rx.search(s):
                errors.append(f"{why}: {s[:70]!r}")
        for m in re.finditer(r"[\u20B9]?\d[\d,]*", s):
            raw = m.group(0).lstrip("\u20B9")
            ctx = re.search(r"Class(es)? (%s)\b|\b%s (Class|step)|IV to XII|\b(19|20)\d\d\b" % (re.escape(raw), re.escape(raw)), s)
            if raw not in ok and raw.replace(",", "") not in ok and not ctx:
                if raw in facts.get("papers_candidates", {}) and facts.get("papers") is None:
                    errors.append(f"number {raw!r} is an UNCONFIRMED paper count: " + PAPERS_ASK)
                else:
                    errors.append(f"number {raw!r} does not trace to a fact: {s[:70]!r}")
    try:
        age = ((today or datetime.date.today()) - datetime.date.fromisoformat(facts["asOf"])).days
        if age > 14:
            warns.append(f"FACTS are {age} days old (asOf {facts['asOf']}): re-read the live counts before publishing")
    except Exception:
        pass
    return errors, warns


# ═════════════════════════════════════════════════════════════════════════════
# 5. CSS  (tokens + the component stylesheet)
# ═════════════════════════════════════════════════════════════════════════════
def _b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def font_css():
    """Archivo (wght 100-900, wdth 62-125) and Geist (wght 100-900), embedded so a render never
    depends on the network or on a Google Fonts outage."""
    d = os.path.join(ASSETS, "fonts")
    return (
        "@font-face{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:62% 125%;"
        f"src:url(data:font/woff2;base64,{_b64(os.path.join(d, 'archivo-latin.woff2'))}) format('woff2')}}\n"
        "@font-face{font-family:'Geist';font-style:normal;font-weight:100 900;"
        f"src:url(data:font/woff2;base64,{_b64(os.path.join(d, 'geist-latin.woff2'))}) format('woff2')}}\n"
    )


def tokens_css():
    L = [":root{"]
    for k, v in C.items():
        L.append(f"  --{k.replace('_', '-')}:{v};")
    L += [
        "  --ink-rgb:31 31 31;",
        "  --ring:0 1px 2px 0 rgb(var(--ink-rgb)/.12),0 0 0 1px rgb(var(--ink-rgb)/.08);",
        "  --ring-card:0 0 0 1px rgb(var(--ink-rgb)/.07),0 1px 2px 0 rgb(var(--ink-rgb)/.12),0 3px 4px -2px rgb(var(--ink-rgb)/.08);",
        "  --ring-lift:0 0 0 1px rgb(var(--ink-rgb)/.09),0 1px 2px 0 rgb(var(--ink-rgb)/.14),0 6px 8px -4px rgb(var(--ink-rgb)/.14);",
        "  --press:.97;--press-small:.94;--press-card:.99;",
        "  --ease-out-strong:cubic-bezier(.23,1,.32,1);--ease-settle:cubic-bezier(.16,1,.3,1);",
        "  --r-slab:30px;--r-photo:24px;--r-card:20px;--r-tile:13px;--r-ctl:12px;--r-pill:9999px;",
    ]
    for fam, seed in SUBJECT_SEEDS.items():
        p = palette_from_seed(seed)
        for role in ("tint", "solid", "text", "meta", "badge"):
            L.append(f"  --cat-{fam}-{role}:{p[role]};")
    L.append("}")
    return "\n".join(L)


STYLESHEET = r"""
*{box-sizing:border-box;margin:0}
html{background:var(--page)}
body{font-family:'Geist',system-ui,sans-serif;font-weight:500;color:var(--ink);-webkit-font-smoothing:antialiased;line-height:1.5}
h1,h2,h3{font-family:'Archivo',system-ui,sans-serif;letter-spacing:-.045em;text-wrap:balance;line-height:.98}
p{text-wrap:pretty}
.wrap{max-width:1152px;margin:0 auto;padding:0 22px}
@media(min-width:900px){.wrap{padding:0 32px}}
.stack{display:flex;flex-direction:column;gap:0;position:relative}
.panel{border-radius:30px;padding:22px 0}
@media(min-width:900px){.panel{padding:32px 0}}
.bone{background:var(--card)}.peach{background:var(--orange-tint)}.lav{background:var(--indigo-tint)}
.mintbg{background:var(--mint)}.org{background:var(--orange)}.ind{background:var(--indigo);color:#fff}.dark{background:var(--panel);color:var(--page)}
.pill{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 20px;border-radius:999px;font-weight:700;font-size:14px;white-space:nowrap;font-style:normal;transition:transform .15s var(--ease-out-strong)}
.pill:active{transform:scale(var(--press))}
.pill.cream{background:#EFE9E1;color:var(--prose);box-shadow:var(--ring)}
.pill.go{background:var(--orange);color:var(--ink);box-shadow:0 1px 2px 0 rgba(163,82,0,.38),0 0 0 1px rgba(163,82,0,.26)}
.pill.indigo{background:var(--indigo);color:#fff;box-shadow:0 1px 2px 0 rgba(46,58,214,.38),0 0 0 1px rgba(46,58,214,.26)}
.pill.darkb{background:var(--panel);color:var(--page);box-shadow:0 1px 2px 0 rgba(0,0,0,.38)}
.pill.white{background:#fff;color:var(--indigo-deep);box-shadow:0 1px 2px rgba(0,0,0,.2)}
.pill.wa{background:var(--whatsapp);color:var(--whatsapp-text);box-shadow:0 1px 2px 0 rgba(15,90,40,.38),0 0 0 1px rgba(15,90,40,.26)}
.pill.ghost{background:rgba(255,255,255,.2);color:inherit;box-shadow:var(--ring)}
.chip{flex:none;height:44px;padding:0 18px;display:inline-flex;align-items:center;border-radius:999px;background:var(--muted);box-shadow:var(--ring);font-weight:600;font-size:15px}
.chip.on{background:var(--orange-tint);color:var(--orange-deep)}.chip.on.papers{background:var(--indigo-tint);color:var(--indigo-deep)}
.count{flex:none;display:flex;align-items:center;gap:8px;height:38px;padding:0 14px;border-radius:999px;background:var(--muted);font-size:13px;font-weight:600;box-shadow:var(--ring)}
.count s{width:8px;height:8px;border-radius:2px;text-decoration:none}
.eyebrow{font-size:13px;font-weight:600;color:var(--orange-deep)}
.eyelab{font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--text3)}
.org .eyelab{color:var(--ink)}.ind .eyelab{color:#fff}
.h1{font-weight:400;font-size:clamp(36px,5.6vw,66px);margin-top:8px;letter-spacing:-.05em}
.h1 b{font-weight:800;color:var(--orange)}.h1 b.papers{color:var(--indigo)}
.mark{background:var(--orange);padding:.04em .22em;margin:0 -.06em;border-radius:4px;display:inline-block;transform:rotate(-1.5deg);-webkit-box-decoration-break:clone;box-decoration-break:clone}
.mark.dark{background:var(--panel);color:#fff}
.sticker{position:absolute;height:26px;padding:0 12px;border-radius:999px;background:var(--panel);color:var(--page);font-weight:800;font-size:11px;display:flex;align-items:center;box-shadow:var(--ring)}
.sticker.brand{background:var(--orange);color:var(--ink)}.sticker.papers{background:var(--indigo);color:#fff}
.tile{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;flex:none}
.tile.o{background:var(--orange);color:var(--ink)}.tile.i{background:var(--indigo);color:#fff}
.nh{position:relative;font-size:clamp(27px,3.8vw,46px);font-weight:800;letter-spacing:-.045em;line-height:1}
.nh span{display:block}.nh span+span{padding-left:34px}
.nh i{position:absolute;left:0;bottom:.5em;font-style:normal;font-family:'Geist';font-size:12px;font-weight:700;letter-spacing:.07em;color:var(--text3)}
.sup{margin-top:12px;font-size:14px;color:var(--text2);max-width:52ch}
.mosaic{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:22px}
@media(min-width:900px){.mosaic{grid-template-columns:repeat(4,1fr);gap:12px}}
.cat{border-radius:20px;padding:20px}
.cat .tile{width:42px;height:42px;border-radius:13px;margin-bottom:26px}
.cat h3{font-size:23px;font-weight:700;letter-spacing:-.04em;line-height:1.1}
.cat p{font-size:13px;font-weight:500;margin-top:5px}
.boards{display:grid;gap:8px;margin-top:22px}
@media(min-width:900px){.boards{grid-template-columns:repeat(5,1fr)}}
.brow{height:50px;border-radius:999px;padding:0 20px;display:flex;align-items:center;justify-content:space-between;font-weight:700;font-size:15px}
.brow small{font-weight:500;font-size:13px;opacity:.8}
.slabgrid{display:grid;gap:22px;grid-template-columns:minmax(0,1fr)}
.slabgrid>*{min-width:0}
@media(min-width:900px){.slabgrid{grid-template-columns:minmax(0,1fr) minmax(0,1.7fr);gap:40px;align-items:center}}
.slab h2{font-size:clamp(26px,3vw,38px);font-weight:800;letter-spacing:-.045em}
.slab p{margin-top:12px;line-height:1.55;font-size:15px}
.covers{display:flex;gap:12px;overflow:auto;padding:14px;border:1.5px dashed rgba(255,255,255,.4);border-radius:22px;scrollbar-width:none}
.cover{flex:none;width:158px;height:206px;border-radius:14px;display:flex;overflow:hidden;box-shadow:0 10px 24px -8px rgba(0,0,0,.35)}
.cover u{width:12px;flex:none}
.cover div{padding:14px 12px;display:flex;flex-direction:column;gap:3px;flex:1;font-size:12px;line-height:1.25;color:var(--ink)}
.cover .t{font-family:'Archivo';font-weight:800;font-size:19px;letter-spacing:-.04em;line-height:1.05}
.cover .m{font-weight:700;letter-spacing:.04em;font-size:11px;text-transform:uppercase}
.cover .f{margin-top:auto;font-weight:600}
.steps{display:grid;gap:22px;margin-top:24px}
@media(min-width:900px){.steps{grid-template-columns:repeat(3,1fr);gap:32px}}
.step .tile{background:rgba(31,31,31,.12);color:var(--ink);width:40px;height:40px}
.step h3{font-size:19px;font-weight:700;letter-spacing:-.03em;margin-top:14px}
.step p{font-size:15px;margin-top:6px;color:#2a1700}
.stats{display:grid;gap:10px;margin-top:22px}
@media(min-width:900px){.stats{grid-template-columns:repeat(3,1fr);gap:12px}}
.stat{border-radius:20px;padding:20px 22px}
.stat b{display:block;font-family:'Archivo';font-weight:800;font-size:46px;letter-spacing:-.05em;line-height:1;font-variant-numeric:tabular-nums}
.stat span{display:block;font-size:13.5px;margin-top:8px;color:var(--text2)}
.top{display:grid;grid-template-columns:minmax(0,1fr)}.top>*{min-width:0}
.hw{padding:0 22px}.hero{padding-top:88px}
@media(min-width:900px){.hero{padding-top:104px}.top{grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)}.hw{padding:0 28px 0 max(32px,calc((100vw - 1152px)/2 + 32px))}}
.counts{display:flex;gap:8px;overflow:auto;margin:20px -22px 0;padding:0 22px;scrollbar-width:none}
.desk{margin-top:26px}
.toggle{display:inline-flex;padding:5px;border-radius:999px;background:var(--muted);gap:2px}
.toggle span{height:40px;padding:0 20px;display:grid;place-items:center;border-radius:999px;font-size:14px;font-weight:600;color:var(--text2)}
.toggle .on{background:var(--panel);color:var(--page);box-shadow:0 1px 2px rgba(0,0,0,.3)}
.search{display:flex;align-items:center;gap:12px;height:64px;margin-top:14px;padding:0 8px 0 18px;border-radius:24px;background:var(--muted);color:var(--text2);font-size:16px}
.search .ph{flex:1;min-width:0}.search .pill{height:48px}
.chips{display:flex;gap:8px;margin-top:14px;overflow:auto;scrollbar-width:none;margin-right:-22px;padding-right:22px}
.avatar{display:inline-grid;place-items:center;width:.64em;height:.64em;border-radius:50%;background:repeating-linear-gradient(45deg,#F2ECE4 0 5px,#F9F5F1 5px 10px);vertical-align:.03em;margin-right:.14em;box-shadow:var(--ring);font-family:'Archivo';font-weight:800;color:rgba(31,31,31,.3);line-height:1}
.avatar i{font-style:normal;font-size:.34em;letter-spacing:0}
.forks{display:flex;flex-direction:column}@media(min-width:900px){.forks{flex-direction:row}.forks .fork{flex:1}}
.fork{position:relative;padding:22px;overflow:hidden;min-height:176px;display:flex;flex-direction:column;justify-content:space-between;border-radius:30px}
@media(min-width:900px){.fork{padding:100px 28px 28px;min-height:0}}   /* the nav pill overlays the top 72px of the first panels: reserve it INSIDE the panel (the live site's NavReserve) */
.fork .sticker{top:14px;right:16px}@media(min-width:900px){.fork .sticker{top:86px}}
.fork .lab{font-size:13px;color:var(--text2);margin-top:22px}
.fork .big{font-family:'Archivo';font-size:25px;font-weight:800;letter-spacing:-.045em;line-height:1.05;margin-top:2px;max-width:58%}
@media(min-width:900px){.fork .big{max-width:none}}
.fork.peach .big b{color:var(--orange-deep)}.fork.lav .big b{color:var(--indigo-deep)}.fork .big span{font-weight:400}
.mascot{position:absolute;right:-14px;bottom:-26px;width:132px;height:132px}
@media(min-width:900px){.mascot{width:170px;height:170px;right:18px;bottom:auto;top:58%;transform:translateY(-50%)}.fork.lav .mascot{top:auto;bottom:-30px;transform:none;width:120px;height:120px;right:16px}}
.nav{position:absolute;top:12px;left:12px;right:12px;height:56px;border-radius:999px;background:var(--card);box-shadow:0 8px 28px -6px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:space-between;padding:0 12px 0 20px;z-index:5}
.nav img{height:28px}.nav .links,.nav .cta{display:none}
.burger{width:40px;height:40px;border-radius:50%;background:var(--muted);box-shadow:var(--ring);display:grid;place-items:center}
.burger i{display:block;width:16px;height:2px;background:var(--ink);box-shadow:0 5px 0 var(--ink),0 -5px 0 var(--ink)}
@media(min-width:900px){.nav{height:60px;background:var(--panel);color:var(--page);padding:0 12px 0 28px}.nav img{filter:brightness(0) invert(1);height:30px}
 .nav .links{display:flex;gap:28px;margin-left:36px;flex:1;font-size:15px;color:rgba(249,245,241,.7)}.nav .links b{color:var(--page);font-weight:600}
 .nav .cta{display:flex;gap:8px}.burger{display:none}}
.eyes{background:var(--orange);border-radius:30px;padding:0 0 28px;overflow:hidden;position:relative}
.dome{height:96px;background:var(--card);border-radius:0 0 50% 50%/0 0 100% 100%;margin-bottom:-6px}
.eye-row{display:flex;justify-content:center;gap:22px;margin-top:-46px;position:relative}
.eye{width:98px;height:84px;border-radius:50%;background:var(--card);box-shadow:inset 0 3px 6px rgba(31,31,31,.13);position:relative;overflow:hidden}
.pupil{position:absolute;left:50%;top:50%;width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;background:var(--ink)}
.pupil:after{content:'';position:absolute;left:9px;top:8px;width:10px;height:10px;border-radius:50%;background:#fff}
.sentence{margin:22px auto 0;text-align:center;padding:0 22px;font-family:'Archivo';font-weight:800;font-size:clamp(25px,3.2vw,36px);letter-spacing:-.04em;line-height:1.55;max-width:760px}
.slot{display:inline-block;padding:0 14px;margin:0 2px;border-radius:14px;background:rgba(255,255,255,.18);box-shadow:0 0 0 1px rgba(255,255,255,.25),0 6px 14px -6px rgba(0,0,0,.35);transform:rotate(-1.5deg)}
.slot:nth-of-type(2){transform:rotate(1.5deg)}
.eyes .pill{margin:22px auto 0;display:flex;width:max-content}
.heads{text-align:center;padding:36px 22px 30px;background:var(--page)}
.foot{border-radius:30px 30px 0 0;padding:44px 0 0;overflow:hidden}
.foot p.l{font-family:'Archivo';font-weight:900;font-size:clamp(21px,3.2vw,32px);letter-spacing:-.03em;line-height:1.6;max-width:36ch;color:#fff}
.foot em{font-style:normal;background:rgba(255,255,255,.14);padding:.04em .3em;margin-right:-.12em;border-radius:8px;box-shadow:0 0 0 1px rgba(255,255,255,.1)}
.foot .row{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}.foot .row .pill{background:#2a2926;color:var(--page);box-shadow:var(--ring)}
.foot .small{margin-top:28px;font-size:13px;color:rgba(249,245,241,.6);max-width:60ch}
.wordmark{font-family:'Archivo';font-weight:900;font-stretch:125%;font-size:17.2vw;letter-spacing:-.05em;line-height:.8;text-align:center;color:var(--page);margin-top:30px;height:12.6vw;overflow:hidden;white-space:nowrap}
@media(min-width:900px){.wordmark{font-size:min(17.2vw,290px);height:min(12.6vw,212px)}}

.mark.papers{background:var(--indigo);color:#fff}.mark.mint{background:var(--mint-solid);color:var(--ink)}
.pchip{display:inline-flex;align-items:center;border-radius:999px;font-weight:800;white-space:nowrap;box-shadow:var(--ring-card)}
.pchip.bone{background:var(--card);color:var(--ink)}.pchip.dark{background:var(--panel);color:var(--page)}
.pchip.orange{background:var(--orange);color:var(--ink)}.pchip.indigo{background:var(--indigo);color:#fff}
.pchip.dash{background:transparent;color:inherit;box-shadow:none;border:3px dashed currentColor}
.cardrow{display:flex;align-items:center;justify-content:space-between;gap:24px}
/* the site's own graph-paper grounds (index.css device I) */
.grid-paper-fine{--grid-line-color:rgba(31,31,31,.07);background-image:repeating-linear-gradient(0deg,var(--grid-line-color) 0 1px,transparent 1px 12px),repeating-linear-gradient(90deg,var(--grid-line-color) 0 1px,transparent 1px 12px)}
.grid-paper-ruled{--grid-line-color:rgba(31,31,31,.09);background-image:repeating-linear-gradient(0deg,var(--grid-line-color) 0 1px,transparent 1px 28px)}
/* poster furniture */
.p{position:relative;overflow:hidden;background:var(--page)}
.pp{position:absolute;border-radius:64px;overflow:hidden}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""


# ═════════════════════════════════════════════════════════════════════════════
# 6. BUILDERS  (small, proven pieces: icons, mascots, blobs, tiles, covers)
# ═════════════════════════════════════════════════════════════════════════════
_ICONS = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 010 7M18.5 14.8c1.8.7 2.8 2.4 3 5"/>',
    "book": '<path d="M12 6c-1.6-1.3-4-2-7-2v14c3 0 5.4.7 7 2 1.6-1.3 4-2 7-2V4c-3 0-5.4.7-7 2zM12 6v14"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7.5h7M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
    "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 001.8 3h10.4A2 2 0 0019 18l-5-9V3M7.5 15h9"/>',
    "translate": '<path d="M4 6h9M8.5 4v2M6 6c.5 3 2.5 5.5 6 7M12 6c-.5 3-3 5.5-7 7M13 20l4-9 4 9M14.5 17h5"/>',
    "chat": '<path d="M21 12a8 8 0 01-11.6 7.1L4 20l1-4.6A8 8 0 1121 12z"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "rupee": '<path d="M7 5h10M7 9h10M7 5c5 0 7 1.5 7 4s-2 4-7 4l7 6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/>',
}


def icon(name, size=20, color="currentColor", stroke=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICONS[name]}</svg>')


SUBJECT_ICON = {"maths": "calc", "science": "flask", "english": "book", "commerce": "rupee",
                "computer": "calc", "hindi": "translate", "history": "book", "geography": "book"}


def mascot(kind="orange", cls="mascot", size=None):
    """The two brand characters. orange = awake eyes, indigo = asleep. Decorative (aria-hidden)."""
    sz = f' style="width:{size}px;height:{size}px"' if size else ""
    if kind == "indigo":
        body = ('<circle cx="50" cy="50" r="50" fill="#4351FF"/>'
                '<path d="M28 48q8 6 16 0M56 48q8 6 16 0" stroke="#1F1F1F" stroke-width="4" fill="none" stroke-linecap="round"/>'
                '<path d="M42 68q8 5 16 0" stroke="#1F1F1F" stroke-width="4" fill="none" stroke-linecap="round"/>')
    else:
        body = ('<circle cx="50" cy="50" r="50" fill="#FF8000"/><ellipse cx="36" cy="44" rx="9" ry="12" fill="#E87400"/>'
                '<ellipse cx="64" cy="44" rx="9" ry="12" fill="#E87400"/><ellipse cx="37" cy="45" rx="4" ry="7" fill="#1F1F1F"/>'
                '<ellipse cx="65" cy="45" rx="4" ry="7" fill="#1F1F1F"/><circle cx="38" cy="42" r="1.4" fill="#fff"/>'
                '<circle cx="66" cy="42" r="1.4" fill="#fff"/>')
    return f'<svg class="{cls}"{sz} viewBox="0 0 100 100" aria-hidden="true" data-art>{body}</svg>'


_BLOB_BODY = {"rough": "#D14545", "meh": "#EFA063", "fine": "#9B4FC4", "good": "#3FAFA8", "great": "#FF8000"}
_BLOB_MOUTH = {"rough": "M36 68 L64 68", "meh": "M36 68 L64 68", "fine": "M37 63 Q50 76 63 63",
               "good": "M34 61 Q50 79 66 61", "great": "M34 60 Q50 80 66 60"}
BLOB_USE = {"rough": "error states", "meh": "zero results after filters", "fine": "neutral empty states",
            "good": "confirmation and progress", "great": "success: message sent, feedback sent"}


def blob(mood="fine", size=64):
    """The mood family from src/components/ui/blob.tsx: an arch with two dots and a mouth. The mood
    is the meaning, so each owns a FIXED colour. 'great' is a circle, the one celebratory shape."""
    if mood not in _BLOB_BODY:
        raise ShikshaqError(f"blob mood {mood!r}: one of {sorted(_BLOB_BODY)}")
    shape = ('<circle cx="50" cy="50" r="42" fill="%s"/>' % _BLOB_BODY[mood] if mood == "great"
             else '<path d="M8 92 L8 46 A42 42 0 0 1 92 46 L92 92 Z" fill="%s"/>' % _BLOB_BODY[mood])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" aria-hidden="true">{shape}'
            '<circle cx="37" cy="45" r="5.5" fill="#1F1F1F"/><circle cx="63" cy="45" r="5.5" fill="#1F1F1F"/>'
            f'<path d="{_BLOB_MOUTH[mood]}" stroke="#1F1F1F" stroke-width="7" stroke-linecap="round" fill="none"/></svg>')


def logo(on_dark=False, height=28):
    """The wordmark SVG, embedded. It is authored dark on transparent; on dark it is forced to white
    (the site does the same). NEVER recoloured otherwise."""
    svg = open(os.path.join(ASSETS, "logo.svg"), encoding="utf-8").read()
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    flt = "filter:brightness(0) invert(1);" if on_dark else ""
    return f'<img src="{uri}" alt="Shikshaq" style="height:{height}px;{flt}" data-tag="logo">'


def sticker(text, tilt=4, tone="", style=""):
    if not -9 <= tilt <= 9:
        raise ShikshaqError(f"sticker tilt {tilt}: the language allows -9 to 9 degrees")
    return f'<span class="sticker {tone}" style="transform:rotate({tilt}deg);{style}">{text}</span>'


def mark(text, tone=""):
    return f'<b class="mark {tone}">{text}</b>'


def eyebrow(text):
    return f'<p class="eyelab">{text}</p>'


def numbered_heading(ordinal, line1, line2, extra_style=""):
    return f'<h2 class="nh" style="{extra_style}"><i>{ordinal}</i><span>{line1}</span><span>{line2}</span></h2>'


def cat_tile(name, count_text):
    p, fam = subject_palette(name), subject_family(name)
    ic = SUBJECT_ICON.get(fam, "book")
    return (f'<div class="cat" style="background:{p["tint"]}"><div class="tile" style="background:{p["solid"]};color:{p["badge"]}">'
            f'{icon(ic, 21)}</div><h3 style="color:{p["text"]}">{name}</h3><p style="color:{p["meta"]}">{count_text}</p></div>')


def board_row(name, count_text, style="muted"):
    sty = {"orange": f"background:{C['orange']};color:{C['ink']}", "indigo": f"background:{C['indigo_tint']};color:{C['indigo_deep']}",
           "dark": f"background:{C['panel']};color:{C['page']}", "muted": f"background:{C['muted']}"}[style]
    return f'<div class="brow" style="{sty}">{name} <small>{count_text}</small></div>'


def cover(title, kicker, line2, foot, key=None, subject=None):
    """A paper cover: coloured spine, tinted body. Colour is DECORATIVE (palette_from_key) unless the
    colour is meant to mean a subject, then pass subject=."""
    p = subject_palette(subject) if subject else palette_from_key(key or f"{kicker} {title} {line2}")
    return (f'<div class="cover" style="background:{p["tint"]}"><u style="background:{p["solid"]}"></u>'
            f'<div style="color:{p["text"]}"><span class="m">{kicker}</span><span class="t">{title}</span>'
            f'<span>{line2}</span><span class="f">{foot}</span></div></div>')


def stat(number, label, mode="teachers"):
    tint, deep = {"teachers": (C["orange_tint"], C["orange_deep"]), "papers": (C["indigo_tint"], C["indigo_deep"]),
                  "mint": (C["mint"], "#24603D")}[mode]
    return f'<div class="stat" style="background:{tint}"><b style="color:{deep}">{number}</b><span>{label}</span></div>'


def pill(text, tone="go", arrow=False, tap=True):
    a = f" {icon('arrow', 16, stroke=2.4)}" if arrow else ""
    return f'<span class="pill {tone}"{" data-tap" if tap else ""}>{text}{a}</span>'


def chip(text, on=False, papers=False):
    return f'<span class="chip{" on" if on else ""}{" papers" if papers else ""}" data-tap>{text}</span>'


# ═════════════════════════════════════════════════════════════════════════════
# 7. SECTION BUILDERS  (the page recipes, so a landing page assembles instead of being invented)
# ═════════════════════════════════════════════════════════════════════════════
def nav(links=("Teachers", "Past papers", "Subjects", "About"), active=0):
    ls = "".join(f"<b>{l}</b>" if i == active else f"<span>{l}</span>" for i, l in enumerate(links))
    return (f'<div class="nav" data-deco>{logo(False, 28)}<div class="links">{ls}</div>'
            f'<div class="cta">{pill("Join as a teacher", "cream")}{pill("Sign in", "go")}</div>'
            f'<div class="burger"><i></i></div></div>')


def fork(kind, label, bold, plain, sticker_text=None):
    mode = "teachers" if kind == "teachers" else "papers"
    bg = "peach" if mode == "teachers" else "lav"
    tile = f'<div class="tile {"o" if mode == "teachers" else "i"}">{icon("people" if mode == "teachers" else "book", 20)}</div>'
    st = sticker(sticker_text, 4) if sticker_text else ""
    return (f'<div class="fork {bg}" style="background:{MODES[mode]["tint"]}">{st}<div>{tile}<p class="lab">{label}</p>'
            f'<p class="big"><b>{bold}</b> <span>{plain}</span></p></div>'
            f'{mascot("orange" if mode == "teachers" else "indigo")}</div>')


def hero(eyebrow_text, plain, bold, after="", counts=(), quick=(), mode="teachers", search="Subject, class, area",
         avatar="S", fork_teachers=("Find a teacher", "Message them", "yourself, free"),
         fork_papers=("Past papers", "Revise", "for free"), sticker_text="Free"):
    """Hero formula: eyebrow, mixed-weight H1 (+inline avatar), live-count pills, mode toggle, ONE dominant
    search, quick chips; on desktop two fork panels with mascots. counts: [(label, subject)]."""
    cs = "".join(f'<span class="count"><s style="background:{subject_palette(sub)["solid"]}"></s>{lab}</span>' for lab, sub in counts)
    qs = "".join(chip(q) for q in quick)
    tog = ('<div class="toggle"><span class="on">Teachers</span><span>Past papers</span></div>' if mode == "teachers"
           else '<div class="toggle"><span>Teachers</span><span class="on">Past papers</span></div>')
    bcls = "" if mode == "teachers" else "papers"
    return (f'<div class="top"><section class="panel bone hero" data-fill="bone" style="padding-bottom:0"><div class="wrap hw">'
            f'<div><p class="eyebrow">{eyebrow_text}</p>'
            f'<h1 class="h1"><span class="avatar"><i>{avatar}</i></span>{plain} <b class="{bcls}" data-accent-display>{bold}</b>{after}</h1>'
            f'<div class="counts">{cs}</div><div class="desk">{tog}'
            f'<div class="search">{icon("search", 20)}<span class="ph">{search}</span>{pill("Search", "go" if mode == "teachers" else "indigo", arrow=True)}</div>'
            f'<div class="chips">{qs}</div></div><div style="height:26px"></div></div></div></section>'
            f'<div class="forks">{fork("teachers", *fork_teachers)}{fork("papers", *fork_papers, sticker_text=sticker_text)}</div></div>')


def category_section(ordinal, line1, line2, support, subjects, boards=()):
    """subjects: [(name, count_text)]; boards: [(name, count_text, style)] with style orange|indigo|dark|muted."""
    return (f'<section class="panel bone" data-fill="bone"><div class="wrap">{numbered_heading(ordinal, line1, line2)}'
            f'<p class="sup">{support}</p><div class="mosaic">{"".join(cat_tile(n, c) for n, c in subjects)}</div>'
            f'<div class="boards">{"".join(board_row(*b) for b in boards)}</div></div></section>')


def papers_slab(ordinal, title, body, cta, covers):
    return (f'<section class="panel ind slab" data-fill="indigo"><div class="wrap slabgrid"><div>'
            f'<p class="eyelab">{ordinal}</p><h2 style="margin-top:6px">{title}</h2><p>{body}</p>'
            f'<div style="margin-top:20px">{pill(cta, "white", arrow=True)}</div></div>'
            f'<div class="covers">{"".join(covers)}</div></div></section>')


def steps_slab(ordinal, title, steps, fine):
    """steps: [(icon, heading, text)]. Ink on orange, never white."""
    st = "".join(f'<div class="step"><div class="tile">{icon(i, 20)}</div><h3>{h}</h3><p>{t}</p></div>' for i, h, t in steps)
    return (f'<section class="panel org" data-fill="orange"><div class="wrap"><p class="eyelab">{ordinal}</p>'
            f'<h2 style="font-size:clamp(28px,3.6vw,44px);font-weight:800;margin-top:8px">{title}</h2>'
            f'<div class="steps">{st}</div><p style="margin-top:22px;font-weight:700;font-size:15px">{fine}</p></div></section>')


def stats_section(ordinal, line1, line2_html, support, stats):
    """stats: [(number, label, mode)]. line2_html may carry a mark()."""
    return (f'<section class="panel bone" data-fill="bone"><div class="wrap">'
            f'{numbered_heading(ordinal, line1, line2_html, "line-height:1.12")}<p class="sup">{support}</p>'
            f'<div class="stats">{"".join(stat(*s) for s in stats)}</div></div></section>')


def eyes_section(heading_plain, heading_bold, support, cta, slots=("+ subject", "+ class", "+ area")):
    """The signature panel: a domed eyes panel (pupils follow the pointer) with the sentence builder."""
    a, b, c = slots
    return (f'<section class="heads" data-fill="bone"><h2 style="font-size:clamp(26px,3.6vw,42px);font-weight:400;letter-spacing:-.045em">'
            f'{heading_plain} <b style="font-weight:800">{heading_bold}</b></h2><p class="sup" style="margin:10px auto 0">{support}</p></section>'
            f'<section class="eyes" data-fill="orange"><div class="dome" data-deco></div>'
            f'<div class="eye-row" data-deco><div class="eye"><div class="pupil" id="p1"></div></div><div class="eye"><div class="pupil" id="p2"></div></div></div>'
            f'<div class="sentence">I need a <span class="slot">{a}</span> teacher for <span class="slot">{b}</span> near <span class="slot">{c}</span></div>'
            f'<span class="pill ghost" data-tap>{cta}</span></section>')


EYES_JS = ("<script>const pu=[document.getElementById('p1'),document.getElementById('p2')].filter(Boolean);"
           "addEventListener('pointermove',e=>{pu.forEach(p=>{const r=p.parentElement.getBoundingClientRect();"
           "const dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2);const d=Math.hypot(dx,dy)||1,k=Math.min(1,d/260);"
           "p.style.transform=`translate(${dx/d*20*k}px,${dy/d*18*k}px)`})});</script>")


def footer(lead_html, pills=("find a teacher", "past papers", "contact"), small=""):
    ps = "".join(pill(p, "cream") for p in pills)
    return (f'<footer class="foot dark" data-fill="dark"><div class="wrap"><p class="l">{lead_html}</p><div class="row">{ps}</div>'
            f'<p class="small">{small}</p></div><div class="wordmark" data-crop data-tag="wordmark">shikshaq</div></footer>')


def emph(text):
    """A highlighted phrase inside the footer lead sentence."""
    return f"<em>{text}</em>"


def sun(size=160, fill="#FFC700"):
    """The campaign's burst: a spiky sun with squinting happy eyes (ported from addons/shikshaq/campaign/characters.mjs)."""
    import math
    d = ""
    for i in range(28):
        a = i / 28.0 * math.pi * 2
        r = 41 if i % 2 else 49
        d += ("L" if i else "M") + f"{50 + r * math.cos(a):.1f} {50 + r * math.sin(a):.1f}"
    face = ('<path d="M30 44 L40 49 L30 54" stroke="#1F1F1F" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M70 44 L60 49 L70 54" stroke="#1F1F1F" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M40 62 Q50 70 60 62" stroke="#1F1F1F" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" aria-hidden="true" data-art><path d="{d}Z" fill="{fill}"/>{face}</svg>')


def lobe(size=160, fill="#5B7BD9"):
    """The campaign's four-lobe X with a face (ported from characters.mjs)."""
    l = lambda a: f'<ellipse cx="50" cy="50" rx="15" ry="46" fill="{fill}" transform="rotate({a} 50 50)"/>'
    face = ('<circle cx="38" cy="48" r="5" fill="#1F1F1F"/><circle cx="62" cy="48" r="5" fill="#1F1F1F"/>'
            '<path d="M40 60 Q50 68 60 60" stroke="#1F1F1F" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" aria-hidden="true" data-art>{l(45)}{l(135)}'
            f'<circle cx="50" cy="50" r="22" fill="{fill}"/>{face}</svg>')


def art(html, style):
    """Position decorative art. Marked data-art so the gate keeps it off the words."""
    return f'<div data-art style="position:absolute;{style}">{html}</div>'


# ─────────────────────────────────────────────────────────────────────────────
# SCHOOL-OBJECT CHARACTERS: a full set of 16, one system (owner approved the first four 2026-11-27 and asked for the rest).
# The vocabulary is the campaign's (addons/shikshaq/campaign/characters.mjs): a flat body, two dots, one mouth, no outlines, no
# gradients, no shadows. COLOUR comes ONLY from CHAR_PALETTE (the site's own colours: blob moods, the burst yellow, the subject
# solids, brand orange and indigo, the warm neutrals). They are shapes, not mascots: no names, no stories. Faces: dots are INK,
# r 3.4, 12 apart; the mouth is a 3.4 round-capped stroke. The warning sign is a SIGN, so it carries a mark, not a face.
# ─────────────────────────────────────────────────────────────────────────────
_INK = "#1F1F1F"
CHAR_PALETTE = {
    _INK, "#FFFFFF", "#FFC700", "#EFA063", "#FCECDE", "#F0EAE2", "#D8CFC4", "#E3F7EC", "#3FAFA8", "#C68B39", "#604724",
    "#4775D1", "#D74242", "#9F53C6", "#34B268", "#46B9B9", "#F2A15A", "#FF8000", "#4351FF", "#D14545", "#9B4FC4",
}


def _csvg(size, inner, rot=0):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" aria-hidden="true" data-art '
            f'style="overflow:visible;transform:rotate({rot}deg)">{inner}</svg>')


def _cface(cx, cy, gap=12, r=3.4, mouth="smile", sw=3.4):
    m = {"smile": f"M{cx-6} {cy+9} Q{cx} {cy+16} {cx+6} {cy+9}", "flat": f"M{cx-6} {cy+11} L{cx+6} {cy+11}",
         "smirk": f"M{cx-6} {cy+10} Q{cx+1} {cy+16} {cx+7} {cy+8}"}[mouth]
    return (f'<circle cx="{cx-gap/2}" cy="{cy}" r="{r}" fill="{_INK}"/><circle cx="{cx+gap/2}" cy="{cy}" r="{r}" fill="{_INK}"/>'
            f'<path d="{m}" stroke="{_INK}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>')


def _stroke(d, color=_INK, w=4, cap="round"):
    return f'<path d="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="{cap}" stroke-linejoin="round"/>'


def _ch_pencil():
    return (f'<rect x="34" y="20" width="32" height="56" fill="#FFC700"/><rect x="34" y="8" width="32" height="14" rx="7" fill="#EFA063"/>'
            f'<rect x="34" y="20" width="32" height="7" fill="#F0EAE2"/><polygon points="34,76 66,76 50,96" fill="#FCECDE"/>'
            f'<polygon points="44.5,87 55.5,87 50,96" fill="{_INK}"/>' + _cface(50, 47))


def _ch_star():
    import math
    pts = " ".join(f"{50 + (46 if i % 2 == 0 else 22) * math.cos(-math.pi / 2 + i * math.pi / 5):.1f},"
                   f"{54 + (46 if i % 2 == 0 else 22) * math.sin(-math.pi / 2 + i * math.pi / 5):.1f}" for i in range(10))
    return (f'<polygon points="{pts}" fill="#3FAFA8" stroke="#3FAFA8" stroke-width="9" stroke-linejoin="round"/>'
            + _stroke("M36 47 L45 50", w=3.4) + _cface(50, 54, mouth="smirk"))


def _ch_kulhad():
    steam = "".join(_stroke(f"M{x} 30 q-5 -6 0 -12 q5 -6 0 -12", "#D8CFC4", 3.2) for x in (38, 50, 62))
    return (steam + '<path d="M24 38 H76 L69 86 Q68 90 64 90 H36 Q32 90 31 86 Z" fill="#C68B39"/><ellipse cx="50" cy="38" rx="26" ry="6.5" fill="#604724"/>'
            + _stroke("M41 62 q4 -5 8 0", w=3.4) + _stroke("M53 62 q4 -5 8 0", w=3.4) + _stroke("M44 70 Q50.5 76 57 70", w=3.4))


def _ch_warning():
    return ('<polygon points="50,14 90,82 10,82" fill="#FFC700" stroke="#FFC700" stroke-width="10" stroke-linejoin="round"/>'
            + _stroke("M50 38 L50 60", w=6) + f'<circle cx="50" cy="71" r="4" fill="{_INK}"/>')


def _ch_book():
    return ('<rect x="24" y="12" width="52" height="76" rx="6" fill="#4775D1"/><rect x="70" y="16" width="8" height="68" rx="2" fill="#F0EAE2"/>'
            '<polygon points="58,12 66,12 66,36 62,31 58,36" fill="#D74242"/><rect x="33" y="24" width="20" height="6" rx="3" fill="#F0EAE2"/>' + _cface(48, 54))


def _ch_backpack():
    return (f'{_stroke("M42 28 v-8 q8 -8 16 0 v8", w=4.5)}<rect x="22" y="40" width="7" height="30" rx="3.5" fill="{_INK}"/><rect x="71" y="40" width="7" height="30" rx="3.5" fill="{_INK}"/>'
            '<rect x="26" y="26" width="48" height="62" rx="20" fill="#F2A15A"/><rect x="33" y="60" width="34" height="22" rx="8" fill="#C68B39"/>'
            + _stroke("M35 63 H65", w=3) + _cface(50, 39))


def _ch_ruler():
    ticks = "".join(_stroke(f"M{14 + i * 7.2:.1f} 33 v{9 if i % 5 == 0 else 5}", w=2.6, cap="butt") for i in range(11))
    return ('<rect x="8" y="31" width="84" height="38" rx="6" fill="#46B9B9"/>' + ticks + _cface(50, 50, r=3.2, mouth="smile", sw=3.2))


def _ch_calculator():
    cols = [["#FF8000", "#FFC700", "#3FAFA8"], ["#D8CFC4"] * 3, ["#D8CFC4", "#D8CFC4", "#F2A15A"]]
    btn = "".join(f'<circle cx="{36 + c * 14}" cy="{52 + r * 13}" r="4.6" fill="{cols[r][c]}"/>' for r in range(3) for c in range(3))
    return (f'<rect x="22" y="8" width="56" height="84" rx="10" fill="{_INK}"/><rect x="28" y="14" width="44" height="26" rx="5" fill="#E3F7EC"/>'
            + _cface(50, 24, gap=12, r=3, sw=3).replace("Q50 37", "Q50 35") + btn)


def _ch_clock():
    return (f'<circle cx="26" cy="22" r="11" fill="#FFC700"/><circle cx="74" cy="22" r="11" fill="#FFC700"/>{_stroke("M30 84 l-5 7 M70 84 l5 7", w=4.5)}'
            '<circle cx="50" cy="54" r="34" fill="#D74242"/><circle cx="50" cy="54" r="27" fill="#F0EAE2"/>'
            + _stroke("M50 31 v5 M73 54 h-5 M50 77 v-5 M27 54 h5", w=2.8, cap="butt") + _cface(50, 50, gap=14, mouth="smile"))


def _ch_bulb():
    rays = "".join(_stroke(f"M{50 + 36 * __import__('math').cos(a):.1f} {40 + 36 * __import__('math').sin(a):.1f} L{50 + 44 * __import__('math').cos(a):.1f} {40 + 44 * __import__('math').sin(a):.1f}", "#FFC700", 4)
                    for a in [__import__('math').radians(d) for d in (-150, -120, -90, -60, -30)])
    return (rays + '<circle cx="50" cy="42" r="28" fill="#FFC700"/><polygon points="38,62 62,62 60,74 40,74" fill="#FFC700"/>'
            '<rect x="39" y="72" width="22" height="16" rx="4" fill="#D8CFC4"/>' + _stroke("M40 79 H60 M41 84 H59", w=2.6) + _cface(50, 40))


def _ch_globe():
    return ('<circle cx="50" cy="46" r="32" fill="#4775D1"/><path d="M26 34 q7 -12 19 -6 q4 8 -6 12 q-9 3 -13 -6z" fill="#34B268"/>'
            '<path d="M61 58 q10 -4 14 5 q-2 10 -12 8 q-6 -6 -2 -13z" fill="#34B268"/>'
            f'<rect x="47" y="76" width="6" height="10" fill="{_INK}"/><rect x="34" y="84" width="32" height="7" rx="3.5" fill="{_INK}"/>' + _cface(50, 46))


def _ch_trophy():
    return (_stroke("M28 22 H18 Q13 22 13 28 Q13 42 28 46", "#FFC700", 6) + _stroke("M72 22 H82 Q87 22 87 28 Q87 42 72 46", "#FFC700", 6)
            + '<path d="M28 14 H72 V40 Q72 62 50 64 Q28 62 28 40 Z" fill="#FFC700"/><rect x="44" y="62" width="12" height="14" fill="#C68B39"/>'
            '<rect x="30" y="74" width="40" height="14" rx="4" fill="#C68B39"/>' + _cface(50, 34))


def _ch_notebook():
    rings = "".join(f'<rect x="17" y="{16 + i * 13}" width="16" height="5.5" rx="2.75" fill="{_INK}"/>' for i in range(6))
    return ('<rect x="24" y="10" width="58" height="80" rx="8" fill="#9F53C6"/>' + rings + '<rect x="40" y="26" width="34" height="38" rx="8" fill="#F0EAE2"/>'
            '<rect x="40" y="72" width="34" height="4" rx="2" fill="#F0EAE2"/><rect x="40" y="80" width="22" height="4" rx="2" fill="#F0EAE2"/>' + _cface(57, 42, gap=11, r=3.2, sw=3.2))


def _ch_cap():
    return ('<path d="M24 42 v22 Q24 82 50 82 Q76 82 76 64 v-22 L50 56 Z" fill="#4351FF"/>'
            f'<polygon points="50,12 95,33 50,54 5,33" fill="{_INK}"/>' + _stroke("M86 36 v26", "#FFC700", 3.8) + '<circle cx="86" cy="65" r="4.6" fill="#FFC700"/>'
            + _cface(50, 66, gap=12, r=3.2, sw=3.2))


def _ch_flask():
    return ('<path d="M42 10 H58 V34 L82 80 Q87 90 74 90 H26 Q13 90 18 80 L42 34 Z" fill="#34B268"/><rect x="38" y="6" width="24" height="7" rx="3.5" fill="#D8CFC4"/>'
            '<circle cx="66" cy="74" r="3.4" fill="#E3F7EC"/><circle cx="31" cy="82" r="2.6" fill="#E3F7EC"/>' + _cface(50, 68, gap=13, mouth="smile"))


def _ch_compass():
    return (_stroke("M50 24 L26 84", "#F2A15A", 9) + _stroke("M50 24 L74 84", "#C68B39", 9)
            + f'<polygon points="21.5,82 30,86 24,96" fill="{_INK}"/><polygon points="70,86 78.5,82 76,96" fill="{_INK}"/>'
            f'<circle cx="50" cy="9" r="5" fill="{_INK}"/><circle cx="50" cy="26" r="14" fill="#FFC700"/>' + _cface(50, 24, gap=8, r=2.6, sw=2.8).replace("Q50 38", "Q50 37"))


# name -> (builder, default tilt, silhouette colour (what the shape IS against a ground), note)
CHARACTERS = {
    "pencil":     (_ch_pencil, -18, "#FFC700", "practice, drafts, the first mark"),
    "star":       (_ch_star, 8, "#3FAFA8", "praise, a top mark, a highlight"),
    "kulhad":     (_ch_kulhad, 0, "#C68B39", "a break, chai, calm before a paper"),
    "warning":    (_ch_warning, -6, "#FFC700", "heads up, a note before you start (a sign: no face)"),
    "book":       (_ch_book, 6, "#4775D1", "reading, a subject, a syllabus"),
    "backpack":   (_ch_backpack, 0, "#F2A15A", "school day, being ready"),
    "ruler":      (_ch_ruler, -20, "#46B9B9", "measuring, geometry, accuracy"),
    "calculator": (_ch_calculator, 8, _INK, "maths, numbers, checking"),
    "clock":      (_ch_clock, 4, "#D74242", "time, timed practice, a deadline"),
    "bulb":       (_ch_bulb, 0, "#FFC700", "an idea, understanding, a tip"),
    "globe":      (_ch_globe, -8, "#4775D1", "geography, the wider world"),
    "trophy":     (_ch_trophy, 0, "#FFC700", "a result, a milestone (never a claim about results)"),
    "notebook":   (_ch_notebook, -6, "#9F53C6", "notes, revision, homework"),
    "cap":        (_ch_cap, 8, _INK, "graduation, qualifications (the logo's own cap)"),
    "flask":      (_ch_flask, 6, "#34B268", "science, trying things out"),
    "compass":    (_ch_compass, 0, "#F2A15A", "geometry, direction, finding your way"),
}


def character(name, size=160, rot=None):
    """One school-object character as inline svg (decorative: data-art). rot defaults to the character's own tilt."""
    if name not in CHARACTERS:
        raise ShikshaqError(f"character {name!r}: one of {sorted(CHARACTERS)}")
    fn, tilt, _, _ = CHARACTERS[name]
    return _csvg(size, fn(), tilt if rot is None else rot)


def character_ok(name, ground, floor=1.5):
    """Is this character's silhouette colour distinguishable from this ground? (measured, floor 1.5:1).
    The cup (terracotta) is lost on orange, ink characters on the dark panel, yellow ones on bone cards' lightest tints, etc."""
    if name not in CHARACTERS:
        raise ShikshaqError(f"character {name!r}: one of {sorted(CHARACTERS)}")
    return contrast(CHARACTERS[name][2], ground) >= floor



def place(html, style):
    """Position a TEXT-BEARING object (a chip, a badge). Unlike art(), it is not decorative, so the gate treats its words as words."""
    return f'<div style="position:absolute;{style}">{html}</div>'


def pchip(text, tilt=0, tone="bone", size=40, extra=""):
    """A poster-scale chip/sticker (inline, not absolute). tone: bone|dark|orange|indigo|dash."""
    if not -9 <= tilt <= 9:
        raise ShikshaqError(f"chip tilt {tilt}: the language allows -9 to 9 degrees")
    return (f'<span class="pchip {tone}" style="height:{int(size*1.7)}px;padding:0 {int(size*.7)}px;font-size:{size}px;'
            f'transform:rotate({tilt}deg);{extra}">{text}</span>')


def swipe_arrow(color="currentColor", w=190):
    """The carousel 'next' cue: one long drawn arrow."""
    return (f'<svg width="{w}" height="40" viewBox="0 0 190 40" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" data-art><path d="M6 21 C60 17 110 24 180 20"/><path d="M158 6 L182 20 L158 34"/></svg>')


def index_tag(i, n, color=None):
    c = f"color:{color};" if color else ""
    return f'<span class="eyelab" style="font-size:26px;{c}">{i:02d} / {n:02d}</span>'


def slide_header(i, n, on_dark=False, color=None):
    """Logo left, index right: the carousel's constant top row. The logo goes white on dark only."""
    return (f'<div style="display:flex;justify-content:space-between;align-items:center">{logo(on_dark, 56)}'
            f'{index_tag(i, n, color)}</div>')


def contact_sheet(files, out, cols=None, cell=360):
    """One image of every slide side by side, judged like a feed grid (the carousel's looking gate)."""
    from PIL import Image
    ims = [Image.open(f).convert("RGB") for f in files]
    cols = cols or len(ims)
    h = int(cell * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell + 16) + 16, rows * (h + 16) + 16), (237, 231, 223))
    for k, im in enumerate(ims):
        sheet.paste(im.resize((cell, h)), (16 + (k % cols) * (cell + 16), 16 + (k // cols) * (h + 16)))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out)
    return out


async def render_carousel(slides, out_dir, name, W=1080, H=1350, scale=1, copy=None):
    """Render a list of slide HTML bodies (each from sk.poster) through ONE browser, gate each, and write a contact sheet.
    copy: every visible string in the carousel; it must pass copy_gate or this raises before anything is drawn."""
    if copy is not None:
        errs, warns = copy_gate(copy)
        for w in warns:
            print("[copy] note:", w)
        if errs:
            raise ShikshaqError("copy gate failed:\n  " + "\n  ".join(errs))
    results = []
    async with session() as s:
        for k, body in enumerate(slides, 1):
            html = doc(body, kind="poster", W=W, H=H, title=f"{name} {k}/{len(slides)}")
            results.append(await s.render(html, os.path.join(out_dir, f"{name}-{k:02d}.png"), W, H, kind="poster", scale=scale, name=f"{name}-{k:02d}"))
    contact_sheet([r.png for r in results], os.path.join(out_dir, f"{name}-sheet.png"))
    return results


def doc(body, kind="page", W=None, H=None, title="Shikshaq", extra_css=""):
    """Wrap a body in a full HTML document. kind='poster' fixes the canvas to W x H and the gate measures
    against it; kind='page' is a normal scrolling page measured against the viewport."""
    head = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{font_css()}\n{tokens_css()}\n{STYLESHEET}\n{extra_css}</style></head>')
    if kind == "poster":
        if not (W and H):
            raise ShikshaqError("doc(kind='poster') needs W and H")
        return f'{head}<body style="margin:0"><div class="p" style="width:{W}px;height:{H}px">{body}</div></body></html>'
    return f'{head}<body><div class="stack">{body}</div></body></html>'


def poster(panels, W=1080, H=1350, margin=24, radius=64):
    """A poster as a column of rounded panels on bone. panels: [(fill, html, height_px or None)].
    The last panel with height None takes the rest. fill: bone | indigo | orange | dark | peach | lav | mint."""
    fills = {"bone": "var(--card)", "indigo": "var(--indigo)", "orange": "var(--orange)", "dark": "var(--panel)",
             "peach": "var(--orange-tint)", "lav": "var(--indigo-tint)", "mint": "var(--mint)"}
    fixed = sum(h for _, _, h in panels if h)
    free = [p for p in panels if not p[2]]
    each = (H - 2 * margin - fixed) // max(1, len(free))
    y, out = margin, []
    for fill, html, h in panels:
        hh = h or each
        fg = "color:#fff;" if fill == "indigo" else ("color:var(--page);" if fill == "dark" else "")
        # the fill CLASS rides along so the stylesheet's per-ground rules (label colour on indigo, ink on orange) apply
        cls = {"bone": "bone", "indigo": "ind", "orange": "org", "dark": "dark", "peach": "peach", "lav": "lav", "mint": "mintbg"}[fill]
        out.append(f'<div class="pp {cls}" data-fill="{fill}" style="left:{margin}px;right:{margin}px;top:{y}px;height:{hh}px;'
                   f'background:{fills[fill]};border-radius:{radius}px;{fg}">{html}</div>')
        y += hh
    return "".join(out)


# ═════════════════════════════════════════════════════════════════════════════
# 8. THE GATE  (measured on the rendered DOM: the only check that sees what was DRAWN)
# ═════════════════════════════════════════════════════════════════════════════
GATE_JS = r"""
(args)=>{
 const {kind,W,H}=args; const out=[];
 const rgb=s=>{const m=s.match(/[\d.]+/g).map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1}};
 const L=c=>{const v=[c.r,c.g,c.b].map(x=>{x/=255;return x<=.03928?x/12.92:((x+.055)/1.055)**2.4});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
 const ratio=(a,b)=>{const [x,y]=[L(a),L(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
 const hex=c=>'#'+[c.r,c.g,c.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join('').toUpperCase();
 const over=(f,b)=>({r:f.r*f.a+b.r*(1-f.a),g:f.g*f.a+b.g*(1-f.a),b:f.b*f.a+b.b*(1-f.a),a:1});
 const surface=el=>{const layers=[];for(let e=el;e;e=e.parentElement){const cs=getComputedStyle(e);
   if(cs.backgroundImage!=='none'&&e!==el)return null; if(cs.backgroundImage!=='none')return null;
   const c=rgb(cs.backgroundColor);if(c.a>0){layers.push(c);if(c.a>=.99)break}}
   let base={r:249,g:245,b:241,a:1};for(let i=layers.length-1;i>=0;i--)base=over(layers[i],base);return base};
 const root=document.querySelector('.p')||document.body;
 const vis=el=>{const r=el.getBoundingClientRect(),cs=getComputedStyle(el);return r.width>0&&r.height>0&&cs.display!=='none'&&cs.visibility!=='hidden'};
 // a leaf's layout box in the frame of a transformed ancestor (null if the offset chain does not reach it)
 const local=(el,T)=>{let x=0,y=0,e=el;while(e&&e!==T){x+=e.offsetLeft;y+=e.offsetTop;e=e.offsetParent}
   return e===T?{left:x,top:y,right:x+el.offsetWidth,bottom:y+el.offsetHeight}:null};
 const leaves=[];
 root.querySelectorAll('*').forEach(el=>{
   if(/^(STYLE|SCRIPT|SVG|PATH|svg)$/i.test(el.tagName)||el.closest('[data-deco]')||el.closest('svg'))return;
   const own=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
   if(!own||!vis(el))return;
   // GLYPH box: union of the element's OWN text nodes, not its block box (a padded block is not text)
   // one rect per LINE of the element's own text (a paragraph's union box is mostly air beside a short last line)
   let u=null;const rs=[];[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).forEach(n=>{const rg=document.createRange();rg.selectNodeContents(n);
     [...rg.getClientRects()].forEach(q=>{if(q.width>1&&q.height>1){rs.push({left:q.left,right:q.right,top:q.top,bottom:q.bottom});
       u=u?{left:Math.min(u.left,q.left),right:Math.max(u.right,q.right),top:Math.min(u.top,q.top),bottom:Math.max(u.bottom,q.bottom)}:{left:q.left,right:q.right,top:q.top,bottom:q.bottom}}})});
   if(!u)return;u.width=u.right-u.left;u.height=u.bottom-u.top;
   let T=null;for(let a=el.parentElement;a&&a!==root;a=a.parentElement){const tf=getComputedStyle(a).transform;if(tf&&tf!=='none'){T=a;break}}
   leaves.push({el,r:u,rs,T,txt:el.textContent.trim().slice(0,28)});
 });
 // S9 horizontal overflow (pages)
 if(kind==='page'){const de=document.documentElement;
   if(de.scrollWidth>de.clientWidth+1){const bad=[];
     document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>de.clientWidth+1&&r.width>0){
       let a=e,cl=false;while((a=a.parentElement)){const o=getComputedStyle(a).overflowX;if(o!=='visible'&&a!==document.body&&a!==document.documentElement){cl=true;break}}
       if(!cl)bad.push(e.tagName.toLowerCase()+'.'+(e.className&&e.className.baseVal===undefined?String(e.className).split(' ')[0]:'')+'@'+Math.round(r.right))}});
     out.push(['HARD','OVERFLOW-X page is '+de.scrollWidth+'px in a '+de.clientWidth+'px viewport; widest: '+bad.slice(0,3).join(', ')+'. A scroller inside a grid cell needs min-width:0 on the cell.'])}}
 leaves.forEach(l=>{
   const cs=getComputedStyle(l.el),size=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight)||400;
   const minSize=kind==='poster'?20:11;
   if(size<minSize&&!l.el.closest('[data-tiny]'))out.push(['HARD','TINY-TEXT '+size+'px < '+minSize+'px on "'+l.txt+'"']);
   const bg=surface(l.el);
   if(bg&&!l.el.closest('[data-lowcontrast]')){
     const tc=rgb(cs.color);const eff=over(tc,bg);const got=ratio(eff,bg);
     const large=size>=24||(size>=18.66&&wt>=700);const need=large?3:4.5;
     if(got<need){
       // The site's signature payoff (heavy orange display type on bone) measures 2.4:1, under the 3:1
       // large-text floor, and no owner ruling covers it. It is allowed ONLY when declared, only at 28px+ bold (the site's own mobile hero is 29px),
       // display size, and it is reported every time so it stays a visible decision, never a silent pass.
       if(l.el.closest('[data-accent-display]')&&size>=28&&wt>=700)out.push(['INFO','ACCENT-DISPLAY '+got.toFixed(2)+':1 on "'+l.txt+'" (the live site does this; unruled by the owner, below the 3:1 floor)']);
       else out.push(['HARD','CONTRAST '+got.toFixed(2)+':1 < '+need+' on "'+l.txt+'" ('+hex(eff)+' on '+hex(bg)+')'])}}
   if(kind==='poster'&&!l.el.closest('[data-bleed]')){const r=l.r;
     if(r.left<-1||r.top<-1||r.right>W+1||r.bottom>H+1)out.push(['HARD','OFF-CANVAS "'+l.txt+'"'])}
   // text sliced by an overflow:hidden ancestor
   if(!l.el.closest('[data-crop]')){let a=l.el.parentElement;
     while(a&&a!==document.body){const o=getComputedStyle(a);
       if(/hidden|clip/.test(o.overflowX+o.overflowY)){const q=a.getBoundingClientRect();
         const ix=Math.min(l.r.right,q.right)-Math.max(l.r.left,q.left),iy=Math.min(l.r.bottom,q.bottom)-Math.max(l.r.top,q.top);
         const vis2=Math.max(0,ix)*Math.max(0,iy),full=l.r.width*l.r.height;
         if(full>0&&vis2<full*.9){out.push(['HARD','CLIPPED "'+l.txt+'" is '+Math.round(100*(1-vis2/full))+'% cut off by '+a.tagName.toLowerCase()+'.'+String(a.className).split(' ')[0]]);break}}
       a=a.parentElement}}
 });
 // text-on-text collisions
 for(let i=0;i<leaves.length;i++)for(let j=i+1;j<leaves.length;j++){const a=leaves[i],b=leaves[j];
   if(a.el.contains(b.el)||b.el.contains(a.el))continue;
   if(a.T&&a.T===b.T){const A=local(a.el,a.T),B=local(b.el,b.T);
     if(A&&B){const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left),oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
       if(ox>8&&oy>8)out.push(['HARD','COLLISION "'+a.txt+'" x "'+b.txt+'" ('+Math.round(ox)+'x'+Math.round(oy)+', measured in the tilted group\'s own frame)']);continue}}
   let hit=null;a.rs.forEach(p=>b.rs.forEach(q=>{const ox=Math.min(p.right,q.right)-Math.max(p.left,q.left),oy=Math.min(p.bottom,q.bottom)-Math.max(p.top,q.top);
     if(ox>8&&oy>8&&(!hit||ox*oy>hit[0]*hit[1]))hit=[ox,oy]}));
   if(hit)out.push(['HARD','COLLISION "'+a.txt+'" x "'+b.txt+'" ('+Math.round(hit[0])+'x'+Math.round(hit[1])+')'])}
 // TEXT-COVERED: a line of type partly painted over by an unrelated opaque object (a pill sitting on the last line of a paragraph).
 // Walk the paint stack at 9 points per line; elements above the text that have an opaque fill and are not its ancestor/descendant hide it.
 leaves.forEach(l=>{if(l.el.closest('[data-crop]'))return;let worst=null;
   l.rs.forEach(q=>{let hidden=0,seen=0,by=null;
     for(let i=0;i<3;i++)for(let j=0;j<3;j++){const x=q.left+(q.right-q.left)*(i+.5)/3,y=q.top+(q.bottom-q.top)*(j+.5)/3;
       const st=document.elementsFromPoint(x,y),it=st.findIndex(e=>e===l.el||l.el.contains(e));if(it===-1)continue;seen++;
       const cover=st.slice(0,it).find(e=>{if(e.contains(l.el)||l.el.contains(e)||e.closest('svg')||e.dataset&&e.dataset.deco!==undefined)return false;
         const cs=getComputedStyle(e);return rgb(cs.backgroundColor).a>.9||cs.backgroundImage!=='none'});
       if(cover){hidden++;by=cover}}
     if(seen&&hidden/seen>=.25&&(!worst||hidden>worst.h))worst={h:hidden,n:seen,by}});
   if(worst)out.push(['HARD','TEXT-COVERED "'+l.txt+'" is '+Math.round(100*worst.h/worst.n)+'% hidden under '+worst.by.tagName.toLowerCase()+'.'+String(worst.by.className).split(' ')[0]+(worst.by.textContent.trim()?' "'+worst.by.textContent.trim().slice(0,22)+'"':'')])});
 // ART-ON-TEXT: a mascot or other art that lands on type (art clipped by an overflow:hidden parent only counts where it is visible)
 root.querySelectorAll('svg.mascot,[data-art]').forEach(sv=>{let r=sv.getBoundingClientRect();
   for(let a=sv.parentElement;a&&a!==document.body;a=a.parentElement){if(/hidden|clip/.test(getComputedStyle(a).overflow)){const q=a.getBoundingClientRect();
     r={left:Math.max(r.left,q.left),right:Math.min(r.right,q.right),top:Math.max(r.top,q.top),bottom:Math.min(r.bottom,q.bottom)}}}
   leaves.forEach(l=>{if(sv.contains(l.el))return;let hit=null;l.rs.forEach(q=>{const ox=Math.min(r.right,q.right)-Math.max(r.left,q.left),oy=Math.min(r.bottom,q.bottom)-Math.max(r.top,q.top);
       if(ox>8&&oy>8&&(!hit||ox*oy>hit[0]*hit[1]))hit=[ox,oy,(Math.max(r.left,q.left)+Math.min(r.right,q.right))/2,(Math.max(r.top,q.top)+Math.min(r.bottom,q.bottom))/2]});
     if(hit){ // art peeking from BEHIND an opaque panel is covered, not landing: walk the paint stack at the overlap
       const st=document.elementsFromPoint(hit[2],hit[3]),ia=st.findIndex(e=>sv.contains(e));
       const opaque=e=>{const cs=getComputedStyle(e);const c=rgb(cs.backgroundColor);return (c.a>.9||cs.backgroundImage!=='none')&&!sv.contains(e)};
       const covered=ia===-1||st.slice(0,ia).some(opaque);
       if(!covered)out.push(['HARD','ART-ON-TEXT art lands on "'+l.txt+'" ('+Math.round(hit[0])+'x'+Math.round(hit[1])+')'])}})});
 // 44px targets on anything declared interactive
 document.querySelectorAll('[data-tap]').forEach(e=>{if(!vis(e))return;const r=e.getBoundingClientRect();
   if(Math.min(r.width,r.height)<43.5)out.push(['HARD','TAP-TARGET '+Math.round(r.width)+'x'+Math.round(r.height)+' < 44 on "'+e.textContent.trim().slice(0,20)+'"'])});
 // S10 saturated seams
 const SAT=new Set(['orange','indigo']);let seams=0;
 document.querySelectorAll('[data-fill]').forEach(e=>{const n=e.nextElementSibling;
   if(n&&n.dataset&&n.dataset.fill&&SAT.has(e.dataset.fill)&&SAT.has(n.dataset.fill)){seams++;
     if(e.dataset.fill===n.dataset.fill)out.push(['HARD','SAME-HUE seam: two '+e.dataset.fill+' panels touch'])}});
 if(seams>1)out.push(['HARD','SATURATED-SEAMS '+seams+' orange/indigo panels touch; the live site allows one']);
 else if(seams===1)out.push(['INFO','one orange/indigo seam (the live home does this once, deliberately)']);
 // fonts: every word is Archivo or Geist, and whichever a page USES must have loaded (a browser skips unused faces)
 const loaded=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family.replace(/['"]/g,''));
 const used=new Set(),offb=new Set();
 leaves.forEach(l=>{const fam=getComputedStyle(l.el).fontFamily.split(',')[0].replace(/['"]/g,'').trim();
   if(fam==='Archivo'||fam==='Geist')used.add(fam);else if(!l.el.closest('[data-font-ok]'))offb.add(fam+' on "'+l.txt+'"')});
 offb.forEach(f=>out.push(['HARD','FONT-FALLBACK off-brand face '+f+' (every word is Archivo or Geist)']));
 used.forEach(f=>{if(!loaded.includes(f))out.push(['HARD','FONT-FALLBACK '+f+' is used but did not load; every glyph is in a fallback face'])});
 // S8 dashes
 const txt=(root.innerText||'');if(/[\u2014\u2013]/.test(txt))out.push(['HARD','DASH em or en dash in visible text (site rule: none)']);
 return out;
}
"""


class Result:
    def __init__(self, png, issues, W, H):
        self.png, self.issues, self.W, self.H = png, issues, W, H
        self.hard = [m for s, m in issues if s == "HARD"]
        self.info = [m for s, m in issues if s != "HARD"]
        self.clean = not self.hard

    def __repr__(self):
        return f"<shikshaq.Result {'CLEAN' if self.clean else str(len(self.hard)) + ' HARD'} {self.png}>"


class session:
    """`async with sk.session():` holds one browser open across many renders."""
    def __init__(self):
        self._pw = self._b = None

    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self._pw = await async_playwright().start()
        self._b = await self._pw.chromium.launch()
        return self

    async def __aexit__(self, *exc):
        await self._b.close(); await self._pw.stop()

    async def render(self, html, out_png, W, H, kind="poster", scale=1, full_page=None, strict=False, name=None):
        pg = await self._b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
        try:
            await pg.set_content(html, wait_until="load")
            await pg.evaluate("async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}")
            issues = await pg.evaluate(GATE_JS, {"kind": kind, "W": W, "H": H})
            os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
            if kind == "poster":
                await pg.locator(".p").screenshot(path=out_png)
            else:
                await pg.screenshot(path=out_png, full_page=True if full_page is None else full_page)
        finally:
            await pg.close()
        res = Result(out_png, issues, W, H)
        tag = name or os.path.basename(out_png)
        for s, m in issues:
            print(f"[{tag}] {'FAIL' if s == 'HARD' else 'note'}: {m}")
        print(f"[{tag}] shikshaq gate: {'CLEAN' if res.clean else str(len(res.hard)) + ' HARD issue(s)'}")
        if strict and not res.clean:
            raise ShikshaqError(f"{tag}: {len(res.hard)} hard gate failure(s); first: {res.hard[0]}")
        return res


async def render(html, out_png, W, H, **kw):
    async with session() as s:
        return await s.render(html, out_png, W, H, **kw)


def render_sync(html, out_png, W, H, **kw):
    return asyncio.run(render(html, out_png, W, H, **kw))


# ═════════════════════════════════════════════════════════════════════════════
# 9. SCAFFOLDS + CLI
# ═════════════════════════════════════════════════════════════════════════════
_SCAFFOLD_POSTER = '''"""{name}: a Shikshaq poster. Generated by `python engine/shikshaq.py scaffold poster {name}`.
Read brain/SHIKSHAQ.md. Every number must be a FACT (sk.FACTS) and the copy passes sk.copy_gate()."""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

W, H = sk.SIZES["feed"]
F = sk.FACTS
P = sk.need("papers")          # asked each time: raises with the question until sk.confirm("papers", N) or SHIKSHAQ_PAPERS=N
headline = [f"{{P}} board papers.", "Free to read."]
errs, warns = sk.copy_gate(headline + ["First 2 questions need no account"])
assert not errs, errs

top = (f'<div style="padding:56px 64px">{{sk.logo(False, 64)}}'
       f'<p class="eyebrow" style="font-size:30px;margin-top:44px">Board exams \\u00b7 ICSE, CBSE, ISC</p>'
       f'<h1 style="font-family:Archivo;font-weight:400;font-size:122px;line-height:1;letter-spacing:-.05em;margin-top:30px;white-space:nowrap">'
       f'{{headline[0]}}<br><b style="font-weight:800;color:var(--orange)" data-accent-display>{{headline[1]}}</b></h1>'
       f'{{sk.sticker("First 2 questions need no account", 5, style="right:56px;top:60px;height:60px;font-size:26px;padding:0 28px")}}</div>')
bottom = '<div style="padding:56px 64px"><p class="eyelab" style="font-size:24px">The boards set</p></div>'
body = sk.poster([("bone", top, 600), ("indigo", bottom, None)], W, H)
html = sk.doc(body, kind="poster", W=W, H=H, title="{name}")
res = sk.render_sync(html, "out/shikshaq/{name}.png", W, H, kind="poster")
print("CLEAN" if res.clean else res.hard)
'''

_SCAFFOLD_PAGE = '''"""{name}: a Shikshaq page. Generated by `python engine/shikshaq.py scaffold page {name}`.
Read brain/SHIKSHAQ.md. A page is a stack of 30px panels that differ by FILL."""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

F = sk.FACTS
body = (sk.nav()
        + sk.hero("Board exams \\u00b7 ICSE, CBSE, ISC", "That paper you keep avoiding?", "Read it today.",
                  counts=[(f"Maths \\u00b7 {{F['subject_teachers']['Maths']}}", "Maths")], quick=["Class 10", "Maths"])
        + sk.stats_section("05", "No commission.", sk.mark("Ever."), "The fee you agree is the fee they keep.",
                           [(F["teachers"], "verified teachers listed", "teachers"), (sk.need("papers"), "past papers, free to read", "papers")])
        + sk.footer("Shikshaq is " + sk.emph("verified teachers") + " in Kolkata.", small="Free to search, free to contact."))
for w, h, tag in ((390, 844, "m"), (1280, 800, "d")):
    html = sk.doc(body, kind="page", title="{name}")
    sk.render_sync(html, f"out/shikshaq/{name}-{{tag}}.png", w, h, kind="page")
'''


def _cli(argv):
    cmd = argv[1] if len(argv) > 1 else "help"
    if cmd == "selftest":
        bad = verify_tokens()
        for b in bad: print("DRIFT", b)
        print("tokens match the vendored site source" if not bad else f"{len(bad)} drifted token(s)")
        return 1 if bad else 0
    if cmd == "css":
        print(tokens_css()); return 0
    if cmd == "facts":
        print(json.dumps(FACTS, indent=1, ensure_ascii=False)); return 0
    if cmd == "scaffold" and len(argv) >= 4:
        kind, name = argv[2], argv[3]
        tpl = {"poster": _SCAFFOLD_POSTER, "page": _SCAFFOLD_PAGE}.get(kind)
        if not tpl:
            print("scaffold poster|page <name>"); return 2
        dest = os.path.join(ROOT, "scratchpad", f"shik_{name}.py")
        io.open(dest, "w", encoding="utf-8").write(tpl.format(name=name))
        print("wrote", os.path.relpath(dest, ROOT)); return 0
    if cmd == "gate" and len(argv) >= 3:
        html = io.open(argv[2], encoding="utf-8").read()
        kind = argv[3] if len(argv) > 3 else "page"
        W, H = SIZES["mobile"] if kind == "page" else SIZES["feed"]
        r = render_sync(html, os.path.join(ROOT, "out", "shikshaq", "_gate.png"), W, H, kind=kind)
        return 0 if r.clean else 1
    print(__doc__.split("HOW TO USE")[-1]); return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
