#!/usr/bin/env python3
"""Validate Chapter 1 after NORMALIZATION_MATCH batch approval."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_reviews import validate_review_text  # noqa: E402

CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
DECISION_TYPE = "BATCH_NORMALIZATION_MATCH_APPROVAL"


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.info: dict[str, Any] = {}

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_normalization_match_approval(
    *,
    chapter_dir: Path = CHAPTER_DIR,
    reviews_dir: Path = REVIEWS_DIR,
) -> Result:
    result = Result()
    cand_path = chapter_dir / "normalization-match-approval-candidate.jsonl"
    conf_path = chapter_dir / "source-conflict-analysis.jsonl"
    draft_path = chapter_dir / "canonical-draft.jsonl"
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"
    result_path = chapter_dir / "normalization-match-approval-result.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    report_path = chapter_dir / "automated-comparison-report.jsonl"

    for path in (
        cand_path,
        conf_path,
        draft_path,
        manifest_path,
        result_path,
        comparison_path,
        report_path,
    ):
        if not path.is_file():
            result.errors.append(f"missing {path}")
            return result

    candidates = load_jsonl(cand_path)
    conflicts = load_jsonl(conf_path)
    draft = load_jsonl(draft_path)
    results = load_jsonl(result_path)
    comparisons = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)}
    reports = {r["canonicalReference"]: r for r in load_jsonl(report_path)}
    manifest = load_json(manifest_path)

    cand_refs = [c["canonicalReference"] for c in candidates]
    conf_refs = [c["canonicalReference"] for c in conflicts]
    if len(candidates) != 34:
        result.errors.append(f"expected 34 candidates, found {len(candidates)}")
    if len(conflicts) != 13:
        result.errors.append(f"expected 13 conflicts, found {len(conflicts)}")
    approved = [r for r in draft if r.get("approvalStatus") == "APPROVED"]
    prior = [
        r
        for r in approved
        if r.get("decisionType") == "BATCH_NORMALIZATION_MATCH_APPROVAL"
    ]
    # Original batch gate: the 34 NORMALIZATION_MATCH approvals remain present.
    # Later orthographic resolutions may raise total APPROVED above 34.
    if len(prior) != 34:
        result.errors.append(
            f"expected 34 BATCH_NORMALIZATION_MATCH_APPROVAL rows, found {len(prior)}"
        )
    unapproved_or_other = [r for r in draft if r.get("approvalStatus") != "APPROVED"]
    # Allow post-orthographic (45/2) and post-final-conflict (47/0) Chapter states.
    if len(approved) not in {34, 45, 47}:
        result.errors.append(f"expected 34, 45, or 47 APPROVED draft rows, found {len(approved)}")
    if len(approved) == 34 and len(unapproved_or_other) != 13:
        result.errors.append(f"expected 13 unapproved draft rows, found {len(unapproved_or_other)}")
    if len(approved) == 45 and len(unapproved_or_other) != 2:
        result.errors.append(f"expected 2 unapproved draft rows after ortho resolve, found {len(unapproved_or_other)}")
    if len(approved) == 47 and len(unapproved_or_other) != 0:
        result.errors.append(f"expected 0 unapproved draft rows after final conflicts, found {len(unapproved_or_other)}")
    cand_set = set(cand_refs)
    prior_refs = {r["canonicalReference"] for r in prior}
    if prior_refs != cand_set:
        result.errors.append("prior NORMALIZATION_MATCH approvals must equal candidate set")
    if len(approved) == 34:
        if set(cand_refs) != {r["canonicalReference"] for r in approved}:
            result.errors.append("approved draft refs must equal NORMALIZATION_MATCH candidate set")
        if set(conf_refs) != {r["canonicalReference"] for r in unapproved_or_other}:
            result.errors.append("unapproved draft refs must equal SOURCE_CONFLICT set")
    if len(approved) == 45:
        if {r["canonicalReference"] for r in unapproved_or_other} != {"1.20", "1.22"}:
            result.errors.append("after orthographic resolution only 1.20/1.22 may remain unapproved")
    if len(approved) == 47:
        final_ids = {
            r.get("decisionType")
            for r in draft
            if r.get("canonicalReference") in {"1.20", "1.22"}
        }
        if final_ids != {"FINAL_CHAPTER01_CONFLICT_RESOLUTION"}:
            result.errors.append("1.20/1.22 must use FINAL_CHAPTER01_CONFLICT_RESOLUTION after full approval")
    if set(cand_refs) & set(conf_refs):
        result.errors.append("candidate/conflict overlap")
    if set(cand_refs) | set(conf_refs) != {f"1.{i}" for i in range(1, 48)}:
        result.errors.append("47-reference partition incomplete")

    for row in prior:
        ref = row["canonicalReference"]
        if reports.get(ref, {}).get("classification") != "NORMALIZATION_MATCH":
            result.errors.append(f"{ref}: approved but not NORMALIZATION_MATCH in report")
        if reports.get(ref, {}).get("classification") == "SOURCE_CONFLICT":
            result.errors.append(f"{ref}: SOURCE_CONFLICT must not be approved via norm-match path")
        if row.get("transliteration") is not None:
            result.errors.append(f"{ref}: transliteration must be null")
        cand = next(c for c in candidates if c["canonicalReference"] == ref)
        wiki = next(
            s
            for s in comparisons[ref]["sources"]
            if s.get("sourceId") == WIKISOURCE_ID
        )
        if row.get("sanskritText") != cand.get("proposedSanskritText"):
            result.errors.append(f"{ref}: draft Sanskrit != candidate proposed text")
        if row.get("sanskritText") != wiki.get("sanskritText"):
            result.errors.append(f"{ref}: draft Sanskrit not byte-identical to Wikisource")
        if WIKISOURCE_ID not in (row.get("approvedSourceIds") or []):
            result.errors.append(f"{ref}: missing Wikisource in approvedSourceIds")
        iitk_ids = [s for s in (row.get("approvedSourceIds") or []) if "iitk" in s]
        if not iitk_ids:
            result.errors.append(f"{ref}: missing IIT verification source id")
        if row.get("decisionType") != DECISION_TYPE:
            result.errors.append(f"{ref}: unexpected decisionType")
        if not row.get("editorialDecisionId"):
            result.errors.append(f"{ref}: missing editorialDecisionId")
        if not row.get("editorialApprovalChecksum"):
            result.errors.append(f"{ref}: missing editorialApprovalChecksum")

        review_path = reviews_dir / f"{ref}.md"
        if not review_path.is_file():
            result.errors.append(f"missing review {ref}.md")
        else:
            text = review_path.read_text(encoding="utf-8")
            errs = validate_review_text(text, expected_ref=ref, path_label=str(review_path))
            result.errors.extend(errs)
            status_block = text.split("# Status", 1)[-1].split("#", 1)[0]
            if "APPROVED" not in status_block.split():
                result.errors.append(f"{ref}: review status must be APPROVED")

    for row in unapproved_or_other:
        ref = row["canonicalReference"]
        if reports.get(ref, {}).get("classification") != "SOURCE_CONFLICT":
            result.errors.append(f"{ref}: unapproved must be SOURCE_CONFLICT")
        if row.get("approvalStatus") == "APPROVED":
            result.errors.append(f"{ref}: conflict must not be APPROVED")
        if row.get("sanskritText") is not None:
            result.errors.append(f"{ref}: conflict Sanskrit must remain null")
        review_path = reviews_dir / f"{ref}.md"
        if review_path.is_file():
            text = review_path.read_text(encoding="utf-8")
            status_block = text.split("# Status", 1)[-1].split("#", 1)[0]
            if "APPROVED" in status_block.split():
                result.errors.append(f"{ref}: conflict review must not be APPROVED")

    if any(c.get("approvalStatus") == "APPROVED" for c in conflicts):
        result.errors.append("conflict analysis rows must remain unapproved")

    if manifest.get("status") not in {"PARTIALLY_APPROVED", "APPROVED"}:
        result.errors.append("manifest status must be PARTIALLY_APPROVED or APPROVED")
    if manifest.get("approved") not in {34, 45, 47}:
        result.errors.append("manifest approved must be 34, 45, or 47")
    if manifest.get("pending") not in {13, 2, 0}:
        result.errors.append("manifest pending must be 13, 2, or 0")
    if manifest.get("rejected") != 0:
        result.errors.append("manifest rejected must be 0")
    if manifest.get("normalizationMatchCandidates") != 34:
        result.errors.append("manifest normalizationMatchCandidates must be 34")
    if manifest.get("sourceConflicts") != 13:
        result.errors.append("manifest sourceConflicts must be 13")
    if manifest.get("secondReviewer") is not None:
        result.errors.append("manifest secondReviewer must be null")
    if manifest.get("status") == "PARTIALLY_APPROVED" and manifest.get("importReady") is not False:
        result.errors.append("PARTIALLY_APPROVED importReady must be false")
    if manifest.get("status") == "APPROVED":
        if manifest.get("approved") != 47 or manifest.get("pending") != 0:
            result.errors.append("APPROVED manifest requires approved=47 pending=0")
        if manifest.get("importReady") is not True:
            result.errors.append("APPROVED manifest importReady must be true")
    if not manifest.get("reviewer"):
        result.errors.append("manifest reviewer must be set")
    if not manifest.get("decisionDate"):
        result.errors.append("manifest decisionDate must be set")

    if len(results) != 34:
        result.errors.append(f"approval result expected 34 rows, found {len(results)}")
    for row in results:
        if row.get("approvalStatus") != "APPROVED":
            result.errors.append(f"result {row.get('canonicalReference')}: not APPROVED")
        if row.get("canonicalReference") not in set(cand_refs):
            result.errors.append(f"result {row.get('canonicalReference')}: unexpected ref")
        draft_row = next(r for r in prior if r["canonicalReference"] == row["canonicalReference"])
        expected_cs = sha256_text(
            json.dumps(draft_row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        )
        if row.get("canonicalDraftRecordChecksum") != expected_cs:
            result.errors.append(
                f"{row.get('canonicalReference')}: draft record checksum mismatch"
            )

    # Editorial manifest importReady may become true at 47 Sanskrit approvals;
    # draft-level import_ready stays false while transliteration remains null.
    sanskrit_ok = all(
        isinstance(r.get("sanskritText"), str) and r["sanskritText"].strip() for r in approved
    )
    translit_populated = sum(
        1
        for r in draft
        if isinstance(r.get("transliteration"), str) and r["transliteration"].strip()
    )
    import_ready = (
        len(approved) == 47
        and sanskrit_ok
        and translit_populated == 47
        and all(r.get("approvalStatus") == "APPROVED" for r in draft)
    )
    if import_ready:
        result.errors.append(
            "chapter draft-level import readiness must remain false while transliteration is null"
        )
    result.info = {
        "approved": len(approved),
        "pendingConflicts": len(unapproved_or_other),
        "importReady": False,
        "manifestImportReady": manifest.get("importReady"),
        "transliterationPopulated": translit_populated,
        "manifestStatus": manifest.get("status"),
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Chapter 1 NORMALIZATION_MATCH batch approval state"
    )
    parser.add_argument("--chapter-dir", type=Path, default=CHAPTER_DIR)
    parser.add_argument("--reviews-dir", type=Path, default=REVIEWS_DIR)
    args = parser.parse_args(argv)
    result = validate_normalization_match_approval(
        chapter_dir=args.chapter_dir,
        reviews_dir=args.reviews_dir,
    )
    payload = {"ok": result.ok, "errors": result.errors, "info": result.info}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
