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

This repo is also the **single source of truth for the naming conventions** across every
machine. Clone it once per machine, run `install.py`, and Claude Code applies the same
rules everywhere. See [Multi-machine setup](#multi-machine-setup).

---

## Table of contents

1. [Requirements](#requirements)
2. [Quick start](#quick-start)
3. [Multi-machine setup](#multi-machine-setup)
4. [Profiles](#profiles)
5. [Command reference](#command-reference)
6. [The folder structure](#the-folder-structure)
7. [The seven disciplines](#the-seven-disciplines)
8. [Discipline subfolders](#discipline-subfolders)
9. [Video / motion projects](#video--motion-projects)
10. [Naming conventions (strict)](#naming-conventions-strict)
11. [Worked examples](#worked-examples)
12. [File metadata (add_meta.py)](#file-metadata-add_metapy)
13. [Rules & do / don't](#rules--do--dont)
14. [FAQ](#faq)

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

## Multi-machine setup

The naming conventions only pay off if they're **identical everywhere**. So the repo is
the source of truth and each machine points at its own clone — nothing is copied by hand,
and `git pull` updates every machine.

```bash
git clone <your-remote> ~/dev/ux-toolkit
cd ~/dev/ux-toolkit

python install.py                          # dry run — prints what it would change
python install.py --apply                  # work machine (default profile: work)
python install.py --apply --profile personal   # private machine
```

`install.py` does three things, all idempotent and all reversible with `--uninstall`:

| What                                        | Where                                    | Why |
| ------------------------------------------- | ---------------------------------------- | --- |
| `@`-imports `claude/CLAUDE.snippet.md`      | `~/.claude/CLAUDE.md`                    | Naming rules in context for **every** Claude Code session on the machine |
| Links `claude/skills/project-organization/` | `~/.claude/skills/`                      | Folder structure + metadata guidance, loaded only when relevant |
| Writes `profile = <name>`                   | `~/.uxkit`                               | This machine's default project shape |

Notes:

- It **never clobbers** your existing `~/.claude/CLAUDE.md` — the import goes in a marked
  block, and everything around it is preserved. `--uninstall` removes just that block.
- The skill is **symlinked** where possible, so a `git pull` is enough. On Windows without
  Developer Mode symlinks aren't permitted, so it falls back to a copy and tells you to
  re-run `install.py` after pulling. `--copy` forces that behaviour anywhere.
- A `project-organization` directory you wrote yourself is never overwritten without
  `--force`.
- On macOS, `./install.sh` is a wrapper that finds `python3` for you.
- Restart Claude Code afterwards so it picks up the new `CLAUDE.md` and skill.

### Which file holds which rules

| File                                            | Loaded         | Contains |
| ----------------------------------------------- | -------------- | -------- |
| `CONVENTIONS.md`                                | by humans      | The canonical, full naming reference |
| `claude/CLAUDE.snippet.md`                      | every session  | The short always-on directive — kept deliberately brief, since it costs context every time |
| `claude/skills/project-organization/SKILL.md`   | on demand      | Stages, disciplines, file placement, metadata workflow |

Change `CONVENTIONS.md` first, then mirror the change into the other two.

---

## Profiles

A **profile** answers "what shape should a project be?" — it's a property of the
*machine*, not of each project, so the same command gives you the full studio structure
at work and something lean at home.

```bash
python new_project.py --list-profiles      # what's available, and this machine's default
python new_project.py my_app               # uses the machine default
python new_project.py my_app --profile personal
```

| Profile    | Stages                                          | Disciplines            |
| ---------- | ----------------------------------------------- | ---------------------- |
| `work`     | research · prototyping · design · production     | all seven              |
| `personal` | exploration · production                         | dev · design · research |

Profiles are plain JSON in `profiles/` (JSON rather than TOML so the toolkit keeps
running on Python 3.9 with zero dependencies). Add or edit them freely — `personal.json`
is a starting point, not a decision you're locked into. **The naming conventions are not
part of a profile**; they're identical on every machine by design.

Resolution order, highest first:

1. Explicit `--stages` / `--disciplines` — these override only the axis they name, so
   `--stages spike --profile personal` keeps that profile's disciplines.
2. `--profile NAME`
3. `profile = <name>` in `~/.uxkit` (written by `install.py`)
4. Built-in `work`

Every run prints which of these it used, e.g. `Structure from: profile 'personal'`.

---

## Command reference

```
python new_project.py <project_name> [options]
```

| Argument / option        | Required | Default                     | Description                                                        |
| ------------------------ | -------- | --------------------------- | ------------------------------------------------------------------ |
| `project_name`           | Yes*     | —                           | Name of the new project. **Use snake_case** (see conventions).     |
| `--base-dir PATH`        | No       | `.` (current dir)           | Parent directory where the project folder is created.              |
| `--type ux\|video`       | No       | `ux`                        | `video` builds the fixed video pipeline instead. See [Video / motion projects](#video--motion-projects). |
| `--profile NAME`         | No       | `~/.uxkit`, else `work`     | Structure profile to use. See [Profiles](#profiles).               |
| `--stages STAGE ...`     | No       | the profile's stages        | Which stage folders to create. Overrides the profile.              |
| `--disciplines DISC ...` | No       | the profile's disciplines   | Which disciplines to include. Keys from `--list-disciplines`.      |
| `--list-profiles`        | No       | —                           | Print profiles, their shape and this machine's default, then exit. |
| `--list-disciplines`     | No       | —                           | Print discipline keys → folder names, then exit.                   |
| `--init-global`          | No       | off                         | Also create a shared `_global_workspace/` next to the project (video: `_assets/` + `_templates/`). |
| `--force`                | No       | off                         | Overwrite an existing `README.md` (otherwise it is left untouched). |
| `--dry-run`              | No       | off                         | Print planned actions without writing anything to disk.            |

\* `project_name` is required for every command **except** `--list-disciplines` and
`--list-profiles`.

### Examples

```bash
# The lean structure, wherever you are
python new_project.py side_project --profile personal

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

## Video / motion projects

Video work flows one way — sources → graphics / 3D / audio → motion → exports — so a video
project skips stages and gets a **fixed pipeline**. Every folder is always created, whether
the project is After Effects-heavy or Blender-heavy, and the numbers never change.
Profiles, `--stages` and `--disciplines` don't apply.

```bash
python new_project.py product_reveal --type video --base-dir "D:/videos"
python new_project.py product_reveal --type video --init-global    # + shared _assets/ _templates/
python new_project.py --list-disciplines --type video
```

```
videos/
├── _assets/                 music · sfx · fonts · luts · brand   ← shared by every project
├── _templates/              ae · blender
└── product_reveal/
    ├── README.md            brief, pipeline, working rules, tracking commands
    ├── .gitignore           + *.pkf, *.cfa, *.blend1
    ├── 01_docs/             script, brief, storyboard, client feedback
    ├── 02_sources/          video · audio · images · other      ← received, never edited
    ├── 03_graphics/         working · exports · _archive         (Photoshop, Illustrator, Figma)
    ├── 04_3d/               scenes · assets · renders · renders/_archive · _cache · _archive
    ├── 05_audio/            sessions · mixdowns · _archive       (Audition)
    ├── 06_motion/           projects · renders · renders/_archive · _cache · _archive  (After Effects)
    └── 07_exports/          _archive                             ← what the client receives
```

- **Came from outside** ⇒ `02_sources/`. **Made by you** ⇒ the folder of the tool that made
  it. **Used by several projects** ⇒ `videos/_assets/`.
- `06_motion/renders/` holds full-quality masters; `07_exports/` holds compressed delivery
  encodes (`product_reveal_full_v03-web.mp4`).
- App-generated folders (AE `Auto-Save/`, Audition `Backup/` and `Imported Files/`) stay
  where the app puts them.

### Image sequences

One folder per sequence **and** version, frames named like the folder (see
[`CONVENTIONS.md`](CONVENTIONS.md#5-image-sequences)):

```
04_3d/renders/product_reveal_logo_spin_v02/product_reveal_logo_spin_v02_0001.png
```

- **Blender output path:** `//../renders/product_reveal_logo_spin_v02/product_reveal_logo_spin_v02_`
  (`//` is the `.blend`'s folder; Blender appends the frame number).
- **In After Effects:** File › Import, pick the first frame, tick *PNG Sequence*. From
  `06_motion/projects/` the footage sits at `../../04_3d/renders/…` — AE stores the absolute
  path but falls back to this relative one, so keep the project folder intact and **never
  move the `.aep` on its own**.
- **New version:** render v03 into a new folder, select the v02 item in AE → File › Replace
  Footage › File (layers, effects and keyframes are kept), then move the v02 folder and its
  sidecar into `renders/_archive/`. Never overwrite frames in place.
- **Never rename linked media** to change its status — that breaks the link. Use a sidecar.

### Tracking video projects

| What                                 | Where                                     | How |
| ------------------------------------ | ----------------------------------------- | --- |
| Client, deadline, deliverable specs  | project `README.md` → *Brief*             | by hand at kickoff |
| Render version status                | sidecar beside the render **folder**      | `add_meta.py set 04_3d/renders/<name>_v02 --status review --supersedes <name>_v01` |
| `.aep` / `.blend` status             | `-wip` / `-review` tag, or a sidecar if another file links to it | rename, or `add_meta.py set` |
| What was sent and signed off         | sidecar on each file in `07_exports/`     | `--status approved --requested-by client` |
| One project at a glance              | `INDEX.md` + `assets.csv` in the project  | `add_meta.py index <project>` |
| Every video project at once          | `INDEX.md` + `assets.csv` in `videos/`    | `add_meta.py index <videos folder>` |

`add_meta.py set` works on folders as well as files; the sidecar (`<folder>.meta.md`) sits
beside the folder, so it never gets picked up by a sequence import.

---

## Naming conventions (strict)

> 📌 **[`CONVENTIONS.md`](CONVENTIONS.md) is the canonical copy** — it's what the Claude
> Code directive and skill are generated from. Edit that file first; this section is a
> summary for readers who are already here.

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
No. Use `--stages` to pick your own (e.g. `--stages exploration production`), or set a
[profile](#profiles) so the machine defaults to the shape you actually want.

**How do I get the naming rules onto another machine?**
Clone the repo there and run `python install.py --apply` — see
[Multi-machine setup](#multi-machine-setup). Don't copy the folder around by hand; you'd
end up with three drifting versions of the same rules, which defeats the point.

**Can each machine have a different structure but the same naming rules?**
That's exactly what profiles are for. Structure is per-machine (`~/.uxkit`); naming is
global and identical everywhere.

**Why is `~/.uxkit` outside the repo?**
It's a per-machine choice, not a shared one — committing it would mean every machine
fighting over the same default. `install.py` writes it once and won't silently change an
existing value unless you pass `--profile`.

**Claude isn't following the naming rules — what do I check?**
1. `~/.claude/CLAUDE.md` contains the `@…/CLAUDE.snippet.md` line (re-run `install.py`).
2. The path in that line actually resolves — it breaks if you move the clone. Re-running
   `install.py --apply` rewrites it.
3. Claude Code was restarted after installing.
4. Remember the rules deliberately yield to an existing codebase's conventions and
   ecosystem-mandated filenames (`README.md`, `page.tsx`, `__init__.py`).
