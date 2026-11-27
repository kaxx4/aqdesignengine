# Shikshaq reference screens

34 full-page captures (first 9000px) of the public Shikshaq site, 390px wide (`-m`) and 1280px wide (`-d`), read on 2026-11-27.

| File stem | Route |
|---|---|
| home, browse, past-papers, results, about | `/`, `/browse`, `/past-papers`, `/past-papers/results`, `/about` |
| teacher, paper, school | `/tuition-teachers/<slug>`, `/past-papers/<id>`, `/school/<slug>` |
| maths | `/maths-tuition-teachers-in-kolkata` (the templated taxonomy landing) |
| join, faq, nf, auth, schools, subjects, contact, submit | `/join`, `/faq`, a 404, `/auth`, `/schools`, `/subjects`, `/contact`, `/submit-a-paper` |

**Provenance.** shikshaq.in sits behind a Vercel bot checkpoint, so these were read from `shikshaqkanitest`, the owner's own
test deployment (same code, same Supabase project, so the data is the live data). They show real teachers' photos and reviews:
these are REFERENCES for layout and language only. Do not reuse a person's photo or a review in a design.

**Artifacts to ignore.** The test build adds a purple "TEST BUILD, NOT LIVE" role toggle, a "PREVIEW" pill and a "DISCOVERY %"
pill. Some captures still show the pill remnants. They are not part of the design.

**Use.** Look at the matching screen before building a page or poster of that kind (`brain/SHIKSHAQ.md` section 6), measure it
(`compare.geometry`) when proportions matter, and build with `engine/shikshaq.py`. Re-capture when the site changes.
