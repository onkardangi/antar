#!/usr/bin/env python3
"""Validate Chapter 1 editorial workspace after Wikisource acquisition/extraction.

Structural + provenance gates only. Does not approve textual accuracy.
Does not modify corpus files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

_VALIDATION_DIR = Path(__file__).resolve().parent
if str(_VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(_VALIDATION_DIR))

from validate_chapter_draft import (  # noqa: E402
    ALLOWED_APPROVAL_STATUSES,
    load_jsonl,
    validate_path,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
IITK_SOURCE_ID = "bhagavad-gita-sanskrit-iitk-verse-1.1-verification-v1"
EXPECTED = 47
ALLOWED_COMPARISON_STATUSES = ALLOWED_APPROVAL_STATUSES


class WorkspaceValidation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: dict[str, Any] = {}

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def looks_like_commentary(text: str) -> bool:
    markers = (
        "{{व्याख्या",
        "रामानुजभाष्यम्",
        "शांकरभाष्य",
        "Madhusudan",
    )
    return any(m in text for m in markers)


def validate_workspace(
    *,
    repo_root: Path = REPO_ROOT,
    chapter_dir: Path | None = None,
) -> WorkspaceValidation:
    result = WorkspaceValidation()
    chapter_dir = chapter_dir or (
        repo_root / "content/editorial/bhagavad-gita/chapter-01"
    )
    raw_path = (
        repo_root
        / "content/raw/sanskrit/wikisource/chapter-01"
        / "sa-wikisource-bg-chapter-01-revision-343151.json"
    )
    meta_path = (
        repo_root / "content/raw/sanskrit/wikisource/chapter-01/metadata.json"
    )
    sums_path = repo_root / "content/checksums/raw.sha256"
    registry_path = repo_root / "content/registry/sources.json"
    extraction_path = chapter_dir / "wikisource-extraction.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    draft_path = chapter_dir / "canonical-draft.jsonl"

    if not raw_path.is_file():
        result.errors.append(f"missing raw snapshot: {raw_path}")
        return result

    digest = sha256_file(raw_path)
    result.info["rawSha256"] = digest
    sums_text = sums_path.read_text(encoding="utf-8") if sums_path.is_file() else ""
    expected_line = f"{digest}  content/raw/sanskrit/wikisource/chapter-01/sa-wikisource-bg-chapter-01-revision-343151.json"
    if expected_line not in sums_text:
        result.errors.append("raw snapshot checksum missing/mismatch in content/checksums/raw.sha256")

    meta = load_json(meta_path) if meta_path.is_file() else {}
    if meta.get("rawSha256") != digest:
        result.errors.append("metadata.json rawSha256 does not match snapshot file")
    if meta.get("revisionId") != 343151:
        result.errors.append(f"unexpected revisionId in metadata: {meta.get('revisionId')}")
    if meta.get("pageId") != 164:
        result.errors.append(f"unexpected pageId in metadata: {meta.get('pageId')}")

    registry = load_json(registry_path)
    registry_sources = registry.get("sources") or []
    entry = next((s for s in registry_sources if s.get("id") == SOURCE_ID), None)
    if entry is None:
        result.errors.append(f"registry missing source id {SOURCE_ID}")
    else:
        if entry.get("sha256") != digest:
            result.errors.append("registry sha256 does not match raw snapshot")
        if entry.get("status") == "APPROVED_FOR_IMPORT":
            result.errors.append("source must not be APPROVED_FOR_IMPORT yet")
        result.info["registryStatus"] = entry.get("status")

    extraction, ext_errs = load_jsonl(extraction_path)
    result.errors.extend(f"extraction: {e}" for e in ext_errs)
    if len(extraction) != EXPECTED:
        result.errors.append(f"extraction expected {EXPECTED} records, found {len(extraction)}")

    refs = [r.get("canonicalReference") for r in extraction]
    if refs != [f"1.{v}" for v in range(1, EXPECTED + 1)]:
        result.errors.append("extraction references are not exactly 1.1–1.47 in order")
    if len(refs) != len(set(refs)):
        result.errors.append("extraction contains duplicate references")

    for record in extraction:
        text = record.get("sanskritText")
        if not isinstance(text, str) or text.strip() == "":
            result.errors.append(
                f"extraction {record.get('canonicalReference')}: blank Sanskrit"
            )
            continue
        if text != unicodedata.normalize("NFC", text):
            result.errors.append(
                f"extraction {record.get('canonicalReference')}: Sanskrit not NFC"
            )
        if looks_like_commentary(text):
            result.errors.append(
                f"extraction {record.get('canonicalReference')}: commentary markers found"
            )
        if record.get("transliteration") is not None:
            result.errors.append(
                f"extraction {record.get('canonicalReference')}: transliteration must be null"
            )
        if record.get("sourceId") != SOURCE_ID:
            result.errors.append(
                f"extraction {record.get('canonicalReference')}: unexpected sourceId"
            )

    comparison, cmp_errs = load_jsonl(comparison_path)
    result.errors.extend(f"comparison: {e}" for e in cmp_errs)
    if len(comparison) != EXPECTED:
        result.errors.append(
            f"source-comparison expected {EXPECTED} records, found {len(comparison)}"
        )

    extraction_by_ref = {r["canonicalReference"]: r for r in extraction}
    cmp_statuses: Counter[str] = Counter()
    for record in comparison:
        ref = record.get("canonicalReference")
        status = record.get("status")
        cmp_statuses[str(status)] += 1
        if status not in ALLOWED_COMPARISON_STATUSES:
            result.errors.append(f"comparison {ref}: invalid status {status!r}")
        if ref not in extraction_by_ref:
            result.errors.append(f"comparison {ref}: no matching extraction record")
            continue
        sources = record.get("sources") or []
        wiki = [s for s in sources if s.get("sourceId") == SOURCE_ID]
        if len(wiki) != 1:
            result.errors.append(
                f"comparison {ref}: expected exactly one Wikisource source entry"
            )
            continue
        if not isinstance(wiki[0].get("sanskritText"), str) or not wiki[0]["sanskritText"].strip():
            result.errors.append(f"comparison {ref}: Wikisource Sanskrit blank")
        if wiki[0].get("sanskritText") != extraction_by_ref[ref].get("sanskritText"):
            result.errors.append(
                f"comparison {ref}: Sanskrit does not match extraction"
            )

        iitk_id = f"bhagavad-gita-sanskrit-iitk-verse-{ref}-verification-v1"
        iitk = [s for s in sources if s.get("sourceId") == iitk_id]
        if ref in {"1.20", "1.22"}:
            if len(sources) != 3:
                result.errors.append(
                    f"comparison {ref}: expected three source references "
                    "(Wikisource + IIT + Sanskrit Documents)"
                )
            third = [
                s
                for s in sources
                if s.get("sourceRole") == "THIRD_EDITORIAL_VERIFICATION_REFERENCE"
                or "sanskritdocuments" in str(s.get("sourceId") or "")
            ]
            if len(third) != 1:
                result.errors.append(
                    f"comparison {ref}: missing THIRD_EDITORIAL_VERIFICATION_REFERENCE"
                )
        elif len(sources) != 2:
            result.errors.append(
                f"comparison {ref}: expected exactly two source references (Wikisource + IIT)"
            )
        if len(iitk) != 1:
            result.errors.append(f"comparison {ref}: missing IIT verification source {iitk_id}")
        else:
            if iitk[0].get("sourceRole") != "SECONDARY_VERIFICATION_REFERENCE":
                result.errors.append(
                    f"comparison {ref}: IIT sourceRole must be SECONDARY_VERIFICATION_REFERENCE"
                )
            evidence_checksum = iitk[0].get("evidenceChecksum")
            if not evidence_checksum:
                result.errors.append(f"comparison {ref}: IIT evidenceChecksum missing")
            else:
                evidence_path = (
                    repo_root
                    / f"content/raw/sanskrit/iit-kanpur/verse-{ref}/verse-{ref}-mool-evidence.json"
                )
                if evidence_path.is_file():
                    digest = sha256_file(evidence_path)
                    if digest != evidence_checksum:
                        result.errors.append(
                            f"comparison {ref}: IIT evidenceChecksum mismatch"
                        )
                else:
                    result.errors.append(f"comparison {ref}: missing IIT evidence file")
        if status not in {
            "READY_FOR_REVIEW",
            "SOURCE_CONFLICT",
            "SOURCE_MISSING",
            "NEEDS_SOURCE",
            "UNDER_REVIEW",
        }:
            result.errors.append(
                f"comparison {ref}: unexpected status {status!r}"
            )

    result.info["comparisonStatusCounts"] = dict(cmp_statuses)

    # Registry: all IIT verse entries must remain verification-only / not import-approved
    iitk_entries = [
        s for s in registry_sources if str(s.get("id", "")).startswith(
            "bhagavad-gita-sanskrit-iitk-verse-"
        )
    ]
    if len(iitk_entries) < EXPECTED:
        result.errors.append(
            f"registry expected >= {EXPECTED} IIT verification entries, found {len(iitk_entries)}"
        )
    for iitk_entry in iitk_entries:
        if iitk_entry.get("status") in {
            "APPROVED_FOR_IMPORT",
            "APPROVED_FOR_NORMALIZATION",
            "IMPORTED",
        }:
            result.errors.append(
                f"IIT {iitk_entry.get('id')} must not be approved for import"
            )
        if iitk_entry.get("status") != "VERIFICATION_ONLY":
            result.errors.append(
                f"IIT {iitk_entry.get('id')} status must be VERIFICATION_ONLY, "
                f"found {iitk_entry.get('status')!r}"
            )
        if iitk_entry.get("source_role") != "SECONDARY_VERIFICATION_REFERENCE":
            result.errors.append(
                f"IIT {iitk_entry.get('id')} source_role must be SECONDARY_VERIFICATION_REFERENCE"
            )
    result.info["iitkRegistryCount"] = len(iitk_entries)

    # Review file 1.1 — status may be UNDER_REVIEW (pre-approval) or APPROVED (batch approved)
    review_path = repo_root / "content/editorial/reviews/1.1.md"
    if not review_path.is_file():
        result.errors.append("missing review file content/editorial/reviews/1.1.md")
    else:
        review_text = review_path.read_text(encoding="utf-8")
        status_block = review_text.split("# Status", 1)[-1].split("#", 1)[0]
        status_token = next((ln.strip() for ln in status_block.splitlines() if ln.strip()), "")
        if status_token not in {"UNDER_REVIEW", "APPROVED"}:
            result.errors.append(
                f"review 1.1 status must be UNDER_REVIEW or APPROVED, found {status_token!r}"
            )
        if SOURCE_ID not in review_text or IITK_SOURCE_ID not in review_text:
            result.errors.append("review 1.1 must reference both Wikisource and IIT source IDs")
        approval_block = review_text.split("# Approval", 1)[-1].split("#", 1)[0]
        if "Reviewer:" not in approval_block or "Date:" not in approval_block:
            result.errors.append("review 1.1 Approval section incomplete")
        if status_token == "UNDER_REVIEW":
            for label in ("Reviewer", "Second Reviewer", "Date"):
                m = re.search(rf"^{label}:[ \t]*(.*)$", approval_block, re.M)
                if m and m.group(1).strip():
                    result.errors.append(f"review 1.1 Approval {label} must remain blank")
        elif status_token == "APPROVED":
            reviewer = re.search(r"^Reviewer:[ \t]*(.*)$", approval_block, re.M)
            date_value = re.search(r"^Date:[ \t]*(.*)$", approval_block, re.M)
            if not reviewer or not reviewer.group(1).strip():
                result.errors.append("review 1.1 APPROVED requires Reviewer")
            if not date_value or not date_value.group(1).strip():
                result.errors.append("review 1.1 APPROVED requires Date")
        audit = review_text.split("# Audit Log", 1)[-1]
        if "TEXT_MATCH_AFTER_DOCUMENTED_NORMALIZATION" not in audit and "SOURCE_CONFLICT" not in audit:
            result.errors.append("review 1.1 audit log missing comparison event")
        if "IIT" not in audit and "iitk" not in audit.lower() and IITK_SOURCE_ID not in audit:
            result.errors.append("review 1.1 audit log missing IIT comparison event")

    draft_result = validate_path(draft_path)
    if not draft_result.ok:
        result.errors.extend(f"canonical-draft: {e}" for e in draft_result.errors)
    result.info["draftApprovedCount"] = draft_result.approved_count
    result.info["draftImportReady"] = draft_result.import_ready
    result.info["draftSanskritPopulated"] = draft_result.sanskrit_populated

    # Pre-approval: 0. Norm-match: 34. Orthographic: 45. Final conflicts: 47.
    # Draft-level import_ready also requires transliteration; Sanskrit-only 47 stays false.
    if draft_result.import_ready:
        result.errors.append("import readiness must remain false")
    if draft_result.approved_count not in {0, 34, 45, 47}:
        result.errors.append(
            f"canonical-draft approved count must be 0, 34, 45, or 47, found {draft_result.approved_count}"
        )
    if draft_result.approved_count == 0 and draft_result.sanskrit_populated != 0:
        result.errors.append("canonical-draft must not yet contain Sanskrit text")
    if draft_result.approved_count in {34, 45, 47}:
        if draft_result.sanskrit_populated != draft_result.approved_count:
            result.errors.append(
                "approved count must equal Sanskrit-populated count for Sanskrit-only approvals"
            )
        if draft_result.transliteration_populated != 0:
            result.errors.append("transliteration must remain null after Sanskrit-only approval")

    result.info["extractionCount"] = len(extraction)
    result.info["sourceAcquisitionValidated"] = (
        raw_path.is_file() and entry is not None and not any(
            e.startswith("raw ") or e.startswith("registry") or e.startswith("metadata")
            for e in result.errors
        )
    )
    result.info["structuralExtractionValidated"] = len(extraction) == EXPECTED and not any(
        e.startswith("extraction") for e in result.errors
    )
    result.info["textualAccuracyEditoriallyApproved"] = draft_result.approved_count == EXPECTED
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Chapter 1 Wikisource acquisition/extraction workspace."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: inferred)",
    )
    args = parser.parse_args(argv)
    result = validate_workspace(repo_root=args.repo_root.resolve())
    payload = {
        "ok": result.ok,
        "errors": result.errors,
        "info": result.info,
        "note": (
            "Source acquisition and structural extraction checks only. "
            "Textual accuracy is not editorially approved."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
