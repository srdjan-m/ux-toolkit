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

## 5. Palette and harmony

Contrast decides whether a palette *works*; this section is about whether it *looks*
designed. Judge it with numbers from `ux_measure.py oklch HEX ...` (OKLCH: L =
perceived lightness 0–1, C = chroma/colourfulness, H = hue angle), not by eye.

**What makes a UI palette read as harmonious.** It's mostly not the hue wheel:
- **Restraint.** Neutrals carry most of the surface; one accent hue carries "primary";
  status hues appear only where they mean something. Rough guide: ~60 % neutral
  surfaces, ~30 % secondary surfaces/text, ~10 % accent. Three or more saturated hues
  competing on one screen is a finding.
- **Matched lightness and chroma.** Colours used side by side in the same role (chart
  series, badges, category tags, status set) should sit close in L and C, differing
  mainly in hue. Check the spread `oklch` reports. One badge visibly louder than its
  siblings (L or C far off the group) reads as a mistake or as false emphasis.
- **Tinted neutrals.** Greys pulled slightly toward the accent hue (C ≈ 0.005–0.02)
  look intentional; pure greys next to a warm accent can look dirty. Neutrals that
  drift between warm and cool across the UI are a Polish finding.
- **Tonal scales, not one-offs.** Each hue used for UI states (hover, pressed,
  selected, subtle background) should come from one scale with even L steps. Hover
  colours picked ad hoc are a finding: name the scale step to use.
- **Status hues stay apart from the accent.** If the brand accent is red or orange,
  error and warning lose meaning; if it's green, so does success. Keep ≥ ~40° of hue
  between accent and the nearest status hue, or change the status cue (icon + label).
- **Dark mode lowers chroma.** The same hue at the same C looks louder on dark; expect
  dark-theme accents at somewhat lower C and higher L than the light theme.

**Hue-wheel harmonies are starting points, not rules.** Use them when a palette needs
a *new* hue (a second accent, chart series, illustration colours):

| Scheme | Hues (offset from base) | Good for |
|---|---|---|
| Analogous | −30°, 0, +30° | Calm, related categories; chart series of one family |
| Complementary | 0, 180° | One accent against a base; strong contrast, use sparingly |
| Split complementary | 0, 150°, 210° | Accent plus two supports, less harsh than complementary |
| Triadic | 0, 120°, 240° | Categorical data with 3 distinct series |
| Tetradic (square) | 0, 90°, 180°, 270° | 4 categorical series; needs one dominant hue |

`ux_measure.py harmony BASE [--scheme NAME]` builds these in OKLCH, keeping the base's
L and C (reducing C only where a hue can't reach it in sRGB) and printing the text
contrast on each colour. Then still check each pair you'll actually use with
`contrast`, and check colour-blind separation (§2): harmonious hues can still collapse
for red/green deficiency.

**Recommending a better palette.** In a project with a design system, recommend
existing tokens or scale steps first; a colour the system lacks is raised as a gap,
marked as a local value, never silently invented. Without a system, propose a small,
complete set (neutral scale, one accent scale, four status colours), each given as hex
with its OKLCH and the contrast it achieves in the role it's meant for. A palette
critique is usually Polish or Minor; it's Major only when it hurts meaning (status
confusion, false emphasis, chart series that can't be told apart).

## 6. Report language

Give the measured value and the target, and a fix that keeps the design intent:
"Helper text #8A8F98 on #FFFFFF = 3.25:1 — fails 1.4.3 (4.5:1). `text-secondary`
(#5F6672, 5.78:1) keeps the muted look and passes."
