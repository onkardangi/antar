#!/usr/bin/env python3
"""Resolve Chapter 1 orthographic-only SOURCE_CONFLICT Verses.

Approves only the 11 eligible references by selecting exact Wikisource text.
Never touches 1.20 / 1.22. Never synthesizes Sanskrit. Never builds packages.
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

from compare_sources import (  # noqa: E402
    apply_normalization,
    enabled_rules,
    fold_approved_orthography,
    load_json as load_norm_json,
    split_segments,
)
from validate_reviews import split_sections, validate_review_text  # noqa: E402

WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
POLICY_PATH = REPO_ROOT / "content/editorial/orthographic-resolution-policy.json"
NORM_POLICY_PATH = REPO_ROOT / "content/editorial/normalization-policy.json"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
REGISTRY_PATH = REPO_ROOT / "content/registry/sources.json"
DECISION_TYPE = "ORTHOGRAPHIC_SOURCE_CONFLICT_RESOLUTION"
PRIOR_DECISION_TYPE = "BATCH_NORMALIZATION_MATCH_APPROVAL"
EXPECTED_ELIGIBLE = 11
FORBIDDEN_REFS = frozenset({"1.20", "1.22"})
EXPECTED_FINAL_APPROVED = 45
EXPECTED_FINAL_PENDING = 2


class ResolutionError(Exception):
    """Orthographic resolution eligibility or atomic apply failure."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n"


def decision_id_for(ref: str, decision_date: str) -> str:
    return f"ortho-resolve-ch01-{ref}-{decision_date}"


