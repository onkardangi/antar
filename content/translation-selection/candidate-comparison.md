# Candidate Comparison — English Bhagavad Gita Translations

**Phase:** Translation Content Phase 1 (research only)  
**Antar numbering target:** Chapter 1 = 47, Chapter 13 = 34, 18 Chapters, 700 Verses  
(`content/validation/antar_verse_counts.json`)

No text was acquired or scraped in bulk for this comparison. Assessments use published bibliographic facts, public catalog records, and previously inspected public index/sample pages.

---

## Evaluation criteria

| Criterion | Why it matters for Antar |
|-----------|--------------------------|
| License safety | Mobile + backend redistribution; no unlicensed import |
| Machine readability | Deterministic extraction into `translations.jsonl` |
| Editorial consistency | Stable prose suitable for contemplative Reader display |
| Verse mapping | 1:1 map to Antar `chapter.verse` identities |
| Ease of acquisition | Clear raw artifact path under `content/raw/` later |
| Long-term maintainability | Provenance, attribution, edition stability |

---

## 1. Sir Edwin Arnold — *The Song Celestial*

| Field | Finding |
|-------|---------|
| Translator | Sir Edwin Arnold (1832–1904) |
| Title | *The Song Celestial; Or, Bhagavad-Gîtâ (from the Mahâbhârata)* |
| First publication | 1885 (widely reprinted; e.g. Truslove / Trübner printings around 1900–1906) |
| Copyright status | Expired. Author died 1904; 19th-century publication |
| Public-domain status (US) | **Yes** — published well before 1931 |
| Redistribution rights | Underlying work: unrestricted public domain in the US. Project Gutenberg editions (#2388) additionally carry PG trademark terms if redistributed *as* a PG eBook |
| Machine-readable availability | High for full text (Project Gutenberg plain text / HTML; Internet Archive scans). **Low for verse units** |
| Verse completeness | Literary paraphrase of the whole Gita; not a scholarly verse inventory |
| Chapter/verse numbering | **No reliable per-verse numbering** in the common PG HTML/etext. Chapters only |
| Source quality | Stable, well-known English classic |
| Formatting consistency | Poetic blank verse / lyrical measures; speaker labels; not tabular |
| Known editorial quirks | Victorian poetic diction; meter prioritized over shloka alignment; unsuitable as “literal” companion to Sanskrit |
| Attribution requirements | Attribute translator + title + edition year. If using PG bytes with PG branding, obey PG license; for product redistribution prefer stripping PG trademark wrappers and citing the public-domain work + Antar provenance |
| Suitability for Antar | **Poor as primary Translation.** Fails verse-mapping requirement central to `translation.translations` ↔ `scripture.verses` |

### Antar fit

Reading experience is literary, but Antar’s Translation BC requires one published English row per Verse identity. Arnold would force invented verse splits — forbidden by Antar editorial/provenance discipline.

---

## 2. Annie Besant & Bhagavan Das

| Field | Finding |
|-------|---------|
| Translators | Annie Besant (1847–1933); Bhagavan Das (1869–1958) for the 1905 word-for-word / free-translation edition |
| Title | *The Bhagavad-Gita: with Saṁskṛta text, free translation into English, a word-for-word translation, and an introduction on Saṁskṛta grammar* (London: Theosophical Publishing Society, 1905). Related: Besant-only cheap editions (e.g. Natesan 4th ed., Madras, 1922) with Devanagari + English |
| Publication year | **1905** (joint scholarly edition); Besant English also circulated in later cheap editions through early 1920s |
| Copyright status | 1905 edition: authors’ rights expired under typical life+70 / US pre-1931 rules for the published text. Besant died 1933; Das died 1958 — **US public domain remains clear for US-published/pre-1931 printings**; confirm jurisdiction for any later revised printing before acquisition |
| Public-domain status (US) | **Yes** for the 1905 and other pre-1931 printings |
| Redistribution rights | Underlying translation: PD in US. Wikisource/Internet Archive **transcription/markup** may carry CC BY-SA or similar contributor terms — treat transcription layer separately from the PD underlying work (same pattern as Sanskrit Wikisource in `content/licenses/`) |
| Machine-readable availability | Strong. Internet Archive PDF/DjVu + OCR; Wikisource structured pages for Besant editions; verse-oriented layout |
| Verse completeness | Full Gita; free English translation presented verse-by-verse alongside Sanskrit / word analysis |
| Chapter/verse numbering | Editions are **verse-numbered**. Expect alignment with standard 18-chapter tradition; **Chapter 13 34-vs-35** must be verified at acquisition (not assumed) |
| Source quality | High for study; historically influential Theosophical edition |
| Formatting consistency | Multi-layer pages (Sanskrit, free translation, word-for-word). Product must extract **only** the free English translation layer |
| Known editorial quirks | Theosophical vocabulary and framing; grammar introduction and word-for-word apparatus are **not** Translation product fields; cheap Besant-only reprints may differ slightly from 1905 joint text — pick **one** edition and freeze it |
| Attribution requirements | “Annie Besant & Bhagavan Das” (or Besant alone if that edition is chosen), title, year, publisher. No Theosophical Society endorsement claim |
| Suitability for Antar | **Strong runner-up.** Excellent structure for mapping; more editorial separation work (layers) and tone less “plain Reader prose” than Swarupananda |

### Antar fit

Best structural competitor to Swarupananda. Wins on apparatus richness; loses slightly on simplicity of Reader-facing English and on needing careful layer extraction.

---

## 3. Swami Swarupananda

| Field | Finding |
|-------|---------|
| Translator | Published as Swami Swarupananda (Advaita Ashrama, Mayavati). Preface notes collaboration with Mayavati sannyasins and some Western disciples of Vivekananda; manuscripts ~1901–1903; book form 1909 |
| Title | *Srimad-Bhagavad-Gita* (English translation and commentary) |
| Publication year | **1909** (Advaita Ashrama / Prabuddha Bharata Press lineage) |
| Copyright status | Published 1909; US PD as pre-1929/1931 publication. Translator attribution follows the published byline |
| Public-domain status (US) | **Yes** |
| Redistribution rights | Underlying 1909 work: PD in US. **Internet Sacred Text Archive (ISTA)** HTML etexts include an ISTA production/attribution notice and commercial-use constraints on ISTA-produced files — do **not** treat Sacred Texts HTML as the redistribution master. Prefer Internet Archive / print-scan bytes of the 1909 book as raw provenance |
| Machine-readable availability | High. Sacred Texts chapter HTML is verse-marked (research reference). IA / DLI scans provide immutable raw candidates |
| Verse completeness | Full 18 chapters; close prose translation intended to track Sanskrit |
| Chapter/verse numbering | Explicit verse numbers in the Advaita Ashrama / Sacred Texts presentation. Sacred Texts states numbering “correspond[s] closely to the Sanskrit text.” **Must verify** Antar Chapter 1 = 47 and Chapter 13 = 34 against the chosen raw edition before `APPROVED_FOR_NORMALIZATION` |
| Source quality | Readable early-20th-century prose; Advaita Ashrama editorial tradition |
| Formatting consistency | Numbered verses; occasional **combined labels** (e.g. `9-10`, `12-13`) in etext presentation; footnotes/commentary interwoven |
| Known editorial quirks | (1) Commentary/notes must **not** enter `translationText`. (2) Combined verse labels require editorial policy (no silent invention of splits). (3) Public debate exists about Sister Nivedita’s possible role; Antar should attribute **as published** (Swarupananda / Advaita Ashrama 1909) and record the debate as a provenance caveat, not rewrite authorship |
| Attribution requirements | “Swami Swarupananda, *Srimad-Bhagavad-Gita*, Advaita Ashrama, Mayavati, 1909.” No claim of Ramakrishna Mission / Advaita Ashrama endorsement |
| Suitability for Antar | **Best overall for Phase 1.** License-safe, verse-oriented prose, Reader-appropriate tone, clear acquisition path via book scan |

### Antar fit

Closest match to Antar needs: contemplative readable English, verse-aligned packaging, independent of Scripture Sanskrit corpus, and PD redistribution for a commercial mobile product — provided commentary is stripped and numbering is verified.

---

## 4. Kashinath Trimbak Telang — Sacred Books of the East

| Field | Finding |
|-------|---------|
| Translator | Kâshinâth Trimbak Telang (1850–1893) |
| Title | *The Bhagavadgîtâ* with the *Sanatsugâtîya* and the *Anugîtâ* — Sacred Books of the East, Volume 8 |
| Publication year | **1882** (Oxford: Clarendon Press); 2nd edition 1898 noted on Wikisource |
| Copyright status | Author died 1893; 1882 publication — long public domain |
| Public-domain status (US) | **Yes** |
| Redistribution rights | Underlying SBE text: PD. Sacred Texts / Wikisource hosting layers may add attribution or CC terms for markup — prefer IA/Google Books scan of Clarendon 1882/1898 as raw master |
| Machine-readable availability | Full text available (IA, Sacred Texts, Wikisource, Wisdom Library). **Verse segmentation weaker** — continuous scholarly prose with footnotes more than one-English-block-per-shloka |
| Verse completeness | Complete Gita translation; volume also contains Sanatsujatiya and Anugita (**must be excluded** from Gita Translation packages) |
| Chapter/verse numbering | Chapter structure present; inline per-verse numbering in common HTML etexts is **less crisp** than Swarupananda/Besant |
| Source quality | Foundational Indological translation; historically cited by later scholars (including Edgerton) |
| Formatting consistency | Victorian scholarly prose; heavy footnotes; archaic spellings (e.g. diacritic systems of SBE) |
| Known editorial quirks | Extra texts in the same volume; footnote apparatus; Müller/SBE orthography; not written as a modern Reader companion |
| Attribution requirements | “K. T. Telang, Sacred Books of the East, Vol. 8, Oxford, 1882 (or 1898 2nd ed. if that printing is acquired).” |
| Suitability for Antar | **License-safe but operationally weaker** for first product Translation due to verse packaging cost and archaic Reader tone |

### Antar fit

Excellent scholarly provenance; poorer path to 700 clean `translations.jsonl` rows than Swarupananda or Besant & Das.

---

## 5. Additional candidate considered — Charles Johnston (1908)

| Field | Finding |
|-------|---------|
| Translator | Charles Johnston (1867–1931) |
| Title | *Bhagavad-gîta: “The Songs of the Master”* |
| Publication year | **1908** |
| Public-domain status (US) | **Yes** (pre-1931 US publication; Library of Congress / IA records treat as unrestricted) |
| Notes | Theosophical-leaning literary translation; less commonly used as a digital verse corpus than Swarupananda/Besant; available on Internet Archive |
| Suitability for Antar | Viable PD alternative; **not preferred** over Swarupananda for prose clarity + ecosystem familiarity + verse-marked editions |

---

## 6. Explicitly deferred — Franklin Edgerton (1944)

| Field | Finding |
|-------|---------|
| Translator | Franklin Edgerton |
| Publication | Harvard Oriental Series vols. 38–39, **1944** |
| Why deferred | US works published 1929–1963 require **timely copyright renewal** analysis before claiming PD. Harvard University Press still sells editions. Online “PD” copies are **not** sufficient clearance for Antar |
| Suitability for Antar | Scholarly excellence, but **not license-cleared** in this Phase 1 research. Do not select without a documented renewal search and counsel-ready memo |

---

## Side-by-side snapshot

| Candidate | US PD? | Verse-numbered? | Reader prose? | Acquisition clarity | Phase 1 rank |
|-----------|--------|-----------------|---------------|---------------------|--------------|
| Swarupananda 1909 | Yes | Yes (verify counts) | Yes | IA book scan preferred | **1 — recommend** |
| Besant & Das 1905 | Yes | Yes (verify counts) | Good (layered) | IA / Wikisource | **2 — runner-up** |
| Telang SBE 1882 | Yes | Weak in etexts | Archaic scholarly | IA Clarendon scan | 3 |
| Johnston 1908 | Yes | Moderate | Literary | IA | 4 |
| Arnold *Song Celestial* | Yes | **No** | Poetic | PG / IA | Reject as primary |
| Edgerton 1944 | **Unclear / likely restricted** | Yes (scholarly) | Literal scholarly | HUP | Deferred |

---

## Mapping risk note (all verse-numbered candidates)

Antar rejects corpora that require automated split/merge/renumber to force identities (`docs/content/01_SCRIPTURE_PROVENANCE.md`).

Before any Swarupananda or Besant package:

1. Count verses per chapter against `antar_verse_counts.json`.
2. Especially confirm **Chapter 1 = 47** and **Chapter 13 = 34**.
3. Document every combined label (`9-10`) or missing number as an editorial finding — do not invent text to fill gaps.
