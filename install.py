#!/usr/bin/env python3
"""
install.py — wire this checkout into Claude Code on the current machine.

Three things, all idempotent:

  1. Imports claude/CLAUDE.snippet.md into ~/.claude/CLAUDE.md, so the file naming
     conventions are in context for every session on this machine.
  2. Links each skill in claude/skills/ (project-organization, spec-driven) into
     ~/.claude/skills/, so their guidance loads on demand.
  3. Writes the machine's default structure profile to ~/.uxkit.

Usage:
    python install.py                        # inspect first — this is a dry run
    python install.py --apply                # actually make the changes
    python install.py --apply --profile personal
    python install.py --apply --copy         # copy the skill instead of symlinking
    python install.py --uninstall --apply

Re-run after `git pull` only if the skill was copied rather than symlinked (the
script tells you which happened).
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SNIPPET = REPO / "claude" / "CLAUDE.snippet.md"
SKILLS_SRC = REPO / "claude" / "skills"

CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
SKILLS_DST = CLAUDE_DIR / "skills"
CONFIG = Path.home() / ".uxkit"

# The managed block is delimited so re-running can replace it in place instead of
# appending a second copy, and --uninstall can remove exactly what was added.
MARK_START = "<!-- ux-toolkit:start — managed by install.py, edits will be overwritten -->"
MARK_END = "<!-- ux-toolkit:end -->"

# Dropped inside a copied skill directory so a later run can tell "a copy we made,
# safe to refresh" from "a directory the user wrote by hand, never touch it".
COPY_MARKER = ".installed-by-ux-toolkit"

CONFIG_TEMPLATE = """\
# ux-toolkit machine config.
# Which structure profile new_project.py uses when none is passed explicitly.
# See: python new_project.py --list-profiles
profile = {profile}
"""


class Reporter:
    """Prints planned vs. performed actions, and tracks whether anything failed."""

    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.failed = False

    def act(self, message: str) -> None:
        print(f"  {'[done]' if self.apply else '[plan]'} {message}")

    def skip(self, message: str) -> None:
        print(f"  [ok]   {message}")

    def warn(self, message: str) -> None:
        print(f"  [warn] {message}")

    def error(self, message: str) -> None:
        print(f"  [error] {message}")
        self.failed = True


# ── ~/.claude/CLAUDE.md ────────────────────────────────────────────────────────

def import_line() -> str:
    """`@`-import path for the snippet, home-relative when possible.

    Written with forward slashes: Claude Code accepts them on Windows too, and it
    keeps the line identical in shape to the one on the Macs.
    """
    try:
        rel = SNIPPET.relative_to(Path.home())
    except ValueError:
        return "@" + SNIPPET.as_posix()
    return "@~/" + rel.as_posix()


def managed_block() -> str:
    return f"{MARK_START}\n{import_line()}\n{MARK_END}\n"


def strip_block(text: str) -> str:
    """Remove an existing managed block, returning the rest of the file."""
    if MARK_START not in text:
        return text
    head, _, tail = text.partition(MARK_START)
    _, _, after = tail.partition(MARK_END)
    return head.rstrip("\n") + ("\n" + after.lstrip("\n") if after.strip() else "\n")


def install_claude_md(rep: Reporter) -> None:
    print(f"\n~/.claude/CLAUDE.md  ->  imports {import_line()}")

    if not SNIPPET.is_file():
        rep.error(f"snippet not found at {SNIPPET} — is this a complete checkout?")
        return

    existing = CLAUDE_MD.read_text(encoding="utf-8") if CLAUDE_MD.is_file() else ""

    if managed_block().strip() in existing:
        rep.skip("import already present and current")
        return

    if MARK_START in existing:
        rep.act("updating the existing ux-toolkit block (repo path changed)")
    elif existing:
        rep.act("appending the ux-toolkit block (existing content left untouched)")
    else:
        rep.act("creating CLAUDE.md with the ux-toolkit block")

    body = strip_block(existing)
    if body and not body.endswith("\n"):
        body += "\n"
    new_text = (body + "\n" if body else "") + managed_block()

    if rep.apply:
        CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
        CLAUDE_MD.write_text(new_text, encoding="utf-8")


def uninstall_claude_md(rep: Reporter) -> None:
    print("\n~/.claude/CLAUDE.md")
    if not CLAUDE_MD.is_file():
        rep.skip("no CLAUDE.md — nothing to remove")
        return
    text = CLAUDE_MD.read_text(encoding="utf-8")
    if MARK_START not in text:
        rep.skip("no ux-toolkit block — nothing to remove")
        return
    rep.act("removing the ux-toolkit block (rest of the file preserved)")
    if rep.apply:
        CLAUDE_MD.write_text(strip_block(text), encoding="utf-8")


# ── ~/.claude/skills/<skill> ───────────────────────────────────────────────────

def skill_names() -> list[str]:
    """Every skill shipped in claude/skills/, i.e. each folder holding a SKILL.md."""
    if not SKILLS_SRC.is_dir():
        return []
    return sorted(p.parent.name for p in SKILLS_SRC.glob("*/SKILL.md"))


def is_our_copy(path: Path) -> bool:
    return (path / COPY_MARKER).is_file()


def install_skill(rep: Reporter, name: str, copy: bool, force: bool) -> None:
    src = SKILLS_SRC / name
    dst = SKILLS_DST / name
    print(f"\n~/.claude/skills/{name}  ->  {src}")

    refreshing_copy = False

    if dst.is_symlink():
        current = dst.resolve()
        if current == src and not copy:
            rep.skip("already symlinked here")
            return
        rep.act(f"replacing existing symlink (currently -> {current})")
        if rep.apply:
            dst.unlink()
    elif dst.exists():
        if is_our_copy(dst):
            # Our own copy from a previous run: replacing it wholesale is how a
            # `git pull` gets picked up, and it drops files deleted upstream.
            refreshing_copy = True
            rep.act("refreshing the copied skill directory")
            if rep.apply:
                shutil.rmtree(dst)
        elif not force:
            # Never silently delete a directory the user may have hand-written.
            rep.error(
                f"{dst} exists, is not a symlink, and wasn't created by this "
                "script. Move it aside, or re-run with --force to replace it."
            )
            return
        else:
            rep.act("removing the existing directory (--force)")
            if rep.apply:
                shutil.rmtree(dst)

    if rep.apply:
        dst.parent.mkdir(parents=True, exist_ok=True)

    # A previous run already proved symlinks don't work here — don't re-fail noisily.
    if not copy and not refreshing_copy:
        rep.act("creating symlink (tracks git pull automatically)")
        if not rep.apply:
            return
        try:
            dst.symlink_to(src, target_is_directory=True)
            return
        except OSError as exc:
            # Windows needs Developer Mode or an elevated shell for symlinks.
            rep.warn(f"symlink failed ({exc}); falling back to a copy")

    if not refreshing_copy:
        rep.act("copying the skill directory — re-run install.py after each git pull")
    if rep.apply:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        (dst / COPY_MARKER).write_text(
            f"Copied from {src} by install.py. Re-run it after `git pull`.\n",
            encoding="utf-8",
        )


def uninstall_skill(rep: Reporter, name: str, force: bool) -> None:
    dst = SKILLS_DST / name
    print(f"\n~/.claude/skills/{name}")
    if dst.is_symlink():
        rep.act("removing symlink")
        if rep.apply:
            dst.unlink()
    elif dst.is_dir():
        ours = is_our_copy(dst)
        if not ours and not force:
            rep.error(
                "a directory is there that this script didn't create; "
                "re-run with --force to delete it"
            )
            return
        rep.act("deleting the copied skill directory" if ours
                else "deleting the directory that was in its place (--force)")
        if rep.apply:
            shutil.rmtree(dst)
    else:
        rep.skip("not installed — nothing to remove")


# ── ~/.uxkit ───────────────────────────────────────────────────────────────────

def set_profile(rep: Reporter, profile: str, explicit: bool) -> None:
    print(f"\n~/.uxkit  ->  profile = {profile}")

    if not (REPO / "profiles" / f"{profile}.json").is_file():
        rep.error(
            f"no such profile '{profile}' in {REPO / 'profiles'} — "
            "run `python new_project.py --list-profiles`"
        )
        return

    if not CONFIG.is_file():
        rep.act(f"creating {CONFIG}")
        if rep.apply:
            CONFIG.write_text(CONFIG_TEMPLATE.format(profile=profile), encoding="utf-8")
        return

    lines = CONFIG.read_text(encoding="utf-8").splitlines(keepends=True)
    current = None
    index = None
    for i, raw in enumerate(lines):
        key, sep, value = raw.split("#", 1)[0].partition("=")
        if sep and key.strip() == "profile":
            current = value.strip().strip("\"'")
            index = i
            break

    if current == profile:
        rep.skip("already set")
        return
    if current and not explicit:
        # Don't quietly change a deliberate choice during a plain re-install.
        rep.skip(f"leaving existing profile '{current}' alone (pass --profile to change)")
        return

    if index is None:
        rep.act(f"appending `profile = {profile}`")
        if rep.apply:
            with CONFIG.open("a", encoding="utf-8") as handle:
                if lines and not lines[-1].endswith("\n"):
                    handle.write("\n")
                handle.write(f"profile = {profile}\n")
        return

    rep.act(f"changing profile '{current}' -> '{profile}'")
    if rep.apply:
        lines[index] = f"profile = {profile}\n"
        CONFIG.write_text("".join(lines), encoding="utf-8")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install this ux-toolkit checkout into Claude Code on this machine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Make the changes. Without it, the script only prints what it would do.",
    )
    parser.add_argument(
        "--profile",
        default=None,
        metavar="NAME",
        help="Default structure profile for this machine (default: work)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the skill instead of symlinking it (needs a re-run after git pull)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing non-symlinked skill directory",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove the CLAUDE.md block and the skill links (~/.uxkit is left alone)",
    )
    args = parser.parse_args()

    rep = Reporter(args.apply)
    mode = "Uninstalling" if args.uninstall else "Installing"
    print(f"{mode} ux-toolkit from {REPO}")
    if not args.apply:
        print("Dry run — nothing will be written. Re-run with --apply to commit.")

    skills = skill_names()
    if not skills:
        rep.error(f"no skills found in {SKILLS_SRC} — is this a complete checkout?")

    if args.uninstall:
        uninstall_claude_md(rep)
        for name in skills:
            uninstall_skill(rep, name, args.force)
        print(f"\nLeft {CONFIG} in place — delete it by hand if you want it gone.")
    else:
        install_claude_md(rep)
        for name in skills:
            install_skill(rep, name, args.copy, args.force)
        set_profile(rep, args.profile or "work", explicit=args.profile is not None)

    if rep.failed:
        print("\nFinished with errors — see [error] lines above.")
        sys.exit(1)
    if args.apply:
        print("\nDone. Restart Claude Code so it picks up the new CLAUDE.md and skill.")
    else:
        print("\nLooks right? Re-run with --apply.")


if __name__ == "__main__":
    main()
