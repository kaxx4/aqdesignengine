"""The full Shikshaq character set (16), as one review sheet: every character on bone, then a ground-safety grid.
The set lives in engine/shikshaq.py (CHARACTERS, character(), character_ok()). Run:
  PYTHONIOENCODING=utf-8 python scratchpad/shik_characters_sheet.py"""
import asyncio, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

GROUNDS = [("bone", sk.C["card"]), ("indigo", sk.C["indigo"]), ("orange", sk.C["orange"]), ("dark", sk.C["panel"]), ("mint", sk.C["mint"])]


def tile(name, size=150):
    note = sk.CHARACTERS[name][3]
    return (f'<div style="width:240px;display:flex;flex-direction:column;align-items:center;gap:10px">'
            f'<div style="width:216px;height:216px;border-radius:44px;background:var(--card);box-shadow:var(--ring-card);display:grid;place-items:center">{sk.character(name, size)}</div>'
            f'<span style="font-family:Archivo;font-weight:800;font-size:30px;letter-spacing:-.03em">{name}</span>'
            f'<span style="font-size:20px;line-height:1.25;text-align:center;color:var(--prose);max-width:216px">{note}</span></div>')


def chip(name, gcol):
    ok = sk.character_ok(name, gcol)
    return (f'<div style="width:54px;height:54px;border-radius:14px;background:{gcol};display:grid;place-items:center;'
            f'{"" if ok else "box-shadow:inset 0 0 0 3px #D14545;"}">{sk.character(name, 38)}</div>')


async def main():
    names = list(sk.CHARACTERS)
    W, H = 1080, 1990
    rows = "".join(f'<div style="display:flex;gap:8px;justify-content:center">{"".join(tile(n) for n in names[i:i+4])}</div>' for i in range(0, 16, 4))
    grid = ""
    for gn, gc in GROUNDS:
        grid += (f'<div style="display:flex;gap:4px;align-items:center"><span style="width:82px;font-weight:600;font-size:20px;color:var(--text2)">{gn}</span>'
                 + "".join(chip(n, gc) for n in names) + "</div>")
    body = (f'<div style="position:absolute;inset:0;padding:48px 36px;background:var(--page)">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin:0 6px 26px"><span class="eyelab" style="font-size:24px">Characters: the full set of 16</span>'
            f'<span class="eyelab" style="font-size:24px">flat, two dots, one mouth</span></div>'
            f'<div style="display:flex;flex-direction:column;gap:22px">{rows}</div>'
            f'<div style="margin:34px 6px 14px;display:flex;justify-content:space-between"><span class="eyelab" style="font-size:22px">On each ground (a red ring = lost on it, below 1.5:1)</span>'
            f'<span class="eyelab" style="font-size:22px">in the order above</span></div>'
            f'<div style="display:flex;flex-direction:column;gap:8px">{grid}</div></div>')
    html = sk.doc(body, kind="poster", W=W, H=H, title="characters")
    async with sk.session() as s:
        return await s.render(html, "out/shikshaq/characters-set.png", W, H, kind="poster", name="characters-set")

if __name__ == "__main__":
    r = asyncio.run(main())
    print("CLEAN" if r.clean else r.hard)
