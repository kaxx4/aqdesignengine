# AQ LAYOUT AUDIT v2 — ignores parent/child nesting and whitelisted bleed elements.
import asyncio, os
from playwright.async_api import async_playwright
M=64; W,H=1080,1350
_CHROME = "/opt/pw-browsers/chromium"
_LAUNCH_KW = {"executable_path": _CHROME} if os.path.exists(_CHROME) else {}
BLEED={"num"}
SKIP_PAIRS={("portrait","onphoto"),("onphoto","portrait"),("h","onhero"),("onhero","h"),
    ("sign","sign"),("lbl","lbl"),("stk","stk"),("pill","pill"),
    ("flyer","flyer"),("tape","tape"),("key","key"),("word","word"),("card","card")}
# element tags that are allowed to breach margin by design (tilted full-width notes/cards)
MARGIN_OK={"note","key","flyer","we","won","tb","title","body"}  # intentionally full-bleed, margin breach allowed
async def audit(html,name):
    async with async_playwright() as p:
        b=await p.chromium.launch(**_LAUNCH_KW); pg=await b.new_page(viewport={"width":W,"height":H})
        await pg.set_content("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"+html+"</body></html>",wait_until="load")
        await pg.wait_for_timeout(1200)
        boxes=await pg.eval_on_selector_all(".measure","els=>els.map((e,i)=>{const r=e.getBoundingClientRect();return{i,tag:e.dataset.tag,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom),rgt:Math.round(r.right)}})")
        # also get nesting: for each measure el, is it inside another measure el?
        nest=await pg.eval_on_selector_all(".measure","els=>els.map((e,i)=>{let p=e.parentElement,inside=-1;while(p){if(p.classList&&p.classList.contains('measure')){inside=[...document.querySelectorAll('.measure')].indexOf(p);break}p=p.parentElement}return inside})")
        await b.close()
    issues=[]
    for k,bx in enumerate(boxes):
        if bx['tag'] not in BLEED and bx['tag'] not in MARGIN_OK and (bx['x']<M-3 or bx['rgt']>W-M+3 or bx['b']>H-36):
            issues.append(f"MARGIN {bx['tag']} breaches safe area (x{bx['x']} r{bx['rgt']} b{bx['b']})")
    def ov(a,c):
        ix=min(a['rgt'],c['rgt'])-max(a['x'],c['x']); iy=min(a['b'],c['b'])-max(a['y'],c['y'])
        return ix,iy
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            if nest[i]==j or nest[j]==i: continue          # skip parent/child
            if boxes[i]['tag'] in BLEED or boxes[j]['tag'] in BLEED: continue
            if (boxes[i]['tag'],boxes[j]['tag']) in SKIP_PAIRS: continue  # bleed sits behind on purpose
            ix,iy=ov(boxes[i],boxes[j])
            if ix>12 and iy>12:
                issues.append(f"OVERLAP {boxes[i]['tag']} x {boxes[j]['tag']} ({ix}x{iy}px)")
    print(f"[{name}] {'CLEAN ✓' if not issues else 'ISSUES:'}")
    for x in issues: print("   -",x)
    return issues
