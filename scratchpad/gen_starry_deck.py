"""STARRY NIGHT SPONSORSHIP DECK, COLD (user brief 2026-11-22: "assess this and make me a similar deck for our upcoming event Starry Nights and keep the place for pictures blank").

A fork of scratchpad/gen_sponsor_deck.py (the Disco Diwali master, 36 slides) on the same scaffold (engine/deckkit.py), so the design is the original's: same grounds, tilted
accent tag, pill stats, 28px frames, one icon set. What differs:
  * EVERY PHOTO SLOT IS BLANK (user: pictures come later, once the outline is approved). `K.photo` is replaced by a labelled blank frame ("Photo 04.2" = slide 04, slot 2) so
    the user can say which picture goes where. Past-event FLYERS, third-party LOGOS, the two 'your logo here' mock-ups and the QR are not photographs of people, so they are kept
    (cropped from the user's own PDF by scratchpad/starry_deck_assets.py into the git-ignored engine/assets/sponsorship/starry/).
  * User change 1 (cover): orange chip = LAST WEEK OF DECEMBER (TENTATIVE) [user wrote square brackets; the deck's own style is parentheses], outline chip = 600+ EXPECTED,
    white box = STARRY NIGHTS.
  * User change 2 (slide 9): the green 'You are next' box is replaced by a Disco Diwali card in the other cards' format: Nov 2026, 600+ guests, Rs 7L raised, 60 Chowringhee Banquets.
  * DERIVED from those (stated, not asked): events become EIGHT, so the totals are Rs 40.3L+ (33.3 + 7) and 4,450+ guests (3,850 + 600); slides 10, 11 and 23 say eight.
    User changes 3-5 (2026-11-22): slide 12 = DISCO DIWALI, THRICE (third picture slot carries no overlay text; 400+ -> 600+, labels as in the original); slide 13 = STARRY NIGHT, AGAIN with a third box\n    (Dec 2026, 600+ expected) and no picture; slide 15 = DISCO DIWALI, YEAR 3 (pictures and the OCTOBER 2025 chip unchanged).
  * Event-specific copy adapted: date (last week of December, tentative), 600+ expected, 'Starry Night' for 'Disco Diwali', the four reasons (from past Starry Night flyers), tier root.
  * NOT KNOWN, so not invented: the run-of-show times (chips read TIME TBC), the venue ('confirmed shortly'), a 2026 Starry Night flyer (blank slot).
Contact details live in scratchpad/sponsorship_private/facts.json (git-ignored: the repo is public).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_starry_deck.py [slide numbers ...]   ->  out/decks/starry_night/slide_NN.png (+ the PDF when all render)
"""
import asyncio, base64, importlib.util, json, os, sys

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

FACTS = json.load(open(os.path.join(ROOT, "scratchpad", "sponsorship_private", "facts.json")))
ASSET = os.path.join(ROOT, "engine", "assets", "sponsorship", "starry")
OUT = os.path.join(ROOT, "out", "decks", "starry_night")
LABEL = "Starry Night 2026  ·  Partnership proposal"
G, BL, LM, INK, MUTE = K.GREEN, K.BLUE, K.ORANGE, K.INK, K.MUTE
CREAM = K.CREAM_ON_DARK
TONES = [G, BL, LM]
INK2 = K.INK2
NL = "\n"
DATE = "Last week of December 2026 (tentative)"


# ── blank photo slots ─────────────────────────────────────────────────────────────────────────
CUR = [0, 0]          # [slide number, slot counter on that slide]


def blank(i=0, focus="50% 50%", r=K.R_FRAME, extra="", tag="photo", alt="", dark=False):
    """A labelled BLANK picture frame (user: keep the places for pictures blank). Label = Photo <slide>.<slot>, so a later brief can say 'photo 04.2 = X'."""
    CUR[1] += 1
    bg, fg, ol = ("#262630", "rgba(244,239,224,.55)", "rgba(244,239,224,.24)") if dark else ("#DCD5C0", "rgba(10,10,10,.45)", "rgba(10,10,10,.22)")
    return (f'<div class="ph blank" data-tag="{tag}" style="background:{bg};border-radius:{r}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;'
            f'outline:2px dashed {ol};outline-offset:-14px;color:{fg};{extra}">{K.icon("camera", 44, fg, 1.6)}'
            f'<span class="mono" style="font-size:15px">Photo {CUR[0]:02d}.{CUR[1]}</span></div>')


K.photo = blank


def asset_uri(name):
    p = name if os.path.isabs(name) else os.path.join(ASSET, name + ".png")
    im = Image.open(p)
    if max(im.size) > 900: im.thumbnail((900, 900), Image.LANCZOS)
    import io
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


class Ctx:
    def __init__(self, n=1, total=1, tone=None): self.n, self.total, self.tone = n, total, tone


def S(body, head=None, c=None, dark=False, **kw):
    if "tone" not in kw and c.tone: kw["tone"] = c.tone
    return K.slide(body, head, c.n, c.total, LABEL, dark, **kw)


def ph(i=0, focus="50% 50%", cap=None, alt="", extra="", dark=False):
    cp = f'<div class="cap">{K.esc(cap)}</div>' if cap else ""
    return f'<div class="frame" style="width:100%;height:100%;{extra}">{blank(i, focus, dark=dark)}{cp}</div>'


def real(file, focus="50% 50%", r=K.R_FRAME, cap=None):
    """A FILLED picture slot (same frame and corner as blank()), for the pictures the user has supplied. Takes a file name in engine/assets/img/events/starry-night-2026-11/."""
    CUR[1] += 1                                    # keep the Photo NN.k numbering of the remaining blanks stable
    u = K.uri(os.path.join(ROOT, "engine", "assets", "img", "events", "starry-night-2026-11", file))
    return (f'<div class="frame" style="width:100%;height:100%"><div class="ph" data-tag="photo" role="img" style="background-image:url({u});background-position:{focus};border-radius:{r}px"></div></div>')


def grid(children, cols, rows=None, gap=24, style=""):
    cols = cols.replace("1fr", "minmax(0,1fr)")
    r = f"grid-template-rows:repeat({rows},minmax(0,1fr));" if rows else ""
    return (f'<div style="display:grid;grid-template-columns:{cols};{r}gap:{gap}px;width:100%;height:100%;{style}">' + "".join(children) + "</div>")


def bento_photo(items, cols, rows, gap=20, files=None):
    cells = [f'<div style="grid-column:span {cs};grid-row:span {rs};min-height:0;min-width:0">{real(files[k], f) if files and files[k] else ph(0, f)}</div>' for k, (_, f, cs, rs) in enumerate(items)]
    return grid(cells, cols, rows, gap)


def photo_story(c, n_photos, cols, rows, caption, tag, tone=G, spans=None, files=None, focus=None):
    """The ONE photo-slide template: a bento of photo slots, a tag chip top-left and a cream caption card overlapping the lower-left."""
    items = [(0, (focus[k] if focus else "50% 50%"), *(spans[k] if spans else (1, 1))) for k in range(n_photos)]
    body = (f'<div style="position:relative;width:100%;height:100%">{bento_photo(items, cols, rows, files=files)}'
            f'<div style="position:absolute;left:28px;top:28px">{K.chip(tag, tone)}</div>'
            f'<div style="position:absolute;left:28px;bottom:28px;background:{K.BG};border-radius:22px;padding:26px 38px;max-width:880px;color:{K.INK};'
            f'box-shadow:0 18px 40px -20px rgba(0,0,0,.5)">'
            f'<div style="font:900 62px/.98 var(--d);text-transform:uppercase;letter-spacing:-.01em">{caption}</div></div></div>')
    return S(body, None, c, body_style="margin-top:0")


def sticker_html(svg, w, h, x, y, rot=0):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:6;pointer-events:none">{svg}</div>'


def moon_sticker(width=190):
    """A die-cut crescent moon + star in the kit's treatment, in place of the Disco Diwali ball (which belongs to the other event)."""
    art = (f'<path d="M118,22 A78,78 0 1 0 176,132 A62,62 0 1 1 118,22 Z" fill="{stk.Y}" stroke="{stk.YD}" stroke-width="5" stroke-linejoin="round"/>'
           f'{stk.ddt.star4(162, 52, 28, stk.G, 12, .34)}{stk.ddt.star4(112, 150, 14, stk.B, 0, .34)}')
    return stk.wrap(art, (0, 0, 200, 200), width, 4)


