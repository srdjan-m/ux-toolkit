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
