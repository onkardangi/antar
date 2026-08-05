#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from validate_package import validate  # noqa: E402

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "fixture-translation-en-chapter-01-v1"
)


class TranslationPackageFormatTests(unittest.TestCase):
    def test_synthetic_fixture_is_importable(self) -> None:
        outcome = validate(FIXTURE)
        self.assertTrue(outcome["structurallyValid"], outcome)
        self.assertTrue(outcome["editoriallyValid"], outcome)
        self.assertTrue(outcome["importable"], outcome)
        self.assertEqual(outcome["errors"], [])
        self.assertEqual(outcome["warnings"], [])

    def test_fixture_text_is_synthetic(self) -> None:
        rows = [
            json.loads(line)
            for line in (FIXTURE / "translations.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(rows[0]["translationText"], "FIXTURE_TRANSLATION_VERSE_1")
        self.assertTrue(
            all(r["translationText"].startswith("FIXTURE_TRANSLATION_VERSE_") for r in rows)
        )

    def test_record_count_mismatch_is_structurally_invalid(self) -> None:
        import hashlib
        import tempfile
        import shutil

        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / FIXTURE.name
            shutil.copytree(FIXTURE, dst)
            manifest = json.loads((dst / "manifest.json").read_text(encoding="utf-8"))
            manifest["recordCount"] = 999
            translations = (dst / "translations.jsonl").read_bytes()
            provenance = (dst / "provenance.json").read_bytes()

            def sha(data: bytes) -> str:
                return hashlib.sha256(data).hexdigest()

            manifest["packageChecksum"] = sha(translations + provenance)
            manifest["fileChecksums"] = {
                "translations.jsonl": sha(translations),
                "provenance.json": sha(provenance),
            }
            manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
            (dst / "manifest.json").write_bytes(manifest_bytes)
            (dst / "SHA256SUMS").write_text(
                f"{sha(manifest_bytes)}  manifest.json\n"
                f"{sha(provenance)}  provenance.json\n"
                f"{sha(translations)}  translations.jsonl\n",
                encoding="utf-8",
            )
            outcome = validate(dst)
            self.assertFalse(outcome["structurallyValid"], outcome)
            self.assertFalse(outcome["importable"], outcome)
            self.assertTrue(any("recordCount" in e for e in outcome["errors"]))


if __name__ == "__main__":
    unittest.main()
