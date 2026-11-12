"""Shared kit for the AQ recruitment campaign (Nov 2026). Import as `import recruit_kit as K` from any script in scratchpad/.

It carries the CAMPAIGN CONSTANTS so that 20 pieces built from 20 different style recipes still read as one campaign:
  * the (just a student) tab, top right      -> K.series_tab()
  * a lane chip in the department colour    -> K.lane_chip("events")
  * the logo, top left                       -> K.logo()  /  K.logo_pill() on photos
  * the exit, ngoaquaterra.com/recruitment   -> K.url_pill() / K.footer()
  * photos: always real AQ photos            -> K.PH (named), K.contact() to browse a folder
and the helpers the earlier waves already proved (cover/mono/posterise/dither, text, boxes, glass, doodles).

    K.render("events_1", html, H=1350)    # writes out/recruit_nov2026/v4/events_1.png + .jpg preview, runs the render gate
"""
import os, sys, asyncio, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_recruit_v2 as V          # chdirs to the repo root and loads the engine modules
import gen_recruit_v3 as T          # the five reference formats from the earlier waves (hero, cast, blank, note, site, chat)

core, B, dd, shapes = V.core, V.B, V.dd, V.shapes
def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(V.ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
tex = _load("tex"); lay = _load("layout")

W = 1080
INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
URL = "ngoaquaterra.com/recruitment"
OUT = "out/recruit_nov2026/v4"
IMG = V.IMG                      # "engine/assets/img/"

# The eight departments and their colours (the Social team's own "this week at AQ" slides use exactly this code).
LANE = {
    "events":   ("events", SKY),
    "welfare":  ("welfare", MINT),
    "crftd":    ("crftd", TOM),
    "shikshaq": ("shikshaq", LEM),
    "social":   ("social media", GRAPE),
    "blogs":    ("blogs", GRAPE),
    "collabs":  ("collabs", PINK),
    "hr":       ("hr", TEAL),
    "all":      ("aquaterra", PAPER),     # connectors that belong to every lane
}

# Re-exported helpers (all proven in the earlier waves)
cover, uri, mono, posterise, dither, hexrgb = V.cover, V.uri, V.mono, V.posterise, V.dither, V.hexrgb
box, t, img, stick, mw = V.box, V.t, V.img, V.stick, V.mw
glass, pill = T.glass, T.pill
logo_pill = V.logo_pill

def series_tab(y=58):            return T.series_tab(y)
def lane_chip(dept, x=64, y=116, label=None):
    lab, col = LANE[dept]
    return T.lane_chip(label or lab, col, x, y)

def logo(x=64, y=48):            return B.logo(dark=False, x=x, y=y)

def url_pill(x=64, y=1188, w=952, bg=INK, fg=LEM, size=34):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:84px;background:{bg};border-radius:999px;z-index:20"></div>'
            + V.t(URL, x + 40, y + 22, size, color=fg, font="m", weight=700, ls=.02, z=21, upper=False, tag="url"))

def footer(H=1350, color="var(--ink3)"):
    return (f'<span class="measure" data-tag="footer" style="position:absolute;left:64px;top:{H-96}px;font-family:var(--m);font-weight:700;font-size:15px;'
            f'letter-spacing:.06em;color:{color};z-index:20">@ngo.aquaterra &nbsp;·&nbsp; {URL}</span>')

def page(inner, H=1350, bg=CREAM):
    return B.page(W, H, bg, inner, grain=False)

def doodle(kind, x, y, size, color, rot=0, z=9):
    return V.dood(kind, x, y, size, color, rot, z)

