"""DISCO DIWALI marketing-pointer posters: NANDU'S and LIVE DHOL, feed (1080x1350) and story (1080x1920).

Same skeleton as dd_charity.py (user-approved): event photo graded dark, string lights, small LIVE badge top left, a huge two-line headline as the hero with the edition
line under it, a drawn red-copper sticker top right, the DISCO DIWALI lockup (with its ball) as a footer mark. No pill, no link, no card.
Stickers follow dd_copper.py (surface borrowed from the photographed copper mask): a CLOCHE for Nandu's, a DHOL for the live dhol.

Facts printed (all supplied): "Nandu's", "live dhol" (the user's brief), "Masquerade Sangeet Edition", and the date 10 November 2026 (SHOW_DATE=0 drops it).
Nothing else: no menu, no price, no dhol time, no artist. The library holds no photo of Nandu's or a dhol, so both sit on atmosphere frames, not on pictures of the thing.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_pointers.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_copper as cp, dd_photo_bg as pb
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "pointers")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
SHOW_DATE = os.environ.get("SHOW_DATE", "1") != "0"


def cloche(size=380, rot=0, u="n", shadow=True):
    """Copper serving dome on a tray (Nandu's). Dome and tray share the mask texture; the knob is a gem."""
    dome = "M46 270 C46 138 120 74 200 74 C280 74 354 138 354 270 Z"
    tray = "M16 284 H384 Q392 284 392 294 V312 Q392 322 382 322 H18 Q8 322 8 312 V294 Q8 284 16 284 Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{cp._defs(u)}{cp._defs(u + "t")}'
            f'<defs><radialGradient id="gem{u}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFEADF"/><stop offset=".35" stop-color="#FF7A5A"/><stop offset="1" stop-color="#6A1208"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 200 200)"{cp._sh(u, shadow)}>{cp._metal(u, dome, 400, 400, .93, 200, 200)}{cp._metal(u + "t", tray, 400, 400, .9, 200, 303)}'
            f'<circle cx="200" cy="62" r="26" fill="url(#gem{u})" stroke="url(#tr{u})" stroke-width="7"/>'
            f'<path d="M96 196 C108 150 144 118 190 106" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="9" stroke-linecap="round"/></g></svg>')


def dhol(size=420, rot=0, u="d2", shadow=True):
    """Copper dhol lying on its side: barrel body in the mask texture, a cream skin at each end, rope lacing in zigzag."""
    body = "M78 104 C140 86 260 86 322 104 L322 296 C260 314 140 314 78 296 Z"
    zig = " ".join(f"{x},{y}" for x, y in [(98 + i * 18, 118 + (i % 2) * 164) for i in range(13)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400" style="display:block;overflow:visible">{cp._defs(u)}'
            f'<defs><radialGradient id="sk{u}" cx=".4" cy=".35" r=".9"><stop offset="0" stop-color="#FFF3E2"/><stop offset=".7" stop-color="#E8C9A0"/><stop offset="1" stop-color="#B58A5C"/></radialGradient></defs>'
            f'<g transform="rotate({rot} 200 200)"{cp._sh(u, shadow)}>'
            f'<ellipse cx="322" cy="200" rx="40" ry="98" fill="#7A2A12" stroke="url(#tr{u})" stroke-width="8"/><ellipse cx="322" cy="200" rx="28" ry="84" fill="url(#sk{u})" stroke="#3A0F06" stroke-width="4"/>'
            f'{cp._metal(u, body, 400, 400, .98, 200, 200)}'
            f'<polyline points="{zig}" fill="none" stroke="#2E0C05" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<polyline points="{zig}" fill="none" stroke="#FFEBDD" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<ellipse cx="78" cy="200" rx="40" ry="98" fill="#7A2A12" stroke="url(#tr{u})" stroke-width="8"/><ellipse cx="78" cy="200" rx="28" ry="84" fill="url(#sk{u})" stroke="#3A0F06" stroke-width="4"/>'
            f'<ellipse cx="70" cy="200" rx="9" ry="30" fill="#2E0C05" opacity=".45"/></g></svg>')


POSTERS = {
    "nandus": dict(l1="Nandu's", l2="is coming", sticker=cloche, stk=(360, 12), photo="07_12", pos="50% 50%", bright=1.3, cap=215, box=(30, 330)),
    "dhol":   dict(l1="Live", l2="Dhol", sticker=dhol, stk=(400, -10), photo="14_09", pos="50% 45%", bright=1.0, cap=250, box=(70, 260)),
}


async def fit(lines, cap, max_w=960):
    """One size for both lines so the block reads as a single mass: the widest line fills max_w, capped."""
    m = await B.measure_text([dict(text=t.upper(), font="d", size=200, weight=700) for t in lines])
    w = max(x["text_w"] for x in m)
    return min(cap, int(200 * max_w / w))


def poster(p, H, size):
    story = H > 1350
    parts, els = [pb.photo_ground(dd, W, H, p["photo"], p["pos"], bright=p["bright"])], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    step = round(size * .96)
    hy = 760 if story else (440 if size > 215 else 470)
    def line(tag, txt, top, fsize, weight, h):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("head1", p["l1"], hy, size, 700, size)
    line("head2", p["l2"], hy + step, size, 700, size)
    sy = hy + step * 2 + 24
    line("sub", "Masquerade Sangeet Edition", sy, 42, 400, 44)
    if SHOW_DATE:
        line("date", "10th November 2026", sy + 60, 36, 700, 38)
    ss, rot = p["stk"]
    sx, sty = 1040 - ss + 10, (240 if story else 60)
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sty}px;z-index:12">{p["sticker"](ss, rot)}</div>'); els.append(("sticker", sx, sty + p["box"][0], ss, p["box"][1]))
    vw = 400 if story else 330
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    vy = 1420 if story else H - 64 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh


async def main():
    os.makedirs(OUT, exist_ok=True)
    sizes = {k: await fit([v["l1"], v["l2"]], v["cap"]) for k, v in POSTERS.items()}
    print("headline sizes:", sizes)
    async with B.session():
        for key, p in POSTERS.items():
            for name, H in (("feed", 1350), ("story", 1920)):
                inner, els, bottom = poster(p, H, sizes[key])
                print(f"[{key} {name}] last element ends at y={bottom} of {H}")
                await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{key}_{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                               page_bg="#000", collision_ignore=[])
    print("pointers done ->", OUT)
asyncio.run(main())
