#!/usr/bin/env python3
"""Validate Antar Translation segment-draft / coverage workspace files.

Read-only with respect to content/raw/. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = frozenset(
    {
        "UNREVIEWED",
        "READY_FOR_REVIEW",
        "SOURCE_CONFLICT",
        "APPROVED",
        "REJECTED",
    }
)

# Heuristic leakage detectors (not perfect; editorial review still required).
COMMENTARY_MARKERS = re.compile(r"(?m)^\s*\[|\]\s*$|^\s*\[[^\]]{20,}\]")
WORD_BY_WORD_HINT = re.compile(
    r"\b(उवाच|अर्जुन|संजय|धृतराष्ट्र)\s+[A-Za-z]|"
    r"\b(said\s*:)\s*[A-Za-z]*\s*(O |the |having |with )",
    re.I,
)


class ValidationError(Exception):
    """Fatal validation failure."""


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValidationError(f"Missing JSONL: {path}")
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{path}:{i}: invalid JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValidationError(f"{path}:{i}: each line must be a JSON object")
        rows.append(obj)
    return rows


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"Missing JSON: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValidationError(f"{path} root must be an object")
    return payload


def canonical_refs(chapter: int, verses: list[int]) -> list[str]:
    return [f"{chapter}.{v}" for v in verses]


def verses_contiguous(verses: list[int]) -> bool:
    if not verses:
        return False
    ordered = sorted(verses)
    return ordered == list(range(ordered[0], ordered[-1] + 1)) and ordered == verses


def looks_like_commentary(text: str) -> bool:
    stripped = text.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        return True
    if stripped.count("[") >= 2 and stripped.count("]") >= 2 and len(stripped) > 80:
        # Multiple bracket blocks often mean commentary leakage
        return True
    return False


def looks_like_word_by_word(text: str) -> bool:
    # Dense Devanagari interleaved with English glosses is a strong signal.
    dev = len(re.findall(r"[\u0900-\u097F]", text))
    if dev >= 8 and len(text) < 800:
        return True
    if dev >= 20:
        return True
    return False


def validate_workspace(
    workspace: Path,
    *,
    expected_verse_count: int = 47,
    source_id: str | None = None,
    source_checksum: str | None = None,
    registry_path: Path | None = None,
    allow_approved: bool = False,
) -> dict[str, Any]:
    segments_path = workspace / "segment-draft.jsonl"
    coverage_path = workspace / "coverage-map.json"
    extraction_path = workspace / "source-extraction.jsonl"

    segments = load_jsonl(segments_path)
    coverage = load_json(coverage_path)
    extraction = load_jsonl(extraction_path) if extraction_path.is_file() else []

    errors: list[str] = []
    warnings: list[str] = []

    chapter = 1
    ids: list[str] = []
    verse_owner: dict[int, str] = {}
    multi: list[str] = []
    status_counts: Counter[str] = Counter()

    for idx, seg in enumerate(segments, start=1):
        sid = seg.get("segmentId")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"segment[{idx}]: missing segmentId")
            continue
        if sid in ids:
            errors.append(f"duplicate segmentId: {sid}")
        ids.append(sid)

        if seg.get("chapterNumber") != chapter:
            errors.append(f"{sid}: chapterNumber must be {chapter}")

        label = seg.get("sourceLabel")
        if not isinstance(label, str) or not label.strip():
            errors.append(f"{sid}: sourceLabel blank")

        text = seg.get("translationText")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{sid}: translationText blank")
        else:
            if looks_like_commentary(text):
                errors.append(f"{sid}: translationText looks like commentary leakage")
            if looks_like_word_by_word(text):
                errors.append(f"{sid}: translationText looks like word-by-word leakage")

        verses = seg.get("coveredVerseNumbers")
        refs = seg.get("coveredCanonicalReferences")
        if not isinstance(verses, list) or not verses:
            errors.append(f"{sid}: coveredVerseNumbers missing")
            continue
        if not all(isinstance(v, int) for v in verses):
            errors.append(f"{sid}: coveredVerseNumbers must be ints")
            continue
        if any(v < 1 or v > expected_verse_count for v in verses):
            errors.append(f"{sid}: verse number out of range 1..{expected_verse_count}")
        if not verses_contiguous(verses):
            errors.append(f"{sid}: coveredVerseNumbers must be sorted and contiguous")
        expected_refs = canonical_refs(chapter, verses)
        if refs != expected_refs:
            errors.append(
                f"{sid}: coveredCanonicalReferences mismatch "
                f"(got {refs!r}, expected {expected_refs!r})"
            )

        for v in verses:
            if v in verse_owner:
                errors.append(
                    f"duplicate coverage for {chapter}.{v}: "
                    f"{verse_owner[v]} and {sid}"
                )
            else:
                verse_owner[v] = sid

        if len(verses) > 1:
            multi.append(sid)

        status = seg.get("publicationStatus")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{sid}: invalid publicationStatus {status!r}")
        else:
            status_counts[str(status)] += 1

        if status == "APPROVED":
            notes = seg.get("editorialNotes") or []
            reviewers = seg.get("reviewerIds") or []
            if not allow_approved:
                if not reviewers and not any(
                    isinstance(n, str) and "reviewer" in n.lower() for n in notes
                ):
                    errors.append(
                        f"{sid}: APPROVED without reviewer metadata "
                        "(reviewerIds or editorialNotes)"
                    )

        if source_id is not None and seg.get("sourceId") not in (None, source_id):
            # Allow matching expected source when provided
            if seg.get("sourceId") != source_id:
                errors.append(f"{sid}: sourceId mismatch")

        checksum = None
        sp = seg.get("sourcePage") or {}
        if isinstance(seg.get("sourceChecksum"), str):
            checksum = seg["sourceChecksum"]
        if source_checksum and checksum and checksum != source_checksum:
            errors.append(f"{sid}: sourceChecksum mismatch")

        if seg.get("language") != "en":
            errors.append(f"{sid}: language must be 'en'")

        # Segment drafts must not carry package/import metadata.
        for forbidden in (
            "packageId",
            "importBatchId",
            "importedAt",
            "translationPackageVersion",
            "databaseId",
        ):
            if forbidden in seg:
                errors.append(f"{sid}: forbidden package/import field {forbidden}")

        sp = seg.get("sourcePage")
        if not isinstance(sp, dict) or "printed" not in sp or "scanLeaf" not in sp:
            errors.append(f"{sid}: sourcePage.printed/scanLeaf required")

    if extraction and len(extraction) != len(segments):
        errors.append(
            f"source-extraction unit count {len(extraction)} "
            f"!= segment count {len(segments)}"
        )

    missing = [v for v in range(1, expected_verse_count + 1) if v not in verse_owner]
    if missing:
        errors.append(f"uncovered verses: {missing}")

    # coverage-map consistency
    if coverage.get("chapterNumber") != chapter:
        errors.append("coverage-map chapterNumber must be 1")
    if coverage.get("expectedVerseCount") != expected_verse_count:
        errors.append("coverage-map expectedVerseCount mismatch")
    if coverage.get("segmentCount") != len(segments):
        errors.append(
            f"coverage-map segmentCount {coverage.get('segmentCount')} "
            f"!= actual {len(segments)}"
        )

    vmap = coverage.get("verseToSegment") or {}
    for v in range(1, expected_verse_count + 1):
        key = f"{chapter}.{v}"
        if key not in vmap:
            errors.append(f"coverage-map missing verseToSegment[{key}]")
        elif verse_owner.get(v) and vmap[key] != verse_owner[v]:
            errors.append(
                f"coverage-map verseToSegment[{key}]={vmap[key]!r} "
                f"!= segment {verse_owner[v]!r}"
            )

    if coverage.get("uncoveredVerses") not in ([], None) and missing == []:
        if coverage.get("uncoveredVerses"):
            errors.append("coverage-map uncoveredVerses should be empty")
    if coverage.get("multiplyCoveredVerses") not in ([], None):
        if coverage.get("multiplyCoveredVerses"):
            errors.append("coverage-map multiplyCoveredVerses should be empty")

    if registry_path is not None and source_id:
        try:
            reg = load_json(registry_path)
            found = any(s.get("id") == source_id for s in reg.get("sources", []))
            if not found:
                errors.append(f"sourceId {source_id!r} not found in registry")
        except ValidationError as exc:
            errors.append(str(exc))

    approved = status_counts.get("APPROVED", 0)
    package_ready = False
    import_ready = False
    reasons = [
        "records are not APPROVED (or approval not authorized in this phase)",
        "no Translation package built in this phase",
    ]
    if approved == 0:
        reasons.insert(0, "approved count is 0")
    if multi:
        reasons.append(
            "package v1 cannot represent N→1 segments "
            f"(present: {len(multi)})"
        )
    elif coverage.get("packageFormatV1Compatible") is True:
        reasons.append(
            "structurally packageFormatV1Compatible, but not packageReady "
            "until APPROVED + package build"
        )

    report = {
        "workspace": str(workspace),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "segmentCount": len(segments),
        "oneToOneSegmentCount": len(segments) - len(multi),
        "multiVerseSegmentCount": len(multi),
        "multiVerseSegmentIds": multi,
        "expectedVerseCount": expected_verse_count,
        "coveredVerseCount": len(verse_owner),
        "uncoveredVerses": missing,
        "multiplyCoveredVerses": [],
        "statusCounts": dict(status_counts),
        "approvedCount": approved,
        "extractionUnitCount": len(extraction),
        "packageReady": package_ready,
        "importReady": import_ready,
        "packageReadinessReasons": reasons,
        "deterministicKeyOrder": [
            "segmentId",
            "coveredVerseNumbers",
            "coveredCanonicalReferences",
        ],
    }
    return report


def render_report(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--workspace",
        type=Path,
        default=Path(
            "content/translation-editorial/swarupananda-1909/chapter-01"
        ),
    )
    p.add_argument("--expected-verse-count", type=int, default=47)
    p.add_argument(
        "--source-id",
        default="bhagavad-gita-translation-en-swarupananda-1909-v1",
    )
    p.add_argument(
        "--source-checksum",
        default="ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e",
    )
    p.add_argument(
        "--registry",
        type=Path,
        default=Path("content/registry/sources.json"),
    )
    p.add_argument(
        "--write-report",
        type=Path,
        default=None,
        help="Optional path to write validation-report JSON",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = validate_workspace(
            args.workspace,
            expected_verse_count=args.expected_verse_count,
            source_id=args.source_id,
            source_checksum=args.source_checksum,
            registry_path=args.registry if args.registry.exists() else None,
        )
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    text = render_report(report)
    if args.write_report is not None:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text, encoding="utf-8")
    print(text)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
