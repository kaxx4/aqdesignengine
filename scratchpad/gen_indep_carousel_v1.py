import asyncio, os, sys, importlib.util
ROOT = "/home/user/aqdesignengine"
os.chdir(ROOT)
ENGINE_DIR = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS  # 0 pink,1 mint,2 lemon,3 tomato,4 sky,5 grape,6 teal

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

def index_tag(i, total, accent, on_dark=True):
    fg = "#0A0A0A" if accent in core.INK_ON else "#fff"
    return (f'<span style="position:absolute;top:{M}px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:15px;letter-spacing:.1em;color:{fg};background:{accent};padding:8px 14px;'
            f'border-radius:999px;border:3px solid var(--ink);box-shadow:3px 3px 0 var(--ink);z-index:20">'
            f'{i:02d} / {total:02d}</span>')

def swipe_cue(accent, on_dark=False):
    col = "var(--ink)" if not on_dark else "#fff"
    label = (f'<span style="position:absolute;bottom:{M+18}px;right:{M+44}px;font-family:var(--m);'
             f'font-weight:700;font-size:14px;letter-spacing:.12em;text-transform:uppercase;'
             f'color:{col};z-index:20">swipe</span>')
    arrow = doodle("arrow", W-M-36, H-M-44, 34, accent, rot=0, z=20)
    return label + arrow

def logo_el(dark=False):
    return B.logo(dark=dark, x=M, y=52)

def footer(dark=False):
    col = "#fff" if dark else "var(--ink3)"
    return (f'<span style="position:absolute;bottom:{M-12}px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.08em;color:{col};z-index:20">@ngo.aquaterra</span>')

slug = "indep_carousel_2026"
outdir = f"out/versions/{slug}"
os.makedirs(outdir, exist_ok=True)

# ============================================================ SLIDE 1 — the hook
def slide1():
    accent = A[3]  # tomato — red-bull-can red, doubles as brand accent
    elements = [(M,52,180,32), (W-M-140,M,140,40)]
    hero = (f'<div class="measure" style="position:absolute;top:340px;left:{M}px;width:{W-2*M}px;'
            f'font-family:var(--d);font-weight:900;font-size:104px;line-height:.92;'
            f'text-transform:uppercase;color:var(--ink);z-index:6">your generation\'s<br>'
            f'freedom fits in<br>a <span style="color:{accent}">can.</span></div>')
    elements.append((M,340,W-2*M,420))
    colw = int(W-2*M-160)
    sub = (f'<div style="position:absolute;top:840px;left:{M}px;width:{colw}px;'
           f'font-family:var(--e);font-weight:600;font-size:26px;line-height:1.35;color:var(--ink3);'
           f'z-index:6">"gives you wiings," they say.<br>we\'ve been giving kids real ones since 2021.</div>')
    elements.append((M,840,colw,90))
    ring = f'<div style="position:absolute;top:-140px;right:-140px;width:480px;height:480px;border-radius:50%;border:4px solid {accent}55;z-index:0"></div>'
    can = doodle("lightning", W-260, 980, 150, A[2], rot=8, z=6)
    elements.append((W-260,980,150,150))
    star1 = doodle("star", 60, 1050, 70, A[4], rot=-10)
    elements.append((60,1050,70,70))
    dots_row = ''.join(
        f'<div style="position:absolute;bottom:{M+8}px;left:{M+i*22}px;width:{12 if i==0 else 10}px;height:10px;'
        f'border-radius:5px;background:{"var(--ink)" if i==0 else "var(--ink3)"};opacity:{1 if i==0 else .35};z-index:20"></div>'
        for i in range(4))
    inner = "".join([
        f'<div style="position:absolute;inset:0;background:var(--bg)"></div>',
        ring, logo_el(), index_tag(1,4,accent),
        hero, sub, can, star1, dots_row, swipe_cue(accent),
    ])
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    color_pairs = [("hero_txt","var(--ink)","var(--bg)")]
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg="var(--bg)", core=core, expect_hero=True)
    return html, pf