# ---- photos (all real AQ photos, tracked in git, owner permission given for every frame including children) ----
def ph(rel): return rel          # K.cover(K.PH["..."], w, h) takes a path relative to engine/assets/img/
_E = "events/"; _W = "events/welfare-feed-2026/"
PH = {
    # events
    "vendor": _E + "nandu-jee/01_nandu-jee-googly-eyes.jpg", "desk": _E + "summer-aq-turns-five/01_registration-desk.jpg",
    "five_banner": _E + "summer-aq-turns-five/05_five-banner-net.jpg", "five_group": _E + "summer-aq-turns-five/07_group-portrait-pink-light.jpg",
    "five_gossip": _E + "summer-aq-turns-five/02_gossip-board.jpg", "dd_floor_green": _E + "unsorted-2026-10-07/11_dance-green-light-portrait.jpg",
    "dd_booth": _E + "unsorted-2026-10-07/10_disco-diwali-photo-booth.jpg", "dd_group": _E + "unsorted-2026-10-07/01_IMG_7180_group-aquaterra-banner.jpg",
    "dd_blue": _E + "unsorted-2026-10-07/07_dance-blur-blue-light.jpg", "dd_stage": _W + "30_disco-diwali-2-stage.png",
    "dd_faces_green": _E + "disco-diwali-hall-2026-10-14/05_boys-crowd-green-light.jpg", "dd_dhol": _E + "disco-diwali-dhol/01_live-dhol-pink-turban.jpg",
    "dd_charms": _E + "disco-diwali-charms/01_charm-trays-crop.jpg",
    # welfare
    "dog_bhowanipur": _W + "08_dog-drive-bhowanipur.jpg", "dog_night": _W + "06_dog-drive-night-volunteers.webp", "dog_biscuit": _W + "04_dog-biscuits-pat.webp",
    "dog_saltlake": _W + "27_dog-biscuit-salt-lake.jpg", "cow_biscuit": _W + "16_cow-biscuit-dobson.png", "street_dog": _W + "07_street-tree-dog.webp",
    "sundarbans": _W + "09_sundarbans-sunset-group.png", "teach_abc": _W + "10_teaching-abc-board.jpg", "teach_board": _W + "03_disha-volunteer-blackboard.webp",
    "teach_class": _W + "05_disha-grammar-class-wide.webp", "art_table": _W + "11_art-workshop-table.jpg", "holi": _W + "24_holi-workshop.jpg",
    "green_talk": _W + "28_green-talk-group.jpg", "fable": _W + "29_fable-factory-storytelling.jpg", "sharbat_cup": _W + "17_sharbat-cup-teghoria.jpg",
    "sharbat_jar": _W + "02_sharbat-jar-bottles.webp", "sharbat_stall": _W + "01_sharbat-stall-volunteers.webp", "sharbat_bananas": _W + "18_sharbat-bananas-north-park.jpg",
    "bananas_group": _W + "14_food-for-all-bananas.jpg", "clothes_pile": _W + "19_wear-and-share-clothes-pile.jpg", "plant": _W + "20_plantation-planting.jpg",
    "plant_school": _W + "21_plantation-school-group.jpg", "old_age": _W + "22_old-age-home.jpg", "books": _W + "23_book-basket.jpg",
    "cookie": _W + "25_cookie-pass-on.jpg", "smile_notes": _W + "26_smile-notes.png", "emami": _W + "15_emami-science-city-lineup.png",
    # crftd (formerly ROOTS)
    "tee_novus": _W + "12_roots-stall-novus-tee.jpg", "tee_morpheus": _W + "13_roots-stall-morpheus-tee.jpg",
    "tee_confluence": _W + "31_roots-stall-confluence-tee.jpg", "tee_concord": _W + "32_roots-stall-concord-tee.jpg",
    # blogs (real student cover art)
    "blog_mirror": _W + "blog-people-in-the-mirror.jpg", "blog_dynamics": _W + "blog-dynamics.jpg", "blog_barks": _W + "blog-he-barks-i-heal.jpg",
    "blog_opinions": _W + "blog-voicing-opinions.jpg", "blog_city": _W + "blog-letter-to-my-city.jpg", "blog_tea": "blog/cover-1.jpg",
    "blog_nostalgia": "blog/cover-2.jpg", "blog_syntax": "blog/cover-3.jpg", "blog_judge": "blog/cover-4.jpg", "blog_empathy": "blog/cover-5.jpg",
    "blog_pebbles": "blog/cover-6.jpg",
    # core embedded photos
    "food": "food-distribution.jpeg", "edu": "education-sundarban.jpeg", "diwali": "fundraising-diwali.jpeg", "xmas": "christmas-khidirpur.jpeg",
}
# the Social team's own published slides (real designs, real voice): engine/assets/img/social/this-week-at-aq-01..16.png|jpg
def social_slide(n):
    base = IMG + "social/this-week-at-aq-%02d." % n
    for ext in ("png", "jpg"):
        if os.path.exists(base + ext): return "social/this-week-at-aq-%02d.%s" % (n, ext)
    raise FileNotFoundError(base)

