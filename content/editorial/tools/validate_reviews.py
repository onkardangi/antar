#!/usr/bin/env python3
"""Validate Antar Verse editorial review Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = frozenset(
    {
        "UNREVIEWED",
        "READY_FOR_REVIEW",
        "UNDER_REVIEW",
        "APPROVED",
        "REJECTED",
        "NEEDS_SOURCE",
        "SOURCE_MISSING",
        "SOURCE_CONFLICT",
    }
)

REQUIRED_SECTIONS = [
    "Canonical Reference",
    "Status",
    "Sources",
    "Source Comparison",
    "Differences",
    "Editorial Notes",
    "Decision",
    "Approval",
    "Audit Log",
]

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"


class ReviewValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.files_checked = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def split_sections(text: str) -> dict[str, str]:
    """Split markdown into H1 sections by '# Title' headings."""
    lines = text.splitlines()
    sections: dict[str, list[str]] = {}
    order: list[str] = []
    current: str | None = None
    for line in lines:
        if line.startswith("# "):
            current = line[2:].strip()
            if current not in sections:
                order.append(current)
                sections[current] = []
            else:
                # duplicate heading — keep appending under same key; validator catches order issues
                pass
            continue
        if current is not None:
            sections[current].append(line)
    return {key: "\n".join(sections[key]).strip("\n") for key in order}


def first_nonempty_line(body: str) -> str:
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def approval_field(body: str, label: str) -> str:
    """Return text after 'Label:' on the same line, or empty."""
    pattern = re.compile(rf"^{re.escape(label)}:[ \t]*(.*)$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    return match.group(1).strip()


def validate_review_text(
    text: str,
    *,
    expected_ref: str | None = None,
    path_label: str = "<memory>",
) -> list[str]:
    errors: list[str] = []
    sections = split_sections(text)
    names = list(sections.keys())

    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(f"{path_label}: missing required section '# {required}'")

    # Order check among present required sections
    present_required = [n for n in names if n in REQUIRED_SECTIONS]
    expected_present = [n for n in REQUIRED_SECTIONS if n in sections]
    if present_required != expected_present:
        errors.append(
            f"{path_label}: required sections out of order "
            f"(found {present_required}, expected {expected_present})"
        )

    if "Canonical Reference" in sections:
        ref = first_nonempty_line(sections["Canonical Reference"])
        if not re.fullmatch(r"\d+\.\d+", ref or ""):
            errors.append(f"{path_label}: canonical reference must look like chapter.verse")
        if expected_ref is not None and ref != expected_ref:
            errors.append(
                f"{path_label}: canonical reference {ref!r} does not match filename {expected_ref!r}"
            )

    status = None
    if "Status" in sections:
        status = first_nonempty_line(sections["Status"])
        if status not in ALLOWED_STATUSES:
            errors.append(f"{path_label}: invalid status {status!r}")

    if "Audit Log" in sections:
        audit = sections["Audit Log"].strip()
        if audit == "":
            errors.append(f"{path_label}: audit log is empty")
    else:
        errors.append(f"{path_label}: audit log section missing")

    if "Approval" in sections:
        approval = sections["Approval"]
        for label in ("Reviewer", "Second Reviewer", "Date"):
            if not re.search(rf"^{label}:", approval, re.MULTILINE):
                errors.append(f"{path_label}: Approval missing '{label}:' field")
        reviewer = approval_field(approval, "Reviewer")
        second = approval_field(approval, "Second Reviewer")
        date_value = approval_field(approval, "Date")
        if status == "APPROVED":
            if reviewer == "":
                errors.append(f"{path_label}: APPROVED requires non-blank Reviewer")
            if date_value == "":
                errors.append(f"{path_label}: APPROVED requires non-blank Date")
        else:
            # Phase 1 rule: approval identity fields blank unless APPROVED
            if reviewer or second or date_value:
                errors.append(
                    f"{path_label}: Approval fields must be blank unless status is APPROVED"
                )

    if "Differences" in sections:
        # Soft reminder only if section empty
        if sections["Differences"].strip() == "":
            errors.append(f"{path_label}: Differences section must not be empty")

    return errors


def validate_review_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: file not found"]
    expected_ref = path.stem
    text = path.read_text(encoding="utf-8")
    return validate_review_text(text, expected_ref=expected_ref, path_label=str(path))


def validate_reviews_dir(reviews_dir: Path) -> ReviewValidationResult:
    result = ReviewValidationResult()
    if not reviews_dir.is_dir():
        result.errors.append(f"reviews directory not found: {reviews_dir}")
        return result
    files = sorted(
        p for p in reviews_dir.glob("*.md") if re.fullmatch(r"\d+\.\d+", p.stem)
    )
    for path in files:
        result.files_checked += 1
        result.errors.extend(validate_review_file(path))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Antar editorial review files.")
    parser.add_argument(
        "--reviews-dir",
        type=Path,
        default=DEFAULT_REVIEWS_DIR,
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Validate a single review file",
    )
    args = parser.parse_args(argv)

    if args.file is not None:
        errors = validate_review_file(args.file)
        files_checked = 1
    else:
        outcome = validate_reviews_dir(args.reviews_dir)
        errors = outcome.errors
        files_checked = outcome.files_checked

    payload: dict[str, Any] = {
        "ok": not errors,
        "filesChecked": files_checked,
        "errors": errors,
    }
    print(json_dumps(payload))
    return 0 if not errors else 1


def json_dumps(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    raise SystemExit(main())
