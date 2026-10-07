// node campaign/runsheets.mjs  -> three run sheets (one per person) and the reply bank, in out/.../texts/
// Run sheets are checklists generated from the plan. The reply bank is hand-written, gated, and holds only claims the facts file supports.
import fs from 'node:fs';
import { WEEKS, AQUATERRA } from './plan.mjs';
import { expand } from './catalog.mjs';
import { PUSHES } from './wa.mjs';
import { validateText } from './validate-campaign.mjs';
const OUT = new URL('../out/campaign-what-is-shikshaq/texts', import.meta.url).pathname;
fs.mkdirSync(OUT, { recursive: true });
const files = t => expand(t).map(i => `${i.dir}/${i.id}.png`).join(', ');
const gated = t => expand(t).some(i => i.gated);

// ---- Instagram: feed posts (reels are on hold) -------------------------------------------------------------------------------------------
let ig = '# Run sheet: Instagram feed\n\nOwner: the person who posts to the feed. Launch is Monday 12 October. Post at 19:30 IST. Reels are on hold.\n\n**Before launch (Sunday 11 October):** set the profile link to shikshaq.in, pin nothing yet, and add the highlight covers FQ0, HC1 to HC7 (see the stories sheet).\n\n**Every post:** open the week file (`week1.md` to `week4.md`) for the caption, hashtags and alt text. Paste the alt text into Instagram\'s accessibility field. Reply to every comment within the day, using `reply-bank.md`.\n\n';
for (const wk of WEEKS) {
  ig += `## Week ${wk.n}\n\n`;
  for (const d of wk.days.filter(d => d.feed)) ig += `- [ ] **${d.d} 19:30** ${d.feed}${gated(d.feed) ? ' (GATED: only post once real data is in; else use the swap in the note)' : ''}${AQUATERRA.includes(d.feed) ? ' (+ also on the AquaTerra account)' : ''}: ${files(d.feed)}${d.note ? `\n  - ${d.note}` : ''}\n`;
  ig += '\n';
}
ig += `## AquaTerra account (cross-posts)\n\nOnly the posts marked above. Use the same image and swap the first line of the caption for "Made by us, for every student in Kolkata:". Posts: ${AQUATERRA.join(', ')}.\n`;
fs.writeFileSync(`${OUT}/run-sheet-instagram.md`, ig);

// ---- Stories ----------------------------------------------------------------------------------------------------------------------------------
let st = '# Run sheet: Stories\n\nOwner: the person who posts Stories. Post through the day in the order listed. Every story stands alone (a story lasts a day). Stickers (poll, question, link) are added by hand in Instagram: the dotted boxes in IN1 to IN4 are the room for them.\n\n**Highlights (set up once on Sunday 11 October):** FAQ (cover FQ0, stories FQ1 to FQ8, pinned first), How it works (HC1), Who made it (HC2), Reviews (HC3), Parents say (HC4), Ask a tutor (HC5), Messages (HC6), Stickers (HC7). Tutor FAQ (cover TQ0, stories TQ1 to TQ6) goes up in week 3.\n\n';
for (const wk of WEEKS) {
  st += `## Week ${wk.n}\n\n`;
  for (const d of wk.days) {
    st += `### ${d.d}\n\n`;
    if (d.stories?.length) st += d.stories.map(t => `- [ ] ${files(t)}${gated(t) ? ' (GATED)' : ''}`).join('\n') + '\n';
    else st += '- (no new stories)\n';
    if (d.rerun?.length) st += `- [ ] Rerun: ${d.rerun.join(', ')}\n`;
    st += '\n';
  }
}
fs.writeFileSync(`${OUT}/run-sheet-stories.md`, st);

