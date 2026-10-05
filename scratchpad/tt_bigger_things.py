"""BIGGER THINGS IN STORE: Instagram feed teaser (1080x1350), post-TerraThon. A cream page with the four sport emojis is being TURNED (bottom-right corner peeled back);
behind the page, in the revealed corner, a hint of a DISCO DIWALI diya glowing marigold. Caption: BIGGER THINGS IN STORE. (user brief, 2026-10-05)
Adaptations: sport emojis are Noto Color Emoji (Apple set not available; same stand-in as the event posters). No pickleball emoji exists, so the ping-pong paddle stands in. The diya is a bespoke flat SVG (the engine has no diya doodle):
ink outline like the craft layer. Date 10th Nov is from the user (year omitted). No venue (not supplied).
Fold geometry: the corner (W,H) is folded over the diagonal A(W,H-C)-B(W-C,H); its reflection is (W-C,H-C), so the flap is triangle A,B,(W-C,H-C).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_bigger_things.py   ->  out/collaterals/bigger_things_in_store.png
"""
import asyncio, importlib.util, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
H, C = 1350, 520
INK, CREAM, ORCHID = "#0A0A0A", "#F5EEE1", tt.ORCHID
els = []


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


DIYA = '''<svg viewBox="0 0 310 210" width="360" height="244" style="position:absolute;left:690px;top:1035px;z-index:1;overflow:visible">
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
    parts = [f'<style>{tt.FONT_CSS}</style>']
    # revealed ground behind the page: warm glow centred on the diya
    parts.append(f'<div style="position:absolute;inset:0;z-index:0;background:radial-gradient(circle at 905px 1170px,#FF9A1F 0%,#B8430A 14%,#4A0F12 40%,#14040A 80%)"></div>')
    parts.append(DIYA)
    for i, (x, y, r) in enumerate([(940, 1010, 4), (1000, 1090, 3), (800, 1290, 3), (1030, 1250, 4), (880, 1000, 3)]):
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{r*2}px;height:{r*2}px;border-radius:50%;background:#FFC700;opacity:.8;z-index:1"></div>')
    # the page, with its bottom-right corner cut away along the fold
    parts.append(f'<div style="position:absolute;inset:0;z-index:3;filter:drop-shadow(-4px -4px 16px rgba(0,0,0,.55))"><div style="position:absolute;inset:0;background:{CREAM};'
                 f'clip-path:polygon(0 0,{W}px 0,{W}px {H-C}px,{W-C}px {H}px,0 {H}px)"></div></div>')
    # headline: StretchPro, fitted to 940px on its longer line. ZWNJ stops the GG ligature stretching.
    l1, l2 = "BIG‌GER THINGS", "IN STORE"
    m = await B.measure_text([dict(text=l1, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
    px = 100 * 940 / m[0]["text_w"]
    for i, (tag, t) in enumerate([("h1", l1), ("h2", l2)]):
        y = 64 + i * px * 0.98
        parts.append(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:64px;top:{y}px;color:{INK};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * px}px {INK};letter-spacing:{tt.ST_LS}em;'
                     f'font-feature-settings:{tt.ST_FEAT};font-size:{px}px;line-height:1;white-space:nowrap;text-shadow:6px 6px 0 {ORCHID};z-index:5">{t}</div>')
        els.append((tag, 64, y + 4, 940 if i == 0 else 600, px * .8))
    ty = 64 + px * 0.98 * 2 + 36
    # four sport tiles, tilted, each a sticker with ink outline and hard shadow
    tiles = [("\U0001F3CF", "#FFC700", -5), ("\U0001F3D3", "#3DA9FC", 4), ("⚽", "#FF4D8C", -3), ("\U0001F3AE", "#00E5A0", 5)]
    S, G = 220, 24
    for i, (emo, bg, deg) in enumerate(tiles):
        x = 64 + i * (S + G); y = ty + (10 if i % 2 else 0)
        parts.append(f'<div class="measure" data-tag="tile{i}" style="position:absolute;left:{x}px;top:{y}px;width:{S}px;height:{S}px;box-sizing:border-box;transform:rotate({deg}deg);border:6px solid {INK};border-radius:48px;background:{bg};box-shadow:10px 10px 0 {INK};'
                     f'display:flex;align-items:center;justify-content:center;font-family:\'Noto Color Emoji\';font-size:128px;line-height:1;z-index:5">{emo}</div>')
        els.append((f"tile{i}", *rb(x, y, S + 10, S + 10, deg)))
    by = ty + S + 190
    parts.append(f'<div class="measure" data-tag="b1" style="position:absolute;left:64px;top:{by}px;color:{INK};font-family:var(--e);font-weight:700;font-size:60px;line-height:1;white-space:nowrap;z-index:5">turn the page.</div>'); els.append(("b1", 64, by, 440, 52))
    parts.append(f'<div class="measure" data-tag="b2" style="position:absolute;left:64px;top:{by+76}px;color:{INK};font-family:var(--e);font-weight:400;font-size:46px;line-height:1;white-space:nowrap;z-index:5">disco diwali is next.</div>'); els.append(("b2", 64, by + 76, 470, 40))
    parts.append(f'<div class="measure" data-tag="date" style="position:absolute;left:64px;top:{by+150}px;height:70px;padding:0 30px;display:flex;align-items:center;background:{INK};color:#FFC700;border-radius:999px;font-family:var(--d);font-weight:900;font-size:34px;white-space:nowrap;z-index:5">10TH NOV</div>'); els.append(("date", 64, by + 150, 250, 70))
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:64px;top:{H-64-56}px;height:56px;z-index:5">'); els.append(("logo", 64, H - 120, 320, 56))
    # the turned corner: the page's back, lit near the tip and shadowed at the fold
    parts.append(f'<div style="position:absolute;inset:0;z-index:6;filter:drop-shadow(-10px -10px 16px rgba(0,0,0,.45))"><div style="position:absolute;left:{W-C}px;top:{H-C}px;width:{C}px;height:{C}px;'
                 f'background:linear-gradient(315deg,#B9AC8C 0%,#B9AC8C 50%,#F0E7D2 56%,#FFFFFF 100%);clip-path:polygon({C}px 0,0 {C}px,0 0)"></div></div>')
    html = B.page(W, H, CREAM, "".join(parts), grain=False)
    text_pairs = [("h1", INK, CREAM, 100, True), ("h2", INK, CREAM, 100, True), ("b1", INK, CREAM, 60, True), ("b2", INK, CREAM, 46, False), ("date", "#FFC700", INK, 34, True)]
    os.makedirs("out/collaterals", exist_ok=True)
    async with B.session():
        await B.render(html, "out/collaterals/bigger_things_in_store.png", W, H, elements=els, text_pairs=text_pairs, page_bg=CREAM, expect_hero=False, margin=12)
    print("done")

asyncio.run(main())
