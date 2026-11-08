"""Disco Diwali wish, fresh build (feed 1080x1350). Workflow C style bespoke, ink ground = the Disco Diwali format's
recorded exception to the cream rule. Mechanism taken from a user-supplied reference: a hero disco ball made of
halftone-style round tiles in many colours, ringed by thin orbits carrying planets and sparkles. Everything is drawn here
from scratch. Real assets used: title_lockup_noball (the lettering is never rebuilt from a font), live_badge, sparkles, grain.
Palette: the ball's tiles use Diwali warm colours + cream; orbits and type stay off-white/gold per the format.
Copy: greeting + 'Team AquaTerra' only. No date/venue/price (none supplied for a wish)."""
import asyncio, os, sys, math, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/engine"); os.chdir(ROOT)
import discodiwali as dd
core, B, uri = dd.core, dd.B, dd.uri
W, H = core.SIZES["feed"]; OFF, GOLD, GROUND = dd.OFFWHITE, "#E8C063", "#000000"
CX, CY, R = 540, 392, 250
TILES = ["#F4EFE0", "#FF8A1E", "#F5B700", "#E03A2F", "#EE7FA6", "#2E9E5B", "#7A55C8", "#1D2C86", "#F4EFE0", "#FF8A1E"]
rnd = random.Random(11)
def ball():
    o = [f'<circle cx="{CX}" cy="{CY}" r="{R+10}" fill="#120d0a"/>']
    for ri, lat in enumerate(range(-80, 81, 7)):
        phi = math.radians(lat); ring_r = R * math.cos(phi)
        n = max(5, round(2 * math.pi * ring_r / 31))
        for k in range(n):
            lam = ((k + (0.5 if ri % 2 else 0)) / n) * 2 * math.pi - math.pi
            if abs(lam) > math.radians(86): continue
            x = CX + R * math.cos(phi) * math.sin(lam); y = CY + R * math.sin(phi)
            rx = 15 * math.cos(lam) + 1.2; ry = 15 * math.cos(phi) + 1.2
            o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{rnd.choice(TILES)}"/>')
    o.append(f'<defs><radialGradient id="sh" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient></defs>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R+10}" fill="url(#sh)"/>')
    o.append(f'<line x1="{CX}" y1="0" x2="{CX}" y2="{CY-R-10}" stroke="{OFF}" stroke-width="3"/>')
    return "".join(o)
def orbits():
    o = []
    for r in (330, 430, 540, 660):
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{OFF}" stroke-opacity="1" stroke-width="2"/>')
    pl = [(330, -150, 15, "#FF8A1E"), (330, 20, 10, GOLD), (430, -35, 18, "#2E9E5B"), (430, 200, 11, "#EE7FA6"), (540, -110, 13, "#F5B700"), (540, 40, 21, "#7A55C8"), (660, -70, 11, OFF), (660, 150, 14, "#E03A2F")]
    for r, a, pr, c in pl:
        x, y = CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a))
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{pr}" fill="{c}"/>')
    for x, y, s in [(130, 330, 24), (960, 120, 26), (985, 520, 22), (90, 640, 20), (800, 690, 20), (300, 40, 18)]:
        o.append(f'<path transform="translate({x} {y})" d="M0 -{s} Q3 -3 {s} 0 Q3 3 0 {s} Q-3 3 -{s} 0 Q-3 -3 0 -{s}Z" fill="{OFF}"/>')
    return "".join(o)
L = 930 / 2000; lx = 140 - 264 * L; ly = 760 - 400 * L
parts = [
 f'<svg width="{W}" height="800" style="position:absolute;left:0;top:0;z-index:2;-webkit-mask-image:linear-gradient(#000 62%,transparent 100%);mask-image:linear-gradient(#000 62%,transparent 100%)" viewBox="0 0 {W} 800">{orbits()}</svg>',
 f'<svg width="{W}" height="780" style="position:absolute;left:0;top:0;z-index:3" viewBox="0 0 {W} 780">{ball()}</svg>',
 f'<img src="{uri("live_badge.png")}" data-tag="badge" style="position:absolute;left:52px;top:44px;width:250px;z-index:9">',
 f'<img src="{uri("title_lockup_noball.png")}" data-tag="title" style="position:absolute;left:{lx:.0f}px;top:{ly:.0f}px;width:930px;z-index:8">',
 f'<div data-tag="wish" style="position:absolute;left:0;right:0;top:1232px;text-align:center;font-family:var(--e);font-weight:700;font-size:44px;letter-spacing:.01em;color:{OFF};text-transform:uppercase;z-index:12;-webkit-text-stroke:1.5px {OFF}">Happy Diwali, everyone</div>',
 f'<div data-tag="from" style="position:absolute;left:0;right:0;top:1292px;text-align:center;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.3em;color:{GOLD};text-transform:uppercase;z-index:12">from team aquaterra</div>',
 f'<img src="{uri("sparkles.png")}" data-tag="sparkles" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:14;mix-blend-mode:screen;object-fit:cover">',
 f'<img src="{uri("grain.png")}" data-tag="grain" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:15;mix-blend-mode:screen;object-fit:cover;opacity:.9">',
]
elements = [("ball", CX-R, CY-R, 2*R, 2*R), ("badge", 52, 44, 250, 237), ("title", 140, 760, 800, 426),
            ("wish", 190, 1232, 700, 50), ("from", 340, 1292, 400, 24)]
html = B.page(W, H, GROUND, "".join(parts), grain=False)
async def main():
    await B.render(html, f"{ROOT}/out/discodiwali/wish_ball_v2.png", W, H, elements=elements,
                   text_pairs=[("wish", OFF, GROUND, 44, True), ("from", GOLD, GROUND, 20, True)],
                   collision_ignore=[("badge", "ball")], bleed_tags=("title", "sparkles", "grain"),
                   crop_tags=("sparkles", "grain"), page_bg=GROUND)
asyncio.run(main())
