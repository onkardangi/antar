#!/usr/bin/env python3
"""Build / refresh Besant & Das 1905 Chapter 1 Translation editorial workspace.

Stdlib only. Does not modify content/raw/. Does not build packages or import.

Pin authority:
  content/raw/translations/besant-das-1905/bhagavadgitawith00londiala.pdf
  SHA-256 7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115

Fluent English transcribed from IA IIIF page images of the pinned item
(scanLeaf = 46 + printedPage). OCR used only as a locator aid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SOURCE_ID = "bhagavad-gita-translation-en-besant-das-1905-v1"
SOURCE_CHECKSUM = (
    "7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115"
)
PROVIDER = "Annie Besant & Bhagavan Das"
CHAPTER = 1
WORKSPACE = Path("content/translation-editorial/besant-das-1905/chapter-01")

COMMON_EXCL = (
    "Excluded Sanskrit/Devanagari, word-by-word gloss, footnotes, page numbers, "
    "and running headers."
)
COMMON_SCAN = (
    "Fluent English transcribed from pinned IA page image "
    "(IIIF leaf of bhagavadgitawith00londiala)."
)


def scan_leaf(printed: int) -> int:
    return 46 + printed


def seg_id(verse: int) -> str:
    return f"besant-das-1905-bg-1-{verse:03d}"


def unit(
    verse: int,
    *,
    label: str,
    text: str,
    printed: int,
    status: str = "UNREVIEWED",
    extraction_notes: list[str] | None = None,
    commentary_notes: list[str] | None = None,
    editorial_notes: list[str] | None = None,
    review_flags: list[str] | None = None,
) -> dict[str, Any]:
    notes = list(extraction_notes or [])
    notes.insert(0, COMMON_SCAN)
    return {
        "segmentId": seg_id(verse),
        "chapterNumber": CHAPTER,
        "coveredVerseNumbers": [verse],
        "coveredCanonicalReferences": [f"{CHAPTER}.{verse}"],
        "sourceLabel": label,
        "translationText": text,
        "language": "en",
        "provider": PROVIDER,
        "sourceId": SOURCE_ID,
        "sourceChecksum": SOURCE_CHECKSUM,
        "sourceRole": "PRIMARY_TRANSLATION_CANDIDATE",
        "sourcePage": {"printed": printed, "scanLeaf": scan_leaf(printed)},
        "publicationStatus": status,
        "editorialNotes": editorial_notes or [],
        "reviewFlags": review_flags or [],
        "contentVersion": 1,
        "extractionNotes": notes,
        "commentarySeparationNotes": commentary_notes or [COMMON_EXCL],
    }


def chapter01_units() -> list[dict[str, Any]]:
    """Ordered 1→1 publisher free-translation units for Chapter 1."""
    # Texts are publisher-faithful transcriptions from page images.
    # Soft hyphenation across line breaks is joined; hard hyphens retained.
    # Footnote superscript markers are omitted from translationText.
    return [
        unit(
            1,
            label="॥ १ ॥",
            printed=1,
            text=(
                "Dhritarâshtra said :\n"
                "On the holy plain, on the field of Kuru, gathered together, "
                "eager for battle, what did they, O Sañjaya, my people and the "
                "Pândavas?"
            ),
            extraction_notes=[
                "Arabic (1) absent from fluent block; identity from Sanskrit ॥ १ ॥.",
                "English speaker attribution retained as printed before free translation "
                "(same convention as Swarupananda Chapter 1 drafts).",
            ],
            review_flags=["LABEL_QUIRK_NO_ARABIC", "SPEAKER_ATTRIBUTION"],
        ),
        unit(
            2,
            label="(2)",
            printed=2,
            text=(
                "Sañjaya said :\n"
                "Having seen arrayed the army of the Pândavas, the Râjâ Duryodhana "
                "approached his teacher, and spake these words :"
            ),
            extraction_notes=[
                "Footnote superscript after 'teacher' omitted from translationText.",
            ],
            review_flags=["SPEAKER_ATTRIBUTION", "FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            3,
            label="(3)",
            printed=2,
            text=(
                "Behold this mighty host of the sons of Pându, O teacher, arrayed by "
                "the son of Drupada, thy wise disciple."
            ),
        ),
        unit(
            4,
            label="(4)",
            printed=2,
            text=(
                "Heroes are these, mighty bowmen, to Bhîma and Arjuna equal in battle ; "
                "Yuyudhâna, Virâta, and Drupada of the great car :"
            ),
            extraction_notes=[
                "Footnote superscript after 'car' omitted from translationText.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            5,
            label="(5)",
            printed=3,
            text=(
                "Dhrishtaketu, Chekitâna, and the valiant Râjâ of Kâshî ; Purujit and "
                "Kuntibhoja, and Shaibya, bull among men ;"
            ),
            extraction_notes=[
                "Footnote superscript after 'bull' omitted from translationText.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED", "DIACRITIC_COMPLEXITY"],
        ),
        unit(
            6,
            label="(6)",
            printed=3,
            text=(
                "Yudhâmanyu the strong, and Uttamaujâ the brave ; Saubhadra and the "
                "Draupadeyas, all of great cars."
            ),
            extraction_notes=[
                "Footnote superscript after 'Draupadeyas' omitted from translationText.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            7,
            label="(7)",
            printed=4,
            text=(
                "Know further all those who are our chiefs, O best of the twice-born, "
                "the leaders of my army ; these I name to thee for thy information :"
            ),
        ),
        unit(
            8,
            label="(8)",
            printed=4,
            text=(
                "Thou, lord and Bhîshma, and Karna, and Kripa, conquering in battle ; "
                "Ashvatthâmâ, Vikarna, and Saumadatti also ;"
            ),
            extraction_notes=[
                "Footnote superscript after 'Saumadatti' omitted from translationText.",
                "Underdot diacritics on Karna/Kripa/Vikarna simplified where page-image "
                "vision was ambiguous; flagged for human diacritic check.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED", "DIACRITIC_COMPLEXITY"],
        ),
        unit(
            9,
            label="(9)",
            printed=5,
            text=(
                "And many others, heroes, for my sake renouncing their lives, with "
                "divers weapons and missiles, and all well-skilled in war."
            ),
        ),
        unit(
            10,
            label="(10)",
            printed=5,
            text=(
                "Yet insufficient seems this army of ours, though marshalled by "
                "Bhîshma, while that army of theirs seems sufficient, though "
                "marshalled by Bhîma;"
            ),
            extraction_notes=[
                "Footnote superscript after 'Bhîma' omitted from translationText.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            11,
            label="(11)",
            printed=5,
            text=(
                "Therefore in the rank and file let all, standing firmly in their "
                "respective divisions, guard Bhîshma, even all ye Generals."
            ),
            extraction_notes=[
                "Closing quotation mark after Generals is uncertain on page image "
                "(OCR lacks it; one IIIF reading suggested a closing quote). Period "
                "retained without quote pending human confirmation.",
            ],
            review_flags=["QUOTATION_MARK_UNCERTAIN"],
        ),
        unit(
            12,
            label="(12)",
            printed=6,
            text=(
                "To enhearten him, the Ancient of the Kurus, the Grandsire, the "
                "glorious, blew his conch, sounding on high a lion's roar."
            ),
        ),
        unit(
            13,
            label="(13)",
            printed=6,
            text=(
                "Then conches and kettledrums, tabors and drums and cowhorns suddenly "
                "blared forth, and the sound was tumultuous."
            ),
        ),
        unit(
            14,
            label="(14)",
            printed=7,
            text=(
                "Then, stationed in their great war-chariot, yoked to white horses, "
                "Mâdhava and the son of Pându blew their divine conches,"
            ),
            extraction_notes=[
                "Footnote superscripts after Mâdhava and 'son of Pându' omitted.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            15,
            label="(15)",
            printed=7,
            text=(
                "Pânchajanya by Hrishîkesha, and Devadatta by Dhananjaya. Vrikodara, "
                "of terrible deeds, blew his mighty conch, Paundra ;"
            ),
            extraction_notes=[
                "Footnote superscripts after Dhananjaya and Vrikodara omitted.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            16,
            label="(16)",
            printed=8,
            text=(
                "The Râjâ Yudhishthira, the son of Kuntî, blew Anantavijaya ; Nakula "
                "and Sahadeva, Sughosha and Manipushpaka."
            ),
            extraction_notes=[
                "Footnote superscript after Manipushpaka omitted.",
                "Diacritics on Yudhishthira/Sughosha/Manipushpaka flagged for check.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED", "DIACRITIC_COMPLEXITY"],
        ),
        unit(
            17,
            label="(17)",
            printed=8,
            text=(
                "And Kâshya, of the great bow, and Shikhandî, the mighty car-warrior, "
                "Dhrishtadyumna and Virâta and Sâtyaki, the unconquered."
            ),
            extraction_notes=[
                "Footnote superscript after Kâshya omitted.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED", "DIACRITIC_COMPLEXITY"],
        ),
        unit(
            18,
            label="(18)",
            printed=8,
            text=(
                "Drupada and the Draupadeyas, O Lord of earth, and Saubhadra, the "
                "mighty-armed, on all sides their several conches blew."
            ),
        ),
        unit(
            19,
            label="(19)",
            printed=9,
            text=(
                "That tumultuous uproar rent the hearts of the sons of Dhritarâshtra, "
                "filling the earth and sky with sound."
            ),
        ),
        unit(
            20,
            label="(20)",
            printed=9,
            text=(
                "Then, beholding the sons of Dhritarâshtra standing arrayed, and the "
                "flight of missiles about to begin, he whose crest is an ape, the son "
                "of Pându, took up his bow,"
            ),
            extraction_notes=[
                "Sentence continues into 1.21 on printed page 10 ('And spake this "
                "word...'). Publisher places (20) at end of this page's fluent block.",
            ],
            review_flags=["CROSS_PAGE_CONTINUATION"],
        ),
        unit(
            21,
            label="(21)",
            printed=10,
            text=(
                "And spake this word to Hrishîkesha, O Lord of earth:\n"
                "Arjuna said :\n"
                '"In the midst, between the two armies, stay my chariot, O Achyuta,'
            ),
            extraction_notes=[
                "Includes Sanjaya continuation of 1.20 sense plus Arjuna speech under "
                "publisher label (21).",
                "Opening quotation retained; speech continues through 1.22–1.23.",
            ],
            review_flags=[
                "SPEAKER_ATTRIBUTION",
                "CROSS_PAGE_CONTINUATION",
                "OPEN_QUOTATION_CONTINUES",
            ],
        ),
        unit(
            22,
            label="(22)",
            printed=10,
            text=(
                "That I may behold these standing, longing for battle, with whom I "
                "must strive in this out-breaking war ;"
            ),
            review_flags=["OPEN_QUOTATION_CONTINUES"],
        ),
        unit(
            23,
            label="(23)",
            printed=11,
            text=(
                "And gaze on those here gathered together, ready to fight, desirous of "
                "pleasing in battle the evil-minded son of Dhritarâshtra."
            ),
            extraction_notes=[
                "Closing of Arjuna quotation may fall at end of 1.23; confirm quote "
                "closure on page image during review.",
            ],
            review_flags=["QUOTATION_MARK_UNCERTAIN"],
        ),
        unit(
            24,
            label="(24)",
            printed=11,
            text=(
                "Sañjaya said :\n"
                "Thus addressed by Gudâkesha, Hrishîkesha, O Bhârata, having stayed "
                "that best of chariots in the midst, between the two armies,"
            ),
            extraction_notes=[
                "Footnote superscript after Gudâkesha omitted.",
            ],
            review_flags=[
                "SPEAKER_ATTRIBUTION",
                "FOOTNOTE_MARKER_STRIPPED",
                "DIACRITIC_COMPLEXITY",
            ],
        ),
        unit(
            25,
            label="(25)",
            printed=12,
            text=(
                'Over against Bhîshma, Drona and all the rulers of the world, said : '
                '"O Pârtha, behold these Kurus gathered together."'
            ),
        ),
        unit(
            26,
            label="(26)",
            printed=12,
            text=(
                "Then saw Pârtha standing there uncles and grandfathers, teachers, "
                "mother's brothers, cousins, sons and grandsons, comrades,"
            ),
            extraction_notes=[
                "Soft hyphen grand-fathers joined as grandfathers.",
            ],
        ),
        unit(
            27,
            label="(27)",
            printed=13,
            text=(
                "Fathers-in-law and friends also in both armies. Seeing all these "
                "kinsmen, thus standing arrayed, Kaunteya,"
            ),
            extraction_notes=[
                "Fluent spans printed pages 12–13; recorded on completion page 13.",
                "Footnote superscript after Kaunteya omitted.",
                "Soft hyphen Kaun-teya joined as Kaunteya.",
            ],
            review_flags=["CROSS_PAGE_CONTINUATION", "FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            28,
            label="॥ २८ ॥",
            printed=13,
            text=(
                "Deeply moved to pity, this uttered in sadness :\n"
                "Arjuna said :\n"
                "Seeing these, my kinsmen, O Krishna, arrayed eager to fight,"
            ),
            extraction_notes=[
                "Arabic (28) absent from fluent block; identity from Sanskrit ॥ २८ ॥.",
                "Speaker attribution retained mid-unit as printed.",
            ],
            review_flags=["LABEL_QUIRK_NO_ARABIC", "SPEAKER_ATTRIBUTION"],
        ),
        unit(
            29,
            label="(29)",
            printed=13,
            text=(
                "My limbs fail and my mouth is parched, my body quivers, and my hair "
                "stands on end,"
            ),
        ),
        unit(
            30,
            label="(30)",
            printed=14,
            text=(
                "Gândîva slips from my hand, and my skin burns all over ; I am not "
                "able to stand, and my mind is whirling,"
            ),
            review_flags=["DIACRITIC_COMPLEXITY"],
        ),
        unit(
            31,
            label="(31)",
            printed=14,
            text=(
                "And I see adverse omens, O Keshava. Nor do I foresee any advantage "
                "from slaying kinsmen in battle."
            ),
            extraction_notes=[
                "Footnote superscript after Keshava omitted.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            32,
            label="(32)",
            printed=15,
            text=(
                "For I desire not victory, O Krishna, nor kingdom, nor pleasures ; "
                "what is kingdom to us, O Govinda, what enjoyment, or even life ?"
            ),
        ),
        unit(
            33,
            label="॥ ३३ ॥",
            printed=15,
            text=(
                "Those for whose sake we desire kingdom, enjoyments and pleasures, "
                "they stand here in battle, abandoning life and riches—"
            ),
            extraction_notes=[
                "Arabic (33) absent from fluent block; identity from Sanskrit ॥ ३३ ॥.",
                "Ends with em-dash continuing into 1.34 list.",
            ],
            review_flags=["LABEL_QUIRK_NO_ARABIC", "CROSS_PAGE_CONTINUATION"],
        ),
        unit(
            34,
            label="(34)",
            printed=16,
            text=(
                "Teachers, fathers, sons, as well as grandfathers, mother's brothers, "
                "fathers-in-law, grandsons, brothers-in-law, and other relatives."
            ),
            extraction_notes=[
                "Fluent starts on printed page 15; completes with (34) on page 16.",
            ],
            review_flags=["CROSS_PAGE_CONTINUATION"],
        ),
        unit(
            35,
            label="(35)",
            printed=16,
            text=(
                "These I do not wish to kill, though myself slain, O Madhusûdana, even "
                "for the sake of the kingship of the three worlds; how then for earth?"
            ),
            review_flags=["DIACRITIC_COMPLEXITY"],
        ),
        unit(
            36,
            label="(36)",
            printed=16,
            text=(
                "Slaying these sons of Dhritarâshtra, what pleasure can be ours, O "
                "Janârdana? killing these desperadoes sin will but take hold of us."
            ),
            extraction_notes=[
                "Footnote superscript after Janârdana omitted.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            37,
            label="(37)",
            printed=17,
            text=(
                "Therefore we should not kill the sons of Dhritarâshtra, our "
                "relatives ; for how, killing our kinsmen, may we be happy, O "
                "Mâdhava ?"
            ),
            extraction_notes=[
                "Soft hyphen Dhritarâ-shtra joined as Dhritarâshtra.",
            ],
        ),
        unit(
            38,
            label="(38)",
            printed=17,
            text=(
                "Although these, with intelligence overpowered by greed, see no guilt "
                "in the destruction of a family, no crime in hostility to friends,"
            ),
        ),
        unit(
            39,
            label="(39)",
            printed=18,
            text=(
                "Why should not we learn to turn away from such a sin, O Janârdana, "
                "who see the evils in the destruction of a family?"
            ),
        ),
        unit(
            40,
            label="(40)",
            printed=18,
            text=(
                "In the destruction of a family the immemorial family traditions "
                "perish ; in the perishing of traditions lawlessness overcomes the "
                "whole family ;"
            ),
            extraction_notes=[
                "Footnote superscript after 'traditions' omitted.",
                "Soft hyphen fami-ly joined as family.",
            ],
            review_flags=["FOOTNOTE_MARKER_STRIPPED"],
        ),
        unit(
            41,
            label="(41)",
            printed=19,
            text=(
                "Owing to predominance of lawlessness, O Krishna, the women of the "
                "family become corrupt; women corrupted, O Vârshneya, there ariseth "
                "caste-confusion;"
            ),
            review_flags=["DIACRITIC_COMPLEXITY"],
        ),
        unit(
            42,
            label="(42)",
            printed=19,
            text=(
                "This confusion draggeth to hell the slayers of the family and the "
                "family ; for their ancestors fall, deprived of rice-balls and "
                "libations."
            ),
        ),
        unit(
            43,
            label="(43)",
            printed=20,
            text=(
                "By these caste-confusing misdeeds of the slayers of the family, the "
                "everlasting caste customs and family customs are abolished."
            ),
            extraction_notes=[
                "Sanskrit on page 19; fluent completes with (43) on page 20.",
            ],
            review_flags=["CROSS_PAGE_CONTINUATION"],
        ),
        unit(
            44,
            label="(44)",
            printed=20,
            text=(
                "The abode of the men whose family customs are extinguished, O "
                "Janârdana, is everlastingly in hell. Thus have we heard."
            ),
            extraction_notes=[
                "Janârdana appears italicized in print; italics not encoded in plain "
                "translationText (presentation deferred).",
            ],
            review_flags=["ITALICS_PRESENTATION_DEFERRED"],
        ),
        unit(
            45,
            label="(45)",
            printed=20,
            text=(
                "Alas! in committing a great sin are we engaged, we who are "
                "endeavouring to kill our kindred from greed of the pleasures of "
                "kingship."
            ),
        ),
        unit(
            46,
            label="(46)",
            printed=21,
            text=(
                "If the sons of Dhritarâshtra, weapon-in-hand, should slay me, "
                "unresisting, unarmed, in the battle, that would for me be the better."
            ),
        ),
        unit(
            47,
            label="(47)",
            printed=21,
            text=(
                "Sañjaya said :\n"
                "Having thus spoken on the battle-field, Arjuna sank down on the seat "
                "of the chariot, casting away his bow and arrow, his mind overborne by "
                "grief."
            ),
            review_flags=["SPEAKER_ATTRIBUTION"],
        ),
    ]


def dumps_jsonl(rows: list[dict[str, Any]]) -> str:
    lines = []
    for row in rows:
        # Deterministic key order via sort_keys on each object.
        lines.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return "\n".join(lines) + "\n"


def build_coverage(units: list[dict[str, Any]]) -> dict[str, Any]:
    vmap = {}
    for u in units:
        for ref in u["coveredCanonicalReferences"]:
            vmap[ref] = u["segmentId"]
    flagged = [
        {
            "segmentId": u["segmentId"],
            "canonicalReference": u["coveredCanonicalReferences"][0],
            "reviewFlags": u.get("reviewFlags") or [],
        }
        for u in units
        if u.get("reviewFlags")
    ]
    return {
        "chapterNumber": CHAPTER,
        "expectedVerseCount": 47,
        "segmentCount": len(units),
        "oneToOneSegmentCount": len(units),
        "multiVerseSegmentCount": 0,
        "combinedLabelInventory": [],
        "verseToSegment": vmap,
        "segmentsWithMultiVerseCoverage": [],
        "uncoveredVerses": [],
        "multiplyCoveredVerses": [],
        "packageReady": False,
        "importReady": False,
        "packageFormatV1Compatible": True,
        "packageFormatV1CompatibilityReason": (
            "All 47 Chapter 1 units are ONE_TO_ONE; Package Format v1 can represent "
            "them faithfully after editorial approval."
        ),
        "sourceId": SOURCE_ID,
        "sourceChecksum": SOURCE_CHECKSUM,
        "provider": PROVIDER,
        "status": "DRAFT_UNREVIEWED",
        "reviewFlagInventory": flagged,
        "approvedCount": 0,
    }


def write_workspace(workspace: Path) -> dict[str, str]:
    workspace.mkdir(parents=True, exist_ok=True)
    units = chapter01_units()
    assert len(units) == 47

    # segment-draft mirrors Swarupananda schema (validator expects these fields).
    segment_rows = []
    extraction_rows = []
    for u in units:
        seg = {k: v for k, v in u.items() if k not in ("extractionNotes", "commentarySeparationNotes")}
        # Keep reviewFlags on segment-draft for review support.
        segment_rows.append(seg)
        extraction_rows.append(
            {
                "chapterNumber": CHAPTER,
                "coveredVerseNumbers": u["coveredVerseNumbers"],
                "segmentId": u["segmentId"],
                "sourceId": SOURCE_ID,
                "sourceChecksum": SOURCE_CHECKSUM,
                "sourceLabel": u["sourceLabel"],
                "sourcePage": u["sourcePage"],
                "sourceRole": u["sourceRole"],
                "publicationStatus": u["publicationStatus"],
                "translationText": u["translationText"],
                "reviewFlags": u.get("reviewFlags") or [],
                "extractionNotes": u.get("extractionNotes") or [],
                "commentarySeparationNotes": u.get("commentarySeparationNotes") or [],
            }
        )

    coverage = build_coverage(units)
    artifacts = {
        "segment-draft.jsonl": dumps_jsonl(segment_rows),
        "source-extraction.jsonl": dumps_jsonl(extraction_rows),
        "coverage-map.json": json.dumps(coverage, indent=2, sort_keys=True) + "\n",
    }

    hashes = {}
    for name, body in artifacts.items():
        path = workspace / name
        data = body.encode("utf-8")
        path.write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()

    sums = workspace / "SHA256SUMS"
    sums.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items())),
        encoding="utf-8",
    )
    return hashes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=WORKSPACE,
        help="Editorial workspace directory",
    )
    args = parser.parse_args(argv)
    hashes = write_workspace(args.workspace)
    print(
        json.dumps(
            {
                "status": "ok",
                "workspace": str(args.workspace),
                "segmentCount": 47,
                "hashes": hashes,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
