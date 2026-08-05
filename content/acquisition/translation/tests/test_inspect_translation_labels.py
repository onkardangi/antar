"""Offline tests for Translation OCR label inspection helpers."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_ACQ = Path(__file__).resolve().parents[1]
if str(_ACQ) not in sys.path:
    sys.path.insert(0, str(_ACQ))

from inspect_translation_labels import (  # noqa: E402
    InspectionError,
    inspect_chapter_1_ocr,
    missing_labels,
)


SAMPLE_OCR = """
CONTENTS
CHAP: I. THE GRIEF OF ARJUNA ... 1
CHAP: II. THE WAY OF KNOWLEDGE ... 27

PREFACE
Something about the book.

FIRST CHAPTER
THE GRIEF OF ARJUNA

1. 1.
Dhritarashtra said: ...

1. 2.
Sanjaya said: ...

1. 3-4.
Some combined rendering.

1. 5.
Next verse.

I. 47.
Final verse of chapter one.

SECOND CHAPTER
THE WAY OF KNOWLEDGE

2. 1.
Chapter two begins.
"""


class InspectTranslationLabelsTests(unittest.TestCase):
    def test_chapter_1_collects_labels_and_combined(self) -> None:
        result = inspect_chapter_1_ocr(SAMPLE_OCR, expected_verse_count=47)
        self.assertEqual(result["chapterNumber"], 1)
        self.assertIn("1.1", result["observedLabels"])
        self.assertIn("1.2", result["observedLabels"])
        self.assertIn("1.47", result["observedLabels"])
        combined = {(c["from"], c["to"]) for c in result["combinedLabels"]}
        self.assertIn((3, 4), combined)
        self.assertIn("1.6", result["missingLabels"])

    def test_missing_labels_helper(self) -> None:
        self.assertEqual(missing_labels(3, [1, 3]), ["1.2"])

    def test_missing_chapter_marker_raises(self) -> None:
        with self.assertRaises(InspectionError):
            inspect_chapter_1_ocr("no chapter here")

    def test_does_not_rewrite_ocr_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ocr.txt"
            path.write_text(SAMPLE_OCR, encoding="utf-8")
            before = path.read_bytes()
            inspect_chapter_1_ocr(path.read_text(encoding="utf-8"))
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
