import asyncio, base64, os, sys, importlib.util
os.chdir("/home/user/aqdesignengine"); sys.path.insert(0,"engine")
def load(n):
    s=importlib.util.spec_from_file_location(n,f"engine/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core"); B=load("build")
f=base64.b64encode(open("engine/assets/fonts/SigmarOne-Regular.woff2","rb").read()).decode()
face=f"@font-face{{font-family:'SigmarOne';src:url(data:font/woff2;base64,{f}) format('woff2')}}"
rows=["A CRICKET TOURNAMENT","A PICKLEBALL TOURNAMENT","A FIFA TOURNAMENT","MINI-GAMES | COMPETITIONS"]
h="".join(f'<div style="font-family:SigmarOne;font-size:70px;line-height:1.3;color:#000;white-space:nowrap">{r}</div>' for r in rows)
html=B.page(1400,520,"#fff",f'<style>{face}</style><div style="position:absolute;left:30px;top:10px">{h}</div>',grain=False)
asyncio.run(B.render(html,"scratchpad/tt/sigmar_spec.png",1400,520))
