# IDEATION — the Instagram + LinkedIn post-idea engine

Status: **specification, usable by hand today; not yet encoded.** Same posture as `VOICE.md`:
sign off on the framework, then §7 scopes what `engine/ideation.py` would need to generate a
week of briefs automatically. Until then, run this manually — it is a checklist and a set of
formulas, not prose to admire.

Depends on `VOICE.md` for everything downstream of "what idea." Every idea this doc produces
still resolves through `VOICE.md` §7 (audience sets ceiling, intent sets shape, lane fills nouns,
channel sets length) before it becomes copy.

---

## 0. WHAT THIS DOC ADDS THAT VOICE.MD DOESN'T

`VOICE.md` answers "given a brief, how should it sound." This doc answers the question one step
upstream: **"what should the next 10 posts even be about."** That is a different failure mode —
`ENGINE_STATE.md` already logged the sound of the old failure ("exact wording repeats across the
44 batch"); the *topic* version of that failure is a feed that is 80% "come volunteer" posts
because that is the easiest idea to reach for, with recognition, proof-of-work, and reflection
never getting a turn.

The fix is the same shape as the voice fix: don't write ideas ad hoc, generate them from a small
number of orthogonal slots — **PILLAR × POST-TYPE × INTENT** — and enforce rotation across all
three so two weeks never look the same.

---

## 1. CONTENT PILLARS (the "what is this account even for" layer)

**Replaced 2026-08-26 with AQ's own real pillar system**, source: `AQ Content dump/aq-master-
brief.md` §7 (full text also indexed in `AQ_FACTS.md` §12). The 6-pillar system this section used
to have was built from first principles before that document's full text was available — it is
gone now, not merged, because AQ already had a complete, specific, real one with worked examples
per pillar. Read the source file directly for full pillar descriptions and example posts; this
table is the reference, not the full text.

| Pillar | Job it does for the account | Cadence weight |
|---|---|---|
| **Chaos Chronicles** ("what are we even doing?") | behind-the-scenes, the messy real process — the identity-defining pillar | 25% |
| **Impact Without Preaching** ("wait, students did this?") | real outcomes, framed as "look at this wild thing," never "look how much good we did" | 20% |
| **Member Spotlights** ("who even are these people?") | real people, real stories — the most under-leveraged asset per the source doc | 20% |
| **Skill Flex** ("you didn't learn this in school") | unexpected real-world skills, framed as a flex, not as education | 15% |
| **Local Identity** ("Kolkata, but make it ours") | grounds AQ in Kolkata culture, weather, food, student life | 10% |
| **Soft Recruitment** ("okay but actually join") | the ONLY pillar that explicitly invites people in — deliberately the rarest | 5-10% |
| **Culture + Takes** ("the internet is broken") | trending-format adaptations, hot takes — exists purely for reach, 48-hour shelf life | 5% |

A pillar is not a `VOICE.md` lane — it's a higher-level bucket any lane can sit inside. A
tree-planting drive can be Chaos Chronicles or Impact Without Preaching; the lane (climate) stays
the same, the pillar changes what job the post does for the account.

**The sharpest correction from this real system:** recruitment is the *rarest* pillar (5-10%),
not a headline one — the source doc calls this "the anti-recruitment principle": make joining
feel like discovering a secret, never a form submission. The earlier invented version of this
table had a RECRUIT-equivalent pillar at 20%, roughly triple the real weight. If a task leans
recruitment-heavy by default, that's a bias to actively correct against, not a neutral choice.

The weights are a rotation target, not a quota to hit exactly. Their point is structural: **if
four of the last five posts were Soft Recruitment, the next one cannot be** — doubly true now
that the real weight for that pillar is 5-10%, the smallest on the list. This mirrors `TASTE.md`
Test B ("two pieces in a row sharing a skeleton = failure") applied to pillar instead of archetype,
and it's also just restating the source doc's own Rule 4 (`AQ_FACTS.md` §12): the One-Time Rule,
which for carousel-level phrasing specifically is an absolute one-carousel cooldown, not a
5-post rolling window — stricter than this section's general rotation rule below.

---

## 2. POST-TYPE TAXONOMY (the "what shape is this post" layer)

Each type lists: what it needs as raw material, which pillar(s) it usually serves, and which
`VOICE.md` intent it resolves to.

| Post type | Needs | Usual pillar | VOICE intent |
|---|---|---|---|
| **recap** | photos + a real count from the event | PROOF | recap/report |
| **announcement** | date, time, place, one line of what | RECRUIT | announcement |
| **milestone / counter** | a real cumulative number crossing a threshold | PROOF, TRANSPARENCY | recap/report |
| **behind-the-scenes** | one process photo (the sorting table, not the event) | CULTURE, TRANSPARENCY | awareness |
| **spotlight / gratitude** | a first name, a role, what they actually did | PEOPLE | gratitude |
| **myth-bust / FAQ** | a real question AQ actually gets asked | RECRUIT, TRANSPARENCY | awareness |
| **listicle** | 3-6 real, distinct items (lanes, ways to help, roles) | RECRUIT | recruit |
| **day-in-the-life** | a photo sequence from one volunteer's actual day | CULTURE, PEOPLE | awareness |
| **before/after** | two real photos of the same thing, honestly labelled | PROOF | recap/report |
| **poll / question** | a genuine question AQ wants the answer to | VOICE-ONLY, CULTURE | awareness |
| **partner spotlight** | a real partner name + what they actually provided | TRANSPARENCY, PEOPLE | gratitude |
| **voice-only line** | one dry observation, no event attached | VOICE-ONLY | awareness |

**Hard rule inherited from `VOICE.md` §1.7 and §2:** every "needs" column entry must be real. A
myth-bust post answering a question nobody asked is a fabrication the same way an invented stat
is. If the raw material doesn't exist yet, the post doesn't get made yet — it goes on the
**wishlist** (§6) instead of getting invented.

---

## 3. HOOK FORMULAS, BY INTENT

First-line patterns, not scripts — each still has to clear `VOICE.md` §9 (do-not-say) and the
truth ladder (§2 there). These are shapes, fill them from the real brief.

**recruit**
- "no [barrier]. no [barrier]. [one honest condition]." → "no cv. no fee. one saturday a month."
- "[verb]. that's the ask." → "show up. that's the ask."
- "[N] lanes. pick one." (only if N is real)

**recap / report**
- "[one number]. [what it was for]." → "15k meals. one queue, sorted by hand."
- "[past-tense scene], and then [the unglamorous part]." → "the queue started before we finished
  setting up."

**gratitude**
- "[first name/role] [did the specific thing]." → "three doctors gave their day."
- never "thank you to..." as the opener — that's abstraction (`VOICE.md` §6 note)

**awareness**
- "[flat fact]. [immediate cut to a scene]." → the fact never gets an adjective; the scene does
  the emotional work

**announcement**
- "[date]. [place]. [time]. [one line of what]." — logistics-forward, no hype language

**myth-bust**
- "\"[the actual thing people say]\" — [the honest correction, dry, not defensive]"

**milestone**
- "[the number] just happened." then one line of what it took, never a self-congratulation
  adjective ("amazing", "incredible") — the number is the celebration, invariant §1.11

---

## 4. ROTATION RULE (the variety gate)

Track the last 10 posts as a list of `(pillar, post_type, lane)` tuples. Before finalising the
next idea:

1. **No pillar may appear more than 4 times in the last 10.** If it would, force a different
   pillar even if the "obvious" idea for this week's material is off-pillar.
2. **No exact `(post_type, lane)` pair repeats within 5 posts.** A recap-of-a-food-drive and a
   recap-of-a-tree-drive are fine back to back; two recap-of-a-food-drives are not.
3. **VOICE-ONLY runs at least once every 10 posts**, deliberately, even when there's plenty of
   "real" content queued — it's the pillar most likely to get starved by urgency, and it's the one
   that makes the account read as a personality instead of a newsletter.
4. This is the same enforcement mechanism `GENERATION_MAP.md` §[5] specs for the visual ledger
   (`GENERATION_LEDGER.json`) — when that's built, pillar/post-type/lane should be additional
   columns on the same ledger row, not a second system.

---

## 5. THE BRIEF GENERATOR (idea → renderable brief, one pass)

Given a piece of raw material (an event happened, a milestone was hit, someone wants a LinkedIn
post), resolve in this order:

```
1. LANE       — what is this actually about?            (VOICE.md §3)
2. PILLAR     — what job should THIS post do, given the rotation state?  (§1, §4 above)
3. POST-TYPE  — which shape serves that pillar with the material on hand?  (§2 above)
4. INTENT     — post-type implies it (§2 table) unless the brief overrides
5. AUDIENCE   — default general followers; override only if the brief names one  (VOICE.md §4)
6. CHANNEL    — feed / story / carousel / linkedin / whatsapp  (VOICE.md §5)
7. VOICE_PROFILE = resolve(lane, audience, channel, intent)    (VOICE.md §7 — the actual formula)
8. ARCHETYPE  — pick a poster archetype/format that fits POST-TYPE (see §5a below)
9. hook       — pull the matching formula from §3, fill from real material
10. body/chips — filled from VOICE_PROFILE's noun/verb/proof banks (VOICE.md §3, per lane)
11. fingerprint check — does this brief contain a real number/place/name?  (VOICE.md §1.6, §8)
    if not: this is VOICE-ONLY or it doesn't ship yet.
```

### 5a. Post-type → archetype/format mapping
Connects this doc to the actual render surfaces (poster engine archetypes, `GENERATION_MAP.md`'s
pending ones, and carousels per `CAROUSEL_PLAYBOOK.md`).

| Post type | Feed poster archetype | Or | Carousel? |
|---|---|---|---|
| milestone / counter | `number_hero` | | no |
| listicle | `radial_orbit` (orbit of N items) | `card_grid_board` (pending) | maybe, if >6 items |
| voice-only line | `giant_type` | | no |
| recap | — | photo-based | **usually yes** — recap is the carousel's home format |
| day-in-the-life | — | | **always** — this post-type IS a carousel by definition |
| before/after | — | `photo_card_stack` (pending) | 2-slide carousel works too |
| behind-the-scenes | — | photo-based single frame | sometimes |
| spotlight/gratitude | `stacked_zones` | | no |
| myth-bust | `giant_type` (question) | | 2-slide (question → answer) |
| partner spotlight | `stacked_zones` | | no |
| announcement | `number_hero` (date-led) or `giant_type` | | no |

Where the mapped archetype is one of the 5 still-pending ones (`GENERATION_MAP.md` §12), that
idea routes through Workflow B (bespoke script) until it's built, exactly like any other
under-covered composition.

---

## 6. THE WISHLIST (ideas blocked on missing raw material)

Ideas that are good but fail the fingerprint/reality check in step 11 don't get invented into
existence — they get parked here as a request for real material, same posture as the real-assets
rule in `CLAUDE.md` §9.

Format: `[post type] — [what's missing] — [who can supply it]`

*(empty — populate as ideas get blocked. This section exists so a blocked idea is tracked, not
silently dropped or, worse, silently fabricated.)*

---

## 7. LINKEDIN — same pillars, one different shape

LinkedIn is a channel (`VOICE.md` §5), not a separate voice, but its post *shape* is different
enough from a feed poster to spell out here.

**Structure (per post):**
1. Hook line — same formulas as §3, but as a sentence, not a fragment.
2. 2-4 short paragraphs. One idea per paragraph. No chip-speak, no doodle-voice asides.
3. One soft close — an invitation or an offer, never "link in bio" pressure language.
4. Signature: first name only, per `VOICE.md` §1.3, if it's a personal post; org voice if it's
   the AQ page.

**Which pillars actually belong on LinkedIn:**
- PROOF and TRANSPARENCY — yes, this is LinkedIn's best material (documented delivery, real
  numbers, real process). See `VOICE.md` §10 example 5 for the register.
- PEOPLE — yes, spotlight/gratitude posts translate well as short profiles.
- RECRUIT — only for skilled/leadership roles, not general volunteer barrier-removal (that post
  belongs on Instagram, where the "no cv" register lands; on LinkedIn it reads as talking down).
- CULTURE and VOICE-ONLY — **generally no.** The register ceiling for most LinkedIn audiences
  (corporate/CSR, government — `VOICE.md` §4) is 0-1, which strips the dry wit that carries a
  CULTURE post. If a CULTURE story is genuinely worth telling here, it needs to survive being
  told at register 1: specific and warm, not snarky.

**Hashtags:** none, or at most 2-3 specific ones (#Sundarbans, #Kolkata) — never a block of 10
generic ones. That register is a fabrication signal (looks like reach-gaming, not documentation)
and undercuts the "we document, we don't perform" positioning `VOICE.md` §4 gives corporate/CSR.

**Cadence:** 1-2 per week is enough. LinkedIn punishes filler more than Instagram does — a weak
LinkedIn post costs more credibility than a weak Instagram one, so the bar for "does this have a
real fingerprint" (§5 step 11) should be read strictly here.

---

## 8. WHAT ENCODING THIS WILL REQUIRE (`engine/ideation.py`)

Not built. Mirrors `VOICE.md` §11's posture — spec the plan, don't build ahead of sign-off.

1. **`IdeaLedger`** — extends `GENERATION_MAP.md`'s planned `ledger.py` with `pillar`, `post_type`
   columns alongside the existing archetype/palette ones. One ledger, not two.
2. **`next_brief(raw_material, ledger) -> brief`** — implements §5's 11-step resolution
   mechanically: reads the ledger, applies §4's rotation rule, returns a brief dict shaped exactly
   like the `content` dicts `generate.py`'s `JOBS` already use, plus `pillar`/`post_type`/`channel`.
3. **`fingerprint_check(raw_material) -> bool`** — step 11, gate. If it fails, the material is
   appended to §6's wishlist instead of producing a brief. Zero false positives needed (it's a
   presence check on brief fields, not a language model judgment) — auto-gateable.
4. **Rotation self-test** — reproduce §4 rule 1 and rule 2 as assertions against a synthetic
   10-post ledger, same pattern as `scratchpad/test_layout_rules.py`.
5. **LinkedIn is a separate render path**, not a poster — it needs no Playwright canvas, just
   the resolved `VOICE_PROFILE` and §7's structure applied to text. This is the cheapest surface
   in the whole content system to encode and should be built early.

---

## 9. OPEN QUESTIONS — now tracked centrally in `GAPS.md`

1. ~~Cadence~~ — **resolved 2026-08-26.** AQ's own 2026 Virality Plan states it directly (see §11
   below and `AQ_FACTS.md` §12): 3-5 feed posts/week minimum, 60% carousels / 25% reels / 15%
   static content mix. The 35/20/15/10/10/10 pillar split in §1 is still a proportion, not a
   volume, but it now has a real weekly denominator to apply against.
