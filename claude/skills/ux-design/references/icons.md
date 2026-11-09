# Icons

Two halves: **usability** (when an icon helps, and how users read it) from Nielsen
Norman Group research, and **craft** (how icons are drawn, sized and coded so a set
looks like one family and works for everyone) from established icon-system practice.

## 1. Usability (NN/g)

Gathered 2026-11-09; all URLs confirmed then. Close paraphrases unless quoted.

### Label icons — almost always
[icon-usability](https://www.nngroup.com/articles/icon-usability/) ·
[utility-navigation](https://www.nngroup.com/articles/utility-navigation/) ·
[magnifying-glass-icon](https://www.nngroup.com/articles/magnifying-glass-icon/)
- Only a few icons are close to universal: **home, print, magnifying glass (search)**.
  Everything else is ambiguous across products (heart vs star for favourite / bookmark /
  rating).
- **Give icons a visible text label**, even standard ones; essential for navigation.
  Not on hover only — hover costs effort and doesn't exist on touch.
  "People like icons, but they don't understand them and have trouble memorizing them."
- Search: the magnifying glass may go unlabelled, but on desktop show an open search
  field (≥ 27 characters wide or expanding), not an icon-only button; the icon button
  needs "Search" as its accessible name.

### Choosing an image
[classifying-icons](https://www.nngroup.com/articles/classifying-icons/) ·
[bad-icons](https://www.nngroup.com/articles/bad-icons/) ·
[floppy-disk-icon-understandability](https://www.nngroup.com/articles/floppy-disk-icon-understandability/) ·
[digital-icons-ux-quiz](https://www.nngroup.com/articles/digital-icons-ux-quiz/)
- **Resemblance** icons (a picture of the thing) work best. **Reference** icons (an
  analogy) work only if users make the leap — a clock for "history" failed in tests.
  **Arbitrary** icons work only when already standard ("?" for help, warning triangle):
  "Don't be the one to try to teach the world a new arbitrary icon."
- **5-second rule:** if you can't think of an image for a concept within ~5 s, an icon
  probably can't communicate it — use text.
- Don't reuse an image that already means something else (a star for "templates"); no
  obscure chains (rocket → launch → apps); no interface puns (a dining table for a data
  table); culturally neutral objects for international audiences (envelope, not a
  country-specific mailbox).
- Simple and schematic; must work at small size and be understood at a glance.
- Every icon costs design, testing, space and noise. If the label is always shown,
  check the icon still adds something. If you can't make a usable, consistent set,
  **use text links and no icons.**
- Match the icon to the real behaviour: floppy disk only for a true Save (83 % read it
  as save), not for sync/export/download. Circular arrows read as refresh/sync (73 %).
- Known pitfalls from NN/g's quiz: a **globe reads as "internet", not "language"**
  (57.8 %); lines inside a border read as a document (71 %) — so don't frame a
  hamburger; don't use both a flame and a trend line for "trending".
- **Language switchers: no flags.** Use each language's name in its own script
  (matches VVSG 7.3-M).

### Navigation and menu icons
[hamburger-menus](https://www.nngroup.com/articles/hamburger-menus/) ·
[hamburger-menu-icon-recognizability](https://www.nngroup.com/articles/hamburger-menu-icon-recognizability/) ·
[find-navigation-mobile-even-hamburger](https://www.nngroup.com/articles/find-navigation-mobile-even-hamburger/) ·
[mobile-navigation-patterns](https://www.nngroup.com/articles/mobile-navigation-patterns/) ·
[contextual-menus-guidelines](https://www.nngroup.com/articles/contextual-menus-guidelines/)
- **Desktop: never hide navigation behind a hamburger.** Hidden nav was used in 27 % of
  cases vs 48 % visible; discoverability dropped > 20 %; tasks ≥ 39 % slower.
- Mobile: ≤ 4 top-level items → show them. More → a hamburger is acceptable, standard
  form (3 equal lines, top-left, no border), labelled **"Menu"**, looking tappable, plus
  in-page links to key content. A wide labelled "Browse" button got 89 % use vs 44 % for
  a tiny unlabelled icon.
- Tab bars: **labelled icons**, 4–5 items max.
- Kebab ⋮ / meatball ⋯ = "more actions" on **one object**, placed next to it, visible
  without hover, for **secondary** actions only. Show 1–2 actions directly instead.
  Hamburger = global navigation only.
- Accordions: use a **caret** (plus and right-arrow did no better than no icon); the
  label and the icon toggle the same thing.

### Close, state and info icons
[cancel-vs-close](https://www.nngroup.com/articles/cancel-vs-close/) ·
[state-switch-buttons](https://www.nngroup.com/articles/state-switch-buttons/) ·
[info-tips-bad](https://www.nngroup.com/articles/info-tips-bad/)
- An unlabelled **X is ambiguous** (close and keep vs cancel and discard). Prefer text
  buttons (Cancel / Apply); if X must discard work, confirm first. "When in doubt, save,
  then out."
- **State toggles** (mute, pin): an icon whose state is shown only by colour fails.
  Show the current state *and* a labelled action, or an icon showing state with a label
  saying what will happen.
- Encircled **i** = more information; encircled **?** = help. Assume most users never
  open them: no constraints, character limits or instructions inside tips. Show the tip
  inline — never a modal or new page from an info icon.

### Status icons and indicators
[visual-indicators-differentiators](https://www.nngroup.com/articles/visual-indicators-differentiators/) ·
[errors-forms-design-guidelines](https://www.nngroup.com/articles/errors-forms-design-guidelines/)
- Indicators that differ in **both colour and icon** were fastest (text-only was 57 %
  slower). If only one cue, a distinct icon beats colour. Subtly different shapes get
  missed when scanning.
- Error icon to the left of the message; red = error, orange/yellow = warning,
  green/blue = success. At most a subtle pulse on one icon; never animate text. Never an
  icon whose message needs hover.
- Don't repeat the same icon on every row of a list (a person icon by every name).

### Testing icons
[icon-testing](https://www.nngroup.com/articles/icon-testing/)
- Test four things separately: **findability** (in context, time and first-click
  success), **recognition** (icon alone, no label — if guesses miss, drop it),
  **information scent** ("what would happen if you selected this?") and
  **attractiveness** (1–7 rating; best/worst in the family).
- Don't test by showing the label and asking which icon fits — real users may never
  read the label. Vary task wording so it doesn't prime the answer.
- Memorability: ask the same people again a couple of weeks later.
- Desktop icon-target sizing and touch sizes: see `nng_visual.md` (Fitts's law, 1 cm).

## 2. Craft

Source: common practice across major icon systems (Material Symbols, Apple SF Symbols,
Lucide, IBM Carbon) — not NN/g. Where systems disagree, the project's chosen set wins.

### One set, one style
- Use **one icon family** per product. Mixing sets shows up as different stroke widths,
  corner radii and visual weight even when each icon is fine alone.
- Pick one style per context: outline (default, lighter) **or** filled. A common,
  meaningful exception: filled = selected/active state of the same icon (tab bars).
- Don't draw a one-off icon when the set has a close match; if you must, draw it on the
  set's grid with its stroke, corners and keylines, and flag it as a gap.

### Grid, size and alignment
- Design on the set's grid (typically 24 × 24 with ~2 px padding; 20 and 16 for dense
  UI). Render at the sizes the set was drawn for; scaling a 24 px icon to 18 px blurs
  strokes.
- Size icons to the adjacent text: roughly the cap height to line height of the label
  (16–20 px next to 14–16 px text). Align to the text's optical centre, not the box.
- Keep stroke width constant across the set at a given size (e.g. 1.5 or 2 px at 24).
- Visual weight differs by shape: a circle looks smaller than a square of the same box —
  sets correct this with keylines; don't "fix" it by resizing individual icons.

### Touch and click targets
- The **target**, not the glyph, must meet the size rules: WCAG 2.5.8 ≥ 24 × 24 CSS px
  (aim for 44 × 44 on touch), VVSG 7.2-I ≥ 12.7 mm for voting. A 20 px icon gets padding
  to reach the target size. Measure with `ux_measure.py size`.
- Space adjacent icon buttons so their targets don't overlap.

### Colour and contrast
- Icons that carry meaning need ≥ 3:1 against their background (WCAG 1.4.11; VVSG
  10:1). Decorative icons are exempt but should then be truly decorative.
- Icon colour follows text colour by default (`currentColor`); colour an icon only to
  carry meaning (status), and never by colour alone — the shape and a label carry it too.
- Status icons should differ in **shape**, not just colour: e.g. circle-check (success),
  triangle-exclamation (warning), circle- or octagon-x (error), circle-i (info).

### Accessibility in code
- **Decorative** icon next to a text label: hide it from assistive tech
  (`aria-hidden="true"` on the SVG / icon element). The label does the work.
- **Icon-only button**: the button gets an accessible name (`aria-label="Delete
  contest"`, or visually hidden text), the icon is `aria-hidden`. Name the action, not
  the picture ("Search", not "Magnifying glass").
- **Meaningful standalone icon** (status in a table cell): `role="img"` with an
  `aria-label`, or adjacent visually hidden text.
- Prefer inline SVG or an SVG sprite over icon fonts: icon fonts break when fonts fail
  to load or are overridden (user stylesheets, high-contrast modes), and screen readers
  can announce their private-use glyphs.
- In Windows forced-colours / high-contrast mode, SVG icons using `currentColor` follow
  the text colour; hard-coded fills may vanish — test it.
- Tooltips on icon-only buttons supplement the accessible name; they don't replace it
  and aren't available on touch.

### Review checks
- Every icon-only control: is the meaning obvious without its tooltip? If not, add a
  visible label (see §1).
- Same concept, same icon everywhere; different concepts, different icons.
- No icon used for two meanings across the product (a gear for both "settings" and
  "configure device" is fine only if they're the same thing).
