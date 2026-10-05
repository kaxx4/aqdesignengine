// Matrix test: every style in the bank on every template it allows must render gate-clean,
// across mirrored and shuffled variants. Slow (browser); run with `npm run test:render`.
import fs from 'node:fs';
import { loadBank, realize, rng } from './style.mjs';
import { renderPlan } from './render.mjs';

const bank = loadBank(), facts = JSON.parse(fs.readFileSync(new URL('../facts/facts.sample.json', import.meta.url)));
const base = {
  'paper-spotlight': { accent: 'indigo', cta: 'Read two questions free', paper: facts.newPapers[0], copy: { eyebrow: 'Paper of the week', plain: 'Do it like', bold: 'exam day.', line: 'Phone away, timer on, one sitting.' } },
  'subject-mosaic': { accent: 'indigo', cta: 'Pick your subject', featuredSubject: 'Maths', subjectCounts: {}, copy: { plain: 'Start with the', bold: 'one you avoid.', sub: 'That is where the marks are hiding.' } },
  steps: { accent: 'mint', cta: 'Save this for revision', stepSubjects: ['Maths', 'Science', 'History'], copy: { plain: 'Puja break,', bold: 'sorted.', sub: 'A revision plan that still leaves time for pandal hopping.', steps: [{ t: 'Pick one weak chapter', b: 'Only one. Not the whole book.' }, { t: 'Solve a paper on it', b: 'Timed, no phone.' }, { t: 'Fix what you missed', b: 'Write the right answer next to the wrong one.' }] } },
  'find-teacher': { accent: 'orange', cta: 'Find a teacher near you', search: { subject: 'Commerce', cls: 'Class 12', area: 'Tollygunge' }, copy: { plain: 'Message the', bold: 'teacher directly.', sub: 'No agent in between. Agree timing and fees yourselves.', ask: 'What does your child need help with?' } },
  'number-bento': { accent: 'orange', cta: 'See how it works', copy: { plain: 'Zero', bold: 'middlemen.', sub: 'You message the teacher directly. We never take a cut.', bigDisplay: '₹0', bigLabel: 'commission, ever' } },
  'bento-board': { accent: 'orange', cta: 'Find a teacher near you', search: { subject: 'Science', cls: 'Class 10', area: 'Behala' }, copy: { plain: 'Papers and', bold: 'teachers.', sub: 'Read a past paper free. Message a teacher directly.' } },
};
let n = 0, bad = 0;
for (const s of bank.styles) for (const t of Object.keys(base)) {
  if (s.templates !== 'any' && !s.templates.includes(t)) continue;
  for (const seed of [1, 2]) {
    const post = { day: 'T', template: t, ...structuredClone(base[t]), style: realize(s, bank, rng(seed), seed) };
    const [res] = await renderPlan({ posts: [post] }, new URL('../out/_matrix', import.meta.url).pathname);
    n++; if (res.issues.length) { bad++; console.error(`FAIL ${s.id} x ${t} seed ${seed}: ${res.issues.join(' | ')}`); }
  }
}
if (bad) { console.error(`${bad} of ${n} combinations failed the layout gate`); process.exit(1); }
console.log(`ALL ${n} STYLE x TEMPLATE RENDERS PASSED THE GATE`);