COVER_SIZE = [124]
COVER_SCRIM = (.62, .40, .22)   # left-to-right navy fade so the white title and chips clear contrast on the bright hall photo (measured, see brain/SPONSORSHIP_DECKS.md)
COVER_FOCUS = 8            # vertical focus of the 4:3 photo inside the 16:9 cover (higher = shows more of the lower light strings)


def s_cover(c):
    chips = [("All for charity", G), ("Last week of December (tentative)", LM), ("600+ expected", "outline")]
    chip_html = "".join(K.chip(*ch) if ch[1] != "outline" else f'<span class="chip" style="border:3px solid #fff;color:#fff;font-size:26px">{K.esc(ch[0])}</span>' for ch in chips)
    svg, w, h = moon_sticker(190)
    CUR[1] += 1                                    # the cover photo is slot 01.1; it is FILLED (2026-11-26: first the DNG star-light shot, then replaced by the user with the balloons-and-chandeliers hall photo)
    cover_img = K.uri(os.path.join(ROOT, "engine", "assets", "img", "events", "starry-night-2026-11", "cover_balloons.jpg"))
    body = (f'<div style="position:absolute;inset:0;background:#000 url({cover_img}) 50% {COVER_FOCUS}%/cover no-repeat"></div>'
            f'<div style="position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.30),rgba(0,0,0,.05) 45%,rgba(0,0,0,.34)),linear-gradient(90deg,rgba(8,6,30,{COVER_SCRIM[0]}),rgba(8,6,30,{COVER_SCRIM[1]}) 60%,rgba(8,6,30,{COVER_SCRIM[2]}))"></div>'
            f'<div style="position:absolute;inset:34px;border:14px solid #fff;border-radius:46px"></div>'
            f'<div style="position:absolute;left:96px;top:92px;color:#fff;font:900 108px/.9 var(--d);text-transform:uppercase;letter-spacing:-.02em">Sponsorship &amp;<br>partnership<br>proposal</div>'
            f'<div style="position:absolute;right:96px;top:88px;background:#fff;border-radius:999px;padding:14px 30px"><img src="{core.LOGO}" style="height:36px;display:block" alt="AquaTerra"></div>'
            f'<div style="position:absolute;left:96px;bottom:96px;background:#fff;color:#000;border-radius:40px;padding:18px 48px 28px;font:900 {COVER_SIZE[0]}px/.88 var(--d);text-transform:uppercase;letter-spacing:-.02em;white-space:nowrap">Starry Nights</div>'
            f'<div style="position:absolute;right:96px;bottom:110px;display:flex;flex-direction:column;gap:14px;align-items:flex-end">{chip_html}</div>'
            + sticker_html(svg, w, h, 1560, 250, 8))
    return S(body, None, c, tone="black", body_style="margin-top:0;position:static", cls="nofoot")


def s_about(c):
    kp = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:34px 30px;align-content:center;height:100%">{K.pillstat("5+", "Years of active student welfare work", BL, 96)}{K.pillstat("1.5K+", "Student volunteers in the community", G, 96)}{K.pillstat("500+", "Welfare projects delivered", G, 96)}{K.pillstat("5K+", "Instagram followers", BL, 96)}</div>'
    left = (f'<div style="width:900px;display:flex;flex-direction:column;gap:30px;min-height:0">'
            f'{K.lede("AquaTerra is a student-run, registered NGO based in Kolkata. We power some of the city’s biggest youth-led fundraising events, and net proceeds, after event costs, go back into welfare work across the city.", 30)}'
            f'<div style="flex:1;min-height:0">{kp}</div></div>')
    return S(left + f'<div style="flex:1;margin-left:56px">{real("team_group_balloons.jpg", "50% 90%")}</div>', (K.eyebrow("About AquaTerra"), K.title("A student-run NGO that *delivers*")), c)   # slot 02.1 FILLED (user, 2026-11-26)


def s_glance(c):
    facts = [("calendar", "When and where", f"{DATE}. Venue confirmed shortly."), ("users", "Who", "Classes 9-12 and college students"),
             ("ticket", "How many", "600+ guests expected"), ("shield", "House rules", "No alcohol at the event. Under-18 entry allowed."), ("heart", "Why", "Net proceeds fund AquaTerra’s welfare work")]
    left = K.card("".join(f'<div style="display:flex;align-items:center;gap:22px;padding:20px 0;{"border-top:1.5px solid " + K.LINE + ";" if i else ""}">'
                          f'<span class="disc" style="background:{TONES[i % 3]};color:{core.text_on(TONES[i % 3])}">{K.icon(ic, 30)}</span>'
                          f'<div><div class="mono" style="font-size:16px;color:{K.MUTE}">{k}</div><div style="font:600 27px/1.2 var(--e);margin-top:4px">{v}</div></div></div>'
                          for i, (ic, k, v) in enumerate(facts)), "", "width:760px;padding:18px 40px;display:flex;flex-direction:column;justify-content:center")
    ladder = [("Title sponsor", LM), ("Co-sponsor", BL), ("Associate sponsor", G), ("Education and media partners", K.PAPER), ("Category sponsors: hydration, fashion", K.PAPER), ("In-kind partners", K.PAPER), ("Stall space at the venue", K.PAPER)]
    rows = "".join(f'<div style="background:{t};color:{core.text_on(t) if t != K.PAPER else K.INK};border:1.5px solid {K.LINE};border-radius:20px;padding:15px 30px;'
                   f'font:900 31px/1 var(--d);text-transform:uppercase;display:flex;justify-content:space-between;align-items:center">{n}{K.icon("arrow", 30, "currentColor", 2.2)}</div>' for n, t in ladder)
    ct = FACTS["contact"]
    right = (f'<div style="flex:1;margin-left:40px;display:flex;flex-direction:column;gap:14px;justify-content:center"><div class="mono" style="font-size:16px;color:{K.MUTE};margin-bottom:6px">Ways to be part of it</div>{rows}'
             f'<div style="font:600 25px/1.3 var(--e);color:{INK2};margin-top:8px">Prices on request. Call {K.esc(ct["name"])}, {K.esc(ct["role"])}, {K.esc(ct["phone"])}.</div></div>')
    return S(left + right, (K.eyebrow("The short version"), K.title("The offer, in *one* page")), c)


def s_different(c):
    items = [("eye", "Student run", "Every event is planned and run entirely by student volunteers.", G),
             ("heart", "Welfare first", "Net proceeds go directly into funding welfare projects and campaigns.", BL),
             ("megaphone", "Visibility", "A night of visibility with hundreds of Kolkata’s most engaged students on the night, and thousands more in our network.", LM)]
    cards = []
    for k, (ic, t, d, tone) in enumerate(items, 1):
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="height:330px;flex:none;position:relative">{real(f"dd_different_{k}.jpg", "50% 0%", r=0)}'   # the three Disco Diwali deck photos, cropped from its page 4 (user, 2026-11-26)
                     f'<span class="disc" style="position:absolute;left:34px;bottom:-30px;background:{tone};color:{core.text_on(tone)};width:84px;height:84px;border:6px solid {BL}">{K.icon(ic, 38)}</span></div>'
                     f'<div style="padding:58px 40px 34px"><div style="font:900 50px/1 var(--d);text-transform:uppercase;margin-bottom:16px">{t}</div>'
                     f'<div style="font:400 28px/1.35 var(--e);color:{INK2}">{d}</div></div></div>')
    return S(grid(cards, "1fr 1fr 1fr", None, 28), (K.eyebrow("Why AquaTerra"), K.title("What makes us *different*")), c)


def s_vision(c):
    t = ("Five-plus years turning youth energy into real " f'<span class="tg" style="background:{INK};color:#fff">welfare</span> work across Kolkata.')
    left = (f'<div style="display:flex;flex-direction:column;justify-content:center;gap:44px;width:1060px">'
            f'<div style="font:900 84px/.98 var(--d);text-transform:uppercase;letter-spacing:-.01em">{t}</div>'
            f'<div style="display:flex;gap:14px;flex-wrap:wrap">{K.chip("1.5K+ community", G)}{K.chip("4000+ kids reached", BL)}{K.chip("80G certified", INK, "#fff")}{K.chip_o("Darpan registered", dark=True)}</div></div>')
    return S(left + f'<div style="flex:1;margin-left:64px;min-height:0">{real("dd_vision.jpg")}</div>', (K.eyebrow("Our vision", LM),), c)   # slot 05.1 FILLED: the Disco Diwali deck's picture


