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
ok(len(present) >= 2, f"the manual is referenced from several places: {present}")

# A copy that carries the template must teach the self-locating root. A copy that
# carries NO template (a pointer to CLAUDE.md) is the strongest agreement available
# and is what AGENTS.md became — it had frozen four sessions behind while claiming
# to be the manual, which is worse than being absent.
for p in present:
    body = read(p)
    has_template = "os.chdir(" in body
    if has_template:
        ok("os.path.dirname(os.path.abspath(__file__))" in body,
           f"{p} carries the template and teaches a self-locating root")
    else:
        ok("CLAUDE.md" in body,
           f"{p} carries no template and points at CLAUDE.md instead")

ok("os.chdir(" not in read("AGENTS.md"),
   "AGENTS.md is a pointer, not a second manual that can drift out of step")

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

# ── THE §6 TEMPLATE MUST ACTUALLY RUN ───────────────────────────────────────
# CLAUDE.md §6 is a copy-paste skeleton. It carried a dead `os.chdir` for months
# and BOTH building agents in session 10e hit it — a model following the manual
# alone failed on line 2. Nothing caught that because nobody ever executed the
# thing people are told to execute. Now the test suite does.
#
# This extracts the first ```python block under "## 6." and runs it end to end
# (it renders, so it is the slowest assertion here and worth every second).
import re as _re, subprocess as _sp, sys as _sys, tempfile as _tf

_man = read("CLAUDE.md")
_s6 = _man.index("## 6.")
_s7 = _man.index("## 7.", _s6)
_blocks = _re.findall(r"```python\n(.*?)```", _man[_s6:_s7], _re.S)
ok(len(_blocks) >= 1, "§6 contains a python template block to copy")

_tpl = _blocks[0]
ok("os.path.abspath(__file__)" in _tpl and ":\\" not in _tpl,
   "the template derives its own root and names no absolute path")
ok("elements=elements" in _tpl,
   "the template's render call passes elements= (without it the measured tier is off)")

# Run it from a scratch copy, with its output redirected out of the repo.
_out = _tf.mkdtemp(prefix="aq_tpl_")
_run = _tpl.replace('f"out/versions/{slug}"', repr(_out)) \
           .replace('f"out/versions/{slug}/v2.png"', repr(os.path.join(_out, "v2.png")))
_p = os.path.join("scratchpad", "_tpl_smoke.py")
io.open(_p, "w", encoding="utf-8").write(_run)
try:
    _env = dict(os.environ, PYTHONIOENCODING="utf-8")
    _r = _sp.run([_sys.executable, _p], capture_output=True, text=True,
                 timeout=300, env=_env, errors="replace")
    ok(_r.returncode == 0,
       "the §6 template RUNS as written (stderr: %s)" % (_r.stderr or "")[-400:])
    ok(os.path.exists(os.path.join(_out, "v2.png")),
       "...and produces the PNG it claims to")
    ok("[preflight]" in (_r.stdout or ""),
       "...with the gate actually reporting, not silently skipped")
    # A copy-paste template that prints errors on its first run teaches the reader
    # that errors are normal. The declarations in it must be self-consistent: the
    # first draft shipped a column-trap example and a container naming an element
    # that was never appended, so it printed two failures out of the box.
    ok("ISSUES" not in (_r.stdout or "") and "CLEAN" in (_r.stdout or ""),
       "...and the template's OWN example passes its own gate (stdout: %s)"
       % (_r.stdout or "")[-300:])
finally:
    try:
        os.remove(_p)
    except OSError:
        pass

print(f"\nALL {N} ASSERTIONS PASSED")
