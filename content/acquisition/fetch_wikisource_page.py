#!/usr/bin/env python3
"""Fetch a Sanskrit Wikisource page revision via the official MediaWiki API.

Writes an untouched API JSON snapshot plus metadata. Does not scrape HTML.
Does not mutate an existing raw revision file silently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_API = "https://sa.wikisource.org/w/api.php"
DEFAULT_USER_AGENT = (
    "AntarContentAcquisition/0.1 "
    "(+https://github.com/antar-project/antar; content-acquisition@antar.example)"
)
DEFAULT_TIMEOUT_SEC = 60


class AcquisitionError(Exception):
    """Fatal acquisition failure."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_query_url(
    api_url: str,
    title: str,
    *,
    revision_id: int | None = None,
    page_id: int | None = None,
) -> str:
    params: dict[str, str] = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "info|revisions",
        "rvprop": "ids|timestamp|size|sha1|content|contentmodel|user|comment",
        "rvslots": "main",
        "inprop": "url|displaytitle",
        "redirects": "1",
    }
    if revision_id is not None:
        # Pin exact revision content via revids (preferred over HTML oldid scraping).
        params["revids"] = str(revision_id)
    elif page_id is not None:
        params["pageids"] = str(page_id)
    else:
        params["titles"] = title
    return f"{api_url}?{urllib.parse.urlencode(params)}"


