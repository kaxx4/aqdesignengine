# VOICE — the AQ marketing voice system across verticals

Status: **specification, not yet encoded.** This is the written spec for `engine/copy.py`
(the COPYWRITER component, `GENERATION_MAP.md` §[2], still unbuilt). Nothing here runs yet.
Sign off on the writing first; §11 lists what encoding it will require.

Supersedes the two thin voice notes it was built from:
- `DECISIONS.md` §Voice (4 rules)
- `ENGINE.md` §VOICE (1 line)

Both are folded into §1 below and should be replaced by a pointer to this file once approved.

---

## 0. WHY THIS IS A SYSTEM AND NOT A LIST

Today the engine has exactly one voice: an 8-line `snark` bank in `engine/engine.py:35`
("cv? never met her", "run by literal teenagers"). It is a good voice. It is also the *only*
voice, so a corporate CSR deck and a stray-dog feeding drive come out sounding identical, and
`ENGINE_STATE.md` already records the consequence: exact wording repeats across the 44-sample batch.

We are extending along four axes:

| Axis | Question it answers | What it controls |
|---|---|---|
| **LANE** | what is this about? | the nouns, the verbs, what counts as proof |
| **AUDIENCE** | who is being addressed? | the register ceiling, who "we" and "you" are, the ask |
| **CHANNEL** | where does it land? | length, reading posture, sentence fragmentation |
| **INTENT** | what job is it doing? | tense, sentence shape, where the piece ends |

8 lanes x 6 audiences x 5 channels x 6 intents = **1,440 combinations**. That is not a bank you
can write, and a bank is what failed last time. So the architecture is:

> **ONE base voice (§1) + four modifier layers that apply deltas to it (§3-§6),
> resolved by a fixed precedence rule (§7).**

A lane does not have "its own voice." A lane supplies vocabulary. The *voice* is the base,
bent by audience, shaped by intent, and cut to length by channel.

---

## 1. LAYER 0 — THE INVARIANTS (true in all 1,440 combinations)

These never bend. Not for a corporate client, not for a government form, not for a fundraiser.

**Craft**
1. No em dashes anywhere. Ever. Use a full stop or a comma.
   (Scope: this governs AQ-facing *copy*. Internal `brain/` prose, this file included, is not
   copy and is not bound by it. The encoded scan in §11.4 must only ever run on copy strings.)
2. No emojis on graphics. Use doodles or a star glyph.
3. First names and handles only. Never a full name of a beneficiary, never a child's name.
4. Body copy and chips are lowercase. Display type is UPPERCASE. (Typographic rule, not tonal;
   the one channel that relaxes it is LinkedIn, §5.)

**Truth**
5. **Never fabricate a stat.** A number comes from the brief or it is omitted. See the truth
   ladder, §2.
6. **At least one real fingerprint per piece** — a real number, a real place, a real programme
   name, a real date. A piece with no fingerprint is a mood board, not marketing.
7. Copy must survive being held up against the photo. "Every plate, every form" on an image with
   neither is a fail, already caught once (`CAROUSEL_PLAYBOOK.md` §5).

**Stance — the part that is actually distinctive**
8. **Never preachy.** No lecture, no moral, no "we must."
9. **Never guilt-trip.** This is AQ's strongest voice signature and it was never written down.
   The corpus does it repeatedly and on purpose: "or don't. no guilt either way", "home by two,
   nobody guilt-trips you into staying", "impact as a side effect", "no minimum hours."
   Every ask must leave an easy, un-shamed exit. **An ask that closes the exit is off-voice even
   if every other rule passes.**
10. **Never savior-framed.** AQ is not rescuing anyone. The people served are people, not
    recipients of virtue. This kills the entire standard NGO register (§9).
11. **Honest-as-warmth.** Warmth comes from specificity and from admitting the unglamorous part
    ("everyone is late. we wait anyway.", "spray paint under your fingernails for a week"),
    never from adjectives about how meaningful it was.
12. **Soft CTAs only.** "pick a lane." "come once, decide after." Never "donate now", never
    "act today", never a countdown pressure line.
13. Hinglish is fine and native. Do not sanitise it out for a formal audience; just use less of it.
    Real vocabulary AQ actually uses (from `AQ_FACTS.md` §12, not invented): *yaar, ngl, lowkey,
    bhai.* Draw from this list before reaching for generic Hindi.

**The dryness**
14. The house register is dry and understated. The joke, when there is one, is always at AQ's own
    expense ("run by literal teenagers", "1,200 of us, still unhinged"), never at anyone else's,
    and never at the expense of the people served. **Self-deprecating, never other-deprecating.**
