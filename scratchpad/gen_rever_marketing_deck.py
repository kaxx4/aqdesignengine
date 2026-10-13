"""REVER x DISCO DIWALI 2026: the MARKETING deck, TerraThon look (Workflow C, bespoke build; user 2026-10-13).

Brief (user): a marketing deck for Rever, the cafe that is AquaTerra's Exclusive Food and Location Partner. It is the companion to the 29-slide partnership proposal
(scratchpad/gen_rever_deck.py), so it re-uses that deck's whole system (black ground with flecks, blue shuriken, white slabs with an orchid border, StretchPro / Sigmar One
display type, die-cut stickers, Rever's pill bottom-right) rather than restating it. The channels are the user's: Instagram (reels, posts, stories, collabs, and
follows / reach / views / shares / likes), WhatsApp (community, broadcasts, school outreach) and the 18+ school student network. The content plan is the user's list,
phase by phase. No prices slide. Contact is Pratyaksh Singhania.

EVERY FIGURE ON A SLIDE LIVES IN `FACTS` BELOW (user: "rerun a script"). Edit a number there, rerun, done. Where the two source decks disagreed, this deck uses the Rever
deck's figure for anything Rever has already seen (1,800+ WhatsApp members, 1.11M+ impressions) and the user's own words for schools ("18+"). See the open list in
brain/REVER_MARKETING_DECK.md.

Adaptations (CLAUDE.md sec 2 rule 4), recorded:
  * 1920x1080 landscape (16:9), M=96, like the proposal deck. Output is PDF (rasterised slides), not editable slides.
  * The user wrote "spam" for WhatsApp. It reads here as "broadcasts" (it is going to the cafe); flagged to the user.
  * Rever has no food or venue photo in the repo, and food imagery may not be invented (real assets only), so the menu and food items are die-cut stickers, not photos.
  * Photos are Disco Diwali 2025 / AQ event photos already in the repo, plus crops cut from the two exported PDFs by scratchpad/rever_marketing_assets.py (git-ignored).
  * No Instagram or WhatsApp logos: generic drawn icons only.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_rever_marketing_deck.py [1 2 3 ...]   ->  out/decks/rever_marketing/slide_NN.png (+ rever_marketing_deck.pdf when all are rendered)
Needs: python scratchpad/rever_marketing_assets.py once (crops), pip install playwright==1.56.0.
"""
import asyncio, importlib.util, os, sys

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
rd.OUT = OUT

# ------------------------------------------------------------------------------------------------ the facts (edit here, rerun)
FACTS = dict(
    event_date="10 November 2026",
    followers="5K+",                     # Instagram followers (both decks)
    views30="4.3 LAKH",                  # Instagram views in a recent 30 days (sponsors deck)
    summer_post="21.7K",                 # views on the Summer Sunset post (sponsors deck)
    paradox_post="9.3K",                 # views on the Paradox 2026 post (sponsors deck)
    impressions="1.11M+",                # impressions across the last few events (Rever deck)
    whatsapp="1,800+",                   # members in the WhatsApp community where Rever is promoted (Rever deck)
    schools="18+",                       # Kolkata schools in the student network (user, 2026-10-13)
    school_chips=("DBPC", "LA MARTINIERE FOR BOYS", "LA MARTINIERE FOR GIRLS", "MODERN HIGH", "LORETO", "AND OTHER LEADING KOLKATA SCHOOLS"),   # the five the Rever deck names
    contact=("PRATYAKSH SINGHANIA", "+91 98305 54654", "@ngo.aquaterra", "@aquaterra.live", "ngoaquaterra.com"),
)
F = FACTS


async def st_size(texts, maxw, cap=220):
    """Largest StretchPro size (px) at which every string fits maxw, measured with the real font (the fallback measures ~33% narrow)."""
    m = await B.measure_text([dict(text=t, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT) for t in texts], W, H, extra_css=tt.FONT_CSS)
    return min(cap, min(100 * maxw / r["text_w"] for r in m))