2. **Who approves before publish?** — still open, `GAPS.md` #2.
3. **Does AQ want a shared idea backlog** — still open, `GAPS.md` #1.

---

## 10. REAL AQ TECHNIQUES — grounded in the 2026-08-26 ingestion

Everything below is sourced, not invented — see `AQ_FACTS.md` §12 for the full citations. Two
real AQ documents (`aq-master-brief.md`, the 2026 Strategic Growth & Virality Plan) are AQ's own
internal content-strategy playbooks. Where this file's earlier sections (§1-9) were built from
first principles, this section defers to what AQ has already written for itself.

**80/20 proof/philosophy.** AQ's own stated content-mix ratio: 80% of content should be PROOF
(the scene, the count, the receipt) and 20% PHILOSOPHY (why AQ works the way it does). This maps
almost exactly onto this file's PROOF pillar already being weighted heaviest (§1, 35%) — the real
ratio confirms that weighting and gives it a harder number to check against.

**Real cadence and format mix:** 3-5 feed posts minimum per week; 60% carousels / 25% reels / 15%
static content. Use this as the actual denominator when applying §4's rotation rule — "no pillar
over 4 of the last 10" now has a real weekly volume it's dividing into.

**Personality-first, mission-second — a named, deliberate technique, general-audience only.** The
Virality Plan states this explicitly: "embrace the chaos on camera and bury the NGO labels until
people are already hooked on the personality." Real examples of what this produces: "we planned a
fundraiser. 14 of us showed up to set up. 3 people knew what a 'budget' was. we raised 47K. don't
ask how." / "pov: you join an ngo for the certificate and now you're managing a supply chain to
the Sundarbans." This is a genuine reversal of the standard nonprofit funnel (impact-first,
personality-incidental) and it's real AQ strategy, not a style suggestion.
- **Scope, hard:** this technique applies to the **general-followers and volunteers/recruits
  audiences only** (`VOICE.md` §4, register 3-4). It does not apply to CSR/institutional content,
  which the real Emami proposal shows behaving in exactly the opposite way — mission-and-
  compliance-forward from the first line, zero "bury the labels" energy. Applying this technique
  to a CSR piece would be a register violation, not just a style mismatch.
