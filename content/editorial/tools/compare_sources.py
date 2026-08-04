#!/usr/bin/env python3
"""Deterministic automated editorial source comparison engine (Phase 2).

Classifies Verses; never grants final APPROVED status.
Does not invent Sanskrit. Does not modify canonical-draft.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENGINE_VERSION = "1"
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_POLICY = REPO_ROOT / "content/editorial/normalization-policy.json"
DEFAULT_CHAPTER_DIR = REPO_ROOT / "content/editorial/bhagavad-gita/chapter-01"

SPEAKER_RE = re.compile(r"^(.+?उवाच)\s*$")
MARKER_RE = re.compile(
    r"(॥\s*[०-९0-9]+\s*[-–—.]\s*[०-९0-9]+\s*॥|।{1,2}\s*[०-९0-9]+\s*[.।-]\s*[०-९0-9]+\s*।{0,2})"
)

CLASSIFICATIONS = frozenset(
    {"AUTO_MATCH", "NORMALIZATION_MATCH", "SOURCE_CONFLICT", "INSUFFICIENT_SOURCES"}
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n",
        encoding="utf-8",
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def enabled_rules(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {r["id"]: r for r in policy.get("rules", []) if r.get("enabled", True)}


def apply_normalization(text: str, rules: dict[str, dict[str, Any]]) -> tuple[str, list[str]]:
    applied: list[str] = []
    original = text

    if "line_endings_to_LF" in rules:
        text2 = text.replace("\r\n", "\n").replace("\r", "\n")
        if text2 != text:
            applied.append("line_endings_to_LF")
        text = text2

    if "unicode_nfc" in rules:
        nfc = unicodedata.normalize("NFC", text)
        if nfc != text:
            applied.append("unicode_nfc")
        text = nfc

    if "trimmed_surrounding_whitespace" in rules:
        stripped = text.strip()
        if stripped != text:
            applied.append("trimmed_surrounding_whitespace")
        text = stripped

    if "collapsed_structural_whitespace" in rules:
        lines = [re.sub(r"[ \t]+$", "", ln) for ln in text.split("\n")]
        out: list[str] = []
        changed = False
        for ln in lines:
            new_ln = re.sub(r"[ \t]{2,}", " ", ln)
            if new_ln != ln:
                changed = True
            out.append(new_ln)
        collapsed = re.sub(r"\n+", "\n", "\n".join(out)).strip("\n")
        if collapsed != text:
            changed = True
        if changed:
            applied.append("collapsed_structural_whitespace")
        text = collapsed

    if "removed_spaces_before_danda" in rules:
        spaced = re.sub(r"[ \t]+([।॥])", r"\1", text)
        if spaced != text:
            applied.append("removed_spaces_before_danda")
        text = spaced

    if "normalize_equivalent_danda_spacing" in rules:
        # Collapse runs of spaces around danda to no leading / single trailing space
        # for comparison only; originals remain preserved elsewhere.
        danda = re.sub(r"[ \t]*([।॥])[ \t]*", r"\1", text)
        if danda != text:
            applied.append("normalize_equivalent_danda_spacing")
        text = danda

    _ = original
    return text, list(dict.fromkeys(applied))


def split_segments(full_text: str, rules: dict[str, dict[str, Any]]) -> dict[str, Any]:
    text, ops = apply_normalization(full_text, rules)
    marker = None
    body = text
    if "separate_verse_marker" in rules:
        m = MARKER_RE.search(text)
        if m:
            marker = m.group(0)
            body = text[: m.start()].rstrip()
            ops = list(dict.fromkeys(ops + ["separate_verse_marker"]))
    lines = body.split("\n")
    speaker_idx = None
    for i, ln in enumerate(lines):
        if SPEAKER_RE.match(ln.strip()):
            speaker_idx = i
            break
    if speaker_idx is None:
        return {
            "frontMatter": "",
            "speakerLabel": None,
            "rootVerseBody": body,
            "verseMarker": marker,
            "ops": ops,
            "sourceFaithful": full_text,
        }
    return {
        "frontMatter": "\n".join(lines[:speaker_idx]).strip("\n"),
        "speakerLabel": lines[speaker_idx].strip(),
        "rootVerseBody": "\n".join(lines[speaker_idx + 1 :]).strip("\n"),
        "verseMarker": marker,
        "ops": ops,
        "sourceFaithful": full_text,
    }


def tokenize_words(text: str) -> list[str]:
    # Exclude danda (U+0964) and double danda (U+0965) from word tokens.
    return re.findall(r"[\u0900-\u0963\u0966-\u097F]+", text)


def fold_approved_orthography(word: str, rules: dict[str, dict[str, Any]]) -> str:
    """Fold approved orthographic variants to a stable comparison key."""
    rule = rules.get("orthography_sanjaya_equivalence")
    if rule:
        for a, b in rule.get("pairs", []):
            if word in {a, b}:
                return a
    return word


def punct_mask(s: str) -> str:
    return re.sub(r"[\u0900-\u097F\s]+", "", s)


def compare_two_texts(
    text_a: str,
    text_b: str,
    *,
    source_id_a: str,
    source_id_b: str,
    policy: dict[str, Any],
) -> dict[str, Any]:
    rules = enabled_rules(policy)
    seg_a = split_segments(text_a, rules)
    seg_b = split_segments(text_b, rules)

    root_a, ops_a = apply_normalization(seg_a["rootVerseBody"], rules)
    root_b, ops_b = apply_normalization(seg_b["rootVerseBody"], rules)
    # ensure pāda blank collapse even if already partially done
    if "collapsed_structural_whitespace" in rules:
        root_a2 = re.sub(r"\n+", "\n", root_a).strip()
        root_b2 = re.sub(r"\n+", "\n", root_b).strip()
        if root_a2 != root_a and "collapsed_structural_whitespace" not in ops_a:
            ops_a.append("collapsed_structural_whitespace")
        if root_b2 != root_b and "collapsed_structural_whitespace" not in ops_b:
            ops_b.append("collapsed_structural_whitespace")
        root_a, root_b = root_a2, root_b2

    applied = list(dict.fromkeys(seg_a["ops"] + seg_b["ops"] + ops_a + ops_b))
    differences: list[dict[str, str]] = []

    # Document structural whitespace differences on source-faithful text before discard.
    faithful_a_ws = re.sub(r"\n+", "\n", text_a.strip())
    faithful_b_ws = re.sub(r"\n+", "\n", text_b.strip())
    if re.sub(r"[ \t]+", " ", text_a) != re.sub(r"[ \t]+", " ", text_b):
        if text_a.replace(" ", "").replace("\t", "").replace("\n", "") != text_b.replace(
            " ", ""
        ).replace("\t", "").replace("\n", ""):
            pass  # not whitespace-only; word/ortho logic handles
        elif text_a != text_b:
            differences.append(
                {
                    "category": "WHITESPACE",
                    "detail": "Structural or horizontal whitespace differs between sources",
                }
            )
    # Blank-line structure specifically (common IIT vs Wikisource pattern)
    if ("\n\n" in text_a) != ("\n\n" in text_b) or text_a.count("\n\n") != text_b.count("\n\n"):
        differences.append(
            {
                "category": "WHITESPACE",
                "detail": "Blank-line structure between pādas or blocks differs",
            }
        )
    _ = faithful_a_ws, faithful_b_ws

    if (seg_a["frontMatter"] or "").strip() or (seg_b["frontMatter"] or "").strip():
        if (seg_a["frontMatter"] or "").strip() != (seg_b["frontMatter"] or "").strip():
            differences.append(
                {
                    "category": "FRONT_MATTER",
                    "detail": f"{source_id_a} vs {source_id_b}: front matter mismatch/presence",
                }
            )

    if (seg_a["speakerLabel"] or "") != (seg_b["speakerLabel"] or ""):
        differences.append(
            {
                "category": "SPEAKER_LABEL",
                "detail": f"{seg_a['speakerLabel']!r} vs {seg_b['speakerLabel']!r}",
            }
        )

    if (seg_a["verseMarker"] or "") != (seg_b["verseMarker"] or ""):
        differences.append(
            {
                "category": "VERSE_MARKER",
                "detail": f"{seg_a['verseMarker']!r} vs {seg_b['verseMarker']!r}",
            }
        )
        if ("॥" in (seg_a["verseMarker"] or "")) != ("॥" in (seg_b["verseMarker"] or "")):
            differences.append(
                {
                    "category": "DANDA_STYLE",
                    "detail": "Marker danda style differs between sources",
                }
            )

    words_a = tokenize_words(root_a)
    words_b = tokenize_words(root_b)
    if words_a != words_b:
        if len(words_a) != len(words_b):
            if len(words_a) < len(words_b):
                differences.append(
                    {
                        "category": "MISSING_TEXT",
                        "detail": f"word_count {len(words_a)} vs {len(words_b)}",
                    }
                )
                differences.append(
                    {
                        "category": "EXTRA_TEXT",
                        "detail": f"word_count {len(words_b)} vs {len(words_a)} on alternate source",
                    }
                )
            else:
                differences.append(
                    {
                        "category": "EXTRA_TEXT",
                        "detail": f"word_count {len(words_a)} vs {len(words_b)}",
                    }
                )
                differences.append(
                    {
                        "category": "MISSING_TEXT",
                        "detail": f"word_count {len(words_b)} vs {len(words_a)} on alternate source",
                    }
                )
        folded_a = [fold_approved_orthography(w, rules) for w in words_a]
        folded_b = [fold_approved_orthography(w, rules) for w in words_b]
        if folded_a == folded_b and len(words_a) == len(words_b):
            pairs = [f"{a} vs {b}" for a, b in zip(words_a, words_b) if a != b]
            differences.append(
                {
                    "category": "ORTHOGRAPHY_APPROVED",
                    "detail": "; ".join(pairs) if pairs else "approved orthography fold",
                }
            )
            if "orthography_sanjaya_equivalence" in rules:
                applied.append("orthography_sanjaya_equivalence")
        elif sorted(folded_a) == sorted(folded_b) and folded_a != folded_b:
            differences.append(
                {
                    "category": "WORD_ORDER",
                    "detail": f"{words_a} vs {words_b}",
                }
            )
        else:
            # distinguish unapproved ortho vs word difference
            unapproved = []
            word_diffs = []
            for i in range(max(len(words_a), len(words_b))):
                a = words_a[i] if i < len(words_a) else None
                b = words_b[i] if i < len(words_b) else None
                if a == b:
                    continue
                if a and b and fold_approved_orthography(a, rules) == fold_approved_orthography(b, rules):
                    continue
                if a and b and a != b and unicodedata.normalize("NFC", a) != unicodedata.normalize("NFC", b):
                    # similar length heuristic for unapproved ortho
                    if abs(len(a) - len(b)) <= 2 and a[0] == b[0]:
                        unapproved.append(f"{a} vs {b}")
                    else:
                        word_diffs.append(f"{a} vs {b}")
                else:
                    word_diffs.append(f"{a} vs {b}")
            if unapproved and not word_diffs:
                differences.append(
                    {"category": "ORTHOGRAPHY_UNAPPROVED", "detail": "; ".join(unapproved)}
                )
            if word_diffs:
                differences.append(
                    {"category": "WORD_DIFFERENCE", "detail": "; ".join(word_diffs)}
                )

    if punct_mask(root_a) != punct_mask(root_b):
        differences.append(
            {
                "category": "PUNCTUATION",
                "detail": f"{punct_mask(root_a)!r} vs {punct_mask(root_b)!r}",
            }
        )

    # Segmentation: same (folded) word sequence, different danda placement in root
    folded_chk_a = [fold_approved_orthography(w, rules) for w in tokenize_words(root_a)]
    folded_chk_b = [fold_approved_orthography(w, rules) for w in tokenize_words(root_b)]
    danda_pos = lambda t: [m.start() for m in re.finditer(r"[।॥]", t)]
    if (
        folded_chk_a
        and folded_chk_a == folded_chk_b
        and re.sub(r"[।॥\s]+", "", root_a) == re.sub(r"[।॥\s]+", "", root_b)
        and [root_a.count(c) for c in "।॥"] != [root_b.count(c) for c in "।॥"]
    ) or (
        folded_chk_a == folded_chk_b
        and len(danda_pos(root_a)) == len(danda_pos(root_b))
        and len(danda_pos(root_a)) > 0
        and tokenize_words(root_a[: danda_pos(root_a)[0]] if danda_pos(root_a) else root_a)
        != tokenize_words(root_b[: danda_pos(root_b)[0]] if danda_pos(root_b) else root_b)
    ):
        differences.append(
            {
                "category": "SEGMENTATION",
                "detail": "Danda / pāda segmentation differs with equivalent word inventory",
            }
        )

    # Deduplicate categories preferring first detail
    dedup: dict[str, dict[str, str]] = {}
    for d in differences:
        dedup.setdefault(d["category"], d)
    differences = list(dedup.values())

    exact_match = text_a == text_b
    harmless = set(policy.get("harmlessDifferenceCategories") or [])
    substantive = set(policy.get("substantiveDifferenceCategories") or [])
    cats = {d["category"] for d in differences}

    substantive_hit = bool(cats & substantive)
    folded_root_a = [fold_approved_orthography(w, rules) for w in tokenize_words(root_a)]
    folded_root_b = [fold_approved_orthography(w, rules) for w in tokenize_words(root_b)]
    normalized_roots_equal = folded_root_a == folded_root_b and punct_mask(root_a) == punct_mask(
        root_b
    )
    speakers_equal = (seg_a["speakerLabel"] or "") == (seg_b["speakerLabel"] or "")

    if exact_match:
        classification = "AUTO_MATCH"
        confidence = 1.0
        normalized_match = True
    elif substantive_hit or not normalized_roots_equal or not speakers_equal:
        classification = "SOURCE_CONFLICT"
        confidence = 0.0
        normalized_match = False
    elif not differences and not applied:
        classification = "AUTO_MATCH"
        confidence = 1.0
        normalized_match = True
    else:
        classification = "NORMALIZATION_MATCH"
        confidence = 0.95
        normalized_match = True
        if applied and "orthography_sanjaya_equivalence" not in applied:
            # keep list as-is
            pass

    human_cats = set(policy.get("humanReviewCategories") or [])
    requires_human = (
        bool(cats & human_cats)
        or classification in {"SOURCE_CONFLICT", "INSUFFICIENT_SOURCES"}
    )

    if classification == "SOURCE_CONFLICT":
        recommended = "SOURCE_CONFLICT"
    elif classification == "INSUFFICIENT_SOURCES":
        recommended = "NEEDS_SOURCE"
    else:
        recommended = "READY_FOR_HUMAN_APPROVAL"

    return {
        "classification": classification,
        "confidence": confidence,
        "exactMatch": exact_match,
        "normalizedMatch": normalized_match,
        "substantiveDifference": substantive_hit or classification == "SOURCE_CONFLICT",
        "differences": differences,
        "normalizationRulesApplied": list(dict.fromkeys(applied)),
        "requiresHumanReview": requires_human,
        "recommendedStatus": recommended,
        "segments": {"a": seg_a, "b": seg_b},
        "normalizedRoots": {"a": root_a, "b": root_b},
    }


def sanskrit_sources(record: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for s in record.get("sources") or []:
        text = s.get("sanskritText")
        if isinstance(text, str) and text.strip():
            out.append(s)
    return out


def compare_record(
    record: dict[str, Any],
    *,
    policy: dict[str, Any],
) -> dict[str, Any]:
    chapter = record["chapterNumber"]
    verse = record["verseNumber"]
    ref = record["canonicalReference"]
    sources = sanskrit_sources(record)
    source_ids = [s.get("sourceId") for s in (record.get("sources") or [])]

    if len(sources) < 2:
        return {
            "chapterNumber": chapter,
            "verseNumber": verse,
            "canonicalReference": ref,
            "sourceIds": source_ids,
            "classification": "INSUFFICIENT_SOURCES",
            "confidence": 0.4 if len(sources) == 1 else 0.0,
            "sourceCount": len(sources),
            "comparison": {
                "exactMatch": False,
                "normalizedMatch": False,
                "substantiveDifference": False,
            },
            "differences": [
                {
                    "category": "SOURCE_ERROR" if len(sources) == 0 else "MISSING_TEXT",
                    "detail": f"Need >=2 Sanskrit sources; found {len(sources)}",
                }
            ]
            if len(sources) == 0
            else [
                {
                    "category": "MISSING_TEXT",
                    "detail": "Only one Sanskrit source available for comparison",
                }
            ],
            "normalizationRulesApplied": [],
            "recommendedStatus": "NEEDS_SOURCE",
            "requiresHumanReview": True,
            "engineVersion": ENGINE_VERSION,
        }

    # Pairwise compare first two Sanskrit sources (Phase 2: primary pair)
    a, b = sources[0], sources[1]
    cmp = compare_two_texts(
        a["sanskritText"],
        b["sanskritText"],
        source_id_a=str(a.get("sourceId")),
        source_id_b=str(b.get("sourceId")),
        policy=policy,
    )
    return {
        "chapterNumber": chapter,
        "verseNumber": verse,
        "canonicalReference": ref,
        "sourceIds": source_ids,
        "classification": cmp["classification"],
        "confidence": cmp["confidence"],
        "sourceCount": len(sources),
        "comparison": {
            "exactMatch": cmp["exactMatch"],
            "normalizedMatch": cmp["normalizedMatch"],
            "substantiveDifference": cmp["substantiveDifference"],
        },
        "differences": cmp["differences"],
        "normalizationRulesApplied": cmp["normalizationRulesApplied"],
        "recommendedStatus": cmp["recommendedStatus"],
        "requiresHumanReview": cmp["requiresHumanReview"],
        "engineVersion": ENGINE_VERSION,
    }


def deterministic_audit_sample(
    results: list[dict[str, Any]],
    *,
    policy: dict[str, Any],
) -> dict[str, Any]:
    seed = policy.get("corpusVersionSeed") or "antar-default"
    by_verse = sorted(results, key=lambda r: (r["chapterNumber"], r["verseNumber"]))
    selected: set[str] = set()
    if by_verse:
        selected.add(by_verse[0]["canonicalReference"])
        selected.add(by_verse[-1]["canonicalReference"])

    match_pool = [
        r
        for r in by_verse
        if r["classification"] in {"AUTO_MATCH", "NORMALIZATION_MATCH"}
    ]
    for r in by_verse:
        if r.get("normalizationRulesApplied"):
            selected.add(r["canonicalReference"])

    need = max(1, (len(match_pool) + 9) // 10) if match_pool else 0
    ranked = sorted(
        match_pool,
        key=lambda r: sha256_text(f"{seed}:{r['canonicalReference']}"),
    )
    for r in ranked:
        selected.add(r["canonicalReference"])
        if sum(1 for m in match_pool if m["canonicalReference"] in selected) >= need:
            break

    refs = sorted(selected, key=lambda ref: tuple(map(int, ref.split("."))))
    return {
        "corpusVersionSeed": seed,
        "engineVersion": ENGINE_VERSION,
        "selectedReferences": refs,
        "matchPoolSize": len(match_pool),
        "minimumMatchSample": need,
        "policy": "deterministic_sha256_rank_plus_first_last_plus_normalized",
    }


def update_review_file(
    review_path: Path,
    result: dict[str, Any],
    *,
    audit_selected: bool,
    set_under_review: bool,
) -> bool:
    """Update review markdown with automation block; preserve human notes/decision/approval."""
    if not review_path.is_file():
        return False
    text = review_path.read_text(encoding="utf-8")
    # Never approve
    if result["classification"] == "SOURCE_CONFLICT":
        new_status = "SOURCE_CONFLICT"
    elif result["classification"] == "INSUFFICIENT_SOURCES":
        new_status = "NEEDS_SOURCE"
    elif set_under_review:
        new_status = "UNDER_REVIEW"
    else:
        # keep existing status unless UNREVIEWED
        m = re.search(r"# Status\n\n([A-Z_]+)\n", text)
        current = m.group(1) if m else "UNREVIEWED"
        if current == "UNREVIEWED":
            new_status = "READY_FOR_REVIEW"
        elif current == "APPROVED":
            new_status = current  # never change away automatically toward approve; leave human
        else:
            new_status = current

    if new_status == "APPROVED":
        new_status = "UNDER_REVIEW"  # hard refuse auto-approve

    text2 = re.sub(r"(# Status\n\n)([A-Z_]+)(\n)", rf"\1{new_status}\3", text, count=1)

    auto_block = (
        "\n## Automated Comparison (engine v"
        + ENGINE_VERSION
        + ")\n\n"
        + f"- Classification: `{result['classification']}`\n"
        + f"- Confidence: `{result['confidence']}`\n"
        + f"- Source count: `{result['sourceCount']}`\n"
        + f"- Requires human review: `{result['requiresHumanReview']}`\n"
        + f"- Recommended status: `{result['recommendedStatus']}`\n"
        + f"- Audit sample: `{audit_selected}`\n"
        + f"- Normalization rules: `{', '.join(result.get('normalizationRulesApplied') or []) or 'none'}`\n"
        + "- Differences:\n"
        + (
            "\n".join(
                f"  - `{d['category']}`: {d['detail']}"
                for d in (result.get("differences") or [])
            )
            or "  - none"
        )
        + "\n"
    )
    # Replace previous automation block if present; insert before Decision or after Editorial Notes
    if "## Automated Comparison" in text2:
        def _repl(_match: re.Match[str]) -> str:
            return auto_block + "\n"

        text2 = re.sub(
            r"\n## Automated Comparison \(engine v.*?(?=\n# Decision\n)",
            _repl,
            text2,
            count=1,
            flags=re.S,
        )
    else:
        text2 = text2.replace(
            "\n# Decision\n",
            auto_block + "\n# Decision\n",
            1,
        )

    audit_line = (
        f"- engine-v{ENGINE_VERSION} — Automated comparison: "
        f"{result['classification']} confidence={result['confidence']} "
        f"sources={result['sourceCount']} audit_sample={audit_selected}. "
        f"No approval granted.\n"
    )
    if "# Audit Log\n" in text2:
        # append if not already present for this classification run signature
        sig = f"Automated comparison: {result['classification']} confidence={result['confidence']}"
        if sig not in text2:
            text2 = text2.rstrip() + "\n" + audit_line
    review_path.write_text(text2 if text2.endswith("\n") else text2 + "\n", encoding="utf-8")
    return True


def run_chapter(
    *,
    chapter_dir: Path,
    policy_path: Path,
    reference: str | None,
    update_reviews: bool,
    set_under_review: bool,
) -> dict[str, Any]:
    policy = load_json(policy_path)
    comparison_path = chapter_dir / "source-comparison.jsonl"
    records = load_jsonl(comparison_path)
    if reference:
        records = [r for r in records if r.get("canonicalReference") == reference]
        if not records:
            raise SystemExit(f"No record for {reference}")

    results = [compare_record(r, policy=policy) for r in records]
    results.sort(key=lambda r: (r["chapterNumber"], r["verseNumber"]))

    report_path = chapter_dir / "automated-comparison-report.jsonl"
    write_jsonl(report_path, results)

    sample: dict[str, Any] = {"selectedReferences": []}
    if reference is None:
        sample = deterministic_audit_sample(results, policy=policy)
        selected = set(sample.get("selectedReferences") or [])
        # Policy: every audit-sample Verse requires human review.
        for result in results:
            if result["canonicalReference"] in selected:
                result["requiresHumanReview"] = True
                result["auditSample"] = True
            else:
                result["auditSample"] = False
        write_jsonl(report_path, results)
        (chapter_dir / "audit-sample.json").write_text(
            json.dumps(sample, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        sample_path = chapter_dir / "audit-sample.json"
        if sample_path.is_file():
            sample = load_json(sample_path)

    try:
        report_rel = str(report_path.relative_to(REPO_ROOT))
    except ValueError:
        report_rel = str(report_path)

    run_meta = {
        "engineVersion": ENGINE_VERSION,
        "policyVersion": policy.get("version"),
        "generatedAt": utc_now_iso(),
        "chapterDir": str(chapter_dir),
        "resultCount": len(results),
        "reportPath": report_rel,
        "reportSha256": sha256_text(report_path.read_text(encoding="utf-8")),
    }
    (chapter_dir / "automated-comparison-run-meta.json").write_text(
        json.dumps(run_meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if update_reviews:
        reviews_dir = REPO_ROOT / "content/editorial/reviews"
        selected = set(sample.get("selectedReferences") or [])
        for result in results:
            path = reviews_dir / f"{result['canonicalReference']}.md"
            update_review_file(
                path,
                result,
                audit_selected=result["canonicalReference"] in selected,
                set_under_review=set_under_review,
            )

    # Sync chapter source-comparison status from classifications (never APPROVED).
    if reference is None and comparison_path.is_file():
        by_ref = {r["canonicalReference"]: r for r in results}
        synced = []
        for record in load_jsonl(comparison_path):
            out = dict(record)
            result = by_ref.get(record["canonicalReference"])
            if result:
                cls = result["classification"]
                if cls == "SOURCE_CONFLICT":
                    out["status"] = "SOURCE_CONFLICT"
                elif cls == "INSUFFICIENT_SOURCES":
                    out["status"] = "SOURCE_MISSING"
                elif out.get("status") not in {"UNDER_REVIEW", "SOURCE_CONFLICT", "SOURCE_MISSING"}:
                    out["status"] = "READY_FOR_REVIEW"
                if out.get("status") == "APPROVED":
                    out["status"] = "READY_FOR_REVIEW"
            synced.append(out)
        write_jsonl(comparison_path, synced)

    return {"results": results, "sample": sample, "runMeta": run_meta, "reportPath": report_path}


def write_summary(chapter_dir: Path, results: list[dict[str, Any]], sample: dict[str, Any]) -> None:
    from collections import Counter

    classifications = Counter(r["classification"] for r in results)
    source_counts = Counter(r["sourceCount"] for r in results)
    rule_usage: Counter[str] = Counter()
    for r in results:
        for rule in r.get("normalizationRulesApplied") or []:
            rule_usage[rule] += 1
    human = [r["canonicalReference"] for r in results if r.get("requiresHumanReview")]
    conflicts = [r["canonicalReference"] for r in results if r["classification"] == "SOURCE_CONFLICT"]
    insufficient = [
        r["canonicalReference"] for r in results if r["classification"] == "INSUFFICIENT_SOURCES"
    ]

    lines = [
        "# Chapter 1 automated review summary",
        "",
        "**Automated comparison is not scholarly approval.**",
        "",
        f"- Engine version: `{ENGINE_VERSION}`",
        f"- Total identities: `{len(results)}`",
        f"- Source-count distribution: `{dict(source_counts)}`",
        f"- Classification counts: `{dict(classifications)}`",
        f"- Normalization-rule usage: `{dict(rule_usage)}`",
        f"- Conflicts: `{conflicts or 'none'}`",
        f"- Insufficient-source records: `{len(insufficient)}` (`{', '.join(insufficient[:10])}{'…' if len(insufficient)>10 else ''}`)",
        f"- Audit-sample references: `{sample.get('selectedReferences')}`",
        f"- Human reviews required: `{len(human)}`",
        "",
        "## Recommended next acquisition work",
        "",
        "- Resolve `SOURCE_CONFLICT` Verses with human editorial review (do not auto-approve).",
        "- Prefer additional independent scholarly witnesses where orthography remains disputed.",
        "- Keep IIT / verification-only sources out of canonical import.",
        "",
        "## Notes",
        "",
        "- No Verse was auto-approved.",
        "- Canonical draft was not modified by this engine.",
        "",
    ]
    (chapter_dir / "automated-review-summary.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Antar automated editorial comparison engine")
    parser.add_argument("--chapter-dir", type=Path, default=DEFAULT_CHAPTER_DIR)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--reference", help="Optional single reference like 1.1")
    parser.add_argument("--update-reviews", action="store_true")
    parser.add_argument(
        "--set-under-review",
        action="store_true",
        help="When updating reviews, allow READY_FOR_REVIEW → UNDER_REVIEW",
    )
    args = parser.parse_args(argv)

    outcome = run_chapter(
        chapter_dir=args.chapter_dir,
        policy_path=args.policy,
        reference=args.reference,
        update_reviews=args.update_reviews,
        set_under_review=args.set_under_review,
    )
    if args.reference is None:
        write_summary(args.chapter_dir, outcome["results"], outcome["sample"])
    print(
        json.dumps(
            {
                "resultCount": len(outcome["results"]),
                "reportPath": str(outcome["reportPath"]),
                "reportSha256": outcome["runMeta"]["reportSha256"],
                "classifications": {
                    k: sum(1 for r in outcome["results"] if r["classification"] == k)
                    for k in sorted(CLASSIFICATIONS)
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
