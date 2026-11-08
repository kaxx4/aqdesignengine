"""Disco Diwali wish (feed 1080x1350), built on discodiwali.Poster kind=announce, style=diya, copper mask.
The ONLY copy facts are the supplied event facts (10th Nov 2026, 4:30 PM) plus the greeting. Added on top of the
format: orbit rings with small planets and sparkles around the title lockup's disco ball (idea from a user-supplied
reference, drawn here from scratch in the format's own palette: off-white, gold, copper)."""
import asyncio, os, sys, math, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, f"{ROOT}/engine"); os.chdir(f"{ROOT}/engine")
import discodiwali as dd
GOLD, COP, OFF = "#E8C063", "#C8693A", "#F2EFE9"
BX, BY = 262, 427                     # the lockup's ball centre, measured off the v1 render
def orbit_svg(W, H):
    o = []
    for r in (150, 270, 400, 560):
        o.append(f'<circle cx="{BX}" cy="{BY}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.2"/>')
    for r, a, pr, c in [(150, 155, 12, COP), (270, 118, 15, GOLD), (400, 38, 13, COP), (560, 14, 14, OFF), (400, -112, 10, GOLD), (270, -128, 9, OFF)]:
        x, y = BX + r * math.cos(math.radians(a)), BY + r * math.sin(math.radians(a))
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{pr}" fill="{c}"/>')
    for x, y, s in [(985, 560, 24), (610, 735, 20), (90, 560, 20), (700, 40, 18)]:
        o.append(f'<path transform="translate({x} {y})" d="M0 -{s} Q3 -3 {s} 0 Q3 3 0 {s} Q-3 3 -{s} 0 Q-3 -3 0 -{s}Z" fill="{OFF}"/>')
    return f'<svg width="{W}" height="780" viewBox="0 0 {W} 780" style="position:absolute;left:0;top:0;z-index:2">{"".join(o)}</svg>'
class WishPoster(dd.Poster):
    def build(self):
        self.parts.insert(0, orbit_svg(self.W, self.H))
        return super().build()
async def go(out):
    c = dict(edition="Happy Diwali from Team AquaTerra", date="10th November, 2026", time="4:30 PM Onwards",
             status="Wishing you a bright one", cta="See you at Disco Diwali")
    dd.Poster_orig = dd.Poster; dd.Poster = WishPoster
    try: await dd.render_poster("announce", c, "feed", out, style="diya", mask="copper")
    finally: dd.Poster = dd.Poster_orig
asyncio.run(go(f"{ROOT}/out/discodiwali/wish_v3.png"))