def contact(folder, out, tile=240, cols=8):
    """Make a labelled contact sheet of a folder under engine/assets/img/ so you can LOOK at what is there. Read the PNG afterwards."""
    from PIL import Image, ImageDraw
    d0 = IMG + folder
    fs = sorted(f for f in os.listdir(d0) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    rows = (len(fs) + cols - 1) // cols
    S = Image.new("RGB", (cols * tile, rows * (tile + 16)), "white"); d = ImageDraw.Draw(S)
    for i, f in enumerate(fs):
        im = Image.open(os.path.join(d0, f)).convert("RGB"); im.thumbnail((tile, tile))
        x, y = (i % cols) * tile, (i // cols) * (tile + 16)
        S.paste(im, (x, y + 16)); d.text((x + 2, y + 2), f[:30], fill="black")
    S.save(out, quality=82); return out

# ---- real facts (counted, with the qualifier that must travel with them). Do not invent any number outside this table. ----
FACTS = {
    "members": "1,400+ students aged 14 to 19 (site)", "drives": "540+ drives, workshops and events since 2021 (site)",
    "saplings": "4,000+ saplings (site)", "trips": "8 Sundarbans trips (site)", "bananas": "15,000+ bananas (site)",
    "founded": "June 2021, by 16 students (site)", "money": "zero donations; students earn what they spend (site)", "fees": "zero fees, unpaid, no experience needed (site)",
    "tails": "Tails and Treats, stray-dog feeding: 53 numbered editions, first logged January 2022 (platform)",
    "sharbat": "Sharbat Seva: 33 editions May 2024 to May 2025; up to 20 L of Rooh Afza in one round (platform)",
    "grow": "Grow Green plantation: 26 editions since July 2021; 100 saplings in one round (platform)",
    "food": "Food For All: 17 editions; 5,400 bananas in one round (platform)", "wear": "Wear and Share clothes drive: 22 editions; Book Basket: 16; Wear & Write: 15; Respect and Reach (old age home): 8",
    "smile": "Smile Notes Campaign 2026: 100 affirmation notes and 100 toffees per round",
    "sundarbans": "Sunderbans 8.0, December 2025: 120+ checkups, 25K worth of medicines and stationery",
    "emami": "AQ x Vishwajagriti and Emami collab at Science City: 300 stationery kits, 30 kids hosted",
    "dd2": "Disco Diwali 2.0 (Oct 2025): 550 registrations, 10+ small businesses; Disco Diwali Masquerade Sangeet Edition, 10 November 2026",
    "crftd_stalls": "Crftd (formerly ROOTS) school-fest stalls: Novus 300 walk-ins; Confluence 300 and 250; Concord 200 and 250; Morpheus 300 and 350 (platform). Every rupee of profit funds a welfare drive (site)",
    "teaching": "about 70% of welfare activity is teaching workshops; Pather Sathi Sunday School, 65+ children, running 2.5 years",
    "shikshaq": "ShikshAQ tutor search: 11 days before, under 48 hours after launch; 50+ verified tutor profiles at launch; zero commission (launch research, scoped)",
    "places": "205 distinct locations across 558 logged projects, June 2021 to September 2026 (platform)",
    "events_list": "Paradox 3.0 (June 2025, 300 attendees), Disco Diwali 1.0 Oct 2024 and 2.0 Oct 2025, Starry Night Dec 2024, TerraThon, TerraMUN",
    "loop": "~90% of revenue is fundraising events (80% tickets, 20% sponsorship), ~10% Crftd, 0% individual donations",
    "points": "welfare points: 1 per volunteering activity, redeemable for discounted Crftd merch and event entry; certificates and LORs issued by HR for people who do the work",
}

def contrast_ok(fg, bg, large=False):
    return core.contrast(fg, bg) >= (core.AA_LARGE if large else core.AA_NORMAL)

# ---- rendering ----
async def _render(name, html, H, elements, text_pairs, **kw):
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        await B.render(html, f"{OUT}/{name}.png", W, H, elements=elements, text_pairs=text_pairs, page_bg="var(--bg)", **kw)
    from PIL import Image
    im = Image.open(f"{OUT}/{name}.png").convert("RGB"); im.thumbnail((1080, 1920)); im.save(f"{OUT}/{name}.jpg", quality=88)

def render(name, html, H=1350, elements=None, text_pairs=None, **kw):
    """Render + gate. Then READ out/recruit_nov2026/v4/<name>.jpg and run the looking gate (CLAUDE.md section 3)."""
    V.H = H
    asyncio.run(_render(name, html, H, elements, text_pairs, **kw))
    print("rendered", f"{OUT}/{name}.jpg")
    return f"{OUT}/{name}.jpg"

def style_brief(style_id):
    """Print the judged recipe for a style from the 74-reference bank and the path of its reference image to LOOK at."""
    import json
    ent = json.load(open("brain/STYLE_BANK.json"))["styles"]
    k = [x for x in ent if x.startswith(style_id)][0]; e = ent[k]
    print("REFERENCE IMAGE:", "training_samples/reference_posters/" + e["file"])
    print("KIND/HERO/CANVAS:", e["kind"], e["hero"], e["canvas"]); print("MECHANISM:", e["mechanism"]); print("RECIPE:", e["recipe"])
