// One sample of every look on every canvas it supports. Run: node campaign/lookbook.mjs [look ...]
import { renderSpecs, sheet } from './renderer.mjs';
const lines = (...a) => a;
const S = {
  plate: { lines: [['Where you'], [{ tag: 'find' }, 'your'], [{ pill: 'tutor.' }]], support: 'Connecting every student in Kolkata to teachers.', cta: 'Search by subject', mascot: { kind: 'arch', mood: 'great' }, kicker: 'Classes IV to XII' },
  answer: { q: 'Do I pay Shikshaq?', answer: 'No. Fees are between you and the tutor.', support: 'Shikshaq takes no commission.', mascot: { kind: 'arch', mood: 'good' }, cta: 'Find your tutor', tag: 'FAQ 06' },
  eyes: { lines: [['Looking for a'], [{ b: 'tutor?' }]], support: 'Search by subject, class, board and area.', cta: 'Start searching' },
  mood: { mood: 'rough', lines: [['Exams soon.'], [{ b: 'No tutor yet.' }]], support: 'There is a quicker way.' },
  poll: { lines: [['What did you think'], [{ b: 'Shikshaq was?' }]], hint: 'Poll sticker goes in this space', mascot: true },
  cover: { label: 'FAQ', mood: 'good' },
  button: { button: 'Message your tutor', lead: 'One tap opens WhatsApp.', body: 'You talk to the tutor yourself. No middleman.', badge: 'Free for families' },
  ui: { variant: 'search', lines: [['Search by'], [{ b: 'subject, class,' }], ['board and area.']], cta: 'Open shikshaq.in' },
  bands: { q: 'Who made Shikshaq? Is it a charity?', a: 'Not a charity. Not a class.', foot: 'Made by AquaTerra, an NGO whose team are students.', mascot: true, kicker: 'FAQ 03' },
  brief: { title: 'Before you pick a tutor', rows: [{ pre: 'Check the', hl: 'subject and board' }, { pre: 'Read the', hl: 'reviews' }, { pre: 'Message', hl: 'first' }], note: 'Checked', cta: 'See profiles' },
  card: { scheme: 'indigo', small: 'Shikshaq\nKolkata', lines: ['Search.', 'Read.', 'Message.'], foot: 'shikshaq.in', rot: 0 },
  swarm: { lines: [['Find'], ['your'], [{ b: 'tutor.' }]], words: ['ICSE', 'ISC', 'CBSE', 'State board', 'Class IV', 'Class XII', 'Maths', 'Science', 'Kolkata'] },
  chat: { lines: [['The chat'], [{ b: 'at home.' }]], msgs: [{ who: 'S', t: 'Ma, I found where to find a Maths tutor near us.' }, { who: 'P', t: 'Another coaching centre?' }, { who: 'S', t: 'No centre. You search, pick a tutor and message them.' }, { who: 'P', t: 'Show me.' }], cta: 'Send them the link' },
  calendar: { lines: [['Your week'], [{ b: 'with a tutor.' }]], notes: [{ col: 0, row: 0, t: 'Maths' }, { col: 3, row: 0, t: 'English' }, { col: 5, row: 1, t: 'Mock paper' }, { col: 1, row: 1, t: 'Doubts' }], cta: 'Find a slot' },
  review: { review: { text: 'Sample review text goes here as a placeholder for the live data.', first: 'Name', subject: 'Maths', cls: 'Class X' }, cta: 'Read more reviews' },
  tutor: { tutor: { name: 'Tutor name', subject: 'Science', quote: 'A placeholder quote the tutor approves before it goes out.' }, cta: 'See the profile' },
};
const want = process.argv.slice(2);
const items = [];
for (const [look, base] of Object.entries(S)) {
  if (want.length && !want.includes(look)) continue;
  const canv = look === 'cover' ? ['C'] : ['S', 'F', 'Q'];
  for (const c of canv) items.push({ id: `${look}-${c}`, look, canvas: c, accent: ['orange', 'indigo', 'mint'][items.length % 3], ground: look === 'swarm' || look === 'brief' ? 'panel' : 'bone', ...structuredClone(base), dir: 'lookbook' });
}
const out = new URL('../out/campaign-what-is-shikshaq', import.meta.url).pathname;
const res = await renderSpecs(items, out);
for (const r of res) if (r.issues.length) console.log(r.id, '\n   ', r.issues.slice(0, 6).join('\n    '));
for (const c of ['S', 'F', 'Q']) { const sub = res.filter(r => r.canvas === c); if (sub.length) await sheet(sub, `${out}/lookbook/_sheet-${c}.png`, { cols: c === 'S' ? 7 : 5 }); }
console.log('rendered', res.length);
