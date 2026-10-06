// The campaign catalog, part one: FAQ highlights, anchor, three steps, student-to-parent.
// Every visible word lives here and nowhere else. Looks hold no copy. The copy gate reads this file's output.
import { C } from '../src/tokens.mjs';

// Headline mini-language. Lines split on " / ". Inside a line:  *bold*   [word on a tilted tag]   {word in a pill}
// A tag may carry a fill:  [Maths|#F2A15A]
export const L = str => str.split(' / ').map(line => { for (const [o, c] of [['*', '*'], ['[', ']'], ['{', '}']]) if (line.split(o).length !== line.split(c).length || (o === c && (line.split(o).length - 1) % 2)) throw new Error(`unbalanced ${o}${c} in headline line "${line}": a bold, tag or pill run cannot span two lines, close it and reopen it`); return line.split(/(\*[^*]+\*|\[[^\]]+\]|\{[^}]+\})/).filter(x => x.trim() !== '').map(tok => {
  const t = tok.trim();
  if (t[0] === '*') return { b: t.slice(1, -1) };
  if (t[0] === '[') { const [w, fill] = t.slice(1, -1).split('|'); return fill ? { tag: w, fill } : { tag: w }; }
  if (t[0] === '{') { const [w, fill] = t.slice(1, -1).split('|'); return fill ? { pill: w, fill } : { pill: w }; }
  return t;
}); });

export const mk = (id, family, canvas, look, accent, o = {}) => ({ id, family, dir: family, canvas, look, accent, post: o.post || id, aud: o.aud || 'all', ...o });
// A carousel: one post, N slides, each its own file with a page counter.
export const slides = (post, family, canvas, accent, arr, aud = 'all') =>
  arr.map((s, i) => mk(`${post}-${i + 1}`, family, canvas, s.look, s.accent || accent, { ...s, post, aud, count: `${String(i + 1).padStart(2, '0')}/${String(arr.length).padStart(2, '0')}` }));

const FREE = 'Free for families';
const ORIGIN = 'Made by AquaTerra, an NGO whose team are students.';

