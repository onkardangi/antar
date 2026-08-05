#!/usr/bin/env python3
"""Controlled batch approval for Chapter NORMALIZATION_MATCH candidates.

Never approves SOURCE_CONFLICT. Never invents Sanskrit. Never builds packages.
Requires explicit --apply; --dry-run validates and reports with zero mutations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_reviews import (  # noqa: E402
    split_sections,
    validate_review_text,
)

WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
POLICY_PATH = REPO_ROOT / "content/editorial/batch-normalization-match-approval-policy.json"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
REGISTRY_PATH = REPO_ROOT / "content/registry/sources.json"
DECISION_TYPE = "BATCH_NORMALIZATION_MATCH_APPROVAL"
EXPECTED_CANDIDATES = 34
EXPECTED_CONFLICTS = 13
EXPECTED_VERSES = 47


class ApprovalError(Exception):
    """Batch eligibility or atomic apply failure."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n"


def load_registry_map(path: Path = REGISTRY_PATH) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    sources = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(sources, list):
        raise ApprovalError(f"{path}: expected sources array")
    out: dict[str, dict[str, Any]] = {}
    for entry in sources:
        if isinstance(entry, dict) and "id" in entry:
            out[str(entry["id"])] = entry
    return out


def decision_id_for(ref: str, decision_date: str) -> str:
    return f"batch-norm-match-ch01-{ref}-{decision_date}"


