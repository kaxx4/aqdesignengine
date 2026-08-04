# AQ DOODLE PACK v2 — geometric + hand-drawn(rough) + AQ-specific. Auto-generated SVG.
# Every shape: thick ink outline, accent fill/stroke, rotatable, scalable.
# style="clean" = crisp geometric ; style="rough" = wobbly marker (hand-drawn feel)
import math, random
SW=8
def _svg(inner,w,h,rot=0):
    return f'<svg class="dood" viewBox="0 0 {w} {h}" style="transform:rotate({rot}deg)" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def _rough(pts,seed=0,amp=3.5):
    # jitter a point list to fake a hand-drawn wobble
    r=random.Random(seed); return [(x+r.uniform(-amp,amp),y+r.uniform(-amp,amp)) for x,y in pts]
def _path(pts,closed=True):
    d="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+(" Z" if closed else "")
    return d
def _poly_pts(cx,cy,R,r,n,off=-math.pi/2):
    p=[]
    for i in range(n*2):
        ang=off+i*math.pi/n; rad=R if i%2==0 else r
        p.append((cx+rad*math.cos(ang),cy+rad*math.sin(ang)))
    return p

# ---- core geometric (with rough option) ----
def star(fill="#FFC700",rot=0,style="clean",seed=1):
    pts=_poly_pts(60,60,52,22,5)
    if style=="rough": pts=_rough(pts,seed,4)
    lj="round"
    extra='stroke-linecap="round"' if style=="rough" else ''
    return _svg(f'<path d="{_path(pts)}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="{lj}" {extra}/>',120,120,rot)
