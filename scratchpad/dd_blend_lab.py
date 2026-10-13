"""DISCO DIWALI blend-mode and shader lab: a full-screen navy diya pattern as the ground, a BLUE layer composited over it.

Six recipes on the same announce poster (feed), each a different way of layering the blue:
  v1 dodge     colour-dodge blue light burning the gold up        v4 shimmer  heat-haze displacement + soft-light blue + RGB-split title
  v2 overlay   overlay blue grade, gold lifted by lighten          v5 invert   difference blend flips gold to pink-blue
  v3 duotone   SVG luminance remap navy->gold, screen blue glow    v6 rays     repeating-conic disco beams, screen-blended

Every layer is tagged "plate" so the gate treats it as deliberate full bleed. The skeleton (mask, title, type, CTA, sparkles, grain)
comes from engine/discodiwali.py unchanged; only base() and the title filter differ.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_blend_lab.py [v1 v2 ...]
"""
import asyncio, importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)

VARIANT = "v1"
SVG_DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="ca" x="-4%" y="-4%" width="108%" height="108%" color-interpolation-filters="sRGB">
  <feColorMatrix in="SourceGraphic" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r"/>
  <feColorMatrix in="SourceGraphic" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
  <feColorMatrix in="SourceGraphic" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b"/>
  <feOffset in="r" dx="-3" dy="0" result="ro"/><feOffset in="b" dx="3" dy="0" result="bo"/>
  <feBlend in="ro" in2="g" mode="screen" result="rg"/><feBlend in="rg" in2="bo" mode="screen"/>
</filter>
<filter id="heat" x="-2%" y="-2%" width="104%" height="104%">
  <feTurbulence type="fractalNoise" baseFrequency="0.010 0.032" numOctaves="2" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="34" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="duo" color-interpolation-filters="sRGB">
  <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 1 0"/>
  <feComponentTransfer>
    <feFuncR type="table" tableValues="0.01 0.05 0.78 1"/>
    <feFuncG type="table" tableValues="0.02 0.10 0.55 0.88"/>
    <feFuncB type="table" tableValues="0.10 0.42 0.16 0.55"/>
  </feComponentTransfer>