def s_welfare(c):
    return photo_story(c, 3, "1.25fr 1fr 1fr", 2, "Children, welfare and education", "Our work", G, spans=[(2, 2), (1, 1), (1, 1)], files=["dd_welfare_1.jpg", "dd_welfare_2.jpg", "dd_welfare_3.jpg"])   # slots 06.1-3 FILLED: the Disco Diwali deck's pictures


def s_impact(c):
    data = [("1600+", "Doctor check-ups in the Sundarbans"), ("3000+", "Dogs fed across Kolkata"), ("5K+", "Saplings planted by our team"),
            ("2.5T", "Of clothes collected in donation drives"), ("15K+", "Bananas distributed in our most recent campaign"), ("4000+", "Kids reached across workshops")]
    tiles = [f'<div style="display:flex;align-items:center">{K.pillstat(v, l, (G if (i + i // 3) % 2 else None), 120)}</div>' for i, (v, l) in enumerate(data)]
    return S(grid(tiles, "1fr 1fr 1fr", 2, 26), (K.eyebrow("Impact"), K.title("Impact *metrics*")), c)


def s_growth(c):
    big = lambda v, l, tone: (f'<div style="background:{tone};color:{core.text_on(tone)};border-radius:{K.R_CARD}px;display:flex;flex-direction:column;justify-content:flex-end;padding:44px 48px">'
                              f'<div class="kv" style="font-size:150px;margin-bottom:12px">{v}</div><div style="font:600 28px/1.25 var(--e)">{l}</div></div>')
    left = grid([big("5M+", "impressions across social media and marketing", G), big("5+", "marketing verticals running all year", LM),
                 big("112", "projects completed in 2025 alone", BL), big("500+", "projects since 2021: a five-year record of delivering", G)], "1fr 1fr", 2, 24, "width:1040px")
    right = f'<div style="flex:1;margin-left:40px;display:grid;grid-template-rows:1fr 1fr;gap:24px;min-height:0">{real("dj_decks_2.jpg", "50% 62%")}{real("summer_five_banner.jpg", "50% 60%")}</div>'   # slots 08.1 / 08.2 FILLED (user, 2026-11-26)
    return S(left + right, (K.eyebrow("Track record"), K.title("A five-year record of *delivering*")), c)


# (flyer asset or None, name, when, guests, raised, where). Chronological; funds are GROSS. EIGHT flagship events now: Disco Diwali Nov 2026 is the 8th (user, 2026-11-22).
DD26_FLYER = os.path.join(ROOT, "engine", "assets", "img", "events", "starry-night-2026-11", "dd26_poster.jpg")   # the user-supplied Disco Diwali 2026 poster (red mask, diya ground), Instagram UI icons inpainted out (2026-11-26)
EVENTS = [
    ("flyer_dd24", "Disco Diwali", "Oct 2024", "350+", "₹1.7L", "Orbit Crystal"),
    ("flyer_sn24", "The Starry Night", "Dec 2024", "550+", "₹3L", "Sky Turf, DJ Saif Side"),
    ("flyer_paradox", "Paradox 3.0", "2025", "1000+", "₹8.9L", "VS Arena, Battleground, Desi Lane Esplanade"),
    ("flyer_punjabi", "The AQ Punjabi Night", "Jun 2025", "400+", "₹2.2L", "60 Chowringhee, DJ Omar"),
    (None, "Disco Diwali", "22 Oct 2025", "500", "₹4.5L+", ""),
    ("flyer_sn25", "Starry Night 2.0", "Dec 2025", "550+", "₹6.7L", "Sky Turf, DJ Rajiv"),
    ("flyer_summer", "Summer Sunset", "Jun 2026", "500+", "₹6.3L", "60 Chowringhee Banquet"),
    (DD26_FLYER, "Disco Diwali", "Nov 2026", "600+", "₹7L", "60 Chowringhee Banquets"),
]
E_DD24, E_SN24, E_PARADOX, E_PUNJABI, E_DD25, E_SN25, E_SUMMER, E_DD26 = range(8)
TOTAL_FUNDS, TOTAL_GUESTS = "₹40.3L+", "4,450+"     # 1.7+3+8.9+2.2+4.5+6.3+6.7+7 = 40.3 ; 350+550+1000+400+500+550+500+600 = 4450


def _poster(p, big=None):
    if p is None:
        return f'<div style="width:100%;aspect-ratio:4/5">{blank(0, r=16)}</div>'
    src = asset_uri(big or p)
    return (f'<div style="width:100%;aspect-ratio:4/5;background-image:url({src});background-size:cover;background-position:50% 20%;border-radius:16px;box-shadow:0 0 0 1.5px {K.LINE}"></div>')


def s_events(c):
    """Slide 9, NINE cards (user, 2026-11-26): the eight events plus a STARRY NIGHT 2026 box in the same card format. Nine do not fit the original 4x2, so the grid is 3x3 with the SAME card
    (150px 4:5 picture, mono date, 24px display name, two stats, venue line). The Oct 2025 Disco Diwali card is FILLED with the original deck's photo (cropped from its page 9; the original
    used a photo there, not a flyer). Starry Night 2026 is kept OUT of EVENTS on purpose: it has not happened, so the 'eight events' totals elsewhere stay true. It shows 600+ expected and
    no raised figure, and its picture slot is blank (no 2026 flyer yet)."""
    dd25 = (f'<div style="width:100%;aspect-ratio:4/5;background-image:url({K.uri(os.path.join(ROOT, "engine", "assets", "img", "events", "starry-night-2026-11", "dd25_card_photo.jpg"))});'
            f'background-size:cover;background-position:50% 50%;border-radius:16px;box-shadow:0 0 0 1.5px {K.LINE}"></div>')
    rows = [(dd25 if i == E_DD25 else _poster(p), name, when, [(foot, "guests"), (funds, "raised")], where) for i, (p, name, when, foot, funds, where) in enumerate(EVENTS)]
    rows.append((_poster(None), "Starry Night", "Dec 2026 · next", [("600+", "expected")], "Last week of December (tentative)"))
    cards = []
    for poster, name, when, stat_list, where in rows:
        stat = lambda v, l: (f'<div><div class="kv" style="font-size:34px">{v}</div><div class="mono" style="font-size:14px;color:{K.MUTE};margin-top:5px">{l}</div></div>')
        stats = f'<div style="display:flex;gap:16px;margin:12px 0 10px">{"".join(stat(v, l) for v, l in stat_list)}</div>'
        cards.append(K.card(f'<div style="display:flex;gap:18px;height:100%;align-items:center"><div style="width:150px;flex:none">{poster}</div>'
                            f'<div style="display:flex;flex-direction:column;justify-content:center;min-width:0">'
                            f'<div class="mono" style="font-size:14px;color:{K.MUTE}">{when}</div>'
                            f'<div style="font:900 24px/1 var(--d);text-transform:uppercase;margin-top:6px">{K.esc(name)}</div>{stats}'
                            f'<div style="font:400 17px/1.3 var(--e);color:{INK2}">{K.esc(where)}</div></div></div>', style="padding:18px 20px"))
    body = (f'<div style="display:flex;flex-direction:column;gap:14px;width:100%;min-height:0"><div style="flex:1;min-height:0">{grid(cards, "repeat(3,1fr)", 3, 20)}</div>'
            f'<div style="font:400 19px var(--e);color:{K.MUTE}">Raised figures are gross, before event costs.</div></div>')
    return S(body, (K.eyebrow("Prominent past events"), K.title("Events people *show up* for")), c)


