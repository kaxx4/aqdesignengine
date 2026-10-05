import { C, SUBJECT_SEEDS, subjectPalette, textOn } from '../tokens.mjs';
import { page, card, box, mascot, logoBar, handle, headline, ctaBar, frame, esc, sticker, DEFAULT_STYLE, ground } from '../kit.mjs';

// The eight-subject pastel mosaic: the biggest colour source on the site.
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const { a } = frame(post.accent), c = post.copy;
  const names = Object.keys(SUBJECT_SEEDS), tiles = [];
  if (S.shuffle) { let t = (S.seed || 1) >>> 0; const rnd = () => { t += 0x6D2B79F5; let x = Math.imul(t ^ (t >>> 15), 1 | t); x ^= x + Math.imul(x ^ (x >>> 7), 61 | x); return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; for (let i = names.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [names[i], names[j]] = [names[j], names[i]]; } }
  names.forEach((n, i) => {
    const pal = subjectPalette(n), col = i % 2, row = Math.floor(i / 2);
    const x = 48 + col * 502, y = 424 + row * 160;
    const count = post.subjectCounts && post.subjectCounts[n];
    tiles.push(card('tile-' + n, x, y, 482, 140, pal.tint, { r: 20, ring: S.ground !== 'bone', inner:
      `<div style="position:absolute;left:24px;top:30px;width:80px;height:80px;border-radius:16px;background:${pal.solid};color:${textOn(pal.solid)};display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;letter-spacing:-.04em">${esc(n[0])}</div>
       <div data-fit="26" style="position:absolute;left:124px;top:${count ? 34 : 48}px;width:208px;height:48px;font-size:44px;font-weight:700;letter-spacing:-.045em;color:${pal.text};line-height:1">${esc(n)}</div>
       ${count ? `<div style="position:absolute;left:124px;top:84px;font-size:26px;font-weight:500;color:${pal.meta}">${count} papers</div>` : ''}` }));
  });
  const fi = names.indexOf(post.featuredSubject);
  const parts = [
    logoBar(48, 44),
    headline(48, 132, 984, c.plain, c.bold, 112),
    c.sub ? `<div class="a" data-tag="sub" data-fit="22" style="left:48px;top:374px;width:984px;height:44px;font-size:32px;font-weight:500;color:${C.prose};letter-spacing:-.02em">${esc(c.sub)}</div>` : '',
    ...tiles,
    sticker('stk', 48 + (fi % 2) * 502 + 340, 424 + Math.floor(fi / 2) * 160 + 52, 'start here', a, (fi % 2 ? -4 : 4) * S.stickerSign, 22),
    mascot('m1', S.kit.shapes[3], 874, 1100, 150, C.mintSolid, S.kit.moods[1], 6),
    ctaBar(1100, post.cta, a, { w: 800, variant: S.cta }),
    handle(52, 1254),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
