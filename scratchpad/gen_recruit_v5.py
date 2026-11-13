"""AQ recruitment v5: ONE message, said directly. "A STUDENT [did a real thing] THIS."

Owner brief (2026-11-13): "more direct, cleaner, more visually appealing stuff around a certain message."
v2 to v4 gave every piece its own clever idea and its own skeleton. v5 does the opposite: one sentence pattern, three
quiet layouts, one real photo per department, one real fact, the exit. Nothing else on the page.

THE SYSTEM (every piece)
  headline   "A STUDENT <verb phrase> THIS." in NeutralFace caps, the verb phrase on a lane-colour highlight bar
  proof      one mono line with one real fact and its qualifier (K.FACTS)
  chrome     logo, lane chip, the URL pill. No doodles, no stickers, no second headline.
LAYOUTS
  L1 PHOTO   full-bleed real photo, a graded scrim, headline lower third, white type
  L2 SLAB    framed photo on a lane-colour ground, headline underneath
  L3 TYPE    cream ground, headline up top, one real artifact (a slide, a cover, a number) below
Feed 1080x1350 and story 1080x1920 (top 200 and bottom 250 stay clear of the Instagram UI).
ADAPTATIONS: the earlier '(just a student)' tab is dropped, the headline carries it. Copy uses only K.FACTS and the
ShikshAQ cleared facts (Kolkata, classes IV to XII, boards, shikshaq.in).
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
core, B = K.core, K.B
W = 1080
INK, CREAM, PAPER = K.INK, K.CREAM, K.PAPER
M = 64
OUT = "out/recruit_nov2026/v5"

def chip_right(dept, y, x_right=W - M):
    lab, col = K.LANE[dept]
    w = int(len(lab) * 15 * .66 + 36)
    return K.t(lab, x_right - w, y, 15, color=core.text_on(col), font="m", weight=700, ls=.06, upper=True, tag="lane", z=30,
               extra=f"background:{col};border:3px solid #0A0A0A;box-shadow:4px 4px 0 #0A0A0A;padding:6px 12px;")

def url_pill(y, dark=True, w=None):
    s = K.URL
    w = w or int(len(s) * 15.6 + 80)
    bg, fg = (INK, K.LEM) if dark else (CREAM, INK)
    return (f'<div style="position:absolute;left:{M}px;top:{y}px;width:{w}px;height:60px;border-radius:999px;background:{bg};z-index:30;'
            f'{"" if dark else "border:3px solid #0A0A0A;"}"></div>'
            + K.t(s, M + 36, y + 17, 23, color=fg, font="m", weight=700, ls=.02, z=31, upper=False, tag="url"))

async def fit_size(lines, maxw=W - 2 * M, cap=150):
    txt = [" ".join(t for t, _ in ln) for ln in lines]
    ws = await K.mw([dict(text=s, font="d", size=150, weight=900) for s in txt])
    need = []
    for ln, w in zip(lines, ws):
        pad = sum(.26 for _, h in ln if h)          # highlight padding, in em
        need.append(w / 150 + pad)
    return int(min(cap, maxw / max(need)))

STEP = 1.08
def head(lines, size, x, y, color, hlbg, hlfg, tag="h"):
    out = []; step = round(size * STEP)
    for i, ln in enumerate(lines):
        sp = ""
        for txt, hl in ln:
            if hl:
                sp += (f'<span style="display:inline-block;background:{hlbg};color:{hlfg};padding:0 {round(size*.13)}px;margin:0 -{round(size*.02)}px;'
                       f'border:3px solid #0A0A0A">{txt}</span>')
            else:
                sp += f'<span>{txt}</span>'
        out.append(f'<div class="measure" data-tag="{tag}{i}" style="position:absolute;left:{x}px;top:{y+i*step}px;white-space:nowrap;font-family:var(--d);'
                   f'font-weight:900;font-size:{size}px;line-height:{step}px;color:{color};text-transform:uppercase;z-index:10">{sp}</div>')
    return "".join(out), len(lines) * step

def proof(txt, x, y, color, w=952):
    return K.t(txt, x, y, 21, color=color, font="m", weight=700, ls=.02, w=w, lh=30, z=12, upper=False, tag="proof")

def safe(H, story):
    return (200, 250) if story else (0, 0)

# ---------------------------------------------------------------------------------------------- L1: full-bleed photo
async def L1(name, dept, photo, lines, fact, fx=.5, fy=.5, story=False, zoom=1.0, text_at='bottom'):
    H = 1920 if story else 1350
    top, bot = safe(H, story)
    lab, col = K.LANE[dept]
    ph = K.cover(photo, W, H, fx=fx, fy=fy, zoom=zoom)
    P = [K.img(K.uri(ph), 0, 0, W, H, z=1),
         K.box(0, 0, W, H, ("background:linear-gradient(180deg,rgba(10,10,10,.30) 0%,rgba(10,10,10,0) 22%,rgba(10,10,10,0) 38%,rgba(10,10,10,.82) 100%);" if text_at != 'top' else
                              "background:linear-gradient(180deg,rgba(10,10,10,.78) 0%,rgba(10,10,10,.62) 28%,rgba(10,10,10,0) 52%,rgba(10,10,10,0) 80%,rgba(10,10,10,.6) 100%);"), z=2)]
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip_right(dept, 56 + top))
    size = await fit_size(lines)
    uy = H - bot - 64 - 60          # url pill
    py = uy - 30 - 34               # proof line
    hh = len(lines) * round(size * STEP)
    hy = py - 26 - hh
    if text_at == 'top':
        hy = 175 + top; py = hy + hh + 18
    h, _ = head(lines, size, M, hy, "#FFFFFF", col, core.text_on(col))
    P += [h, proof(fact, M, py, "#FFFFFF"), url_pill(uy)]
    await K._render(name + ("_story" if story else ""), K.page("".join(P), H), H, None, None)

# ---------------------------------------------------------------------------------------------- L2: framed photo on lane colour
async def L2(name, dept, photo, lines, fact, fx=.5, fy=.5, story=False, zoom=1.0):
    H = 1920 if story else 1350
    top, bot = safe(H, story)
    lab, col = K.LANE[dept]
    fg = core.text_on(col)
    P = [K.box(0, 0, W, H, f"background:{col};", z=0)]
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip_right(dept, 56 + top))
    uy = H - bot - 64 - 60; py = uy - 30 - 34
    size = await fit_size(lines)
    hh = len(lines) * round(size * STEP); hy = py - 30 - hh
    fy0 = 150 + top; fh = hy - 40 - fy0
    ph = K.cover(photo, W - 2 * M, fh, fx=fx, fy=fy, zoom=zoom)
    P.append(f'<div style="position:absolute;left:{M}px;top:{fy0}px;width:{W-2*M}px;height:{fh}px;border:4px solid #0A0A0A;border-radius:30px;overflow:hidden;box-shadow:8px 8px 0 #0A0A0A;z-index:5">'
             f'<img src="{K.uri(ph)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    h, _ = head(lines, size, M, hy, fg, CREAM, INK)
    P += [h, proof(fact, M, py, fg), url_pill(uy)]
    await K._render(name + ("_story" if story else ""), K.page("".join(P), H, bg=col), H, None, None)

# ---------------------------------------------------------------------------------------------- L3: type-led, one artifact
async def L3(name, dept, lines, fact, arts=None, chips=None, number=None, story=False, big=None, lane_row=False):
    H = 1920 if story else 1350
    top, bot = safe(H, story)
    lab, col = K.LANE[dept]
    P = [K.logo(M, 48 + top), chip_right(dept, 56 + top)]
    size = await fit_size(lines)
    hy = 190 + top
    h, hh = head(lines, size, M, hy, INK, col, core.text_on(col))
    P.append(h)
    uy = H - bot - 64 - 60; py = uy - 30 - 34
    y0 = hy + hh + 40
    if arts:
        from PIL import Image
        maxh = py - 30 - y0
        n = len(arts)
        dims = [Image.open(K.IMG + a_[0]).size for a_ in arts]
        ratio = max(h_ / w_ for w_, h_ in dims)
        aw = int(min((W - 2 * M) / n * 1.10, maxh / ratio))
        total = aw * n - 40 * (n - 1)
        x0 = (W - total) // 2
        for i, (path, rot, yoff) in enumerate(arts):
            w_, h_ = dims[i]; ah = int(aw * h_ / w_)
            ay = y0 + (maxh - ah) // 2 + yoff
            P.append(f'<div style="position:absolute;left:{x0 + i*(aw-40)}px;top:{ay}px;width:{aw}px;height:{ah}px;transform:rotate({rot}deg);border:4px solid #0A0A0A;'
                     f'border-radius:20px;overflow:hidden;box-shadow:9px 9px 0 #0A0A0A;z-index:{6+i}"><img src="{K.uri(K.cover(path, aw, ah))}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    if chips:
        cx, cy = M, y0 + 10
        cws = await K.mw([dict(text=c, font="d", size=34, weight=900) for c in chips])
        for c, tw_ in zip(chips, cws):
            cw = int(tw_ + 60 + 6)
            if cx + cw > W - M: cx, cy = M, cy + 108
            P.append(f'<div style="position:absolute;left:{cx}px;top:{cy}px;height:84px;padding:0 30px;border:3px solid #0A0A0A;border-radius:999px;background:{PAPER};box-shadow:6px 6px 0 #0A0A0A;'
                     f'font-family:var(--d);font-weight:900;font-size:34px;line-height:78px;text-transform:uppercase;color:{INK};z-index:6">{c}</div>')
            cx += cw + 20
    if big:
        P.append(K.t(big, M - 4, py - 190, 150, color=INK, font="m", weight=700, lh=150, tag="big", z=6, upper=False, ls=-.04))
    if number:
        P.append(K.t(number[0], M - 6, y0 - 10, 250, color=INK, font="d", weight=900, lh=250, tag="num", z=6, upper=True))
        P.append(K.t(number[1], M, y0 + 250, 34, color=INK, font="e", weight=600, w=900, lh=44, tag="numcap", z=6))
    if lane_row:
        names = ["events", "welfare", "crftd", "shikshaq", "social media", "blogs", "collabs", "hr"]
        cx, cy = M, y0 + 330
        for n_ in names:
            lab, col_ = K.LANE[{"social media": "social"}.get(n_, n_)]
            cw = int(len(n_) * 23 * .64 + 44)
            if cx + cw > W - M: cx, cy = M, cy + 78
            P.append(f'<div style="position:absolute;left:{cx}px;top:{cy}px;height:62px;padding:0 20px;border:3px solid #0A0A0A;border-radius:999px;background:{col_};color:{core.text_on(col_)};'
                     f'font-family:var(--m);font-weight:700;font-size:23px;line-height:56px;letter-spacing:.04em;text-transform:uppercase;z-index:6">{n_}</div>')
            cx += cw + 12
    P += [proof(fact, M, py, "#5A5A55"), url_pill(uy)]
    await K._render(name + ("_story" if story else ""), K.page("".join(P), H), H, None, None)

PH = K.PH
async def main(only=None):
    jobs = [
        ("a1_events", lambda s: L1("a1_events", "events", PH["dd_dhol"], [[("A STUDENT", False)], [("BOOKED THE DHOL", True)], [("FOR THIS.", False)]],
            "disco diwali 2.0 drew 550 registrations and 10+ small businesses.", fy=.4, story=s)),
        ("a2_dogs", lambda s: L1("a2_dogs", "welfare", PH["dog_bhowanipur"], [[("A STUDENT", False)], [("FED THESE DOGS", True)]],
            "tails and treats. edition 53, first run january 2022.", fy=.45, story=s)),
        ("a3_sundarbans", lambda s: L1("a3_sundarbans", "welfare", PH["sundarbans"], [[("STUDENTS", False)], [("RAN THIS HEALTH CAMP", True)]],
            "sunderbans 8.0, december 2025. 120+ checkups.", fy=.5, story=s, text_at="top")),
        ("a4_teach", lambda s: L2("a4_teach", "welfare", PH["teach_abc"], [[("A STUDENT TAUGHT", False)], [("THIS CLASS", True)]],
            "about 70% of our welfare work is teaching.", fy=.4, story=s)),
        ("a5_crftd", lambda s: L2("a5_crftd", "crftd", PH["tee_novus"], [[("A STUDENT", False)], [("RUNS THIS LABEL", True)]],
            "crftd, formerly roots. every rupee of profit funds a welfare drive.", fy=.35, story=s)),
        ("a6_collabs", lambda s: L2("a6_collabs", "collabs", PH["emami"], [[("STUDENTS HOSTED", False)], [("30 KIDS", True)], [("AT SCIENCE CITY", False)]],
            "with vishwajagriti and emami. 300 stationery kits.", fy=.5, story=s)),
        ("a7_blogs", lambda s: L3("a7_blogs", "blogs", [[("A STUDENT", False)], [("WROTE THIS", True)]],
            "three real posts from our own site.",
            arts=[(PH["blog_mirror"], -3, 0), (PH["blog_dynamics"], 1.5, 24), (PH["blog_city"], -2, 0)], story=s)),
        ("a8_social", lambda s: L3("a8_social", "social", [[("A STUDENT WROTE", False)], [("THIS CAPTION", True)]],
            "this week at aq, by the social media team.",
            arts=[(K.social_slide(9), -3, 0), (K.social_slide(12), 2, 18)], story=s)),
        ("a9_shikshaq", lambda s: L3("a9_shikshaq", "shikshaq", [[("A STUDENT RUNS", False)], [("THE TUTOR", True)], [("SEARCH", True)]],
            "a tutor search for kolkata, run by students.", chips=["KOLKATA", "CLASS IV TO XII", "ICSE", "ISC", "CBSE", "STATE BOARD"], big="shikshaq.in", story=s)),
        ("a10_students", lambda s: L3("a10_students", "hr", [[("STUDENTS", True)], [("RUN ALL OF THIS.", False)]],
            "ages 14 to 19. zero donations, zero fees.", number=("1,400+", "students, across eight departments."), lane_row=True, story=s)),
        ("a11_yourturn", lambda s: L1("a11_yourturn", "hr", PH["dd_group"], [[("YOUR", False)], [("TURN.", True)]],
            "applications are open.", fx=.5, fy=.6, story=s)),
    ]
    for key, mk in jobs:
        for story in (False, True):
            if only and key not in only: continue
            if story and key not in STORY: continue
            await mk(story)
            print("rendered", key, "story" if story else "feed")

STORY = {"a2_dogs", "a3_sundarbans", "a4_teach", "a5_crftd", "a6_collabs", "a11_yourturn", "a1_events"}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    K.OUT = OUT
    asyncio.run(main(set(sys.argv[1:]) or None))