# ============================================================ SLIDE 2 — the pop-culture riff (ink field)
def slide2():
    accent = A[2]  # lemon — red bull's own yellow-gold, still on-brand
    elements = [(M,52,180,32), (W-M-140,M,140,40)]  # logo, index tag
    bg = f'<div style="position:absolute;inset:0;background:var(--ink)"></div>'
    ringA = f'<div style="position:absolute;top:60px;left:-100px;width:360px;height:360px;border-radius:50%;border:3px solid {A[4]}44;z-index:0"></div>'
    ringB = f'<div style="position:absolute;bottom:-80px;right:-80px;width:420px;height:420px;border-radius:50%;border:3px solid {A[0]}44;z-index:0"></div>'
    strike = (f'<div style="position:absolute;top:330px;left:{M}px;width:{W-2*M}px;font-family:var(--m);'
              f'font-weight:700;font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:{accent};z-index:6">'
              f'the ad says</div>')
    elements.append((M,330,W-2*M,32))
    line1 = (f'<div style="position:absolute;top:400px;left:{M}px;width:{W-2*M}px;font-family:var(--d);'
              f'font-weight:900;font-size:88px;line-height:.95;text-transform:uppercase;color:#fff;z-index:6">'
              f'"gives you<br><span style="text-decoration:line-through;text-decoration-color:{A[0]};text-decoration-thickness:6px">wiings</span>."</div>')
    elements.append((M,400,W-2*M,240))
    line2meta = (f'<div style="position:absolute;top:720px;left:{M}px;width:{W-2*M}px;font-family:var(--m);'
              f'font-weight:700;font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:{accent};z-index:6">'
              f'we\'d rather give</div>')
    elements.append((M,720,W-2*M,32))
    line2 = (f'<div class="measure" style="position:absolute;top:786px;left:{M}px;width:{W-2*M}px;font-family:var(--s);'
              f'font-style:italic;font-size:96px;line-height:.92;color:{accent};z-index:6">a fair shot.</div>')
    elements.append((M,786,W-2*M,220))
    body = (f'<div style="position:absolute;top:1010px;left:{M}px;width:{int(W-2*M-140)}px;font-family:var(--e);'
            f'font-weight:600;font-size:24px;line-height:1.4;color:rgba(255,255,255,.85);z-index:6">'
            f'the loudest freedom this generation knows comes from a tin can.<br>ours comes from a classroom seat that was never guaranteed.</div>')
    elements.append((M,1010,int(W-2*M-140),90))
    lightning = doodle("lightning", W-230, 210, 130, accent, rot=-6)
    elements.append((W-230,210,130,130))
    zig = doodle("zigzag", W-190, 380, 90, A[4])
    elements.append((W-190,380,90,90))
    inner = "".join([bg, ringA, ringB, logo_el(dark=True), index_tag(2,4,accent),
                      strike, line1, line2meta, line2, body, lightning, zig,
                      swipe_cue(accent, on_dark=True)])
    html = B.page(W, H, "var(--ink)", inner, grain=False)
    color_pairs = [("meta1","{}".format(accent),"var(--ink)"), ("meta2",accent,"var(--ink)"), ("hero2",accent,"var(--ink)")]
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg="var(--ink)", core=core, expect_hero=True)
    return html, pf

# ============================================================ SLIDE 3 — the sentimental turn (real photo)
def slide3():
    accent = A[4]  # sky
    elements = [(M,52,180,32), (W-M-140,M,140,40)]  # logo, index tag
    photo = f'<img src="{core.PHOTOS["edu"]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0">'
    scrim = (f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.15) 0%,'
              f'rgba(10,10,10,.15) 45%,rgba(10,10,10,.92) 100%);z-index:1"></div>')
    top_scrim = f'<div style="position:absolute;top:0;left:0;right:0;height:220px;background:linear-gradient(180deg,rgba(10,10,10,.55),rgba(10,10,10,0));z-index:1"></div>'
    eyebrow = (f'<div style="position:absolute;top:760px;left:{M}px;font-family:var(--m);font-weight:700;'
               f'font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:{accent};z-index:6">'
               f'meanwhile, in kolkata</div>')
    elements.append((M,760,400,28))
    line = (f'<div class="measure" style="position:absolute;top:816px;left:{M}px;width:{W-2*M}px;font-family:var(--d);'
            f'font-weight:900;font-size:64px;line-height:1.0;text-transform:uppercase;color:#fff;z-index:6">'
            f'freedom, for a<br>student here, means<br>a <span style="color:{accent}">seat in class</span> that<br>stays hers.</div>')
    elements.append((M,816,W-2*M,340))
    body = (f'<div style="position:absolute;top:1188px;left:{M}px;width:{int(W-2*M-100)}px;font-family:var(--e);'
            f'font-weight:600;font-size:22px;line-height:1.35;color:rgba(255,255,255,.85);z-index:6">'
            f'no ad campaign for it. just teenagers showing up, week after week.</div>')
    elements.append((M,1188,int(W-2*M-100),64))
    chip = f'<div style="position:absolute;top:140px;right:{M}px;z-index:20">{B.chip("est. 2021 · kolkata", accent, "#0A0A0A" if accent in core.INK_ON else "#fff")}</div>'
    elements.append((W-M-260,140,260,50))
    inner = "".join([photo, top_scrim, scrim, logo_el(dark=True), index_tag(3,4,accent), chip,
                      eyebrow, line, body, swipe_cue(accent, on_dark=True)])
    html = B.page(W, H, "var(--ink)", inner, grain=False)
    pf = lay.preflight(W, H, elements, html=html, page_bg="var(--ink)", core=core, expect_hero=True)
    return html, pf

