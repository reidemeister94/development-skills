#!/usr/bin/env python3
"""
Documentation structure validator.

Validates that the generated documentation follows the expected
folder structure and file naming conventions.

Usage:
    python validate_structure.py <docs_dir>
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List


def validate_folder_structure(docs_dir: str) -> List[str]:
    """Validate expected folder structure exists."""
    errors = []
    docs_path = Path(docs_dir)

    expected_dirs = [
        "data-model",
        "workflows",
        "workflows/etl",
        "workflows/api",
    ]

    expected_files = [
        "data-model/_overview.md",
        "workflows/etl/_pipeline-overview.md",
        "workflows/api/_endpoints-overview.md",
        "_index.md",
    ]

    for dir_name in expected_dirs:
        dir_path = docs_path / dir_name
        if not dir_path.exists():
            errors.append(f"Missing directory: {dir_name}/")
        elif not dir_path.is_dir():
            errors.append(f"Expected directory but found file: {dir_name}")

    for file_name in expected_files:
        file_path = docs_path / file_name
        if not file_path.exists():
            errors.append(f"Missing required file: {file_name}")

    return errors


def validate_entity_files(docs_dir: str) -> List[str]:
    """Validate entity documentation files."""
    errors = []
    entity_path = Path(docs_dir) / "data-model"

    if not entity_path.exists():
        return errors

    for md_file in entity_path.glob("*.md"):
        if md_file.name.startswith("_"):
            continue

        # Check filename is lowercase
        if md_file.name != md_file.name.lower():
            errors.append(f"Entity file should be lowercase: {md_file.name}")

        # Check required sections
        content = md_file.read_text(errors="ignore")
        required_sections = [
            ("## Definition", "Definition section"),
            ("## Role in Project", "Role in Project section"),
            ("## Attributes", "Attributes section"),
            ("## Relationships", "Relationships section"),
        ]

        for pattern, name in required_sections:
            if pattern not in content:
                errors.append(f"{md_file.name}: Missing {name}")

        # Check for attribute table
        if "| Attribute |" not in content and "|Attribute|" not in content:
            errors.append(f"{md_file.name}: Missing attributes table")

    return errors


def validate_etl_files(docs_dir: str) -> List[str]:
    """Validate ETL step documentation files."""
    errors = []
    etl_path = Path(docs_dir) / "workflows" / "etl"

    if not etl_path.exists():
        return errors

    step_pattern = re.compile(r"^step-(\d{2}[a-z]?)-[\w-]+\.md$")

    for md_file in etl_path.glob("*.md"):
        if md_file.name.startswith("_"):
            continue

        # Check filename format
        if not step_pattern.match(md_file.name):
            errors.append(f"ETL file naming: {md_file.name} should be step-NN-name.md")

        # Check required sections
        content = md_file.read_text(errors="ignore")
        required_sections = [
            ("## Purpose", "Purpose section"),
            ("## Input", "Input section"),
            ("## Processing Logic", "Processing Logic section"),
            ("## Output", "Output section"),
        ]

        for pattern, name in required_sections:
            if pattern not in content:
                errors.append(f"{md_file.name}: Missing {name}")

        # Check for code reference
        if not re.search(r"\w+\.py:\d+", content):
            errors.append(f"{md_file.name}: Missing code reference (file.py:line)")

    return errors


def validate_api_files(docs_dir: str) -> List[str]:
    """Validate API endpoint documentation files."""
    errors = []
    api_path = Path(docs_dir) / "workflows" / "api"

    if not api_path.exists():
        return errors

    method_pattern = re.compile(r"^(get|post|put|delete|patch)-[\w-]+\.md$")

    for md_file in api_path.glob("*.md"):
        if md_file.name.startswith("_"):
            continue

        # Check filename format
        if not method_pattern.match(md_file.name):
            errors.append(f"API file naming: {md_file.name} should be method-path-slug.md")

        # Check required sections
        content = md_file.read_text(errors="ignore")
        required_sections = [
            ("## Purpose", "Purpose section"),
            ("## Request", "Request section"),
            ("## Response", "Response section"),
            ("## Implementation", "Implementation section"),
        ]

        for pattern, name in required_sections:
            if pattern not in content:
                errors.append(f"{md_file.name}: Missing {name}")

        # Check for response example
        if "```json" not in content:
            errors.append(f"{md_file.name}: Missing JSON response example")

    return errors


def validate_mermaid_diagrams(docs_dir: str) -> List[str]:
    """Check that overview files contain Mermaid diagrams."""
    errors = []
    docs_path = Path(docs_dir)

    overview_files = [
        ("data-model/_overview.md", "erDiagram"),
        ("workflows/etl/_pipeline-overview.md", "flowchart"),
        ("workflows/api/_endpoints-overview.md", "table or list"),
    ]

    for file_path, expected in overview_files:
        full_path = docs_path / file_path
        if full_path.exists():
            content = full_path.read_text(errors="ignore")
            if "```mermaid" not in content:
                errors.append(f"{file_path}: Missing Mermaid diagram")
            elif expected != "table or list" and expected not in content:
                errors.append(f"{file_path}: Expected {expected} diagram type")

    return errors


def validate_cross_references(docs_dir: str) -> List[str]:
    """Check for broken internal links."""
    errors = []
    docs_path = Path(docs_dir)

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for md_file in docs_path.rglob("*.md"):
        content = md_file.read_text(errors="ignore")
        file_dir = md_file.parent

        for match in link_pattern.finditer(content):
            link_text, link_target = match.groups()

            # Skip external links and anchors
            if link_target.startswith(("http://", "https://", "#")):
                continue

            # Resolve relative path
            target_path = (file_dir / link_target).resolve()

            # Remove anchor if present
            if "#" in str(target_path):
                target_path = Path(str(target_path).split("#")[0])

            if not target_path.exists():
                rel_file = md_file.relative_to(docs_path)
                errors.append(f"{rel_file}: Broken link to {link_target}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate documentation structure")
    parser.add_argument("docs_dir", help="Documentation directory")
    parser.add_argument("--strict", action="store_true", help="Exit with error on warnings")

    args = parser.parse_args()

    print("=" * 60)
    print("DOCUMENTATION STRUCTURE VALIDATION")
    print("=" * 60)

    all_errors = []

    # Run validations
    validations = [
        ("Folder Structure", validate_folder_structure),
        ("Entity Files", validate_entity_files),
        ("ETL Files", validate_etl_files),
        ("API Files", validate_api_files),
        ("Mermaid Diagrams", validate_mermaid_diagrams),
        ("Cross References", validate_cross_references),
    ]

    for name, validator in validations:
        print(f"\n[{name}]")
        errors = validator(args.docs_dir)

        if errors:
            for error in errors:
                print(f"  ERROR: {error}")
            all_errors.extend(errors)
        else:
            print("  OK")

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} errors found")
        if args.strict:
            sys.exit(1)
    else:
        print("VALIDATION PASSED: All checks OK")
    print("=" * 60)


if __name__ == "__main__":
    main()
