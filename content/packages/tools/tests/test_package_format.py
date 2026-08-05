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

    def test_chapter1_package_gate(self) -> None:
        manifest = load_json(CHAPTER01 / "chapter-01-approval-manifest.json")
        self.assertIn(
            manifest.get("status"),
            {"PENDING_EDITORIAL_REVIEW", "PARTIALLY_APPROVED", "APPROVED"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            if manifest.get("status") != "APPROVED" or manifest.get("importReady") is not True:
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
                self.assertTrue(
                    "no approved" in msg
                    or "approved=0" in msg
                    or "incomplete" in msg
                    or "expected 47" in msg
                    or "found 34" in msg
                    or "found 45" in msg,
                    msg,
                )
                self.assertFalse((Path(tmp) / "bhagavad-gita-chapter-01-v1").exists())
            else:
                self.assertEqual(manifest.get("approved"), 47)
                self.assertEqual(manifest.get("pending"), 0)
                path = build_package(
                    approval_manifest_path=CHAPTER01 / "chapter-01-approval-manifest.json",
                    approved_records_path=CHAPTER01 / "canonical-draft.jsonl",
                    output_parent=Path(tmp),
                    package_id="bhagavad-gita-chapter-01-v1-test",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="APPROVED",
                    created_at=CREATED_AT,
                    sources_registry=SOURCES,
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale=(
                        "Wikisource PRIMARY_TRANSCRIPTION exact copy for all 47 "
                        "Chapter 1 Verses; IIT Kanpur is SECONDARY_VERIFICATION and "
                        "Sanskrit Documents is third-witness SUPPORTING_REFERENCE. "
                        "Transliteration remains null. No synthesis."
                    ),
                    known_caveats=[
                        "Verse 1.22: Wikisource minority reading retained for edition coherence.",
                        "IIT Kanpur and Sanskrit Documents are verification-only.",
                    ],
                    require_complete_chapter=True,
                )
                result = validate_package(path, sources_registry=SOURCES)
                self.assertTrue(result.structurally_valid, result.errors)
                self.assertTrue(result.editorially_valid, result.errors)
                self.assertTrue(result.importable, result.errors)
                self.assertEqual(result.warnings, [])
                self.assertEqual(load_json(path / "manifest.json")["recordCount"], 47)


class ProductionPackageTests(unittest.TestCase):
    """Gate the first production Chapter 1 package when present."""

    PRODUCTION = REPO_ROOT / "content/packages/bhagavad-gita-chapter-01-v1"

    def test_production_package_importable_without_warnings(self) -> None:
        if not self.PRODUCTION.is_dir():
            self.skipTest("production package not built yet")
        result = validate_package(self.PRODUCTION, sources_registry=SOURCES)
        self.assertTrue(result.structurally_valid, result.errors)
        self.assertTrue(result.editorially_valid, result.errors)
        self.assertTrue(result.importable, result.errors)
        self.assertEqual(result.warnings, [])
        self.assertEqual(result.errors, [])
        manifest = load_json(self.PRODUCTION / "manifest.json")
        self.assertEqual(manifest["packageId"], "bhagavad-gita-chapter-01-v1")
        self.assertEqual(manifest["packageStatus"], "APPROVED")
        self.assertEqual(manifest["chapterNumber"], 1)
        self.assertEqual(manifest["contentVersion"], 1)
        self.assertEqual(manifest["recordCount"], 47)
        self.assertEqual(
            manifest["canonicalReferenceRange"],
            {"from": "1.1", "to": "1.47", "expectedCount": 47},
        )
        verses = [
            json.loads(line)
            for line in (self.PRODUCTION / "verses.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        self.assertEqual(len(verses), 47)
        self.assertTrue(all(v.get("transliteration") is None for v in verses))
        draft = [
            json.loads(line)
            for line in (CHAPTER01 / "canonical-draft.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        by_ref = {r["canonicalReference"]: r for r in draft}
        for verse in verses:
            draft_row = by_ref[verse["canonicalReference"]]
            self.assertEqual(verse["sanskritText"], draft_row["sanskritText"])
            self.assertEqual(
                verse["editorialApprovalChecksum"],
                draft_row["editorialApprovalChecksum"],
            )
            self.assertEqual(
                verse["editorialDecisionId"],
                draft_row["editorialDecisionId"],
            )

    def test_production_package_layout_exactly_four_files(self) -> None:
        if not self.PRODUCTION.is_dir():
            self.skipTest("production package not built yet")
        names = sorted(p.name for p in self.PRODUCTION.iterdir() if p.is_file())
        self.assertEqual(
            names,
            ["SHA256SUMS", "manifest.json", "provenance.json", "verses.jsonl"],
        )

    def test_production_rebuild_is_byte_identical(self) -> None:
        if not self.PRODUCTION.is_dir():
            self.skipTest("production package not built yet")
        prod_manifest = load_json(self.PRODUCTION / "manifest.json")
        prod_prov = load_json(self.PRODUCTION / "provenance.json")
        with tempfile.TemporaryDirectory() as tmp:
            rebuilt = build_package(
                approval_manifest_path=CHAPTER01 / "chapter-01-approval-manifest.json",
                approved_records_path=CHAPTER01 / "canonical-draft.jsonl",
                output_parent=Path(tmp),
                package_id="bhagavad-gita-chapter-01-v1",
                scripture_id="bhagavad-gita",
                chapter_number=1,
                content_version=1,
                package_status="APPROVED",
                created_at=prod_manifest["createdAt"],
                sources_registry=SOURCES,
                allow_null_transliteration=True,
                normalization_policy_version=prod_prov["normalizationPolicyVersion"],
                comparison_engine_version=prod_prov["comparisonEngineVersion"],
                source_selection_rationale=prod_prov["sourceSelectionRationale"],
                known_caveats=list(prod_prov["knownCaveats"]),
                require_complete_chapter=True,
            )
            for name in ("manifest.json", "verses.jsonl", "provenance.json", "SHA256SUMS"):
                self.assertEqual(
                    (self.PRODUCTION / name).read_bytes(),
                    (rebuilt / name).read_bytes(),
                    msg=name,
                )
            self.assertEqual(
                load_json(rebuilt / "manifest.json")["packageChecksum"],
                prod_manifest["packageChecksum"],
            )


class Chapter1WorkspaceGuardTests(unittest.TestCase):
    def test_conflicts_and_candidates_remain_pending_in_prep_artifacts(self) -> None:
        candidates = [
            json.loads(l)
            for l in (
                CHAPTER01 / "normalization-match-approval-candidate.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        conflicts = [
            json.loads(l)
            for l in (
                CHAPTER01 / "source-conflict-analysis.jsonl"
            ).read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        self.assertTrue(all(r.get("approvalStatus") == "PENDING" for r in candidates))
        self.assertTrue(all(r.get("approvalStatus") == "PENDING" for r in conflicts))

    def test_draft_approval_is_partial_or_empty(self) -> None:
        draft = [
            json.loads(l)
            for l in (CHAPTER01 / "canonical-draft.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        approved = [r for r in draft if r.get("approvalStatus") == "APPROVED"]
        self.assertIn(len(approved), {0, 34, 45, 47})
        if approved:
            self.assertTrue(all(r.get("transliteration") is None for r in approved))
            if len(approved) == 47:
                self.assertTrue(all(r.get("approvalStatus") == "APPROVED" for r in draft))
            elif len(approved) == 45:
                unresolved = {
                    r["canonicalReference"]
                    for r in draft
                    if r.get("approvalStatus") != "APPROVED"
                }
                self.assertEqual(unresolved, {"1.20", "1.22"})
            elif len(approved) == 34:
                conflict_refs = {
                    json.loads(l)["canonicalReference"]
                    for l in (
                        CHAPTER01 / "source-conflict-analysis.jsonl"
                    ).read_text(encoding="utf-8").splitlines()
                    if l.strip()
                }
                self.assertTrue(
                    all(r["canonicalReference"] not in conflict_refs for r in approved)
                )

if __name__ == "__main__":
    unittest.main()
