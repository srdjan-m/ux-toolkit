#!/usr/bin/env python3
"""
new_project.py — Project folder scaffolder for UI/UX workflow
Usage:
    python new_project.py my_app_name
    python new_project.py my_app_name --profile personal
    python new_project.py my_app_name --stages research prototyping design production
    python new_project.py my_app_name --disciplines dev design 3d
    python new_project.py my_app_name --list-disciplines
    python new_project.py --list-profiles
    python new_project.py my_app_name --dry-run
    python new_project.py product_reveal --type video
    python new_project.py product_reveal --type video --init-global

The structure a machine produces by default comes from a profile (see profiles/).
Set the machine default once in ~/.uxkit — `profile = personal` — so the same command
gives the full studio structure at work and a lean one on a private machine, while the
file naming conventions stay identical everywhere.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Optional  # PEP 604 `str | None` needs 3.10; this keeps the 3.9 floor

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

# ── Video projects ────────────────────────────────────────────────────────────
# Video work flows one way — sources → graphics / 3d / audio → motion → exports — so
# it gets a flat pipeline instead of stage → discipline. Every folder is always
# created, whether the project is 2D- or 3D-heavy, and the numbers never change:
# 06_motion means the same thing in every video project. Not driven by profiles —
# a video project has the same shape on every machine.

VIDEO_FOLDERS = {
    "docs":     ("01_docs",     "Script, brief, storyboard, client feedback"),
    "sources":  ("02_sources",  "Received material, never edited: video, audio, images"),
    "graphics": ("03_graphics", "Photoshop / Illustrator / Figma graphics"),
    "3d":       ("04_3d",       "Blender scenes, assets, image-sequence renders"),
    "audio":    ("05_audio",    "Audition sessions and mixdowns"),
    "motion":   ("06_motion",   "After Effects projects and master renders"),
    "exports":  ("07_exports",  "Delivery encodes sent to the client"),
}

# Nested paths are allowed: renders keep their own _archive so superseded sequence
# folders don't mix with superseded .blend / .aep files.
VIDEO_SUBFOLDERS = {
    "docs":     [],
    "sources":  ["video", "audio", "images", "other"],
    "graphics": ["working", "exports", "_archive"],
    "3d":       ["scenes", "assets", "renders", "renders/_archive", "_cache", "_archive"],
    "audio":    ["sessions", "mixdowns", "_archive"],
    "motion":   ["projects", "renders", "renders/_archive", "_cache", "_archive"],
    "exports":  ["_archive"],
}

# Shared across every video project, created next to them with --init-global.
VIDEO_WORKSPACE = {
    "_assets":    ["music", "sfx", "fonts", "luts", "brand"],
    "_templates": ["ae", "blender"],
}

# ── Profiles ──────────────────────────────────────────────────────────────────
# A profile is the machine-level answer to "what shape should a project be?".
# JSON rather than TOML so the script keeps working on Python 3.9 with no
# dependencies (tomllib only landed in 3.11).

PROFILE_DIR = Path(__file__).resolve().parent / "profiles"
CONFIG_PATH = Path.home() / ".uxkit"
FALLBACK_PROFILE = "work"

# Used when no profile file can be found at all, so the script still runs from a
# bare checkout with profiles/ missing.
BUILTIN_PROFILE = {
    "description": "Built-in fallback — full structure.",
    "stages": DEFAULT_STAGES,
    "disciplines": DEFAULT_DISCIPLINES,
}

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

VIDEO_README_TEMPLATE = """\
# {project_name}

Created: {date}
Type: video

## Brief
- Client / requested by:
- Deadline:
- Deliverables (resolution · fps · duration · format):

## Pipeline
{folder_list}

## Working rules
- `02_sources/` holds received material only. Never edit it; work on copies elsewhere.
- File names: `{project_name}_feature_v01.ext` (`.aep`, `.blend`, `.psd`, `.sesx`).
- Image sequences: one folder per sequence and version, frames named like the folder:
  `04_3d/renders/{project_name}_shot_v01/{project_name}_shot_v01_0001.png`
  Blender output path: `//../renders/{project_name}_shot_v01/{project_name}_shot_v01_`
- Never rename a file or folder another app links to (renders, mixdowns, exports
  used in AE). Track its status in a sidecar instead — see Tracking.
- New render version: render into a new `_v02` folder, then in AE select the old item →
  File › Replace Footage › File. Move the old folder (and its `.meta.md`) into
  `renders/_archive/`.
- Move or copy the whole project folder, never the `.aep` alone — AE relinks footage
  relative to the project file.
- Leave app-generated folders where the app puts them (AE `Auto-Save/`, Audition
  `Backup/` and `Imported Files/`).

