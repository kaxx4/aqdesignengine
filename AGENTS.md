# AQ POSTER ENGINE — read `CLAUDE.md`

**The operating manual is [`CLAUDE.md`](./CLAUDE.md). Read it now, in full, before doing
anything in this repo.** This file is a pointer, deliberately. It is not a summary, and
there is nothing here that is not there.

---

## Why this file is four lines instead of four hundred

It used to be a full second copy of the manual, and it drifted. By 2026-09-20 it was
frozen somewhere before session 10: it still taught `M = 48` (the real constant is 64),
still showed a `render()` call that silently disables the entire measured gate tier,
still claimed "all 44 references processed" against a 74-item queue, still cited test
counts from a suite less than a third its current size, and knew nothing at all about
`measure_text`, `measure_dom`, `scatter_solve`, the style bank, `design.py` or Workflow C.

It also carried the same dead `os.chdir` path that broke two agents in session 10e —
because that fix was applied to CLAUDE.md, and nobody remembered there was a second copy.
Three documents held that broken template; one got fixed.

None of that was noticeable from the inside. A model whose harness reads `AGENTS.md` by
convention got a confident, authoritative, four-sessions-stale manual that contradicted
the real one, with no indication anything was wrong. That is worse than a file which is
merely missing: a loud failure gets fixed, a silent one gets followed.

So: one source of truth. If you are adding guidance, add it to `CLAUDE.md`.
`scratchpad/test_repo_hygiene.py` asserts that every copy of the bespoke-script template
agrees, and executes the one in `CLAUDE.md` §6 to prove it still runs.

## The two things worth repeating here

1. **Read `CLAUDE.md` §3 — the looking gate.** Every numeric check in this repo is a
   proxy. Posters have passed the entire automated stack while visibly broken. After
   every render, open the PNG and actually look at it.

2. **On entering this repo with no other task**, run `python engine/runqueue.py next`
   and follow `brain/RECREATION_PROTOCOL.md`. The recreation run is expected to outlive
   any single context window and resumes without asking.