def s_proof(c):
    pics = [("s10_e.jpg", "50% 35%"), ("s10_f.jpg", "42% 45%"), ("s10_g.jpg", "58% 40%"), ("s10_h.jpg", "55% 40%")]      # slots 10.1-10.4 FILLED, second set (user, 2026-11-26); the first set s10_a-d is superseded
    strip = "".join(f'<div style="flex:1;min-width:0;min-height:0">{real(f, fo)}</div>' for f, fo in pics)
    body = (f'<div style="display:flex;flex-direction:column;width:100%;gap:36px;min-height:0"><div style="display:flex;gap:60px;align-items:flex-end">'
            f'<div><div class="kv" style="font-size:250px;color:{G}">{TOTAL_FUNDS}</div><div style="font:600 34px/1.2 var(--e);color:#D8D3C2;margin-top:6px">raised (gross) across eight flagship events</div></div>'
            f'<div style="padding-bottom:14px"><div class="kv" style="font-size:120px;color:{LM}">{TOTAL_GUESTS}</div><div style="font:600 30px/1.2 var(--e);color:#D8D3C2;margin-top:6px">guests across the same eight</div></div></div>'
            f'<div style="display:flex;gap:20px;width:100%;flex:1;min-height:0">{strip}</div></div>')
    return S(body, (K.eyebrow("The proof", LM),), c)


def s_notoneoff(c):
    dd25 = (f'<div style="width:100%;aspect-ratio:4/5;background-image:url({K.uri(os.path.join(ROOT, "engine", "assets", "img", "events", "starry-night-2026-11", "dd25_card_photo.jpg"))});'
            f'background-size:cover;background-position:50% 50%;border-radius:16px;box-shadow:0 0 0 1.5px {K.LINE}"></div>')      # Disco Diwali 2025: the slide-9 picture (user, 2026-11-26)
    posters = "".join(f'<div style="flex:1;min-width:0">{dd25 if i == E_DD25 else _poster(e[0])}</div>' for i, e in enumerate(EVENTS))
    body = (f'<div style="display:flex;flex-direction:column;justify-content:space-between;width:100%;min-height:0">'
            f'<div><div style="font:900 220px/.88 var(--d);text-transform:uppercase;letter-spacing:-.02em">Not a <span class="tg" style="background:{BL};color:#fff">one-off</span></div>'
            f'<div style="font:600 38px/1.25 var(--e);margin-top:26px;max-width:1400px">Eight flagship events. Disco Diwali three times. Starry Night twice, and now a third. Every one of them for charity.</div></div>'
            f'<div style="display:flex;gap:18px;width:100%">{posters}</div></div>')
    return S(body, None, c, body_style="margin-top:0")


def s_series_diwali(c):
    """Disco Diwali, THRICE (user, 2026-11-22). The third picture keeps its slot but carries NO overlay text (the original's 'YOU ARE HERE 2026' and the white date line are removed).
    The third stat bar is the original's with ONE change: 400+ -> 600+ (still labelled EXPECTED, still NOV 2026, as the user wrote it; slide 9's card says 600+ guests / Rs 7L raised, so
    EXPECTED now reads stale next to it. Flagged to the user, not changed)."""
    def col(yr, img, stats):
        return (f'<div style="display:flex;flex-direction:column;gap:18px;min-height:0;min-width:0"><div>{K.chip(yr, INK, K.CREAM_ON_DARK, 26)}</div>'
                f'<div style="flex:1;min-height:0">{img}</div><div class="card" style="padding:18px 26px;display:flex;justify-content:space-between;align-items:center">{stats}</div></div>')
    st = lambda a, b: f'<div style="font:900 34px/1 var(--d);text-transform:uppercase">{a}</div><div class="mono" style="font-size:16px;color:{K.MUTE}">{b}</div>'
    c24 = col("Oct 2024", _poster(EVENTS[E_DD24][0], "flyer_dd24_big").replace("aspect-ratio:4/5", "height:100%"), st("350+", "guests") + st("₹1.7L", "raised"))
    c25 = col("Oct 2025", real("dd25_card_photo.jpg", "50% 50%"), st("500", "guests") + st("₹4.5L+", "raised"))   # the slide-9/11 picture (user, 2026-11-26)
    c26 = col("2026", real("dd26_discoball.jpg", "50% 55%"), st("600+", "expected") + st("Nov", "2026"))   # user photo; chip no longer says (tentative) (user, 2026-11-26)
    body = f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;width:100%;min-height:0">{c24}{c25}{c26}</div>'
    return S(body, (K.eyebrow("Disco Diwali", INK), K.title("Disco Diwali, *thrice*")), c)


def s_series_starry(c):
    """Starry Night, AGAIN (user, 2026-11-22). The two past editions keep flyer + chip + stats + venue. The THIRD box replicates them WITHOUT a picture (user): chip DEC 2026, 600+ EXPECTED,
    and no raised figure or venue (none supplied). The big 600+ takes the picture's height so the column keeps its weight instead of leaving a dead gap above the label."""
    PW = 380; PH = round(PW * 5 / 4)
    stat = lambda v, col_, l, sz=76: (f'<div><div class="kv" style="font-size:{sz}px;color:{col_}">{v}</div><div class="mono" style="font-size:15px;color:#fff;opacity:.85;margin-top:4px">{l}</div></div>')
    def col(yr, poster, a, a_lab, b, b_lab, where):
        return (f'<div style="display:flex;flex-direction:column;gap:16px;min-height:0;min-width:0;align-items:flex-start"><div>{K.chip(yr, INK, K.CREAM_ON_DARK, 24)}</div>'
                f'<div style="width:{PW}px">{poster}</div><div style="display:flex;gap:34px">{stat(a, "#fff", a_lab)}{stat(b, LM, b_lab)}</div>'
                f'<div style="font:600 22px/1.3 var(--e);color:#fff">{where}</div></div>')
    CARD_H = PH + 16 + 94 + 16 + 29 - 12            # same top and bottom as the other two columns: picture top to the venue line's bottom
    c26 = (f'<div style="display:flex;flex-direction:column;gap:16px;min-height:0;min-width:0;align-items:flex-start"><div>{K.chip("Dec 2026", INK, K.CREAM_ON_DARK, 24)}</div>'
           f'<div style="width:480px;height:{CARD_H}px;box-sizing:border-box;background:{INK};border-radius:{K.R_FRAME}px;padding:34px 36px;display:flex;flex-direction:column">'
           f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center"><div class="kv" style="font-size:150px;color:#fff;line-height:.85">600+</div><div class="mono" style="font-size:16px;color:{LM};margin-top:16px">EXPECTED</div></div>'
           f'<div style="font:600 24px/1.3 var(--e);color:#fff">Last week of December (tentative)</div></div></div>')
    cols = (col("Dec 2024", _poster("flyer_sn24", "flyer_sn24_big"), "550+", "guests", "₹3L", "raised", "Sky Turf, DJ Saif Side")
            + col("Dec 2025", _poster("flyer_sn25", "flyer_sn25_big"), "550+", "guests", "₹6.7L", "raised", "Sky Turf, DJ Rajiv") + c26)
    body = (f'<div style="display:flex;flex-direction:column;gap:26px;width:100%;min-height:0"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;flex:1;min-height:0;align-items:start">{cols}</div>'
            f'<div style="background:{LM};color:{INK};border-radius:999px;padding:18px 40px;font:900 40px/1 var(--d);text-transform:uppercase;align-self:center">Same crowd size. More than double the funds.</div></div>')
    return S(body, (K.eyebrow("Starry Night", "#fff"), K.title("Starry Night, *again*")), c)


def s_photo_summer(c):
    return photo_story(c, 3, "1fr 1fr 1fr", 1, "Summer Sunset: AQ turned five", "June 2026", LM, files=["dd_summer_1.jpg", "dd_summer_2.jpg", "dd_summer_3.jpg"])   # slots 14.1-3 FILLED: the Disco Diwali deck's pictures


def s_photo_diwali25(c):
    return photo_story(c, 3, "1.4fr 1fr 1fr", 2, "Disco Diwali, year 3", "October 2025", G, spans=[(2, 2), (1, 1), (1, 1)], files=["s15_i.jpg", "s15_j.jpg", "s15_k.jpg"], focus=["60% 6%", "45% 35%", "50% 60%"])   # slots 15.1-3 FILLED (user, 2026-11-26)


def s_photo_starry25(c):
    """NEW slide 16 (user, 2026-11-26): 'copy the template of slide 15 and make one for Starry Nights year 2'. Same photo_story template as slide 15 (large frame left, tag chip, caption card),
    with THREE small frames on the right (four pictures were supplied, the template holds three). Starry Night 2.0 was Dec 2025 (events list); 'year 2' is the user's wording."""
    return photo_story(c, 4, "1.4fr 1fr 1fr", 3, "Starry Night, year 2", "December 2025", BL, spans=[(2, 3), (1, 1), (1, 1), (1, 1)],
                       files=["sn25_d.jpg", "sn25_a.jpg", "sn25_b.jpg", "sn25_c.jpg"], focus=["50% 62%", "45% 30%", "35% 35%", "70% 40%"])


