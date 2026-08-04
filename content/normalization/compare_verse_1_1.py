#!/usr/bin/env python3
"""Comparison-only normalization and Verse 1.1 Wikisource/IIT diff helpers.

Does not modify source extractions or invent Sanskrit.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from typing import Any


VERSE_MARKER_WS = re.compile(r"॥\s*[०-९0-9]+\s*[-–—.]\s*[०-९0-9]+\s*॥")
VERSE_MARKER_IIT = re.compile(r"।{1,2}\s*[०-९0-9]+\s*[.।-]\s*[०-९0-9]+\s*।{0,2}")
SPEAKER_RE = re.compile(r"^(.+?उवाच)\s*$")


def comparison_normalize(text: str) -> tuple[str, list[str]]:
    """Deterministic comparison-only normalization."""
    changes: list[str] = []
    original = text
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text != original and ("\r" in original):
        changes.append("line_endings_to_LF")

    nfc = unicodedata.normalize("NFC", text)
    if nfc != text:
        changes.append("unicode_nfc")
        text = nfc

    stripped = text.strip()
    if stripped != text:
        changes.append("trimmed_surrounding_whitespace")
        text = stripped

    # Collapse purely structural blank lines / trailing spaces per line.
    lines = [re.sub(r"[ \t]+$", "", ln) for ln in text.split("\n")]
    collapsed: list[str] = []
    blank_run = 0
    for ln in lines:
        if ln.strip() == "":
            blank_run += 1
            if blank_run == 1:
                collapsed.append("")
            else:
                continue
        else:
            blank_run = 0
            # collapse internal runs of spaces/tabs only (not newlines)
            new_ln = re.sub(r"[ \t]{2,}", " ", ln)
            if new_ln != ln:
                changes.append("collapsed_horizontal_whitespace")
            collapsed.append(new_ln)
    text2 = "\n".join(collapsed).strip("\n")
    if text2 != text:
        if "collapsed_horizontal_whitespace" not in changes and text2 != text:
            changes.append("collapsed_structural_blank_lines")
        text = text2

    # Documented danda spacing normalization for comparison only:
    # remove spaces immediately before danda characters.
    spaced = re.sub(r"[ \t]+([।॥])", r"\1", text)
    if spaced != text:
        changes.append("removed_spaces_before_danda_for_comparison")
        text = spaced

    return text, list(dict.fromkeys(changes))  # stable unique


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class WikisourceBoundaries:
    front_matter: str
    speaker_label: str | None
    root_verse_body: str
    verse_marker: str | None
    full_text: str


def split_wikisource_1_1(full_text: str) -> WikisourceBoundaries:
    """Identify front matter / speaker / root body / marker without mutating source."""
    text, _ = comparison_normalize(full_text)
    marker_match = VERSE_MARKER_WS.search(text)
    marker = marker_match.group(0) if marker_match else None
    body = text[: marker_match.start()].rstrip() if marker_match else text

    lines = body.split("\n")
    # Front matter: lines before speaker label ending with उवाच
    speaker_idx = None
    for i, ln in enumerate(lines):
        if SPEAKER_RE.match(ln.strip()):
            speaker_idx = i
            break
    if speaker_idx is None:
        return WikisourceBoundaries(
            front_matter="",
            speaker_label=None,
            root_verse_body=body,
            verse_marker=marker,
            full_text=full_text,
        )
    front = "\n".join(lines[:speaker_idx]).strip("\n")
    speaker = lines[speaker_idx].strip()
    root = "\n".join(lines[speaker_idx + 1 :]).strip("\n")
    return WikisourceBoundaries(
        front_matter=front,
        speaker_label=speaker,
        root_verse_body=root,
        verse_marker=marker,
        full_text=full_text,
    )


@dataclass
class IitkBoundaries:
    speaker_label: str | None
    root_verse_body: str
    verse_marker: str | None
    full_text: str
    front_matter: str = ""


def split_iitk_1_1(full_text: str) -> IitkBoundaries:
    text, _ = comparison_normalize(full_text)
    # IIT marker form ।।1.1।।
    marker_match = re.search(r"।{2}\s*1\s*\.\s*1\s*।{2}", text)
    if not marker_match:
        marker_match = VERSE_MARKER_IIT.search(text)
    marker = marker_match.group(0) if marker_match else None
    body = text[: marker_match.start()].rstrip() if marker_match else text
    lines = [ln for ln in body.split("\n")]
    speaker_idx = None
    for i, ln in enumerate(lines):
        if SPEAKER_RE.match(ln.strip()):
            speaker_idx = i
            break
    if speaker_idx is None:
        return IitkBoundaries(
            speaker_label=None,
            root_verse_body=body.strip("\n"),
            verse_marker=marker,
            full_text=full_text,
        )
    speaker = lines[speaker_idx].strip()
    root = "\n".join(lines[speaker_idx + 1 :]).strip("\n")
    return IitkBoundaries(
        speaker_label=speaker,
        root_verse_body=root,
        verse_marker=marker,
        full_text=full_text,
        front_matter="",
    )


def tokenize_words(text: str) -> list[str]:
    # Split on whitespace and danda/punctuation, keep Devanagari words.
    parts = re.findall(r"[\u0900-\u097F]+", text)
    return parts


def fold_nasal_orthography(word: str) -> str:
    """Fold common anusvara vs explicit-nasal orthography for comparison."""
    return word.replace("ञ्", "ं").replace("न्", "ं").replace("ण्", "ं").replace("म्", "ं")


def ws_words_equal_ignoring_nasal(a: str, b: str) -> bool:
    wa = [fold_nasal_orthography(w) for w in tokenize_words(a)]
    wb = [fold_nasal_orthography(w) for w in tokenize_words(b)]
    return wa == wb


def compare_verse_1_1(wikisource_full: str, iitk_full: str) -> dict[str, Any]:
    ws = split_wikisource_1_1(wikisource_full)
    iit = split_iitk_1_1(iitk_full)

    ws_root_norm, ws_ops = comparison_normalize(ws.root_verse_body)
    iit_root_norm, iit_ops = comparison_normalize(iit.root_verse_body)
    # Extra comparison step: collapse remaining structural blank lines between pādas.
    ws_root_cmp = re.sub(r"\n+", "\n", ws_root_norm).strip()
    iit_root_cmp = re.sub(r"\n+", "\n", iit_root_norm).strip()
    if ws_root_cmp != ws_root_norm:
        ws_ops = list(ws_ops) + ["collapsed_all_blank_lines_between_padas_for_comparison"]
    if iit_root_cmp != iit_root_norm:
        iit_ops = list(iit_ops) + ["collapsed_all_blank_lines_between_padas_for_comparison"]

    differences: list[dict[str, str]] = []

    if ws.front_matter.strip():
        differences.append(
            {
                "category": "front_matter",
                "detail": (
                    "Wikisource poem includes pre-Verse front matter; "
                    "IIT mool block has none."
                ),
            }
        )

    if (ws.speaker_label or "") != (iit.speaker_label or ""):
        differences.append(
            {
                "category": "speaker_label",
                "detail": f"Wikisource={ws.speaker_label!r} IIT={iit.speaker_label!r}",
            }
        )

    if (ws.verse_marker or "") != (iit.verse_marker or ""):
        differences.append(
            {
                "category": "verse_marker",
                "detail": f"Wikisource={ws.verse_marker!r} IIT={iit.verse_marker!r}",
            }
        )

    if "\n\n" in iit_root_norm and "\n\n" not in ws_root_norm:
        differences.append(
            {
                "category": "whitespace",
                "detail": "IIT root retains a blank line between pādas; Wikisource does not.",
            }
        )

    ws_words = tokenize_words(ws_root_cmp)
    iit_words = tokenize_words(iit_root_cmp)
    if ws_words != iit_words:
        ortho = []
        word_diffs = []
        limit = max(len(ws_words), len(iit_words))
        for i in range(limit):
            a = ws_words[i] if i < len(ws_words) else None
            b = iit_words[i] if i < len(iit_words) else None
            if a == b:
                continue
            if a is not None and b is not None and fold_nasal_orthography(a) == fold_nasal_orthography(b):
                ortho.append(f"{a} vs {b}")
            else:
                word_diffs.append(f"{a} vs {b}")
        if word_diffs:
            differences.append({"category": "words", "detail": "; ".join(word_diffs)})
        if ortho:
            differences.append({"category": "orthography", "detail": "; ".join(ortho)})

    def punct_mask(s: str) -> str:
        return re.sub(r"[\u0900-\u097F\s]+", "", s)

    if punct_mask(ws_root_cmp) != punct_mask(iit_root_cmp):
        differences.append(
            {
                "category": "punctuation",
                "detail": (
                    f"Wikisource punct={punct_mask(ws_root_cmp)!r} "
                    f"IIT punct={punct_mask(iit_root_cmp)!r}"
                ),
            }
        )

    # Danda style note if double vs single appears in markers (already covered) or roots.
    if ("॥" in (ws.verse_marker or "")) != ("॥" in (iit.verse_marker or "")):
        differences.append(
            {
                "category": "danda_style",
                "detail": "Wikisource uses double-danda verse markers; IIT uses doubled single-danda ASCII-digit markers.",
            }
        )

    substantive = [d for d in differences if d["category"] in {"words", "substantive_textual_difference"}]
    roots_match = ws_words_equal_ignoring_nasal(ws_root_cmp, iit_root_cmp) and punct_mask(
        ws_root_cmp
    ) == punct_mask(iit_root_cmp)
    speakers_match = (ws.speaker_label or "") == (iit.speaker_label or "")

    if substantive:
        result = "SOURCE_CONFLICT"
    elif roots_match and speakers_match:
        result = "TEXT_MATCH_AFTER_DOCUMENTED_NORMALIZATION"
    else:
        result = "SOURCE_CONFLICT"

    return {
        "result": result,
        "wikisourceBoundaries": {
            "frontMatter": ws.front_matter,
            "speakerLabel": ws.speaker_label,
            "rootVerseBody": ws.root_verse_body,
            "verseMarker": ws.verse_marker,
        },
        "iitkBoundaries": {
            "frontMatter": iit.front_matter,
            "speakerLabel": iit.speaker_label,
            "rootVerseBody": iit.root_verse_body,
            "verseMarker": iit.verse_marker,
        },
        "comparisonNormalized": {
            "wikisourceRoot": ws_root_cmp,
            "iitkRoot": iit_root_cmp,
            "wikisourceRootChecksum": sha256_text(ws_root_cmp),
            "iitkRootChecksum": sha256_text(iit_root_cmp),
            "wikisourceOps": list(dict.fromkeys(ws_ops)),
            "iitkOps": list(dict.fromkeys(iit_ops)),
        },
        "differences": differences,
    }
