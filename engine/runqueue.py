"""AQ ENGINE — queue: durable, resumable state for the 44-poster recreation run.

WHY THIS EXISTS
The recreation run is long (44 posters x several convergence iterations each) and WILL outlive any
single context window. Without durable state, a fresh window has no idea which posters are done,
which failed, or what the last score was — so the run silently restarts or skips.

This makes resumption STATELESS: any model in any new window runs `python engine/queue.py next`
and immediately knows what to work on. No human hand-off, no memory of the prior session required.

Commands (run from repo root):
    python engine/queue.py init      # build the queue from training_samples/ (idempotent, safe)
    python engine/queue.py next      # print the next poster to work on + its slug
    python engine/queue.py status    # progress summary
    python engine/queue.py record <slug> <score> <iters> "<note>"   # save an outcome
    python engine/queue.py fail <slug> "<why>"                      # park a blocked poster

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
    prog = [k for k, v in it.items() if v["status"] == "in_progress"]
    print(f"DONE {len(done)} | IN-PROGRESS {len(prog)} | BLOCKED {len(failed)} | PENDING {len(pend)}"
          f"  (of {len(it)})")
    if done:
        sc = [it[k]["score"] for k in done if it[k]["score"] is not None]
        if sc:
            print(f"  mean score {sum(sc)/len(sc):.3f} (accept <= {q['accept_score']})")
    for k in prog:
        print(f"  in-progress: {k} ({it[k]['note']})")
    for k in failed:
        print(f"  BLOCKED: {k} — {it[k]['note']}")


def nxt():
    q = _load()
    it = q["items"]
    # resume an interrupted poster before starting a new one
    for k, v in it.items():
        if v["status"] == "in_progress":
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
    print("ALL DONE — no pending posters.")


def record(slug, score, iters, note=""):
    q = _load()
    if slug not in q["items"]:
        print(f"unknown slug {slug}"); return
    score = float(score)
    q["items"][slug].update(
        status="done" if score <= q["accept_score"] else "in_progress",
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