def s_photo_sports(c):
    return photo_story(c, 3, "1fr 1fr 1fr", 1, "And not only parties: the sports fest", "TerraThon", BL, files=["dd_sports_1.jpg", "dd_sports_2.jpg", "dd_sports_3.jpg"])   # the Disco Diwali deck's pictures (user, 2026-11-26)


def s_sponsors(c):
    tiles = []
    for n in range(1, 31):
        dk = n in (16, 23)
        tiles.append(f'<div style="background:{"#16181C" if dk else K.PAPER};border:1.5px solid {K.LINE};border-radius:20px;overflow:hidden">'
                     f'<img src="{asset_uri(f"logo_{n:02d}")}" style="width:100%;height:100%;object-fit:cover;display:block" alt=""></div>')
    return S(grid(tiles, "repeat(6,1fr)", 5, 16), (K.eyebrow("Trusted by"), K.title("Past *sponsors*")), c)


QUOTES = [("q_redbull", "Delivered exactly what they had promised to perfection."),
          ("q_realmark", "It was a wonderful experience partnering with AquaTerra. The team was enthusiastic, organised, and professional."),
          ("q_leveraged", "We loved being a part of AquaTerra’s initiative. Their energy and dedication really stood out."),
          ("q_friends", "AquaTerra creates a great platform for young people to explore, connect, and create. Proud to support their work."),
          ("q_subway", "AquaTerra is doing great work by bringing young people together for meaningful initiatives. We’re happy to support them.")]


def s_feedback(c):
    def q(i, text, size, dark=False, big=False):
        mark = f'<div style="font:900 {120 if big else 80}px/.7 var(--d);color:{G if dark else K.GREEN_D}">“</div>'
        return K.card(f'{mark}<div style="font:{"900" if big else "600"} {size}px/1.22 var({"--d" if big else "--e"});{"text-transform:uppercase;" if big else ""}margin-top:12px;flex:1">{K.esc(text)}</div>'
                      f'<div style="height:64px;display:flex;align-items:center"><img src="{asset_uri(i)}" style="height:60px;border-radius:14px;display:block" alt=""></div>',
                      "q", f"display:flex;flex-direction:column;{'padding:46px 52px;' if big else 'padding:28px 32px;'}", dark=dark)
    hero = q(*QUOTES[0], 60, True, True)
    small = grid([q(i, t, 27) for i, t in QUOTES[1:]], "1fr 1fr", 2, 22)
    return S(grid([hero, small], "0.8fr 1.5fr", None, 24), (K.eyebrow("Feedback from past sponsors"), K.title("In their *words*")), c)


def s_photo_energy(c):
    return photo_story(c, 3, "1.4fr 1fr 1fr", 2, "The party the city talks about", "Disco Diwali", LM, spans=[(2, 2), (1, 1), (1, 1)], files=["dd_energy_1.jpg", "dd_energy_2.jpg", "dd_energy_3.jpg"])   # the Disco Diwali deck's pictures; the tag says DISCO DIWALI because they ARE Disco Diwali photos (user, 2026-11-26)


def s_flagship(c):
    feats = [("Food and sales stalls", G), ("A Christmas carnival night", LM), ("The party: a DJ-led night", BL), ("Neon bands and surprises", G)]
    tile = ["dd_reasons_1.jpg", "sn25_d.jpg", "dd_reasons_3.jpg", "s10_a.jpg"]     # tiles 1 and 3 are the Disco Diwali deck's (their captions match); 2 and 4 would contradict the Starry Night captions (a Diwali arch under 'A Christmas carnival night'), so they use the user's Starry Night photos
    tfocus = ["50% 50%", "50% 62%", "50% 50%", "45% 42%"]
    cards = [f'<div class="card dk" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column"><div style="flex:1;min-height:0">{real(tile[k], tfocus[k], r=0)}</div>'
             f'<div style="padding:22px 28px;display:flex;align-items:center;gap:16px"><span style="width:16px;height:16px;border-radius:50%;background:{t};flex:none"></span>'
             f'<div style="font:900 34px/1.02 var(--d);text-transform:uppercase">{n}</div></div></div>' for k, (n, t) in enumerate(feats)]
    left = (f'<div style="width:620px;display:flex;flex-direction:column;justify-content:space-between;min-height:0">'
            f'<div><div class="kv" style="font-size:230px;color:{G}">600+</div><div style="font:600 34px/1.2 var(--e);color:#D8D3C2;margin-top:8px">expected at the Starry Night party</div></div>'
            f'<div class="card dk" style="padding:24px 30px;display:flex;flex-direction:column;gap:18px">'
            f'<div><div class="mono" style="font-size:16px;color:#A7A292">Tentative date, venue confirmed shortly</div><div style="font:900 36px/1 var(--d);text-transform:uppercase;margin-top:8px">Last week of December 2026</div></div>'
            f'<div style="border-top:1.5px solid rgba(244,239,224,.14);padding-top:18px"><div class="mono" style="font-size:16px;color:#A7A292">Target market</div><div style="font:900 36px/1 var(--d);text-transform:uppercase;margin-top:8px">Classes 9-12 and college students</div></div>'
            f'<div style="border-top:1.5px solid rgba(244,239,224,.14);padding-top:18px"><div class="mono" style="font-size:14px;color:#A7A292">House rules</div><div style="font:900 30px/1.05 var(--d);text-transform:uppercase;margin-top:8px">No alcohol. Under-18 entry allowed.</div></div></div></div>')
    right = f'<div style="flex:1;margin-left:48px;min-height:0">{grid(cards, "1fr 1fr", 2, 22)}</div>'
    return S(left + right, (K.eyebrow("The flagship", LM), K.title("One night, *four* reasons")), c)


def s_demo(c):
    counts = [("Class 9-10", "14-16 years", 525, "#93A0FF"), ("Class 11-12", "16-18 years", 820, BL), ("College", "18+ years", 465, K.INDIGO)]
    tot = sum(v for _, _, v, _ in counts)
    sl = [(n, 100 * v / tot, col) for n, _, v, col in counts]
    pct = [round(p) for _, p, _ in sl]; assert sum(pct) == 100, pct
    legend = "".join(
        f'<div class="card" data-tag="card" style="display:flex;align-items:center;gap:22px;padding:24px 30px"><span style="width:28px;height:28px;border-radius:50%;background:{col};flex:none"></span>'
        f'<div style="flex:1"><div style="font:900 40px/1 var(--d);text-transform:uppercase">{n}</div><div class="mono" style="font-size:16px;color:{K.MUTE};margin-top:8px">{sub}</div></div>'
        f'<div class="kv" style="font-size:72px">{p}%</div></div>' for (n, sub, v, col), p in zip(counts, pct))
    vol = K.card(f'<span class="disc" style="background:#000;color:#fff">{K.icon("users", 30)}</span>'
                 f'<div><div class="kv" style="font-size:72px">1.5K+</div><div class="kl">active volunteers in the AQ network, on top of the audience</div></div>', "kpi", "padding:26px 30px;flex-direction:row;align-items:center;justify-content:flex-start;gap:26px")
    note = f'<div style="font:600 22px/1.35 var(--e);color:{INK}">Age split of 1,810 survey respondents across Classes 9-12 and college.</div>'
    pie = K.donut([(n, p, col) for (n, p, col) in sl], 700, 350)
    left = f'<div style="width:760px;display:flex;align-items:center;justify-content:center">{pie}</div>'
    right = f'<div style="flex:1;display:flex;flex-direction:column;gap:18px;justify-content:center">{legend}{vol}{note}</div>'
    return S(left + right, (K.eyebrow("Demographics"), K.title("Who is in the *room*")), c)


SCHOOLS = ["Calcutta Boys’ School", "St. Xavier’s Collegiate School", "La Martiniere for Boys", "La Martiniere for Girls", "Loreto House", "St. James’ School", "Birla High School",
           "Don Bosco School Park Circus", "Modern High School for Girls", "South Point High School", "Mahadevi Birla World Academy", "Garden High School", "Army Public School Ballygunge",
           "Delhi Public School Ruby Park", "St. Lawrence High School", "The Heritage School", "Calcutta International School", "Cambridge Academy"]


