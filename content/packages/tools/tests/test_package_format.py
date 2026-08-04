#!/usr/bin/env python3
"""Tests for Antar Content Package v1 format, builder, and validator."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_package import BuildError, build_package  # noqa: E402
from validate_package import (  # noqa: E402
    dump_json,
    load_json,
    sha256_file,
    validate_package,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
EXAMPLE = REPO_ROOT / "content/packages/examples/bhagavad-gita-chapter-01-v1-example"
CHAPTER01 = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
SOURCES = REPO_ROOT / "content/registry/sources.json"
CREATED_AT = "2026-08-04T00:00:00Z"


def _copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


class SyntheticPackageTests(unittest.TestCase):
    def test_valid_synthetic_draft_example(self) -> None:
        result = validate_package(EXAMPLE, sources_registry=SOURCES)
        self.assertTrue(result.structurally_valid, result.errors)
        self.assertFalse(result.importable)
        manifest = load_json(EXAMPLE / "manifest.json")
        self.assertEqual(manifest["packageStatus"], "DRAFT")
        self.assertEqual(manifest["packageId"], EXAMPLE.name)

    def test_valid_synthetic_approved_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            path = build_package(
                approval_manifest_path=FIXTURES / "approval-manifest-approved.json",
                approved_records_path=FIXTURES / "approved-records.jsonl",
                output_parent=out,
                package_id="fixture-scripture-chapter-01-v1",
                scripture_id="bhagavad-gita",
                chapter_number=1,
                content_version=1,
                package_status="APPROVED",
                created_at=CREATED_AT,
                sources_registry=SOURCES,
                allow_null_transliteration=True,
                normalization_policy_version=1,
                comparison_engine_version=1,
                source_selection_rationale="Synthetic APPROVED fixture.",
                known_caveats=["fixture only"],
                require_complete_chapter=False,
            )
            result = validate_package(path, sources_registry=SOURCES)
            self.assertTrue(result.structurally_valid, result.errors)
            self.assertTrue(result.editorially_valid, result.errors)
            self.assertTrue(result.importable, result.errors)
            self.assertEqual(load_json(path / "manifest.json")["packageStatus"], "APPROVED")


class ValidatorNegativeTests(unittest.TestCase):
    def _stage_example(self) -> Path:
        tmp = Path(tempfile.mkdtemp())
        dest = tmp / EXAMPLE.name
        _copy_tree(EXAMPLE, dest)
        self.addCleanup(shutil.rmtree, tmp, True)
        return dest

    def test_missing_file(self) -> None:
        pkg = self._stage_example()
        (pkg / "provenance.json").unlink()
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertFalse(result.importable)
        self.assertTrue(any("missing required file: provenance.json" in e for e in result.errors))

    def test_unexpected_file(self) -> None:
        pkg = self._stage_example()
        (pkg / "NOTES.md").write_text("nope\n", encoding="utf-8")
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertTrue(any("unexpected file: NOTES.md" in e for e in result.errors))

    def test_checksum_mismatch(self) -> None:
        pkg = self._stage_example()
        verses = pkg / "verses.jsonl"
        verses.write_text(verses.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertTrue(any("checksum mismatch" in e for e in result.errors))

    def test_duplicate_verse(self) -> None:
        pkg = self._stage_example()
        lines = [l for l in (pkg / "verses.jsonl").read_text(encoding="utf-8").splitlines() if l]
        row = json.loads(lines[0])
        lines.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
        (pkg / "verses.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        # Refresh checksums so we exercise duplicate detection, not checksum short-circuit
        self._rewrite_checksums(pkg)
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertTrue(any("duplicate Verse" in e for e in result.errors))

    def test_missing_verse(self) -> None:
        pkg = self._stage_example()
        lines = [l for l in (pkg / "verses.jsonl").read_text(encoding="utf-8").splitlines() if l]
        # Keep only verse 1 → range still says 1.1..1.2 / count 2 after rewrite
        (pkg / "verses.jsonl").write_text(lines[0] + "\n", encoding="utf-8")
        manifest = load_json(pkg / "manifest.json")
        manifest["recordCount"] = 1
        manifest["canonicalReferenceRange"] = {
            "from": "1.1",
            "to": "1.1",
            "expectedCount": 1,
        }
        # Leave provenance/packageChecksum to be refreshed
        verses_bytes = (pkg / "verses.jsonl").read_bytes()
        provenance_bytes = (pkg / "provenance.json").read_bytes()
        from validate_package import combined_package_checksum, format_sha256sums, sha256_bytes

        manifest["fileChecksums"] = {
            "verses.jsonl": sha256_bytes(verses_bytes),
            "provenance.json": sha256_bytes(provenance_bytes),
        }
        manifest["packageChecksum"] = combined_package_checksum(verses_bytes, provenance_bytes)
        (pkg / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
        (pkg / "SHA256SUMS").write_text(
            format_sha256sums(
                {
                    "manifest.json": sha256_file(pkg / "manifest.json"),
                    "verses.jsonl": sha256_bytes(verses_bytes),
                    "provenance.json": sha256_bytes(provenance_bytes),
                }
            ),
            encoding="utf-8",
        )
        # Structural completeness for a 1-verse DRAFT is OK; use gap inside range instead
        # Rebuild as 1.1 and 1.3 missing 1.2
        row1 = json.loads(lines[0])
        row3 = json.loads(lines[1])
        row3["verseNumber"] = 3
        row3["canonicalReference"] = "1.3"
        payload = (
            json.dumps(row1, ensure_ascii=False, sort_keys=True)
            + "\n"
            + json.dumps(row3, ensure_ascii=False, sort_keys=True)
            + "\n"
        )
        (pkg / "verses.jsonl").write_text(payload, encoding="utf-8")
        manifest = load_json(pkg / "manifest.json")
        manifest["recordCount"] = 2
        manifest["canonicalReferenceRange"] = {
            "from": "1.1",
            "to": "1.3",
            "expectedCount": 2,
        }
        verses_bytes = (pkg / "verses.jsonl").read_bytes()
        provenance_bytes = (pkg / "provenance.json").read_bytes()
        manifest["fileChecksums"] = {
            "verses.jsonl": sha256_bytes(verses_bytes),
            "provenance.json": sha256_bytes(provenance_bytes),
        }
        manifest["packageChecksum"] = combined_package_checksum(verses_bytes, provenance_bytes)
        (pkg / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
        (pkg / "SHA256SUMS").write_text(
            format_sha256sums(
                {
                    "manifest.json": sha256_file(pkg / "manifest.json"),
                    "verses.jsonl": sha256_bytes(verses_bytes),
                    "provenance.json": sha256_bytes(provenance_bytes),
                }
            ),
            encoding="utf-8",
        )
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertTrue(any("not contiguous" in e for e in result.errors))

    def test_bad_canonical_reference(self) -> None:
        pkg = self._stage_example()
        lines = [l for l in (pkg / "verses.jsonl").read_text(encoding="utf-8").splitlines() if l]
        row = json.loads(lines[0])
        row["canonicalReference"] = "9.9"
        lines[0] = json.dumps(row, ensure_ascii=False, sort_keys=True)
        (pkg / "verses.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        self._rewrite_checksums(pkg)
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.structurally_valid)
        self.assertTrue(any("canonicalReference" in e for e in result.errors))

    def test_unresolved_source_id(self) -> None:
        pkg = self._stage_example()
        lines = [l for l in (pkg / "verses.jsonl").read_text(encoding="utf-8").splitlines() if l]
        row = json.loads(lines[0])
        row["sourceIds"] = ["does-not-exist-in-registry"]
        row["sourceChecksums"] = {
            "does-not-exist-in-registry": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        }
        lines[0] = json.dumps(row, ensure_ascii=False, sort_keys=True)
        (pkg / "verses.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        provenance = load_json(pkg / "provenance.json")
        provenance["sourceIds"] = ["does-not-exist-in-registry"]
        provenance["sourceRoles"] = {"does-not-exist-in-registry": "FIXTURE"}
        provenance["sourceChecksums"] = row["sourceChecksums"]
        provenance["licenses"] = {
            "does-not-exist-in-registry": {
                "licenseDisplayed": "none",
                "licenseCatalogId": None,
            }
        }
        (pkg / "provenance.json").write_text(dump_json(provenance), encoding="utf-8")
        manifest = load_json(pkg / "manifest.json")
        manifest["sourceRegistryReferences"] = ["does-not-exist-in-registry"]
        (pkg / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
        self._rewrite_checksums(pkg)
        result = validate_package(pkg, sources_registry=SOURCES)
        self.assertFalse(result.importable)
        self.assertTrue(any("unresolved source ID" in e for e in result.errors))

    def _rewrite_checksums(self, pkg: Path) -> None:
        from validate_package import combined_package_checksum, format_sha256sums, sha256_bytes

        manifest = load_json(pkg / "manifest.json")
        verses_bytes = (pkg / "verses.jsonl").read_bytes()
        provenance_bytes = (pkg / "provenance.json").read_bytes()
        manifest["fileChecksums"] = {
            "verses.jsonl": sha256_bytes(verses_bytes),
            "provenance.json": sha256_bytes(provenance_bytes),
        }
        manifest["packageChecksum"] = combined_package_checksum(verses_bytes, provenance_bytes)
        # Keep recordCount aligned with file for non-count tests
        n = sum(1 for l in verses_bytes.decode("utf-8").splitlines() if l.strip())
        manifest["recordCount"] = n
        (pkg / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
        (pkg / "SHA256SUMS").write_text(
            format_sha256sums(
                {
                    "manifest.json": sha256_file(pkg / "manifest.json"),
                    "verses.jsonl": sha256_bytes(verses_bytes),
                    "provenance.json": sha256_bytes(provenance_bytes),
                }
            ),
            encoding="utf-8",
        )


class BuilderRejectionTests(unittest.TestCase):
    def test_pending_editorial_record_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(BuildError) as ctx:
                build_package(
                    approval_manifest_path=FIXTURES / "approval-manifest-draft.json",
                    approved_records_path=FIXTURES / "pending-record.jsonl",
                    output_parent=Path(tmp),
                    package_id="should-not-exist",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="DRAFT",
                    created_at=CREATED_AT,
                    sources_registry=SOURCES,
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale="n/a",
                    known_caveats=[],
                    require_complete_chapter=False,
                )
            self.assertIn("pending", str(ctx.exception).lower())

    def test_conflicted_record_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(BuildError) as ctx:
                build_package(
                    approval_manifest_path=FIXTURES / "approval-manifest-draft.json",
                    approved_records_path=FIXTURES / "conflicted-record.jsonl",
                    output_parent=Path(tmp),
                    package_id="should-not-exist",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="DRAFT",
                    created_at=CREATED_AT,
                    sources_registry=SOURCES,
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale="n/a",
                    known_caveats=[],
                    require_complete_chapter=False,
                )
            self.assertIn("conflict", str(ctx.exception).lower())

    def test_missing_reviewer_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # Manifest without reviewer + records without reviewerId
            manifest = load_json(FIXTURES / "approval-manifest-approved.json")
            manifest["reviewer"] = None
            manifest["secondReviewer"] = None
            manifest["approved"] = 1
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(dump_json(manifest), encoding="utf-8")
            with self.assertRaises(BuildError) as ctx:
                build_package(
                    approval_manifest_path=manifest_path,
                    approved_records_path=FIXTURES / "approved-missing-reviewer.jsonl",
                    output_parent=Path(tmp) / "out",
                    package_id="should-not-exist",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="DRAFT",
                    created_at=CREATED_AT,
                    sources_registry=SOURCES,
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale="n/a",
                    known_caveats=[],
                    require_complete_chapter=False,
                )
            self.assertIn("missing reviewer", str(ctx.exception).lower())

    def test_refuse_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            kwargs = dict(
                approval_manifest_path=FIXTURES / "approval-manifest-approved.json",
                approved_records_path=FIXTURES / "approved-records.jsonl",
                output_parent=out,
                package_id="fixture-overwrite-v1",
                scripture_id="bhagavad-gita",
                chapter_number=1,
                content_version=1,
                package_status="DRAFT",
                created_at=CREATED_AT,
                sources_registry=SOURCES,
                allow_null_transliteration=True,
                normalization_policy_version=1,
                comparison_engine_version=1,
                source_selection_rationale="fixture",
                known_caveats=[],
                require_complete_chapter=False,
            )
            build_package(**kwargs)
            with self.assertRaises(BuildError) as ctx:
                build_package(**kwargs)
            self.assertIn("overwrite", str(ctx.exception).lower())

    def test_deterministic_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out1 = Path(tmp) / "a"
            out2 = Path(tmp) / "b"
            kwargs = dict(
                approval_manifest_path=FIXTURES / "approval-manifest-approved.json",
                approved_records_path=FIXTURES / "approved-records.jsonl",
                scripture_id="bhagavad-gita",
                chapter_number=1,
                content_version=1,
                package_status="DRAFT",
                created_at=CREATED_AT,
                sources_registry=SOURCES,
                allow_null_transliteration=True,
                normalization_policy_version=1,
                comparison_engine_version=1,
                source_selection_rationale="fixture determinism",
                known_caveats=["same caveats"],
                require_complete_chapter=False,
            )
            p1 = build_package(output_parent=out1, package_id="fixture-det-v1", **kwargs)
            p2 = build_package(output_parent=out2, package_id="fixture-det-v1", **kwargs)
            for name in ("manifest.json", "verses.jsonl", "provenance.json", "SHA256SUMS"):
                self.assertEqual(
                    (p1 / name).read_bytes(),
                    (p2 / name).read_bytes(),
                    msg=name,
                )
            self.assertEqual(sha256_file(p1 / "SHA256SUMS"), sha256_file(p2 / "SHA256SUMS"))

    def test_chapter1_cannot_produce_approved_package(self) -> None:
        manifest = load_json(CHAPTER01 / "chapter-01-approval-manifest.json")
        self.assertEqual(manifest.get("approved"), 0)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(BuildError) as ctx:
                build_package(
                    approval_manifest_path=CHAPTER01 / "chapter-01-approval-manifest.json",
                    approved_records_path=None,
                    output_parent=Path(tmp),
                    package_id="bhagavad-gita-chapter-01-v1",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="APPROVED",
                    created_at=CREATED_AT,
                    sources_registry=SOURCES,
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale="n/a",
                    known_caveats=[],
                    require_complete_chapter=True,
                    chapter_workspace=CHAPTER01,
                )
            msg = str(ctx.exception).lower()
            self.assertTrue("no approved" in msg or "approved=0" in msg)
            self.assertFalse((Path(tmp) / "bhagavad-gita-chapter-01-v1").exists())


class Chapter1WorkspaceGuardTests(unittest.TestCase):
    def test_no_verse_approved_in_workspace(self) -> None:
        draft = [
            json.loads(l)
            for l in (CHAPTER01 / "canonical-draft.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        self.assertTrue(draft)
        self.assertTrue(all(r.get("approvalStatus") != "APPROVED" for r in draft))
        candidates = [
            json.loads(l)
            for l in (
                CHAPTER01 / "normalization-match-approval-candidate.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        self.assertTrue(all(r.get("approvalStatus") != "APPROVED" for r in candidates))


if __name__ == "__main__":
    unittest.main()