## Tracking
Status lives in `.meta.md` sidecars, never in the names of linked files. Run from this
folder, with `<ux-toolkit>` being wherever the toolkit is cloned:

    python <ux-toolkit>/add_meta.py set 04_3d/renders/{project_name}_shot_v02 --status review --reason "..."
    python <ux-toolkit>/add_meta.py set 07_exports/{project_name}_full_v03-web.mp4 --status approved --requested-by client
    python <ux-toolkit>/add_meta.py index .     # regenerates INDEX.md + assets.csv

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

# Appended for video projects: files the apps regenerate on their own.
GITIGNORE_VIDEO = """\

# ── Video apps (regenerable) ─────────────────────
*.pkf
*.cfa
*.blend1
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


def available_profiles() -> list[str]:
    """Profile names found in profiles/, sorted."""
    if not PROFILE_DIR.is_dir():
        return []
    return sorted(p.stem for p in PROFILE_DIR.glob("*.json"))


def load_profile(name: str) -> dict:
    """Read profiles/<name>.json and validate its shape."""
    path = PROFILE_DIR / f"{name}.json"
    if not path.is_file():
        found = available_profiles()
        print(f"[error] Unknown profile '{name}' (looked for {path}).")
        print(f"        Available: {', '.join(found) if found else '(none found)'}")
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[error] Could not read profile '{name}': {exc}")
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"[error] Profile '{name}' must be a JSON object.")
        sys.exit(1)

    for key in ("stages", "disciplines"):
        value = data.get(key)
        if not isinstance(value, list) or not value or not all(
            isinstance(item, str) for item in value
        ):
            print(f"[error] Profile '{name}': '{key}' must be a non-empty list of strings.")
            sys.exit(1)

    return data


def read_configured_profile() -> Optional[str]:
    """Machine default profile from ~/.uxkit (`profile = personal`), if set.

    Unrecognized keys are ignored so the file can grow without breaking old checkouts.
    """
    if not CONFIG_PATH.is_file():
        return None
    try:
        lines = CONFIG_PATH.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"[warn] Could not read {CONFIG_PATH}: {exc}")
        return None

    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == "profile":
            name = value.strip().strip("\"'")
            if name:
                return name
    return None


def resolve_structure(args: argparse.Namespace) -> tuple[list[str], list[str], str]:
    """Decide stages + disciplines.

    Precedence: explicit --stages/--disciplines > --profile > ~/.uxkit > fallback.
    Explicit flags override only the axis they name, so `--stages a b --profile personal`
    keeps that profile's disciplines.
    """
    name = args.profile or read_configured_profile()
    source = f"profile '{name}'" if name else None

    if name:
        profile = load_profile(name)
    elif FALLBACK_PROFILE in available_profiles():
        profile = load_profile(FALLBACK_PROFILE)
        source = f"default profile '{FALLBACK_PROFILE}'"
    else:
        profile = BUILTIN_PROFILE
        source = "built-in defaults"

    stages = args.stages if args.stages is not None else profile["stages"]
    disciplines = args.disciplines if args.disciplines is not None else profile["disciplines"]

    if args.stages is not None and args.disciplines is not None:
        source = "command line"
    elif args.stages is not None or args.disciplines is not None:
        source = f"{source} + command line"

    return list(stages), list(disciplines), source


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
    subfolders: Optional[dict[str, list[str]]] = None,
) -> None:
    """Create each discipline folder and its subfolders under `parent`."""
    subfolders = DISCIPLINE_SUBFOLDERS if subfolders is None else subfolders
    for key, (folder_name, _) in disciplines.items():
        disc_path = parent / folder_name
        make_dir(disc_path, dry_run)
        subs = subfolders.get(key, [])
        if not subs:
            make_gitkeep(disc_path, dry_run)
        for sub in subs:
            sub_path = disc_path / sub
            make_dir(sub_path, dry_run)
            # Cache folders get a self-ignoring .gitignore; everything else a .gitkeep.
            if is_cache(sub_path.name):
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


def scaffold_video_project(
    base_dir: Path,
    project_name: str,
    dry_run: bool,
    force: bool,
) -> None:
    root = base_dir / project_name
    make_dir(root, dry_run)

    build_discipline_tree(root, VIDEO_FOLDERS, dry_run, subfolders=VIDEO_SUBFOLDERS)

    folder_list = "\n".join(f"  - `{v[0]}/` — {v[1]}" for v in VIDEO_FOLDERS.values())
    content = VIDEO_README_TEMPLATE.format(
        project_name=project_name,
        date=datetime.date.today().isoformat(),
        folder_list=folder_list,
    )
    write_guarded_file(root / "README.md", content, dry_run, force)
    write_guarded_file(root / ".gitignore", GITIGNORE_PROJECT + GITIGNORE_VIDEO, dry_run, force)

    print(f"\n{'[dry-run] ' if dry_run else ''}Video project '{project_name}' scaffolded at {root}")
    print(f"  Pipeline: {', '.join(v[0] for v in VIDEO_FOLDERS.values())}")


def scaffold_video_workspace(base_dir: Path, dry_run: bool) -> None:
    """Create the shared _assets/ and _templates/ folders next to the video projects."""
    for meta, subs in VIDEO_WORKSPACE.items():
        make_dir(base_dir / meta, dry_run)
        for sub in subs:
            sub_path = base_dir / meta / sub
            make_dir(sub_path, dry_run)
            make_gitkeep(sub_path, dry_run)

    print(f"\n{'[dry-run] ' if dry_run else ''}Shared video workspace created in {base_dir}")
    print(f"  {', '.join(VIDEO_WORKSPACE)}")


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
        "--type",
        choices=("ux", "video"),
        default="ux",
        help="Project type: 'ux' (stage -> discipline, shaped by the profile) or "
             "'video' (fixed pipeline 01_docs ... 07_exports; ignores profiles)",
    )
    parser.add_argument(
        "--profile",
        metavar="NAME",
        help="Structure profile to use (default: the machine default in ~/.uxkit, "
             f"else '{FALLBACK_PROFILE}'). See --list-profiles.",
    )
    parser.add_argument(
        "--stages",
        nargs="+",
        default=None,
        metavar="STAGE",
        help="Stage folders to create (overrides the profile's stages)",
    )
    parser.add_argument(
        "--disciplines",
        nargs="+",
        default=None,
        metavar="DISC",
        help="Disciplines to include (overrides the profile's disciplines). "
             "See --list-disciplines.",
    )
    parser.add_argument(
        "--list-disciplines",
        action="store_true",
        help="Print available discipline keys and exit",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="Print available profiles and the structure each produces, then exit",
    )
    parser.add_argument(
        "--init-global",
        action="store_true",
        help="Also create the shared workspace alongside the project "
             "(_global_workspace/ for ux; _assets/ and _templates/ for video)",
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

    if args.list_disciplines and args.type == "video":
        print("Video pipeline (always created in full):")
        for key, (folder_name, desc) in VIDEO_FOLDERS.items():
            subs = " · ".join(VIDEO_SUBFOLDERS[key]) or "-"
            print(f"  {folder_name:<12} {desc}")
            print(f"  {'':<12} {subs}")
        sys.exit(0)

    if args.list_disciplines:
        print("Available disciplines:")
        for key, (folder_name, desc) in DISCIPLINES.items():
            print(f"  {key:<14} -> {folder_name:<22} {desc}")
        sys.exit(0)

    if args.list_profiles:
        names = available_profiles()
        if not names:
            print(f"No profiles found in {PROFILE_DIR} — using built-in defaults.")
            sys.exit(0)
        configured = read_configured_profile()
        print(f"Available profiles ({PROFILE_DIR}):\n")
        for name in names:
            profile = load_profile(name)
            marker = "  <- machine default (~/.uxkit)" if name == configured else ""
            print(f"  {name}{marker}")
            if profile.get("description"):
                print(f"      {profile['description']}")
            print(f"      stages:      {', '.join(profile['stages'])}")
            print(f"      disciplines: {', '.join(profile['disciplines'])}\n")
        if not configured:
            print(f"No machine default set — falling back to '{FALLBACK_PROFILE}'.")
            print(f"Set one with:  echo 'profile = personal' > {CONFIG_PATH}")
        sys.exit(0)

    if not args.project_name:
        print("[error] project_name is required unless using "
              "--list-disciplines or --list-profiles")
        sys.exit(1)

    if args.type == "video":
        if args.profile or args.stages is not None or args.disciplines is not None:
            print("[error] --profile, --stages and --disciplines don't apply to --type video;")
            print("        video projects always get the full 01_docs ... 07_exports pipeline.")
            sys.exit(1)
        validate_name(args.project_name)
        base_dir = Path(args.base_dir).expanduser().resolve()
        print("Structure from: video pipeline")
        if args.init_global:
            scaffold_video_workspace(base_dir, args.dry_run)
        scaffold_video_project(base_dir, args.project_name, args.dry_run, args.force)
        if not args.dry_run:
            print("\nDone. Open README.md inside the project to fill in the brief.")
        return

    raw_stages, raw_disciplines, source = resolve_structure(args)

    validate_name(args.project_name)
    for stage in raw_stages:
        validate_name(stage, label="stage name")

    # Drop duplicate stages while preserving the order they were given.
    stages = list(dict.fromkeys(raw_stages))

    base_dir     = Path(args.base_dir).expanduser().resolve()
    disciplines  = resolve_disciplines(list(dict.fromkeys(raw_disciplines)))

    print(f"Structure from: {source}")

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
