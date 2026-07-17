# UI/UX Project Toolkit

Two small, dependency-free Python scripts that keep every project consistent:

- **`new_project.py`** — scaffolds a standard folder structure and enforces one shared
  file-naming convention across every project.
- **`add_meta.py`** — attaches metadata (who requested a file, why it exists, its status)
  as sidecar files, and rolls them up into a per-project index. See
  [File metadata](#file-metadata-add_metapy).

The goal is simple: every project looks the same, so anyone (including future‑you)
can open any folder and immediately know where things live, what state they're in,
and why each file exists.

---

## Table of contents

1. [Requirements](#requirements)
2. [Quick start](#quick-start)
3. [Command reference](#command-reference)
4. [The folder structure](#the-folder-structure)
5. [The seven disciplines](#the-seven-disciplines)
6. [Discipline subfolders](#discipline-subfolders)
7. [Naming conventions (strict)](#naming-conventions-strict)
8. [Worked examples](#worked-examples)
9. [File metadata (add_meta.py)](#file-metadata-add_metapy)
10. [Rules & do / don't](#rules--do--dont)
11. [FAQ](#faq)

---

## Requirements

- **Python 3.9 or newer** (uses `list[str]` / `dict` type hints).
- No third‑party packages — standard library only.

Check your version:

```bash
python --version      # or: python3 --version
```

---

## Quick start

```bash
# Create a project in the current folder with all defaults
python new_project.py my_app_name

# See exactly what would be created — without touching disk
python new_project.py my_app_name --dry-run

# List the available disciplines and their folder names
python new_project.py --list-disciplines
```

> **Tip:** Always run `--dry-run` first when you use custom `--stages` or
> `--disciplines`. It prints every folder that *would* be created so you can
> confirm the shape before committing to it.

---

## Command reference

```
python new_project.py <project_name> [options]
```

| Argument / option        | Required | Default                                    | Description                                                        |
| ------------------------ | -------- | ------------------------------------------ | ------------------------------------------------------------------ |
| `project_name`           | Yes*     | —                                          | Name of the new project. **Use snake_case** (see conventions).     |
| `--base-dir PATH`        | No       | `.` (current dir)                          | Parent directory where the project folder is created.              |
| `--stages STAGE ...`     | No       | `research prototyping design production`   | Which stage folders to create.                                     |
| `--disciplines DISC ...` | No       | all seven                                  | Which disciplines to include. Keys from `--list-disciplines`.      |
| `--list-disciplines`     | No       | —                                          | Print discipline keys → folder names, then exit.                   |
| `--init-global`          | No       | off                                        | Also create a shared `_global_workspace/` next to the project.     |
| `--force`                | No       | off                                        | Overwrite an existing `README.md` (otherwise it is left untouched). |
| `--dry-run`              | No       | off                                        | Print planned actions without writing anything to disk.            |

\* `project_name` is required for every command **except** `--list-disciplines`.

### Examples

```bash
# Only the disciplines you actually need
python new_project.py voter_portal --disciplines dev design research

# Custom stages (e.g. a quick spike with just two phases)
python new_project.py logo_refresh --stages exploration production --disciplines design illustration

# Create the project somewhere specific
python new_project.py precinct --base-dir "D:/Work/Clients"

# Scaffold the shared workspace once, alongside your first project
python new_project.py precinct --init-global
```

---

## The folder structure

Each project is organized as **stage → discipline → working subfolders**:

```
my_app_name/
├── README.md                     ← auto-generated project metadata + conventions
├── .gitignore                    ← starter ignores for OS/editor/dev junk
├── research/                     ← STAGE
│   ├── 01_dev/                   ← DISCIPLINE
│   │   ├── src/                  ← subfolder
│   │   ├── libs/
│   │   └── _archive/
│   ├── 02_research/
│   │   ├── references/
│   │   ├── notes/
│   │   └── _archive/
│   ├── 03_design/  … 07_diagrams/
│   ├── _assets/                  ← shared assets for this stage
│   └── _templates/               ← reusable templates for this stage
├── prototyping/                  ← same discipline tree as above
├── design/
└── production/                   ← final, approved, deliverable-ready ONLY
```

- **Stages** describe *where the work is in the process* (research → prototyping → design → production).
- **Disciplines** describe *what kind of work it is* (dev, design, motion, 3d, …).
- The numeric prefixes (`01_`, `02_` …) keep disciplines in a **fixed sort order** in every file browser.
- Folders prefixed with `_` (underscore) sort to the top and are **infrastructure**, not deliverables:
  `_assets`, `_templates`, `_archive`, `_cache`.
- Empty folders contain a `.gitkeep` so the structure survives in version control.
- A starter **`.gitignore`** is written at the project root (OS/editor/dev junk). It
  deliberately leaves `_cache/` alone — those folders manage their own ignores.

### Optional shared workspace (`--init-global`)

`_global_workspace/` sits **next to** your projects and holds cross‑project resources
(brand assets, shared component libraries, reusable templates). It mirrors the
discipline structure but has **no stages** — it isn't tied to any single project.

---

## The seven disciplines

| Key            | Folder             | Use for                                   |
| -------------- | ------------------ | ----------------------------------------- |
| `dev`          | `01_dev`           | JS, SCSS, Python, QML source files        |
| `research`     | `02_research`      | References, notes, briefs, audits         |
| `design`       | `03_design`        | UI layouts, icons, color systems          |
| `illustration` | `04_illustration`  | Illustrations and graphics                |
| `motion`       | `05_motion`        | After Effects projects and exports        |
| `3d`           | `06_3d`            | Blender files, models, rigs, renders      |
| `diagrams`     | `07_diagrams`      | Flowcharts, schematics, specs             |

> The numeric prefix is part of the folder name but **not** the key.
> You pass the key (`dev`, `3d`, …) on the command line; the script creates the
> numbered folder for you.

---

## Discipline subfolders

Each discipline gets a purpose-built set of subfolders:

| Discipline     | Subfolders                                       |
| -------------- | ------------------------------------------------ |
| `dev`          | `src` · `libs` · `_archive`                       |
| `research`     | `references` · `notes` · `_archive`               |
| `design`       | `working` · `exports` · `_archive`                |
| `illustration` | `working` · `exports` · `_archive`                |
| `motion`       | `projects` · `renders` · `_cache` · `_archive`    |
| `3d`           | `scenes` · `assets` · `renders` · `_cache` · `_archive` |
| `diagrams`     | `working` · `exports` · `_archive`                |

Convention for the common ones:

- **`working/`** — live, editable source files (`.fig`, `.ai`, `.aep`, `.blend`).
- **`exports/`** / **`renders/`** — generated output (`.png`, `.svg`, `.mp4`). Never hand-edit these.
- **`_archive/`** — superseded versions you want to keep but not see day-to-day.
- **`_cache/`** — regenerable temp files (previews, proxies). Safe to delete anytime.
  These folders carry a self-ignoring `.gitignore` (`*` + `!.gitignore`), so the folder
  stays in version control but its contents are **never committed**.

---

## Naming conventions (strict)

> **Golden rule: `snake_case` everywhere, no spaces, ever.**
> Spaces break command-line tools, URLs, and scripts, and behave inconsistently
> across macOS / Linux / Windows. Lowercase + underscores keep everything portable.

### 1. Design & dev files — versioned

```
{project}_{feature}_v{NN}[-{tag}].{ext}
```

| Part        | Rule                                              | Example        |
| ----------- | ------------------------------------------------- | -------------- |
| `project`   | The project name, snake_case                      | `precinct`     |
| `feature`   | What the file is, snake_case                      | `login_screen` |
| `v{NN}`     | Two-digit version, always zero-padded, starts `v01` | `v03`        |
| `-{tag}`    | Optional status/variant tag (see below)           | `-approved`    |
| `.{ext}`    | Lowercase extension                               | `.fig`         |

Examples:

```
precinct_login_screen_v01.fig
precinct_login_screen_v02-dark.fig
precinct_login_screen_v03-wip.fig
precinct_login_screen_v03-review.fig
precinct_login_screen_v04-approved.ai
```

### 2. Research / notes / audits — dated

```
YYYY-MM_topic-name.ext
```

Date first so files sort chronologically. Examples:

```
2026-07_competitor-audit.md
2026-07_accessibility-notes.md
2026-08_user-interview-summary.pdf
```

### 3. Status tags (append to the version)

| Tag         | Meaning                                            |
| ----------- | -------------------------------------------------- |
| `-wip`      | Work in progress — not ready for anyone else       |
| `-review`   | Ready for feedback / sign-off                      |
| `-approved` | Signed off — safe to hand off or ship              |

You may also use short **variant** tags in the same slot: `-dark`, `-mobile`, `-alt`.

### 4. Version numbers

- Always **two digits**: `v01`, `v02`, … `v10` (so they sort correctly).
- **Increment for meaningful iterations**, not every save.
- When a version is superseded, move the old file into the discipline's `_archive/`.

### 5. `production/` is sacred

Only **final, approved, deliverable-ready** files go in a `production/` stage folder.
If it isn't signed off, it lives in `design/` or `prototyping/` instead.

---

## Worked examples

**A designer's login screen, from first draft to shipped:**

```
prototyping/03_design/working/precinct_login_screen_v01-wip.fig
design/03_design/working/precinct_login_screen_v02-review.fig
design/03_design/working/precinct_login_screen_v03-approved.fig
design/03_design/exports/precinct_login_screen_v03.png
production/03_design/exports/precinct_login_screen_v03.png     ← the deliverable
```

**A research audit:**

```
research/02_research/notes/2026-07_competitor-audit.md
research/02_research/references/2026-07_design-system-links.md
```

**A motion piece:**

```
design/05_motion/projects/precinct_intro_v02-wip.aep
design/05_motion/renders/precinct_intro_v02.mp4
```

---

## File metadata (`add_meta.py`)

Filenames tell you *what* and *what state* a file is in — but not **who asked for it**
or **why it exists**. `add_meta.py` attaches that context as a small **sidecar** file
(`<filename>.meta.md`) that lives right next to the asset.

Sidecars work for **any** file type — including binaries like `.fig`, `.ai`, `.aep`,
and `.blend` — and travel with the asset through Creative Cloud sync and version
control. (Metadata embedded *inside* files, or in NTFS attributes, doesn't survive
those round-trips; a sidecar does.)

### Commands

```bash
# Attach / update metadata on a file
python add_meta.py set design/03_design/working/precinct_login_screen_v03-approved.fig \
    --requested-by product_team \
    --reason "Redesign login flow for accessibility audit AA-2026-07" \
    --status approved --tags login accessibility \
    --supersedes precinct_login_screen_v02.fig

# Read a file's metadata
python add_meta.py show design/03_design/working/precinct_login_screen_v03-approved.fig

# Rebuild a project-wide INDEX.md + assets.csv from every sidecar in the tree
python add_meta.py index precinct
```

### `set` options

| Option            | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `--requested-by`  | Who asked for the file                                   |
| `--reason`        | Why it was created                                       |
| `--author`        | Who made it (defaults to the current OS user)            |
| `--status`        | `wip` · `review` · `approved` (validated)                |
| `--supersedes`    | The filename this version replaces                       |
| `--tags TAG ...`  | Free-form tags for grouping/searching                   |
| `--note`          | Free-text note stored in the sidecar body               |
| `-i`, `--interactive` | Prompt for every field instead of passing flags     |
| `--dry-run`       | Print the result without writing                         |

Re-running `set` **updates** the sidecar in place: the original `created` date is
preserved, `updated` is refreshed, and fields you don't pass again are kept as-is.

### Guided (interactive) mode

Not comfortable with long command lines? Run `set` with `-i` and it walks you through
each field, offering the current value as the default (just press Enter to keep it):

```bash
python add_meta.py set precinct_login_screen_v03-approved.fig -i
```
```
Editing metadata for precinct_login_screen_v03-approved.fig  (Enter keeps the [current] value)

  Requested by [product_team]:
  Reason [Redesign login flow…]:
  Author [srdjan.markovic]:
  Status (wip/review/approved) [approved]:
  Supersedes:
  Tags (comma- or space-separated) [login, accessibility]:
  Notes:
```

Flags and `-i` combine — any flags you pass pre-fill the prompts' defaults.

### What a sidecar looks like

```markdown
---
file: precinct_login_screen_v03-approved.fig
created: 2026-07-17
updated: 2026-07-17
author: srdjan.markovic
requested_by: product_team
reason: Redesign login flow for accessibility audit AA-2026-07
status: approved
supersedes: precinct_login_screen_v02.fig
tags: [login, accessibility]
---

Notes: dark-mode variant pending in v04.
```

### The project index

`add_meta.py index <project>` scans the whole tree and writes two files at the root:

- **`INDEX.md`** — a readable table of every tracked file (status, requester, reason, author, updated).
- **`assets.csv`** — the same data as a spreadsheet you can sort/filter/pivot.

Re-run it whenever you want a fresh snapshot — it's regenerated from the sidecars,
so it never drifts out of sync with reality.

---

## Rules & do / don't

✅ **Do**

- Use `snake_case` for the project name and every file.
- Zero-pad versions (`v01`, not `v1`).
- Keep exports/renders separate from working files.
- Archive old versions instead of deleting them.
- Run `--dry-run` before non-default runs.

❌ **Don't**

- Use spaces, capital letters, or special characters (`&`, `#`, `()`).
- Put unfinished work in `production/`.
- Hand-edit files inside `exports/` or `renders/` — re-export from the source instead.
- Invent new discipline folders ad-hoc — extend the script's `DISCIPLINES` map instead so everyone stays in sync.

---

## FAQ

**What happens if the project already exists?**
The script uses `mkdir(exist_ok=True)`, so it will **merge** into an existing folder
rather than error, and existing files are left alone. An existing `README.md` is
**preserved** by default (you'll see a `[skip]` message) — pass `--force` to regenerate
it. Run `--dry-run` first if you're pointing at an existing project.

**Are project and stage names validated?**
Yes. Both must be `snake_case` (lowercase letters, digits, single underscores). Names
with spaces, capitals, or special characters are rejected with a clear error before
anything is written.

**Can I add a new discipline?**
Yes — edit `DISCIPLINES` and `DISCIPLINE_SUBFOLDERS` at the top of `new_project.py`.
Keep the numeric prefix sequence intact so sort order stays predictable.

**Why `.gitkeep` files everywhere?**
Git doesn't track empty folders. The `.gitkeep` placeholders keep the full structure
intact when the project is committed. They're harmless and can be deleted once a
folder has real content. Cache folders (`_cache/`) get a `.gitignore` instead, which
both keeps the folder and ensures its regenerable contents are never committed.

**Do I have to use all four stages?**
No. Use `--stages` to pick your own (e.g. `--stages exploration production`).
Stage names are free‑form, but keep them `snake_case` and consistent across projects.
