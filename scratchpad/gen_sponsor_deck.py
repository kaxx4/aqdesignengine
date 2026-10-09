"""SPONSORS DECK, COLD (the master build for the AQ sponsorship + stalls family; user brief 2026-10-09).

Rebuilds the Disco Diwali sponsorship deck from zero: every photo, logo and line of copy was extracted from the user's Figma export
(training_samples/sponsorship_deck/source_export.pdf, git-ignored) and re-laid on ONE scaffold (engine/deckkit.py). The goal was
cohesion, so slides here cannot choose their own ground, heading size, radius or icon family; they only fill the scaffold.

Adaptations / rulings (CLAUDE.md sec 2 rule 4), recorded:
  * Design language: the "softer, cleaner" AQ system the user chose (cream + paper cards + keylines, 28px photo frames), NOT TerraThon.
    TerraThon / Diwali die-cut STICKERS are used sparingly as accents (user: "include just the stickers"), drawn by rever_deck_stickers.py.
  * Charts rebuilt: age pie (4 slices, percentages only), exclusivity funnel (replaces the mixed-unit 'Our Numbers' bar chart), school map
    (vector silhouette + numbered pins + a legend, replacing the unreadable raster).
  * Numbers: 5K+ followers (user ruling; the source screenshot shows 5,019). Projects: 112 in 2025 / 500+ since 2021 (user ruling; the
    source's yearly bars summed to 400 against a 500+ claim, so the bars are gone). The age pie's volunteer slice is 1.5K+ volunteers against
    1,810 survey respondents (user ruling, flagged on the slide as approximate: a volunteer can also be a respondent).
  * Run of show re-sorted chronologically (the source listed 5:30 PM briefing before 4:00 PM DJ setup).
  * Icons: one line-icon set replaces three emoji sets. Past sponsors: logo wall on uniform tiles.
  * Source facts NOT changed without the user: tier benefits, 'Google reviews' counts, 'all days / five days / 15 events' wording. They are
    flagged in brain/SPONSORSHIP_DECKS.md as open items.

Run:  python scratchpad/gen_sponsor_deck.py [slide numbers ...]      ->  out/decks/sponsors_cold/slide_NN.png (+ the PDF when all render)
"""
import asyncio, importlib.util, io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
os.chdir(ROOT)


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


stk = _load("rever_deck_stickers", "scratchpad/rever_deck_stickers.py")
K = _load("deckkit", "engine/deckkit.py")
B = _load("build", "engine/build.py")
core = K.core
from PIL import Image

PRIV = os.path.join(ROOT, "scratchpad", "sponsorship_private")
MAP = json.load(open(os.path.join(PRIV, "map.json")))
FACTS = json.load(open(os.path.join(PRIV, "facts.json"))) if os.path.exists(os.path.join(PRIV, "facts.json")) else {}
OUT = os.path.join(ROOT, "out", "decks", "sponsors_cold")
LABEL = "Disco Diwali 2026  ·  Partnership proposal"
G, BL, LM, INK, MUTE = K.GREEN, K.BLUE, K.LEMON, K.INK, K.MUTE
CREAM = K.CREAM_ON_DARK
TONES = [G, BL, LM]            # the one accent rotation: every repeated element cycles these three, in this order


class Ctx:
    def __init__(self, n=1, total=1): self.n, self.total = n, total


def S(body, head=None, c=None, dark=False, **kw):
    return K.slide(body, head, c.n, c.total, LABEL, dark, **kw)


def ph(i, focus="50% 50%", cap=None, alt="", extra=""):
    cp = f'<div class="cap">{K.esc(cap)}</div>' if cap else ""
    return f'<div class="frame" style="width:100%;height:100%;{extra}">{K.photo(i, focus, alt=alt)}{cp}</div>'


def grid(children, cols, rows=None, gap=24, style=""):
    cols = cols.replace("1fr", "minmax(0,1fr)")          # a bare 1fr is min-content, so wide content blew a column off the canvas
    r = f"grid-template-rows:repeat({rows},minmax(0,1fr));" if rows else ""
    return (f'<div style="display:grid;grid-template-columns:{cols};{r}gap:{gap}px;width:100%;height:100%;{style}">'
            + "".join(children) + "</div>")


def sticker(fn, width, x, y, rot=0, **kw):
    """A TerraThon/Diwali die-cut sticker from rever_deck_stickers.py, placed absolutely (accent only, never carries information)."""
    if fn in (stk.disco_ball, stk.diya, stk.ticket):          # the Diwali ticket-kit builders: fn(size) -> (svg, h)
        svg, h = fn(width, **kw); w = width
    else:                                                     # the Rever kit builders: fn(width=) -> (svg, w, h)
        svg, w, h = fn(width=width, **kw)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:6;'
            f'pointer-events:none">{svg}</div>')




# ═════════════════════════════════════ SLIDES ═════════════════════════════════════
NL = "\n"
INK2 = K.INK2


def bento_photo(items, cols, rows, gap=20):
    """items: [(img, focus, col-span, row-span)] placed in reading order on a grid. Every photo is a K.photo, so the frame is uniform."""
    cells = [f'<div style="grid-column:span {cs};grid-row:span {rs};min-height:0;min-width:0">{ph(i, f)}</div>' for i, f, cs, rs in items]
    return grid(cells, cols, rows, gap)


def photo_story(c, items, cols, rows, caption, tag, tone=G):
    """The ONE photo-slide template: a bento of photos filling the frame, a tag chip top-left and a cream caption card overlapping the
    lower-left. Same on every photo slide, which is what stops 'picture slides' reading as filler."""
    body = (f'<div style="position:relative;width:100%;height:100%">{bento_photo(items, cols, rows)}'
            f'<div style="position:absolute;left:28px;top:28px">{K.chip(tag, tone)}</div>'
            f'<div style="position:absolute;left:28px;bottom:28px;background:{K.BG};border-radius:22px;padding:26px 38px;max-width:880px;'
            f'box-shadow:0 18px 40px -20px rgba(0,0,0,.5)">'
            f'<div style="font:900 62px/.98 var(--d);text-transform:uppercase;letter-spacing:-.01em">{caption}</div></div></div>')
    return S(body, None, c, body_style="margin-top:0")


