#!/usr/bin/env python3
"""
new_project.py — Project folder scaffolder for UI/UX workflow
Usage:
    python new_project.py my_app_name
    python new_project.py my_app_name --stages research prototyping design production
    python new_project.py my_app_name --disciplines dev design 3d
    python new_project.py my_app_name --list-disciplines
    python new_project.py my_app_name --dry-run
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

# ── Discipline definitions ─────────────────────────────────────────────────────

DISCIPLINES = {
    "dev":          ("01_dev",          "JS, SCSS, Python, QML source files"),
    "research":     ("02_research",     "References, notes, briefs, audits"),
    "design":       ("03_design",       "UI layouts, icons, color systems"),
    "illustration": ("04_illustration", "Illustrations and graphics"),
    "motion":       ("05_motion",       "After Effects projects and exports"),
    "3d":           ("06_3d",           "Blender files, models, rigs, renders"),
    "diagrams":     ("07_diagrams",     "Flowcharts, schematics, specs"),
}

# Sub-structure within each discipline folder
DISCIPLINE_SUBFOLDERS = {
    "dev":          ["src", "libs", "_archive"],
    "research":     ["references", "notes", "_archive"],
    "design":       ["working", "exports", "_archive"],
    "illustration": ["working", "exports", "_archive"],
    "motion":       ["projects", "renders", "_cache", "_archive"],
    "3d":           ["scenes", "assets", "renders", "_cache", "_archive"],
    "diagrams":     ["working", "exports", "_archive"],
}

DEFAULT_STAGES = ["research", "prototyping", "design", "production"]
DEFAULT_DISCIPLINES = list(DISCIPLINES.keys())

README_TEMPLATE = """\
# {project_name}

Created: {date}

## Stages
{stage_list}

## Disciplines used
{discipline_list}

## File naming conventions
- Design/dev files:    `{project_name}_feature_v01.ext`
- Research files:      `YYYY-MM_topic-name.ext`
- Status tags:         `-wip` · `-review` · `-approved`
- `production/` only: final, approved, deliverable-ready files
- No spaces — use snake_case throughout

## Notes
"""

# Project-root .gitignore. Note: `_cache/` folders are intentionally NOT listed here —
# each carries its own self-ignoring .gitignore so the folder is kept while its
# contents stay out of version control. A `**/_cache/` rule here would drop the folder.
GITIGNORE_PROJECT = """\
# ── OS / editor junk ─────────────────────────────
.DS_Store
Thumbs.db
desktop.ini
*.swp
*~

# ── Temp / scratch ───────────────────────────────
*.tmp
*.bak

# ── Dev artifacts ────────────────────────────────
node_modules/
__pycache__/
.venv/
dist/
build/
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

# Valid snake_case: lowercase letters/digits, underscores between, no leading/
# trailing/double underscore, no spaces or special characters.
NAME_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def validate_name(name: str, label: str = "project name") -> None:
    """Enforce snake_case naming; exit with a helpful message if invalid."""
    if not NAME_RE.match(name):
        print(f"[error] '{name}' is not a valid {label}.")
        print("        Use lowercase letters, digits and single underscores only")
        print("        (e.g. my_app_name) - no spaces, capitals or special characters.")
        sys.exit(1)


def resolve_disciplines(keys: list[str]) -> dict[str, tuple[str, str]]:
    """Return ordered discipline dict for the given shorthand keys."""
    unknown = [k for k in keys if k not in DISCIPLINES]
    if unknown:
        print(f"[error] Unknown discipline(s): {', '.join(unknown)}")
        print(f"        Valid options: {', '.join(DISCIPLINES)}")
        sys.exit(1)
    return {k: DISCIPLINES[k] for k in keys}


def make_dir(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry] mkdir {path}")
    else:
        path.mkdir(parents=True, exist_ok=True)


def make_gitkeep(path: Path, dry_run: bool) -> None:
    target = path / ".gitkeep"
    if dry_run:
        print(f"  [dry] touch {target}")
    else:
        target.touch(exist_ok=True)


# .gitignore that keeps the folder in version control but ignores its contents.
# Used for regenerable cache folders so previews/proxies never get committed.
GITIGNORE_CACHE = "# Regenerable cache — contents ignored, folder kept.\n*\n!.gitignore\n"


def make_gitignore(path: Path, dry_run: bool) -> None:
    target = path / ".gitignore"
    if dry_run:
        print(f"  [dry] write {target}")
    else:
        target.write_text(GITIGNORE_CACHE, encoding="utf-8")


def is_cache(folder: str) -> bool:
    return folder == "_cache"


def write_guarded_file(path: Path, content: str, dry_run: bool, force: bool) -> None:
    """Write a text file, but never clobber an existing one unless --force."""
    if dry_run:
        print(f"  [dry] write {path}")
    elif path.exists() and not force:
        print(f"  [skip] {path} already exists — not overwritten (use --force)")
    else:
        path.write_text(content, encoding="utf-8")


