# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py==4.*", "pyyaml==6.*"]
# ///
"""Check local document targets, sequential names, and plan closure under docs/."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token

MARKDOWN = MarkdownIt().enable(["table", "strikethrough"])
NUMBERED = re.compile(r"^(\d{4})__(?:(\d{4}-\d{2}-\d{2})__|research(?:__|\.md$))")


def read_document(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = re.search(r"^---[ \t]*$", text[4:], re.MULTILINE)
    if end is None:
        raise ValueError("frontmatter has no closing delimiter")
    metadata = yaml.safe_load(text[4 : 4 + end.start()])
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise TypeError("frontmatter must be a mapping")
    for field in ("plan", "chronicle", "superseded_by"):
        if field in metadata and not isinstance(metadata[field], str):
            raise ValueError(f"{field} must be a document ID string")
    if "supersedes" in metadata and (
        not isinstance(metadata["supersedes"], list)
        or not all(isinstance(item, str) for item in metadata["supersedes"])
    ):
        raise ValueError("supersedes must be a list of document ID strings")
    if "archived" in metadata and not isinstance(metadata["archived"], bool):
        raise ValueError("archived must be true or false")
    return metadata, text[4 + end.end() :].lstrip("\n")


def legacy_name(path: Path, cutoff: date | None) -> bool:
    match = NUMBERED.match(path.name)
    if not match or cutoff is None:
        return False
    if match[2] is None:
        return True
    try:
        return date.fromisoformat(match[2]) < cutoff
    except ValueError:
        return False


def walk_tokens(tokens: list[Token]) -> Iterator[Token]:
    for token in tokens:
        yield token
        if token.children:
            yield from walk_tokens(token.children)


def local_links(tokens: list[Token]) -> Iterator[str]:
    for token in walk_tokens(tokens):
        if token.type in ("link_open", "image"):
            target = token.attrGet("href" if token.type == "link_open" else "src")
            if target:
                yield target


def missing_targets(root: Path, path: Path, metadata: dict, tokens: list[Token]) -> Iterator[str]:
    for target in local_links(tokens):
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
            continue
        if not (path.parent / unquote(url.path)).exists():
            yield f"link target {target!r} is missing; repair the link or restore its target"
    for field in ("plan", "chronicle", "superseded_by", "supersedes"):
        values = metadata.get(field, [])
        values = [values] if isinstance(values, str) else values
        for target in values:
            identifier = target if target.endswith(".md") else f"{target}.md"
            if not (root / identifier).is_file():
                yield f"{field} target {target!r} is missing; use its current repository-relative document ID"


def open_tasks(tokens: list[Token]) -> int:
    list_depth = 0
    count = 0
    for token in tokens:
        if token.type == "list_item_open":
            list_depth += 1
        elif token.type == "list_item_close":
            list_depth -= 1
        elif list_depth and token.type == "inline" and re.match(r"^\[ \](?:\s|$)", token.content):
            count += 1
    return count


def document_issues(
    root: Path, path: Path, metadata: dict, tokens: list[Token], cutoff: date | None
) -> Iterator[tuple[str, str]]:
    relative = path.relative_to(root)
    archived = "archive" in relative.parts
    active = (
        not archived
        and not metadata.get("archived", False)
        and metadata.get("status") not in ("superseded", "obsolete")
    )
    if active:
        for issue in missing_targets(root, path, metadata, tokens):
            yield "ERROR", issue
    collection = relative.parts[1] if len(relative.parts) > 2 else ""
    if collection not in ("plans", "chronicles"):
        return
    legacy = legacy_name(path, cutoff)
    if re.match(r"^\d{4}__", path.name) and not legacy:
        yield (
            "ERROR",
            "sequential prefix is not allowed; use YYYY-MM-DD__<slug>.md or the documented legacy cutoff",
        )
    is_plan = collection == "plans" and metadata.get("type", "plan") == "plan"
    if not is_plan:
        return
    if metadata.get("work_status") == "completed" and not archived:
        yield (
            "ERROR",
            "completed plan is outside archive/; close its items and archive it with repaired links",
        )
    if archived and (count := open_tasks(tokens)):
        yield (
            ("WARNING" if legacy else "ERROR"),
            f"archived plan has {count} open task items; verify completion or record dropped work with its reason",
        )


def citation_text(tokens: list[Token]) -> str:
    text = []
    link_depth = 0
    for token in walk_tokens(tokens):
        if token.type == "link_open":
            link_depth += 1
        elif token.type == "link_close":
            link_depth -= 1
        elif not link_depth and token.type in ("text", "code_inline"):
            text.append(token.content)
    return " ".join(text)


def check_documents(root: Path, cutoff: date | None) -> list[tuple[str, str]]:
    issues = []
    numbers = defaultdict(list)
    active_text = {}
    for path in sorted((root / "docs").rglob("*.md")):
        relative = path.relative_to(root)
        try:
            metadata, body = read_document(path)
        except (OSError, TypeError, UnicodeError, ValueError, yaml.YAMLError) as error:
            issues.append(
                (
                    "ERROR",
                    f"{relative}: invalid document: {error}; repair its frontmatter or encoding",
                )
            )
            continue
        tokens = MARKDOWN.parse(body)
        issues.extend(
            (level, f"{relative}: {message}")
            for level, message in document_issues(root, path, metadata, tokens, cutoff)
        )
        if (
            len(relative.parts) > 2
            and relative.parts[1] in ("plans", "chronicles")
            and (match := NUMBERED.match(path.name))
        ):
            numbers[(relative.parts[1], match[1])].append(str(relative))
        if "archive" not in relative.parts and metadata.get("status") not in (
            "superseded",
            "obsolete",
        ):
            active_text[str(relative)] = citation_text(tokens)
    duplicates = {number for (_, number), paths in numbers.items() if len(paths) > 1}
    for (collection, number), paths in sorted(numbers.items()):
        if len(paths) > 1:
            issues.append(
                (
                    "WARNING",
                    f"docs/{collection}: duplicate prefix {number}: {', '.join(paths)}; cite full paths",
                )
            )
    for path, text in active_text.items():
        cited = set(re.findall(r"(?<![\w-])0\d{3}(?![\w-])", text)) & duplicates
        for number in sorted(cited):
            issues.append(
                ("WARNING", f"{path}: ambiguous citation {number}; use the full document path")
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Repository root to check.")
    parser.add_argument(
        "--legacy-before",
        type=date.fromisoformat,
        help="Accept numbered filenames dated before this date and undated numbered research; warn on archived open work.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root {root} does not exist; supply an existing directory")
    issues = check_documents(root, args.legacy_before)
    for level, message in issues:
        print(f"{level}: {message}.")
    errors = sum(level == "ERROR" for level, _ in issues)
    print(f"Document check: {errors} errors, {len(issues) - errors} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
