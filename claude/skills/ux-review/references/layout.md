# Layout and visual structure — review checklist

Values marked *(guideline)* are craft conventions; hard limits are cited by ID.

## 1. Scan path and priority

- **Squint test**: blur the screen (or imagine it from across the room). The first
  thing you see should be the most important thing for the user's task. If it's a
  logo, decoration or a secondary button, that's a finding.
- One **primary action** per view, visually dominant; secondary actions clearly
  quieter. Two equal-weight buttons = the user has to think (H8).
- Reading order (F/Z pattern for LTR) matches task order: question → options → action.
- Primary action placement is consistent across the flow (same corner every time).

## 2. Grouping (Gestalt)

- **Proximity**: related items are closer to each other than to unrelated items.
  The space *between* groups must be visibly larger than the space *within* them
  *(guideline: ≥ 2×)*. A label equidistant from two fields is a finding.
- **Common region**: cards/borders group items — use them where proximity alone is
  ambiguous, not everywhere (boxes inside boxes = noise).
- **Similarity**: things that behave the same look the same; things that look the same
  must behave the same.
- Voting: each contest must read as **one** group, never two (VVSG 7.3-B) — check the
  gaps inside a contest are smaller than between contests and that a column break or
  page break doesn't split it.

## 3. Alignment and grid

- Elements align to a grid; count the distinct left edges on the screen. Many slightly
  different edges = misalignment. Name the offending element and the offset in px.
- Text baselines in a row line up; icons optically centred with text.
- Labels and controls follow one rule throughout (labels above fields, or left — not mixed).
- Marking targets in the same position relative to names across the ballot (VVSG 7.3-D).

## 4. Spacing system

- Spacing values come from a scale *(guideline: 4 or 8 px base — 4, 8, 12, 16, 24,
  32, 48…)*. Off-scale values (13 px, 22 px) are findings: name the token they should be.
- Consistent padding inside the same component type.
- Enough breathing room around touch targets: WCAG 2.5.8 spacing rule (24 px circle);
  VVSG 7.2-I ≥ 2.54 mm between voting targets, no overlap.

## 5. Density and responsiveness

- Density fits the user: expert dashboards can be dense; first-time or occasional users
  (voters!) need generous space and one task per screen.
- What happens at the narrowest and widest breakpoint, at 200 % text, and with the
  longest real content (long candidate names, long translations, 50 candidates)?
  Designs that only work with ideal short content are a finding.
- Reflow at 320 px without horizontal scroll (WCAG 1.4.10); voting: no horizontal
  scrolling up to 200 % text (VVSG 7.1-H).
- Fixed headers/footers don't hide focused content (WCAG 2.4.11) and, on long voting
  contests, keep the contest name, rule and navigation visible (VVSG 7.2-D).
- Scroll affordance: if content continues below the fold, is that obvious? (VVSG 7.2-D
  requires a clear "more options" cue.)

## 6. Report language

Point to the exact element and measurement: "Gap between 'Vote for 1' and first
candidate = 32 px, same as gap between contests → the rule reads as belonging to the
previous contest. Reduce to 12 px (`space-3`)."
