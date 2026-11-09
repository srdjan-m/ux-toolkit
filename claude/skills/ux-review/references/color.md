# Colour — review checklist

Always **measure** contrast with `scripts/ux_measure.py contrast FG BG` — never judge
it by eye. Get exact hex values from Figma (`get_design_context`) or the code; a
screenshot's pixels shift with compression and anti-aliasing, so mark values sampled
from a screenshot as *Estimated*.

## 1. Contrast (hard rules)

| Element | WCAG 2.2 AA | Voting (VVSG 2.0) |
|---|---|---|
| Body text | ≥ 4.5:1 (1.4.3) | ≥ 10:1 default (7.1-C) |
| Large text (≥ 24 px / ≥ 18.66 px bold) | ≥ 3:1 | ≥ 10:1 |
| UI component boundaries, meaningful icons, focus ring, selected-state indicator | ≥ 3:1 vs adjacent colour (1.4.11) | ≥ 10:1 incl. marking-target outline |
| High / low contrast modes | — | required options (7.1-D): ≥ 20:1, yellow/cyan/white on black ≥ 17.5/15/18:1, low 4.5–8:1 |

Check the hard cases, not just the main text: placeholder text, helper text, disabled
look-alikes that are actually active, text on images or gradients (measure the worst
spot), text on coloured buttons, links in body text, chart labels, focus rings on both
light and dark surfaces.

## 2. Colour is never the only signal (WCAG 1.4.1, VVSG 7.1-F)

- Selected vs unselected, error vs valid, required, link vs text, chart series, status
  badges — each needs a second cue: icon, text, shape, underline, pattern, position.
- Quick test: describe the screen as if in greyscale. Anything you can no longer tell
  apart is a finding.
- Colour-blind safety: red/green is the most common confusion (≈ 8 % of men). Never pair
  them as the only difference; blue/orange is a safer pair.

## 3. Meaning and roles

- Colours map to **roles** (primary action, surface, text, border, success, warning,
  error, info), defined as tokens. A raw hex in a design that isn't a token is a finding:
  name the token it should use.
- Status colours follow convention — VVSG 7.1-E makes it a rule for voting: green / blue
  / white = information or normal; amber / yellow = warning; red = error or urgent. Red
  for a neutral or primary action is a finding.
- One primary-action colour per screen region. If three things are "brand blue", none
  is the primary.
- Destructive actions are distinguishable from primary ones (not the same filled style).

## 4. Surfaces and dark mode

- Dark mode is not inverted light mode: avoid pure #000 backgrounds behind long text
  for general products (halation for astigmatic users) — use near-black, and reduce
  saturated colours, which vibrate on dark. (Voting high-contrast modes are a deliberate
  exception: 7.1-D specifies #000000–#111111.)
- Elevation in dark mode is shown by lighter surfaces, not shadows.
- Every state (hover, focus, pressed, selected, disabled, error) must be defined in
  *every* theme — missing states in the dark theme are a frequent gap.

## 5. Report language

Give the measured value and the target, and a fix that keeps the design intent:
"Helper text #8A8F98 on #FFFFFF = 3.25:1 — fails 1.4.3 (4.5:1). `text-secondary`
(#5F6672, 5.78:1) keeps the muted look and passes."
