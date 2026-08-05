# Risk Analysis — First English Translation Selection

**Scope:** Risks of selecting and later operationalizing a PD English Translation for Antar.  
**Recommended candidate:** Swarupananda 1909.

---

## Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | Chapter 13 uses 35-verse tradition (or other count drift) | Medium | High — blocks canonical mapping | Gate on `antar_verse_counts.json` before normalization approval; fallback to Besant & Das |
| R2 | Combined verse labels (`9-10`) prevent 1:1 rows without invention | Medium | High | Inventory at inspection; unpublished gaps allowed; never AI-fill as Swarupananda |
| R3 | Commentary/footnotes leak into `translationText` | Medium | Medium | Explicit extraction rules; editorial checklist; package schema has no commentary field — keep it that way |
| R4 | Sacred Texts HTML used as redistribution master → ToS/commercial conflict | Medium | High | IA book scan as raw; Sacred Texts research-only |
| R5 | Authorship debate (Nivedita claim) creates attribution dispute | Low | Medium | Attribute **as published**; record debate in provenance caveats; no speculative byline rewrite |
| R6 | OCR errors alter meaning | High (for scans) | Medium | Human editorial review; prefer proofed passages; dual-source spot checks |
| R7 | Mixing Besant cheap reprint with 1905 joint text | Medium (if fallback) | Medium | Freeze one printing; refuse cross-edition merges |
| R8 | Arnold chosen for “famous English” brand | Low (if process followed) | High | Decision matrix rejects Arnold on verse mapping |
| R9 | Edgerton or modern copyrighted Gita imported “because better English” | Medium (pressure risk) | Critical | License gate; Phase 1 explicitly defers Edgerton |
| R10 | Partial chapter coverage confuses mobile UX | Medium | Medium | Product already allows missing Translation as unavailable; ship Chapter 1 first deliberately |
| R11 | Host CC BY-SA transcription obligations misunderstood | Medium | Medium | Prefer IA images + Antar transcription; if Wikisource bytes used, catalog CC BY-SA honestly |
| R12 | Translation tone feels sectarian (Advaita / Theosophy) | Low–Medium | Medium | UI copy: attributed historical translation, not Antar doctrine; future multi-provider selection |
| R13 | Scope creep into importer/API/mobile during content work | Medium | High | Phase boundaries in README; no runtime changes until package exists |
| R14 | Public-domain myth → skip editorial review | Medium | High | Provenance policy: PD ≠ import approval |

---

## Risks specific to rejected / deferred candidates

### Arnold

- **Primary risk:** irreversible mapping failure.  
- **Secondary:** Readers may prefer poetic English; resist by offering Arnold only if a future “literary edition” product mode appears — **not** as Verse-linked Translation rows.

### Telang

- **Primary risk:** expensive segmentation and footnote entanglement.  
- **Secondary:** archaic diction reduces contemplative readability.

### Edgerton

- **Primary risk:** copyright infringement if treated as PD without renewal proof.  
- **Mitigation:** deferred until documented clearance.

---

## Residual risks after mitigations

Even with Swarupananda selected:

1. Full 700-verse editorial quality will take time — **partial coverage is acceptable**.  
2. Some verses may remain unpublished pending combined-label resolution.  
3. International copyright edge cases outside US should get counsel review before wide global store distribution claims.

These are acceptable Phase 1 residuals; they are not reasons to choose an unmappable or uncleared text.

---

## Stop conditions (hard)

Halt acquisition/normalization/import if:

- Chapter 1 ≠ 47 or Chapter 13 ≠ 34 after honest counting  
- Raw checksum changes after registration  
- License/host terms forbid intended commercial redistribution of the **chosen bytes**  
- Team proposes AI-generated “Swarupananda-style” filler  
- Work starts modifying V007 / importers / mobile to “make the text fit”

---

## Summary

The largest real risks are **numbering fidelity**, **combined-verse handling**, and **wrong acquisition channel** (ISTA HTML / random mirrors) — not the underlying copyright of Swarupananda 1909 itself.
