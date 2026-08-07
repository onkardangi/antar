#!/usr/bin/env python3
"""Fetch pinned Internet Archive item files for Translation acquisition.

Downloads selected files only. Refuses silent overwrite of differing bytes.
Computes SHA-256 locally. Does not approve, normalize, package, or import.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_USER_AGENT = (
    "AntarContentAcquisition/0.1 "
    "(+https://github.com/antar-project/antar; content-acquisition@antar.example)"
)
DEFAULT_TIMEOUT_SEC = 120
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BACKOFF_SEC = 2.0

# Swarupananda 1909 first-edition defaults (Phase 2 pin).
DEFAULT_ITEM_ID = "in.ernet.dli.2015.386852"
DEFAULT_FILES = (
    "2015.386852.Srimad-Bhagavad.pdf",
    "in.ernet.dli.2015.386852_meta.xml",
    "in.ernet.dli.2015.386852_files.xml",
    "2015.386852.Srimad-Bhagavad_djvu.txt",
    "2015.386852.Srimad-Bhagavad_page_numbers.json",
    "2015.386852.Srimad-Bhagavad_scandata.xml",
)


class AcquisitionError(Exception):
    """Fatal acquisition failure."""


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def write_bytes_exclusive(path: Path, data: bytes) -> str:
    """Write data only if absent or identical. Refuse different existing bytes."""
    if path.exists():
        existing = path.read_bytes()
        if existing == data:
            return "unchanged"
        raise AcquisitionError(
            f"Refusing silent overwrite: different content already exists at {path}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return "written"


def fetch_bytes(
    url: str,
    *,
    user_agent: str,
    timeout_sec: int,
    retries: int,
    retry_backoff_sec: float,
) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(url, headers={"User-Agent": user_agent})
        try:
            with urllib.request.urlopen(request, timeout=timeout_sec) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            last_error = AcquisitionError(f"HTTP error {exc.code} for {url}")
            if exc.code in {408, 429, 500, 502, 503, 504} and attempt < retries:
                time.sleep(retry_backoff_sec * attempt)
                continue
            raise last_error from exc
        except urllib.error.URLError as exc:
            last_error = AcquisitionError(f"URL error for {url}: {exc}")
            if attempt < retries:
                time.sleep(retry_backoff_sec * attempt)
                continue
            raise last_error from exc
    raise AcquisitionError(f"Failed to fetch {url}: {last_error}")


def metadata_api_url(item_id: str) -> str:
    return f"https://archive.org/metadata/{item_id}"


def download_url(item_id: str, filename: str) -> str:
    return f"https://archive.org/download/{item_id}/{filename}"


def select_file_records(
    metadata: dict[str, Any], filenames: list[str]
) -> dict[str, dict[str, Any]]:
    files = metadata.get("files")
    if not isinstance(files, list):
        raise AcquisitionError("Internet Archive metadata missing files list")
    by_name = {
        entry["name"]: entry
        for entry in files
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    missing = [name for name in filenames if name not in by_name]
    if missing:
        raise AcquisitionError(
            "Requested files missing from item metadata: " + ", ".join(missing)
        )
    return {name: by_name[name] for name in filenames}


# Edition-specific acquisition defaults keyed by IA item id.
# Human verification still required after download; these seed metadata.json only.
EDITION_PROFILES: dict[str, dict[str, Any]] = {
    "in.ernet.dli.2015.386852": {
        "translator": "Swami Swarupananda",
        "defaultTitle": "Srimad Bhagavad Gita",
        "editionTarget": {
            "edition": "First Edition",
            "year": 1909,
            "publisher": "Prabuddha Bharata Press, Mayavati, Almora, Himalayas",
            "series": "Himalayan Series — No. XX",
            "verification": "Confirm from scan title page after acquisition",
        },
        "rejectedMasters": [
            {
                "itemId": "in.ernet.dli.2015.237563",
                "reason": (
                    "Title-page/OCR evidence indicates Tenth Impression, 1967, "
                    "despite misleading 1909 metadata"
                ),
            }
        ],
        "endorsement": (
            "Internet Archive / Digital Library of India / Advaita Ashrama do "
            "not endorse Antar."
        ),
    },
    "bhagavadgitawith00londiala": {
        "translator": "Annie Besant & Bhagavan Das",
        "defaultTitle": (
            "The Bhagavad-Gita : with Samskrit text, free translation into "
            "English, a word-for-word translation, and an introduction on "
            "Samskrit grammar"
        ),
        "editionTarget": {
            "edition": "1905 joint scholarly edition",
            "year": 1905,
            "publisher": "Theosophical Publishing Society, London and Benares",
            "printer": "Freeman & Co. Ltd., Tara Printing Works, Benares",
            "verification": "Confirm from scan title page after acquisition",
        },
        "rejectedMasters": [
            {
                "itemId": "bhagavadgitaorlo00besa",
                "reason": (
                    "Besant-only Natesan Madras 1922 cheap edition; not the "
                    "1905 joint Besant & Das scholarly printing"
                ),
            },
            {
                "itemId": "wg1100",
                "reason": (
                    "Folkscanomy upload claiming 1905; prefer UC Libraries "
                    "institutional pin bhagavadgitawith00londiala"
                ),
            },
        ],
        "endorsement": (
            "Internet Archive / University of California Libraries / "
            "Theosophical Publishing Society do not endorse Antar."
        ),
    },
}


def build_acquisition_metadata(
    *,
    item_id: str,
    retrieval_timestamp: str,
    user_agent: str,
    ia_metadata: dict[str, Any],
    retained: list[dict[str, Any]],
    pinned_master: str,
) -> dict[str, Any]:
    md = ia_metadata.get("metadata") or {}
    profile = EDITION_PROFILES.get(item_id, {})
    return {
        "platform": "Internet Archive",
        "itemId": item_id,
        "itemUrl": f"https://archive.org/details/{item_id}",
        "metadataApiUrl": metadata_api_url(item_id),
        "retrievalTimestamp": retrieval_timestamp,
        "userAgent": user_agent,
        "status": "ACQUIRED_UNREVIEWED",
        "sourceRole": "PRIMARY_TRANSLATION_CANDIDATE",
        "language": "en",
        "translator": profile.get("translator") or md.get("creator") or "unknown",
        "title": md.get("title") or profile.get("defaultTitle") or item_id,
        "creatorDisplayed": md.get("creator"),
        "dateDisplayed": md.get("date") or md.get("year"),
        "pinnedMasterFilename": pinned_master,
        "editionTarget": profile.get("editionTarget")
        or {
            "edition": "unspecified",
            "year": None,
            "publisher": md.get("publisher"),
            "verification": "Confirm from scan title page after acquisition",
        },
        "rejectedMasters": list(profile.get("rejectedMasters") or []),
        "ocrIsAuthoritative": False,
        "retainedArtifacts": retained,
        "iaMetadataSummary": {
            "title": md.get("title"),
            "creator": md.get("creator"),
            "date": md.get("date"),
            "year": md.get("year"),
            "language": md.get("language"),
            "identifier": md.get("identifier"),
            "identifierArk": md.get("identifier-ark"),
            "publicdate": md.get("publicdate"),
            "collection": md.get("collection"),
        },
        "endorsement": profile.get("endorsement")
        or "Internet Archive does not endorse Antar.",
        "scope": "Chapter 1 inspection acquisition; no Translation approval",
    }


def write_sha256sums(path: Path, entries: list[tuple[str, str]]) -> None:
    """Write SHA256SUMS with local filenames (directory-relative)."""
    lines = [f"{digest}  {name}\n" for digest, name in entries]
    write_bytes_exclusive(path, "".join(lines).encode("utf-8"))


def acquire(
    *,
    item_id: str,
    output_dir: Path,
    filenames: list[str],
    pinned_master: str,
    user_agent: str,
    timeout_sec: int,
    retries: int,
    retry_backoff_sec: float,
) -> dict[str, Any]:
    if pinned_master not in filenames:
        raise AcquisitionError(
            f"Pinned master {pinned_master!r} must be included in --file list"
        )

    retrieval_timestamp = utc_now_iso()
    output_dir.mkdir(parents=True, exist_ok=True)

    meta_bytes = fetch_bytes(
        metadata_api_url(item_id),
        user_agent=user_agent,
        timeout_sec=timeout_sec,
        retries=retries,
        retry_backoff_sec=retry_backoff_sec,
    )
    try:
        ia_metadata = json.loads(meta_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcquisitionError("Invalid JSON from Internet Archive metadata API") from exc
    if not isinstance(ia_metadata, dict):
        raise AcquisitionError("Internet Archive metadata root must be a JSON object")

    file_records = select_file_records(ia_metadata, filenames)

    # Persist full metadata API snapshot (stable keys for review).
    snapshot = {
        "createdBy": "content/acquisition/translation/fetch_internet_archive_item.py",
        "itemId": item_id,
        "metadataApiUrl": metadata_api_url(item_id),
        "retrievalTimestamp": retrieval_timestamp,
        "userAgent": user_agent,
        "response": ia_metadata,
    }
    snapshot_bytes = (json.dumps(snapshot, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    # Retrieval timestamp makes exact bytes non-deterministic across runs; allow
    # overwrite only when caller passes force_metadata via replacing after delete.
    metadata_path = output_dir / "ia-metadata-api.json"
    if metadata_path.exists():
        # Keep prior snapshot if present; acquisition metadata.json carries latest stamp.
        pass
    else:
        write_bytes_exclusive(metadata_path, snapshot_bytes)

    # Also store a compact deterministic-ish working metadata.json (timestamp varies).
    retained: list[dict[str, Any]] = []
    checksum_entries: list[tuple[str, str]] = []

    for name in filenames:
        dest = output_dir / name
        if dest.exists():
            digest = sha256_file(dest)
            status = "unchanged"
            data_len = dest.stat().st_size
        else:
            url = download_url(item_id, name)
            data = fetch_bytes(
                url,
                user_agent=user_agent,
                timeout_sec=timeout_sec,
                retries=retries,
                retry_backoff_sec=retry_backoff_sec,
            )
            status = write_bytes_exclusive(dest, data)
            digest = sha256_bytes(data)
            data_len = len(data)
        record = file_records[name]
        retained.append(
            {
                "filename": name,
                "role": "pinned_master" if name == pinned_master else "retained",
                "format": record.get("format"),
                "sizeBytes": data_len,
                "sha256": digest,
                "iaMd5": record.get("md5"),
                "iaSha1": record.get("sha1"),
                "sourceUrl": download_url(item_id, name),
                "writeStatus": status,
                "authoritativeForTranscription": name == pinned_master,
                "ocrInspectionAidOnly": name.endswith("_djvu.txt"),
            }
        )
        checksum_entries.append((digest, name))

    # Include metadata API snapshot in checksums if written/present.
    if metadata_path.exists():
        meta_digest = sha256_file(metadata_path)
        checksum_entries.append((meta_digest, metadata_path.name))
        retained.append(
            {
                "filename": metadata_path.name,
                "role": "ia_metadata_api_snapshot",
                "format": "JSON",
                "sizeBytes": metadata_path.stat().st_size,
                "sha256": meta_digest,
                "sourceUrl": metadata_api_url(item_id),
                "writeStatus": "present",
                "authoritativeForTranscription": False,
                "ocrInspectionAidOnly": False,
            }
        )

    acquisition_metadata = build_acquisition_metadata(
        item_id=item_id,
        retrieval_timestamp=retrieval_timestamp,
        user_agent=user_agent,
        ia_metadata=ia_metadata,
        retained=retained,
        pinned_master=pinned_master,
    )
    # metadata.json may be refreshed with a new retrieval timestamp when files
    # were already present; always rewrite via explicit replace of this file only.
    metadata_json_path = output_dir / "metadata.json"
    metadata_json_bytes = (
        json.dumps(acquisition_metadata, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if metadata_json_path.exists():
        metadata_json_path.unlink()
    write_bytes_exclusive(metadata_json_path, metadata_json_bytes)
    checksum_entries.append((sha256_bytes(metadata_json_bytes), "metadata.json"))

    sums_path = output_dir / "SHA256SUMS"
    if sums_path.exists():
        sums_path.unlink()
    write_sha256sums(sums_path, checksum_entries)

    return acquisition_metadata


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--item-id", default=DEFAULT_ITEM_ID)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("content/raw/translations/swarupananda-1909"),
    )
    parser.add_argument(
        "--file",
        dest="files",
        action="append",
        default=None,
        help="Filename to retain (repeatable). Defaults to Phase 2 pin set.",
    )
    parser.add_argument(
        "--pinned-master",
        default="2015.386852.Srimad-Bhagavad.pdf",
        help="Filename treated as the authoritative scan master",
    )
    parser.add_argument(
        "--user-agent",
        default=os.environ.get("ANTAR_CONTENT_USER_AGENT", DEFAULT_USER_AGENT),
    )
    parser.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--retry-backoff-sec", type=float, default=DEFAULT_RETRY_BACKOFF_SEC
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    filenames = args.files if args.files else list(DEFAULT_FILES)
    try:
        result = acquire(
            item_id=args.item_id,
            output_dir=args.output_dir,
            filenames=filenames,
            pinned_master=args.pinned_master,
            user_agent=args.user_agent,
            timeout_sec=args.timeout_sec,
            retries=args.retries,
            retry_backoff_sec=args.retry_backoff_sec,
        )
    except AcquisitionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "ok", "itemId": result["itemId"], "retrievalTimestamp": result["retrievalTimestamp"], "retained": [r["filename"] for r in result["retainedArtifacts"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