# ── Scaffold builders ─────────────────────────────────────────────────────────

def build_discipline_tree(
    parent: Path,
    disciplines: dict[str, tuple[str, str]],
    dry_run: bool,
) -> None:
    """Create each discipline folder and its subfolders under `parent`."""
    for key, (folder_name, _) in disciplines.items():
        disc_path = parent / folder_name
        make_dir(disc_path, dry_run)
        for sub in DISCIPLINE_SUBFOLDERS.get(key, []):
            sub_path = disc_path / sub
            make_dir(sub_path, dry_run)
            # Cache folders get a self-ignoring .gitignore; everything else a .gitkeep.
            if is_cache(sub):
                make_gitignore(sub_path, dry_run)
            else:
                make_gitkeep(sub_path, dry_run)


def scaffold_project(
    base_dir: Path,
    project_name: str,
    stages: list[str],
    disciplines: dict[str, tuple[str, str]],
    dry_run: bool,
    force: bool,
) -> None:
    root = base_dir / project_name
    make_dir(root, dry_run)

    for stage in stages:
        stage_path = root / stage
        make_dir(stage_path, dry_run)

        # Every stage gets a discipline subfolder for each active discipline
        build_discipline_tree(stage_path, disciplines, dry_run)

        # Shared assets + templates inside each stage
        for meta in ("_assets", "_templates"):
            meta_path = stage_path / meta
            make_dir(meta_path, dry_run)
            make_gitkeep(meta_path, dry_run)

    # Project-level README
    readme_path = root / "README.md"
    stage_list = "\n".join(f"  - {s}" for s in stages)
    disc_list  = "\n".join(f"  - {k}: {v[1]}" for k, v in disciplines.items())
    content = README_TEMPLATE.format(
        project_name=project_name,
        date=datetime.date.today().isoformat(),
        stage_list=stage_list,
        discipline_list=disc_list,
    )
    write_guarded_file(readme_path, content, dry_run, force)

    # Project-root .gitignore for common OS/editor/dev junk.
    write_guarded_file(root / ".gitignore", GITIGNORE_PROJECT, dry_run, force)

    print(f"\n{'[dry-run] ' if dry_run else ''}Project '{project_name}' scaffolded at {root}")
    print(f"  Stages:      {', '.join(stages)}")
    print(f"  Disciplines: {', '.join(disciplines)}")


def scaffold_global_workspace(base_dir: Path, dry_run: bool) -> None:
    """Create the global workspace folder at the same level as projects/."""
    workspace = base_dir / "_global_workspace"
    make_dir(workspace, dry_run)

    build_discipline_tree(workspace, DISCIPLINES, dry_run)

    for meta in ("_assets", "_templates"):
        meta_path = workspace / meta
        make_dir(meta_path, dry_run)
        make_gitkeep(meta_path, dry_run)

    print(f"\n{'[dry-run] ' if dry_run else ''}Global workspace created at {workspace}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new project folder with the standard UI/UX structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the new project (snake_case recommended)",
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Parent directory where the project folder will be created (default: current dir)",
    )
    parser.add_argument(
        "--stages",
        nargs="+",
        default=DEFAULT_STAGES,
        metavar="STAGE",
        help=f"Stage folders to create (default: {' '.join(DEFAULT_STAGES)})",
    )
    parser.add_argument(
        "--disciplines",
        nargs="+",
        default=DEFAULT_DISCIPLINES,
        metavar="DISC",
        help="Disciplines to include (default: all). See --list-disciplines.",
    )
    parser.add_argument(
        "--list-disciplines",
        action="store_true",
        help="Print available discipline keys and exit",
    )
    parser.add_argument(
        "--init-global",
        action="store_true",
        help="Also create the _global_workspace folder alongside the project",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing README.md (by default it is left untouched)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without touching the filesystem",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_disciplines:
        print("Available disciplines:")
        for key, (folder_name, desc) in DISCIPLINES.items():
            print(f"  {key:<14} -> {folder_name:<22} {desc}")
        sys.exit(0)

    if not args.project_name:
        print("[error] project_name is required unless using --list-disciplines")
        sys.exit(1)

    validate_name(args.project_name)
    for stage in args.stages:
        validate_name(stage, label="stage name")

    # Drop duplicate stages while preserving the order they were given.
    stages = list(dict.fromkeys(args.stages))

    base_dir     = Path(args.base_dir).expanduser().resolve()
    disciplines  = resolve_disciplines(args.disciplines)

    if args.init_global:
        scaffold_global_workspace(base_dir, args.dry_run)

    scaffold_project(
        base_dir=base_dir,
        project_name=args.project_name,
        stages=stages,
        disciplines=disciplines,
        dry_run=args.dry_run,
        force=args.force,
    )

    if not args.dry_run:
        print("\nDone. Open README.md inside the project to add your notes.")


if __name__ == "__main__":
    main()
