#!/usr/bin/env python3
"""Validate an Antar Chapter editorial canonical-draft.jsonl file.

Structural and approval-gate checks only. Does not modify corpus data.
Does not judge textual accuracy of Sanskrit or transliteration.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_APPROVAL_STATUSES = frozenset(
    {
        "UNREVIEWED",
        "SOURCE_MISSING",
        "SOURCE_CONFLICT",
        "READY_FOR_REVIEW",
        "APPROVED",
        "REJECTED",
    }
)

DEFAULT_CHAPTER = 1
DEFAULT_EXPECTED_VERSES = 47


class ValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.records: list[dict[str, Any]] = []
        self.approved_count = 0
        self.sanskrit_populated = 0
        self.transliteration_populated = 0
        self.import_ready = False

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_nonblank(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8")
    if text.strip() == "":
        errors.append("file is empty")
        return records, errors
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.strip() == "":
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: JSON parse error: {exc}")
            continue
        if not isinstance(obj, dict):
            errors.append(f"line {line_no}: record must be a JSON object")
            continue
        records.append(obj)
    return records, errors


def validate_records(
    records: list[dict[str, Any]],
    *,
    chapter_number: int = DEFAULT_CHAPTER,
    expected_verses: int = DEFAULT_EXPECTED_VERSES,
) -> ValidationResult:
    result = ValidationResult()
    result.records = records

    if len(records) != expected_verses:
        result.errors.append(
            f"expected {expected_verses} records, found {len(records)}"
        )

    seen_refs: dict[str, int] = {}
    verse_numbers: list[int] = []

    for index, record in enumerate(records, start=1):
        ch = record.get("chapterNumber")
        vn = record.get("verseNumber")
        ref = record.get("canonicalReference")
        status = record.get("approvalStatus")
        sanskrit = record.get("sanskritText")
        transliteration = record.get("transliteration")

        if ch != chapter_number:
            result.errors.append(
                f"record {index}: chapterNumber must be {chapter_number}, found {ch!r}"
            )

        if not isinstance(vn, int) or isinstance(vn, bool):
            result.errors.append(
                f"record {index}: verseNumber must be an integer, found {vn!r}"
            )
            continue

        verse_numbers.append(vn)
        expected_ref = f"{chapter_number}.{vn}"
        if ref != expected_ref:
            result.errors.append(
                f"record {index}: canonicalReference must be {expected_ref!r}, found {ref!r}"
            )

        if ref in seen_refs:
            result.errors.append(
                f"record {index}: duplicate canonicalReference {ref!r} "
                f"(also record {seen_refs[ref]})"
            )
        else:
            if isinstance(ref, str):
                seen_refs[ref] = index

        if status not in ALLOWED_APPROVAL_STATUSES:
            result.errors.append(
                f"record {index} ({ref}): invalid approvalStatus {status!r}"
            )

        if _is_nonblank(sanskrit):
            result.sanskrit_populated += 1
        if _is_nonblank(transliteration):
            result.transliteration_populated += 1

        if status == "APPROVED":
            result.approved_count += 1
            if not _is_nonblank(sanskrit):
                result.errors.append(
                    f"record {index} ({ref}): APPROVED requires nonblank sanskritText"
                )
            # Sanskrit-only editorial approval may keep transliteration null.
            # Blank/whitespace strings are invalid; import_ready still requires
            # nonblank transliteration for every Verse.
            if transliteration is not None and not _is_nonblank(transliteration):
                result.errors.append(
                    f"record {index} ({ref}): transliteration must be null or nonblank"
                )

    expected_set = set(range(1, expected_verses + 1))
    actual_set = set(verse_numbers)
    missing = sorted(expected_set - actual_set)
    unexpected = sorted(actual_set - expected_set)
    if missing:
        result.errors.append(f"missing verse numbers: {missing}")
    if unexpected:
        result.errors.append(f"unexpected verse numbers: {unexpected}")

    duplicates = [v for v, n in Counter(verse_numbers).items() if n > 1]
    if duplicates:
        result.errors.append(f"duplicate verse numbers: {sorted(duplicates)}")

    result.import_ready = (
        result.ok
        and result.approved_count == expected_verses
        and result.sanskrit_populated == expected_verses
        and result.transliteration_populated == expected_verses
        and all(r.get("approvalStatus") == "APPROVED" for r in records)
    )

    if result.ok and not result.import_ready:
        # Not an error: unreviewed workspace is valid structurally.
        pass

    return result


def validate_path(
    path: Path,
    *,
    chapter_number: int = DEFAULT_CHAPTER,
    expected_verses: int = DEFAULT_EXPECTED_VERSES,
) -> ValidationResult:
    records, load_errors = load_jsonl(path)
    result = validate_records(
        records,
        chapter_number=chapter_number,
        expected_verses=expected_verses,
    )
    result.errors = load_errors + result.errors
    if load_errors:
        result.import_ready = False
    return result


def format_report(path: Path, result: ValidationResult) -> str:
    status_counts = Counter(r.get("approvalStatus") for r in result.records)
    lines = [
        f"file: {path}",
        f"structural_ok: {result.ok}",
        f"record_count: {len(result.records)}",
        f"approved_count: {result.approved_count}",
        f"sanskrit_populated: {result.sanskrit_populated}",
        f"transliteration_populated: {result.transliteration_populated}",
        f"import_ready: {result.import_ready}",
        f"approval_status_counts: {dict(status_counts)}",
    ]
    if result.errors:
        lines.append("errors:")
        lines.extend(f"  - {err}" for err in result.errors)
    else:
        lines.append("errors: []")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Antar Chapter canonical-draft.jsonl (structure only)."
    )
    parser.add_argument(
        "draft_jsonl",
        type=Path,
        help="Path to canonical-draft.jsonl",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=DEFAULT_CHAPTER,
        help="Expected chapter number (default: 1)",
    )
    parser.add_argument(
        "--expected-verses",
        type=int,
        default=DEFAULT_EXPECTED_VERSES,
        help="Expected verse count (default: 47)",
    )
    args = parser.parse_args(argv)

    if not args.draft_jsonl.is_file():
        print(f"error: file not found: {args.draft_jsonl}", file=sys.stderr)
        return 2

    result = validate_path(
        args.draft_jsonl,
        chapter_number=args.chapter,
        expected_verses=args.expected_verses,
    )
    print(format_report(args.draft_jsonl, result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
