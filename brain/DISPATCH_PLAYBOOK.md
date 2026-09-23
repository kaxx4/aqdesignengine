# DISPATCH — the internal roundup series

**For the internal community manager.** You collect what every team did this week, you fill in
one list, you run one command, and you get the same three things every time:

| # | What | Size | How many |
|---|---|---|---|
| 1 | WhatsApp promotional poster | 1080×1350 | **always exactly one** |
| 2 | WhatsApp message | text | **always exactly one** |
| 3 | Instagram stories | 1080×1920 | a cover + one per item |

Plus an Instagram caption for the story set or a feed crosspost.

Engine: `engine/dispatch.py`. Worked example: `scratchpad/gen_dispatch_001.py`.
Output: `out/dispatch/no01/`.

---

## 1. THE WEEKLY LOOP

```bash
PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_001.py
```

1. Copy `scratchpad/gen_dispatch_001.py` to `gen_dispatch_0NN.py`.
2. Change `issue`, `dateline`, and the `items` list. **Nothing else.**
3. Run it. Read the PNGs before you send them. Every time.
4. `out/dispatch/no0NN/copy.md` holds the message and the caption, ready to paste.

If the output looks wrong, that is an **engine bug**, not something to fix by hand in one
issue — `CLAUDE.md` §1. Open `engine/dispatch.py` and fix the rule.

---

## 2. THE BRIEF — the whole input surface

```python
BRIEF = {
    "issue":     "01",
    "kicker":    "this week at aq",     # the top-right stamp + the message header
    "dateline":  "22 sep 2026",
    "tagline":   "what's / moving",     # the masthead. "/" splits it into lines
    "cover_photo": "diwali",            # a REAL AQ photo key, or leave it out
    "handle":    "@ngo.aquaterra",
    "site":      "ngoaquaterra.com",
    "story_cta": "swipe for all five.",
    "items": [ ... ],
}
```

### Per item

| Field | Budget | Where it shows | Notes |
|---|---|---|---|
| `dept` | one of `events` `welfare` `labs` `ops` `content` | picks the colour | **not a free choice** — see §3 |
| `chip` | ≤ 3 words | poster row + story | the little label over the headline |
| `head` | ≤ 5 words | poster, story, cover index, message | rendered UPPERCASE |
| `line` | ≤ 28 words | the poster row + the IG caption | narrative, not a fragment |
| `story` | ≤ 70 words, optional | the story slide only | the long version |
| `wa` | ≤ 70 words, optional | the WhatsApp message, **only** when `wa_mode="full"` | the default message is headers only |
| `photo` | `food` `edu` `diwali` `xmas`, optional | masthead card + story band | **real AQ photos only** |

Fallback chain for the story body: `story` → `wa` → `line`. So a minimal item with just
`dept/chip/head/line` still produces a complete set.

**Max 6 items.** A WhatsApp graphic is read at thumbnail size in a group chat. Past six rows
nothing is legible and people stop opening it. Split into two issues instead.

---

## 3. WHAT THE ENGINE DECIDES, SO YOU DON'T

You are writing content. Everything below is already decided and will stay consistent across
every issue, which is the entire point of a series.

- **Colour is semantic.** `dept` picks it via `core.accent_for` — welfare=mint, events=sky,
  labs=lemon, ops=teal, content=grape, matching the website. A department that isn't in
  `dispatch.DEPTS` raises rather than defaulting to pink; adding one is a colour decision
  somebody makes once, on purpose.
- **The text is headers; the graphics carry the detail.** The WhatsApp message and IG caption
  list each item's headline and department only. The full sentences live on the poster and the
  stories for whoever wants to read them. Set `"wa_mode": "full"` in the brief for the rare issue
  that needs the long message.
- **The craft layer is applied equally.** Every item is a tinted card with an ink outline, a hard
  shadow and a department-colour badge. Pink is brand furniture (the swipe behind the accent word,
  the count burst) and never a department, so it can't be misread as one.
- **Every item is equal.** No spotlight row, no "act on this" stamp. A weekly roundup that ranks
  its own items teaches people to read one row and skip four, and it would make you decide every
  week which team gets the big treatment. The masthead is the hero; the rows are an index.
- **Type sizes are solved, not chosen.** The row solver measures your actual copy and picks the
  largest size whose stack fits. Longer items get smaller type automatically, down to a floor.
- **Contrast is measured.** Every colour pairing is checked against WCAG before it renders.
- **Nothing is invented.** No stock images, no fabricated screenshots, no made-up numbers.

### When it refuses

```
BriefError: item 3 'line' is 34 words, budget is 28 (R4). Cut it: '...'
BriefError: the 5 items do not fit the poster even at the smallest type in ROW_SIZES.
            This is a CONTENT problem, not a layout one.
```