def card_inner(title, desc, st=None, num=None, tsize=30, dsize=24, st_h=110, gap=14):
    top = ""
    if st or num:
        top = (f'<div style="display:flex;justify-content:space-between;align-items:center;height:{st_h}px;margin-bottom:{gap}px">'
               f'{rd.numdot(num, 52, 27) if num else "<span></span>"}<div style="flex:none">{st[0] if st else ""}</div></div>')
    return (top + f'<div class="v" style="font-size:{tsize}px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:10px">{title}</div>'
            f'<div class="b" style="font-size:{dsize}px;line-height:1.3;color:{INK}">{desc}</div>')


def callout(s, y, text, size=34, w=None):
    s.pill("callout", M, y, text, size, w=w, align="left")
    s.el("callout", M, y, w or int(len(text) * size * .63 + size * 1.8 + 16), int(size * 2.1)); s.text_pair("callout", INK, CTA, size, True)


# ================================================================================================ 1 cover
async def s_cover(n):
    s = rd.Slide(n, specks_on=False)
    s.add(f'<div style="position:absolute;inset:0;background:url({rd.photo_full(PH["wall"], 1500)}) 62% 38%/cover;z-index:0;filter:brightness(1.25) saturate(1.1)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.93) 28%,rgba(0,0,0,.5) 52%,rgba(0,0,0,.08) 100%)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,0) 28%)"></div>')
    s.add(f'<div class="measure k" data-tag="eyebrow" style="position:absolute;left:{M}px;top:64px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap;letter-spacing:.08em">A MARKETING PLAN FOR REVER</div>')
    s.el("eyebrow", M, 64, 620, 28); s.text_pair("eyebrow", WHITE, GROUND, 26, False)
    s.add(f'<div class="measure k" data-tag="t1" style="position:absolute;left:{M}px;top:136px;font-size:96px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">REVER x</div>')
    s.el("t1", M, 142, 444, 84); s.text_pair("t1", WHITE, GROUND, 96, False)
    s.add(f'<div class="measure v" data-tag="year" style="position:absolute;left:{M + 484}px;top:140px;height:84px;border:8px solid {ORCHID};border-radius:999px;background:{SLAB};'
          f'display:flex;align-items:center;padding:0 34px;font-size:50px;color:{INK};z-index:6">2026</div>')
    s.el("year", M + 484, 140, 215, 84)
    s.add(f'<div class="measure v" data-tag="t2" style="position:absolute;left:{M}px;top:242px;font-size:196px;line-height:.9;color:{WHITE};z-index:6;white-space:nowrap">DISCO<br>DIWALI</div>')
    s.el("t2", M, 252, 720, 360); s.text_pair("t2", WHITE, GROUND, 196, True)
    s.add(f'<div class="measure sg" data-tag="sub" style="position:absolute;left:{M}px;top:648px;width:860px;font-size:50px;line-height:1.1;color:{ORCHID};z-index:6">'
          f'Everything we will post, send and say about Rever.</div>')
    s.el("sub", M, 648, 860, 110); s.text_pair("sub", ORCHID, GROUND, 50, True)
    inner = (f'<div style="display:flex;align-items:center;gap:36px;height:100%"><img src="{rd.REVER}" style="height:70px;flex:none">'
             f'<div style="width:5px;align-self:stretch;background:{ORCHID};border-radius:3px"></div>'
             f'<div class="v" style="font-size:38px;line-height:1.05;color:{INK}">EXCLUSIVE FOOD AND<br>LOCATION PARTNER</div></div>')
    s.slab("slab", M, 800, 960, 140, inner, rot=-1.0, pad="10px 38px", radius=44, tilt=True)
    s.text_pair("slab", INK, SLAB, 38, True)
    s.add(f'<img class="measure" data-tag="logo" src="{rd.core.LOGO}" style="position:absolute;left:{M}px;top:{H - 90}px;height:50px;z-index:9">'); s.el("logo", M, H - 90, 296, 50)
    s.pill("cta", M, H - 112, f"TEAM AQUATERRA, EST. 2021&nbsp;&nbsp;|&nbsp;&nbsp;{F['event_date'].upper()}", 28, align="right")
    s.el("cta", W - M - 700, H - 112, 700, 59); s.text_pair("cta", INK, CTA, 28, True)
    s.cord(1488, 0, 76); s.ball("st_ball", 340, 1318, 70, 0)
    s.sticker("st_mask", stk.mask(width=820, seed=3), 1040, 290, -7)
    s.sticker("st_sp1", (rd.ddt_spark(70, GREEN, "c1"), 70, 70), 1010, 230, 0, 7)
    s.sticker("st_sp2", (rd.ddt_spark(56, ORCHID, "c2"), 56, 56), 1130, 120, 0, 7)
    s.stars([(1760, 80)], 90)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 2 the plan in one page
