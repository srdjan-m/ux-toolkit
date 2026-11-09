---
name: ux-design
description: Design UI — palettes and colour tokens, screen layouts, components, icons and interaction patterns — grounded in Nielsen Norman Group guidance, and deliver it as HTML/CSS, Figma or token files with the reasoning behind each decision. Use when asked to design, redesign, propose, mock up, wireframe or prototype a screen, flow, form, dashboard, palette, colour scheme, icon set or component, or to "make this look better". Also used by the ux-designer agent. Triggers on "design", "redesign", "mockup", "wireframe", "layout", "palette", "colour scheme", "color scheme", "icons", "make it look better", "UI for".
---

# UX design

Good design here means: **the user's task gets easier, every decision has a reason you
can name, and the result passes review.** Pretty comes from restraint and consistency,
not decoration.

## Knowledge — load only what applies

| File | Read when |
|---|---|
| `references/nng_patterns.md` | Always — NN/g guidance on forms, errors, navigation, feedback, reading, content. |
| `references/nng_visual.md` | Any visual work — NN/g on hierarchy, Gestalt, colour, type, controls, dialogs, tables. |
| `references/icons.md` | Any screen with icons, or designing icons. |
| `references/palettes.md` | Creating or changing colours, themes or colour tokens. |
| `references/layouts.md` | Creating or changing a screen, flow or component layout. |

The **ux-review** skill holds the pass/fail rules — WCAG 2.2, VVSG 2.0 for anything
voting-related, typography, colour and layout checklists — and the measuring script
`ux_measure.py` (`contrast`, `size`, `oklch`, `harmony`, `scale`). Design to those rules
from the start; don't treat review as a later step. The script lives in that skill's
`scripts/` folder (installed at `~/.claude/skills/ux-review/scripts/ux_measure.py`).

## Design system first

If the project has a design system, it wins: read it before designing (for PES/DVS work
that's `~/Projects/design-system`, `CONTEXT.md` first). Use its tokens and components by
name. Anything it lacks: use a clearly marked local value and list it as a **gap** in
your hand-off. Never add to the system or invent a parallel one unasked.

## Process

1. **Brief.** Who uses it, what task, on what device and display size, in what
   conditions (stress, time pressure, gloves, glare)? What exists today and what's wrong
   with it? If something decisive is missing, ask once; otherwise state assumptions.
2. **Constraints.** Design system, platform conventions, regulations (VVSG/WCAG),
   technical limits (framework, no build step), content (real data, longest strings,
   translations).
3. **Structure before style.** Task flow → content priority → layout (wireframe level).
   Get the hierarchy right in greyscale first; colour comes last and carries meaning,
   not structure.
4. **Options.** For anything non-trivial, give 2–3 genuinely different directions with
   the trade-off of each, then recommend one. Don't make three variations of one idea.
5. **Build** the chosen direction in the requested format (`references/layouts.md`
   lists them). Real content, every state (empty, loading, error, long text, disabled,
   focus), both themes if the product has them.
6. **Self-check** against the ux-review checklists and measure: contrast on every text
   and UI pair, target sizes, `oklch` spread for colour sets. Fix what fails before
   handing off.
7. **Hand off** (format below). Recommend an independent `ux-critic` review for
   anything that ships; a designer shouldn't be the only reviewer of their own work.

## Hand-off format

```
## Design: <what>
**Brief / assumptions:** <users, task, device, what you assumed>
**Direction:** <chosen option and why; one line on each rejected option>

### Files
- <path> — <what it is>

### Decisions
| Decision | Why | Source |
|---|---|---|
| Primary button only on "Cast ballot" | One primary action per view | NN/g; ux-review color.md §3 |

### Measured
- <pair> = <ratio> (target); <target> = <px / mm>

### Gaps and open questions
- <tokens the design system lacks, things only the user can decide>
```

Cite the NN/g article (from the reference files) or rule ID behind every non-obvious
decision. If you can't name a reason, reconsider the decision.
