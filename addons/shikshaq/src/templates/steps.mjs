import { C, SUBJECT_SEEDS, subjectPalette, textOn } from '../tokens.mjs';
import { page, card, mascot, logoBar, handle, headline, ctaBar, frame, esc, DEFAULT_STYLE, ground } from '../kit.mjs';

// Three stacked cards, each in a different subject tint, numbered in its own solid.
export function render(post, W, H) {
  const S = post.style || DEFAULT_STYLE;
  const { a } = frame(post.accent), c = post.copy;
  const order = post.stepSubjects, shapes = S.kit.shapes.slice(0, 3), moods = ['none', 'none', 'none'];
  const cards = c.steps.map((s, i) => {
    const pal = subjectPalette(order[i]), y = 424 + i * 224;
    return card('step' + i, 48, y, 984, 204, pal.tint, { r: 28, ring: S.ground !== 'bone', inner:
      `<div data-fit="22" style="position:absolute;left:200px;top:30px;width:740px;height:62px;font-size:52px;font-weight:700;letter-spacing:-.045em;line-height:1.05;color:${pal.text}">${esc(s.t)}</div>
       <div data-fit="20" style="position:absolute;left:200px;top:104px;width:740px;height:70px;font-size:34px;font-weight:500;line-height:1.2;color:${pal.meta};letter-spacing:-.02em">${esc(s.b)}</div>` })
      + mascot('n' + i, shapes[i], 56, y + 40, 120, pal.solid, moods[i], (i - 1) * 6)
      + `<div class="a d" data-tag="num${i}" data-bg="${pal.solid}" style="left:56px;top:${y + 40}px;width:120px;height:120px;display:flex;align-items:center;justify-content:center;font-size:72px;color:${textOn(pal.solid)}">${i + 1}</div>`;
  });
  const parts = [
    logoBar(48, 44),
    headline(48, 132, 984, c.plain, c.bold, 112),
    `<div class="a" data-tag="sub" data-fit="22" style="left:48px;top:374px;width:984px;height:44px;font-size:32px;font-weight:500;color:${C.prose};letter-spacing:-.02em">${esc(c.sub)}</div>`,
    ...cards,
    ctaBar(1110, post.cta, a, { variant: S.cta }),
    handle(52, 1284),
  ];
  return page(W, H, parts.join(''), ground(S, post.accent));
}
