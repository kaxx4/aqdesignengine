"""Shared Diwali scene-diya: big layered flame over a half-round bowl whose body is a lit night scene
(candles, arch gateway with garland, hanging lanterns, string lights, sparkler figures).
Original drawing (idea only taken from a user-supplied reference). Palette-driven so each brand
passes its own colours. viewBox 0 0 1000 840."""
import random
def scene(P, uid="a"):
    r = random.Random(7); ink=P["ink"]; sw=P.get("sw",0); st=f'stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ''
    o = []
    A = o.append
    A(f'<defs><clipPath id="bowl{uid}"><path d="M50 412 A450 378 0 0 0 950 412 Z"/></clipPath></defs>')
    # ground shadow
    A(f'<ellipse cx="500" cy="806" rx="400" ry="30" fill="{P["ground_shadow"]}"/>')
    if P.get("hard"):
        A(f'<g transform="translate(14,14)" fill="{P.get('shadow', ink)}"><path d="M500 0 C430 120 380 190 380 250 A120 120 0 0 0 620 250 C620 190 570 120 500 0Z"/><path d="M50 412 A450 378 0 0 0 950 412 Z"/></g>')
    # flame
    A(f'<path d="M500 0 C430 120 380 190 380 250 A120 120 0 0 0 620 250 C620 190 570 120 500 0Z" fill="{P["night"]}" {st}/>')
    for _ in range(46):
        x=r.uniform(400,600); y=r.uniform(40,260)
        if ((x-500)/125)**2+((y-250)/130)**2 < 1 or y<170: A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.6,2.2,3])}" fill="{P["star"]}"/>')
    for k,(c,s) in enumerate([(P["f1"],1),(P["f2"],.74),(P["f3"],.5)]):
        A(f'<path transform="translate(500 262) scale({s}) translate(-500 -262)" d="M500 150 C470 200 440 240 440 275 A60 60 0 0 0 560 275 C560 240 530 200 500 150Z" fill="{c}" {st if k==0 else ""}/>')
    A(f'<line x1="500" y1="330" x2="500" y2="376" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>')
    # bowl body
    A(f'<path d="M50 412 A450 378 0 0 0 950 412 Z" fill="{P["night"]}" {st}/>')
    A(f'<g clip-path="url(#bowl{uid})">')
    # side lower tint + stripes
    A(f'<rect x="50" y="600" width="900" height="200" fill="{P["sand"]}"/>')
    for x in range(54,950,12): A(f'<line x1="{x}" y1="604" x2="{x}" y2="800" stroke="{P["sand2"]}" stroke-width="2"/>')
    # sky stars both sides
    for _ in range(70):
        x=r.uniform(60,940); y=r.uniform(420,590)
        if not 340<x<660: A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.4,2,2.6])}" fill="{P["star"]}"/>')
    # wave hills behind figures
    for x0 in (50,660):
        A(f'<path d="M{x0} 560 q40 -22 80 0 t80 0 t80 0 t80 0 V600 H{x0} Z" fill="{P["hill"]}"/>')
    # string lights band
    A(f'<rect x="50" y="596" width="900" height="9" fill="{P["bulb"]}"/>')
    # candles
    def candle(x,w,h,c):
        A(f'<rect x="{x}" y="{596-h}" width="{w}" height="{h}" rx="4" fill="{c}" {st and f"stroke=\"{ink}\" stroke-width=\"{sw*.6}\""}/>')
        fy=596-h-8
        A(f'<path d="M{x+w/2} {fy-34} C{x+w/2-20} {fy-10} {x+w/2-14} {fy+6} {x+w/2} {fy+6} C{x+w/2+14} {fy+6} {x+w/2+20} {fy-10} {x+w/2} {fy-34}Z" fill="{P["f2"]}"/>')
        A(f'<path d="M{x+w/2} {fy-20} C{x+w/2-8} {fy-8} {x+w/2-6} {fy+2} {x+w/2} {fy+2} C{x+w/2+6} {fy+2} {x+w/2+8} {fy-8} {x+w/2} {fy-20}Z" fill="{P["f3"]}"/>')
    candle(118,42,88,P["candle1"]); candle(166,34,66,P["candle2"]); candle(270,46,96,P["candle1"])
    candle(700,34,70,P["candle2"]); candle(740,34,84,P["candle1"]); candle(780,34,62,P["candle2"])
    # figures
    def person(x,cloth,skin,raise_arm=None):
        A(f'<circle cx="{x}" cy="520" r="15" fill="{P["skin"]}"/>')
        A(f'<path d="M{x-20} 596 L{x-14} 538 Q{x} 528 {x+14} 538 L{x+20} 596Z" fill="{cloth}"/>')
        A(f'<rect x="{x-12}" y="596" width="9" height="4" fill="{ink}"/><rect x="{x+3}" y="596" width="9" height="4" fill="{ink}"/>')
    person(225,P["cloth1"],0); person(852,P["cloth2"],0)
    A(f'<path d="M231 534 L249 498" stroke="{P["cloth1"]}" stroke-width="9" stroke-linecap="round"/><rect x="240" y="474" width="20" height="26" rx="5" fill="{P["lantern_up"]}"/>')
    A(f'<path d="M846 538 L822 528" stroke="{P["cloth2"]}" stroke-width="9" stroke-linecap="round"/>')
    for a in range(0,360,45): A(f'<line x1="816" y1="524" x2="{816+11*__import__("math").cos(a*3.14159/180):.1f}" y2="{524+11*__import__("math").sin(a*3.14159/180):.1f}" stroke="{P["bulb"]}" stroke-width="2.5"/>')
    # centre: tile + diamond window with diyas
    A(f'<rect x="340" y="412" width="320" height="190" fill="{P["tile"]}"/>')
    A(f'<path d="M500 440 L612 520 L500 600 L388 520Z" fill="{P["night"]}"/>')
    for dx in (-44,0,44):
        A(f'<path d="M{500+dx-16} 560 q16 22 32 0Z" fill="{P["candle1"]}"/><path d="M{500+dx} 536 q-9 12 0 22 q9 -10 0 -22Z" fill="{P["f2"]}"/>')
    # balustrade + building
    A(f'<rect x="340" y="596" width="320" height="26" fill="{P["bal"]}"/>')
    for x in range(352,650,20): A(f'<rect x="{x}" y="602" width="6" height="14" fill="{P["night"]}" opacity=".85"/>')
    A(f'<rect x="340" y="622" width="320" height="180" fill="{P["wall"]}"/>')
    for y in range(640,800,14): A(f'<line x1="340" y1="{y}" x2="660" y2="{y}" stroke="{P["wall2"]}" stroke-width="2"/>')
    A(f'<path d="M400 800 V700 A100 100 0 0 1 600 700 V800Z" fill="{P["night"]}"/>')
    A(f'<path d="M412 800 V702 A88 88 0 0 1 588 702 V800" fill="none" stroke="{P["bulb"]}" stroke-width="3"/>')
    A(f'<path d="M430 684 Q500 740 570 684" fill="none" stroke="{P["star"]}" stroke-width="2" stroke-dasharray="1 7" stroke-linecap="round"/>')
    for sx in (372,628):
        for i in range(6): A(f'<circle cx="{sx+(-4 if i%2 else 4)}" cy="{650+i*24}" r="9" fill="{P["flower"]}"/>')
    for dx in (-70,0,70):
        A(f'<path d="M{500+dx-18} 782 q18 -26 36 0Z" fill="{P["candle1"]}"/><path d="M{500+dx} 746 q-9 14 0 26 q9 -12 0 -26Z" fill="{P["f2"]}"/>')
    # lanterns + swags on side lower zone
    for x,y,c in [(235,650,P["lan1"]),(298,690,P["lan2"]),(765,650,P["lan2"]),(702,690,P["lan1"])]:
        A(f'<line x1="{x}" y1="610" x2="{x}" y2="{y-20}" stroke="{ink}" stroke-width="2"/>')
        A(f'<path d="M{x} {y-20} l16 20 l-16 24 l-16 -24Z" fill="{c}"/>')
    for x0,x1 in ((110,300),(700,890)):
        A(f'<path d="M{x0} 614 Q{(x0+x1)/2} 690 {x1} 614" fill="none" stroke="{P["bulb"]}" stroke-width="3" stroke-dasharray="1 9" stroke-linecap="round"/>')
    A('</g>')
    # rim
    A(f'<rect x="30" y="372" width="940" height="42" rx="21" fill="{P["rim"]}" {st}/>')
    for x in range(64,950,30): A(f'<circle cx="{x}" cy="393" r="6.5" fill="{P["rim_bead"]}"/>')
    return f'<svg viewBox="-20 -10 1040 850" xmlns="http://www.w3.org/2000/svg">{"".join(o)}</svg>'