That second one means: shorten the longest `line`, or move an item to next week. It will not
ship type nobody can read on a phone.

---

## 4. VOICE

Full system: `brain/VOICE.md`. For this series specifically:

- Audience is **volunteers / recruits** — register ceiling 4, snark budget 2, "you" is a peer.
- Intent is mostly **announcement** (date, place, one line of what) with some **recruit**.
- **No em dashes** (the validator rejects them), no emoji, body copy lowercase, display UPPERCASE.
- **Say the thing.** This is the note that matters most here, and it took a round to learn.
  A roundup exists to tell people what happened, so an item has to carry the actual information:
  who did what, where it now lives, what changes for the reader. "new spot, new vibe" over
  "both move somewhere new" is a mood, not an update. "diwali and terathon both move to a new
  venue this year, and events is now running its own page, which is live" is an update.
  **Write the second one.** The `head` can be short and punchy; the `line` under it must be a
  real sentence that stands on its own.
- **Don't perform.** The house register is dry and understated, which is not the same as clipped.
  A trailing "or don't, it will probably be fine" reads as trying too hard; drop it and just say
  there is no deadline. Understatement comes from specificity, not from withholding.
- **Soft CTAs only.** Every ask still leaves an easy, un-shamed exit — "it is worth booking a spot
  at some point rather than leaving it to the end" does that plainly. "register now, spots are
  filling fast" does not, and it is off-voice even if everything else passes.
- **Never ask a volunteer for money.** Hard rule, `VOICE.md` §4.
- **No paragraph explaining what AQ is.** The content is the explanation.
- Every number must be real. If you are not sure, leave it out.

The engine writes the *structure* of the message; you write the *sentences*. That split is
deliberate — the format never drifts, and the words stay written by someone who was in the room.

---

## 5. THE LOOKING GATE — do not skip this

The automated checks are proxies. They pass things that are visually broken. **Open every PNG
and look at it** before anything goes out (`CLAUDE.md` §3, `brain/VISUAL_REVIEW.md`):

- every word readable, nothing clipped by an edge or another element
- one clear hero; the eye knows where to land
- no dead quadrant
- dark type on light field; accents punctuate, never flood
- no collisions

The console also prints a pixel critique. Two notes on reading it honestly:

- `flat_dominant` fires on the poster because cream is more than half the canvas. Cream **is**
  the AQ ground and this format is a text index; that flag is expected here.
- `sparse` / `dead_quadrant` on the story slides is worth a second look, but the frames were
  rebuilt around an always-present bottom band precisely so no slide has a dead half. Judge it
  with your eyes.

---

## 6. HISTORY — what went wrong while building this, so it doesn't recur

Each of these is now a rule in `engine/dispatch.py` rather than a thing to remember.

| What broke | The fix |
|---|---|
| Row heights split equally between items, so two-line bodies got sliced in half by the next row | rows are MEASURED and the stack is solved; the hairline sits in the solved gap |
| The masthead was a typed constant, leaving a dead band under it | the wordmark is scaled to fill the column the photo leaves |
| The photo card, tilted 4°, breached the right margin by 9px | placed from `layout.rotated_bbox`, not from its CSS width |
| Story slides left the lower 55% of the frame empty | content is centred in its region, and a band is always painted across the lower third |
| A count pill looked good and ate 130px the rows needed | the solver refused to fit; mass moved to the footer band |
| Copy was clipped to the point of being cryptic. "new spot, new vibe" over "both move somewhere new" tells a reader nothing | budgets raised to 28/70/70 and the rule restated: **say the thing**. The masthead and photo gave up vertical so the rows could have it |
| Every photo reported as "buried" under its own halftone | fixed in `engine/reconcile.py` — a blended layer cannot hide what is under it (`scratchpad/test_buried_text.py` 28-29) |

---

## 7. OPEN QUESTIONS FOR ISSUE 01

Carried from the verbal brief of 2026-09-22, unverified:

1. ~~The domain.~~ **Resolved 2026-09-22: it is `ngoaquaterra.com`.** It was transcribed by
   ear as "ngoacqua.com" from a verbal brief and sat on a rendered poster before anyone caught
   it. Read a URL back before it ships; a wrong one is the expensive kind of typo.
2. **Terathon "priority access"** — is that a real commitment or an intention? The copy currently
   states it as fact.
3. **"AQ Labs closed off"** — wrapped for the season, or shut? The copy says "labs is wrapped",
   which reads as the former.
4. **Magazine inductions** — "after the first draft" is as specific as the brief was.

See also: `brain/VOICE.md`, `brain/CONTENT_SYSTEM.md`, `brain/AQ_FACTS.md`, `CLAUDE.md` §3 and §9.
