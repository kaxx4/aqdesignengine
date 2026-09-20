"""AQ ENGINE — runqueue: durable, resumable state for the recreation run.

WHY THIS EXISTS
The recreation run is long (74 posters x several convergence iterations each) and WILL outlive any
single context window. Without durable state, a fresh window has no idea which posters are done,
which failed, or what the last score was — so the run silently restarts or skips.

This makes resumption STATELESS: any model in any new window runs `python engine/runqueue.py next`
and immediately knows what to work on. No human hand-off, no memory of the prior session required.

Commands (run from repo root):
    python engine/runqueue.py init      # build the queue from training_samples/ (idempotent, safe)
    python engine/runqueue.py next      # print the next poster to work on + its slug
    python engine/runqueue.py status    # progress summary
    python engine/runqueue.py record <slug> <score> <iters> "<note>"   # save an outcome
    python engine/runqueue.py fail <slug> "<why>"                      # park a blocked poster

NOTE ON THE FILENAME: this is runqueue.py, not queue.py. Every command above used to
read `engine/queue.py`, a file that does not exist and must not — a module named
queue.py in engine/ shadows the stdlib and broke every bespoke script once already
(CLAUDE.md section 10). Copy-pasting from this docstring failed until 2026-09-20.

STATUSES: pending (never opened) | in_progress (claimed by `next`, no score recorded
yet) | attempted (tried and scored, still above the accept line) | done | blocked.
`attempted` exists because `record` used to write `in_progress` for an unconverged
score, which made 36 finished attempts look like live work and jammed `next` on the
first of them for a month. See _status().

State lives in brain/RECREATION_QUEUE.json. ACCEPT_SCORE mirrors RECREATION_PROTOCOL.md.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFDIR = os.path.join(ROOT, "training_samples", "reference_posters")
QPATH = os.path.join(ROOT, "brain", "RECREATION_QUEUE.json")
ACCEPT_SCORE = 0.16


def _load():
    if not os.path.exists(QPATH):
        return {"accept_score": ACCEPT_SCORE, "items": {}}
    with open(QPATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(q):
    os.makedirs(os.path.dirname(QPATH), exist_ok=True)
    with open(QPATH, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)


# ── STATUS, DERIVED ─────────────────────────────────────────────────────────
# THE BUG THIS FIXES (session 10f). `record()` set status back to "in_progress"
# whenever the score missed the accept line, so "attempted, did not converge" became
# indistinguishable from "a session is working on this RIGHT NOW". `nxt()` resumes
# in-progress work before starting anything new and returns the FIRST such entry — so
# with 36 of them, every new window was handed the same stuck poster, and the 26
# never-touched references were unreachable through the documented entry point.
#
# CLAUDE.md tells every session to run `runqueue.py next` on entry. That command had
# been returning one identical answer, which is why the run sat at 3 done out of 74
# while 36 had been worked. All 36 carried a recorded score; not one was a real
# interruption.
#
# DERIVED rather than migrated, because four agents were recording outcomes into this
# JSON while the fix was being written and a read-time derivation cannot race with
# them. `record()` stores the correct value going forward; both agree on meaning.
def _status(v):
    """attempted = tried and scored, above the line. in_progress = claimed, no score yet."""
    st = v.get("status")
    if st == "in_progress" and v.get("score") is not None:
        return "attempted"
    return st


def init():
    q = _load()
    files = sorted(f for f in os.listdir(REFDIR) if f.lower().endswith((".jpg", ".png")))
    added = 0
    for f in files:
        slug = f[:14]
        if slug not in q["items"]:                      # never clobber existing progress
            q["items"][slug] = {"file": f, "status": "pending", "score": None,
                                "iters": 0, "note": ""}
            added += 1
    _save(q)
    print(f"queue: {len(q['items'])} posters ({added} newly added) -> {QPATH}")


def status():
    q = _load()
    it = q["items"]
    done = [k for k, v in it.items() if v["status"] == "done"]
    failed = [k for k, v in it.items() if v["status"] == "blocked"]
    pend = [k for k, v in it.items() if v["status"] == "pending"]
    prog = [k for k, v in it.items() if _status(v) == "in_progress"]
    tried = [k for k, v in it.items() if _status(v) == "attempted"]
    print(f"DONE {len(done)} | IN-PROGRESS {len(prog)} | BLOCKED {len(failed)} | PENDING {len(pend)}"
          f"  (of {len(it)})")
    if done:
        sc = [it[k]["score"] for k in done if it[k]["score"] is not None]
        if sc:
            print(f"  mean score {sum(sc)/len(sc):.3f} (accept <= {q['accept_score']})")
    for k in prog:
        print(f"  in-progress (claimed, no score yet): {k} ({it[k]['note']})")
    if tried:
        best = sorted((it[k]["score"], k) for k in tried)[:3]
        print(f"  attempted, above the line: {len(tried)} "
              f"— closest: " + ", ".join(f"{k} {sc}" for sc, k in best))
    for k in failed:
        print(f"  BLOCKED: {k} — {it[k]['note']}")


def nxt():
    q = _load()
    it = q["items"]
    # 1. A GENUINE interruption: claimed by a previous `next` and never recorded.
    for k, v in it.items():
        if _status(v) == "in_progress":
            print(f"RESUME {k}\nfile: {v['file']}\niters so far: {v['iters']}\nnote: {v['note']}")
            return
    for k, v in it.items():
        if v["status"] == "pending":
            v["status"] = "in_progress"
            _save(q)
            print(f"NEXT {k}\nfile: {v['file']}\n"
                  f"reference: training_samples/reference_posters/{v['file']}\n"
                  f"output dir: out/versions/{k}/\n"
                  f"protocol: brain/RECREATION_PROTOCOL.md (accept score <= {q['accept_score']})")
            return
    # 3. Nothing new left: return the ATTEMPT CLOSEST TO CONVERGING, so the run keeps
    #    making progress instead of re-opening whichever entry happens to be first.
    tried = sorted(((v["score"], k) for k, v in it.items()
                    if _status(v) == "attempted" and v.get("score") is not None))
    if tried:
        score, k = tried[0]
        v = it[k]
        print(f"RETRY {k}  (best unconverged attempt, {score} vs accept "
              f"{q['accept_score']})\nfile: {v['file']}\n"
              f"reference: training_samples/reference_posters/{v['file']}\n"
              f"output dir: out/versions/{k}/\niters so far: {v['iters']}\n"
              f"note: {v['note']}")
        return
    print("ALL DONE — nothing pending and nothing left to converge.")


def record(slug, score, iters, note=""):
    q = _load()
    if slug not in q["items"]:
        print(f"unknown slug {slug}"); return
    score = float(score)
    q["items"][slug].update(
        status="done" if score <= q["accept_score"] else "attempted",
        score=score, iters=int(iters), note=note)
    _save(q)
    ok = "ACCEPTED" if score <= q["accept_score"] else "NOT YET (keep iterating)"
    print(f"{slug}: score {score} after {iters} iters -> {ok}")


def fail(slug, why):
    q = _load()
    if slug in q["items"]:
        q["items"][slug].update(status="blocked", note=why)
        _save(q)
        print(f"{slug} parked as BLOCKED: {why}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "init": init()
    elif cmd == "next": nxt()
    elif cmd == "status": status()
    elif cmd == "record": record(*sys.argv[2:6])
    elif cmd == "fail": fail(sys.argv[2], " ".join(sys.argv[3:]))
    else: print(__doc__)
