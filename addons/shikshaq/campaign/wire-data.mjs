// Wire the owner's Supabase export into campaign/data.json, then every gated slot fills on the next build.
//   1. run the queries in campaign/queries.sql and save each result as JSON under campaign/import/
//   2. put the approved tutors in campaign/import/tutors.json:  [{"name","subject","quote","photo"?,"approved":true}]
//   3. node campaign/wire-data.mjs [--attribution=initial|first|role]
//   4. node campaign/build.mjs --final
// Reviews are quoted exactly. By default the reviewer shows as an initial, because the authors are school students.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url)), imp = f => path.join(here, 'import', f);
const arg = k => (process.argv.find(a => a.startsWith(`--${k}=`)) || '').split('=')[1];
const attribution = arg('attribution') || 'initial';

// accepts a plain array, {rows:[...]}, or the connector's wrapped text
export function rows(file) {
  if (!fs.existsSync(file)) return null;
  let j = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (typeof j === 'string') { const m = j.match(/(\[[\s\S]*\])/); j = m ? JSON.parse(m[1]) : []; }
  if (Array.isArray(j)) return j;
  if (Array.isArray(j.rows)) return j.rows;
  if (Array.isArray(j.result)) return j.result;
  return [];
}
const SUBJECTS = ['Maths', 'Science', 'English', 'Commerce', 'Computer', 'Hindi', 'History', 'Geography'];
export const pickSubject = s => SUBJECTS.find(x => new RegExp(x === 'Maths' ? 'math' : x, 'i').test(s || '')) || SUBJECTS.find(x => (s || '').toLowerCase().includes(x.toLowerCase())) || 'Maths';
export function byline(r, mode) {
  const first = (r.full_name || '').trim().split(/\s+/)[0];
  if (r.is_anonymous || !first) return 'A parent';
  if (mode === 'first') return first;
  if (mode === 'role') return 'A student';
  return first[0].toUpperCase() + '.';
}

function main() {
  const live = path.join(here, 'data.json'), tpl = path.join(here, 'data.template.json');
  const data = JSON.parse(fs.readFileSync(fs.existsSync(live) ? live : tpl, 'utf8'));
  const rv = rows(imp('reviews.json'));
  if (rv) data.reviews = rv.filter(r => r.comment && r.id).slice(0, 12).map(r => ({ id: r.id, text: r.comment.trim(), first: byline(r, attribution), subject: pickSubject(r.subject), cls: '', rating: r.rating ?? null, source: `teacher_comments:${r.id}` }));
  const ar = rows(imp('areas.json'));
  if (ar) data.areas = ar.map(r => String(r.location).split(',')[0].trim()).filter((v, i, a) => v && a.indexOf(v) === i).slice(0, 6);
  const ct = rows(imp('counts.json'));
  if (ct && ct[0]) data.counts = ct[0];
  const tt = rows(imp('tutors.json'));
  if (tt) data.tutors = tt.filter(t => t.name && t.quote).map(t => ({ name: t.name, subject: pickSubject(t.subject), quote: t.quote, photo: t.photo || null, approved: t.approved === true }));
  data.attribution = attribution;
  data.mode = (data.reviews?.length || data.tutors?.length) ? 'live' : 'placeholder';
  data.asOf = new Date().toISOString().slice(0, 10);
  fs.writeFileSync(path.join(here, 'data.json'), JSON.stringify(data, null, 1));
  console.log(`reviews ${data.reviews.length} . tutors ${data.tutors.length} (${data.tutors.filter(t => t.approved).length} approved) . areas ${data.areas.length} . attribution ${attribution}`);
}
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) main();
