# Phase I metrics implemented — quantify a rendered poster on ACC, VDR, palette, flow.
# Measures MY output so improvement is data-driven, not vibes.
import importlib.util
from PIL import Image
import math
def load(n):
    s=importlib.util.spec_from_file_location(n,f"" + os.path.dirname(os.path.abspath(__file__)) + "/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core")

async def element_boxes(html, w=1080, h=1350):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":w,"height":h})
        await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(700)
        js = """els => els.map(e => {
            const r = e.getBoundingClientRect();
            const s = getComputedStyle(e);
            return {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), fs:parseFloat(s.fontSize)||0, fw:s.fontWeight};
        }).filter(b => b.w>8 && b.h>8 && b.w<1200)"""
        boxes=await pg.eval_on_selector_all(".p *", js)
        await b.close()
    return boxes

def ACC(boxes, unit=8, M=64, tol=3):
    # Alignment Consistency: fraction of element edges that land on the grid (multiple of unit) or margin
    edges=[]
    for b in boxes:
        edges+= [b['x'], b['x']+b['w'], b['y'], b['y']+b['h']]
    good=0
    for e in edges:
        if abs(e-M)<=tol or abs(e-(1080-M))<=tol or (e%unit)<=tol or (unit-(e%unit))<=tol:
            good+=1
    return good/max(len(edges),1)

def VDR(boxes, w=1080, h=1350):
    # Visual Dominance Ratio: screen area of the single largest text element / total canvas
    texts=[b for b in boxes if b['fs']>0]
    if not texts: return 0
    big=max(texts,key=lambda b:b['fs'])
    return (big['w']*big['h'])/(w*h), big['fs']

def type_scale_ratio(boxes):
    # ratio between largest and smallest text sizes = hierarchy strength
    fs=sorted(set(round(b['fs']) for b in boxes if b['fs']>6))
    if len(fs)<2: return 0, fs
    return fs[-1]/fs[0], fs

def palette(png_path, k=6):
    im=Image.open(png_path).convert("RGB").resize((100,125)); px=list(im.getdata())
    from collections import Counter
    # quantize
    q=[(r//32*32,g//32*32,b//32*32) for r,g,b in px]
    common=Counter(q).most_common(k)
    return [(c,round(n/len(px),3)) for c,n in common]

def flow_score(boxes, w=1080, h=1350, reading="top-left"):
    # does the focal sit where the reading axis expects entry? reading-axis-aware.
    texts=[b for b in boxes if b['fs']>0]
    if not texts: return 0
    big=max(texts,key=lambda b:b['fs']*b['w'])
    cx,cy=(big['x']+big['w']/2)/w,(big['y']+big['h']/2)/h
    ideals={
      "top-left":(0.42,0.38),"top-down":(0.42,0.30),"typographic":(0.5,0.45),
      "center-out":(0.5,0.44),"diagonal":(0.5,0.5),"edge-anchored":(0.6,0.42),
      "corner-diagonal":(0.68,0.68),"z-pattern":(0.5,0.5),"scan":(0.5,0.4),
    }
    ix,iy=ideals.get(reading,(0.42,0.38))
    dist=math.hypot(cx-ix,cy-iy)
    return max(0,1-dist*1.4)


def functional_saturation(boxes, cta_tags={"chip","cta","bubble","button","date"}):
    """Do high-saturation accents concentrate on action/CTA elements vs structural text?
    Returns (cta_accent_rate, body_neutral_rate). High FS = accents reserved for actions."""
    # heuristic via role: title/hero can be bold; body/meta should be neutral; chips/cta should be accent
    def is_accent_role(t): return t in cta_tags
    def is_struct_role(t): return t in {"body","meta","sub","BODY","META","P","SPAN","DIV"}
    cta=[b for b in boxes if is_accent_role(b.get("tag",""))]
    struct=[b for b in boxes if is_struct_role(b.get("tag",""))]
    # we can't read color here reliably, so report counts as a proxy of intent separation
    return len(cta), len(struct)

async def audit_metrics(build_fn, png_path, name, reading="top-left"):
    html=build_fn()
    boxes=await element_boxes(html)
    acc=ACC(boxes); vdr,bigfs=VDR(boxes); tsr,fs=type_scale_ratio(boxes); flow=flow_score(boxes,reading=reading)
    pal=palette(png_path)
    print(f"\n=== {name} ===")
    print(f"  ACC (alignment consistency): {acc:.2f}  (>0.75 = tight)")
    print(f"  VDR (dominance ratio): {vdr:.3f}  hero font {bigfs:.0f}px  (0.06-0.20 = strong hero)")
    print(f"  Type scale ratio: {tsr:.1f}x  sizes={fs[:8]}  (>4x = clear hierarchy)")
    print(f"  Flow score: {flow:.2f}  (>0.7 = focal in natural entry zone)")
    print(f"  Palette top: {[c for c,_ in pal[:4]]}")
    return dict(acc=acc,vdr=vdr,tsr=tsr,flow=flow)
