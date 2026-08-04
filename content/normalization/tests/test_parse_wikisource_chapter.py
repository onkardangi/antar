"""Offline tests for Wikisource Chapter 1 parser."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import unicodedata
from pathlib import Path

_NORM = Path(__file__).resolve().parents[1]
if str(_NORM) not in sys.path:
    sys.path.insert(0, str(_NORM))

from parse_wikisource_chapter import (  # noqa: E402
    ParseError,
    extract_verses,
    normalize_poem_body,
    parse_snapshot_file,
    records_to_jsonl,
)


def dev(n: int) -> str:
    table = str.maketrans("0123456789", "०१२३४५६७८९")
    return str(n).translate(table)


def verse_poem(verse: int, body: str | None = None) -> str:
    marker = f"॥{dev(1)}-{dev(verse)}॥"
    if body is None:
        body = f"श्लोकपाठः {dev(verse)} ।\nद्वितीयं पादम् {marker}"
    elif marker not in body:
        body = body.rstrip() + f"  {marker}"
    return f"<poem>\n{body}\n</poem>"


def build_wikitext(
    *,
    verses: int = 47,
    duplicate_verse: int | None = None,
    skip_verse: int | None = None,
    include_commentary: bool = True,
    include_colophon: bool = True,
) -> str:
    chunks = [
        "[[File:Bhagavadgita-1st Chapter.wav|श्रूयताम्]]\n",
        "{{भगवद्गीतायाः अध्यायाः}}\n",
        "==प्रथमोऽध्याय: अर्जुनविषादयोगः==\n",
    ]
    for v in range(1, verses + 1):
        if skip_verse is not None and v == skip_verse:
            continue
        if v == 1:
            body = (
                "ॐ\nश्रीपरमात्मने नमः\nअथ श्रीमद्भगवद्गीता\n'''प्रथमोऽध्यायः'''\n\n"
                f"'''धृतराष्ट्र उवाच'''\nधर्मक्षेत्रे कुरुक्षेत्रे ।\nमामकाः पाण्डवाश्चैव ॥{dev(1)}-{dev(1)}॥"
            )
            chunks.append(verse_poem(1, body))
        else:
            chunks.append(verse_poem(v))
        if include_commentary:
            chunks.append(
                "{{व्याख्या\n|शीर्षकम्=व्याख्याः\n|\n'''रामानुजभाष्यम्'''<br>\ncommentary text\n}}\n"
            )
        if duplicate_verse is not None and v == duplicate_verse:
            chunks.append(verse_poem(v))
    if include_colophon:
        chunks.append(
            "<poem>\nॐ तत्सदिति श्रीमद्भगवद्गीता ... प्रथमोऽध्यायः ॥ १ ॥\n</poem>\n"
        )
    return "".join(chunks)


def snapshot_for(wikitext: str, revid: int = 343151) -> dict:
    return {
        "query": {
            "pages": [
                {
                    "pageid": 164,
                    "title": "भगवद्गीता/अर्जुनविषादयोगः",
                    "revisions": [
                        {
                            "revid": revid,
                            "timestamp": "2022-08-10T14:13:52Z",
                            "slots": {"main": {"content": wikitext}},
                        }
                    ],
                }
            ]
        }
    }


class ParseWikisourceChapterTests(unittest.TestCase):
    def test_47_verse_extraction(self) -> None:
        records = extract_verses(
            build_wikitext(),
            source_id="test-source",
            revision_id=343151,
        )
        self.assertEqual(len(records), 47)
        self.assertEqual(records[0]["canonicalReference"], "1.1")
        self.assertEqual(records[-1]["canonicalReference"], "1.47")
        self.assertIsNone(records[0]["transliteration"])
        self.assertIn("parsingNotes", records[0])
        self.assertIn("धृतराष्ट्र उवाच", records[0]["sanskritText"])
        self.assertIn("ॐ", records[0]["sanskritText"])
        self.assertNotIn("रामानुजभाष्यम्", records[0]["sanskritText"])

    def test_commentary_exclusion(self) -> None:
        records = extract_verses(
            build_wikitext(include_commentary=True),
            source_id="test-source",
            revision_id=343151,
        )
        joined = "\n".join(r["sanskritText"] for r in records)
        self.assertNotIn("{{व्याख्या", joined)
        self.assertNotIn("रामानुजभाष्यम्", joined)
        self.assertNotIn("commentary text", joined)

    def test_duplicate_verse_marker(self) -> None:
        with self.assertRaises(ParseError):
            extract_verses(
                build_wikitext(duplicate_verse=5),
                source_id="test-source",
                revision_id=343151,
            )

    def test_missing_verse_marker(self) -> None:
        with self.assertRaises(ParseError):
            extract_verses(
                build_wikitext(skip_verse=10),
                source_id="test-source",
                revision_id=343151,
            )

    def test_unicode_nfc_normalization(self) -> None:
        # Decomposed vowel sign combining sequence force via NFD on a line.
        base = "धर्मक्षेत्रे"
        nfd = unicodedata.normalize("NFD", base)
        body = f"{nfd} कुरुक्षेत्रे ।\nमामकाः ॥{dev(1)}-{dev(1)}॥"
        text, changes = normalize_poem_body(body)
        self.assertEqual(text, unicodedata.normalize("NFC", text))
        if nfd != unicodedata.normalize("NFC", nfd):
            self.assertIn("unicode_nfc", changes)

    def test_deterministic_extraction(self) -> None:
        snap = snapshot_for(build_wikitext())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snap.json"
            path.write_text(
                json.dumps(snap, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            _r1, t1 = parse_snapshot_file(path, source_id="test-source")
            _r2, t2 = parse_snapshot_file(path, source_id="test-source")
            self.assertEqual(t1, t2)
            self.assertEqual(records_to_jsonl(_r1), t1)


if __name__ == "__main__":
    unittest.main()
