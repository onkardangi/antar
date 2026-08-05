"""Tests for Chapter 1 final conflict approval (1.20 / 1.22 only)."""

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

from approve_final_chapter01_conflicts import (  # noqa: E402
    ALLOWED_REFS,
    ApprovalError,
    prepare_context,
    run,
    sha256_file,
)
from validate_reviews import split_sections  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
WIKI = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _snapshot_pre_apply(tmp: Path) -> Path:
    """Copy repo subset into tmp and ensure 1.20/1.22 are UNDER_REVIEW / unapproved."""
    root = tmp / "repo"
    chapter = root / "content/editorial/bhagavad-gita/chapter-01"
    reviews = root / "content/editorial/reviews"
    registry = root / "content/registry"
    chapter.mkdir(parents=True)
    reviews.mkdir(parents=True)
    registry.mkdir(parents=True)

    for name in (
        "canonical-draft.jsonl",
        "chapter-01-approval-manifest.json",
        "source-comparison.jsonl",
        "source-conflict-analysis.jsonl",
        "normalization-match-approval-result.jsonl",
        "orthographic-resolution-result.jsonl",
        "final-conflict-resolution-candidates.jsonl",
        "third-reference-queue.json",
    ):
        src = CHAPTER_DIR / name
        if src.is_file():
            shutil.copy2(src, chapter / name)
    shutil.copy2(REPO_ROOT / "content/registry/sources.json", registry / "sources.json")
    for path in REVIEWS_DIR.glob("1.*.md"):
        shutil.copy2(path, reviews / path.name)

    # If already applied in live tree, rewind only 1.20/1.22 for tool tests.
    draft = _load_jsonl(chapter / "canonical-draft.jsonl")
    comps = {r["canonicalReference"]: r for r in _load_jsonl(chapter / "source-comparison.jsonl")}
    cands = _load_jsonl(chapter / "final-conflict-resolution-candidates.jsonl")
    changed = False
    for row in draft:
        if row["canonicalReference"] in ALLOWED_REFS and row.get("approvalStatus") == "APPROVED":
            row["approvalStatus"] = "UNREVIEWED"
            row["sanskritText"] = None
            for k in (
                "approvalDate",
                "decisionType",
                "editorialDecisionId",
                "editorialApprovalChecksum",
                "editorialNotes",
                "selectedSourceId",
                "selectedSourceChecksum",
                "approvedSourceIds",
                "reviewFileChecksum",
                "reviewerId",
                "sanskritTextChecksum",
                "classification",
                "priorClassification",
            ):
                row.pop(k, None)
            changed = True
    if changed:
        (chapter / "canonical-draft.jsonl").write_text(
            "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in draft) + "\n",
            encoding="utf-8",
        )
        for cand in cands:
            cand["approvalStatus"] = "PENDING"
        (chapter / "final-conflict-resolution-candidates.jsonl").write_text(
            "\n".join(json.dumps(c, ensure_ascii=False, sort_keys=True) for c in cands) + "\n",
            encoding="utf-8",
        )
        (chapter / "chapter-01-approval-manifest.json").write_text(
            json.dumps(
                {
                    "approved": 45,
                    "pending": 2,
                    "status": "PARTIALLY_APPROVED",
                    "importReady": False,
                    "unresolvedReferences": ["1.20", "1.22"],
                    "reviewer": "onkar-dangi",
                    "decisionDate": "2026-08-04",
                    "chapterNumber": 1,
                    "rejected": 0,
                    "normalizationMatchCandidates": 34,
                    "sourceConflicts": 13,
                    "secondReviewer": None,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        # Restore UNDER_REVIEW review stubs from candidates + comparison texts.
        for ref in ALLOWED_REFS:
            wiki = next(s for s in comps[ref]["sources"] if s["sourceId"] == WIKI)
            path = reviews / f"{ref}.md"
            text = path.read_text(encoding="utf-8")
            sections = split_sections(text)
            sections["Status"] = "UNDER_REVIEW\n"
            sections["Approval"] = "Reviewer:\n\nSecond Reviewer:\n\nDate:\n"
            # Keep existing comparison/decision proposal body; strip approval audit apply line if present.
            audit = sections.get("Audit Log", "")
            lines = [
                ln
                for ln in audit.splitlines()
                if "Final conflict resolution" not in ln
            ]
            sections["Audit Log"] = "\n".join(lines).rstrip() + "\n"
            sections["Decision"] = (
                "No editorial decision applied yet. Proposal recorded; status `UNDER_REVIEW`.\n"
            )
            order = [
                "Canonical Reference",
                "Status",
                "Sources",
                "Source Comparison",
                "Differences",
                "Editorial Notes",
                "Decision",
                "Approval",
                "Audit Log",
            ]
            parts = []
            for key in order:
                if key in sections:
                    parts.append(f"# {key}\n\n{sections[key].rstrip()}\n")
            path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
            # ensure proposed text still matches wiki
            assert any(
                c["canonicalReference"] == ref and c["proposedSanskritText"] == wiki["sanskritText"]
                for c in cands
            )
    return root


class FinalConflictApprovalTests(unittest.TestCase):
    def test_dry_run_zero_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _snapshot_pre_apply(Path(tmp))
            before = {
                str(p.relative_to(root)): p.read_bytes()
                for p in root.rglob("*")
                if p.is_file()
            }
            code = run(
                reviewer_id="onkar-dangi",
                reviewer_name="Onkar Dangi",
                decision_date="2026-08-04",
                apply=False,
                repo_root=root,
            )
            self.assertEqual(code, 0)
            after = {
                str(p.relative_to(root)): p.read_bytes()
                for p in root.rglob("*")
                if p.is_file()
            }
            self.assertEqual(before, after)

    def test_apply_approves_only_1_20_and_1_22(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _snapshot_pre_apply(Path(tmp))
            prior = {
                r["canonicalReference"]: r
                for r in _load_jsonl(
                    root / "content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl"
                )
                if r["canonicalReference"] not in ALLOWED_REFS
            }
            prior_bytes = {
                ref: (
                    root / "content/editorial/reviews" / f"{ref}.md"
                ).read_bytes()
                for ref in prior
            }
            code = run(
                reviewer_id="onkar-dangi",
                reviewer_name="Onkar Dangi",
                decision_date="2026-08-04",
                apply=True,
                repo_root=root,
            )
            self.assertEqual(code, 0)
            draft = _load_jsonl(
                root / "content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl"
            )
            approved = [r for r in draft if r["approvalStatus"] == "APPROVED"]
            self.assertEqual(len(approved), 47)
            comps = {
                r["canonicalReference"]: r
                for r in _load_jsonl(
                    root / "content/editorial/bhagavad-gita/chapter-01/source-comparison.jsonl"
                )
            }
            for ref in ALLOWED_REFS:
                row = next(r for r in draft if r["canonicalReference"] == ref)
                wiki = next(s for s in comps[ref]["sources"] if s["sourceId"] == WIKI)
                self.assertEqual(row["sanskritText"], wiki["sanskritText"])
                self.assertIsNone(row["transliteration"])
                self.assertEqual(row["selectedSourceId"], WIKI)
                self.assertEqual(len(row["approvedSourceIds"]), 3)
                self.assertEqual(row["decisionType"], "FINAL_CHAPTER01_CONFLICT_RESOLUTION")
            for ref, before in prior.items():
                after = next(r for r in draft if r["canonicalReference"] == ref)
                self.assertEqual(after, before)
                self.assertEqual(
                    (root / "content/editorial/reviews" / f"{ref}.md").read_bytes(),
                    prior_bytes[ref],
                )
            manifest = json.loads(
                (
                    root
                    / "content/editorial/bhagavad-gita/chapter-01/chapter-01-approval-manifest.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["approved"], 47)
            self.assertEqual(manifest["pending"], 0)
            self.assertEqual(manifest["status"], "APPROVED")
            self.assertTrue(manifest["importReady"])

    def test_refuses_without_human_accept_flag_on_1_22(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _snapshot_pre_apply(Path(tmp))
            path = (
                root
                / "content/editorial/bhagavad-gita/chapter-01/final-conflict-resolution-candidates.jsonl"
            )
            rows = _load_jsonl(path)
            for r in rows:
                if r["canonicalReference"] == "1.22":
                    r["notes"] = [
                        n
                        for n in r.get("notes") or []
                        if "humanAcceptsMinorityPrimaryReading=true" not in n
                    ]
            path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ApprovalError) as ctx:
                prepare_context(root)
            self.assertIn("1.22", str(ctx.exception))
            self.assertIn("unresolved substantive ambiguity", str(ctx.exception))

    def test_refuses_synthesized_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _snapshot_pre_apply(Path(tmp))
            path = (
                root
                / "content/editorial/bhagavad-gita/chapter-01/final-conflict-resolution-candidates.jsonl"
            )
            rows = _load_jsonl(path)
            for r in rows:
                if r["canonicalReference"] == "1.20":
                    r["proposedSanskritText"] = r["proposedSanskritText"] + " "
            path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ApprovalError) as ctx:
                prepare_context(root)
            self.assertIn("byte-identical", str(ctx.exception))

    def test_refuses_wrong_reviewer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _snapshot_pre_apply(Path(tmp))
            with self.assertRaises(ApprovalError):
                run(
                    reviewer_id="someone-else",
                    reviewer_name="Onkar Dangi",
                    decision_date="2026-08-04",
                    apply=False,
                    repo_root=root,
                )


if __name__ == "__main__":
    unittest.main()
