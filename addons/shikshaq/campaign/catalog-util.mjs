// Headline mini-language and asset builders. Lines split on " / ". Inside a line:  *bold payoff*   [marker tag]   {highlight pill}
// A bold or tag run cannot span two lines: close it and reopen it (the parser throws, because a stray asterisk shipped once).
export const L = str => str.split(' / ').map(line => {
  for (const [o, c] of [['*', '*'], ['[', ']'], ['{', '}']]) if (line.split(o).length !== line.split(c).length || (o === c && (line.split(o).length - 1) % 2)) throw new Error(`unbalanced ${o}${c} in headline line "${line}"`);
  return line.split(/(\*[^*]+\*|\[[^\]]+\]|\{[^}]+\})/).filter(x => x.trim() !== '').map(tok => {
    const t = tok.trim();
    if (t[0] === '*') return { b: t.slice(1, -1) };
    if (t[0] === '[') { const [w, fill] = t.slice(1, -1).split('|'); return fill ? { tag: w, fill } : { tag: w }; }
    if (t[0] === '{') { const [w, fill] = t.slice(1, -1).split('|'); return fill ? { hl: w, fill } : { hl: w }; }
    return t;
  });
});
export const mk = (id, family, canvas, accent, panels, o = {}) => ({ id, family, dir: family, canvas, look: 'stack', accent, panels, post: o.post || id, aud: o.aud || 'all', ...o });
export const slides = (post, family, canvas, accent, arr, aud = 'all') =>
  arr.map((s, i) => mk(`${post}-${i + 1}`, family, canvas, s.accent || accent, s.panels, { post, aud, count: `${String(i + 1).padStart(2, '0')}/${String(arr.length).padStart(2, '0')}`, ...(s.o || {}) }));
export const ORIGIN = 'Made by AquaTerra, an NGO whose team are students.';
export const FREE = 'Free for families';
