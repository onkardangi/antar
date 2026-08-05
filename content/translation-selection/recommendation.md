# Recommendation — First English Translation for Antar

**Decision status:** Recommended for Phase 1 (selection only; not acquired or imported)  
**Date:** August 2026

---

## Recommendation

Adopt **Swami Swarupananda, *Srimad-Bhagavad-Gita* (Advaita Ashrama, Mayavati, 1909)** as Antar’s first English Translation source.

Language: `en`  
Provider (proposed packaging identity): `Swami Swarupananda`  
Edition freeze: **1909 Advaita Ashrama book** (exact printing to be pinned at acquisition via checksum)

---

## Why this wins

Antar’s first Translation must be:

1. **Licensable** for redistribution in a commercial mobile + backend product  
2. **Mappable** 1:1 to Scripture Verse identities (not a free-standing poem)  
3. **Readable** in a contemplative Reader (Read → Reflect), without sounding like a Victorian epic poem  
4. **Separable** from commentary, notes, and Sanskrit (Translation BC owns English only; ADR-012)

Swarupananda is the only candidate that scores highly on all four at once:

| Need | Swarupananda fit |
|------|------------------|
| License | Clear US public domain (1909) |
| Mapping | Explicit verse numbering; close Sanskrit tracking (must still verify 47/34) |
| Reader tone | Clear early-modern prose suitable for verse cards |
| Separation | Translation body distinct from footnotes — extract translation only |
| Operations | Book scans on Internet Archive / DLI; no need for bulk web scrape |

---

## Why not the others (brief)

| Candidate | Why not first |
|-----------|---------------|
| **Arnold** | Public domain but **not verse-aligned**. Would require forbidden invented segmentation |
| **Besant & Das** | Excellent structure and PD status; stronger as runner-up. More layered extraction; Theosophical diction; slightly heavier editorial overhead for V1 |
| **Telang (SBE)** | PD and scholarly; weaker machine verse boundaries; archaic Reader voice; extra non-Gita texts in the volume |
| **Johnston** | PD but less operationally mature as a numbered digital corpus for Antar’s pipeline |
| **Edgerton** | Not cleared for PD redistribution without renewal diligence |

---

## Product positioning

Swarupananda should be presented as:

- An **attributed historical English Translation**
- A **companion** to Antar’s Sanskrit Verse identities
- **Not** “the meaning of the Gita,” not Saar, not Understanding, not commentary

Attribution must survive into `translation.translation_sources` / `translation.translations` per editorial policy.

---

## Editorial strategy (high level)

1. Freeze one raw edition (1909 scan) with checksum + provenance README.  
2. Extract **English verse translation only** — discard commentary footnotes, prefatory essays, “Greatness of the Gita,” indexes.  
3. Map each extracted unit to Antar `chapter.verse`.  
4. Treat combined labels (`9-10`) as **stop-and-review** items: either source already prints separable sense-units that match Antar identities without invention, or those Verses remain unpublished until resolved.  
5. First package scope: **Chapter 1 only** (47 Verses), mirroring Scripture package sequencing — then expand chapter-by-chapter.  
6. Never generate missing English with AI and present it as Swarupananda.

---

## Package strategy (high level)

Use the existing Translation package format under `content/packages/translation/`:

```text
<package-id>/
  manifest.json
  translations.jsonl
  provenance.json
  SHA256SUMS
```

Proposed first real package id (future): `translation-en-swarupananda-1909-chapter-01-v1`

- `language`: `en`  
- `provider`: `Swami Swarupananda`  
- `sourceName`: `Srimad-Bhagavad-Gita (Advaita Ashrama, 1909)`  
- `licenseType`: public-domain catalog entry (to be added at acquisition — not added in this phase)  
- `packageStatus`: only `APPROVED` after editorial sign-off  

Synthetic fixtures remain unrelated research/test artifacts.

---

## Runner-up retention

Keep **Besant & Das 1905** documented as the approved fallback if Swarupananda numbering verification fails Chapter 13 or combined-verse density proves unworkable without invention.

Do not acquire either corpus in this phase.

---

## What this recommendation is not

- Not an import approval  
- Not a license catalog mutation  
- Not a change to V007, importers, API, mobile, or Scripture packages  
- Not permission to scrape Sacred Texts or any site in bulk  
