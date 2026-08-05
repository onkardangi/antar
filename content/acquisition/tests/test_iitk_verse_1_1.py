"""Offline tests for IIT Verse 1.1 acquisition parsing and comparison."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_ACQ = Path(__file__).resolve().parents[1]
_NORM = Path(__file__).resolve().parents[2] / "normalization"
for p in (_ACQ, _NORM):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from fetch_iitk_verse_1_1 import (  # noqa: E402
    AcquisitionError,
    SOURCE_ID,
    extract_mool_root_text,
)
from compare_verse_1_1 import (  # noqa: E402
    compare_verse_1_1,
    comparison_normalize,
    split_wikisource_1_1,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

SAMPLE_HTML = """
<html><body>
<p><font size="4px"><b>मूल श्लोकः</b></font></p>
<p align="center"><font size="3px">धृतराष्ट्र उवाच<br />
<br />
धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।<br />
<br />
मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।</font><br />
&nbsp;</p>
<div>Translation English commentary should be ignored</div>
<div>व्याख्या should be outside mool</div>
</body></html>
"""

WIKI_FULL = """ॐ
श्रीपरमात्मने नमः
अथ श्रीमद्भगवद्गीता
प्रथमोऽध्यायः

धृतराष्ट्र उवाच
धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः ।
मामकाः पाण्डवाश्चैव किमकुर्वत संजय  ॥१-१॥"""

IIT_FULL = """धृतराष्ट्र उवाच

धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।

मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।"""


class IitkExtractionTests(unittest.TestCase):
    def test_root_verse_extraction_from_iit_like_page(self) -> None:
        text = extract_mool_root_text(SAMPLE_HTML)
        self.assertIn("धृतराष्ट्र उवाच", text)
        self.assertIn("धर्मक्षेत्रे", text)
        self.assertIn("1.1", text)

    def test_commentary_exclusion(self) -> None:
        text = extract_mool_root_text(SAMPLE_HTML)
        self.assertNotIn("व्याख्या", text)

    def test_translation_exclusion(self) -> None:
        text = extract_mool_root_text(SAMPLE_HTML)
        self.assertNotIn("Translation", text)
        self.assertNotIn("English commentary", text)

    def test_ambiguous_mool_raises(self) -> None:
        bad = SAMPLE_HTML + SAMPLE_HTML
        with self.assertRaises(AcquisitionError):
            extract_mool_root_text(bad)


class CompareVerse11Tests(unittest.TestCase):
    def test_comparison_match_after_whitespace_punctuation_normalization(self) -> None:
        result = compare_verse_1_1(WIKI_FULL, IIT_FULL)
        self.assertEqual(result["result"], "TEXT_MATCH_AFTER_DOCUMENTED_NORMALIZATION")
        cats = {d["category"] for d in result["differences"]}
        self.assertIn("orthography", cats)
        self.assertNotIn("words", cats)

    def test_substantive_word_difference_detection(self) -> None:
        iit = IIT_FULL.replace("धर्मक्षेत्रे", "अधर्मक्षेत्रे")
        result = compare_verse_1_1(WIKI_FULL, iit)
        self.assertEqual(result["result"], "SOURCE_CONFLICT")
        self.assertTrue(any(d["category"] == "words" for d in result["differences"]))

    def test_front_matter_separation(self) -> None:
        bounds = split_wikisource_1_1(WIKI_FULL)
        self.assertIn("ॐ", bounds.front_matter)
        self.assertEqual(bounds.speaker_label, "धृतराष्ट्र उवाच")
        self.assertIn("धर्मक्षेत्रे", bounds.root_verse_body)
        self.assertNotIn("ॐ", bounds.root_verse_body)

    def test_speaker_label_comparison(self) -> None:
        result = compare_verse_1_1(WIKI_FULL, IIT_FULL)
        self.assertEqual(
            result["wikisourceBoundaries"]["speakerLabel"],
            result["iitkBoundaries"]["speakerLabel"],
        )

    def test_comparison_normalize_nfc_lf(self) -> None:
        text, ops = comparison_normalize("धर्मक्षेत्रे  \r\n")
        self.assertTrue(text.endswith("धर्मक्षेत्रे") or "धर्मक्षेत्रे" in text)
        self.assertIn("trimmed_surrounding_whitespace", ops)


class PolicyAndWorkspaceTests(unittest.TestCase):
    def test_refusal_to_mark_verification_only_as_import_approved(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "content/registry/sources.json").read_text(encoding="utf-8")
        )
        entry = next(s for s in registry["sources"] if s["id"] == SOURCE_ID)
        self.assertEqual(entry["status"], "VERIFICATION_ONLY")
        self.assertNotIn(
            entry["status"],
            {"APPROVED_FOR_IMPORT", "APPROVED_FOR_NORMALIZATION", "IMPORTED"},
        )

    def test_only_1_1_source_comparison_record_changed_from_baseline_shape(self) -> None:
        recs = [
            json.loads(l)
            for l in (
                REPO_ROOT
                / "content/editorial/bhagavad-gita/chapter-01/source-comparison.jsonl"
            )
            .read_text(encoding="utf-8")
            .splitlines()
            if l.strip()
        ]
        one = next(r for r in recs if r["canonicalReference"] == "1.1")
        self.assertEqual(len(one["sources"]), 2)
        # After Chapter 1 secondary acquisition, other verses may also have IIT evidence.
        # Invariant: Wikisource remains present; IIT entries stay verification-only ids.
        for r in recs:
            ids = [s.get("sourceId") for s in r.get("sources") or []]
            self.assertIn(
                "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151",
                ids,
            )
            for sid in ids:
                if sid and "iitk" in sid:
                    self.assertIn("verification", sid)

    def test_canonical_draft_unresolved_conflict_rows_remain_null_sanskrit(self) -> None:
        """IIT acquisition must not populate unresolved conflict Verses."""
        import json

        draft = [
            json.loads(l)
            for l in (
                REPO_ROOT
                / "content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        final_refs = {"1.20", "1.22"}
        for row in draft:
            if row["canonicalReference"] not in final_refs:
                continue
            if row.get("approvalStatus") == "APPROVED":
                # Allowed only via later final-conflict human apply, not IIT acquisition.
                self.assertEqual(
                    row.get("decisionType"),
                    "FINAL_CHAPTER01_CONFLICT_RESOLUTION",
                )
                self.assertIsNotNone(row.get("sanskritText"))
                self.assertNotIn("iitk", str(row.get("selectedSourceId") or ""))
            else:
                self.assertIsNone(row.get("sanskritText"))


if __name__ == "__main__":
    unittest.main()
