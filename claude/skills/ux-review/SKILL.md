---
name: ux-review
description: Review a UI design for usability, accessibility and visual quality, and report prioritised findings with the rule each one breaks. Use for design reviews, critiques, audits, accessibility or contrast checks, "does this look right", heuristic evaluations, or checking a screenshot, Figma frame, live URL, flow, form, dashboard, ballot layout or voting-machine screen against WCAG 2.2 or VVSG 2.0. Also used by the ux-critic agent. Triggers on "review", "critique", "audit", "UX feedback", "accessibility", "a11y", "contrast", "WCAG", "VVSG", "ballot", "touch target", "heuristics".
---

# UX review

A review is only useful if every finding is **specific, measured where possible, tied
to a rule, ranked, and fixable**. "The hierarchy feels off" teaches nothing; "Contest
title and candidate names are both 18 px / 400, so the title doesn't read as a header —
use 22 px / 600" does.

## Knowledge — load only what applies

Each discipline is a reference file. Read the ones the review needs, not all of them.

| File | Read when |
|---|---|
| `references/heuristics.md` | Always — Nielsen's 10 as check questions (H1–H10). |
| `references/accessibility.md` | Always — WCAG 2.2 AA criteria checkable from a design. |
| `references/voting_vvsg.md` | **Any voting, ballot, poll-worker or election screen** — VVSG 2.0 requirement IDs with exact values. Stricter than WCAG; the stricter rule wins. |
| `references/typography.md` | Text hierarchy, sizes, readability. |
| `references/color.md` | Colour roles, contrast, states, dark mode, palette harmony. |
| `references/layout.md` | Grouping, alignment, spacing, priority, responsiveness. |
| `references/content.md` | Labels, buttons, errors, instructions, translations. |
| `references/reports_data.md` | **Any report, table, dashboard or generated/compliance output**: summary-vs-data truth, filter behaviour on real data, print/export. |

If the project has a design system (tokens, component docs), read it too and name
tokens in fixes. Deviations from the project's own system are findings.

## Process

1. **Context.** Who are the users, what is the task on this screen, what platform and
   **display size** (needed for any mm measurement), what stage (sketch → polish)? If
   something important is missing, ask once; otherwise state your assumption in the
   summary and continue.
2. **Get the real pixels and values.**
   - Image file → Read it.
   - Figma URL → Figma MCP tools: a screenshot for the look, design context for exact
     sizes, colours and tokens. Exact values beat sampled pixels.
   - Live page → browser screenshot; inspect styles where possible. Pitfalls with
     headless Chrome/Edge (seen 2026-11-09): a URL with a `#fragment` can capture
     blank, so capture without it. Headless follows the OS colour scheme, so check
     which theme you actually got before calling it "light" or "dark".
   - Look at **every state** you can get: default, hover/focus, selected, error, empty,
     loading, longest content, largest text size. Missing states are findings.
   - **Every output medium.** If the screen is printed, exported or attached (PDF,
     certification package, email), produce that output and review it too.
3. **Walk the task** as the user, screen by screen, before checking rules. Note where
   you hesitate — that's usually the most important finding.
   - **Is the content true?** When the screen summarises data (counts, badges, status
     banners), cross-check the summary against the rows or source. A summary that
     omits or misstates items beats any visual issue. See `references/reports_data.md`.
4. **Check against the references** you loaded.
5. **Measure, don't eyeball.** Use the bundled script (stdlib Python):
   ```
   python scripts/ux_measure.py contrast FG BG [FG BG ...]
   python scripts/ux_measure.py size --diag 21.5 --res 1920x1080 --px 48 --font-px 28
   ```
   Contrast reports WCAG and VVSG pass/fail; size converts px to mm and shows the VVSG
   minimums for that display. For palette findings, `oklch HEX ...` gives perceived
   lightness/chroma/hue and their spread, and `harmony BASE [--scheme triadic]` builds
   hue harmonies to recommend from (see `references/color.md` §5). Run it from this
   skill's directory.
6. **Rank and report** (format below). Merge duplicates; one root cause = one finding
   listing every place it occurs.

## Severity

| Level | Meaning |
|---|---|
| **Blocker** | Fails a requirement (VVSG, WCAG AA, legal), or the user can't complete the task or could cast/submit something they didn't intend. |
| **Major** | Causes errors, confusion or significant slowdown for many users; likely support calls. |
| **Minor** | Friction or inconsistency that users work around. |
| **Polish** | Craft: alignment, off-scale values, visual noise. |

Mark every finding **Measured** (value from Figma/code/script) or **Estimated** (judged
from a screenshot). Never present an estimate as a measurement.

## Output format

```
## Review: <what was reviewed>
**Context / assumptions:** <users, task, display size, what was available>
**Verdict:** <one sentence: ready / ready with fixes / needs rework, and the main reason>

| # | Severity | Where | Problem | Rule | Fix |
|---|---|---|---|---|---|
| 1 | Blocker | Contest "City Council", rows 1–8 | Touch targets 48 px = 11.9 mm on 21.5" 1080p (Measured) | VVSG 7.2-I (≥ 12.7 mm) | Raise row height to 56 px (13.9 mm) |

### What works
- 2–3 specific things to keep, and why they work.

### Not checked
- What couldn't be verified from this material (audio, keyboard behaviour, physical
  hardware, mm sizes without a display size, states not provided).
```

Sort by severity, then by how much of the flow it affects. Keep fixes concrete
(value, token, wording). Don't redesign the screen in the report — point the way.
