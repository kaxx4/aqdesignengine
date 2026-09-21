# AQ LAYOUT AUDIT v2 — ignores parent/child nesting and whitelisted bleed elements.
import asyncio
from playwright.async_api import async_playwright
M=64; W,H=1080,1350
BLEED={"num"}
SKIP_PAIRS={("portrait","onphoto"),("onphoto","portrait"),("h","onhero"),("onhero","h"),
    ("sign","sign"),("lbl","lbl"),("stk","stk"),("pill","pill"),
    ("flyer","flyer"),("tape","tape"),("key","key"),("word","word"),("card","card")}
# element tags that are allowed to breach margin by design (tilted full-width notes/cards)
MARGIN_OK={"note","key","flyer","we","won","tb","title","body"}  # intentionally full-bleed, margin breach allowed
_BOXES_JS = "els=>els.map((e,i)=>{const r=e.getBoundingClientRect();return{i,tag:e.dataset.tag,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom),rgt:Math.round(r.right)}})"
# nesting: for each measure el, is it inside another measure el?
_NEST_JS = "els=>els.map((e,i)=>{let p=e.parentElement,inside=-1;while(p){if(p.classList&&p.classList.contains('measure')){inside=[...document.querySelectorAll('.measure')].indexOf(p);break}p=p.parentElement}return inside})"

async def audit(html, name, page=None, canvas=None, ignore_pairs=(), margin=None,
                bleed_tags=()):
    """Margin + overlap gate over the `.measure`-tagged DOM.

    `page`  — an ALREADY-LOADED playwright page showing this html. Pass it and the
              audit measures that page instead of cold-starting a second browser.
              This used to launch its own chromium on every single render, which
              (with the screenshot's launch) meant TWO browser cold starts and
              2.7s of blind sleeps per poster. See build.render / build.session.
    `canvas` — (W,H) of the piece. The module constants are feed-sized; a story
              (1080x1920) audited against 1350 reported phantom bottom breaches.
    `ignore_pairs` — by-design overlaps, in ANY pair spelling, SAME argument the
              caller already passes to layout.collision_check. Until this existed,
              the two overlap checkers did not cooperate: a bespoke script could
              silence layout's report and this one kept printing the same five
              overlaps on every render, from a closed SKIP_PAIRS vocabulary baked
              into this file that no caller could extend. The only thing that
              actually suppressed it was DOM parent/child nesting, which an agent
              found by reading this source after the documented parameter appeared
              to do nothing (session 10f, agent c3). A gate nobody can silence is a
              gate everybody learns to scroll past.
    `bleed_tags` — tags that leave the safe area ON PURPOSE, added to this module's
              BLEED and MARGIN_OK sets for this call. Those were closed vocabularies
              baked into this file (`BLEED={"num"}`, plus a fixed MARGIN_OK list), so
              a bespoke script with a deliberately bleeding element could not tell
              this gate about it and either lived with permanent warning noise or
              dropped the element from the gate entirely — an agent chose the latter
              and got DOM coverage on 4 of its 7 elements (session 10f, f80cb/f62f8).
              Same argument `preflight` and `measure_dom` already take, forwarded by
              `build.render`, so ONE declaration reaches all three.
    `margin` — the safe-area inset. Defaults to this module's M, which is a SECOND
              hardcoded 64 living in a different file from build.py's M=64. They
              agree today by coincidence of two separate literals, not because one
              reads the other; pass build's own value and they cannot drift.
    """
    aW, aH = canvas if canvas else (W, H)
    aM = M if margin is None else margin
    _bleed = set(BLEED) | {str(t) for t in (bleed_tags or ())}
    _mok = set(MARGIN_OK) | {str(t) for t in (bleed_tags or ())}
    _ign = set()
    for it in (ignore_pairs or ()):
        if isinstance(it, (frozenset, set, tuple, list)) and len(it) == 2:
            _ign.add(frozenset(str(x) for x in it))
    if page is not None:
        boxes = await page.eval_on_selector_all(".measure", _BOXES_JS)
        nest  = await page.eval_on_selector_all(".measure", _NEST_JS)
    else:
        async with async_playwright() as p:
            b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":aW,"height":aH})
            await pg.set_content("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"+html+"</body></html>",wait_until="load")
            await pg.wait_for_timeout(1200)
            boxes=await pg.eval_on_selector_all(".measure", _BOXES_JS)
            nest=await pg.eval_on_selector_all(".measure", _NEST_JS)
            await b.close()
    # TWO NAMESPACES, ONE ARGUMENT. layout.collision_check matches the LABELS in the
    # caller's `elements` tuples; this matches the DOM's `data-tag`. They are usually
    # the same strings, and nothing makes them be — an agent whose three plates all
    # shared data-tag="plate" had the tuple-level ignore work and the DOM-level one
    # silently miss, in the same render call (session 10f, agent g2). Say so rather
    # than let one half of a declaration quietly do nothing.
    _tags = {str(b.get('tag')) for b in boxes}
    _named = {l for pr in _ign for l in pr}
    _ghosts = sorted(_named - _tags)
    # PARTIAL mismatch only. If NONE of the ignored labels match a data-tag, the author
    # is simply using a different naming scheme for their element tuples than for the
    # DOM — legitimate, and warning about it printed identical noise on every render of
    # a 14-iteration recreation (session 10f, f2514b). If SOME match and some do not,
    # that asymmetry is the signal: one name in a working set is probably a typo.
    if _ghosts and len(_ghosts) < len(_named):
        print(f"   [{name}] IGNORE PAIRS NAME NO data-tag IN THE DOM: {_ghosts} — "
              f"this gate matches data-tag, while layout.collision_check matches your "
              f"element LABELS. Tags present: {sorted(_tags)[:8]}")
    issues=[]
    for k,bx in enumerate(boxes):
        if bx['tag'] not in _bleed and bx['tag'] not in _mok and (bx['x']<aM-3 or bx['rgt']>aW-aM+3 or bx['b']>aH-36):
            issues.append(f"MARGIN {bx['tag']} breaches safe area (x{bx['x']} r{bx['rgt']} b{bx['b']})")
    def ov(a,c):
        ix=min(a['rgt'],c['rgt'])-max(a['x'],c['x']); iy=min(a['b'],c['b'])-max(a['y'],c['y'])
        return ix,iy
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            if nest[i]==j or nest[j]==i: continue          # skip parent/child
            if boxes[i]['tag'] in _bleed or boxes[j]['tag'] in _bleed: continue
            if (boxes[i]['tag'],boxes[j]['tag']) in SKIP_PAIRS: continue  # bleed sits behind on purpose
            if frozenset((str(boxes[i]['tag']),str(boxes[j]['tag']))) in _ign: continue  # caller declared it
            ix,iy=ov(boxes[i],boxes[j])
            if ix>12 and iy>12:
                issues.append(f"OVERLAP {boxes[i]['tag']} x {boxes[j]['tag']} ({ix}x{iy}px)")
    # SCOPE-QUALIFIED on purpose. This says only "no margin breach or overlap among
    # the .measure-tagged DOM" — it is printed BEFORE reconcile's measured tier runs,
    # so a bare "CLEAN" here sat directly above lines like "BURIED copy ... is painted
    # but INVISIBLE". A verdict that reads as final while a later check is still to
    # report is how a real defect gets skimmed past.
    print(f"[{name}] {'margins/overlap CLEAN ✓' if not issues else 'ISSUES:'}")
    for x in issues: print("   -",x)
    return issues
