#!/usr/bin/env python3
"""Sequential batch acquisition of IIT Kanpur mool verification evidence.

Verification-only. Sequential requests only. Conservative delay. No concurrency.
Does not claim chapter completion unless all requested Verses succeed.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from fetch_iitk_verse import (
    DEFAULT_DELAY_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_UA,
    AcquisitionError,
    TransientAcquisitionError,
    acquire_verse,
    evidence_dir,
    load_existing_valid_metadata,
    utc_now_iso,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "content/raw/sanskrit/iit-kanpur"
# Stop the batch after this many consecutive provider/transient failures.
MAX_CONSECUTIVE_PROVIDER_ERRORS = 3


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_batch(
    *,
    chapter: int,
    verse_start: int,
    verse_end: int,
    output_root: Path,
    delay_seconds: float,
    timeout_seconds: float,
    user_agent: str,
    resume: bool,
    dry_run: bool,
    sleep_fn: Callable[[float], None] = time.sleep,
    acquire_fn: Callable[..., dict[str, Any]] | None = None,
    stop_on_consecutive_errors: int = MAX_CONSECUTIVE_PROVIDER_ERRORS,
) -> dict[str, Any]:
    if verse_start > verse_end:
        raise AcquisitionError("verse-start must be <= verse-end")
    if delay_seconds < 2.0:
        raise AcquisitionError("delay-seconds must be >= 2")

    verses = list(range(verse_start, verse_end + 1))
    started = utc_now_iso()
    records: list[dict[str, Any]] = []
    acquired: list[str] = []
    skipped: list[str] = []
    failed: list[dict[str, str]] = []
    consecutive_errors = 0
    stopped_early = False
    stop_reason = None

    do_acquire = acquire_fn or acquire_verse

    for verse in verses:
        ref = f"{chapter}.{verse}"
        entry: dict[str, Any] = {
            "canonicalReference": ref,
            "chapterNumber": chapter,
            "verseNumber": verse,
            "requested": True,
        }
        out_dir = evidence_dir(output_root, chapter, verse)

        if resume:
            existing = load_existing_valid_metadata(out_dir, chapter, verse)
            if existing:
                entry.update(
                    {
                        "outcome": "skipped",
                        "retrievalTimestamp": existing.get("retrievalTimestamp"),
                        "evidenceChecksum": existing.get("evidenceSha256"),
                        "rootTextChecksum": existing.get("observedRootTextChecksumSha256"),
                        "responseUrl": existing.get("finalUrl"),
                        "sourceId": existing.get("sourceId"),
                    }
                )
                records.append(entry)
                skipped.append(ref)
                consecutive_errors = 0
                continue

        if dry_run:
            entry.update(
                {
                    "outcome": "dry_run",
                    "retrievalUrl": (
                        "https://old.gitasupersite.in/srimad"
                        f"?choose=1&language=dv&field_chapter_value={chapter}"
                        f"&field_nsutra_value={verse}&show_mool=1"
                    ),
                }
            )
            records.append(entry)
            skipped.append(ref)
            continue

        try:
            # Delay is applied inside acquire_verse (except tests that inject acquire_fn).
            meta = do_acquire(
                chapter=chapter,
                verse=verse,
                output_root=output_root,
                user_agent=user_agent,
                timeout_seconds=timeout_seconds,
                delay_seconds=delay_seconds,
                apply_delay=acquire_fn is None,
                sleep_fn=sleep_fn,
            )
            entry.update(
                {
                    "outcome": "acquired",
                    "retrievalTimestamp": meta.get("retrievalTimestamp"),
                    "evidenceChecksum": meta.get("evidenceSha256"),
                    "rootTextChecksum": meta.get("observedRootTextChecksumSha256"),
                    "responseUrl": meta.get("finalUrl"),
                    "sourceId": meta.get("sourceId"),
                }
            )
            records.append(entry)
            acquired.append(ref)
            consecutive_errors = 0
        except AcquisitionError as exc:
            reason = str(exc)
            entry.update({"outcome": "failed", "failureReason": reason})
            records.append(entry)
            failed.append({"canonicalReference": ref, "reason": reason})
            consecutive_errors += 1
            if consecutive_errors >= stop_on_consecutive_errors:
                stopped_early = True
                stop_reason = (
                    f"Stopped after {consecutive_errors} consecutive provider/acquisition "
                    f"errors (last: {ref}: {reason}). Manual rerun required."
                )
                break

    complete = (
        not dry_run
        and not stopped_early
        and len(failed) == 0
        and (len(acquired) + len(skipped)) == len(verses)
    )
    manifest = {
        "schemaVersion": 1,
        "chapterNumber": chapter,
        "verseStart": verse_start,
        "verseEnd": verse_end,
        "requested": [f"{chapter}.{v}" for v in verses],
        "acquired": acquired,
        "skipped": skipped,
        "failed": failed,
        "startedAt": started,
        "finishedAt": utc_now_iso(),
        "delaySeconds": delay_seconds,
        "userAgent": user_agent,
        "resume": resume,
        "dryRun": dry_run,
        "chapterComplete": complete,
        "stoppedEarly": stopped_early,
        "stopReason": stop_reason,
        "records": records,
        "notes": [
            "Verification-only acquisition. Not an import corpus.",
            "LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION.",
            "Partial failures are recorded; chapterComplete is true only if all succeed.",
        ],
    }
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sequentially acquire IIT mool verification evidence for a Verse range."
    )
    parser.add_argument("--chapter", type=int, default=1)
    parser.add_argument("--verse-start", type=int, required=True)
    parser.add_argument("--verse-end", type=int, required=True)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--user-agent", default=DEFAULT_UA)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Manifest path (default: <output-root>/chapter-NN-manifest.json)",
    )
    args = parser.parse_args(argv)

    manifest_path = args.manifest or (
        args.output_root / f"chapter-{args.chapter:02d}-manifest.json"
    )

    try:
        manifest = run_batch(
            chapter=args.chapter,
            verse_start=args.verse_start,
            verse_end=args.verse_end,
            output_root=args.output_root,
            delay_seconds=args.delay_seconds,
            timeout_seconds=args.timeout_seconds,
            user_agent=args.user_agent,
            resume=args.resume,
            dry_run=args.dry_run,
        )
    except AcquisitionError as exc:
        print(f"batch error: {exc}", file=sys.stderr)
        return 1

    write_manifest(manifest_path, manifest)
    print(
        json.dumps(
            {
                "manifestPath": str(manifest_path),
                "acquired": len(manifest["acquired"]),
                "skipped": len(manifest["skipped"]),
                "failed": len(manifest["failed"]),
                "chapterComplete": manifest["chapterComplete"],
                "stoppedEarly": manifest["stoppedEarly"],
                "stopReason": manifest["stopReason"],
                "failedDetails": manifest["failed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if manifest["failed"] or manifest["stoppedEarly"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
