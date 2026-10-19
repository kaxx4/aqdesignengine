"""Welfare stats counted from the table the user pasted on 2026-10-19 (558 rows, transcribed to welfare_projects_2026-10-19.psv).
Every figure the TerraThon welfare stories print comes from here. Counting convention matches CLAUDE.md sec 12: all logged rows,
volunteers are TURNOUTS (one person at five drives counts five times), never unique people.
Run: python scratchpad/tt_welfare_stats.py
"""
import collections, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = []
for ln in open(os.path.join(ROOT, "scratchpad", "welfare_projects_2026-10-19.psv"), encoding="utf-8"):
    t, loc, cat, ym, vol, st = ln.rstrip("\n").split("|")
    ROWS.append(dict(title=t, loc=loc, cat=cat, year=2000 + int(ym[:2]), month=int(ym[2:]), vol=int(vol) if vol.isdigit() else 0, live=st == "L"))

SERIES = [("tails", r"^Tails and Treats"), ("grow", r"^Grow Green"), ("sharbat", r"^Sharbat (Seva|Drive)"), ("food", r"^Food For All"),
          ("books", r"^Book Basket"), ("clothes", r"^Wear and (Share|Write)"), ("toy", r"^Toy and Thread"), ("respect", r"^Respect and Reach"),
          ("sundar", r"^(Sunderbans|Genesis Sunderbans|Mukti Sunderbans|Pather Sathi Sunderbans|Medical Camp)"), ("cookie", r"^Cookie Pass On")]


def series(key):
    pat = dict(SERIES)[key]
    return [r for r in ROWS if re.search(pat, r["title"])]


N = len(ROWS)
VOLS = sum(r["vol"] for r in ROWS)
BY_CAT = collections.Counter(r["cat"] for r in ROWS)
BY_YEAR = collections.Counter(r["year"] for r in ROWS)
PATHER = sum(1 for r in ROWS if r["loc"] == "PS")
FUND = [r for r in ROWS if r["cat"] == "FE"]
_ENV = r"Earth|Green Talk|Waste|Bottle To Better|Plant Pact|Nature|Roots|Planet First|Heal The Earth|Green Hour|Green Christmas|Climate|Bottled Greens|Life in a Bottle|Paint the Planet|Sustainable|ReTee|Our Earth|For the Future|Plantation"
_HEALTH = r"Medical Camp|One Drop|Say Cheese|Tooth Talk|Dental|Health Over Sugar|Crisis Care|Safety First|Healthy Minds|Open Minds|Mind Matters|Healing Space|Peace Within|World Health|Mind and Body|Teen Talk|Well Within|Pose and Peace"
_WOMEN = r"Comfort Kits|Cycle of Care|Breaking the Cycle|Body Basics|Menstrual|Power Within|Her Voice|Empower Her|One for All|Budget Basics|Money Talks|Finance for All|Lab Legends"
PILLARS = ["children", "health", "women", "elderly", "community", "environment", "animals"]


def pillar(r):
    """One pillar per row, or None for fundraisers/misc. Order matters: women and health beat environment keywords; Smile Notes and Cookie are distribution."""
    t, c = r["title"], r["cat"]
    if c == "FD" and not t.startswith("Book Segregation"): return "animals"
    if c == "OA": return "elderly"
    if c in ("FE", "OT", "ST"): return None
    if re.search(_WOMEN, t): return "women"
    if re.search(_HEALTH, t): return "health"
    if c == "PD" or re.search(_ENV, t): return "environment"
    if c in ("DD", "XW", "SR") or t.startswith(("Smile Notes", "Cookie Pass On", "Book Segregation")): return "community"
    return "children"


def pstat(p):
    rs = [r for r in ROWS if pillar(r) == p]
    return dict(n=len(rs), vol=sum(r["vol"] for r in rs), rows=rs)


if __name__ == "__main__":
    print("rows", N, "(user table says 558)")
    for p in PILLARS:
        s = pstat(p); print("PILLAR", p, s["n"], "projects", s["vol"], "turnouts")
    print("not a pillar (fundraisers/misc)", sum(1 for r in ROWS if pillar(r) is None))
    for p in ("health", "women", "environment"):
        print(p, "->", sorted({r["title"].split(" 0")[0][:28] for r in pstat(p)["rows"]})[:60])
    print("volunteer turnouts", VOLS)
    print("by category", dict(BY_CAT))
    print("by year", dict(sorted(BY_YEAR.items())))
    print("Pather Sathi/Saathi", PATHER)
    for k, _ in SERIES:
        s = series(k); print(k, len(s), "projects", sum(r["vol"] for r in s), "turnouts")
    print("fundraisers", len(FUND), "turnouts", sum(r["vol"] for r in FUND))
    print("distinct locations", len({r["loc"] for r in ROWS}))
    print("draft rows", sum(1 for r in ROWS if not r["live"]))
