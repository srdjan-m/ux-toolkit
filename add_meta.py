#!/usr/bin/env python3
"""
add_meta.py — File metadata sidecars for the UI/UX project structure

Attaches a small `<file>.meta.md` sidecar (YAML front-matter + notes) next to any
asset, recording who requested it, why it was created, its status, and more. Works
for any file type — including binaries like .fig / .ai / .aep / .blend — and the
sidecar travels next to the asset through Creative Cloud sync and version control.

Usage:
    # Create or update a sidecar for a file
    python add_meta.py set path/to/login_screen_v03.fig \\
        --requested-by product_team \\
        --reason "Redesign login flow for accessibility audit AA-2026-07" \\
        --status approved --tags login accessibility

    # Show a file's metadata
    python add_meta.py show path/to/login_screen_v03.fig

    # Rebuild the project-wide INDEX.md + assets.csv from every sidecar in a tree
    python add_meta.py index path/to/project_root

    # Preview any command without touching disk
    python add_meta.py set my_file.png --reason "hero image" --dry-run
"""

import argparse
import csv
import datetime
import getpass
import sys
from pathlib import Path

SIDECAR_SUFFIX = ".meta.md"
STATUSES = ("wip", "review", "approved")

# Order in which front-matter keys are written (stable, diff-friendly output).
FIELD_ORDER = [
    "file", "created", "updated", "author",
    "requested_by", "reason", "status", "supersedes", "tags",
]


# ── Front-matter (de)serialization ──────────────────────────────────────────────
# A deliberately tiny YAML subset — flat `key: value` pairs plus an inline `tags`
# list — so the script stays dependency-free like new_project.py.

def _fmt_value(value: str) -> str:
    """Quote a scalar only when it could confuse the minimal parser."""
    s = str(value)
    if s == "":
        return '""'
    needs_quote = (
        s != s.strip()
        or any(c in s for c in ":#")
        or s[0] in "\"'[]{}"
    )
    if needs_quote:
        return '"' + s.replace('"', '\\"') + '"'
    return s


def _parse_value(raw: str) -> str:
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].replace('\\"', '"')
    return s


def _parse_tags(raw: str) -> list[str]:
    s = raw.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [t.strip() for t in s.split(",") if t.strip()]


def read_sidecar(path: Path) -> tuple[dict, str]:
    """Return (metadata dict, body text) parsed from a sidecar file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    meta: dict = {}
    if lines and lines[0].strip() == "---":
        body_start = len(lines)
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            if ":" in lines[i]:
                key, _, val = lines[i].partition(":")
                key = key.strip()
                if key == "tags":
                    meta[key] = _parse_tags(val)
                else:
                    meta[key] = _parse_value(val)
        body = "\n".join(lines[body_start:]).strip()
    else:
        body = "\n".join(lines).strip()
    return meta, body


def write_sidecar(path: Path, meta: dict, body: str, dry_run: bool) -> None:
    out = ["---"]
    for key in FIELD_ORDER:
        if key == "tags":
            tags = meta.get("tags") or []
            if tags:
                out.append(f"tags: [{', '.join(tags)}]")
        else:
            value = meta.get(key)
            if value:
                out.append(f"{key}: {_fmt_value(value)}")
    out.append("---")
    out.append("")
    out.append(body if body else "Notes:")
    out.append("")
    content = "\n".join(out)
    if dry_run:
        print(f"  [dry] write {path}")
    else:
        path.write_text(content, encoding="utf-8")


# ── Helpers ─────────────────────────────────────────────────────────────────────

def sidecar_for(asset: Path) -> Path:
    """Sidecar path for an asset (e.g. logo.ai -> logo.ai.meta.md)."""
    return asset.with_name(asset.name + SIDECAR_SUFFIX)


def asset_for(sidecar: Path) -> Path:
    return sidecar.with_name(sidecar.name[: -len(SIDECAR_SUFFIX)])


def validate_status(status: str) -> None:
    if status not in STATUSES:
        print(f"[error] Unknown status '{status}'.")
        print(f"        Valid options: {', '.join(STATUSES)}")
        sys.exit(1)


# ── Interactive prompts ─────────────────────────────────────────────────────────

def _prompt(label: str, current) -> str:
    """Ask for a value, showing the current one as the default. Enter keeps it."""
    shown = current if current else ""
    suffix = f" [{shown}]" if shown else ""
    try:
        answer = input(f"  {label}{suffix}: ").strip()
    except EOFError:
        answer = ""
    return answer or (current or "")


def _prompt_status(current) -> str:
    """Prompt for status, re-asking until it's valid or left blank."""
    while True:
        answer = _prompt(f"Status ({'/'.join(STATUSES)})", current)
        if not answer or answer in STATUSES:
            return answer
        print(f"    [!] '{answer}' is not valid — choose one of: {', '.join(STATUSES)}")


def _prompt_tags(current) -> list[str]:
    default = ", ".join(current or [])
    answer = _prompt("Tags (comma- or space-separated)", default)
    return [t.strip() for t in answer.replace(",", " ").split() if t.strip()]


# ── Commands ────────────────────────────────────────────────────────────────────

