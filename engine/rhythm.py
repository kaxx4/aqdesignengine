# AQ RHYTHM ENGINE — bands are placed by a computed vertical cadence, never hand-typed y-values.
# A poster is a STACK of bands. Each band declares its height; the engine spaces them on a fixed beat.
M=64; W=1080; H=1350
TOP=176          # first band baseline (under logo/eyebrow zone)
BOTTOM=1290      # last usable y (above CTA at ~1294)
UNIT=8           # baseline grid unit
def snap(v): return round(v/UNIT)*UNIT

class Stack:
    """Places bands top->bottom with a consistent GAP between them (a multiple of UNIT).
       If content is shorter than the canvas, distributes SLACK evenly so rhythm stays even."""
    def __init__(self, top=TOP, bottom=BOTTOM, gap=48):
        self.top=top; self.bottom=bottom; self.gap=snap(gap); self.bands=[]
    def add(self, name, height, gap_after=None):
        self.bands.append({"name":name,"h":snap(height),"gap":snap(gap_after) if gap_after else self.gap})
        return self
    def layout(self):
        # total content height + gaps
        n=len(self.bands)
        content=sum(b["h"] for b in self.bands)
        gaps=sum(self.bands[i]["gap"] for i in range(n-1))
        used=content+gaps
        avail=self.bottom-self.top
        slack=avail-used
        # distribute slack across gaps so the stack fills the canvas with EVEN rhythm
        extra = snap(slack/(n-1)) if n>1 and slack>0 else 0
        y=self.top; pos={}
        for i,b in enumerate(self.bands):
            pos[b["name"]]=y
            y += b["h"] + (b["gap"]+extra if i<n-1 else 0)
        # rule line sits at the midpoint of each gap for consistent divider rhythm
        rules={}
        y=self.top
        for i,b in enumerate(self.bands):
            y2=y+b["h"]
            if i<n-1:
                g=b["gap"]+extra
                rules[b["name"]]=snap(y2+g/2)
            y=y2+(b["gap"]+extra if i<n-1 else 0)
        return pos, rules, extra
