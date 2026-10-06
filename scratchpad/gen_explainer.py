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

def hl(x): return f'<span class="hl">{x}</span>'
STEPS = [
 ("Open Claude and choose Google", A[4], "Go to claude.ai. Click 'Continue with Google'.",
  win('<div class="center"><div class="spark">✻</div><h3 class="sm">Your ideas, amplified</h3><div class="inp">Enter your email</div><div class="btn2 hlr">G&nbsp; Continue with Google</div><div class="btn2">Continue with email</div><p class="s">By continuing you agree to the Terms.</p></div>')),
 ("Pick the tech AI account", A[1], "Choose aquaterra.techai@gmail.com. Not a personal account.",
  win('<div class="center"><h3 class="sm">Choose an account</h3><p class="s">to continue to Claude</p><div class="acc hlr"><b class="av">A</b><div><div class="nm">AquaTerra Tech AI</div><small>aquaterra.techai@gmail.com</small></div></div><div class="acc"><b class="av g">K</b><div><div class="nm">Kanishk</div><small>personal account</small></div></div><div class="acc"><b class="av g">+</b><div class="nm">Use another account</div></div></div>', "accounts.google.com")),
 ("Kanishk approves the login", A[2], "Google asks for a second check. Kanishk gets a prompt on his phone and taps the number shown here. No tap, no login.",
  win('<div class="split"><div class="center"><h3 class="sm">2-Step Verification</h3><p>Open the Google prompt on your phone and tap the number below.</p><div class="num">42</div><p class="s">Waiting for approval…</p></div><div class="phone"><div class="pn">Sign-in attempt?</div><p>aquaterra.techai@gmail.com<br>claude.ai · Kolkata</p><div class="pb">Yes, it\'s me</div><div class="pb off">No</div><div class="pick"><i>17</i><i class="hlr">42</i><i>68</i></div></div></div>', "accounts.google.com")),
 ("Press Code", A[5], "You land in Claude. Press 'Code' in the left sidebar.",
  win('<div class="app"><div class="side"><div class="logo">Claude</div><div>＋ New chat</div><div>Chats</div><div>Projects</div><div class="on hlr">&lt;/&gt; Code</div><div class="foot">techai · Pro</div></div><div class="main"><h3 class="sm">Good evening</h3><div class="inp big">How can I help you today?</div></div></div>', "claude.ai/new")),
 ("Switch to the AQ Design Engine folder", A[0], "Open the repo picker. Change whatever is selected to aqdesignengine.",
  win('<div class="app"><div class="side"><div class="logo">Claude</div><div>Chats</div><div class="on">&lt;/&gt; Code</div></div><div class="main"><div class="pill">▾ some-other-folder</div><div class="menu"><div class="mi">some-other-folder</div><div class="mi">old-website</div><div class="mi hlr">✓ aqdesignengine</div></div></div></div>', "claude.ai/code")),
 ("Set Sonnet 5.5, effort Low, then prompt", A[3], "Pick model Sonnet 5.5 and effort Low. Type your brief and press send.",
  win('<div class="app"><div class="side"><div class="logo">Claude</div><div>Chats</div><div class="on">&lt;/&gt; Code</div></div><div class="main"><div class="pill">aqdesignengine</div><div class="box"><div class="txt">Make an AQ poster: 126 return visits to one partner in Kolkata</div><div class="tools"><span>＋</span><span class="hlr">Sonnet 5.5</span><span class="hlr">Effort: Low</span><span class="send">↑</span></div></div></div></div>', "claude.ai/code")),
 ("Add the necessary pictures", A[6], "Press + and attach the photos the poster needs. The engine only uses real AQ photos.",
  win('<div class="app"><div class="side"><div class="logo">Claude</div><div>Chats</div><div class="on">&lt;/&gt; Code</div></div><div class="main"><div class="box"><div class="thumbs"><div style="background:var(--pink)">food.jpg ✕</div><div style="background:var(--lemon)">edu.jpg ✕</div><div style="background:var(--sky)">event.jpg ✕</div></div><div class="txt">Use these three photos on the poster</div><div class="tools"><span class="hlr">＋ Add files</span><span>Sonnet 5.5</span><span>Low</span><span class="send">↑</span></div></div></div></div>', "claude.ai/code")),
 ("Save your changes: 'merge to main'", A[1], "Your edits show as a pending number. Type 'merge to main'. When the merge finishes, the number disappears.",
  win('<div class="app"><div class="side"><div class="logo">Claude</div><div>Chats</div><div class="on">&lt;/&gt; Code <b class="cnt">3</b></div></div><div class="main"><div class="msg">Poster saved. 3 files changed on your branch.</div><div class="box"><div class="txt">merge to main</div><div class="tools"><span>Sonnet 5.5</span><span>Low</span><span class="send">↑</span></div></div><div class="msg ok">✓ Merged to main. Pending count cleared: no number beside Code now.</div></div></div>', "claude.ai/code")),
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
.side{{padding:36px 22px;display:flex;flex-direction:column;gap:20px;font:700 24px var(--m)}}
.side div{{padding:12px 18px;border-radius:14px}}.side .on{{background:var(--hl);border:4px solid var(--ink)}}

.chips{{display:flex;gap:16px}}.chips span{{border:4px solid var(--ink);border-radius:999px;padding:12px 26px;font:700 24px var(--m);background:var(--hl)}}
.badge{{background:var(--tomato)!important;color:#fff}}.badge.off{{background:var(--bg2)!important;color:var(--ink3);text-decoration:line-through}}
.prompt{{border:4px solid var(--ink);border-radius:18px;padding:28px;font-size:30px;width:800px;background:var(--bg)}}
.thumbs{{display:flex;gap:24px}}.thumbs div{{width:230px;height:230px;border:4px solid var(--ink);border-radius:18px;display:flex;align-items:center;justify-content:center;font:700 22px var(--m);box-shadow:8px 8px 0 var(--ink)}}
.center{{width:100%;display:flex;flex-direction:column;align-items:center;gap:20px;text-align:center}}
h3.sm{{font-size:42px}}.spark{{font:900 80px var(--d);color:var(--tomato)}}
.inp{{width:620px;border:3px solid var(--ink3);border-radius:14px;padding:18px 22px;font-size:24px;color:var(--ink3);text-align:left}}.inp.big{{width:100%;padding:36px;margin-top:60px;font-size:28px}}
.btn2{{width:620px;border:3px solid var(--ink);border-radius:14px;padding:18px;font:700 24px var(--e);background:#fff}}
.hlr{{outline:7px solid var(--hl);outline-offset:5px;border-radius:14px}}
.acc{{display:flex;gap:20px;align-items:center;width:620px;border:3px solid var(--ink3);border-radius:14px;padding:18px 24px;text-align:left}}
.av{{width:60px;height:60px;border-radius:50%;background:var(--teal);color:#fff;display:flex;align-items:center;justify-content:center;font:900 28px var(--d)}}.av.g{{background:var(--ink3)}}.nm{{font:600 26px var(--e)}}
.split{{display:flex;gap:30px;width:100%;align-items:center}}.split .center{{flex:1}}
.phone{{width:290px;height:560px;border:6px solid var(--ink);border-radius:40px;padding:40px 22px;background:var(--bg);display:flex;flex-direction:column;gap:16px;font-size:20px;box-shadow:8px 8px 0 var(--ink)}}
.pn{{font:900 30px var(--d)}}.phone p{{font-size:17px;word-break:break-all}}.pb{{background:var(--ink);color:#fff;border-radius:999px;padding:14px;text-align:center;font:700 20px var(--e)}}.pb.off{{background:#fff;color:var(--ink);border:3px solid var(--ink)}}
.pick{{display:flex;gap:10px;justify-content:center;margin-top:10px}}.pick i{{font:900 34px var(--d);padding:10px 14px;border:3px solid var(--ink);border-radius:12px;background:#fff;font-style:normal}}
.app{{position:absolute;inset:0;display:flex}}
.side{{position:relative!important;width:250px!important;flex:none;background:var(--bg2);border-right:4px solid var(--ink)}}
.side .logo{{font:900 34px var(--s);font-style:italic;margin-bottom:16px;padding:0}}.side .foot{{margin-top:auto;font:500 18px var(--m);color:var(--ink3)}}
.main{{flex:1;margin:0!important;padding:50px 40px;display:flex;flex-direction:column;gap:20px}}
.pill{{align-self:flex-start;border:3px solid var(--ink);border-radius:999px;padding:10px 22px;font:700 22px var(--m);background:#fff}}
.menu{{border:4px solid var(--ink);border-radius:16px;background:#fff;width:420px;box-shadow:8px 8px 0 var(--ink)}}.mi{{padding:18px 24px;font:600 24px var(--e);border-bottom:2px solid var(--bg2)}}
.box{{border:4px solid var(--ink);border-radius:20px;padding:26px;background:#fff;display:flex;flex-direction:column;gap:22px;margin-top:20px}}
.txt{{font-size:28px;line-height:1.3}}.tools{{display:flex;gap:14px;align-items:center}}.tools span{{border:3px solid var(--ink);border-radius:999px;padding:8px 20px;font:700 20px var(--m)}}.tools .send{{margin-left:auto;background:var(--ink);color:#fff;width:52px;height:52px;display:flex;align-items:center;justify-content:center;padding:0}}
.side .on{{display:flex;align-items:center;white-space:nowrap}}.cnt{{background:var(--tomato);color:#fff;border-radius:999px;padding:2px 12px;font:700 20px var(--m);margin-left:8px}}
.msg{{background:var(--bg2);border-radius:16px;padding:22px 26px;font-size:26px}}.msg.ok{{background:var(--mintbright)}}
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
