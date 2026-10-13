"""REVER x DISCO DIWALI 2026: the MARKETING deck, TerraThon look, formal register (Workflow C, bespoke build; user 2026-10-13).

Brief (user): a marketing deck for Rever, the cafe that is AquaTerra's Exclusive Food and Location Partner. It is the companion to the 29-slide partnership proposal
(scratchpad/gen_rever_deck.py), so it re-uses that deck's system (black ground with flecks, blue shuriken, white cards with an orchid border, NeutralFace type, Rever's pill
bottom-right). The channels are the user's: Instagram (reels, posts, stories, collabs; follows / reach / views / shares / likes), WhatsApp (community, broadcasts, school
outreach) and the 18+ school student network. The content plan is the user's list, phase by phase, each phase ending in "and many more". No prices slide. Contact is Pratyaksh.

ROUND 2 (user, same day): "make it look a bit formal", "add and many more to the on the day plan", "every content plan will be approved by Rever first before being shot",
and "should we showcase screenshots as proof of reach?". Applied:
  * FORMAL REGISTER, done once in the overrides below rather than slide by slide: no tilted cards, 6px keylines and 20px corners (was 10px and 34px), NeutralFace for every
    headline, number and sub-line (the StretchPro numerals and the Sigmar One sub-lines are gone), no die-cut stickers inside cards (they remain on the cover, the closing slide
    and the photo slide), headlines rewritten as plain statements.
  * The approval line is on the calendar, all three content-plan slides, the requirements slide and the contact slide.
  * "AND MANY MORE" now closes the before AND the on-the-day plans.
  * PROOF-OF-REACH slide is conditional: it renders only when real screenshots are in engine/assets/rever_marketing/proof/ (or REVER_PROOF_DIR). Neither source deck contains an
    Insights screenshot (checked, all 36 + 29 pages), so none can be cut from them, and one must never be mocked up.

EVERY FIGURE ON A SLIDE LIVES IN `FACTS` BELOW (user: "rerun a script"). Edit a number there, rerun, done. Where the two source decks disagreed, this deck uses the Rever
deck's figure for anything Rever has already seen (1,800+ WhatsApp members, 1.11M+ impressions) and the user's own words for schools ("18+"). See the open list in
brain/REVER_MARKETING_DECK.md.

Adaptations (CLAUDE.md sec 2 rule 4), recorded:
  * 1920x1080 landscape (16:9), M=96, like the proposal deck. Output is PDF (rasterised slides), not editable slides.
  * The user wrote "spam" for WhatsApp. It reads here as "broadcasts" (it is going to the cafe); flagged to the user.
  * Rever has no food or venue photo in the repo, and food imagery may not be invented (real assets only), so the deck uses no food imagery at all.
  * Photos are Disco Diwali 2025 / AQ event photos already in the repo, plus crops cut from the two exported PDFs by scratchpad/rever_marketing_assets.py (git-ignored).
  * No Instagram or WhatsApp logos.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_rever_marketing_deck.py [1 2 3 ...]   ->  out/decks/rever_marketing/slide_NN.png (+ rever_marketing_deck.pdf when all are rendered)
Needs: python scratchpad/rever_marketing_assets.py once (crops), pip install playwright==1.56.0.
"""
import asyncio, base64, importlib.util, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m


rd = _load("gen_rever_deck", "scratchpad/gen_rever_deck.py")          # the proposal deck's Slide class, tokens and helpers
mk = _load("rever_marketing_stickers", "scratchpad/rever_marketing_stickers.py")
stk, tt, B, W, H, M = rd.stk, rd.tt, rd.B, rd.W, rd.H, rd.M
GROUND, ORCHID, HALO, SLAB, INK, WHITE, CTA, GREEN, BLUE = rd.GROUND, rd.ORCHID, rd.HALO, rd.SLAB, rd.INK, rd.WHITE, rd.CTA, rd.GREEN, rd.BLUE
PH = rd.PH
OUT = os.path.join(ROOT, "out", "decks", "rever_marketing")
CR = "engine/assets/rever_marketing/photos/"
PROOF_DIR = os.environ.get("REVER_PROOF_DIR", os.path.join(ROOT, "engine", "assets", "rever_marketing", "proof"))
rd.OUT = OUT

