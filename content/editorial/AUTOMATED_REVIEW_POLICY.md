# Automated Editorial Review Policy

**Status:** Phase 2  
**Engine version:** 1  
**Last Updated:** August 2026

## Purpose

Automate deterministic source comparison so humans review **exceptions** and **sampled audits**, not every identical Verse.

**Automated comparison is not scholarly approval.**

The engine may recommend readiness. It must **never** set review status to `APPROVED`.

## Classifications

| Classification | Meaning |
|----------------|---------|
| `AUTO_MATCH` | Two or more sources match exactly after only identity-preserving structural checks with no normalization rules needed |
| `NORMALIZATION_MATCH` | Sources match after documented approved comparison-only normalization; originals still preserved |
| `SOURCE_CONFLICT` | Substantive difference detected |
| `INSUFFICIENT_SOURCES` | Fewer than two Sanskrit source evidences |

## Human review is mandatory for

- `SOURCE_CONFLICT`
- `INSUFFICIENT_SOURCES`
- front-matter differences (`FRONT_MATTER`)
- speaker-label differences (`SPEAKER_LABEL`) unless a future explicit policy resolves them
- segmentation differences
- unapproved orthographic differences
- every Verse selected for audit sampling

## Human review may be streamlined for

- exact matches (`AUTO_MATCH`)
- approved normalization matches (`NORMALIZATION_MATCH`) **without** mandatory human-review categories

Streamlined still means a human must eventually approve. Automation only prepares evidence.

### Controlled batch approval (explicit `--apply` only)

A narrowly scoped tool may perform **human-authorized** batch approval of `NORMALIZATION_MATCH` candidates when:

1. The operator supplies `--apply` with named reviewer identity and decision date
2. Every candidate passes eligibility (exact selected-source Sanskrit copy; registered primary + verification sources; no `SOURCE_CONFLICT`)
3. Policy `content/editorial/batch-normalization-match-approval-policy.json` permits the path
4. The operation is all-or-nothing (no partial subset writes)

`FRONT_MATTER` Verses are batch-eligible only when the candidate already defines `proposedSanskritText` as an exact selected-source copy (retention is explicit; silent strip is forbidden).

This path still records Reviewer, Date, Decision text, and Audit Log. It is **not** automatic approval by the comparison engine.

## Final `APPROVED` still requires

1. Named reviewer
2. Date
3. Decision text
4. Audit-log entry

No automated path may fill Approval fields or set `APPROVED`.

## Confidence (transparent, rule-based)

| Case | Confidence |
|------|------------|
| Exact match across 2+ sources | `1.00` |
| Approved normalization match across 2+ sources | `0.95` |
| One source only | `0.40` |
| Substantive conflict | `0.00` |

Confidence never substitutes for editorial approval.

## Audit sampling

Deterministic sample of `AUTO_MATCH` + `NORMALIZATION_MATCH`:

- at least 10% of those classifications
- always first and last Verse of the Chapter
- always any Verse where a normalization rule was applied
- stable seed derived from `corpusVersionSeed` in the normalization policy

## Recommended next acquisition work

Acquire second-source verification evidence for Verses that remain `INSUFFICIENT_SOURCES` before expecting normalization matches Chapter-wide.
