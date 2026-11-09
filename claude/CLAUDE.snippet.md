# File naming conventions

Apply to every file you create, in any project, unless the surrounding code or the
ecosystem mandates otherwise (`README.md`, `Dockerfile`, `page.tsx`, `__init__.py`, …).
When editing an existing codebase, match its conventions instead.

- **`snake_case` everywhere, no spaces, no capitals, no special characters.** Lowercase
  extensions.
- **Design & dev files:** `{project}_{feature}_v{NN}[-{tag}].{ext}` — two-digit
  zero-padded version starting at `v01` (`precinct_login_screen_v03-wip.fig`).
- **Research, notes & audits:** `YYYY-MM_topic-name.ext` — date first so they sort
  chronologically (`2026-07_competitor-audit.md`).
- **Status tags** go in the `-{tag}` slot: `-wip`, `-review`, `-approved`. Variant tags
  share that slot: `-dark`, `-mobile`, `-alt`.
- **Image sequences:** one folder per sequence and version, frames named like the folder
  (`{project}_{feature}_v{NN}/{project}_{feature}_v{NN}_0001.png`). Never put status tags
  on files other files link to (renders, mixdowns) — use a `.meta.md` sidecar.
- **Folders prefixed `_`** are infrastructure, never deliverables: `_assets`,
  `_templates`, `_archive`, `_cache`.
- Bump the version for meaningful iterations, not every save; move superseded versions
  into the nearest `_archive/`.

For folder structure, stages, disciplines and file metadata, use the
`project-organization` skill. Full reference: `CONVENTIONS.md` in the ux-toolkit repo.

# Comments

In design, SCSS and code projects, comment everything in detail: why a rule exists, what
breaks without it, what it overrides or is overridden by, where a value comes from, and the
decision behind it with its date. Never restate what the code says. State checked facts only;
mark anything unverified as such. When a comment would run past ~3 lines, point to the
decision record instead. One tier of plain comments — builds strip them from production.
Never copy a token's value into a comment: name the token, so a token change can't leave the
comment stale. Original values a decision replaced, and numbers inside a dated decision, are
history and may be quoted.
