# 2. Two Workflows

There are exactly two ways to make a poster, and they use different code paths. Do not mix them.

| | **A. Fresh generation** | **B. Reference recreation ("training")** |
|---|---|---|
| Goal | make a NEW AQ poster for real content | reproduce a specific reference layout, learn from the gap |
| Code path | `engine.generate(...)` (the ARCHETYPES registry in `engine/engine.py`) | a **bespoke script** built directly from `core`+`build`+`doodles`+`layout` primitives — **never** `engine.py`'s ARCHETYPES |
| Input | intent + archetype + content dict + accent index | a full written composition description of the reference |
| Output | `out/<name>.png` | `out/versions/<slug>/vN.png` (versioned, iterated) |
| Ends when | looking gate passes | render matches the reference element-by-element; outcome logged |

Both workflows are gated by §3 (looking) and §7 (the automated checks). Both feed §8 (encode fixes).

## See also
- [[03 The Looking Gate]]
- [[07 The Gate Stack]]

[[Manual Index]]
