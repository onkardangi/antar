#!/usr/bin/env python3
"""Validate Chapter 1 human-approval preparation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_approval_prep(
    *,
    chapter_dir: Path = CHAPTER_DIR,
    draft_sha_expected: str | None = None,
) -> Result:
    result = Result()
    cand_path = chapter_dir / "normalization-match-approval-candidate.jsonl"
    conf_path = chapter_dir / "source-conflict-analysis.jsonl"
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"
    queue_path = chapter_dir / "third-reference-queue.json"
    draft_path = chapter_dir / "canonical-draft.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    report_path = chapter_dir / "automated-comparison-report.jsonl"

    for p in (cand_path, conf_path, manifest_path, queue_path):
        if not p.is_file():
            result.errors.append(f"missing {p}")
            return result

    candidates = load_jsonl(cand_path)
    conflicts = load_jsonl(conf_path)
    comparisons = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)}
    reports = {r["canonicalReference"]: r for r in load_jsonl(report_path)}
    manifest = load_json(manifest_path)
    queue = load_json(queue_path)

    if len(candidates) != 34:
        result.errors.append(f"expected 34 candidates, found {len(candidates)}")
    if len(conflicts) != 13:
        result.errors.append(f"expected 13 conflicts, found {len(conflicts)}")

    cand_refs = [c["canonicalReference"] for c in candidates]
    conf_refs = [c["canonicalReference"] for c in conflicts]
    if len(cand_refs) != len(set(cand_refs)):
        result.errors.append("duplicate candidate references")
    if len(conf_refs) != len(set(conf_refs)):
        result.errors.append("duplicate conflict references")
    if set(cand_refs) & set(conf_refs):
        result.errors.append("candidate/conflict reference overlap")

    expected = {f"1.{i}" for i in range(1, 48)}
    if set(cand_refs) | set(conf_refs) != expected:
        result.errors.append(
            f"partition incomplete: missing={(expected - (set(cand_refs)|set(conf_refs)))} "
            f"extra={((set(cand_refs)|set(conf_refs)) - expected)}"
        )

    for c in candidates:
        ref = c["canonicalReference"]
        if reports.get(ref, {}).get("classification") != "NORMALIZATION_MATCH":
            result.errors.append(f"{ref}: candidate not NORMALIZATION_MATCH in report")
        if c.get("approvalStatus") != "PENDING":
            result.errors.append(f"{ref}: candidate approvalStatus must be PENDING")
        if c.get("proposedTransliteration") is not None:
            result.errors.append(f"{ref}: transliteration must be null")
        if c.get("selectedSourceId") != WIKISOURCE_ID:
            result.errors.append(f"{ref}: selected source must be Wikisource primary")
        rec = comparisons.get(ref)
        if not rec:
            result.errors.append(f"{ref}: missing source-comparison record")
            continue
        wiki = next(
            (s for s in rec["sources"] if s.get("sourceId") == WIKISOURCE_ID),
            None,
        )
        if wiki is None:
            result.errors.append(f"{ref}: Wikisource source missing")
            continue
        proposed = c.get("proposedSanskritText")
        if proposed != wiki.get("sanskritText"):
            result.errors.append(f"{ref}: proposed text is not exact Wikisource copy")
        if c.get("proposedSanskritTextChecksumSha256") != sha256_text(proposed or ""):
            result.errors.append(f"{ref}: proposed text checksum mismatch")
        if proposed != wiki.get("sanskritText"):
            result.errors.append(f"{ref}: synthesized or altered Sanskrit detected")

    for c in conflicts:
        ref = c["canonicalReference"]
        if reports.get(ref, {}).get("classification") != "SOURCE_CONFLICT":
            result.errors.append(f"{ref}: conflict analysis not SOURCE_CONFLICT in report")
        if not c.get("humanDecisionRequired"):
            result.errors.append(f"{ref}: humanDecisionRequired must be true")
        if c.get("approvalStatus") != "PENDING":
            result.errors.append(f"{ref}: conflict approvalStatus must be PENDING")

    if manifest.get("approved") != 0:
        result.errors.append("manifest approved must be 0")
    if manifest.get("status") == "APPROVED":
        result.errors.append("manifest must not be APPROVED")
    if manifest.get("reviewer") is not None or manifest.get("secondReviewer") is not None:
        result.errors.append("manifest reviewers must remain null until human review")
    if manifest.get("normalizationMatchCandidates") != 34:
        result.errors.append("manifest candidate count mismatch")
    if manifest.get("sourceConflicts") != 13:
        result.errors.append("manifest conflict count mismatch")
    if manifest.get("pending") != 47:
        result.errors.append("manifest pending must be 47")

    for e in queue.get("entries") or []:
        if e["canonicalReference"] not in conf_refs:
            result.errors.append(
                f"queue {e['canonicalReference']} not in conflict set"
            )

    if draft_path.is_file():
        digest = sha256_file(draft_path)
        if draft_sha_expected and digest != draft_sha_expected:
            result.errors.append("canonical-draft.jsonl checksum changed")
        draft_rows = load_jsonl(draft_path)
        approved = sum(1 for r in draft_rows if r.get("approvalStatus") == "APPROVED")
        if approved != 0:
            result.errors.append("draft approved count must remain 0")

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Chapter 1 approval preparation")
    parser.add_argument("--chapter-dir", type=Path, default=CHAPTER_DIR)
    parser.add_argument(
        "--expected-draft-sha",
        default="31ff228c649096422a20bbe43423b9fcce28e6ce32d7e1e7a6462e9a92717d1a",
    )
    args = parser.parse_args(argv)
    result = validate_approval_prep(
        chapter_dir=args.chapter_dir,
        draft_sha_expected=args.expected_draft_sha,
    )
    for e in result.errors:
        print(f"ERROR: {e}")
    print("OK" if result.ok else "FAIL")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
