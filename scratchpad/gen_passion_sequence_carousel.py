import asyncio, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
PINK, MINT, LEMON, TOMATO, SKY, GRAPE, TEAL = A

SLUG = "passion_sequence"
OUTDIR = f"out/versions/{SLUG}"
os.makedirs(OUTDIR, exist_ok=True)

# ---------- shared helpers (carousel UI thread) ----------
def logo(dark=False, x=M, y=52):
    sh = "filter:drop-shadow(0 2px 8px rgba(0,0,0,.55));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{x}px;height:34px;z-index:20;{sh}">'

def dots(n, active, accent, dark):
    off = "rgba(255,255,255,.35)" if dark else "rgba(10,10,10,.18)"
    out = f'<div style="position:absolute;top:60px;right:{M}px;z-index:20;display:flex;gap:9px">'
    for i in range(n):
        c = accent if i == active else off
        b = "border:2px solid var(--ink);" if i == active else ""
        out += f'<span style="width:10px;height:10px;border-radius:50%;background:{c};{b}"></span>'
    return out + "</div>"

def footer(dark, tag=""):
    c = "#FFFFFF" if dark else "var(--ink3)"
    sh = "text-shadow:0 2px 6px rgba(0,0,0,.4);" if dark else ""
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};{sh}z-index:20">@ngo.aquaterra{(" &middot; " + tag) if tag else ""}</span>')

def index_tag(i, total, accent, dark):
    ink = core.text_on(accent)
    return (f'<span style="position:absolute;bottom:52px;right:{M}px;z-index:20;font-family:var(--m);'
            f'font-weight:700;font-size:12px;letter-spacing:.08em;color:{ink};background:{accent};'
            f'border:2.5px solid var(--ink);border-radius:999px;padding:5px 13px;'
            f'box-shadow:2.5px 2.5px 0 var(--ink)">{i:02d} / {total:02d}</span>')

def chip(t, bg, fg=None, rot=0, fs=19):
    fg = fg or core.text_on(bg)
    return (f'<span style="display:inline-block;background:{bg};color:{fg};font-family:var(--m);'
            f'font-weight:700;font-size:{fs}px;letter-spacing:.05em;text-transform:uppercase;'
            f'padding:9px 18px;border-radius:999px;border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);'
            f'transform:rotate({rot}deg);white-space:nowrap;position:absolute">{t}</span>')

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean", op=1):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z};opacity:{op}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

TOTAL = 5

# ============================================================ SLIDE 1 — COVER (minimal)
def slide1():
    dark = True
    bg = "var(--ink)"
    els = []
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += logo(dark=True)
    els.append((M, 52, 140, 34))
    inner += dots(TOTAL, 0, TOMATO, dark)
    els.append((W-M-9*4-30, 60, 9*5+36, 10))

    # crossed-out phrase — the cliche, killed on sight
    strike_y = 470
    inner += (f'<div style="position:absolute;top:{strike_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:96px;line-height:1.0;'
              f'letter-spacing:-.01em;color:#5A5A5A;text-transform:uppercase;z-index:6">'
              f'FOLLOW YOUR<br>PASSION'
              f'<div style="position:absolute;top:47%;left:0;width:100%;height:8px;background:{TOMATO};'
              f'transform:rotate(-2deg);box-shadow:0 0 0 3px var(--ink)"></div></div>')
    els.append((M, strike_y, W-2*M, 220))

    # the one-line hook that replaces it
    hook_y = 760
    inner += (f'<div style="position:absolute;top:{hook_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:118px;line-height:.98;'
              f'letter-spacing:-.01em;color:#F4EFE0;text-transform:uppercase;z-index:6">'
              f'EAT SHIT<br>FIRST.</div>')
    els.append((M, hook_y, W-2*M, 260))

    # single small tag, bottom-anchored, carries the source + the rest of the sentence
    tag_y = H - 210
    inner += (f'<span style="position:absolute;top:{tag_y}px;left:{M}px;z-index:8;'
              f'font-family:var(--s);font-style:italic;font-weight:400;font-size:30px;color:{TOMATO}">'
              f'then earn the right to choose.</span>')
    els.append((M, tag_y, 700, 44))

    # single doodle, restrained
    inner += doodle("lightning", W-260, 200, 130, LEMON, rot=8, z=6)
    els.append((W-260, 200, 130, 130))

    inner += footer(dark)
    els.append((M, H-70, 260, 20))
    inner += index_tag(1, TOTAL, TOMATO, dark)
    els.append((W-M-90, H-70, 90, 30))

    color_pairs = [("strike_bar", TOMATO, bg), ("hook_text", "#F4EFE0", bg), ("lightning", LEMON, bg)]
    html_inner = inner
    html = B.page(W, H, bg, html_inner, grain=True)
    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=bg, core=core)
    return html, pf

