#!/usr/bin/env python3
"""Build / refresh Swarupananda 1909 Chapter 1 Translation editorial workspace.

Stdlib only. Does not modify content/raw/. Does not build packages or import.

Pin authority:
  content/raw/translations/swarupananda-1909/2015.386852.Srimad-Bhagavad.pdf
  SHA-256 ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e

The pinned DLI/IA Image Container PDF is missing printed pages 14–15, 17–18,
and 20–21 (confirmed by consecutive BookReader leaves 34→35→36→37 jumping
13→16→19→22). Gap fluent English is provisionally filled from public-domain
secondary transcriptions (Sacred Texts 1909 etext + later Advaita Ashrama OCR
for combined-label evidence on I. 28—29.) and marked SOURCE_CONFLICT.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SOURCE_ID = "bhagavad-gita-translation-en-swarupananda-1909-v1"
SOURCE_CHECKSUM = (
    "ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e"
)
PROVIDER = "Swami Swarupananda"
CHAPTER = 1

# scanLeaf = printedPage + 21 for pages present in the pinned item (1–13, 16, 19, 22–23).
# Missing printed pages: 14, 15, 17, 18, 20, 21 → scanLeaf 0.


def seg_id(verses: list[int]) -> str:
    if len(verses) == 1:
        return f"swarupananda-1909-bg-1-{verses[0]:03d}"
    return f"swarupananda-1909-bg-1-{verses[0]:03d}-{verses[-1]:03d}"


def unit(
    verses: list[int],
    *,
    label: str,
    text: str,
    printed: int,
    scan_leaf: int,
    status: str,
    extraction_notes: list[str],
    commentary_notes: list[str],
    editorial_notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "segmentId": seg_id(verses),
        "chapterNumber": CHAPTER,
        "coveredVerseNumbers": verses,
        "coveredCanonicalReferences": [f"{CHAPTER}.{v}" for v in verses],
        "sourceLabel": label,
        "translationText": text,
        "language": "en",
        "provider": PROVIDER,
        "sourceId": SOURCE_ID,
        "sourceChecksum": SOURCE_CHECKSUM,
        "sourcePage": {"printed": printed, "scanLeaf": scan_leaf},
        "publicationStatus": status,
        "editorialNotes": editorial_notes or [],
        "contentVersion": 1,
        "extractionNotes": extraction_notes,
        "commentarySeparationNotes": commentary_notes,
    }


def chapter01_units() -> list[dict[str, Any]]:
    """Ordered publisher translation units for Chapter 1."""
    scan = "Fluent English taken from pinned scan page image (BookReader leaf)."
    excl = (
        "Excluded Sanskrit, word-by-word gloss, and bracketed commentary on the "
        "same page(s)."
    )
    gap = (
        "Pinned scan missing this printed page (DLI/IA leaf gap). Provisional "
        "fluent English from Sacred Texts 1909 etext (PD), cross-checked against "
        "later Advaita Ashrama OCR for structure; not page-image verified against "
        "1909 leaves."
    )
    gap_2829 = (
        "Pinned scan missing pages 14–15. Later Advaita Ashrama OCR shows "
        "publisher-combined label 28—29; Sacred Texts merges the same unit under "
        "a single numbered block. Treated as one N→1 segment pending complete "
        "1909 page images."
    )

    return [
        unit(
            [1],
            label="I. 1.",
            text=(
                "Dhritarâshtra said :\n"
                "Tell me, O Sanjaya! Assembled on Kurukshetra the centre of "
                "religious activity, desirous to fight, what indeed my people and "
                "the Pândavas did do?"
            ),
            printed=1,
            scan_leaf=22,
            status="UNREVIEWED",
            extraction_notes=[scan, "Opening speaker line retained as printed."],
            commentary_notes=[excl],
        ),
        unit(
            [2],
            label="I. 2.",
            text=(
                "Sanjaya said:\n"
                "But then king Duryodhana, having seen the Pândava forces in "
                "battle-array, approached his teacher Drona, and spoke these words:"
            ),
            printed=2,
            scan_leaf=23,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [3],
            label="I. 3.",
            text=(
                "Behold, O Teacher ! this mighty army of the sons of Pându, "
                "arrayed by the son of Drupada, thy gifted pupil."
            ),
            printed=3,
            scan_leaf=24,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Fluent paragraph begins on printed page 3 after Sanskrit/gloss "
                "on page 2.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [4, 5, 6],
            label="I. 4. 5. 6.",
            text=(
                "Here (are) heroes, mighty archers, the equals in battle of Bhima "
                "and Arjuna—the great warriors Yuyudhâna, Virâta, Drupada ; the "
                "valiant Dhrishtaketu, Chekitâna and the king of Kâshi, the best of "
                "men Purujit, Kuntibhoja and Shaibya ; the powerful Yudhâmanyu and "
                "the brave Uttamaujas, the son of Subhadrâ, and the sons of "
                "Draupadi,—lords of great chariots."
            ),
            printed=4,
            scan_leaf=25,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Combined label I. 4. 5. 6. verified on page image; one fluent "
                "paragraph on pages 3–4 (unit recorded on printed page of fluent "
                "completion).",
            ],
            commentary_notes=[
                excl,
                "Excluded [Great-charioted : …] gloss after the fluent unit.",
            ],
        ),
        unit(
            [7],
            label="I. 7.",
            text=(
                "Hear also, O Best of the twice-born ! the names of those who "
                "(are) distinguished amongst ourselves, the leaders of my army. "
                "These I relate (to you) for your information."
            ),
            printed=4,
            scan_leaf=25,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [8],
            label="I. 8.",
            text=(
                "Thyself and Bhishma and Karna and Kripa, the victorious in war, "
                "Asvatthâma and Vikarna and Jayadratha, the son of Somadatta."
            ),
            printed=5,
            scan_leaf=26,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [9],
            label="I. 9.",
            text=(
                "And many other heroes also, well-skilled in fight, and armed with "
                "many kinds of weapons, are here determined to lay down their lives "
                "for my sake."
            ),
            printed=5,
            scan_leaf=26,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [10],
            label="I. 10.",
            text=(
                "This our army commanded by Bhishma (is) impossible to be counted, "
                "but that army of theirs, commanded by Bhima (is) easy to number."
            ),
            printed=6,
            scan_leaf=27,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Scan fluent uses 'commanded by' (not 'defended by').",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [11],
            label="I. 11.",
            text=(
                "(Now) Do, being stationed in your proper places in the divisions "
                "of the army, support Bhishma alone."
            ),
            printed=6,
            scan_leaf=27,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [12],
            label="I. 12.",
            text=(
                "That powerful, eldest of the Kurus, Bhishma the grandsire, in "
                "order to cheer Duryodhana, now sounded aloud a lion-roar and blew "
                "his conch."
            ),
            printed=7,
            scan_leaf=28,
            status="UNREVIEWED",
            extraction_notes=[scan, "Scan uses 'eldest' (not 'oldest')."],
            commentary_notes=[excl],
        ),
        unit(
            [13],
            label="I. 13.",
            text=(
                "Then following Bhishma, conches and kettle-drums, tabors, "
                "trumpets and cowhorns blared forth suddenly from the Kaurava side "
                "and the noise was tremendous."
            ),
            printed=7,
            scan_leaf=28,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [14],
            label="I. 14.",
            text=(
                "Then, also, Mâdhava and Pândava, stationed in their magnificent "
                "chariot yoked to white horses, blew their divine conches with a "
                "furious noise."
            ),
            printed=8,
            scan_leaf=29,
            status="UNREVIEWED",
            extraction_notes=[scan, "Scan uses 'yoked to' (not 'yoked with')."],
            commentary_notes=[excl],
        ),
        unit(
            [15],
            label="I. 15.",
            text=(
                "Hrishikesha blew the Pânchajanya, Dhananjaya, the Devadatta, and "
                "Vrikodara, the doer of terrific deeds, his large conch Paundra."
            ),
            printed=8,
            scan_leaf=29,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [16],
            label="I. 16.",
            text=(
                "King Yudhishthira, son of Kunti, blew the conch named "
                "Anantavijaya, and Nakula and Sahadeva their Sughosha and "
                "Manipushpaka."
            ),
            printed=9,
            scan_leaf=30,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [17],
            label="I. 17.",
            text=(
                "The expert bowman, king of Kâshi, and the great warrior "
                "Shikhandi, Dhrishtadyumna and Virâta and the unconquered Sâtyaki;"
            ),
            printed=9,
            scan_leaf=30,
            status="UNREVIEWED",
            extraction_notes=[scan, "Fluent unit ends with semicolon as printed."],
            commentary_notes=[excl],
        ),
        unit(
            [18],
            label="I. 18.",
            text=(
                "O Lord of Earth ! Drupada and the sons of Draupadi, and the "
                "mighty-armed son of Subhadrâ, all also blew each his own conch."
            ),
            printed=10,
            scan_leaf=31,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [19],
            label="I. 19.",
            text=(
                "And the terrific noise resounding throughout heaven and earth "
                "rent the hearts of the Dhritarâshtra's party."
            ),
            printed=10,
            scan_leaf=31,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Preserved printed phrasing 'the Dhritarâshtra's party'.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [20],
            label="I. 20.",
            text=(
                "Then, O Lord of Earth, seeing Dhritarâshtra army standing "
                "marshalled and the shooting about to begin, that Pândava whose "
                "ensign was the monkey, raising his bow, said the following words "
                "to Krishna :"
            ),
            printed=11,
            scan_leaf=32,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Initial OCR/vision misread 'shooting' region; corrected against "
                "page image and word-by-word locator "
                "(शस्त्रसंपाते = discharge of missiles; fluent prints 'shooting').",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [21, 22],
            label="I. 21—22.",
            text=(
                "Arjuna said :\n"
                "Place my chariot, O Achyuta ! between the two armies that I may "
                "see those who stand here prepared for war. On this the eve of "
                "battle (let me know) with whom I have to fight."
            ),
            printed=11,
            scan_leaf=32,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Combined label I. 21—22. verified on page image; fluent spans "
                "pages 11–12.",
                "Preserved 'On this the eve of battle' as on scan.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [23],
            label="I. 23.",
            text=(
                "For I desire to observe those who are assembled here for fight, "
                "wishing to please the evil-minded Duryodhana by taking his part "
                "on this battle-field."
            ),
            printed=12,
            scan_leaf=33,
            status="UNREVIEWED",
            extraction_notes=[scan, "Scan uses 'taking his part' (not 'side')."],
            commentary_notes=[excl],
        ),
        unit(
            [24, 25],
            label="I. 24—25.",
            text=(
                "Sanjaya said :\n"
                "Commanded thus by Gudâkesha, Hrishikesha, O Bhârata, drove that "
                "grandest of chariots to a place between the two hosts, facing "
                "Bhishma, Drona and all the rulers of the earth, and then spoke "
                "thus, “Behold, O Pârtha, all the Kurus gathered together!”"
            ),
            printed=13,
            scan_leaf=34,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Combined label I. 24—25. verified on page image; fluent completes "
                "on printed page 13.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [26],
            label="I. 26.",
            text=(
                "Then saw Pârtha stationed there in both the armies, grandfathers, "
                "fathers-in-law and uncles, brothers and cousins, his own and their "
                "sons and grandsons, and comrades, teachers, and other friends as "
                "well."
            ),
            printed=13,
            scan_leaf=34,
            status="SOURCE_CONFLICT",
            extraction_notes=[
                "Fluent unit begins on printed page 13 (scan leaf 34) and continues "
                "onto missing printed pages 14–15.",
                gap,
            ],
            commentary_notes=[excl],
            editorial_notes=[
                "SOURCE_CONFLICT: completion beyond page 13 not present in pinned "
                "scan; provisional secondary text.",
            ],
        ),
        unit(
            [27],
            label="I. 27.",
            text=(
                "Then he, the son of Kunti, seeing all those kinsmen stationed in "
                "their ranks, spoke thus sorrowfully, filled with deep compassion."
            ),
            printed=14,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=[
                "Secondary sources separate word-by-word from fluent paragraph; "
                "commentary not included in translationText."
            ],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 14–15 absent from pinned scan.",
            ],
        ),
        unit(
            [28, 29],
            label="I. 28—29.",
            text=(
                "Arjuna said :\n"
                "Seeing, O Krishna, these my kinsmen gathered here, eager for "
                "fight, my limbs fail me, and my mouth is parched up. I shiver all "
                "over, and my hair stands on end. The bow Gândiva slips from my "
                "hand, and my skin burns."
            ),
            printed=15,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap, gap_2829],
            commentary_notes=[
                "Excluded secondary commentary about compassion / self-control."
            ],
            editorial_notes=[
                "SOURCE_CONFLICT: pages missing; N→1 28—29 asserted by later "
                "Advaita OCR + Sacred Texts block structure, not by 1909 leaf image.",
            ],
        ),
        unit(
            [30],
            label="I. 30.",
            text=(
                "Neither, O Keshava, can I stand upright. My mind is in a whirl. "
                "And I see adverse omens."
            ),
            printed=15,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 14–15 absent from pinned scan.",
            ],
        ),
        unit(
            [31],
            label="I. 31.",
            text=(
                "Neither, Oh Krishna, do I see any good in killing these my own "
                "people in battle. I desire neither victory nor empire, nor yet "
                "pleasure."
            ),
            printed=16,
            scan_leaf=35,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Full fluent paragraph appears at top of printed page 16 "
                "(continuation from missing page 15); wording verified on leaf 35.",
                "Preserved printed 'Oh Krishna' (not 'O Krishna').",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [32, 33, 34],
            label="I. 32—34.",
            text=(
                "Of what avail is dominion to us, of what avail are pleasures and "
                "even life, if these, O Govinda! for whose sake it is desired that "
                "empire, enjoyment and pleasure should be ours, themselves stand "
                "here in battle, having renounced life and wealth—\n"
                "Teachers, uncles, sons and also grandfathers, maternal uncles, "
                "fathers-in-law, grandsons, brothers-in-law, besides other kinsmen."
            ),
            printed=16,
            scan_leaf=35,
            status="SOURCE_CONFLICT",
            extraction_notes=[
                "Combined label I. 32—34. verified on printed page 16 image.",
                "Fluent begins on page 16; completion spans missing pages 17–18.",
                gap,
            ],
            commentary_notes=[excl],
            editorial_notes=[
                "SOURCE_CONFLICT: unit incomplete on pinned scan; tail from "
                "secondary PD transcription.",
            ],
        ),
        unit(
            [35],
            label="I. 35.",
            text=(
                "Even though these were to kill me, O slayer of Madhu, I could not "
                "wish to kill them, not even for the sake of dominion over the "
                "three worlds, how much less for the sake of the earth!"
            ),
            printed=17,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 17–18 absent from pinned scan.",
            ],
        ),
        unit(
            [36],
            label="I. 36.",
            text=(
                "What pleasure indeed could be ours, O Janârdana, from killing "
                "these sons of Dhritarâshtra? Sin only could take hold of us by the "
                "slaying of these felons."
            ),
            printed=18,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["Excluded Atatâyin / felons commentary footnote."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 17–18 absent from pinned scan.",
            ],
        ),
        unit(
            [37],
            label="I. 37.",
            text=(
                "Therefore ought we not to kill our kindred, the sons of "
                "Dhritarâshtra. For how could we, O Mâdhava, gain happiness by the "
                "slaying of our own kinsmen?"
            ),
            printed=18,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 17–18 absent from pinned scan.",
            ],
        ),
        unit(
            [38, 39],
            label="I. 38. 39.",
            text=(
                "Though these, with understanding overpowered by greed, see no "
                "evil due to decay of families, and no sin in hostility to friends, "
                "why should we, O Janârdana, who see clearly the evil due to the "
                "decay of families, not turn away from this sin?"
            ),
            printed=19,
            scan_leaf=36,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Combined label I. 38. 39. verified on page image.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [40],
            label="I. 40.",
            text=(
                "On the decay of a family the immemorial religious rites of that "
                "family die out. On the destruction of spirituality, impiety "
                "further overwhelms the whole of the family."
            ),
            printed=19,
            scan_leaf=36,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [41],
            label="I. 41.",
            text=(
                "On the prevalence of impiety, O Krishna, the women of the family "
                "become corrupt; and women being corrupted, there arises, O "
                "Vârshneya, intermingling of castes."
            ),
            printed=20,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[
                "Sanskrit for I. 41. begins on printed page 19; fluent English is "
                "on missing pages 20–21.",
                gap,
            ],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 20–21 absent from pinned scan.",
            ],
        ),
        unit(
            [42],
            label="I. 42.",
            text=(
                "Admixture of castes, indeed, is for the hell of the family and "
                "the destroyers of the family; their ancestors fall, deprived of "
                "the offerings of rice-ball and water."
            ),
            printed=20,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["Excluded Srâddha commentary."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 20–21 absent from pinned scan.",
            ],
        ),
        unit(
            [43],
            label="I. 43.",
            text=(
                "By these misdeeds of the destroyers of the family, bringing about "
                "confusion of castes, are the immemorial religious rites of the "
                "caste and the family destroyed."
            ),
            printed=21,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 20–21 absent from pinned scan.",
            ],
        ),
        unit(
            [44],
            label="I. 44.",
            text=(
                "We have heard, O Janârdana, that inevitable is the dwelling in "
                "hell of those men in whose families religious practices have been "
                "destroyed."
            ),
            printed=21,
            scan_leaf=0,
            status="SOURCE_CONFLICT",
            extraction_notes=[gap],
            commentary_notes=["No commentary included."],
            editorial_notes=[
                "SOURCE_CONFLICT: printed pages 20–21 absent from pinned scan.",
            ],
        ),
        unit(
            [45],
            label="I. 45.",
            text=(
                "Alas, we are involved in a great sin, in that we are prepared to "
                "slay our kinsmen, from greed of the pleasures of a kingdom!"
            ),
            printed=22,
            scan_leaf=37,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Fluent paragraph complete on printed page 22; running header "
                "45-47] is pagination only.",
            ],
            commentary_notes=[excl],
        ),
        unit(
            [46],
            label="I. 46.",
            text=(
                "Verily, if the sons of Dhritarâshtra, weapons in hand, were to "
                "slay me, unresisting and unarmed, in the battle, that would be "
                "better for me."
            ),
            printed=22,
            scan_leaf=37,
            status="UNREVIEWED",
            extraction_notes=[scan],
            commentary_notes=[excl],
        ),
        unit(
            [47],
            label="I. 47.",
            text=(
                "Sanjaya said :\n"
                "Speaking thus in the midst of the battle-field, Arjuna casting "
                "away his bow and arrows, sank down on the seat of his chariot, "
                "with his mind distressed with sorrow."
            ),
            printed=23,
            scan_leaf=38,
            status="UNREVIEWED",
            extraction_notes=[
                scan,
                "Fluent spans pages 22–23; chapter-end formula excluded from "
                "translationText.",
            ],
            commentary_notes=[excl],
        ),
    ]


def to_segment_draft(u: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "segmentId",
        "chapterNumber",
        "coveredVerseNumbers",
        "coveredCanonicalReferences",
        "sourceLabel",
        "translationText",
        "language",
        "provider",
        "sourceId",
        "sourceChecksum",
        "sourcePage",
        "publicationStatus",
        "editorialNotes",
        "contentVersion",
    ]
    return {k: u[k] for k in keys}


def to_extraction(u: dict[str, Any]) -> dict[str, Any]:
    return {
        "segmentId": u["segmentId"],
        "chapterNumber": u["chapterNumber"],
        "coveredVerseNumbers": u["coveredVerseNumbers"],
        "sourceLabel": u["sourceLabel"],
        "translationText": u["translationText"],
        "sourceId": u["sourceId"],
        "sourceChecksum": u["sourceChecksum"],
        "sourcePage": u["sourcePage"],
        "extractionNotes": u["extractionNotes"],
        "commentarySeparationNotes": u["commentarySeparationNotes"],
        "publicationStatus": u["publicationStatus"],
    }


def build_coverage(units: list[dict[str, Any]]) -> dict[str, Any]:
    verse_to: dict[str, str] = {}
    multi: list[dict[str, Any]] = []
    combined: list[dict[str, Any]] = []
    for u in units:
        verses = u["coveredVerseNumbers"]
        for v in verses:
            verse_to[f"1.{v}"] = u["segmentId"]
        if len(verses) > 1:
            multi.append(
                {
                    "segmentId": u["segmentId"],
                    "sourceLabel": u["sourceLabel"],
                    "coveredVerseNumbers": verses,
                    "coveredCanonicalReferences": u["coveredCanonicalReferences"],
                }
            )
            combined.append(
                {
                    "label": u["sourceLabel"],
                    "from": verses[0],
                    "to": verses[-1],
                    "segmentId": u["segmentId"],
                    "evidence": (
                        "page_image"
                        if u["publicationStatus"] == "UNREVIEWED"
                        else "secondary_transcription_pending_page_image"
                    ),
                }
            )
    return {
        "chapterNumber": 1,
        "expectedVerseCount": 47,
        "segmentCount": len(units),
        "verseToSegment": dict(sorted(verse_to.items(), key=lambda kv: int(kv[0].split(".")[1]))),
        "segmentsWithMultiVerseCoverage": multi,
        "uncoveredVerses": [],
        "multiplyCoveredVerses": [],
        "combinedLabelInventory": combined,
        "status": "DRAFT_WITH_SOURCE_GAPS",
        "pinnedScanGaps": {
            "missingPrintedPages": [14, 15, 17, 18, 20, 21],
            "observedLeafPageJumps": [
                {"scanLeaf": 34, "printedPage": 13},
                {"scanLeaf": 35, "printedPage": 16},
                {"scanLeaf": 36, "printedPage": 19},
                {"scanLeaf": 37, "printedPage": 22},
                {"scanLeaf": 38, "printedPage": 23},
            ],
            "notes": [
                "Pinned IA/DLI master skips six Chapter 1 body pages.",
                "Gap segments marked SOURCE_CONFLICT; not APPROVED.",
                "I. 28—29. added from secondary evidence; not in Phase 2 "
                "page-image combined-label list because those pages are missing.",
            ],
        },
        "packageReady": False,
        "importReady": False,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_workspace(workspace: Path) -> dict[str, Any]:
    workspace.mkdir(parents=True, exist_ok=True)
    units = chapter01_units()
    write_jsonl(workspace / "segment-draft.jsonl", [to_segment_draft(u) for u in units])
    write_jsonl(workspace / "source-extraction.jsonl", [to_extraction(u) for u in units])
    coverage = build_coverage(units)
    (workspace / "coverage-map.json").write_text(
        json.dumps(coverage, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "segmentCount": len(units),
        "sourceConflictCount": sum(
            1 for u in units if u["publicationStatus"] == "SOURCE_CONFLICT"
        ),
        "multiVerseCount": sum(1 for u in units if len(u["coveredVerseNumbers"]) > 1),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--workspace",
        type=Path,
        default=Path("content/translation-editorial/swarupananda-1909/chapter-01"),
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = write_workspace(args.workspace)
    print(json.dumps({"workspace": str(args.workspace), **summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
