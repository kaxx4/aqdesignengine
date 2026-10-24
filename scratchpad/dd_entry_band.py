"""DISCO DIWALI entry band: a printed fabric (satin) wristband, 350 x 15 mm, BLACK ground only, in four sticker layouts (user, 2026-10-24).

Spec: 350 x 15 mm at 12 px/mm = 4200 x 180 px output (305 dpi). Designed at 2100 x 90 CSS px, rendered at device scale 2.
End zones (15 mm each) carry no type: the clasp or snap sits there. Symmetric about the centre, because the centre faces out on the wrist: the title lockup
WITH its ball is the hero. The AQ wordmark (core.LOGO, never inverted) sits straight on the black ground at the right.
Copy is supplied facts only: ALL FOR CHARITY, MASQUERADE SANGEET EDITION, 10 NOV 2026, 4:30 PM ONWARDS. No venue (so no pin sticker), price, tier or serial number.
Layouts: A separators (stickers replace the diamonds) / B bookends (diya + heart at each end) / C scatter (small stickers sit on the rules, top and bottom) /
D burst (a cluster round the ball, diamonds elsewhere). Type, rules and diamonds: off-white and gold, the format palette (DISCO_DIWALI.md rule 1).
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
RIGHT = ("10 NOV 2026", "4:30 PM ONWARDS")
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


def band(layout):
    src, (lw, lh) = lockup_uri(); LW = round(LH * lw / lh)
    lg = Image.open(os.path.join(ROOT, "engine", "assets", "logo.png")); LGH = 30; LGW = round(LGH * lg.width / lg.height)
    logo = f'<img data-tag="logo" src="{core.LOGO}" style="flex:none;height:{LGH}px;width:{LGW}px">'
    S = lambda *a, **k: sticker(*a, **k)[0]
    lead_l = tail_r = ""; lead_w = tail_w = 0
    seps_l, seps_r = [diamond()], [diamond(), diamond()]              # right: date|time and time|logo
    extras = []                                                        # absolute stickers: (html, (x, y, w, h))
    cx = W // 2
    if layout == "A":                                                  # separators: stickers replace the diamonds
        seps_l = [S("heart", 38, -8)]; seps_r = [S("calendar", 38, 8), S("star", 38, -10)]   # the second right sticker sits before the logo
    elif layout == "B":                                                # bookends: a sticker at each end of the type run
        h1, w1 = sticker("diya", 34, -6); h2, w2 = sticker("heart", 34, 8)
        lead_l, lead_w = h1, w1 + 18; tail_r, tail_w = h2, w2 + 18
    elif layout == "C":                                                # scatter: small stickers ride the rules, top and bottom
        for i, (name, h, rot, x, top) in enumerate([("star", 24, -12, 330, True), ("heart", 28, 10, 560, False), ("diya", 26, -8, 760, True), ("calendar", 26, 9, 1250, False),
                                                    ("star", 30, 14, 1360, True), ("heart", 24, -10, 1590, False), ("diya", 28, 8, 1780, True), ("star", 22, -14, 1900, False)]):
            y = 1 if top else H - h - 1
            html, w = sticker(name, h, rot, (x, y), f"scatter{i}"); extras.append((html, (x, y, w, h)))
    elif layout == "D":                                                # burst: a cluster round the ball
        for i, (name, h, rot, dx, y) in enumerate([("heart", 28, -12, -LW // 2 - 40, 6), ("star", 26, 10, -LW // 2 - 34, 58), ("calendar", 26, -9, LW // 2 + 6, 6), ("diya", 24, 8, LW // 2 + 6, 60)]):
            x = cx + dx; html, w = sticker(name, h, rot, (x, y), f"burst{i}"); extras.append((html, (x, y, w, h)))
    txt = f"font-family:var(--d);font-weight:700;font-size:{FS}px;letter-spacing:.16em;line-height:1;color:{INK};white-space:nowrap;text-transform:uppercase"
    def group(words, tag, seps):
        parts = []
        for i, w in enumerate(words):
            if i: parts.append(seps[i - 1])
            parts.append(f'<span data-tag="{tag}{i}" style="{txt}">{w}</span>')
        return "".join(parts)
    pad = END + 14
    half = (W - 2 * pad - LW - 2 * GAP) // 2
    lw_in, rw_in = half, half
    fl = "position:absolute;top:0;height:%dpx;display:flex;align-items:center;justify-content:space-between" % H
    row = (f'<div data-tag="left" style="{fl};left:{pad}px;width:{half}px">{lead_l}{group(LEFT, "L", seps_l)}</div>'
           f'<img data-tag="lockup" src="{src}" style="position:absolute;left:{(W - LW) // 2}px;top:{(H - LH) // 2}px;width:{LW}px;height:{LH}px">'
           f'<div data-tag="right" style="{fl};left:{W - pad - half}px;width:{half}px">{group(RIGHT, "R", seps_r)}{"" if layout == "B" else seps_r[1] if layout == "A" else diamond()}{logo}{tail_r}</div>')
    rules = "".join(f'<div style="position:absolute;left:0;width:{W}px;top:{y}px;height:1.5px;background:{ACCENT}"></div>' for y in (7, H - 8.5))
    html = B.page(W, H, GROUND, rules + row + "".join(e[0] for e in extras), grain=False)
    els = [("left", pad, 0, half, H), ("lockup", (W - LW) // 2, (H - LH) // 2, LW, LH), ("right", W - pad - half, 0, half, H)] + [(f"x{i}",) + e[1] for i, e in enumerate(extras)]
    return html, els


NAMES = {"A": "separators", "B": "bookends", "C": "scatter", "D": "burst"}


async def main():
    outs = []
    async with B.session():
        for k, nm in NAMES.items():
            html, els = band(k)
            out = os.path.join(OUT, f"entry_band_{k}_{nm}.png")
            await B.render(html, out, W, H, elements=els, page_bg=GROUND, text_pairs=[("type", INK, GROUND, FS, True)], margin=6,
                           collision_ignore={(a, f"x{i}") for a in ("left", "right") for i in range(8)})   # stickers sit in the type rows' free bands by design
            outs.append(out)
    print("done", outs)
asyncio.run(main())
