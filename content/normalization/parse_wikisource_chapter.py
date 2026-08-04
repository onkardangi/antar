#!/usr/bin/env python3
"""Parse Chapter 1 root verses from a preserved Sanskrit Wikisource snapshot.

Reads only the local raw MediaWiki API JSON. Does not fetch the network.
Does not invent, split, merge, renumber, or rewrite Sanskrit characters.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
VERSE_MARKER_RE = re.compile(
    r"॥\s*([०-९0-9]+)\s*[-–—]\s*([०-९0-9]+)\s*॥"
)
POEM_RE = re.compile(r"<poem>(.*?)</poem>", re.IGNORECASE | re.DOTALL)
BOLD_MARKUP_RE = re.compile(r"'''(.*?)'''", re.DOTALL)

EXPECTED_CHAPTER = 1
EXPECTED_VERSES = 47


class ParseError(Exception):
    """Fatal parse ambiguity or structural failure."""


def load_snapshot(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ParseError(f"Cannot read snapshot JSON: {path}: {exc}") from exc
    return payload


def extract_wikitext(payload: dict[str, Any]) -> tuple[str, int, dict[str, Any]]:
    try:
        page = payload["query"]["pages"][0]
        revision = page["revisions"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise ParseError("Snapshot missing query.pages[0].revisions[0]") from exc
    revid = revision.get("revid")
    if not isinstance(revid, int):
        raise ParseError("Snapshot revision missing integer revid")
    slots = revision.get("slots") or {}
    main = slots.get("main") or {}
    content = main.get("content")
    if content is None:
        content = revision.get("content")
    if not isinstance(content, str) or content == "":
        raise ParseError(f"Revision {revid} has no wikitext content")
    return content, revid, page


def strip_balanced_templates(text: str, template_name: str) -> tuple[str, int]:
    """Remove {{template_name ...}} blocks including nested braces."""
    token = "{{" + template_name
    removed = 0
    out: list[str] = []
    i = 0
    while True:
        j = text.find(token, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        depth = 0
        k = j
        closed = False
        while k < len(text) - 1:
            if text[k : k + 2] == "{{":
                depth += 1
                k += 2
                continue
            if text[k : k + 2] == "}}":
                depth -= 1
                k += 2
                if depth == 0:
                    closed = True
                    removed += 1
                    break
                continue
            k += 1
        if not closed:
            raise ParseError(f"Unbalanced template {template_name!r} starting at {j}")
        i = k
    return "".join(out), removed


def normalize_poem_body(body: str) -> tuple[str, list[str]]:
    """Recover readable source text with recorded normalization operations."""
    changes: list[str] = []
    text = body.replace("\r\n", "\n").replace("\r", "\n")
    if "\r" in body or "\r\n" in body:
        changes.append("normalized_line_endings_to_LF")

    # Remove only structural wikitext bold delimiters; keep inner text (speakers, titles).
    if "'''" in text:
        text = BOLD_MARKUP_RE.sub(r"\1", text)
        changes.append("removed_wikitext_bold_delimiters")

    nfc = unicodedata.normalize("NFC", text)
    if nfc != text:
        changes.append("unicode_nfc")
        text = nfc

    stripped = text.strip("\n")
    # Trim only surrounding blank lines / outer whitespace; preserve internal spacing.
    if stripped != text:
        changes.append("trimmed_surrounding_whitespace")
        text = stripped
    # Also trim pure leading/trailing spaces on the whole block edges already handled;
    # do not alter Sanskrit spelling or punctuation characters.
    text = text.strip()
    if text != stripped.strip():
        # unreachable safeguard
        changes.append("trimmed_surrounding_whitespace")

    # Ensure LF-only final form.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text, changes


def parse_marker(text: str) -> tuple[int, int, str]:
    matches = list(VERSE_MARKER_RE.finditer(text))
    if not matches:
        raise ParseError("Poem block has no Verse marker ॥ch-verse॥")
    if len(matches) > 1:
        raise ParseError(
            f"Poem block has {len(matches)} Verse markers; refusing ambiguous extract"
        )
    match = matches[0]
    chapter = int(match.group(1).translate(DEVANAGARI_DIGITS))
    verse = int(match.group(2).translate(DEVANAGARI_DIGITS))
    source_reference = f"{match.group(1)}-{match.group(2)}"
    return chapter, verse, source_reference


def front_matter_note(verse_number: int, text: str) -> str | None:
    if verse_number != 1:
        return None
    # Identify material before the first śloka line containing a danda near the marker.
    marker = VERSE_MARKER_RE.search(text)
    if not marker:
        return None
    before = text[: marker.start()]
    # Heuristic documentation only: note presence of known front-matter tokens.
    tokens = []
    for token in ("ॐ", "श्रीपरमात्मने", "अथ श्रीमद्भगवद्गीता", "प्रथमोऽध्याय"):
        if token in before:
            tokens.append(token)
    if not tokens and not before.strip():
        return None
    return (
        "Verse 1.1 poem contains pre-Verse front matter before the marked śloka; "
        "preserved in full without editorial stripping. Observed tokens/material: "
        + (", ".join(tokens) if tokens else "non-empty prefix before marker")
        + "."
    )


def extract_verses(
    wikitext: str,
    *,
    source_id: str,
    revision_id: int,
) -> list[dict[str, Any]]:
    # Exclude commentary and navigation templates before scanning poems.
    working, removed_vyakhya = strip_balanced_templates(wikitext, "व्याख्या")
    working, removed_nav = strip_balanced_templates(working, "भगवद्गीतायाः अध्यायाः")
    file_hits = len(re.findall(r"\[\[File:.*?\]\]", working, flags=re.IGNORECASE | re.DOTALL))
    working = re.sub(r"\[\[File:.*?\]\]", "", working, flags=re.IGNORECASE | re.DOTALL)

    poems = POEM_RE.findall(working)
    records: list[dict[str, Any]] = []
    seen: dict[tuple[int, int], int] = {}

    for poem in poems:
        if not VERSE_MARKER_RE.search(poem):
            # Colophon / non-verse poem — excluded by design.
            continue
        chapter, verse, source_reference = parse_marker(poem)
        if chapter != EXPECTED_CHAPTER:
            raise ParseError(f"Unexpected chapter marker {chapter}.{verse}")
        key = (chapter, verse)
        if key in seen:
            raise ParseError(f"Duplicate Verse marker for {chapter}.{verse}")
        seen[key] = 1

        sanskrit, changes = normalize_poem_body(poem)
        if not sanskrit.strip():
            raise ParseError(f"Blank Sanskrit after normalization for {chapter}.{verse}")

        # Always record template/file exclusions once on each record's shared context?
        # Keep per-verse changes local; global exclusions go into notes for 1.1 only + all get baseline.
        baseline_changes = list(changes)
        if removed_vyakhya and "excluded_vyakhya_templates" not in baseline_changes:
            # Record globally applied exclusions on every record for provenance honesty.
            baseline_changes.insert(0, f"excluded_vyakhya_templates:{removed_vyakhya}")
        if removed_nav and "excluded_nav_template" not in baseline_changes:
            baseline_changes.insert(0, "excluded_nav_template:भगवद्गीतायाः अध्यायाः")
        if file_hits and "excluded_file_links" not in baseline_changes:
            baseline_changes.insert(0, f"excluded_file_links:{file_hits}")

        note = front_matter_note(verse, sanskrit)
        record: dict[str, Any] = {
            "chapterNumber": chapter,
            "verseNumber": verse,
            "canonicalReference": f"{chapter}.{verse}",
            "sourceId": source_id,
            "sourceReference": source_reference,
            "sanskritText": sanskrit,
            "transliteration": None,
            "rawRevisionId": revision_id,
            "normalization": {
                "unicode": "NFC",
                "lineEndings": "LF",
                "changes": baseline_changes,
            },
        }
        if note:
            record["parsingNotes"] = [note]
        records.append(record)

    records.sort(key=lambda r: r["verseNumber"])
    expected = set(range(1, EXPECTED_VERSES + 1))
    actual = {r["verseNumber"] for r in records}
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise ParseError(
            f"Expected exactly {EXPECTED_VERSES} verses 1..{EXPECTED_VERSES}; "
            f"missing={missing} unexpected={unexpected}"
        )
    if len(records) != EXPECTED_VERSES:
        raise ParseError(f"Expected {EXPECTED_VERSES} records, found {len(records)}")
    return records


def records_to_jsonl(records: list[dict[str, Any]]) -> str:
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    return "\n".join(lines) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_snapshot_file(
    snapshot_path: Path,
    *,
    source_id: str,
) -> tuple[list[dict[str, Any]], str]:
    payload = load_snapshot(snapshot_path)
    wikitext, revid, _page = extract_wikitext(payload)
    records = extract_verses(wikitext, source_id=source_id, revision_id=revid)
    text = records_to_jsonl(records)
    return records, text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse Wikisource Chapter 1 snapshot into extraction JSONL."
    )
    parser.add_argument(
        "--snapshot",
        type=Path,
        required=True,
        help="Path to preserved raw MediaWiki API JSON snapshot",
    )
    parser.add_argument(
        "--source-id",
        required=True,
        help="Stable registry source id",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output wikisource-extraction.jsonl path",
    )
    args = parser.parse_args(argv)

    try:
        _records, text = parse_snapshot_file(args.snapshot, source_id=args.source_id)
    except ParseError as exc:
        print(f"parse error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "recordCount": EXPECTED_VERSES,
                "sha256": sha256_text(text),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
