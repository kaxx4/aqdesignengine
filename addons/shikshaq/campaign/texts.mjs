// Text deliverables generated from the catalog, the plan and the pushes. All of it goes through the copy gate.
import fs from 'node:fs';
import path from 'node:path';
import { ITEMS, FAMILIES, expand, byId } from './catalog.mjs';
import { WEEKS, RESERVE } from './plan.mjs';
import { PUSHES, ADMIN_ASK, FORMAT } from './wa.mjs';
import { CAPTIONS, HASHTAGS, AUDIENCE } from './captions.mjs';
import { fillTokens } from './resolve.mjs';
import { validateText, visible } from './validate-campaign.mjs';

const w = (dir, f, s) => { fs.mkdirSync(dir, { recursive: true }); fs.writeFileSync(path.join(dir, f), s); };

export function altText(it) {
  const parts = visible(it).filter(([k]) => !['tag'].includes(k)).map(([, v]) => v);
  if (it.review) parts.unshift(it.review.text);
  if (it.tutor) parts.unshift(`${it.tutor.name}, ${it.tutor.subject}: ${it.tutor.quote}`);
  const kind = { S: 'Story', F: 'Instagram post', Q: 'Square image', C: 'Highlight cover' }[it.canvas];
  return `${kind} for Shikshaq. ${[...new Set(parts)].join(' ')}`.slice(0, 380);
}
export const hashtagsFor = post => [...HASHTAGS.core, ...(HASHTAGS[AUDIENCE[post] || 'parents'] || [])].slice(0, 8);

// Feed and square posts: one row per POST (a carousel is one post).
export function feedPosts() {
  const seen = new Map();
  for (const it of ITEMS) if ((it.canvas === 'F' || (it.canvas === 'Q' && it.family !== 'wa' && it.id !== 'RP5')) && !seen.has(it.post)) seen.set(it.post, it);
  return [...seen.keys()];
}

export function writeCaptions(dir, items) {
  const errors = []; let md = '# Captions, alt text and hashtags\n\nOne caption per feed or square post. A carousel is one post. Alt text is per image.\n\n';
  for (const post of feedPosts()) {
    const cap = CAPTIONS[post];
    if (!cap) { errors.push(`no caption for post ${post}`); continue; }
    const tags = hashtagsFor(post).join(' ');
    errors.push(...validateText(post, cap), ...(tags.split(' ').length > 8 ? [`${post}: more than 8 hashtags`] : []));
    const imgs = items.filter(i => i.post === post);
    md += `## ${post}\n\n${cap}\n\n${tags}\n\n` + imgs.map(i => `- ${i.id}: ${altText(i)}`).join('\n') + '\n\n';
  }
  w(dir, 'captions.md', md);
  return errors;
}

export function writeSchedule(dir, items, data) {
  const errors = []; const used = new Set();
  let md = '# Four-week schedule\n\nOne feed post a day, stories through the day, WhatsApp pushes by id. Times are IST. A post marked GATED waits on real data.\n\n';
  const gate = tok => { const e = expand(tok); if (!e.length && !/^WP|best performing/.test(tok)) errors.push(`plan names ${tok} but no asset has that id or post`); e.forEach(x => used.add(x.id)); return e.some(x => x.gated); };
  for (const wk of WEEKS) {
    md += `## Week ${wk.n}: ${wk.theme}\n\n| Day | Feed (19:30) | Stories and Status | WhatsApp | Notes |\n|---|---|---|---|---|\n`;
    for (const d of wk.days) {
      const g = gate(d.feed); (d.stories || []).forEach(gate);
      const wa = (d.wa || []).map(id => { const p = PUSHES.find(x => x.id === id); return p ? `${id} ${p.time} ${p.to}` : id; }).join('; ');
      md += `| ${d.d} | ${d.feed}${g ? ' (GATED)' : ''} | ${(d.stories || []).join(', ') || '-'}${d.rerun ? ' . Rerun: ' + d.rerun.join(', ') : ''} | ${wa || '-'} | ${d.note || ''} |\n`;
    }
    md += '\n';
  }
  RESERVE.forEach(gate);
  md += `## Reserve (swap in when a gated post is not ready)\n\n${RESERVE.join(', ')}\n\n`;
  const unscheduled = ITEMS.filter(i => !used.has(i.id) && i.family !== 'wa' && !['PF4-1', 'PF4-2', 'PF4-3', 'PF4-4', 'RP5'].includes(i.id)).map(i => i.id);
  if (unscheduled.length) errors.push(`assets in no plan slot: ${unscheduled.join(', ')}`);
  w(dir, 'schedule.md', md);
  return errors;
}

