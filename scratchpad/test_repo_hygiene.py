"""Self-tests for repo-wide invariants that no single module owns.

These exist because the failures they catch are INVISIBLE to a module-level test:
nothing imports a stale path or a duplicated manual, so nothing fails until a person
or an agent follows the instruction and hits a wall.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_repo_hygiene.py
"""
import io, os, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 0


def ok(cond, msg):
    global N
    assert cond, "FAILED: " + msg
    N += 1
    print(f"  ok {N}: {msg}")


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".obsidian"}


def walk(exts):
    for dp, dn, fns in os.walk("."):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for fn in fns:
            if fn.lower().endswith(exts):
                yield os.path.join(dp, fn)


def read(p):
    try:
        return io.open(p, encoding="utf-8").read()
    except Exception:
        return ""


# ── THE DEAD REPO ROOT ──────────────────────────────────────────────────────
# `C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE` has not existed
# since the repo moved. It broke the self-tests (twice), CLAUDE.md's copy-paste
# template (session 10e), a checked-in example script and FOUR scripts inside a
# live skill. Each time it was fixed in the one place it was noticed. By session
# 10f it was in 50 Python files, AGENTS.md, and a second copy of the manual in the
# Obsidian vault — three documents carrying the same broken template, of which
# 10e had fixed exactly one.
#
# It reached that scale because nothing was watching. Now something is.
DEAD = r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE"

# Files that are ALLOWED to name it: the ones whose job is to tell the story of
# the bug. A changelog that cannot quote the broken path is a worse changelog.
NARRATIVE = ("brain/decisions.md", "scratchpad/friction", "scratchpad/sonnet_b_",
             "scratchpad/test_repo_hygiene.py")


def narrative(p):
    q = p.replace("\\", "/").lstrip("./").lower()
    return any(q.startswith(n) or n in q for n in NARRATIVE)


offenders = [p for p in walk((".py", ".md")) if DEAD in read(p) and not narrative(p)]
ok(offenders == [],
   f"no instruction file names the dead pre-move repo root (found: {offenders[:4]})")

# ── EVERY SCRIPT LOCATES ITS OWN ROOT ───────────────────────────────────────
# The rule from CLAUDE.md §6: derive the root from the script's own location.
# Any absolute Windows path in an os.chdir is the same bug wearing a new address.
absolute_chdir = []
for p in walk((".py",)):
    if narrative(p):
        continue
    for i, line in enumerate(read(p).split("\n"), 1):
        s = line.strip()
        if s.startswith("os.chdir(") and (":\\" in s or ':/' in s):
            absolute_chdir.append(f"{p}:{i}")
ok(absolute_chdir == [],
   f"no script chdir's to a hardcoded absolute path (found: {absolute_chdir[:4]})")

# ── THE TEMPLATE EXISTS IN THREE PLACES; THEY MUST AGREE ────────────────────
# CLAUDE.md, AGENTS.md and the vault's Manual/06 all carry the bespoke-script
# skeleton. 10e fixed one. An agent reading AGENTS.md — which many harnesses read
# by convention — still got the broken one.
COPIES = ["CLAUDE.md", "AGENTS.md", "AQ Design Engine/Manual/06 The Bespoke Script.md"]
present = [p for p in COPIES if os.path.exists(p)]
ok(len(present) >= 2, f"the manual really does exist in several copies: {present}")
for p in present:
    ok("os.path.dirname(os.path.abspath(__file__))" in read(p),
       f"{p} teaches a self-locating repo root")

# ── ONE PASS BANNER PER TEST FILE ───────────────────────────────────────────
# test_stylebank.py had accumulated THREE "ALL {N} ASSERTIONS PASSED" prints, two
# of them mid-file. A run that died at assertion 19 printed "ALL 18 ASSERTIONS
# PASSED" first, so anything grepping the output read a failure as a success.
for p in sorted(walk((".py",))):
    base = os.path.basename(p)
    if not base.startswith("test_"):
        continue
    # Count PRINT STATEMENTS, not occurrences of the words — this file names the
    # banner in its own matcher, and counting substrings made it fail itself.
    banners = [l for l in read(p).split("\n")
               if l.lstrip().startswith("print(")
               and ("ASSERTIONS PASSED" in l.upper() or "assertions passed" in l)]
    ok(len(banners) <= 1,
       f"{base} prints at most one pass banner (found {len(banners)})")

print(f"\nALL {N} ASSERTIONS PASSED")
