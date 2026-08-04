#!/usr/bin/env python3
"""Generate a Verse editorial review Markdown file from the template.

Never overwrites an existing review file.
Does not approve Verses and does not invent Sanskrit.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"

ALLOWED_CREATE_STATUSES = frozenset({"UNREVIEWED", "READY_FOR_REVIEW"})


class GenerateError(Exception):
    pass


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def find_comparison(chapter: int, verse: int) -> dict[str, Any] | None:
    path = CHAPTER_DIR / "source-comparison.jsonl"
    ref = f"{chapter}.{verse}"
    for record in load_jsonl(path):
        if record.get("canonicalReference") == ref:
            return record
    return None


def find_registry_entry(source_id: str) -> dict[str, Any] | None:
    registry_path = REPO_ROOT / "content/registry/sources.json"
    if not registry_path.is_file():
        return None
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in data.get("sources") or []:
        if entry.get("id") == source_id:
            return entry
    return None


def format_sources_table(sources: list[dict[str, Any]]) -> str:
    header = (
        "| Source ID | Revision | License | Retrieved | Checksum | Status |\n"
        "|-----------|----------|---------|-----------|----------|--------|"
    )
    if not sources:
        return header + "\n| _None attached_ |  |  |  |  |  |"

    rows = [header]
    for source in sources:
        source_id = source.get("sourceId") or ""
        registry = find_registry_entry(source_id) or {}
        revision = registry.get("revision_id", "")
        license_status = source.get("licenseStatus") or registry.get("license_status") or ""
        retrieved = source.get("retrievedAt") or registry.get("retrieval_timestamp") or ""
        checksum = source.get("sourceChecksum") or registry.get("sha256") or ""
        status = registry.get("status") or source.get("status") or ""
        rows.append(
            f"| `{source_id}` | `{revision}` | {license_status} | `{retrieved}` | `{checksum}` | `{status}` |"
        )
    return "\n".join(rows)


def format_source_comparison(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return (
            "No sources attached yet.\n\n"
            "- Source reference: _n/a_\n"
            "- Observed Sanskrit: _n/a_\n"
            "- Observed transliteration: _n/a_\n"
            "- Normalization notes: _n/a_"
        )

    blocks: list[str] = []
    for source in sources:
        source_id = source.get("sourceId")
        sanskrit = source.get("sanskritText")
        transliteration = source.get("transliteration")
        notes = source.get("notes") or []
        notes_text = (
            "\n".join(f"  - `{n}`" if not str(n).startswith("Verse ") else f"  - {n}" for n in notes)
            if notes
            else "  - _None recorded._"
        )
        if sanskrit is None:
            sanskrit_block = "_null_ (not present in comparison record)"
        else:
            # Include observed Sanskrit only because this section compares sources.
            sanskrit_block = f"```text\n{sanskrit}\n```"
        translit_display = (
            "`null`"
            if transliteration is None
            else f"```text\n{transliteration}\n```"
        )
        blocks.append(
            f"## Source: `{source_id}`\n\n"
            f"- Source reference: `{source.get('sourceReference')}`\n"
            f"- Observed Sanskrit (comparison only):\n\n{sanskrit_block}\n\n"
            f"- Observed transliteration: {translit_display}\n"
            f"- Normalization notes:\n{notes_text}"
        )
    return "\n\n".join(blocks)


def differences_section(sources: list[dict[str, Any]]) -> str:
    if len(sources) <= 1:
        prefix = (
            "Only one source is currently attached to this Verse identity. "
            "Cross-source textual differences cannot be assessed yet.\n\n"
            if len(sources) == 1
            else "No sources are attached yet.\n\n"
        )
        return prefix + "No differences currently observed."
    return (
        "Multiple sources are attached. Explicit textual diff analysis is still required.\n\n"
        "No differences currently observed."
    )


def render_review(
    *,
    chapter: int,
    verse: int,
    status: str,
    comparison: dict[str, Any] | None,
) -> str:
    ref = f"{chapter}.{verse}"
    sources = list((comparison or {}).get("sources") or [])
    if status not in ALLOWED_CREATE_STATUSES:
        raise GenerateError(
            f"Generator may only create status in {sorted(ALLOWED_CREATE_STATUSES)}"
        )
    # Prefer READY_FOR_REVIEW when a nonblank Wikisource/source Sanskrit exists.
    if status == "READY_FOR_REVIEW" and sources:
        if not any(
            isinstance(s.get("sanskritText"), str) and s["sanskritText"].strip()
            for s in sources
        ):
            raise GenerateError(
                "READY_FOR_REVIEW requires at least one nonblank source Sanskrit"
            )

    today = date.today().isoformat()
    return "\n".join(
        [
            "# Canonical Reference",
            "",
            ref,
            "",
            "# Status",
            "",
            status,
            "",
            "# Sources",
            "",
            format_sources_table(sources),
            "",
            "# Source Comparison",
            "",
            format_source_comparison(sources),
            "",
            "# Differences",
            "",
            differences_section(sources),
            "",
            "# Editorial Notes",
            "",
            "_None._",
            "",
            "# Decision",
            "",
            "No editorial decision recorded.",
            "",
            "# Approval",
            "",
            "Reviewer:",
            "",
            "Second Reviewer:",
            "",
            "Date:",
            "",
            "# Audit Log",
            "",
            f"- {today} — Review file created. Status set to `{status}`. No approval granted.",
            "",
        ]
    )


def generate_review(
    *,
    chapter: int,
    verse: int,
    reviews_dir: Path = DEFAULT_REVIEWS_DIR,
    status: str = "READY_FOR_REVIEW",
    force_unreviewed: bool = False,
) -> Path:
    if chapter < 1 or verse < 1:
        raise GenerateError("chapter and verse must be positive integers")
    ref = f"{chapter}.{verse}"
    path = reviews_dir / f"{ref}.md"
    if path.exists():
        raise GenerateError(f"Refusing overwrite: review already exists at {path}")

    comparison = find_comparison(chapter, verse)
    if force_unreviewed or comparison is None:
        status = "UNREVIEWED"
    content = render_review(
        chapter=chapter,
        verse=verse,
        status=status,
        comparison=comparison,
    )
    reviews_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an Antar Verse editorial review Markdown file."
    )
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--verse", type=int, required=True)
    parser.add_argument(
        "--reviews-dir",
        type=Path,
        default=DEFAULT_REVIEWS_DIR,
        help="Directory for review Markdown files",
    )
    parser.add_argument(
        "--status",
        choices=sorted(ALLOWED_CREATE_STATUSES),
        default="READY_FOR_REVIEW",
    )
    parser.add_argument(
        "--unreviewed",
        action="store_true",
        help="Force UNREVIEWED even if comparison evidence exists",
    )
    args = parser.parse_args(argv)
    try:
        path = generate_review(
            chapter=args.chapter,
            verse=args.verse,
            reviews_dir=args.reviews_dir,
            status=args.status,
            force_unreviewed=args.unreviewed,
        )
    except GenerateError as exc:
        print(f"generate error: {exc}", file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
