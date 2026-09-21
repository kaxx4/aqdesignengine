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
    python engine/runqueue.py verify   # re-score every recorded entry against its render

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


_BANK = None


def _kind(slug):
    """The style bank's judged `kind` for a slug, or None when it has no entry.

    The queue does not know what a reference IS; the bank does. That matters for
    ordering, because a `mockup` or a `sheet` cannot be scored as it stands — the
    protocol says crop the design out first and expect to PARK it — while a `poster`
    scores honestly. Reading the bank is best-effort: a missing or unreadable bank
    must never stop the run, so any failure degrades to None and the old ordering.
    """
    global _BANK
    if _BANK is None:
        try:
            with open(os.path.join(ROOT, "brain", "STYLE_BANK.json"), "r",
                      encoding="utf-8") as f:
                _BANK = json.load(f).get("styles", {})
        except Exception:
            _BANK = {}
    return (_BANK.get(slug) or {}).get("kind")


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
    # 2. Start something NEW — but a PENDING POSTER before a pending mockup.
    #
    # THE ORDERING BUG (session 10f, found the day after the status fix above). Taking
    # pending strictly in key order was fine until the last unstarted POSTER was
    # consumed. After that, all 22 remaining pending entries are mockups or sheets —
    # references the protocol says to crop and usually PARK — while 23 attempted
    # posters sat with real scores, the closest 0.009 from accepting. `next` would
    # have handed every new session an unscorable mockup and left the convergeable
    # work unreachable: the same shape of jam as the status conflation above, with a
    # different cause.
    _pend = sorted(((k, v) for k, v in it.items() if v["status"] == "pending"),
                   key=lambda kv: 0 if _kind(kv[0]) == "poster" else 1)
    for k, v in _pend:
        if True:
            v["status"] = "in_progress"
            _save(q)
            if _kind(k) in ("mockup", "sheet"):
                print(f"NOTE: this is a {_kind(k)} — crop the design out first "
                      f"(compare.crop), then measure and score against the CROP. Read "
                      f"RECREATION_PROTOCOL.md's MOCKUPS section; expect to park it.")
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


def record(slug, score, iters, note="", render=None):
    """Save an outcome. `render` is the PNG the score was measured FROM.

    WHY PROVENANCE (session 10f). Two agents independently found a stored score that
    no file on disk reproduced: one entry's 0.27 had been measured against an unrelated
    demo render, and another's 0.328 was worse than every PNG actually in its folder.
    Nothing recorded WHAT was scored, so a later session either trusts a number that
    describes a different image or has to re-derive it — and the queue is the run's
    ground truth across context windows, so an unverifiable number there is worse than
    no number.

    Defaults to the newest PNG in out/versions/<slug>/ when not told, which is right
    far more often than not and is at least a claim that can be checked. `verify`
    re-scores every recorded entry against its stored render and reports drift.
    """
    q = _load()
    if slug not in q["items"]:
        print(f"unknown slug {slug}"); return
    score = float(score)
    if render is None:
        d = os.path.join(ROOT, "out", "versions", slug)
        pngs = sorted((os.path.getmtime(os.path.join(d, f)), f)
                      for f in os.listdir(d) if f.lower().endswith(".png"))             if os.path.isdir(d) else []
        render = f"out/versions/{slug}/{pngs[-1][1]}" if pngs else None
    q["items"][slug].update(
        status="done" if score <= q["accept_score"] else "attempted",
        score=score, iters=int(iters), note=note, render=render)
    _save(q)
    ok = "ACCEPTED" if score <= q["accept_score"] else "NOT YET (keep iterating)"
    print(f"{slug}: score {score} after {iters} iters -> {ok}")


def verify(limit=None):
    """Re-score every recorded entry against the render it claims, and report drift.

    The queue is the run's ground truth across context windows. Until `record` stored
    provenance there was no way to ask whether a number still described a file — and
    twice it did not. This makes that question one command.
    """
    q = _load()
    import importlib.util as _il
    _s = _il.spec_from_file_location("compare", os.path.join(ROOT, "engine", "compare.py"))
    cmp_ = _il.module_from_spec(_s); _s.loader.exec_module(cmp_)
    rows, n = [], 0
    for slug, v in q["items"].items():
        if v.get("score") is None:
            continue
        ref = os.path.join(ROOT, "training_samples", "reference_posters", v["file"])
        gen, assumed = (os.path.join(ROOT, v["render"]) if v.get("render") else None), False
        if not gen or not os.path.exists(gen):
            # No provenance stored (every entry before session 10f). Fall back to the
            # newest PNG in the slug's folder and SAY it is assumed — an assumed
            # comparison that surfaces real drift is worth far more than "unknown",
            # and this is exactly how two wrong scores were caught by hand.
            d = os.path.join(ROOT, "out", "versions", slug)
            pngs = sorted((os.path.getmtime(os.path.join(d, f)), f)
                          for f in os.listdir(d)
                          if f.lower().endswith(".png")) if os.path.isdir(d) else []
            if not pngs:
                rows.append((slug, v["score"], None, "no render on disk")); continue
            gen, assumed = os.path.join(d, pngs[-1][1]), True
        if not os.path.exists(ref):
            rows.append((slug, v["score"], None, "reference missing")); continue
        try:
            got = cmp_.compare(ref, gen)["score"]
        except Exception as e:
            rows.append((slug, v["score"], None, f"scoring failed: {e}")); continue
        drift = abs(got - v["score"])
        tag = "ok" if drift <= 0.01 else f"DRIFT {got - v['score']:+.3f}"
        if assumed and tag != "ok":
            tag += " (render assumed: newest on disk)"
        rows.append((slug, v["score"], round(got, 3), tag))
        n += 1
        if limit and n >= limit:
            break
    bad = [r for r in rows if r[3] != "ok"]
    for slug, was, now, what in rows:
        if what != "ok":
            print(f"  {slug}  recorded {was}  now {now}  -> {what}")
    print(f"verified {len(rows)} recorded entries; {len(bad)} need attention")
    return rows


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
    elif cmd == "record": record(*sys.argv[2:7])
    elif cmd == "verify": verify()
    elif cmd == "fail": fail(sys.argv[2], " ".join(sys.argv[3:]))
    else: print(__doc__)
