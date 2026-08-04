"""RECREATION — 17c7de5509caae, iteration 2. Renders the ALREADY-WRITTEN contact_sheet() scene
from gen_showcase5d.py (never routed into out/versions/ before) into the queue's own folder.

WHY THIS SCENE: the reference is a 6-tile moodboard of "PORTFOLIO" treatments. Per CLAUDE.md §5's
multi-slide rule, a poster should pick ONE mechanism rather than the whole board. The prior v1.png
(script since lost, same pattern as two other posters this session) picked a single ransom-note
wordmark tile in isolation, which scored 1.2 against compare.py because compare.py's target is the
FULL moodboard image — a mismatch the metric cannot see past (no SEMANTIC axis, per DECISIONS.md).
contact_sheet() instead recreates the reference's own GRID MECHANISM — seven independent mini
compositions of one word, unified by a caption strip — which is the more faithful "one mechanism"
choice: not one tile copied, but the moodboard's own organizing idea, applied to AQ's own ask.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))

src = open("scratchpad/gen_showcase5d.py", encoding="utf-8").read().split("JOBS = [")[0]
ns = {}
exec(compile(src, "gen_showcase5d_partial", "exec"), ns)

async def main():
    html = await ns["contact_sheet"]()
    os.makedirs("out/versions/17c7de5509caae", exist_ok=True)
    await ns["B"].render(html, "out/versions/17c7de5509caae/v2.png", ns["W"], ns["H"])
    print("wrote v2.png")
asyncio.run(main())
