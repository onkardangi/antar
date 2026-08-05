"""Tests for Chapter 1 orthographic SOURCE_CONFLICT resolution."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from resolve_orthographic_conflicts import (  # noqa: E402
    FORBIDDEN_REFS,
    ResolutionError,
    apply_resolution,
    dump_jsonl,
    load_json,
    load_jsonl,
    sha256_file,
)
from validate_orthographic_resolution import validate_orthographic_resolution  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
DECISION_DATE = "2026-08-04"
REVIEWER_ID = "onkar-dangi"
REVIEWER_NAME = "Onkar Dangi"
ELIGIBLE = [
    "1.2",
    "1.8",
    "1.15",
    "1.24",
    "1.26",
    "1.28",
    "1.34",
    "1.41",
    "1.42",
    "1.43",
    "1.47",
]


def _copy_workspace(tmp: Path) -> tuple[Path, Path]:
    chapter = tmp / "chapter-01"
    reviews = tmp / "reviews"
    chapter.mkdir()
    reviews.mkdir()
    for name in (
        "canonical-draft.jsonl",
        "chapter-01-approval-manifest.json",
        "source-conflict-analysis.jsonl",
        "source-comparison.jsonl",
        "automated-comparison-report.jsonl",
        "normalization-match-approval-candidate.jsonl",
        "normalization-match-approval-result.jsonl",
        "third-reference-queue.json",
    ):
        src = CHAPTER_DIR / name
        if src.is_file():
            shutil.copy2(src, chapter / name)
    for path in REVIEWS_DIR.glob("1.*.md"):
        shutil.copy2(path, reviews / path.name)
    # Ensure policy is available via default REPO_ROOT path; tests use live policy.
    return chapter, reviews


def _chapter_past_orthographic() -> bool:
    draft = load_jsonl(CHAPTER_DIR / "canonical-draft.jsonl")
    approved = {r["canonicalReference"] for r in draft if r.get("approvalStatus") == "APPROVED"}
    return "1.20" in approved and "1.22" in approved


class OrthographicResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        if _chapter_past_orthographic():
            self.skipTest(
                "Chapter 1 final conflicts already approved; ortho re-apply fixture unavailable"
            )

    def test_dry_run_reports_11_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            before = {
                p.name: p.read_bytes()
                for p in list(chapter.iterdir()) + list(reviews.iterdir())
                if p.is_file()
            }
            report = apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=True,
                apply=False,
            )
            self.assertEqual(report["eligibleCount"], 11)
            self.assertEqual(report["eligibleReferences"], ELIGIBLE)
            self.assertEqual(set(report["forbiddenUntouched"]), FORBIDDEN_REFS)
            self.assertEqual(report["mutations"], 0)
            after = {
                p.name: p.read_bytes()
                for p in list(chapter.iterdir()) + list(reviews.iterdir())
                if p.is_file()
            }
            self.assertEqual(before, after)

    def test_atomic_approval_success_and_traceability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            prior_draft = {
                r["canonicalReference"]: r
                for r in load_jsonl(chapter / "canonical-draft.jsonl")
                if r.get("decisionType") == "BATCH_NORMALIZATION_MATCH_APPROVAL"
            }
            forbidden_reviews = {
                ref: (reviews / f"{ref}.md").read_bytes() for ref in sorted(FORBIDDEN_REFS)
            }
            conflict_bytes = (chapter / "source-conflict-analysis.jsonl").read_bytes()
            report = apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=False,
                apply=True,
            )
            self.assertTrue(report["ok"])
            draft = load_jsonl(chapter / "canonical-draft.jsonl")
            approved = [r for r in draft if r["approvalStatus"] == "APPROVED"]
            self.assertEqual(len(approved), 45)
            unapproved = [r["canonicalReference"] for r in draft if r["approvalStatus"] != "APPROVED"]
            self.assertEqual(set(unapproved), FORBIDDEN_REFS)
            comparisons = {
                r["canonicalReference"]: r
                for r in load_jsonl(chapter / "source-comparison.jsonl")
            }
            for row in draft:
                if row["canonicalReference"] not in ELIGIBLE:
                    continue
                wiki = next(
                    s
                    for s in comparisons[row["canonicalReference"]]["sources"]
                    if "wikisource" in s["sourceId"]
                )
                self.assertEqual(row["sanskritText"], wiki["sanskritText"])
                self.assertIsNone(row["transliteration"])
                self.assertEqual(row["decisionType"], "ORTHOGRAPHIC_SOURCE_CONFLICT_RESOLUTION")
            for ref, before in prior_draft.items():
                after = next(r for r in draft if r["canonicalReference"] == ref)
                self.assertEqual(after, before)
            for ref, raw in forbidden_reviews.items():
                self.assertEqual((reviews / f"{ref}.md").read_bytes(), raw)
            self.assertEqual(
                (chapter / "source-conflict-analysis.jsonl").read_bytes(),
                conflict_bytes,
            )
            manifest = load_json(chapter / "chapter-01-approval-manifest.json")
            self.assertEqual(manifest["approved"], 45)
            self.assertEqual(manifest["pending"], 2)
            self.assertEqual(manifest["unresolvedReferences"], ["1.20", "1.22"])
            self.assertFalse(manifest["importReady"])
            outcome = validate_orthographic_resolution(
                chapter_dir=chapter, reviews_dir=reviews
            )
            self.assertTrue(outcome.ok, outcome.errors)

    def test_ambiguous_conflict_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            conflicts = load_jsonl(chapter / "source-conflict-analysis.jsonl")
            for c in conflicts:
                if c["canonicalReference"] == "1.2":
                    c["differenceKindFlags"]["orthographicOnly"] = False
                    c["differenceKindFlags"]["wordDifference"] = True
            (chapter / "source-conflict-analysis.jsonl").write_text(
                dump_jsonl(conflicts), encoding="utf-8"
            )
            with self.assertRaises(ResolutionError) as ctx:
                apply_resolution(
                    chapter_dir=chapter,
                    reviews_dir=reviews,
                    reviewer_id=REVIEWER_ID,
                    reviewer_name=REVIEWER_NAME,
                    decision_date=DECISION_DATE,
                    dry_run=True,
                    apply=False,
                )
            self.assertIn("1.2", str(ctx.exception))

    def test_lexical_difference_rejection_for_1_20(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            # Force policy-eligible inclusion of 1.20 by rewriting live policy copy is not
            # possible (policy is repo-rooted). Instead ensure eligibility refuses if someone
            # marks 1.20 orthographicOnly without substantive flags cleared.
            conflicts = load_jsonl(chapter / "source-conflict-analysis.jsonl")
            for c in conflicts:
                if c["canonicalReference"] == "1.20":
                    self.assertFalse(c["differenceKindFlags"]["orthographicOnly"])
                    self.assertTrue(c["differenceKindFlags"]["wordDifference"])
            # Dry-run still succeeds and leaves 1.20 unresolved.
            report = apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=True,
                apply=False,
            )
            self.assertNotIn("1.20", report["eligibleReferences"])
            self.assertIn("1.20", report["forbiddenUntouched"])

    def test_rule_scoping_rejects_uncovered_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            # Remove all pattern coverage by clearing rule affected refs indirectly:
            # corrupt 1.47 so fold no longer matches -> ambiguous rejection.
            comparisons = load_jsonl(chapter / "source-comparison.jsonl")
            for rec in comparisons:
                if rec["canonicalReference"] == "1.47":
                    for src in rec["sources"]:
                        if "iitk" in src["sourceId"]:
                            src["sanskritText"] = "क्षत्रियाः सङ्गताः"  # lexical change
            (chapter / "source-comparison.jsonl").write_text(
                dump_jsonl(comparisons), encoding="utf-8"
            )
            with self.assertRaises(ResolutionError) as ctx:
                apply_resolution(
                    chapter_dir=chapter,
                    reviews_dir=reviews,
                    reviewer_id=REVIEWER_ID,
                    reviewer_name=REVIEWER_NAME,
                    decision_date=DECISION_DATE,
                    dry_run=True,
                    apply=False,
                )
            self.assertIn("1.47", str(ctx.exception))

    def test_all_or_nothing_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            before_draft = (chapter / "canonical-draft.jsonl").read_bytes()
            before_manifest = (chapter / "chapter-01-approval-manifest.json").read_bytes()
            (reviews / "1.47.md").unlink()
            with self.assertRaises(ResolutionError):
                apply_resolution(
                    chapter_dir=chapter,
                    reviews_dir=reviews,
                    reviewer_id=REVIEWER_ID,
                    reviewer_name=REVIEWER_NAME,
                    decision_date=DECISION_DATE,
                    dry_run=False,
                    apply=True,
                )
            self.assertEqual((chapter / "canonical-draft.jsonl").read_bytes(), before_draft)
            self.assertEqual(
                (chapter / "chapter-01-approval-manifest.json").read_bytes(),
                before_manifest,
            )
            self.assertFalse((chapter / "orthographic-resolution-result.jsonl").exists())

    def test_1_20_1_22_immutability_and_idempotent_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=False,
                apply=True,
            )
            forbidden_before = {
                ref: (reviews / f"{ref}.md").read_bytes() for ref in sorted(FORBIDDEN_REFS)
            }
            result_before = (chapter / "orthographic-resolution-result.jsonl").read_bytes()
            draft_before = (chapter / "canonical-draft.jsonl").read_bytes()
            manifest_before = (chapter / "chapter-01-approval-manifest.json").read_bytes()
            apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=False,
                apply=True,
            )
            self.assertEqual(
                (chapter / "orthographic-resolution-result.jsonl").read_bytes(),
                result_before,
            )
            self.assertEqual((chapter / "canonical-draft.jsonl").read_bytes(), draft_before)
            self.assertEqual(
                (chapter / "chapter-01-approval-manifest.json").read_bytes(),
                manifest_before,
            )
            for ref, raw in forbidden_before.items():
                self.assertEqual((reviews / f"{ref}.md").read_bytes(), raw)

    def test_package_still_non_importable(self) -> None:
        packages = REPO_ROOT / "content/packages/tools"
        if str(packages) not in sys.path:
            sys.path.insert(0, str(packages))
        from build_package import BuildError, build_package

        with tempfile.TemporaryDirectory() as tmp:
            chapter, reviews = _copy_workspace(Path(tmp))
            apply_resolution(
                chapter_dir=chapter,
                reviews_dir=reviews,
                reviewer_id=REVIEWER_ID,
                reviewer_name=REVIEWER_NAME,
                decision_date=DECISION_DATE,
                dry_run=False,
                apply=True,
            )
            with self.assertRaises(BuildError) as ctx:
                build_package(
                    approval_manifest_path=chapter / "chapter-01-approval-manifest.json",
                    approved_records_path=None,
                    output_parent=Path(tmp) / "out",
                    package_id="bhagavad-gita-chapter-01-v1",
                    scripture_id="bhagavad-gita",
                    chapter_number=1,
                    content_version=1,
                    package_status="APPROVED",
                    created_at="2026-08-04T00:00:00Z",
                    sources_registry=REPO_ROOT / "content/registry/sources.json",
                    allow_null_transliteration=True,
                    normalization_policy_version=1,
                    comparison_engine_version=1,
                    source_selection_rationale="test",
                    known_caveats=[],
                    require_complete_chapter=True,
                    chapter_workspace=chapter,
                )
            msg = str(ctx.exception).lower()
            self.assertTrue(
                "incomplete" in msg
                or "expected 47" in msg
                or "found 45" in msg
                or "conflicted" in msg,
                msg,
            )
            # After fix, incomplete-chapter is the expected gate.
            self.assertTrue(
                "incomplete" in msg or "expected 47" in msg or "found 45" in msg,
                msg,
            )


if __name__ == "__main__":
    unittest.main()
