import asyncio, os, sys, importlib.util, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, "engine")
s = importlib.util.spec_from_file_location("core", "engine/core.py")
core = importlib.util.module_from_spec(s); s.loader.exec_module(core)
from playwright.async_api import async_playwright
OUT = "out/explainer"; W, H = 1920, 1080
A = core.ACCENTS

def win(inner, url="claude.ai"):
    return f'''<div class="win"><div class="bar"><i></i><i></i><i></i><span>{url}</span></div><div class="body">{inner}</div></div>'''
def btn(t, c="var(--ink)", fg="#fff", ring=False):
    return f'<div class="btn{" ring" if ring else ""}" style="background:{c};color:{fg}">{t}</div>'

STEPS = [
 ("Open Claude and choose Google", A[4],
  "Go to claude.ai. Click 'Continue with Google'.",
  win(f'<h3>Welcome back</h3>{btn("Continue with Google","#fff","var(--ink)",True)}{btn("Continue with email","#fff","var(--ink3)")}')),
 ("Pick the tech AI account", A[1],
  "Choose aquaterra.techai@gmail.com. Not a personal account.",
  win('<h3>Choose an account</h3><div class="row ring"><b>AQ</b><div>AquaTerra Tech AI<br><small>aquaterra.techai@gmail.com</small></div></div><div class="row"><b>+</b><div>Use another account</div></div>', "accounts.google.com")),
 ("Kanishk approves the login", A[2],
  "Google asks for a second check. Kanishk gets a prompt on his phone and taps the number shown on screen. No tap, no login.",
  win('<h3>Check your phone</h3><p>Google sent a prompt to Kanishk\'s device. Tap the matching number.</p><div class="num">42</div><p class="s">Wait on this screen until it moves on.</p>', "accounts.google.com")),
 ("Press Code", A[5],
  "You land in Claude. Press 'Code' in the left sidebar.",
  win('<div class="side"><div>Chats</div><div>Projects</div><div class="on ring">Code</div></div><div class="main"><h3>What do you want to build?</h3></div>')),
 ("Switch to the AQ Design Engine folder", A[0],
  "Open the folder or repo picker. Change whatever is selected to aqdesignengine.",
  win('<h3>Repository</h3><div class="row"><b>·</b><div>some-other-folder</div></div><div class="row ring"><b>✓</b><div>aqdesignengine</div></div>')),
 ("Set Sonnet 5.5, effort Low, then prompt", A[3],
  "Pick model Sonnet 5.5 and effort Low. Type your brief and send.",
  win('<div class="chips"><span>Sonnet 5.5</span><span>Effort: Low</span></div><div class="prompt">Make an AQ poster: 126 return visits to one partner in Kolkata</div>' + btn("Send","var(--ink)"))),
 ("Add the necessary pictures", A[6],
  "Attach any photos the poster needs. The engine only uses real AQ photos, never invented ones.",
  win('<h3>Attach files</h3><div class="thumbs"><div style="background:var(--pink)">photo 1</div><div style="background:var(--lemon)">photo 2</div><div style="background:var(--sky)">photo 3</div></div>')),
 ("Save your changes: 'merge to main'", A[1],
  "Your edits show as a pending number. Type 'merge to main'. When the merge finishes, the number disappears.",
  win('<div class="chips"><span class="badge">3 changes</span></div><div class="prompt">merge to main</div><div class="chips"><span class="badge off">0 changes</span><span>✓ merged</span></div>')),
]

