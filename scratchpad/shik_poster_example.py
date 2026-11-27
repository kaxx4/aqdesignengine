"""WORKED EXAMPLE: a Shikshaq feed poster (1080x1350), built ONLY from engine/shikshaq.py.

Mechanism: bone top panel with a mixed-weight headline, an indigo slab below carrying real paper
covers, one tilted sticker, one mascot. Every figure is a sk.FACTS value and the copy passes copy_gate.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/shik_poster_example.py
"""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

W, H = sk.SIZES["feed"]
F = sk.FACTS
sp = F["sample_papers"]
line1, line2 = f"{F['papers']} board papers.", "Free to read."
sticker_txt = f"First {F['free_questions']} questions need no account"
copy = [line1, line2, sticker_txt, "Read the paper before it reads you.", "Browse past papers", "Free to read. Always."]
errs, warns = sk.copy_gate(copy)
assert not errs, errs

top = (f'<div style="padding:56px 64px">{sk.logo(False, 64)}'
       f'<p class="eyebrow" style="font-size:30px;margin-top:44px">Board exams · ICSE, CBSE, ISC</p>'
       f'<h1 style="font-weight:400;font-size:122px;line-height:1;letter-spacing:-.05em;margin-top:30px;white-space:nowrap">'
       f'{line1}<br><b style="font-weight:800;color:var(--orange)" data-accent-display>{line2}</b></h1>'
       f'{sk.sticker(sticker_txt, 5, style="right:56px;top:60px;height:60px;font-size:26px;padding:0 28px")}</div>')

def big_cover(i):
    p = sk.palette_from_key(f"{sp[i]['board']} {sp[i]['subject']} {sp[i]['cls']}")
    return (f'<div style="width:296px;height:290px;border-radius:30px;display:flex;overflow:hidden;background:{p["tint"]};box-shadow:0 20px 44px -16px rgba(0,0,0,.45)">'
            f'<u style="width:26px;background:{p["solid"]}"></u><div style="display:flex;flex-direction:column;gap:6px;padding:28px 24px;font-size:24px;line-height:1.2;flex:1;color:{p["text"]}">'
            f'<span style="font-weight:700;letter-spacing:.04em;font-size:22px;text-transform:uppercase">{sp[i]["board"]} · {sp[i]["year"]}</span>'
            f'<span style="font-family:Archivo;font-weight:800;font-size:64px;letter-spacing:-.05em;line-height:1">{sp[i]["subject"]}</span>'
            f'<span>Class {sp[i]["cls"]}</span><span style="margin-top:auto;font-weight:700">Board · {sp[i]["questions"]} questions</span></div></div>')

bottom = (f'<div style="padding:56px 64px;position:relative;height:100%"><div style="position:absolute;right:64px;top:44px;width:176px;height:176px">{sk.mascot("orange", cls="", size=176)}</div>'
          f'<p class="eyelab" style="font-size:24px;color:#fff">The boards set</p>'
          f'<h2 style="font-weight:800;font-size:58px;margin-top:10px;max-width:690px">Read the paper before it reads you.</h2>'
          f'<div style="display:flex;gap:26px;margin-top:34px">{big_cover(0)}{big_cover(1)}{big_cover(2)}</div>'
          f'<div style="position:absolute;left:64px;bottom:44px;display:flex;align-items:center;justify-content:space-between;width:calc(100% - 128px)">'
          f'<span class="pill white" data-tap style="height:92px;padding:0 44px;font-size:34px;font-weight:800">Browse past papers →</span>'
          f'<span style="font-size:26px;color:#fff;text-align:right;line-height:1.3">{F["site"]}<br>Free to read. Always.</span></div></div>')

html = sk.doc(sk.poster([("bone", top, 600), ("indigo", bottom, None)], W, H), kind="poster", W=W, H=H, title="655 board papers")
res = sk.render_sync(html, "out/shikshaq/poster-papers.png", W, H, kind="poster")
print("CLEAN" if res.clean else res.hard)