def s_glance(c):
    facts = [("calendar", "When", "2nd week of November 2026 (tentative)"), ("users", "Who", "School (classes 6-12) and college students"),
             ("ticket", "How many", "600+ guests expected"), ("heart", "Why", "Net proceeds fund AquaTerra\u2019s welfare work")]
    left = K.card("".join(f'<div style="display:flex;align-items:center;gap:22px;padding:20px 0;{"border-top:1.5px solid " + K.LINE + ";" if i else ""}">'
                          f'<span class="disc" style="background:{TONES[i % 3]};color:{core.text_on(TONES[i % 3])}">{K.icon(ic, 30)}</span>'
                          f'<div><div class="mono" style="font-size:14px;color:{K.MUTE}">{k}</div><div style="font:600 30px/1.2 var(--e);margin-top:4px">{v}</div></div></div>'
                          for i, (ic, k, v) in enumerate(facts)), "", "width:760px;padding:18px 40px;display:flex;flex-direction:column;justify-content:center")
    ladder = [("Title sponsor", LM), ("Co-sponsor", BL), ("Associate sponsor", G), ("Education, media and cafe partners", K.PAPER), ("In-kind partners", K.PAPER), ("Stall space at the venue", K.PAPER)]
    rows = "".join(f'<div style="background:{t};color:{core.text_on(t) if t != K.PAPER else K.INK};border:1.5px solid {K.LINE};border-radius:20px;padding:18px 30px;'
                   f'font:900 34px/1 var(--d);text-transform:uppercase;display:flex;justify-content:space-between;align-items:center">{n}{K.icon("arrow", 30, "currentColor", 2.2)}</div>' for n, t in ladder)
    right = f'<div style="flex:1;margin-left:40px;display:flex;flex-direction:column;gap:14px;justify-content:center"><div class="mono" style="font-size:15px;color:{K.MUTE};margin-bottom:6px">Ways to be part of it</div>{rows}</div>'
    return S(left + right, (K.eyebrow("The short version"), K.title("The offer, in *one* page")), c)


def s_proof(c):
    chips = "".join(f'<div style="flex:1;min-width:0">{_poster(e[0])}</div>' for e in [EVENTS[0], EVENTS[1], EVENTS[2], EVENTS[3], EVENTS[4]])
    body = (f'<div style="display:flex;flex-direction:column;width:100%;gap:36px;min-height:0"><div style="display:flex;gap:60px;align-items:flex-end">'
            f'<div><div class="kv" style="font-size:250px;color:{G}">\u20b922.5L+</div><div style="font:600 34px/1.2 var(--e);color:#D8D3C2;margin-top:6px">raised for welfare across five flagship events</div></div>'
            f'<div style="padding-bottom:14px"><div class="kv" style="font-size:120px;color:{LM}">2,850+</div><div style="font:600 30px/1.2 var(--e);color:#D8D3C2;margin-top:6px">guests across the same five</div></div></div>'
            f'<div style="display:flex;gap:18px;width:100%;flex:1;min-height:0;align-items:flex-start">{chips}</div></div>')
    return S(body, (K.eyebrow("The proof", LM),), c, dark=True)


def s_photo_tiers(c):
    return photo_story(c, [(186, "50% 40%", 1, 2), (184, "50% 50%", 2, 1), (178, "50% 50%", 2, 1)], "1fr 1fr 1fr", 2,
                       "Your brand, in the middle of it", "On the night", G)


def s_cover(c):
    t = K.title("Disco" + NL + "*Diwali*", 190)
    left = (f'<div style="display:flex;flex-direction:column;justify-content:center;gap:34px;width:800px">'
            f'{K.eyebrow("Sponsorship & partnership proposal")}{t}'
            f'{K.lede("The flagship Diwali fundraiser from AquaTerra, Kolkata’s student-run NGO. A DJ-led party night where every net rupee goes to welfare work.", 34, 720)}'
            f'<div style="display:flex;gap:14px;flex-wrap:wrap">{K.chip("All for charity", G)}{K.chip("2nd week of Nov 2026 (tentative)", LM)}'
            f'{K.chip_o("600+ guests")}</div></div>')
    right = f'<div style="flex:1;margin-left:64px;position:relative">{ph(148, "50% 38%", alt="Disco Diwali dance floor")}</div>'
    stick = sticker(stk.disco_ball, 200, 1590, 38, 8) + sticker(stk.diya, 170, 830, 130, -8)
    return S(left + right + stick, None, c, body_style="margin-top:0")


def s_about(c):
    kp = grid([K.kpi("5+", "years of active student welfare work", "calendar", G, 80),
               K.kpi("1.5K+", "student volunteers in the community", "users", BL, 80),
               K.kpi("500+", "welfare projects delivered", "heart", LM, 80),
               K.kpi("5K+", "followers on Instagram", "insta", G, 80)], "1fr 1fr", 2, 22)
    left = (f'<div style="width:900px;display:flex;flex-direction:column;gap:30px;min-height:0">'
            f'{K.lede("AquaTerra is a student-run, registered NGO based in Kolkata. We power some of the city’s biggest youth-led fundraising events, and every net rupee goes back into welfare work across the city.", 30)}'
            f'<div style="flex:1;min-height:0">{kp}</div></div>')
    right = f'<div style="flex:1;margin-left:56px">{ph(34, "40% 50%", alt="AquaTerra volunteers at the Diwali photo wall")}</div>'
    return S(left + right, (K.eyebrow("About AquaTerra"), K.title("A student-run NGO that *delivers*")), c)


def s_different(c):
    items = [("eye", "Student run", "Every event is planned and run entirely by student volunteers.", G, 130, "50% 40%"),
             ("heart", "Welfare first", "Net proceeds go directly into funding welfare projects and campaigns.", BL, 156, "50% 40%"),
             ("megaphone", "Visibility", "A night of visibility in front of thousands of Kolkata’s most engaged students.", LM, 126, "50% 35%")]
    cards = []
    for ic, t, d, tone, img, f in items:
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="height:330px;flex:none;position:relative">{K.photo(img, f, r=0)}'
                     f'<span class="disc" style="position:absolute;left:34px;bottom:-30px;background:{tone};color:{core.text_on(tone)};width:84px;height:84px;'
                     f'border:6px solid {K.PAPER}">{K.icon(ic, 38)}</span></div>'
                     f'<div style="padding:58px 40px 34px"><div style="font:900 50px/1 var(--d);text-transform:uppercase;margin-bottom:16px">{t}</div>'
                     f'<div style="font:400 28px/1.35 var(--e);color:{INK2}">{d}</div></div></div>')
    return S(grid(cards, "1fr 1fr 1fr", None, 28), (K.eyebrow("Why AquaTerra"), K.title("What makes us *different*")), c)


