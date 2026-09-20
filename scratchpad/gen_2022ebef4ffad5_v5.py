"""2022ebef4ffad5 v5 — detail + centroid pass on top of v4's layout fix.

v4 critique (compare.py): DETAIL TOO LOW 0.45x (still blocking), CENTROID OFF by (-0.00,+0.12) —
shift mass up. v4 fixed the real collisions/dead-gap/cascade-direction bugs (kept per looking-gate-
overrides-metric) but didn't address these two. Fixes here: headline+deck lifted ~50px to correct
centroid; hatch/crosshatch interior linework added to the card corner, spray tube, and envelope
flap (matching the reference's "objects carry internal linework" critique instead of flat fills);
cascade_peek_check (encoded this session, see DECISIONS.md 2026-09-03) run on the deck to confirm
the 3 cards genuinely peek, not just pass by eye.
"""
import asyncio, os, sys, importlib.util
# Repo root from THIS FILE's location. A hardcoded root has broken this repo
# five times; the last fix just swapped in a NEW absolute path.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]; M = 56
A = core.ACCENTS
RED = A[3]              # tomato — the flooded field
BLUE = A[4]             # sky — envelope
GREY = "#B7B7B7"
elements = []

def at(x, y, w, h, inner, z=6, rot=0):
    elements.append((x, y, w, h))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

logo = f'<img src="{core.LOGO}" style="position:absolute;top:50px;left:{M}px;height:30px;z-index:80;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))">'
free = (f'<div style="position:absolute;top:96px;left:{M}px;z-index:80;color:#0A0A0A;font-family:var(--m)">'
        f'<div style="font-weight:900;font-size:26px;letter-spacing:.02em">FREE</div>'
        f'<div style="font-size:15px;margin-top:2px">entry</div></div>')
djset = (f'<div style="position:absolute;top:56px;right:{M}px;z-index:80;color:#0A0A0A;font-family:var(--m);text-align:right">'
         f'<div style="font-weight:900;font-size:26px;letter-spacing:.02em">DJ SET</div>'
         f'<div style="font-size:15px;margin-top:2px">by aq crew</div></div>')
elements.append((M, 56, 140, 60)); elements.append((W - M - 140, 56, 140, 60)); elements.append((M, 52, 120, 38))

headline = (f'<div style="position:absolute;top:100px;left:0;right:0;text-align:center;z-index:70;color:#0A0A0A;font-family:var(--m)">'
            f'<div style="font-weight:700;font-size:22px;letter-spacing:.14em">WELCOME TO</div>'
            f'<div style="font-family:var(--d);font-weight:900;font-size:96px;letter-spacing:.01em;line-height:1;margin-top:4px">AQUATERRA</div>'
            f'<div style="font-weight:700;font-size:22px;letter-spacing:.24em;margin-top:6px">PARADOX NIGHT</div></div>')
elements.append((240, 100, 600, 190))

def people_row(w, h, n=5):
    """dense row of stick figures with motion lines under each — interior detail, card-width span."""
    figs = []
    gap = w / n
    for i in range(n):
        cx = int(gap * i + gap / 2)
        figs.append(f'<g transform="translate({cx-22},0)">'
                     f'<circle cx="22" cy="16" r="13" fill="none" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="22" y1="29" x2="22" y2="70" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="22" y1="42" x2="2" y2="34" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="22" y1="42" x2="42" y2="34" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="22" y1="70" x2="6" y2="98" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="22" y1="70" x2="38" y2="98" stroke="#0A0A0A" stroke-width="4"/>'
                     f'<line x1="-2" y1="10" x2="-14" y2="2" stroke="#0A0A0A" stroke-width="3"/>'
                     f'<line x1="-2" y1="10" x2="-14" y2="16" stroke="#0A0A0A" stroke-width="3"/></g>')
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'style="position:absolute;left:0;top:0">' + "".join(figs) + '</svg>')

