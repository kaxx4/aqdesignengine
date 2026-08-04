# MEASURE, don't guess (learned the hard way on Mershe/WeWon bottoms)

When a piece has dead space, DON'T eyeball pixel fixes — MEASURE:
- PIL row-band fill scan: divide canvas into 5% bands, compute fill ratio per band vs bg color, find bands <0.15 = dead zones.
- Playwright eval_on_selector_all to get exact element bottoms in CSS px, find the largest gap between last element and footer.
- A tall dead gutter at the bottom = top-weighted layout; fix by EXTENDING elements down (grow card heights, push hero type lower) to reach ~within 60-100px of footer, not by dropping a doodle in the hole.
- Bottom bands/cards should reach toward the footer; target content fill to ~88-90% of height before the footer margin.
This measure-then-place loop is exactly what the auto-filler should automate.

## See also
- [[Decisions Index]]
- (no direct cross-link identified)
