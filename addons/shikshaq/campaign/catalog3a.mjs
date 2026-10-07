// Catalog v3, part one. Every visible word is here. The voice is the site's own: specific, a little dry, never a slogan.
// Facts are the site's published ones (home, About, Join, Help, Recommend). Nothing is invented.
import { L, mk, slides, ORIGIN, FREE } from './catalog-util.mjs';

const EYES = { kind: 'eyes' }, SMILE = { kind: 'smile' }, SUN = { kind: 'sun' }, LOBE = { kind: 'lobe' };
const H = o => ({ type: 'head', fill: 'card', grow: .9, ...o });
const FAQ_PILLS = { type: 'pills', grow: 1 };

// ---- FAQ highlight (parents and students) ------------------------------------------------------------------------------------
export const faq = [
  mk('FQ0', 'faq', 'C', 'orange', [], { look: 'cover', label: 'FAQ', mood: 'good', disc: '#FFF4E8', aud: 'parents' }),
  mk('FQ1', 'faq', 'S', 'orange', [
    H({ eyebrow: 'FAQ 01', lines: L('So what is / *Shikshaq*, exactly?'), size: 118 }),
    { type: 'answer', fill: 'orange', lines: L('Where you / find your / tutor.'), sub: 'Connecting every student in Kolkata to teachers.', mascot: { ...EYES, size: 400 }, grow: 1.7 },
    { ...FAQ_PILLS, runs: ['You can', { t: 'filter by subject or board', fill: 'orange' }, 'or', { t: 'search your own area', fill: 'indigo' }, '. Then you message the tutor yourself on WhatsApp.'], foot: 'Free to search. Free to contact.' },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ2', 'faq', 'S', 'indigo', [
    H({ eyebrow: 'FAQ 02', lines: L('Is it for / *my class*?'), size: 124 }),
    { type: 'answer', fill: 'indigo', lines: L('Classes / IV to XII.'), sub: 'ICSE, ISC, CBSE and State board.', mascot: { ...SUN, size: 380 }, grow: 1.5 },
    { type: 'grid', fill: 'card', lines: L('Pick yours'), size: 80, tiles: ['4', '5', '6', '7', '8', '9', '10', '11', '12'], on: ['10'], foot: 'Every board, every class.', grow: 1.2 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ3', 'faq', 'S', 'indigo', [
    H({ eyebrow: 'FAQ 03', lines: L('Who made this? / Is it a *charity*?'), size: 108 }),
    { type: 'answer', fill: 'indigo', lines: L('Not a charity. / Not a class.'), sub: ORIGIN, mascot: { ...LOBE, size: 380 }, grow: 1.7 },
    { type: 'tile', fill: 'orangeTint', icon: 'cap', label: 'Why it exists', lines: L('Finding a tutor / should not be a *favour* / you ask around for.'), size: 76, grow: 1.1 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ4', 'faq', 'S', 'orange', [
    H({ eyebrow: 'FAQ 04', lines: L('How do I find / *the right one*?'), size: 112 }),
    { type: 'steps', fill: 'orange', ordinal: '', lines: L('Three taps, / no account.'), rows: [{ icon: 'search', t: 'Tell us the subject', b: 'Subject, class and your area.' }, { icon: 'users', t: 'Compare real profiles', b: 'Rates, boards, reviews and travel radius, all on one card.' }, { icon: 'chat', t: 'Message on WhatsApp', b: 'Talk to the tutor directly.' }], grow: 3 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ5', 'faq', 'S', 'orange', [
    H({ eyebrow: 'FAQ 05', lines: L('How do I / *reach* a tutor?'), size: 118 }),
    { type: 'ticket', fill: 'bone', tfill: 'orange', kicker: 'One tap', title: 'Message on WhatsApp', sub: 'Shikshaq never sits in the middle.', foot: 'shikshaq.in', size: 96, grow: 1.4 },
    { type: 'tile', fill: 'mintTint', icon: 'shield', label: 'Your number', lines: L('Never shared / until *you* message.'), size: 78, tileFill: 'mint', grow: 1.2 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ6', 'faq', 'S', 'orange', [
    H({ eyebrow: 'FAQ 06', lines: L('Do I pay / *Shikshaq*?'), size: 126 }),
    { type: 'answer', fill: 'orange', lines: L('No. Fees go / to the tutor.'), sub: 'They keep every rupee of their fee, and we take nothing.', mascot: { ...EYES, size: 380 }, grow: 1.5 },
    { type: 'bento', fill: 'bone', tiles: [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart' }, { label: 'To contact', big: 'Free', fill: 'mint', icon: 'chat' }], grow: 1 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ7', 'faq', 'S', 'indigo', [
    H({ eyebrow: 'FAQ 07', lines: L('Are the tutors / *checked*?'), size: 118 }),
    { type: 'steps', fill: 'indigo', lines: L('Before a profile / goes live'), rows: [{ icon: 'edit', t: 'Tutors apply', b: 'A five-step form.' }, { icon: 'shield', t: 'A human checks', b: 'ID and degree, by hand.' }, { icon: 'users', t: 'Our team selects', b: 'Only then are they listed.' }], grow: 3 },
  ], { aud: 'parents', tag: 'FAQ' }),
  mk('FQ8', 'faq', 'S', 'orange', [
    H({ eyebrow: 'FAQ 08', lines: L('Is my number / *safe*?'), size: 122 }),
    { type: 'answer', fill: 'mint', lines: L('Yes. We never / sell your number.'), sub: 'You choose who you contact.', mascot: { kind: 'arch', mood: 'good', size: 340 }, grow: 1.6 },
    { ...FAQ_PILLS, runs: ['Your number is never shared with the teacher until', { t: 'you message them yourself', fill: 'orange' }, '.'], foot: 'Free to search. Free to contact.' },
  ], { aud: 'parents', tag: 'FAQ' }),
  ...slides('FQ9', 'faq', 'F', 'orange', [
    { panels: [H({ eyebrow: 'The short answers', lines: L('What is / *Shikshaq*?'), size: 118 }), { type: 'answer', fill: 'orange', lines: L('Where you find / your tutor.'), sub: 'Connecting every student in Kolkata to teachers.', mascot: { ...EYES, size: 340 }, grow: 1.6 }] },
    { accent: 'indigo', panels: [H({ eyebrow: 'The short answers', lines: L('Is it for / *my class*?'), size: 118 }), { type: 'answer', fill: 'indigo', lines: L('Classes IV to XII.'), sub: 'ICSE, ISC, CBSE and State board.', mascot: { ...SUN, size: 340 }, grow: 1.6 }] },
    { accent: 'indigo', panels: [H({ eyebrow: 'The short answers', lines: L('Is it a *charity*?'), size: 118 }), { type: 'answer', fill: 'indigo', lines: L('Not a charity. / Not a class.'), sub: ORIGIN, mascot: { ...LOBE, size: 340 }, grow: 1.6 }] },
    { panels: [H({ eyebrow: 'The short answers', lines: L('Do I pay / *Shikshaq*?'), size: 118 }), { type: 'answer', fill: 'orange', lines: L('No. Fees go / to the tutor.'), sub: 'They keep every rupee. We take nothing.', mascot: { ...EYES, size: 340 }, grow: 1.6 }] },
    { panels: [{ type: 'loud', fill: 'orange', lines: L('Ready?'), sub: 'Subject, class and your area. Three taps, no account needed.', button: 'shikshaq.in', mascot: SMILE, msize: 340 }] },
  ], 'parents'),
];

// ---- FAQ for tutors ------------------------------------------------------------------------------------------------------------------
const TQ = (id, n, q, a, sub, mas, accent = 'orange') => mk(id, 'tfaq', 'S', accent, [
  H({ eyebrow: `For tutors ${n}`, lines: q, size: 118 }),
  { type: 'answer', fill: accent === 'indigo' ? 'indigo' : accent === 'mint' ? 'mint' : 'orange', lines: a, sub, mascot: { ...mas, size: 390 }, grow: 1.7 },
  { type: 'tile', fill: accent === 'indigo' ? 'indigoTint' : 'orangeTint', icon: 'heart', label: 'Built by students', lines: L('We were students in / this *city*.'), size: 76, grow: 1 },
], { aud: 'tutors', tag: 'Tutors' });
export const tfaq = [
  mk('TQ0', 'tfaq', 'C', 'orange', [], { look: 'cover', label: 'For tutors', mood: 'great', disc: '#FFF4E8', aud: 'tutors' }),
  TQ('TQ1', '01', L('What do I get / on *Shikshaq*?'), L('A profile / students search.'), 'Students and parents find you by subject, class, board and area.', SUN),
  TQ('TQ2', '02', L('Does it cost / to *list*?'), L('Free to list.'), 'No listing fee. No lead credits. No bidding for students.', EYES),
  TQ('TQ3', '03', L('Do you take / a *cut*?'), L('No. Keep every / rupee.'), 'You set your rate. We never invoice anyone.', LOBE, 'indigo'),
  TQ('TQ4', '04', L('Who *messages* me?'), L('Real people, / on WhatsApp.'), 'Enquiries reach you directly. Shikshaq never sits in the middle.', { kind: 'arch', mood: 'great' }),
  TQ('TQ5', '05', L('How do I / *join*?'), L('Fill in one / form.'), 'A five-step form. Reviewed in about three working days.', SUN, 'mint'),
  TQ('TQ6', '06', L('Can *anyone* list?'), L('Tutors apply. / We check.'), 'ID and degree checked by a human. No paid placement in results. Ever.', EYES),
];

// ---- Anchor ------------------------------------------------------------------------------------------------------------------------------
export const hero = [
  mk('H1', 'hero', 'F', 'orange', [
    H({ eyebrow: 'Tuition in Kolkata', lines: L('That one chapter / *nobody understands*?'), size: 124, mascot: { ...EYES, size: 300 }, grow: 1.2 }),
    { type: 'tile', fill: 'orangeTint', icon: 'users', label: 'Find a tutor', lines: L('*Message them* yourself, / free.'), size: 92, grow: 1.2 },
    { type: 'search', fill: 'card', toggle: false, chips: ['Class 10', 'Maths', 'Home tuition'], query: 'Subject, class, area', grow: .9 },
  ], { aud: 'all' }),
  mk('H2', 'hero', 'S', 'orange', [
    { type: 'loud', fill: 'orange', lines: L('Shikshaq is / where you find / your tutor.'), sub: 'Connecting every student in Kolkata to teachers.', button: 'Free to contact', mascot: SMILE },
  ], { aud: 'all' }),
  mk('H3', 'hero', 'F', 'indigo', [
    { type: 'head', fill: 'card', eyebrow: 'The facts, plainly', lines: L('Four things / *worth knowing*'), size: 110, grow: .9 },
    { type: 'bento', fill: 'bone', tiles: [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart', h: 250 }, { label: 'Classes', big: 'IV to XII', fill: 'orange', icon: 'book', h: 250 }, { label: 'Boards', big: 'Four', fill: 'indigo', icon: 'file', h: 250 }, { label: 'To contact', big: 'Free', fill: 'mint', icon: 'chat', h: 250 }], grow: 1.6 },
  ], { aud: 'all' }),
  mk('H4', 'hero', 'S', 'orange', [
    H({ eyebrow: 'Tuition in Kolkata', lines: L('That one chapter / *nobody understands*?'), size: 128, mascot: { ...EYES, size: 360 }, grow: 1.2 }),
    { type: 'tile', fill: 'orangeTint', icon: 'users', label: 'Find a tutor', lines: L('*Message them* / yourself, free.'), size: 96, grow: 1 },
    { type: 'steps', fill: 'orange', lines: L('Then talk to / them yourself'), rows: [{ icon: 'search', t: 'Tell us the subject', b: 'Subject, class and your area.' }, { icon: 'users', t: 'Compare real profiles', b: 'All on one card.' }, { icon: 'chat', t: 'Message on WhatsApp', b: 'No middleman.' }], grow: 2.2 },
  ], { aud: 'all' }),
  mk('H5', 'hero', 'S', 'orange', [
    { type: 'builder', fill: 'orange', title: L('Still deciding?'), sub: 'Fill in the blanks and we will take you straight there.', lines: [['I need a'], [{ t: 'subject' }, 'tutor'], ['for', { t: 'class' }], ['near', { t: 'area' }]], button: 'Find them', grow: 1 },
  ], { aud: 'all' }),
];

// ---- Find your tutor in three steps -----------------------------------------------------------------------------------------------
const STEP = (canvas) => [
  { panels: [{ type: 'loud', fill: 'indigo', lines: L('That one chapter / nobody / understands?'), sub: 'Here is how Shikshaq works. Three steps.', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 400 }] },
  { accent: 'orange', panels: [H({ ordinal: '01', lines: L('Tell us / *the subject*'), sub: 'Subject, class and your area. Three taps, no account needed.', size: 124, grow: 1.1 }), { type: 'search', fill: 'card', chips: ['Class 10', 'Maths', 'Home tuition'], grow: 1.3 }] },
  { accent: 'orange', panels: [H({ ordinal: '02', lines: L('Compare / *real profiles*'), sub: 'Rates, boards, reviews and travel radius, all on one card.', size: 124, grow: 1.1 }), { type: 'chips', fill: 'card', solid: true, chips: ['Rates', 'Boards', 'Reviews', 'Travel radius'], csize: 56, grow: 1.3 }] },
  { accent: 'orange', panels: [H({ ordinal: '03', lines: L('Message / *on WhatsApp*'), size: 124, grow: 1 }), { type: 'chat', fill: 'tint', msgs: [{ who: 'S', t: 'Hello Sir, is the Maths slot on Saturday free?' }, { who: 'P', t: 'Yes. Tell me the board and what is giving trouble.' }], grow: 1.4 }, { type: 'tile', fill: 'orangeTint', icon: 'shield', label: 'Shikshaq never sits in the middle', lines: L('No fees, / no middleman, / *no commission*.'), size: 70, grow: 1 }] },
  { accent: 'indigo', panels: [H({ eyebrow: 'So what is it?', lines: L('Not a *charity*. / Not a class.'), size: 118, grow: 1 }), { type: 'answer', fill: 'indigo', lines: L('It is where / you find / your tutor.'), mascot: { kind: 'sun', size: 360 }, grow: 1.8 }, { type: 'pills', runs: ['Made by', { t: 'AquaTerra', fill: 'orange' }, ', an NGO whose team are students.'], grow: .8 }] },
  { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('Your turn.'), sub: 'Show it to a parent.', button: 'shikshaq.in', mascot: SMILE }] },
];
export const steps = [
  ...slides('B1', 'steps', 'S', 'orange', STEP('S'), 'parents'),
  ...slides('B2', 'steps', 'F', 'orange', STEP('F'), 'parents'),
  mk('B3', 'steps', 'F', 'orange', [
    H({ eyebrow: 'Find your tutor', lines: L('In three / *steps*'), size: 118, grow: .8 }),
    { type: 'index', fill: 'card', rows: [{ t: 'Tell us the subject', b: 'Subject, class and your area.' }, { t: 'Compare real profiles', b: 'Rates, boards, reviews, travel radius.' }, { t: 'Message on WhatsApp', b: 'Talk to the tutor directly.' }], grow: 2 },
    { type: 'ticket', fill: 'bone', tfill: 'orange', kicker: 'Free to contact', title: 'shikshaq.in', size: 100, foot: 'No fees. No middleman. No commission.', grow: 1 },
  ], { aud: 'parents' }),
];

// ---- The chat at home --------------------------------------------------------------------------------------------------------------------
const CH = [
  { n: 1, ac: 'orange', lines: L('What is / *this*?'), msgs: [{ who: 'S', t: 'Ma, found where to find a Maths tutor near us.' }, { who: 'P', t: 'Another coaching centre?' }, { who: 'S', t: 'No centre. You search, pick a tutor and message them.' }, { who: 'P', t: 'Hm. Show me.' }] },
  { n: 2, ac: 'indigo', lines: L('Who runs / *this*?'), msgs: [{ who: 'P', t: 'Who runs this? Some charity?' }, { who: 'S', t: 'AquaTerra, an NGO run by students. It is for any school student in Kolkata.' }, { who: 'P', t: 'So not a charity class?' }, { who: 'S', t: 'Not a class at all. It is where you find your tutor.' }] },
  { n: 3, ac: 'orange', lines: L('Do we / *pay*?'), msgs: [{ who: 'P', t: 'Do we pay them?' }, { who: 'S', t: 'Not Shikshaq. Fees are between you and the tutor, and they keep every rupee.' }, { who: 'P', t: 'No commission?' }, { who: 'S', t: 'None. Ever.' }] },
  { n: 4, ac: 'indigo', lines: L('Is the tutor / *good*?'), msgs: [{ who: 'P', t: 'How will we know the tutor is good?' }, { who: 'S', t: 'A human checks their ID and degree before the profile goes live. Every review is from a student who messaged them.' }, { who: 'P', t: 'Fine. We message first.' }] },
  { n: 5, ac: 'orange', lines: L('Which / *area*?'), msgs: [{ who: 'P', t: 'Which area?' }, { who: 'S', t: 'You filter by area. Salt Lake, Jadavpur, Howrah, wherever.' }, { who: 'P', t: 'Send me the link.' }, { who: 'S', t: 'Sending now.' }] },
];
export const chat = CH.flatMap(c => ['F', 'S'].map(cv => mk(`CH${c.n}${cv === 'S' ? 's' : ''}`, 'chat', cv, c.ac, [
  H({ eyebrow: 'The chat at home', lines: c.lines, size: 124, grow: .7, sticker: { t: `Episode ${['one', 'two', 'three', 'four', 'five'][c.n - 1]}`, tone: 'dark' } }),
  { type: 'chat', fill: 'tint', msgs: c.msgs, fs: 48, grow: 2 },
  ...(c.n === 5 ? [{ type: 'cta', fill: 'accent', lines: L('Send them / the link.'), button: 'shikshaq.in', size: 96, grow: .8 }] : []),
], { post: cv === 'F' ? `CH${c.n}` : `CH${c.n}s`, count: `0${c.n}/05`, aud: 'students' })));

// ---- Student to parent -----------------------------------------------------------------------------------------------------------------------
export const parents = [
  mk('PF1', 'parents', 'S', 'indigo', [{ type: 'loud', fill: 'indigo', lines: L('Find a tutor / near you.'), sub: 'Search by subject, class, board and area. Message the tutor yourself. Free for families.', button: 'For parents', mascot: { kind: 'eyes', fill: '#FFFFFF' } }], { aud: 'parents' }),
  mk('PF2', 'parents', 'S', 'orange', [
    H({ eyebrow: 'For parents', lines: L('What is / *Shikshaq*?'), size: 124, grow: .8 }),
    { type: 'pills', runs: ['Shikshaq is', { t: 'a place to find a tutor', fill: 'orange' }, 'in Kolkata. You can', { t: 'filter by subject or board', fill: 'orange' }, 'or', { t: 'search your own area', fill: 'indigo' }, '. Then you message the tutor yourself on WhatsApp. No agent stands in between, they keep every rupee of their fee, and we take nothing.'], psize: 56, foot: 'Free to search. Free to contact. We never sell your number.', grow: 2.4 },
  ], { aud: 'parents' }),
  mk('PF3', 'parents', 'S', 'indigo', [
    H({ eyebrow: 'For parents', lines: L('Who is / *behind it*?'), size: 124, grow: .8 }),
    { type: 'answer', fill: 'indigo', lines: L('A student team.'), sub: ORIGIN, mascot: { ...SUN, size: 380 }, grow: 1.4 },
    { type: 'tile', fill: 'orangeTint', icon: 'cap', label: 'Why', lines: L('The list / Kolkata *never had*.'), size: 84, grow: 1 },
  ], { aud: 'parents' }),
  ...[['orange', L('Where you / find your / tutor.'), 'Say it in one line', 'eyes'], ['indigo', L('Free for / families.'), 'No commission', 'sun'], ['orange', L('Checked / by a human.'), 'ID and degree, by hand', 'smile'], ['indigo', L('Message / the tutor / yourself.'), 'On WhatsApp', 'eyes']].map(([ac, lines, sub, m], i) =>
    mk(`PF4-${i + 1}`, 'parents', 'Q', ac, [{ type: 'loud', fill: ac === 'indigo' ? 'indigo' : 'orange', lines, sub, mascot: { kind: m, fill: ac === 'indigo' && m === 'eyes' ? '#FFFFFF' : undefined }, msize: 260, size: 130 }], { post: 'PF4', count: `0${i + 1}/04`, aud: 'students' })),
  ...slides('PF5', 'parents', 'F', 'indigo', [
    { panels: [{ type: 'loud', fill: 'indigo', lines: L('A note / for parents.'), sub: 'Shikshaq is where your child finds a tutor.', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 340 }] },
    { accent: 'orange', panels: [H({ eyebrow: 'What it is', lines: L('A place to / *find a tutor*'), size: 112, grow: .9 }), { type: 'chips', fill: 'card', eyebrow: 'Covers', chips: ['Classes IV to XII', 'ICSE', 'ISC', 'CBSE', 'State board', 'Kolkata'], csize: 48, grow: 1.4 }] },
    { accent: 'orange', panels: [H({ eyebrow: 'What it costs', lines: L('Nothing, to / *you or the tutor*'), size: 100, grow: .9 }), { type: 'bento', fill: 'bone', tiles: [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart', h: 230 }, { label: 'To contact', big: 'Free', fill: 'mint', icon: 'chat', h: 230 }], grow: 1.2 }] },
    { accent: 'indigo', panels: [H({ eyebrow: 'Why trust it', lines: L('A human / *checks* each one'), size: 104, grow: .9 }), { type: 'steps', fill: 'indigo', lines: L('Before a profile / goes live'), rows: [{ icon: 'shield', t: 'ID and degree', b: 'Checked by a human.' }, { icon: 'users', t: 'Our team selects', b: 'Only then are they listed.' }], grow: 1.6 }] },
    { accent: 'orange', panels: [{ type: 'loud', fill: 'orange', lines: L('For your / child.'), sub: 'You message the tutor yourself.', button: 'shikshaq.in', mascot: SMILE, msize: 320 }] },
  ], 'parents'),
];

// ---- Character stories ----------------------------------------------------------------------------------------------------------------------
const MOODS = { rough: '#D14545', meh: '#EFA063', fine: '#9B4FC4', good: '#3FAFA8', great: '#FF8000' };
const MB = (id, mood, lines, sub, ac) => mk(id, 'char', 'S', ac, [{ type: 'loud', fill: MOODS[mood], lines, sub, mascot: { kind: 'arch', mood, fill: '#FFFFFF', rot: 4 }, msize: 560 }], { aud: 'students' });
export const char = [
  MB('MB1', 'rough', L('Exams soon. / No tutor yet.'), 'Asking around is slow.', 'orange'),
  MB('MB2', 'meh', L('Asked around. / Got a number / that does not work.'), '', 'orange'),
  MB('MB3', 'fine', L('Subject. Class. / Area. Three taps.'), 'No account needed.', 'indigo'),
  MB('MB4', 'good', L('Found a tutor / near you.'), 'Read the profile and the reviews first.', 'mint'),
  MB('MB5', 'great', L('Message sent. / Now it is / their turn.'), '', 'orange'),
  mk('EY1', 'char', 'S', 'orange', [{ type: 'loud', fill: 'orange', lines: L('Looking / for a tutor?'), sub: 'Search by subject, class, board and area.', button: 'shikshaq.in', mascot: EYES, msize: 520 }], { aud: 'students' }),
  mk('EY2', 'char', 'S', 'indigo', [{ type: 'loud', fill: 'indigo', lines: L('Maths? / Science? / English?'), sub: 'Pick a subject. Find your tutor.', button: 'Pick yours', mascot: { kind: 'eyes', fill: '#FFFFFF' }, msize: 420 }], { aud: 'students' }),
  mk('EY3', 'char', 'S', 'orange', [
    H({ eyebrow: 'Found one you like?', lines: L('One tap / opens *WhatsApp*'), size: 124, grow: .8 }),
    { type: 'ticket', fill: 'bone', tfill: 'orange', kicker: 'No middleman', title: 'Message your tutor', sub: 'You talk to them yourself.', foot: 'shikshaq.in', size: 92, grow: 1.6 },
    { type: 'tile', fill: 'orangeTint', icon: 'shield', label: 'Your number', lines: L('Never shared / until *you* message.'), size: 76, grow: 1 },
  ], { aud: 'students' }),
  ...[['IN1', 'orange', L('What did you think / *Shikshaq was*?'), 'Poll: Where you find a tutor | A charity | A coaching centre | Not sure'], ['IN2', 'indigo', L('Which subject / do you need / *a tutor for*?'), 'Poll: Maths | Science | English | Commerce'], ['IN3', 'orange', L('Ask us anything / *about finding* / *a tutor*.'), 'Question box sticker'], ['IN4', 'indigo', L('Did you show / *your parents*?'), 'Poll: Yes | Not yet']].map(([id, ac, lines, st]) =>
    mk(id, 'char', 'S', ac, [{ type: 'zone', fill: 'bone', lines, size: 124, h: 700, icon: 'users', grow: 1 }], { aud: 'students', sticker: st })),
  mk('BB1', 'char', 'F', 'orange', [
    H({ eyebrow: 'Tuition in Kolkata', lines: L('Every subject, / *every class*'), size: 116, mascot: { ...EYES, size: 280 }, grow: .9 }),
    { type: 'bento', fill: 'bone', tiles: [{ label: 'Commission', big: '₹0', fill: 'card', icon: 'heart', h: 240 }, { label: 'Classes', big: 'IV to XII', fill: 'orange', icon: 'book', h: 240 }, { label: 'Checked by', big: 'A human', fill: 'indigo', icon: 'shield', h: 240, size: 84 }, { label: 'To contact', big: 'Free', fill: 'mint', icon: 'chat', h: 240 }], grow: 1.6 },
  ], { aud: 'all' }),
];