def s_vision(c):
    t = ("Five-plus years turning youth energy into real "
         f'<em style="font-family:var(--s);font-style:italic;font-weight:400;text-transform:none;color:{LM}">welfare</em> work across Kolkata.')
    left = (f'<div style="display:flex;flex-direction:column;justify-content:center;gap:44px;width:1060px">'
            f'<div style="font:900 84px/.98 var(--d);text-transform:uppercase;letter-spacing:-.01em">{t}</div>'
            f'<div style="display:flex;gap:14px;flex-wrap:wrap">{K.chip("1.5K+ community", G)}{K.chip("4000+ kids reached", BL, "#fff")}'
            f'{K.chip("80G certified", LM)}{K.chip_o("Darpan registered", dark=True)}</div></div>')
    right = f'<div style="flex:1;margin-left:64px;display:grid;grid-template-rows:1.15fr 1fr;gap:22px;min-height:0">{ph(156, "50% 55%")}{ph(160, "50% 45%")}</div>'
    return S(left + right, (K.eyebrow("Our vision", LM),), c, dark=True)


def s_welfare(c):
    return photo_story(c, [(156, "50% 55%", 2, 2), (158, "50% 30%", 1, 1), (164, "50% 30%", 1, 1)], "1.25fr 1fr 1fr", 2,
                       "Children, welfare and education", "Our work", G)


def s_impact(c):
    data = [("1600+", "doctor check-ups in the Sundarbans", "pulse"), ("3000+", "dogs fed across Kolkata", "paw"),
            ("5K+", "saplings planted by our team", "sprout"), ("2.5T", "of clothes collected in donation drives", "shirt"),
            ("15K+", "bananas distributed in our most recent campaign", "box"), ("4000+", "kids reached across workshops", "users")]
    tiles = [K.kpi(v, l, ic, TONES[i % 3], 120) for i, (v, l, ic) in enumerate(data)]
    return S(grid(tiles, "1fr 1fr 1fr", 2, 26), (K.eyebrow("Impact"), K.title("What five years of *work* adds up to")), c)


def s_growth(c):
    big = lambda v, l, tone: K.card(f'<div class="kv" style="font-size:150px;margin-bottom:12px">{v}</div><div class="kl" style="font-size:28px">{l}</div>',
                                    style=f"background:{tone};border-color:transparent;display:flex;flex-direction:column;justify-content:flex-end;padding:44px 48px")
    left = grid([big("5M+", "impressions across social media and marketing", G), big("5+", "marketing verticals running all year", LM),
                 big("112", "projects completed in 2025 alone", BL), big("500+", "projects since 2021: a five-year record of delivering", G)],
                "1fr 1fr", 2, 24, "width:1040px")
    right = f'<div style="flex:1;margin-left:40px;display:grid;grid-template-rows:1fr 1fr;gap:24px;min-height:0">{ph(188, "50% 35%")}{ph(130, "50% 40%")}</div>'
    return S(left + right, (K.eyebrow("Track record"), K.title("A five-year record of *delivering*")), c)


EVENTS = [  # (poster, name, when, footfall, funds, where)
    ((132, (0, .19, 1, .728)), "The Starry Night", "Dec 2024", "550+", "₹3L", "Sky Turf, DJ Saif Side"),
    ((134, (0, .19, 1, .728)), "Disco Diwali", "Oct 2024", "350+", "₹1.7L", "Orbit Crystal"),
    (136, "Paradox 3.0", "Third edition", "1000+", "₹8.9L", "VS Arena, Battleground, Desi Lane Esplanade"),
    ((138, (0, .19, 1, .728)), "The AQ Punjabi Night", "Jun 2025", "400+", "₹2.2L", "60 Chowringhee, DJ Omar"),
    ((142, (0, .19, 1, .728)), "Starry Night 2.0", "Dec 2025", "550+", "₹6.7L", "Sky Turf, DJ Rajiv"),
    ((146, (0, .095, 1, .865)), "Summer Sunset", "Jun 2026", "500+", None, "60 Chowringhee Banquet"),
]


def _poster(p):
    src = K.crop_uri(p[0], p[1]) if isinstance(p, tuple) else K.uri(K.asset(p))
    return (f'<div style="width:100%;aspect-ratio:4/5;background-image:url({src});background-size:cover;background-position:50% 20%;'
            f'border-radius:16px;box-shadow:0 0 0 1.5px {K.LINE}"></div>')


def s_events(c):
    cards = []
    for p, name, when, foot, funds, where in EVENTS:
        stat = lambda v, l: (f'<div><div class="kv" style="font-size:42px">{v}</div><div class="mono" style="font-size:13px;color:{K.MUTE};margin-top:6px">{l}</div></div>')
        stats = f'<div style="display:flex;gap:18px;margin:16px 0 14px">{stat(foot, "footfall")}{stat(funds, "raised") if funds else ""}</div>'
        cards.append(K.card(f'<div style="display:flex;gap:24px;height:100%;align-items:center"><div style="width:210px;flex:none">{_poster(p)}</div>'
                            f'<div style="display:flex;flex-direction:column;justify-content:center;min-width:0">'
                            f'<div class="mono" style="font-size:14px;color:{K.MUTE}">{when}</div>'
                            f'<div style="font:900 32px/1 var(--d);text-transform:uppercase;margin-top:8px">{K.esc(name)}</div>{stats}'
                            f'<div style="font:400 21px/1.3 var(--e);color:{INK2}">{K.esc(where)}</div></div></div>', style="padding:20px 24px"))
    return S(grid(cards, "1fr 1fr 1fr", 2, 24), (K.eyebrow("Prominent past events"), K.title("Events people *show up* for")), c)


LOGOS = [(84, 0), (66, 0), (70, 0), (68, 0), (80, 0), (82, 0), (72, 0), (74, 0), (76, 0), (78, 0), (86, 0), (110, 0), (88, 0), (90, 0),
         (92, 0), (96, 1), (98, 0), (100, 0), (104, 0), (108, 0), (112, 0), (106, 0), (56, 1), (60, 0),
         ("logo_yrs.png", 0), ("logo_cross.png", 0), ("logo_police.png", 0), ("logo_heritage.png", 0), ("logo_dillilane.png", 0), ("logo_kanxshkag.png", 0)]


def s_sponsors(c):
    tiles = []
    for a, dk in LOGOS:
        bg = "#16181C" if dk else K.PAPER
        blend = "" if dk else "mix-blend-mode:multiply;"
        tiles.append(f'<div style="background:{bg};border:1.5px solid {K.LINE};border-radius:20px;display:flex;align-items:center;justify-content:center;padding:20px 26px;overflow:hidden">'
                     f'<img src="{K.logo_uri(a, flat=not dk)}" style="max-width:100%;max-height:100%;object-fit:contain;{blend}" alt=""></div>')
    return S(grid(tiles, "repeat(6,1fr)", 5, 16), (K.eyebrow("Trusted by"), K.title("Past *sponsors*")), c)