# ============================================================ SLIDE 2 — the setup / cliche critique
def slide2():
    dark = False
    bg = "var(--bg)"
    els = []
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += logo(dark=False)
    els.append((M, 52, 140, 34))
    inner += dots(TOTAL, 1, SKY, dark)
    els.append((W-M-9*4-30, 60, 9*5+36, 10))

    eyebrow_y = 170
    inner += (f'<div style="position:absolute;top:{eyebrow_y}px;left:{M}px;z-index:6;'
              f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;'
              f'text-transform:uppercase;color:var(--ink3);display:flex;align-items:center;gap:10px">'
              f'<span style="width:11px;height:11px;border-radius:50%;background:{SKY}"></span>'
              f'EVERY NGO PANEL, EVERY LINKEDIN POST</div>')
    els.append((M, eyebrow_y, 700, 24))

    head_y = 230
    inner += (f'<div style="position:absolute;top:{head_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:78px;line-height:1.03;'
              f'letter-spacing:-.01em;color:var(--ink);text-transform:uppercase;z-index:6">'
              f'"FOLLOW YOUR<br>PASSION"</div>')
    els.append((M, head_y, W-2*M, 250))

    body_y = 590
    inner += (f'<div style="position:absolute;top:{body_y}px;left:{M}px;width:{colspan(W,5)}px;'
              f'font-family:var(--e);font-weight:500;font-size:30px;line-height:1.42;'
              f'color:var(--ink);z-index:6">'
              f'cute in theory. doesn\'t pay <span style="font-family:var(--s);font-style:italic;color:{SKY}">rent</span>, '
              f'doesn\'t cover tuition, and doesn\'t account for the fact that most of us are still '
              f'figuring out what our passion even is, while juggling deadlines, part-time gigs, '
              f'and family expectations.</div>')
    els.append((M, body_y, colspan(W,5), 320))

    # a single "chip" objection, pinned lower-left, slight tilt, real furniture not filler
    c1_y = 990
    inner += (f'<span style="position:absolute;top:{c1_y}px;left:{M}px;z-index:8;display:inline-block;'
              f'background:{SKY};color:{core.text_on(SKY)};font-family:var(--m);font-weight:700;font-size:19px;'
              f'letter-spacing:.05em;text-transform:uppercase;padding:9px 18px;border-radius:999px;'
              f'border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);transform:rotate(-3deg);'
              f'white-space:nowrap">doesn\'t pay rent</span>')
    els.append((M, c1_y, 300, 50))

    inner += doodle("cross", W-220, 940, 110, TOMATO, rot=-6, z=6)
    els.append((W-220, 940, 110, 110))

    inner += footer(dark)
    els.append((M, H-70, 260, 20))
    inner += index_tag(2, TOTAL, SKY, dark)
    els.append((W-M-90, H-70, 90, 30))

    color_pairs = [("rent_word", SKY, bg), ("cross_doodle", TOMATO, bg), ("chip_bg", SKY, bg)]
    html = B.page(W, H, bg, inner, grain=True)
    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=bg, core=core)
    return html, pf

def colspan(W, n):
    return B.colspan(W, n)

