#!/usr/bin/env python3
"""
Completeness checker for project documentation.

Validates that all entities, ETL steps, and API endpoints discovered
in the codebase have corresponding documentation files.

Usage:
    python check_completeness.py <docs_dir> [--ddl-dir <path>] [--main <path>] [--api-dir <path>]

Example:
    python check_completeness.py docs/ --ddl-dir sql/ --main main.py --api-dir api/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Set, Tuple, List


def find_entities_in_ddls(ddl_dir: str) -> Set[str]:
    """Extract table names from DDL files."""
    entities = set()
    ddl_path = Path(ddl_dir)

    if not ddl_path.exists():
        print(f"Warning: DDL directory '{ddl_dir}' not found")
        return entities

    # Patterns for CREATE TABLE statements
    patterns = [
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\']?(\w+)[`"\']?',
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:\w+\.)?[`"\']?(\w+)[`"\']?',
    ]

    for ddl_file in ddl_path.rglob("*.sql"):
        content = ddl_file.read_text(errors="ignore")
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities.update(m.lower() for m in matches)

    return entities


def find_etl_steps_in_main(main_file: str) -> List[str]:
    """Identify logical steps/functions in main.py."""
    steps = []
    main_path = Path(main_file)

    if not main_path.exists():
        print(f"Warning: Main file '{main_file}' not found")
        return steps

    content = main_path.read_text(errors="ignore")

    # Look for main function calls or step definitions
    # Pattern 1: Functions with step/process/extract/transform/load in name
    step_patterns = [
        r"def\s+((?:step|process|extract|transform|load|run|execute)_?\w*)\s*\(",
        r"def\s+(\w*(?:_step|_process|_extract|_transform|_load))\s*\(",
    ]

    for pattern in step_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        steps.extend(matches)

    # Pattern 2: Comments indicating steps
    step_comments = re.findall(r"#\s*(?:Step|Phase)\s*(\d+)[:\s]+(\w+)", content, re.IGNORECASE)
    for num, name in step_comments:
        steps.append(f"step_{num}_{name}")

    return list(dict.fromkeys(steps))  # Remove duplicates, preserve order


def find_api_endpoints(api_dir: str) -> Set[Tuple[str, str]]:
    """Extract API endpoints from route files."""
    endpoints = set()
    api_path = Path(api_dir)

    if not api_path.exists():
        print(f"Warning: API directory '{api_dir}' not found")
        return endpoints

    # Patterns for various frameworks
    patterns = [
        # FastAPI/Flask decorators
        r'@\w+\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
        # Express.js style
        r'\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
        # Generic route definitions
        r'route\s*=\s*["\']([^"\']+)["\']\s*.*method\s*=\s*["\'](\w+)["\']',
    ]

    for py_file in api_path.rglob("*.py"):
        content = py_file.read_text(errors="ignore")
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    method, path = match[0].upper(), match[1]
                    endpoints.add((method, path))

    return endpoints


def find_documented_entities(docs_dir: str) -> Set[str]:
    """Find entities with documentation files."""
    documented = set()
    entity_path = Path(docs_dir) / "data-model"

    if entity_path.exists():
        for md_file in entity_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                documented.add(md_file.stem.lower())

    return documented


def find_documented_etl_steps(docs_dir: str) -> Set[str]:
    """Find ETL steps with documentation files."""
    documented = set()
    etl_path = Path(docs_dir) / "workflows" / "etl"

    if etl_path.exists():
        for md_file in etl_path.glob("step-*.md"):
            documented.add(md_file.stem.lower())

    return documented


def find_documented_endpoints(docs_dir: str) -> Set[Tuple[str, str]]:
    """Find API endpoints with documentation files."""
    documented = set()
    api_path = Path(docs_dir) / "workflows" / "api"

    if api_path.exists():
        for md_file in api_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                # Parse filename: get-api-users.md -> (GET, /api/users)
                parts = md_file.stem.split("-", 1)
                if len(parts) == 2:
                    method = parts[0].upper()
                    path = "/" + parts[1].replace("-", "/")
                    documented.add((method, path))

    return documented


def check_code_references(docs_dir: str) -> List[str]:
    """Check that documentation files contain code references."""
    missing_refs = []
    docs_path = Path(docs_dir)

    # Pattern for code references like file.py:123 or file.py:10-20
    ref_pattern = r"\w+\.\w+:\d+"

    for md_file in docs_path.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        content = md_file.read_text(errors="ignore")

        # Skip template/overview files
        if "template" in md_file.name.lower():
            continue

        if not re.search(ref_pattern, content):
            missing_refs.append(str(md_file.relative_to(docs_path)))

    return missing_refs


def main():
    parser = argparse.ArgumentParser(description="Check documentation completeness")
    parser.add_argument("docs_dir", help="Documentation directory")
    parser.add_argument("--ddl-dir", default="sql", help="DDL files directory")
    parser.add_argument("--main", default="main.py", help="Main ETL script")
    parser.add_argument("--api-dir", default="api", help="API routes directory")
    parser.add_argument("--strict", action="store_true", help="Exit with error if incomplete")

    args = parser.parse_args()

    print("=" * 60)
    print("DOCUMENTATION COMPLETENESS CHECK")
    print("=" * 60)

    issues = []

    # Check entities
    print("\n[Entities]")
    source_entities = find_entities_in_ddls(args.ddl_dir)
    documented_entities = find_documented_entities(args.docs_dir)

    if source_entities:
        missing_entities = source_entities - documented_entities
        extra_entities = documented_entities - source_entities

        print(f"  Found in DDLs: {len(source_entities)}")
        print(f"  Documented: {len(documented_entities)}")

        if missing_entities:
            print(f"  MISSING documentation for: {', '.join(sorted(missing_entities))}")
            issues.append(f"{len(missing_entities)} entities missing documentation")

        if extra_entities:
            print(f"  Extra docs (no DDL): {', '.join(sorted(extra_entities))}")
    else:
        print("  No DDL files found to check")

    # Check ETL steps
    print("\n[ETL Steps]")
    source_steps = find_etl_steps_in_main(args.main)
    documented_steps = find_documented_etl_steps(args.docs_dir)

    if source_steps:
        print(f"  Found in main.py: {len(source_steps)}")
        print(f"  Documented: {len(documented_steps)}")

        if len(documented_steps) < len(source_steps):
            issues.append(
                f"ETL: {len(source_steps)} steps found, only {len(documented_steps)} documented"
            )
    else:
        print("  No ETL steps detected (check main.py naming conventions)")

    # Check API endpoints
    print("\n[API Endpoints]")
    source_endpoints = find_api_endpoints(args.api_dir)
    documented_endpoints = find_documented_endpoints(args.docs_dir)

    if source_endpoints:
        missing_endpoints = source_endpoints - documented_endpoints

        print(f"  Found in code: {len(source_endpoints)}")
        print(f"  Documented: {len(documented_endpoints)}")

        if missing_endpoints:
            for method, path in sorted(missing_endpoints):
                print(f"    MISSING: {method} {path}")
            issues.append(f"{len(missing_endpoints)} API endpoints missing documentation")
    else:
        print("  No API endpoints found to check")

    # Check code references
    print("\n[Code References]")
    missing_refs = check_code_references(args.docs_dir)

    if missing_refs:
        print(f"  Files WITHOUT code references ({len(missing_refs)}):")
        for f in missing_refs[:10]:  # Show first 10
            print(f"    - {f}")
        if len(missing_refs) > 10:
            print(f"    ... and {len(missing_refs) - 10} more")
        issues.append(f"{len(missing_refs)} files missing code references")
    else:
        print("  All documentation files contain code references")

    # Summary
    print("\n" + "=" * 60)
    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")

        if args.strict:
            print("\nExiting with error (--strict mode)")
            sys.exit(1)
    else:
        print("ALL CHECKS PASSED")

    print("=" * 60)


if __name__ == "__main__":
    main()
