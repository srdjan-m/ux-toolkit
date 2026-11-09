# Accessibility — WCAG 2.2 AA checks a designer can verify

Which version applies: **WCAG 2.2 AA** is current best practice and what to review
against by default. Voting systems are legally held to **WCAG 2.0 AA via Section 508**
(VVSG 8.2-A) *plus* VVSG's stricter rules — see `voting_vvsg.md`; the stricter value
wins. Cite the success-criterion number in every finding.

Sizes below are **CSS px** (web/app). For a physical device convert with
`scripts/ux_measure.py size`.

## Contents

1. Perceivable — colour, contrast, text, structure
2. Operable — targets, focus, keyboard, motion, timing
3. Understandable — labels, errors, consistency, help
4. What a static design can't prove

---

## 1. Perceivable

| SC | Level | Check | How to verify |
|---|---|---|---|
| 1.1.1 | A | Every meaningful image/icon has a text alternative; decorative ones are marked decorative. | Ask for alt text in the spec / annotations. Icon-only buttons need an accessible name. |
| 1.3.1 | A | Structure shown visually (headings, lists, groups, tables, required fields) is also defined structurally. | Look for heading levels and form-group annotations in the handoff. |
| 1.3.3 | A | Instructions don't rely only on shape, size, position or sound ("click the round button on the right"). | Read every instruction. |
| 1.4.1 | A | Colour is not the only way to convey info: links in text, error fields, selected state, chart series, required fields. | Imagine the screen in greyscale. Underline links; add icons/text to errors. |
| 1.4.3 | AA | Text contrast **≥ 4.5:1**; large text **≥ 3:1** (large = ≥ 24 px regular or ≥ 18.66 px bold). Placeholder text and disabled-looking-but-active text count. | `ux_measure.py contrast FG BG`. Disabled controls are exempt. |
| 1.4.4 | AA | Text can be resized to 200 % without loss of content or function. | Check that containers grow; no fixed-height text boxes. |
| 1.4.10 | AA | Reflow: content works at **320 px** wide (400 % zoom) without horizontal scrolling — except data tables, maps, toolbars. | Ask for or check the narrowest breakpoint. |
| 1.4.11 | AA | Non-text contrast **≥ 3:1** against adjacent colours for: input borders, checkbox/radio outlines, focus indicators, icons that carry meaning, chart lines, the *selected* state indicator. | Measure border vs background, not fill vs text. |
| 1.4.12 | AA | Layout survives line-height 1.5×, paragraph spacing 2×, letter-spacing 0.12 em, word-spacing 0.16 em. | Look for tight fixed-height components, truncated labels. |
| 1.4.13 | AA | Tooltips/popovers on hover or focus: dismissible (Esc), hoverable (pointer can move onto them), persistent (don't vanish on their own). | Check tooltip spec. |

## 2. Operable

| SC | Level | Check | How to verify |
|---|---|---|---|
| 2.1.1 | A | Everything works by keyboard (no hover-only or drag-only function). | Walk the flow with Tab/Enter/Space/arrows in your head. |
| 2.2.1 | A | Time limits can be turned off, adjusted, or extended — warn **≥ 20 s** before and allow extending with a simple action. | Session-timeout dialogs. |
| 2.3.1 | A | Nothing flashes more than **3 times per second**. | Animations, loading states. |
| 2.4.3 | A | Focus order follows the visual/reading order. | Number the focus order on the design. |
| 2.4.6 | AA | Headings and labels describe their topic or purpose. | "Details", "Info", "Click here" fail. |
| 2.4.7 | AA | A visible focus indicator on every interactive element. | Is a focus state designed for every component? Missing focus states are the most common gap in design files. |
| 2.4.11 | AA | Focused element is **not entirely hidden** by sticky headers/footers, cookie bars, chat widgets. | Check sticky regions over scrolling content. |
| 2.5.3 | A | Visible label text is contained in the accessible name (voice control users say what they see). | Button "Send" must not be named "Submit form". |
| 2.5.7 | AA | Any **dragging** action has a single-pointer alternative (buttons, tap-to-select). | Sliders, reorder lists, drag-and-drop uploads, maps. |
| 2.5.8 | AA | Targets **≥ 24 × 24 px**, or spaced so a 24 px circle centred on each doesn't overlap another target. Inline text links exempt. | Measure icon buttons, close "×", table row actions, pagination. (Platform guidance is larger: Apple 44 pt, Material 48 dp. VVSG voting is 12.7 mm.) |

## 3. Understandable

| SC | Level | Check | How to verify |
|---|---|---|---|
| 3.1.1 | A | Page language defined; 3.1.2 language of parts for mixed-language content. | Multilingual screens. |
| 3.2.1/3.2.2 | A | Focusing or changing an input doesn't trigger an unexpected context change (auto-submit, navigation). | Dropdowns that navigate on change. |
| 3.2.3 | AA | Repeated navigation is in the same order on every screen. | Compare screens in the flow. |
| 3.2.4 | AA | Same function = same name and icon everywhere. | "Save" vs "Apply" vs "OK" for one action. |
| 3.2.6 | A | Help (contact, chat, FAQ link) appears in the **same relative place** on every page that has it. | Compare screens. |
| 3.3.1 | A | Errors identified in text, naming the field. | Red border alone fails (also 1.4.1). |
| 3.3.2 | A | Labels or instructions for every input; required fields marked; format hints (dates, phone) shown before input. | Placeholder-only labels fail in practice (vanish on typing). |
| 3.3.3 | AA | Error messages suggest how to fix it when known. | "Invalid date" → "Enter a date like 03/15/2026". |
| 3.3.4 | AA | Legal, financial or data-changing submissions are reversible, checked, or confirmed. | Review step before submit. |
| 3.3.7 | A | Don't ask for the same info twice in one process — pre-fill or let the user select it. | "Billing same as shipping". |
| 3.3.8 | AA | Login doesn't require a cognitive test (memorise, transcribe, solve) unless there's an alternative; allow paste and password managers. | Login, 2FA, CAPTCHA screens. |
| 4.1.3 | AA | Status messages (saved, 3 results, error count) are announced without moving focus. | Annotate toasts and inline status as live regions. |

## 4. What a static design can't prove

List these under **Not checked** unless you have a build: real keyboard behaviour,
screen-reader names and announcements, focus management on open/close of dialogs,
zoom/reflow in a browser, motion-reduction preference (2.3.3 AAA / `prefers-reduced-motion`).
Recommend an annotation for each in the handoff instead.