QUOTES = [(76, "Delivered exactly what they had promised to perfection."),
          (66, "It was a wonderful experience partnering with AquaTerra. The team was enthusiastic, organised, and professional."),
          (112, "We loved being a part of AquaTerra’s initiative. Their energy and dedication really stood out."),
          (106, "AquaTerra creates a great platform for young people to explore, connect, and create. Proud to support their work."),
          (72, "AquaTerra is doing great work by bringing young people together for meaningful initiatives. We’re happy to support them.")]


def s_feedback(c):
    def q(i, text, size, dark=False, big=False):
        mark = f'<div style="font:900 {120 if big else 80}px/.7 var(--d);color:{G if dark else K.GREEN_D}">“</div>'
        return K.card(f'{mark}<div style="font:{"900" if big else "600"} {size}px/1.22 var({"--d" if big else "--e"});{"text-transform:uppercase;" if big else ""}margin-top:12px;flex:1">{K.esc(text)}</div>'
                      f'<div style="height:64px;display:flex;align-items:center"><div style="background:#fff;border:1.5px solid {K.LINE};border-radius:14px;padding:8px 18px;height:60px;display:flex;align-items:center">'
                      f'<img src="{K.logo_uri(i, flat=True)}" style="max-height:40px;max-width:200px;mix-blend-mode:multiply" alt=""></div></div>',
                      "q", f"display:flex;flex-direction:column;{'padding:46px 52px;' if big else 'padding:28px 32px;'}", dark=dark)
    hero = q(*QUOTES[0], 60, True, True)
    small = grid([q(i, t, 27) for i, t in QUOTES[1:]], "1fr 1fr", 2, 22)
    return S(grid([hero, small], "0.8fr 1.5fr", None, 24), (K.eyebrow("Feedback from past sponsors"), K.title("In their *words*")), c)


def s_photo_energy(c):
    return photo_story(c, [(148, "50% 40%", 2, 2), (126, "50% 40%", 1, 1), (194, "50% 40%", 1, 1)], "1.4fr 1fr 1fr", 2,
                       "The party the city talks about", "Disco Diwali", LM)


def s_flagship(c):
    feats = [("Food and sales stalls", 182, G), ("A traditional Diwali event", 184, LM), ("The party: a DJ-led night", 188, BL), ("Cash prizes and surprise gifts", 198, G)]
    cards = [f'<div class="card dk" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column"><div style="flex:1;min-height:0">{K.photo(img, "50% 40%", r=0)}</div>'
             f'<div style="padding:22px 28px;display:flex;align-items:center;gap:16px"><span style="width:16px;height:16px;border-radius:50%;background:{t};flex:none"></span>'
             f'<div style="font:900 34px/1.02 var(--d);text-transform:uppercase">{n}</div></div></div>' for n, img, t in feats]
    left = (f'<div style="width:620px;display:flex;flex-direction:column;justify-content:space-between;min-height:0">'
            f'<div><div class="kv" style="font-size:230px;color:{G}">600+</div><div style="font:600 34px/1.2 var(--e);color:#D8D3C2;margin-top:8px">attendees at the Disco Diwali party</div></div>'
            f'<div class="card dk" style="padding:24px 30px;display:flex;flex-direction:column;gap:18px">'
            f'<div><div class="mono" style="font-size:14px;color:#A7A292">Tentative date</div><div style="font:900 36px/1 var(--d);text-transform:uppercase;margin-top:8px">2nd week of November 2026</div></div>'
            f'<div style="border-top:1.5px solid rgba(244,239,224,.14);padding-top:18px"><div class="mono" style="font-size:14px;color:#A7A292">Target market</div><div style="font:900 36px/1 var(--d);text-transform:uppercase;margin-top:8px">School (classes 6-12) and college students</div></div></div></div>')
    right = f'<div style="flex:1;margin-left:48px;min-height:0">{grid(cards, "1fr 1fr", 2, 22)}</div>'
    return S(left + right, (K.eyebrow("The flagship", LM), K.title("One night, *four* reasons")), c, dark=True)


def s_demo(c):
    counts = [("Class 9-10", "14-16 years", 525, G), ("Class 11-12", "16-18 years", 820, BL), ("College", "18+ years", 465, LM)]
    tot = sum(v for _, _, v, _ in counts)
    sl = [(n, 100 * v / tot, col) for n, _, v, col in counts]
    pct = [round(p) for _, p, _ in sl]; assert sum(pct) == 100, pct
    legend = "".join(
        f'<div class="card" data-tag="card" style="display:flex;align-items:center;gap:22px;padding:24px 30px"><span style="width:28px;height:28px;border-radius:50%;background:{col};flex:none"></span>'
        f'<div style="flex:1"><div style="font:900 40px/1 var(--d);text-transform:uppercase">{n}</div><div class="mono" style="font-size:15px;color:{K.MUTE};margin-top:8px">{sub}</div></div>'
        f'<div class="kv" style="font-size:72px">{p}%</div></div>' for (n, sub, v, col), p in zip(counts, pct))
    vol = K.card(f'<span class="disc" style="background:{K.INK};color:{K.CREAM_ON_DARK}">{K.icon("users", 30)}</span>'
                 f'<div><div class="kv" style="font-size:72px">1.5K+</div><div class="kl">active volunteers in the AQ network, on top of the audience</div></div>', "kpi", "padding:26px 30px;flex-direction:row;align-items:center;justify-content:flex-start;gap:26px")
    note = f'<div style="font:400 20px/1.35 var(--e);color:{K.MUTE}">Age split of 1,810 survey respondents across Classes 9-12 and college.</div>'
    pie = K.donut([(n, p, col) for (n, p, col) in sl], 700, 350)
    left = f'<div style="width:760px;display:flex;align-items:center;justify-content:center">{pie}</div>'
    right = f'<div style="flex:1;display:flex;flex-direction:column;gap:18px;justify-content:center">{legend}{vol}{note}</div>'
    return S(left + right, (K.eyebrow("Demographics"), K.title("Who is in the *room*")), c)


