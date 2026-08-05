#!/usr/bin/env python3
"""Validate automated comparison reports and audit samples (Phase 2).

Does not approve Verses. Does not modify canonical drafts.
"""

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

from compare_sources import (  # noqa: E402
    CLASSIFICATIONS,
    deterministic_audit_sample,
    load_json,
    load_jsonl,
    run_chapter,
)

ALLOWED_DIFF_CATEGORIES = frozenset(
    {
        "FRONT_MATTER",
        "SPEAKER_LABEL",
        "VERSE_MARKER",
        "WHITESPACE",
        "PUNCTUATION",
        "DANDA_STYLE",
        "ORTHOGRAPHY_APPROVED",
        "ORTHOGRAPHY_UNAPPROVED",
        "WORD_DIFFERENCE",
        "WORD_ORDER",
        "MISSING_TEXT",
        "EXTRA_TEXT",
        "SEGMENTATION",
        "SOURCE_ERROR",
    }
)

SUBSTANTIVE = frozenset(
    {
        "SPEAKER_LABEL",
        "ORTHOGRAPHY_UNAPPROVED",
        "WORD_DIFFERENCE",
        "WORD_ORDER",
        "MISSING_TEXT",
        "EXTRA_TEXT",
        "SEGMENTATION",
        "SOURCE_ERROR",
    }
)


class ValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_report(
    *,
    chapter_dir: Path,
    policy_path: Path,
    expected_identities: int = 47,
    draft_sha_before: str | None = None,
) -> ValidationResult:
    result = ValidationResult()
    policy = load_json(policy_path)
    rule_ids = {r["id"] for r in policy.get("rules", [])}
    report_path = chapter_dir / "automated-comparison-report.jsonl"
    sample_path = chapter_dir / "audit-sample.json"
    draft_path = chapter_dir / "canonical-draft.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    reviews_dir = REPO_ROOT / "content/editorial/reviews"

    if not report_path.is_file():
        result.errors.append(f"missing report: {report_path}")
        return result

    rows = load_jsonl(report_path)
    if len(rows) != expected_identities:
        result.errors.append(f"expected {expected_identities} results, found {len(rows)}")

    refs = [r.get("canonicalReference") for r in rows]
    if len(refs) != len(set(refs)):
        result.errors.append("duplicate canonicalReference in automated report")

    source_rows = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)} if comparison_path.is_file() else {}

    approved_count = 0
    for row in rows:
        ref = row.get("canonicalReference")
        cls = row.get("classification")
        conf = row.get("confidence")
        if cls not in CLASSIFICATIONS:
            result.errors.append(f"{ref}: invalid classification {cls!r}")
        if not isinstance(conf, (int, float)) or not (0.0 <= float(conf) <= 1.0):
            result.errors.append(f"{ref}: confidence out of range: {conf!r}")
        for rule in row.get("normalizationRulesApplied") or []:
            if rule not in rule_ids:
                result.errors.append(f"{ref}: unknown normalization rule {rule!r}")
        cats = []
        for d in row.get("differences") or []:
            cat = d.get("category")
            cats.append(cat)
            if cat not in ALLOWED_DIFF_CATEGORIES:
                result.errors.append(f"{ref}: unknown difference category {cat!r}")
        if cls == "SOURCE_CONFLICT" and not row.get("requiresHumanReview"):
            result.errors.append(f"{ref}: SOURCE_CONFLICT must require human review")
        if cls == "INSUFFICIENT_SOURCES" and not row.get("requiresHumanReview"):
            result.errors.append(f"{ref}: INSUFFICIENT_SOURCES must require human review")
        if cls == "SOURCE_CONFLICT" and not (set(cats) & SUBSTANTIVE) and not row["comparison"].get(
            "substantiveDifference"
        ):
            result.warnings.append(f"{ref}: SOURCE_CONFLICT without substantive category")

        # Preserve original source forms in source-comparison
        src = source_rows.get(ref)
        if src:
            for s in src.get("sources") or []:
                if "sanskritText" in s and s["sanskritText"] is not None:
                    if not isinstance(s["sanskritText"], str):
                        result.errors.append(f"{ref}: source text not preserved as string")

        review_path = reviews_dir / f"{ref}.md"
        if review_path.is_file():
            text = review_path.read_text(encoding="utf-8")
            if re_status_approved(text):
                approved_count += 1
                # Engine must never create APPROVED; existing APPROVED would be human — still flag if automation claimed it
                if "No approval granted" not in text and "## Automated Comparison" in text:
                    result.warnings.append(f"{ref}: review is APPROVED; confirm human-only")

    if draft_path.is_file():
        draft_sha = sha256_text(draft_path.read_text(encoding="utf-8"))
        if draft_sha_before and draft_sha != draft_sha_before:
            result.errors.append("canonical-draft.jsonl checksum changed")
        # Phase 2 comparison must not itself grant approval. Human-approved
        # draft rows are allowed after controlled batch/editorial approval.
        for d in load_jsonl(draft_path):
            if d.get("approvalStatus") == "APPROVED":
                approved_count += 1
                if d.get("classification") not in {
                    None,
                    "NORMALIZATION_MATCH",
                    "AUTO_MATCH",
                    "ORTHOGRAPHIC_EQUIVALENCE",
                    "FINAL_CONFLICT_RESOLUTION",
                }:
                    result.errors.append(
                        f"draft {d.get('canonicalReference')}: unexpected "
                        "classification on APPROVED row"
                    )
                continue
            if d.get("approvalStatus") not in {
                None,
                "UNREVIEWED",
                "READY_FOR_REVIEW",
                "UNDER_REVIEW",
                "SOURCE_CONFLICT",
                "SOURCE_MISSING",
                "NEEDS_SOURCE",
                "PENDING",
            }:
                result.errors.append(
                    f"draft {d.get('canonicalReference')}: unexpected approvalStatus "
                    f"{d.get('approvalStatus')!r}"
                )

    if sample_path.is_file():
        sample = load_json(sample_path)
        recomputed = deterministic_audit_sample(rows, policy=policy)
        if sample.get("selectedReferences") != recomputed.get("selectedReferences"):
            result.errors.append("audit-sample.json is not deterministic vs recomputation")
    else:
        result.errors.append(f"missing audit sample: {sample_path}")

    result.warnings  # placate linters
    return result


