# Texture utilities — richness BUILT IN, priority order: halftone-in-fill, cut-paper depth, riso photo.
# These are meant to be part of an element's construction, not overlaid after.

def halftone_fill(base, dot="#0A0A0A", size=9, dot_op=0.06, angle=0):
    # RULE: no halftone on solid colors. Return FLAT fill. (Halftone lives only in riso_photo_wrap.)
    return f'background-color:{base};'

def halftone_gradient(base, dot="#0A0A0A", size_from=6, size_to=16):
    # graduated halftone (dots grow) — the classic riso/print shading. Use for shaded panels.
    return (f'background-color:{base};'
            f'background-image:radial-gradient({dot} 30%, transparent 32%);'
            f'background-size:{size_from}px {size_from}px;')

def riso_photo(src, tint="#1B3A8A", mix="multiply", contrast=1.15):
    # duotone/riso photo treatment: grayscale + tint + grain. Returns an <img> style string body.
    return (f'width:100%;height:100%;object-fit:cover;'
            f'filter:grayscale(1) contrast({contrast});')

def riso_photo_wrap(src, tint, size_css, extra=""):
    # full riso photo element: grayscale photo under a tint blend + halftone overlay
    return (f'<div style="position:relative;{size_css};overflow:hidden;{extra}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.2) brightness(1.05)">'
            f'<div style="position:absolute;inset:0;background:{tint};mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;background-image:radial-gradient(#00000055 1.2px,transparent 1.6px);background-size:5px 5px;mix-blend-mode:multiply;opacity:.4"></div>'
            f'</div>')

def cutpaper(x,y,w,h,col,rot=0,z=3,shadow=14,radius="0",ht=True):
    # a single flat cut-paper shape: flat fill + optional halftone-in + hard flat drop (no blur)
    htcss=halftone_fill(col,"#0A0A0A",11,0.10) if ht else f'background:{col};'
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{w}px;height:{h}px;{htcss}'
            f'border-radius:{radius};transform:rotate({rot}deg);z-index:{z};'
            f'box-shadow:{shadow}px {shadow}px 0 rgba(10,10,10,.22)"></div>')