def s_map(c):
    pins = MAP["pins"]
    half = (len(pins) + 1) // 2
    col = lambda ps: "".join(
        f'<div style="display:flex;align-items:center;gap:16px;height:54px"><span style="width:42px;height:42px;border-radius:50%;background:{G};border:2.5px solid {INK};'
        f'display:flex;align-items:center;justify-content:center;font:900 22px var(--d);flex:none">{p["n"]}</span>'
        f'<span style="font:600 25px/1.1 var(--e)">{K.esc(p["name"])}</span></div>' for p in ps)
    left = (f'<div style="flex:1;display:flex;flex-direction:column;gap:30px;min-height:0">'
            f'{K.lede("Students from DBPC, La Martiniere for Boys, La Martiniere for Girls, Modern High, Loreto and other leading Kolkata schools make up the AQ community. Disco Diwali is where that community comes together, and it grows every year.", 29)}'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:24px;align-content:start">{col(pins[:half])}{col(pins[half:])}</div></div>')
    right = f'<div style="width:660px;display:flex;justify-content:center;margin-left:40px">{K.map_svg(MAP, 740)}</div>'
    return S(left + right, (K.eyebrow("Reach"), K.title("Where our *schools* are")), c)


def s_reach(c):
    T = [("Instagram", "5K+", "followers", "insta", G), ("Instagram", "4.3L", "views in a recent 30 days", "eye", BL),
         ("Instagram", "21.7K", "views on the Summer Sunset post", "trend", LM), ("Instagram", "9.3K", "views on the Paradox 2026 post", "trend", G),
         ("WhatsApp", "3,162", "members across 4 community groups", "users", BL), ("Student database", "2000+", "student contacts we can reach directly", "mail", LM),
         ("Schools", "18", "leading Kolkata schools in our network", "school", G), ("All channels", "5M+", "impressions across social media and marketing", "megaphone", BL)]
    cards = [K.card(f'<div style="display:flex;align-items:center;gap:14px"><span class="disc" style="background:{tone};color:{core.text_on(tone)};width:54px;height:54px">{K.icon(ic, 26)}</span>'
                    f'<span class="mono" style="font-size:15px;color:#A7A292">{ch}</span></div>'
                    f'<div><div class="kv" style="font-size:92px;color:{CREAM}">{v}</div><div class="kl" style="font-size:24px">{lab}</div></div>', "kpi", "padding:28px 32px", dark=True)
             for ch, v, lab, ic, tone in T]
    return S(grid(cards, "repeat(4,1fr)", 2, 22), (K.eyebrow("Reach", LM), K.title("Numbers, *by touchpoint*")), c, dark=True)


def s_promote(c):
    ch = [("users", "School networks and groups", "Class and school networks across Kolkata, reached directly and through our volunteers.", G, 158),
          ("insta", "Instagram reels and posts", "A year-round content engine: reels, posts and stories, with our event pages and partner collabs.", BL, 188),
          ("megaphone", "Website and offline marketing", "The website, plus marketing stunts and events that put Disco Diwali in front of students before the poster does.", LM, 178)]
    cards = []
    for ic, t, d, tone, img in ch:
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="height:300px;flex:none;position:relative">{K.photo(img, "50% 40%", r=0)}'
                     f'<span class="disc" style="position:absolute;left:34px;bottom:-30px;background:{tone};color:{core.text_on(tone)};width:84px;height:84px;border:6px solid {K.PAPER}">{K.icon(ic, 38)}</span></div>'
                     f'<div style="padding:58px 40px 34px"><div style="font:900 44px/1.02 var(--d);text-transform:uppercase;margin-bottom:16px">{t}</div>'
                     f'<div style="font:400 27px/1.35 var(--e);color:{INK2}">{d}</div></div></div>')
    return S(grid(cards, "1fr 1fr 1fr", None, 28), (K.eyebrow("Promotion"), K.title("How we *promote*")), c)


WA = [("Community AquaTerra (1/2)", 847), ("Community AquaTerra (2/2)", 746), ("Summer Sunset | Paradox 2026", 822), ("Paradox 2026 | @ngo.aquaterra", 747)]


def s_social(c):
    ig = K.crop_uri(166, (.30, .05, .97, .27))
    rows = "".join(f'<div style="display:flex;align-items:center;justify-content:space-between;gap:20px;padding:15px 0;border-top:1.5px solid {K.LINE}">'
                   f'<span style="font:600 25px var(--e)">{K.esc(n)}</span><span class="kv" style="font-size:40px">{m}</span></div>' for n, m in WA)
    wa = K.card(f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:12px"><span class="disc" style="background:{LM};color:{INK}">{K.icon("users", 30)}</span>'
                f'<div><div style="font:900 34px/1 var(--d);text-transform:uppercase">WhatsApp communities</div>'
                f'<div class="mono" style="font-size:14px;color:{K.MUTE};margin-top:6px">Members per group, {sum(m for _, m in WA):,} in total</div></div></div>{rows}', "", "flex:1;padding:28px 34px")
    left = (f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:24px;min-height:0">'
            f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;height:300px">{K.kpi("5K+", "followers on Instagram", "insta", G, 100)}{K.kpi("4.3L", "Instagram views in a recent 30 days", "eye", BL, 100)}</div>{wa}</div>')
    right = (f'<div style="width:640px;margin-left:48px;display:flex;flex-direction:column;justify-content:center;gap:16px;min-height:0">'
             f'<div class="mono" style="font-size:14px;color:{K.MUTE}">Our Instagram profile</div>'
             f'<div style="width:100%;aspect-ratio:480/171;background:url({ig}) center/cover;border-radius:24px;box-shadow:0 0 0 1.5px {K.LINE},0 24px 40px -26px rgba(0,0,0,.5)"></div>'
             f'{ph(194, "50% 40%")}</div>')
    return S(left + right, (K.eyebrow("Presence"), K.title("Where the *audience* already is")), c)


def s_offline(c):
    t = K.crop_uri(176, (0, 0, 1, .5), 1400); p = K.crop_uri(176, (0, .5, 1, 1), 1400)
    ph_u = lambda src, f="50% 50%": f'<div class="ph" style="background-image:url({src});background-position:{f};border-radius:{K.R_FRAME}px"></div>'
    items = [ph_u(t), K.photo(178, "50% 40%"), ph_u(p, "50% 40%")]
    left = (f'<div style="width:520px;display:flex;flex-direction:column;gap:24px;justify-content:center">'
            f'{K.lede("The party is the finale. In the weeks before it we are on the ground: school visits, stalls and pop-up stunts that turn students into guests, and guests into your audience.", 29)}'
            f'<ul class="ck">{"".join(f"<li>{K.icon(i, 30, K.GREEN_D)}<span>{t_}</span></li>" for i, t_ in [("school", "School visits and class networks"), ("store", "Pop-up stalls and brand activations"), ("megaphone", "Marketing stunts and events")])}</ul></div>')
    right = f'<div style="flex:1;margin-left:48px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:22px;min-height:0">' \
            f'<div style="grid-row:span 2">{items[1]}</div>{items[0]}{items[2]}</div>'
    return S(left + right, (K.eyebrow("Offline engagement"), K.title("We are on the *ground* too")), c)


RUN = [("1:00 PM", "Decor and venue setup", 184), ("3:00 PM", "Stall setup", 182), ("4:00 PM", "DJ and sound setup", 188), ("5:30 PM", "Team and vendor briefing", 130),
       ("6:30 PM", "Registrations open, stalls go live", 190), ("7:45 PM", "Dhol entry and opening", 192), ("8:00 - 10:30 PM", "DJ set: peak hours", 194), ("10:30 PM", "Closing moment", 148)]


def s_run(c):
    cards = []
    for i, (t, n, img) in enumerate(RUN):
        tone = TONES[i % 3]
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="flex:1;min-height:0;position:relative">{K.photo(img, "50% 40%", r=0)}'
                     f'<div style="position:absolute;left:18px;top:18px">{K.chip(t, tone, size=20)}</div></div>'
                     f'<div style="padding:20px 26px 24px;font:900 30px/1.02 var(--d);text-transform:uppercase;min-height:104px">{n}</div></div>')
    return S(grid(cards, "repeat(4,1fr)", 2, 22), (K.eyebrow("Run of show"), K.title("The day, *hour* by hour")), c)


