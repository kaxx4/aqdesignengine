import asyncio, os, sys, importlib.util
ROOT = "/home/user/aqdesignengine"
os.chdir(ROOT)
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]
M = 64
A = core.ACCENTS  # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

SLUG = "latentjudgesexamprep"
OUTDIR_LIVE = f"out/versions/{SLUG}"
os.makedirs(OUTDIR_LIVE, exist_ok=True)

# ---------------------------------------------------------------------------
# COVER SLIDE
# ---------------------------------------------------------------------------
def cover_html():
    accent = A[3]  # tomato — loud, judgmental, punchy for a "verdict" theme
    elements = []
    parts = []
    parts.append(f'<div style="position:absolute;inset:0;background:var(--bg)"></div>')

    # background geometry: faint ring cluster upper-right, solid corner block lower-left
    parts.append(B.bggeo([
        ("ring", 760, -80, 420, A[5], .5),
        ("circle", -100, 980, 340, A[2], .6),
    ]))

    parts.append(B.logo(dark=False))
    elements.append(("logo", M, 56, 200, 32))

    # eyebrow label
    eyebrow_y = 170
    parts.append(B.eyebrow("AI VERDICT SERIES", A[6], eyebrow_y))
    elements.append(("eyebrow", M, eyebrow_y, 300, 24))

    # headline — big stacked uppercase, split across lines for hierarchy
    hl_y = 230
    headline = (
        f'<div class="measure" data-tag="headline" style="position:absolute;top:{hl_y}px;left:{M}px;'
        f'width:{W-2*M}px;font-family:var(--d);font-weight:900;text-transform:uppercase;'
        f'color:var(--ink);z-index:6;line-height:.94">'
        f'<span style="font-size:80px;display:block">MAKING</span>'
        f'<span style="font-size:80px;display:block;color:{accent};-webkit-text-stroke:3px var(--ink)">LATENT JUDGES</span>'
        f'<span style="font-size:56px;display:block;margin-top:10px">RATE EXAM PREP</span>'
        f'<span style="font-size:56px;display:block">TECHNIQUES</span>'
        f'</div>'
    )
    parts.append(headline)
    elements.append(("headline", M, hl_y, W-2*M, 340))

    # sub-line in serif italic accent word usage
    sub_y = hl_y + 380
    sub = (f'<div class="measure" data-tag="sub" style="position:absolute;top:{sub_y}px;left:{M}px;'
           f'width:{W-2*M-80}px;font-family:var(--e);font-weight:400;font-size:24px;color:var(--ink2);'
           f'z-index:6;line-height:1.35">6 techniques. 5 unhinged judges. '
           f'<span style="font-family:var(--s);font-style:italic;color:{A[3]}">zero mercy.</span></div>')
    parts.append(sub)
    elements.append(("sub", M, sub_y, W-2*M-80, 90))

    # a giant gavel-less "verdict" badge lower-right as hero-ish accent (using star doodle as a stamp)
    badge_x, badge_y, badge_size = W-320, sub_y+100, 260
    parts.append(f'<div style="position:absolute;top:{badge_y}px;left:{badge_x}px;width:{badge_size}px;'
                 f'height:{badge_size}px;z-index:8">{dd.stamp("burst", accent, rot=8)}</div>')
    elements.append(("burst_badge", badge_x, badge_y, badge_size, badge_size))
    stamp_txt = (f'<div style="position:absolute;top:{badge_y+90}px;left:{badge_x+18}px;width:{badge_size-36}px;'
                 f'text-align:center;font-family:var(--d);font-weight:900;font-size:30px;color:#fff;'
                 f'z-index:9;line-height:1;transform:rotate(-6deg)">VERDICT<br>IN</div>')
    parts.append(stamp_txt)

    # scattered small doodles in free zones (below sub text, left side; above badge)
    d1x, d1y = M, sub_y + 130
    parts.append(doodle("spiral", d1x, d1y, 70, A[1], rot=-10))
    elements.append(("doodle_spiral", d1x, d1y, 70, 70))
    d2x, d2y = M+120, sub_y+150
    parts.append(doodle("zigzag", d2x, d2y, 60, A[4], rot=6))
    elements.append(("doodle_zigzag", d2x, d2y, 60, 60))

    # footer
    parts.append(B.cta("carousel"))
    elements.append(("footer", M, H-70, 320, 20))

    color_pairs = [("headline_stroke_accent", accent, "var(--bg)"),
                   ("burst_badge", accent, "var(--bg)")]
    inner = "".join(parts)
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    return html, elements, color_pairs

# ---------------------------------------------------------------------------
# JUDGE CARD SLIDE
# ---------------------------------------------------------------------------
def score_color(score):
    n = int(score.split("/")[0])
    if n <= 2: return A[3]     # tomato — brutal
    if n <= 4: return A[5]     # grape
    if n <= 7: return A[4]     # sky
    return A[1]                # mint — praise (even if backhanded)

