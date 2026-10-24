"""DISCO DIWALI entry band: a printed fabric (satin) wristband, 350 x 15 mm, in four colourways: gold, copper, navy, black.

Spec: 350 x 15 mm at 12 px/mm = 4200 x 180 px output (305 dpi). Designed at 2100 x 90 CSS px, rendered at device scale 2.
End zones (15 mm each) carry no type: the clasp or snap sits there. Type stays 2 mm inside the band's edges.
Symmetric about the centre, because the centre is what faces out on the wrist: the title lockup (ball-free, a 15 mm band cannot carry the ball) is the hero.
Copy is supplied facts only: ALL FOR CHARITY, MASQUERADE SANGEET EDITION, 10 NOV 2026, 4:30 PM ONWARDS. The AQ wordmark (core.LOGO, never inverted) sits on a cream pill at the right, the AQ presence. No venue, price, tier or serial number.
Adaptations (CLAUDE.md sec 2 ladder): the format's own ground and palette (CLAUDE.md sec 9 exception, DISCO_DIWALI.md rule 1); lockup recoloured to ink on the two
light grounds (it is lettering, so only its colour changes, never its shape). Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_entry_band.py"""
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
OFFWHITE, GOLD = dd.OFFWHITE, dd.GOLD
# name -> (ground, type, diamond/rule, lockup colour). Copper is the lighter copper of the mask's highlight, so ink type clears 4.5:1.
WAYS = {"gold":   ("#D2A22A", "#0A0A0A", "#0A0A0A", "ink"),
        "copper": ("#C4673E", "#0A0A0A", "#0A0A0A", "ink"),
        "navy":   ("#08102C", GOLD,      GOLD,      "white"),
        "black":  ("#000000", OFFWHITE,  GOLD,      "white")}
LEFT = ("ALL FOR CHARITY", "MASQUERADE SANGEET EDITION")
RIGHT = ("10 NOV 2026", "4:30 PM ONWARDS")


def lockup_uri(colour):
    im = Image.open(dd.ASSETS + "title_lockup_noball.png").convert("RGBA")
    im = im.crop(im.getbbox())
    if colour == "ink":
        a = im.getchannel("A"); im = Image.new("RGBA", im.size, (10, 10, 10, 0)); im.putalpha(a)
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


def diamond(c):
    return f'<i style="display:block;flex:none;width:7px;height:7px;background:{c};transform:rotate(45deg)"></i>'


def band(name):
    ground, ink, accent, lk = WAYS[name]
    src, (lw, lh) = lockup_uri(lk)
    LH = 66; LW = round(LH * lw / lh)
    txt = f"font-family:var(--d);font-weight:700;font-size:{FS}px;letter-spacing:.16em;line-height:1;color:{ink};white-space:nowrap;text-transform:uppercase"
    def group(words, tag):
        parts = []
        for i, w in enumerate(words):
            if i: parts.append(diamond(accent))
            parts.append(f'<span data-tag="{tag}{i}" style="{txt}">{w}</span>')
        return "".join(parts)
    lg = Image.open(os.path.join(ROOT, "engine", "assets", "logo.png")); PH = 50; LGH = 30; LGW = round(LGH * lg.width / lg.height); PW = LGW + 36
    pill = (f'<div data-tag="logo" style="flex:none;width:{PW}px;height:{PH}px;border-radius:999px;background:{core.CREAM};display:flex;align-items:center;justify-content:center">'
            f'<img src="{core.LOGO}" style="height:{LGH}px;width:{LGW}px"></div>')
    pad = END + 14
    half = (W - 2 * pad - LW - 2 * GAP) // 2
    row = (f'<div data-tag="left" style="position:absolute;left:{pad}px;top:0;width:{half}px;height:{H}px;display:flex;align-items:center;justify-content:space-between">{group(LEFT, "L")}</div>'
           f'<img data-tag="lockup" src="{src}" style="position:absolute;left:{(W - LW) // 2}px;top:{(H - LH) // 2}px;width:{LW}px;height:{LH}px">'
           f'<div data-tag="right" style="position:absolute;left:{W - pad - half}px;top:0;width:{half}px;height:{H}px;display:flex;align-items:center;justify-content:space-between">{group(RIGHT, "R")}{diamond(accent)}{pill}</div>')
    rules = "".join(f'<div style="position:absolute;left:0;width:{W}px;top:{y}px;height:1.5px;background:{accent}"></div>' for y in (7, H - 8.5))
    inner = f"{rules}{row}"
    return B.page(W, H, ground, inner, grain=False), (LW, LH, half, pad), ground, ink


async def main():
    outs = []
    async with B.session():
        for name in WAYS:
            html, (LW, LH, half, pad), ground, ink = band(name)
            els = [("left", pad, 0, half, H), ("lockup", (W - LW) // 2, (H - LH) // 2, LW, LH), ("right", W - pad - half, 0, half, H)]
            out = os.path.join(OUT, f"entry_band_{name}.png")
            await B.render(html, out, W, H, elements=els, containers=(), page_bg=ground,
                           text_pairs=[("type", ink, ground, FS, True)], margin=6)
            outs.append((name, out))
    print("done", [o for _, o in outs])
asyncio.run(main())