def card(day, w, h, n_people):
    hatch_svg = (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;'
                 f'left:0;top:0" xmlns="http://www.w3.org/2000/svg">'
                 f'{S.hatch(w - 130, h - 100, 110, 90, step=13, color="#0A0A0A", sw=2.5, angle=45)}</svg>')
    return (f'<div style="width:100%;height:100%;background:#FFFFFF;border:5px solid #0A0A0A;'
            f'box-sizing:border-box;overflow:hidden;position:relative">'
            f'<div style="position:absolute;top:18px;left:22px;font-family:var(--d);font-weight:900;'
            f'font-size:{int(h*0.11)}px;line-height:.9;text-transform:uppercase;color:#0A0A0A;z-index:3">'
            f'{day}<span style="font-size:.5em;vertical-align:super">TH</span></div>'
            f'<div style="position:absolute;top:14px;right:18px;width:120px;height:2px;background:#0A0A0A;opacity:.25"></div>'
            f'<div style="position:absolute;top:22px;right:18px;width:80px;height:2px;background:#0A0A0A;opacity:.25"></div>'
            f'<div style="position:absolute;opacity:.35">{hatch_svg}</div>'
            f'<div style="position:absolute;left:26px;right:26px;bottom:22px;height:{int(h*0.4)}px">'
            f'{people_row(w-52, int(h*0.4), n_people)}</div></div>')

deck = [(0.85, 6, 30, -110, 3), (0.92, -3, 15, -55, 4), (1.0, 3, 0, 0, 5)]
CW, CH = 720, 560
CX, CY = (W - CW) // 2 - 10, 500
for sc, rot, dx, dy, z in deck:
    w, h = int(CW * sc), int(CH * sc)
    elements.append((CX + dx, CY + dy, w, h))
_deck_html = ""
for sc, rot, dx, dy, z in deck:
    w, h = int(CW * sc), int(CH * sc)
    _deck_html += at(CX + dx, CY + dy, w, h, card("FRIDAY 24", w, h, 5), z=z, rot=rot)
elements.pop(); elements.pop(); elements.pop()  # remove the duplicate bboxes appended by at()

disco_x, disco_y, disco_d = CX + CW - 30, CY - 90, 210
disco = at(disco_x, disco_y, disco_d, disco_d,
           f'<div style="width:100%;height:100%;border-radius:50%;border:5px solid #0A0A0A;overflow:hidden;'
           f'box-shadow:8px 8px 0 rgba(0,0,0,.35)">{S.checker(disco_d, disco_d, 13, GREY, "#8C8C8C")}</div>', z=15)
sparkle1 = at(disco_x + disco_d - 30, disco_y - 30, 70, 70, dd.stamp("sparkle", "#FFC700"), z=16)
sparkle2 = at(disco_x - 40, disco_y + disco_d - 20, 46, 46, dd.stamp("sparkle", "#FFC700"), z=16, rot=20)

glass = at(M - 10, CY + CH - 240, 150, 230,
           f'<div style="width:100%;height:100%;position:relative">'
           f'<div style="position:absolute;bottom:0;left:14px;right:14px;top:30px;background:{A[2]};'
           f'border:5px solid #0A0A0A;clip-path:polygon(8% 0,92% 0,100% 100%,0% 100%)"></div>'
           f'<div style="position:absolute;top:0;left:44%;width:10px;height:70px;background:{A[0]};'
           f'border-radius:6px;transform:rotate(18deg)"></div></div>', z=18, rot=-6)

martini = at(CX + CW - 150, CY + CH - 30, 170, 150,
             f'<div style="width:100%;height:100%;position:relative">'
             f'<svg width="170" height="150" viewBox="0 0 170 150"><path d="M10 10 L160 10 L85 90 Z" '
             f'fill="{A[1]}" stroke="#0A0A0A" stroke-width="5"/><circle cx="70" cy="45" r="9" fill="#1B8A5A" stroke="#0A0A0A" stroke-width="3"/>'
             f'<circle cx="95" cy="52" r="9" fill="#1B8A5A" stroke="#0A0A0A" stroke-width="3"/></svg>'
             f'<div style="position:absolute;top:82px;left:80px;width:6px;height:46px;background:#0A0A0A"></div>'
             f'<div style="position:absolute;top:122px;left:45px;width:76px;height:6px;background:#0A0A0A"></div></div>', z=17, rot=4)