15. **The Description Ban (added 2026-08-26, source: `aq-master-brief.md` Rule 5 — a real invariant
    this file was missing entirely).** Never include a paragraph describing what AQ *is*.
    "AquaTerra is a student-run NGO where teenagers turn ideas into real projects" is the exact
    banned sentence — it appeared in 6 consecutive real carousels before being banned outright.
    **The content IS the explanation.** If a piece needs a sentence explaining what AQ is before
    the actual content lands, the content isn't doing its job yet — cut the sentence, not add
    context to it.

---

## 2. THE TRUTH LADDER (governs every number, in every vertical)

Extends the hard rule in `CLAUDE.md` §9 and the `index_tag` precedent in `CAROUSEL_PLAYBOOK.md` §6.

| Tier | Definition | May appear as | Example |
|---|---|---|---|
| **Counted** | present in the brief, someone actually counted it | a hero number, a chip, body copy | "15k meals", "534 drives", "1,200 members" |
| **Derivable** | literally true from the artefact itself | a tag, an index | "01 / 05" carousel position |
| **Scoped** | true only with its qualifier attached | only ever WITH the qualifier | "logged across kolkata in 2025" |
| **Estimated** | approximate, honestly | only with a hedge word | "around 40 of us" |
| **Fabricated** | invented to look impressive | **never, in any vertical** | "day 1/8" (real historical failure) |

A scoped number that loses its qualifier becomes a fabricated one. "534 drives" is honest;
"534 drives" implying all-time when it was 2025-only is not. **The qualifier travels with the
number or the number does not ship.**

CSR/institutional-partner content is where this ladder is under the most pressure and matters the
most — see §4. The real fact bank behind every number on this ladder is `AQ_FACTS.md`; pull real
figures from there rather than inventing plausible-sounding ones.

**Claim laundering (added 2026-08-26, adopted from external research into a comparable fact-checked
content system — see `DECISIONS.md`).** A specific failure mode worth naming: don't let a partner's
or a program's number borrow the credibility of an unrelated official source. Example: AQ's real
DARPAN registration (`AQLLMS.txt`) is a genuine, citable fact about AQ's legal status — it does
NOT make an adjacent, less-verified claim (say, a specific dollar-value "impact" figure from a
different document) equally certain just because it sits in the same paragraph. Cite each number
to its own actual source; never let one Verified-tier fact's credibility rub off on a
neighboring Scoped- or Estimated-tier one.

---

## 3. LAYER 1 — LANE (supplies vocabulary, not tone)

A lane answers: what concrete nouns, verbs and sensory details are available, and what counts as
proof that the work happened. **Lanes do not have tones.** A lane that appears to have a tone is
usually an audience assumption smuggled in.

Each lane below gives: **NOUNS** (things that appear) · **VERBS** (what people do) ·
**PROOF** (the detail that shows it was real) · **PULL** (the one register nudge the subject
matter justifies, applied in §7).

### welfare / food
- NOUNS: crates, plates, kits, the queue, the counter, dawn, hot food, sorting tables
- VERBS: sort, carry, pack, serve, hand over
- PROOF: the handover moment and the count. "handed across the counter, mid-shift",
  "one crate at a time", "every plate had a face."
- PULL: none. House register.

### climate / trees
- NOUNS: saplings, gloves, bags, the beach, the bank, Diamond Harbour, the Sundarbans
- VERBS: plant, clear, haul, sort, weigh
- PROOF: the physical unglamour and the location. "show up at 7am. we bring the gloves, bags,
  and the rest.", "beach cleanup, diamond harbour"
- PULL: none. Physical work is already dry and concrete; do not inflate it into "saving the planet."

### education
- NOUNS: books, the back row, the board, worksheets, a clipboard, the same kids
- VERBS: teach, explain, walk through, sit with
- PROOF: a specific classroom moment, never an outcome claim. "questions from the back row,
  halfway through", "a volunteer walking the class through one more example"
- PULL: **down 1.** Never joke about a child's learning. Warmth yes, wryness about the room yes,
  wryness about the kids no.
- HARD: no claim about a child's future ("changing lives", "building futures"). AQ teaches a
  session; it does not own an outcome.

### shikshaq
**Confirmed 2026-08-26 as its own distinct system, not an education sub-lane** — see `AQ_FACTS.md`
§10 for the full sourcing. Three real, shipped things education doesn't have:
- A distinct **audience**: tutors/teachers being recruited to list on the platform, not just
  students/parents using it. Real published copy addresses them directly, in a persona voice:
  "Maths Sir, beta, derivatives and trigonometry stop being scary in my class. I'll help you set
  up your Shikshaq profile."
