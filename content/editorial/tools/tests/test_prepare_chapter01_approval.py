"""Tests for Chapter 1 human-approval preparation."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from prepare_chapter01_approval import (  # noqa: E402
    build_batch_candidates,
    build_conflict_analyses,
    build_third_reference_queue,
    generate_all,
    looks_orthographic_pair,
    sha256_text,
    token_level_diff,
)
from validate_chapter01_approval_prep import validate_approval_prep  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class ApprovalPrepTests(unittest.TestCase):
    def test_batch_candidate_generation(self) -> None:
        reports = load_jsonl(CHAPTER_DIR / "automated-comparison-report.jsonl")
        comparisons = {
            r["canonicalReference"]: r
            for r in load_jsonl(CHAPTER_DIR / "source-comparison.jsonl")
        }
        cands = build_batch_candidates(reports, comparisons)
        self.assertEqual(len(cands), 34)
        for c in cands:
            self.assertEqual(c["approvalStatus"], "PENDING")
            self.assertTrue(c["requiresHumanApproval"])
            self.assertIsNone(c["proposedTransliteration"])

    def test_source_text_checksum_verification(self) -> None:
        cands = load_jsonl(CHAPTER_DIR / "normalization-match-approval-candidate.jsonl")
        comparisons = {
            r["canonicalReference"]: r
            for r in load_jsonl(CHAPTER_DIR / "source-comparison.jsonl")
        }
        for c in cands:
            wiki = next(
                s
                for s in comparisons[c["canonicalReference"]]["sources"]
                if "wikisource" in s["sourceId"]
            )
            self.assertEqual(c["proposedSanskritText"], wiki["sanskritText"])
            self.assertEqual(
                c["proposedSanskritTextChecksumSha256"],
                sha256_text(wiki["sanskritText"]),
            )

    def test_no_cross_source_text_synthesis(self) -> None:
        cands = load_jsonl(CHAPTER_DIR / "normalization-match-approval-candidate.jsonl")
        comparisons = {
            r["canonicalReference"]: r
            for r in load_jsonl(CHAPTER_DIR / "source-comparison.jsonl")
        }
        for c in cands:
            wiki = next(
                s
                for s in comparisons[c["canonicalReference"]]["sources"]
                if "wikisource" in s["sourceId"]
            )
            iitk = next(
                s
                for s in comparisons[c["canonicalReference"]]["sources"]
                if "iitk" in s["sourceId"]
            )
            self.assertEqual(c["proposedSanskritText"], wiki["sanskritText"])
            # Must not equal a blend: if sources differ, proposed equals only wiki
            if wiki["sanskritText"] != iitk["sanskritText"]:
                self.assertNotEqual(c["proposedSanskritText"], iitk["sanskritText"])

    def test_conflict_token_diff(self) -> None:
        diffs = token_level_diff(
            "आचार्यमुपसंगम्य राजा",
            "आचार्यमुपसङ्गम्य राजा",
        )
        self.assertTrue(any(d.get("looksOrthographic") for d in diffs))

    def test_orthographic_only_classification(self) -> None:
        self.assertTrue(looks_orthographic_pair("वर्णसंकरः", "वर्णसङ्करः"))
        self.assertTrue(looks_orthographic_pair("धनञ्जयः", "धनंजयः"))
        self.assertFalse(looks_orthographic_pair("धर्मक्षेत्रे", "अधर्मक्षेत्रे"))

    def test_substantive_word_conflict(self) -> None:
        self.assertFalse(looks_orthographic_pair("कुरुक्षेत्रे", "काशीक्षेत्रे"))

    def test_repeated_pattern_clustering(self) -> None:
        text = (CHAPTER_DIR / "orthographic-patterns.md").read_text(encoding="utf-8")
        self.assertIn("anusvara_vs_nga_cluster", text)
        self.assertIn("avagraha_representation", text)

    def test_third_reference_queue_generation(self) -> None:
        conflicts = load_jsonl(CHAPTER_DIR / "source-conflict-analysis.jsonl")
        queue = build_third_reference_queue(conflicts)
        refs = {e["canonicalReference"] for e in queue["entries"]}
        self.assertIn("1.20", refs)
        self.assertIn("1.22", refs)
        self.assertNotIn("1.24", refs)  # speaker orthography only
        for e in queue["entries"]:
            self.assertEqual(e["status"], "QUEUED_NOT_ACQUIRED")

    def test_all_47_references_partitioned_exactly_once(self) -> None:
        cands = {c["canonicalReference"] for c in load_jsonl(CHAPTER_DIR / "normalization-match-approval-candidate.jsonl")}
        confs = {c["canonicalReference"] for c in load_jsonl(CHAPTER_DIR / "source-conflict-analysis.jsonl")}
        self.assertEqual(len(cands), 34)
        self.assertEqual(len(confs), 13)
        self.assertFalse(cands & confs)
        self.assertEqual(cands | confs, {f"1.{i}" for i in range(1, 48)})

    def test_no_automatic_approval(self) -> None:
        manifest = json.loads(
            (CHAPTER_DIR / "chapter-01-approval-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["approved"], 0)
        self.assertEqual(manifest["status"], "PENDING_EDITORIAL_REVIEW")
        self.assertIsNone(manifest["reviewer"])
        for c in load_jsonl(CHAPTER_DIR / "normalization-match-approval-candidate.jsonl"):
            self.assertEqual(c["approvalStatus"], "PENDING")
        for c in load_jsonl(CHAPTER_DIR / "source-conflict-analysis.jsonl"):
            self.assertEqual(c["approvalStatus"], "PENDING")

    def test_deterministic_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # Copy required inputs into temp chapter dir
            tmp_chapter = Path(tmp) / "chapter-01"
            tmp_chapter.mkdir()
            for name in (
                "automated-comparison-report.jsonl",
                "source-comparison.jsonl",
            ):
                (tmp_chapter / name).write_bytes((CHAPTER_DIR / name).read_bytes())
            generate_all(chapter_dir=tmp_chapter)
            first = {
                p.name: p.read_bytes()
                for p in tmp_chapter.iterdir()
                if p.suffix in {".jsonl", ".json", ".md"}
                and p.name
                in {
                    "normalization-match-approval-candidate.jsonl",
                    "source-conflict-analysis.jsonl",
                    "third-reference-queue.json",
                    "chapter-01-approval-manifest.json",
                    "normalization-match-review.md",
                    "orthographic-patterns.md",
                }
            }
            generate_all(chapter_dir=tmp_chapter)
            second = {
                p.name: p.read_bytes()
                for p in tmp_chapter.iterdir()
                if p.name in first
            }
            self.assertEqual(first, second)

    def test_validator_ok_on_workspace(self) -> None:
        draft_sha = hashlib.sha256(
            (CHAPTER_DIR / "canonical-draft.jsonl").read_bytes()
        ).hexdigest()
        result = validate_approval_prep(
            chapter_dir=CHAPTER_DIR, draft_sha_expected=draft_sha
        )
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
