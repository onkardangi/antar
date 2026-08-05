# Licensing Analysis — Phase 1 Translation Candidates

**Status:** Research conclusions for selection  
**Not legal advice.** Confirm with counsel before commercial redistribution if Antar’s distribution jurisdictions expand beyond US-centric assumptions.

---

## Governing Antar rules

From `docs/content/03_EDITORIAL_POLICY.md` and MVP plan:

- Do not import unlicensed Translation content  
- Every Translation row retains attribution  
- Displayed public-domain labels do **not** alone authorize import when edition/numbering fails Antar rules  
- Record license **as displayed** at acquisition in `content/licenses/` + registry (future acquisition phase)

---

## Jurisdiction baseline used here

| Assumption | Implication |
|------------|-------------|
| US publication before 1931 | Work is in the US public domain |
| Author death + long terms abroad | Pre-1930 Indian/UK printings of these translators are generally PD in major markets, but **pin the exact printing** |
| Hosting site terms ≠ underlying copyright | Wikisource/Sacred Texts/Project Gutenberg wrappers can add trademark or CC obligations on *their* files even when the underlying book is PD |

---

## Candidate licensing matrix

| Candidate | Underlying copyright (US) | Safe to redistribute English text commercially (US)? | Hosting caveats | Attribution |
|-----------|---------------------------|------------------------------------------------------|-----------------|-------------|
| Arnold 1885 | PD | Yes | PG trademark if redistributing as PG eBook | Translator + title + year |
| Besant & Das 1905 | PD (1905 printing) | Yes | Wikisource markup may be CC BY-SA; IA scans preferred | Both translators + title + year |
| Swarupananda 1909 | PD | Yes | Sacred Texts ISTA-produced HTML has commercial-use / attribution constraints — **do not use as redistribution master** | Swarupananda + Advaita Ashrama 1909 |
| Telang SBE 1882 | PD | Yes | Same host-layer caveats | Telang + SBE Vol. 8 + year |
| Johnston 1908 | PD | Yes | IA preferred | Johnston + title + year |
| Edgerton 1944 | **Not cleared** | **No** until renewal search proves PD or license obtained | HUP commercial edition exists | N/A for Phase 1 |

---

## Recommended source — licensing conclusion

**Swarupananda 1909 is license-safe for Antar Phase 1 selection**, contingent on:

1. Acquiring an **immutable scan or transcription derived from the 1909 book**, not Sacred Texts HTML as the canonical bytes.  
2. Recording the displayed upstream terms at download time.  
3. Cataloging a public-domain (or PD-mark) entry in `content/licenses/` during acquisition.  
4. Retaining human-readable attribution in package `provenance.json` and eventual `translation.translation_sources`.  
5. Excluding commentary footnotes from the licensed Translation field (commentary would be a later BC/policy if ever used).

### Sacred Texts (ISTA) note

Sacred Texts states many files are public domain and encourages reuse of PD content, but **ISTA-produced texts** carry notice-of-attribution requirements and **commercial-use restrictions** on those produced files in their entirety without a license. For a commercial app:

- Use Sacred Texts only as a **research reference** (spot-check numbering/style)  
- Acquire **Internet Archive / library scan** of the 1909 printing as raw  
- Optionally produce Antar’s own transcription under Antar provenance (not claiming ISTA etext copyright)

### Project Gutenberg note (Arnold and any PG mirror)

PG allows use of the underlying PD work. Keeping the phrase “Project Gutenberg” / PG headers triggers PG trademark license terms. Product path: remove PG trademark wrappers; cite the public-domain work and Antar acquisition provenance.

### Wikisource note (Besant)

Underlying Besant translation may be PD while the **Wikisource transcription/markup** is often under CC BY-SA. If Antar ever uses Wikisource bytes, catalog CC BY-SA and satisfy attribution/share-alike for that layer — same honesty pattern used for Sanskrit Wikisource in `content/licenses/catalog.json`. Prefer IA page images + Antar transcription when possible to keep the redistribution story simple.

---

## What “public domain” does **not** grant

| Myth | Antar reality |
|------|---------------|
| PD ⇒ approved for import | Still need numbering match, editorial sign-off, package validation |
| PD ⇒ may scrape any mirror | Host ToS, robots, and trademark rules still apply |
| PD ⇒ may omit attribution | Antar product policy still requires translator attribution |
| PD commentary ⇒ may store as Translation | Commentary is not Translation; hierarchy must stay clean |

---

## Proposed future license catalog entries (not created in this phase)

When acquisition begins, add catalog rows such as:

| id | Purpose |
|----|---------|
| `us-pd-pre-1931` | Generic US public-domain classification for pre-1931 printings |
| `swarupananda-1909-pd` | Specific notes for the chosen Swarupananda printing + acquisition URL |

Do **not** invent SPDX for pure PD; `spdx` may be null with clear notes (pattern already used for non-standard Sanskrit Documents terms).

---

## Clearance checklist before `APPROVED_FOR_IMPORT`

- [ ] Exact printing identified (title page photo/PDF page)  
- [ ] SHA-256 of raw bytes recorded  
- [ ] Displayed upstream license/terms recorded verbatim  
- [ ] Host-layer terms evaluated (IA vs Wikisource vs ISTA vs PG)  
- [ ] Attribution string approved for UI / API fields  
- [ ] Confirmation that only Translation prose is packaged (no commentary)  
- [ ] Counsel review if shipping outside US-centric assumptions  

---

## Phase 1 licensing verdict

| Question | Answer |
|----------|--------|
| Is there at least one safe English PD Translation? | **Yes** — Swarupananda 1909 (primary), Besant & Das 1905 (backup) |
| Is Arnold safe but usable? | Safe copyright; **unusable** for verse packaging |
| Is Edgerton cleared? | **No** |
| May Antar import now? | **No** — selection only; acquisition not performed |
