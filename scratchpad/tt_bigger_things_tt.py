"""TERRATHON-STYLE rebuild of the BIGGER THINGS IN STORE teaser (user, 2026-10-05: "Terra thin style" = TerraThon style): black starry ground, blue shurikens, a white slab with an orchid border, StretchPro title, and the three REAL kit stickers (cricket, pickleball, FIFA controller = the three TerraThon events) instead of emojis. Same page-turn + diya concept; the slab corner is peeled to reveal the diya.
OLD DOC: BIGGER THINGS IN STORE: Instagram feed teaser (1080x1350), post-TerraThon. A cream page with the four sport emojis is being TURNED (bottom-right corner peeled back);
behind the page, in the revealed corner, a hint of a DISCO DIWALI diya glowing marigold. Caption: BIGGER THINGS IN STORE. (user brief, 2026-10-05)
Adaptations: sport emojis are Noto Color Emoji (Apple set not available; same stand-in as the event posters). No pickleball emoji exists, so the ping-pong paddle stands in. The diya is a bespoke flat SVG (the engine has no diya doodle):
ink outline like the craft layer. Date 10th Nov is from the user (year omitted). No venue (not supplied).
Fold geometry: the corner (W,H) is folded over the diagonal A(W,H-C)-B(W-C,H); its reflection is (W-C,H-C), so the flap is triangle A,B,(W-C,H-C).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_bigger_things_tt.py   ->  out/collaterals/bigger_things_in_store_terrathon.png
"""
import asyncio, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
H, C = 1350, 480
SX, SY, SW, SH = 50, 150, 980, 1100      # the slab (page)
import random
SLAB, GROUND, HALO = tt.SLAB, tt.GROUND, tt.CREAM_HALO
INK, CREAM, ORCHID = "#0A0A0A", "#F5EEE1", tt.ORCHID
els = []


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


DIYA = '''<svg viewBox="0 0 310 210" width="360" height="244" style="position:absolute;left:690px;top:975px;z-index:1;overflow:visible">
<defs><radialGradient id="g" cx="50%" cy="45%" r="50%"><stop offset="0" stop-color="#FFC700" stop-opacity=".85"/><stop offset=".5" stop-color="#FF7A00" stop-opacity=".35"/><stop offset="1" stop-color="#FF7A00" stop-opacity="0"/></radialGradient></defs>
<circle cx="155" cy="80" r="190" fill="url(#g)"/>
<path d="M30 100 C 40 165 100 195 160 195 C 220 195 272 165 282 100 Z" fill="#C4501B" stroke="#0A0A0A" stroke-width="7" stroke-linejoin="round"/>
<path d="M60 128 C 90 170 130 180 160 180 C 200 180 240 165 262 128 C 220 150 100 150 60 128Z" fill="#E0702A" opacity=".9"/>
<ellipse cx="156" cy="100" rx="126" ry="24" fill="#8B2E0E" stroke="#0A0A0A" stroke-width="7"/>
<ellipse cx="156" cy="98" rx="104" ry="15" fill="#FFB347"/>
<g fill="#FFC700" stroke="#0A0A0A" stroke-width="3"><circle cx="88" cy="150" r="7"/><circle cx="122" cy="166" r="7"/><circle cx="160" cy="171" r="7"/><circle cx="198" cy="166" r="7"/><circle cx="232" cy="150" r="7"/></g>
<path d="M155 98 L155 80" stroke="#0A0A0A" stroke-width="6" stroke-linecap="round"/>
<path d="M155 14 C 190 52 196 86 155 96 C 114 86 120 52 155 14Z" fill="#FFC700" stroke="#0A0A0A" stroke-width="6" stroke-linejoin="round"/>
<path d="M155 48 C 174 68 176 86 155 92 C 134 86 136 68 155 48Z" fill="#FFF3B0"/>
</svg>'''