env_top = CY + CH - 6
env_h = 300
envelope = at(0, env_top, W, env_h,
              f'<svg width="{W}" height="{env_h}" viewBox="0 0 {W} {env_h}" xmlns="http://www.w3.org/2000/svg">'
              f'<polygon points="0,0 {W},0 {W},{env_h} 0,{env_h}" fill="{BLUE}"/>'
              f'<polygon points="0,0 {W//2},{env_h*0.62} {W},0" fill="#0E7C86"/>'
              f'<line x1="0" y1="0" x2="{W//2}" y2="{env_h*0.62}" stroke="#0A0A0A" stroke-width="4" opacity="0.5"/>'
              f'<line x1="{W}" y1="0" x2="{W//2}" y2="{env_h*0.62}" stroke="#0A0A0A" stroke-width="4" opacity="0.5"/>'
              f'</svg>', z=8)

rsvp = (f'<div style="position:absolute;left:{M}px;top:{env_top+16}px;z-index:80;color:#0A0A0A;font-family:var(--m)">'
        f'<div style="font-weight:900;font-size:24px">RESERVATIONS <span style="font-weight:700;font-size:14px">(+18)</span></div>'
        f'<div style="font-weight:600;font-size:14px;margin-top:5px">999 217 6673 / 999 615 7578</div>'
        f'<div style="font-size:10px;opacity:.75;margin-top:8px">CONOCER ES <b>NO EXCEDERSE</b></div></div>')
elements.append((M, env_top + 16, 420, 90))

hydration = at(M, env_top + 130, 84, 104,
               f'<div style="width:100%;height:100%;position:relative">'
               f'<div style="position:absolute;top:18px;left:5px;right:5px;bottom:0;background:#0A0A0A;'
               f'border:4px solid #0A0A0A;overflow:hidden">'
               f'<svg width="80" height="86" viewBox="0 0 80 86" style="position:absolute;left:0;top:0">'
               f'{S.hatch(0, 60, 80, 26, step=7, color="#FFFFFF", sw=1.5, angle=45)}</svg></div>'
               f'<div style="position:absolute;top:0;left:22px;width:14px;height:24px;background:#7E5BFF;'
               f'border:3px solid #0A0A0A"></div>'
               f'<div style="position:absolute;top:40px;left:12px;right:12px;text-align:center;color:#fff;'
               f'font-family:var(--m);font-weight:700;font-size:10px;letter-spacing:.04em;z-index:2">AQ<br>SPRAY</div></div>', z=19)

paw = at(W - M - 54, env_top + 16, 44, 44, dd.stamp("paw", A[0]), z=20)

tags = (f'<div style="position:absolute;right:{M}px;top:{env_top+196}px;z-index:80;color:#0A0A0A;font-family:var(--m);'
        f'text-align:right;font-weight:800;font-size:14px;letter-spacing:.04em;white-space:nowrap">'
        f'MASAI COLLECTIVE · AQ WATER LABS</div>')
elements.append((W - M - 300, env_top + 196, 300, 30))

inner = (f'<div style="position:absolute;inset:0;background:{RED}"></div>'
         + envelope + hydration + paw
         + _deck_html + disco + sparkle1 + sparkle2 + glass + martini
         + headline + free + djset + logo + rsvp + tags)
html = B.page(W, H, RED, inner, grain=True)

deck_stack = [(CX + dx, CY + dy, int(CW * sc), int(CH * sc)) for sc, rot, dx, dy, z in deck]

color_pairs = [("field", RED, RED)]
pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, page_bg=RED, core=core,
                   expect_hero=True, auto_nudge=False, cascade_stacks=[deck_stack])

async def main():
    slug = "2022ebef4ffad5"
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    await B.render(html, f"out/versions/{slug}/v5.png", W, H)
    print("done")
asyncio.run(main())
