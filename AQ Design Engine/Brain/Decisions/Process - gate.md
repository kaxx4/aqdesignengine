# Process / gate

- Every piece passes audit.py (overlap + margin gate) before shipping. Fix by measuring real free zones, not eyeballing.
- Intended overlaps (e.g. name-chip on portrait) are whitelisted in audit.py via SKIP_PAIRS.
- The engine (this folder) is the single source; samples come out of it. Export = zip this folder.

## See also
- [[Decisions Index]]
- (no direct cross-link identified)
