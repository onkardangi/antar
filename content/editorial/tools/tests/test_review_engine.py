"""Unit tests for editorial review generation and validation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from generate_review import GenerateError, generate_review, render_review  # noqa: E402
from validate_reviews import (  # noqa: E402
    validate_review_file,
    validate_review_text,
    validate_reviews_dir,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


MINIMAL_REVIEW = """# Canonical Reference

9.9

# Status

UNREVIEWED

# Sources

| Source ID | Revision | License | Retrieved | Checksum | Status |
|-----------|----------|---------|-----------|----------|--------|
| _None attached_ |  |  |  |  |  |

# Source Comparison

No sources attached yet.

# Differences

No differences currently observed.

# Editorial Notes

_None._

# Decision

No editorial decision recorded.

# Approval

Reviewer:

Second Reviewer:

Date:

# Audit Log

- Review file created.
"""


class GenerateReviewTests(unittest.TestCase):
    def test_new_review_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = generate_review(
                chapter=1,
                verse=2,
                reviews_dir=Path(tmp),
                status="READY_FOR_REVIEW",
            )
            self.assertTrue(path.is_file())
            text = path.read_text(encoding="utf-8")
            self.assertIn("# Canonical Reference\n\n1.2\n", text)
            self.assertIn("# Status\n\nREADY_FOR_REVIEW\n", text)
            self.assertIn("# Audit Log\n", text)
            self.assertIn("No approval granted.", text)
            self.assertNotIn("\nAPPROVED\n", text)
            errors = validate_review_file(path)
            self.assertEqual(errors, [], errors)

    def test_duplicate_prevention(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            reviews_dir = Path(tmp)
            generate_review(chapter=1, verse=3, reviews_dir=reviews_dir)
            with self.assertRaises(GenerateError):
                generate_review(chapter=1, verse=3, reviews_dir=reviews_dir)


class ValidateReviewTests(unittest.TestCase):
    def test_invalid_status(self) -> None:
        text = MINIMAL_REVIEW.replace("UNREVIEWED", "DONE")
        errors = validate_review_text(text, expected_ref="9.9")
        self.assertTrue(any("invalid status" in e for e in errors), errors)

    def test_missing_section(self) -> None:
        text = MINIMAL_REVIEW.replace("# Differences\n\nNo differences currently observed.\n\n", "")
        errors = validate_review_text(text, expected_ref="9.9")
        self.assertTrue(any("Differences" in e for e in errors), errors)

    def test_approved_review_without_reviewer(self) -> None:
        text = MINIMAL_REVIEW.replace("UNREVIEWED", "APPROVED")
        errors = validate_review_text(text, expected_ref="9.9")
        self.assertTrue(any("Reviewer" in e for e in errors), errors)

    def test_approved_review_without_audit_log(self) -> None:
        text = MINIMAL_REVIEW.replace("UNREVIEWED", "APPROVED").replace(
            "# Audit Log\n\n- Review file created.\n",
            "# Audit Log\n\n",
        )
        # Also needs reviewer to isolate audit check — set reviewer/date so audit emptiness is visible
        text = text.replace("Reviewer:\n", "Reviewer: Ada\n").replace("Date:\n", "Date: 2026-08-04\n")
        errors = validate_review_text(text, expected_ref="9.9")
        self.assertTrue(any("audit log" in e.lower() for e in errors), errors)

    def test_existing_verse_1_1_review_valid_and_unapproved(self) -> None:
        path = REPO_ROOT / "content/editorial/reviews/1.1.md"
        self.assertTrue(path.is_file())
        errors = validate_review_file(path)
        self.assertEqual(errors, [], errors)
        text = path.read_text(encoding="utf-8")
        status_block = text.split("# Status", 1)[-1].split("#", 1)[0]
        self.assertIn("UNDER_REVIEW", status_block)
        self.assertNotIn("APPROVED", status_block.split())

    def test_validate_reviews_dir_includes_1_1(self) -> None:
        result = validate_reviews_dir(REPO_ROOT / "content/editorial/reviews")
        self.assertTrue(result.ok, result.errors)
        self.assertGreaterEqual(result.files_checked, 1)


if __name__ == "__main__":
    unittest.main()
