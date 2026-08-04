#!/usr/bin/env python3
"""Validate an Antar immutable Scripture content package.

Returns structurallyValid / editoriallyValid / importable.
Package validation is not scholarly approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from schema_validate import load_schema, validate_instance  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGES_ROOT = REPO_ROOT / "content/packages"
SCHEMA_DIR = PACKAGES_ROOT / "schema"
DEFAULT_SOURCES = REPO_ROOT / "content/registry/sources.json"
VERSE_COUNTS_PATH = REPO_ROOT / "content/validation/antar_verse_counts.json"

REQUIRED_FILES = ("manifest.json", "verses.jsonl", "provenance.json", "SHA256SUMS")
ALLOWED_STATUSES = frozenset({"DRAFT", "APPROVED", "SUPERSEDED", "REVOKED"})
FORBIDDEN_VERSE_KEYS = frozenset(
    {
        "translation",
        "translations",
        "commentary",
        "commentaries",
        "approvalStatus",
        "reviewStatus",
        "status",
        "auditLog",
        "editorialNotes",
        "placeholder",
    }
)
PLACEHOLDER_RE = re.compile(
    r"(?i)\b(TODO|FIXME|placeholder|lorem ipsum|tbd|xxx|insert text here)\b"
)
PACKAGE_BUILDER_VERSION = 1


class PackageValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.structurally_valid = False
        self.editorially_valid = False
        self.importable = False

    def error(self, message: str) -> None:
        self.errors.append(message)

    def as_dict(self) -> dict[str, Any]:
        return {
            "structurallyValid": self.structurally_valid,
            "editoriallyValid": self.editorially_valid,
            "importable": self.importable,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: line {line_no}: {exc}") from exc
    return rows


def load_source_ids(registry_path: Path) -> set[str]:
    data = load_json(registry_path)
    sources = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(sources, list):
        raise ValueError(f"{registry_path}: expected sources array")
    return {str(s["id"]) for s in sources if isinstance(s, dict) and "id" in s}


def expected_verse_count(chapter_number: int) -> int | None:
    if not VERSE_COUNTS_PATH.is_file():
        return None
    data = load_json(VERSE_COUNTS_PATH)
    counts = data.get("verse_counts") or {}
    value = counts.get(str(chapter_number))
    return int(value) if value is not None else None


def parse_sha256sums(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"SHA256SUMS line {line_no}: expected '<hash>  <filename>'")
        digest, name = parts[0].strip(), parts[1].strip()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError(f"SHA256SUMS line {line_no}: invalid sha256 digest")
        if name in mapping:
            raise ValueError(f"SHA256SUMS duplicate filename {name!r}")
        mapping[name] = digest
    return mapping


def combined_package_checksum(verses_bytes: bytes, provenance_bytes: bytes) -> str:
    """Canonical order: verses.jsonl then provenance.json."""
    return sha256_bytes(verses_bytes + provenance_bytes)


def format_sha256sums(file_digests: dict[str, str]) -> str:
    lines = [f"{file_digests[name]}  {name}" for name in sorted(file_digests)]
    return "\n".join(lines) + "\n"


def validate_package(
    package_dir: Path,
    *,
    sources_registry: Path = DEFAULT_SOURCES,
    require_registry: bool = True,
) -> PackageValidationResult:
    result = PackageValidationResult()
    package_dir = package_dir.resolve()

    if not package_dir.is_dir():
        result.error(f"package directory does not exist: {package_dir}")
        return result

    present = {p.name for p in package_dir.iterdir() if p.is_file()}
    for name in REQUIRED_FILES:
        if name not in present:
            result.error(f"missing required file: {name}")
    unexpected = sorted(present - set(REQUIRED_FILES))
    for name in unexpected:
        result.error(f"unexpected file: {name}")
    if result.errors:
        return result

    try:
        manifest = load_json(package_dir / "manifest.json")
        verses = load_jsonl(package_dir / "verses.jsonl")
        provenance = load_json(package_dir / "provenance.json")
        sums = parse_sha256sums((package_dir / "SHA256SUMS").read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result.error(f"failed to parse package files: {exc}")
        return result

    # Schema checks
    schemas = {
        "manifest": load_schema(SCHEMA_DIR / "package-manifest.schema.json"),
        "verse": load_schema(SCHEMA_DIR / "verse-record.schema.json"),
        "provenance": load_schema(SCHEMA_DIR / "provenance.schema.json"),
        "checksums": load_schema(SCHEMA_DIR / "checksums.schema.json"),
    }
    for err in validate_instance(manifest, schemas["manifest"]):
        result.error(f"manifest schema: {err}")
    for err in validate_instance(provenance, schemas["provenance"]):
        result.error(f"provenance schema: {err}")
    for i, row in enumerate(verses):
        for err in validate_instance(row, schemas["verse"]):
            result.error(f"verses.jsonl[{i}] schema: {err}")

    checksum_meta = {
        "checksumAlgorithm": "SHA-256",
        "sha256sumsFilenames": ["manifest.json", "provenance.json", "verses.jsonl"],
        "canonicalPackageChecksumOrder": ["verses.jsonl", "provenance.json"],
        "sha256sumsLineFormat": "<sha256><two-spaces><filename>\\n",
    }
    for err in validate_instance(checksum_meta, schemas["checksums"]):
        result.error(f"checksums schema: {err}")

    # Directory / package ID alignment
    package_id = manifest.get("packageId")
    if package_id != package_dir.name:
        result.error(
            f"packageId {package_id!r} does not match directory name {package_dir.name!r}"
        )

    # Checksums
    actual = {
        "manifest.json": sha256_file(package_dir / "manifest.json"),
        "verses.jsonl": sha256_file(package_dir / "verses.jsonl"),
        "provenance.json": sha256_file(package_dir / "provenance.json"),
    }
    if set(sums.keys()) != set(REQUIRED_FILES) - {"SHA256SUMS"}:
        result.error(
            f"SHA256SUMS must list exactly manifest.json, provenance.json, verses.jsonl; "
            f"got {sorted(sums)}"
        )
    for name, digest in actual.items():
        if sums.get(name) != digest:
            result.error(f"checksum mismatch for {name}")

    file_checksums = manifest.get("fileChecksums") or {}
    for name in ("verses.jsonl", "provenance.json"):
        if file_checksums.get(name) != actual[name]:
            result.error(f"manifest.fileChecksums mismatch for {name}")

    expected_pkg = combined_package_checksum(
        (package_dir / "verses.jsonl").read_bytes(),
        (package_dir / "provenance.json").read_bytes(),
    )
    if manifest.get("packageChecksum") != expected_pkg:
        result.error("manifest.packageChecksum does not match canonical combined checksum")

    # Status
    status = manifest.get("packageStatus")
    if status not in ALLOWED_STATUSES:
        result.error(f"packageStatus {status!r} is not allowed")

    # Record count / references
    if manifest.get("recordCount") != len(verses):
        result.error(
            f"recordCount {manifest.get('recordCount')} != verses.jsonl length {len(verses)}"
        )

    chapter = manifest.get("chapterNumber")
    ref_range = manifest.get("canonicalReferenceRange") or {}
    refs: list[str] = []
    seen: set[str] = set()
    source_ids_used: set[str] = set()
    allow_null_tl = bool(manifest.get("allowNullTransliteration"))

    for i, row in enumerate(verses):
        ref = row.get("canonicalReference")
        ch = row.get("chapterNumber")
        vn = row.get("verseNumber")
        if ch != chapter:
            result.error(f"verses.jsonl[{i}]: chapterNumber {ch} != manifest {chapter}")
        expected_ref = f"{ch}.{vn}"
        if ref != expected_ref:
            result.error(
                f"verses.jsonl[{i}]: canonicalReference {ref!r} != {expected_ref!r}"
            )
        if not isinstance(row.get("sanskritText"), str) or not row["sanskritText"].strip():
            result.error(f"verses.jsonl[{i}]: sanskritText must be nonblank")
        if PLACEHOLDER_RE.search(row.get("sanskritText") or ""):
            result.error(f"verses.jsonl[{i}]: placeholder text detected in sanskritText")
        tl = row.get("transliteration")
        if tl is None:
            if not allow_null_tl:
                result.error(f"verses.jsonl[{i}]: transliteration null but policy forbids it")
        elif not isinstance(tl, str) or not tl.strip():
            result.error(f"verses.jsonl[{i}]: transliteration must be nonblank string or null")
        elif PLACEHOLDER_RE.search(tl):
            result.error(f"verses.jsonl[{i}]: placeholder text detected in transliteration")

        forbidden = FORBIDDEN_VERSE_KEYS.intersection(row.keys())
        if forbidden:
            result.error(f"verses.jsonl[{i}]: forbidden fields present: {sorted(forbidden)}")

        if ref in seen:
            result.error(f"duplicate Verse canonicalReference: {ref}")
        else:
            seen.add(str(ref))
            refs.append(str(ref))

        for sid in row.get("sourceIds") or []:
            source_ids_used.add(str(sid))
        checksums = row.get("sourceChecksums") or {}
        for sid in row.get("sourceIds") or []:
            if sid not in checksums:
                result.error(f"verses.jsonl[{i}]: missing sourceChecksums entry for {sid}")

    # Completeness of chapter range
    if refs:
        verse_numbers: list[int] = []
        for r in refs:
            parts = r.split(".", 1)
            if len(parts) != 2 or not parts[1].isdigit():
                result.error(f"canonicalReference is not chapter.verse: {r!r}")
                continue
            verse_numbers.append(int(parts[1]))
        if verse_numbers and len(verse_numbers) == len(refs):
            verse_numbers = sorted(verse_numbers)
            expected_from = f"{chapter}.{verse_numbers[0]}"
            expected_to = f"{chapter}.{verse_numbers[-1]}"
            if ref_range.get("from") != expected_from or ref_range.get("to") != expected_to:
                result.error(
                    f"canonicalReferenceRange mismatch: manifest {ref_range} "
                    f"vs data {expected_from}..{expected_to}"
                )
            if ref_range.get("expectedCount") != len(refs):
                result.error("canonicalReferenceRange.expectedCount != record count")
            contiguous = list(range(verse_numbers[0], verse_numbers[0] + len(verse_numbers)))
            if verse_numbers != contiguous:
                result.error(f"Verse numbers are not contiguous: {verse_numbers}")

    antar_count = expected_verse_count(int(chapter)) if isinstance(chapter, int) else None
    declared_full_chapter = bool(
        antar_count is not None
        and ref_range.get("from") == f"{chapter}.1"
        and ref_range.get("to") == f"{chapter}.{antar_count}"
        and ref_range.get("expectedCount") == antar_count
    )
    if antar_count is not None and len(verses) != antar_count:
        if status == "APPROVED" and declared_full_chapter:
            result.error(
                f"APPROVED full-chapter package for chapter {chapter} must contain "
                f"{antar_count} Verses, found {len(verses)}"
            )
        else:
            result.warnings.append(
                f"chapter {chapter} Antar full count is {antar_count}; "
                f"package has {len(verses)}"
            )

    # Source registry resolution
    registry_ids: set[str] = set()
    if require_registry:
        try:
            registry_ids = load_source_ids(sources_registry)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            result.error(f"failed to load source registry: {exc}")
        else:
            for sid in sorted(source_ids_used | set(manifest.get("sourceRegistryReferences") or [])):
                if sid not in registry_ids:
                    result.error(f"unresolved source ID: {sid}")
            for sid in provenance.get("sourceIds") or []:
                if sid not in registry_ids:
                    result.error(f"provenance unresolved source ID: {sid}")

    if provenance.get("packageId") != package_id:
        result.error("provenance.packageId does not match manifest.packageId")

    structural_error_prefixes = (
        "missing required file",
        "unexpected file",
        "failed to parse",
        "manifest schema",
        "verses.jsonl[",
        "provenance schema",
        "checksums schema",
        "packageId",
        "checksum mismatch",
        "SHA256SUMS",
        "manifest.fileChecksums",
        "manifest.packageChecksum",
        "packageStatus",
        "recordCount",
        "canonicalReferenceRange",
        "Verse numbers",
        "duplicate Verse",
        "forbidden fields",
        "placeholder text",
        "sanskritText must",
        "transliteration",
        "chapterNumber",
    )
    structural_ok = not any(
        e.startswith(structural_error_prefixes) or "schema:" in e or "canonicalReference" in e
        for e in result.errors
    )
    # Recompute structural more carefully: any error so far that is not purely editorial
    editorial_only_markers = (
        "unresolved source",
        "APPROVED package",
        "editorial evidence",
        "missing reviewer",
        "importable",
    )
    non_editorial = [
        e
        for e in result.errors
        if not any(m in e for m in editorial_only_markers)
    ]
    result.structurally_valid = len(non_editorial) == 0

    # Editorial validity
    editorial_ok = result.structurally_valid
    if status == "APPROVED":
        if not provenance.get("editorialReviewerIds"):
            result.error("APPROVED package missing editorialReviewerIds")
            editorial_ok = False
        if not provenance.get("approvalDates"):
            result.error("APPROVED package missing approvalDates")
            editorial_ok = False
        if not manifest.get("editorialApprovalManifestChecksum"):
            result.error("APPROVED package missing editorialApprovalManifestChecksum")
            editorial_ok = False
        for i, row in enumerate(verses):
            if not row.get("editorialDecisionId"):
                result.error(f"verses.jsonl[{i}]: APPROVED package missing editorialDecisionId")
                editorial_ok = False
            if not row.get("editorialApprovalChecksum"):
                result.error(
                    f"verses.jsonl[{i}]: APPROVED package missing editorialApprovalChecksum"
                )
                editorial_ok = False
        if declared_full_chapter and antar_count is not None and len(verses) != antar_count:
            editorial_ok = False
    if any("unresolved source" in e for e in result.errors):
        editorial_ok = False

    # Refresh editorial_ok from accumulated errors after structural filter
    editorial_errors = [
        e
        for e in result.errors
        if any(m in e for m in editorial_only_markers) or "APPROVED package" in e
    ]
    result.editorially_valid = result.structurally_valid and not editorial_errors and editorial_ok

    # Importable: only APPROVED + structurally + editorially valid
    if status != "APPROVED":
        result.importable = False
        if status == "DRAFT":
            result.warnings.append("DRAFT package is never importable")
    else:
        result.importable = result.structurally_valid and result.editorially_valid

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Antar Scripture content package")
    parser.add_argument("package_dir", type=Path, help="Path to package directory")
    parser.add_argument(
        "--sources-registry",
        type=Path,
        default=DEFAULT_SOURCES,
        help="Path to content/registry/sources.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable validation result JSON",
    )
    args = parser.parse_args(argv)
    result = validate_package(args.package_dir, sources_registry=args.sources_registry)
    payload = result.as_dict()
    if args.json:
        print(dump_json(payload), end="")
    else:
        for err in result.errors:
            print(f"ERROR: {err}")
        for warn in result.warnings:
            print(f"WARNING: {warn}")
        print(f"structurallyValid: {payload['structurallyValid']}")
        print(f"editoriallyValid: {payload['editoriallyValid']}")
        print(f"importable: {payload['importable']}")
    return 0 if result.structurally_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