# ------------------------------------------------------------------------------------------------ the facts (edit here, rerun)
FACTS = dict(
    event_date="10 November 2026",
    followers="5K+",                     # Instagram followers (both decks; cold deck p2, p23)
    views30="4.3 LAKH",                  # Instagram views in a recent 30 days (cold deck p23)
    summer_post="21.7K",                 # views on the Summer Sunset post (cold deck p23)
    paradox_post="9.3K",                 # views on the Paradox 2026 post (cold deck p23's own label; its event card calls the event Paradox 3.0, 2025: unresolved)
    impressions="1.11M+",                # impressions across the last few events (Rever deck)
    whatsapp="1,800+",                   # members in the WhatsApp community where Rever is promoted (Rever deck)
    schools="18+",                       # Kolkata schools in the student network (user, 2026-10-13)
    school_chips=("DBPC", "LA MARTINIERE FOR BOYS", "LA MARTINIERE FOR GIRLS", "MODERN HIGH", "LORETO", "AND OTHER LEADING KOLKATA SCHOOLS"),   # the five the Rever deck names
    contact=("PRATYAKSH SINGHANIA", "+91 98305 54654", "@ngo.aquaterra", "@aquaterra.live", "ngoaquaterra.com"),
    approval="Every content plan is approved by Rever before anything is shot.",                      # user, 2026-10-13
    proof_captions=("Instagram Insights", "Instagram Insights", "Instagram Insights"),               # one per screenshot, in file-name order; edit when real ones are dropped in
    proof_note="Screenshots from AquaTerra's Instagram account.",
)
F = FACTS


# ------------------------------------------------------------------------------------------------ formal register: ONE place, not 14
_slab, _photo_rect = rd.Slide.slab, rd.Slide.photo_rect


def _f_slab(s, label, x, y, w, h, inner, **kw):
    kw.pop("rot", None); kw.pop("tilt", None)
    kw["border"], kw["radius"] = 6, 20
    return _slab(s, label, x, y, w, h, inner, **kw)


def _f_panel(s, label, x, y, w, h, inner, rot=0, z=8, pad="28px 34px"):
    s.add(f'<div class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#0B0B0D;border:4px solid {ORCHID};'
          f'border-radius:20px;z-index:{z};padding:{pad};color:{WHITE};overflow:hidden">{inner}</div>')
    s.el(label, x - 2, y - 2, w + 4, h + 4); s.conts.append(label)


def _f_photo_rect(s, label, path, x, y, w, h, focus="50% 50%", cap="Disco Diwali 2025", ring=8, radius=30, z=8, maxw=1400):
    return _photo_rect(s, label, path, x, y, w, h, focus, cap, 5, 18, z, maxw)


def _f_pill(s, label, x, y, text, size=34, w=None, align="left", z=12):
    s.add(f'<div class="measure v" data-tag="{label}" style="position:absolute;{align}:{x}px;top:{y}px;{"width:%dpx;" % w if w else ""}height:{size * 2.0:.0f}px;border:4px solid {ORCHID};'
          f'border-radius:14px;background:{CTA};display:flex;align-items:center;justify-content:flex-start;padding:0 {size * .8:.0f}px;font-size:{size}px;color:{INK};white-space:nowrap;z-index:{z}">{text}</div>')


async def _f_heading(s, x, y, w, white, orchid=None, ws=72, os_=36, gap=10, label="h1", wl=None):
    """White NeutralFace headline + an orchid NeutralFace 400 sub-line (the proposal deck used Sigmar One here). Returns the y below the block."""
    items = [dict(text=white.upper(), font="d", size=ws, weight=900, max_width=w)]
    if orchid: items.append(dict(text=orchid.upper(), font="d", size=os_, weight=400, letter_spacing=".05em", max_width=w))
    m = await B.measure_text(items, W, H)
    hw = m[0]["lines"] * ws * .98
    s.add(f'<div class="measure v" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{ws}px;line-height:.98;color:{WHITE};z-index:6">{white.upper()}</div>')
    s.el(label, x, y, min(w, m[0]["text_w"]), hw); s.text_pair(label, WHITE, GROUND, ws, True)
    bottom = y + hw
    if orchid:
        ho = m[1]["lines"] * os_ * 1.15; y2 = bottom + gap
        s.add(f'<div class="measure k" data-tag="{label}o" style="position:absolute;left:{x}px;top:{y2}px;width:{w}px;font-size:{os_}px;line-height:1.15;letter-spacing:.05em;color:{ORCHID};z-index:6">{orchid}</div>')
        s.el(label + "o", x, y2, min(w, m[1]["text_w"]), ho); s.text_pair(label + "o", ORCHID, GROUND, os_, False)
        bottom = y2 + ho
    return bottom


rd.Slide.slab, rd.Slide.panel, rd.Slide.photo_rect, rd.Slide.pill, rd.Slide.heading = _f_slab, _f_panel, _f_photo_rect, _f_pill, _f_heading


async def num_size(texts, maxw, cap=220):
    """Largest NeutralFace 900 size (px) at which every string fits maxw, measured with the real font."""
    m = await B.measure_text([dict(text=t, font="d", size=100, weight=900) for t in texts], W, H)
    return min(cap, min(100 * maxw / r["text_w"] for r in m))


def card_inner(title, desc, num=None, tsize=30, dsize=24, gap=14):
    top = f'<div style="margin-bottom:{gap}px">{rd.numdot(num, 48, 25)}</div>' if num else ""
    return (top + f'<div class="v" style="font-size:{tsize}px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:10px">{title}</div>'
            f'<div class="b" style="font-size:{dsize}px;line-height:1.3;color:{INK}">{desc}</div>')


