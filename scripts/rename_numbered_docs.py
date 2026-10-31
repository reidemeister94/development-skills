# /// script
# requires-python = ">=3.11"
# ///
"""Rename numbered plans, chronicles, and research to YYYY-MM-DD__<slug> names and repair references."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from pathlib import Path

COLLECTIONS = ("plans", "chronicles")
NUMBERED = re.compile(r"^(\d{4})__(.+)$")
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})__(?:implementation_plan__)?(.+)$")
RESEARCH = re.compile(r"^research(?:__(.+))?$")
CITATION = re.compile(
    r"(?<![\w-])(chronicles?|plans?|research)(?:\s+#?|/)(\d{4})(?![\w-])", re.IGNORECASE
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout


def split_suffix(name: str) -> tuple[str, str]:
    return (name[:-3], ".md") if name.endswith(".md") else (name, "")


def repository_files(root: Path, *options: str) -> list[str]:
    return [name for name in git(root, "ls-files", "-z", *options).split("\0") if name]


def find_records(root: Path) -> tuple[list[Path], list[Path], list[str], list[str]]:
    """Sort numbered paths under docs/ into records, nested paths, problems, and other documents."""
    tracked = {Path(name) for name in repository_files(root)}
    tracked |= {parent for name in tracked for parent in name.parents}
    records, nested, problems, outside = [], [], [], []
    for path in sorted((root / "docs").rglob("*")):
        relative = path.relative_to(root)
        if not NUMBERED.match(path.name):
            continue
        if any(NUMBERED.match(parent.name) for parent in relative.parents):
            nested.append(path)
        elif len(relative.parts) < 3 or relative.parts[1] not in COLLECTIONS:
            outside.append(
                f"OUTSIDE {relative}: not under docs/plans or docs/chronicles; move it there "
                "if it is a plan, chronicle, or research record, otherwise leave it"
            )
        elif relative not in tracked:
            problems.append(
                f"UNRESOLVED {relative}: not tracked by Git; add it or rename it by hand"
            )
        else:
            records.append(path)
    return records, nested, problems, outside


def plan_dates(records: list[Path], root: Path) -> dict[str, list[tuple[str, str]]]:
    """Map each plan number to the dates and slugs of its plans, so undated research can borrow them."""
    plans: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for path in records:
        if path.relative_to(root).parts[1] != "plans":
            continue
        number, rest = NUMBERED.match(split_suffix(path.name)[0]).groups()
        if (dated := DATED.match(rest)) and not dated[2].startswith("research"):
            plans[number].append((dated[1], dated[2]))
    return plans


def oldest_commit_date(root: Path, path: Path) -> str | None:
    dates = git(root, "log", "--follow", "--format=%as", "--", str(path)).split()
    return dates[-1] if dates else None


def new_name(root: Path, path: Path, plans: dict[str, list[tuple[str, str]]]) -> str | None:
    stem, suffix = split_suffix(path.name)
    number, rest = NUMBERED.match(stem).groups()
    if dated := DATED.match(rest):
        return f"{dated[1]}__{dated[2]}{suffix}"
    research = RESEARCH.match(rest)
    candidates = plans.get(number, []) if research else []
    same_slug = [plan for plan in candidates if plan[1] == research[1]] if research else []
    plan = same_slug[0] if same_slug else candidates[0] if len(candidates) == 1 else None
    date = plan[0] if plan else oldest_commit_date(root, path)
    if research:
        slug = research[1] or (plan[1] if plan else None)
        rest = f"research__{slug}" if slug else None
    return f"{date}__{rest}{suffix}" if date and rest else None


def plan_renames(root: Path) -> tuple[dict[Path, Path], list[str], list[str]]:
    records, nested, problems, outside = find_records(root)
    plans = plan_dates(records, root)
    targets: dict[Path, list[Path]] = defaultdict(list)
    for path in records:
        if name := new_name(root, path, plans):
            targets[path.with_name(name)].append(path)
        else:
            problems.append(
                f"UNRESOLVED {path.relative_to(root)}: no date or slug; rename it by hand"
            )
    renames = {}
    for target, sources in sorted(targets.items()):
        if len(sources) > 1 or target.exists():
            names = ", ".join(str(source.relative_to(root)) for source in sources)
            problems.append(
                f"CONFLICT {names} -> {target.relative_to(root)}: give each record a distinct slug"
            )
        else:
            renames[sources[0]] = target
    for path in nested:
        parent = next((parent for parent in path.parents if parent in renames), None)
        after = (
            f"; after the move it is {(renames[parent] / path.relative_to(parent)).relative_to(root)}"
            if parent
            else ""
        )
        problems.append(
            f"UNRESOLVED {path.relative_to(root)}: inside a numbered directory"
            f"{after}; rename it by hand"
        )
    return renames, problems, outside


def text_files(root: Path) -> list[Path]:
    return [
        root / name for name in repository_files(root, "--cached", "--others", "--exclude-standard")
    ]


def repair_references(root: Path, renames: dict[Path, Path], write: bool) -> list[str]:
    """Replace each full old name; return every changed file with its line numbers."""
    stems = {split_suffix(old.name)[0]: split_suffix(new.name)[0] for old, new in renames.items()}
    if not stems:
        return []
    pattern = re.compile(
        r"(?<![\w-])("
        + "|".join(map(re.escape, sorted(stems, key=len, reverse=True)))
        + r")(?![\w-])"
    )
    changes = []
    for path in text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except OSError, UnicodeError:
            continue
        updated = [pattern.sub(lambda match: stems[match[1]], line) for line in lines]
        changed = [
            str(number) for number, pair in enumerate(zip(lines, updated), 1) if pair[0] != pair[1]
        ]
        if changed:
            changes.append(f"{path.relative_to(root)}: lines {', '.join(changed)}")
            if write:
                path.write_text("".join(updated), encoding="utf-8")
    return changes


def citations(root: Path, renames: dict[Path, Path]) -> list[str]:
    """List bare number citations; only a reader can tell which repository they name."""
    by_number: dict[tuple[str, str], list[str]] = defaultdict(list)
    for old, new in renames.items():
        collection = old.relative_to(root).parts[1]
        by_number[(collection, NUMBERED.match(old.name)[1])].append(str(new.relative_to(root)))
    found = []
    for path in text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError, UnicodeError:
            continue
        for line_number, line in enumerate(lines, 1):
            for match in CITATION.finditer(line):
                collection = "chronicles" if match[1].lower().startswith("chronicle") else "plans"
                candidates = by_number.get((collection, match[2])) or ["no record here"]
                found.append(
                    f"CITATION {path.relative_to(root)}:{line_number}: {match[0]!r} -> "
                    + ", ".join(candidates)
                )
    return found


def move(root: Path, renames: dict[Path, Path], problems: list[str]) -> dict[Path, Path]:
    """Move each record with git mv; a failed move stays numbered and its references stay unchanged."""
    moved = {}
    for old, new in renames.items():
        try:
            git(root, "mv", str(old), str(new))
        except subprocess.CalledProcessError as error:
            problems.append(
                f"UNRESOLVED {old.relative_to(root)}: git mv failed: {error.stderr.strip()}"
            )
        else:
            moved[old] = new
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Exit 1 means some records still need a person; --apply has moved all the others.",
    )
    parser.add_argument("root", type=Path, help="Repository root.")
    parser.add_argument(
        "--apply", action="store_true", help="Move the records, then repair references."
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / ".git").exists():
        parser.error(f"{root} is not the root of a Git repository; supply the repository root")
    renames, problems, outside = plan_renames(root)
    for old, new in renames.items():
        print(f"RENAME {old.relative_to(root)} -> {new.relative_to(root)}")
    if args.apply:
        renames = move(root, renames, problems)
    label = "REPAIRED" if args.apply else "REFERENCE"
    for change in repair_references(root, renames, write=args.apply):
        print(f"{label} {change}")
    remaining = citations(root, renames)
    for line in problems + outside + remaining:
        print(line)
    print(
        f"Numbered records: {len(renames)} {'moved' if args.apply else 'to rename'}, "
        f"{len(problems)} to fix by hand, {len(outside)} other numbered documents, "
        f"{len(remaining)} number citations to check."
    )
    unresolved_citations = any(not line.endswith(" -> no record here") for line in remaining)
    return 1 if problems or (args.apply and unresolved_citations) else 0


if __name__ == "__main__":
    raise SystemExit(main())