def re_status_approved(text: str) -> bool:
    import re

    m = re.search(r"# Status\n\n([A-Z_]+)\n", text)
    return bool(m and m.group(1) == "APPROVED")


def check_determinism(chapter_dir: Path, policy_path: Path) -> ValidationResult:
    result = ValidationResult()
    first = run_chapter(
        chapter_dir=chapter_dir,
        policy_path=policy_path,
        reference=None,
        update_reviews=False,
        set_under_review=False,
    )
    sha1 = first["runMeta"]["reportSha256"]
    second = run_chapter(
        chapter_dir=chapter_dir,
        policy_path=policy_path,
        reference=None,
        update_reviews=False,
        set_under_review=False,
    )
    sha2 = second["runMeta"]["reportSha256"]
    if sha1 != sha2:
        result.errors.append(f"non-deterministic report: {sha1} vs {sha2}")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate automated comparison outputs")
    parser.add_argument(
        "--chapter-dir",
        type=Path,
        default=REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=REPO_ROOT / "content/editorial/normalization-policy.json",
    )
    parser.add_argument("--check-determinism", action="store_true")
    args = parser.parse_args(argv)

    draft_path = args.chapter_dir / "canonical-draft.jsonl"
    draft_sha = sha256_text(draft_path.read_text(encoding="utf-8")) if draft_path.is_file() else None

    result = validate_report(
        chapter_dir=args.chapter_dir,
        policy_path=args.policy,
        draft_sha_before=draft_sha,
    )
    if args.check_determinism:
        det = check_determinism(args.chapter_dir, args.policy)
        result.errors.extend(det.errors)

    for e in result.errors:
        print(f"ERROR: {e}")
    for w in result.warnings:
        print(f"WARN: {w}")
    print("OK" if result.ok else "FAIL")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
