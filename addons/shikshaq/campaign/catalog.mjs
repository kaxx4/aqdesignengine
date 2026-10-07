// The whole campaign as data. Build order follows the owner's ruling: the FAQ highlight first.
import { faq, tfaq, hero, steps, chat, parents, char } from './catalog3a.mjs';
import { subjects, who, proof, tutors, season, close, covers, wq, say, ask, msg, exam, cls, way, facts, stickers } from './catalog3b.mjs';

export const FAMILIES = [
  ['faq', 'FAQ highlight (parents and students)'], ['tfaq', 'FAQ highlight (for tutors)'], ['hero', 'Anchor'], ['steps', 'Find your tutor in three steps'],
  ['chat', 'The chat at home'], ['parents', 'Student to parent'], ['char', 'Character stories'], ['subjects', 'Subject posters'], ['who', 'Who made it'],
  ['say', 'Things parents say'], ['ask', 'Questions to ask a tutor'], ['msg', 'Copy this message'], ['exam', 'Exam season'], ['class', 'By the class'], ['way', 'Wayfinding'], ['facts', 'The facts, plainly'],
  ['proof', 'Proof (reviews and tutors)'], ['tutors', 'Tutor side'], ['season', 'Season and calendar'], ['close', 'Week 4 close'], ['covers', 'Highlight covers'], ['stickers', 'WhatsApp stickers'], ['wa', 'WhatsApp squares'],
];
export const ITEMS = [...faq, ...tfaq, ...hero, ...steps, ...chat, ...parents, ...char, ...subjects, ...who, ...say, ...ask, ...msg, ...exam, ...cls, ...way, ...facts, ...proof, ...tutors, ...season, ...close, ...covers, ...stickers, ...wq];
export const byId = id => ITEMS.find(i => i.id === id);
// A plan token is an asset id OR a post id; a post id expands to every slide.
export const expand = tok => ITEMS.filter(i => i.id === tok || i.post === tok);
