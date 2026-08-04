"""Tests for Chapter 1 workspace validation after Wikisource acquisition."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_VALIDATION_DIR = Path(__file__).resolve().parents[1]
if str(_VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(_VALIDATION_DIR))

from validate_chapter01_workspace import SOURCE_ID, validate_workspace  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]


class Chapter01WorkspaceValidationTests(unittest.TestCase):
    def test_workspace_structural_gates(self) -> None:
        result = validate_workspace(repo_root=REPO_ROOT)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.info.get("extractionCount"), 47)
        self.assertEqual(result.info.get("draftApprovedCount"), 0)
        self.assertFalse(result.info.get("draftImportReady"))
        self.assertFalse(result.info.get("textualAccuracyEditoriallyApproved"))
        self.assertEqual(
            result.info.get("comparisonStatusCounts"),
            {"READY_FOR_REVIEW": 34, "SOURCE_CONFLICT": 13},
        )
        self.assertEqual(result.info.get("registryStatus"), "ACQUIRED_UNREVIEWED")
        self.assertEqual(result.info.get("iitkRegistryCount"), 47)
        self.assertTrue(SOURCE_ID)