</filter></defs></svg>"""


def layer(style, tag="plate", z=1):
    return f'<div data-tag="{tag}" style="position:absolute;inset:0;z-index:{z};pointer-events:none;{style}"></div>'


class LabPoster(dd.Poster):
    def base(self):
        W, H, P = self.W, self.H, self.parts
        pat = dd.uri("pattern_diya_navy.jpg")
        P.append(f'<div style="position:absolute;inset:0;background:#000"></div>' + SVG_DEFS)

        def bg(extra="", z=1):
            P.append(f'<img data-tag="plate" src="{pat}" style="position:absolute;left:{-(H - W) // 2}px;top:0;width:{H}px;height:{H}px;'
                     f'object-fit:cover;z-index:{z};{extra}">')

        # the type zone always gets dimmed, so the pattern lives in the corners (format rule 3)
        dim = layer("background:radial-gradient(ellipse 62% 44% at 50% 64%,rgba(0,0,0,.86),rgba(0,0,0,.55) 62%,rgba(0,0,0,.05) 100%)", z=4)
        v = VARIANT
        if v == "v1":      # colour-dodge: blue light that burns the gold and blooms the whites
            bg("filter:brightness(.7) saturate(1.15);")
            P.append(layer("background:radial-gradient(circle at 82% 10%,#3D7BFF 0%,rgba(20,60,220,.0) 58%),linear-gradient(165deg,#1038FF,#001060 70%);"
                           "mix-blend-mode:color-dodge;opacity:.62", z=2))
            P.append(dim)
        elif v == "v2":    # overlay grade + lighten: blue pulls the whole field cool while gold stays warm
            bg("filter:contrast(1.1);")
            P.append(layer("background:linear-gradient(180deg,#2A66FF 0%,#0B1E96 100%);mix-blend-mode:overlay;opacity:.95", z=2))
            P.append(layer("background:radial-gradient(circle at 12% 92%,rgba(255,170,60,.55),transparent 55%);mix-blend-mode:lighten", z=3))
            P.append(dim)
        elif v == "v3":    # SVG duotone shader: luminance remapped navy->gold, blue screened over the shadows
            bg("filter:url(#duo) brightness(1.1);")
            P.append(layer("background:radial-gradient(circle at 20% 15%,#2B5CFF,rgba(10,30,150,0) 65%),radial-gradient(circle at 88% 85%,#00B3FF,rgba(0,40,160,0) 55%);"
                           "mix-blend-mode:screen;opacity:.55", z=2))
            P.append(dim)
        elif v == "v4":    # heat-haze displacement shader + soft-light blue
            bg("filter:url(#heat) saturate(1.2) brightness(.9);transform:scale(1.06);")
            P.append(layer("background:linear-gradient(200deg,#3A7BFF,#0A1670 75%);mix-blend-mode:soft-light;opacity:1", z=2))
            P.append(layer("background:radial-gradient(circle at 50% 100%,rgba(60,140,255,.5),transparent 60%);mix-blend-mode:screen", z=3))
            P.append(dim)
        elif v == "v5":    # difference: the blue subtracts from the pattern, gold flips to pink-blue
            bg("filter:brightness(.9);")
            P.append(layer("background:#1B3CFF;mix-blend-mode:difference;opacity:.55", z=2))
            P.append(layer("background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,40,.5));mix-blend-mode:multiply", z=3))
            P.append(dim)
        elif v == "v7":    # hybrid: dodge-blue base + disco beams + a cool vignette
            bg("filter:brightness(.7) saturate(1.15);")
            P.append(layer("background:radial-gradient(circle at 82% 10%,#3D7BFF 0%,rgba(20,60,220,.0) 58%),linear-gradient(165deg,#1038FF,#001060 70%);"
                           "mix-blend-mode:color-dodge;opacity:.6", z=2))
            P.append(layer("background:repeating-conic-gradient(from 188deg at 88% -6%,rgba(120,175,255,.95) 0deg 3deg,transparent 3deg 10deg);"
                           "-webkit-mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.5) 50%,transparent 90%);"
                           "mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.5) 50%,transparent 90%);"
                           "mix-blend-mode:screen;opacity:.75", z=3))
            P.append(dim)
        elif v in ("v8", "v9"):   # calmer: darker pattern, weaker blue, beams soft (v8) or gone (v9)
            bg("filter:brightness(.5) saturate(1.0);")
            P.append(layer("background:radial-gradient(circle at 82% 10%,#3D7BFF 0%,rgba(20,60,220,.0) 58%),linear-gradient(165deg,#1038FF,#001060 70%);"
                           "mix-blend-mode:color-dodge;opacity:.38", z=2))
            if v == "v8":
                P.append(layer("background:repeating-conic-gradient(from 188deg at 88% -6%,rgba(120,175,255,.9) 0deg 2deg,transparent 2deg 12deg);"
                               "-webkit-mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.4) 45%,transparent 80%);"
                               "mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.4) 45%,transparent 80%);"
                               "mix-blend-mode:screen;opacity:.4", z=3))
            P.append(dim)
        elif v == "v6":    # repeating-conic disco beams from the top right, screened over the pattern
            bg("filter:brightness(.62) saturate(1.1);")
            P.append(layer("background:repeating-conic-gradient(from 188deg at 88% -6%,rgba(90,150,255,.9) 0deg 3.4deg,transparent 3.4deg 11deg);"
                           "-webkit-mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.55) 55%,transparent 95%);"
                           "mask-image:radial-gradient(circle at 88% -6%,#000 0,rgba(0,0,0,.55) 55%,transparent 95%);"
                           "mix-blend-mode:screen;opacity:.8", z=2))
            P.append(layer("background:radial-gradient(circle at 88% -6%,rgba(120,170,255,.55),transparent 42%);mix-blend-mode:screen", z=3))
            P.append(dim)

    def title(self, scale=1.0, cx_shift=0, y_ref=390):
        super().title(scale, cx_shift, y_ref)
        if VARIANT in ("v4", "v6", "v3", "v7"):                       # RGB-split the lockup on the shader recipes
            self.parts[-1] = self.parts[-1].replace('style="', 'style="filter:url(#ca);', 1)


dd.Poster = LabPoster
CONTENT = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards",
               status="Ticket sales open soon", note="More details soon", cta="Link in bio")


async def main():
    global VARIANT
    want = sys.argv[1:] or ["v1", "v2", "v3", "v4", "v5", "v6"]
    out = os.path.join(ROOT, "out", "discodiwali", "blendlab")
    async with dd.B.session():
        for v in want:
            VARIANT = v
            await dd.render_poster("announce", CONTENT, "feed", os.path.join(out, f"{v}.png"), style="plate", mask="copper")
    print("lab done ->", out)

asyncio.run(main())
