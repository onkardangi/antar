#!/usr/bin/env python3
"""Validate Chapter 1 orthographic SOURCE_CONFLICT resolution state."""

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
DECISION_TYPE = "ORTHOGRAPHIC_SOURCE_CONFLICT_RESOLUTION"
PRIOR_DECISION_TYPE = "BATCH_NORMALIZATION_MATCH_APPROVAL"
ELIGIBLE = {
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
}
FORBIDDEN = {"1.20", "1.22"}


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


def validate_orthographic_resolution(
    *,
    chapter_dir: Path = CHAPTER_DIR,
    reviews_dir: Path = REVIEWS_DIR,
) -> Result:
    result = Result()
    draft_path = chapter_dir / "canonical-draft.jsonl"
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"
    result_path = chapter_dir / "orthographic-resolution-result.jsonl"
    conflict_path = chapter_dir / "source-conflict-analysis.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    prior_result = chapter_dir / "normalization-match-approval-result.jsonl"

    for path in (draft_path, manifest_path, result_path, conflict_path, comparison_path):
        if not path.is_file():
            result.errors.append(f"missing {path}")
            return result

    draft = load_jsonl(draft_path)
    results = load_jsonl(result_path)
    conflicts = load_jsonl(conflict_path)
    comparisons = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)}
    manifest = load_json(manifest_path)

    approved = [r for r in draft if r.get("approvalStatus") == "APPROVED"]
    unapproved = [r for r in draft if r.get("approvalStatus") != "APPROVED"]
    prior = [r for r in approved if r.get("decisionType") == PRIOR_DECISION_TYPE]
    ortho = [r for r in approved if r.get("decisionType") == DECISION_TYPE]

    if len(approved) not in {45, 47}:
        result.errors.append(f"expected 45 or 47 APPROVED, found {len(approved)}")
    if len(approved) == 45:
        if len(unapproved) != 2:
            result.errors.append(f"expected 2 unapproved, found {len(unapproved)}")
        if {r["canonicalReference"] for r in unapproved} != FORBIDDEN:
            result.errors.append("unapproved refs must be exactly 1.20 and 1.22")
    elif len(approved) == 47:
        if len(unapproved) != 0:
            result.errors.append(f"expected 0 unapproved after final conflicts, found {len(unapproved)}")
    if len(prior) != 34:
        result.errors.append(f"expected 34 prior NORMALIZATION_MATCH approvals, found {len(prior)}")
    if len(ortho) != 11:
        result.errors.append(f"expected 11 orthographic approvals, found {len(ortho)}")
    if {r["canonicalReference"] for r in ortho} != ELIGIBLE:
        result.errors.append("orthographic approved set mismatch")

    for row in ortho:
        ref = row["canonicalReference"]
        wiki = next(
            s for s in comparisons[ref]["sources"] if s.get("sourceId") == WIKISOURCE_ID
        )
        if row.get("sanskritText") != wiki.get("sanskritText"):
            result.errors.append(f"{ref}: Sanskrit not byte-identical to Wikisource")
        if row.get("transliteration") is not None:
            result.errors.append(f"{ref}: transliteration must be null")
        if "iitk" not in " ".join(row.get("approvedSourceIds") or []):
            result.errors.append(f"{ref}: missing IIT verification source id")
        review_path = reviews_dir / f"{ref}.md"
        if not review_path.is_file():
            result.errors.append(f"missing review {ref}")
        else:
            errs = validate_review_text(
                review_path.read_text(encoding="utf-8"),
                expected_ref=ref,
                path_label=str(review_path),
            )
            result.errors.extend(errs)

    for ref in sorted(FORBIDDEN):
        row = next(r for r in draft if r["canonicalReference"] == ref)
        if len(approved) == 45:
            if row.get("approvalStatus") == "APPROVED" or row.get("sanskritText") is not None:
                result.errors.append(f"{ref}: must remain unresolved")
        elif len(approved) == 47:
            if row.get("approvalStatus") != "APPROVED" or not row.get("sanskritText"):
                result.errors.append(f"{ref}: must be approved after final conflicts")
            if row.get("decisionType") != "FINAL_CHAPTER01_CONFLICT_RESOLUTION":
                result.errors.append(f"{ref}: expected FINAL_CHAPTER01_CONFLICT_RESOLUTION")
        review_path = reviews_dir / f"{ref}.md"
        if review_path.is_file():
            status = (
                review_path.read_text(encoding="utf-8")
                .split("# Status", 1)[-1]
                .split("#", 1)[0]
            )
            if len(approved) == 45 and "APPROVED" in status.split():
                result.errors.append(f"{ref}: review must not be APPROVED")
            if len(approved) == 47 and "APPROVED" not in status.split():
                result.errors.append(f"{ref}: review must be APPROVED after final conflicts")

    # Conflict history preserved.
    if len(conflicts) != 13:
        result.errors.append("conflict analysis must still contain 13 historical records")
    if any(c.get("classification") != "SOURCE_CONFLICT" for c in conflicts):
        result.errors.append("conflict analysis classifications must remain SOURCE_CONFLICT")

    if len(results) != 11:
        result.errors.append(f"result file expected 11 rows, found {len(results)}")
    for row in results:
        ref = row.get("canonicalReference")
        if ref not in ELIGIBLE:
            result.errors.append(f"unexpected result ref {ref}")
        draft_row = next(r for r in ortho if r["canonicalReference"] == ref)
        if row.get("canonicalTextChecksum") != sha256_text(draft_row["sanskritText"]):
            result.errors.append(f"{ref}: canonical text checksum mismatch")
        if row.get("originalWikisourceForm") != draft_row["sanskritText"]:
            result.errors.append(f"{ref}: result Wikisource form mismatch")
        if row.get("approvalStatus") != "APPROVED":
            result.errors.append(f"{ref}: result not APPROVED")

    if len(approved) == 45:
        if manifest.get("approved") != 45 or manifest.get("pending") != 2:
            result.errors.append("manifest approved/pending counts incorrect")
        if manifest.get("importReady") is not False:
            result.errors.append("importReady must be false")
        if manifest.get("unresolvedReferences") != ["1.20", "1.22"]:
            result.errors.append("manifest unresolvedReferences incorrect")
        if manifest.get("status") != "PARTIALLY_APPROVED":
            result.errors.append("manifest status must remain PARTIALLY_APPROVED")
        unresolved = sorted(FORBIDDEN)
        import_ready = False
    else:
        # Post final-conflict Chapter state: orthographic resolutions remain intact.
        if manifest.get("approved") != 47 or manifest.get("pending") != 0:
            result.errors.append("post-final manifest must be approved=47 pending=0")
        if manifest.get("importReady") is not True:
            result.errors.append("post-final importReady must be true")
        if manifest.get("unresolvedReferences") not in ([], None):
            result.errors.append("post-final unresolvedReferences must be empty")
        if manifest.get("status") != "APPROVED":
            result.errors.append("post-final manifest status must be APPROVED")
        for ref in FORBIDDEN:
            row = next(r for r in draft if r["canonicalReference"] == ref)
            if row.get("decisionType") != "FINAL_CHAPTER01_CONFLICT_RESOLUTION":
                result.errors.append(f"{ref}: expected FINAL_CHAPTER01_CONFLICT_RESOLUTION")
        unresolved = []
        import_ready = True

    if prior_result.is_file():
        prior_rows = load_jsonl(prior_result)
        if len(prior_rows) != 34:
            result.errors.append("prior normalization-match approval result must remain 34 rows")

    result.info = {
        "approved": len(approved),
        "priorNormalizationMatchApproved": len(prior),
        "orthographicApproved": len(ortho),
        "unresolved": unresolved,
        "importReady": import_ready,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Chapter 1 orthographic conflict resolution"
    )
    parser.add_argument("--chapter-dir", type=Path, default=CHAPTER_DIR)
    parser.add_argument("--reviews-dir", type=Path, default=REVIEWS_DIR)
    args = parser.parse_args(argv)
    result = validate_orthographic_resolution(
        chapter_dir=args.chapter_dir,
        reviews_dir=args.reviews_dir,
    )
    print(
        json.dumps(
            {"ok": result.ok, "errors": result.errors, "info": result.info},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