def callout(s, y, text, size=30, w=None):
    w = w or int(len(text) * size * .68 + size * 1.7 + 8)
    s.pill("callout", M, y, text, size, w=w, align="left")
    s.el("callout", M, y, w, int(size * 2.0)); s.text_pair("callout", INK, CTA, size, True)


# ================================================================================================ cover
async def s_cover(n):
    s = rd.Slide(n, specks_on=False)
    s.add(f'<div style="position:absolute;inset:0;background:url({rd.photo_full(PH["wall"], 1500)}) 62% 38%/cover;z-index:0;filter:brightness(1.25) saturate(1.1)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.93) 28%,rgba(0,0,0,.5) 52%,rgba(0,0,0,.08) 100%)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,0) 28%)"></div>')
    s.add(f'<div class="measure k" data-tag="eyebrow" style="position:absolute;left:{M}px;top:64px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap;letter-spacing:.08em">A MARKETING PLAN FOR REVER</div>')
    s.el("eyebrow", M, 64, 620, 28); s.text_pair("eyebrow", WHITE, GROUND, 26, False)
    s.add(f'<div class="measure k" data-tag="t1" style="position:absolute;left:{M}px;top:136px;font-size:96px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">REVER x</div>')
    s.el("t1", M, 142, 444, 84); s.text_pair("t1", WHITE, GROUND, 96, False)
    s.add(f'<div class="measure v" data-tag="year" style="position:absolute;left:{M + 484}px;top:140px;height:84px;border:5px solid {ORCHID};border-radius:14px;background:{SLAB};'
          f'display:flex;align-items:center;padding:0 34px;font-size:50px;color:{INK};z-index:6">2026</div>')
    s.el("year", M + 484, 140, 215, 84)
    s.add(f'<div class="measure v" data-tag="t2" style="position:absolute;left:{M}px;top:242px;font-size:196px;line-height:.9;color:{WHITE};z-index:6;white-space:nowrap">DISCO<br>DIWALI</div>')
    s.el("t2", M, 252, 720, 360); s.text_pair("t2", WHITE, GROUND, 196, True)
    s.add(f'<div class="measure k" data-tag="sub" style="position:absolute;left:{M}px;top:652px;width:900px;font-size:36px;line-height:1.2;letter-spacing:.05em;color:{ORCHID};z-index:6">'
          f'HOW WE WILL PROMOTE REVER, BEFORE, ON THE DAY AND AFTER THE EVENT</div>')
    s.el("sub", M, 652, 900, 90); s.text_pair("sub", ORCHID, GROUND, 36, False)
    inner = (f'<div style="display:flex;align-items:center;gap:36px;height:100%"><img src="{rd.REVER}" style="height:70px;flex:none">'
             f'<div style="width:4px;align-self:stretch;background:{ORCHID}"></div>'
             f'<div class="v" style="font-size:38px;line-height:1.05;color:{INK}">EXCLUSIVE FOOD AND<br>LOCATION PARTNER</div></div>')
    s.slab("slab", M, 800, 960, 140, inner, pad="10px 38px")
    s.text_pair("slab", INK, SLAB, 38, True)
    s.add(f'<img class="measure" data-tag="logo" src="{rd.core.LOGO}" style="position:absolute;left:{M}px;top:{H - 90}px;height:50px;z-index:9">'); s.el("logo", M, H - 90, 296, 50)
    s.pill("cta", M, H - 112, f"TEAM AQUATERRA, EST. 2021&nbsp;&nbsp;|&nbsp;&nbsp;{F['event_date'].upper()}", 28, align="right")
    s.el("cta", W - M - 700, H - 112, 700, 56); s.text_pair("cta", INK, CTA, 28, True)
    s.cord(1488, 0, 76); s.ball("st_ball", 340, 1318, 70, 0)
    s.stars([(1760, 80)], 90)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ plan at a glance
async def s_overview(n):
    s = rd.Slide(n); s.chrome("OVERVIEW")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "The plan at a glance.", "Three channels, one student audience.", 72, 36)
    cards = [("Instagram", F["followers"], "followers", "Reels, posts, stories and collab posts, with Rever tagged."),
             ("WhatsApp", F["whatsapp"], "members in our community, where Rever is promoted", "Callouts to the community, broadcast lists and school groups."),
             ("Schools", F["schools"], "Kolkata schools in our student network", "Reached directly and through our volunteers.")]
    fs = await num_size([c[1] for c in cards], 440, 150)
    cw = (1728 - 2 * 28) / 3
    for i, (t, v, lab, line) in enumerate(cards):
        inner = (f'<div class="v" style="font-size:40px;line-height:1;color:{INK};text-transform:uppercase;margin-bottom:36px">{t}</div>'
                 f'<div class="v" style="font-size:{fs:.0f}px;line-height:1;color:{INK};white-space:nowrap;margin-bottom:22px">{v}</div>'
                 f'<div class="v" style="font-size:25px;line-height:1.12;color:{INK};text-transform:uppercase;margin-bottom:18px">{lab}</div>'
                 f'<div class="b" style="font-size:25px;line-height:1.3;color:{INK}">{line}</div>')
        s.slab(f"card{i}", M + i * (cw + 28), 296, cw, 520, inner, pad="34px 38px")
    s.text_pair("card0", INK, SLAB, 25, True)
    callout(s, 850, "BEFORE THE EVENT. ON THE DAY. AFTER THE EVENT.", 32)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ audience
