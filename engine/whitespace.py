# WHITESPACE ACTIVATION — techniques to make negative space active, ranked by clutter-cost (low first).
# Applied to MEASURED dead zones, not scattered blindly.
import importlib.util
def load(n):
    s=importlib.util.spec_from_file_location(n,f"" + os.path.dirname(os.path.abspath(__file__)) + "/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core")

# 1. GHOST ELEMENT — faint oversized letter/word/shape in a dead zone. Fills visually, near-zero clutter.
def ghost_word(txt, x, y, size, color="var(--ink)", op=0.06, rot=0, z=0):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;font-family:var(--d);font-weight:900;'
            f'font-size:{size}px;line-height:.8;text-transform:uppercase;letter-spacing:-.04em;'
            f'color:{color};opacity:{op};transform:rotate({rot}deg);z-index:{z};pointer-events:none;white-space:nowrap">{txt}</div>')

def ghost_shape(x, y, d, color="var(--ink)", op=0.05, kind="circle", z=0):
    br="50%" if kind=="circle" else "38% 62% 55% 45%/48% 38% 62% 52%"
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{d}px;height:{d}px;'
            f'background:{color};opacity:{op};border-radius:{br};z-index:{z}"></div>')

# 2. TONE PATTERN — faint dot-grid or line-grid filling a dead zone (like graph paper / halftone field)
def tone_patch(x, y, w, h, kind="dots", color="#0A0A0A", op=0.06, z=0):
    if kind=="dots":
        bg=f'background-image:radial-gradient({color} 1.5px, transparent 2px);background-size:22px 22px;'
    else:
        bg=f'background-image:linear-gradient({color} 1px,transparent 1px),linear-gradient(90deg,{color} 1px,transparent 1px);background-size:40px 40px;'
    return f'<div style="position:absolute;top:{y}px;left:{x}px;width:{w}px;height:{h}px;{bg}opacity:{op};z-index:{z};pointer-events:none"></div>'

# 3. DIRECTIONAL CONNECTOR — hand-drawn arrow/dotted path traveling across empty space linking two points
def connector(x1,y1,x2,y2,color="var(--ink)",sw=6,z=5,dotted=False,arrow=True):
    dx,dy=x2-x1,y2-y1
    # a curved path with optional arrowhead
    cx,cy=(x1+x2)/2+dy*0.2,(y1+y2)/2-dx*0.2  # control point offset for curve
    dash='stroke-dasharray="2 14"' if dotted else ''
    head=''
    if arrow:
        import math
        ang=math.atan2(y2-cy,x2-cx)
        a1=ang+2.5; a2=ang-2.5; L=22
        head=(f'<path d="M{x2} {y2} L{x2+L*math.cos(a1)} {y2+L*math.sin(a1)} M{x2} {y2} '
              f'L{x2+L*math.cos(a2)} {y2+L*math.sin(a2)}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return (f'<svg style="position:absolute;inset:0;width:100%;height:100%;z-index:{z};pointer-events:none" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M{x1} {y1} Q{cx} {cy} {x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {dash}/>{head}</svg>')

# helper: given a measured dead box (css px), pick the lowest-clutter activation
def activate(box, brand_word="AQUATERRA", accents=None):
    """box=(x,y,w,h) in css px. Returns html using the cheapest technique that fits."""
    x,y,w,h=box
    accents=accents or core.ACCENTS
    # wide+short -> ghost word or connector; big square -> ghost shape + tone; tall -> ghost word rotated
    if w>300 and h<220:
        return ghost_word(brand_word, x+10, y+h*0.1, int(h*0.9), op=0.05)
    if w>200 and h>200:
        return tone_patch(x,y,w,h,kind="dots",op=0.06)+ghost_shape(x+w*0.2,y+h*0.2,int(min(w,h)*0.6),color=accents[2],op=0.05)
    return tone_patch(x,y,w,h,kind="dots",op=0.05)


# ===== MODE-CONDITIONAL EYE CANDY (Architecture of Attraction) =====

# MODE 1 — FRAMING: eye candy CONTAINS a text zone (halftone field + corner bursts + jagged border)
# rather than spreading across the whole design. Returns a wrapper you place text inside.
def frame_zone(x, y, w, h, accent, z=2, halftone=True):
    """A contained 'chaotic zone' frame: tinted halftone field + bursts pinned to corners + thick border."""
    import importlib.util
    ht = f'background-image:radial-gradient(#0A0A0A18 1.6px,transparent 2px);background-size:12px 12px;' if halftone else ''
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{w}px;height:{h}px;'
            f'background-color:{accent};{ht}border:4px solid var(--ink);border-radius:14px;'
            f'box-shadow:8px 8px 0 var(--ink);z-index:{z}"></div>')

# MODE 4 — DIRECTIONAL CUE: a colored flag/tag that classifies + an arrow that shows flow.
def flow_flag(x, y, txt, accent, fg="#fff", z=8):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;background:{accent};color:{fg};'
            f'font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;'
            f'padding:5px 12px;border-radius:4px;z-index:{z}">{txt}</div>')

# MODE 3 — LETTER AS ASSET: wrap a single letter with independent color/rotation (per-letter treatment)
def letter_asset(ch, color, rot=0, bg=None, fs=100):
    bgcss=f'background:{bg};padding:0 8px;' if bg else ''
    return (f'<span style="display:inline-block;color:{color};{bgcss}transform:rotate({rot}deg);'
            f'font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:.9">{ch}</span>')
