import asyncio, base64, os, sys, importlib.util
os.chdir("/home/user/aqdesignengine"); sys.path.insert(0,"engine")
def load(n):
    s=importlib.util.spec_from_file_location(n,f"engine/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core"); B=load("build")
f=base64.b64encode(open("engine/assets/fonts/StretchPro.otf","rb").read()).decode()
face=f"@font-face{{font-family:'StretchPro';src:url(data:font/otf;base64,{f}) format('opentype')}}"
S="font-family:StretchPro;font-size:80px;line-height:1.1;color:#000;white-space:nowrap"
def unit(t,ls): 
    import re
    return "".join(f'<span style="display:inline-block;margin-right:{ls}em">{u.group(0)}</span>' for u in re.finditer(r"(.)\1|.",t))
rows=[("ls=0",f'<div style="{S}">WICKEET</div>'),
      ("ls -0.035em (breaks?)",f'<div style="{S};letter-spacing:-0.035em">WICKEET</div>'),
      ("ls + font-feature-settings liga/dlig",f'<div style="{S};letter-spacing:-0.035em;font-feature-settings:\'liga\' 1,\'dlig\' 1;font-variant-ligatures:common-ligatures discretionary-ligatures">WICKEET</div>'),
      ("units with negative margin (ls 0)",f'<div style="{S}">{unit("WICKEET",-0.035)}</div>'),
      ("units + stroke .05em",f'<div style="{S};-webkit-text-stroke:4px #000">{unit("WICKEET",-0.06)}</div>')]
h="".join(f'<div style="margin:4px 0"><div style="font:400 20px var(--e)">{n}</div>{r}</div>' for n,r in rows)
html=B.page(1000,700,"#fff",f'<style>{face}</style><div style="position:absolute;left:20px;top:10px">{h}</div>',grain=False)
asyncio.run(B.render(html,"scratchpad/tt/lig_test.png",1000,700))
