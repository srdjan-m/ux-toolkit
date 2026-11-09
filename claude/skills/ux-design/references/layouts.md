# Designing layouts

Rules to meet are in ux-review's `layout.md` and `typography.md`; NN/g guidance on
hierarchy, Gestalt and reading patterns is in `nng_visual.md` and `nng_patterns.md`.
This file covers **how to produce** a layout and in what form.

## Deliverable formats

Pick by what the user will do next; ask if unclear.

| Format | When | Notes |
|---|---|---|
| **ASCII / Markdown wireframe** | Early structure, quick options in chat | Boxes and labels only. Fast to compare 2–3 directions. |
| **Static HTML + CSS mockup** | Default for anything visual | One self-contained file, real content, all states reachable (a state switcher or one section per state). Open it and screenshot it to check your own work. |
| **Figma** | User works in Figma or asks for it | Use the figma skills (`figma:figma-use`, `figma:figma-generate-design`) and the file's existing components and variables. |
| **Code in the project** | User asks to implement | Follow the codebase's conventions and component library; tokens, never raw values. |

File names follow the user's convention: `{project}_{feature}_v{NN}[-{tag}].{ext}`, e.g.
`dvs_results_dashboard_v01-wip.html`.

## Procedure

1. **Inventory the content.** List every element the screen must show, with its real
   (and longest) content. Rank by importance *for the task*, not for the business.
2. **Choose the pattern.** Use a known pattern (list–detail, form, wizard, dashboard,
   table + filters, master–detail) unless there's a reason not to; users bring
   expectations from other products (NN/g: Jakob's law — see `nng_patterns.md`).
3. **Grid and spacing.** One spacing scale (design system's, else 4/8-based: 4, 8, 12,
   16, 24, 32, 48). One column grid. Every value on the scale; an off-scale value needs
   a reason.
4. **Hierarchy in greyscale.** Size, weight, position and space first. If the screen
   doesn't read correctly without colour, colour won't fix it.
5. **Group by proximity.** Related things close, groups separated by clearly more space
   than items inside them (≥ 2× is a reliable starting ratio). Use borders and cards
   only when space alone can't do it.
6. **One primary action per view**, placed where the eye ends (bottom-right of a form on
   desktop LTR, or full-width at the bottom on mobile). Secondary actions visually
   quieter; destructive actions separated from the primary.
7. **All states.** Empty, loading, error, partial, overflowing, long translation (+30–40
   % text length), largest supported text size, keyboard focus visible.
8. **Responsive.** Decide breakpoints from the content (when does a line exceed ~75
   characters, when do two columns get too narrow), not from device names.
9. **Self-check and measure** (SKILL.md step 6).

## Density

Expert, repeated-use tools (poll-worker dashboards, admin tables) can be denser than
first-time or public flows (voters). Decide density deliberately from the users, write
it in the brief, and keep it consistent across screens.