def s_photo_night(c):
    return photo_story(c, [(34, "50% 50%", 1, 1), (192, "50% 30%", 2, 2), (184, "50% 50%", 1, 1)], "1fr 1.4fr 1fr", 2,
                       "Every corner worth a photo", "On the night", BL)


def s_why(c):
    why = [("users", "Unique audience", "Access to a hard-to-reach youth demographic, with indirect reach into their parent and family networks.", G),
           ("heart", "Welfare motive", "All proceeds are directed towards charity.", BL),
           ("megaphone", "Brand awareness", "Placement across signage, content and take-home merchandise that lasts beyond the event.", LM),
           ("eye", "Visibility", "In front of thousands of Kolkata’s most engaged students, in one night.", G)]
    cards = [K.card(f'<span class="disc" style="background:{t};color:{core.text_on(t)}">{K.icon(ic, 30)}</span>'
                    f'<div style="flex:none"><div style="font:900 38px/1 var(--d);text-transform:uppercase;margin-bottom:14px;min-height:76px;display:flex;align-items:flex-end">{n}</div><div style="font:400 27px/1.3 var(--e);color:{INK2}">{d}</div></div>',
                    "kpi", "padding:30px 34px") for ic, n, d, t in why]
    left = f'<div style="width:1000px">{grid(cards, "1fr 1fr", 2, 22)}</div>'
    right = (f'<div style="flex:1;margin-left:44px;display:grid;grid-template-rows:1.25fr 1fr;gap:22px;min-height:0">'
             f'<div class="card" style="padding:18px;display:flex;align-items:center;justify-content:center;min-height:0"><img src="{K.uri(K.asset(204))}" style="max-height:100%;max-width:100%;border-radius:14px" alt=""><div class="mono" style="font-size:13px;color:{K.MUTE};margin-left:18px;width:120px">Your logo on the standee</div></div>'
             f'<div class="card" style="padding:18px;display:flex;align-items:center;justify-content:center;min-height:0"><img src="{K.uri(K.asset(206))}" style="max-height:100%;max-width:70%;border-radius:14px" alt=""><div class="mono" style="font-size:13px;color:{K.MUTE};margin-left:18px;width:110px">Your logo on thank-you cards</div></div></div>')
    return S(left + right, (K.eyebrow("The fit"), K.title("Why this fits *you*")), c)


def _node(x, y, w, h, title_, sub, tone, big=False):
    fg = core.text_on(tone) if tone not in (K.INK,) else K.CREAM_ON_DARK
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{tone};color:{fg};border-radius:24px;padding:0 28px;'
            f'display:flex;flex-direction:column;justify-content:center;box-shadow:0 18px 34px -24px rgba(10,10,10,.5)">'
            f'<div style="font:900 {44 if big else 34}px/1 var(--d);text-transform:uppercase">{title_}</div>'
            f'{f"<div class=mono style=font-size:15px;margin-top:10px;opacity:.75>{sub}</div>" if sub else ""}</div>')


def s_tiers(c):
    nodes = [("root", 0, 270, 340, 140, "Disco Diwali", "The event", K.INK, True),
             ("title", 460, 60, 390, 140, "Title sponsor", "Powered by", LM, True),
             ("co", 460, 400, 390, 140, "Co-sponsor", "Second billing", BL, True),
             ("assoc", 960, 270, 360, 124, "Associate sponsor", "Visible partner", G, False),
             ("media", 960, 520, 360, 124, "Media sponsor", "Content partner", G, False),
             ("hyd", 1420, 70, 308, 104, "Hydration", "Category sponsor", K.PAPER, False),
             ("cafe", 1420, 280, 308, 104, "Cafe", "Category sponsor", K.PAPER, False),
             ("fash", 1420, 490, 308, 104, "Fashion", "Category sponsor", K.PAPER, False)]
    pos = {n[0]: n for n in nodes}
    link = lambda a, b: (f'M{pos[a][1] + pos[a][3]},{pos[a][2] + pos[a][4] / 2} C{pos[a][1] + pos[a][3] + 70},{pos[a][2] + pos[a][4] / 2} '
                         f'{pos[b][1] - 70},{pos[b][2] + pos[b][4] / 2} {pos[b][1]},{pos[b][2] + pos[b][4] / 2}')
    paths = "".join(f'<path d="{link(a, b)}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" opacity=".55"/>'
                    for a, b in [("root", "title"), ("root", "co"), ("co", "assoc"), ("co", "media"), ("assoc", "hyd"), ("assoc", "cafe"), ("assoc", "fash")])
    html = "".join(_node(x, y, w, h, t, sb, tone, big) for _, x, y, w, h, t, sb, tone, big in nodes)
    note = (f'<div style="position:absolute;left:1420px;top:630px;width:308px;font:400 22px/1.3 var(--e);color:{K.MUTE}">Partner and in-kind offerings sit alongside these tiers.</div>')
    body = f'<div style="position:relative;width:1728px;height:100%"><svg width="1728" height="720" style="position:absolute;left:0;top:0">{paths}</svg>{html}{note}</div>'
    return S(body, (K.eyebrow("Sponsorship"), K.title("Disco Diwali sponsorship *tiers*")), c)


def _check_list(items, dark=False, big=False):
    fs = "font-size:25px;" if big else ""
    return f'<ul class="ck" style="{fs}gap:{13 if big else 12}px">' + "".join(f"<li style='{fs}'>{K.icon('check', 26, K.GREEN_D if not dark else G, 2.4)}<span>{K.esc(i)}</span></li>" for i in items) + "</ul>"