def fetch_json(url: str, *, user_agent: str, timeout_sec: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=timeout_sec) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise AcquisitionError(f"HTTP error {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise AcquisitionError(f"URL error for {url}: {exc}") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcquisitionError(f"Invalid JSON response from {url}") from exc
    if not isinstance(payload, dict):
        raise AcquisitionError("API response root must be a JSON object")
    return payload


def fetch_site_rights(
    api_url: str, *, user_agent: str, timeout_sec: int
) -> dict[str, Any]:
    url = (
        f"{api_url}?{urllib.parse.urlencode({'action': 'query', 'format': 'json', 'formatversion': '2', 'meta': 'siteinfo', 'siprop': 'rightsinfo|general'})}"
    )
    return fetch_json(url, user_agent=user_agent, timeout_sec=timeout_sec)


def extract_page(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        pages = payload["query"]["pages"]
    except (KeyError, TypeError) as exc:
        raise AcquisitionError("API response missing query.pages") from exc
    if not pages:
        raise AcquisitionError("API response contained no pages")
    page = pages[0]
    if page.get("missing") is True or "pageid" not in page:
        raise AcquisitionError(f"Page missing: {page.get('title')!r}")
    return page


def extract_revision(page: dict[str, Any], expected_revid: int | None) -> dict[str, Any]:
    revisions = page.get("revisions") or []
    if not revisions:
        raise AcquisitionError(f"No revisions returned for page id {page.get('pageid')}")
    revision = revisions[0]
    revid = revision.get("revid")
    if expected_revid is not None and revid != expected_revid:
        raise AcquisitionError(
            f"Expected revision {expected_revid}, API returned {revid}"
        )
    slots = revision.get("slots") or {}
    main = slots.get("main") or {}
    content = main.get("content")
    if content is None:
        content = revision.get("content")
    if not isinstance(content, str) or content == "":
        raise AcquisitionError(f"Revision {revid} has no main wikitext content")
    return revision


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_bytes_exclusive(path: Path, data: bytes) -> str:
    """Write data only if absent. Return 'written' or 'unchanged'.

    Refuses when an existing file has different bytes (no silent mutation).
    """
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


def snapshot_filename(revision_id: int) -> str:
    return f"sa-wikisource-bg-chapter-01-revision-{revision_id}.json"


def build_metadata(
    *,
    title: str,
    page: dict[str, Any],
    revision: dict[str, Any],
    api_query_url: str,
    api_base: str,
    retrieval_timestamp: str,
    user_agent: str,
    rightsinfo: dict[str, Any],
    raw_path: str,
    raw_sha256: str,
    expected_page_id: int | None,
) -> dict[str, Any]:
    page_id = page["pageid"]
    if expected_page_id is not None and page_id != expected_page_id:
        raise AcquisitionError(
            f"Expected page ID {expected_page_id}, API returned {page_id}"
        )
    revid = revision["revid"]
    return {
        "sourceTitle": title,
        "sourceRole": "PRIMARY_TRANSCRIPTION_CANDIDATE",
        "provider": "Sanskrit Wikisource (sa.wikisource.org)",
        "pageUrl": page.get("canonicalurl") or page.get("fullurl"),
        "apiBaseUrl": api_base,
        "apiQueryUrl": api_query_url,
        "pageId": page_id,
        "revisionId": revid,
        "revisionTimestamp": revision.get("timestamp"),
        "revisionSize": revision.get("size"),
        "revisionSha1": revision.get("sha1"),
        "retrievalTimestamp": retrieval_timestamp,
        "userAgent": user_agent,
        "rawPath": raw_path,
        "rawSha256": raw_sha256,
        "status": "ACQUIRED_UNREVIEWED",
        "license": {
            "contributorContent": {
                "name": rightsinfo.get("text")
                or "Creative Commons Attribution-Share Alike 4.0",
                "url": rightsinfo.get("url")
                or "https://creativecommons.org/licenses/by-sa/4.0/",
                "spdx": "CC-BY-SA-4.0",
                "notes": (
                    "Wikisource contributor transcription and markup are generally "
                    "governed by CC BY-SA 4.0 per sa.wikisource.org site rightsinfo."
                ),
            },
            "underlyingWork": {
                "status": "public_domain",
                "notes": (
                    "The underlying ancient Sanskrit Bhagavad Gita text is in the "
                    "public domain. This does not waive attribution duties for the "
                    "Wikisource contributor layer."
                ),
            },
            "endorsement": "Wikisource does not endorse Antar.",
            "attributionRequirements": [
                "Preserve exact page URL",
                "Preserve MediaWiki page ID and revision ID",
                "Preserve retrieval timestamp",
                "Preserve CC BY-SA 4.0 notice for contributor content",
                "Do not imply Wikisource endorsement",
            ],
        },
        "chapterScope": 1,
        "expectedVerseCount": 47,
        "approvedFields": ["sanskrit_transcription", "canonical_verse_markers"],
        "prohibitedFields": [
            "commentary",
            "translations",
            "contributor_ui",
            "navigation_text",
            "unrelated_templates",
        ],
    }


def acquire(
    *,
    title: str,
    output_dir: Path,
    api_url: str,
    user_agent: str,
    timeout_sec: int,
    revision_id: int | None,
    page_id: int | None,
) -> dict[str, Any]:
    retrieval_timestamp = utc_now_iso()
    query_url = build_query_url(
        api_url, title, revision_id=revision_id, page_id=page_id
    )
    payload = fetch_json(query_url, user_agent=user_agent, timeout_sec=timeout_sec)
    page = extract_page(payload)
    revision = extract_revision(page, revision_id)
    rights_payload = fetch_site_rights(
        api_url, user_agent=user_agent, timeout_sec=timeout_sec
    )
    rightsinfo = rights_payload.get("query", {}).get("rightsinfo", {})

    revid = int(revision["revid"])
    raw_name = snapshot_filename(revid)
    raw_path = output_dir / raw_name
    # Store the untouched API response body shape as deterministic UTF-8 JSON.
    # Retrieval timestamp is recorded only in metadata.json.
    raw_text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    raw_bytes = raw_text.encode("utf-8")
    digest = sha256_bytes(raw_bytes)
    write_status = write_bytes_exclusive(raw_path, raw_bytes)

    rel_raw = str(raw_path).replace("\\", "/")
    for marker in ("content/",):
        idx = rel_raw.find(marker)
        if idx >= 0:
            rel_raw = rel_raw[idx:]
            break

    metadata = build_metadata(
        title=page.get("title") or title,
        page=page,
        revision=revision,
        api_query_url=query_url,
        api_base=api_url,
        retrieval_timestamp=retrieval_timestamp,
        user_agent=user_agent,
        rightsinfo=rightsinfo,
        raw_path=rel_raw,
        raw_sha256=digest,
        expected_page_id=page_id,
    )
    metadata["rawWriteStatus"] = write_status
    metadata_path = output_dir / "metadata.json"
    metadata_text = (
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    if metadata_path.exists():
        existing = json.loads(metadata_path.read_text(encoding="utf-8"))
        if existing.get("revisionId") != revid or existing.get("rawSha256") != digest:
            raise AcquisitionError(
                f"Refusing to replace metadata.json for a different "
                f"revision/checksum at {metadata_path}"
            )
        # Keep original retrievalTimestamp for provenance stability on idempotent re-run.
        metadata["retrievalTimestamp"] = existing.get(
            "retrievalTimestamp", retrieval_timestamp
        )
        metadata_text = (
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
    metadata_path.write_text(metadata_text, encoding="utf-8")

    sums_path = output_dir / "SHA256SUMS"
    sums_line = f"{digest}  {raw_name}\n"
    if sums_path.exists():
        lines = [
            ln for ln in sums_path.read_text(encoding="utf-8").splitlines() if ln.strip()
        ]
        if sums_line.strip() not in lines:
            # Do not replace other revision lines; refuse conflicting digest for same name.
            for ln in lines:
                if ln.endswith(f"  {raw_name}") and not ln.startswith(digest):
                    raise AcquisitionError(
                        f"SHA256SUMS already records a different digest for {raw_name}"
                    )
            lines.append(sums_line.strip())
            sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        sums_path.write_text(sums_line, encoding="utf-8")

    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a sa.wikisource.org page revision for Antar raw provenance."
    )
    parser.add_argument(
        "--title",
        default="भगवद्गीता/अर्जुनविषादयोगः",
        help="MediaWiki page title",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("content/raw/sanskrit/wikisource/chapter-01"),
        help="Directory for raw snapshot and metadata",
    )
    parser.add_argument("--api-url", default=DEFAULT_API)
    parser.add_argument(
        "--user-agent",
        default=os.environ.get("ANTAR_CONTENT_USER_AGENT", DEFAULT_USER_AGENT),
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SEC)
    parser.add_argument("--revision-id", type=int, default=343151)
    parser.add_argument("--page-id", type=int, default=164)
    args = parser.parse_args(argv)

    try:
        metadata = acquire(
            title=args.title,
            output_dir=args.output_dir,
            api_url=args.api_url,
            user_agent=args.user_agent,
            timeout_sec=args.timeout,
            revision_id=args.revision_id,
            page_id=args.page_id,
        )
    except AcquisitionError as exc:
        print(f"acquisition error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({
        "status": metadata["status"],
        "pageId": metadata["pageId"],
        "revisionId": metadata["revisionId"],
        "rawPath": metadata["rawPath"],
        "rawSha256": metadata["rawSha256"],
        "retrievalTimestamp": metadata["retrievalTimestamp"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