CSS = f"""{core.FONTS}{core.ROOT}
*{{box-sizing:border-box;margin:0}}body{{width:{W}px;height:{H}px;background:var(--bg);font-family:var(--e);color:var(--ink);position:relative;overflow:hidden}}
.top{{position:absolute;left:80px;top:60px;font:700 22px var(--m);letter-spacing:.08em}}
.tag{{position:absolute;right:80px;top:60px;font:700 18px var(--m);color:var(--ink3)}}
.num-big{{position:absolute;left:80px;top:150px;font:900 220px/0.9 var(--d)}}
h1{{position:absolute;left:80px;top:400px;width:700px;font:900 76px/1 var(--d);text-transform:uppercase}}
.cap{{position:absolute;left:80px;top:760px;width:640px;font:400 30px/1.35 var(--e)}}
.win{{position:absolute;left:860px;top:150px;width:980px;height:780px;background:#fff;border:5px solid var(--ink);border-radius:22px;box-shadow:14px 14px 0 var(--ink);overflow:hidden}}
.bar{{height:56px;background:var(--bg2);border-bottom:4px solid var(--ink);display:flex;align-items:center;gap:10px;padding:0 20px}}
.bar i{{width:16px;height:16px;border-radius:50%;background:var(--ink)}}.bar span{{margin-left:20px;font:700 18px var(--m)}}
.body{{padding:60px;display:flex;flex-direction:column;gap:26px;align-items:flex-start;position:relative;height:calc(100% - 56px)}}
h3{{font:900 52px var(--d);text-transform:uppercase}}p{{font-size:26px;line-height:1.35}}.s{{color:var(--ink3);font-size:20px}}
.btn{{padding:20px 34px;border:4px solid var(--ink);border-radius:999px;font:700 24px var(--m);width:560px;text-align:center}}
.ring{{outline:7px solid var(--hl);outline-offset:6px}}
.row{{display:flex;gap:20px;align-items:center;border:4px solid var(--ink);border-radius:18px;padding:22px 28px;width:700px;font-size:26px}}
.row b{{width:56px;height:56px;border-radius:50%;background:var(--hl);display:flex;align-items:center;justify-content:center;font:900 24px var(--d)}}
small{{font:500 20px var(--m);color:var(--ink3)}}
.num{{font:900 190px/1 var(--d);background:var(--hl);border:5px solid var(--ink);padding:10px 60px;border-radius:26px}}
.side{{position:absolute;left:0;top:0;bottom:0;width:240px;background:var(--bg2);border-right:4px solid var(--ink);padding:40px 24px;display:flex;flex-direction:column;gap:24px;font:700 26px var(--m)}}
.side div{{padding:12px 18px;border-radius:14px}}.side .on{{background:var(--hl);border:4px solid var(--ink)}}
.main{{margin-left:260px}}
.chips{{display:flex;gap:16px}}.chips span{{border:4px solid var(--ink);border-radius:999px;padding:12px 26px;font:700 24px var(--m);background:var(--hl)}}
.badge{{background:var(--tomato)!important;color:#fff}}.badge.off{{background:var(--bg2)!important;color:var(--ink3);text-decoration:line-through}}
.prompt{{border:4px solid var(--ink);border-radius:18px;padding:28px;font-size:30px;width:800px;background:var(--bg)}}
.thumbs{{display:flex;gap:24px}}.thumbs div{{width:230px;height:230px;border:4px solid var(--ink);border-radius:18px;display:flex;align-items:center;justify-content:center;font:700 22px var(--m);box-shadow:8px 8px 0 var(--ink)}}
.note{{position:absolute;left:80px;bottom:40px;font:500 16px var(--m);color:var(--ink3)}}
.dots{{position:absolute;right:80px;bottom:44px;display:flex;gap:10px}}.dots i{{width:16px;height:16px;border-radius:50%;border:3px solid var(--ink)}}
"""
def frame(i, title, accent, cap, mock, total):
    dots = "".join(f'<i style="background:{accent if j==i else "transparent"}"></i>' for j in range(total))
    return f'''<html><head><style>{CSS}</style></head><body style="--hl:{accent}">
<div class="top">AQUATERRA / DESIGN ENGINE</div><div class="tag">STEP {i+1} OF {total}</div>
<div class="num-big" style="color:{accent};-webkit-text-stroke:4px var(--ink)">{i+1:02d}</div>
<h1>{title}</h1><div class="cap">{cap}</div>{mock}
<div class="note">Illustrated mockup, not a real screenshot</div><div class="dots">{dots}</div></body></html>'''

def title_card(t, sub, accent):
    return f'''<html><head><style>{CSS}</style></head><body style="--hl:{accent};background:var(--ink);color:var(--bg)">
<div class="top">AQUATERRA</div><h1 style="top:330px;width:1500px;font-size:150px">{t}</h1>
<div class="cap" style="top:700px;width:1200px;font-size:38px;color:{accent}">{sub}</div></body></html>'''

async def main():
    pages = [title_card("How to use the AQ Design Engine","Login with Google, Kanishk approves, then make a poster.",A[2])]
    pages += [frame(i,*st,len(STEPS)) for i,st in enumerate(STEPS)]
    pages.append(title_card("Done.","Tip: always look at the PNG before it ships.",A[1]))
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome" if os.path.exists("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") else None)
        pg = await b.new_page(viewport={"width":W,"height":H})
        for n,h in enumerate(pages):
            await pg.set_content(h); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"{OUT}/f{n:02d}.png")
        await b.close()
    subprocess.run(["ffmpeg","-y","-framerate","1/6","-i",f"{OUT}/f%02d.png","-vf","fps=30,format=yuv420p","-c:v","libx264",f"{OUT}/aq_design_engine_explainer.mp4"],check=True,capture_output=True)
    print("ok", len(pages))
asyncio.run(main())
