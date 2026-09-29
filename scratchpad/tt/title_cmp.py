import asyncio, base64, os, sys, importlib.util
os.chdir("/home/user/aqdesignengine"); sys.path.insert(0,"engine")
def load(n):
    s=importlib.util.spec_from_file_location(n,f"engine/{n}.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core=load("core"); B=load("build")
f=base64.b64encode(open("engine/assets/fonts/StretchPro.otf","rb").read()).decode()
face=f"@font-face{{font-family:'StretchPro';src:url(data:font/otf;base64,{f}) format('opentype')}}"
S="font-family:StretchPro"; N="font-family:var(--d);font-weight:900"
sp=lambda t: f'<span style="{S}">{t}</span>'
nf=lambda t: f'<span style="{N}">{t}</span>'
rows=[
 ("A all StretchPro EE", f'<div style="{S};font-size:92px">WICKEET<br>WAARS</div>'),
 ("A2 all StretchPro EEE/AA", f'<div style="{S};font-size:78px">WICKEEET<br>WAARS</div>'),
 ("B NeutralFace + Stretch E/A", f'<div style="font-size:150px;line-height:.9">{nf("WICK")}{sp("EE")}{nf("T")}<br>{nf("W")}{sp("AA")}{nf("RS")}</div>'),
 ("B2 NeutralFace + Stretch EEE/AA", f'<div style="font-size:150px;line-height:.9">{nf("WICK")}{sp("EEE")}{nf("T")}<br>{nf("W")}{sp("AA")}{nf("RS")}</div>'),
]
h="".join(f'<div style="margin:6px 0"><div style="font:400 22px var(--e)">{n}</div>{r}</div>' for n,r in rows)
html=B.page(1200,1500,"#fff",f'<style>{face}</style><div style="position:absolute;left:20px;top:10px;color:#000">{h}</div>',grain=False)
asyncio.run(B.render(html,"scratchpad/tt/title_cmp.png",1200,1500))
