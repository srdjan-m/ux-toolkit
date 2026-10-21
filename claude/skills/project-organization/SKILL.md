---
name: project-organization
description: Scaffold and organize UI/UX and video/motion project folders — stages, disciplines, the video pipeline, subfolder placement — and attach file metadata sidecars. Use when creating a new project, deciding where a file belongs in an existing project tree, promoting work toward production, placing After Effects / Blender / Audition files and image-sequence renders, or recording who requested a file and why. Triggers on "new project", "video project", "motion project", "scaffold", "where does this file go", "project structure", "render folder", "image sequence", "file metadata", "sidecar", "INDEX.md", new_project.py, add_meta.py.
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
│   ├── … 08_docs/
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
| `docs`         | `08_docs`         | Pages, guides, documentation text    | `drafts` · `exports` · `_archive`                 |

- **`working/`** — live, editable source (`.fig`, `.ai`, `.aep`, `.blend`). For `docs`
  it's **`drafts/`** (editable `.md`).
- **`exports/`** / **`renders/`** — generated output (`.png`, `.svg`, `.mp4`). Never
  hand-edit; re-export from the source instead.
- **`_archive/`** — superseded versions worth keeping but not seeing day-to-day.
- **`_cache/`** — regenerable temp files. Safe to delete anytime; carries a
  self-ignoring `.gitignore` so the folder is versioned but its contents never are.

**`production/` is sacred.** Only final, approved, deliverable-ready files. If it isn't
signed off, it belongs in `design/` or `prototyping/`.

## Placing a file

1. Which stage is the work in? Not signed off ⇒ never `production/`.
2. Which discipline produced it? Written content meant to be read (pages, guides) ⇒
   `08_docs`; raw input (notes, audits, references) ⇒ `02_research`.
3. Editable source ⇒ `working/`/`src/`/`drafts/`/`projects/`/`scenes/`. Generated ⇒
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

## Video / motion projects — `--type video`

Video work flows one way, so it skips stages and uses a fixed pipeline. Every folder is
always created — 2D (After Effects) or 3D (Blender) heavy, both get everything — and the
numbers never change. Profiles don't apply.

```bash
python new_project.py product_reveal --type video --base-dir <videos folder>
python new_project.py product_reveal --type video --init-global   # + shared _assets/ _templates/
python new_project.py --list-disciplines --type video
```

```
videos/
├── _assets/      music · sfx · fonts · luts · brand        ← shared by all projects
├── _templates/   ae · blender
└── product_reveal/
    ├── README.md            brief, pipeline, working rules, tracking commands
    ├── 01_docs/             script, brief, storyboard, client feedback
    ├── 02_sources/          video · audio · images · other   ← received, never edited
    ├── 03_graphics/         working · exports · _archive
    ├── 04_3d/               scenes · assets · renders(/_archive) · _cache · _archive
    ├── 05_audio/            sessions · mixdowns · _archive
    ├── 06_motion/           projects · renders(/_archive) · _cache · _archive
    └── 07_exports/          _archive                         ← what the client receives
```

Placing a file:

- **Came from outside** (client clips, voiceover, screenshots) ⇒ `02_sources/`. Made by
  you ⇒ the folder of the tool that made it. Used by 2+ projects ⇒ `videos/_assets/`.
- **Texture only a Blender scene uses** ⇒ `04_3d/assets/`, not `02_sources/images/`.
- **`06_motion/renders/`** = full-quality masters out of AE. **`07_exports/`** = compressed
  delivery encodes (`product_reveal_full_v03-web.mp4`).
- **Mixdowns and graphics exports** feed AE; AE imports them from where they sit.
- **App-generated folders** (AE `Auto-Save/`, Audition `Backup/`, `Imported Files/`) stay
  where the app puts them, even though they break the naming rules.

Image sequences and linking — the rules that keep AE projects from breaking:

- **One folder per sequence and version**, frames named like the folder:
  `04_3d/renders/product_reveal_logo_spin_v02/product_reveal_logo_spin_v02_0001.png`.
  Render passes go one level deeper (`…_v02/beauty/`, `…_v02/shadow/`).
- **Blender output path** (`//` = the `.blend`'s folder):
  `//../renders/product_reveal_logo_spin_v02/product_reveal_logo_spin_v02_`
- **Never overwrite a version.** Render v03 into a new folder, then in AE select the
  footage item → File › Replace Footage › File. Layers, effects and keyframes are kept.
  Move the v02 folder (with its sidecar) into `renders/_archive/`.
- **Never rename anything another app links to** — render folders, frames, mixdowns,
  graphics exports. No status tags on them; status goes in a sidecar.
- **Move the whole project folder, never the `.aep` alone.** AE stores an absolute path
  but falls back to the path relative to the `.aep`, which is what makes projects survive
  Creative Cloud sync across machines with different user names.
- **Don't point AE's disk cache or Blender's bakes at a synced drive** by default —
  `_cache/` is for regenerable proxies/pre-renders you deliberately keep with the project.

### Tracking video projects

Filenames can't carry status for linked media, so tracking is sidecars + index:

| What                          | Where                                   | How |
| ----------------------------- | --------------------------------------- | --- |
| Client, deadline, deliverable specs | project `README.md` → Brief        | fill in by hand at kickoff |
| Render version status         | sidecar next to the render **folder**   | `add_meta.py set 04_3d/renders/<name>_v02 --status review --supersedes <name>_v01` |
| Project file status           | `-wip`/`-review` tag on `.aep`/`.blend` — unless another file links to it (an `.aep` imported into another project, a `.blend` linked as a library), then a sidecar | rename, or `add_meta.py set` |
| What was sent / signed off    | sidecar on each file in `07_exports/`   | `--status approved --requested-by client --reason "..."` |
| Project overview              | `INDEX.md` + `assets.csv` at project root | `add_meta.py index <project>` |
| All video projects at once    | `INDEX.md` in `videos/`                 | `add_meta.py index <videos folder>` |

`add_meta.py set` accepts a folder as well as a file — the sidecar
(`<folder>.meta.md`) sits beside the folder, not inside it, so it never pollutes a
sequence import. Re-run `index` after a review round or a delivery.

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