def s_community(c):
    chips = "".join(f'<span class="chip" style="background:{TONES[i % 3] if i % 2 == 0 else K.PAPER};color:{INK};border:1.5px solid {K.LINE};font-size:22px;padding:10px 20px">{K.esc(n)}</span>' for i, n in enumerate(SCHOOLS))
    left = (f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:26px;justify-content:center;min-height:0">'
            f'<div style="display:flex;align-items:flex-end;gap:26px"><div class="kv" style="font-size:140px">18</div>'
            f'<div style="font:600 32px/1.2 var(--e);padding-bottom:18px">leading Kolkata schools in the AQ community</div></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:12px">{chips}</div></div>')
    right = f'<div style="width:640px;margin-left:48px;display:grid;grid-template-rows:1.2fr 1fr;gap:22px;min-height:0">{real("dd_school_1.jpg")}<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;min-height:0">{real("dd_school_2.jpg")}{real("dd_school_3.jpg")}</div></div>'
    return S(left + right, (K.eyebrow("Community"), K.title("Where our *students* come from")), c)


def s_reach(c):
    T = [("Instagram", "5K+", "followers", "insta", G), ("Instagram", "4.3L", "views in a recent 30 days", "eye", BL),
         ("Instagram", "21.7K", "views on the Summer Sunset post", "trend", LM), ("Instagram", "9.3K", "views on the Paradox 2026 post", "trend", G),
         ("WhatsApp", "3,162", "members across 4 community groups", "users", BL), ("Events", "8", "flagship events since October 2024", "ticket", LM),
         ("Schools", "18", "leading Kolkata schools in our network", "school", G), ("All channels", "5M+", "impressions, lifetime, all channels", "megaphone", BL)]
    cards = [K.card(f'<div style="display:flex;align-items:center;gap:14px"><span class="disc" style="background:{tone};color:{core.text_on(tone)};width:54px;height:54px">{K.icon(ic, 26)}</span>'
                    f'<span class="mono" style="font-size:19px;color:#C9C4B3">{ch}</span></div>'
                    f'<div><div class="kv" style="font-size:92px;color:{CREAM}">{v}</div><div class="kl" style="font-size:24px">{lab}</div></div>', "kpi", "padding:28px 32px", dark=True)
             for ch, v, lab, ic, tone in T]
    return S(grid(cards, "repeat(4,1fr)", 2, 22), (K.eyebrow("Reach", LM), K.title("Numbers, *by touchpoint*")), c)


def s_promote(c):
    ch = [("users", "School networks and groups", "Class and school networks across Kolkata, reached directly and through our volunteers.", G),
          ("insta", "Instagram reels and posts", "A year-round content engine: reels, posts and stories, with our event pages and partner collabs.", BL),
          ("megaphone", "Website and offline marketing", "The website, plus marketing stunts and events that put Starry Night in front of students before the poster does.", LM)]
    cards = []
    for k, (ic, t, d, tone) in enumerate(ch, 1):
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="height:300px;flex:none;position:relative">{real(f"dd_promote_{k}.jpg", "50% 30%", r=0)}'
                     f'<span class="disc" style="position:absolute;left:34px;bottom:-30px;background:{tone};color:{core.text_on(tone)};width:84px;height:84px;border:6px solid {BL}">{K.icon(ic, 38)}</span></div>'
                     f'<div style="padding:58px 40px 34px"><div style="font:900 44px/1.02 var(--d);text-transform:uppercase;margin-bottom:16px">{t}</div>'
                     f'<div style="font:400 27px/1.35 var(--e);color:{INK2}">{d}</div></div></div>')
    return S(grid(cards, "1fr 1fr 1fr", None, 28), (K.eyebrow("Promotion"), K.title("How we *promote*")), c)


def s_offline(c):
    left = (f'<div style="width:520px;display:flex;flex-direction:column;gap:24px;justify-content:center">'
            f'{K.lede("The party is the finale. In the weeks before it we are on the ground: school visits, stalls and pop-up stunts that turn students into guests, and guests into your audience.", 29)}'
            f'<ul class="ck">{"".join(f"<li>{K.icon(i, 30, K.GREEN_D)}<span>{t_}</span></li>" for i, t_ in [("school", "School visits and class networks"), ("store", "Pop-up stalls and brand activations"), ("megaphone", "Marketing stunts and events")])}</ul></div>')
    right = (f'<div style="flex:1;margin-left:48px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:22px;min-height:0">'
             f'<div style="grid-row:span 2">{real("dd_ground_1.jpg")}</div>{real("dd_ground_2.jpg")}{real("dd_ground_3.jpg")}</div>')
    return S(left + right, (K.eyebrow("Offline engagement"), K.title("We are on the *ground* too")), c)


# Run of show: Starry Night 2026 times are NOT supplied, so each chip reads TIME TBC (the Disco Diwali times are not reused). Steps are the generic ones; the dhol entry is Diwali-specific.
RUN = ["Decor and venue setup", "Stall setup", "Setup done, stalls go live", "Registrations open", "Opening", "Main DJ set: peak hours", "Closing moment"]


def s_run(c):
    """Run of show (slide 27 since the new slide 16). User, 2026-11-26: the dhol box is removed (here that is the 'Opening' step, the dhol entry and opening of the original) and the supplied pictures
    go in, in the order given. SIX steps remain, FIVE pictures were supplied, so the sixth ('Closing moment') keeps a labelled blank. The House rules card spans two columns on row 2 so the 4x2 grid has no hole."""
    steps = [n for n in RUN if n != "Opening"]
    # box 1 decor (user, 2026-11-27); boxes 2, 4, 5, 6 from the user's 2026-11-27 list "first picture in box 2, 3rd in box 4, 4th in box 5, 6th in box 6". Only FIVE pictures arrived, so the order is
    # pasted-first (1 Pristine Edge, 2 table students [unused], 3 Meetcute, then the HEICs 4 = IMG_3824_2, 5 = IMG_3817_2) and "6th" is read as the LAST one (5). Box 3 keeps run_h.
    pics = [("run_decor.jpg", "50% 40%"),            # box 1 Decor and venue setup (user, 2026-11-27)
            ("r3_1.jpg", "50% 62%"),                  # box 2 Stall setup: Pristine Edge stall pair (3rd set, 2026-11-27, picture 1)
            ("r3_3.jpg", "50% 42%"),                  # box 3 Setup done, stalls go live: Meetcute Cafe chef (picture 3)
            ("r3_2.jpg", "40% 40%"),                  # box 4 Registrations open: three students (picture 2)
            ("r3_4.jpg", "50% 62%"),                  # box 5 Main DJ set: crowd under the star-light net (picture 4)
            ("r3_5.jpg", "50% 62%")]                  # box 6 Closing moment: crowd, arm raised (picture 5; the user wrote '6th picture', five were sent)
    cards = []
    for k, n in enumerate(steps):
        inner = real(pics[k][0], pics[k][1], r=0) if k < len(pics) else real("dd_closing_1.jpg", "50% 50%", r=0)   # 6th step: the Disco Diwali deck's closing-moment picture (user, 2026-11-26)
        cards.append(f'<div class="card" data-tag="card" style="padding:0;overflow:hidden;display:flex;flex-direction:column">'
                     f'<div style="flex:1;min-height:0;position:relative">{inner}'
                     f'<div style="position:absolute;left:18px;top:18px">{K.chip("Time TBC", INK, K.CREAM_ON_DARK, size=20)}</div></div>'
                     f'<div style="padding:20px 26px 24px;font:900 30px/1.02 var(--d);text-transform:uppercase;min-height:104px">{n}</div></div>')
    cards.append(f'<div class="card dk" data-tag="card" style="grid-column:span 2;padding:30px 40px;display:flex;flex-direction:column;justify-content:space-between">'
                 f'<span class="disc" style="background:{G};color:{INK}">{K.icon("shield", 30)}</span><div><div class="mono" style="font-size:16px;color:#A7A292">House rules</div>'
                 f'<div style="font:900 52px/1.02 var(--d);text-transform:uppercase;margin-top:10px">No alcohol at the event.</div><div style="font:600 32px/1.25 var(--e);margin-top:12px">Under-18 entry allowed.</div></div></div>')
    return S(grid(cards, "repeat(4,1fr)", 2, 22), (K.eyebrow("Run of show"), K.title("The day, *hour* by hour")), c)


