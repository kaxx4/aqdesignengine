"""TerraThon REEL COVERS: 20 covers, 1080x1920, six layout families, real event photos only (engine/assets/terrathon/recap_photos/).
Photo key: 01 group selfie · 02 cricket lineup (white kits) · 03 marigold mirror dome · 04 Disco Diwali stall · 05 WE LOVE AQ frame · 06/07 cricket groups.
SAFE BAND: Instagram's profile grid crops a 9:16 cover to the centre 3:4, so ~240px top and bottom are cut there. Every headline, sticker and the sponsor strip
sits inside y 285..1635; only photo and ground bleed past it.
FACTS: copy is a hook line or describes what is visible. The only facts printed are TerraThon 2026 and "2ND TO 4TH OCT" (brain/TERRATHON.md) and Disco Diwali
10 Nov (user, 2026-10-01). No scores, winners, counts or names. Run: python scratchpad/tt_reel_covers.py [only-number ...]"""
import asyncio, base64, importlib.util, io, os, random, sys, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
from PIL import Image
H = 1920
GROUND, ORCHID, CREAM, INK, WHITE, SLAB = "#000000", tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.SLAB
GREEN, BLUE = "#2FD284", "#0396FF"
PH = "engine/assets/terrathon/recap_photos"
OUT = "out/collaterals/terrathon_reel_covers"

_pi = Image.open("engine/assets/terrathon/partners/partner_strip.png").convert("RGBA"); _pi = _pi.resize((1600, round(1600 * _pi.height / _pi.width)))
_b = io.BytesIO(); _pi.save(_b, "PNG"); STRIP = "data:image/png;base64," + base64.b64encode(_b.getvalue()).decode()

