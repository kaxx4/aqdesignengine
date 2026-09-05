#!/usr/bin/env python3
"""
AQ POSTER ENGINE — generation entrypoint.

Usage (from repo root):
    python generate.py

This runs the full self-correcting pipeline for a piece:
    pick archetype + content  ->  engine builds from ENCODED RULES
    ->  render (Playwright)  ->  numeric gate (preview.critique)
    ->  per-archetype gate (ARCHETYPE_PROFILES)  ->  ENCODED self-correction (density escalate)
    ->  writes PNG to out/  ->  flags looking_required (the human/agent LOOKS at the PNG)

THE ONE RULE: every design must be a DIRECT OUTCOME of the engine's encoded rules.
If quality depends on hand-editing a single output, that is an ENGINE BUG — fix the RULE
in engine/engine.py (RULES / ARCHETYPE_PROFILES / the archetype fn), never the individual file.

After generation, ALWAYS run the LOOKING GATE (see brain/VISUAL_REVIEW.md):
present/open the PNG, review against every principle, and if a visual flaw appears that the
numeric gates missed, encode the fix as a RULE and regenerate. In Claude Code, wire the browser/
screenshot tool into the loop so looking runs every iteration automatically.
"""
import asyncio, os, sys, importlib.util
ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s=importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
eng = load("engine")

# ---- EXAMPLE CONTENT (edit or replace; content is INPUT, correction is the engine's job) ----
JOBS = [
  ("meals", "number_hero", dict(
      meta="welfare · food", kicker="we served", number="15k",
      label='<span style="font-family:var(--s);font-style:italic;text-transform:none;color:var(--tomato)">meals.</span> not<br>numbers.',
      chips=["one crate at a time","students, not staff"], band="every plate had a face.",
      body="hot food, sorted and served by hand across kolkata.", footer="@ngo.aquaterra"), 3),
  ("roots", "giant_type", dict(
      meta="est. 2021 · kolkata", word="roots", tags=["welfare","climate","education"],
      big="deep roots.<br>loud growth.", band="grown by teenagers.",
      body="a youth movement from one idea: teenagers can run real change.", footer="@ngo.aquaterra"), 2),
  ("community", "radial_orbit", dict(
      meta="everything we do", top="one community,", kicker="since 2021",
      number="534", label="drives", big="six ways to<br>show up.",
      orbit=[("food",3),("trees",1),("books",4),("dogs",0),("clothes",5),("health",6)],
      chips=["pick any. or all six.","no fees, ever"], footer="@ngo.aquaterra → pick your lane"), 2),
  ("teachers_day", "giant_type", dict(
      field="cream", meta="teachers' day · sept 5", word="teachers",
      tags=["mentors","patience","gratitude"],
      body="every kid we've reached learned from someone who chose to teach first. sundarban's classrooms run on you.",
      big="thank you for<br>showing up.", band="you taught us this too.",
      footer="@ngo.aquaterra"), 1),
]

async def main():
    os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
    for name, archetype, content, accent in JOBS:
        rep = await eng.generate(name, archetype, content, accent_idx=accent)
        status = "PASS" if rep.get("final_ok") else "NEEDS-LOOK"
        print(f"[{name:12}] {archetype:13} {status}  fill={rep['iters'][-1]['fill']}  -> out/{name}.png")
        print(f"               LOOKING GATE REQUIRED: open out/{name}.png and review (brain/VISUAL_REVIEW.md)")

if __name__ == "__main__":
    asyncio.run(main())