async def s_who(n):
    s = rd.Slide(n); s.chrome("THE AUDIENCE")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1600, "Who sees it.", "Students, reached on Instagram first.", 72, 36)
    fs = await num_size(["16-19"], 480, 300)
    inner = (rd.label("Age band, roughly", 28, INK, "margin-bottom:12px") + f'<div class="v" style="font-size:{fs:.0f}px;line-height:1.05;color:{INK};white-space:nowrap">16-19</div>')
    s.slab("age", M, 300, 620, 300, inner, pad="36px 44px")
    s.text_pair("age", INK, SLAB, 28, False)
    rows = [("Who", "Classes 9 to 12 and college students from across Kolkata"),
            ("How they show up", "In friend groups, for birthdays, celebrations and weekend plans"),
            ("How they find things", "Instagram first, heavily influenced by peers and event content")]
    inner = "".join(f'<div style="margin-bottom:22px">{rd.label(k, 24, ORCHID)}<div class="b" style="font-size:31px;line-height:1.22;color:{WHITE};margin-top:6px">{v}</div></div>' for k, v in rows)
    s.add(f'<div class="measure" data-tag="rows" style="position:absolute;left:{M + 700}px;top:290px;width:1020px;z-index:6">{inner}</div>')
    s.el("rows", M + 700, 290, 1020, 262); s.text_pair("rows", WHITE, GROUND, 31, False)
    s.photo_rect("ph_a", PH["friends"], M, 650, 1728, 290, "50% 42%", cap="Friends at an AquaTerra evening")
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ instagram
async def s_insta(n):
    s = rd.Slide(n); s.chrome("CHANNELS  (1 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Instagram.", "Four formats, five measures.", 72, 36)
    fm = [("Reels", "The venue, the menu, the decor and the night itself, shot at Rever and cut by our team."),
          ("Posts", "The location drop, the sponsor mention, the layout blueprint, the menu and the thank-you."),
          ("Stories", "Rever tagged as the venue on every story we post about the night."),
          ("Collabs", "Event reels go out as collab posts, so they also appear on Rever's profile and reach Rever's followers.")]
    cw = (1728 - 3 * 24) / 4
    for i, (t, d) in enumerate(fm):
        s.slab(f"fmt{i}", M + i * (cw + 24), 290, cw, 340, card_inner(t, d, i + 1, 38, 25), pad="28px 30px")
    s.text_pair("fmt0", INK, SLAB, 25, False)
    tr = [("Reach", "accounts reached"), ("Views", "times viewed"), ("Shares", "times shared"), ("Likes", "likes received"), ("Follows", "followers gained")]
    cells = "".join(f'<div style="border-left:3px solid {ORCHID};padding-left:22px"><div class="v" style="font-size:38px;color:{WHITE};text-transform:uppercase;margin-bottom:8px">{t}</div>'
                    f'<div class="k" style="font-size:20px;color:{ORCHID}">{d}</div></div>' for t, d in tr)
    inner = rd.label("What we measure for Rever", 25, ORCHID, "margin-bottom:22px") + f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:24px">{cells}</div>'
    s.panel("track", M, 676, 1728, 214, inner, pad="24px 40px")
    s.text_pair("track", WHITE, "#0B0B0D", 38, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ reach
async def s_reach(n):
    s = rd.Slide(n); s.chrome("CHANNELS  (1 OF 3, CONTINUED)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Reach.", "Recent Instagram figures.", 72, 36)
    fs = await num_size([F["views30"]], 640, 260)
    inner = (rd.label("Instagram, in a recent 30 days", 27, ORCHID, "margin-bottom:18px")
             + f'<div class="v" style="font-size:{fs:.0f}px;line-height:1;color:{WHITE};white-space:nowrap">{F["views30"]}</div>'
             + f'<div class="v" style="font-size:44px;line-height:1.05;color:{WHITE};margin-top:14px;text-transform:uppercase">views</div>')
    s.panel("hero", M, 290, 760, 640, inner, pad="40px 48px")
    s.text_pair("hero", WHITE, "#0B0B0D", 44, True)
    s.photo_rect("ph_a", PH["blue"], M + 44, 600, 672, 284, "50% 40%", cap="Disco Diwali 2025")
    tiles = [(F["followers"], "followers on Instagram"), (F["summer_post"], "views on the Summer Sunset post"),
             (F["paradox_post"], "views on the Paradox 2026 post"), (F["impressions"], "impressions across our last few events")]
    tfs = await num_size([t[0] for t in tiles], 340, 150)
    for i, (v, l) in enumerate(tiles):
        x, y = 888 + (i % 2) * 476, 290 + (i // 2) * 332
        s.slab(f"tile{i}", x, y, 450, 308, f'<div class="v" style="font-size:{tfs:.0f}px;line-height:1;color:{INK};white-space:nowrap;margin-bottom:18px">{v}</div>'
               f'<div class="v" style="font-size:27px;line-height:1.1;color:{INK};text-transform:uppercase">{l}</div>', pad="36px 36px", fill=ORCHID if i == 0 else SLAB)
    s.text_pair("tile0", INK, ORCHID, 27, True); s.text_pair("tile1", INK, SLAB, 27, True)
    s.add(f'<div class="measure k" data-tag="src" style="position:absolute;left:888px;top:944px;font-size:19px;color:{WHITE};opacity:.8;z-index:6;white-space:nowrap">FIGURES SUPPLIED BY TEAM AQUATERRA</div>')
    s.el("src", 888, 944, 420, 22); s.text_pair("src", WHITE, GROUND, 19, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ proof of reach (only when real screenshots exist)
def proof_files():
    if not os.path.isdir(PROOF_DIR): return []
    return sorted(os.path.join(PROOF_DIR, f) for f in os.listdir(PROOF_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg")))[:3]


async def s_proof(n):
    from PIL import Image
    s = rd.Slide(n); s.chrome("CHANNELS  (1 OF 3, EVIDENCE)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Proof of reach.", "Instagram Insights, as captured.", 72, 36)
    ims = [Image.open(p).convert("RGB") for p in proof_files()]
    asp = [im.width / im.height for im in ims]
    gap, top, right = 28, 290, W - M
    h = min(640, (1180 - gap * (len(ims) - 1)) / sum(asp) - 0)
    widths = [h * a for a in asp]
    total = sum(widths) + gap * (len(ims) - 1) + 10 * len(ims)
    x = right - total
    caps = F["proof_captions"]
    for i, (im, w_) in enumerate(zip(ims, widths)):
        r = min(1.0, 1500 / max(im.size)); im2 = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS) if r < 1 else im
        buf = io.BytesIO(); im2.save(buf, "JPEG", quality=90)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        s.add(f'<img class="measure" data-tag="proof{i}" src="{uri}" style="position:absolute;left:{x:.0f}px;top:{top}px;width:{w_:.0f}px;height:{h:.0f}px;border:5px solid {ORCHID};'
              f'border-radius:18px;box-sizing:content-box;object-fit:cover;z-index:8">')
        s.el(f"proof{i}", x, top, w_ + 10, h + 10)
        cap = caps[i] if i < len(caps) else "Instagram Insights"
        s.add(f'<div class="measure k" data-tag="proofcap{i}" style="position:absolute;left:{x:.0f}px;top:{top + h + 24:.0f}px;width:{w_ + 10:.0f}px;text-align:center;font-size:20px;color:{WHITE};z-index:6">{cap}</div>')
        s.el(f"proofcap{i}", x, top + h + 24, w_ + 10, 24); s.text_pair(f"proofcap{i}", WHITE, GROUND, 20, False)
        x += w_ + 10 + gap
    inner = (rd.label("How to read these", 26, INK, "margin-bottom:16px")
             + f'<div class="b" style="font-size:28px;line-height:1.36;color:{INK}">{F["proof_note"]}</div>')
    s.slab("note", M, 290, max(420, int(right - total - M - 40)), 300, inner, pad="32px 38px")
    s.text_pair("note", INK, SLAB, 28, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ whatsapp
async def s_whatsapp(n):
    s = rd.Slide(n); s.chrome("CHANNELS  (2 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "WhatsApp.", "Community, broadcasts and school groups.", 72, 36)
    rows = [("The community", f"{F['whatsapp']} members in our WhatsApp community, where Rever is promoted for close to a month."),
            ("Broadcasts", "Rever in every callout across our community and broadcast lists, from the venue reveal to event day."),
            ("School outreach", "Class and school groups across Kolkata, reached directly and through our volunteers.")]
    for i, (t, d) in enumerate(rows):
        inner = (f'<div style="display:flex;gap:30px;align-items:center;height:100%">{rd.numdot(i + 1, 56, 29)}'
                 f'<div><div class="v" style="font-size:38px;line-height:1.05;color:{INK};text-transform:uppercase;margin-bottom:10px">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.32;color:{INK}">{d}</div></div></div>')
        s.slab(f"row{i}", M, 296 + i * 214, 1060, 190, inner, pad="12px 38px")
    s.text_pair("row0", INK, SLAB, 27, False)
    s.photo_rect("ph_a", PH["phone"], 1210, 290, 614, 640, "50% 50%", cap="Disco Diwali 2025")
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ schools
async def s_schools(n):
    s = rd.Slide(n); s.chrome("CHANNELS  (3 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "The student network.", "Reached directly and through our volunteers.", 72, 36)
    fs = await num_size([F["schools"]], 420, 300)
    s.add(f'<div class="measure v" data-tag="big" style="position:absolute;left:{M}px;top:290px;font-size:{fs:.0f}px;line-height:1;color:{ORCHID};white-space:nowrap;z-index:6">{F["schools"]}</div>')
    s.el("big", M, 290, 420, int(fs)); s.text_pair("big", ORCHID, GROUND, fs, True)
    s.add(f'<div class="measure b" data-tag="body" style="position:absolute;left:{M + 470}px;top:310px;width:600px;font-size:31px;line-height:1.36;color:{WHITE};z-index:6">'
          f'Kolkata schools in our community network, with students from Classes 9 to 12 and college.</div>')
    s.el("body", M + 470, 310, 600, 170); s.text_pair("body", WHITE, GROUND, 31, False)
    chips = "".join(f'<span class="v" style="display:inline-block;background:{CTA};border:4px solid {ORCHID};border-radius:12px;padding:8px 22px;font-size:27px;color:{INK};margin:0 12px 14px 0;white-space:nowrap">{c}</span>'
                    for c in F["school_chips"])
    s.add(f'<div class="measure" data-tag="chips" style="position:absolute;left:{M}px;top:560px;width:1060px;z-index:6">{chips}</div>')
    s.el("chips", M, 560, 1060, 190); s.text_pair("chips", INK, CTA, 27, True)
    s.photo_rect("ph_a", CR + "school_banner.jpg", 1240, 250, 584, 630, "50% 50%", cap="School network", maxw=900)
    s.photo_rect("ph_b", CR + "volunteers_laptops.jpg", M, 780, 1060, 170, "50% 40%", cap="Student volunteers", maxw=900)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ calendar
async def s_timeline(n):
    s = rd.Slide(n); s.chrome("TIMELINE")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Campaign calendar.", "From sign-off to the week after.", 72, 36)
    cw = 1728 / 6
    groups = [("BEFORE THE EVENT", 0, 4, ORCHID), ("ON THE DAY", 4, 5, GREEN), ("AFTER", 5, 6, BLUE)]
    for lab, a, b, col in groups:
        x = M + a * cw + 6; w = (b - a) * cw - 12
        s.add(f'<div class="measure v" data-tag="grp{a}" style="position:absolute;left:{x:.0f}px;top:290px;width:{w:.0f}px;height:56px;border-radius:12px;background:{col};'
              f'display:flex;align-items:center;justify-content:center;font-size:25px;color:{INK};z-index:6;white-space:nowrap">{lab}</div>')
        s.el(f"grp{a}", x, 290, w, 56)
    s.text_pair("grp0", INK, ORCHID, 25, True); s.text_pair("grp4", INK, GREEN, 25, True); s.text_pair("grp5", INK, BLUE, 25, True)
    s.add(f'<div style="position:absolute;left:{M + 40}px;top:405px;width:{1728 - 80}px;height:4px;background:{HALO};z-index:3"></div>')
    steps = [("Partnership sign-off", "Menu, deliverables and dates locked"),
             ("Content shoots at Rever", "After Rever approves the content plan. Multiple days, scheduled with Rever"),
             ("Venue reveal", "Within two weeks of sign-off. The reveal reel launches the campaign"),
             ("Ticket sales and promotion", "Collab reels, Rever reels and WhatsApp callouts, through to event day"),
             ("Event day", F["event_date"]), ("The week after", "Thank-you post, recap, reach and views summary, asset handover")]
    for i, (t, d) in enumerate(steps):
        cx = M + i * cw + cw / 2
        hot = i == 4
        s.add(f'<div style="position:absolute;left:{cx - 31:.0f}px;top:377px;z-index:7">{rd.numdot(i + 1, 62, 32, GREEN if hot else (BLUE if i == 5 else ORCHID))}</div>')
        s.slab(f"st{i}", M + i * cw + 6, 450, cw - 12, 360, f'<div class="v" style="font-size:29px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:12px">{t}</div>'
               f'<div class="b" style="font-size:24px;line-height:1.3;color:{INK}">{d}</div>', pad="26px 22px", fill=GREEN if hot else SLAB)
    s.text_pair("st0", INK, SLAB, 24, False)
    callout(s, 846, "THE SOONER WE SIGN OFF, THE MORE OF THE MONTH WE CAN PROMOTE.", 30)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ content plan, three phases
async def s_before(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (1 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Before the event.", "Building awareness of Rever.", 72, 36)
    items = [("Location drop post", "Rever Skydeck announced as the venue."), ("Sponsor mention post", "Rever announced as our Exclusive Food and Location Partner."),
             ("Blueprint post", "A basic layout of how the location will look on the day."), ("Location showcase reel", "Rever Skydeck on camera, shot by our team."),
             ("Menu post", "The event menu that Rever's kitchen designs."), ("Fun menu reels", "Fun reels starring the items on the menu."),
             ("Collabs and callouts", "Collab posts, stories and WhatsApp callouts, all the way to event day.")]
    cw, ch = (1728 - 3 * 24) / 4, 272
    for i, (t, d) in enumerate(items):
        s.slab(f"it{i}", M + (i % 4) * (cw + 24), 290 + (i // 4) * (ch + 24), cw, ch, card_inner(t, d, i + 1, 27, 22, 10), pad="22px 26px")
    s.text_pair("it0", INK, SLAB, 22, False)
    fs = await num_size(["MANY"], 300, 80)
    s.slab("more", M + 3 * (cw + 24), 290 + (ch + 24), cw, ch, f'<div class="v" style="font-size:{fs:.0f}px;line-height:1;color:{INK};display:flex;flex-direction:column;justify-content:center;height:100%">AND<br>MANY<br>MORE</div>',
           fill=ORCHID, pad="24px 30px")
    s.text_pair("more", INK, ORCHID, fs, True)
    callout(s, 884, F["approval"].upper(), 28)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_day(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (2 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "On the day.", "10 November 2026.", 72, 36)
    items = [("Decor going up", "A reel of the decor going up, as the room turns into Disco Diwali."),
             ("Registration, and a walk through", "Registration has started: a full run through the location, with Rever's space in frame."),
             ("Fun reels, all night", "Fun reels in general, from the first guest through to the last song.")]
    step, rh = 148, 132
    for i, (t, d) in enumerate(items):
        inner = (f'<div style="display:flex;gap:26px;align-items:center;height:100%">{rd.numdot(i + 1, 52, 27)}'
                 f'<div><div class="v" style="font-size:30px;line-height:1.05;color:{INK};text-transform:uppercase;margin-bottom:6px">{t}</div>'
                 f'<div class="b" style="font-size:24px;line-height:1.28;color:{INK}">{d}</div></div></div>')
        s.slab(f"row{i}", M, 296 + i * step, 980, rh, inner, pad="8px 30px")
    s.text_pair("row0", INK, SLAB, 24, False)
    inner = (f'<div style="display:flex;gap:26px;align-items:center;height:100%">{rd.numdot("+", 52, 30, WHITE)}'
             f'<div class="v" style="font-size:40px;line-height:1;color:{INK}">AND MANY MORE</div></div>')
    s.slab("more", M, 296 + 3 * step, 980, rh, inner, fill=ORCHID, pad="8px 30px")
    s.text_pair("more", INK, ORCHID, 40, True)
    s.photo_rect("ph_a", CR + "reg_desk.jpg", 1110, 290, 714, 262, "40% 50%", cap="Registration, Disco Diwali 2025", maxw=1200)
    s.photo_rect("ph_b", CR + "decor_globe.jpg", 1110, 580, 714, 280, "50% 50%", cap="The stage, Disco Diwali 2025", maxw=900)
    callout(s, 892, F["approval"].upper(), 28)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_after(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (3 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "After the event.", "Recap, reviews and reporting.", 72, 36)
    items = [("Decor dump", "A photo dump of the finished decor."), ("Favourite item reel", "Guests answer on camera: what was your favourite item on the menu?"),
             ("Location reviews reel", "Guests say what they thought of the location, on camera."), ("Thank-you post", "A thank-you to Rever and to everyone who came."),
             ("Podcast with the owner", "A sit-down podcast with Rever's owner.")]
    cw, ch = (1728 - 2 * 24) / 3, 262
    for i, (t, d) in enumerate(items):
        s.slab(f"it{i}", M + (i % 3) * (cw + 24), 290 + (i // 3) * (ch + 24), cw, ch, card_inner(t, d, i + 1, 30, 25, 12), pad="24px 30px")
    s.text_pair("it0", INK, SLAB, 25, False)
    inner = (f'<div class="v" style="font-size:30px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:12px">The report</div>'
             f'<div class="b" style="font-size:25px;line-height:1.3;color:{INK}">A reach and views summary, plus the photo and video assets for Rever to keep using.</div>')
    s.slab("report", M + 2 * (cw + 24), 290 + (ch + 24), cw, ch, inner, fill=GREEN, pad="30px 30px")
    s.text_pair("report", INK, GREEN, 25, False)
    callout(s, 878, F["approval"].upper(), 28)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ what we need
async def s_need(n):
    s = rd.Slide(n); s.chrome("WHAT WE NEED")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Requirements from Rever.", "To keep the plan on schedule.", 72, 36)
    items = [("Access to Skydeck", "Shoot days at Rever Skydeck, across multiple days and scheduled with Rever."),
             ("Menu and handle", "The event menu and its items for the posts and reels, and Rever's Instagram handle for collab posts."),
             ("Approvals", "Rever approves every content plan before anything is shot, and every post, reel and broadcast that carries its name before it goes out."),
             ("Your people", "One named contact to coordinate with, and the owner's time for the podcast.")]
    for i, (t, d) in enumerate(items):
        x, y = M + (i % 2) * 888, 290 + (i // 2) * 284
        inner = card_inner(t, d, i + 1, 34, 26, 12)
        s.slab(f"card{i}", x, y, 840, 266, inner, pad="22px 36px")
    s.text_pair("card0", INK, SLAB, 27, False)
    callout(s, 876, "NOTHING IS SHOT, POSTED OR SENT WITHOUT REVER'S APPROVAL.", 32)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ close
async def s_next(n):
    s = rd.Slide(n); s.chrome("CLOSING")
    s.stars([(1760, 560)], 90)
    await s.heading(M, 104, 1180, "Next steps.", "Let's put Rever in front of Kolkata's students.", 72, 34)
    steps = [("Sign off", "Menu, deliverables and dates locked"), ("Content plan approved", "Rever approves the plan before anything is shot"), ("Shoot and reveal", "Shoots at Rever, then the venue reveal")]
    sx = M
    for i, ((t, d), sw) in enumerate(zip(steps, (340, 340, 340))):
        inner = (f'<div style="display:flex;flex-direction:column;gap:10px">{rd.numdot(i + 1, 56, 30)}<div class="v" style="font-size:28px;line-height:1.08;color:{INK};text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:22px;line-height:1.28;color:{INK}">{d}</div></div>')
        s.slab(f"step{i}", sx, 320, sw, 280, inner, pad="22px 26px")
        sx += sw + 20
    s.text_pair("step0", INK, SLAB, 28, True)
    name, phone, ig1, ig2, web = F["contact"]
    inner = (rd.label("Contact", 24, INK, "margin-bottom:8px") + f'<div class="v" style="font-size:54px;line-height:1.1;color:{INK}">{name}</div>'
             f'<div class="k" style="font-size:30px;color:{INK};margin:8px 0 18px">Team AquaTerra&nbsp;&nbsp;|&nbsp;&nbsp;{phone}</div>'
             f'<div class="b" style="font-size:30px;line-height:1.35;color:{INK}">Instagram: <b>{ig1}</b> | <b>{ig2}</b><br>{web}</div>')
    s.slab("contact", M, 620, 1060, 316, inner, pad="26px 40px")
    s.text_pair("contact", INK, SLAB, 30, False)
    s.add(f'<div class="measure" data-tag="rever_logo" style="position:absolute;left:1290px;top:96px;width:440px;height:440px;border-radius:50%;background:#fff;border:12px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8">'
          f'<img src="{rd.REVER}" style="width:320px"></div>')
    s.el("rever_logo", 1290, 96, 440, 440)
    s.add(f'<div class="measure" data-tag="qr" style="position:absolute;left:1350px;top:590px;width:320px;height:320px;border-radius:24px;background:#fff;border:10px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8">'
          f'<img src="{rd.QR}" style="width:250px;height:250px"></div>')
    s.el("qr", 1350, 590, 320, 320)
    s.add(f'<div class="measure k" data-tag="qrcap" style="position:absolute;left:1330px;top:922px;width:360px;text-align:center;font-size:21px;color:{WHITE};z-index:9">SCAN FOR {ig1.upper()}</div>')
    s.el("qrcap", 1330, 922, 360, 24); s.text_pair("qrcap", WHITE, GROUND, 21, False)
    s.cord(1815, 0, 280); s.ball("st_ball", 150, 1740, 270, 0)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ the running order
def photo_slide(*a, **k):
    async def run(n): await rd.photo_full_slide(n, *a, **k)
    return run


def build_order():
    order = [s_cover, s_overview, s_who, s_insta, s_reach]
    if proof_files(): order.append(s_proof)               # only with real screenshots; never a mock-up
    order += [s_whatsapp, s_schools,
              photo_slide("purple", "One night.\n300 to 350 guests.", "Crowd at Disco Diwali 2025", "50% 45%"),
              s_timeline, s_before, s_day, s_after, s_need, s_next]
    return order


ORDER = build_order()


async def main(which):
    rd.TOTAL = len(ORDER)
    os.makedirs(OUT, exist_ok=True)
    async with B.session(scale=1):
        for i in which:
            await ORDER[i - 1](i)
            print("slide", i, "done")
    if len(which) == len(ORDER):
        from PIL import Image
        pages = [Image.open(f"{OUT}/slide_{n:02d}.png").convert("RGB") for n in range(1, len(ORDER) + 1)]
        pages[0].save(f"{OUT}/rever_marketing_deck.pdf", save_all=True, append_images=pages[1:], resolution=96, quality=92)
        print("pdf written", len(ORDER), "pages")


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or list(range(1, len(ORDER) + 1))
    asyncio.run(main(which))
