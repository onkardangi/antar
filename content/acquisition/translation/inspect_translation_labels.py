#!/usr/bin/env python3
"""Inspect Translation OCR aids for Verse-label structure.

Read-only: never rewrites source files under content/raw/.
OCR is an inspection aid only — not authoritative transcription.
Does not emit Translation text into output JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

CHAPTER_1_START_MARKERS = (
    "FIRST CHAPTER",
    "THE GRIEF OF ARJUNA",
)
CHAPTER_2_START_MARKERS = (
    "SECOND CHAPTER",
    "THE WAY OF KNOWLEDGE",
)
CHAPTER_13_START_MARKERS = (
    "THIRTEENTH CHAPTER",
    "DISCRIMINATION OF THE KSHETRA",
)
CHAPTER_14_START_MARKERS = (
    "FOURTEENTH CHAPTER",
    "DISCRIMINATION OF THE THREE GUNAS",
)

# Labels like "1. 12.", "I. 12.", "1.12", "॥१२॥" are noisy; prefer Latin "1. N."
LATIN_CHAPTER_VERSE = re.compile(
    r"(?m)(?<!\d)(?P<label>(?:I|1)\s*[\.\,]\s*(?P<verse>\d{1,2}))(?!\d)"
)
COMBINED_RANGE = re.compile(
    r"(?m)(?<!\d)(?P<label>(?:I|1)\s*[\.\,]\s*(?P<a>\d{1,2})\s*[-–—]\s*(?P<b>\d{1,2}))(?!\d)"
)
STANDALONE_COMBINED = re.compile(
    r"(?m)^\s*(?P<a>\d{1,2})\s*[-–—]\s*(?P<b>\d{1,2})\s*[\.:]?\s*$"
)


class InspectionError(Exception):
    """Fatal inspection failure."""


def find_section(text: str, start_markers: tuple[str, ...], occurrence: int = -1) -> int:
    """Return start index of marker occurrence (default: last early / chosen index)."""
    hits: list[int] = []
    upper = text.upper()
    for marker in start_markers:
        start = 0
        needle = marker.upper()
        while True:
            idx = upper.find(needle, start)
            if idx < 0:
                break
            hits.append(idx)
            start = idx + len(needle)
    if not hits:
        raise InspectionError(f"No section markers found for {start_markers!r}")
    hits.sort()
    if occurrence < 0:
        # Prefer a hit that is not in the table of contents: take the last hit
        # among those before mid-book for ch1 is wrong; for chapter bodies,
        # callers pass explicit occurrence or we take hits[1] when available.
        return hits[1] if len(hits) > 1 else hits[0]
    if occurrence >= len(hits):
        raise InspectionError(
            f"Requested occurrence {occurrence} but only {len(hits)} hits for {start_markers!r}"
        )
    return hits[occurrence]


def extract_region(text: str, start: int, end: int) -> str:
    if end <= start:
        raise InspectionError("Invalid region bounds")
    return text[start:end]


def normalize_label(chapter: int, verse: int) -> str:
    return f"{chapter}.{verse}"


def collect_labels_from_ocr(region: str, chapter: int) -> dict[str, Any]:
    """Collect structural label evidence from an OCR region. No Translation text."""
    combined: list[dict[str, Any]] = []
    singles: list[int] = []

    for match in COMBINED_RANGE.finditer(region):
        a = int(match.group("a"))
        b = int(match.group("b"))
        if a >= b or b > 78:
            continue
        combined.append(
            {
                "label": f"{chapter}.{a}-{b}",
                "from": a,
                "to": b,
                "evidence": "ocr_combined_range",
            }
        )

    for match in STANDALONE_COMBINED.finditer(region):
        a = int(match.group("a"))
        b = int(match.group("b"))
        if a >= b or b > 78:
            continue
        combined.append(
            {
                "label": f"{chapter}.{a}-{b}",
                "from": a,
                "to": b,
                "evidence": "ocr_standalone_combined",
            }
        )

    for match in LATIN_CHAPTER_VERSE.finditer(region):
        verse = int(match.group("verse"))
        if 1 <= verse <= 78:
            singles.append(verse)

    # Deduplicate combined by (from,to)
    combined_key = {(c["from"], c["to"]): c for c in combined}
    combined_list = [combined_key[k] for k in sorted(combined_key)]

    # Verses covered by combined ranges
    covered_by_combined: set[int] = set()
    for item in combined_list:
        covered_by_combined.update(range(item["from"], item["to"] + 1))

    counts = Counter(singles)
    observed_verses = sorted(set(singles) | covered_by_combined)
    observed_labels = [normalize_label(chapter, v) for v in observed_verses]
    duplicate_labels = [
        normalize_label(chapter, v) for v, n in sorted(counts.items()) if n > 1
    ]
    return {
        "observedVerses": observed_verses,
        "observedLabels": observed_labels,
        "duplicateLabels": duplicate_labels,
        "combinedLabels": [
            {"label": c["label"], "from": c["from"], "to": c["to"]} for c in combined_list
        ],
        "ocrSingleHitCounts": {str(k): v for k, v in sorted(counts.items())},
    }


def missing_labels(expected: int, observed_verses: list[int]) -> list[str]:
    present = set(observed_verses)
    return [f"1.{n}" for n in range(1, expected + 1) if n not in present]


def inspect_chapter_1_ocr(
    ocr_text: str,
    *,
    expected_verse_count: int = 47,
    chapter1_start_occurrence: int = 1,
    chapter2_start_occurrence: int = 0,
) -> dict[str, Any]:
    start = find_section(ocr_text, CHAPTER_1_START_MARKERS, chapter1_start_occurrence)
    end = find_section(ocr_text, CHAPTER_2_START_MARKERS, chapter2_start_occurrence)
    if end <= start:
        # Fallback: search for chapter 2 after chapter 1 start
        upper = ocr_text.upper()
        idx = upper.find("SECOND CHAPTER", start + 10)
        if idx < 0:
            idx = upper.find("THE WAY OF KNOWLEDGE", start + 10)
        if idx < 0 or idx <= start:
            raise InspectionError("Could not locate Chapter 2 boundary after Chapter 1")
        end = idx
    region = extract_region(ocr_text, start, end)
    collected = collect_labels_from_ocr(region, chapter=1)
    missing = missing_labels(expected_verse_count, collected["observedVerses"])
    return {
        "chapterNumber": 1,
        "expectedVerseCount": expected_verse_count,
        "ocrRegionCharStart": start,
        "ocrRegionCharEnd": end,
        "ocrRegionCharLength": end - start,
        **collected,
        "missingLabels": missing,
        "ocrObservedDistinctCount": len(collected["observedVerses"]),
        "warning": (
            "OCR-derived labels are candidates only. Final conclusions require "
            "direct page-image inspection of the pinned scan."
        ),
    }


def inspect_chapter_13_max_label_ocr(ocr_text: str) -> dict[str, Any] | None:
    try:
        start = find_section(ocr_text, CHAPTER_13_START_MARKERS, occurrence=1)
    except InspectionError:
        try:
            start = find_section(ocr_text, CHAPTER_13_START_MARKERS, occurrence=0)
        except InspectionError:
            return None
    try:
        end = find_section(ocr_text, CHAPTER_14_START_MARKERS, occurrence=0)
    except InspectionError:
        upper = ocr_text.upper()
        end = upper.find("FOURTEENTH CHAPTER", start + 10)
        if end < 0:
            end = upper.find("THE DISCRIMINATION OF THE THREE", start + 10)
        if end < 0:
            return None
    if end <= start:
        return None
    region = extract_region(ocr_text, start, end)
    # Look for "XIII. N" / "13. N" / bare trailing verse numbers in Latin form
    hits = []
    for match in re.finditer(
        r"(?m)(?:XIII|13|XIH)\s*[\.\,]\s*(\d{1,2})", region, flags=re.I
    ):
        n = int(match.group(1))
        if 1 <= n <= 40:
            hits.append(n)
    for match in re.finditer(r"(?m)^\s*(\d{1,2})\s*[\.]\s*$", region):
        n = int(match.group(1))
        if 1 <= n <= 40:
            hits.append(n)
    if not hits:
        return {
            "chapterNumber": 13,
            "ocrMaxLabel": None,
            "confidence": "low",
            "note": "Chapter 13 region located but no reliable Latin verse labels in OCR",
        }
    return {
        "chapterNumber": 13,
        "ocrMaxLabel": max(hits),
        "ocrDistinctLabels": sorted(set(hits)),
        "confidence": "low",
        "note": (
            "OCR-only Chapter 13 observation; confirm against scan before relying "
            "on 34-vs-35 tradition."
        ),
    }


def load_text(path: Path) -> str:
    if not path.is_file():
        raise InspectionError(f"OCR aid not found: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ocr-file",
        type=Path,
        required=True,
        help="Path to retained DjVuTXT / OCR inspection aid (read-only)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to write structural label JSON (no Translation text)",
    )
    parser.add_argument("--expected-verse-count", type=int, default=47)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        text = load_text(args.ocr_file)
        chapter1 = inspect_chapter_1_ocr(
            text, expected_verse_count=args.expected_verse_count
        )
        chapter13 = inspect_chapter_13_max_label_ocr(text)
        payload = {
            "ocrFile": str(args.ocr_file),
            "ocrIsAuthoritative": False,
            "chapter1": chapter1,
            "chapter13": chapter13,
        }
    except InspectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        if args.output_json.exists():
            args.output_json.unlink()
        args.output_json.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
