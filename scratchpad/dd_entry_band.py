"""DISCO DIWALI entry band: a printed fabric (satin) wristband, 350 x 15 mm, BLACK ground only, in four sticker layouts (user, 2026-10-24).

Spec: 350 x 15 mm at 12 px/mm = 4200 x 180 px output (305 dpi). Designed at 2100 x 90 CSS px, rendered at device scale 2.
End zones (15 mm each) carry no type: the clasp or snap sits there. Symmetric about the centre, because the centre faces out on the wrist: the title lockup
WITH its ball is the hero. The AQ wordmark (core.LOGO, never inverted) sits straight on the black ground at the right.
Copy is supplied facts only: ALL FOR CHARITY, MASQUERADE SANGEET EDITION, 10 NOV 2026, the LIVE badge. No time, venue (so no pin sticker), price, tier or serial number.
Four DIFFERENT scatter patterns (user, 2026-10-24: "all 4 will be diff scatter patterns"), stickers riding the top and bottom rules clear of the type row: confetti (random, small) /
rails (a strict big row above, a quiet small row below) / clusters (six pockets of three) / crescendo (zigzag, size swelling left to right). Type, rules and diamonds: off-white and gold, the format palette (DISCO_DIWALI.md rule 1).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_entry_band.py"""
import asyncio, base64, importlib.util, io, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, core = dd.B, dd.core
OUT = os.path.join(ROOT, "out", "discodiwali", "entry_band"); os.makedirs(OUT, exist_ok=True)
W, H = 2100, 90                       # CSS px; 6 px/mm, so 350 x 15 mm
END, GAP, FS = 90, 54, 21             # clasp zone each end (15 mm), gap round the lockup, type size
GROUND, INK, ACCENT = "#000000", dd.OFFWHITE, dd.GOLD
LEFT = ("ALL FOR CHARITY", "MASQUERADE SANGEET EDITION")
RIGHT = ("10 NOV 2026", "@BADGE")      # the LIVE badge (ALL FOR CHARITY / LIVE / AQUATERRA card) takes the slot the time line held (user, 2026-10-24)
LH = 70                               # lockup height; its ball must clear the rule at y=7
_cache = {}


def lockup_uri():
    im = Image.open(dd.ASSETS + "title_lockup.png").convert("RGBA"); im = im.crop(im.getbbox())
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