async def s_overview(n):
    s = rd.Slide(n); s.chrome("THE PLAN IN ONE PAGE")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Rever, in every place", "our students look.", 76, 56, gap=4)
    cards = [("Instagram", F["followers"], "followers", "Reels, posts, stories and collab posts, with Rever tagged.", stk.phone(150)),
             ("WhatsApp", F["whatsapp"], "members in our community, where Rever is promoted", "Callouts to the community, broadcast lists and school groups.", mk.chat(170)),
             ("Schools", F["schools"], "Kolkata schools in our student network", "Reached directly and through our volunteers.", mk.school(180))]
    fs = await st_size([c[1] for c in cards], 440, 190)
    cw = (1728 - 2 * 28) / 3
    for i, (t, v, lab, line, st) in enumerate(cards):
        inner = (f'<div style="display:flex;justify-content:space-between;align-items:flex-start;height:190px"><div class="v" style="font-size:44px;line-height:1;color:{INK};text-transform:uppercase;padding-top:6px">{t}</div>'
                 f'<div style="flex:none">{st[0]}</div></div>'
                 f'<div class="st" style="font-size:{fs:.0f}px;line-height:1;color:{INK};white-space:nowrap;margin:6px 0 14px">{v}</div>'
                 f'<div class="v" style="font-size:25px;line-height:1.12;color:{INK};text-transform:uppercase;margin-bottom:18px">{lab}</div>'
                 f'<div class="b" style="font-size:25px;line-height:1.3;color:{INK}">{line}</div>')
        s.slab(f"card{i}", M + i * (cw + 28), 296, cw, 566, inner, pad="30px 36px")
    s.text_pair("card0", INK, SLAB, 25, True)
    s.pill("callout", M, 886, "BEFORE THE EVENT. ON THE DAY. AFTER THE EVENT.", 36, align="left")
    s.el("callout", M, 886, 1100, 76); s.text_pair("callout", INK, CTA, 36, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 3 who sees it
async def s_who(n):
    s = rd.Slide(n); s.chrome("WHO OUR MARKETING REACHES")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1600, "Who sees it.", "Students, in friend groups, on Instagram first.", 76, 56, gap=4)
    fs = await st_size(["16-19"], 480, 300)
    inner = (rd.label("Age band, roughly", 28, INK, "margin-bottom:12px") + f'<div class="st" style="font-size:{fs:.0f}px;line-height:1.05;color:{INK};white-space:nowrap">16-19</div>')
    s.slab("age", M, 300, 620, 300, inner, rot=-1.0, pad="36px 44px", tilt=True)
    s.text_pair("age", INK, SLAB, 28, False)
    rows = [("Who", "Classes 9 to 12 and college students from across Kolkata"),
            ("How they show up", "In friend groups, for birthdays, celebrations and weekend plans"),
            ("How they find things", "Instagram first, heavily influenced by peers and event content")]
    inner = "".join(f'<div style="margin-bottom:22px">{rd.label(k, 24, ORCHID)}<div class="b" style="font-size:31px;line-height:1.22;color:{WHITE};margin-top:6px">{v}</div></div>' for k, v in rows)
    s.add(f'<div class="measure" data-tag="rows" style="position:absolute;left:{M + 700}px;top:290px;width:1020px;z-index:6">{inner}</div>')
    s.el("rows", M + 700, 290, 1020, 262); s.text_pair("rows", WHITE, GROUND, 31, False)
    s.photo_rect("ph_a", PH["friends"], M, 650, 1728, 290, "50% 42%", cap="Friends at an AquaTerra evening")
    s.sticker("st_follow", mk.follow(width=170), 1560, 580, 8, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 4 instagram
async def s_insta(n):
    s = rd.Slide(n); s.chrome("INSTAGRAM  (1 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Instagram,", "in four formats.", 76, 56, gap=4)
    fm = [("Reels", "The venue, the menu, the decor and the night itself, shot at Rever and cut by our team.", stk.phone(100)),
          ("Posts", "The location drop, the sponsor mention, the layout blueprint, the menu and the thank-you.", stk.camera(130)),
          ("Stories", "Rever tagged as the venue on every story we post about the night.", stk.pin(100)),
          ("Collabs", "Event reels go out as collab posts, so they also appear on Rever's profile and reach Rever's followers.", stk.badge(96))]
    cw = (1728 - 3 * 24) / 4
    for i, (t, d, st) in enumerate(fm):
        s.slab(f"fmt{i}", M + i * (cw + 24), 290, cw, 384, card_inner(t, d, st, None, 40, 25, 104), pad="26px 30px")
    s.text_pair("fmt0", INK, SLAB, 25, False)
    tr = [("Reach", stk.megaphone(110)), ("Views", mk.eye(116)), ("Shares", mk.plane(104)), ("Likes", stk.heart(92)), ("Follows", mk.follow(100))]
    cells = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px"><div style="height:104px;display:flex;align-items:center">{st[0]}</div>'
                    f'<div class="v" style="font-size:34px;color:{WHITE};text-transform:uppercase">{t}</div></div>' for t, st in tr)
    inner = rd.label("What we track for Rever", 25, ORCHID, "margin-bottom:12px") + f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px;justify-items:center">{cells}</div>'
    s.panel("track", M, 700, 1728, 262, inner, pad="22px 40px")
    s.text_pair("track", WHITE, "#0B0B0D", 34, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 5 reach
async def s_reach(n):
    s = rd.Slide(n); s.chrome("INSTAGRAM  (2 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Reach,", "with receipts.", 76, 56, gap=4)
    fs = await st_size([F["views30"]], 640, 260)
    inner = (rd.label("Instagram, in a recent 30 days", 27, ORCHID, "margin-bottom:18px")
             + f'<div class="st" style="font-size:{fs:.0f}px;line-height:1;color:{WHITE};white-space:nowrap">{F["views30"]}</div>'
             + f'<div class="v" style="font-size:44px;line-height:1.05;color:{WHITE};margin-top:14px;text-transform:uppercase">views</div>')
    s.panel("hero", M, 290, 760, 640, inner, pad="40px 48px")
    s.text_pair("hero", WHITE, "#0B0B0D", 44, True)
    s.photo_rect("ph_a", PH["blue"], M + 44, 600, 672, 284, "50% 40%", cap="Disco Diwali 2025")
    s.sticker("st_eye", mk.eye(width=250), 530, 760, -6, 11)
    tiles = [(F["followers"], "followers on Instagram"), (F["summer_post"], "views on the Summer Sunset post"),
             (F["paradox_post"], "views on the Paradox 2026 post"), (F["impressions"], "impressions across our last few events")]
    tfs = await st_size([t[0] for t in tiles], 340, 150)
    for i, (v, l) in enumerate(tiles):
        x, y = 888 + (i % 2) * 476, 290 + (i // 2) * 332
        s.slab(f"tile{i}", x, y, 450, 308, f'<div class="st" style="font-size:{tfs:.0f}px;line-height:1;color:{INK};white-space:nowrap;margin-bottom:18px">{v}</div>'
               f'<div class="v" style="font-size:27px;line-height:1.1;color:{INK};text-transform:uppercase">{l}</div>', pad="36px 36px", fill=ORCHID if i == 0 else SLAB)
    s.text_pair("tile0", INK, ORCHID, 27, True); s.text_pair("tile1", INK, SLAB, 27, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 6 whatsapp
async def s_whatsapp(n):
    s = rd.Slide(n); s.chrome("WHATSAPP")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "WhatsApp,", "a direct line to the group chats.", 76, 56, gap=4)
    rows = [("The community", f"{F['whatsapp']} members in our WhatsApp community, where Rever is promoted for close to a month.", mk.follow(120)),
            ("Broadcasts", "Rever in every callout across our community and broadcast lists, from the venue reveal to event day.", stk.megaphone(130)),
            ("School outreach", "Class and school groups across Kolkata, reached directly and through our volunteers.", mk.school(120))]
    for i, (t, d, st) in enumerate(rows):
        inner = (f'<div style="display:flex;gap:30px;align-items:center;height:100%"><div style="flex:none;width:150px;display:flex;justify-content:center">{st[0]}</div>'
                 f'<div><div class="v" style="font-size:38px;line-height:1.05;color:{INK};text-transform:uppercase;margin-bottom:10px">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.32;color:{INK}">{d}</div></div></div>')
        s.slab(f"row{i}", M, 296 + i * 214, 1060, 190, inner, pad="12px 34px")
    s.text_pair("row0", INK, SLAB, 27, False)
    s.photo_rect("ph_a", PH["phone"], 1210, 290, 614, 640, "50% 50%", cap="Disco Diwali 2025")
    s.sticker("st_chat", mk.chat(width=240), 1186, 262, -6, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 7 schools
async def s_schools(n):
    s = rd.Slide(n); s.chrome("THE STUDENT NETWORK")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "18+ schools,", "one student network.", 76, 56, gap=4)
    fs = await st_size([F["schools"]], 420, 300)
    s.add(f'<div class="measure st" data-tag="big" style="position:absolute;left:{M}px;top:290px;font-size:{fs:.0f}px;line-height:1;color:{ORCHID};white-space:nowrap;z-index:6">{F["schools"]}</div>')
    s.el("big", M, 290, 420, int(fs)); s.text_pair("big", ORCHID, GROUND, fs, True)
    s.add(f'<div class="measure b" data-tag="body" style="position:absolute;left:{M + 470}px;top:310px;width:600px;font-size:31px;line-height:1.36;color:{WHITE};z-index:6">'
          f'Classes 9 to 12 and college students across Kolkata, reached directly and through our volunteers.</div>')
    s.el("body", M + 470, 310, 600, 170); s.text_pair("body", WHITE, GROUND, 31, False)
    chips = "".join(f'<span class="v" style="display:inline-block;background:{CTA};border:5px solid {ORCHID};border-radius:999px;padding:8px 22px;font-size:27px;color:{INK};margin:0 12px 14px 0;white-space:nowrap">{c}</span>'
                    for c in F["school_chips"])
    s.add(f'<div class="measure" data-tag="chips" style="position:absolute;left:{M}px;top:560px;width:1060px;z-index:6">{chips}</div>')
    s.el("chips", M, 560, 1060, 190); s.text_pair("chips", INK, CTA, 27, True)
    s.photo_rect("ph_a", CR + "school_banner.jpg", 1240, 250, 584, 630, "50% 50%", cap="School network", maxw=900)
    s.sticker("st_school", mk.school(width=196), M + 14, 764, -5, 11)
    s.photo_rect("ph_b", CR + "volunteers_laptops.jpg", M + 290, 780, 770, 170, "50% 40%", cap="Student volunteers", maxw=900)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 9 timeline
async def s_timeline(n):
    s = rd.Slide(n); s.chrome("THE CALENDAR")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "From sign-off", "to the last story.", 76, 56, gap=4)
    cw = 1728 / 6
    groups = [("BEFORE THE EVENT", 0, 4, ORCHID), ("ON THE DAY", 4, 5, GREEN), ("AFTER", 5, 6, BLUE)]
    for lab, a, b, col in groups:
        x = M + a * cw + 6; w = (b - a) * cw - 12
        s.add(f'<div class="measure v" data-tag="grp{a}" style="position:absolute;left:{x:.0f}px;top:290px;width:{w:.0f}px;height:60px;border-radius:999px;background:{col};border:4px solid {HALO};'
              f'display:flex;align-items:center;justify-content:center;font-size:26px;color:{INK};z-index:6;white-space:nowrap">{lab}</div>')
        s.el(f"grp{a}", x, 290, w, 60)
    s.text_pair("grp0", INK, ORCHID, 26, True); s.text_pair("grp4", INK, GREEN, 26, True); s.text_pair("grp5", INK, BLUE, 26, True)
    s.add(f'<div style="position:absolute;left:{M + 40}px;top:407px;width:{1728 - 80}px;height:6px;background:{HALO};border-radius:3px;z-index:3"></div>')
    steps = [("Partnership sign-off", "Menu, deliverables and dates locked"), ("Content shoots at Rever", "Multiple days, scheduled with Rever"),
             ("Venue reveal", "Within two weeks of sign-off. The reveal reel launches the campaign"), ("Ticket sales and promotion", "Collab reels, Rever reels and WhatsApp callouts, through to event day"),
             ("Event day", F["event_date"]), ("The week after", "Thank-you post, recap, reach and views summary, asset handover")]
    stks = [stk.clipboard(100), stk.camera(120), stk.pin(100), stk.megaphone(104), stk.mask(width=170, plume=False, seed=4), stk.heart(100)]
    for i, (t, d) in enumerate(steps):
        cx = M + i * cw + cw / 2
        hot = i == 4
        s.add(f'<div style="position:absolute;left:{cx - 31:.0f}px;top:379px;z-index:7">{rd.numdot(i + 1, 62, 32, GREEN if hot else (BLUE if i == 5 else ORCHID))}</div>')
        text = (f'<div class="v" style="font-size:29px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:12px">{t}</div>'
                f'<div class="b" style="font-size:24px;line-height:1.3;color:{INK}">{d}</div>')
        s.slab(f"st{i}", M + i * cw + 6, 450, cw - 12, 420, f'<div style="display:flex;flex-direction:column;justify-content:space-between;height:100%"><div>{text}</div>'
               f'<div style="display:flex;justify-content:flex-end">{stks[i][0]}</div></div>', pad="26px 22px", fill=GREEN if hot else SLAB, border=8, radius=28)
    s.text_pair("st0", INK, SLAB, 24, False)
    callout(s, 892, "THE SOONER WE SIGN OFF, THE MORE OF THE MONTH WE CAN PROMOTE.", 30, 1360)
    s.sticker("st_clock", stk.clock(width=170), 1650, 60, 8)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 10 before
async def s_before(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (1 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "Before the event,", "Rever goes up first.", 76, 56, gap=4)
    items = [("Location drop post", "Rever Skydeck announced as the venue.", stk.pin(80)), ("Sponsor mention post", "Rever announced as our Exclusive Food and Location Partner.", stk.shirt(84)),
             ("Blueprint post", "A basic layout of how the location will look on the day.", stk.clipboard(76)), ("Location showcase reel", "Rever Skydeck on camera, shot by our team.", stk.phone(74)),
             ("Menu post", "The event menu that Rever's kitchen designs.", stk.cloche(88)), ("Fun menu reels", "Fun reels starring the items on the menu.", stk.burger(84)),
             ("Collabs and callouts", "Collab posts, stories and WhatsApp callouts, all the way to event day.", stk.heart(76))]
    cw, ch = (1728 - 3 * 24) / 4, 316
    for i, (t, d, st) in enumerate(items):
        s.slab(f"it{i}", M + (i % 4) * (cw + 24), 290 + (i // 4) * (ch + 24), cw, ch, card_inner(t, d, st, i + 1, 27, 22, 88, 6), pad="20px 24px")
    s.text_pair("it0", INK, SLAB, 22, False)
    fs = await st_size(["MANY", "MORE"], 330, 92)
    s.slab("more", M + 3 * (cw + 24), 290 + (ch + 24), cw, ch, f'<div class="st" style="font-size:{fs:.0f}px;line-height:1;color:{INK};display:flex;flex-direction:column;justify-content:center;height:100%">AND<br>MANY<br>MORE</div>', fill=ORCHID, border=10, pad="30px 30px", rot=-1.2, tilt=True)
    s.text_pair("more", INK, ORCHID, fs, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 11 on the day
async def s_day(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (2 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "On the day,", "10 November. We film everything.", 76, 56, gap=4)
    items = [("Decor going up", "A reel of the decor going up, as the room turns into Disco Diwali.", stk.camera(120)),
             ("Registration, and a walk through", "Registration has started: a full run through the location, with Rever's space in frame.", stk.clipboard(100)),
             ("Fun reels, all night", "Fun reels in general, from the first guest through to the last song.", stk.phone(96))]
    for i, (t, d, st) in enumerate(items):
        inner = (f'<div style="display:flex;gap:28px;align-items:center;height:100%"><div style="flex:none;width:130px;display:flex;justify-content:center">{st[0]}</div>'
                 f'<div><div class="v" style="font-size:32px;line-height:1.05;color:{INK};text-transform:uppercase;margin-bottom:10px">{t}</div>'
                 f'<div class="b" style="font-size:25px;line-height:1.3;color:{INK}">{d}</div></div></div>')
        s.slab(f"row{i}", M, 296 + i * 214, 980, 190, inner, pad="12px 32px")
    s.text_pair("row0", INK, SLAB, 25, False)
    s.photo_rect("ph_a", CR + "reg_desk.jpg", 1110, 290, 714, 280, "40% 50%", cap="Registration, Disco Diwali 2025", maxw=1200)
    s.photo_rect("ph_b", CR + "decor_globe.jpg", 1110, 600, 714, 330, "50% 50%", cap="The stage, Disco Diwali 2025", maxw=900)
    s.sticker("st_sp", (rd.ddt_spark(64, GREEN, "c21"), 64, 64), 1070, 250, 0, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 12 after
async def s_after(n):
    s = rd.Slide(n); s.chrome("THE CONTENT PLAN  (3 OF 3)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "After the event,", "the story keeps going.", 76, 56, gap=4)
    items = [("Decor dump", "A photo dump of the finished decor.", stk.camera(124)), ("Favourite item reel", "Guests answer on camera: what was your favourite item on the menu?", stk.cloche(110)),
             ("Location reviews reel", "Guests say what they thought of the location, on camera.", stk.review(150)), ("Thank-you post", "A thank-you to Rever and to everyone who came.", stk.heart(100)),
             ("Podcast with the owner", "A sit-down podcast with Rever's owner.", mk.mic(96))]
    cw, ch = (1728 - 2 * 24) / 3, 300
    for i, (t, d, st) in enumerate(items):
        s.slab(f"it{i}", M + (i % 3) * (cw + 24), 290 + (i // 3) * (ch + 24), cw, ch, card_inner(t, d, st, i + 1, 30, 25, 112, 8), pad="24px 30px")
    s.text_pair("it0", INK, SLAB, 25, False)
    inner = (f'<div class="v" style="font-size:30px;line-height:1.06;color:{INK};text-transform:uppercase;margin-bottom:12px">The report</div>'
             f'<div class="b" style="font-size:25px;line-height:1.3;color:{INK}">A reach and views summary, as promised in the proposal, plus the photo and video assets for Rever to keep using.</div>')
    s.slab("report", M + 2 * (cw + 24), 290 + (ch + 24), cw, ch, inner, fill=GREEN, border=10, pad="30px 30px", rot=1.0, tilt=True)
    s.text_pair("report", INK, GREEN, 25, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 13 what we need
async def s_need(n):
    s = rd.Slide(n); s.chrome("WHAT WE NEED FROM REVER")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "What we need from Rever.", "Four things, so the plan runs.", 76, 56, gap=4)
    items = [("Access to Skydeck", "Shoot days at Rever Skydeck, across multiple days and scheduled with Rever.", stk.pin(120)),
             ("Menu and handle", "The event menu and its items for the posts and reels, and Rever's Instagram handle so every collab post goes out on both profiles.", stk.cloche(130)),
             ("Approvals", "Rever approves every post, reel and broadcast that carries its name before it goes out.", stk.badge(112)),
             ("Your people", "One named contact to coordinate with, and the owner's time for the podcast.", mk.mic(104))]
    for i, (t, d, st) in enumerate(items):
        x, y = M + (i % 2) * 888, 296 + (i // 2) * 286
        inner = (f'<div style="display:flex;gap:26px;height:100%"><div style="flex:1"><div class="v" style="font-size:36px;line-height:1.05;color:{INK};margin-bottom:14px;text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.34;color:{INK}">{d}</div></div>'
                 f'<div style="flex:none;width:150px;display:flex;justify-content:center;padding-top:6px">{st[0]}</div></div>')
        s.slab(f"card{i}", x, y, 840, 262, inner, pad="28px 34px")
    s.text_pair("card0", INK, SLAB, 27, False)
    callout(s, 876, "WE SHOOT, POST AND SEND. REVER APPROVES.", 34, 980)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ 14 close
async def s_next(n):
    s = rd.Slide(n); s.chrome("NEXT STEPS")
    s.stars([(1760, 560)], 90)
    await s.heading(M, 104, 1180, "Let's put Rever", "in front of Kolkata's students.", 76, 54)
    steps = [("Sign off", "Menu, deliverables and dates locked"), ("Shoot at Rever", "Multiple days, scheduled with Rever"), ("Venue reveal", "Within two weeks of sign-off")]
    sx = M
    for i, ((t, d), sw) in enumerate(zip(steps, (340, 340, 340))):
        inner = (f'<div style="display:flex;flex-direction:column;gap:10px">{rd.numdot(i + 1, 56, 30)}<div class="v" style="font-size:29px;line-height:1.08;color:{INK};text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:22px;line-height:1.28;color:{INK}">{d}</div></div>')
        s.slab(f"step{i}", sx, 320, sw, 270, inner, rot=(-1.2, .9, -.8)[i], pad="22px 26px", tilt=False)
        sx += sw + 20
    s.text_pair("step0", INK, SLAB, 29, True)
    name, phone, ig1, ig2, web = F["contact"]
    inner = (rd.label("Contact", 24, INK, "margin-bottom:8px") + f'<div class="v" style="font-size:54px;line-height:1.1;color:{INK}">{name}</div>'
             f'<div class="k" style="font-size:30px;color:{INK};margin:8px 0 18px">Team AquaTerra&nbsp;&nbsp;|&nbsp;&nbsp;{phone}</div>'
             f'<div class="b" style="font-size:30px;line-height:1.35;color:{INK}">Instagram: <b>{ig1}</b> | <b>{ig2}</b><br>{web}</div>')
    s.slab("contact", M, 620, 1060, 316, inner, pad="26px 40px")
    s.text_pair("contact", INK, SLAB, 30, False)
    s.add(f'<div class="measure" data-tag="rever_logo" style="position:absolute;left:1290px;top:96px;width:440px;height:440px;border-radius:50%;background:#fff;border:16px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8">'
          f'<img src="{rd.REVER}" style="width:320px"></div>')
    s.el("rever_logo", 1290, 96, 440, 440)
    s.add(f'<div class="measure" data-tag="qr" style="position:absolute;left:1350px;top:590px;width:320px;height:320px;border-radius:36px;background:#fff;border:14px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8;transform:rotate(3deg)">'
          f'<img src="{rd.QR}" style="width:250px;height:250px"></div>')
    s.el("qr", 1350, 590, 320, 320)
    s.add(f'<div class="measure k" data-tag="qrcap" style="position:absolute;left:1330px;top:922px;width:360px;text-align:center;font-size:21px;color:{WHITE};z-index:9">SCAN FOR {ig1.upper()}</div>')
    s.el("qrcap", 1330, 922, 360, 24); s.text_pair("qrcap", WHITE, GROUND, 21, False)
    s.cord(1815, 0, 280); s.ball("st_ball", 150, 1740, 270, 0)
    s.sticker("st_mask", stk.mask(width=200, plume=False, seed=5), 1676, 700, -10)
    s.sticker("st_diya", rd.ddt_diya(140), 1166, 800, 6, 10)
    s.sticker("st_sp", (rd.ddt_spark(60, GREEN, "c14"), 60, 60), 1270, 560, 0, 7)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ================================================================================================ the running order
def photo_slide(*a, **k):
    async def run(n): await rd.photo_full_slide(n, *a, **k)
    return run


ORDER = [
    s_cover,
    s_overview,
    s_who,
    s_insta,
    s_reach,
    s_whatsapp,
    s_schools,
    photo_slide("purple", "One night.\n300 to 350 guests.", "Crowd at Disco Diwali 2025", "50% 45%", stickers=[(stk.mask(width=260, plume=False, seed=2), 1560, 110, 8)]),
    s_timeline,
    s_before,
    s_day,
    s_after,
    s_need,
    s_next,
]


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
