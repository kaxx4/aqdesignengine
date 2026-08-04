# Supporting palette now rotates WITH the hero accent, not independently of it (session 6)

User-flagged bug: every generation "looked the same" even across different archetypes and accent
choices. Root cause found: `generate()` picks ONE hero accent per call (`accent_idx`), but every
supporting color inside each archetype function — chips, doodles, corner masses, ticks, tag pills,
row colors — was a FIXED absolute index into RULES["accents"] (e.g. always accents[4] for chip 1,
always accents[5] for the doodle), regardless of which hero accent was chosen. So swapping accent_idx
only ever changed ONE element; the rest of the palette was frozen, and the piece read as "the same
design with one color swapped," not a genuinely different composition.
FIX (all 4 archetypes — number_hero, radial_orbit, giant_type, stacked_zones): every archetype now
computes `ai = RULES["accents"].index(accent)` and a helper `A(offset) = RULES["accents"][(ai+offset)%7]`,
then every supporting color reference uses `A(n)` instead of a fixed literal index. The whole palette
now rotates together with the hero choice — genuinely different color relationships per generation,
not just one swapped chip.
VERIFIED: generated the same content/archetype (number_hero, "15k meals") at accent_idx=0 vs accent_idx=3.
Before the fix this always produced blue/purple chips + orange tick regardless of hero color (confirmed
by re-reading the pre-fix code path). After: accent_idx=3 shifts chips to pink/green, tick to teal,
doodle to green, footer band to sky — a coordinated, different palette, not a reskin.
This does NOT solve the "same skeleton" problem (that needs more archetypes / genuinely different
content per generation, still pending) — it solves the narrower "same archetype looks identical even
with a different hero color" problem, which was a real and separate bug.

## See also
- [[Decisions Index]]
- [[04 Workflow A - Fresh Generation]]