export function pushTexts(data) {
  const errors = [], out = [];
  for (const p of PUSHES) {
    const { text, missing } = fillTokens(p.message, data);
    if (!missing.length) errors.push(...validateText(p.id, text, { cap: 1000 }));
    p.replies.forEach(([q, a]) => errors.push(...validateText(p.id + ' reply', a)));
    out.push({ ...p, text, missing });
  }
  errors.push(...validateText('ADMIN_ASK', ADMIN_ASK), ...validateText('FORMAT', FORMAT));
  return { out, errors };
}
export function writeWhatsApp(dir, pushes) {
  let md = `# WhatsApp promotions\n\n${PUSHES.length} pushes over four weeks. Each is an image with its message as the caption, sent once.\n\n**How to send.** ${FORMAT}\n\n**When a group needs the admin's permission, send this first:**\n\n> ${ADMIN_ASK}\n\n`;
  for (const p of pushes) {
    md += `## ${p.id}: Week ${p.week} ${p.day} ${p.time}, ${p.to}\n\nImage: ${p.image.join(', ')}${p.gated ? `  (GATED on ${p.gated}${p.missing.length ? ': ' + p.missing.length + ' slot(s) pending' : ''})` : ''}\n\n\`\`\`\n${p.text}\n\`\`\`\n\n**Replies to expect**\n\n` + p.replies.map(([q, a]) => `- "${q}" Reply: ${a}`).join('\n') + '\n\n';
    w(path.join(dir, 'wa'), `${p.id}.txt`, p.text + '\n');
  }
  w(dir, 'whatsapp-promotions.md', md);
}

export function writeVolunteer(dir) {
  const md = `# If someone asks about Shikshaq

**Say this first, always:** Shikshaq is where you find your tutor. Connecting every student in Kolkata to teachers.

## Answers

- **Is it a charity?** No. It is where you find your tutor, for any school student in Kolkata. It is made by AquaTerra, an NGO whose team are students.
- **Is it a coaching centre or a class?** No. There are no classes at Shikshaq. You search for a tutor, read the profile and message them yourself.
- **Is it only for students who cannot afford tuition?** No. It is for any school student in Kolkata who is looking for a tutor.
- **Do families pay Shikshaq?** No. It is free for families. Fees are between you and the tutor, and Shikshaq takes no commission.
- **Are the tutors checked?** Yes. Tutors apply with a form. Our team runs background checks and selects who is listed.
- **Which classes and boards?** Classes IV to XII. ICSE, ISC, CBSE and State board.
- **Who is behind it?** A student team. AquaTerra, an NGO whose team are students.

## Do

- Lead with "where you find your tutor". Say what it is before you say what it is not.
- Send people to shikshaq.in.
- Say "checked and selected by our team" about tutors.

## Do not

- Do not open with "it is not a charity". The first words stick.
- Do not give a number that is not on the site.
- Do not promise a result, a rating or a price.
- Do not describe the checks in any words other than "checked and selected". Do not rank tutors.
`;
  w(dir, 'volunteer-answers.md', md);
  return validateText('volunteer sheet', md.replace(/^#.*$/gm, ''), { cap: 4000 });
}

export function writeReels(dir) {
  const md = `# Reel scripts (script and storyboard only)

Screen footage must be a real recording of the live site. No invented screens, names or reviews.

## R1: Tell your parents in three steps (about fifteen seconds)

| Beat | Picture | On-screen text | Voice |
|---|---|---|---|
| 1 | A student looks at a phone, thinking | Looking for a tutor? | Looking for a tutor? |
| 2 | Real recording: the search on shikshaq.in | Search | Search by subject, class, board and area. |
| 3 | Real recording: a tutor profile and its reviews | Read | Read the profile and the reviews. |
| 4 | Real recording: the WhatsApp message opening | Message | Message the tutor yourself. |
| 5 | The student shows the phone to a parent, who nods | Where you find your tutor. | Shikshaq. Where you find your tutor. |
| End card | Logo on bone | shikshaq.in | |

## R2: The chat at home (about twenty seconds)

The conversation from CH2 typed out one bubble at a time, parent first, then student, with the blob avatars. Hold on the last line, then the end card.

| Beat | Bubble | Picture |
|---|---|---|
| 1 | Who runs this? Some charity? | Parent bubble types in |
| 2 | AquaTerra, an NGO run by students. It is for any school student in Kolkata. | Student bubble |
| 3 | So not a charity class? | Parent bubble |
| 4 | Not a class at all. It is where you find your tutor. | Student bubble, then the great blob smiles |
| End card | | shikshaq.in |
`;
  w(dir, 'reels.md', md);
  return validateText('reels', md.replace(/^#.*$/gm, '').replace(/\|[-| ]+\|/g, ''), { cap: 4000 }).filter(e => !/digit/.test(e));
}
