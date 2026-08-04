#!/usr/bin/env python3
"""Acquire minimal IIT Kanpur / Gita Supersite root-Sanskrit mool evidence.

Verification-only. Does not approve import. Does not store commentary/Translation.
Fetches exactly one Verse per request from the legacy HTML host that embeds मूल श्लोकः.

robots.txt (old.gitasupersite.in): User-agent * ; Crawl-delay: 10 ; /srimad not Disallow'd.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

DEFAULT_UA = (
    "AntarContentAcquisition/0.1 "
    "(+https://github.com/antar-project/antar; content-acquisition@antar.example)"
)
# Respect Crawl-delay: 10 from old.gitasupersite.in/robots.txt (also >= 2s floor).
DEFAULT_DELAY_SECONDS = 10.0
DEFAULT_TIMEOUT_SECONDS = 60
MAX_ATTEMPTS = 3
REPO_ROOT = Path(__file__).resolve().parents[2]

DEVANAGARI_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")


class AcquisitionError(Exception):
    """Non-retryable acquisition failure."""


class TransientAcquisitionError(AcquisitionError):
    """Retryable transient failure (timeout / 5xx / network blip)."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_id_for(chapter: int, verse: int) -> str:
    return f"bhagavad-gita-sanskrit-iitk-verse-{chapter}.{verse}-verification-v1"


def requested_page_url(chapter: int, verse: int) -> str:
    return (
        "https://www.gitasupersite.iitk.ac.in/srimad"
        f"?choose=1&field_chapter_value={chapter}&field_nsutra_value={verse}"
        "&language=dv&show_mool=1"
    )


def retrieval_url(chapter: int, verse: int) -> str:
    return (
        "https://old.gitasupersite.in/srimad"
        f"?choose=1&language=dv&field_chapter_value={chapter}"
        f"&field_nsutra_value={verse}&show_mool=1"
    )


def evidence_dir(output_root: Path, chapter: int, verse: int) -> Path:
    return output_root / f"verse-{chapter}.{verse}"


