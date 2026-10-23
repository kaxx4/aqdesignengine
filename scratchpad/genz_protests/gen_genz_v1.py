"""GEN Z PROTESTS, SEVEN COUNTRIES — Workflow C, bespoke build (8 slides: cover + 7).

Reference post (instagram.com/p/Deuz70koONs, slide 4) was UNREACHABLE from the build
environment (DNS failure), so no reference was matched. The style bank draw
(b2d4cc55d7fdbb, instrument vignettes) has no bearing on a text-dense explainer and was
discarded per the section 2 precedence ladder (mechanism cannot survive the content).
Pattern used instead: CAROUSEL_PLAYBOOK type slide (cream ground, accent field, measured
spacing, paper cards with ink outline + hard shadow).

Adaptations recorded:
- accent rotates per country (7 slides, 7 accents) instead of one semantic department hue:
  the carousel's job is telling seven stories apart; content=grape is used on the cover.
- body copy is lowercase per house rule; country names are the only display caps.
- every figure is from the cited outlets in the SOURCES line of its slide; none invented.
"""
import asyncio, os, sys, importlib.util

_r = os.path.abspath(__file__)
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
os.chdir(_r)
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
INK, PAPER = core.INK, core.PAPER
OUT = "out/genz_protests/v1"

# accent per country: pink, mint, lemon, tomato, sky, grape, teal
COUNTRIES = [
    dict(name="india", tag="ladakh · sept 2025", acc=3,
         cause="ladakh became a union territory in 2019. after peaceful protests and a hunger strike by activist sonam wangchuk brought no result, young people took to the streets of leh.",
         demands="statehood, sixth schedule status, a second lok sabha seat and a ladakh public service commission.",
         response="prohibitory orders in leh. reports say at least four people were killed and over 50 injured. the home ministry blamed “politically motivated individuals”. talks were set for 6 october.",
         src="al jazeera · deccan herald · tribune india", note=""),
    dict(name="france", tag="bloquons tout · sept 2025", acc=4,
         cause="an online call to “block everything” on 10 september, aimed at the budget cuts of prime minister françois bayrou, which included scrapping two public holidays.",
         demands="an end to austerity. the grievances run wider: purchasing power, social justice and political reform.",
         response="bayrou stepped down the day before. officials counted nearly 200,000 protesters, deployed over 80,000 security personnel and reported almost 500 arrests.",
         src="wikipedia · new statesman · deccan herald", note="gen z label is disputed by media"),
    dict(name="spain", tag="housing · sept to oct 2026", acc=2,
         cause="an 87-year-old woman was evicted in madrid. tent camps followed and protests spread to about 50 cities. spain is short roughly 750,000 homes.",
         demands="stronger tenant protections, action on housing fraud, and no evictions unless alternative housing exists.",
         response="the government issued emergency decrees on evictions, speculation and indefinite leases. parliament voted two of them down. police used tear gas and rubber bullets in valencia.",
         src="al jazeera · reuters · euronews", note="a renters' movement, young adults among them"),
    dict(name="brazil", tag="election season · oct 2026", acc=0,
         cause="online gen z groups, modelled on nepal's 2025 uprising, have been organising ahead of the 2026 election. in october, students marched in 14 states.",
         demands="no single list yet. groups call for deep political change, defence of democracy, and better study and work conditions.",
         response="no formal federal response reported yet. rio police arrested three suspects linked to a gen z group over alleged attack plans.",
         src="brasil de fato · jornal opção · politize", note="thin sourcing, marches tied to the presidential race"),
    dict(name="albania", tag="tirana · oct 2026", acc=5,
         cause="corruption, the cost of education and a coastal resort deal tied to jared kushner brought students and a wider movement onto the streets.",
         demands="prime minister edi rama resigns. students also list education and healthcare reform.",
         response="rama refused to resign and blamed “foreign hands”. police used tear gas, water cannon and rubber bullets. hundreds of injuries and arrests were reported.",
         src="al jazeera · nbc news · balkan insight", note=""),
    dict(name="kenya", tag="finance bill · june 2024 on", acc=1,
         cause="the finance bill 2024 proposed new taxes on everyday goods, including bread and mobile money. protesters called it taxation without jobs.",
         demands="scrap the bill. later asks: end police killings, stop borrowing, and give young people jobs.",
         response="ruto declined to sign and dissolved his cabinet. rights groups count at least 60 deaths. a later $15m compensation fund covers 1,100 people. no officer has been convicted.",
         src="al jazeera · csis · global voices", note=""),
    dict(name="chile", tag="students · 2026", acc=6,
         cause="president kast's budget cuts to education and health. students and teachers say free university tuition is under threat.",
         demands="protect free tuition, reverse the education cuts, and drop the planned register of “vandals” that could strip benefits.",
         response="at least 20 were detained at the 3 june march. a national strike followed on 1 october. kast's approval sits near 30%.",
         src="cnn español · la jornada · infobae", note="student-led movement"),
]

