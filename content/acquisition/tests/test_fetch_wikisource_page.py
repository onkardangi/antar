"""Offline tests for Wikisource acquisition helpers."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_ACQ = Path(__file__).resolve().parents[1]
if str(_ACQ) not in sys.path:
    sys.path.insert(0, str(_ACQ))

from fetch_wikisource_page import (  # noqa: E402
    AcquisitionError,
    extract_page,
    extract_revision,
    snapshot_filename,
    write_bytes_exclusive,
)


def sample_payload(*, missing: bool = False, with_content: bool = True) -> dict:
    if missing:
        return {"query": {"pages": [{"title": "Missing", "missing": True}]}}
    content = "demo"
    main = {"contentmodel": "wikitext"}
    if with_content:
        main["content"] = content
    return {
        "query": {
            "pages": [
                {
                    "pageid": 164,
                    "title": "भगवद्गीता/अर्जुनविषादयोगः",
                    "fullurl": "https://sa.wikisource.org/wiki/Demo",
                    "canonicalurl": "https://sa.wikisource.org/wiki/Demo",
                    "revisions": [
                        {
                            "revid": 343151,
                            "parentid": 1,
                            "timestamp": "2022-08-10T14:13:52Z",
                            "size": 10,
                            "sha1": "abc",
                            "slots": {"main": main},
                        }
                    ],
                }
            ]
        }
    }


class FetchWikisourcePageTests(unittest.TestCase):
    def test_successful_mediawiki_response_parsing(self) -> None:
        payload = sample_payload()
        page = extract_page(payload)
        revision = extract_revision(page, 343151)
        self.assertEqual(page["pageid"], 164)
        self.assertEqual(revision["revid"], 343151)
        self.assertEqual(revision["slots"]["main"]["content"], "demo")

    def test_missing_page(self) -> None:
        with self.assertRaises(AcquisitionError):
            extract_page(sample_payload(missing=True))

    def test_missing_revision_content(self) -> None:
        page = extract_page(sample_payload(with_content=False))
        with self.assertRaises(AcquisitionError):
            extract_revision(page, 343151)

    def test_refuse_overwrite_different_raw_revision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / snapshot_filename(343151)
            write_bytes_exclusive(path, b'{"a":1}\n')
            with self.assertRaises(AcquisitionError):
                write_bytes_exclusive(path, b'{"a":2}\n')

    def test_idempotent_identical_raw_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / snapshot_filename(343151)
            data = b'{"a":1}\n'
            self.assertEqual(write_bytes_exclusive(path, data), "written")
            self.assertEqual(write_bytes_exclusive(path, data), "unchanged")


if __name__ == "__main__":
    unittest.main()