def s_photo_night(c):
    # user, 2026-11-26: five files, FOUR distinct photos (the two IMG_3824 HEICs are byte-identical pixels), so a four-frame layout: large crowd (caption card sits on it, not on faces), two upright frames, one wide frame
    return photo_story(c, 4, "1fr 1fr 1fr 1fr", 2, "Every corner worth a photo", "On the night", BL, spans=[(2, 2), (1, 1), (1, 1), (2, 1)],
                       files=["n28_d.jpg", "n28_b.jpg", "n28_c.jpg", "n28_a.jpg"], focus=["50% 62%", "50% 30%", "50% 45%", "50% 50%"])


def s_why(c):
    why = [("users", "Unique audience", "Access to a hard-to-reach youth demographic, with indirect reach into their parent and family networks.", G),
           ("heart", "Welfare motive", "Net proceeds are directed towards charity.", BL),
           ("megaphone", "Brand awareness", "Placement across signage, content and take-home merchandise that lasts beyond the event.", LM),
           ("eye", "Visibility", "Hundreds of Kolkata’s most engaged students in the room, and thousands more in our network.", G)]
    cards = [K.card(f'<span class="disc" style="background:{t};color:{core.text_on(t)}">{K.icon(ic, 30)}</span>'
                    f'<div style="flex:none"><div style="font:900 38px/1 var(--d);text-transform:uppercase;margin-bottom:14px;min-height:76px;display:flex;align-items:flex-end">{n}</div><div style="font:400 27px/1.3 var(--e);color:{INK2}">{d}</div></div>',
                    "kpi", "padding:30px 34px") for ic, n, d, t in why]
    left = f'<div style="width:1000px">{grid(cards, "1fr 1fr", 2, 22)}</div>'
    right = (f'<div style="flex:1;margin-left:44px;display:grid;grid-template-rows:1.25fr 1fr;gap:22px;min-height:0">'
             f'<div class="card" style="padding:18px;display:flex;align-items:center;justify-content:center;min-height:0"><img src="{asset_uri("mock_standee")}" style="max-height:100%;max-width:100%;border-radius:14px" alt=""><div class="mono" style="font-size:16px;color:{K.MUTE};margin-left:18px;width:120px">Your logo on the standee</div></div>'
             f'<div class="card" style="padding:18px;display:flex;align-items:center;justify-content:center;min-height:0"><img src="{asset_uri("mock_card")}" style="max-height:100%;max-width:70%;border-radius:14px" alt=""><div class="mono" style="font-size:16px;color:{K.MUTE};margin-left:18px;width:110px">Your logo on thank-you cards</div></div></div>')
    return S(left + right, (K.eyebrow("The fit"), K.title("Why this fits *you*")), c)


def _node(x, y, w, h, title_, sub, tone, big=False):
    fg = core.text_on(tone)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{tone};color:{fg};border-radius:24px;padding:0 28px;'
            f'display:flex;flex-direction:column;justify-content:center;box-shadow:0 18px 34px -24px rgba(10,10,10,.5)">'
            f'<div style="font:900 {44 if big else 34}px/1 var(--d);text-transform:uppercase">{title_}</div>'
            f'{f"<div class=mono style=font-size:15px;margin-top:10px;opacity:.75>{sub}</div>" if sub else ""}</div>')


def s_tiers(c):
    nodes = [("root", 0, 270, 340, 140, "Starry Night", "The event", "#FFFFFF", True),
             ("title", 460, 60, 390, 140, "Title sponsor", "Powered by", LM, True),
             ("co", 460, 400, 390, 140, "Co-sponsor", "Second billing", BL, True),
             ("assoc", 960, 270, 360, 124, "Associate sponsor", "Visible partner", G, False),
             ("media", 960, 520, 360, 124, "Media sponsor", "Content partner", G, False),
             ("hyd", 1420, 140, 308, 104, "Hydration", "Category exclusivity", K.PAPER, False),
             ("fash", 1420, 400, 308, 104, "Fashion", "Category exclusivity", K.PAPER, False)]
    pos = {n[0]: n for n in nodes}
    link = lambda a, b: (f'M{pos[a][1] + pos[a][3]},{pos[a][2] + pos[a][4] / 2} C{pos[a][1] + pos[a][3] + 70},{pos[a][2] + pos[a][4] / 2} '
                         f'{pos[b][1] - 70},{pos[b][2] + pos[b][4] / 2} {pos[b][1]},{pos[b][2] + pos[b][4] / 2}')
    paths = "".join(f'<path d="{link(a, b)}" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" opacity=".7"/>'
                    for a, b in [("root", "title"), ("root", "co"), ("co", "assoc"), ("co", "media"), ("assoc", "hyd"), ("assoc", "fash")])
    html = "".join(_node(x, y, w, h, t, sb, tone, big) for _, x, y, w, h, t, sb, tone, big in nodes)
    note = (f'<div style="position:absolute;left:1420px;top:630px;width:308px;font:400 22px/1.3 var(--e);color:#fff;opacity:.85">Category sponsors hold one exclusive category each. Partner and in-kind offerings sit alongside. All prices on request.</div>')
    body = f'<div style="position:relative;width:1728px;height:100%"><svg width="1728" height="720" style="position:absolute;left:0;top:0">{paths}</svg>{html}{note}</div>'
    return S(body, (K.eyebrow("Sponsorship"), K.title("Starry Night sponsorship *tiers*")), c)


def s_photo_tiers(c):
    return photo_story(c, 3, "1fr 1fr 1fr", 2, "Your brand, in the middle of it", "On the night", G, spans=[(1, 2), (2, 1), (2, 1)], files=["dd_night_1.jpg", "dd_night_2.jpg", "dd_night_3.jpg"])   # the Disco Diwali deck's pictures


def _check_list(items, dark=False, big=False):
    fs = "font-size:25px;" if big else ""
    return f'<ul class="ck" style="{fs}gap:{13 if big else 12}px">' + "".join(f"<li style='{fs}'>{K.icon('check', 26, K.GREEN_D if not dark else G, 2.4)}<span>{K.esc(i)}</span></li>" for i in items) + "</ul>"


TIER = [("Title sponsor", "Powered by", LM, []), ("Co-sponsor", "Second billing", BL, []), ("Associate sponsor", "Visible partner", G, [])]


