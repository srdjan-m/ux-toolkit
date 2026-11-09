# Typography — review checklist

Values marked *(guideline)* are widely used craft ranges, not standards — report a
miss as Minor/Polish unless it causes a readability or accessibility failure. Hard
limits (WCAG, VVSG) are cited by ID and outrank everything here.

## 1. Hierarchy

- Can you name the **three levels** of the screen in one glance (title → section →
  body)? If two levels look the same, the hierarchy is broken.
- Each step in the hierarchy should differ by **more than one** property, or by a clear
  size jump *(guideline: ≥ 1.2× between adjacent sizes)*. Size + weight is strong; size
  alone at 14 → 15 px is invisible.
- One typeface family is usually enough; two maximum (one for UI, one for display).
  Count the families and the weights used — more than ~4 sizes and ~3 weights on one
  screen usually means no system.
- Headings sit closer to the content they introduce than to the content above
  (proximity — see `layout.md`).

## 2. Size and scale

- Body text on screens *(guideline)*: 16 px web, 17 pt iOS, 14–16 sp Android; never
  smaller than 12 px for anything users must read.
- Sizes come from a **scale** (design tokens), not ad-hoc values. Off-scale sizes
  (15, 17, 19 px in a 14/16/20 scale) are findings: name the token they should use.
- Voting screens: default uppercase-I height **≥ 4.8 mm**, range 3.5–9.0 mm, paper
  ≥ 3.5 mm (VVSG 7.1-G, 7.1-I). Convert with `ux_measure.py size --font-px`.
- Large text for WCAG contrast is ≥ 24 px regular / ≥ 18.66 px bold (1.4.3).

## 3. Readability

- **Line length** *(guideline)*: 45–75 characters for body text, ~66 ideal. Count a
  line in the design; very wide text columns on desktop are a common miss.
- **Line height** *(guideline)*: 1.4–1.6× for body, tighter (1.1–1.3×) for large
  headings. Must survive 1.5× without clipping (WCAG 1.4.12).
- **Paragraph spacing** larger than line spacing, so paragraphs read as units.
- Left-aligned text for anything longer than two lines (in LTR languages). Centred
  and justified body text hurt reading — justified creates rivers, centred breaks the
  scan line.
- ALL CAPS only for short labels, with added letter-spacing *(guideline: +0.05 em)*;
  never for sentences or names (they lose word shape and read slower).
- Avoid light/thin weights below ~18 px; they fail contrast in practice even when the
  hex values pass.

## 4. Type for voters and forms

- Sans-serif available for all voter text (VVSG 7.1-J). Good candidates the VVSG names:
  Arial, Calibri, Helvetica, Univers, Clearview ADA, Open Sans.
- Distinguishable characters: I / l / 1 and O / 0 must differ — matters for codes,
  candidate names, write-ins.
- Candidate names and options all use **identical** type settings (VVSG 5.2-A No bias).
- Numbers in tables use **tabular figures** so columns align.
- Truncation: names and translated labels must not be cut with "…" where the full text
  matters. Check the longest real value and the longest translation (German, Spanish
  run ~30 % longer than English).

## 5. Report language

Say what it *is* and what it *should be*, by token if one exists:
"Contest title uses 18 px / 400 — same as candidate names; use `heading-sm` (22 px / 600)
so the contest reads as a header."
