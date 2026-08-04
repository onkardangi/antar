#!/usr/bin/env python3
"""Backward-compatible Verse 1.1 entrypoint.

Delegates to fetch_iitk_verse.acquire_verse. Keeps existing 1.1 evidence compatible.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fetch_iitk_verse import (  # noqa: E402
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_UA,
    AcquisitionError,
    acquire_verse,
    extract_mool_root_text as _extract_mool_root_text,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "bhagavad-gita-sanskrit-iitk-verse-1.1-verification-v1"


def extract_mool_root_text(html: str, *, chapter: int = 1, verse: int = 1) -> str:
    """Compatibility wrapper defaulting to Verse 1.1 identity checks."""
    return _extract_mool_root_text(html, chapter=chapter, verse=verse)


__all__ = [
    "AcquisitionError",
    "SOURCE_ID",
    "acquire_verse",
    "extract_mool_root_text",
    "main",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Acquire IIT/Gita Supersite Verse 1.1 mool verification evidence."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "content/raw/sanskrit/iit-kanpur/verse-1.1",
    )
    parser.add_argument("--user-agent", default=DEFAULT_UA)
    parser.add_argument("--timeout", type=int, default=int(DEFAULT_TIMEOUT_SECONDS))
    parser.add_argument(
        "--force-refetch",
        action="store_true",
        help="Unused compatibility flag; overwrite remains refused for differing bytes.",
    )
    args = parser.parse_args(argv)
    output_root = args.output_dir.parent
    # If caller passed verse-1.1 dir, parent is iit-kanpur root.
    try:
        metadata = acquire_verse(
            chapter=1,
            verse=1,
            output_root=output_root,
            user_agent=args.user_agent,
            timeout_seconds=float(args.timeout),
            delay_seconds=2.0,
            apply_delay=False,
        )
    except AcquisitionError as exc:
        print(f"acquisition error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