- A distinct **visual system** `engine/core.py` does not currently encode: black background,
  orange (#FF9500/#FF9800) + blue (#5B5FFF/#5B6FFF) neon-gradient accents, a graduation-cap
  doodle, a leaf/hat logo mark, and a recurring WhatsApp-chat-bubble mockup format. Tracked as an
  open engineering gap in `GAPS.md` #5, not solved here.
- NOUNS: tutor profiles, verification, the discovery layer, WhatsApp contact, the 11-day problem
- VERBS: verify, discover, contact, list, match
- PROOF: real, sourced UX research — "11 days to under 48 hours," "50+ verified tutors,"
  zero-commission model. See `AQ_FACTS.md` §10 for the full sourced figures.
- PULL: **up 1** for tutor-recruitment content specifically (real published copy is sharper/
  funnier than the AQUATERRA-proper default — "YOUR TUITION TEACHER HAS 69 SKILLS. MAKING A
  SHIKSHAQ PROFILE ISN'T ONE OF THEM."); stays at the house default for student/parent-facing
  platform copy, which reads more like the trust-first product register in the source docs.
- HARD: never claim to employ, vet-guarantee, or take responsibility for a tutor's teaching
  quality — the platform's own terms are explicit that it handles zero payments and zero
  employment relationships and accepts zero liability for outcomes (`AQ_FACTS.md` §10).

### roots (apparel venture — NOT the same as the "clothes/kits" lane below)
**Added 2026-08-26** — the ingestion surfaced a real distinction the original lane list conflated.
ROOTS is AquaTerra's apparel brand (~10% of org revenue, sold merchandise), not the donated-
clothing welfare lane.
- NOUNS: the drop, the tag ("Made to give back"), the fabric, the print run
- VERBS: wear, fund, design, sell
- PROOF: real production photography exists (kraft-paper tags, flat-lay merchandise shots) — use
  it as reference for what "real" looks like here, same real-assets rule as everywhere else.
- PULL: open question — see `GAPS.md` #6. "Apparel that's more of a voice rather than fashion" is
  a real positioning line (`AQ_FACTS.md` §11) that suggests ROOTS may want its own register
  distinct from general AQUATERRA content, not yet resolved.

### animal welfare
- NOUNS: strays, feeding rounds, bowls, the gate, paws
- VERBS: feed, treat, walk, sit with
- PROOF: the routine and the specific animal. Named animals are allowed where named people are not.
- PULL: **down 1.** The corpus temptation here is cutesiness. Stay dry; a dog does not need a
  caption doing a voice for it.

### health
- NOUNS: camps, forms, blood pressure, sugar, eyes, the doctors, the register
- VERBS: check, log, screen, register
- PROOF: the admin reality. "logging patient details by hand, one form at a time",
  "doctors who gave their day"
- PULL: **down 1.** Health data is somebody's body. Zero snark on the patients. Snark on AQ's own
  paperwork is fine.
- HARD: never imply diagnosis, treatment or cure. AQ runs screenings. "free health checkups in
  communities that don't get them" is the ceiling of the claim.

### clothes / kits
**Not the same as ROOTS (below).** This lane is donated, collected clothing distributed as
welfare (real figure: 2,500kg / 2.5 tons collected and donated, `AQ_FACTS.md` §2) — a welfare
activity, zero revenue. ROOTS is a sold apparel brand. Confirmed distinct 2026-08-26; the original
spec had conflated them.
- NOUNS: winter clothing, school kits, racks, sizes, the drive
- VERBS: collect, sort, size, distribute
- PROOF: the sorting labour, which is the invisible half. "kit racks and brackets up"
- PULL: none.

### events / fest
- NOUNS: the floor, ladders, star curtains, the dj booth, brackets, court lines, walkies, the
  balloon drop, sound check, merch
- VERBS: build, rig, call, run, tear down
- PROOF: the build, not the party. "a 500-person floor that you built that morning",
  "a crew that texts at 2am about balloon counts"
- PULL: **up 1.** This is the one lane allowed to be loud. It is also the lane most likely to
  drift into hype, so the proof rule matters more here: show the ladder, not the confetti.

---

## 4. LAYER 2 — AUDIENCE (sets the register ceiling and the ask)

This is the axis that actually changes how AQ sounds. It defines a **register ceiling** on the
0-4 ladder, a **snark budget** (max wry chips per piece), who "we" and "you" are, and what
counts as proof to that reader.

**The register ladder**
```
0  flat-factual      dates, counts, no colour
1  plain-warm        clear sentences, human, no jokes
2  dry               understated, specific, no jokes
3  dry + wry         HOUSE DEFAULT. one aside per piece
4  loud              playful, exclamatory, events-only
```

| Audience | Ceiling | Snark budget | "we" = | "you" = | Proof they need |
|---|---|---|---|---|---|
| general followers | 4 | 2 | AQ, casually | anyone scrolling | the scene itself |
| volunteers / recruits | 4 | 2 | your future crew | a peer | what the day feels like |
| tutors / teachers (Shikshaq only) | 4 | 2 | the platform, casually | a working tutor | the friction the platform removes |
| schools / parents | 2 | 0 | supervising adults | a guardian | safety, supervision, specifics |
| corporate / CSR | 1 | 0 | a reliable delivery partner | a partner with a mandate | scale, reliability, documentation |
| government / institutional | 0 | 0 | a registered organisation | an official | counts, dates, coverage |

**"donors" removed 2026-08-26 — see below.** The row this table used to have for individual
donors is gone, not renamed. AquaTerra runs on 0% individual donations by explicit, stated
organizational policy (`AQ_FACTS.md` §8) — the audience that row was built for does not exist as
a real AQ practice. What remains in its place is corporate/CSR (already in this table, now backed
by a real sent proposal instead of an invented register) and the new tutors/teachers row, which
Shikshaq's real published recruitment copy proves is a distinct persona the base system never
modeled.

### volunteers / recruits — the home audience
The corpus is almost entirely this. Barrier-removal is the whole move: "no cv needed", "no fee,
no cv", "no experience needed, no fee, ever.", "no minimum hours. pick a lane, come once, and
decide after."
- **HARD RULE: never ask a volunteer for money.** The corpus states it outright: "nothing, in
  either direction. we do not fundraise from you." Volunteer-facing and CSR-facing copy do not
  mix on one piece. If a brief asks for both, that is two pieces.
- **The real value proposition, confirmed 2026-08-26 (`AQ_FACTS.md` §12, source:
  `AquaTerra_Customers.md`), goes deeper than barrier-removal:** "AquaTerra is built for students
  first; social impact is created through them, not just for others." The real, stated draws are
  certificates, leadership roles, documented work experience, a social outlet, and real
  responsibility/ownership — "learning happens through doing, not structured teaching." Recruit
  copy can lean on this directly: the pitch isn't only "no barriers," it's "here's what you
  actually get" — CV-worthy execution experience and a peer community, with impact as the
  byproduct, not the headline. This is a genuine reversal of the standard NGO recruitment pitch
  (impact-first, incidentally-yours-too) and it's worth writing to deliberately.

### tutors / teachers — Shikshaq-only, added 2026-08-26
A persona the original spec never modeled, found only because real published Shikshaq
recruitment copy addresses tutors directly, by role, in a chat-style format: "Maths Sir, beta,
derivatives and trigonometry stop being scary in my class. I'll help you set up your Shikshaq
profile." "Chemistry Ma'am... How about I walk you through Shikshaq?"
- The ask is specific and low-friction: list a verified profile, get discovered, keep 100% of
  earnings (Shikshaq is zero-commission — a real, checkable fact, `AQ_FACTS.md` §10).
- Register runs slightly hotter than the AQUATERRA house default for this one persona — real
  shipped copy is genuinely playful/cheeky ("YOUR TUITION TEACHER HAS 69 SKILLS. MAKING A
  SHIKSHAQ PROFILE ISN'T ONE OF THEM."), closer to register 4 than the general default of 3.
- Never imply Shikshaq vets teaching quality or takes responsibility for outcomes — its own terms
  are explicit that it's connection-only (`AQ_FACTS.md` §10).

### corporate / CSR — confirmed 2026-08-26 against a real sent proposal
Ceiling 1 means **no jokes at all**, and this is the only place lowercase-everything starts to
cost credibility. This section was originally a proposed register; it is now validated almost
exactly by a real document — the Emami Foundation CSR proposal (`AQ_FACTS.md` §9), which is
formal, zero-snark, zero-Hinglish, compliance-and-metrics-forward throughout.
- Keep: specificity, honest numbers, no savior framing, soft close.
- Drop: snark, Hinglish density, fragments.
- The differentiator is not that AQ is fun. It is that AQ **documents**: real counts, real dates,
  photos of the actual work, and — per the real proposal — regulatory specifics that matter to a
  CSR partner (Schedule VII pillar mapping, 80G tax benefit, DARPAN certification, 100% pro-bono
  volunteer hours, itemized use of funds). Lead with that, not with mission language.
- The real proposal's actual pitch to the partner is worth naming as a technique: the volunteer
  base itself is offered as the value-add — "1,050+ student volunteers as organic brand
  ambassadors amplifying [partner]'s CSR story on social media." A CSR piece can honestly lean on
  scale-of-reach as a benefit to the partner, not just scale-of-impact.
- Still no preachiness. A CSR deck that lectures a company about responsibility is off-voice.
- **This audience does not get a "donors" framing.** AquaTerra's real revenue model has 0%
  individual donations (`AQ_FACTS.md` §8) — CSR is an institutional B2B partnership, not an
  emotional individual ask. Do not write a CSR piece as if it were a personal-donor appeal; the
  register, the ask, and the proof are all different (see the table note above).

### schools / parents
Ceiling 2, snark 0. A parent is deciding whether their child is safe.
- Lead with supervision, timing, transport, who is present.
- Concrete beats warm: "one saturday, 7am to noon. bus provided from esplanade." is the ideal line.
- Never wry about the kids or the parents.

### government / institutional
Ceiling 0. Counts, dates, coverage, registration status. No chips, no doodle voice, no asides.
This is the one vertical where the AQ voice is almost fully suppressed, and that is correct.

---

## 5. LAYER 3 — CHANNEL (sets length and posture, never tone)

| Channel | Budget | Posture | Shape |
|---|---|---|---|
| **feed poster** | hero 3-7 words · 1 band · 1-2 chips · body ≤ 14 words | glanced, then read | fragments. one hero thought, one proof, one aside |
| **story** | 1 line, ≤ 8 words | thumb-speed, gone in 3s | one thought. no body copy. the CTA is the tap |
| **carousel slide** | caption ≤ 12 words · 1 sticker | sequential, committed reader | slide 1 hooks, middles are scenes, last one asks |
| **reel** (video) | zero on-screen AQ mentions, zero CTA | pure entertainment, no conversion job | see hard rule below — this channel breaks the normal pattern entirely |
| **linkedin** | 40-120 words | professional feed, sentences expected | **the one place sentence case is allowed.** full sentences, no chips, no doodle voice |
| **whatsapp / email** | 30-80 words | direct, one-to-one | address a person, make one real ask, sign it with a first name |

Rules:
- **Channel never raises the register ceiling.** A story is shorter, not louder. Events lane at
  ceiling 4 is loud on a story because of the lane, not the channel.
- **Carousels earn a narrative arc the other channels cannot have.** Use it: hook, scenes, ask.
  Each middle slide describes its own photo (§1.7), never a generic mood word.
- **LinkedIn is the only sentence-case exception** and it is a legibility concession, not a
  register change. The stance rules (§1.8-14) are unchanged. It is still not preachy, still not
  savior-framed, still does not guilt-trip.

**Reel is a real, distinct channel with its own hard rules (added 2026-08-26, source:
`aq-master-brief.md` §8) — do not treat it as "a short story" or "a small carousel."**
1. Zero AQ mentions on-screen — no text overlay saying "AquaTerra," "register," "join," "apply."
2. Zero CTAs in the video itself — no "link in bio," no "follow us."
3. No preachy or inspirational messaging of any kind.
4. AQ exists only in the caption's account tag and the profile the reel posts from.
5. **The test:** if the reel could be posted by any random funny student account and still work,
   it passes. If it couldn't, it's not a reel yet.

This is not a softer version of the other channel rules — it is close to their opposite. A reel's
only job is top-of-funnel discovery (a stranger laughs, checks the profile); the profile and the
carousels behind it do the actual converting. Writing "AQ voice" into a reel script the way you
would a caption is a category error for this channel specifically.

---

## 6. LAYER 4 — INTENT (sets tense and sentence shape)

| Intent | Tense | Shape | Ends on | House example |
|---|---|---|---|---|
| **recruit** | present / imperative | remove a barrier, then invite | an easy exit | "pick a lane. come once, decide after." |
| **partner (CSR)** | present | map real capability to the partner's compliance needs, then the proof | the ask to talk | "five pillars, one partner. here's what we've already delivered." |
| **recap / report** | past | count it, then name who did it | attribution | "logged by the volunteers who did it." |
| **awareness** | present | state the fact flat, then a scene | the scene | fact, then the room it happens in |
| **gratitude** | past | name people, never abstractions | the people | "doctors who gave their day" |
| **announcement** | future | date, place, time, one line of what | the logistics | "one saturday a month, 7am to noon" |

Notes:
- **"fundraise" renamed "partner (CSR)" 2026-08-26.** AquaTerra runs 0% individual donations by
  stated policy (`AQ_FACTS.md` §8) — there is no real individual-giving intent to write for. The
  intent that exists is a CSR partnership pitch, shaped like the real Emami proposal: map AQ's
  actual programs to the partner's compliance pillars, then prove delivery. "One kit. one child,
  one term." (the old house example) was an invented individual-donor line — the real equivalent,
  grounded in the actual proposal, is closer to "five pillars, one partner. here's what we've
  already delivered."
- **awareness is the highest-risk intent.** It is the one that pulls hardest toward preaching,
  because there is no action to describe. The rule: state one fact without adjectives, then cut
  immediately to a concrete scene. If the piece has no scene, it has no business being awareness.
- **gratitude must name.** "thank you to our volunteers" is abstraction. "doctors who gave their
  day" is a person. First names and roles only (§1.3).
- **recap must attribute.** AQ counts things and then says who did them. This is the anti-savior
  invariant in operational form.

---

## 7. COMPOSITION — how the four layers resolve

Applied in this order. Each step constrains the next, mirroring the decision cascade in `TASTE.md`.

```
1. AUDIENCE  sets the register CEILING and the snark budget      (hard cap)
2. LANE      applies its PULL (+1 / -1) to the house default 3   (subject-matter nudge)
3. REGISTER  = min(audience_ceiling, 3 + lane_pull)              (the cap always wins)
4. INTENT    picks the tense and the sentence shape              (structure)
5. CHANNEL   cuts it to length                                   (budget)
6. LANE      fills the nouns, verbs and proof detail             (vocabulary)
7. INVARIANTS (§1) are checked last and override everything      (veto)
```

**The precedence rule, in one line:**
> Audience sets the ceiling. Intent sets the shape. Lane fills the nouns. Channel sets the length.
> Invariants veto.

Worked resolutions:

| Brief | Audience ceiling | Lane pull | Register | Result |
|---|---|---|---|---|
| events recap, general followers | 4 | +1 (events) | **4** | loud, playful, 2 chips |
| events recap, corporate CSR | 1 | +1 (events) | **1** | plain. the ceiling wins. describe the build, no jokes |
| health camp, volunteers | 4 | -1 (health) | **2** | dry, no snark on patients, snark allowed on AQ's own forms |
| food drive, government | 0 | 0 | **0** | counts, dates, coverage. no voice |
| education, parents | 2 | -1 (education) | **2** | warm, concrete, supervision-led, zero wryness |

Note the second row. That is the whole point of the precedence rule: the loudest lane in the
system, addressed to the most formal audience, comes out formal. The lane still changes what the
piece is *about* (ladders, sound check, the 2am texts) but not how loud it is.

**Conflicts that resolve to "this is two pieces, not one":**
- volunteer recruitment + donation ask (§4 hard rule)
- a child's photo + a fundraising number on the same frame (savior framing, §1.10)
- gratitude + recruit (thanking people while asking for more is a guilt lever, §1.9)

---

## 8. THE FINGERPRINT REQUIREMENT, PER LANE

Invariant 6 requires at least one real fingerprint per piece. What qualifies:

| Lane | Valid fingerprints |
|---|---|
| welfare / food | meals counted, the location, the drive date, "one crate at a time" |
| climate / trees | saplings counted, Diamond Harbour, the Sundarbans, the 7am call time |
| education | the centre name, the term, the session count |
| animal welfare | the feeding round, the area, a named animal |
| health | camps run, checkups conducted, the doctors present |
| clothes / kits | kits distributed, the season, the collection point |
| events / fest | floor count, team count, the venue, the date |

Never a fingerprint: a percentage with no source, a "lives changed" figure, a growth claim,
a comparison to another organisation.

---

## 9. THE DO-NOT-SAY LIST

**Sector boilerplate — banned in every vertical, including corporate and government.**
This list exists because it is exactly what a generic model reaches for, and every entry
violates §1.8 (preachy) or §1.10 (savior).

> make a difference · be the change · give back · change lives · touched lives · lend a hand ·
> helping hands · underprivileged · less fortunate · needy · voiceless · beneficiaries ·
> empowering the · uplift · noble cause · God's work · heartwarming · heart-melting ·
> tears in our eyes · restore your faith in humanity · they had nothing but gave everything ·
> smile that says it all · together we can · join hands · be a hero · every child deserves

**Mechanically banned (§1.1-1.2, already gate-able):**
> em dashes · emojis on graphics · exclamation stacks · ALL CAPS body copy · countdown urgency

**Banned for AQ specifically:**
- Any jab at another organisation. Self-deprecating only (§1.14).
- Any claim of outcome AQ does not own: cured, educated, lifted out of, transformed.
- Any minimum, guilt or obligation framing: "the least you can do", "just one hour of your time".
- Full names or faces of children attached to a need. (Also a repo-level rule.)
- "Volunteer with us and get a certificate" as the lead ask. The corpus is explicit that AQ is
  not a CV exercise, and leading with the certificate contradicts "cv? never met her."

**AI-tell scrub — mechanical, two-tier, added 2026-08-26** (adopted from external research into a
current Instagram-focused content-skill repo; see `DECISIONS.md` for the source). This is a
pre-publish pass, distinct from voice/tone — it catches copy that reads as machine-generated
regardless of whether it otherwise obeys every rule above.
- *Forensic tier (delete on sight):* leaked model markers, unfilled template blanks like
  `[Your Name]`, 3+ em dashes in one piece (redundant with invariant 1, but explicitly a forensic
  tell on its own).
- *Strict tier — vocabulary blacklist:* leverage, utilize, delve, harness, elevate, unlock,
  robust, seamless.
- *Strict tier — dead phrases:* "in today's fast-paced world," "game-changer," "deep dive."
- *Strict tier — dead closers:* "what do you think?," "double tap if," "comment YES," "tag 3
  friends," "repost if..." — these are also, independently, manipulative-engagement patterns
  Instagram itself downranks; banning them serves both the voice and the reach.
- *Strict tier — negative-parallelism ban:* "it's not just X, it's Y" as a sentence template.

---

## 10. WORKED EXAMPLE — one event, eight renderings

Brief, held constant: *Sundarbans health camp. 6 volunteers, 1 Saturday, 3 doctors,
checkups conducted (count comes from the brief). Bus from Esplanade, 7am to noon.*
Lane = health (pull -1). All copy below obeys §2: the only numbers used are ones the brief states.

**1. general followers · feed · recap** (ceiling 4, register 2 after health pull)
> hero: `one saturday.` / band: `three doctors gave their day.`
> body: `checkups in a village that does not get them. logged by hand, one form at a time.`
> chip: `the forms took longer than the drive`

**2. volunteers · feed · recruit** (register 2)
> hero: `come once.` / band: `bus from esplanade, 7am.`
> body: `no experience needed. you get paired on day one.`
> chip: `home by two, nobody guilt-trips you into staying`

**3. volunteers · story · announcement** (register 2, one line)
> `saturday. esplanade, 7am. bus provided.`

**4. donors · feed · fundraise** (ceiling 2, snark 1)
> hero: `one camp.` / band: `three doctors, one saturday, a village that had none.`
> body: `funding a camp covers the transport, the register and the medicines. that is the whole line item.`
> chip: `run by students, audited like it isn't`
> *(no cost figure appears because the brief did not supply one. §2.)*

**5. corporate / CSR · linkedin · report** (ceiling 1, sentence case, no chips)
> `Six volunteers ran a health camp in the Sundarbans this Saturday, with three doctors
> donating the day. Screenings covered blood pressure, sugar and vision. Every patient record
> was logged on site by hand.`
> `We publish the counts and the photographs for every camp we run. If your CSR programme needs
> documented delivery in the Sundarbans, that record is available.`

**6. schools / parents · whatsapp · announcement** (ceiling 2, snark 0)
> `Saturday's camp leaves Esplanade at 7am and is back by 2pm. Bus both ways, three doctors on
> site, and two of our coordinators travel with the group the whole day. Reply here if your
> child is coming and we will add them to the list. - Kanishk`

**7. government · feed · report** (ceiling 0)
> hero: the checkup count / band: `sundarbans, [date]`
> body: `blood pressure, blood sugar and vision screening. three registered practitioners present.`
> *(no chips, no doodle voice, no asides.)*

**8. general followers · carousel · recap** (register 2, arc)
> slide 1: `one saturday. one village. three doctors.`
> slide 2 (photo of the register): `logging patient details by hand, one form at a time`
> slide 3 (photo of the queue): `the queue started before we finished setting up`
> slide 4 (photo of doctors): `doctors who gave their day`
> slide 5 (ask): `next one is monthly. pick the saturday that fits.`

Note what does not change across all eight: no guilt, no savior framing, no invented number,
at least one fingerprint each, a soft close every time. What changes is the ceiling, the length
and the shape. That is the system working.

---

## 11. WHAT ENCODING THIS WILL REQUIRE (`engine/copy.py`)

Not built. Scoped here so §12 sign-off covers the plan, not just the prose.

1. **`VOICE_PROFILE(lane, audience, channel, intent) -> profile`** — pure resolution of §7:
   returns register int, snark budget, tense, sentence shape, length budgets, noun/verb/proof banks.
   No text generation. Deterministic, trivially unit-testable.
2. **Slot grammars, not banks** (`GENERATION_MAP.md` §[2]) — kicker / hero / label / chips / band /
   body per archetype, filled from brief nouns crossed with lane vocabulary. This is what stops the
   ~10-post repeat cycle.
3. **`banned_phrase_scan(text)`** — §9 as a hard gate. Zero false positives, so it can auto-run in
   `build.render()` alongside `css_var_check`. This one is cheap and should ship first.
4. **`em_dash_scan` / `emoji_scan`** — §1.1-1.2, mechanical, also auto-gate.
5. **`number_provenance_check(text, brief)`** — §2. Any digit in the copy must trace to a brief
   field or the derivable set. **This is the highest-value gate in the whole spec** and the one
   that most needs a self-test reproducing the historical "day 1/8" failure.
6. **`register_check(text, profile)`** — advisory only. Detecting tone by rule is unreliable;
   it flags for the looking gate rather than blocking, in line with the CLAUDE.md §8 rule that a
   noisy check must never sit in the auto-gate.
7. **Ledger integration** (`GENERATION_MAP.md` §[5]) — reject any phrase used in the last N pieces.
   Voice variety and visual variety are the same problem and want the same ledger.
8. **Self-test** — `scratchpad/test_voice.py`, per CLAUDE.md §8.3: every assertion reproduces a
   real failure. Seed cases: the "day 1/8" fabrication, a volunteer piece carrying a donation ask,
   a corporate piece carrying a snark chip, an awareness piece with no scene.

Build order: gates 3-5 first (mechanical, high value, independent), then 1, then 2 with the ledger.

---

## 12. OPEN QUESTIONS — now tracked centrally in `GAPS.md`

This section listed six questions as of first draft. A real content-ingestion pass on
2026-08-26 (see `AQ_FACTS.md` and `DECISIONS.md`) resolved four of them with sourced facts rather
than guesses — full resolutions are in `GAPS.md`'s RESOLVED section, summarized here:

1. ~~Two competing lane taxonomies~~ — **resolved.** Neither list was fully right; `AQ_FACTS.md`
   §1-11 is the real, sourced lane/fact bank, and it surfaces two lanes neither prior list had
   cleanly separated (ROOTS vs. the welfare "clothes/kits" lane — see §3 above).
2. ~~Is Shikshaq a separate voice~~ — **resolved, yes**, on three independent grounds. See §3
   above and `AQ_FACTS.md` §10.
3. ~~The donor register is largely invented~~ — **resolved by removal.** There is no donor
   audience to write for; see §4's note and `AQ_FACTS.md` §8.
5. ~~Does AQ take individual donations at all~~ — **resolved, no, by explicit stated policy** —
   0% of revenue, `AQ_FACTS.md` §8.

Still genuinely open — see `GAPS.md` #3-4 for the live tracking:
4. **LinkedIn, WhatsApp and email have zero precedent** in the ingested corpus. Every rule in §5
   for those three is still invented. If real copy on those surfaces turns up, it should drive
   the rules instead.
6. **Sentence case on LinkedIn** — still an unforced legibility concession, no precedent found
   either way.

---

## 13. SEE ALSO — this file's place in the tree

- **Hub:** `CONTENT_SYSTEM.md` — indexes this file alongside every other surface; its §1 spine
  diagram is where `VOICE_PROFILE` (§7 here) sits relative to brand tokens and the gate stack.
- **Feeds into:** `IDEATION.md` §5 step 7 calls `VOICE_PROFILE` directly as part of resolving a
  brief; `IDEATION.md` §7 (LinkedIn) and `BROCHURE_CATALOG.md` §4/§7 both apply this file's
  audience ceilings (§4) to their own formats rather than restating them.
- **Built precedent:** `CAROUSEL_PLAYBOOK.md` §5 ("sticker copy must describe THIS photo") and §6
  ("never let a sticker/tag invent a fact") are the truth-ladder (§2) and fingerprint rule (§1.6)
  already operating in shipped code — this file generalizes what that playbook does by hand.
- **Shares its resolution logic with:** `TASTE.md`'s decision cascade (§7's precedence rule —
  audience caps, intent shapes, lane fills, channel cuts, invariants veto — is the same "each
  choice constrains the next, don't hedge" structure `TASTE.md` uses for visual composition).
- **Fixes discovered while using this file** log in `DECISIONS.md`, per `CLAUDE.md` §8 — not a
  new changelog here.
- **Evidence spine:** `AQ_FACTS.md` — every real number, real quote, and sourced claim this file
  now cites traces back to that file, ingested 2026-08-26 from AQ's actual strategy docs, CSR
  proposal, and published posts. Pull real figures from there; don't invent plausible ones.
- **Open questions:** `GAPS.md` — the live, centrally-tracked version of §12 above.
- **Standing practice, added 2026-08-26:** re-ground this file against real published/internal
  copy periodically, not just once. The 2026-08-26 ingestion is the first instance of this
  practice (adopted from external research into how a comparable voice system re-derives style
  from real samples rather than only prescriptive rules — see `DECISIONS.md`); repeat it
  whenever a meaningful amount of new real content exists to check this file's rules against.
