# NN/g guidance: visual design, controls and data

Nielsen Norman Group recommendations, gathered 2026-11-09 from the pages linked under
each heading (all URLs confirmed then). Bullets are close paraphrases, not NN/g's exact
wording, except text in quotes. Check a figure on the live page before quoting it to a
client. Icons have their own file, `icons.md`.

**Where NN/g and other rules differ, the stricter one wins** — e.g. NN/g's 1 cm touch
target vs VVSG's 12.7 mm for voting; NN/g's light-mode default vs a design system that
has decided on dark (follow the system, note the trade-off).

## Hierarchy and visual design

[visual-hierarchy-ux-definition](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) ·
[principles-visual-design](https://www.nngroup.com/articles/principles-visual-design/) ·
[aesthetic-usability-effect](https://www.nngroup.com/articles/aesthetic-usability-effect/)
- **≤ 3 type sizes** (web guide: ~14–16 px body, 18–22 px subheads, up to 32 px heads).
  The most important element is the biggest; at most **2 "big" elements** per view.
- Bright, saturated colour for what matters, muted for the rest; keep warm/red for
  warnings, errors and destructive actions.
- Don't show hierarchy with colour alone. **Don't lower text contrast to de-emphasise**
  — it hurts legibility; use size, weight or position.
- Containers (border/background) only when whitespace can't do the grouping.
- **Blur test:** blur the design (~20 px) — the intended focal element must still stand
  out. Test with real content.
- Balance visual weight by area, not by element count.
- Aesthetic-usability effect: users forgive *minor* issues in attractive designs, not
  major ones. Never trade function for looks (e.g. a hero image that pushes content
  down). In tests, compare behaviour with ratings — a high rating after a struggle is
  this effect.

## Grouping (Gestalt)

[gestalt-proximity](https://www.nngroup.com/articles/gestalt-proximity/) ·
[gestalt-similarity](https://www.nngroup.com/articles/gestalt-similarity/) ·
[common-region](https://www.nngroup.com/articles/common-region/)
- **Proximity:** related items close, unrelated separated by whitespace; it can
  override similarity. Labels close to their own field, bigger gap before the next.
  Chunk long forms (12 fields → 3 groups of 4). Don't cluster unrelated buttons; don't
  exile an option like "Skip" to a far corner. Check stacked mobile layouts for related
  items drifting apart.
- **Similarity:** one link colour, only on clickable things. Same-coloured buttons read
  as equal — give the primary action its own colour. Different categories need
  clearly different icons; different content types shouldn't share a size (a video
  sized like an ad got ignored).
- **Common region** (border/background) beats proximity and similarity: use for cards,
  sticky headers, zebra-striped comparison rows. Prefer whitespace when it suffices;
  avoid heavy full-width bands that look like the page ends ("false floor").

## Colour

[color-enhance-design](https://www.nngroup.com/articles/color-enhance-design/) ·
[dark-mode](https://www.nngroup.com/articles/dark-mode/)
- Start with 2–3 colours; cap the palette at 3. **60-30-10:** 60 % dominant, 30 %
  secondary (both fairly neutral), 10 % accent — on the primary call to action.
- One CTA colour everywhere; never give warning red a second meaning.
- Test contrast and colour blindness; watch for grey buttons that look disabled and
  colour pairs that vibrate. Colour meanings vary across cultures — test.
- **Light mode as default for general audiences**: better acuity and proofreading for
  ages 18–33 and 60–85; the advantage grows as text gets smaller. Offer dark mode (it
  helps e.g. cataract users), on every screen, following the OS setting.
- Palette procedure and measurement: `palettes.md`; harmony theory: ux-review
  `color.md` §5.

## Readability

[legibility-readability-comprehension](https://www.nngroup.com/articles/legibility-readability-comprehension/)
- Reasonably large default size that users can change; high-contrast text on a plain
  background; clean typeface.
- Reading level: **grade 8** for broad audiences; several grades below the audience's
  education for experts.
- Users read ~28 % of words on a page visit: inverted pyramid, scannable layout.
- Measure: words-per-minute vs a reference (≥ ~20 % slower = legibility problem); Cloze
  test for comprehension.
- (No NN/g line-length figure found; use ux-review `typography.md`.)

## Clickability and buttons

[clickable-elements](https://www.nngroup.com/articles/clickable-elements/) ·
[flat-design](https://www.nngroup.com/articles/flat-design/) ·
[flat-design-best-practices](https://www.nngroup.com/articles/flat-design-best-practices/) ·
[button-states-communicate-interaction](https://www.nngroup.com/articles/button-states-communicate-interaction/)
- Keep signifiers: links blue or underlined; buttons rectangular (rounded corners
  fine) and looking pressable; never link-style non-clickable text; never style
  headings like buttons. Semi-flat (subtle meaningful shadows) over fully flat.
- No ghost buttons for primary actions. Primary = solid fill in the accent; secondary
  = outlined; tertiary = least emphasis.
- Make every part of an item (image, icon, text) clickable.
- **States:** enabled, disabled, hover, focus, pressed (+ loading, selected). Focus
  within ~100–150 ms, as an outline, not colour alone; pressed within ~100–150 ms or
  users press again; hover after ~150–200 ms. Disabled: lower contrast but still
  readable; `aria-disabled="true"` so it stays focusable. Loading spinner left of the
  label.

## Target size (Fitts's law)

[fitts-law](https://www.nngroup.com/articles/fitts-law/) ·
[touch-target-size](https://www.nngroup.com/articles/touch-target-size/)
- Big targets; the smaller of width/height is what counts. Make icon + label one
  target. Don't rely on invisible padding — people aim at what they see.
- Touch minimum **1 cm × 1 cm** physical (bigger for primary actions, on-the-move use,
  children and seniors); ~2 mm spacing minimum — spacing doesn't rescue a too-small
  target. **Voting: VVSG 12.7 mm / 2.54 mm wins.**
- Submit/Save right after the last field; contextual options open next to their
  trigger; order menus by frequency.

## Controls

[checkboxes-vs-radio-buttons](https://www.nngroup.com/articles/checkboxes-vs-radio-buttons/) ·
[toggle-switch-guidelines](https://www.nngroup.com/articles/toggle-switch-guidelines/) ·
[drop-down-menus](https://www.nngroup.com/articles/drop-down-menus/) ·
[date-input](https://www.nngroup.com/articles/date-input/)
- **Radio** = exactly one; **checkbox** = any number incl. zero. Vertical lists,
  clickable labels, positive wording. Radio lists get a default (add "None" if
  declining is valid) — *[interp] except where law forbids pre-selection, e.g. ballot
  contests (VVSG 5.2-A no bias): never pre-select a candidate.* Prefer radios to a
  dropdown when there's room.
- **Toggle** only for two states that apply immediately — never inside a form with
  Submit. Short keyword-first label (say "<label> on/off"); position moves with state;
  Off left, On right.
- **Dropdowns:** not when typing is faster (country, state, quantity) or for familiar
  data (birth date); no long scrolling lists; no options that change from another
  menu; grey out unavailable options rather than removing them; support type-to-jump.
- **Dates:** calendar picker for near dates and ranges, always allow typing; accept any
  separator; don't guess on invalid dates; block illogical dates; label D/M/Y and spell
  months for international users.

## Disclosure: tabs, accordions, tooltips

[tabs-used-right](https://www.nngroup.com/articles/tabs-used-right/) ·
[accordions-on-desktop](https://www.nngroup.com/articles/accordions-on-desktop/) ·
[tooltip-guidelines](https://www.nngroup.com/articles/tooltip-guidelines/)
- **Tabs:** few, clearly separate groups users don't compare side by side; selected tab
  shown by ≥ 2 cues (not a 1 px or faint line); one row, directly above the panel; most
  used first and default; 1–2-word labels, no ALL CAPS; keyboard + ARIA roles. On mobile
  prefer accordions.
- **Accordions:** only when users need a few sections; not for content most users need,
  short pages or continuous reading. Caret icon; heading and icon both toggle; allow
  several open; Expand all / Collapse all; expand all when printing.
- **Tooltips:** never hold task-critical information; appear on hover **and** keyboard
  focus; on touch use a tap-to-open "i"/"?" tip; brief, don't repeat the label;
  all-or-none across a set; enough contrast; don't cover related content.

## Dialogs

[modal-nonmodal-dialog](https://www.nngroup.com/articles/modal-nonmodal-dialog/) ·
[confirmation-dialog](https://www.nngroup.com/articles/confirmation-dialog/)
- **Modal** only to prevent lost work / irreversible actions, or to collect what's
  needed to continue the user's own task. Not for unrelated content (no newsletter
  pop-ups), not for form errors (show inline), avoid in high-stakes flows. Multi-step
  modals need progress — or should be a page.
- **Non-modal** for non-critical tasks; don't let it go full-screen on mobile.
- Confirmations: see `nng_patterns.md` (outcome-named buttons, specific text, undo
  preferred).

## Tables, dashboards and charts

[data-tables](https://www.nngroup.com/articles/data-tables/) ·
[dashboards-preattentive](https://www.nngroup.com/articles/dashboards-preattentive/) ·
[choosing-chart-types](https://www.nngroup.com/articles/choosing-chart-types/)
- **Tables:** first column a human-readable identifier; columns by importance, related
  ones adjacent; freeze header row and first column when large; borders, zebra or hover
  to keep place; show active filters and hidden columns ("15 columns hidden"); column
  hide/reorder without drag-and-drop; 1–2 inline row actions, else checkboxes + batch
  actions + Select all; edit in a non-modal side panel.
- **Dashboards:** encode quantity by length or position (sorted bars, lines,
  scatterplots). Avoid pie/donut (except one overwhelming share), radial gauges (use
  bullet charts), treemaps and any 3-D. **Never colour for magnitude**; categories by
  shape, position or borders, colour only as support.
- **Charts:** always give a comparison point (24 % vs 17 % last year). Bars by default;
  horizontal bars for long labels; never rotated labels; separate bar charts instead of
  stacked; lines with markers for trends; scatter for relationships. Avoid pie, bubble,
  waffle, Sankey, stacked area unless nothing basic works.
- Also see the `dataviz` skill when building a chart.
