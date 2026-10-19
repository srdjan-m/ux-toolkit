#!/usr/bin/env python3
"""
new_spec.py — scaffold a language-neutral spec from _templates/spec/

A spec describes *what* a program does — requirements, data, flows and concrete
input/output examples — without committing to a programming language. Claude Code
(with the spec-driven skill) then implements it in whichever language you ask for, and
checks every implementation against the same examples.

Usage:
    python new_spec.py ballot_parser                         # ./spec/
    python new_spec.py ballot_parser --dir tools/ballot/spec
    python new_spec.py ballot_parser --targets python typescript
    python new_spec.py ballot_parser --targets rust          # add a target later
    python new_spec.py ballot_parser --dry-run

Re-running is safe: existing files are never overwritten unless --force is passed, so
the same command adds new targets to a spec that already exists.
"""

import argparse
import datetime
import getpass
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
TEMPLATE_DIR = REPO / "_templates" / "spec"

# The per-language note is a template for targets/<lang>.md, not a file to copy as-is.
TARGET_TEMPLATE = Path("targets") / "_target.md"

NAME_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def validate_name(name: str, label: str) -> None:
    """Enforce snake_case naming; exit with a helpful message if invalid."""
    if not NAME_RE.match(name):
        print(f"[error] '{name}' is not a valid {label}.")
        print("        Use lowercase letters, digits and single underscores only")
        print("        (e.g. ballot_parser, typescript) - no spaces, capitals or symbols.")
        sys.exit(1)


def render(template: str, values: dict) -> str:
    """Fill {{placeholders}}. Unknown ones are left visible rather than blanked."""
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def write_guarded_file(path: Path, content: str, dry_run: bool, force: bool) -> bool:
    """Write a text file, but never clobber an existing one unless --force.

    Returns whether the file was (or, in a dry run, would be) written.
    """
    if path.exists() and not force:
        print(f"  [skip] {path} already exists — not overwritten (use --force)")
        return False
    if dry_run:
        print(f"  [dry] write {path}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  [new]  {path}")
    return True


def scaffold_spec(
    name: str, dest: Path, targets: list[str], author: str, dry_run: bool, force: bool
) -> None:
    if not TEMPLATE_DIR.is_dir():
        print(f"[error] template not found at {TEMPLATE_DIR} — is this a complete checkout?")
        sys.exit(1)

    values = {
        "name": name,
        "date": datetime.date.today().isoformat(),
        "author": author,
    }
    written = 0

    for source in sorted(TEMPLATE_DIR.rglob("*")):
        rel = source.relative_to(TEMPLATE_DIR)
        if source.is_dir() or rel == TARGET_TEMPLATE:
            continue
        text = render(source.read_text(encoding="utf-8"), values)
        written += write_guarded_file(dest / rel, text, dry_run, force)

    target_text = (TEMPLATE_DIR / TARGET_TEMPLATE).read_text(encoding="utf-8")
    for target in targets:
        text = render(target_text, {**values, "target": target})
        written += write_guarded_file(dest / "targets" / f"{target}.md", text, dry_run, force)

    # Keep targets/ in version control before the first language is chosen.
    if not targets and not (dest / "targets").exists():
        written += write_guarded_file(dest / "targets" / ".gitkeep", "", dry_run, force)

    verb = "would write" if dry_run else "wrote"
    print(f"\n{'[dry-run] ' if dry_run else ''}Spec '{name}' at {dest} — {verb} {written} file(s)")
    if targets:
        print(f"  Targets: {', '.join(targets)}")
    if not dry_run and written:
        print("  Next: ask Claude Code to \"interview me and fill in the spec\".")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a language-neutral spec that Claude Code can implement in any language.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("name", help="What is being specified, in snake_case (e.g. ballot_parser)")
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("spec"),
        metavar="PATH",
        help="Folder to create the spec in (default: ./spec)",
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        default=[],
        metavar="LANG",
        help="Languages to add a targets/<lang>.md note for (e.g. python typescript)",
    )
    parser.add_argument(
        "--author",
        default=getpass.getuser(),
        help="Author recorded in spec.md (default: the current OS user)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing spec files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without writing")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_name(args.name, "spec name")
    for target in args.targets:
        validate_name(target, "target language")
    scaffold_spec(
        args.name,
        args.dir.resolve(),
        list(dict.fromkeys(args.targets)),
        args.author,
        args.dry_run,
        args.force,
    )


if __name__ == "__main__":
    main()