- Practically: a general-audience PROOF post can lead with the chaos/scene/joke and let "this is
  an NGO" arrive two sentences later, or not explicitly at all if the visual already carries it.

**Meta-principle, independently convergent with the poster engine's own philosophy.** AQ's own
master brief states: "Every rule here exists because of a real mistake." This is the copy-voice
version of `CLAUDE.md` §1's "every visual flaw you catch by eye is a rule you haven't written
yet." Two systems arriving at the same principle from opposite directions (visual craft vs. copy
voice) is a strong signal it generalizes — worth carrying forward explicitly as brief-generator
briefs get written: **a voice rule that can't point to the real mistake it prevents is a guess,
not a rule.**

**Post-type "data philosophy + never-does" pairing** (adopted from external research into a
newsletter-voice framework; see `DECISIONS.md`). Extends §2's post-type table: each post-type
should eventually carry, alongside its shape, an explicit statement of what counts as evidence for
it and a named list of its characteristic failure mode. Example for `milestone`: data philosophy
= "the number must be in `AQ_FACTS.md` or the brief, never rounded up for effect"; never-does =
"never pairs a real number with an invented percentage-growth claim." Not yet written out per
post-type — flagged as a genuine extension to build, not done here.

**Engagement-goal-first, as a second axis alongside intent** (adopted from external research into
a current Instagram hook-formula framework; see `DECISIONS.md`). Reframed for a small honest NGO,
not a growth-hacking framing: before picking a hook formula (§3), ask what you want a viewer to
*do* — save it to reference later, send it to someone who should see it, comment with a real
question, or follow for more. Then pick the container (single image / carousel / story) that
signal actually rewards, then the hook formula. This is a genuinely different selection order than
"intent first" and is offered as a second lens, not a replacement — use whichever produces the
sharper brief for a given piece of material.

