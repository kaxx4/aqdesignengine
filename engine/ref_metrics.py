# Measure the REFERENCE images on metric proxies so I know the TARGET numbers.
# From a flat JPEG I can extract: palette (dominant colors + accent ratio), VDR proxy (largest
# high-contrast connected region), edge/ink density, contrast, "ink coverage" (how much dark type),
# and a structure proxy (vertical/horizontal edge alignment).
import os, math
from PIL import Image, ImageFilter
import numpy as np
from collections import Counter

def analyze(path):
    im=Image.open(path).convert("RGB")
    w,h=im.size
    small=im.resize((160,int(160*h/w)))
    arr=np.asarray(small).astype(int)
    H2,W2,_=arr.shape
    # palette (quantized), dominant coverage
    q=(arr//48*48).reshape(-1,3)
    pal=Counter(map(tuple,q)).most_common(6)
    total=len(q)
    dom_cov=pal[0][1]/total
    # saturation: mean of (max-min)/max per pixel
    mx=arr.max(2); mn=arr.min(2)
    sat=np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    mean_sat=sat.mean()
    hi_sat_frac=(sat>0.5).mean()  # fraction of vivid pixels
    # contrast (std of luminance)
    lum=(0.299*arr[:,:,0]+0.587*arr[:,:,1]+0.114*arr[:,:,2])
    contrast=lum.std()/255
    # ink coverage: very dark pixels (headlines/outlines)
    ink=(lum<60).mean()
    # VDR proxy: biggest connected high-contrast region vs canvas (approx via dark-mask bounding blob)
    darkmask=(lum<90)
    # find largest row-run band of dark to approximate the dominant type block area
    colsum=darkmask.sum(0); rowsum=darkmask.sum(1)
    # crude bbox of the densest quadrant
    ys=np.where(rowsum>rowsum.max()*0.4)[0]; xs=np.where(colsum>colsum.max()*0.4)[0]
    if len(ys)>1 and len(xs)>1:
        vdr=((ys[-1]-ys[0])*(xs[-1]-xs[0]))/(H2*W2)
    else: vdr=0
    # structure/ACC proxy: edge alignment — Sobel, then how peaked are edge histograms (aligned edges = sharp peaks)
    g=small.convert("L").filter(ImageFilter.FIND_EDGES)
    ga=np.asarray(g)
    vprof=ga.sum(0); hprof=ga.sum(1)
    def peakiness(p):
        p=p/ (p.sum()+1e-6); 
        return (p.max()/ (p.mean()+1e-9))  # higher = more concentrated (aligned) edges
    acc_proxy=(peakiness(vprof)+peakiness(hprof))/2
    return dict(dom_cov=dom_cov, mean_sat=mean_sat, hi_sat_frac=hi_sat_frac,
                contrast=contrast, ink=ink, vdr=vdr, acc_proxy=acc_proxy, pal=[c for c,_ in pal[:4]])

if __name__=="__main__":
    files=sorted(os.listdir("/mnt/user-data/uploads"))
    files=[f for f in files if f.endswith(".jpg")]
    rows=[]
    for f in files:
        try:
            r=analyze("/mnt/user-data/uploads/"+f); rows.append((f[:10],r))
        except Exception as e:
            print("skip",f,e)
    # aggregate
    import statistics as st
    def col(k): return [r[k] for _,r in rows]
    print(f"analyzed {len(rows)} reference images\n")
    print(f"{'metric':16} {'median':>8} {'min':>8} {'max':>8}")
    for k in ["vdr","contrast","ink","mean_sat","hi_sat_frac","dom_cov","acc_proxy"]:
        v=col(k); print(f"{k:16} {st.median(v):8.3f} {min(v):8.3f} {max(v):8.3f}")
    print("\nInterpretation targets derived from references above.")
    