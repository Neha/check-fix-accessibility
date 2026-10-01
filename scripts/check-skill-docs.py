#!/usr/bin/env python3
"""Check that the skill version matches the changelog, and relative links resolve."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "check-fix-accessibility" / "SKILL.md"
README = ROOT / "README.md"
DOC_FILES = [
    README,
    SKILL,
    ROOT / "check-fix-accessibility" / "frameworks.md",
    ROOT / "check-fix-accessibility" / "reference.md",
    ROOT / "examples" / "mcp" / "README.md",
]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
VERSION_RE = re.compile(r"^version:\s*(\S+)\s*$", re.MULTILINE)
CHANGELOG_RE = re.compile(r"^- \*\*(\d+\.\d+\.\d+)\*\*", re.MULTILINE)


def github_slug(heading: str) -> str:
    """Match GitHub's heading anchors: drop punctuation, keep hyphens, spaces become hyphens."""
    kept = []
    for char in heading.strip().lower():
        if char.isalnum() or char in "-_ ":
            kept.append(char)
    return "".join(kept).replace(" ", "-")


def headings(path: Path) -> set[str]:
    return {github_slug(match.group(2)) for match in HEADING_RE.finditer(path.read_text(encoding="utf-8"))}


def check_version() -> list[str]:
    skill = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    version = VERSION_RE.search(skill)
    changelog = CHANGELOG_RE.search(skill)
    errors = []
    if not version:
        return ["SKILL.md is missing a version field"]
    if not changelog:
        return ["SKILL.md changelog has no version entry"]
    current = version.group(1)
    if changelog.group(1) != current:
        errors.append(
            f"frontmatter version {current} does not match the first changelog entry {changelog.group(1)}"
        )
    for label, pattern in (
        ("Skill version", rf"Skill version {re.escape(current)}"),
        ("summary version", rf"\*\*Version\*\*: {re.escape(current)}"),
    ):
        if not re.search(pattern, readme):
            errors.append(f"README is missing {label} {current}")
    return errors


def check_links() -> list[str]:
    errors = []
    for path in DOC_FILES:
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = target.partition("#")
            if not file_part:
                destination = path
            else:
                destination = (path.parent / file_part).resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)} links outside the repo: {target}")
                continue
            if not destination.is_file():
                errors.append(f"{path.relative_to(ROOT)} links to a missing file: {target}")
                continue
            if anchor and anchor not in headings(destination):
                errors.append(f"{path.relative_to(ROOT)} links to a missing heading: {target}")
    return errors


def main() -> int:
    errors = check_version() + check_links()
    if errors:
        print("\n".join(errors))
        return 1
    print("Skill version and relative links check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