# ============================================================ SLIDE 3 — STEP 1: EAT SHIT
def slide3():
    dark = False
    bg = "var(--bg)"
    els = []
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += logo(dark=False)
    els.append((M, 52, 140, 34))
    inner += dots(TOTAL, 2, LEMON, dark)
    els.append((W-M-9*4-30, 60, 9*5+36, 10))

    # giant number hero
    num_y = 150
    inner += (f'<div style="position:absolute;top:{num_y}px;left:{M}px;z-index:5;'
              f'font-family:var(--d);font-weight:900;font-size:340px;line-height:.85;'
              f'color:{LEMON};-webkit-text-stroke:5px var(--ink);text-shadow:8px 8px 0 var(--ink)">01</div>')
    els.append((M, num_y, 400, 300))

    eyebrow_y = num_y + 300 + 20
    inner += (f'<div style="position:absolute;top:{eyebrow_y}px;left:{M}px;z-index:6;'
              f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;'
              f'text-transform:uppercase;color:var(--ink3)">STEP ONE, NO SHORTCUT</div>')
    els.append((M, eyebrow_y, 500, 24))

    head_y = eyebrow_y + 46
    inner += (f'<div style="position:absolute;top:{head_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:120px;line-height:.94;'
              f'letter-spacing:-.01em;color:var(--ink);text-transform:uppercase;z-index:6">EAT<br>SHIT.</div>')
    els.append((M, head_y, W-2*M, 260))

    body_y = head_y + 300
    inner += (f'<div style="position:absolute;top:{body_y}px;left:{M}px;width:{colspan(W,5)}px;'
              f'font-family:var(--e);font-weight:500;font-size:27px;line-height:1.45;'
              f'color:var(--ink);z-index:6">'
              f'the work you don\'t love. the unglamorous, unpaid-your-dues, '
              f'&ldquo;why am i even doing this&rdquo; work. every creator, founder, freelancer '
              f'who\'s &ldquo;made it&rdquo; has a version of this phase. it\'s not optional. '
              f'it\'s the <span style="font-family:var(--s);font-style:italic;color:{TOMATO}">entry fee</span>.</div>')
    els.append((M, body_y, colspan(W,5), 260))

    inner += doodle("thumbsup", W-230, 210, 130, MINT, rot=-10, z=6)
    els.append((W-230, 210, 130, 130))
    inner += doodle("squiggle", W-190, 60, 100, TOMATO, rot=0, z=6)
    els.append((W-190, 60, 100, 100))

    inner += footer(dark)
    els.append((M, H-70, 260, 20))
    inner += index_tag(3, TOTAL, LEMON, dark)
    els.append((W-M-90, H-70, 90, 30))

    color_pairs = [("num_hero", LEMON, bg), ("entry_fee_word", TOMATO, bg),
                   ("thumbsup", MINT, bg), ("squiggle", TOMATO, bg)]
    html = B.page(W, H, bg, inner, grain=True)
    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=bg, core=core, expect_hero=True)
    return html, pf

# ============================================================ SLIDE 4 — STEP 2: EARN THE RIGHT TO CHOOSE
def slide4():
    dark = False
    bg = "var(--bg)"
    els = []
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += logo(dark=False)
    els.append((M, 52, 140, 34))
    inner += dots(TOTAL, 3, MINT, dark)
    els.append((W-M-9*4-30, 60, 9*5+36, 10))

    num_y = 150
    inner += (f'<div style="position:absolute;top:{num_y}px;left:{M}px;z-index:5;'
              f'font-family:var(--d);font-weight:900;font-size:340px;line-height:.85;'
              f'color:{MINT};-webkit-text-stroke:5px var(--ink);text-shadow:8px 8px 0 var(--ink)">02</div>')
    els.append((M, num_y, 400, 300))

    eyebrow_y = num_y + 300 + 20
    inner += (f'<div style="position:absolute;top:{eyebrow_y}px;left:{M}px;z-index:6;'
              f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;'
              f'text-transform:uppercase;color:var(--ink3)">STEP TWO, ONLY AFTER STEP ONE</div>')
    els.append((M, eyebrow_y, 500, 24))

    head_y = eyebrow_y + 46
    inner += (f'<div style="position:absolute;top:{head_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:78px;line-height:1.0;'
              f'letter-spacing:-.01em;color:var(--ink);text-transform:uppercase;z-index:6">'
              f'EARN THE RIGHT<br>TO CHOOSE.</div>')
    els.append((M, head_y, W-2*M, 220))

    body_w = colspan(W, 4)
    body_y = head_y + 260
    inner += (f'<div style="position:absolute;top:{body_y}px;left:{M}px;width:{body_w}px;'
              f'font-family:var(--e);font-weight:500;font-size:27px;line-height:1.45;'
              f'color:var(--ink);z-index:6">'
              f'once you\'ve built <span style="font-family:var(--s);font-style:italic;color:{MINT}">skill</span>, '
              f'reputation, and a bit of financial cushion. that\'s when &ldquo;follow your '
              f'passion&rdquo; actually becomes possible. not before.</div>')
    els.append((M, body_y, body_w, 260))

    # three small skill-cushion chips, stacked in the free column to the right of the body text
    chip_x = M + body_w + 30
    chip_y0 = body_y + 20
    chip_accents = [MINT, TEAL, MINT]
    labels = ["skill", "reputation", "cushion"]
    for i, lbl in enumerate(labels):
        cy = chip_y0 + i*66
        acc = chip_accents[i]
        inner += (f'<span style="position:absolute;top:{cy}px;left:{chip_x}px;z-index:8;'
                  f'display:inline-block;background:{acc};color:{core.text_on(acc)};'
                  f'font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.04em;text-transform:uppercase;'
                  f'padding:8px 16px;border-radius:999px;border:3px solid var(--ink);box-shadow:3.5px 3.5px 0 var(--ink);'
                  f'transform:rotate({-3 + i*3}deg);white-space:nowrap">{lbl}</span>')
        els.append((chip_x, cy, 30 + len(lbl)*13, 44))

    inner += footer(dark)
    els.append((M, H-70, 260, 20))
    inner += index_tag(4, TOTAL, MINT, dark)
    els.append((W-M-90, H-70, 90, 30))

    color_pairs = [("num_hero", MINT, bg), ("skill_word", MINT, bg),
                   ("chip_mint", MINT, bg), ("chip_teal", TEAL, bg)]
    html = B.page(W, H, bg, inner, grain=True)
    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=bg, core=core, expect_hero=True)
    return html, pf

