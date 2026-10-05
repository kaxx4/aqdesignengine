import { renderPlan } from './render.mjs';
const post = { day: 'Demo', template: 'bento-board', accent: 'orange', cta: 'Find a teacher', search: { subject: 'Maths', cls: 'Class 10', area: 'Salt Lake' },
  copy: { plain: 'Find your', bold: 'teacher.', sub: 'Search by subject, class and area. Message on WhatsApp.' } };
const r = await renderPlan({ posts: [post] }, new URL('../out/demo-bento', import.meta.url).pathname);
console.log(r[0].file); r[0].issues.forEach(i => console.log('  ' + i)); if (!r[0].issues.length) console.log('  gates clean');
