# File naming conventions

The single source of truth for how files are named across every machine and every
project. Machine-agnostic on purpose: nothing here depends on the OS, the folder
structure, or which tools are installed.

Two derived files are generated from this one and should not be edited directly in
isolation — change this document first, then mirror the change:

- `claude/CLAUDE.snippet.md` — the short always-on directive imported into
  `~/.claude/CLAUDE.md`, so the rules apply to every session on the machine.
- `claude/skills/project-organization/SKILL.md` — the on-demand skill covering
  folder structure and metadata, which references these rules rather than restating them.

---

## Golden rule

**`snake_case` everywhere, no spaces, ever.**

Spaces break command-line tools, URLs and scripts, and behave inconsistently across
macOS, Linux and Windows. Lowercase plus underscores keeps everything portable.

No capitals. No special characters (`&`, `#`, `(`, `)`, `'`). No trailing spaces before
the extension. Extensions are always lowercase.

---

## 1. Design & dev files — versioned

```
{project}_{feature}_v{NN}[-{tag}].{ext}
```

| Part      | Rule                                                | Example        |
| --------- | --------------------------------------------------- | -------------- |
| `project` | The project name, snake_case                        | `precinct`     |
| `feature` | What the file is, snake_case                        | `login_screen` |
| `v{NN}`   | Two-digit version, always zero-padded, starts `v01` | `v03`          |
| `-{tag}`  | Optional status or variant tag (see below)          | `-approved`    |
| `.{ext}`  | Lowercase extension                                 | `.fig`         |

```
precinct_login_screen_v01.fig
precinct_login_screen_v02-dark.fig
precinct_login_screen_v03-wip.fig
precinct_login_screen_v03-review.fig
precinct_login_screen_v04-approved.ai
```

## 2. Research, notes & audits — dated

```
YYYY-MM_topic-name.ext
```

Date first so files sort chronologically. Note the deliberate mix: underscore separates
the date from the topic, hyphens separate words *within* the topic.

```
2026-07_competitor-audit.md
2026-07_accessibility-notes.md
2026-08_user-interview-summary.pdf
```

## 3. Status tags

Appended to the version, in the `-{tag}` slot.

| Tag         | Meaning                                      |
| ----------- | -------------------------------------------- |
| `-wip`      | Work in progress — not ready for anyone else |
| `-review`   | Ready for feedback / sign-off                |
| `-approved` | Signed off — safe to hand off or ship        |

Short **variant** tags use the same slot: `-dark`, `-mobile`, `-alt`. One tag per file —
if you need two axes, the second belongs in `feature`.

## 4. Version numbers

- Always **two digits**: `v01`, `v02`, … `v10`, so they sort correctly.
- **Increment for meaningful iterations**, not every save.
- When a version is superseded, move the old file into the nearest `_archive/`.

## 5. Infrastructure folders

Folders prefixed with `_` sort to the top and are infrastructure, not deliverables:
`_assets`, `_templates`, `_archive`, `_cache`. Never put a deliverable in one.

---

## Do / don't

✅ **Do**

- Use `snake_case` for project names and every file.
- Zero-pad versions (`v01`, not `v1`).
- Keep generated output (`exports/`, `renders/`) separate from working files.
- Archive superseded versions instead of deleting them.

❌ **Don't**

- Use spaces, capitals or special characters.
- Hand-edit anything inside `exports/` or `renders/` — re-export from the source.
- Reuse a version number for a different iteration.

---

## Where this applies

These rules cover **files you create**. They do not override a project's existing
conventions or an ecosystem's mandatory names: `README.md`, `Dockerfile`, `Makefile`,
`CHANGELOG.md`, `LICENSE`, `CLAUDE.md`, `.github/`, framework-mandated filenames
(`page.tsx`, `__init__.py`, `conftest.py`), and language-idiomatic module names all stay
as their ecosystem requires. Match the surrounding code when editing an existing
codebase; apply these rules when naming something new and unconstrained.
