#!/usr/bin/env python3
"""Validate an Antar immutable Translation content package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FILES = ("manifest.json", "translations.jsonl", "provenance.json", "SHA256SUMS")
ALLOWED_STATUSES = frozenset({"DRAFT", "APPROVED", "SUPERSEDED", "REVOKED"})
FORBIDDEN_KEYS = frozenset({
    "sanskrit", "sanskritText", "commentary", "commentaries", "notes",
    "approvalStatus", "reviewStatus", "status", "auditLog", "editorialNotes",
})
UNSAFE_RE = re.compile(r"(?i)\b(TODO|FIXME|lorem ipsum|tbd|xxx|insert text here)\b")
PACKAGE_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CREATED_AT_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def parse_sums(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, name = line.strip().split(None, 1)
        out[name] = digest.lower()
    return out


def is_editorial(msg: str) -> bool:
    return (
        "APPROVED package missing" in msg
        or "editorialDecisionId" in msg
        or "editorialApprovalChecksum" in msg
        or "unresolved source" in msg
    )


def validate(package_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not package_dir.is_dir():
        return {
            "structurallyValid": False,
            "editoriallyValid": False,
            "importable": False,
            "errors": ["package directory does not exist"],
            "warnings": [],
        }

    present = {p.name for p in package_dir.iterdir() if p.is_file()}
    for req in REQUIRED_FILES:
        if req not in present:
            errors.append(f"missing required file: {req}")
    for name in present:
        if name not in REQUIRED_FILES:
            errors.append(f"unexpected file: {name}")
    if errors:
        return _result(False, False, False, errors, warnings)

    manifest_bytes = (package_dir / "manifest.json").read_bytes()
    translations_bytes = (package_dir / "translations.jsonl").read_bytes()
    provenance_bytes = (package_dir / "provenance.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    provenance = json.loads(provenance_bytes)
    rows = load_jsonl(package_dir / "translations.jsonl")
    sums = parse_sums((package_dir / "SHA256SUMS").read_text(encoding="utf-8"))

    package_id = manifest.get("packageId")
    if package_id != package_dir.name:
        errors.append(
            f"packageId '{package_id}' does not match directory name '{package_dir.name}'"
        )

    actual = {
        "manifest.json": sha256_bytes(manifest_bytes),
        "translations.jsonl": sha256_bytes(translations_bytes),
        "provenance.json": sha256_bytes(provenance_bytes),
    }
    if set(sums) != set(actual):
        errors.append(
            "SHA256SUMS must list exactly manifest.json, provenance.json, translations.jsonl"
        )
    for name, digest in actual.items():
        if sums.get(name) != digest:
            errors.append(f"checksum mismatch for {name}")

    expected_pkg = sha256_bytes(translations_bytes + provenance_bytes)
    if manifest.get("packageChecksum") != expected_pkg:
        errors.append("manifest.packageChecksum does not match canonical combined checksum")

    for name in ("translations.jsonl", "provenance.json"):
        if (manifest.get("fileChecksums") or {}).get(name) != actual[name]:
            errors.append(f"manifest.fileChecksums mismatch for {name}")

    status = manifest.get("packageStatus")
    if status not in ALLOWED_STATUSES:
        errors.append(f"packageStatus '{status}' is not allowed")

    if manifest.get("recordCount") != len(rows):
        errors.append("recordCount != translations.jsonl length")

    if not PACKAGE_ID_RE.match(str(package_id or "")):
        errors.append("packageId has invalid format")
    if not CREATED_AT_RE.match(str(manifest.get("createdAt") or "")):
        errors.append("createdAt must be UTC Zulu timestamp")
    if manifest.get("packageFormatVersion") != 1:
        errors.append("packageFormatVersion must be 1")
    if manifest.get("checksumAlgorithm") != "SHA-256":
        errors.append("checksumAlgorithm must be SHA-256")
    for field in ("language", "provider", "sourceName", "licenseType", "scriptureId"):
        if not str(manifest.get(field) or "").strip():
            errors.append(f"{field} is required")

    chapter = manifest.get("chapterNumber")
    verse_numbers: list[int] = []
    seen: set[str] = set()
    for i, row in enumerate(rows):
        for key in row:
            if key in FORBIDDEN_KEYS:
                errors.append(f"translations.jsonl[{i}]: forbidden fields present: [{key}]")
        ref = row.get("canonicalReference")
        ch = row.get("chapterNumber")
        vn = row.get("verseNumber")
        if ch != chapter:
            errors.append(f"translations.jsonl[{i}]: chapterNumber mismatch")
        if ref != f"{ch}.{vn}":
            errors.append(f"translations.jsonl[{i}]: canonicalReference mismatch")
        text = row.get("translationText") or ""
        if not text.strip():
            errors.append(f"translations.jsonl[{i}]: translationText must be nonblank")
        elif UNSAFE_RE.search(text):
            errors.append(
                f"translations.jsonl[{i}]: unsafe placeholder markers in translationText"
            )
        if ref in seen:
            errors.append(f"duplicate Verse canonicalReference: {ref}")
        else:
            seen.add(str(ref))
            verse_numbers.append(int(vn))

    ref_range = manifest.get("canonicalReferenceRange") or {}
    if verse_numbers:
        sorted_ns = sorted(verse_numbers)
        expected_from = f"{chapter}.{sorted_ns[0]}"
        expected_to = f"{chapter}.{sorted_ns[-1]}"
        if ref_range.get("from") != expected_from or ref_range.get("to") != expected_to:
            errors.append("canonicalReferenceRange mismatch")
        if ref_range.get("expectedCount") != len(verse_numbers):
            errors.append("canonicalReferenceRange.expectedCount != record count")

    if provenance.get("packageId") != package_id:
        errors.append("provenance.packageId does not match manifest.packageId")

    if status == "APPROVED":
        if not provenance.get("editorialReviewerIds"):
            errors.append("APPROVED package missing editorialReviewerIds")
        if not provenance.get("approvalDates"):
            errors.append("APPROVED package missing approvalDates")
        if not SHA_RE.match(str(manifest.get("editorialApprovalManifestChecksum") or "")):
            errors.append("APPROVED package missing editorialApprovalManifestChecksum")
        for i, row in enumerate(rows):
            if not row.get("editorialDecisionId"):
                errors.append(
                    f"translations.jsonl[{i}]: APPROVED package missing editorialDecisionId"
                )
            if not SHA_RE.match(str(row.get("editorialApprovalChecksum") or "")):
                errors.append(
                    f"translations.jsonl[{i}]: APPROVED package missing editorialApprovalChecksum"
                )

    structurally_valid = not any(not is_editorial(e) for e in errors)
    editorially_valid = structurally_valid and not any(is_editorial(e) for e in errors)
    importable = status == "APPROVED" and structurally_valid and editorially_valid
    if status != "APPROVED":
        importable = False
        if status == "DRAFT":
            warnings.append("DRAFT package is never importable")

    return _result(structurally_valid, editorially_valid, importable, errors, warnings)


def _result(
    structurally_valid: bool,
    editorially_valid: bool,
    importable: bool,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "structurallyValid": structurally_valid,
        "editoriallyValid": editorially_valid,
        "importable": importable,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", type=Path)
    args = parser.parse_args()
    outcome = validate(args.package_dir.resolve())
    print(json.dumps(outcome, indent=2, sort_keys=True))
    return 0 if outcome["structurallyValid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
