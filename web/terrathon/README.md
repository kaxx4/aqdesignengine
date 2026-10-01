# TerraThon schedule page

`schedule.html` is a standalone page (no build step). Keep the `fonts/` folder next to it.

- Content: only facts from the live sport pages (times, venues, fees, prize splits, age rule, contact) plus the user-given Mini-Fete note and the "registrations close 1 Oct" line.
- To change a time, edit it in BOTH places: the card (source of truth) and the matching `.blk` / `.rep` in the At a glance timeline (`--s`, `--e`, `--t` are hours on a 24h clock, e.g. 11.5 = 11:30).
- Progressive enhancement only: JS marks today's day (Asia/Kolkata) and powers Add to calendar. The page is complete without it.
- Registration state is static: cricket shows "Registrations closed"; pickleball and FIFA show "close 1 Oct". Update after that date.
- Fonts: NeutralFace + Eina (AQ brand). StretchPro is NOT used here; it is licensed "Free For Personal Use".
- Links are absolute to www.ngoaquaterra.com, so it can drop into that site or be previewed from disk.
