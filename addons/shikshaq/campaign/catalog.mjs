// The whole campaign as data. Build order follows the owner's ruling: the FAQ highlight first.
import { faq, tfaq, hero, steps, chat, parents } from './catalog-a.mjs';
import { char, subjects, who, proof, tutors, season, close, covers, wq } from './catalog-b.mjs';

export const FAMILIES = [
  ['faq', 'FAQ highlight (parents and students)'], ['tfaq', 'FAQ highlight (for tutors)'], ['hero', 'Anchor'], ['steps', 'Find your tutor in three steps'],
  ['chat', 'The chat at home'], ['parents', 'Student to parent'], ['char', 'Character stories'], ['subjects', 'Subject posters'], ['who', 'Who made it'],
  ['proof', 'Proof (reviews and tutors)'], ['tutors', 'Tutor side'], ['season', 'Season and calendar'], ['close', 'Week 4 close'], ['covers', 'Highlight covers'], ['wa', 'WhatsApp squares'],
];
export const ITEMS = [...faq, ...tfaq, ...hero, ...steps, ...chat, ...parents, ...char, ...subjects, ...who, ...proof, ...tutors, ...season, ...close, ...covers, ...wq];
export const byId = id => ITEMS.find(i => i.id === id);
// A plan token is an asset id OR a post id; a post id expands to every slide.
export const expand = tok => ITEMS.filter(i => i.id === tok || i.post === tok);
