import asyncio, base64, os, sys, importlib.util
os.chdir("/home/user/aqdesignengine"); sys.path.insert(0,"engine")
def load(n):
    s=importlib.util.spec_from_file_location(n,f"engine/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core"); B=load("build")
f=base64.b64encode(open("engine/assets/fonts/StretchPro.otf","rb").read()).decode()
face=f"@font-face{{font-family:'StretchPro';src:url(data:font/otf;base64,{f}) format('opentype')}}"
rows=["WICKET","WICKEET","WICKEEET","WICKEEEET","WARS","WAARS","WAAARS","SOCCER","SOOCCER","STORM","STOORM","STOOORM","PICKLEEJAAM","TERRATHON","MINI-FEETE","MINI-FEEETE"]
h="".join(f'<div style="font-family:StretchPro;font-size:92px;line-height:1.05;color:#000;white-space:nowrap">{r} <span style="font:400 24px var(--e)">{r}</span></div>' for r in rows)
html=B.page(1600,1900,"#fff",f'<style>{face}</style><div style="position:absolute;left:30px;top:20px">{h}</div>',grain=False)
asyncio.run(B.render(html,"scratchpad/tt/stretch_spec.png",1600,1900))