def s_matrix(c):
    rows = [("Price", "On request", "On request", "On request"), ("Standee spots", "Exclusive, on the night", "Shared, on the night", "At the event"), ("Logo on creatives and banners", 1, 1, 1),
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
    P = [("Education partner", "school", G, ["Promotional standees at the venue", "Logo on creatives and banners", "5+ stories and interactions", "25+ Google reviews", "Exclusive Instagram post", "Webinar promotion on WhatsApp", "25+ story reshares", "Coupons and business cards"]),
         ("Media partner", "news", BL, ["Designated stall space at the venue", "Logo on creatives and banners", "Reel made for you, at your store or the event", "5+ stories and interactions", "Your offer posted on AQ’s WhatsApp and Instagram, sent by us", "30+ online reviews", "Offer coupons and business cards"])]
    cards = [K.card(f'<div style="display:flex;align-items:center;gap:18px"><span class="disc" style="background:{t};color:{core.text_on(t)}">{K.icon(ic, 30)}</span>'
                    f'<div style="font:900 40px/1 var(--d);text-transform:uppercase">{n}</div></div>'
                    f'<div style="margin-top:24px">{_check_list(it, big=True)}</div><div style="flex:1;min-height:120px;margin-top:22px">{real(f"dd_partner_{k}.jpg")}</div>',
                    "", "display:flex;flex-direction:column;padding:34px 40px") for k, (n, ic, t, it) in enumerate(P, 1)]
    return S(grid(cards, "1fr 1fr", None, 28), (K.eyebrow("Partnership offerings"), K.title("Education and media *partners*")), c)


def s_inkind(c):
    P = [("Media", "news", G, ["Logo on creatives and banners", "Social media collaborations", "50+ Google and social reviews"]),
         ("Stationery", "pencil", LM, ["Logo on creatives and banners", "10+ stories and interactions"]),
         ("Gift", "gift", BL, ["Logo on creatives and banners", "10+ stories and interactions", "Samples gifted to all winners"])]
    cards = [K.card(f'<div style="display:flex;align-items:center;gap:18px"><span class="disc" style="background:{t};color:{core.text_on(t)}">{K.icon(ic, 30)}</span>'
                    f'<div style="font:900 44px/1 var(--d);text-transform:uppercase">{n}</div></div><div style="margin-top:24px">{_check_list(it, big=True)}</div>'
                    f'<div style="flex:1;min-height:150px;margin-top:24px">{real(f"dd_inkind_{k}.jpg")}</div>', "", "display:flex;flex-direction:column;padding:34px 36px") for k, (n, ic, t, it) in enumerate(P, 1)]
    return S(grid(cards, "1fr 1fr 1fr", None, 24), (K.eyebrow("In-kind"), K.title("Other in-kind *partnerships*")), c)


def s_stalls(c):
    ben = [("pin", "Spots we know you’ll love"), ("wand", "Basic amenities and support"), ("megaphone", "Dedicated shoutouts"), ("store", "Ample stall space"),
           ("users", "Connect directly with your audience"), ("target", "Benefit from high footfall at the event"), ("eye", "Showcase your brand to a real audience"), ("megaphone", "Marketing and coverage")]
    tiles = [K.card(f'<span class="disc" style="background:{TONES[i % 3]};color:{core.text_on(TONES[i % 3])};width:64px;height:64px">{K.icon(ic, 30)}</span>'
                    f'<div style="font:600 25px/1.2 var(--e)">{t}</div>', "", "display:flex;align-items:center;gap:20px;padding:18px 26px") for i, (ic, t) in enumerate(ben)]
    left = f'<div style="width:640px;display:grid;grid-template-rows:1.1fr 1fr 1fr;gap:20px;min-height:0">{real("n35_a.jpg", "50% 64%")}{real("n35_b.jpg", "35% 40%")}{real("n35_c.jpg", "55% 38%")}</div>'   # slots 35.1-3 FILLED (user, 2026-11-26), in the order sent
    right = f'<div style="flex:1;margin-left:40px;min-height:0">{grid(tiles, "1fr 1fr", 4, 18)}</div>'
    return S(left + right, (K.eyebrow("Stall space"), K.title("Stall space at the *location*")), c)


def s_join(c):
    cells = [f'<div style="min-height:0">{real(f"dd_join_{k}.jpg")}</div>' for k in range(1, 6)]   # the Disco Diwali deck\'s five pictures
    body = (f'<div style="position:relative;width:100%;height:100%">{grid(cells, "repeat(5,1fr)", None, 18)}'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:{G};color:{INK};border-radius:80px;padding:40px 96px;'
            f'box-shadow:0 30px 60px -30px rgba(0,0,0,.6)"><div style="font:900 190px/.9 var(--d);text-transform:uppercase;text-align:center">Join<br>us</div></div></div>')
    return S(body, None, c, body_style="margin-top:0")


def s_close(c):
    ct, rg = FACTS["contact"], FACTS["reg"]
    qr = K.uri("../terrathon/qr_instagram_ngo_aquaterra.svg")
    row = lambda ic, t: f'<div style="display:flex;align-items:center;gap:20px;font:600 32px var(--e)">{K.icon(ic, 36, K.GREEN_D)}<span>{K.esc(t)}</span></div>'
    photo_c = f'<div style="width:520px;flex:none">{real("s10_e.jpg", "50% 50%")}</div>'   # slot 37.1 FILLED (user, 2026-11-26): the two volunteers in AquaTerra shirts, same file as slide 10's first photo
    touch = K.card(f'<div class="mono" style="font-size:16px;color:{K.MUTE};margin-bottom:22px">Get in touch</div>'
                   f'<div style="font:900 78px/.95 var(--d);text-transform:uppercase;margin-bottom:10px">{K.esc(ct["name"])}</div><div style="font:600 30px/1.2 var(--e);color:{INK2};margin-bottom:30px">{K.esc(ct["role"])}</div>'
                   f'<div style="display:flex;flex-direction:column;gap:22px">{row("phone", ct["phone"])}{row("insta", ct["insta"])}{row("globe", ct["web"])}{row("mail", ct["mail"])}</div>',
                   "", "padding:44px 52px;flex:1;display:flex;flex-direction:column;justify-content:center")
    reg = K.card(f'<div class="mono" style="font-size:16px;color:{K.MUTE};margin-bottom:18px">Registration</div>'
                 f'<div style="display:flex;flex-direction:column;gap:14px;align-items:flex-start">{K.chip(rg["tax"], G, size=26)}'
                 f'{K.chip("80G approval no. " + rg["darpan"], BL, "#fff", 20)}'
                 f'<div style="font:400 23px/1.3 var(--e);color:{INK2}">{K.esc(rg["trust"])}.</div></div>', "", "padding:30px 34px")
    qrc = K.card(f'<img src="{qr}" style="width:150px;border-radius:10px;flex:none" alt="QR code for @ngo.aquaterra"><div><div style="font:900 34px/1 var(--d);text-transform:uppercase">Follow the work</div>'
                 f'<div class="mono" style="font-size:16px;color:{K.MUTE};margin-top:10px">@ngo.aquaterra</div></div>', "", "padding:24px 30px;display:flex;align-items:center;gap:24px")
    body = f'<div style="display:flex;gap:24px;width:100%;min-height:0">{photo_c}{touch}<div style="width:520px;display:flex;flex-direction:column;gap:24px">{reg}{qrc}</div></div>'
    return S(body, (K.eyebrow("Let’s talk"), K.title("Get in *touch*")), c)


ORDER = [s_cover, s_about, s_glance, s_different, s_vision, s_welfare, s_impact, s_growth, s_events, s_proof, s_notoneoff, s_series_diwali, s_series_starry, s_photo_summer, s_photo_diwali25, s_photo_starry25, s_photo_sports,
         s_sponsors, s_feedback, s_photo_energy, s_flagship, s_demo, s_community, s_reach, s_promote, s_offline, s_run, s_photo_night, s_why, s_tiers, s_photo_tiers, s_matrix, s_partners, s_inkind,
         s_stalls, s_join, s_close]
TONE_OF = {"s_cover": "black", "s_about": "cream", "s_glance": "purple", "s_different": "black", "s_vision": "orange", "s_welfare": "black", "s_impact": "blue", "s_growth": "purple",
           "s_events": "cream", "s_proof": "black", "s_notoneoff": "green", "s_series_diwali": "orange", "s_series_starry": "purple", "s_photo_summer": "black", "s_photo_diwali25": "black", "s_photo_starry25": "black",
           "s_photo_sports": "black", "s_sponsors": "cream", "s_feedback": "cream", "s_photo_energy": "black", "s_flagship": "purple", "s_demo": "green", "s_community": "blue", "s_reach": "black",
           "s_promote": "black", "s_offline": "black", "s_run": "black", "s_photo_night": "black", "s_why": "green", "s_tiers": "black", "s_photo_tiers": "black", "s_matrix": "cream",
           "s_partners": "cream", "s_inkind": "cream", "s_stalls": "cream", "s_join": "cream", "s_close": "cream"}


async def main(which):
    os.makedirs(OUT, exist_ok=True)
    total = len(ORDER)
    async with B.session(scale=1):
        probe = await B.measure_text([{"text": "STARRY NIGHTS", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"}], K.W, K.H)
        COVER_SIZE[0] = int(100 * 1070 / probe[0]["text_w"])           # the white box ends before the chip column (x ~1340)
        print("cover box size", COVER_SIZE[0])
        for i in which:
            fn = ORDER[i - 1]; CUR[0], CUR[1] = i, 0
            await B.render(fn(Ctx(i, total, TONE_OF.get(fn.__name__))), f"{OUT}/slide_{i:02d}.png", K.W, K.H, page_bg=K.BG)
    if len(which) == total:
        pages = [Image.open(f"{OUT}/slide_{n:02d}.png").convert("RGB") for n in range(1, total + 1)]
        pages[0].save(f"{OUT}/starry_night_sponsors_cold.pdf", save_all=True, append_images=pages[1:], resolution=96, quality=90)
        print("pdf written", total, "pages")


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or list(range(1, len(ORDER) + 1))
    asyncio.run(main(which))
