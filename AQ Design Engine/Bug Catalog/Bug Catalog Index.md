# Bug Catalog Index

Every recurring visual failure class caught during the 44-sample Workflow B pass, now guarded by an encoded rule. See [[10 The Bug Catalog]] for the source table.

- [[Element clips off-canvas|Element clips off-canvas]] — seen in 6, 9, 10
- [[Doodle-badge dropped over text or shape|Doodle-badge dropped over text or shape]] — seen in 26, 27, 32
- [[Shape fill equals page bg (invisible)|Shape fill equals page bg (invisible)]] — seen in 21
- [[Text stroke approx equals bg (invisible outline)|Text stroke approx equals bg (invisible outline)]] — seen in 24
- [[var(--typo) undefined renders transparent|var(--typo) undefined renders transparent]] — seen in 32
- [[Text overflows a star or burst's narrow waist|Text overflows a star or burst's narrow waist]] — seen in 19, 44
- [[Hero scaled far too small vs the reference|Hero scaled far too small vs the reference]] — seen in 42
- [[Wide bottom-anchored child in rotated overflow parent renders blank|Wide bottom-anchored child in rotated overflow parent renders blank]] — seen in 7
- [[Stale bbox tuple hides a real off-canvas or collision|Stale bbox tuple hides a real off-canvas or collision]] — seen in 6
- [[Dead half the reference fills|Dead half the reference fills]] — seen in 15, 25, 30, 31, 39
- [[One flat color floods the field|One flat color floods the field]] — seen in (batch)
- [[Cramming a pile into one corner starves other quadrants|Cramming a pile into one corner starves other quadrants]] — seen in 87525f70

## Added after the 44-sample pass

Caught during production work rather than reference recreation — same loop, same standard.

- [[Ink outline and hard shadow on an ink field (craft layer invisible)|Ink outline and hard shadow on an ink field (craft layer invisible)]] — seen in friendship_day 01, 08
- [[Nested doodles svg inherits the parent viewBox|Nested doodles svg inherits the parent viewBox]] — seen in friendship_day 06
- [[Faint low-opacity background fields read as dirt|Faint low-opacity background fields read as dirt]] — seen in friendship_day (all slides)
- [[Stroke-drawn doodles silently discard the requested colour|Stroke-drawn doodles silently discard the requested colour]] — seen in friendship_day, and retroactively in EVERY bespoke script

[[Home]]
