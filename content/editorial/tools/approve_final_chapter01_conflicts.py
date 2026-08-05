#!/usr/bin/env python3
"""Apply human approval for Chapter 1 final conflicts 1.20 and 1.22 only.

Requires three registered sources, exact proposed-source Sanskrit, and reviewer
metadata. All-or-nothing. Never synthesizes Sanskrit. Never builds packages.
Never touches any other Verse.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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

from validate_reviews import split_sections, validate_review_text  # noqa: E402

WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
REVIEWS_DIR = REPO_ROOT / "content/editorial/reviews"
REGISTRY_PATH = REPO_ROOT / "content/registry/sources.json"
CANDIDATES_NAME = "final-conflict-resolution-candidates.jsonl"
RESULT_NAME = "final-conflict-resolution-result.jsonl"
DECISION_TYPE = "FINAL_CHAPTER01_CONFLICT_RESOLUTION"
ALLOWED_REFS = ("1.20", "1.22")
EXPECTED_PRIOR_APPROVED = 45
EXPECTED_FINAL_APPROVED = 47


class ApprovalError(Exception):
    """Final conflict approval eligibility or atomic apply failure."""


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
    return f"final-conflict-ch01-{ref}-{decision_date}"


def editorial_approval_checksum(
    *,
    ref: str,
    decision_id: str,
    sanskrit_text: str,
    selected_source_id: str,
    supporting_source_ids: list[str],
    reviewer_id: str,
    decision_date: str,
) -> str:
    material = json.dumps(
        {
            "canonicalReference": ref,
            "decisionDate": decision_date,
            "decisionId": decision_id,
            "decisionType": DECISION_TYPE,
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


def registry_by_id(repo_root: Path) -> dict[str, dict[str, Any]]:
    data = load_json(repo_root / "content/registry/sources.json")
    return {s["id"]: s for s in data.get("sources", [])}


def source_text_from_comparison(comp: dict[str, Any], source_id: str) -> str | None:
    for s in comp.get("sources") or []:
        if s.get("sourceId") == source_id:
            return s.get("sanskritText")
    return None


def classify_roles(source_ids: list[str], registry: dict[str, dict[str, Any]]) -> dict[str, str]:
    roles: dict[str, str] = {}
    for sid in source_ids:
        entry = registry.get(sid)
        if entry is None:
            raise ApprovalError(f"source not registered: {sid}")
        role = str(entry.get("source_role") or entry.get("sourceRole") or "")
        roles[sid] = role
    return roles


def validate_candidate(
    candidate: dict[str, Any],
    *,
    registry: dict[str, dict[str, Any]],
    comparison: dict[str, Any] | None,
    draft: dict[str, Any] | None,
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    errors: list[str] = []
    ref = candidate.get("canonicalReference")
    if ref not in ALLOWED_REFS:
        errors.append(f"reference {ref!r} not in allowed final-conflict set")
        return errors

    if candidate.get("approvalStatus") not in {"PENDING", "APPROVED"}:
        errors.append(f"{ref}: approvalStatus must be PENDING before apply")
    if candidate.get("requiresHumanApproval") is not True:
        errors.append(f"{ref}: requiresHumanApproval must be true")

    source_ids = list(candidate.get("sourceIds") or [])
    if len(source_ids) != 3:
        errors.append(f"{ref}: exactly three sourceIds required, found {len(source_ids)}")
    if len(set(source_ids)) != 3:
        errors.append(f"{ref}: sourceIds must be unique")

    try:
        roles = classify_roles(source_ids, registry)
    except ApprovalError as exc:
        errors.append(str(exc))
        return errors

    role_values = list(roles.values())
    if role_values.count("PRIMARY_TRANSCRIPTION_CANDIDATE") != 1:
        errors.append(f"{ref}: exactly one PRIMARY_TRANSCRIPTION_CANDIDATE required")
    if role_values.count("SECONDARY_VERIFICATION_REFERENCE") != 1:
        errors.append(f"{ref}: exactly one SECONDARY_VERIFICATION_REFERENCE required")
    if role_values.count("THIRD_EDITORIAL_VERIFICATION_REFERENCE") != 1:
        errors.append(f"{ref}: exactly one THIRD_EDITORIAL_VERIFICATION_REFERENCE required")

    proposed_id = candidate.get("proposedSourceId")
    proposed_text = candidate.get("proposedSanskritText")
    if not proposed_id:
        errors.append(f"{ref}: missing proposedSourceId")
    if not isinstance(proposed_text, str) or not proposed_text:
        errors.append(f"{ref}: missing proposedSanskritText")
    if proposed_id not in source_ids:
        errors.append(f"{ref}: proposedSourceId must be one of sourceIds")

    if proposed_id:
        entry = registry.get(str(proposed_id))
        if entry is None:
            errors.append(f"{ref}: proposed source not registered")
        else:
            role = entry.get("source_role") or entry.get("sourceRole")
            if role != "PRIMARY_TRANSCRIPTION_CANDIDATE":
                errors.append(
                    f"{ref}: proposed source must be PRIMARY_TRANSCRIPTION_CANDIDATE "
                    f"(got {role!r}); verification-only sources cannot be canonical"
                )

    if comparison is None:
        errors.append(f"{ref}: missing source-comparison record")
    else:
        comp_ids = [s.get("sourceId") for s in comparison.get("sources") or []]
        for sid in source_ids:
            if sid not in comp_ids:
                errors.append(f"{ref}: source {sid} missing from source-comparison")
            else:
                entry = registry.get(sid)
                if entry and entry.get("sha256"):
                    # observed comparison text checksum optional; require text present
                    text = source_text_from_comparison(comparison, sid)
                    if not text:
                        errors.append(f"{ref}: empty comparison text for {sid}")
        if proposed_id and proposed_text is not None:
            exact = source_text_from_comparison(comparison, str(proposed_id))
            if exact is None:
                errors.append(f"{ref}: proposed source text missing in comparison")
            elif exact != proposed_text:
                errors.append(
                    f"{ref}: proposedSanskritText is not byte-identical to proposed source form"
                )

    # Substantive ambiguity gate: mixed majority-against-primary on WORD_DIFFERENCE
    # with unresolved segmentation is refused unless human override note present.
    cats = set(candidate.get("differenceCategories") or [])
    pattern = candidate.get("agreementPattern")
    seg_resolved = candidate.get("segmentationResolved")
    notes = " ".join(candidate.get("notes") or [])
    if pattern == "MIXED_2_OF_3" and "WORD_DIFFERENCE" in cats and seg_resolved is not True:
        if "humanAcceptsMinorityPrimaryReading=true" not in notes:
            errors.append(
                f"{ref}: unresolved substantive ambiguity "
                "(MIXED_2_OF_3 WORD_DIFFERENCE with segmentationResolved!=true); "
                "refuse batch unless candidate notes include "
                "humanAcceptsMinorityPrimaryReading=true"
            )

    if draft is None:
        errors.append(f"{ref}: missing canonical-draft row")
    elif draft.get("approvalStatus") == "APPROVED":
        errors.append(f"{ref}: draft already APPROVED (refusing re-approval in this tool)")
    elif draft.get("sanskritText") not in (None, ""):
        errors.append(f"{ref}: draft Sanskrit must be null before final-conflict apply")

    return errors


def build_decision_block(candidate: dict[str, Any], decision_id: str) -> str:
    return (
        f"Resolved via three-source final Chapter 1 conflict process.\n\n"
        f"Selected Wikisource (`{candidate['proposedSourceId']}`) as canonical Sanskrit "
        f"transcription (exact selected-source copy; no synthesis / hybrid).\n\n"
        f"Agreement pattern: `{candidate.get('agreementPattern')}`.\n"
        f"Segmentation resolved flag: `{candidate.get('segmentationResolved')}`.\n\n"
        f"IIT and Sanskrit Documents remain verification-only and are not import corpora.\n\n"
        f"Decision type: `{DECISION_TYPE}`.\n"
        f"Editorial decision ID: `{decision_id}`.\n"
    )


def update_review(
    text: str,
    *,
    candidate: dict[str, Any],
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
    decision_id: str,
) -> str:
    sections = split_sections(text)
    sections["Status"] = "APPROVED\n"
    sections["Decision"] = build_decision_block(candidate, decision_id) + "\n"
    approval = (
        f"Reviewer: {reviewer_name}\n"
        f"Reviewer ID: {reviewer_id}\n"
        f"Second Reviewer:\n"
        f"Date: {decision_date}\n"
    )
    sections["Approval"] = approval
    audit = sections.get("Audit Log", "").rstrip() + "\n"
    audit += (
        f"- {decision_date} — Final conflict resolution `{DECISION_TYPE}` by "
        f"`{reviewer_id}` ({reviewer_name}). Selected Wikisource exact text; "
        f"IIT + Sanskrit Documents verification-only. Decision `{decision_id}`. "
        f"Status set to `APPROVED`. Three-source comparison retained.\n"
    )
    sections["Audit Log"] = audit

    # Rebuild in original order
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
    parts: list[str] = []
    seen = set()
    for key in order:
        if key in sections:
            parts.append(f"# {key}\n\n{sections[key].rstrip()}\n")
            seen.add(key)
    for key, val in sections.items():
        if key not in seen:
            parts.append(f"# {key}\n\n{val.rstrip()}\n")
    return "\n".join(parts).rstrip() + "\n"


def build_draft_row(
    *,
    draft: dict[str, Any],
    candidate: dict[str, Any],
    reviewer_id: str,
    decision_date: str,
    decision_id: str,
    review_checksum: str,
) -> dict[str, Any]:
    proposed_id = str(candidate["proposedSourceId"])
    supporting = [s for s in candidate["sourceIds"] if s != proposed_id]
    text = str(candidate["proposedSanskritText"])
    row = dict(draft)
    row.update(
        {
            "approvalDate": decision_date,
            "approvalStatus": "APPROVED",
            "approvedSourceIds": [proposed_id] + supporting,
            "classification": "FINAL_CONFLICT_RESOLUTION",
            "decisionType": DECISION_TYPE,
            "editorialApprovalChecksum": editorial_approval_checksum(
                ref=str(candidate["canonicalReference"]),
                decision_id=decision_id,
                sanskrit_text=text,
                selected_source_id=proposed_id,
                supporting_source_ids=supporting,
                reviewer_id=reviewer_id,
                decision_date=decision_date,
            ),
            "editorialDecisionId": decision_id,
            "editorialNotes": [
                f"decisionType={DECISION_TYPE}",
                f"agreementPattern={candidate.get('agreementPattern')}",
                f"segmentationResolved={candidate.get('segmentationResolved')}",
                "Selected exact Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE text; no synthesis.",
                "IIT remains SECONDARY_VERIFICATION_REFERENCE.",
                "Sanskrit Documents remains THIRD_EDITORIAL_VERIFICATION_REFERENCE.",
                "Three-source comparison documented in review; 2_OF_3/mixed does not auto-approve.",
            ]
            + list(candidate.get("notes") or []),
            "priorClassification": "SOURCE_CONFLICT",
            "reviewFileChecksum": review_checksum,
            "reviewerId": reviewer_id,
            "sanskritText": text,
            "selectedSourceChecksum": next(
                (
                    s.get("sourceChecksum")
                    for s in []  # filled below from comparison externally if needed
                ),
                None,
            ),
            "selectedSourceId": proposed_id,
            "transliteration": None,
        }
    )
    return row


def build_manifest(*, decision_date: str, reviewer_id: str) -> dict[str, Any]:
    return {
        "approved": EXPECTED_FINAL_APPROVED,
        "candidatePath": f"content/editorial/bhagavad-gita/chapter-01/{CANDIDATES_NAME}",
        "chapterNumber": 1,
        "conflictAnalysisPath": "content/editorial/bhagavad-gita/chapter-01/source-conflict-analysis.jsonl",
        "corpusVersion": "antar-bhagavad-gita-chapter-01-v1",
        "decisionDate": decision_date,
        "decisionType": DECISION_TYPE,
        "importReady": True,
        "normalizationMatchCandidates": 34,
        "notes": [
            "APPROVED: all 47 Chapter 1 Verses approved (34 NORMALIZATION_MATCH + 11 orthographic + 2 final-conflict).",
            "Final conflicts 1.20 and 1.22 resolved with third witness Sanskrit Documents bhagvadnew.",
            "Selected canonical source: Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE (exact copy; no synthesis).",
            "IIT remains SECONDARY_VERIFICATION_REFERENCE / verification-only.",
            "Sanskrit Documents remains THIRD_EDITORIAL_VERIFICATION_REFERENCE / verification-only.",
            "Transliteration remains null. No package built. No database import performed by this tool.",
        ],
        "orthographicResolutions": 11,
        "finalConflictResolutions": 2,
        "pending": 0,
        "rejected": 0,
        "reviewer": reviewer_id,
        "secondReviewer": None,
        "sourceConflicts": 13,
        "status": "APPROVED",
        "unresolvedReferences": [],
        "unresolvedSourceConflicts": 0,
    }


def prepare_context(repo_root: Path) -> dict[str, Any]:
    chapter_dir = repo_root / "content/editorial/bhagavad-gita/chapter-01"
    reviews_dir = repo_root / "content/editorial/reviews"
    candidates_path = chapter_dir / CANDIDATES_NAME
    if not candidates_path.is_file():
        raise ApprovalError(f"missing candidates file: {candidates_path}")
    candidates = load_jsonl(candidates_path)
    if [c.get("canonicalReference") for c in candidates] != list(ALLOWED_REFS):
        raise ApprovalError(
            f"candidates must be exactly {list(ALLOWED_REFS)} in order, "
            f"found {[c.get('canonicalReference') for c in candidates]}"
        )

    draft_path = chapter_dir / "canonical-draft.jsonl"
    drafts = load_jsonl(draft_path)
    draft_by = {d["canonicalReference"]: d for d in drafts}
    approved_prior = [
        d
        for d in drafts
        if d.get("approvalStatus") == "APPROVED" and d["canonicalReference"] not in ALLOWED_REFS
    ]
    if len(approved_prior) != EXPECTED_PRIOR_APPROVED:
        raise ApprovalError(
            f"expected {EXPECTED_PRIOR_APPROVED} prior approved Verses, found {len(approved_prior)}"
        )

    comparison_path = chapter_dir / "source-comparison.jsonl"
    comps = {r["canonicalReference"]: r for r in load_jsonl(comparison_path)}
    registry = registry_by_id(repo_root)

    errors: list[str] = []
    for cand in candidates:
        ref = cand["canonicalReference"]
        errors.extend(
            validate_candidate(
                cand,
                registry=registry,
                comparison=comps.get(ref),
                draft=draft_by.get(ref),
                repo_root=repo_root,
            )
        )
        review_path = reviews_dir / f"{ref}.md"
        if not review_path.is_file():
            errors.append(f"{ref}: missing review file")
        else:
            review_text = review_path.read_text(encoding="utf-8")
            status = None
            secs = split_sections(review_text)
            if "Status" in secs:
                status = secs["Status"].strip().splitlines()[0].strip()
            if status != "UNDER_REVIEW":
                errors.append(
                    f"{ref}: review status must be UNDER_REVIEW before apply (got {status!r})"
                )
            approval = secs.get("Approval", "")
            lines = {
                ln.split(":", 1)[0].strip(): ln.split(":", 1)[1].strip()
                for ln in approval.splitlines()
                if ":" in ln
            }
            if lines.get("Reviewer") or lines.get("Date") or lines.get("Reviewer ID"):
                errors.append(f"{ref}: Approval fields must be blank before apply")

    if errors:
        raise ApprovalError("eligibility failed:\n- " + "\n- ".join(errors))

    prior_bytes = {
        "canonical-draft.jsonl": draft_path.read_bytes(),
        "source-comparison.jsonl": comparison_path.read_bytes(),
        "source-conflict-analysis.jsonl": (
            chapter_dir / "source-conflict-analysis.jsonl"
        ).read_bytes(),
        "normalization-match-approval-result.jsonl": (
            chapter_dir / "normalization-match-approval-result.jsonl"
        ).read_bytes(),
        "orthographic-resolution-result.jsonl": (
            chapter_dir / "orthographic-resolution-result.jsonl"
        ).read_bytes(),
    }
    prior_review_bytes = {
        ref: (reviews_dir / f"{ref}.md").read_bytes()
        for ref in [f"1.{n}" for n in range(1, 48)]
        if ref not in ALLOWED_REFS
    }

    return {
        "repo_root": repo_root,
        "chapter_dir": chapter_dir,
        "reviews_dir": reviews_dir,
        "candidates": candidates,
        "candidates_path": candidates_path,
        "drafts": drafts,
        "draft_by": draft_by,
        "comps": comps,
        "registry": registry,
        "prior_bytes": prior_bytes,
        "prior_review_bytes": prior_review_bytes,
        "draft_path": draft_path,
    }


def apply_mutations(
    context: dict[str, Any],
    *,
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
    stage_root: Path,
) -> dict[str, Any]:
    chapter_dir: Path = context["chapter_dir"]
    stage_chapter = stage_root / "content/editorial/bhagavad-gita/chapter-01"
    stage_reviews = stage_root / "content/editorial/reviews"
    stage_chapter.mkdir(parents=True, exist_ok=True)
    stage_reviews.mkdir(parents=True, exist_ok=True)

    # copy immutable priors
    for name, data in context["prior_bytes"].items():
        (stage_chapter / name).write_bytes(data)
    for ref, data in context["prior_review_bytes"].items():
        (stage_reviews / f"{ref}.md").write_bytes(data)

    # also copy candidates into stage as starting point
    shutil.copy2(context["candidates_path"], stage_chapter / CANDIDATES_NAME)

    new_drafts = []
    results = []
    updated_candidates = []
    for draft in context["drafts"]:
        ref = draft["canonicalReference"]
        if ref not in ALLOWED_REFS:
            new_drafts.append(draft)
            continue
        candidate = next(c for c in context["candidates"] if c["canonicalReference"] == ref)
        decision_id = decision_id_for(ref, decision_date)
        review_src = context["reviews_dir"] / f"{ref}.md"
        review_text = review_src.read_text(encoding="utf-8")
        new_review = update_review(
            review_text,
            candidate=candidate,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision_date=decision_date,
            decision_id=decision_id,
        )
        review_errors = validate_review_text(new_review, path_label=f"reviews/{ref}.md")
        if review_errors:
            raise ApprovalError(f"review validation failed for {ref}: {review_errors}")
        (stage_reviews / f"{ref}.md").write_text(new_review, encoding="utf-8")
        review_checksum = sha256_text(new_review)

        proposed_id = str(candidate["proposedSourceId"])
        supporting = [s for s in candidate["sourceIds"] if s != proposed_id]
        text = str(candidate["proposedSanskritText"])
        comp = context["comps"][ref]
        selected_checksum = None
        for s in comp.get("sources") or []:
            if s.get("sourceId") == proposed_id:
                selected_checksum = s.get("sourceChecksum")
                break

        row = dict(draft)
        row.update(
            {
                "approvalDate": decision_date,
                "approvalStatus": "APPROVED",
                "approvedSourceIds": [proposed_id] + supporting,
                "classification": "FINAL_CONFLICT_RESOLUTION",
                "contentVersion": draft.get("contentVersion", 1),
                "decisionType": DECISION_TYPE,
                "editorialApprovalChecksum": editorial_approval_checksum(
                    ref=ref,
                    decision_id=decision_id,
                    sanskrit_text=text,
                    selected_source_id=proposed_id,
                    supporting_source_ids=supporting,
                    reviewer_id=reviewer_id,
                    decision_date=decision_date,
                ),
                "editorialDecisionId": decision_id,
                "editorialNotes": [
                    f"decisionType={DECISION_TYPE}",
                    f"agreementPattern={candidate.get('agreementPattern')}",
                    f"segmentationResolved={candidate.get('segmentationResolved')}",
                    "Selected exact Wikisource PRIMARY_TRANSCRIPTION_CANDIDATE text; no synthesis.",
                    "IIT remains SECONDARY_VERIFICATION_REFERENCE.",
                    "Sanskrit Documents remains THIRD_EDITORIAL_VERIFICATION_REFERENCE.",
                ]
                + list(candidate.get("notes") or []),
                "priorClassification": "SOURCE_CONFLICT",
                "reviewFileChecksum": review_checksum,
                "reviewerId": reviewer_id,
                "sanskritText": text,
                "sanskritTextChecksum": sha256_text(text),
                "selectedSourceChecksum": selected_checksum,
                "selectedSourceId": proposed_id,
                "transliteration": None,
            }
        )
        new_drafts.append(row)

        cand_out = dict(candidate)
        cand_out["approvalStatus"] = "APPROVED"
        updated_candidates.append(cand_out)

        results.append(
            {
                "approvalStatus": "APPROVED",
                "canonicalReference": ref,
                "canonicalTextChecksum": sha256_text(text),
                "decisionDate": decision_date,
                "editorialDecisionId": decision_id,
                "agreementPattern": candidate.get("agreementPattern"),
                "originalWikisourceForm": text,
                "reviewFileChecksum": review_checksum,
                "reviewerId": reviewer_id,
                "segmentationResolved": candidate.get("segmentationResolved"),
                "selectedSourceId": proposed_id,
                "sourceIds": candidate.get("sourceIds"),
            }
        )

    # verify prior approved drafts byte-identical in payload sense
    for old, new in zip(context["drafts"], new_drafts):
        if old["canonicalReference"] in ALLOWED_REFS:
            continue
        if json.dumps(old, ensure_ascii=False, sort_keys=True) != json.dumps(
            new, ensure_ascii=False, sort_keys=True
        ):
            raise ApprovalError(
                f"prior approved draft mutated: {old['canonicalReference']}"
            )

    (stage_chapter / "canonical-draft.jsonl").write_text(dump_jsonl(new_drafts), encoding="utf-8")
    (stage_chapter / CANDIDATES_NAME).write_text(dump_jsonl(updated_candidates), encoding="utf-8")
    (stage_chapter / RESULT_NAME).write_text(dump_jsonl(results), encoding="utf-8")
    (stage_chapter / "chapter-01-approval-manifest.json").write_text(
        dump_json(build_manifest(decision_date=decision_date, reviewer_id=reviewer_id)),
        encoding="utf-8",
    )

    # freeze historical conflict analysis / comparison / prior results
    for name in (
        "source-comparison.jsonl",
        "source-conflict-analysis.jsonl",
        "normalization-match-approval-result.jsonl",
        "orthographic-resolution-result.jsonl",
    ):
        if (stage_chapter / name).read_bytes() != context["prior_bytes"][name]:
            raise ApprovalError(f"{name} must remain byte-identical")

    return {"results": results, "drafts": new_drafts}


def publish_stage(stage_root: Path, repo_root: Path) -> None:
    src_chapter = stage_root / "content/editorial/bhagavad-gita/chapter-01"
    dst_chapter = repo_root / "content/editorial/bhagavad-gita/chapter-01"
    src_reviews = stage_root / "content/editorial/reviews"
    dst_reviews = repo_root / "content/editorial/reviews"
    for name in (
        "canonical-draft.jsonl",
        CANDIDATES_NAME,
        RESULT_NAME,
        "chapter-01-approval-manifest.json",
    ):
        shutil.copy2(src_chapter / name, dst_chapter / name)
    for ref in ALLOWED_REFS:
        shutil.copy2(src_reviews / f"{ref}.md", dst_reviews / f"{ref}.md")


def run(
    *,
    reviewer_id: str,
    reviewer_name: str,
    decision_date: str,
    apply: bool,
    repo_root: Path = REPO_ROOT,
) -> int:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", decision_date):
        raise ApprovalError("decision-date must be YYYY-MM-DD")
    if reviewer_id != "onkar-dangi":
        raise ApprovalError("reviewer-id must be onkar-dangi for this Chapter 1 tool")
    if reviewer_name != "Onkar Dangi":
        raise ApprovalError('reviewer-name must be "Onkar Dangi" for this Chapter 1 tool')

    context = prepare_context(repo_root)
    with tempfile.TemporaryDirectory(prefix="antar-final-conflict-") as tmp:
        stage_root = Path(tmp)
        outcome = apply_mutations(
            context,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision_date=decision_date,
            stage_root=stage_root,
        )
        if not apply:
            print("DRY_RUN_OK")
            print(f"would_approve={',' .join(ALLOWED_REFS)}")
            print(f"result_count={len(outcome['results'])}")
            print("mutations=0")
            return 0
        publish_stage(stage_root, repo_root)
        print("APPLY_OK")
        print(f"approved={',' .join(ALLOWED_REFS)}")
        print(f"final_approved_count={EXPECTED_FINAL_APPROVED}")
        print("importReady=true")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Approve Chapter 1 final conflicts 1.20 and 1.22 only."
    )
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--reviewer-name", required=True)
    parser.add_argument("--decision-date", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        return run(
            reviewer_id=args.reviewer_id,
            reviewer_name=args.reviewer_name,
            decision_date=args.decision_date,
            apply=args.apply,
        )
    except ApprovalError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
