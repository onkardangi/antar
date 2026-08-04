#!/usr/bin/env python3
"""Prepare Chapter 1 for human editorial approval.

Generates batch-approval candidates for NORMALIZATION_MATCH Verses and
focused conflict/orthography reports for SOURCE_CONFLICT Verses.

Never sets APPROVED. Never modifies canonical-draft.jsonl.
Never invents or synthesizes Sanskrit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from compare_sources import (  # noqa: E402
    apply_normalization,
    enabled_rules,
    load_json,
    load_jsonl,
    split_segments,
    tokenize_words,
    write_jsonl,
)

WIKISOURCE_ID = "bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151"
CORPUS_VERSION = "antar-bhagavad-gita-chapter-01-v1"
ENGINE_NOTE = "prepare_chapter01_approval/v1"

# Narrow pattern detectors (analysis only; no policy mutation).
ANUSVARA_VS_NGA = re.compile(r"सं(?=कर)|सङ्(?=कर)|सं(?=बन्ध)|सम्(?=बन्ध)|संग(?=म्य)|सङ्ग(?=म्य)")
ANUSVARA_VS_NYA = re.compile(r"ंजय|ञ्जय|ंजयः|ञ्जयः")
AVAGRAHA = re.compile(r"ऽ+")
VOCALIC_R_VARIANT = re.compile(r"ॄ|ृ़")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_by_role(record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    wiki = next(s for s in record["sources"] if s.get("sourceId") == WIKISOURCE_ID)
    iitk = next(s for s in record["sources"] if "iitk" in str(s.get("sourceId", "")))
    return wiki, iitk


def selection_reason() -> str:
    return (
        "Prefer Wikisource as PRIMARY_TRANSCRIPTION_CANDIDATE per editorial provenance; "
        "IIT remains SECONDARY_VERIFICATION_REFERENCE only. Proposed text is an exact copy "
        "of the Wikisource observed Sanskrit — not a synthesis."
    )


def build_batch_candidates(
    reports: list[dict[str, Any]],
    comparisons: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for report in reports:
        if report["classification"] != "NORMALIZATION_MATCH":
            continue
        ref = report["canonicalReference"]
        rec = comparisons[ref]
        wiki, iitk = source_by_role(rec)
        proposed = wiki["sanskritText"]
        if not isinstance(proposed, str) or not proposed.strip():
            raise SystemExit(f"{ref}: Wikisource Sanskrit missing")
        out.append(
            {
                "canonicalReference": ref,
                "chapterNumber": report["chapterNumber"],
                "verseNumber": report["verseNumber"],
                "proposedSanskritText": proposed,
                "proposedSanskritTextChecksumSha256": sha256_text(proposed),
                "proposedTransliteration": None,
                "selectedSourceId": wiki["sourceId"],
                "selectedSourceChecksum": wiki.get("sourceChecksum"),
                "selectedSourceEvidenceChecksum": wiki.get("recordChecksum")
                or wiki.get("sourceChecksum"),
                "supportingSourceIds": [iitk["sourceId"]],
                "supportingSourceChecksums": {
                    iitk["sourceId"]: {
                        "sourceChecksum": iitk.get("sourceChecksum"),
                        "evidenceChecksum": iitk.get("evidenceChecksum"),
                    }
                },
                "selectionReason": selection_reason(),
                "classification": "NORMALIZATION_MATCH",
                "confidence": report["confidence"],
                "differences": report.get("differences") or [],
                "normalizationRulesApplied": report.get("normalizationRulesApplied") or [],
                "requiresHumanApproval": True,
                "approvalStatus": "PENDING",
            }
        )
    out.sort(key=lambda r: (r["chapterNumber"], r["verseNumber"]))
    return out


def pattern_group_key(differences: list[dict[str, Any]], rules: list[str]) -> str:
    cats = tuple(sorted(d["category"] for d in differences))
    if cats == ("DANDA_STYLE", "VERSE_MARKER", "WHITESPACE"):
        return "A_marker_whitespace_danda"
    if "FRONT_MATTER" in cats and "ORTHOGRAPHY_APPROVED" in cats:
        return "B_front_matter_plus_approved_orthography"
    return "Z_other_" + "-".join(cats)


def write_batch_review_md(path: Path, candidates: list[dict[str, Any]]) -> None:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in candidates:
        key = pattern_group_key(c["differences"], c["normalizationRulesApplied"])
        groups[key].append(c)

    lines = [
        "# Chapter 1 — NORMALIZATION_MATCH batch approval candidate",
        "",
        "**Automated preparation is not scholarly approval.**",
        "",
        f"- Candidates: `{len(candidates)}`",
        "- Selected source policy: Wikisource `PRIMARY_TRANSCRIPTION_CANDIDATE`",
        "- Supporting source: IIT Kanpur `SECONDARY_VERIFICATION_REFERENCE`",
        "- Proposed Sanskrit is an **exact copy** of the selected source text",
        "- Transliteration: `null` (not populated)",
        "- Approval: all checkboxes left unchecked / `PENDING`",
        "",
        "## Reviewer checklist",
        "",
        "- [ ] Reviewer name recorded in `chapter-01-approval-manifest.json`",
        "- [ ] Second reviewer recorded (if required)",
        "- [ ] Batch candidates inspected by pattern group",
        "- [ ] No Verse auto-approved",
        "",
    ]

    group_titles = {
        "A_marker_whitespace_danda": (
            "Group A — Whitespace / verse-marker / danda-style only "
            "(roots otherwise match after approved comparison normalization)"
        ),
        "B_front_matter_plus_approved_orthography": (
            "Group B — Front matter + approved संजय↔सञ्जय orthography + marker/whitespace"
        ),
    }

    for key in sorted(groups.keys()):
        items = groups[key]
        title = group_titles.get(key, f"Group {key}")
        lines.extend([f"## {title}", "", f"Count: `{len(items)}`", ""])
        lines.append(
            "| Ref | Selected | Supporting | Diff categories | Exact differing forms | Proposed form | Conf | Approve |"
        )
        lines.append("|-----|----------|------------|-----------------|----------------------|---------------|------|---------|")
        for c in items:
            cats = ", ".join(d["category"] for d in c["differences"]) or "none"
            forms = "; ".join(
                f"`{d['category']}`: {d.get('detail','')}" for d in c["differences"]
            ) or "none (exact structural match after documented normalization)"
            # Keep table compact: truncate long proposed text
            proposed_preview = c["proposedSanskritText"].replace("\n", " / ")
            if len(proposed_preview) > 80:
                proposed_preview = proposed_preview[:77] + "…"
            lines.append(
                f"| `{c['canonicalReference']}` | `{c['selectedSourceId']}` | "
                f"`{', '.join(c['supportingSourceIds'])}` | `{cats}` | {forms} | "
                f"`{proposed_preview}` | `{c['confidence']}` | [ ] |"
            )
        lines.append("")
        lines.append(
            "Exact proposed Sanskrit for each reference is in "
            "`normalization-match-approval-candidate.jsonl` "
            "(byte-identical to Wikisource `sanskritText`)."
        )
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def classify_conflict_kind(
    *,
    categories: set[str],
    token_diffs: list[dict[str, Any]],
    speakers_equal: bool,
) -> dict[str, bool]:
    orthographic_only = False
    root_diffs = [t for t in token_diffs if t.get("field") != "speakerLabel"]
    speaker_diffs = [t for t in token_diffs if t.get("field") == "speakerLabel"]

    if categories <= {"WHITESPACE", "VERSE_MARKER", "DANDA_STYLE", "ORTHOGRAPHY_UNAPPROVED", "PUNCTUATION"}:
        if "ORTHOGRAPHY_UNAPPROVED" in categories and root_diffs:
            orthographic_only = all(t.get("looksOrthographic", False) for t in root_diffs)
        elif "ORTHOGRAPHY_UNAPPROVED" not in categories and not root_diffs:
            orthographic_only = True

    # Speaker-label-only conflicts that are orthographic (e.g. संजय↔सञ्जय).
    if (
        "SPEAKER_LABEL" in categories
        and not root_diffs
        and speaker_diffs
        and all(t.get("looksOrthographic", False) for t in speaker_diffs)
    ):
        orthographic_only = True

    if categories == {"WHITESPACE", "SPEAKER_LABEL", "VERSE_MARKER", "DANDA_STYLE"} and not speakers_equal:
        if not root_diffs and (
            not speaker_diffs or all(t.get("looksOrthographic", False) for t in speaker_diffs)
        ):
            orthographic_only = True

    return {
        "orthographicOnly": orthographic_only,
        "punctuationOnly": categories <= {"PUNCTUATION", "DANDA_STYLE", "VERSE_MARKER", "WHITESPACE"}
        and "ORTHOGRAPHY_UNAPPROVED" not in categories
        and "WORD_DIFFERENCE" not in categories
        and not root_diffs,
        "speakerLabelRelated": "SPEAKER_LABEL" in categories,
        "wordDifference": "WORD_DIFFERENCE" in categories,
        "wordOrderDifference": "WORD_ORDER" in categories,
        "missingText": "MISSING_TEXT" in categories,
        "extraText": "EXTRA_TEXT" in categories,
        "segmentationDifference": any(t.get("looksSegmentation", False) for t in root_diffs),
    }


def looks_orthographic_pair(a: str, b: str) -> bool:
    """Heuristic: same letters ignoring anusvara/nasal/avagraha/vocalic-r presentation."""
    if a == b:
        return True

    def fold(s: str) -> str:
        s = unicodedata.normalize("NFC", s)
        s = s.replace("ऽ", "")
        # anusvara / ङ् / ञ् / म् before common consonants — fold for identity check only
        s = s.replace("ङ्क", "ंक").replace("ङ्ख", "ंख").replace("ङ्ग", "ंग").replace("ङ्घ", "ंघ")
        s = s.replace("ञ्च", "ंच").replace("ञ्ज", "ंज")
        s = s.replace("म्ब", "ंब").replace("म्भ", "ंभ")
        s = s.replace("सङ्", "सं").replace("सम्", "सं")
        s = s.replace("ृ़", "ॄ").replace("ॄ", "ृ")  # presentation variants of vocalic r
        s = re.sub(r"[\s।॥]+", "", s)
        return s

    return fold(a) == fold(b)


def looks_segmentation_pair(a: str, b: str) -> bool:
    """One side is concatenation of tokens that appear split on the other (approx)."""
    return a.replace(" ", "") == b.replace(" ", "") and a != b


def token_level_diff(wiki_root: str, iitk_root: str) -> list[dict[str, Any]]:
    wa = tokenize_words(wiki_root)
    wb = tokenize_words(iitk_root)
    diffs: list[dict[str, Any]] = []
    # align greedily
    i = j = 0
    while i < len(wa) or j < len(wb):
        if i < len(wa) and j < len(wb) and wa[i] == wb[j]:
            i += 1
            j += 1
            continue
        if i < len(wa) and j < len(wb):
            # try segmentation: wiki compound vs two iitk tokens
            if j + 1 < len(wb) and wa[i] == wb[j] + wb[j + 1]:
                diffs.append(
                    {
                        "wikisourceToken": wa[i],
                        "iitkTokens": [wb[j], wb[j + 1]],
                        "surrounding": _surround(wa, i),
                        "looksOrthographic": False,
                        "looksSegmentation": True,
                        "charDiffs": _char_diffs(wa[i], wb[j] + wb[j + 1]),
                    }
                )
                i += 1
                j += 2
                continue
            if i + 1 < len(wa) and wb[j] == wa[i] + wa[i + 1]:
                diffs.append(
                    {
                        "wikisourceTokens": [wa[i], wa[i + 1]],
                        "iitkToken": wb[j],
                        "surrounding": _surround(wb, j),
                        "looksOrthographic": False,
                        "looksSegmentation": True,
                        "charDiffs": _char_diffs(wa[i] + wa[i + 1], wb[j]),
                    }
                )
                i += 2
                j += 1
                continue
            diffs.append(
                {
                    "wikisourceToken": wa[i],
                    "iitkToken": wb[j],
                    "surrounding": _surround(wa, i),
                    "looksOrthographic": looks_orthographic_pair(wa[i], wb[j]),
                    "looksSegmentation": looks_segmentation_pair(wa[i], wb[j]),
                    "charDiffs": _char_diffs(wa[i], wb[j]),
                }
            )
            i += 1
            j += 1
            continue
        if i < len(wa):
            diffs.append(
                {
                    "wikisourceToken": wa[i],
                    "iitkToken": None,
                    "surrounding": _surround(wa, i),
                    "looksOrthographic": False,
                    "looksSegmentation": False,
                    "charDiffs": [],
                }
            )
            i += 1
        else:
            diffs.append(
                {
                    "wikisourceToken": None,
                    "iitkToken": wb[j],
                    "surrounding": _surround(wb, j),
                    "looksOrthographic": False,
                    "looksSegmentation": False,
                    "charDiffs": [],
                }
            )
            j += 1
    return diffs


def _surround(tokens: list[str], idx: int) -> str:
    lo = max(0, idx - 1)
    hi = min(len(tokens), idx + 2)
    return " ".join(tokens[lo:hi])


def _char_diffs(a: str, b: str) -> list[dict[str, Any]]:
    # Simple LCS-ish reporting of unequal code points with NFC forms
    a_n = unicodedata.normalize("NFC", a)
    b_n = unicodedata.normalize("NFC", b)
    out: list[dict[str, Any]] = []
    # zip to min length then leftovers
    for i, (ca, cb) in enumerate(zip(a_n, b_n)):
        if ca != cb:
            out.append(
                {
                    "index": i,
                    "wikisourceChar": ca,
                    "wikisourceCodepoint": f"U+{ord(ca):04X}",
                    "iitkChar": cb,
                    "iitkCodepoint": f"U+{ord(cb):04X}",
                    "sameVisibleFamily": looks_orthographic_pair(ca, cb)
                    or unicodedata.normalize("NFD", ca) == unicodedata.normalize("NFD", cb),
                }
            )
    if len(a_n) != len(b_n):
        out.append(
            {
                "index": min(len(a_n), len(b_n)),
                "detail": f"length {len(a_n)} vs {len(b_n)}",
                "wikisourceSuffix": a_n[len(b_n) :] if len(a_n) > len(b_n) else "",
                "iitkSuffix": b_n[len(a_n) :] if len(b_n) > len(a_n) else "",
            }
        )
    return out


def detect_pattern_ids(wiki_tok: str | None, iitk_tok: str | None) -> list[str]:
    ids: list[str] = []
    pair = f"{wiki_tok or ''}::{iitk_tok or ''}"
    if wiki_tok and iitk_tok and looks_orthographic_pair(wiki_tok, iitk_tok):
        if ("ं" in pair or "ङ्" in pair or "ञ्" in pair or "म्" in pair) and (
            "ं" in (wiki_tok + iitk_tok) or "ङ्" in pair or "ञ्" in pair
        ):
            if "जय" in pair or "ञ्ज" in pair or "ंज" in pair:
                ids.append("anusvara_vs_nya_cluster")
            elif "कर" in pair or "ङ्क" in pair or "सङ्" in pair or "संक" in pair:
                ids.append("anusvara_vs_nga_cluster")
            elif "बन्ध" in pair or "म्ब" in pair:
                ids.append("anusvara_vs_ma_cluster")
            else:
                ids.append("anusvara_vs_homorganic_nasal")
        if "ऽ" in pair:
            ids.append("avagraha_representation")
        if "ॄ" in pair or "ृ़" in pair or "ृ" in pair:
            ids.append("vocalic_r_presentation")
        if "संग" in pair or "सङ्ग" in pair:
            ids.append("anusvara_vs_nga_in_sangamya")
    if wiki_tok and iitk_tok and looks_segmentation_pair(wiki_tok, iitk_tok):
        ids.append("sandhi_segmentation")
    return ids


def recommendation_for(
    *,
    kinds: dict[str, bool],
    categories: set[str],
    pattern_ids: list[str],
    covered_by_policy: bool,
) -> str:
    if kinds["wordDifference"] and not kinds["orthographicOnly"]:
        if kinds["segmentationDifference"] and not any(
            p.startswith("anusvara") or p == "avagraha_representation" for p in pattern_ids
        ):
            return "REQUIRES_EDITORIAL_SOURCE"
        if kinds["missingText"] or kinds["extraText"]:
            return "REQUIRES_EDITORIAL_SOURCE"
        return "SUBSTANTIVE_CONFLICT"
    if kinds["orthographicOnly"]:
        if covered_by_policy:
            return "CONSIDER_NORMALIZATION_RULE"  # e.g. extend speaker-label application
        if pattern_ids:
            return "CONSIDER_NORMALIZATION_RULE"
        return "REQUIRES_EDITORIAL_SOURCE"
    if kinds["speakerLabelRelated"] and kinds["orthographicOnly"]:
        return "CONSIDER_NORMALIZATION_RULE"
    return "SUBSTANTIVE_CONFLICT"


def build_conflict_analyses(
    reports: list[dict[str, Any]],
    comparisons: dict[str, dict[str, Any]],
    policy: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    rules = enabled_rules(policy)
    pattern_hits: dict[str, list[str]] = defaultdict(list)
    analyses: list[dict[str, Any]] = []

    # First pass collect pattern frequencies
    interim: list[dict[str, Any]] = []
    for report in reports:
        if report["classification"] != "SOURCE_CONFLICT":
            continue
        ref = report["canonicalReference"]
        rec = comparisons[ref]
        wiki, iitk = source_by_role(rec)
        seg_a = split_segments(wiki["sanskritText"], rules)
        seg_b = split_segments(iitk["sanskritText"], rules)
        root_a, _ = apply_normalization(seg_a["rootVerseBody"], rules)
        root_b, _ = apply_normalization(seg_b["rootVerseBody"], rules)
        root_a = re.sub(r"\n+", "\n", root_a).strip()
        root_b = re.sub(r"\n+", "\n", root_b).strip()
        token_diffs = token_level_diff(root_a, root_b)
        # speaker orthography
        if (seg_a["speakerLabel"] or "") != (seg_b["speakerLabel"] or ""):
            token_diffs.append(
                {
                    "wikisourceToken": seg_a["speakerLabel"],
                    "iitkToken": seg_b["speakerLabel"],
                    "surrounding": "speaker_label",
                    "looksOrthographic": looks_orthographic_pair(
                        seg_a["speakerLabel"] or "", seg_b["speakerLabel"] or ""
                    ),
                    "looksSegmentation": False,
                    "charDiffs": _char_diffs(
                        seg_a["speakerLabel"] or "", seg_b["speakerLabel"] or ""
                    ),
                    "field": "speakerLabel",
                }
            )
        cats = {d["category"] for d in report.get("differences") or []}
        kinds = classify_conflict_kind(
            categories=cats,
            token_diffs=token_diffs,
            speakers_equal=(seg_a["speakerLabel"] or "") == (seg_b["speakerLabel"] or ""),
        )
        # segmentation flag from 1.20-style
        if any(t.get("looksSegmentation") for t in token_diffs):
            kinds["segmentationDifference"] = True

        pids: list[str] = []
        for t in token_diffs:
            a = t.get("wikisourceToken") or (
                "".join(t["wikisourceTokens"]) if t.get("wikisourceTokens") else None
            )
            b = t.get("iitkToken") or (
                "".join(t["iitkTokens"]) if t.get("iitkTokens") else None
            )
            for pid in detect_pattern_ids(a, b):
                pids.append(pid)
                pattern_hits[pid].append(ref)

        covered = False
        speaker_diffs = [t for t in token_diffs if t.get("field") == "speakerLabel"]
        if speaker_diffs and all(t.get("looksOrthographic") for t in speaker_diffs):
            for t in speaker_diffs:
                wa = (t.get("wikisourceToken") or "").replace(" उवाच", "").strip()
                wb = (t.get("iitkToken") or "").replace(" उवाच", "").strip()
                if {wa, wb} <= {"संजय", "सञ्जय"}:
                    covered = True
                    pids = list(dict.fromkeys(pids + ["sanjaya_speaker_label_extension"]))
                    pattern_hits["sanjaya_speaker_label_extension"].append(ref)

        interim.append(
            {
                "report": report,
                "wiki": wiki,
                "iitk": iitk,
                "root_a": root_a,
                "root_b": root_b,
                "seg_a": seg_a,
                "seg_b": seg_b,
                "token_diffs": token_diffs,
                "cats": cats,
                "kinds": kinds,
                "pids": list(dict.fromkeys(pids)),
                "covered": covered,
            }
        )

    for item in interim:
        report = item["report"]
        ref = report["canonicalReference"]
        freqs = {pid: len(set(pattern_hits[pid])) for pid in item["pids"]}
        rec = recommendation_for(
            kinds=item["kinds"],
            categories=item["cats"],
            pattern_ids=item["pids"],
            covered_by_policy=item["covered"],
        )
        requires_third = rec in {"REQUIRES_EDITORIAL_SOURCE", "SUBSTANTIVE_CONFLICT"} and not (
            item["kinds"]["orthographicOnly"] and rec == "CONSIDER_NORMALIZATION_RULE"
        )
        # Explicit: non-orthographic-only → third reference
        if not item["kinds"]["orthographicOnly"]:
            requires_third = True
            if rec == "CONSIDER_NORMALIZATION_RULE":
                rec = "REQUIRES_EDITORIAL_SOURCE"

        candidate_rule = None
        if rec == "CONSIDER_NORMALIZATION_RULE" and item["pids"]:
            candidate_rule = {
                "proposedRuleIds": item["pids"],
                "scope": "comparison-only; do not rewrite stored sources",
                "status": "PROPOSED_NOT_ADDED",
            }

        analyses.append(
            {
                "canonicalReference": ref,
                "chapterNumber": report["chapterNumber"],
                "verseNumber": report["verseNumber"],
                "classification": "SOURCE_CONFLICT",
                "wikisourceObservedText": item["wiki"]["sanskritText"],
                "iitkObservedText": item["iitk"]["sanskritText"],
                "wikisourceSourceId": item["wiki"]["sourceId"],
                "iitkSourceId": item["iitk"]["sourceId"],
                "wikisourceRootNormalizedForAnalysis": item["root_a"],
                "iitkRootNormalizedForAnalysis": item["root_b"],
                "speakerLabels": {
                    "wikisource": item["seg_a"]["speakerLabel"],
                    "iitk": item["seg_b"]["speakerLabel"],
                },
                "differenceCategories": sorted(item["cats"]),
                "tokenLevelDifferences": item["token_diffs"],
                "characterLevelDifferences": [
                    c for t in item["token_diffs"] for c in (t.get("charDiffs") or [])
                ],
                "differenceKindFlags": item["kinds"],
                "existingNormalizationRuleCovers": item["covered"],
                "candidateNormalizationRule": candidate_rule,
                "patternIds": item["pids"],
                "patternFrequencyInChapter1": freqs,
                "recommendation": rec,
                "requiresThirdReference": requires_third,
                "humanDecisionRequired": True,
                "approvalStatus": "PENDING",
            }
        )

    analyses.sort(key=lambda r: (r["chapterNumber"], r["verseNumber"]))
    return analyses, {k: sorted(set(v)) for k, v in pattern_hits.items()}


def write_orthographic_patterns_md(
    path: Path,
    pattern_hits: dict[str, list[str]],
    analyses: list[dict[str, Any]],
) -> None:
    catalog = {
        "anusvara_vs_nga_cluster": {
            "observedForms": ["संकर / सङ्कर", "संगम्य / सङ्गम्य"],
            "description": (
                "Anusvāra (ं) versus explicit velar nasal cluster (ङ्) before क/ग."
            ),
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": (
                "Consider a narrowly scoped comparison-only equivalence for "
                "सं↔सङ् before क/ग in these attested Chapter 1 forms only — "
                "do not add broad spelling substitutions yet."
            ),
            "overNormRisk": "High if generalized beyond attested environments.",
        },
        "anusvara_vs_nga_in_sangamya": {
            "observedForms": ["आचार्यमुपसंगम्य / आचार्यमुपसङ्गम्य"],
            "description": "Same anusvāra↔ङ् alternation inside उपसंगम्य.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": "Fold into narrow anusvāra↔ङ् comparison rule if approved.",
            "overNormRisk": "Medium — limit to documented lemma environments.",
        },
        "anusvara_vs_nya_cluster": {
            "observedForms": ["समितिंजयः / समितिञ्जयः", "धनञ्जयः / धनंजयः"],
            "description": "Anusvāra versus ñ-cluster (ञ्ज) in -जय compounds.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": (
                "Consider comparison-only equivalence for ंजय↔ञ्जय in epithets; "
                "distinct from the already-approved संजय↔सञ्जय pair."
            ),
            "overNormRisk": "Medium if applied outside -जय epithets.",
        },
        "anusvara_vs_ma_cluster": {
            "observedForms": ["संबन्धिनस्तथा / सम्बन्धिनस्तथा"],
            "description": "Anusvāra versus explicit म् before ब (homorganic labial).",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": "Consider narrow संब↔सम्ब comparison equivalence if approved.",
            "overNormRisk": "Medium.",
        },
        "anusvara_vs_homorganic_nasal": {
            "observedForms": ["generic anusvāra ↔ homorganic nasal"],
            "description": "Catch-all for anusvāra/homorganic nasal presentation.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": "Do not add a broad rule from mixed cases; prefer narrow lemmas.",
            "overNormRisk": "Very high if broad.",
        },
        "avagraha_representation": {
            "observedForms": ["परयाविष्टो / परयाऽऽविष्टो", "एवमुक्त्वार्जुनः / एवमुक्त्वाऽर्जुनः"],
            "description": "Presence/absence of avagraha (ऽ) marking vowel sandhi elision.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": (
                "Consider comparison-only avagraha-optional rule for identical vowel sandhi; "
                "do not strip avagraha from stored sources."
            ),
            "overNormRisk": "Medium — avagraha can be editorially meaningful in some editions.",
        },
        "vocalic_r_presentation": {
            "observedForms": ["पितॄनथ / पितृ़नथ", "भ्रातॄन् / भ्रातृ़न्"],
            "description": "Long vocalic ṝ versus ṛ + nukta-like presentation variants.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": "Inspect with a Sanskrit orthography specialist before any rule.",
            "overNormRisk": "High — may hide real editorial choices.",
        },
        "sanjaya_speaker_label_extension": {
            "observedForms": ["सञ्जय उवाच / संजय उवाच"],
            "description": "Approved संजय↔सञ्जय pair appearing in speaker labels.",
            "changesLexicalIdentity": False,
            "alreadyCovered": True,
            "proposedPolicyAction": (
                "Extend existing orthography_sanjaya_equivalence application to speaker-label "
                "comparison (policy already lists the pair)."
            ),
            "overNormRisk": "Low if limited to the approved pair.",
        },
        "sandhi_segmentation": {
            "observedForms": ["व्यवस्थितान्दृष्ट्वा / व्यवस्थितान् + दृष्ट्वा"],
            "description": "Sandhi-joined vs spaced/tokenized segmentation of the same akṣaras.",
            "changesLexicalIdentity": False,
            "alreadyCovered": False,
            "proposedPolicyAction": "Do not auto-normalize; use third reference if lexical uncertainty remains.",
            "overNormRisk": "High if treated as spelling equivalence.",
        },
    }

    lines = [
        "# Chapter 1 orthographic pattern clusters",
        "",
        "**Analysis only. No normalization rules were added.**",
        "",
        "Automated comparison is not scholarly approval.",
        "",
    ]
    for pid, refs in sorted(pattern_hits.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        meta = catalog.get(
            pid,
            {
                "observedForms": ["see conflict analyses"],
                "description": pid,
                "changesLexicalIdentity": "unknown",
                "alreadyCovered": False,
                "proposedPolicyAction": "No rule proposed from insufficient evidence.",
                "overNormRisk": "unknown",
            },
        )
        lines.extend(
            [
                f"## `{pid}`",
                "",
                f"- Observed forms: {', '.join(f'`{f}`' for f in meta['observedForms'])}",
                f"- Affected Verses: `{', '.join(refs)}`",
                f"- Frequency: `{len(refs)}`",
                f"- Description: {meta['description']}",
                f"- Changes lexical identity: `{meta['changesLexicalIdentity']}`",
                f"- Already covered by policy: `{meta['alreadyCovered']}`",
                f"- Proposed policy action: {meta['proposedPolicyAction']}",
                f"- Risk of over-normalization: {meta['overNormRisk']}",
                "",
            ]
        )

    # Also list conflicts with no orthographic pattern id
    bare = [
        a["canonicalReference"]
        for a in analyses
        if not a["patternIds"] or a["recommendation"] != "CONSIDER_NORMALIZATION_RULE"
    ]
    lines.extend(
        [
            "## Non-cluster / editorial attention",
            "",
            "References that remain more than a repeated orthographic cluster "
            f"(or lack a safe narrow rule): `{', '.join(bare) if bare else 'none'}`",
            "",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_third_reference_queue(analyses: list[dict[str, Any]]) -> dict[str, Any]:
    entries = []
    for a in analyses:
        if not a.get("requiresThirdReference"):
            continue
        entries.append(
            {
                "canonicalReference": a["canonicalReference"],
                "conflictSummary": {
                    "categories": a["differenceCategories"],
                    "recommendation": a["recommendation"],
                    "tokenDiffs": a["tokenLevelDifferences"],
                },
                "exactEvidenceNeeded": (
                    "Independent root-Sanskrit witness for this Verse identity, "
                    "with clear edition statement and license suitable for verification."
                ),
                "recommendedTrustedManualReference": (
                    "A printed critical edition or other trusted scholarly edition "
                    "(e.g. well-documented BORI / Gita Press critical apparatus citation) "
                    "consulted manually — not bulk-scraped."
                ),
                "reasonThirdReferenceRequired": (
                    "Difference is not clearly orthographic-only under current policy; "
                    "Wikisource vs IIT alone is insufficient to choose a canonical form."
                ),
                "status": "QUEUED_NOT_ACQUIRED",
            }
        )
    return {
        "chapterNumber": 1,
        "status": "PENDING_MANUAL_ACQUISITION",
        "entryCount": len(entries),
        "entries": entries,
        "notes": [
            "No third source was acquired in this task.",
            "IIT remains verification-only and not an import corpus.",
        ],
    }


def build_manifest(candidates: list[dict[str, Any]], conflicts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "chapterNumber": 1,
        "corpusVersion": CORPUS_VERSION,
        "normalizationMatchCandidates": len(candidates),
        "sourceConflicts": len(conflicts),
        "approved": 0,
        "rejected": 0,
        "pending": len(candidates) + len(conflicts),
        "reviewer": None,
        "secondReviewer": None,
        "decisionDate": None,
        "status": "PENDING_EDITORIAL_REVIEW",
        "candidatePath": "content/editorial/bhagavad-gita/chapter-01/normalization-match-approval-candidate.jsonl",
        "conflictAnalysisPath": "content/editorial/bhagavad-gita/chapter-01/source-conflict-analysis.jsonl",
        "notes": [
            "Manifest must not become APPROVED automatically.",
            "Human reviewers must record names/dates before any Verse approval.",
        ],
    }


def generate_all(*, chapter_dir: Path = CHAPTER_DIR) -> dict[str, Any]:
    policy = load_json(REPO_ROOT / "content/editorial/normalization-policy.json")
    reports = load_jsonl(chapter_dir / "automated-comparison-report.jsonl")
    comparisons = {
        r["canonicalReference"]: r
        for r in load_jsonl(chapter_dir / "source-comparison.jsonl")
    }

    candidates = build_batch_candidates(reports, comparisons)
    conflicts, pattern_hits = build_conflict_analyses(reports, comparisons, policy)
    queue = build_third_reference_queue(conflicts)
    manifest = build_manifest(candidates, conflicts)

    # Partition check
    cand_refs = {c["canonicalReference"] for c in candidates}
    conf_refs = {c["canonicalReference"] for c in conflicts}
    if cand_refs & conf_refs:
        raise SystemExit(f"Overlap between candidate and conflict sets: {cand_refs & conf_refs}")
    expected = {f"1.{i}" for i in range(1, 48)}
    if cand_refs | conf_refs != expected:
        missing = expected - (cand_refs | conf_refs)
        extra = (cand_refs | conf_refs) - expected
        raise SystemExit(f"Partition error missing={missing} extra={extra}")

    write_jsonl(chapter_dir / "normalization-match-approval-candidate.jsonl", candidates)
    write_batch_review_md(chapter_dir / "normalization-match-review.md", candidates)
    write_jsonl(chapter_dir / "source-conflict-analysis.jsonl", conflicts)
    write_orthographic_patterns_md(
        chapter_dir / "orthographic-patterns.md", pattern_hits, conflicts
    )
    (chapter_dir / "third-reference-queue.json").write_text(
        json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (chapter_dir / "chapter-01-approval-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "candidates": len(candidates),
        "conflicts": len(conflicts),
        "thirdReferenceQueue": queue["entryCount"],
        "patternIds": sorted(pattern_hits.keys()),
        "candidateRefs": sorted(cand_refs, key=lambda r: tuple(map(int, r.split(".")))),
        "conflictRefs": sorted(conf_refs, key=lambda r: tuple(map(int, r.split(".")))),
        "thirdRefs": [e["canonicalReference"] for e in queue["entries"]],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare Chapter 1 human approval packages")
    parser.add_argument("--chapter-dir", type=Path, default=CHAPTER_DIR)
    args = parser.parse_args(argv)
    summary = generate_all(chapter_dir=args.chapter_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