def editorial_approval_checksum(
    *,
    ref: str,
    decision_id: str,
    sanskrit_text: str,
    selected_source_id: str,
    supporting_source_ids: list[str],
    reviewer_id: str,
    decision_date: str,
    decision_type: str,
) -> str:
    material = json.dumps(
        {
            "canonicalReference": ref,
            "decisionDate": decision_date,
            "decisionId": decision_id,
            "decisionType": decision_type,
            "reviewerId": reviewer_id,
            "sanskritText": sanskrit_text,
            "selectedSourceId": selected_source_id,
            "supportingSourceIds": supporting_source_ids,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256_text(material)


def difference_categories(candidate: dict[str, Any]) -> list[str]:
    return [str(d.get("category")) for d in (candidate.get("differences") or [])]


def wiki_and_iitk(
    comparison: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = comparison.get("sources") or []
    wiki = next((s for s in sources if s.get("sourceId") == WIKISOURCE_ID), None)
    iitk = next((s for s in sources if "iitk" in str(s.get("sourceId", ""))), None)
    if wiki is None or iitk is None:
        raise ApprovalError(
            f"{comparison.get('canonicalReference')}: missing Wikisource or IIT source evidence"
        )
    return wiki, iitk


def validate_eligibility(
    *,
    chapter_dir: Path,
    reviews_dir: Path,
    registry: dict[str, dict[str, Any]],
    policy: dict[str, Any],
    reviewer_id: str,
    reviewer_name: str,
) -> tuple[list[dict[str, Any]], list[str], dict[str, Any]]:
    if not reviewer_id.strip():
        raise ApprovalError("missing reviewer id")
    if not reviewer_name.strip():
        raise ApprovalError("missing reviewer name")
    if policy.get("requiresSecondReviewer"):
        raise ApprovalError(
            "policy requires a second reviewer; cannot proceed without inventing one"
        )

    cand_path = chapter_dir / "normalization-match-approval-candidate.jsonl"
    conf_path = chapter_dir / "source-conflict-analysis.jsonl"
    draft_path = chapter_dir / "canonical-draft.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    report_path = chapter_dir / "automated-comparison-report.jsonl"
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"

    for path in (cand_path, conf_path, draft_path, comparison_path, report_path, manifest_path):
        if not path.is_file():
            raise ApprovalError(f"missing required file: {path}")

    candidates = load_jsonl(cand_path)
    conflicts = load_jsonl(conf_path)
    draft_rows = load_jsonl(draft_path)
    comparisons = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)}
    reports = {r["canonicalReference"]: r for r in load_jsonl(report_path)}
    conflict_refs = [c["canonicalReference"] for c in conflicts]
    conflict_set = set(conflict_refs)

    if len(candidates) != EXPECTED_CANDIDATES:
        raise ApprovalError(
            f"expected {EXPECTED_CANDIDATES} NORMALIZATION_MATCH candidates, "
            f"found {len(candidates)}"
        )
    if len(conflicts) != EXPECTED_CONFLICTS:
        raise ApprovalError(
            f"expected {EXPECTED_CONFLICTS} SOURCE_CONFLICT records, found {len(conflicts)}"
        )

    cand_refs = [c["canonicalReference"] for c in candidates]
    if len(cand_refs) != len(set(cand_refs)):
        raise ApprovalError("duplicate candidate references")
    if set(cand_refs) & conflict_set:
        raise ApprovalError("candidate/conflict overlap")
    expected = {f"1.{i}" for i in range(1, EXPECTED_VERSES + 1)}
    if set(cand_refs) | conflict_set != expected:
        raise ApprovalError("Chapter 1 partition incomplete (must be 34 + 13 = 47)")

    draft_by_ref = {r["canonicalReference"]: r for r in draft_rows}
    if len(draft_rows) != EXPECTED_VERSES:
        raise ApprovalError(f"canonical-draft must have {EXPECTED_VERSES} rows")

    # Idempotent re-run: already approved with matching evidence is allowed.
    eligible: list[dict[str, Any]] = []
    for candidate in candidates:
        ref = candidate["canonicalReference"]
        errors: list[str] = []

        if ref in conflict_set:
            errors.append("Verse is in SOURCE_CONFLICT set")
        if candidate.get("classification") != "NORMALIZATION_MATCH":
            errors.append("classification is not NORMALIZATION_MATCH")
        report = reports.get(ref) or {}
        if report.get("classification") != "NORMALIZATION_MATCH":
            errors.append("automated report classification is not NORMALIZATION_MATCH")
        if report.get("classification") == "SOURCE_CONFLICT":
            errors.append("SOURCE_CONFLICT cannot be approved")

        status = candidate.get("approvalStatus")
        draft = draft_by_ref.get(ref)
        if draft is None:
            errors.append("missing canonical-draft row")
        already_approved = (
            draft is not None and draft.get("approvalStatus") == "APPROVED"
        )
        if status not in {"PENDING", "APPROVED"}:
            errors.append(f"candidate approvalStatus {status!r} not eligible")
        if status == "APPROVED" and not already_approved:
            errors.append("candidate APPROVED but draft is not APPROVED")
        if not already_approved and status != "PENDING":
            errors.append("candidate approvalStatus must be PENDING before first apply")

        selected_id = candidate.get("selectedSourceId")
        if selected_id != WIKISOURCE_ID:
            errors.append("selected source must be Wikisource primary candidate")
        selected_entry = registry.get(str(selected_id))
        if selected_entry is None:
            errors.append(f"selected source not registered: {selected_id}")
        else:
            role = selected_entry.get("source_role") or selected_entry.get("sourceRole")
            if role != policy.get("requiredSelectedSourceRole"):
                errors.append(
                    f"selected source role must be {policy.get('requiredSelectedSourceRole')}"
                )

        supporting_ids = list(candidate.get("supportingSourceIds") or [])
        if len(supporting_ids) < 1:
            errors.append("missing supporting IIT source")
        for sid in supporting_ids:
            entry = registry.get(str(sid))
            if entry is None:
                errors.append(f"supporting source not registered: {sid}")
                continue
            role = entry.get("source_role") or entry.get("sourceRole")
            if role != policy.get("requiredSupportingSourceRole"):
                errors.append(
                    f"{sid}: supporting role must be "
                    f"{policy.get('requiredSupportingSourceRole')}"
                )
            if entry.get("status") in {
                "APPROVED_FOR_IMPORT",
                "APPROVED_FOR_NORMALIZATION",
                "IMPORTED",
            }:
                errors.append(f"{sid}: IIT must remain verification-only")

        comparison = comparisons.get(ref)
        if comparison is None:
            errors.append("missing source-comparison record")
        else:
            wiki, iitk = wiki_and_iitk(comparison)
            proposed = candidate.get("proposedSanskritText")
            if not isinstance(proposed, str) or not proposed.strip():
                errors.append("proposed Sanskrit missing")
            elif proposed != wiki.get("sanskritText"):
                errors.append("proposed Sanskrit is not exact Wikisource copy")
            expected_cs = sha256_text(proposed or "")
            if candidate.get("proposedSanskritTextChecksumSha256") != expected_cs:
                errors.append("selected Sanskrit checksum mismatch")
            if candidate.get("selectedSourceChecksum") != wiki.get("sourceChecksum"):
                errors.append("selected-source checksum mismatch")
            if candidate.get("proposedTransliteration") is not None:
                errors.append("transliteration must remain null")

            cats = difference_categories(candidate)
            substantive = set(cats) & {
                "SPEAKER_LABEL",
                "ORTHOGRAPHY_UNAPPROVED",
                "WORD_DIFFERENCE",
                "WORD_ORDER",
                "MISSING_TEXT",
                "EXTRA_TEXT",
                "SEGMENTATION",
                "SOURCE_ERROR",
            }
            if substantive:
                errors.append(f"unresolved substantive differences: {sorted(substantive)}")

            if "FRONT_MATTER" in cats:
                fm = policy.get("frontMatterPolicy") or {}
                if not fm.get("batchEligible"):
                    errors.append("FRONT_MATTER present; batch policy does not permit approval")
                # Retention of exact selected source text is the explicit boundary decision.
                if proposed != wiki.get("sanskritText"):
                    errors.append("FRONT_MATTER Verse lacks explicit proposed canonical text")

            if iitk.get("sourceRole") not in {
                None,
                "SECONDARY_VERIFICATION_REFERENCE",
            } and iitk.get("sourceRole") != policy.get("requiredSupportingSourceRole"):
                # source-comparison may omit role; registry is authoritative
                pass

        review_path = reviews_dir / f"{ref}.md"
        if not review_path.is_file():
            errors.append(f"missing review file {review_path.name}")
        else:
            review_errors = validate_review_text(
                review_path.read_text(encoding="utf-8"),
                expected_ref=ref,
                path_label=str(review_path),
            )
            if already_approved:
                # Idempotent re-run: review must already be a valid APPROVED file.
                if review_errors:
                    errors.extend(review_errors)
            else:
                # Pre-approval: allow blank Approval fields; fail on structural issues.
                structural = [
                    e
                    for e in review_errors
                    if "Approval fields must be blank" not in e
                    and "APPROVED requires" not in e
                ]
                if structural:
                    errors.extend(structural)

        if already_approved and draft is not None:
            # Conflicting evidence rejects whole batch.
            if draft.get("sanskritText") != candidate.get("proposedSanskritText"):
                errors.append("already-approved draft Sanskrit conflicts with candidate")
            if draft.get("transliteration") is not None:
                errors.append("already-approved draft transliteration must be null")
            if draft.get("classification") not in {None, "NORMALIZATION_MATCH"}:
                errors.append("already-approved draft has conflicting classification")
        if errors:
            raise ApprovalError(f"{ref}: " + "; ".join(errors))

        eligible.append(candidate)

    if len(eligible) != EXPECTED_CANDIDATES:
        raise ApprovalError(
            f"eligible count {len(eligible)} != expected {EXPECTED_CANDIDATES}; "
            "refusing partial batch"
        )

    context = {
        "candidates": candidates,
        "conflicts": conflicts,
        "conflict_refs": conflict_refs,
        "draft_rows": draft_rows,
        "draft_by_ref": draft_by_ref,
        "comparisons": comparisons,
        "reports": reports,
        "manifest": load_json(manifest_path),
    }
    return eligible, conflict_refs, context


def build_approved_draft_row(
    *,
    candidate: dict[str, Any],
    existing: dict[str, Any],
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
) -> dict[str, Any]:
    ref = candidate["canonicalReference"]
    sanskrit = candidate["proposedSanskritText"]
    supporting_ids = list(candidate.get("supportingSourceIds") or [])
    selected_id = candidate["selectedSourceId"]
    decision_id = decision_id_for(ref, decision_date)
    cats = difference_categories(candidate)
    rules = list(candidate.get("normalizationRulesApplied") or [])
    approval_cs = editorial_approval_checksum(
        ref=ref,
        decision_id=decision_id,
        sanskrit_text=sanskrit,
        selected_source_id=selected_id,
        supporting_source_ids=supporting_ids,
        reviewer_id=reviewer_id,
        decision_date=decision_date,
        decision_type=DECISION_TYPE,
    )
    source_checksums: dict[str, str] = {
        selected_id: str(candidate.get("selectedSourceChecksum"))
    }
    for sid, meta in (candidate.get("supportingSourceChecksums") or {}).items():
        if isinstance(meta, dict) and meta.get("sourceChecksum"):
            source_checksums[str(sid)] = str(meta["sourceChecksum"])
        elif isinstance(meta, str):
            source_checksums[str(sid)] = meta

    notes = [
        f"decisionType={DECISION_TYPE}",
        f"classification=NORMALIZATION_MATCH",
        f"normalizationCategories={','.join(cats)}",
        f"normalizationRulesApplied={','.join(rules)}",
        str(candidate.get("selectionReason") or ""),
        "IIT is verification-only and not the imported source.",
    ]
    if "FRONT_MATTER" in cats:
        notes.append(
            "Front matter retained as present in selected Wikisource text; "
            "no silent strip or rewrite."
        )

    row = dict(existing)
    row.update(
        {
            "chapterNumber": int(candidate["chapterNumber"]),
            "verseNumber": int(candidate["verseNumber"]),
            "canonicalReference": ref,
            "sanskritText": sanskrit,
            "transliteration": None,
            "approvalStatus": "APPROVED",
            "approvedSourceIds": [selected_id] + supporting_ids,
            "editorialNotes": notes,
            "contentVersion": int(existing.get("contentVersion") or 1),
            "editorialDecisionId": decision_id,
            "editorialApprovalChecksum": approval_cs,
            "reviewerId": reviewer_id,
            "reviewer": reviewer_name,
            "secondReviewerId": None,
            "approvalDate": decision_date,
            "decisionType": DECISION_TYPE,
            "selectedSourceId": selected_id,
            "supportingSourceIds": supporting_ids,
            "sourceChecksums": source_checksums,
            "classification": "NORMALIZATION_MATCH",
            "selectedSourceChecksum": candidate.get("selectedSourceChecksum"),
            "supportingSourceChecksums": candidate.get("supportingSourceChecksums"),
        }
    )
    return row


def build_approval_result_row(
    *,
    candidate: dict[str, Any],
    draft_row: dict[str, Any],
    review_path: Path,
    reviewer_id: str,
    decision_date: str,
) -> dict[str, Any]:
    ref = candidate["canonicalReference"]
    return {
        "approvalStatus": "APPROVED",
        "approvalClassification": DECISION_TYPE,
        "canonicalReference": ref,
        "canonicalDraftRecordChecksum": sha256_text(
            json.dumps(draft_row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ),
        "decisionDate": decision_date,
        "editorialDecisionId": draft_row["editorialDecisionId"],
        "reviewFileChecksum": sha256_file(review_path),
        "reviewerId": reviewer_id,
        "selectedSanskritChecksum": candidate["proposedSanskritTextChecksumSha256"],
        "selectedSourceId": candidate["selectedSourceId"],
        "supportingSourceIds": list(candidate.get("supportingSourceIds") or []),
    }


def update_review_markdown(
    text: str,
    *,
    ref: str,
    candidate: dict[str, Any],
    reviewer_name: str,
    reviewer_id: str,
    decision_date: str,
    decision_id: str,
) -> str:
    sections = split_sections(text)
    cats = difference_categories(candidate)
    supporting = ", ".join(f"`{s}`" for s in (candidate.get("supportingSourceIds") or []))
    decision_lines = [
        f"Selected Wikisource (`{candidate['selectedSourceId']}`) as canonical Sanskrit "
        "transcription (exact selected-source copy; no synthesis).",
        "",
        f"IIT Kanpur ({supporting}) used as secondary verification only — not an import source.",
        "",
        "Match accepted after documented comparison-only normalization "
        f"(categories: {', '.join(cats)}).",
        "",
        f"Decision type: `{DECISION_TYPE}`.",
        f"Editorial decision ID: `{decision_id}`.",
    ]
    if "FRONT_MATTER" in cats:
        decision_lines.extend(
            [
                "",
                "Front matter retained exactly as present in the selected Wikisource poem body; "
                "boundary was not silently stripped or rewritten. Canonical text equals the "
                "batch candidate `proposedSanskritText`.",
            ]
        )
    sections["Status"] = "APPROVED"
    sections["Decision"] = "\n".join(decision_lines)
    sections["Approval"] = "\n".join(
        [
            f"Reviewer: {reviewer_name}",
            f"Reviewer ID: {reviewer_id}",
            "Second Reviewer:",
            f"Date: {decision_date}",
        ]
    )
    audit = sections.get("Audit Log", "").rstrip() + "\n"
    audit += (
        f"- {decision_date} — Batch `{DECISION_TYPE}` by `{reviewer_id}` "
        f"({reviewer_name}). Selected Wikisource as canonical transcription; "
        f"IIT verification-only. Decision `{decision_id}`. Status set to `APPROVED`.\n"
    )
    sections["Audit Log"] = audit.rstrip("\n")

    # Preserve section order from original + required schema.
    order = [
        "Canonical Reference",
        "Status",
        "Sources",
        "Source Comparison",
        "Differences",
        "Editorial Notes",
        "Decision",
        "Approval",
        "Audit Log",
    ]
    # Keep any unexpected sections after required ones.
    for name in sections:
        if name not in order:
            order.append(name)

    parts: list[str] = []
    for name in order:
        if name not in sections:
            continue
        body = sections[name]
        parts.append(f"# {name}\n\n{body.strip()}\n")
    updated = "\n".join(parts)
    if not updated.endswith("\n"):
        updated += "\n"
    # Ensure canonical reference line preserved
    if split_sections(updated).get("Canonical Reference", "").strip().splitlines()[0].strip() != ref:
        raise ApprovalError(f"{ref}: review update lost canonical reference")
    errs = validate_review_text(updated, expected_ref=ref, path_label=f"{ref}.md")
    if errs:
        raise ApprovalError(f"{ref}: invalid updated review: {errs}")
    return updated


def build_manifest(
    existing: dict[str, Any],
    *,
    reviewer_id: str,
    decision_date: str,
) -> dict[str, Any]:
    manifest = dict(existing)
    manifest.update(
        {
            "normalizationMatchCandidates": EXPECTED_CANDIDATES,
            "sourceConflicts": EXPECTED_CONFLICTS,
            "approved": EXPECTED_CANDIDATES,
            "rejected": 0,
            "pending": EXPECTED_CONFLICTS,
            "reviewer": reviewer_id,
            "secondReviewer": None,
            "decisionDate": decision_date,
            "status": "PARTIALLY_APPROVED",
            "decisionType": DECISION_TYPE,
            "importReady": False,
            "notes": [
                "PARTIALLY_APPROVED: 34 NORMALIZATION_MATCH Verses approved; "
                "13 SOURCE_CONFLICT Verses remain unresolved.",
                "Chapter is not import-ready. No package or database import authorized.",
                "Selected canonical source: Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE.",
                "IIT remains SECONDARY_VERIFICATION_REFERENCE / verification-only.",
            ],
        }
    )
    return manifest


def snapshot_paths(
    chapter_dir: Path,
    reviews_dir: Path,
    refs: list[str],
) -> dict[str, str]:
    paths = [
        chapter_dir / "canonical-draft.jsonl",
        chapter_dir / "chapter-01-approval-manifest.json",
        chapter_dir / "normalization-match-approval-candidate.jsonl",
        chapter_dir / "source-conflict-analysis.jsonl",
        chapter_dir / "source-comparison.jsonl",
    ]
    for ref in refs:
        paths.append(reviews_dir / f"{ref}.md")
    result_path = chapter_dir / "normalization-match-approval-result.jsonl"
    out: dict[str, str] = {}
    for path in paths:
        if path.is_file():
            out[str(path.resolve())] = sha256_file(path)
        else:
            out[str(path.resolve())] = ""
    # Result file may be absent before first apply.
    out[str(result_path.resolve())] = (
        sha256_file(result_path) if result_path.is_file() else ""
    )
    return out


def assert_unchanged(baseline: dict[str, str], paths: list[Path]) -> None:
    for path in paths:
        key = str(path.resolve())
        if key not in baseline:
            continue
        current = sha256_file(path) if path.is_file() else ""
        if current != baseline[key]:
            raise ApprovalError(
                f"refusing to overwrite unrelated human change detected in {path}"
            )


def render_report(
    *,
    dry_run: bool,
    eligible_refs: list[str],
    conflict_refs: list[str],
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
) -> dict[str, Any]:
    return {
        "mode": "dry-run" if dry_run else "apply",
        "eligibleCount": len(eligible_refs),
        "eligibleReferences": eligible_refs,
        "unresolvedConflictCount": len(conflict_refs),
        "unresolvedConflictReferences": conflict_refs,
        "reviewerId": reviewer_id,
        "reviewerName": reviewer_name,
        "decisionDate": decision_date,
        "decisionType": DECISION_TYPE,
        "secondReviewer": None,
        "chapterImportReady": False,
        "mutations": 0 if dry_run else None,
    }


def apply_batch(
    *,
    chapter_dir: Path,
    reviews_dir: Path,
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
    dry_run: bool,
    apply: bool,
) -> dict[str, Any]:
    if dry_run == apply:
        raise ApprovalError("specify exactly one of --dry-run or --apply")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", decision_date):
        raise ApprovalError("decision-date must be YYYY-MM-DD")

    policy = load_json(POLICY_PATH)
    registry = load_registry_map()
    eligible, conflict_refs, ctx = validate_eligibility(
        chapter_dir=chapter_dir,
        reviews_dir=reviews_dir,
        registry=registry,
        policy=policy,
        reviewer_id=reviewer_id,
        reviewer_name=reviewer_name,
    )
    eligible_refs = [c["canonicalReference"] for c in eligible]
    report = render_report(
        dry_run=dry_run,
        eligible_refs=eligible_refs,
        conflict_refs=conflict_refs,
        reviewer_id=reviewer_id,
        reviewer_name=reviewer_name,
        decision_date=decision_date,
    )
    if dry_run:
        report["mutations"] = 0
        report["ok"] = True
        return report

    # Baseline checksums for conflict files + all targets (detect concurrent edits).
    baseline = snapshot_paths(chapter_dir, reviews_dir, eligible_refs + conflict_refs)
    conflict_review_bytes = {
        ref: (reviews_dir / f"{ref}.md").read_bytes()
        for ref in conflict_refs
        if (reviews_dir / f"{ref}.md").is_file()
    }
    conflict_analysis_bytes = (
        chapter_dir / "source-conflict-analysis.jsonl"
    ).read_bytes()
    comparison_bytes = (chapter_dir / "source-comparison.jsonl").read_bytes()
    candidate_bytes = (
        chapter_dir / "normalization-match-approval-candidate.jsonl"
    ).read_bytes()

    with tempfile.TemporaryDirectory(prefix="antar-norm-match-approve-") as tmp:
        staging = Path(tmp)
        stage_chapter = staging / "chapter-01"
        stage_reviews = staging / "reviews"
        stage_chapter.mkdir()
        stage_reviews.mkdir()

        # Copy inputs into staging.
        for name in (
            "canonical-draft.jsonl",
            "chapter-01-approval-manifest.json",
            "normalization-match-approval-candidate.jsonl",
            "source-conflict-analysis.jsonl",
            "source-comparison.jsonl",
            "automated-comparison-report.jsonl",
        ):
            shutil.copy2(chapter_dir / name, stage_chapter / name)
        for ref in eligible_refs + conflict_refs:
            src = reviews_dir / f"{ref}.md"
            if src.is_file():
                shutil.copy2(src, stage_reviews / f"{ref}.md")

        draft_by_ref = {
            r["canonicalReference"]: r for r in load_jsonl(stage_chapter / "canonical-draft.jsonl")
        }
        new_draft_rows: list[dict[str, Any]] = []
        # Preserve original draft order.
        for row in load_jsonl(stage_chapter / "canonical-draft.jsonl"):
            ref = row["canonicalReference"]
            if ref in {c["canonicalReference"] for c in eligible}:
                cand = next(c for c in eligible if c["canonicalReference"] == ref)
                built = build_approved_draft_row(
                    candidate=cand,
                    existing=row,
                    reviewer_id=reviewer_id,
                    reviewer_name=reviewer_name,
                    decision_date=decision_date,
                )
                # Idempotent: if already approved with identical evidence, keep existing row.
                if (
                    row.get("approvalStatus") == "APPROVED"
                    and row.get("sanskritText") == built["sanskritText"]
                    and row.get("editorialDecisionId") == built["editorialDecisionId"]
                    and row.get("editorialApprovalChecksum") == built["editorialApprovalChecksum"]
                    and row.get("transliteration") is None
                ):
                    new_draft_rows.append(row)
                else:
                    new_draft_rows.append(built)
            else:
                new_draft_rows.append(row)

        result_rows: list[dict[str, Any]] = []
        for candidate in eligible:
            ref = candidate["canonicalReference"]
            decision_id = decision_id_for(ref, decision_date)
            review_path = stage_reviews / f"{ref}.md"
            existing_review = review_path.read_text(encoding="utf-8")
            already = first_status(existing_review) == "APPROVED"
            if already and draft_by_ref.get(ref, {}).get("approvalStatus") == "APPROVED":
                # Keep review bytes unchanged on idempotent re-apply.
                updated = existing_review
            else:
                updated = update_review_markdown(
                    existing_review,
                    ref=ref,
                    candidate=candidate,
                    reviewer_name=reviewer_name,
                    reviewer_id=reviewer_id,
                    decision_date=decision_date,
                    decision_id=decision_id,
                )
                review_path.write_text(updated, encoding="utf-8")
            draft_row = next(r for r in new_draft_rows if r["canonicalReference"] == ref)
            result_rows.append(
                build_approval_result_row(
                    candidate=candidate,
                    draft_row=draft_row,
                    review_path=review_path,
                    reviewer_id=reviewer_id,
                    decision_date=decision_date,
                )
            )

        (stage_chapter / "canonical-draft.jsonl").write_text(
            dump_jsonl(new_draft_rows), encoding="utf-8"
        )
        existing_manifest = load_json(stage_chapter / "chapter-01-approval-manifest.json")
        if int(existing_manifest.get("approved") or 0) > EXPECTED_CANDIDATES:
            # Later editorial stages (e.g. orthographic resolutions) already advanced counts.
            # Idempotent re-apply must not regress the Chapter rollup.
            manifest = existing_manifest
        else:
            manifest = build_manifest(
                existing_manifest,
                reviewer_id=reviewer_id,
                decision_date=decision_date,
            )
        (stage_chapter / "chapter-01-approval-manifest.json").write_text(
            dump_json(manifest), encoding="utf-8"
        )
        result_rows = sorted(
            result_rows, key=lambda r: tuple(map(int, r["canonicalReference"].split(".")))
        )
        (stage_chapter / "normalization-match-approval-result.jsonl").write_text(
            dump_jsonl(result_rows), encoding="utf-8"
        )

        # Validate staged outputs.
        _validate_staged_approval(
            stage_chapter=stage_chapter,
            stage_reviews=stage_reviews,
            eligible_refs=eligible_refs,
            conflict_refs=conflict_refs,
            conflict_analysis_bytes=conflict_analysis_bytes,
            comparison_bytes=comparison_bytes,
            candidate_bytes=candidate_bytes,
            conflict_review_bytes=conflict_review_bytes,
        )

        # Concurrent-edit guard on live workspace before replace.
        assert_unchanged(
            baseline,
            [
                chapter_dir / "canonical-draft.jsonl",
                chapter_dir / "chapter-01-approval-manifest.json",
                chapter_dir / "source-conflict-analysis.jsonl",
                chapter_dir / "source-comparison.jsonl",
                chapter_dir / "normalization-match-approval-candidate.jsonl",
                *[reviews_dir / f"{ref}.md" for ref in eligible_refs + conflict_refs],
            ],
        )

        # Atomic-ish replace: write temp siblings then os.replace.
        replacements = [
            (
                stage_chapter / "canonical-draft.jsonl",
                chapter_dir / "canonical-draft.jsonl",
            ),
            (
                stage_chapter / "chapter-01-approval-manifest.json",
                chapter_dir / "chapter-01-approval-manifest.json",
            ),
            (
                stage_chapter / "normalization-match-approval-result.jsonl",
                chapter_dir / "normalization-match-approval-result.jsonl",
            ),
        ]
        for ref in eligible_refs:
            replacements.append(
                (stage_reviews / f"{ref}.md", reviews_dir / f"{ref}.md")
            )

        tmp_written: list[Path] = []
        try:
            for src, dest in replacements:
                tmp_dest = dest.with_suffix(dest.suffix + ".antar-tmp")
                shutil.copy2(src, tmp_dest)
                tmp_written.append(tmp_dest)
            for src, dest in replacements:
                tmp_dest = dest.with_suffix(dest.suffix + ".antar-tmp")
                os.replace(tmp_dest, dest)
                tmp_written.remove(tmp_dest)
        finally:
            for path in tmp_written:
                path.unlink(missing_ok=True)

    report["mutations"] = len(eligible_refs) + 3  # reviews + draft + manifest + result
    report["ok"] = True
    report["approved"] = EXPECTED_CANDIDATES
    report["pending"] = EXPECTED_CONFLICTS
    report["manifestStatus"] = "PARTIALLY_APPROVED"
    return report


def _validate_staged_approval(
    *,
    stage_chapter: Path,
    stage_reviews: Path,
    eligible_refs: list[str],
    conflict_refs: list[str],
    conflict_analysis_bytes: bytes,
    comparison_bytes: bytes,
    candidate_bytes: bytes,
    conflict_review_bytes: dict[str, bytes],
) -> None:
    draft = load_jsonl(stage_chapter / "canonical-draft.jsonl")
    manifest = load_json(stage_chapter / "chapter-01-approval-manifest.json")
    results = load_jsonl(stage_chapter / "normalization-match-approval-result.jsonl")
    candidates = load_jsonl(stage_chapter / "normalization-match-approval-candidate.jsonl")
    conflicts = load_jsonl(stage_chapter / "source-conflict-analysis.jsonl")

    approved = [r for r in draft if r.get("approvalStatus") == "APPROVED"]
    eligible_set = set(eligible_refs)
    eligible_approved = [r for r in approved if r["canonicalReference"] in eligible_set]
    if len(eligible_approved) != EXPECTED_CANDIDATES:
        raise ApprovalError(
            f"staged eligible approved={len(eligible_approved)} expected 34"
        )
    if {r["canonicalReference"] for r in eligible_approved} != eligible_set:
        raise ApprovalError("staged approved refs mismatch eligible set")

    for row in eligible_approved:
        if row.get("transliteration") is not None:
            raise ApprovalError(f"{row['canonicalReference']}: transliteration must be null")
        if not row.get("sanskritText"):
            raise ApprovalError(f"{row['canonicalReference']}: missing Sanskrit")
        if row.get("classification") != "NORMALIZATION_MATCH":
            raise ApprovalError(f"{row['canonicalReference']}: bad classification")
        cand = next(c for c in candidates if c["canonicalReference"] == row["canonicalReference"])
        if row["sanskritText"] != cand["proposedSanskritText"]:
            raise ApprovalError(f"{row['canonicalReference']}: Sanskrit not traceable to candidate")
        if cand.get("classification") != "NORMALIZATION_MATCH":
            raise ApprovalError("approved Verse was not NORMALIZATION_MATCH")

    # Non-eligible conflict analysis history must remain pending in the analysis artifact.
    if any(c.get("approvalStatus") == "APPROVED" for c in conflicts):
        raise ApprovalError("SOURCE_CONFLICT analysis must not be APPROVED")
    if (stage_chapter / "source-conflict-analysis.jsonl").read_bytes() != conflict_analysis_bytes:
        raise ApprovalError("conflict analysis bytes changed")
    if (stage_chapter / "source-comparison.jsonl").read_bytes() != comparison_bytes:
        raise ApprovalError("source-comparison bytes changed")
    if (
        stage_chapter / "normalization-match-approval-candidate.jsonl"
    ).read_bytes() != candidate_bytes:
        raise ApprovalError("candidate prep artifact bytes changed")

    for ref, raw in conflict_review_bytes.items():
        # Only enforce immutability for conflict reviews that are still unapproved in draft.
        draft_row = next(r for r in draft if r["canonicalReference"] == ref)
        if draft_row.get("approvalStatus") == "APPROVED":
            continue
        if (stage_reviews / f"{ref}.md").read_bytes() != raw:
            raise ApprovalError(f"conflict review {ref} was modified")

    for ref in eligible_refs:
        path = stage_reviews / f"{ref}.md"
        errs = validate_review_text(
            path.read_text(encoding="utf-8"), expected_ref=ref, path_label=str(path)
        )
        if errs:
            raise ApprovalError(f"review validation failed for {ref}: {errs}")
        status = first_status(path.read_text(encoding="utf-8"))
        if status != "APPROVED":
            raise ApprovalError(f"{ref}: review status not APPROVED")

    # Manifest may already reflect later orthographic / final-conflict resolutions.
    status = manifest.get("status")
    if status not in {"PARTIALLY_APPROVED", "APPROVED"}:
        raise ApprovalError("manifest status must be PARTIALLY_APPROVED or APPROVED")
    if int(manifest.get("approved") or 0) < EXPECTED_CANDIDATES:
        raise ApprovalError("manifest approved must be >= 34")
    if manifest.get("rejected") != 0:
        raise ApprovalError("manifest rejected must be 0")
    if manifest.get("secondReviewer") is not None:
        raise ApprovalError("secondReviewer must be null")
    if status == "PARTIALLY_APPROVED" and manifest.get("importReady") is not False:
        raise ApprovalError("manifest importReady must be false")
    if status == "APPROVED" and (
        manifest.get("approved") != 47
        or manifest.get("pending") != 0
        or manifest.get("importReady") is not True
    ):
        raise ApprovalError("APPROVED manifest must be approved=47 pending=0 importReady=true")

    if len(results) != 34:
        raise ApprovalError("approval result must have 34 rows")
    for row in results:
        if row.get("approvalStatus") != "APPROVED":
            raise ApprovalError("approval result row not APPROVED")


def first_status(text: str) -> str:
    sections = split_sections(text)
    body = sections.get("Status", "")
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Batch-approve Chapter NORMALIZATION_MATCH candidates (controlled)."
    )
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--reviewer-name", required=True)
    parser.add_argument("--decision-date", required=True, help="UTC date YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--chapter-dir", type=Path, default=None)
    parser.add_argument("--reviews-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    if args.chapter != 1:
        print("ERROR: only --chapter 1 is supported", file=sys.stderr)
        return 2
    if args.dry_run == args.apply:
        print("ERROR: specify exactly one of --dry-run or --apply", file=sys.stderr)
        return 2

    chapter_dir = args.chapter_dir or CHAPTER_DIR
    reviews_dir = args.reviews_dir or REVIEWS_DIR
    try:
        report = apply_batch(
            chapter_dir=chapter_dir,
            reviews_dir=reviews_dir,
            reviewer_id=args.reviewer_id,
            reviewer_name=args.reviewer_name,
            decision_date=args.decision_date,
            dry_run=args.dry_run,
            apply=args.apply,
        )
    except ApprovalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
