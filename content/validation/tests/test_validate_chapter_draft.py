"""Unit tests for Chapter canonical-draft validator."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_VALIDATION_DIR = Path(__file__).resolve().parents[1]
if str(_VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(_VALIDATION_DIR))

from validate_chapter_draft import validate_path, validate_records


ALLOWED = [
    "UNREVIEWED",
    "SOURCE_MISSING",
    "SOURCE_CONFLICT",
    "READY_FOR_REVIEW",
    "APPROVED",
    "REJECTED",
]


def make_record(
    verse: int,
    *,
    chapter: int = 1,
    status: str = "UNREVIEWED",
    sanskrit: str | None = None,
    transliteration: str | None = None,
    ref: str | None = None,
) -> dict:
    return {
        "chapterNumber": chapter,
        "verseNumber": verse,
        "canonicalReference": ref if ref is not None else f"{chapter}.{verse}",
        "sanskritText": sanskrit,
        "transliteration": transliteration,
        "approvalStatus": status,
        "approvedSourceIds": [],
        "editorialNotes": [],
        "contentVersion": 1,
    }


def write_jsonl(records: list[dict]) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".jsonl",
        delete=False,
    )
    with tmp:
        for record in records:
            tmp.write(json.dumps(record, ensure_ascii=False) + "\n")
    return Path(tmp.name)


class ValidateChapterDraftTests(unittest.TestCase):
    def test_valid_unreviewed_chapter_1_workspace(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        path = write_jsonl(records)
        try:
            result = validate_path(path)
            self.assertTrue(result.ok, result.errors)
            self.assertEqual(result.approved_count, 0)
            self.assertEqual(result.sanskrit_populated, 0)
            self.assertEqual(result.transliteration_populated, 0)
            self.assertFalse(result.import_ready)
        finally:
            path.unlink(missing_ok=True)

    def test_missing_verse(self) -> None:
        records = [make_record(v) for v in range(1, 48) if v != 10]
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing verse numbers" in e for e in result.errors))
        self.assertFalse(result.import_ready)

    def test_duplicate_verse(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records.append(make_record(5))
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(
            any("duplicate" in e for e in result.errors),
            result.errors,
        )
        self.assertFalse(result.import_ready)

    def test_malformed_reference(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records[0]["canonicalReference"] = "1.01"
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(any("canonicalReference" in e for e in result.errors))

    def test_approved_missing_sanskrit(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records[0]["approvalStatus"] = "APPROVED"
        records[0]["sanskritText"] = None
        records[0]["transliteration"] = "dhṛtarāṣṭra uvāca"
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(any("sanskritText" in e for e in result.errors))

    def test_approved_blank_transliteration_invalid(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records[0]["approvalStatus"] = "APPROVED"
        records[0]["sanskritText"] = "धृतराष्ट्र उवाच"
        records[0]["transliteration"] = "   "
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(any("transliteration" in e for e in result.errors))

    def test_approved_null_transliteration_allowed_not_import_ready(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records[0]["approvalStatus"] = "APPROVED"
        records[0]["sanskritText"] = "धृतराष्ट्र उवाच"
        records[0]["transliteration"] = None
        result = validate_records(records)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.approved_count, 1)
        self.assertFalse(result.import_ready)

    def test_invalid_approval_status(self) -> None:
        records = [make_record(v) for v in range(1, 48)]
        records[3]["approvalStatus"] = "DONE"
        result = validate_records(records)
        self.assertFalse(result.ok)
        self.assertTrue(any("invalid approvalStatus" in e for e in result.errors))
        self.assertNotIn("DONE", ALLOWED)

    def test_all_approved_ready_corpus(self) -> None:
        records = [
            make_record(
                v,
                status="APPROVED",
                sanskrit=f"श्लोकः {v}",
                transliteration=f"sloka {v}",
            )
            for v in range(1, 48)
        ]
        result = validate_records(records)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.approved_count, 47)
        self.assertEqual(result.sanskrit_populated, 47)
        self.assertEqual(result.transliteration_populated, 47)
        self.assertTrue(result.import_ready)


if __name__ == "__main__":
    unittest.main()
