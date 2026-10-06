// Binds real data into specs. A spec with `bind` is GATED: it renders from data.json, never from catalog copy.
// Missing data never becomes invented copy: the slot renders as an obvious DRAFT and the build refuses it as final.
import fs from 'node:fs';
export const DATA_PATH = new URL('./data.json', import.meta.url);        // LIVE, git-ignored: holds real people's words
const TEMPLATE = new URL('./data.template.json', import.meta.url);      // committed placeholder
export const loadData = () => JSON.parse(fs.readFileSync(fs.existsSync(DATA_PATH) ? DATA_PATH : TEMPLATE, 'utf8'));

const PH_REVIEW = { text: 'Review text pending. This slot fills from the approved reviews on the site.', first: 'Name', subject: 'Maths', cls: '' };
const PH_TUTOR = { name: 'Tutor name', subject: 'Maths', quote: 'Quote pending the tutor\'s approval.' };

export function resolveItem(item, data) {
  const it = structuredClone(item);
  it.placeholder = false;
  if (it.bind?.review != null) {
    const r = data.reviews?.[it.bind.review];
    if (r && r.text && r.id) it.review = { text: r.text, first: r.first || 'A parent', subject: r.subject || 'Maths', cls: r.cls || '' };
    else { it.review = { ...PH_REVIEW }; it.placeholder = true; }
  }
  if (it.bind?.tutor != null) {
    const t = data.tutors?.[it.bind.tutor];
    if (t && t.approved === true && t.name && t.quote) it.tutor = { name: t.name, subject: t.subject || 'Maths', quote: t.quote, photo: t.photo || null };
    else { it.tutor = { ...PH_TUTOR }; it.placeholder = true; }
  }
  if (it.bind?.areas) {
    const a = (data.areas || []).slice(0, it.bind.areas);
    if (a.length) it.words = [...it.words, ...a]; // areas are optional garnish, never a blocker
  }
  if (it.gated && !it.bind) it.placeholder = !(data.reviews?.length);
  return it;
}
// Fill {{review.N.field}} and {{tutor.N.field}} in a WhatsApp message. Returns {text, missing}.
export function fillTokens(text, data) {
  const missing = [];
  const out = text.replace(/\{\{(review|tutor)\.(\d+)\.(\w+)\}\}/g, (m, kind, i, f) => {
    const row = kind === 'review' ? data.reviews?.[+i] : (data.tutors?.[+i]?.approved ? data.tutors[+i] : null);
    const v = row?.[f];
    if (!v) { missing.push(m); return `[${kind} ${f} pending]`; }
    return v;
  });
  return { text: out, missing };
}
