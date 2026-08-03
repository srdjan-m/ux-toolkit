---
name: project-organization
description: Scaffold and organize UI/UX project folders — stages, disciplines, subfolder placement — and attach file metadata sidecars. Use when creating a new project, deciding where a file belongs in an existing project tree, promoting work toward production, or recording who requested a file and why. Triggers on "new project", "scaffold", "where does this file go", "project structure", "file metadata", "sidecar", "INDEX.md", new_project.py, add_meta.py.
---

# Project organization

Naming rules are already in context via the global `CLAUDE.md` import — don't restate
them, apply them. This skill covers **where files live** and **what context travels with
them**. Full naming reference: `CONVENTIONS.md` in the ux-toolkit repo.

The toolkit lives at the repo root alongside this skill's parent directory. On an
installed machine, find it via the `@` import path in `~/.claude/CLAUDE.md`, or ask.

## The model: stage → discipline → working subfolder

- **Stages** describe *where the work is in the process*. Full profile:
  `research` → `prototyping` → `design` → `production`. Lean profile:
  `exploration` → `production`.
- **Disciplines** describe *what kind of work it is*, and carry a numeric prefix so they
  hold a fixed sort order in every file browser.
- **Subfolders** separate live source from generated output from history.

```
my_app/
├── README.md
├── .gitignore
├── research/                  ← STAGE
│   ├── 01_dev/                ← DISCIPLINE
│   │   ├── src/ libs/ _archive/
│   ├── 02_research/
│   │   ├── references/ notes/ _archive/
│   ├── … 07_diagrams/
│   ├── _assets/               ← shared assets for this stage
│   └── _templates/
├── prototyping/  design/  production/
```

| Key            | Folder            | For                                  | Subfolders                                        |
| -------------- | ----------------- | ------------------------------------ | ------------------------------------------------- |
| `dev`          | `01_dev`          | JS, SCSS, Python, QML source         | `src` · `libs` · `_archive`                       |
| `research`     | `02_research`     | References, notes, briefs, audits    | `references` · `notes` · `_archive`               |
| `design`       | `03_design`       | UI layouts, icons, color systems     | `working` · `exports` · `_archive`                |
| `illustration` | `04_illustration` | Illustrations and graphics           | `working` · `exports` · `_archive`                |
| `motion`       | `05_motion`       | After Effects projects and exports   | `projects` · `renders` · `_cache` · `_archive`    |
| `3d`           | `06_3d`           | Blender files, models, rigs, renders | `scenes` · `assets` · `renders` · `_cache` · `_archive` |
| `diagrams`     | `07_diagrams`     | Flowcharts, schematics, specs        | `working` · `exports` · `_archive`                |

- **`working/`** — live, editable source (`.fig`, `.ai`, `.aep`, `.blend`).
- **`exports/`** / **`renders/`** — generated output (`.png`, `.svg`, `.mp4`). Never
  hand-edit; re-export from the source instead.
- **`_archive/`** — superseded versions worth keeping but not seeing day-to-day.
- **`_cache/`** — regenerable temp files. Safe to delete anytime; carries a
  self-ignoring `.gitignore` so the folder is versioned but its contents never are.

**`production/` is sacred.** Only final, approved, deliverable-ready files. If it isn't
signed off, it belongs in `design/` or `prototyping/`.

## Placing a file

1. Which stage is the work in? Not signed off ⇒ never `production/`.
2. Which discipline produced it?
3. Editable source ⇒ `working/`/`src/`/`projects/`/`scenes/`. Generated ⇒
   `exports/`/`renders/`. Superseded ⇒ `_archive/`. Regenerable junk ⇒ `_cache/`.
4. Name it per the conventions already in context.

A login screen's life:

```
prototyping/03_design/working/precinct_login_screen_v01-wip.fig
design/03_design/working/precinct_login_screen_v02-review.fig
design/03_design/working/precinct_login_screen_v03-approved.fig
design/03_design/exports/precinct_login_screen_v03.png
production/03_design/exports/precinct_login_screen_v03.png     ← the deliverable
```

## Scaffolding — `new_project.py`

```bash
python new_project.py my_app                      # machine's default profile
python new_project.py my_app --profile personal   # lean structure
python new_project.py my_app --dry-run            # print, touch nothing
python new_project.py --list-profiles             # profiles and their shape
python new_project.py --list-disciplines
```

Precedence: explicit `--stages`/`--disciplines` > `--profile` > the machine default in
`~/.uxkit` > built-in `work`. Profiles are JSON in `profiles/` — a machine-level choice,
not a per-project one, so the same command produces the right shape on each machine.

**Always `--dry-run` first** when pointing at an existing folder or using custom stages.
The script merges into existing folders rather than erroring, and preserves an existing
`README.md` unless `--force` is passed.

Adding a discipline means editing `DISCIPLINES` and `DISCIPLINE_SUBFOLDERS` in
`new_project.py` (keep the numeric sequence intact) — never inventing a folder ad-hoc.

## Metadata — `add_meta.py`

Filenames say *what* and *what state*; sidecars say **who asked** and **why**. A
`<filename>.meta.md` sidecar sits next to the asset, works for binaries (`.fig`, `.aep`,
`.blend`), and survives Creative Cloud sync and version control — embedded metadata and
NTFS attributes don't.

```bash
python add_meta.py set design/03_design/working/precinct_login_screen_v03-approved.fig \
    --requested-by product_team \
    --reason "Redesign login flow for accessibility audit AA-2026-07" \
    --status approved --tags login accessibility \
    --supersedes precinct_login_screen_v02.fig

python add_meta.py set precinct_login_screen_v03-approved.fig -i   # guided prompts
python add_meta.py show <file>
python add_meta.py index <project_root>    # regenerate INDEX.md + assets.csv
```

`set` updates in place: `created` is preserved, `updated` refreshed, omitted fields kept.
`--status` is validated against `wip` · `review` · `approved` — the same vocabulary as
the filename tags, so the two should always agree.

Reach for a sidecar when a file was requested by someone, supersedes another version, or
would raise "why does this exist?" in three months. Re-run `index` after a batch of
changes; it's regenerated from the sidecars, so it never drifts.
