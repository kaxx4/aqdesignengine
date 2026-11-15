"""Campaigns r4: the dialled-down system (owner interview 2026-11-15, see brain/CAMPAIGNS_VOICE_R3.md section 5).

ONE look everywhere:
  photos   grainy, slightly faded film (desaturated, lifted blacks, warm cast, grain). Real AQ photos only.
  ground   near-black #0E0E0C with grain where text is not on a photo
  type     NeutralFace caps headline (cream, one key word in sky); Eina sentence-case small line
  colour   two fixed accents: sky (main, the highlighted word) + mint (support, the one small doodle)
  layouts  'full' (text on photo over a dark fade) and 'band' (photo above, text on near-black below)
  absent   glass pills, frosted cards, hard shadows, thick outlines, slide counters, tabs
"""
import os, sys, asyncio, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_aq_content_v13 as C
from PIL import Image, ImageEnhance
core, B, dd = K.core, K.B, K.dd
W = 1080; GROUND = "#0E0E0C"; CREAM = "#F2ECDD"
SKY, MINT = core.ACCENTS[4], core.ACCENTS[1]
OUT = "out/campaigns_r4"; PH = C.PH
rng = np.random.default_rng(7)

def film(key, w, h, fy=.45, fx=.5):
    im = K.cover(PH[key], w, h, fy=fy, fx=fx)
    im = ImageEnhance.Color(im).enhance(.72)
    a = np.asarray(im).astype(np.float32)
    a = a * .86 + 22                                   # lift the blacks, pull the whites: faded
    a[..., 0] += 6; a[..., 2] -= 8                     # warm cast
    a += rng.normal(0, 9, a.shape[:2])[..., None]      # mono grain
    return K.uri(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), q=86)

def grain_layer(H):
    a = np.clip(rng.normal(128, 26, (H // 2, W // 2)), 0, 255).astype(np.uint8)
    return (f'<img src="{K.uri(Image.fromarray(a).convert("RGB"))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;'
            f'mix-blend-mode:overlay;opacity:.22;z-index:90;pointer-events:none">')

def logo(top):
    return (f'<div style="position:absolute;left:64px;top:{48+top}px;padding:9px 16px;background:{CREAM};border-radius:999px;z-index:80">'
            f'<img src="{core.LOGO}" style="height:26px;display:block"></div>')

def hl_html(txt):  # *word* -> sky
    return re.sub(r"\*(.+?)\*", rf'<span style="color:{SKY}">\1</span>', txt)

def text_block(sp, story):
    hs = sp.get("hs", 84) + (8 if story else 0)
    parts = [f'<div style="font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:{hs}px;line-height:{round(hs*.94)}px;'
             f'letter-spacing:-.01em;color:{CREAM}">{hl_html(sp["hl"])}</div>']
    if sp.get("ln"):
        parts.append(f'<div style="font-family:var(--e);font-size:{34 if story else 31}px;line-height:1.38;color:rgba(242,236,221,.86);max-width:860px">{sp["ln"]}</div>')
    return parts

def doodle(sp, H):
    if not sp.get("dd"): return ""
    kind, x, y, s, rot = sp["dd"]
    return (f'<div style="position:absolute;left:{x}px;top:{int(y*H/1350)}px;width:{s}px;height:{s}px;z-index:70">'
            f'{dd.stamp(kind, MINT, rot=rot)}</div>')

def slide(sp, story=False):
    H = 1920 if story else 1350; top = 200 if story else 0; bot = 250 if story else 0
    P = [K.box(0, 0, W, H, f"background:{GROUND};", z=0)]
    tb = text_block(sp, story)
    if sp["L"] == "full":
        P.append(f'<img src="{film(sp["ph"], W, H, sp.get("fy", .45))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">')
        P.append(K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(14,14,12,.45) 0%,rgba(14,14,12,0) 22%,rgba(14,14,12,0) 42%,rgba(14,14,12,.82) 72%,rgba(14,14,12,.95) 100%);", z=2))
        P.append(f'<div style="position:absolute;left:64px;bottom:{88+bot}px;width:952px;display:flex;flex-direction:column;gap:22px;z-index:60">{"".join(tb)}</div>')
    else:  # band
        ph_h = int(H * .62)
        P.append(f'<img src="{film(sp["ph"], W, ph_h, sp.get("fy", .45))}" style="position:absolute;left:0;top:0;width:{W}px;height:{ph_h}px;object-fit:cover;z-index:1">')
        P.append(K.box(0, 0, W, 160 + top, "background:linear-gradient(180deg,rgba(14,14,12,.5),rgba(14,14,12,0));", z=2))
        P.append(f'<div style="position:absolute;left:64px;top:{ph_h}px;height:{H-ph_h-bot}px;width:952px;display:flex;flex-direction:column;justify-content:center;gap:22px;z-index:60">{"".join(tb)}</div>')
    P += [doodle(sp, H), logo(top), grain_layer(H)]
    return K.page("".join(P), H, bg=GROUND), H

WHAT = [
    dict(L="full", ph="dd_group", fy=.4, hl="AquaTerra is a *youth-run* NGO in Kolkata.", ln="About 1,400 of us, all between 14 and 19."),
    dict(L="band", ph="teach_class", fy=.5, hl="Most of what we do is *teach.*",
         ln="Workshops every week at shelters across the city. Chess, science, storytelling, whatever we can pull off."),
    dict(L="full", ph="dog_biscuit", fy=.5, hl="We also feed strays, plant trees and run *drives.*", hs=76,
         ln="The dogs on our routes know the sound of the biscuit packet.", dd=("heart", 880, 140, 96, 8)),
    dict(L="band", ph="sund1", fy=.4, hl="Sometimes we go *further.*", ln="Relief trips and health camps in the Sundarbans. Eight so far."),
    dict(L="full", ph="books", fy=.5, hl="We build things *too.*", ln="ShikshAQ, a free study platform. TerraNotes, our monthly magazine."),
    dict(L="band", ph="plant_school", fy=.45, hl="A registered NGO since *2021.*", ln="DARPAN-certified, in case anyone's parents ask."),
    dict(L="full", ph="sundarbans", fy=.45, hl="Started by 16 members. Run by *1,400* now.", hs=76, ln="Same idea as day one: show up for someone."),
]

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        jobs = [(f"A_what_{i:02d}", sp, False) for i, sp in enumerate(WHAT, 1)]
        jobs += [(f"A_what_story{k}", WHAT[i], True) for k, i in enumerate([0, 1, 6], 1)]
        for name, sp, story in jobs:
            html, H = slide(sp, story)
            await B.render(html, f"{OUT}/{name}.png", W, H, page_bg=GROUND)
            im = Image.open(f"{OUT}/{name}.png").convert("RGB"); im.save(f"{OUT}/{name}.jpg", quality=88)

if __name__ == "__main__":
    asyncio.run(main())
