#!/usr/bin/env node
// Pulls the live facts the week plan is allowed to quote. Anon key only, the same
// structural guarantee scripts/prerender.ts relies on: it cannot read question
// bodies or teacher contacts. Writes facts/facts.live.json (gitignored).
//
// STATUS: written against the documented schema and NOT yet run against production,
// because the build sandbox cannot reach Supabase. First live run is the test.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const sampleFile = path.join(root, 'facts/facts.sample.json');
if (process.argv.includes('--offline')) { // numbers-free week: nothing quoted that we cannot source
  const smp = JSON.parse(fs.readFileSync(sampleFile, 'utf8'));
  const nul = k => ({ value: null, label: k, source: 'unavailable', verified: false });
  fs.writeFileSync(path.join(root, 'facts/facts.live.json'), JSON.stringify({ mode: 'live', asOf: new Date().toISOString().slice(0, 10), note: 'offline: no counts, no new papers', counts: { teachers: nul('teachers'), papers: nul('papers'), schools: nul('schools') }, subjects: smp.subjects, newPapers: [], constants: smp.constants }, null, 2));
  console.log('offline facts written (numbers-free week)'); process.exit(0);
}
const URL_ = process.env.VITE_SUPABASE_URL, KEY = process.env.VITE_SUPABASE_PUBLISHABLE_KEY || process.env.VITE_SUPABASE_ANON_KEY;
if (!URL_ || !KEY) { console.error('Need VITE_SUPABASE_URL and VITE_SUPABASE_PUBLISHABLE_KEY (or VITE_SUPABASE_ANON_KEY) in the environment.'); process.exit(2); }
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };
const get = async (p, init = {}) => { const r = await fetch(URL_ + p, { headers: H, ...init }); if (!r.ok) throw new Error(`${p} -> ${r.status} ${await r.text()}`); return r.json(); };

const counts = await (async () => {
  const r = await fetch(URL_ + '/rest/v1/rpc/site_counts', { method: 'POST', headers: { ...H, 'Content-Type': 'application/json' }, body: '{}' });
  if (!r.ok) throw new Error(`site_counts -> ${r.status} ${await r.text()}`);
  const row = (rows => (Array.isArray(rows) ? rows[0] : rows))(await r.json());
  const mk = (v, label, src) => ({ value: Number(v) || null, label, source: src, verified: true });
  return { teachers: mk(row.teachers, 'teachers', 'rpc site_counts'), papers: mk(row.papers, 'papers', 'rpc site_counts'), schools: mk(row.schools, 'schools', 'rpc site_counts') };
})();

const since = new Date(Date.now() - 14 * 864e5).toISOString();
const rows = await get(`/rest/v1/bank_papers?select=id,subject,cls,board,year,exam,school,has_school,question_count,created_at&is_published=eq.true&question_count=gt.0&created_at=gte.${since}&order=created_at.desc&limit=10`);
const newPapers = rows.map(r => ({ id: r.id, subject: r.subject, cls: r.cls, board: r.board, year: r.year, exam: r.exam, school: r.has_school ? r.school : null, questions: r.question_count }));
if (!newPapers.length) { // quiet fortnight: fall back to the latest paper, whatever its age
  const [r] = await get('/rest/v1/bank_papers?select=id,subject,cls,board,year,exam,school,has_school,question_count&is_published=eq.true&question_count=gt.0&order=created_at.desc&limit=1');
  if (r) newPapers.push({ id: r.id, subject: r.subject, cls: r.cls, board: r.board, year: r.year, exam: r.exam, school: r.has_school ? r.school : null, questions: r.question_count });
}
const sample = JSON.parse(fs.readFileSync(path.join(root, 'facts/facts.sample.json'), 'utf8'));
const facts = { mode: 'live', asOf: new Date().toISOString().slice(0, 10), counts, subjects: sample.subjects.map(s => ({ name: s.name, papers: null })), newPapers, constants: sample.constants };
fs.writeFileSync(path.join(root, 'facts/facts.live.json'), JSON.stringify(facts, null, 2));
console.log(`live facts written: ${counts.teachers.value} teachers, ${counts.papers.value} papers, ${newPapers.length} recent paper(s)`);