# ============================================================ SLIDE 4 — the payoff / CTA
def slide4():
    accent = A[6]  # teal
    elements = [(M,52,180,32), (W-M-140,M,140,40)]  # logo, index tag
    bg = f'<div style="position:absolute;inset:0;background:var(--bg)"></div>'
    mass1 = f'<div style="position:absolute;top:-120px;left:-100px;width:380px;height:380px;border-radius:50%;background:{A[2]}55;border:5px solid var(--ink);z-index:0"></div>'
    mass2 = f'<div style="position:absolute;bottom:-100px;right:-100px;width:420px;height:420px;border-radius:50%;background:{A[0]}55;border:5px solid var(--ink);z-index:0"></div>'
    line = (f'<div class="measure" style="position:absolute;top:420px;left:{M}px;width:{W-2*M}px;font-family:var(--d);'
            f'font-weight:900;font-size:92px;line-height:.95;text-transform:uppercase;color:var(--ink);z-index:6">'
            f'azaadi shouldn\'t<br>come in a <span style="color:{accent}">can.</span></div>')
    elements.append((M,420,W-2*M,280))
    sub = (f'<div class="measure" style="position:absolute;top:760px;left:{M}px;width:{int(W-2*M-120)}px;'
           f'font-family:var(--s);font-style:italic;font-size:44px;line-height:1.15;color:var(--ink);z-index:6">'
           f'it should come free.</div>')
    elements.append((M,760,int(W-2*M-120),120))
    body = (f'<div style="position:absolute;top:940px;left:{M}px;width:{int(W-2*M-120)}px;font-family:var(--e);'
            f'font-weight:600;font-size:24px;line-height:1.4;color:var(--ink3);z-index:6">'
            f'this independence day, give a kid the freedom you already have.</div>')
    elements.append((M,940,int(W-2*M-120),70))
    star = doodle("star", W-220, 200, 100, A[4], rot=-12)
    elements.append((W-220,200,100,100))
    heart = doodle("heart", W-140, 140, 56, A[0], rot=8)
    elements.append((W-140,140,56,56))
    band = f'<div style="position:absolute;bottom:0;left:0;right:0;height:170px;background:{accent};border-top:5px solid var(--ink);z-index:2"></div>'
    bandfg = "#0A0A0A" if accent in core.INK_ON else "#fff"
    bandtxt = (f'<div style="position:absolute;bottom:64px;left:{M}px;font-family:var(--d);font-weight:900;'
               f'font-size:30px;text-transform:uppercase;color:{bandfg};z-index:11">@ngo.aquaterra · link in bio</div>')
    inner = "".join([bg, mass1, mass2, logo_el(), index_tag(4,4,accent),
                      line, sub, body, star, heart, band, bandtxt])
    html = B.page(W, H, "var(--bg)", inner, grain=False)
    color_pairs = [("hero","var(--ink)","var(--bg)")]
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg="var(--bg)", core=core, expect_hero=True)
    return html, pf

async def main():
    slides = [slide1(), slide2(), slide3(), slide4()]
    for i, (html, pf) in enumerate(slides, 1):
        print(f"slide{i} preflight clean={pf.get('clean')} issues={pf.get('issues') if not pf.get('clean') else []}")
        await B.render(html, f"{outdir}/slide{i}_v3.png", W, H)
    print("done")

asyncio.run(main())