def cmd_set(args: argparse.Namespace) -> None:
    asset = Path(args.file)
    if asset.name.endswith(SIDECAR_SUFFIX):
        print(f"[error] '{asset}' is itself a sidecar — point at the asset instead.")
        sys.exit(1)
    if not asset.exists():
        print(f"[warn] '{asset}' does not exist yet — writing metadata anyway.")

    sidecar = sidecar_for(asset)
    existed = sidecar.exists()
    meta, body = read_sidecar(sidecar) if existed else ({}, "")

    today = datetime.date.today().isoformat()
    meta.setdefault("created", today)
    meta["updated"] = today
    meta["file"] = asset.name

    if args.author:
        meta["author"] = args.author
    else:
        meta.setdefault("author", getpass.getuser())
    if args.requested_by:
        meta["requested_by"] = args.requested_by
    if args.reason:
        meta["reason"] = args.reason
    if args.status:
        validate_status(args.status)
        meta["status"] = args.status
    if args.supersedes:
        meta["supersedes"] = args.supersedes
    if args.tags:
        meta["tags"] = args.tags
    if args.note is not None:
        body = args.note

    # Interactive pass: prompt for each field, offering the current value as default.
    if args.interactive:
        print(f"Editing metadata for {asset.name}  (Enter keeps the [current] value)\n")
        meta["requested_by"] = _prompt("Requested by", meta.get("requested_by"))
        meta["reason"]       = _prompt("Reason", meta.get("reason"))
        meta["author"]       = _prompt("Author", meta.get("author"))
        meta["status"]       = _prompt_status(meta.get("status"))
        meta["supersedes"]   = _prompt("Supersedes", meta.get("supersedes"))
        meta["tags"]         = _prompt_tags(meta.get("tags"))
        body                 = _prompt("Notes", body)
        # Drop keys the user cleared so they don't linger as empty entries.
        meta = {k: v for k, v in meta.items() if v not in (None, "", [])}

    write_sidecar(sidecar, meta, body, args.dry_run)
    verb = "Updated" if existed else "Created"
    print(f"{'[dry-run] ' if args.dry_run else ''}{verb} metadata -> {sidecar}")


def cmd_show(args: argparse.Namespace) -> None:
    asset = Path(args.file)
    sidecar = asset if asset.name.endswith(SIDECAR_SUFFIX) else sidecar_for(asset)
    if not sidecar.exists():
        print(f"[error] No metadata found for '{asset}' (expected {sidecar}).")
        sys.exit(1)
    print(sidecar.read_text(encoding="utf-8"))


def cmd_index(args: argparse.Namespace) -> None:
    root = Path(args.dir).expanduser().resolve()
    if not root.is_dir():
        print(f"[error] '{root}' is not a directory.")
        sys.exit(1)

    sidecars = sorted(root.rglob(f"*{SIDECAR_SUFFIX}"))
    rows = []
    for sc in sidecars:
        meta, body = read_sidecar(sc)
        rel = asset_for(sc).relative_to(root).as_posix()
        rows.append((rel, meta, body))

    today = datetime.date.today().isoformat()
    md_path = root / "INDEX.md"
    csv_path = root / "assets.csv"

    # ── INDEX.md ──
    md = [
        f"# Asset index — {root.name}",
        "",
        f"_Generated {today} · {len(rows)} file(s) with metadata_",
        "",
        "| File | Status | Requested by | Reason | Author | Updated |",
        "|------|--------|--------------|--------|--------|---------|",
    ]

    def cell(text: str) -> str:
        return str(text or "").replace("|", "\\|").replace("\n", " ")

    for rel, meta, _ in rows:
        md.append(
            f"| `{rel}` | {cell(meta.get('status'))} | {cell(meta.get('requested_by'))} "
            f"| {cell(meta.get('reason'))} | {cell(meta.get('author'))} "
            f"| {cell(meta.get('updated'))} |"
        )
    md.append("")

    # ── assets.csv ──
    columns = [
        "path", "file", "status", "requested_by", "reason",
        "author", "created", "updated", "supersedes", "tags",
    ]

    if args.dry_run:
        print(f"  [dry] write {md_path}")
        print(f"  [dry] write {csv_path}")
    else:
        md_path.write_text("\n".join(md), encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(columns)
            for rel, meta, _ in rows:
                writer.writerow([
                    rel,
                    meta.get("file", ""),
                    meta.get("status", ""),
                    meta.get("requested_by", ""),
                    meta.get("reason", ""),
                    meta.get("author", ""),
                    meta.get("created", ""),
                    meta.get("updated", ""),
                    meta.get("supersedes", ""),
                    ", ".join(meta.get("tags", []) or []),
                ])

    print(f"\n{'[dry-run] ' if args.dry_run else ''}Indexed {len(rows)} file(s) under {root}")
    print(f"  {md_path}")
    print(f"  {csv_path}")


# ── CLI ─────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Attach and aggregate file metadata sidecars.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_set = sub.add_parser("set", help="Create or update a file's metadata sidecar")
    p_set.add_argument("file", help="The asset to describe")
    p_set.add_argument("--requested-by", dest="requested_by", help="Who asked for this file")
    p_set.add_argument("--reason", help="Why this file was created")
    p_set.add_argument("--author", help="Who made it (default: current OS user)")
    p_set.add_argument("--status", help=f"One of: {', '.join(STATUSES)}")
    p_set.add_argument("--supersedes", help="Filename this version replaces")
    p_set.add_argument("--tags", nargs="+", metavar="TAG", help="Free-form tags")
    p_set.add_argument("--note", help="Free-text note (replaces the sidecar body)")
    p_set.add_argument(
        "-i", "--interactive", action="store_true",
        help="Prompt for each field (any flags above pre-fill the defaults)",
    )
    p_set.add_argument("--dry-run", action="store_true", help="Print without writing")
    p_set.set_defaults(func=cmd_set)

    p_show = sub.add_parser("show", help="Print a file's metadata sidecar")
    p_show.add_argument("file", help="The asset (or its .meta.md sidecar)")
    p_show.set_defaults(func=cmd_show)

    p_index = sub.add_parser("index", help="Rebuild INDEX.md + assets.csv from all sidecars")
    p_index.add_argument("dir", help="Project root to scan recursively")
    p_index.add_argument("--dry-run", action="store_true", help="Print without writing")
    p_index.set_defaults(func=cmd_index)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