TIER = [("Title sponsor", "Powered by", LM, ["Exclusive standee spots on the night", "Logo on creatives and banners", "30+ stories and interactions", "60+ Google reviews", "Grid of 3 exclusive Instagram posts", "Chief guest speaker slot", "Emcee mentions through the night", "Stall space at the event"]),
        ("Co-sponsor", "Second billing", BL, ["Exclusive standee spots on the night", "Logo on creatives and banners", "20+ stories and interactions", "55+ Google reviews", "1 exclusive Instagram post", "Emcee mentions through the night", "Stall space at the event"]),
        ("Associate sponsor", "Visible partner", G, ["Standees at the event", "Logo on creatives and banners", "5+ stories and interactions", "30+ online reviews", "Stall space at the event"])]


def s_tiers_glance(c):
    pics = [(148, "50% 40%"), (194, "50% 40%"), (188, "50% 35%")]
    cards = [K.card(f'<div>{K.chip(n, t, size=24)}<div class="mono" style="font-size:14px;color:{K.MUTE};margin:16px 0 22px">{sub}</div></div>'
                    f'<div>{_check_list(it, big=True)}</div><div style="flex:1;min-height:110px;margin-top:22px">{ph(*pics[i])}</div>',
                    "", "display:flex;flex-direction:column;padding:34px 36px") for i, (n, sub, t, it) in enumerate(TIER)]
    return S(grid(cards, "1fr 1fr 1fr", None, 24), (K.eyebrow("Sponsorship offerings"), K.title("What each tier *includes*")), c)


def s_matrix(c):
    rows = [("Standee spots", "Exclusive, on the night", "Exclusive, on the night", "At the event"), ("Logo on creatives and banners", 1, 1, 1),
            ("Stories and interactions", "30+", "20+", "5+"), ("Online reviews", "60+ Google", "55+ Google", "30+ online"),
            ("Story reshares", "25+", 0, 0), ("Content on your standees and products", 1, 1, 0), ("Instagram feature", "Grid of 3 posts", "1 post", 0),
            ("Chief guest speaker", 1, 0, 0), ("Emcee mentions through the night", 1, 1, 0), ("Stall space at the event", 1, 1, 1), ("Coupons, cards and samples", 1, 1, 0)]
    cell = lambda v: (K.icon("check", 30, K.GREEN_D, 2.6) if v == 1 else (f'<span style="color:{K.MUTE};font:600 24px var(--e)">—</span>' if v == 0 else f'<span style="font:600 24px var(--e)">{K.esc(v)}</span>'))
    head = "".join(f'<div style="display:flex;justify-content:center">{K.chip(n, t, size=22)}</div>' for n, _, t, _ in TIER)
    body = "".join(f'<div style="display:contents"><div style="font:600 24px var(--e);padding:0 4px">{K.esc(r[0])}</div>'
                   + "".join(f'<div style="display:flex;justify-content:center;align-items:center">{cell(v)}</div>' for v in r[1:]) + '</div>' for r in rows)
    sep = "".join(f'<div style="position:absolute;left:0;right:0;top:{70 + i * 56}px;height:1.5px;background:{K.LINE}"></div>' for i in range(len(rows) + 1))
    table = (f'<div class="card" data-tag="card" style="width:100%;padding:24px 40px;position:relative"><div style="position:relative"><div style="display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;align-items:center;'
             f'grid-auto-rows:56px;grid-template-rows:70px;"><div></div>{head}{body}</div>{sep}</div></div>')
    return S(table, (K.eyebrow("Sponsorship offerings"), K.title("Tiers, *side* by side")), c)


def s_partners(c):
    P = [("Education partner", "book", G, ["Promotional standees at the venue", "Logo on creatives and banners", "5+ stories and interactions", "25+ Google reviews", "Exclusive Instagram post", "Webinar promotion on WhatsApp", "25+ story reshares", "Coupons and business cards"]),
         ("Media partner", "news", BL, ["Designated stall space at the venue", "Logo on creatives and banners", "Reel made for you, at your store or the event", "5+ stories and interactions", "Your e-commerce link shared with a 2000+ student database", "30+ online reviews", "Offer coupons and business cards"]),
         ("Cafe partner", "coffee", LM, ["Designated stall space at the venue", "Logo on creatives and banners", "Reel made for you, at your cafe or the event", "5+ stories and interactions", "Your link shared with a 2000+ student database", "45+ Zomato and Swiggy reviews", "20+ Google reviews", "Offer coupons and pamphlets"])]
    cards = []
    PICS = [(160, "50% 40%"), (188, "50% 35%"), (182, "50% 45%")]
    for (n, ic, t, it), pic in zip(P, PICS):
        icon_name = {"book": "school"}.get(ic, ic)
        cards.append(K.card(f'<div style="display:flex;align-items:center;gap:16px"><span class="disc" style="background:{t};color:{core.text_on(t)}">{K.icon(icon_name, 30)}</span>'
                            f'<div style="font:900 31px/1 var(--d);text-transform:uppercase;white-space:nowrap">{n}</div></div><div style="margin-top:26px">{_check_list(it, big=True)}</div>'
                            f'<div style="flex:1;min-height:110px;margin-top:20px">{ph(*pic)}</div>',
                            "", "display:flex;flex-direction:column;padding:32px 34px"))
    return S(grid(cards, "1fr 1fr 1fr", None, 24), (K.eyebrow("Partnership offerings"), K.title("Education, media and *cafe* partners")), c)


def s_inkind(c):
    P = [("Media", "news", G, ["Logo on creatives and banners", "Social media collaborations", "50+ Google and social reviews"]),
         ("Food", "utensils", BL, ["Logo on creatives and banners", "50+ Zomato and Swiggy reviews"]),
         ("Stationery", "pencil", LM, ["Logo on creatives and banners", "10+ stories and interactions"]),
         ("Gift", "gift", G, ["Logo on creatives and banners", "10+ stories and interactions", "Samples gifted to all winners"])]
    cards = [K.card(f'<span class="disc" style="background:{t};color:{core.text_on(t)};width:92px;height:92px;flex:none">{K.icon(ic, 44)}</span>'
                    f'<div style="flex:1"><div style="font:900 46px/1 var(--d);text-transform:uppercase;margin-bottom:18px">{n}</div>{_check_list(it, big=True)}</div>',
                    "", "display:flex;align-items:center;gap:34px;padding:34px 44px") for n, ic, t, it in P]
    return S(grid(cards, "1fr 1fr", 2, 24), (K.eyebrow("In-kind"), K.title("Other in-kind *partnerships*")), c)