// ---- WhatsApp ----------------------------------------------------------------------------------------------------------------------------------
let wa = '# Run sheet: WhatsApp\n\nOwner: the person who sends to groups. Four pushes a week. Each push is one image with its message as the caption, sent once, never reposted. Reply in the group, not in private. Full messages and expected replies are in `whatsapp-promotions.md` and the week files.\n\n**First message to any group that needs the admin\'s permission:**\n\n> Hello. May I share one short note about a free site where families in Kolkata find a tutor? It is one image and a link, nothing else. Please tell me if it is not suitable for this group.\n\n';
for (const wk of WEEKS) {
  wa += `## Week ${wk.n}\n\n`;
  for (const d of wk.days) for (const id of d.wa || []) { const p = PUSHES.find(x => x.id === id); wa += `- [ ] **${d.d} ${p.time}** ${p.id} to ${p.to}. Image: ${p.image.join(', ')}${p.gated ? ` (GATED on ${p.gated})` : ''}\n`; }
  wa += '\n';
}
fs.writeFileSync(`${OUT}/run-sheet-whatsapp.md`, wa);

// ---- Reply bank --------------------------------------------------------------------------------------------------------------------------------
const RB = [
  ['What is Shikshaq?', 'Shikshaq is where you find your tutor. Connecting every student in Kolkata to teachers. Search at shikshaq.in.'],
  ['Is it a charity?', 'No. It is where you find your tutor, for any school student in Kolkata. It is made by AquaTerra, an NGO whose team are students.'],
  ['Is it a coaching class or a centre?', 'No. There are no classes at Shikshaq. You search for a tutor, read the profile, and message them yourself.'],
  ['Who is behind it?', 'A student team. Shikshaq is made by AquaTerra, an NGO whose team are students.'],
  ['Do we pay Shikshaq?', 'No. It is free for families. Fees are between you and the tutor, and Shikshaq takes no commission.'],
  ['How much do tutors charge?', 'Each tutor sets their own rate. You agree the fee with the tutor directly.'],
  ['Are the tutors checked?', 'Yes. Tutors apply with a form. A human checks ID and degree, and our team selects who is listed.'],
  ['Which classes do you cover?', 'Classes IV to XII.'],
  ['Which boards?', 'ICSE, ISC, CBSE and State board.'],
  ['Which subjects?', 'Maths, Science, English, Commerce, Computer, Hindi, History and Geography.'],
  ['Which areas of Kolkata?', 'Tutors are listed across Kolkata. Filter by area on shikshaq.in, for example Salt Lake, Jadavpur, Howrah, Ballygunge or Bhowanipore.'],
  ['How do I contact a tutor?', 'Open the profile and message them on WhatsApp. You talk to the tutor directly.'],
  ['Do you share my number?', 'You message the tutor yourself. Your number is not shared until you message.'],
  ['Where do the reviews come from?', 'From students who messaged the tutor.'],
  ['Can a tutor pay to be listed higher?', 'No. There is no paid placement.'],
  ['How do I teach on Shikshaq?', 'Fill out the form at shikshaq.in. Our team checks your background. If you are selected, you are listed. It is free to list.'],
  ['Do tutors pay a commission?', 'No. Tutors set their own rate and keep every rupee.'],
  ['My tutor is not on Shikshaq. Can they join?', 'Yes. Recommend them at shikshaq.in. We will reach out and, once they are checked, get them listed.'],
  ['Is there a past papers section?', 'Yes, on the site. This campaign is about finding a tutor, so start with the search at shikshaq.in.'],
];
const rb = '# Reply bank\n\nCopy, paste, then add a name. Every line is a claim the facts file supports. If a question is not here, do not guess: say "Let me check and come back to you", and send the question to the team.\n\n' + RB.map(([q, a], i) => `**${i + 1}. ${q}**\n\n${a}\n`).join('\n');
const errs = RB.flatMap(([q, a], i) => validateText('reply ' + (i + 1), a));
if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
fs.writeFileSync(`${OUT}/reply-bank.md`, rb);
console.log('wrote run sheets and reply bank');
