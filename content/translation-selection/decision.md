# Decision — First English Translation (Phase 1)

**Status:** Selection decision recorded  
**Date:** August 2026  
**Outcome:** Recommend **Swami Swarupananda (1909)**  
**Implementation in this phase:** Documentation only

---

## 1. Decision matrix

Scoring: **1** (poor) … **5** (excellent) for Antar Phase 1 needs.

| Criterion | Arnold | Besant & Das | Swarupananda | Telang (SBE) | Johnston |
|-----------|-------:|-------------:|-------------:|-------------:|---------:|
| License safety | 5 | 5 | 5 | 5 | 5 |
| Machine readability | 2 | 4 | **5** | 2 | 3 |
| Editorial consistency | 3 | 4 | **5** | 3 | 3 |
| Verse mapping | **1** | **5** | **4** | 2 | 3 |
| Ease of acquisition | 4 | 4 | **4** | 3 | 3 |
| Long-term maintainability | 2 | 4 | **5** | 3 | 3 |
| **Total** | **17** | **26** | **28** | **18** | **20** |

Edgerton (1944) is **not scored** as a Phase 1 contender: license safety fails the entry gate until renewal clearance.

### Overall recommendation

| Rank | Candidate | Role |
|------|-----------|------|
| **1** | **Swarupananda 1909** | **Selected** |
| 2 | Besant & Das 1905 | Approved fallback |
| 3 | Johnston 1908 | Reserve PD alternative |
| 4 | Telang 1882 | Scholarly reference only |
| — | Arnold | Reject as primary Verse Translation |
| — | Edgerton 1944 | Deferred (license) |

---

## 2. Why Swarupananda wins

Besant & Das nearly ties on structure and license. Swarupananda wins on the **product-shaped** combination Antar needs now:

1. **License safety equal to other PD options**, without Edgerton’s renewal cloud.  
2. **Verse-oriented prose** already presented as numbered English units suitable for `translations.jsonl`.  
3. **Reader tone** closer to contemplative study than Arnold’s poem or Telang’s Victorian treatise.  
4. **Maintainability:** one translator byline, one Ashrama edition to freeze, commentary separable as footnotes.  
5. **Acquisition path** via Internet Archive book scan avoids Sacred Texts commercial etext constraints and PG trademark wrappers.

Besant & Das scores equal or higher on pure verse-mapping *potential*, but costs more operationally (multi-layer pages, Theosophical lexicon, edition-variant risk). It remains the fallback if Swarupananda fails the 47/34 gate.

Arnold loses decisively on verse mapping despite perfect PD status — a textbook case of “license-safe but not Antar-shaped.”

---

## 3. Binding Phase 1 decisions

| Decision | Record |
|----------|--------|
| First English Translation source | Swarupananda, Advaita Ashrama, 1909 |
| Language code | `en` |
| Fallback | Besant & Das 1905 |
| Arnold as Verse Translation | **No** |
| Edgerton | **Not cleared** — deferred |
| Acquire text now | **No** |
| Build package / import now | **No** |
| Change backend / mobile / V007 / importers / API | **No** |

---

## 4. Implementation roadmap (planned only)

Assuming the winning translation proceeds after acquisition approval:

```text
Raw acquisition
    ↓
Verification
    ↓
Normalization
    ↓
Editorial review
    ↓
Translation package
    ↓
Translation importer
    ↓
Translation API
```

### Stage details

| Stage | Work | Out of scope reminders |
|-------|------|------------------------|
| **Raw acquisition** | Download one IA 1909 scan into `content/raw/translation/swarupananda-1909/`; provenance README; checksum; registry `CANDIDATE` | No Sacred Texts bulk scrape |
| **Verification** | Count chapters/verses vs `antar_verse_counts.json`; inventory combined labels; confirm commentary separable; inspection doc | No renumbering to “make it fit” |
| **Normalization** | Deterministic extract of English verse prose → working JSON/JSONL; UTF-8; strip footnotes | Do not edit raw; no AI authorship |
| **Editorial review** | Human review Chapter 1 (47); sign-off per `03_EDITORIAL_POLICY.md` spirit for Translation | No silent wording invention |
| **Translation package** | Build `content/packages/translation/<package-id>/` per existing schema; `validate_package.py` | Do not import editorial workspace directly |
| **Translation importer** | Use **existing** Translation package importer against `APPROVED` package | No importer feature work required for selection; fix only if real package reveals format bugs (separate task) |
| **Translation API** | Existing `GET /api/v1/translations/verses/{verseId}` serves `PUBLISHED` rows | No API contract change required for first corpus; provider selection remains deferred |

### Suggested sequencing

1. Chapter 1 package only (align with Scripture Chapter 1 production reality).  
2. Expand chapters after Chapter 1 proves provenance → package → import → read path.  
3. Multi-translation provider UX later (ADR-012 deferred selection).

---

## 5. Success criteria for later phases

- [ ] Raw Swarupananda 1909 checksummed and registered  
- [ ] Chapter 1 = 47 and Chapter 13 = 34 verified (or fallback triggered)  
- [ ] License catalog + provenance complete  
- [ ] Chapter 1 `APPROVED` Translation package validates  
- [ ] Import into `translation.*` with attribution intact  
- [ ] API returns real Swarupananda text for Chapter 1 Verse ids  
- [ ] Mobile still unchanged until a deliberate Reader composition task  

---

## 6. Document control

| Artifact | Path |
|----------|------|
| Index | `content/translation-selection/README.md` |
| Comparison | `content/translation-selection/candidate-comparison.md` |
| Recommendation | `content/translation-selection/recommendation.md` |
| Licensing | `content/translation-selection/licensing.md` |
| Acquisition plan | `content/translation-selection/acquisition-plan.md` |
| Risks | `content/translation-selection/risk-analysis.md` |
| This decision | `content/translation-selection/decision.md` |

Supersession: a later ADR or content decision may replace this recommendation only with explicit numbering/license evidence — not by convenience.