def s_stalls(c):
    ben = [("pin", "Spots we know you’ll love"), ("wand", "Basic amenities and support"), ("megaphone", "Dedicated shoutouts"), ("store", "Ample stall space"),
           ("users", "Connect directly with your audience"), ("target", "Benefit from high footfall at the event"), ("eye", "Showcase your brand to a real audience"), ("trend", "Gain exposure on your social pages")]
    tiles = [K.card(f'<span class="disc" style="background:{TONES[i % 3]};color:{core.text_on(TONES[i % 3])};width:64px;height:64px">{K.icon(ic, 30)}</span>'
                    f'<div style="font:600 25px/1.2 var(--e)">{t}</div>', "", "display:flex;align-items:center;gap:20px;padding:18px 26px") for i, (ic, t) in enumerate(ben)]
    left = f'<div style="width:640px;display:grid;grid-template-rows:1.1fr 1fr 1fr;gap:20px;min-height:0">{ph(182, "50% 45%")}{ph(186, "50% 35%")}{ph(178, "50% 50%")}</div>'
    right = f'<div style="flex:1;margin-left:40px;min-height:0">{grid(tiles, "1fr 1fr", 4, 18)}</div>'
    return S(left + right, (K.eyebrow("Stall space"), K.title("Stall space at the *location*")), c)


def s_join(c):
    strips = [226, 188, 230, 148, 192]
    cells = [f'<div style="min-height:0">{ph(i, "50% 50%")}</div>' for i in strips]
    body = (f'<div style="position:relative;width:100%;height:100%">{grid(cells, "repeat(5,1fr)", None, 18)}'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:{G};color:{INK};border-radius:80px;padding:40px 96px;'
            f'box-shadow:0 30px 60px -30px rgba(0,0,0,.6)"><div style="font:900 190px/.9 var(--d);text-transform:uppercase;text-align:center">Join<br>us</div></div></div>')
    return S(body, None, c, body_style="margin-top:0")


def s_close(c):
    ct, rg = FACTS.get("contact", {}), FACTS.get("reg", {})
    qr = K.uri("../terrathon/qr_instagram_ngo_aquaterra.svg")
    row = lambda ic, t: f'<div style="display:flex;align-items:center;gap:20px;font:600 32px var(--e)">{K.icon(ic, 36, K.GREEN_D)}<span>{K.esc(t)}</span></div>'
    photo_c = f'<div style="width:520px;flex:none">{ph(226, "50% 50%")}</div>'
    touch = K.card(f'<div class="mono" style="font-size:15px;color:{K.MUTE};margin-bottom:22px">Get in touch</div>'
                   f'<div style="font:900 78px/.95 var(--d);text-transform:uppercase;margin-bottom:34px">{K.esc(ct.get("name", ""))}</div>'
                   f'<div style="display:flex;flex-direction:column;gap:22px">{row("phone", ct.get("phone", ""))}{row("insta", ct.get("insta", ""))}{row("globe", ct.get("web", ""))}{row("mail", ct.get("mail", ""))}</div>',
                   "", "padding:44px 52px;flex:1;display:flex;flex-direction:column;justify-content:center")
    reg = K.card(f'<div class="mono" style="font-size:15px;color:{K.MUTE};margin-bottom:18px">Registration</div>'
                 f'<div style="display:flex;flex-direction:column;gap:14px;align-items:flex-start">{K.chip(rg.get("tax", "80G certified"), G, size=26)}'
                 f'{K.chip("Registration no. " + rg.get("darpan", ""), BL, "#fff", 24)}'
                 f'<div style="font:400 23px/1.3 var(--e);color:{INK2}">{K.esc(rg.get("trust", ""))}. {K.esc(rg.get("csr", ""))}.</div></div>', "", "padding:30px 34px")
    qrc = K.card(f'<img src="{qr}" style="width:150px;border-radius:10px;flex:none" alt="QR code for @ngo.aquaterra"><div><div style="font:900 34px/1 var(--d);text-transform:uppercase">Follow the work</div>'
                 f'<div class="mono" style="font-size:14px;color:{K.MUTE};margin-top:10px">@ngo.aquaterra</div></div>', "", "padding:24px 30px;display:flex;align-items:center;gap:24px")
    body = f'<div style="display:flex;gap:24px;width:100%;min-height:0">{photo_c}{touch}<div style="width:520px;display:flex;flex-direction:column;gap:24px">{reg}{qrc}</div></div>'
    return S(body, (K.eyebrow("Let\u2019s talk"), K.title("Get in *touch*")), c)


# ═════════════════════════════════════ BUILD ═════════════════════════════════════
ORDER = [s_cover, s_about, s_glance, s_different, s_vision, s_welfare, s_impact, s_growth, s_events, s_proof, s_sponsors, s_feedback,
         s_photo_energy, s_flagship, s_demo, s_map, s_reach, s_promote, s_offline, s_run, s_photo_night,
         s_why, s_tiers, s_photo_tiers, s_matrix, s_partners, s_inkind, s_stalls, s_join, s_close]


async def main(which):
    os.makedirs(OUT, exist_ok=True)
    total = len(ORDER)
    async with B.session(scale=1):
        for i in which:
            html = ORDER[i - 1](Ctx(i, total))
            await B.render(html, f"{OUT}/slide_{i:02d}.png", K.W, K.H, page_bg=K.BG)
    if len(which) == total:
        pages = [Image.open(f"{OUT}/slide_{n:02d}.png").convert("RGB") for n in range(1, total + 1)]
        pages[0].save(f"{OUT}/sponsors_cold.pdf", save_all=True, append_images=pages[1:], resolution=96, quality=90)
        print("pdf written", total, "pages")


def text_dump():
    """Every slide's copy as plain text (for persona review and copy checks): out/decks/sponsors_cold/deck_text.md"""
    import re as _re
    out = []
    for i, fn in enumerate(ORDER, 1):
        h = fn(Ctx(i, len(ORDER)))
        h = _re.sub(r"<style.*?</style>", "", h, flags=_re.S); h = _re.sub(r"<svg.*?</svg>", lambda m: " ".join(_re.findall(r">([^<>]{1,40})<", m.group(0))) + " ", h, flags=_re.S)
        h = _re.sub(r"<(br|/div|/li|/h1|/p|/section)[^>]*>", "\n", h); h = _re.sub(r"<[^>]+>", " ", h)
        import html as _h
        lines = [_re.sub(r"\s+", " ", _h.unescape(x)).strip() for x in h.split("\n")]
        out.append(f"## Slide {i}\n" + "\n".join(x for x in lines if x))
    os.makedirs(OUT, exist_ok=True)
    open(f"{OUT}/deck_text.md", "w").write("\n\n".join(out)); print("text written")


if __name__ == "__main__":
    if sys.argv[1:] == ["--text"]:
        text_dump(); sys.exit()
    which = [int(a) for a in sys.argv[1:]] or list(range(1, len(ORDER) + 1))
    asyncio.run(main(which))
