# DESIGN SYSTEMS THINKING (validated framework — now the engine's operating model)

The core competency is NOT graphic-design flair but SYSTEMS THINKING: every placement + color justified by a quantifiable metric. Structure is the primary constraint layer; style serves it.

PIPELINE (enforced order — Phase II):
1. STRUCTURE FIRST: establish ACC-compliant grid + slots + roles BEFORE placing pixels. (compose.py generates the ruleset.)
2. CONTENT MAPPING: map semantic content into slots; magnify the most critical item to hit VDR target. Every layout has a HERO slot.
3. STYLING LAST: apply functional palette + tokens to serve the structure, never dictate it.

METRIC GATES (metrics.py — measure every piece, treat like the collision auditor):
- ACC (alignment consistency) target >0.80 — edges snap to grid/margin, no arbitrary drift.
- VDR (visual dominance ratio) target 0.06–0.20 — ONE hero clearly leads; <0.05 = no hero (weak), >0.22 = headline swallows piece.
- Type scale ratio >4x — clear TITLE/SUB/BODY hierarchy.
- Flow >0.7 — focal in natural entry zone; balance by MASS not symmetry (dense text balanced by one big graphic).
- FUNCTIONAL SATURATION: high-saturation accents reserved for CTA/action/key elements; neutrals (cream/ink) for structure + body. Don't spray accents randomly — they signal action.

Measured baseline: pixel-first pieces drifted (NB_starry VDR 0.23 over; PX_mershe 0.025 under). Structure-first CMP_heroanchor hit ACC 0.85 / VDR 0.159 / scale 10.7x / flow 0.85 — all green. => structure-first is the standing method.

## See also
- [[Decisions Index]]
- [[Doodle-badge dropped over text or shape]]
