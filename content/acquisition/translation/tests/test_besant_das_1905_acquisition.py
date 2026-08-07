"""Offline tests for Besant & Das 1905 acquisition + Chapter 1 inspection."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "content/raw/translations/besant-das-1905"
INSPECTION = (
    ROOT / "content/translation-selection/besant-das-1905-chapter01-inspection.json"
)
REGISTRY = ROOT / "content/registry/sources.json"
CHECKSUMS = ROOT / "content/checksums/raw.sha256"
SWARUPANANDA_RAW = ROOT / "content/raw/translations/swarupananda-1909"

BESANT_ID = "bhagavad-gita-translation-en-besant-das-1905-v1"
SWARUPANANDA_ID = "bhagavad-gita-translation-en-swarupananda-1909-v1"

EXPECTED_MASTER = "bhagavadgitawith00londiala.pdf"
EXPECTED_MASTER_SHA256 = (
    "7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115"
)
EXPECTED_MASTER_SIZE = 26_498_477

REQUIRED_RAW = [
    EXPECTED_MASTER,
    "bhagavadgitawith00londiala_meta.xml",
    "bhagavadgitawith00londiala_files.xml",
    "bhagavadgitawith00londiala_djvu.txt",
    "bhagavadgitawith00londiala_page_numbers.json",
    "ia-metadata-api.json",
    "metadata.json",
    "README.md",
    "SHA256SUMS",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


class BesantDas1905AcquisitionTests(unittest.TestCase):
    def test_required_raw_artifacts_present(self) -> None:
        for name in REQUIRED_RAW:
            path = RAW / name
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_sha256sums_verifies(self) -> None:
        lines = (RAW / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(lines), len(REQUIRED_RAW) - 1)
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            digest, name = line.split(None, 1)
            path = RAW / name
            self.assertTrue(path.is_file(), name)
            self.assertEqual(sha256_file(path), digest, name)

    def test_master_identity(self) -> None:
        master = RAW / EXPECTED_MASTER
        self.assertEqual(master.stat().st_size, EXPECTED_MASTER_SIZE)
        self.assertEqual(sha256_file(master), EXPECTED_MASTER_SHA256)

    def test_metadata_not_approved(self) -> None:
        meta = json.loads((RAW / "metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["status"], "ACQUIRED_UNREVIEWED")
        self.assertEqual(meta["sourceRole"], "PRIMARY_TRANSLATION_CANDIDATE")
        self.assertEqual(meta["itemId"], "bhagavadgitawith00londiala")
        self.assertEqual(meta["translator"], "Annie Besant & Bhagavan Das")
        self.assertEqual(meta["editionTarget"]["year"], 1905)
        self.assertFalse(meta.get("ocrIsAuthoritative", True))


class BesantDas1905InspectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = json.loads(INSPECTION.read_text(encoding="utf-8"))

    def test_exactly_47_unique_canonical_references(self) -> None:
        refs = [v["canonicalReference"] for v in self.doc["verses"]]
        self.assertEqual(len(refs), 47)
        self.assertEqual(len(set(refs)), 47)
        self.assertEqual(refs, [f"1.{i}" for i in range(1, 48)])
        self.assertEqual(self.doc["observedLabels"], refs)
        self.assertEqual(self.doc["missingLabels"], [])
        self.assertEqual(self.doc["duplicateLabels"], [])

    def test_all_one_to_one_and_package_v1_compatible(self) -> None:
        self.assertEqual(self.doc["combinedLabels"], [])
        self.assertEqual(self.doc["multiVerseSegmentCount"], 0)
        self.assertEqual(self.doc["oneToOneSegmentCount"], 47)
        for verse in self.doc["verses"]:
            self.assertEqual(verse["segmentationType"], "ONE_TO_ONE")
            self.assertTrue(verse["fluentTranslationPresent"])
        self.assertTrue(self.doc["segmentationSummary"]["packageFormatV1Compatible"])
        self.assertTrue(self.doc["segmentationSummary"]["allOneToOne"])

    def test_chapter_2_boundary_recorded(self) -> None:
        mapping = self.doc["pageMapping"]
        self.assertEqual(mapping["chapter1PrintedPages"]["from"], 1)
        self.assertEqual(mapping["chapter1PrintedPages"]["to"], 22)
        self.assertEqual(mapping["chapter2BoundaryPrintedPage"], 23)
        self.assertEqual(mapping["chapter2BoundaryScanLeaf"], 69)

    def test_not_approved_normalized_or_importable(self) -> None:
        self.assertFalse(self.doc["approved"])
        self.assertFalse(self.doc["normalized"])
        self.assertFalse(self.doc["importReady"])
        self.assertFalse(self.doc["packageReady"])


class BesantDas1905RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.by_id = {s["id"]: s for s in cls.registry["sources"]}

    def test_besant_registry_entry(self) -> None:
        entry = self.by_id[BESANT_ID]
        self.assertEqual(entry["source_role"], "PRIMARY_TRANSLATION_CANDIDATE")
        self.assertEqual(entry["status"], "ACQUIRED_UNREVIEWED")
        self.assertEqual(entry["license_catalog_id"], "us-pd-pre-1931")
        self.assertEqual(entry["item_identifier"], "bhagavadgitawith00londiala")
        self.assertEqual(entry["sha256"], EXPECTED_MASTER_SHA256)
        self.assertEqual(entry["chapter_1_verse_count"], 47)
        self.assertTrue(entry["package_format_v1_compatible_chapter_01"])
        self.assertNotEqual(entry["status"], "APPROVED")
        self.assertNotIn(entry["status"], {"IMPORT_READY", "PUBLISHED"})

    def test_swarupananda_unchanged_role_and_status(self) -> None:
        entry = self.by_id[SWARUPANANDA_ID]
        self.assertEqual(entry["source_role"], "PRIMARY_TRANSLATION_CANDIDATE")
        self.assertEqual(entry["status"], "ACQUIRED_UNREVIEWED")
        self.assertEqual(
            entry["suitability_decision"], "NEEDS_MANUAL_SEGMENTATION_POLICY"
        )
        self.assertTrue(SWARUPANANDA_RAW.is_dir())
        self.assertTrue(
            (SWARUPANANDA_RAW / "2015.386852.Srimad-Bhagavad.pdf").is_file()
        )

    def test_raw_checksums_catalog_includes_master(self) -> None:
        text = CHECKSUMS.read_text(encoding="utf-8")
        needle = (
            f"{EXPECTED_MASTER_SHA256}  "
            f"content/raw/translations/besant-das-1905/{EXPECTED_MASTER}"
        )
        self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