async def main():
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND};z-index:0"></div>']
    rnd = random.Random(23)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts.append(f'<svg style="position:absolute;inset:0;z-index:0" width="{W}" height="{H}">{specks}</svg>')
    # revealed corner: warm glow on the black, diya in it
    parts.append('<div style="position:absolute;inset:0;z-index:0;background:radial-gradient(circle at 870px 1100px,rgba(255,154,31,.95) 0%,rgba(184,67,10,.7) 12%,rgba(74,15,18,.5) 30%,rgba(0,0,0,0) 55%)"></div>')
    parts.append(DIYA)
    for x, y, r in [(930, 800, 4), (1000, 900, 3), (780, 1290, 3), (1010, 1240, 4), (840, 790, 3)]:
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{r*2}px;height:{r*2}px;border-radius:50%;background:#FFC700;opacity:.8;z-index:1"></div>')
    # slab with the corner cut along the fold
    parts.append(f'<div style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;z-index:3;filter:drop-shadow(-4px -4px 14px rgba(0,0,0,.6))"><div class="measure" data-tag="slab" style="position:absolute;inset:0;box-sizing:border-box;background:{SLAB};border:28px solid {ORCHID};border-radius:70px;'
                 f'clip-path:polygon(0 0,{SW}px 0,{SW}px {SH-C}px,{SW-C}px {SH}px,0 {SH}px)"></div></div>')
    els.append(("slab", SX, SY, SW, SH))
    # eyebrow + stars on the black margin
    parts.append(f'<div class="measure" data-tag="eyebrow" style="position:absolute;left:300px;width:480px;top:62px;text-align:center;color:{HALO};font-family:var(--d);font-weight:400;font-size:40px;letter-spacing:.22em;z-index:5">TERRATHON</div>'); els.append(("eyebrow", 300, 62, 480, 36))
    _, star = tt.crop_to_alpha("shuriken.png")
    for tag, x, y, sz in [("star_tl", 24, 28, 104), ("star_tr", W - 24 - 104, 34, 104), ("star_bl", 36, 1256, 72)]:
        parts.append(f'<img class="measure" data-tag="{tag}" src="{star}" style="position:absolute;left:{x}px;top:{y}px;width:{sz}px;z-index:5">'); els.append((tag, x, y, sz, sz))
    # title: StretchPro, ink on the slab. ZWNJ stops the GG stretch.
    l1, l2 = "BIG\u200cGER THINGS", "IN STORE"
    m = await B.measure_text([dict(text=l1, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
    px = 100 * 840 / m[0]["text_w"]
    for i, (tag, t) in enumerate([("h1", l1), ("h2", l2)]):
        y = SY + 46 + i * px * 0.98
        parts.append(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{SX+60}px;top:{y}px;color:{INK};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * px}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{px}px;line-height:1;white-space:nowrap;z-index:5">{t}</div>')
        els.append((tag, SX + 60, y + 4, 840 if i == 0 else 540, px * .8))
    sy = SY + 46 + px * 0.98 * 2 + 40
    # the three real kit stickers = the three TerraThon events
    kit = [("cricket_set.png", "cricket", 300, SX + 50), ("pickleball_set.png", "pickle", 280, SX + 340), ("controller.png", "fifa", 300, SX + 620)]
    sh_max = 0
    for f, tag, w, x in kit:
        im, src = tt.crop_to_alpha(f); h = w * im.height / im.width; sh_max = max(sh_max, h)
        parts.append(f'<img class="measure" data-tag="{tag}" src="{src}" style="position:absolute;left:{x}px;top:{sy}px;width:{w}px;z-index:5">'); els.append((tag, x, sy, w, h))
    by = sy + sh_max + 50
    parts.append(f'<div class="measure" data-tag="b1" style="position:absolute;left:{SX+60}px;top:{by}px;color:{INK};font-family:var(--e);font-weight:700;font-size:56px;line-height:1;white-space:nowrap;z-index:5">turn the page.</div>'); els.append(("b1", SX + 60, by, 400, 48))
    parts.append(f'<div class="measure" data-tag="b2" style="position:absolute;left:{SX+60}px;top:{by+70}px;color:{INK};font-family:var(--e);font-weight:400;font-size:44px;line-height:1;white-space:nowrap;z-index:5">disco diwali is next.</div>'); els.append(("b2", SX + 60, by + 70, 430, 38))
    parts.append(f'<div class="measure" data-tag="date" style="position:absolute;left:{SX+60}px;top:{by+138}px;height:66px;padding:0 30px;display:flex;align-items:center;background:{ORCHID};color:{INK};border-radius:999px;font-family:var(--d);font-weight:900;font-size:34px;white-space:nowrap;z-index:5">10TH NOV</div>'); els.append(("date", SX + 60, by + 138, 250, 66))
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{SX+60}px;top:{SY+SH-28-40-52}px;height:52px;z-index:5">'); els.append(("logo", SX + 60, SY + SH - 120, 300, 52))
    # the turned corner: back of the page, shadowed at the fold
    parts.append(f'<div style="position:absolute;inset:0;z-index:6;filter:drop-shadow(-10px -10px 16px rgba(0,0,0,.5))"><div style="position:absolute;left:{SX+SW-C}px;top:{SY+SH-C}px;width:{C}px;height:{C}px;'
                 f'background:linear-gradient(315deg,#BDB090 0%,#BDB090 50%,#EFE6D2 56%,#FFFFFF 100%);clip-path:polygon({C}px 0,0 {C}px,0 0)"></div></div>')
    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("h1", INK, SLAB, 100, True), ("h2", INK, SLAB, 100, True), ("b1", INK, SLAB, 56, True), ("b2", INK, SLAB, 44, False), ("date", INK, ORCHID, 34, True), ("eyebrow", HALO, GROUND, 40, False)]
    os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        await B.render(html, "out/collaterals/bigger_things_in_store_terrathon.png", W, H, elements=els, text_pairs=text_pairs, containers=("slab",), collision_ignore={("slab", k) for k in ['cricket', 'pickle', 'fifa', 'b1', 'b2', 'date', 'logo', 'h1', 'h2']}, page_bg=GROUND, expect_hero=False, margin=12)
    print("done")

asyncio.run(main())