# ============================================================ SLIDE 5 — CLOSER
def slide5():
    dark = True
    bg = "var(--ink)"
    els = []
    inner = f'<div style="position:absolute;inset:0;background:{bg}"></div>'
    inner += logo(dark=True)
    els.append((M, 52, 140, 34))
    inner += dots(TOTAL, 4, GRAPE, dark)
    els.append((W-M-9*4-30, 60, 9*5+36, 10))

    head_y = 260
    inner += (f'<div style="position:absolute;top:{head_y}px;left:{M}px;width:{W-2*M}px;'
              f'font-family:var(--d);font-weight:900;font-size:88px;line-height:1.02;'
              f'letter-spacing:-.01em;color:#F4EFE0;text-transform:uppercase;z-index:6">'
              f'PASSION ISN\'T<br>THE START.<br>IT\'S THE <span style="color:{GRAPE}">REWARD</span>.</div>')
    els.append((M, head_y, W-2*M, 400))

    body_y = head_y + 440
    inner += (f'<div style="position:absolute;top:{body_y}px;left:{M}px;width:{colspan(W,5)}px;'
              f'font-family:var(--e);font-weight:500;font-size:27px;line-height:1.45;'
              f'color:rgba(244,239,224,.92);z-index:6">'
              f'the reward for putting in time on things you didn\'t necessarily enjoy. '
              f'ngos skip that part.</div>')
    els.append((M, body_y, colspan(W,5), 130))

    tag_y = body_y + 150
    inner += (f'<span style="position:absolute;top:{tag_y}px;left:{M}px;z-index:8;display:inline-block;'
              f'background:{GRAPE};color:{core.text_on(GRAPE)};font-family:var(--m);font-weight:700;font-size:24px;'
              f'letter-spacing:.05em;text-transform:uppercase;padding:9px 18px;border-radius:999px;'
              f'border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);transform:rotate(-2deg);'
              f'white-space:nowrap">WE\'RE NOT.</span>')
    els.append((M, tag_y, 220, 56))

    inner += doodle("star", W-220, 100, 120, LEMON, rot=12, z=6)
    els.append((W-220, 100, 120, 120))
    inner += doodle("arrow", W-320, 980, 140, TEAL, rot=30, z=6)
    els.append((W-320, 980, 140, 140))

    inner += footer(dark, tag="link in bio")
    els.append((M, H-70, 320, 20))
    inner += index_tag(5, TOTAL, GRAPE, dark)
    els.append((W-M-90, H-70, 90, 30))

    color_pairs = [("reward_word", GRAPE, bg), ("were_not_chip", GRAPE, bg),
                   ("star", LEMON, bg), ("arrow", TEAL, bg)]
    html = B.page(W, H, bg, inner, grain=True)
    pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=bg, core=core)
    return html, pf

async def main():
    slides = [slide1, slide2, slide3, slide4, slide5]
    for i, fn in enumerate(slides, start=1):
        html, pf = fn()
        out = f"{OUTDIR}/v1_slide{i}.png"
        await B.render(html, out, W, H)
        print(f"slide {i}: clean={pf['clean']} -> {out}")

if __name__ == "__main__":
    asyncio.run(main())
