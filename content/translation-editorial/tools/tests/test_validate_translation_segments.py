#!/usr/bin/env python3
"""Offline unit tests for Translation segment validation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from validate_translation_segments import (  # noqa: E402
    render_report,
    validate_workspace,
)


SOURCE_ID = "bhagavad-gita-translation-en-swarupananda-1909-v1"
SOURCE_CHECKSUM = (
    "ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e"
)


def _seg(
    sid: str,
    verses: list[int],
    *,
    label: str | None = None,
    text: str = "Fluent English unit.",
    status: str = "UNREVIEWED",
    **extra,
) -> dict:
    chapter = 1
    row = {
        "segmentId": sid,
        "chapterNumber": chapter,
        "coveredVerseNumbers": verses,
        "coveredCanonicalReferences": [f"{chapter}.{v}" for v in verses],
        "sourceLabel": label if label is not None else f"I. {verses[0]}.",
        "translationText": text,
        "language": "en",
        "provider": "Swami Swarupananda",
        "sourceId": SOURCE_ID,
        "sourceChecksum": SOURCE_CHECKSUM,
        "sourcePage": {"printed": 1, "scanLeaf": 22},
        "publicationStatus": status,
        "editorialNotes": [],
        "contentVersion": 1,
    }
    row.update(extra)
    return row


def _coverage(segments: list[dict], expected: int = 47) -> dict:
    vmap = {}
    multi = []
    for s in segments:
        for v in s["coveredVerseNumbers"]:
            vmap[f"1.{v}"] = s["segmentId"]
        if len(s["coveredVerseNumbers"]) > 1:
            multi.append(s["segmentId"])
    return {
        "chapterNumber": 1,
        "expectedVerseCount": expected,
        "segmentCount": len(segments),
        "verseToSegment": vmap,
        "segmentsWithMultiVerseCoverage": multi,
        "uncoveredVerses": [],
        "multiplyCoveredVerses": [],
        "combinedLabelInventory": [],
        "status": "TEST",
    }


def _write_workspace(tmp: Path, segments: list[dict], expected: int = 47) -> Path:
    ws = tmp / "chapter-01"
    ws.mkdir(parents=True)
    (ws / "segment-draft.jsonl").write_text(
        "\n".join(json.dumps(s, sort_keys=True) for s in segments) + "\n",
        encoding="utf-8",
    )
    (ws / "source-extraction.jsonl").write_text(
        "\n".join(json.dumps(s, sort_keys=True) for s in segments) + "\n",
        encoding="utf-8",
    )
    cov = _coverage(segments, expected=expected)
    # Fix uncovered list in coverage for partial fixtures
    covered = {v for s in segments for v in s["coveredVerseNumbers"]}
    cov["uncoveredVerses"] = [v for v in range(1, expected + 1) if v not in covered]
    (ws / "coverage-map.json").write_text(
        json.dumps(cov, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return ws


def _full_chapter_segments() -> list[dict]:
    """Minimal valid 47-verse coverage with known Chapter 1 combined labels."""
    combined = {
        (4, 5, 6): "I. 4. 5. 6.",
        (21, 22): "I. 21—22.",
        (24, 25): "I. 24—25.",
        (28, 29): "I. 28—29.",
        (32, 33, 34): "I. 32—34.",
        (38, 39): "I. 38. 39.",
    }
    used = set()
    segs: list[dict] = []
    for key, label in combined.items():
        verses = list(key)
        used.update(verses)
        segs.append(
            _seg(
                f"swarupananda-1909-bg-1-{verses[0]:03d}-{verses[-1]:03d}",
                verses,
                label=label,
            )
        )
    for v in range(1, 48):
        if v in used:
            continue
        segs.append(_seg(f"swarupananda-1909-bg-1-{v:03d}", [v]))
    segs.sort(key=lambda s: s["coveredVerseNumbers"][0])
    return segs


class ValidateTranslationSegmentsTests(unittest.TestCase):
    def test_valid_one_to_one_segment(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            # ensure a known 1:1 exists
            one = next(s for s in segs if s["coveredVerseNumbers"] == [1])
            self.assertEqual(len(one["coveredVerseNumbers"]), 1)
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(
                ws,
                source_id=SOURCE_ID,
                source_checksum=SOURCE_CHECKSUM,
            )
            self.assertTrue(report["ok"], report["errors"])
            self.assertEqual(report["oneToOneSegmentCount"], 33)
            self.assertFalse(report["packageReady"])
            self.assertFalse(report["importReady"])

    def test_valid_n_to_one_segment(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            multi = next(s for s in segs if s["coveredVerseNumbers"] == [4, 5, 6])
            self.assertEqual(multi["sourceLabel"], "I. 4. 5. 6.")
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertTrue(report["ok"], report["errors"])
            self.assertEqual(report["multiVerseSegmentCount"], 6)

    def test_duplicate_verse_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs.append(_seg("dup-1-001", [1], label="I. 1. dup"))
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("duplicate coverage" in e for e in report["errors"]))

    def test_missing_verse_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = [s for s in _full_chapter_segments() if s["coveredVerseNumbers"] != [1]]
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("uncovered verses" in e for e in report["errors"]))

    def test_non_contiguous_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            for s in segs:
                if s["segmentId"].endswith("004-006"):
                    s["coveredVerseNumbers"] = [4, 6]
                    s["coveredCanonicalReferences"] = ["1.4", "1.6"]
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("contiguous" in e for e in report["errors"]))

    def test_mismatched_canonical_reference(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["coveredCanonicalReferences"] = ["1.99"]
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("coveredCanonicalReferences mismatch" in e for e in report["errors"]))

    def test_commentary_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["translationText"] = (
                "[True it is that the two parties are gathered together for battle, "
                "but was the influence of Kurukshetra long commentary text here.]"
            )
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("commentary" in e for e in report["errors"]))

    def test_word_by_word_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["translationText"] = (
                "धृतराष्ट्र Dhritarâshtra उवाच said संजय Sanjaya धर्मक्षेत्रे on the "
                "centre कुरुक्षेत्रे in Kurukshetra मामकाः my people पांडवाः the "
                "Pândavas किम् what अकुर्वत did do"
            )
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("word-by-word" in e for e in report["errors"]))

    def test_missing_source_label(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["sourceLabel"] = "   "
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("sourceLabel blank" in e for e in report["errors"]))

    def test_invalid_status(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["publicationStatus"] = "PUBLISHED"
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("invalid publicationStatus" in e for e in report["errors"]))

    def test_approved_without_reviewer(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            segs[0]["publicationStatus"] = "APPROVED"
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertFalse(report["ok"])
            self.assertTrue(any("APPROVED without reviewer" in e for e in report["errors"]))

    def test_deterministic_output(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            ws = _write_workspace(Path(td), segs)
            a = render_report(
                validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            )
            b = render_report(
                validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            )
            self.assertEqual(a, b)

    def test_known_chapter1_combined_label_regression(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            segs = _full_chapter_segments()
            labels = {s["sourceLabel"] for s in segs if len(s["coveredVerseNumbers"]) > 1}
            expected = {
                "I. 4. 5. 6.",
                "I. 21—22.",
                "I. 24—25.",
                "I. 28—29.",
                "I. 32—34.",
                "I. 38. 39.",
            }
            self.assertEqual(labels, expected)
            ws = _write_workspace(Path(td), segs)
            report = validate_workspace(ws, source_id=SOURCE_ID, source_checksum=SOURCE_CHECKSUM)
            self.assertTrue(report["ok"], report["errors"])
            self.assertEqual(report["coveredVerseCount"], 47)
            self.assertEqual(report["approvedCount"], 0)
            self.assertFalse(report["packageReady"])


if __name__ == "__main__":
    unittest.main()