// ---- Family 1: the FAQ highlight (built first) -------------------------------------------------------------------------
export const faq = [
  mk('FQ0', 'faq', 'C', 'cover', 'indigo', { label: 'FAQ', mood: 'good', disc: C.indigoTint, aud: 'parents' }),
  mk('FQ1', 'faq', 'S', 'plate', 'indigo', { tag: 'FAQ 01', kicker: 'What is Shikshaq?', lines: L('Where you / [find] your / {tutor.}'), support: 'Connecting every student in Kolkata to teachers.', mascot: { kind: 'arch', mood: 'great' }, cta: 'Search by subject', aud: 'parents' }),
  mk('FQ2', 'faq', 'S', 'swarm', 'orange', { tag: 'FAQ 02', ground: 'panel', q: 'Which classes and boards?', lines: L('Classes / *IV to XII.*'), words: ['ICSE', 'ISC', 'CBSE', 'State board', 'Class IV', 'Class XII', 'Kolkata', 'Maths', 'Science'], aud: 'parents', bind: { areas: 3 } }),
  mk('FQ3', 'faq', 'S', 'bands', 'indigo', { tag: 'FAQ 03', q: 'Who made Shikshaq? Is it a charity?', a: 'Not a charity. Not a class.', foot: ORIGIN, mascot: true, aud: 'parents' }),
  mk('FQ4', 'faq', 'S', 'card', 'indigo', { tag: 'FAQ 04', scheme: 'indigo', small: 'How do I find the right tutor?', lines: ['Search.', 'Read.', 'Message.'], foot: 'shikshaq.in', aud: 'parents' }),
  mk('FQ5', 'faq', 'S', 'button', 'orange', { tag: 'FAQ 05', lead: 'How do I contact a tutor?', button: 'Message your tutor', badge: 'No middleman', body: 'One tap on the profile opens WhatsApp. You talk to the tutor yourself.', aud: 'parents' }),
  mk('FQ6', 'faq', 'S', 'plate', 'mint', { tag: 'FAQ 06', kicker: 'Do I pay Shikshaq?', lines: L('No. / Fees go / to the [tutor.]'), support: 'Shikshaq takes no commission. You agree the fee with the tutor.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'Find your tutor', aud: 'parents' }),
  mk('FQ7', 'faq', 'S', 'brief', 'orange', { tag: 'FAQ 07', ground: 'panel', title: 'Are the tutors checked?', rows: [{ pre: 'Tutors', hl: 'apply', post: 'with a form.' }, { pre: 'Our team runs', hl: 'background checks.' }, { pre: 'We', hl: 'select', post: 'who is listed.' }], note: 'Yes', cta: 'See the tutors', aud: 'parents' }),
  mk('FQ8', 'faq', 'S', 'answer', 'mint', { tag: 'FAQ 08', q: 'Is my phone number safe?', answer: 'Yes. Your details stay private.', support: 'You choose who you contact.', mascot: { kind: 'arch', mood: 'good' }, cta: 'Find your tutor', aud: 'parents' }),
  ...slides('FQ9', 'faq', 'F', 'indigo', [
    { look: 'answer', q: 'What is Shikshaq?', answer: 'Where you find your tutor.', support: 'Connecting every student in Kolkata to teachers.', mascot: { kind: 'arch', mood: 'great' }, cta: 'Swipe for more' },
    { look: 'answer', accent: 'mint', q: 'Which classes and boards?', answer: 'Classes IV to XII.', support: 'ICSE, ISC, CBSE and State board.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'Swipe for more' },
    { look: 'answer', accent: 'orange', q: 'Is it a charity?', answer: 'Not a charity. Not a class.', support: ORIGIN, mascot: { kind: 'lobe', fill: '#5B7BD9' }, cta: 'Swipe for more' },
    { look: 'answer', q: 'Do I pay Shikshaq?', answer: 'No. Fees go to the tutor.', support: 'Shikshaq takes no commission.', mascot: { kind: 'arch', mood: 'good' }, cta: 'Swipe for more' },
    { look: 'button', accent: 'orange', lead: 'Ready?', button: 'Find your tutor', badge: 'Free', body: 'shikshaq.in. Free for families.' },
  ], 'parents'),
];

// ---- Tutor FAQ highlight ("For tutors") ----------------------------------------------------------------------------------
export const tfaq = [
  mk('TQ0', 'tfaq', 'C', 'cover', 'orange', { label: 'For tutors', mood: 'great', disc: C.orangeTint, aud: 'tutors' }),
  mk('TQ1', 'tfaq', 'S', 'answer', 'orange', { tag: 'Tutors 01', q: 'What is Shikshaq for a tutor?', answer: 'A profile where students and parents search for you.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TQ2', 'tfaq', 'S', 'answer', 'orange', { tag: 'Tutors 02', ground: 'tint', q: 'Does it cost to list?', answer: 'Free to list.', support: 'No fee to be on Shikshaq.', mascot: { kind: 'arch', mood: 'great' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TQ3', 'tfaq', 'S', 'answer', 'indigo', { tag: 'Tutors 03', q: 'Do you take a cut?', answer: 'No. You set your own rate.', support: 'And you keep all of it.', mascot: { kind: 'lobe', fill: '#FFC700' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TQ4', 'tfaq', 'S', 'answer', 'orange', { tag: 'Tutors 04', ground: 'tint', q: 'Who contacts me?', answer: 'Real people, on WhatsApp.', support: 'Not sold leads.', mascot: { kind: 'arch', mood: 'good' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TQ5', 'tfaq', 'S', 'answer', 'mint', { tag: 'Tutors 05', q: 'How do I list?', answer: 'Fill out a form.', support: 'Our team checks your background. If you are selected, you are listed.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'Apply to teach', aud: 'tutors' }),
  mk('TQ6', 'tfaq', 'S', 'answer', 'orange', { tag: 'Tutors 06', q: 'Can anyone list?', answer: 'Tutors apply. We select.', support: 'Our team checks every tutor before they are listed.', mascot: { kind: 'arch', mood: 'fine' }, cta: 'Apply to teach', aud: 'tutors' }),
];

// ---- Family 2: anchor and definition --------------------------------------------------------------------------------------
export const hero = [
  mk('H1', 'hero', 'F', 'plate', 'indigo', { lines: L('Shikshaq is / where you / [find] your / {tutor.}'), support: 'Connecting every student in Kolkata to teachers.', mascot: { kind: 'sun', fill: '#FFC700' }, cta: 'shikshaq.in' }),
  mk('H2', 'hero', 'S', 'plate', 'indigo', { lines: L('Shikshaq is / where you / [find] your / {tutor.}'), support: 'Connecting every student in Kolkata to teachers.', mascot: { kind: 'arch', mood: 'great' }, cta: 'shikshaq.in' }),
  mk('H3', 'hero', 'F', 'swarm', 'orange', { ground: 'panel', lines: L('Find / your / *tutor.*'), words: ['Maths', 'Science', 'English', 'Commerce', 'ICSE', 'ISC', 'CBSE', 'State board', 'Class IV to XII', 'Kolkata'] }),
];

// ---- Family 3: find your tutor in three steps -----------------------------------------------------------------------------
const stepSet = canvas => [
  { look: 'plate', kicker: 'How it works', lines: L('Looking for / a [tutor] / in {Kolkata?}'), support: 'Three steps. Here is how Shikshaq works.', mascot: { kind: 'eyes' } },
  { look: 'ui', variant: 'search', tag: 'Step one', lines: L('Search by / *subject, class,* / board and area.') },
  { look: 'ui', variant: 'profile', tag: 'Step two', lines: L('Read the / *profile and* / the reviews.'), tail: 'Experience, qualifications and reviews' },
  { look: 'ui', variant: 'whatsapp', accent: 'mint', tag: 'Step three', lines: L('Message the / *tutor on* / WhatsApp.'), m1: 'Hello, is the Maths slot on Saturday free?', m2: 'Yes. Let us talk about the batch.' },
  { look: 'bands', accent: 'indigo', q: 'So what is Shikshaq?', a: 'Not a charity. Not a class.', foot: 'A place to find your tutor. ' + ORIGIN, mascot: true },
  { look: 'button', accent: 'orange', lead: 'Your turn.', button: 'Find your tutor', badge: FREE, body: 'shikshaq.in. Show this to a parent.' },
];
export const steps = [
  ...slides('B1', 'steps', 'S', 'indigo', stepSet('S'), 'parents'),
  ...slides('B2', 'steps', 'F', 'indigo', stepSet('F'), 'parents'),
  mk('B3', 'steps', 'F', 'brief', 'indigo', { ground: 'panel', title: 'Find your tutor in three steps', rows: [{ pre: 'Search by', hl: 'subject, class, board and area.' }, { pre: 'Read the', hl: 'profile and the reviews.' }, { pre: 'Message the tutor on', hl: 'WhatsApp.' }], note: 'Free', cta: 'shikshaq.in', aud: 'parents' }),
];

// ---- Family 4: student to parent (the core mechanism) ---------------------------------------------------------------------
const chats = [
  { n: 1, ac: 'indigo', lines: L('What is / [this?]'), msgs: [{ who: 'S', t: 'Ma, I found where to find a Maths tutor near us.' }, { who: 'P', t: 'Another coaching centre?' }, { who: 'S', t: 'No centre. You search, pick a tutor and message them.' }, { who: 'P', t: 'Show me.' }] },
  { n: 2, ac: 'mint', lines: L('Who runs / [this?]'), msgs: [{ who: 'P', t: 'Who runs this? Some charity?' }, { who: 'S', t: 'AquaTerra, an NGO run by students. It is for any school student in Kolkata.' }, { who: 'P', t: 'So not a charity class?' }, { who: 'S', t: 'Not a class at all. It is where you find your tutor.' }] },
  { n: 3, ac: 'orange', lines: L('Do we / [pay?]'), msgs: [{ who: 'P', t: 'Do we pay them?' }, { who: 'S', t: 'Free for us to use. Fees are between you and the tutor. No commission.' }, { who: 'P', t: 'Good.' }] },
  { n: 4, ac: 'indigo', lines: L('Is the tutor / [good?]'), msgs: [{ who: 'P', t: 'How will we know the tutor is good?' }, { who: 'S', t: 'Every tutor is checked and selected by the Shikshaq team, and the profile shows experience and reviews. We message first.' }, { who: 'P', t: 'Message first, then decide.' }] },
  { n: 5, ac: 'mint', lines: L('Which / [area?]'), msgs: [{ who: 'P', t: 'Which area?' }, { who: 'S', t: 'You filter by locality, so near us.' }, { who: 'P', t: 'Send me the link.' }, { who: 'S', t: 'Sending now.' }], cta: 'shikshaq.in' },
];
export const chat = chats.flatMap(c => ['F', 'S'].map(cv => mk(`CH${c.n}${cv === 'S' ? 's' : ''}`, 'chat', cv, 'chat', c.ac, { post: cv === 'F' ? `CH${c.n}` : `CH${c.n}s`, count: `0${c.n}/05`, lines: c.lines, msgs: c.msgs, cta: c.cta, aud: 'students' })));

export const parents = [
  mk('PF1', 'parents', 'S', 'card', 'indigo', { scheme: 'bone', small: 'For parents', lines: ['Find', 'a tutor', 'near you.'], foot: 'shikshaq.in', aud: 'parents' }),
  mk('PF2', 'parents', 'S', 'brief', 'indigo', { ground: 'panel', title: 'What is Shikshaq?', rows: [{ pre: 'A place to', hl: 'find a tutor', post: 'in Kolkata.' }, { pre: 'Search by', hl: 'subject, class, board', post: 'and area.' }, { pre: 'Message the tutor on', hl: 'WhatsApp.' }, { pre: '', hl: 'Free for families', post: 'to use.' }], note: 'Show your parents', cta: 'shikshaq.in', aud: 'parents' }),
  mk('PF3', 'parents', 'S', 'bands', 'orange', { q: 'Who is behind it?', a: 'A student team.', foot: ORIGIN, mascot: true, aud: 'parents' }),
  ...[['indigo', ['Where you', 'find your', 'tutor.'], 'shikshaq.in', 'Say it in one line'], ['orange', ['Free', 'for', 'families.'], 'No commission', 'For parents'], ['bone', ['Checked', 'and', 'selected.'], 'Our team checks every tutor', 'The tutors'], ['ink', ['Message', 'the tutor', 'yourself.'], 'On WhatsApp', 'No middleman']]
    .map(([sc, ln, ft, sm], i) => mk(`PF4-${i + 1}`, 'parents', 'Q', 'card', ['indigo', 'orange', 'mint', 'indigo'][i], { post: 'PF4', count: `0${i + 1}/04`, scheme: sc, small: sm, lines: ln, foot: ft, rot: 0, aud: 'students' })),
  ...slides('PF5', 'parents', 'F', 'indigo', [
    { look: 'plate', kicker: 'A note for parents', lines: L('Your child, / a [tutor,] / {found.}'), support: 'Shikshaq is where your child finds a tutor.', mascot: { kind: 'arch', mood: 'good' } },
    { look: 'brief', ground: 'panel', title: 'What it is', rows: [{ pre: 'A place to', hl: 'find a tutor', post: 'in Kolkata.' }, { pre: 'Classes', hl: 'IV to XII.' }, { pre: 'ICSE, ISC, CBSE and', hl: 'State board.' }], note: 'Plainly' },
    { look: 'ui', variant: 'search', lines: L('How to / *look.*') },
    { look: 'bands', accent: 'orange', q: 'Who is behind Shikshaq?', a: 'A student team.', foot: ORIGIN, mascot: true },
    { look: 'button', accent: 'orange', lead: 'For your child.', button: 'Find a tutor', badge: FREE, body: 'shikshaq.in. You message the tutor yourself.' },
  ], 'parents'),
];
