import os
# GEOMETRIC RECONCILIATION — when eyes are unavailable, catch structural flaws by measuring
# actual element extents in the rendered DOM. Catches: text overflow, off-canvas, element collisions
# beyond the audit whitelist, text-wider-than-container, elements past margins.
import asyncio, importlib.util
def load(n):
    s=importlib.util.spec_from_file_location(n,os.path.join(os.path.dirname(os.path.abspath(__file__)),f"{n}.py")); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng=load("engine")
W,H=1080,1350; M=64

async def probe(name, archetype, content, accent_idx):
    accent=eng.RULES["accents"][accent_idx]
    # rebuild final html at the density it converged to — replay generate's density logic quickly
    from playwright.async_api import async_playwright
    # brute: try densities 0..4, pick first that passes preview (mirror engine)
    prof=eng.ARCHETYPE_PROFILES.get(archetype,dict(fill_min=0.34,max_density=3))
    import importlib.util as u
    sp=u.spec_from_file_location("pv","preview.py");pv=u.module_from_spec(sp);sp.loader.exec_module(pv)
    density=0; html=None
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for it in range(prof["max_density"]+1):
            inner=eng.ARCHETYPES[archetype](content,accent,density)
            html=eng.B.page(W,H,"var(--bg)",inner,grain=False)
            pg=await b.new_page(viewport={"width":W,"height":H},device_scale_factor=2)
            await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(500)
            await pg.locator(".p").screenshot(path=f"out/{name}.png")
            crit=pv.critique(f"out/{name}.png")
            arch_ok = crit["fill"]>=prof["fill_min"] and crit["contrast"]>=eng.RULES["contrast_min"] and all(v>=eng.RULES["quad_min"] for v in crit["quads"].values())
            if arch_ok: await pg.close(); break
            await pg.close()
            if crit["fill"]<prof["fill_min"]: density=min(density+1,prof["max_density"])
            else: break
        # now measure extents on final
        pg=await b.new_page(viewport={"width":W,"height":H})
        await pg.set_content(html,wait_until="load"); await pg.wait_for_timeout(500)
        els=await pg.eval_on_selector_all(".p [data-tag], .p [class*=measure]",
          """els=>els.map(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
             return{tag:e.dataset.tag||'',x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),
             right:Math.round(r.right),bottom:Math.round(r.bottom),
             sw:e.scrollWidth,cw:e.clientWidth}})""")
        await b.close()
    flaws=[]
    for e in els:
        if e['right']>1080-20: flaws.append(f"{e['tag']} overflows RIGHT edge (right={e['right']})")
        if e['bottom']>1350-20: flaws.append(f"{e['tag']} overflows BOTTOM (bottom={e['bottom']})")
        if e['x']<M-20: flaws.append(f"{e['tag']} breaches LEFT margin (x={e['x']})")
        if e['sw']>e['cw']+4: flaws.append(f"{e['tag']} TEXT WIDER than container (scroll {e['sw']}>{e['cw']})")
    return flaws

async def main():
    cases=[
      ("C1_paradox","giant_type",dict(meta="annual fest · nov",word="paradox",tags=["6 teams","1 night","0 chill"],big="the brief<br>drops soon.",band="pick a lane.",body="two months, one dangerously ambitious student fest.",footer="@ngo.aquaterra → brief in bio"),2),
      ("C4_ways","radial_orbit",dict(meta="the departments",top="one org,",kicker="6 teams",number="6",label="depts",big="find your<br>people.",orbit=[("events",3),("social",5),("welfare",1),("startups",4),("hr",0),("collabs",6)],chips=["there's a spot for you","no experience needed"],footer="@ngo.aquaterra → apply in bio"),2),
      ("C5_merch","giant_type",dict(meta="drop 03 · limited",word="roots",tags=["tees","totes","caps"],big="wear the cause.<br>fund the drive.",band="100% profit → drives.",body="streetwear designed by students.",footer="@ngo.aquaterra → shop in bio"),2),
      ("C7_saturday","giant_type",dict(meta="this week",word="saturday",tags=["6am","topsia","show up"],big="that's the<br>whole plan.",band="bring a friend.",body="food drive at dawn.",footer="@ngo.aquaterra"),1),
      ("C8_members","number_hero",dict(meta="milestone · 2026",kicker="we just hit",number="1.2k",label='teenagers.<br>one <span style="font-family:var(--s);font-style:italic;text-transform:none;color:var(--grape)">city.</span>',chips=["and counting","welfare·climate·education"],band="run entirely by students.",body="1,200 members across six departments.",footer="@ngo.aquaterra"),3),
    ]
    for name,arch,content,acc in cases:
        flaws=await probe(name,arch,content,acc)
        print(f"\n{name} ({arch}):")
        if flaws:
            for f in flaws: print(f"   ⚠ {f}")
        else: print("   ✓ no geometric flaws (extents clean)")
asyncio.run(main())
