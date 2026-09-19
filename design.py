#!/usr/bin/env python
"""AQ — "just design something".

    python design.py "126 return visits to one partner in Kolkata"
    python design.py "volunteer sign-ups open" --dept events --canvas story
    python design.py "..." --seed 7          # reproducible pick
    python design.py --list                  # what the bank knows

WHAT THIS IS FOR
Opening the repo and saying "design something" used to mean choosing a composition from
nothing, which is how output drifts toward whatever the model reached for last time. The
74 images in `training_samples/reference_posters/` are not only recreation TARGETS —
each one is a style with a measured ground, density and hero, and a written recipe once
someone has looked at it. This draws one of them, EDUCATED-random: filtered by whatever
you know (department, canvas, ground) and weighted so a judged style with a written
recipe wins over an unjudged one.

It prints a BRIEF, it does not render. The brief is the input to a normal Workflow B
build — because the looking gate (CLAUDE.md section 3) still has to run on a real PNG,
and nothing here can do that for you.
"""
import argparse, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "engine")


def _load(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(ENGINE, name + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def main():
    ap = argparse.ArgumentParser(description="Draw a style from the bank and print a brief.")
    ap.add_argument("subject", nargs="*", help="what the poster is about")
    ap.add_argument("--dept", help="welfare | events | labs | ops | content")
    ap.add_argument("--canvas", help="feed | story | square | linkedin | li_square")
    ap.add_argument("--ground", help="paper | dark | saturated")
    ap.add_argument("--hero", help="type | number | photo | shape | pile | grid")
    ap.add_argument("--kind", default="poster", help="poster | sheet | mockup | carousel")
    ap.add_argument("--seed", type=int, help="reproducible draw")
    ap.add_argument("--n", type=int, default=1, help="draw several options")
    ap.add_argument("--any", action="store_true",
                    help="allow styles nobody has looked at yet")
    ap.add_argument("--list", action="store_true", help="summarise the bank and exit")
    a = ap.parse_args()

    sb = _load("stylebank")
    core = _load("core")

    if a.list:
        bank = sb._load()
        S = bank.get("styles", {})
        judged = {k: v for k, v in S.items() if v.get("judged")}
        print(f"style bank: {len(S)} references, {len(judged)} judged\n")
        for k, v in sorted(judged.items(), key=lambda kv: kv[1].get("kind") or ""):
            m = v["measured"]
            print(f"  {k}  {(v.get('kind') or '?'):7} {(v.get('hero') or '?'):7} "
                  f"{m['ground']:9} cov {m['coverage']:.2f}  {v.get('mechanism') or ''}")
        if len(judged) < len(S):
            print(f"\n  {len(S)-len(judged)} still unjudged — `python engine/stylebank.py todo`")
        return

    subject = " ".join(a.subject).strip() or "(no subject given — pick one before building)"

    # A department implies its colour, which is a RULE, not a preference (core.DEPT).
    accent = core.accent_for(a.dept) if a.dept else None

    picks = sb.pick(dept=a.dept, canvas=a.canvas, ground=a.ground, hero=a.hero,
                    kind=a.kind, judged_only=not a.any, seed=a.seed, n=a.n)
    if not isinstance(picks, list):
        picks = [picks]

    for i, style in enumerate(picks):
        if i:
            print("\n" + "-" * 74 + "\n")
        print(sb.brief(style, subject))
        if accent:
            print(f"\n  DEPARTMENT COLOUR (fixed by rule, core.accent_for('{a.dept}')): {accent}")
            print(f"  text on it: {core.text_on(accent)}   "
                  f"as type on cream at 16px: {core.on_cream(accent, 16)}")
    print("\n" + "=" * 74)
    print("Now build it. Measure the reference first (compare.geometry), write a bespoke")
    print("script, render, and LOOK at the PNG. The score is a proxy; the eye is the gate.")


if __name__ == "__main__":
    main()