def _stk(name):
    if name not in _cache:
        im = Image.open(os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers", f"copper_{name}.png")).convert("RGBA"); im = im.crop(im.getbbox()); im.thumbnail((400, 400))
        buf = io.BytesIO(); im.save(buf, "PNG"); _cache[name] = ("data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size)
    return _cache[name]


def sticker(name, h, rot, pos=None, label=None):
    """In flow (pos None) or absolute at pos=(x, y). Returns (html, width) so the caller can declare its box."""
    src, (iw, ih) = _stk(name); w = round(h * iw / ih)
    place = f"position:absolute;left:{pos[0]}px;top:{pos[1]}px;" if pos else "flex:none;"
    return (f'<img data-tag="{label or "sticker_" + name}" src="{src}" style="{place}height:{h}px;width:{w}px;transform:rotate({rot}deg);'
            f'filter:drop-shadow(0 1.5px 2px rgba(0,0,0,.7))">'), w


def diamond():
    return f'<i style="display:block;flex:none;width:7px;height:7px;background:{ACCENT};transform:rotate(45deg)"></i>'


def band(layout, forbid=()):
    src, (lw, lh) = lockup_uri(); LW = round(LH * lw / lh)
    lg = Image.open(os.path.join(ROOT, "engine", "assets", "logo.png")); LGH = 30; LGW = round(LGH * lg.width / lg.height)
    logo = f'<img data-tag="logo" src="{core.LOGO}" style="flex:none;height:{LGH}px;width:{LGW}px">'
    S = lambda *a, **k: sticker(*a, **k)[0]
    lead_l = tail_r = ""; lead_w = tail_w = 0
    seps_l, seps_r = [diamond()], [diamond(), diamond()]   # diamonds stay in the gaps; the stickers scatter on the rules              # right: date|time and time|logo
    extras = []                                                        # absolute stickers: (html, (x, y, w, h))
    cx = W // 2
    import random
    rng = random.Random({"confetti": 7, "rails": 3, "clusters": 11, "crescendo": 5}[layout])
    KINDS = ["heart", "star", "diya", "calendar", "star", "heart", "diya"]
    lo, hi = END + 6, W - END - 6
    lk0, lk1 = (W - LW) // 2 - 8, (W + LW) // 2 + 8
    def ok(x, w):                                                        # inside the clasp-free run, clear of the lockup and the badge
        return lo <= x and x + w <= hi and (x + w <= lk0 or x >= lk1) and all(x + w <= a or x >= b for a, b in forbid)
    def put(name, h, rot, x, top, tag):
        y = 6 if top else H - h - 6                                      # ride the top or the bottom rule, clear of the 34-56 type row
        html, w = sticker(name, h, rot, (x, y), tag)
        if not ok(x, w): return False
        for _, (ex, ey, ew, eh) in extras:                               # allow a little overlap (it is a pile), never a stack
            if abs((ex + ew / 2) - (x + w / 2)) < (ew + w) * .36 and abs((ey + eh / 2) - (y + h / 2)) < (eh + h) * .4: return False
        extras.append((html, (x, y, w, h))); return True
    n = 0
    if layout == "confetti":                                             # random, small, both rules, every tilt
        while n < 16:
            if put(rng.choice(KINDS), rng.choice([18, 20, 22, 24]), rng.randint(-18, 18), rng.randint(lo, hi), rng.random() < .5, f"sc{len(extras)}"): n += 1
            if len(extras) > 60: break
    elif layout == "rails":                                              # a strict rail: big row on top, a quiet small row below
        x = lo + 4; i = 0
        while x < hi - 30:
            if put(KINDS[i % len(KINDS)], 26, (-9, 7)[i % 2], x, True, f"sc{len(extras)}"): x += 100
            else: x += 20
            i += 1
        x = lo + 56
        while x < hi - 30:
            if put("star", 18, (-12, 12)[(x // 100) % 2], x, False, f"sc{len(extras)}"): x += 100
            else: x += 20
    elif layout == "clusters":                                           # six pockets of three overlapping stickers, alternating rules
        for j, cx_ in enumerate([210, 620, 880, 1240, 1510, 1830]):
            top = j % 2 == 0
            for k, off in enumerate((-22, 0, 22)):
                put(KINDS[(j + k * 2) % len(KINDS)], (22, 26, 22)[k], rng.randint(-18, 18), cx_ + off, top, f"sc{len(extras)}")
    elif layout == "crescendo":                                          # zigzag across the rules, sticker size swelling left to right
        i = 0; x = lo + 4
        while x < hi - 24:
            h = round(18 + 8 * (x - lo) / (hi - lo))
            if put(KINDS[i % len(KINDS)], h, rng.randint(-14, 14), x, i % 2 == 0, f"sc{len(extras)}"): x += 70
            else: x += 15
            i += 1
    BH = 66; BW = round(BH * 1061 / 1005)
    badge = f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="flex:none;height:{BH}px;width:{BW}px">'
    txt = f"font-family:var(--d);font-weight:700;font-size:{FS}px;letter-spacing:.16em;line-height:1;color:{INK};white-space:nowrap;text-transform:uppercase"
    def group(words, tag, seps):
        parts = []
        for i, w in enumerate(words):
            if i: parts.append(seps[i - 1])
            if w == "@BADGE":
                parts.append(badge); continue
            parts.append(f'<span data-tag="{tag}{i}" style="{txt}">{w}</span>')
        return "".join(parts)
    pad = END + 14
    half = (W - 2 * pad - LW - 2 * GAP) // 2
    lw_in, rw_in = half, half
    fl = "position:absolute;top:0;height:%dpx;display:flex;align-items:center;justify-content:space-between" % H
    row = (f'<div data-tag="left" style="{fl};left:{pad}px;width:{half}px">{lead_l}{group(LEFT, "L", seps_l)}</div>'
           f'<img data-tag="lockup" src="{src}" style="position:absolute;left:{(W - LW) // 2}px;top:{(H - LH) // 2}px;width:{LW}px;height:{LH}px">'
           f'<div data-tag="right" style="{fl};left:{W - pad - half}px;width:{half}px">{group(RIGHT, "R", seps_r)}{diamond()}{logo}{tail_r}</div>')
    rules = "".join(f'<div style="position:absolute;left:0;width:{W}px;top:{y}px;height:1.5px;background:{ACCENT}"></div>' for y in (7, H - 8.5))
    html = B.page(W, H, GROUND, rules + row + "".join(e[0] for e in extras), grain=False)
    els = [("left", pad, 0, half, H), ("lockup", (W - LW) // 2, (H - LH) // 2, LW, LH), ("right", W - pad - half, 0, half, H)] + [(f"x{i}",) + e[1] for i, e in enumerate(extras)]
    return html, els


NAMES = {"1": "confetti", "2": "rails", "3": "clusters", "4": "crescendo"}


async def badge_x(html):
    """Where the flex row actually put the badge, so the scatter can keep off it."""
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page(viewport={"width": W, "height": H}); await pg.set_content(html); await pg.wait_for_timeout(300)
        r = await pg.evaluate("(()=>{const r=document.querySelector('[data-tag=badge]').getBoundingClientRect();return [r.left,r.right]})()"); await br.close()
    return r


async def main():
    outs = []
    async with B.session():
        for k, nm in NAMES.items():
            a, b = await badge_x(band(nm)[0]); html, els = band(nm, [(a - 6, b + 6)])
            out = os.path.join(OUT, f"entry_band_{k}_{nm}.png")
            await B.render(html, out, W, H, elements=els, page_bg=GROUND, text_pairs=[("type", INK, GROUND, FS, True)], margin=6,
                           collision_ignore={(a, f"x{i}") for a in ("left", "right") for i in range(80)})   # stickers sit in the type rows' free bands by design
            outs.append(out)
            Image.open(out).convert("RGB").save(out[:-4] + ".pdf", resolution=25.4 * 12)   # 12 px/mm, so the page is exactly 350 x 15 mm
    print("done", outs)
asyncio.run(main())
