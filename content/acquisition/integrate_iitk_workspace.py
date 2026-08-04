#!/usr/bin/env python3
"""Integrate acquired IIT verification evidence into editorial workspace artifacts.

Updates registry + source-comparison. Generates missing review scaffolds.
Never modifies canonical-draft.jsonl. Never sets APPROVED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
_ACQ = Path(__file__).resolve().parent
_TOOLS = REPO_ROOT / "content/editorial/tools"
for p in (_ACQ, _TOOLS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from fetch_iitk_verse import (  # noqa: E402
    evidence_dir,
    evidence_filename,
    load_existing_valid_metadata,
    source_id_for,
)
from generate_review import GenerateError, generate_review  # noqa: E402
from compare_sources import run_chapter, update_review_file  # noqa: E402

WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REGISTRY_PATH = REPO_ROOT / "content/registry/sources.json"
RAW_SUMS = REPO_ROOT / "content/checksums/raw.sha256"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
POLICY_PATH = REPO_ROOT / "content/editorial/normalization-policy.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n",
        encoding="utf-8",
    )


def load_evidence(output_root: Path, chapter: int, verse: int) -> dict[str, Any] | None:
    path = evidence_dir(output_root, chapter, verse) / evidence_filename(chapter, verse)
    if not path.is_file():
        return None
    return load_json(path)


def registry_entry_from_evidence(evidence: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    ref = evidence["canonicalReference"]
    return {
        "id": evidence["sourceId"],
        "title": f"Gita Supersite Verse {ref} mool (IIT Kanpur / legacy host)",
        "creator": "IIT Kanpur Gita Supersite",
        "platform": "Gita Supersite",
        "provider": evidence["provider"],
        "source_url": evidence["requestedPageUrl"],
        "retrieval_url": evidence["retrievalUrl"],
        "final_url": evidence.get("finalUrl") or metadata.get("finalUrl"),
        "retrieval_timestamp": evidence["retrievalTimestamp"],
        "license_displayed": "LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION",
        "license_status": "VERIFICATION_ONLY_LICENSE_UNCONFIRMED",
        "license_catalog_id": None,
        "content_kinds": ["sanskrit"],
        "source_role": "SECONDARY_VERIFICATION_REFERENCE",
        "chapter_scope": evidence["chapterNumber"],
        "verse_scope": ref,
        "expected_verse_count": 1,
        "matches_antar_numbering": True,
        "raw_path": metadata.get("evidencePath")
        or f"content/raw/sanskrit/iit-kanpur/verse-{ref}/verse-{ref}-mool-evidence.json",
        "sha256": metadata["evidenceSha256"],
        "observed_root_text_sha256": evidence["observedRootTextChecksumSha256"],
        "approved_fields": ["verification_checksum", "comparison_evidence"],
        "prohibited_fields": [
            "canonical_import",
            "bulk_corpus_extraction",
            "commentary_import",
            "translation_import",
        ],
        "prohibited_uses": [
            "canonical_import",
            "bulk_corpus_extraction",
            "commentary_import",
            "translation_import",
        ],
        "status": "VERIFICATION_ONLY",
        "inspection_doc": f"content/raw/sanskrit/iit-kanpur/verse-{ref}/README.md",
        "editorial_workspace": f"content/editorial/reviews/{ref}.md",
        "decision_summary": (
            f"Verification-only mool evidence for Verse {ref}. "
            "Not approved for canonical import. License for redistribution unconfirmed."
        ),
        "known_caveats": [
            "Requested SPA URL does not embed mool without authenticated API access.",
            "Evidence retrieved from legacy Drupal host old.gitasupersite.in.",
            "Digital transcription redistribution rights not established by this task.",
            "IIT Kanpur does not endorse Antar.",
            "Do not place this transcription into the canonical corpus.",
        ],
        "updated_at": date.today().isoformat(),
    }


def upsert_registry(entries: list[dict[str, Any]]) -> int:
    data = load_json(REGISTRY_PATH)
    by_id = {s["id"]: s for s in data.get("sources") or []}
    changed = 0
    for entry in entries:
        prev = by_id.get(entry["id"])
        if prev != entry:
            by_id[entry["id"]] = entry
            changed += 1
    # Preserve order: existing first, then new ids sorted
    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for s in data.get("sources") or []:
        sid = s["id"]
        ordered.append(by_id[sid])
        seen.add(sid)
    for sid in sorted(by_id.keys()):
        if sid not in seen:
            ordered.append(by_id[sid])
    data["sources"] = ordered
    REGISTRY_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return changed


def append_raw_checksums(paths_and_digests: list[tuple[str, str]]) -> None:
    """paths_and_digests: list of (sha256, repo-relative-path)."""
    existing = RAW_SUMS.read_text(encoding="utf-8") if RAW_SUMS.is_file() else ""
    lines = existing.splitlines()
    by_path: dict[str, str] = {}
    comment_lines: list[str] = []
    for line in lines:
        if not line.strip() or line.startswith("#"):
            if line.startswith("#"):
                comment_lines.append(line)
            continue
        parts = line.split()
        if len(parts) >= 2:
            by_path[parts[-1]] = parts[0]
    for digest, rel in paths_and_digests:
        by_path[rel] = digest
    if not comment_lines:
        comment_lines = [
            "# SHA-256 checksums for content/raw artifacts.",
            "# Format: <sha256>  <repo-relative-path>",
        ]
    body = [f"{by_path[rel]}  {rel}" for rel in sorted(by_path.keys())]
    RAW_SUMS.write_text("\n".join(comment_lines + body) + "\n", encoding="utf-8")


def iitk_source_comparison_entry(evidence: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidenceChecksum": metadata["evidenceSha256"],
        "licenseStatus": "VERIFICATION_ONLY_LICENSE_UNCONFIRMED",
        "notes": [
            "verification_only",
            "extracted_mool_block_only",
            "legacy_html_host_used_because_spa_lacks_embedded_mool",
            "LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION",
        ],
        "retrievedAt": evidence["retrievalTimestamp"],
        "sanskritText": evidence["observedRootText"],
        "sourceChecksum": evidence["observedRootTextChecksumSha256"],
        "sourceId": evidence["sourceId"],
        "sourceReference": evidence["canonicalReference"],
        "sourceRole": "SECONDARY_VERIFICATION_REFERENCE",
        "transliteration": None,
    }


def apply_evidence_to_record(
    record: dict[str, Any],
    *,
    evidence: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    acquisition_failed: bool,
) -> dict[str, Any]:
    """Return updated comparison record. Preserves Wikisource. Never APPROVED."""
    out = {k: record[k] for k in record}
    sources = [
        s
        for s in (record.get("sources") or [])
        if not str(s.get("sourceId", "")).startswith("bhagavad-gita-sanskrit-iitk-verse-")
    ]
    notes = list(record.get("notes") or [])
    notes = [
        n
        for n in notes
        if n
        not in {
            "IIT Kanpur added as SECONDARY_VERIFICATION_REFERENCE only.",
            "IIT acquisition failed or evidence unusable.",
            "Two unambiguous sources present; awaiting automated comparison / human review.",
        }
    ]

    if evidence and metadata:
        sources.append(iitk_source_comparison_entry(evidence, metadata))
        notes.append("IIT Kanpur added as SECONDARY_VERIFICATION_REFERENCE only.")
        notes.append(
            "Two unambiguous sources present; awaiting automated comparison / human review."
        )
        out["status"] = "READY_FOR_REVIEW"
    elif acquisition_failed:
        notes.append("IIT acquisition failed or evidence unusable.")
        out["status"] = "SOURCE_MISSING"
    else:
        if len(sources) < 2 and out.get("status") not in {"SOURCE_CONFLICT"}:
            out["status"] = record.get("status") or "READY_FOR_REVIEW"

    out["sources"] = sources
    out["notes"] = notes
    if out.get("status") == "APPROVED":
        out["status"] = "READY_FOR_REVIEW"
    return out


def integrate_range(
    *,
    chapter: int,
    verse_start: int,
    verse_end: int,
    output_root: Path,
    failed_refs: set[str] | None = None,
    run_comparison: bool = True,
    update_reviews: bool = True,
) -> dict[str, Any]:
    failed_refs = failed_refs or set()
    comparison_path = CHAPTER_DIR / "source-comparison.jsonl"
    records = load_jsonl(comparison_path)
    by_ref = {r["canonicalReference"]: r for r in records}

    registry_entries: list[dict[str, Any]] = []
    checksum_rows: list[tuple[str, str]] = []
    updated_refs: list[str] = []
    missing_refs: list[str] = []

    for verse in range(verse_start, verse_end + 1):
        ref = f"{chapter}.{verse}"
        record = by_ref.get(ref)
        if record is None:
            continue
        meta = load_existing_valid_metadata(
            evidence_dir(output_root, chapter, verse), chapter, verse
        )
        evidence = load_evidence(output_root, chapter, verse)
        failed = ref in failed_refs or (evidence is None and meta is None)
        if evidence and meta:
            by_ref[ref] = apply_evidence_to_record(
                record, evidence=evidence, metadata=meta, acquisition_failed=False
            )
            registry_entries.append(registry_entry_from_evidence(evidence, meta))
            checksum_rows.append((meta["evidenceSha256"], meta["evidencePath"]))
            updated_refs.append(ref)
        else:
            by_ref[ref] = apply_evidence_to_record(
                record, evidence=None, metadata=None, acquisition_failed=failed
            )
            if failed:
                missing_refs.append(ref)

    # Preserve 1.1 and any verses outside range unchanged except rewrite order
    new_rows = [by_ref[r["canonicalReference"]] for r in records]
    write_jsonl(comparison_path, new_rows)

    if registry_entries:
        upsert_registry(registry_entries)
    if checksum_rows:
        append_raw_checksums(checksum_rows)

    # Generate review scaffolds for missing files
    generated_reviews: list[str] = []
    if update_reviews:
        for verse in range(verse_start, verse_end + 1):
            ref = f"{chapter}.{verse}"
            path = REVIEWS_DIR / f"{ref}.md"
            if path.exists():
                continue
            try:
                generate_review(
                    chapter=chapter,
                    verse=verse,
                    reviews_dir=REVIEWS_DIR,
                    status="READY_FOR_REVIEW"
                    if ref in updated_refs
                    else "UNREVIEWED",
                )
                generated_reviews.append(ref)
            except GenerateError:
                # If READY_FOR_REVIEW rejected, force unreviewed scaffold
                generate_review(
                    chapter=chapter,
                    verse=verse,
                    reviews_dir=REVIEWS_DIR,
                    force_unreviewed=True,
                )
                generated_reviews.append(ref)

    comparison_outcome = None
    if run_comparison:
        comparison_outcome = run_chapter(
            chapter_dir=CHAPTER_DIR,
            policy_path=POLICY_PATH,
            reference=None,
            update_reviews=update_reviews,
            set_under_review=False,
        )
        from compare_sources import write_summary

        write_summary(
            CHAPTER_DIR,
            comparison_outcome["results"],
            comparison_outcome["sample"],
        )

    return {
        "updatedReferences": updated_refs,
        "missingReferences": missing_refs,
        "generatedReviews": generated_reviews,
        "comparison": {
            "resultCount": len(comparison_outcome["results"]) if comparison_outcome else 0,
            "reportSha256": comparison_outcome["runMeta"]["reportSha256"]
            if comparison_outcome
            else None,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Integrate IIT evidence into editorial workspace")
    parser.add_argument("--chapter", type=int, default=1)
    parser.add_argument("--verse-start", type=int, required=True)
    parser.add_argument("--verse-end", type=int, required=True)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=REPO_ROOT / "content/raw/sanskrit/iit-kanpur",
    )
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--skip-comparison", action="store_true")
    parser.add_argument("--skip-reviews", action="store_true")
    args = parser.parse_args(argv)

    failed: set[str] = set()
    if args.manifest and args.manifest.is_file():
        man = load_json(args.manifest)
        failed = {f["canonicalReference"] for f in man.get("failed") or []}

    outcome = integrate_range(
        chapter=args.chapter,
        verse_start=args.verse_start,
        verse_end=args.verse_end,
        output_root=args.output_root,
        failed_refs=failed,
        run_comparison=not args.skip_comparison,
        update_reviews=not args.skip_reviews,
    )
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
