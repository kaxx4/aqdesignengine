"""TerraThon Mini-Fete MARKETING CAROUSEL: "7 reasons to show up" (feed 1080x1350 AND story 1080x1920 from one brief).

Structure taken from the Paradox "13 reasons why" template (training_samples/terrathon/paradox_13_reasons_template.png):
cover -> one slide per reason (a circular hero, headline, one-line wink) -> close. LOOK is TerraThon's (user ruling: black vibes):
black ground, the tilted white slab with orchid border, the four shuriken, the real sticker kit, StretchPro/Sigmar One where the
posters use them. The hero is TUCKED behind the slab exactly like the event posters' hero.

User rulings folded in (2026-09-29): no sponsor strip; footer is JUST the AQ logo and "ALL FOR CHARITY"; the hero of each reason slide is a
STICKER from the kit ("go, use stickers in the circles"). If a real photo named after the slide key exists in
engine/assets/terrathon/carousel_photos/ (mini_games.jpg ...), that photo replaces the sticker inside a circle instead.
CTA is the WhatsApp group (link in bio / caption, never on the image).

Adaptations (CLAUDE.md sec 2 rule 4): stories keep the top ~250px and bottom ~260px free of key content (Instagram UI);
character stickers are recoloured (the brand does this: the carnival pile has a green flower and a blue smiley) so seven slides get seven distinct
stickers from a kit of four objects; copy is DRAFT for the user's approval.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_carousel.py [feed|story ...]
"""
import asyncio, base64, importlib.util, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, np, Image = tt.core, tt.B, tt.np, tt.Image
GROUND, ORCHID, CREAM_HALO, SLAB, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL
GREEN = (47, 210, 132)
PHOTO_DIR = "engine/assets/terrathon/carousel_photos"

DATE, VENUE = "3RD & 4TH OCTOBER, 2026", "TURF XL, NEW ALIPORE"
REASONS = [   # key, headline, tagline, sticker file, recolour-orchid-to-green?   (DRAFT copy; vendor facts confirmed by the user 2026-09-29)
    ("mini_games", "MINI-GAMES", "WIN STUFF. TALK TRASH.", "controller.png", False),
    ("photobooth", "PHOTOBOOTH", "POSE NOW. REGRET NEVER.", "smiley.png", False),
    ("artily", "ARTILY", "SIP BOBA. LOSE MINI-GAMES WITH DIGNITY.", "flower.png", False),
    ("cravella", "CRAVE'LLA", "DESSERTS AND BROWNIES. NO FURTHER QUESTIONS.", "flower.png", True),
    ("crftd", "CRFTD ORDERS", "PRE-ORDER DIY T-SHIRTS AND CUSTOM ORDERS.", "smiley.png", True),
    ("lottery", "LOTTERY AT LOCATION", "LUCK HAS A STALL TOO.", "basketball.png", False),
    ("dd_tickets", "DD TICKET STALL", "YOUR PASS TO THE PARTY IS ONE STALL AWAY.", "carnival.png", False),
]
KNOW = [   # the "all you need to know" deck: ONLY facts the user gave (timings, directions and rules are still missing and are NOT invented)
    ("when", "WHEN", "3RD AND 4TH OCTOBER, 2026.", "flower.png", False),
    ("where", "WHERE", "TURF XL, NEW ALIPORE.", "smiley.png", False),
    ("who", "WHO CAN COME", "OPEN TO ALL. BRING YOUR PEOPLE.", "smiley.png", True),
    ("what", "WHAT'S ON", "MINI-GAMES AND COMPETITIONS. WIN STUFF.", "controller.png", False),
    ("stalls", "STALLS TO ENJOY", "ARTILY BOBA. CRAVE'LLA DESSERTS AND BROWNIES. CRFTD PRE-ORDERS.", "flower.png", True),
    ("extras", "PHOTOBOOTH + LOTTERY", "POSE NOW. LUCK HAS A STALL TOO.", "basketball.png", False),
    ("dd", "DISCO DIWALI PASSES", "GET YOURS AT THE DD TICKET STALL.", "carnival.png", False),
    ("why", "ALL FOR CHARITY", "SHOW UP. HAVE FUN. DO GOOD.", "flower.png", False),
]
DD = [   # Disco Diwali ticket sales. FACTS ONLY: passes are sold at the DD ticket stall at the Mini-Fete (3rd & 4th Oct, Turf XL). No price, no DD date/venue: not supplied.
    ("where", "WHERE", "THE DD TICKET STALL, TURF XL, NEW ALIPORE.", "smiley.png", False),
    ("when", "WHEN", "3RD AND 4TH OCTOBER, 2026.", "flower.png", False),
    ("between", "GRAB IT BETWEEN THE FUN", "MINI-GAMES, BOBA, BROWNIES. PICK UP YOUR PASS ON THE WAY.", "controller.png", False),
    ("cause", "A PARTY FOR A CAUSE", "DISCO DIWALI IS ALL FOR CHARITY.", "flower.png", True),
    ("crew", "OPEN TO ALL", "COME ALONE OR BRING THE WHOLE CREW.", "smiley.png", True),
    ("last", "DON'T SLEEP ON IT", "THE MINI-FETE ENDS ON THE 4TH.", "basketball.png", False),
]
TIMED = [   # single stories, no cover or close
    ("tomorrow", "DD PASSES ON SALE TOMORROW", "AT THE DD TICKET STALL. TURF XL, 3RD OCT.", "carnival.png", False),
    ("today", "DD PASSES ON SALE TODAY", "AT THE DD TICKET STALL. TURF XL, NEW ALIPORE.", "carnival.png", False),
    ("lastday", "LAST DAY AT THE FETE", "GET YOUR DD PASS AT THE DD TICKET STALL, TURF XL.", "carnival.png", False),
]
DECKS = {"reasons": dict(items=REASONS, head=("7 REASONS", "TO SHOW UP"), swipe="SWIPE FOR THE 7"),
         "know": dict(items=KNOW, head=("ALL YOU NEED", "TO KNOW"), swipe="SWIPE FOR THE LOWDOWN"),
         "dd": dict(items=DD, head=("DISCO DIWALI", "PASSES ON SALE"), swipe="SWIPE FOR THE DEETS", close=("GET YOUR PASS", "AT THE DD TICKET STALL", "TURF XL, NEW ALIPORE")),
         "ddtimed": dict(items=TIMED, head=("", ""), swipe="", bare=True)}
