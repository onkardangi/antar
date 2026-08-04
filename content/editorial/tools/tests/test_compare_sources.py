"""Unit tests for automated editorial comparison engine (Phase 2)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from compare_sources import (  # noqa: E402
    compare_record,
    compare_two_texts,
    deterministic_audit_sample,
    load_json,
    load_jsonl,
    run_chapter,
    update_review_file,
    write_jsonl,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
POLICY_PATH = REPO_ROOT / "content/editorial/normalization-policy.json"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"


def policy() -> dict:
    return load_json(POLICY_PATH)


def policy_with_disabled(*rule_ids: str) -> dict:
    p = policy()
    for r in p["rules"]:
        if r["id"] in rule_ids:
            r["enabled"] = False
    return p


MINIMAL_REVIEW = """# Canonical Reference

1.99

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

Human note must survive automation.

# Decision

No editorial decision recorded.

# Approval

Reviewer:

Second Reviewer:

Date:

# Audit Log

- Review file created.
"""


class CompareSourcesTests(unittest.TestCase):
    def test_exact_match(self) -> None:
        text = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\nमामकाः पाण्डवाश्चैव किमकुर्वत संजय॥१-१॥"
        cmp = compare_two_texts(text, text, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "AUTO_MATCH")
        self.assertEqual(cmp["confidence"], 1.0)
        self.assertTrue(cmp["exactMatch"])

    def test_approved_normalization_match(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\nमामकाः पाण्डवाश्चैव किमकुर्वत संजय॥१-१॥"
        b = "धृतराष्ट्र उवाच\n\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "NORMALIZATION_MATCH")
        self.assertEqual(cmp["confidence"], 0.95)
        cats = {d["category"] for d in cmp["differences"]}
        self.assertIn("ORTHOGRAPHY_APPROVED", cats)
        self.assertIn("orthography_sanjaya_equivalence", cmp["normalizationRulesApplied"])

    def test_unapproved_orthographic_difference(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे"
        b = "धृतराष्ट्र उवाच\nधर्मक्षेत्रा कुरुक्षेत्रे"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        cats = {d["category"] for d in cmp["differences"]}
        self.assertTrue(cats & {"ORTHOGRAPHY_UNAPPROVED", "WORD_DIFFERENCE"})
        self.assertEqual(cmp["confidence"], 0.0)

    def test_substantive_word_difference(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता"
        b = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे पृथक्"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        self.assertIn("WORD_DIFFERENCE", {d["category"] for d in cmp["differences"]})

    def test_word_order_difference(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता"
        b = "धृतराष्ट्र उवाच\nकुरुक्षेत्रे धर्मक्षेत्रे समवेता"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        self.assertIn("WORD_ORDER", {d["category"] for d in cmp["differences"]})

    def test_missing_text(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे"
        b = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        cats = {d["category"] for d in cmp["differences"]}
        self.assertIn("MISSING_TEXT", cats)
        self.assertIn("EXTRA_TEXT", cats)

    def test_extra_text(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः अतिरिक्त"
        b = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        self.assertIn("EXTRA_TEXT", {d["category"] for d in cmp["differences"]})

    def test_segmentation_conflict(self) -> None:
        a = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे। समवेता युयुत्सवः"
        b = "धृतराष्ट्र उवाच\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता। युयुत्सवः"
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")
        self.assertIn("SEGMENTATION", {d["category"] for d in cmp["differences"]})
        self.assertTrue(cmp["requiresHumanReview"])

    def test_one_source_insufficient(self) -> None:
        record = {
            "chapterNumber": 1,
            "verseNumber": 2,
            "canonicalReference": "1.2",
            "sources": [
                {
                    "sourceId": "only-one",
                    "sanskritText": "धृतराष्ट्र उवाच\nधर्मक्षेत्रे",
                }
            ],
        }
        out = compare_record(record, policy=policy())
        self.assertEqual(out["classification"], "INSUFFICIENT_SOURCES")
        self.assertEqual(out["confidence"], 0.4)
        self.assertTrue(out["requiresHumanReview"])
        self.assertEqual(out["recommendedStatus"], "NEEDS_SOURCE")

    def test_confidence_calculation(self) -> None:
        exact = "क ख ग"
        self.assertEqual(
            compare_two_texts(exact, exact, source_id_a="a", source_id_b="b", policy=policy())[
                "confidence"
            ],
            1.0,
        )
        a = "क ख संजय"
        b = "क ख सञ्जय"
        self.assertEqual(
            compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=policy())["confidence"],
            0.95,
        )
        conflict = compare_two_texts(
            "क ख ग", "क ख घ", source_id_a="a", source_id_b="b", policy=policy()
        )
        self.assertEqual(conflict["confidence"], 0.0)

    def test_deterministic_audit_sampling(self) -> None:
        results = []
        for i in range(1, 11):
            results.append(
                {
                    "chapterNumber": 1,
                    "verseNumber": i,
                    "canonicalReference": f"1.{i}",
                    "classification": "AUTO_MATCH" if i % 2 else "NORMALIZATION_MATCH",
                    "normalizationRulesApplied": ["unicode_nfc"] if i == 3 else [],
                }
            )
        s1 = deterministic_audit_sample(results, policy=policy())
        s2 = deterministic_audit_sample(results, policy=policy())
        self.assertEqual(s1, s2)
        self.assertIn("1.1", s1["selectedReferences"])
        self.assertIn("1.10", s1["selectedReferences"])
        self.assertIn("1.3", s1["selectedReferences"])  # normalization applied
        self.assertGreaterEqual(len(s1["selectedReferences"]), s1["minimumMatchSample"])

    def test_preservation_of_human_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1.99.md"
            path.write_text(MINIMAL_REVIEW, encoding="utf-8")
            result = {
                "classification": "NORMALIZATION_MATCH",
                "confidence": 0.95,
                "sourceCount": 2,
                "requiresHumanReview": True,
                "recommendedStatus": "READY_FOR_HUMAN_APPROVAL",
                "normalizationRulesApplied": ["unicode_nfc"],
                "differences": [],
            }
            update_review_file(path, result, audit_selected=True, set_under_review=False)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Human note must survive automation", text)
            self.assertIn("## Automated Comparison", text)
            self.assertIn("No approval granted", text)
            self.assertIn("# Status\n\nREADY_FOR_REVIEW\n", text)
            self.assertNotIn("# Status\n\nAPPROVED\n", text)

    def test_refusal_to_auto_approve(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1.99.md"
            path.write_text(MINIMAL_REVIEW.replace("UNREVIEWED", "READY_FOR_REVIEW"), encoding="utf-8")
            result = {
                "classification": "AUTO_MATCH",
                "confidence": 1.0,
                "sourceCount": 2,
                "requiresHumanReview": False,
                "recommendedStatus": "READY_FOR_HUMAN_APPROVAL",
                "normalizationRulesApplied": [],
                "differences": [],
            }
            update_review_file(path, result, audit_selected=False, set_under_review=False)
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("# Status\n\nAPPROVED\n", text)
            self.assertIn("No approval granted", text)

    def test_repeated_run_determinism(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter = Path(tmp) / "chapter-01"
            chapter.mkdir()
            # Minimal two-source + one-source records
            rows = [
                {
                    "chapterNumber": 1,
                    "verseNumber": 1,
                    "canonicalReference": "1.1",
                    "sources": [
                        {"sourceId": "a", "sanskritText": "क ख संजय॥१-१॥"},
                        {"sourceId": "b", "sanskritText": "क ख सञ्जय।।1.1।।"},
                    ],
                },
                {
                    "chapterNumber": 1,
                    "verseNumber": 2,
                    "canonicalReference": "1.2",
                    "sources": [{"sourceId": "a", "sanskritText": "क ख ग"}],
                },
            ]
            write_jsonl(chapter / "source-comparison.jsonl", rows)
            # Copy policy into temp? Use real policy path
            o1 = run_chapter(
                chapter_dir=chapter,
                policy_path=POLICY_PATH,
                reference=None,
                update_reviews=False,
                set_under_review=False,
            )
            o2 = run_chapter(
                chapter_dir=chapter,
                policy_path=POLICY_PATH,
                reference=None,
                update_reviews=False,
                set_under_review=False,
            )
            self.assertEqual(o1["runMeta"]["reportSha256"], o2["runMeta"]["reportSha256"])
            t1 = (chapter / "automated-comparison-report.jsonl").read_text(encoding="utf-8")
            t2 = (chapter / "automated-comparison-report.jsonl").read_text(encoding="utf-8")
            self.assertEqual(t1, t2)

    def test_verse_1_1_regression(self) -> None:
        records = load_jsonl(CHAPTER_DIR / "source-comparison.jsonl")
        record = next(r for r in records if r["canonicalReference"] == "1.1")
        out = compare_record(record, policy=policy())
        self.assertEqual(out["classification"], "NORMALIZATION_MATCH")
        self.assertEqual(out["confidence"], 0.95)
        self.assertTrue(out["comparison"]["normalizedMatch"])
        self.assertFalse(out["comparison"]["substantiveDifference"])
        cats = {d["category"] for d in out["differences"]}
        self.assertIn("ORTHOGRAPHY_APPROVED", cats)
        self.assertIn("FRONT_MATTER", cats)
        self.assertTrue(out["requiresHumanReview"])  # front matter
        self.assertNotEqual(out["recommendedStatus"], "APPROVED")

    def test_rule_disable_supported(self) -> None:
        a = "क ख संजय"
        b = "क ख सञ्जय"
        disabled = policy_with_disabled("orthography_sanjaya_equivalence")
        cmp = compare_two_texts(a, b, source_id_a="a", source_id_b="b", policy=disabled)
        self.assertEqual(cmp["classification"], "SOURCE_CONFLICT")


class ValidateAutomatedComparisonTests(unittest.TestCase):
    def test_chapter_report_shape_when_present(self) -> None:
        report = CHAPTER_DIR / "automated-comparison-report.jsonl"
        if not report.is_file():
            self.skipTest("report not generated yet")
        from validate_automated_comparison import validate_report

        draft = CHAPTER_DIR / "canonical-draft.jsonl"
        draft_sha = (
            __import__("hashlib")
            .sha256(draft.read_text(encoding="utf-8").encode("utf-8"))
            .hexdigest()
        )
        result = validate_report(
            chapter_dir=CHAPTER_DIR,
            policy_path=POLICY_PATH,
            draft_sha_before=draft_sha,
        )
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