FS_BODY, LH_BODY = 24, 1.4
PAD, BORDER = 28, 4
CARD_W = W - 2 * M
BODY_W = CARD_W - 2 * PAD - 2 * BORDER
LABEL_H = 36


def logo():
    return (f'<img src="{core.LOGO}" style="position:absolute;top:44px;left:{M}px;height:56px;'
            f'z-index:20;display:block">')


def dots(n, active, acc):
    out = f'<div style="position:absolute;top:66px;right:{M}px;z-index:20;display:flex;gap:8px">'
    for i in range(n):
        on = i == active
        out += (f'<span style="width:11px;height:11px;border-radius:50%;'
                f'background:{acc if on else "transparent"};border:2px solid var(--ink)"></span>')
    return out + "</div>"


def footer():
    return (f'<div style="position:absolute;bottom:40px;left:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:13px;letter-spacing:.06em;color:var(--ink)">@ngo.aquaterra</div>')


async def main():
    os.makedirs(OUT, exist_ok=True)
    items = [dict(text=c["name"].upper(), font="d", size=100, weight=900) for c in COUNTRIES]
    SIZES_TRY = (24, 26, 28, 30, 32)
    for sz in SIZES_TRY:
        for c in COUNTRIES:
            for k in ("cause", "demands", "response"):
                items.append(dict(text=c[k], font="e", size=sz, weight=500, max_width=BODY_W))
    for ln in ("the streets", "takes to"):
        items.append(dict(text=ln.upper(), font="d", size=100, weight=900))
    async with B.session():
        meas = await B.measure_text(items, W, H)
        hero_m = meas[:7]
        body_by = {sz: meas[7 + n * 21: 7 + (n + 1) * 21] for n, sz in enumerate(SIZES_TRY)}
        title_m = meas[7 + 5 * 21:]
        jobs = []

        # ---------------- country slides ----------------
        for i, c in enumerate(COUNTRIES):
            acc = A[c["acc"]]
            ink_on = core.text_on(acc, large=True)
            els = []
            hero_fs = min(210, int(100 * (W - 2 * M - 16) / hero_m[i]["text_w"]))
            band_y, band_h = 124, 290
            inner = ''
            inner += (f'<div style="position:absolute;top:{band_y}px;left:0;right:0;height:{band_h}px;'
                      f'background:{acc};border-top:5px solid var(--ink);border-bottom:5px solid var(--ink);'
                      f'z-index:2"></div>')
            els.append(("band", 0, band_y, W, band_h))
            kick = f'{i+2:02d} / 08 &middot; {c["tag"]}'
            inner += (f'<div style="position:absolute;top:{band_y+30}px;left:{M}px;z-index:6;'
                      f'font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.14em;'
                      f'text-transform:uppercase;color:{ink_on}">{kick}</div>')
            els.append(("kicker", M, band_y + 30, 760, 24))
            hero_y = band_y + 74
            hero_h = int(hero_fs * 0.9)
            inner += (f'<div style="position:absolute;top:{hero_y}px;left:{M}px;z-index:6;'
                      f'font-family:var(--d);font-weight:900;font-size:{hero_fs}px;line-height:.9;'
                      f'text-transform:uppercase;white-space:nowrap;color:{ink_on}">{c["name"]}</div>')
            els.append(("hero", M, hero_y, int(hero_m[i]["text_w"] * hero_fs / 100), hero_h))

            y0 = band_y + band_h + 34
            room = (H - 112 - 30) - y0          # stop 30px above the sources line
            def stack(sz):
                hs = [BORDER * 2 + 22 + LABEL_H + 12 + round(body_by[sz][i * 3 + j]["lines"] * sz * LH_BODY) + 24
                      for j in range(3)]
                return hs, sum(hs)
            fs = max([sz for sz in SIZES_TRY if stack(sz)[1] + 2 * 22 <= room] or [24])
            heights, tot = stack(fs)
            gap = min(40, (room - tot) // 2)
            y = y0
            for j, lab in enumerate(("cause", "demands", "response")):
                ch = heights[j]
                inner += (f'<div style="position:absolute;top:{y}px;left:{M}px;width:{CARD_W}px;height:{ch}px;'
                          f'background:{PAPER};border:{BORDER}px solid var(--ink);border-radius:22px;'
                          f'box-shadow:8px 8px 0 var(--ink);z-index:5;padding:22px {PAD}px 24px">'
                          f'<span style="display:inline-block;height:{LABEL_H}px;line-height:{LABEL_H-6}px;'
                          f'padding:0 16px;background:{acc};color:{core.text_on(acc)};border:3px solid var(--ink);'
                          f'border-radius:999px;font-family:var(--m);font-weight:700;font-size:15px;'
                          f'letter-spacing:.14em;text-transform:uppercase">{lab}</span>'
                          f'<div style="margin-top:12px;font-family:var(--e);font-weight:500;'
                          f'font-size:{fs}px;line-height:{LH_BODY};color:var(--ink)">{c[lab]}</div></div>')
                els.append((f"card{j}", M, y, CARD_W, ch))
                y += ch + gap
            src_y = H - 112
            line = f'sources: {c["src"]}' + (f' &middot; note: {c["note"]}' if c["note"] else "")
            inner += (f'<div style="position:absolute;top:{src_y}px;left:{M}px;right:{M}px;z-index:6;'
                      f'font-family:var(--m);font-weight:500;font-size:14px;letter-spacing:.05em;'
                      f'text-transform:uppercase;line-height:1.5;color:var(--ink)">{line}</div>')
            els.append(("sources", M, src_y, W - 2 * M, 44))
            inner += logo() + dots(8, i + 1, acc) + footer()
            els += [("logo", M, 44, 180, 56), ("dots", W - M - 150, 66, 150, 11), ("footer", M, H - 60, 160, 20)]
            jobs.append((B.page(W, H, "var(--bg)", inner, grain=False),
                         f"{OUT}/s{i+2:02d}_{c['name']}.png", els, y - gap))

        # ---------------- cover ----------------
        cacc = A[5]
        els = []
        inner = ''
        inner += (f'<div style="position:absolute;top:640px;left:0;right:0;height:420px;background:{cacc};'
                  f'border-top:5px solid var(--ink);border-bottom:5px solid var(--ink);z-index:2"></div>')
        els.append(("band", 0, 640, W, 420))
        inner += (f'<div style="position:absolute;top:150px;left:{M}px;z-index:6;font-family:var(--m);'
                  f'font-weight:700;font-size:17px;letter-spacing:.14em;text-transform:uppercase">'
                  f'01 / 08 &middot; seven countries, one generation</div>')
        els.append(("kicker", M, 150, 760, 24))
        tfs = int(100 * (W - 2 * M) / title_m[0]["text_w"])
        for k, ln in enumerate(("gen z", "takes to", "the streets")):
            tw = {0: 560 * tfs / 168, 1: title_m[1]["text_w"] * tfs / 100, 2: title_m[0]["text_w"] * tfs / 100}[k]
            inner += (f'<div style="position:absolute;top:{200+k*int(tfs*.92)}px;left:{M}px;z-index:6;'
                      f'font-family:var(--d);font-weight:900;font-size:{tfs}px;line-height:.9;'
                      f'text-transform:uppercase;white-space:nowrap;color:var(--ink)">{ln}</div>')
            els.append((f"title{k}", M, 200 + k * int(tfs * .92), int(tw), int(tfs * .9)))
        pos = [(64, 668), (360, 668), (664, 668), (64, 788), (372, 788), (660, 788), (64, 908)]
        for c, (cx, cy) in zip(COUNTRIES, pos):
            col = A[c["acc"]]
            inner += (f'<div style="position:absolute;top:{cy}px;left:{cx}px;z-index:6;">'
                      f'<span style="display:inline-block;background:{col};color:{core.text_on(col)};'
                      f'font-family:var(--d);font-weight:900;font-size:44px;text-transform:uppercase;'
                      f'padding:10px 26px;border-radius:999px;border:4px solid var(--ink);'
                      f'box-shadow:6px 6px 0 var(--ink)">{c["name"]}</span></div>')
        els.append(("chips", 64, 668, 900, 300))
        inner += (f'<div style="position:absolute;top:1096px;left:{M}px;right:{M+80}px;z-index:6;'
                  f'font-family:var(--e);font-weight:500;font-size:30px;line-height:1.35;color:var(--ink)">'
                  f'what sparked it, what they want, and how governments answered. one slide each.</div>')
        els.append(("sub", M, 1096, W - 2 * M - 80, 84))
        inner += (f'<div style="position:absolute;top:1218px;left:{M}px;z-index:6;font-family:var(--m);'
                  f'font-weight:700;font-size:17px;letter-spacing:.14em;text-transform:uppercase">swipe &rarr;</div>')
        els.append(("swipe", M, 1218, 200, 24))
        inner += logo() + dots(8, 0, cacc) + footer()
        els += [("logo", M, 44, 180, 56), ("dots", W - M - 150, 66, 150, 11), ("footer", M, H - 60, 160, 20)]
        jobs.insert(0, (B.page(W, H, "var(--bg)", inner, grain=False), f"{OUT}/s01_cover.png", els, 1242))

        for html, out, els, last in jobs:
            print(out, "content ends y=", last)
            await B.render(html, out, W, H, elements=els, page_bg="var(--bg)",
                           containers=("band", "card0", "card1", "card2", "chips"),
                           collision_ignore={("band", "kicker"), ("band", "hero"),
                                             ("band", "title0"), ("band", "title1"), ("band", "title2")})
    print("done")


asyncio.run(main())