def editorial_approval_checksum(
    *,
    ref: str,
    decision_id: str,
    sanskrit_text: str,
    selected_source_id: str,
    supporting_source_ids: list[str],
    reviewer_id: str,
    decision_date: str,
    rule_ids: list[str],
) -> str:
    material = json.dumps(
        {
            "canonicalReference": ref,
            "decisionDate": decision_date,
            "decisionId": decision_id,
            "decisionType": DECISION_TYPE,
            "reviewerId": reviewer_id,
            "ruleIds": rule_ids,
            "sanskritText": sanskrit_text,
            "selectedSourceId": selected_source_id,
            "supportingSourceIds": supporting_source_ids,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256_text(material)


def load_registry_map(path: Path = REGISTRY_PATH) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    sources = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(sources, list):
        raise ResolutionError(f"{path}: expected sources array")
    out: dict[str, dict[str, Any]] = {}
    for entry in sources:
        if isinstance(entry, dict) and "id" in entry:
            out[str(entry["id"])] = entry
    return out


def wiki_and_iitk(comparison: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = comparison.get("sources") or []
    wiki = next((s for s in sources if s.get("sourceId") == WIKISOURCE_ID), None)
    iitk = next((s for s in sources if "iitk" in str(s.get("sourceId", ""))), None)
    if wiki is None or iitk is None:
        raise ResolutionError(
            f"{comparison.get('canonicalReference')}: missing Wikisource or IIT evidence"
        )
    return wiki, iitk


def build_fold_pairs(policy: dict[str, Any]) -> list[tuple[str, str]]:
    """Build deterministic comparison-only fold pairs from policy observedForms."""
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for rule in policy.get("rules") or []:
        for form_a, form_b in rule.get("observedForms") or []:
            # Prefer folding explicit-cluster / avagraha / nukta forms toward Wikisource-like keys
            # by sorting longer/explicit forms first then mapping both to a stable key.
            key = tuple(sorted([form_a, form_b]))
            if key in seen:
                continue
            seen.add(key)
            # Stable comparison key: prefer anusvara / no-avagraha / long-vocalic forms
            # matching Wikisource orthography where present in the pair.
            preferred = form_a
            if "ऽ" in form_a and "ऽ" not in form_b:
                preferred = form_b
            elif "ऽ" in form_b and "ऽ" not in form_a:
                preferred = form_a
            elif "ङ्" in form_a and "ं" in form_b:
                preferred = form_b
            elif "ङ्" in form_b and "ं" in form_a:
                preferred = form_a
            elif "ञ्ज" in form_a and "ंज" in form_b:
                preferred = form_b
            elif "ञ्ज" in form_b and "ंज" in form_a:
                preferred = form_a
            elif "म्ब्" in form_a.replace("म्ब", "म्ब्") or "म्ब" in form_a:
                if "संब" in form_b:
                    preferred = form_b
            elif "म्ब" in form_b and "संब" in form_a:
                preferred = form_a
            elif "ृ़" in form_a and "ॄ" in form_b:
                preferred = form_b
            elif "ृ़" in form_b and "ॄ" in form_a:
                preferred = form_a
            pairs.append((form_a, preferred))
            pairs.append((form_b, preferred))
    # Longest-first replacement to avoid partial clobbering.
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def fold_orthography(text: str, fold_pairs: list[tuple[str, str]], norm_rules: dict[str, Any]) -> str:
    t = text
    for src, dst in fold_pairs:
        t = t.replace(src, dst)
    # Existing sanjaya fold for residual tokens.
    tokens = re.findall(r"[\u0900-\u097F]+|[^\u0900-\u097F]+", t)
    out: list[str] = []
    for tok in tokens:
        if re.fullmatch(r"[\u0900-\u097F]+", tok):
            out.append(fold_approved_orthography(tok, norm_rules))
        else:
            out.append(tok)
    return "".join(out)


def comparison_roots_match(
    wiki_text: str,
    iitk_text: str,
    *,
    fold_pairs: list[tuple[str, str]],
    norm_policy: dict[str, Any],
) -> tuple[bool, str, str]:
    rules = enabled_rules(norm_policy)
    seg_w = split_segments(wiki_text, rules)
    seg_i = split_segments(iitk_text, rules)
    root_w, _ = apply_normalization(seg_w["rootVerseBody"], rules)
    root_i, _ = apply_normalization(seg_i["rootVerseBody"], rules)
    sp_w = fold_orthography(seg_w.get("speakerLabel") or "", fold_pairs, rules)
    sp_i = fold_orthography(seg_i.get("speakerLabel") or "", fold_pairs, rules)
    rw = fold_orthography(root_w, fold_pairs, rules)
    ri = fold_orthography(root_i, fold_pairs, rules)
    return rw == ri and sp_w == sp_i, rw, ri


def rules_for_reference(policy: dict[str, Any], ref: str) -> list[dict[str, Any]]:
    return [r for r in (policy.get("rules") or []) if ref in (r.get("affectedReferences") or [])]


def first_status(text: str) -> str:
    body = split_sections(text).get("Status", "")
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def validate_eligibility(
    *,
    chapter_dir: Path,
    reviews_dir: Path,
    policy: dict[str, Any],
    reviewer_id: str,
    reviewer_name: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not reviewer_id.strip() or not reviewer_name.strip():
        raise ResolutionError("missing reviewer identity")
    if policy.get("requiresSecondReviewer"):
        raise ResolutionError("policy requires second reviewer; cannot invent one")
    if policy.get("autoApplyToFutureChapters"):
        raise ResolutionError("policy must not auto-apply to future chapters")

    eligible_refs = list(policy.get("eligibleReferences") or [])
    forbidden = set(policy.get("forbiddenReferences") or [])
    if set(eligible_refs) & forbidden:
        raise ResolutionError("eligible/forbidden overlap in policy")
    if set(eligible_refs) != {
        "1.2",
        "1.8",
        "1.15",
        "1.24",
        "1.26",
        "1.28",
        "1.34",
        "1.41",
        "1.42",
        "1.43",
        "1.47",
    }:
        raise ResolutionError("policy eligibleReferences must be exactly the 11 orthographic targets")
    if forbidden != FORBIDDEN_REFS:
        raise ResolutionError("policy forbiddenReferences must be exactly {1.20, 1.22}")

    conflict_path = chapter_dir / "source-conflict-analysis.jsonl"
    comparison_path = chapter_dir / "source-comparison.jsonl"
    draft_path = chapter_dir / "canonical-draft.jsonl"
    manifest_path = chapter_dir / "chapter-01-approval-manifest.json"
    for path in (conflict_path, comparison_path, draft_path, manifest_path):
        if not path.is_file():
            raise ResolutionError(f"missing {path}")

    conflicts = {c["canonicalReference"]: c for c in load_jsonl(conflict_path)}
    comparisons = {c["canonicalReference"]: c for c in load_jsonl(comparison_path)}
    draft_rows = load_jsonl(draft_path)
    draft_by_ref = {r["canonicalReference"]: r for r in draft_rows}
    registry = load_registry_map()
    norm_policy = load_norm_json(NORM_POLICY_PATH)
    fold_pairs = build_fold_pairs(policy)

    # Immutability of forbidden refs at eligibility time.
    for ref in sorted(FORBIDDEN_REFS):
        if ref not in conflicts:
            raise ResolutionError(f"forbidden ref {ref} missing from conflict analysis")
        if conflicts[ref].get("differenceKindFlags", {}).get("orthographicOnly") is True:
            # still forbidden due to substantive flags / third-ref requirement
            flags = conflicts[ref].get("differenceKindFlags") or {}
            if flags.get("wordDifference") or flags.get("segmentationDifference"):
                pass
            else:
                raise ResolutionError(
                    f"{ref}: marked orthographicOnly unexpectedly; refusing silent inclusion"
                )
        draft = draft_by_ref.get(ref)
        if draft is None:
            raise ResolutionError(f"{ref}: missing draft row")
        if draft.get("approvalStatus") == "APPROVED":
            raise ResolutionError(f"{ref}: must remain unapproved")
        if draft.get("sanskritText") is not None:
            raise ResolutionError(f"{ref}: Sanskrit must remain null")

    prior_approved = [
        r
        for r in draft_rows
        if r.get("approvalStatus") == "APPROVED"
        and r.get("decisionType") == PRIOR_DECISION_TYPE
    ]
    if len(prior_approved) != 34:
        raise ResolutionError(
            f"expected 34 prior NORMALIZATION_MATCH approvals, found {len(prior_approved)}"
        )

    eligible: list[dict[str, Any]] = []
    for ref in eligible_refs:
        errors: list[str] = []
        if ref in FORBIDDEN_REFS:
            errors.append("forbidden reference")
        conflict = conflicts.get(ref)
        if conflict is None:
            errors.append("missing conflict analysis")
            raise ResolutionError(f"{ref}: " + "; ".join(errors))
        if conflict.get("classification") != "SOURCE_CONFLICT":
            errors.append("classification is not SOURCE_CONFLICT")
        flags = conflict.get("differenceKindFlags") or {}
        if flags.get("orthographicOnly") is not True:
            errors.append("not orthographic-only")
        for bad in ("wordDifference", "wordOrderDifference", "extraText", "missingText", "segmentationDifference"):
            if flags.get(bad):
                errors.append(f"substantive flag {bad}=true")
        if conflict.get("recommendation") == "REQUIRES_EDITORIAL_SOURCE":
            errors.append("requires editorial/third source")

        comparison = comparisons.get(ref)
        if comparison is None:
            errors.append("missing source-comparison")
            raise ResolutionError(f"{ref}: " + "; ".join(errors))
        wiki, iitk = wiki_and_iitk(comparison)
        wiki_text = wiki.get("sanskritText")
        iitk_text = iitk.get("sanskritText")
        if not isinstance(wiki_text, str) or not wiki_text.strip():
            errors.append("Wikisource Sanskrit missing")
        if not isinstance(iitk_text, str) or not iitk_text.strip():
            errors.append("IIT Sanskrit missing")

        selected_entry = registry.get(WIKISOURCE_ID)
        if not selected_entry or selected_entry.get("source_role") != "PRIMARY_TRANSCRIPTION_CANDIDATE":
            errors.append("selected source not PRIMARY_TRANSCRIPTION_CANDIDATE")
        iitk_entry = registry.get(str(iitk.get("sourceId")))
        if not iitk_entry or iitk_entry.get("source_role") != "SECONDARY_VERIFICATION_REFERENCE":
            errors.append("IIT must remain SECONDARY_VERIFICATION_REFERENCE")
        if iitk_entry and iitk_entry.get("status") != "VERIFICATION_ONLY":
            errors.append("IIT must remain VERIFICATION_ONLY")

        match, _, _ = comparison_roots_match(
            wiki_text or "",
            iitk_text or "",
            fold_pairs=fold_pairs,
            norm_policy=norm_policy,
        )
        if not match:
            errors.append("roots/speakers still differ after scoped orthographic folds (ambiguous)")

        rule_rows = rules_for_reference(policy, ref)
        if not rule_rows:
            errors.append("no scoped orthographic rule covers this reference")
        for rule in rule_rows:
            if rule.get("changesLexicalIdentity") is True:
                errors.append(f"rule {rule.get('id')} claims lexical change")
            if not rule.get("comparisonOnly"):
                errors.append(f"rule {rule.get('id')} is not comparison-only")
            if rule.get("selectedCanonicalSource") != WIKISOURCE_ID:
                errors.append(f"rule {rule.get('id')} must select Wikisource")

        draft = draft_by_ref.get(ref)
        if draft is None:
            errors.append("missing draft row")
        already = draft is not None and draft.get("approvalStatus") == "APPROVED"
        if already:
            if draft.get("sanskritText") != wiki_text:
                errors.append("already-approved Sanskrit conflicts with Wikisource")
            if draft.get("transliteration") is not None:
                errors.append("transliteration must be null")
            if draft.get("decisionType") not in {None, DECISION_TYPE}:
                errors.append("already-approved with conflicting decisionType")
        else:
            if draft and draft.get("approvalStatus") == "APPROVED":
                errors.append("unexpected APPROVED state")
            if draft and draft.get("sanskritText") is not None:
                errors.append("unresolved conflict draft must have null Sanskrit before apply")

        review_path = reviews_dir / f"{ref}.md"
        if not review_path.is_file():
            errors.append("missing review file")
        else:
            review_errors = validate_review_text(
                review_path.read_text(encoding="utf-8"),
                expected_ref=ref,
                path_label=str(review_path),
            )
            if already:
                if review_errors:
                    errors.extend(review_errors)
            else:
                structural = [
                    e
                    for e in review_errors
                    if "Approval fields must be blank" not in e
                    and "APPROVED requires" not in e
                ]
                if structural:
                    errors.extend(structural)

        if errors:
            raise ResolutionError(f"{ref}: " + "; ".join(errors))

        eligible.append(
            {
                "canonicalReference": ref,
                "chapterNumber": 1,
                "verseNumber": int(ref.split(".")[1]),
                "wikisourceText": wiki_text,
                "iitkText": iitk_text,
                "wikisourceSourceId": WIKISOURCE_ID,
                "iitkSourceId": iitk.get("sourceId"),
                "wikisourceChecksum": wiki.get("sourceChecksum"),
                "iitkSourceChecksum": iitk.get("sourceChecksum"),
                "iitkEvidenceChecksum": iitk.get("evidenceChecksum"),
                "ruleIds": [r["id"] for r in rule_rows],
                "differenceClasses": sorted(
                    {r.get("differenceClass") for r in rule_rows if r.get("differenceClass")}
                ),
                "patternIds": list(conflict.get("patternIds") or []),
                "alreadyApproved": already,
            }
        )

    if len(eligible) != EXPECTED_ELIGIBLE:
        raise ResolutionError(
            f"eligible count {len(eligible)} != {EXPECTED_ELIGIBLE}; refusing partial batch"
        )

    context = {
        "conflicts": conflicts,
        "comparisons": comparisons,
        "draft_rows": draft_rows,
        "draft_by_ref": draft_by_ref,
        "manifest": load_json(manifest_path),
        "prior_approved_refs": [r["canonicalReference"] for r in prior_approved],
        "conflict_analysis_bytes": conflict_path.read_bytes(),
        "comparison_bytes": comparison_path.read_bytes(),
        "forbidden_review_bytes": {
            ref: (reviews_dir / f"{ref}.md").read_bytes()
            for ref in sorted(FORBIDDEN_REFS)
            if (reviews_dir / f"{ref}.md").is_file()
        },
        "forbidden_draft_bytes": {
            ref: json.dumps(draft_by_ref[ref], ensure_ascii=False, sort_keys=True)
            for ref in sorted(FORBIDDEN_REFS)
        },
    }
    return eligible, context


def build_approved_draft_row(
    *,
    item: dict[str, Any],
    existing: dict[str, Any],
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
) -> dict[str, Any]:
    ref = item["canonicalReference"]
    sanskrit = item["wikisourceText"]
    supporting = [item["iitkSourceId"]]
    rule_ids = list(item["ruleIds"])
    decision_id = decision_id_for(ref, decision_date)
    approval_cs = editorial_approval_checksum(
        ref=ref,
        decision_id=decision_id,
        sanskrit_text=sanskrit,
        selected_source_id=WIKISOURCE_ID,
        supporting_source_ids=supporting,
        reviewer_id=reviewer_id,
        decision_date=decision_date,
        rule_ids=rule_ids,
    )
    notes = [
        f"decisionType={DECISION_TYPE}",
        "originalClassification=SOURCE_CONFLICT",
        "resolution=orthographic-only; lexical identity unchanged",
        f"ruleIds={','.join(rule_ids)}",
        f"differenceClasses={','.join(item.get('differenceClasses') or [])}",
        "Selected exact Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE text; no synthesis.",
        "IIT remains verification-only and is not the imported source.",
        "SOURCE_CONFLICT history preserved in source-conflict-analysis.jsonl and review Differences.",
    ]
    row = dict(existing)
    row.update(
        {
            "chapterNumber": 1,
            "verseNumber": item["verseNumber"],
            "canonicalReference": ref,
            "sanskritText": sanskrit,
            "transliteration": None,
            "approvalStatus": "APPROVED",
            "approvedSourceIds": [WIKISOURCE_ID] + supporting,
            "editorialNotes": notes,
            "contentVersion": int(existing.get("contentVersion") or 1),
            "editorialDecisionId": decision_id,
            "editorialApprovalChecksum": approval_cs,
            "reviewerId": reviewer_id,
            "reviewer": reviewer_name,
            "secondReviewerId": None,
            "approvalDate": decision_date,
            "decisionType": DECISION_TYPE,
            "selectedSourceId": WIKISOURCE_ID,
            "supportingSourceIds": supporting,
            "sourceChecksums": {
                WIKISOURCE_ID: item["wikisourceChecksum"],
                item["iitkSourceId"]: item["iitkSourceChecksum"],
            },
            "classification": "ORTHOGRAPHIC_EQUIVALENCE",
            "priorClassification": "SOURCE_CONFLICT",
            "resolutionClassification": "ORTHOGRAPHIC_EQUIVALENCE",
            "orthographicRuleIds": rule_ids,
            "selectedSourceChecksum": item["wikisourceChecksum"],
            "supportingSourceChecksums": {
                item["iitkSourceId"]: {
                    "sourceChecksum": item["iitkSourceChecksum"],
                    "evidenceChecksum": item["iitkEvidenceChecksum"],
                }
            },
        }
    )
    return row


def update_review_markdown(
    text: str,
    *,
    item: dict[str, Any],
    reviewer_name: str,
    reviewer_id: str,
    decision_date: str,
    decision_id: str,
) -> str:
    ref = item["canonicalReference"]
    sections = split_sections(text)
    decision_lines = [
        "Resolved as orthographic-only SOURCE_CONFLICT.",
        "",
        f"Selected Wikisource (`{WIKISOURCE_ID}`) as canonical Sanskrit transcription "
        "(exact selected-source copy; no synthesis / hybrid).",
        "",
        f"IIT (`{item['iitkSourceId']}`) remains secondary verification only.",
        "",
        "Documented orthographic difference classes: "
        + ", ".join(item.get("differenceClasses") or [])
        + ".",
        "",
        "Rule IDs applied (comparison-only): " + ", ".join(f"`{r}`" for r in item["ruleIds"]) + ".",
        "",
        "Lexical identity, segmentation, and word order are unchanged after scoped folds.",
        "",
        f"Decision type: `{DECISION_TYPE}`.",
        f"Editorial decision ID: `{decision_id}`.",
        "",
        "SOURCE_CONFLICT history and source differences are preserved above; this decision "
        "selects one exact source form rather than inventing a third form.",
    ]
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
        f"- {decision_date} — Orthographic resolution `{DECISION_TYPE}` by `{reviewer_id}` "
        f"({reviewer_name}). Selected Wikisource exact text; IIT verification-only. "
        f"Rules: {', '.join(item['ruleIds'])}. Decision `{decision_id}`. "
        f"Status set to `APPROVED`. SOURCE_CONFLICT history retained.\n"
    )
    sections["Audit Log"] = audit.rstrip("\n")

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
    for name in sections:
        if name not in order:
            order.append(name)
    parts = [f"# {name}\n\n{sections[name].strip()}\n" for name in order if name in sections]
    updated = "\n".join(parts)
    if not updated.endswith("\n"):
        updated += "\n"
    errs = validate_review_text(updated, expected_ref=ref, path_label=f"{ref}.md")
    if errs:
        raise ResolutionError(f"{ref}: invalid updated review: {errs}")
    return updated


def build_result_row(
    *,
    item: dict[str, Any],
    draft_row: dict[str, Any],
    review_path: Path,
    reviewer_id: str,
    decision_date: str,
) -> dict[str, Any]:
    return {
        "approvalStatus": "APPROVED",
        "canonicalReference": item["canonicalReference"],
        "canonicalTextChecksum": sha256_text(item["wikisourceText"]),
        "decisionDate": decision_date,
        "editorialDecisionId": draft_row["editorialDecisionId"],
        "originalIitkForm": item["iitkText"],
        "originalWikisourceForm": item["wikisourceText"],
        "reviewFileChecksum": sha256_file(review_path),
        "reviewerId": reviewer_id,
        "ruleIdsApplied": list(item["ruleIds"]),
        "selectedSourceId": WIKISOURCE_ID,
    }


def build_manifest(existing: dict[str, Any], *, reviewer_id: str, decision_date: str) -> dict[str, Any]:
    manifest = dict(existing)
    notes = [
        "PARTIALLY_APPROVED: 45 Verses approved (34 NORMALIZATION_MATCH + 11 orthographic resolutions).",
        "Unresolved SOURCE_CONFLICT Verses: 1.20, 1.22 (require third witness / separate editorial process).",
        "Chapter is not import-ready. No package or database import authorized.",
        "Selected canonical source for resolutions: Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE.",
        "IIT remains SECONDARY_VERIFICATION_REFERENCE / verification-only.",
        "Orthographic rules are Chapter 1 scoped and comparison-only.",
    ]
    manifest.update(
        {
            "approved": EXPECTED_FINAL_APPROVED,
            "pending": EXPECTED_FINAL_PENDING,
            "rejected": 0,
            "reviewer": reviewer_id,
            "secondReviewer": None,
            "decisionDate": decision_date,
            "status": "PARTIALLY_APPROVED",
            "importReady": False,
            "normalizationMatchCandidates": 34,
            "orthographicResolutions": 11,
            "sourceConflicts": 13,
            "unresolvedSourceConflicts": 2,
            "unresolvedReferences": ["1.20", "1.22"],
            "decisionType": DECISION_TYPE,
            "notes": notes,
        }
    )
    return manifest


def snapshot_paths(chapter_dir: Path, reviews_dir: Path, refs: list[str]) -> dict[str, str]:
    paths = [
        chapter_dir / "canonical-draft.jsonl",
        chapter_dir / "chapter-01-approval-manifest.json",
        chapter_dir / "source-conflict-analysis.jsonl",
        chapter_dir / "source-comparison.jsonl",
        chapter_dir / "normalization-match-approval-result.jsonl",
    ]
    for ref in refs:
        paths.append(reviews_dir / f"{ref}.md")
    out: dict[str, str] = {}
    for path in paths:
        out[str(path.resolve())] = sha256_file(path) if path.is_file() else ""
    result_path = chapter_dir / "orthographic-resolution-result.jsonl"
    out[str(result_path.resolve())] = sha256_file(result_path) if result_path.is_file() else ""
    return out


def assert_unchanged(baseline: dict[str, str], paths: list[Path]) -> None:
    for path in paths:
        key = str(path.resolve())
        if key not in baseline:
            continue
        current = sha256_file(path) if path.is_file() else ""
        if current != baseline[key]:
            raise ResolutionError(
                f"refusing to overwrite unrelated human change detected in {path}"
            )


def _validate_staged(
    *,
    stage_chapter: Path,
    stage_reviews: Path,
    eligible: list[dict[str, Any]],
    context: dict[str, Any],
    prior_draft_by_ref: dict[str, dict[str, Any]],
) -> None:
    draft = load_jsonl(stage_chapter / "canonical-draft.jsonl")
    manifest = load_json(stage_chapter / "chapter-01-approval-manifest.json")
    results = load_jsonl(stage_chapter / "orthographic-resolution-result.jsonl")
    eligible_refs = {i["canonicalReference"] for i in eligible}
    approved = [r for r in draft if r.get("approvalStatus") == "APPROVED"]
    unapproved = [r for r in draft if r.get("approvalStatus") != "APPROVED"]

    if len(approved) != EXPECTED_FINAL_APPROVED:
        raise ResolutionError(f"staged approved={len(approved)} expected 45")
    if len(unapproved) != EXPECTED_FINAL_PENDING:
        raise ResolutionError(f"staged unapproved={len(unapproved)} expected 2")
    if {r["canonicalReference"] for r in unapproved} != FORBIDDEN_REFS:
        raise ResolutionError("unapproved refs must be exactly 1.20 and 1.22")

    # Prior 34 unchanged.
    for ref in context["prior_approved_refs"]:
        before = prior_draft_by_ref[ref]
        after = next(r for r in draft if r["canonicalReference"] == ref)
        if after != before:
            raise ResolutionError(f"prior approval {ref} changed")

    for ref in sorted(FORBIDDEN_REFS):
        row = next(r for r in draft if r["canonicalReference"] == ref)
        if row.get("approvalStatus") == "APPROVED" or row.get("sanskritText") is not None:
            raise ResolutionError(f"{ref}: forbidden Verse was mutated")
        if (stage_reviews / f"{ref}.md").read_bytes() != context["forbidden_review_bytes"][ref]:
            raise ResolutionError(f"{ref}: forbidden review mutated")

    if (stage_chapter / "source-conflict-analysis.jsonl").read_bytes() != context[
        "conflict_analysis_bytes"
    ]:
        raise ResolutionError("conflict analysis history must remain byte-identical")
    if (stage_chapter / "source-comparison.jsonl").read_bytes() != context["comparison_bytes"]:
        raise ResolutionError("source-comparison evidence must remain byte-identical")

    for item in eligible:
        ref = item["canonicalReference"]
        row = next(r for r in draft if r["canonicalReference"] == ref)
        if row["sanskritText"] != item["wikisourceText"]:
            raise ResolutionError(f"{ref}: Sanskrit not exact Wikisource copy")
        if row.get("transliteration") is not None:
            raise ResolutionError(f"{ref}: transliteration must be null")
        if row.get("decisionType") != DECISION_TYPE:
            raise ResolutionError(f"{ref}: bad decisionType")
        review_path = stage_reviews / f"{ref}.md"
        errs = validate_review_text(
            review_path.read_text(encoding="utf-8"),
            expected_ref=ref,
            path_label=str(review_path),
        )
        if errs:
            raise ResolutionError(f"{ref}: review invalid: {errs}")
        if first_status(review_path.read_text(encoding="utf-8")) != "APPROVED":
            raise ResolutionError(f"{ref}: review not APPROVED")

    if len(results) != EXPECTED_ELIGIBLE:
        raise ResolutionError("orthographic-resolution-result must have 11 rows")
    if manifest.get("approved") != 45 or manifest.get("pending") != 2:
        raise ResolutionError("manifest counts incorrect")
    if manifest.get("importReady") is not False:
        raise ResolutionError("importReady must be false")
    if manifest.get("unresolvedReferences") != ["1.20", "1.22"]:
        raise ResolutionError("manifest unresolvedReferences incorrect")


def apply_resolution(
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
        raise ResolutionError("specify exactly one of --dry-run or --apply")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", decision_date):
        raise ResolutionError("decision-date must be YYYY-MM-DD")

    policy = load_json(POLICY_PATH)
    eligible, context = validate_eligibility(
        chapter_dir=chapter_dir,
        reviews_dir=reviews_dir,
        policy=policy,
        reviewer_id=reviewer_id,
        reviewer_name=reviewer_name,
    )
    eligible_refs = [i["canonicalReference"] for i in eligible]
    report = {
        "mode": "dry-run" if dry_run else "apply",
        "ok": True,
        "eligibleCount": len(eligible_refs),
        "eligibleReferences": eligible_refs,
        "forbiddenUntouched": sorted(FORBIDDEN_REFS),
        "unresolvedConflictReferences": sorted(FORBIDDEN_REFS),
        "reviewerId": reviewer_id,
        "reviewerName": reviewer_name,
        "decisionDate": decision_date,
        "decisionType": DECISION_TYPE,
        "chapterImportReady": False,
        "mutations": 0 if dry_run else None,
    }
    if dry_run:
        return report

    baseline = snapshot_paths(
        chapter_dir,
        reviews_dir,
        eligible_refs + sorted(FORBIDDEN_REFS) + context["prior_approved_refs"],
    )
    prior_draft_by_ref = {
        r["canonicalReference"]: r
        for r in context["draft_rows"]
        if r["canonicalReference"] in context["prior_approved_refs"]
    }

    with tempfile.TemporaryDirectory(prefix="antar-ortho-resolve-") as tmp:
        staging = Path(tmp)
        stage_chapter = staging / "chapter-01"
        stage_reviews = staging / "reviews"
        stage_chapter.mkdir()
        stage_reviews.mkdir()
        for name in (
            "canonical-draft.jsonl",
            "chapter-01-approval-manifest.json",
            "source-conflict-analysis.jsonl",
            "source-comparison.jsonl",
            "normalization-match-approval-result.jsonl",
            "automated-comparison-report.jsonl",
        ):
            src = chapter_dir / name
            if src.is_file():
                shutil.copy2(src, stage_chapter / name)
        for ref in eligible_refs + sorted(FORBIDDEN_REFS) + context["prior_approved_refs"]:
            src = reviews_dir / f"{ref}.md"
            if src.is_file():
                shutil.copy2(src, stage_reviews / f"{ref}.md")

        new_draft_rows: list[dict[str, Any]] = []
        eligible_by_ref = {i["canonicalReference"]: i for i in eligible}
        for row in load_jsonl(stage_chapter / "canonical-draft.jsonl"):
            ref = row["canonicalReference"]
            if ref in eligible_by_ref:
                item = eligible_by_ref[ref]
                built = build_approved_draft_row(
                    item=item,
                    existing=row,
                    reviewer_id=reviewer_id,
                    reviewer_name=reviewer_name,
                    decision_date=decision_date,
                )
                if (
                    row.get("approvalStatus") == "APPROVED"
                    and row.get("sanskritText") == built["sanskritText"]
                    and row.get("editorialDecisionId") == built["editorialDecisionId"]
                    and row.get("editorialApprovalChecksum") == built["editorialApprovalChecksum"]
                ):
                    new_draft_rows.append(row)
                else:
                    new_draft_rows.append(built)
            else:
                new_draft_rows.append(row)

        result_rows: list[dict[str, Any]] = []
        for item in eligible:
            ref = item["canonicalReference"]
            decision_id = decision_id_for(ref, decision_date)
            review_path = stage_reviews / f"{ref}.md"
            existing_review = review_path.read_text(encoding="utf-8")
            if first_status(existing_review) == "APPROVED" and item["alreadyApproved"]:
                updated = existing_review
            else:
                updated = update_review_markdown(
                    existing_review,
                    item=item,
                    reviewer_name=reviewer_name,
                    reviewer_id=reviewer_id,
                    decision_date=decision_date,
                    decision_id=decision_id,
                )
                review_path.write_text(updated, encoding="utf-8")
            draft_row = next(r for r in new_draft_rows if r["canonicalReference"] == ref)
            result_rows.append(
                build_result_row(
                    item=item,
                    draft_row=draft_row,
                    review_path=review_path,
                    reviewer_id=reviewer_id,
                    decision_date=decision_date,
                )
            )

        (stage_chapter / "canonical-draft.jsonl").write_text(
            dump_jsonl(new_draft_rows), encoding="utf-8"
        )
        manifest = build_manifest(
            load_json(stage_chapter / "chapter-01-approval-manifest.json"),
            reviewer_id=reviewer_id,
            decision_date=decision_date,
        )
        (stage_chapter / "chapter-01-approval-manifest.json").write_text(
            dump_json(manifest), encoding="utf-8"
        )
        result_rows = sorted(
            result_rows, key=lambda r: tuple(map(int, r["canonicalReference"].split(".")))
        )
        (stage_chapter / "orthographic-resolution-result.jsonl").write_text(
            dump_jsonl(result_rows), encoding="utf-8"
        )

        _validate_staged(
            stage_chapter=stage_chapter,
            stage_reviews=stage_reviews,
            eligible=eligible,
            context=context,
            prior_draft_by_ref=prior_draft_by_ref,
        )

        assert_unchanged(
            baseline,
            [
                chapter_dir / "canonical-draft.jsonl",
                chapter_dir / "chapter-01-approval-manifest.json",
                chapter_dir / "source-conflict-analysis.jsonl",
                chapter_dir / "source-comparison.jsonl",
                chapter_dir / "normalization-match-approval-result.jsonl",
                *[reviews_dir / f"{ref}.md" for ref in eligible_refs + sorted(FORBIDDEN_REFS)],
            ],
        )

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
                stage_chapter / "orthographic-resolution-result.jsonl",
                chapter_dir / "orthographic-resolution-result.jsonl",
            ),
        ]
        for ref in eligible_refs:
            replacements.append((stage_reviews / f"{ref}.md", reviews_dir / f"{ref}.md"))

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

    report["mutations"] = len(eligible_refs) + 3
    report["approved"] = EXPECTED_FINAL_APPROVED
    report["pending"] = EXPECTED_FINAL_PENDING
    report["manifestStatus"] = "PARTIALLY_APPROVED"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Resolve Chapter 1 orthographic-only SOURCE_CONFLICT Verses."
    )
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--reviewer-name", required=True)
    parser.add_argument("--decision-date", required=True)
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

    try:
        report = apply_resolution(
            chapter_dir=args.chapter_dir or CHAPTER_DIR,
            reviews_dir=args.reviews_dir or REVIEWS_DIR,
            reviewer_id=args.reviewer_id,
            reviewer_name=args.reviewer_name,
            decision_date=args.decision_date,
            dry_run=args.dry_run,
            apply=args.apply,
        )
    except ResolutionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
