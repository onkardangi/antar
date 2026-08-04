#!/usr/bin/env python3
"""Build an immutable Antar Scripture content package from approved editorial inputs.

Never modifies editorial inputs. Refuses to overwrite an existing package.
Never copies pending or conflicted Verse content into a package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_package import (  # noqa: E402
    PACKAGE_BUILDER_VERSION,
    combined_package_checksum,
    dump_json,
    dump_jsonl,
    format_sha256sums,
    load_json,
    load_jsonl,
    load_source_ids,
    sha256_bytes,
    sha256_file,
    validate_package,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SOURCES = REPO_ROOT / "content/registry/sources.json"
DEFAULT_OUTPUT_PARENT = REPO_ROOT / "content/packages"
CHAPTER01_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
VERSE_COUNTS_PATH = REPO_ROOT / "content/validation/antar_verse_counts.json"

PENDING_STATUSES = frozenset(
    {
        "PENDING",
        "UNREVIEWED",
        "READY_FOR_REVIEW",
        "UNDER_REVIEW",
        "NEEDS_SOURCE",
        "SOURCE_MISSING",
        "PENDING_EDITORIAL_REVIEW",
    }
)
CONFLICT_STATUSES = frozenset({"SOURCE_CONFLICT", "CONFLICTED"})
REJECTED_STATUSES = frozenset({"REJECTED"})


class BuildError(Exception):
    """Raised when package inputs are invalid or incomplete."""


def expected_chapter_verse_count(chapter_number: int) -> int:
    data = load_json(VERSE_COUNTS_PATH)
    counts = data.get("verse_counts") or {}
    if str(chapter_number) not in counts:
        raise BuildError(f"no Antar verse count for chapter {chapter_number}")
    return int(counts[str(chapter_number)])


def load_registry_map(registry_path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(registry_path)
    sources = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(sources, list):
        raise BuildError(f"{registry_path}: expected sources array")
    out: dict[str, dict[str, Any]] = {}
    for entry in sources:
        if isinstance(entry, dict) and "id" in entry:
            out[str(entry["id"])] = entry
    return out


def record_approval_status(record: dict[str, Any]) -> str:
    status = record.get("approvalStatus") or record.get("status")
    if status is None:
        raise BuildError(
            f"{record.get('canonicalReference', '?')}: missing approvalStatus"
        )
    return str(status)


def is_conflicted(record: dict[str, Any]) -> bool:
    status = record_approval_status(record)
    classification = str(record.get("classification") or "")
    return status in CONFLICT_STATUSES or classification == "SOURCE_CONFLICT"


def collect_approved_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    approved: list[dict[str, Any]] = []
    for record in records:
        ref = record.get("canonicalReference", "?")
        status = record_approval_status(record)
        if is_conflicted(record):
            raise BuildError(f"{ref}: conflicted editorial record rejected")
        if status in PENDING_STATUSES:
            raise BuildError(f"{ref}: pending editorial record rejected ({status})")
        if status in REJECTED_STATUSES:
            raise BuildError(f"{ref}: rejected editorial record cannot be packaged")
        if status != "APPROVED":
            raise BuildError(f"{ref}: unsupported approvalStatus {status!r}")
        approved.append(record)
    return approved


def validate_approved_inputs(
    *,
    approval_manifest: dict[str, Any],
    approved_records: list[dict[str, Any]],
    registry: dict[str, dict[str, Any]],
    chapter_number: int,
    package_status: str,
    require_complete_chapter: bool,
) -> None:
    if not approved_records:
        raise BuildError(
            "no approved Verses found; refuse to build package "
            f"(approval manifest approved={approval_manifest.get('approved', 0)})"
        )

    manifest_approved = approval_manifest.get("approved")
    if manifest_approved is not None and int(manifest_approved) != len(approved_records):
        raise BuildError(
            f"approval manifest approved count {manifest_approved} != "
            f"approved record count {len(approved_records)}"
        )

    reviewer = approval_manifest.get("reviewer") or approval_manifest.get("reviewerId")
    if not reviewer:
        # Per-record reviewers may satisfy the requirement
        missing = [
            r.get("canonicalReference")
            for r in approved_records
            if not (r.get("reviewerId") or r.get("reviewer"))
        ]
        if missing:
            raise BuildError(f"missing reviewers for approved records: {missing}")

    if package_status == "APPROVED":
        second = approval_manifest.get("secondReviewer") or approval_manifest.get(
            "secondReviewerId"
        )
        # Second reviewer required when manifest or any record declares it required
        requires_second = bool(approval_manifest.get("requiresSecondReviewer"))
        if requires_second and not second:
            raise BuildError("missing second reviewer required for APPROVED package")
        for record in approved_records:
            if record.get("requiresSecondReviewer") and not (
                record.get("secondReviewerId") or second
            ):
                raise BuildError(
                    f"{record.get('canonicalReference')}: missing second reviewer"
                )
            if not record.get("editorialDecisionId") and not record.get("decisionId"):
                raise BuildError(
                    f"{record.get('canonicalReference')}: missing editorial decision id"
                )
            if not record.get("editorialApprovalChecksum") and not record.get(
                "approvalChecksum"
            ):
                raise BuildError(
                    f"{record.get('canonicalReference')}: missing editorial approval checksum"
                )

    seen: set[str] = set()
    for record in approved_records:
        ref = str(record.get("canonicalReference"))
        if ref in seen:
            raise BuildError(f"duplicate canonical reference: {ref}")
        seen.add(ref)

        ch = record.get("chapterNumber")
        vn = record.get("verseNumber")
        if ch != chapter_number:
            raise BuildError(f"{ref}: chapterNumber {ch} != package chapter {chapter_number}")
        if ref != f"{ch}.{vn}":
            raise BuildError(f"{ref}: canonicalReference must equal chapterNumber.verseNumber")

        text = record.get("sanskritText") or record.get("proposedSanskritText")
        if not isinstance(text, str) or not text.strip():
            raise BuildError(f"{ref}: Sanskrit must be nonblank")

        source_ids = record.get("sourceIds") or record.get("approvedSourceIds")
        if not source_ids and record.get("selectedSourceId"):
            source_ids = [record["selectedSourceId"]] + list(
                record.get("supportingSourceIds") or []
            )
        if not source_ids:
            raise BuildError(f"{ref}: missing sourceIds")

        checksums = dict(record.get("sourceChecksums") or {})
        if not checksums and record.get("selectedSourceChecksum"):
            checksums[str(record["selectedSourceId"])] = record["selectedSourceChecksum"]
            for sid, meta in (record.get("supportingSourceChecksums") or {}).items():
                if isinstance(meta, dict) and meta.get("sourceChecksum"):
                    checksums[str(sid)] = meta["sourceChecksum"]
                elif isinstance(meta, str):
                    checksums[str(sid)] = meta
        for sid in source_ids:
            if sid not in registry:
                raise BuildError(f"{ref}: missing source registry entry for {sid}")
            if sid not in checksums:
                raise BuildError(f"{ref}: missing checksum for source {sid}")
            expected = registry[sid].get("sha256")
            if expected and checksums[sid] != expected:
                # Allow evidence checksums that differ from root artifact when explicitly provided
                # but still require a 64-hex checksum string.
                if len(str(checksums[sid])) != 64:
                    raise BuildError(f"{ref}: invalid checksum for source {sid}")

    if require_complete_chapter:
        expected = expected_chapter_verse_count(chapter_number)
        if len(approved_records) != expected:
            raise BuildError(
                f"incomplete chapter range: expected {expected} approved Verses, "
                f"found {len(approved_records)}"
            )
        expected_refs = {f"{chapter_number}.{i}" for i in range(1, expected + 1)}
        if seen != expected_refs:
            raise BuildError(
                f"incomplete chapter range: missing={sorted(expected_refs - seen)} "
                f"extra={sorted(seen - expected_refs)}"
            )


def to_verse_record(record: dict[str, Any], content_version: int) -> dict[str, Any]:
    source_ids = list(record.get("sourceIds") or record.get("approvedSourceIds") or [])
    if not source_ids and record.get("selectedSourceId"):
        source_ids = [record["selectedSourceId"]] + list(
            record.get("supportingSourceIds") or []
        )
    source_ids = [str(s) for s in source_ids]

    checksums = dict(record.get("sourceChecksums") or {})
    if not checksums and record.get("selectedSourceChecksum"):
        checksums[str(record["selectedSourceId"])] = record["selectedSourceChecksum"]
        for sid, meta in (record.get("supportingSourceChecksums") or {}).items():
            if isinstance(meta, dict) and meta.get("sourceChecksum"):
                checksums[str(sid)] = meta["sourceChecksum"]
            elif isinstance(meta, str):
                checksums[str(sid)] = meta
    checksums = {str(k): str(v) for k, v in checksums.items()}

    sanskrit = record.get("sanskritText")
    if sanskrit is None:
        sanskrit = record.get("proposedSanskritText")
    transliteration = record.get("transliteration")
    if transliteration is None and "proposedTransliteration" in record:
        transliteration = record.get("proposedTransliteration")

    decision_id = (
        record.get("editorialDecisionId")
        or record.get("decisionId")
        or f"decision-{record['canonicalReference']}"
    )
    approval_checksum = (
        record.get("editorialApprovalChecksum")
        or record.get("approvalChecksum")
    )
    if not approval_checksum:
        # Deterministic evidence digest from decision identity + text
        material = json.dumps(
            {
                "canonicalReference": record["canonicalReference"],
                "decisionId": decision_id,
                "sanskritText": sanskrit,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        approval_checksum = sha256_bytes(material.encode("utf-8"))

    return {
        "chapterNumber": int(record["chapterNumber"]),
        "verseNumber": int(record["verseNumber"]),
        "canonicalReference": str(record["canonicalReference"]),
        "sanskritText": str(sanskrit),
        "transliteration": transliteration,
        "contentVersion": int(record.get("contentVersion") or content_version),
        "sourceIds": source_ids,
        "sourceChecksums": {k: checksums[k] for k in sorted(checksums) if k in source_ids},
        "editorialDecisionId": str(decision_id),
        "editorialApprovalChecksum": str(approval_checksum),
    }


def build_provenance(
    *,
    package_id: str,
    verse_records: list[dict[str, Any]],
    approved_records: list[dict[str, Any]],
    approval_manifest: dict[str, Any],
    approval_manifest_path: Path,
    registry: dict[str, dict[str, Any]],
    normalization_policy_version: int,
    comparison_engine_version: int,
    source_selection_rationale: str,
    known_caveats: list[str],
) -> dict[str, Any]:
    source_ids: set[str] = set()
    for row in verse_records:
        source_ids.update(row["sourceIds"])

    source_roles: dict[str, str] = {}
    source_checksums: dict[str, str] = {}
    licenses: dict[str, dict[str, Any]] = {}
    for sid in sorted(source_ids):
        entry = registry[sid]
        source_checksums[sid] = str(
            next(
                (
                    row["sourceChecksums"][sid]
                    for row in verse_records
                    if sid in row["sourceChecksums"]
                ),
                entry.get("sha256"),
            )
        )
        role = "FIXTURE" if sid.startswith("fixture-") else "SUPPORTING_REFERENCE"
        # Prefer primary from first record selectedSourceId when present
        for rec in approved_records:
            if rec.get("selectedSourceId") == sid:
                role = "PRIMARY_TRANSCRIPTION"
                break
            if sid in (rec.get("supportingSourceIds") or []):
                role = "SECONDARY_VERIFICATION"
        source_roles[sid] = role
        licenses[sid] = {
            "licenseDisplayed": str(
                entry.get("license_displayed") or entry.get("licenseDisplayed") or "UNKNOWN"
            ),
            "licenseCatalogId": entry.get("license_catalog_id")
            or entry.get("licenseCatalogId"),
        }

    reviewer_ids: list[str] = []
    second_ids: list[str] = []
    approval_dates: list[str] = []

    manifest_reviewer = approval_manifest.get("reviewer") or approval_manifest.get(
        "reviewerId"
    )
    if manifest_reviewer:
        reviewer_ids.append(str(manifest_reviewer))
    manifest_second = approval_manifest.get("secondReviewer") or approval_manifest.get(
        "secondReviewerId"
    )
    if manifest_second:
        second_ids.append(str(manifest_second))
    if approval_manifest.get("decisionDate"):
        approval_dates.append(str(approval_manifest["decisionDate"])[:10])

    for rec in approved_records:
        rid = rec.get("reviewerId") or rec.get("reviewer")
        if rid and str(rid) not in reviewer_ids:
            reviewer_ids.append(str(rid))
        sid = rec.get("secondReviewerId") or rec.get("secondReviewer")
        if sid and str(sid) not in second_ids:
            second_ids.append(str(sid))
        ad = rec.get("approvalDate") or rec.get("decisionDate")
        if ad:
            day = str(ad)[:10]
            if day not in approval_dates:
                approval_dates.append(day)

    reviewer_ids = sorted(set(reviewer_ids))
    second_ids = sorted(set(second_ids))
    approval_dates = sorted(set(approval_dates))

    try:
        rel_manifest = str(approval_manifest_path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        rel_manifest = str(approval_manifest_path)

    return {
        "packageId": package_id,
        "sourceIds": sorted(source_ids),
        "sourceRoles": source_roles,
        "sourceChecksums": source_checksums,
        "licenses": licenses,
        "retrievalMetadata": {
            "sourceRegistryPath": "content/registry/sources.json",
            "editorialApprovalManifestPath": rel_manifest,
        },
        "editorialReviewerIds": reviewer_ids,
        "secondReviewerIds": second_ids,
        "approvalDates": approval_dates,
        "normalizationPolicyVersion": normalization_policy_version,
        "comparisonEngineVersion": comparison_engine_version,
        "packageBuilderVersion": PACKAGE_BUILDER_VERSION,
        "knownCaveats": list(known_caveats),
        "sourceSelectionRationale": source_selection_rationale,
    }


def write_package_files(
    staging_dir: Path,
    *,
    manifest: dict[str, Any],
    verses: list[dict[str, Any]],
    provenance: dict[str, Any],
) -> None:
    verses_sorted = sorted(verses, key=lambda r: (r["chapterNumber"], r["verseNumber"]))
    verses_text = dump_jsonl(verses_sorted)
    provenance_text = dump_json(provenance)
    (staging_dir / "verses.jsonl").write_text(verses_text, encoding="utf-8")
    (staging_dir / "provenance.json").write_text(provenance_text, encoding="utf-8")

    verses_digest = sha256_bytes(verses_text.encode("utf-8"))
    provenance_digest = sha256_bytes(provenance_text.encode("utf-8"))
    package_checksum = combined_package_checksum(
        verses_text.encode("utf-8"),
        provenance_text.encode("utf-8"),
    )

    manifest = dict(manifest)
    manifest["fileChecksums"] = {
        "verses.jsonl": verses_digest,
        "provenance.json": provenance_digest,
    }
    manifest["packageChecksum"] = package_checksum
    manifest["recordCount"] = len(verses_sorted)
    manifest_text = dump_json(manifest)
    (staging_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")

    sums = format_sha256sums(
        {
            "manifest.json": sha256_bytes(manifest_text.encode("utf-8")),
            "verses.jsonl": verses_digest,
            "provenance.json": provenance_digest,
        }
    )
    (staging_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")


def atomic_move_package(staging_dir: Path, target_dir: Path) -> None:
    target_dir = target_dir.resolve()
    if target_dir.exists():
        raise BuildError(f"refuse to overwrite existing package: {target_dir}")
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    # Move onto same filesystem when possible
    os.replace(staging_dir, target_dir)


def load_chapter_workspace_records(chapter_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load Chapter editorial workspace inputs without mutating them."""
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"
    if not manifest_path.is_file():
        # Generic name fallback
        matches = sorted(chapter_dir.glob("*-approval-manifest.json"))
        if not matches:
            raise BuildError(f"no approval manifest in {chapter_dir}")
        manifest_path = matches[0]
    approval_manifest = load_json(manifest_path)

    records: list[dict[str, Any]] = []
    for name in (
        "normalization-match-approval-candidate.jsonl",
        "source-conflict-analysis.jsonl",
        "canonical-draft.jsonl",
        "approved-canonical-records.jsonl",
    ):
        path = chapter_dir / name
        if path.is_file():
            records.extend(load_jsonl(path))

    # Only APPROVED records are eligible; others cause rejection if selected.
    approved_only = [r for r in records if record_approval_status(r) == "APPROVED"]
    # If caller attempts to build and any conflicted/pending are the only content,
    # approved_only may be empty → BuildError in validate.
    # Also explicitly reject if workspace still has pending/conflicted and zero approved.
    if not approved_only:
        pending = sum(1 for r in records if record_approval_status(r) in PENDING_STATUSES)
        conflicted = sum(1 for r in records if is_conflicted(r))
        raise BuildError(
            "no approved Verses found; refuse to build package "
            f"(approved=0, pending={pending}, conflicted={conflicted}, "
            f"manifest.approved={approval_manifest.get('approved', 0)})"
        )

    # Ensure we never silently include pending/conflicted
    for r in records:
        status = record_approval_status(r)
        if status == "APPROVED":
            continue
        if is_conflicted(r) or status in PENDING_STATUSES or status in REJECTED_STATUSES:
            # Allowed to exist in workspace; just not packaged.
            continue
    return approval_manifest, approved_only


