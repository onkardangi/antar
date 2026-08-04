"""Offline tests for generalized IIT acquisition and chapter batching."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_ACQ = Path(__file__).resolve().parents[1]
if str(_ACQ) not in sys.path:
    sys.path.insert(0, str(_ACQ))

from fetch_iitk_chapter import run_batch  # noqa: E402
from fetch_iitk_verse import (  # noqa: E402
    AcquisitionError,
    TransientAcquisitionError,
    acquire_verse,
    extract_mool_root_text,
    fetch_with_retries,
    write_exclusive,
)
from integrate_iitk_workspace import apply_evidence_to_record  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]


def sample_html(chapter: int, verse: int, body: str | None = None) -> str:
    ref = f"{chapter}.{verse}"
    core = body or (
        f"सञ्जय उवाच<br /><br />"
        f"दृष्ट्वा तु पाण्डवानीकं व्यूढं दुर्योधनस्तदा।<br /><br />"
        f"आचार्यमुपसंगम्य राजा वचनमब्रवीत्।।{ref}।।"
    )
    return f"""
<html><body>
<p><font size="4px"><b>मूल श्लोकः</b></font></p>
<p align="center"><font size="3px">{core}</font><br />
&nbsp;</p>
<div>Translation English commentary should be ignored</div>
<div>व्याख्या should be outside mool</div>
</body></html>
"""


class SingleVerseParsingTests(unittest.TestCase):
    def test_single_verse_acquisition_parsing(self) -> None:
        text = extract_mool_root_text(sample_html(1, 2), chapter=1, verse=2)
        self.assertIn("सञ्जय उवाच", text)
        self.assertIn("1.2", text)

    def test_commentary_exclusion(self) -> None:
        text = extract_mool_root_text(sample_html(1, 3), chapter=1, verse=3)
        self.assertNotIn("व्याख्या", text)

    def test_translation_exclusion(self) -> None:
        text = extract_mool_root_text(sample_html(1, 3), chapter=1, verse=3)
        self.assertNotIn("Translation", text)

    def test_malformed_verse_identity(self) -> None:
        html = sample_html(1, 2, body="क ख ग।।1.9।।")
        with self.assertRaises(AcquisitionError):
            extract_mool_root_text(html, chapter=1, verse=2)


class FetchRetryAndOverwriteTests(unittest.TestCase):
    def test_bounded_retry(self) -> None:
        calls = {"n": 0}

        def flaky(_url: str, **_kwargs):
            calls["n"] += 1
            if calls["n"] < 3:
                raise TransientAcquisitionError("boom")
            return "https://example.test", b"ok", "text/html"

        with mock.patch("fetch_iitk_verse.fetch", side_effect=flaky):
            sleeps: list[float] = []
            url, raw, _ = fetch_with_retries(
                "https://example.test",
                user_agent="test",
                timeout=1,
                sleep_fn=sleeps.append,
            )
        self.assertEqual(calls["n"], 3)
        self.assertEqual(raw, b"ok")
        self.assertEqual(len(sleeps), 2)

    def test_refusal_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.json"
            write_exclusive(path, b"aaa")
            self.assertEqual(write_exclusive(path, b"aaa"), "unchanged")
            with self.assertRaises(AcquisitionError):
                write_exclusive(path, b"bbb")

    def test_delay_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sleeps: list[float] = []

            def fake_fetch(_url: str):
                return (
                    "https://old.gitasupersite.in/srimad?x=1",
                    sample_html(1, 4).encode("utf-8"),
                    "text/html",
                )

            meta = acquire_verse(
                chapter=1,
                verse=4,
                output_root=Path(tmp),
                delay_seconds=2.5,
                apply_delay=True,
                sleep_fn=sleeps.append,
                fetch_fn=fake_fetch,
            )
            self.assertEqual(sleeps, [2.5])
            self.assertEqual(meta["canonicalReference"], "1.4")
            self.assertEqual(meta["status"], "VERIFICATION_ONLY")


class BatchTests(unittest.TestCase):
    def test_batch_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            man = run_batch(
                chapter=1,
                verse_start=2,
                verse_end=4,
                output_root=Path(tmp),
                delay_seconds=2.0,
                timeout_seconds=5,
                user_agent="test",
                resume=False,
                dry_run=True,
            )
        self.assertTrue(man["dryRun"])
        self.assertEqual(man["skipped"], ["1.2", "1.3", "1.4"])
        self.assertFalse(man["chapterComplete"])  # dry-run is not completion
        self.assertEqual([r["outcome"] for r in man["records"]], ["dry_run"] * 3)

    def test_sequential_order(self) -> None:
        seen: list[int] = []

        def fake_acquire(**kwargs):
            seen.append(kwargs["verse"])
            return {
                "canonicalReference": f"1.{kwargs['verse']}",
                "retrievalTimestamp": "2026-01-01T00:00:00Z",
                "evidenceSha256": "a" * 64,
                "observedRootTextChecksumSha256": "b" * 64,
                "finalUrl": "https://example.test",
                "sourceId": f"id-{kwargs['verse']}",
            }

        with tempfile.TemporaryDirectory() as tmp:
            man = run_batch(
                chapter=1,
                verse_start=2,
                verse_end=5,
                output_root=Path(tmp),
                delay_seconds=2.0,
                timeout_seconds=5,
                user_agent="test",
                resume=False,
                dry_run=False,
                acquire_fn=fake_acquire,
            )
        self.assertEqual(seen, [2, 3, 4, 5])
        self.assertTrue(man["chapterComplete"])

    def test_resume_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def fake_fetch(_url: str):
                return ("https://example.test", sample_html(1, 2).encode(), "text/html")

            acquire_verse(
                chapter=1,
                verse=2,
                output_root=root,
                apply_delay=False,
                delay_seconds=2.0,
                fetch_fn=fake_fetch,
            )
            calls: list[int] = []

            def acquire_fn(**kwargs):
                calls.append(kwargs["verse"])
                return {
                    "canonicalReference": f"1.{kwargs['verse']}",
                    "retrievalTimestamp": "t",
                    "evidenceSha256": "c" * 64,
                    "observedRootTextChecksumSha256": "d" * 64,
                    "finalUrl": "u",
                    "sourceId": "s",
                }

            man = run_batch(
                chapter=1,
                verse_start=2,
                verse_end=3,
                output_root=root,
                delay_seconds=2.0,
                timeout_seconds=5,
                user_agent="test",
                resume=True,
                dry_run=False,
                acquire_fn=acquire_fn,
            )
        self.assertEqual(man["skipped"], ["1.2"])
        self.assertEqual(man["acquired"], ["1.3"])
        self.assertEqual(calls, [3])

    def test_manifest_success(self) -> None:
        def fake_acquire(**kwargs):
            return {
                "canonicalReference": f"1.{kwargs['verse']}",
                "retrievalTimestamp": "t",
                "evidenceSha256": "e" * 64,
                "observedRootTextChecksumSha256": "f" * 64,
                "finalUrl": "u",
                "sourceId": "s",
            }

        with tempfile.TemporaryDirectory() as tmp:
            man = run_batch(
                chapter=1,
                verse_start=2,
                verse_end=3,
                output_root=Path(tmp),
                delay_seconds=2.0,
                timeout_seconds=5,
                user_agent="test",
                resume=False,
                dry_run=False,
                acquire_fn=fake_acquire,
            )
        self.assertTrue(man["chapterComplete"])
        self.assertEqual(man["failed"], [])

    def test_manifest_partial_failure(self) -> None:
        def fake_acquire(**kwargs):
            if kwargs["verse"] == 3:
                raise AcquisitionError("provider blocked")
            return {
                "canonicalReference": f"1.{kwargs['verse']}",
                "retrievalTimestamp": "t",
                "evidenceSha256": "e" * 64,
                "observedRootTextChecksumSha256": "f" * 64,
                "finalUrl": "u",
                "sourceId": "s",
            }

        with tempfile.TemporaryDirectory() as tmp:
            man = run_batch(
                chapter=1,
                verse_start=2,
                verse_end=4,
                output_root=Path(tmp),
                delay_seconds=2.0,
                timeout_seconds=5,
                user_agent="test",
                resume=False,
                dry_run=False,
                acquire_fn=fake_acquire,
                stop_on_consecutive_errors=99,
            )
        self.assertFalse(man["chapterComplete"])
        self.assertEqual([f["canonicalReference"] for f in man["failed"]], ["1.3"])
        self.assertEqual(man["acquired"], ["1.2", "1.4"])


class WorkspaceIntegrationTests(unittest.TestCase):
    def test_source_comparison_update_for_one_verse(self) -> None:
        record = {
            "canonicalReference": "1.2",
            "chapterNumber": 1,
            "verseNumber": 2,
            "status": "READY_FOR_REVIEW",
            "notes": [],
            "sources": [
                {
                    "sourceId": "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151",
                    "sanskritText": "wiki",
                }
            ],
        }
        evidence = {
            "canonicalReference": "1.2",
            "sourceId": "bhagavad-gita-sanskrit-iitk-verse-1.2-verification-v1",
            "retrievalTimestamp": "2026-08-04T00:00:00Z",
            "observedRootText": "iit text।।1.2।।",
            "observedRootTextChecksumSha256": "aa",
        }
        metadata = {"evidenceSha256": "bb"}
        out = apply_evidence_to_record(
            record, evidence=evidence, metadata=metadata, acquisition_failed=False
        )
        self.assertEqual(len(out["sources"]), 2)
        self.assertEqual(out["status"], "READY_FOR_REVIEW")
        self.assertNotEqual(out["status"], "APPROVED")

    def test_no_auto_approval(self) -> None:
        record = {
            "canonicalReference": "1.2",
            "chapterNumber": 1,
            "verseNumber": 2,
            "status": "APPROVED",
            "notes": [],
            "sources": [],
        }
        out = apply_evidence_to_record(
            record, evidence=None, metadata=None, acquisition_failed=True
        )
        self.assertEqual(out["status"], "SOURCE_MISSING")
        self.assertNotEqual(out["status"], "APPROVED")

    def test_review_file_generation_without_overwriting_human_fields(self) -> None:
        tools = REPO_ROOT / "content/editorial/tools"
        if str(tools) not in sys.path:
            sys.path.insert(0, str(tools))
        from compare_sources import update_review_file
        from generate_review import generate_review

        with tempfile.TemporaryDirectory() as tmp:
            reviews = Path(tmp)
            # Minimal comparison file not required when force_unreviewed
            path = generate_review(
                chapter=1,
                verse=99,
                reviews_dir=reviews,
                force_unreviewed=True,
            )
            original = path.read_text(encoding="utf-8")
            path.write_text(
                original.replace("_None._", "Human note keep me."),
                encoding="utf-8",
            )
            result = {
                "classification": "NORMALIZATION_MATCH",
                "confidence": 0.95,
                "sourceCount": 2,
                "requiresHumanReview": True,
                "recommendedStatus": "READY_FOR_HUMAN_APPROVAL",
                "normalizationRulesApplied": [],
                "differences": [],
            }
            update_review_file(path, result, audit_selected=False, set_under_review=False)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Human note keep me.", text)
            self.assertNotIn("# Status\n\nAPPROVED\n", text)
            self.assertIn("No approval granted", text)


if __name__ == "__main__":
    unittest.main()
