#!/usr/bin/env python3
"""Focused offline tests for Besant & Das 1905 Chapter 1 editorial extraction."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from extract_besant_das_chapter01 import (  # noqa: E402
    SOURCE_CHECKSUM,
    SOURCE_ID,
    WORKSPACE,
    chapter01_units,
    write_workspace,
)
from validate_translation_segments import validate_workspace  # noqa: E402

SWARUPANANDA_WS = (
    ROOT / "content/translation-editorial/swarupananda-1909/chapter-01"
)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
GLOSS_HINTS = re.compile(
    r"(?i)\b(word[- ]by[- ]word|lit\.|literally:|gloss:)\b"
)
LABEL_QUIRK_VERSES = {1, 28, 33}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class BesantDasChapter01ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = ROOT / WORKSPACE
        cls.assertTrue(
            cls.workspace.is_dir(),
            f"missing workspace {cls.workspace}",
        )
        cls.segments = _load_jsonl(cls.workspace / "segment-draft.jsonl")
        cls.extraction = _load_jsonl(cls.workspace / "source-extraction.jsonl")
        cls.coverage = json.loads(
            (cls.workspace / "coverage-map.json").read_text(encoding="utf-8")
        )

    def test_exactly_forty_seven_rows(self) -> None:
        self.assertEqual(len(self.segments), 47)
        self.assertEqual(len(self.extraction), 47)
        self.assertEqual(self.coverage["segmentCount"], 47)
        self.assertEqual(len(chapter01_units()), 47)

    def test_exact_reference_range_no_duplicates(self) -> None:
        refs = [s["coveredCanonicalReferences"][0] for s in self.segments]
        self.assertEqual(refs, [f"1.{v}" for v in range(1, 48)])
        self.assertEqual(len(set(refs)), 47)
        for s in self.segments:
            self.assertEqual(len(s["coveredVerseNumbers"]), 1)
            self.assertEqual(len(s["coveredCanonicalReferences"]), 1)

    def test_no_approved_rows(self) -> None:
        statuses = {s["publicationStatus"] for s in self.segments}
        self.assertEqual(statuses, {"UNREVIEWED"})
        self.assertEqual(self.coverage.get("approvedCount"), 0)

    def test_nonblank_candidate_text(self) -> None:
        for s in self.segments:
            self.assertTrue(s["translationText"].strip(), s["segmentId"])

    def test_source_provenance_present(self) -> None:
        for s in self.segments:
            self.assertEqual(s["sourceId"], SOURCE_ID)
            self.assertEqual(s["sourceChecksum"], SOURCE_CHECKSUM)
            self.assertEqual(s["sourceRole"], "PRIMARY_TRANSLATION_CANDIDATE")
            sp = s["sourcePage"]
            self.assertIsInstance(sp["printed"], int)
            self.assertEqual(sp["scanLeaf"], 46 + sp["printed"])
            self.assertGreaterEqual(sp["printed"], 1)
            self.assertLessEqual(sp["printed"], 22)

    def test_known_label_quirks_handled(self) -> None:
        for v in LABEL_QUIRK_VERSES:
            seg = next(s for s in self.segments if s["coveredVerseNumbers"] == [v])
            self.assertIn("LABEL_QUIRK_NO_ARABIC", seg.get("reviewFlags") or [])
            # Arabic (N) is not the sourceLabel for these quirks.
            self.assertNotRegex(seg["sourceLabel"], rf"^\({v}\)$")

    def test_no_accidental_cross_verse_merging(self) -> None:
        self.assertEqual(self.coverage["multiVerseSegmentCount"], 0)
        self.assertEqual(self.coverage["segmentsWithMultiVerseCoverage"], [])
        self.assertTrue(self.coverage["packageFormatV1Compatible"])
        for s in self.segments:
            self.assertEqual(len(s["coveredVerseNumbers"]), 1)

    def test_no_devanagari_or_obvious_gloss_leakage(self) -> None:
        for s in self.segments:
            text = s["translationText"]
            self.assertIsNone(
                DEVANAGARI.search(text),
                f"Devanagari in {s['segmentId']}",
            )
            self.assertIsNone(
                GLOSS_HINTS.search(text),
                f"gloss hint in {s['segmentId']}",
            )

    def test_no_package_import_metadata(self) -> None:
        forbidden = {
            "packageId",
            "importBatchId",
            "importedAt",
            "translationPackageVersion",
            "databaseId",
        }
        for s in self.segments:
            self.assertFalse(forbidden.intersection(s.keys()), s["segmentId"])

    def test_validator_ok_and_not_package_ready(self) -> None:
        report = validate_workspace(
            self.workspace,
            expected_verse_count=47,
            source_id=SOURCE_ID,
            source_checksum=SOURCE_CHECKSUM,
            registry_path=ROOT / "content/registry/sources.json",
        )
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["approvedCount"], 0)
        self.assertFalse(report["packageReady"])
        self.assertFalse(report["importReady"])
        self.assertEqual(report["statusCounts"].get("UNREVIEWED"), 47)

    def test_deterministic_regeneration(self) -> None:
        before = {
            name: _sha256(self.workspace / name)
            for name in (
                "segment-draft.jsonl",
                "source-extraction.jsonl",
                "coverage-map.json",
            )
        }
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "chapter-01"
            hashes = write_workspace(out)
            for name, digest in before.items():
                self.assertEqual(hashes[name], digest, name)
                self.assertEqual(_sha256(out / name), digest, name)
        # Re-run into the real workspace must not change bytes.
        write_workspace(self.workspace)
        after = {
            name: _sha256(self.workspace / name)
            for name in before
        }
        self.assertEqual(before, after)

    def test_swarupananda_workspace_untouched(self) -> None:
        self.assertTrue(SWARUPANANDA_WS.is_dir())
        # Besant extract must not rewrite Swarupananda segment drafts.
        sw_seg = SWARUPANANDA_WS / "segment-draft.jsonl"
        self.assertTrue(sw_seg.is_file())
        sample = sw_seg.read_text(encoding="utf-8")
        self.assertIn("swarupananda-1909", sample)
        self.assertNotIn("besant-das-1905", sample)
        # Pin: first line still Swarupananda source id.
        first = json.loads(sample.splitlines()[0])
        self.assertEqual(
            first["sourceId"],
            "bhagavad-gita-translation-en-swarupananda-1909-v1",
        )


if __name__ == "__main__":
    unittest.main()