**AI-tell scrub, mechanical pre-publish pass.** Every piece of copy this file's brief generator
(§5) produces should clear `VOICE.md` §9's AI-tell scrub (vocabulary blacklist, dead closers,
dead phrases) before shipping — added there, not duplicated here, since it's a copy-level gate
that applies regardless of post-type.

**What was deliberately NOT adopted** from the external research pass, and why (full detail in
`DECISIONS.md`): clickbait-style hook formulas that instruct including a metric "where possible"
even when one doesn't naturally exist; mandatory "repost if..." /  engagement-bait closers; fake
attributed "viral quotes"; vanity-metric/CAC-style growth-hacker framing applied to volunteer
acquisition. All of these directly conflict with `VOICE.md`'s truth ladder (§2) or the
never-guilt-trip invariant (§1.9) and were rejected on that basis, not overlooked.

---

## 11. SEE ALSO — this file's place in the tree

- **Hub:** `CONTENT_SYSTEM.md` — this file is one of the three docs it indexes; §4 there lists
  where LinkedIn/idea-ledger work sits in the overall build order (steps 3-4).
- **Upstream (this file calls into it):** `VOICE.md` §7's resolver is step 7 of the brief
  generator (§5 above) — this doc never invents tone or register, it only decides *what* to make.
- **Downstream (this file's output feeds these):** the poster engine (`CLAUDE.md` Workflow A/B)
  renders whatever archetype §5a maps a post-type onto; `CAROUSEL_PLAYBOOK.md` is the built home
  for every post-type marked "always/usually a carousel" in that same table.
- **Shares its variety mechanism with:** `TASTE.md`'s Test B ("two pieces in a row sharing a
  skeleton = failure") and the planned visual ledger in `GENERATION_MAP.md` §[5] — §4's rotation
  rule and §8.1's `IdeaLedger` are that same rule applied to pillar/post-type instead of
  archetype/palette, on the *same* ledger file once built, not a parallel one.
- **Pending archetypes referenced in §5a** (`card_grid_board`, `photo_card_stack`) are tracked in
  `GENERATION_MAP.md`'s build order — an idea that needs one of those routes through Workflow B
  (bespoke script) until it exists, same as any other under-covered composition.
- **Fixes discovered while using this file** log in `DECISIONS.md`, per `CLAUDE.md` §8.
- **Evidence spine:** `AQ_FACTS.md` §12 — the real AQ playbooks §10 above draws from, plus every
  sourced number usable in a fingerprint (`VOICE.md` §1.6).
- **Open questions:** `GAPS.md` — the live version of §9 above, plus two new items §10 surfaced:
  no format-mix/cadence enforcement yet (`GAPS.md` #8) and no cross-post cannibalization check
  (`GAPS.md` #9).