def evidence_filename(chapter: int, verse: int) -> str:
    return f"verse-{chapter}.{verse}-mool-evidence.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, *, user_agent: str, timeout: float) -> tuple[str, bytes, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.geturl(), resp.read(), resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        if 500 <= int(exc.code) <= 599:
            raise TransientAcquisitionError(f"HTTP {exc.code} for {url}") from exc
        raise AcquisitionError(f"HTTP {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise TransientAcquisitionError(f"URL error for {url}: {exc}") from exc
    except TimeoutError as exc:
        raise TransientAcquisitionError(f"Timeout for {url}") from exc


def fetch_with_retries(
    url: str,
    *,
    user_agent: str,
    timeout: float,
    max_attempts: int = MAX_ATTEMPTS,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[str, bytes, str]:
    last: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fetch(url, user_agent=user_agent, timeout=timeout)
        except TransientAcquisitionError as exc:
            last = exc
            if attempt >= max_attempts:
                break
            # Bounded backoff between retries (still sequential; no concurrency).
            sleep_fn(min(2.0 * attempt, 6.0))
        except AcquisitionError:
            raise
    assert last is not None
    raise AcquisitionError(f"Exhausted {max_attempts} attempts: {last}") from last


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def html_to_text_fragment(fragment: str) -> str:
    text = fragment
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )
    return text


def verse_marker_candidates(chapter: int, verse: int) -> list[str]:
    ascii_ref = f"{chapter}.{verse}"
    dev_ref = ascii_ref.translate(DEVANAGARI_DIGITS)
    ascii_dash = f"{chapter}-{verse}"
    dev_dash = ascii_dash.translate(DEVANAGARI_DIGITS)
    return [ascii_ref, dev_ref, ascii_dash, dev_dash]


def confirm_verse_identity(text: str, chapter: int, verse: int) -> None:
    markers = verse_marker_candidates(chapter, verse)
    if not any(m in text for m in markers):
        raise AcquisitionError(
            f"Mool text missing Verse {chapter}.{verse} marker "
            f"(looked for {markers})"
        )
    # Fail closed if a different verse marker is the only marker present.
    wrong = re.findall(r"[।|]{1,2}\s*([0-9०-९]+)\s*[.\-–—]\s*([0-9०-९]+)\s*[।|]{0,2}", text)
    if wrong:
        def to_int(s: str) -> int:
            return int(s.translate(str.maketrans("०१२३४५६७८९", "0123456789")))

        for a, b in wrong:
            try:
                if to_int(a) != chapter or to_int(b) != verse:
                    raise AcquisitionError(
                        f"Mool text contains unexpected Verse marker {a}.{b}; "
                        f"expected {chapter}.{verse}"
                    )
            except ValueError as exc:
                raise AcquisitionError(f"Unparseable verse marker {a}.{b}") from exc


def extract_mool_root_text(html: str, *, chapter: int, verse: int) -> str:
    """Extract only the मूल श्लोकः block; fail if ambiguous or identity unclear."""
    if "मूल श्लोकः" not in html:
        raise AcquisitionError("Page does not contain मूल श्लोकः label")

    pattern = re.compile(
        r"मूल श्लोकः</b></font></p>\s*"
        r"<p align=\"center\"><font[^>]*>(.*?)</font>",
        flags=re.S | re.I,
    )
    matches = list(pattern.finditer(html))
    if len(matches) != 1:
        raise AcquisitionError(
            f"Expected exactly one मूल श्लोकः text block, found {len(matches)}"
        )
    fragment = matches[0].group(1)
    text = html_to_text_fragment(fragment)
    banned = ("Translation", "Commentary", "English", "व्याख्या", "टीका", "{{")
    for token in banned:
        if token in fragment or token in text:
            raise AcquisitionError(f"Forbidden non-mool token in mool fragment: {token}")
    cleaned = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not cleaned:
        raise AcquisitionError("Empty mool text after extraction")
    if not re.search(r"[\u0900-\u097F]", cleaned):
        raise AcquisitionError("Mool text lacks Devanagari content")
    confirm_verse_identity(cleaned, chapter, verse)
    return cleaned


def write_exclusive(path: Path, data: bytes) -> str:
    if path.exists():
        if path.read_bytes() == data:
            return "unchanged"
        raise AcquisitionError(f"Refusing silent overwrite of different bytes: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return "written"


def evidence_paths(output_dir: Path, chapter: int, verse: int) -> dict[str, Path]:
    name = evidence_filename(chapter, verse)
    return {
        "evidence": output_dir / name,
        "metadata": output_dir / "metadata.json",
        "sums": output_dir / "SHA256SUMS",
        "readme": output_dir / "README.md",
    }


def load_existing_valid_metadata(output_dir: Path, chapter: int, verse: int) -> dict[str, Any] | None:
    paths = evidence_paths(output_dir, chapter, verse)
    if not paths["evidence"].is_file() or not paths["metadata"].is_file():
        return None
    try:
        evidence = json.loads(paths["evidence"].read_text(encoding="utf-8"))
        metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if evidence.get("canonicalReference") != f"{chapter}.{verse}":
        return None
    if not evidence.get("observedRootText"):
        return None
    if metadata.get("status") != "VERIFICATION_ONLY":
        return None
    return metadata


def write_verse_readme(path: Path, *, chapter: int, verse: int) -> None:
    ref = f"{chapter}.{verse}"
    text = f"""# IIT Kanpur / Gita Supersite — Verse {ref} verification evidence

## Role

`SECONDARY_VERIFICATION_REFERENCE` only.

IIT Kanpur Gita Supersite is used to **verify** Wikisource Verse {ref} root Sanskrit.
It is **not** Antar’s import corpus.

## URLs

| Kind | URL |
|------|-----|
| Requested page URL | {requested_page_url(chapter, verse)} |
| Retrieval URL (embedded mool HTML) | {retrieval_url(chapter, verse)} |

## Status

`VERIFICATION_ONLY` / `VERIFICATION_ONLY_NOT_APPROVED_FOR_REDISTRIBUTION`

## License

| Layer | Status |
|-------|--------|
| Underlying ancient Sanskrit work | Public domain (ancient work) |
| IIT / Gita Supersite digital transcription | **LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION** |

Do not claim redistribution rights that are not explicitly documented.
IIT Kanpur does **not** endorse Antar.

## What is stored

- `{evidence_filename(chapter, verse)}` — minimal observed root Sanskrit + metadata
- `metadata.json` — provenance summary
- `SHA256SUMS`

The **full HTML page is not preserved**.

## What is excluded

- Sanskrit commentary
- English Translation / commentary
- Navigation, forms, audio
- Bulk corpus extraction

## Prohibited uses

- Canonical import into `scripture.verses`
- Bulk corpus harvesting
- Commentary / Translation import
"""
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def acquire_verse(
    *,
    chapter: int,
    verse: int,
    output_root: Path,
    user_agent: str = DEFAULT_UA,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    delay_seconds: float = DEFAULT_DELAY_SECONDS,
    apply_delay: bool = True,
    sleep_fn: Callable[[float], None] = time.sleep,
    fetch_fn: Callable[..., tuple[str, bytes, str]] | None = None,
) -> dict[str, Any]:
    """Acquire one Verse of IIT mool evidence. Never concurrent; delay before fetch when asked."""
    if chapter < 1 or verse < 1:
        raise AcquisitionError("chapter and verse must be positive")
    if delay_seconds < 2.0:
        raise AcquisitionError("delay-seconds must be >= 2 (conservative floor)")

    output_dir = evidence_dir(output_root, chapter, verse)
    output_dir.mkdir(parents=True, exist_ok=True)

    if apply_delay and delay_seconds > 0:
        sleep_fn(delay_seconds)

    retrieval_timestamp = utc_now_iso()
    req_url = requested_page_url(chapter, verse)
    ret_url = retrieval_url(chapter, verse)
    sid = source_id_for(chapter, verse)

    do_fetch = fetch_fn or (
        lambda url: fetch_with_retries(
            url, user_agent=user_agent, timeout=timeout_seconds, sleep_fn=sleep_fn
        )
    )
    final_url, raw, content_type = do_fetch(ret_url)
    html = raw.decode("utf-8")
    title = extract_title(html)
    mool = extract_mool_root_text(html, chapter=chapter, verse=verse)
    root_checksum = sha256_text(mool + "\n")
    ref = f"{chapter}.{verse}"
    evidence_name = evidence_filename(chapter, verse)

    evidence = {
        "schemaVersion": 1,
        "sourceId": sid,
        "sourceRole": "SECONDARY_VERIFICATION_REFERENCE",
        "provider": "IIT Kanpur Gita Supersite (legacy HTML host old.gitasupersite.in)",
        "requestedPageUrl": req_url,
        "retrievalUrl": ret_url,
        "finalUrl": final_url,
        "pageTitle": title,
        "chapterNumber": chapter,
        "verseNumber": verse,
        "canonicalReference": ref,
        "retrievalTimestamp": retrieval_timestamp,
        "retrievalStatus": "ACQUIRED_VERIFICATION_ONLY",
        "contentType": content_type,
        "licenseStatus": "VERIFICATION_ONLY_LICENSE_UNCONFIRMED",
        "licenseDisplayed": "LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION",
        "redistribution": "VERIFICATION_ONLY_NOT_APPROVED_FOR_REDISTRIBUTION",
        "observedRootText": mool,
        "observedRootTextChecksumSha256": root_checksum,
        "normalizationForStorage": [
            "html_br_to_lf",
            "html_tags_stripped_within_mool_font_block_only",
            "trimmed_surrounding_whitespace",
            "preserved_intra_line_punctuation_and_spelling",
        ],
        "excluded": [
            "commentary",
            "translation",
            "navigation",
            "form_controls",
            "audio",
            "unrelated_metadata",
            "full_html_page",
        ],
        "notes": [
            "The requested gitasupersite.iitk.ac.in SPA shell does not embed Verse text without authenticated API access.",
            "Evidence was taken from the legacy Drupal page that still embeds मूल श्लोकः.",
            "IIT Kanpur / Gita Supersite does not endorse Antar.",
            "Do not use this artifact as an Antar import source.",
        ],
    }

    evidence_text = json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    evidence_path = output_dir / evidence_name
    write_exclusive(evidence_path, evidence_text.encode("utf-8"))
    evidence_sha = sha256_text(evidence_text)

    try:
        rel_evidence = str(evidence_path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        rel_evidence = str(evidence_path)

    metadata = {
        "sourceId": sid,
        "sourceRole": "SECONDARY_VERIFICATION_REFERENCE",
        "provider": evidence["provider"],
        "requestedPageUrl": req_url,
        "retrievalUrl": ret_url,
        "finalUrl": final_url,
        "pageTitle": title,
        "chapterNumber": chapter,
        "verseNumber": verse,
        "canonicalReference": ref,
        "retrievalTimestamp": retrieval_timestamp,
        "retrievalStatus": "ACQUIRED_VERIFICATION_ONLY",
        "licenseStatus": "VERIFICATION_ONLY_LICENSE_UNCONFIRMED",
        "licenseDisplayed": "LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION",
        "redistribution": "VERIFICATION_ONLY_NOT_APPROVED_FOR_REDISTRIBUTION",
        "observedRootTextChecksumSha256": root_checksum,
        "evidencePath": rel_evidence,
        "evidenceSha256": evidence_sha,
        "status": "VERIFICATION_ONLY",
    }
    metadata_text = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    write_exclusive(output_dir / "metadata.json", metadata_text.encode("utf-8"))

    sums = (
        f"{evidence_sha}  {evidence_name}\n"
        f"{sha256_text(metadata_text)}  metadata.json\n"
    )
    (output_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")
    write_verse_readme(output_dir / "README.md", chapter=chapter, verse=verse)
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Acquire one IIT/Gita Supersite Verse mool verification evidence."
    )
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--verse", type=int, required=True)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=REPO_ROOT / "content/raw/sanskrit/iit-kanpur",
    )
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--user-agent", default=DEFAULT_UA)
    parser.add_argument(
        "--no-delay",
        action="store_true",
        help="Skip pre-request delay (tests / explicit operator override only).",
    )
    args = parser.parse_args(argv)
    try:
        metadata = acquire_verse(
            chapter=args.chapter,
            verse=args.verse,
            output_root=args.output_root,
            user_agent=args.user_agent,
            timeout_seconds=args.timeout_seconds,
            delay_seconds=args.delay_seconds,
            apply_delay=not args.no_delay,
        )
    except AcquisitionError as exc:
        print(f"acquisition error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