DECK = DECKS["reasons"]
N = len(REASONS)

LAYOUT = {   # canvas px. story keeps Instagram's UI zones clear (top 250, bottom 260)
    "feed":  dict(W=1080, H=1350, hero_max=(700, 520), slab_top=640, slab_h=430, strip_y=1102, foot_y=1235,
                  cover_head_y=52, cover_hero_top=290, cover_hero_h=540, cover_slab_top=744, cover_slab_h=340, cover_strip_y=1130, pill_y=53),
    "story": dict(W=1080, H=1920, hero_max=(760, 660), slab_top=980, slab_h=470, strip_y=1490, foot_y=1585,
                  cover_head_y=280, cover_hero_top=540, cover_hero_h=680, cover_slab_top=1128, cover_slab_h=340, cover_strip_y=1492, pill_y=250),
}


def recolor(im, src=(222, 104, 240), dst=GREEN, tol=70):
    """Swap the orchid fill for green, keeping the print grain (delta from src is carried over)."""
    a = np.array(im.convert("RGBA")).astype(int)
    d = np.sqrt(((a[..., :3] - np.array(src)) ** 2).sum(-1))
    m = (d < tol) & (a[..., 3] > 20)
    a[..., :3][m] = np.clip(np.array(dst) + (a[..., :3][m] - np.array(src)) * 0.6, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def sticker_src(name, recolour=False):
    im = Image.open(f"{tt.ASSET}/{name}").convert("RGBA")
    if recolour: im = recolor(im)
    ys, xs = np.where(np.array(im)[..., 3] > 20)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    buf = io.BytesIO(); im.save(buf, "PNG")
    return im, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def photo_src(key):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = f"{PHOTO_DIR}/{key}.{ext}"
        if os.path.exists(p):
            mime = "image/png" if ext == "png" else "image/webp" if ext == "webp" else "image/jpeg"
            return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
    return None


async def slide(kind, canvas, out, idx=None):
    L = LAYOUT[canvas]; W, H = L["W"], L["H"]
    els = []
    def el(label, x, y, w, h): els.append((label, x, y, w, h))

    def put(src, label, x, y, w, h, z):
        el(label, x, y, w, h)
        return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">')

    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * H / 1350)))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    slab_top, slab_h = (L["cover_slab_top"], L["cover_slab_h"]) if kind == "cover" else (L["slab_top"], L["slab_h"])
    SX, SW = 47, 986
    ST_F = tt.ST_FEAT

    # ---- measure every fitted string, in its real face ----
    items = []
    if kind == "point":
        head = DECK["items"][idx][1]
        items = [dict(text=head, font="d", size=100, weight=900)]
    elif kind == "close":
        items = [dict(text=max(DECK.get("close", ("", "WHATSAPP GROUP", ""))[:2], key=len), font="d", size=96, weight=900)]
    elif kind == "cover":
        items = [dict(text="TERRATHON", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=ST_F),
                 dict(text="MINI-FEETE", font="StretchPro", size=100, weight=400, letter_spacing="-0.02em", features=ST_F),
                 dict(text=DECK["head"][0], font="d", size=124, weight=900), dict(text=DECK["head"][1], font="d", size=80, weight=400)]
    m = await B.measure_text(items, extra_css=tt.FONT_CSS) if items else []

    # ---- hero (tucked ~14% behind the slab) ----
    if kind == "point":
        key, _, _, sfile, rc = DECK["items"][idx]
        ph = photo_src(key)
        if ph:   # a real photo replaces the sticker, inside a circle
            D = 560; cx, cy = W / 2, slab_top - 0.86 * D + D / 2
            parts.append(f'<div class="measure" data-tag="hero" style="position:absolute;left:{cx - D / 2}px;top:{cy - D / 2}px;width:{D}px;height:{D}px;'
                         f'border-radius:50%;border:14px solid {CREAM_HALO};background:{CREAM_HALO};z-index:3;overflow:hidden">'
                         f'<img src="{ph}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;display:block"></div>')
            el("hero", cx - D / 2, cy - D / 2, D, D)
        else:
            im, src = sticker_src(sfile, rc); mw, mh = L["hero_max"]
            k = min(mw / im.width, mh / im.height); w, h = im.width * k, im.height * k
            parts.append(put(src, "hero", (W - w) / 2, slab_top - 0.86 * h, w, h, 3))
    elif kind == "cover":
        im, src = sticker_src("carnival.png"); ch = L["cover_hero_h"]; w = ch * im.width / im.height
        parts.append(put(src, "hero", (W - w) / 2, L["cover_hero_top"], w, ch, 3))
    else:
        im, src = sticker_src("smiley.png"); mw, mh = L["hero_max"]
        k = min(mw / im.width, mh / im.height); w, h = im.width * k, im.height * k
        parts.append(put(src, "hero", (W - w) / 2, slab_top - 0.86 * h, w, h, 3))

    # ---- stars (constant furniture) + fest pill ----
    def star(label, x, y, z):
        _, src = sticker_src("shuriken.png"); parts.append(put(src, label, x, y, 100, 100, z))
    star("star_tl", 42, 53 if canvas == "feed" else 270, 5)
    star("star_tr", 946, slab_top - 330, 5)
    star("star_ml", 19, slab_top - 52, 9)
    star("star_br", 970, slab_top + slab_h - 95, 9)
    if kind != "cover":
        pw, ph_, px_, py_ = 254, 81, 809, L["pill_y"]
        el("fest_pill", px_, py_, pw, ph_)
        parts.append(f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{px_}px;top:{py_}px;width:{pw}px;height:{ph_}px;'
                     f'border:6px solid {ORCHID};border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;z-index:7;'
                     f'font-family:var(--d);font-weight:900;font-size:31px;color:{INK}">TERRATHON</div>')

    # ---- cover header ----
    if kind == "cover":
        hy = L["cover_head_y"]; w1, w2 = m[2]["text_w"], m[3]["text_w"]
        kf = min(1.0, 700 / w1); f1, f2 = 124 * kf, 80 * kf; w1, w2 = w1 * kf, w2 * kf      # a long header shrinks so it clears the corner star
        parts.append(f'<div class="measure" data-tag="c_head1" style="position:absolute;left:{(W - w1) / 2}px;top:{hy}px;font-family:var(--d);font-weight:900;'
                     f'font-size:{f1}px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">{DECK["head"][0]}</div>'
                     f'<div class="measure" data-tag="c_head2" style="position:absolute;left:{(W - w2) / 2}px;top:{hy + 118 * kf}px;font-family:var(--d);font-weight:400;'
                     f'font-size:{f2}px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">{DECK["head"][1]}</div>')
        el("c_head1", (W - w1) / 2, hy + 10, w1, 100); el("c_head2", (W - w2) / 2, hy + 128, w2, 64)

    # ---- slab content (flex-centred: no border-offset arithmetic) ----
    if kind == "cover":
        t_px = 100 * 620 / m[0]["text_w"]; b_px = 100 * 830 / m[1]["text_w"]
        stx = lambda px_, sk=tt.ST_STROKE, ls=tt.ST_LS: (f'font-family:StretchPro;font-weight:400;-webkit-text-stroke:{sk * px_}px {INK};letter-spacing:{ls}em;'
                           f'font-feature-settings:{ST_F};font-size:{px_}px;line-height:1.05')
        body = (f'<div style="{stx(t_px)}">TERRATHON</div><div style="{stx(b_px, 0.03, -0.02)};margin-top:6px">MINI-FEETE</div>'
                f'<div style="font-family:var(--d);font-weight:400;font-size:38px;line-height:1.15;margin-top:14px">{DATE.replace("&", "&amp;")}</div>')
    elif kind == "point":
        tag = DECK["items"][idx][2]
        words = head.split(); two = m[0]["text_w"] * 1.04 > 840 and len(words) > 2   # wider than the slab at full size: two lines
        if two:
            cut = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
            hl = [" ".join(words[:cut]), " ".join(words[cut:])]
            mm = await B.measure_text([dict(text=t, font="d", size=100, weight=900) for t in hl])
            head_px = min(104, 100 * 840 / max(r["text_w"] for r in mm))
            head_html = f'<div>{hl[0]}</div><div>{hl[1]}</div>'
        else:
            head_px = min(104, 100 * 840 / m[0]["text_w"]); head_html = head.replace("&", "&amp;")
        body = (f'<div style="font-weight:900;font-size:{head_px}px;line-height:1">{head_html}</div>'
                f'<div style="font-weight:400;font-size:40px;line-height:1.15;margin-top:18px;max-width:800px;text-wrap:balance">{tag}</div>')
    else:
        c1, c2, c3 = DECK.get("close", ("JOIN THE", "WHATSAPP GROUP", "LINK IN BIO"))
        cf = 96 * min(1.0, 800 / m[0]["text_w"])
        body = (f'<div style="font-weight:900;font-size:{cf}px;line-height:1">{c1}</div>'
                f'<div style="font-weight:900;font-size:{cf}px;line-height:1">{c2}</div>'
                f'<div style="font-weight:400;font-size:40px;line-height:1.15;margin-top:16px">{c3}</div>')
    el("slab", SX - 6, slab_top - 12, SW + 12, slab_h + 24)
    parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{slab_top}px;width:{SW}px;height:{slab_h}px;'
                 f'transform:rotate(-1.25deg);background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;display:flex;flex-direction:column;'
                 f'align-items:center;justify-content:center;text-align:center;font-family:var(--d);color:{INK};white-space:nowrap">{body}</div>')

    # ---- strip under the slab ----
    strip = {"cover": DECK["swipe"], "point": f"{DATE}  |  {VENUE}", "close": f"{DATE}  |  {VENUE}"}[kind]
    sfs = 44 if kind == "cover" else 34
    sm = await B.measure_text([dict(text=strip, font="d", size=sfs, weight=400)])
    sw_ = sm[0]["text_w"]
    if sw_ > 900: sfs *= 900 / sw_; sw_ = 900
    SY_ = L["cover_strip_y"] if kind == "cover" else L["strip_y"]
    parts.append(f'<div class="measure" data-tag="strip" style="position:absolute;left:{(W - sw_) / 2}px;top:{SY_}px;font-family:var(--d);'
                 f'font-weight:400;font-size:{sfs}px;line-height:1;color:{WHITE};white-space:nowrap;z-index:6">{strip.replace("&", "&amp;")}</div>')
    el("strip", (W - sw_) / 2, SY_ + 2, sw_, sfs * 0.81)

    # ---- footer: AQ logo + ALL FOR CHARITY ----
    fy = L["foot_y"]
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{fy + 6}px;height:56px;z-index:9">')
    el("logo", 27, fy + 6, 320, 56)
    cw, chh, cx_ = 337, 67, 720
    el("cta", cx_, fy, cw, chh)
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx_}px;top:{fy}px;width:{cw}px;height:{chh}px;border:6px solid {ORCHID};'
                 f'border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);'
                 f'font-weight:900;font-size:26px;color:{INK}">ALL FOR CHARITY</div>')

    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("strip", WHITE, GROUND, 34, False), ("slab", INK, SLAB, 40, False),
                  ("cta", INK, CTA_FILL, 26, True), ("pill", INK, "#FFFFFF", 31, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=True,
                   collision_ignore={("hero", "slab"), ("star_ml", "slab"), ("star_br", "slab"), ("star_tr", "hero"), ("star_tl", "hero")}, margin=12)


async def main(canvases, decks=("reasons",)):
    global DECK
    async with B.session():
        for dk in decks:
            DECK = DECKS[dk]
            for canvas in canvases:
                d = f"out/versions/terrathon_carousel/{dk}/{canvas}"; os.makedirs(d, exist_ok=True)
                bare = DECK.get("bare")
                if not bare: await slide("cover", canvas, f"{d}/00_cover.png")
                for i, r in enumerate(DECK["items"]):
                    await slide("point", canvas, f"{d}/{i + 1:02d}_{r[0]}.png", idx=i)
                if not bare: await slide("close", canvas, f"{d}/{len(DECK['items']) + 1:02d}_close.png")
                print("done", dk, canvas)

if __name__ == "__main__":
    args = sys.argv[1:]
    decks = tuple(a for a in args if a in DECKS) or ("reasons",)
    cvs = [a for a in args if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(main(cvs, decks))
