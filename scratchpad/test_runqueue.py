"""Self-tests for engine/runqueue.py — the recreation run's resume mechanism.

This is the command CLAUDE.md tells EVERY session to run on entry, so a defect here
is invisible and total: it does not error, it just quietly hands out the wrong work.

THE BUG (session 10f). `record()` wrote status "in_progress" whenever a score missed
the accept line, so "attempted, did not converge" and "a session is working on this
right now" became the same value. `nxt()` resumes in-progress work before starting
anything new, and returns the FIRST such entry — so with 36 of them, every new window
got the same stuck poster and the 26 never-touched references were unreachable through
the documented entry point. The run sat at 3 done of 74 while 36 had been worked.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_runqueue.py
"""
import importlib.util, io, json, os, sys, tempfile

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")

_s = importlib.util.spec_from_file_location("runqueue", os.path.join(ENGINE, "runqueue.py"))
rq = importlib.util.module_from_spec(_s); _s.loader.exec_module(rq)

N = 0


def ok(cond, msg):
    global N
    assert cond, "FAILED: " + msg
    N += 1
    print(f"  ok {N}: {msg}")


import contextlib


def run(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue()


# ── the derivation, on the exact data shape that caused the jam ─────────────
ok(rq._status({"status": "in_progress", "score": 0.34}) == "attempted",
   "a recorded score above the line is ATTEMPTED, not in-progress")
ok(rq._status({"status": "in_progress", "score": None}) == "in_progress",
   "claimed with no score yet really is in-progress — a genuine interruption")
ok(rq._status({"status": "pending", "score": None}) == "pending",
   "pending is untouched")
ok(rq._status({"status": "done", "score": 0.11}) == "done",
   "done is untouched")

# ── next() must advance ─────────────────────────────────────────────────────
_tmp = tempfile.mkdtemp(prefix="aq_q_")
_real = rq.QPATH
rq.QPATH = os.path.join(_tmp, "q.json")
try:
    # the historical state: many finished-but-unconverged attempts, plus untouched work
    rq._save({"accept_score": 0.16, "items": {
        "aaaaaaaaaaaaaa": {"file": "a.jpg", "status": "in_progress", "score": 0.34,
                           "iters": 3, "note": "did not converge"},
        "bbbbbbbbbbbbbb": {"file": "b.jpg", "status": "in_progress", "score": 0.25,
                           "iters": 2, "note": "closer"},
        "cccccccccccccc": {"file": "c.jpg", "status": "pending", "score": None,
                           "iters": 0, "note": ""},
    }})
    out = run(rq.nxt)
    ok("NEXT cccccccccccccc" in out,
       "next() reaches the NEVER-TOUCHED poster instead of re-opening an old attempt")
    ok("RESUME" not in out,
       "...and does not call a finished attempt an interruption")

    # having claimed it, next() must now resume it — that IS a real interruption
    out = run(rq.nxt)
    ok("RESUME cccccccccccccc" in out,
       "a poster claimed by next() and not yet recorded IS resumed")

    # record it above the line: it becomes `attempted`, not a permanent claim
    run(rq.record, "cccccccccccccc", "0.40", "2", "tried")
    q = rq._load()
    ok(q["items"]["cccccccccccccc"]["status"] == "attempted",
       "record() above the accept line writes `attempted`, not `in_progress`")

    # nothing pending left: fall back to the attempt CLOSEST to converging
    out = run(rq.nxt)
    ok("RETRY bbbbbbbbbbbbbb" in out,
       "with nothing new left, next() returns the closest unconverged attempt (0.25)")
    ok("0.25" in out and "accept 0.16" in out,
       "...and shows how far it has to go, so the choice is legible")

    # and a converging score really does finish
    run(rq.record, "bbbbbbbbbbbbbb", "0.12", "4", "converged")
    ok(rq._load()["items"]["bbbbbbbbbbbbbb"]["status"] == "done",
       "record() at or under the accept line marks it done")

    # status() must not report finished attempts as live work
    st = run(rq.status)
    ok("IN-PROGRESS 0" in st,
       "status() reports no live work when every attempt has been recorded")
    ok("attempted, above the line: 2" in st,
       "...and counts the attempts separately, with the closest named")
finally:
    rq.QPATH = _real
    import shutil
    shutil.rmtree(_tmp, ignore_errors=True)

# ── the docstring must name a file that exists ──────────────────────────────
# Every command in it read `engine/queue.py` — a file that does not exist and must
# not, because a module named queue.py in engine/ shadows the stdlib and broke every
# bespoke script once already (CLAUDE.md §10). Copy-pasting from the docs failed.
doc = rq.__doc__ or ""
# Check the COMMAND lines, not the whole docstring — the note explaining this fix
# quotes the bad path on purpose, and a substring test over the lot fails on its own
# explanation. (Same shape as the pass-banner check that counted its own matcher.)
cmds = [l.strip() for l in doc.split("\n") if l.strip().startswith("python ")]
ok(cmds, "the docstring lists runnable commands at all")
ok(all("engine/runqueue.py" in c for c in cmds),
   f"every command names the real file, not engine/queue.py ({len(cmds)} commands)")
ok(os.path.exists(os.path.join(ENGINE, "runqueue.py"))
   and not os.path.exists(os.path.join(ENGINE, "queue.py")),
   "and on disk it really is runqueue.py, with no stdlib-shadowing queue.py beside it")

print(f"\nALL {N} ASSERTIONS PASSED")