def judge_slide_html(idx, technique, judge, quote, score):
    accent = score_color(score)
    elements = []
    parts = [f'<div style="position:absolute;inset:0;background:var(--bg)"></div>']

    # faint corner geometry, alternate per index for variety
    if idx % 2 == 0:
        parts.append(B.bggeo([("circle", W-260, -140, 380, accent, .16), ("ring", -120, H-360, 320, A[2], .35)]))
    else:
        parts.append(B.bggeo([("square", -100, -100, 320, accent, .14), ("circle", W-220, H-260, 340, A[6], .3)]))

    parts.append(B.logo(dark=False))
    elements.append(("logo", M, 56, 200, 32))

    # top-right index tag e.g. "02 / 06"
    idx_tag = f'{idx:02d} / 06'
    parts.append(B.kicker_tr(idx_tag))
    elements.append(("idx_tag", W-160, 62, 100, 20))

    # eyebrow: "THE TECHNIQUE"
    eb_y = 150
    parts.append(B.eyebrow("THE TECHNIQUE", A[6], eb_y))
    elements.append(("eyebrow", M, eb_y, 260, 24))

    # technique headline — uppercase, wraps to width, sized down if long
    tech_len = len(technique)
    fs = 44 if tech_len <= 40 else (36 if tech_len <= 60 else 30)
    hl_y = eb_y + 46
    hl_h = 100 if fs >= 40 else 130
    headline = (f'<div class="measure" data-tag="technique" style="position:absolute;top:{hl_y}px;left:{M}px;'
                f'width:{W-2*M}px;font-family:var(--d);font-weight:900;text-transform:uppercase;'
                f'color:var(--ink);z-index:6;line-height:1.05;font-size:{fs}px">{technique}</div>')
    parts.append(headline)
    elements.append(("technique", M, hl_y, W-2*M, hl_h))

    # score badge — the visual hero, big circle with score
    badge_d = 300
    badge_x = W - badge_d - M
    badge_y = hl_y + hl_h + 30
    parts.append(f'<div class="measure" data-tag="score_badge" style="position:absolute;top:{badge_y}px;left:{badge_x}px;'
                 f'width:{badge_d}px;height:{badge_d}px;border-radius:50%;background:{accent};'
                 f'border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);z-index:8;'
                 f'display:flex;align-items:center;justify-content:center">'
                 f'<span style="font-family:var(--d);font-weight:900;font-size:88px;color:{core.text_on(accent)};'
                 f'line-height:1;transform:rotate(-4deg)">{score}</span></div>')
    elements.append(("score_badge", badge_x, badge_y, badge_d, badge_d))

    # small doodle punctuation above-left of badge, in the free gap under the headline
    dx, dy = M, badge_y + 20
    doodle_kind = ["star","sparkle","thumbsup","lightning","plus","dots"][idx % 6]
    parts.append(doodle(doodle_kind, dx, dy, 64, A[(idx+2) % 7], rot=(idx*11) % 30))
    elements.append(("doodle_score_accent", dx, dy, 64, 64))

    # judge name label — left of/under badge
    jn_y = badge_y + badge_d + 16
    parts.append(f'<div class="measure" data-tag="judge_label" style="position:absolute;top:{jn_y}px;left:{M}px;'
                 f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.1em;'
                 f'text-transform:uppercase;color:var(--ink3);z-index:7">JUDGE</div>')
    elements.append(("judge_kicker", M, jn_y, 100, 18))
    jname_y = jn_y + 24
    parts.append(f'<div class="measure" data-tag="judge_name" style="position:absolute;top:{jname_y}px;left:{M}px;'
                 f'font-family:var(--s);font-style:italic;font-size:38px;color:{accent};z-index:7">{judge}</div>')
    elements.append(("judge_name", M, jname_y, W-2*M, 48))

    # speech-bubble quote card — sized to the quote's actual line count, not stretched
    card_y = jname_y + 66
    card_w = W - 2*M
    approx_chars_per_line = 46
    n_lines = max(2, -(-len(quote) // approx_chars_per_line))
    card_h = min(H - card_y - 220, 64 + n_lines * 34)
    tail = (f'<div style="position:absolute;top:-18px;left:60px;width:0;height:0;'
            f'border-left:16px solid transparent;border-right:16px solid transparent;'
            f'border-bottom:20px solid var(--ink);z-index:6"></div>'
            f'<div style="position:absolute;top:-13px;left:64px;width:0;height:0;'
            f'border-left:12px solid transparent;border-right:12px solid transparent;'
            f'border-bottom:16px solid #fff;z-index:7"></div>')
    quote_card = (f'<div class="measure" data-tag="quote_card" style="position:absolute;top:{card_y}px;left:{M}px;'
                  f'width:{card_w}px;height:{card_h}px;background:#fff;border:5px solid var(--ink);'
                  f'border-radius:28px;box-shadow:8px 8px 0 var(--ink);z-index:6;padding:28px 30px;'
                  f'box-sizing:border-box">{tail}'
                  f'<span style="font-family:var(--e);font-weight:400;font-size:22px;line-height:1.42;'
                  f'color:var(--ink2)">&ldquo;{quote}&rdquo;</span></div>')
    parts.append(quote_card)
    elements.append(("quote_card", M, card_y, card_w, card_h))

    # fill the space below the card with a big rating-scale strip (1..10 ticks, this score lit up)
    strip_y = card_y + card_h + 44
    tick_w = (card_w - 9*10) / 10
    tick_html = ""
    n_score = int(score.split("/")[0])
    for t in range(1, 11):
        lit = t <= n_score
        tx = M + (t-1) * (tick_w + 10)
        tcol = accent if lit else "#E4DCC4"
        ttxt = "var(--ink)" if lit else "var(--ink3)"
        tick_html += (f'<div style="position:absolute;top:{strip_y}px;left:{tx}px;width:{tick_w}px;height:56px;'
                      f'background:{tcol};border:3px solid var(--ink);border-radius:8px;z-index:6;'
                      f'display:flex;align-items:center;justify-content:center;font-family:var(--m);'
                      f'font-weight:700;font-size:15px;color:{ttxt}">{t}</div>')
    parts.append(tick_html)
    elements.append(("rating_strip", M, strip_y, card_w, 56))
    strip_label_y = strip_y + 66
    parts.append(f'<div class="measure" data-tag="strip_label" style="position:absolute;top:{strip_label_y}px;left:{M}px;'
                 f'font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.08em;'
                 f'text-transform:uppercase;color:var(--ink3);z-index:6">latent judge scale &mdash; not a real metric</div>')
    elements.append(("strip_label", M, strip_label_y, 400, 18))

    # footer
    parts.append(B.cta("verdict series"))
    elements.append(("footer", M, H-70, 320, 20))

    color_pairs = [("score_badge", accent, "var(--bg)")]
    inner = "".join(parts)
    html = B.page(W, H, "var(--bg)", inner, grain=True)
    return html, elements, color_pairs

JUDGES = [
    ("Actually studying from the textbook", "Samay Raina",
     "Bro opened chapter 1 and immediately felt bhaari. 2/10, felt like a documentary I fell asleep to.", "2/10"),
    ("Sleeping instead of revising, calling it &lsquo;recharging the brain&rsquo;", "Ashneer Grover",
     "Doglapan hai bhai. You&rsquo;re not recharging, you&rsquo;re just quitting with extra steps. 1/10 &mdash; but I respect the confidence.", "1/10"),
    ("Watching &lsquo;just one YouTube explainer&rsquo; for 2 hours", "Rakhi Sawant",
     "Arre yeh toh pyaar ho gaya YouTube algorithm se! Full drama, zero syllabus. 4/10 for the emotional journey though.", "4/10"),
    ("Relying entirely on god / last-minute prayers", "Kushagra Shrivastav",
     "This is genuinely the most consistent strategy you&rsquo;ve had all semester. Bhagwan bharose full marks energy. 10/10.", "10/10"),
    ("Making a &lsquo;study timetable&rsquo; and never opening it again", "Balraj Ghai",
     "Beautiful color-coding. Zero execution. It&rsquo;s basically abstract art at this point. 3/10, framing-worthy though.", "3/10"),
    ("Cramming everything the night before", "Samay Raina",
     "The real India&rsquo;s Got Latent talent. Panic + caffeine + prayer = a whole genre. 7/10, mildly impressive chaos.", "7/10"),
]

async def main():
    # cover
    html, elements, color_pairs = cover_html()
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                        page_bg="var(--bg)", core=core, expect_hero=False)
    print("COVER preflight clean:", pf["clean"])
    out = f"{OUTDIR_LIVE}/v4_cover.png"
    await B.render(html, out, W, H, elements=elements, color_pairs=color_pairs, page_bg="var(--bg)")
    print("wrote", out)

    for i, (technique, judge, quote, score) in enumerate(JUDGES, start=1):
        html, elements, color_pairs = judge_slide_html(i, technique, judge, quote, score)
        pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                            page_bg="var(--bg)", core=core, expect_hero=True)
        print(f"SLIDE {i} preflight clean:", pf["clean"], pf.get("issues"))
        out = f"{OUTDIR_LIVE}/v4_slide{i}.png"
        await B.render(html, out, W, H, elements=elements, color_pairs=color_pairs,
                       page_bg="var(--bg)", expect_hero=True)
        print("wrote", out)

asyncio.run(main())