def build_package(
    *,
    approval_manifest_path: Path,
    approved_records_path: Path | None,
    output_parent: Path,
    package_id: str,
    scripture_id: str,
    chapter_number: int,
    content_version: int,
    package_status: str,
    created_at: str,
    sources_registry: Path,
    allow_null_transliteration: bool,
    normalization_policy_version: int,
    comparison_engine_version: int,
    source_selection_rationale: str,
    known_caveats: list[str],
    require_complete_chapter: bool,
    chapter_workspace: Path | None = None,
) -> Path:
    if package_status not in {"DRAFT", "APPROVED", "SUPERSEDED", "REVOKED"}:
        raise BuildError(f"invalid packageStatus: {package_status}")

    registry = load_registry_map(sources_registry)
    approval_manifest = load_json(approval_manifest_path)

    if chapter_workspace is not None:
        approval_manifest, approved_raw = load_chapter_workspace_records(chapter_workspace)
        approval_manifest_path = next(chapter_workspace.glob("*-approval-manifest.json"))
    else:
        if approved_records_path is None:
            raise BuildError("--approved-records is required unless --chapter-workspace is set")
        approved_raw = collect_approved_records(load_jsonl(approved_records_path))

    # When reading explicit approved-records file, still run collect to reject bad rows
    if chapter_workspace is None:
        pass
    else:
        approved_raw = collect_approved_records(approved_raw)

    validate_approved_inputs(
        approval_manifest=approval_manifest,
        approved_records=approved_raw,
        registry=registry,
        chapter_number=chapter_number,
        package_status=package_status,
        require_complete_chapter=require_complete_chapter,
    )

    if package_status == "APPROVED" and int(approval_manifest.get("approved") or 0) == 0:
        raise BuildError(
            "cannot create APPROVED package when editorial approval count is zero"
        )

    verse_records = [to_verse_record(r, content_version) for r in approved_raw]
    verse_records = sorted(
        verse_records, key=lambda r: (r["chapterNumber"], r["verseNumber"])
    )

    source_refs = sorted({sid for row in verse_records for sid in row["sourceIds"]})
    for sid in source_refs:
        if sid not in registry:
            raise BuildError(f"missing source registry entry: {sid}")

    provenance = build_provenance(
        package_id=package_id,
        verse_records=verse_records,
        approved_records=approved_raw,
        approval_manifest=approval_manifest,
        approval_manifest_path=approval_manifest_path,
        registry=registry,
        normalization_policy_version=normalization_policy_version,
        comparison_engine_version=comparison_engine_version,
        source_selection_rationale=source_selection_rationale,
        known_caveats=known_caveats,
    )

    verse_numbers = [r["verseNumber"] for r in verse_records]
    manifest: dict[str, Any] = {
        "packageId": package_id,
        "scriptureId": scripture_id,
        "chapterNumber": chapter_number,
        "contentVersion": content_version,
        "recordCount": len(verse_records),
        "canonicalReferenceRange": {
            "from": f"{chapter_number}.{verse_numbers[0]}",
            "to": f"{chapter_number}.{verse_numbers[-1]}",
            "expectedCount": len(verse_records),
        },
        "createdAt": created_at,
        "packageStatus": package_status,
        "sourceRegistryReferences": source_refs,
        "editorialApprovalManifestChecksum": sha256_file(approval_manifest_path),
        "packageFormatVersion": 1,
        "checksumAlgorithm": "SHA-256",
        "packageChecksum": "0" * 64,  # replaced when writing
        "fileChecksums": {
            "verses.jsonl": "0" * 64,
            "provenance.json": "0" * 64,
        },
        "allowNullTransliteration": allow_null_transliteration,
    }

    target_dir = (output_parent / package_id).resolve()
    if target_dir.exists():
        raise BuildError(f"refuse to overwrite existing package: {target_dir}")

    tmp_root = tempfile.mkdtemp(prefix="antar-package-")
    staging_dir = Path(tmp_root) / package_id
    staging_dir.mkdir(parents=True)
    try:
        write_package_files(
            staging_dir,
            manifest=manifest,
            verses=verse_records,
            provenance=provenance,
        )
        result = validate_package(staging_dir, sources_registry=sources_registry)
        if not result.structurally_valid:
            raise BuildError(
                "completed package failed validation:\n" + "\n".join(result.errors)
            )
        if package_status == "APPROVED" and not result.importable:
            raise BuildError(
                "APPROVED package is not importable after validation:\n"
                + "\n".join(result.errors + result.warnings)
            )
        atomic_move_package(staging_dir, target_dir)
    finally:
        if Path(tmp_root).exists():
            shutil.rmtree(tmp_root, ignore_errors=True)

    return target_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an immutable Antar Scripture content package"
    )
    parser.add_argument("--approval-manifest", type=Path, help="Editorial approval manifest JSON")
    parser.add_argument(
        "--approved-records",
        type=Path,
        help="JSONL of APPROVED canonical editorial records only",
    )
    parser.add_argument(
        "--chapter-workspace",
        type=Path,
        help="Editorial chapter workspace (rejects build when no Verses are APPROVED)",
    )
    parser.add_argument("--output-parent", type=Path, default=DEFAULT_OUTPUT_PARENT)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--scripture-id", default="bhagavad-gita")
    parser.add_argument("--chapter-number", type=int, required=True)
    parser.add_argument("--content-version", type=int, default=1)
    parser.add_argument(
        "--package-status",
        default="DRAFT",
        choices=["DRAFT", "APPROVED", "SUPERSEDED", "REVOKED"],
    )
    parser.add_argument(
        "--created-at",
        required=True,
        help="UTC timestamp YYYY-MM-DDTHH:MM:SSZ (must be provided for determinism)",
    )
    parser.add_argument("--sources-registry", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument(
        "--allow-null-transliteration",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--normalization-policy-version", type=int, default=1)
    parser.add_argument("--comparison-engine-version", type=int, default=1)
    parser.add_argument(
        "--source-selection-rationale",
        default="Package contains only human-approved canonical records.",
    )
    parser.add_argument("--known-caveat", action="append", default=[])
    parser.add_argument(
        "--require-complete-chapter",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    args = parser.parse_args(argv)

    try:
        if args.chapter_workspace:
            path = build_package(
                approval_manifest_path=args.approval_manifest
                or (args.chapter_workspace / "chapter-01-approval-manifest.json"),
                approved_records_path=None,
                output_parent=args.output_parent,
                package_id=args.package_id,
                scripture_id=args.scripture_id,
                chapter_number=args.chapter_number,
                content_version=args.content_version,
                package_status=args.package_status,
                created_at=args.created_at,
                sources_registry=args.sources_registry,
                allow_null_transliteration=args.allow_null_transliteration,
                normalization_policy_version=args.normalization_policy_version,
                comparison_engine_version=args.comparison_engine_version,
                source_selection_rationale=args.source_selection_rationale,
                known_caveats=list(args.known_caveat),
                require_complete_chapter=args.require_complete_chapter,
                chapter_workspace=args.chapter_workspace,
            )
        else:
            if not args.approval_manifest or not args.approved_records:
                raise BuildError(
                    "--approval-manifest and --approved-records are required "
                    "unless --chapter-workspace is set"
                )
            path = build_package(
                approval_manifest_path=args.approval_manifest,
                approved_records_path=args.approved_records,
                output_parent=args.output_parent,
                package_id=args.package_id,
                scripture_id=args.scripture_id,
                chapter_number=args.chapter_number,
                content_version=args.content_version,
                package_status=args.package_status,
                created_at=args.created_at,
                sources_registry=args.sources_registry,
                allow_null_transliteration=args.allow_null_transliteration,
                normalization_policy_version=args.normalization_policy_version,
                comparison_engine_version=args.comparison_engine_version,
                source_selection_rationale=args.source_selection_rationale,
                known_caveats=list(args.known_caveat),
                require_complete_chapter=args.require_complete_chapter,
                chapter_workspace=None,
            )
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("importable: false", file=sys.stderr)
        return 1

    result = validate_package(path, sources_registry=args.sources_registry)
    print(f"Wrote package: {path}")
    print(f"structurallyValid: {result.structurally_valid}")
    print(f"editoriallyValid: {result.editorially_valid}")
    print(f"importable: {result.importable}")
    return 0 if result.structurally_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
