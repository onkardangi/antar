"""Offline tests for Internet Archive Translation acquisition helpers."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_ACQ = Path(__file__).resolve().parents[1]
if str(_ACQ) not in sys.path:
    sys.path.insert(0, str(_ACQ))

from fetch_internet_archive_item import (  # noqa: E402
    AcquisitionError,
    acquire,
    select_file_records,
    sha256_bytes,
    write_bytes_exclusive,
)


def sample_ia_metadata() -> dict:
    return {
        "metadata": {
            "identifier": "in.ernet.dli.2015.386852",
            "title": "Srimad Bhagavad Gita",
            "creator": "The Swami Swarupananda",
            "date": "1909",
            "year": "1909",
        },
        "files": [
            {
                "name": "2015.386852.Srimad-Bhagavad.pdf",
                "format": "Image Container PDF",
                "size": "4",
                "md5": "x",
                "sha1": "y",
            },
            {
                "name": "in.ernet.dli.2015.386852_meta.xml",
                "format": "Metadata",
                "size": "5",
                "md5": "a",
                "sha1": "b",
            },
        ],
    }


class FetchInternetArchiveItemTests(unittest.TestCase):
    def test_select_file_records_requires_all_names(self) -> None:
        meta = sample_ia_metadata()
        selected = select_file_records(
            meta, ["2015.386852.Srimad-Bhagavad.pdf"]
        )
        self.assertIn("2015.386852.Srimad-Bhagavad.pdf", selected)
        with self.assertRaises(AcquisitionError):
            select_file_records(meta, ["missing.pdf"])

    def test_refuse_overwrite_different_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.bin"
            write_bytes_exclusive(path, b"one")
            with self.assertRaises(AcquisitionError):
                write_bytes_exclusive(path, b"two")

    def test_idempotent_identical_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.bin"
            self.assertEqual(write_bytes_exclusive(path, b"same"), "written")
            self.assertEqual(write_bytes_exclusive(path, b"same"), "unchanged")

    def test_acquire_writes_files_and_checksums(self) -> None:
        meta = sample_ia_metadata()
        payloads = {
            "https://archive.org/metadata/in.ernet.dli.2015.386852": json.dumps(
                meta
            ).encode("utf-8"),
            "https://archive.org/download/in.ernet.dli.2015.386852/2015.386852.Srimad-Bhagavad.pdf": b"%PDF",
            "https://archive.org/download/in.ernet.dli.2015.386852/in.ernet.dli.2015.386852_meta.xml": b"<meta/>",
        }

        def fake_fetch(url: str, **kwargs: object) -> bytes:
            return payloads[url]

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "raw"
            with mock.patch(
                "fetch_internet_archive_item.fetch_bytes", side_effect=fake_fetch
            ):
                result = acquire(
                    item_id="in.ernet.dli.2015.386852",
                    output_dir=out,
                    filenames=[
                        "2015.386852.Srimad-Bhagavad.pdf",
                        "in.ernet.dli.2015.386852_meta.xml",
                    ],
                    pinned_master="2015.386852.Srimad-Bhagavad.pdf",
                    user_agent="test-agent",
                    timeout_sec=5,
                    retries=1,
                    retry_backoff_sec=0.0,
                )
            self.assertEqual(result["itemId"], "in.ernet.dli.2015.386852")
            pdf = out / "2015.386852.Srimad-Bhagavad.pdf"
            self.assertTrue(pdf.is_file())
            self.assertEqual(sha256_bytes(b"%PDF"), sha256_bytes(pdf.read_bytes()))
            self.assertTrue((out / "SHA256SUMS").is_file())
            self.assertTrue((out / "metadata.json").is_file())
            # second run does not overwrite differing content
            with mock.patch(
                "fetch_internet_archive_item.fetch_bytes", side_effect=fake_fetch
            ):
                acquire(
                    item_id="in.ernet.dli.2015.386852",
                    output_dir=out,
                    filenames=[
                        "2015.386852.Srimad-Bhagavad.pdf",
                        "in.ernet.dli.2015.386852_meta.xml",
                    ],
                    pinned_master="2015.386852.Srimad-Bhagavad.pdf",
                    user_agent="test-agent",
                    timeout_sec=5,
                    retries=1,
                    retry_backoff_sec=0.0,
                )


if __name__ == "__main__":
    unittest.main()