def sparkle(fill="#FF4D8C",rot=0,style="clean",seed=2):
    pts=[(60,6),(66,40),(80,54),(114,60),(80,66),(66,80),(60,114),(54,80),(40,66),(6,60),(40,54),(54,40)]
    if style=="rough": pts=_rough(pts,seed,4)
    return _svg(f'<path d="{_path([(60,6)]+pts) if False else _path(pts)}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def circle(fill="#3DA9FC",rot=0,style="clean",seed=3):
    if style=="rough":
        pts=[(60+46*math.cos(a),60+46*math.sin(a)) for a in [i*math.pi/9 for i in range(18)]]
        pts=_rough(pts,seed,4)
        return _svg(f'<path d="{_path(pts)}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
    return _svg(f'<circle cx="60" cy="60" r="48" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}"/>',120,120,rot)
def ring(stroke="#7E5BFF",rot=0,style="clean",seed=4):
    if style=="rough":
        pts=[(60+46*math.cos(a),60+46*math.sin(a)) for a in [i*math.pi/11 for i in range(23)]]
        pts=_rough(pts,seed,3.5)
        return _svg(f'<path d="{_path(pts)}" fill="none" stroke="{stroke}" stroke-width="{SW+2}" stroke-linecap="round" stroke-linejoin="round"/>',120,120,rot)
    return _svg(f'<circle cx="60" cy="60" r="46" fill="none" stroke="{stroke}" stroke-width="{SW+2}"/>',120,120,rot)
def thumbsup(fill="#1B8A5A",rot=0,style="clean",seed=5):
    d="M40 54 L40 104 L30 104 L30 54 Z M48 54 L48 100 C48 102 50 104 54 104 L86 104 C90 104 94 101 95 97 L104 66 C105 61 101 56 96 56 L74 56 L78 34 C79 26 74 20 68 20 C64 20 61 22 60 26 L48 52 Z"
    return _svg(f'<path d="{d}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',130,120,rot)
def heart(fill="#FF4D8C",rot=0,style="clean",seed=6):
    d="M60 104 C20 76 12 52 12 38 C12 22 24 14 36 14 C46 14 55 20 60 30 C65 20 74 14 84 14 C96 14 108 22 108 38 C108 52 100 76 60 104 Z"
    return _svg(f'<path d="{d}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def arrow(stroke="#FF4D2E",rot=0,style="clean",seed=7):
    return _svg(f'<path d="M14 66 C40 30 82 26 108 44 M92 26 L112 46 L86 56" fill="none" stroke="{stroke}" stroke-width="{SW+1}" stroke-linecap="round" stroke-linejoin="round"/>',126,90,rot)
def squiggle(stroke="#7E5BFF",rot=0,style="clean",seed=8):
    return _svg(f'<path d="M8 40 Q30 8 52 40 T96 40 T140 40" fill="none" stroke="{stroke}" stroke-width="{SW}" stroke-linecap="round"/>',150,80,rot)
def zigzag(stroke="#0E7C86",rot=0,style="clean",seed=9):
    return _svg(f'<path d="M8 48 L34 16 L60 48 L86 16 L112 48 L138 16" fill="none" stroke="{stroke}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>',150,64,rot)
def burst(fill="#FFC700",rot=0,style="clean",seed=10):
    pts=_poly_pts(60,60,52,34,10)
    if style=="rough": pts=_rough(pts,seed,3)
    return _svg(f'<path d="{_path(pts)}" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def plus(fill="#FF4D8C",rot=0,style="clean",seed=11):
    return _svg(f'<path d="M46 12 H74 V46 H108 V74 H74 V108 H46 V74 H12 V46 H46 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
# ---- expansion ----
def lightning(fill="#FFC700",rot=0,style="clean",seed=12):
    return _svg(f'<path d="M66 8 L30 66 L56 66 L44 112 L92 48 L64 48 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def spiral(stroke="#FF4D8C",rot=0,style="clean",seed=13):
    return _svg(f'<path d="M60 60 m0 0 a10 10 0 1 1 -8 8 a22 22 0 1 0 24 -20 a36 36 0 1 1 -40 34" fill="none" stroke="{stroke}" stroke-width="{SW}" stroke-linecap="round"/>',120,120,rot)
def dots(fill="#3DA9FC",rot=0,style="clean",seed=14):
    c="".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{fill}" stroke="#0A0A0A" stroke-width="4"/>' for x,y in [(20,20),(60,20),(100,20),(20,60),(60,60),(100,60),(20,100),(60,100),(100,100)])
    return _svg(c,120,120,rot)
def speech(fill="#00E5A0",rot=0,style="clean",seed=15):
    return _svg(f'<path d="M14 20 H106 A10 10 0 0 1 116 30 V78 A10 10 0 0 1 106 88 H50 L30 108 L34 88 H14 A10 10 0 0 1 4 78 V30 A10 10 0 0 1 14 20 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def cross(fill="#FF4D2E",rot=0,style="clean",seed=16):
    return _svg(f'<path d="M30 22 L60 52 L90 22 L98 30 L68 60 L98 90 L90 98 L60 68 L30 98 L22 90 L52 60 L22 30 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
# ---- AQ-specific ----
def globe(rot=0,style="clean",seed=20):
    # AQ globe: blue circle + green landmasses hint + meridians
    return _svg(f'''<circle cx="60" cy="60" r="48" fill="#3DA9FC" stroke="#0A0A0A" stroke-width="{SW}"/>
    <path d="M40 30 C55 34 52 48 66 50 C78 52 74 66 60 66 C48 66 46 80 58 88" fill="none" stroke="#1B8A5A" stroke-width="10" stroke-linecap="round"/>
    <path d="M20 44 Q40 34 60 44" fill="none" stroke="#0A0A0A" stroke-width="4" opacity=".5"/>
    <ellipse cx="60" cy="60" rx="20" ry="48" fill="none" stroke="#0A0A0A" stroke-width="4" opacity=".5"/>''',120,120,rot)
def leaf(fill="#1B8A5A",rot=0,style="clean",seed=21):
    return _svg(f'<path d="M24 96 C24 48 60 18 100 20 C102 60 72 96 28 96 Z M40 82 C56 66 76 52 92 40" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"/>',120,120,rot)
def paw(fill="#FF4D8C",rot=0,style="clean",seed=22):
    toes="".join(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="13" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>' for x,y in [(34,36),(54,26),(76,30),(94,46)])
    return _svg(f'{toes}<path d="M40 62 C40 50 80 50 80 62 C92 74 96 96 78 102 C68 105 52 105 42 102 C24 96 28 74 40 62 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)
def tree(fill="#1B8A5A",rot=0,style="clean",seed=23):
    return _svg(f'<path d="M60 8 L92 56 L74 56 L100 96 L66 96 L66 114 L54 114 L54 96 L20 96 L46 56 L28 56 Z" fill="{fill}" stroke="#0A0A0A" stroke-width="{SW}" stroke-linejoin="round"/>',120,120,rot)

PACK={"star":star,"sparkle":sparkle,"circle":circle,"ring":ring,"thumbsup":thumbsup,"heart":heart,"arrow":arrow,"squiggle":squiggle,"zigzag":zigzag,"burst":burst,"plus":plus,"lightning":lightning,"spiral":spiral,"dots":dots,"speech":speech,"cross":cross,"globe":globe,"leaf":leaf,"paw":paw,"tree":tree}

# ---- THE COLOUR-CORRECT ENTRY POINT (use this; never call PACK entries by hand) ----
import inspect as _inspect

# 5 doodles are STROKE-drawn, not filled — their colour kwarg is `stroke`, not `fill`.
# globe has no colour arg at all (its colours are intrinsic to the AQ mark).
COLOR_ARG = {}
for _n, _f in PACK.items():
    _p = _inspect.signature(_f).parameters
    COLOR_ARG[_n] = "fill" if "fill" in _p else ("stroke" if "stroke" in _p else None)

def stamp(kind, color=None, rot=0, style="clean", seed=None):
    """Instantiate ANY doodle with the requested colour actually applied.

    WHY THIS EXISTS (bug found 2026-08-03, friendship_day carousel). Every bespoke script — and
    the template in CLAUDE.md §6 itself — used this shape:

        try:    inner = fn(fill=fill, rot=rot)
        except TypeError: inner = fn(rot=rot)          # <-- SILENTLY DROPS THE COLOUR

    For the 5 stroke-drawn doodles (ring, arrow, squiggle, zigzag, spiral) `fill=` raises
    TypeError, so the fallback ran and the doodle rendered in its HARD-CODED DEFAULT colour.
    A pink zigzag came out teal; a pink arrow came out tomato; a mint ring came out grape. The
    request was accepted and discarded with no error, on every poster ever built this way.

    This resolves the correct kwarg by introspection instead of guessing, so a colour is either
    applied or the doodle genuinely has none (globe). Never silently wrong.
    """
    fn = PACK[kind]
    params = _inspect.signature(fn).parameters
    kw = {}
    if "rot" in params:
        kw["rot"] = rot
    if "style" in params:
        kw["style"] = style
    if seed is not None and "seed" in params:
        kw["seed"] = seed
    arg = COLOR_ARG.get(kind)
    if color is not None and arg is not None:
        kw[arg] = color
    return fn(**kw)