def photo_uri(n):
    im = Image.open(f"{PH}/{n}.jpg").convert("RGB")
    if im.width > 1700: im = im.resize((1700, int(im.height * 1700 / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90); return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------------------------------------------------------- the 20 covers
# (family, photo, focus, lines, accent, extra)   lines: headline words/lines, StretchPro or NeutralFace by family
COVERS = [
    ("card",  "01", "50% 38%", ["TERRATHON", "THE CANDID CUT"], ORCHID, {"stk": ["smiley", "cricket_set"]}),
    ("card",  "02", "50% 50%", ["SQUAD GOALS", "ARMS CROSSED. ALL IN WHITE."], GREEN, {"stk": ["pickleball_set"]}),
    ("card",  "06", "50% 60%", ["SHOULDER TO", "SHOULDER"], BLUE, {"stk": ["controller"]}),
    ("card",  "07", "50% 55%", ["POSE PLAN:", "IGNORED"], ORCHID, {"stk": ["basketball"]}),
    ("slab",  "03", "50% 62%", ["MAIN CHARACTER", "ENERGY"], ORCHID, {"stk": ["smiley"]}),
    ("slab",  "05", "50% 52%", ["WE LOVE AQ", "TERRATHON 2026"], GREEN, {"stk": ["flower"]}),
    ("slab",  "04", "50% 38%", ["DISCO DIWALI", "IS NEXT: 10 NOV"], ORCHID, {"stk": ["carnival"]}),
    ("slab",  "03", "18% 62%", ["TAG", "YOURSELF"], BLUE, {"stk": ["aq_live"]}),
    ("giant", "03", "50% 60%", ["3 DAYS.", "ZERO", "CHILL."], ORCHID, {}),
    ("giant", "05", "50% 52%", ["WE LOVE", "AQ"], GREEN, {}),
    ("giant", "04", "50% 40%", ["DISCO", "DIWALI", "HQ"], ORCHID, {}),
    ("giant", "03", "78% 62%", ["PEACE", "SIGNS", "ONLY"], BLUE, {}),
    ("pola",  "01", "50% 45%", ["POV: YOU", "WERE THERE"], ORCHID, {"bg": ORCHID, "stk": ["smiley", "flower"]}),
    ("pola",  "07", "50% 55%", ["ONE PERSON", "FREESTYLED"], GREEN, {"bg": GREEN, "stk": ["controller", "shuriken"]}),
    ("pola",  "06", "50% 60%", ["DIFFERENT", "JERSEYS."], BLUE, {"bg": BLUE, "stk": ["cricket_set", "flower"]}),
    ("split", "02", "50% 50%", ["ARMS", "CROSSED"], GREEN, {"bg": GREEN, "stk": ["aq_live"]}),
    ("split", "01", "50% 38%", ["WATCH", "THE CHAOS"], ORCHID, {"bg": ORCHID, "stk": ["smiley"]}),
    ("split", "07", "50% 55%", ["GAME", "FACE: ON"], BLUE, {"bg": BLUE, "stk": ["basketball"]}),
    ("duo",   "03", "50% 60%", ["NO", "CAPTION", "NEEDED"], ORCHID, {"stk": ["shuriken", "aq_live"]}),
    ("duo",   "05", "50% 52%", ["FEST", "MODE:", "ON"], GREEN, {"stk": ["flower", "shuriken"]}),
]

def esc(t): return t.replace("&", "&amp;").replace("FF", "F\u200cF").replace("SS", "S\u200cS")

async def fit(text, kind, width, cap):
    """Font px at which `text` set in `kind` is `width` wide, capped."""
    if kind == "st":
        m = await B.measure_text([dict(text=text, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
    elif kind == "sg":
        m = await B.measure_text([dict(text=text, font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
    else:
        m = await B.measure_text([dict(text=text, font="d", size=100, weight=900)])
    return min(cap, 100 * width / m[0]["text_w"])

def st_css(px, color=INK, stroke_col=None):
    return (f"font-family:StretchPro;color:{color};-webkit-text-stroke:{tt.ST_STROKE * px}px {stroke_col or INK};letter-spacing:{tt.ST_LS}em;"
            f"font-feature-settings:{tt.ST_FEAT};font-size:{px}px;line-height:1.02")

def sg_css(px, color, stroke_col=INK):
    return f"font-family:SigmarOne;color:{color};-webkit-text-stroke:{tt.SG_STROKE * px}px {stroke_col};letter-spacing:{tt.SG_LS}em;font-size:{px}px;line-height:1"

async def cover(i, spec_):
    fam, ph, focus, lines, acc, ex = spec_
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    parts = [f'<style>{tt.FONT_CSS}</style>']
    def sticker(name, label, x, y, w, z=12, rot=0):
        im, src = tt.crop_to_alpha(name + ".png"); h = w * im.height / im.width; el(label, x, y, w, h)
        r = f"transform:rotate({rot}deg);" if rot else ""
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{r}filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))">'
    def specks(seed=7, col="#fff", n=520, lo=.25, hi=.8):
        rnd = random.Random(seed)
        return f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">' + "".join(
            f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.7, 1, 1.4, 2]):.1f}" fill="{col}" opacity="{rnd.uniform(lo, hi):.2f}"/>' for _ in range(n)) + "</svg>"
    def photo_full(z=1, extra=""):
        return f'<img src="{photo_uri(ph)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;object-position:{focus};z-index:{z};{extra}">'
    def chrome(text_col=WHITE):
        """Logo, fest pill and sponsor strip: the constant furniture, all inside the safe band."""
        p = []
        p.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:44px;top:300px;height:58px;z-index:20;filter:drop-shadow(0 2px 6px rgba(0,0,0,.55))">'); el("logo", 44, 300, 330, 58)
        p.append(f'<div class="measure" data-tag="pill" style="position:absolute;right:44px;top:300px;padding:9px 22px;border:5px solid {ORCHID};border-radius:999px;background:{tt.CTA_FILL};color:{INK};font-family:var(--d);font-weight:900;font-size:26px;line-height:1;z-index:20">TERRATHON 2026</div>'); el("pill", 740, 300, 296, 56)
        sw = 760; sh = round(sw * 322 / 2000); sx = (W - sw) // 2; sy = 1470
        p.append(f'<img class="measure" data-tag="sponsors" src="{STRIP}" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;z-index:20">'); el("sponsors", sx, sy, sw, sh)
        return "".join(p)
    ground = GROUND

    if fam == "card":
        parts += [f'<div style="position:absolute;inset:0;background:{GROUND}"></div>', specks()]
        cx, cy, cw, ch = 60, 400, 960, 700
        el("card", cx, cy, cw, ch)
        parts.append(f'<div class="measure" data-tag="card" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;transform:rotate(.8deg);border:14px solid {CREAM};border-radius:44px;overflow:hidden;background:#111;z-index:3">'
                     f'<img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;object-position:{focus};display:block"></div>')
        t1 = await fit(lines[0], "st", 800, 150); t2 = await fit(lines[1], "sg", 800, 56)
        sx_, sy_, sw_, sh_ = 47, 1060, 986, 340
        el("slab", sx_, sy_, sw_, sh_)
        parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx_}px;top:{sy_}px;width:{sw_}px;height:{sh_}px;transform:rotate(-1.25deg);background:{SLAB};border:19px solid {acc};border-radius:47px;z-index:8;'
                     f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;white-space:nowrap;padding:0 18px">'
                     f'<div style="{st_css(t1)}">{esc(lines[0])}</div><div style="{sg_css(t2, acc)};margin-top:18px">{esc(lines[1])}</div></div>')
        parts.append(sticker("shuriken", "star_a", 20, 560, 100, 9)); parts.append(sticker("shuriken", "star_b", 958, 1330, 100, 9))
        for k, nme in enumerate(ex.get("stk", [])):
            parts.append(sticker(nme, f"stk{k}", [820, 70][k % 2], 380 if k == 0 else 1180, 190, 11, rot=[10, -8][k % 2]))
        parts.append(chrome())

    elif fam == "slab":
        parts += [photo_full(1),
                  f'<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,0) 38%,rgba(0,0,0,0) 62%,rgba(0,0,0,.75) 100%)"></div>']
        t1 = await fit(lines[0], "st", 840, 140); t2 = await fit(lines[1], "sg", 840, 56)
        sx_, sy_, sw_, sh_ = 47, 410, 986, 330
        el("slab", sx_, sy_, sw_, sh_)
        parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx_}px;top:{sy_}px;width:{sw_}px;height:{sh_}px;transform:rotate(-1.25deg);background:{SLAB};border:19px solid {acc};border-radius:47px;z-index:8;'
                     f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;white-space:nowrap;padding:0 18px">'
                     f'<div style="{st_css(t1)}">{esc(lines[0])}</div><div style="{sg_css(t2, acc)};margin-top:18px">{esc(lines[1])}</div></div>')
        parts.append(sticker("shuriken", "star_a", 20, 520, 100, 9)); parts.append(sticker("shuriken", "star_b", 958, 660, 100, 9))
        for k, nme in enumerate(ex.get("stk", [])):
            w_ = 260 if nme in ("carnival", "aq_live") else 200
            parts.append(sticker(nme, f"stk{k}", 740, 690, w_, 11, rot=8))
        parts.append(chrome())

    elif fam == "giant":
        parts += [photo_full(1),
                  f'<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.6) 38%,rgba(0,0,0,.15) 60%,rgba(0,0,0,.75) 100%)"></div>']
        y = 400; cols = [WHITE, acc, WHITE]
        for k, ln in enumerate(lines):
            px_ = await fit(ln, "d", 900, 250)
            parts.append(f'<div class="measure" data-tag="w{k}" style="position:absolute;left:60px;top:{y}px;font-family:var(--d);font-weight:900;font-size:{px_}px;line-height:.92;color:{cols[k]};text-shadow:7px 7px 0 {INK};white-space:nowrap;z-index:10">{esc(ln)}</div>')
            m = await B.measure_text([dict(text=ln, font="d", size=px_, weight=900)])
            el(f"w{k}", 60, y, m[0]["text_w"], px_ * .92); y += px_ * .92 + 14
        parts.append(f'<div class="measure" data-tag="tag" style="position:absolute;left:60px;top:{y + 10:.0f}px;padding:10px 24px;border:5px solid {acc};border-radius:999px;background:{tt.CTA_FILL};color:{INK};font-family:var(--d);font-weight:900;font-size:30px;line-height:1;z-index:10">THE TERRATHON RECAP</div>'); el("tag", 60, y + 10, 420, 60)
        parts.append(sticker("shuriken", "star_a", 880, y - 30, 110, 11, rot=0))
        parts.append(chrome())

    elif fam == "pola":
        bg = ex["bg"]
        parts += [f'<div style="position:absolute;inset:0;background:{bg}"></div>', specks(11, "#000", 380, .12, .3)]
        t1 = await fit(lines[0], "st", 860, 140); t2 = await fit(lines[1], "st", 860, 140)
        parts.append(f'<div class="measure" data-tag="head" style="position:absolute;left:90px;width:900px;top:390px;text-align:center;white-space:nowrap;z-index:10"><div style="{st_css(t1, INK, INK)}">{esc(lines[0])}</div><div style="{st_css(t2, WHITE, INK)};margin-top:4px">{esc(lines[1])}</div></div>')
        el("head", 110, 390, 860, t1 + t2 + 10)
        px_, py_, pw_, phh = 140, 740, 800, 520
        el("polaroid", px_, py_, pw_, phh + 130)
        parts.append(f'<div class="measure" data-tag="polaroid" style="position:absolute;left:{px_}px;top:{py_}px;width:{pw_}px;height:{phh + 130}px;transform:rotate(-3.5deg);background:#fff;border:6px solid {INK};border-radius:14px;box-shadow:14px 14px 0 {INK};z-index:6;padding:26px 26px 0;box-sizing:border-box">'
                     f'<div style="width:100%;height:{phh - 40}px;overflow:hidden;border:4px solid {INK}"><img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;object-position:{focus};display:block"></div>'
                     f'<div style="font-family:var(--m);font-weight:700;font-size:26px;color:{INK};text-align:center;margin-top:26px;letter-spacing:.06em">TERRATHON 2026</div></div>')
        parts.append(f'<div style="position:absolute;left:400px;top:715px;width:230px;height:62px;background:{CREAM};opacity:.92;transform:rotate(-8deg);z-index:9;box-shadow:0 3px 6px rgba(0,0,0,.25)"></div>')
        for k, nme in enumerate(ex.get("stk", [])):
            parts.append(sticker(nme, f"stk{k}", [780, 50][k % 2], [1130, 1090][k % 2], 220 if nme != "shuriken" else 130, 11, rot=[12, -10][k % 2]))
        parts.append(chrome())

    elif fam == "split":
        bg = ex["bg"]
        parts += [f'<div style="position:absolute;inset:0;background:{bg}"></div>',
                  f'<div style="position:absolute;left:0;top:0;width:{W}px;height:1010px;overflow:hidden;z-index:2;border-bottom:14px solid {INK}"><img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;object-position:{focus};display:block"></div>',
                  f'<div style="position:absolute;left:0;top:0;width:{W}px;height:420px;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0))"></div>']
        t1 = await fit(lines[0], "st", 860, 150); t2 = await fit(lines[1], "st", 860, 150)
        txtc = INK if bg in (GREEN, ORCHID) else WHITE
        parts.append(f'<div class="measure" data-tag="head" style="position:absolute;left:90px;width:900px;top:1075px;text-align:center;white-space:nowrap;z-index:10"><div style="{st_css(t1, txtc, INK)}">{esc(lines[0])}</div><div style="{st_css(t2, CREAM, INK)};margin-top:6px">{esc(lines[1])}</div></div>')
        el("head", 110, 1075, 860, t1 + t2 + 6)
        for k, nme in enumerate(ex.get("stk", [])):
            parts.append(sticker(nme, f"stk{k}", 760, 770, 280 if nme == "aq_live" else 230, 12, rot=8))
        parts.append(chrome())

    elif fam == "duo":
        parts += [f'<div style="position:absolute;inset:0;background:{acc}"></div>',
                  f'<div style="position:absolute;inset:0;z-index:1;background:#000"><img src="{photo_uri(ph)}" style="width:100%;height:100%;object-fit:cover;object-position:{focus};filter:grayscale(1) contrast(1.25) brightness(1.05);display:block"></div>',
                  f'<div style="position:absolute;inset:0;z-index:2;background:{acc};mix-blend-mode:multiply"></div>',
                  f'<div style="position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.3),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 55%,rgba(0,0,0,.7))"></div>']
        y = 400
        for k, ln in enumerate(lines):
            px_ = await fit(ln, "st", 860, 170)
            parts.append(f'<div class="measure" data-tag="w{k}" style="position:absolute;left:90px;width:900px;top:{y}px;text-align:center;white-space:nowrap;z-index:10;{st_css(px_, WHITE if k != 1 else CREAM, INK)}">{esc(ln)}</div>')
            el(f"w{k}", 90, y, 900, px_); y += px_ * 1.02 + 6
        for k, nme in enumerate(ex.get("stk", [])):
            parts.append(sticker(nme, f"stk{k}", [30, 740][k % 2], [1250, 1120][k % 2], 150 if nme == "shuriken" else (200 if nme == "flower" else 300), 11, rot=[-8, 8][k % 2]))
        parts.append(chrome())

    html = B.page(W, H, ground, "".join(parts), grain=False)
    labels = [e[0] for e in els]
    ign = {frozenset(p) for p in itertools.combinations(labels, 2)}      # photo covers overlap by design; the measured gates (clipped / off-canvas / margins) still run
    ign = {tuple(sorted(p)) for p in ign} | {tuple(p) for p in ign}
    out = f"{OUT}/{i:02d}_{fam}_{ph}.png"
    tp = [("slab text", INK, SLAB, 60, True), ("pill", INK, tt.CTA_FILL, 26, True)] if fam in ("card", "slab") else [("pill", INK, tt.CTA_FILL, 26, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=tp, page_bg=ground, margin=12, collision_ignore=ign, bleed_tags=("photo",), crop_tags=("card", "polaroid"))
    return out

async def main(only):
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for i, c in enumerate(COVERS, 1):
            if only and i not in only: continue
            print(await cover(i, c))
    print("done")
asyncio.run(main({int(a) for a in sys.argv[1:]}))
