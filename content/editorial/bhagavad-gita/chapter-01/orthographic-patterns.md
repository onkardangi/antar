# Chapter 1 orthographic pattern clusters

**Analysis originally prepared without adding comparison-engine rules.**

On 2026-08-04, Chapter 1–scoped comparison-only resolution rules were recorded in
`content/editorial/orthographic-resolution-policy.json` and applied only to the
11 orthographic-only conflicts listed there. Those rules do **not** auto-apply
to other chapters and do **not** rewrite stored source Sanskrit.

Automated comparison is not scholarly approval.

## `anusvara_vs_nga_cluster`

- Observed forms: `संकर / सङ्कर`, `संगम्य / सङ्गम्य`
- Affected Verses: `1.2, 1.41, 1.42, 1.43`
- Frequency: `4`
- Description: Anusvāra (ं) versus explicit velar nasal cluster (ङ्) before क/ग.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Consider a narrowly scoped comparison-only equivalence for सं↔सङ् before क/ग in these attested Chapter 1 forms only — do not add broad spelling substitutions yet.
- Risk of over-normalization: High if generalized beyond attested environments.

## `anusvara_vs_nya_cluster`

- Observed forms: `समितिंजयः / समितिञ्जयः`, `धनञ्जयः / धनंजयः`
- Affected Verses: `1.15, 1.24, 1.8`
- Frequency: `3`
- Description: Anusvāra versus ñ-cluster (ञ्ज) in -जय compounds.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Consider comparison-only equivalence for ंजय↔ञ्जय in epithets; distinct from the already-approved संजय↔सञ्जय pair.
- Risk of over-normalization: Medium if applied outside -जय epithets.

## `avagraha_representation`

- Observed forms: `परयाविष्टो / परयाऽऽविष्टो`, `एवमुक्त्वार्जुनः / एवमुक्त्वाऽर्जुनः`
- Affected Verses: `1.28, 1.47`
- Frequency: `2`
- Description: Presence/absence of avagraha (ऽ) marking vowel sandhi elision.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Consider comparison-only avagraha-optional rule for identical vowel sandhi; do not strip avagraha from stored sources.
- Risk of over-normalization: Medium — avagraha can be editorially meaningful in some editions.

## `vocalic_r_presentation`

- Observed forms: `पितॄनथ / पितृ़नथ`, `भ्रातॄन् / भ्रातृ़न्`
- Affected Verses: `1.20, 1.26`
- Frequency: `2`
- Description: Long vocalic ṝ versus ṛ + nukta-like presentation variants.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Inspect with a Sanskrit orthography specialist before any rule.
- Risk of over-normalization: High — may hide real editorial choices.

## `anusvara_vs_homorganic_nasal`

- Observed forms: `generic anusvāra ↔ homorganic nasal`
- Affected Verses: `1.26`
- Frequency: `1`
- Description: Catch-all for anusvāra/homorganic nasal presentation.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Do not add a broad rule from mixed cases; prefer narrow lemmas.
- Risk of over-normalization: Very high if broad.

## `anusvara_vs_ma_cluster`

- Observed forms: `संबन्धिनस्तथा / सम्बन्धिनस्तथा`
- Affected Verses: `1.34`
- Frequency: `1`
- Description: Anusvāra versus explicit म् before ब (homorganic labial).
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Consider narrow संब↔सम्ब comparison equivalence if approved.
- Risk of over-normalization: Medium.

## `anusvara_vs_nga_in_sangamya`

- Observed forms: `आचार्यमुपसंगम्य / आचार्यमुपसङ्गम्य`
- Affected Verses: `1.2`
- Frequency: `1`
- Description: Same anusvāra↔ङ् alternation inside उपसंगम्य.
- Changes lexical identity: `False`
- Already covered by policy: `False`
- Proposed policy action: Fold into narrow anusvāra↔ङ् comparison rule if approved.
- Risk of over-normalization: Medium — limit to documented lemma environments.

## `sanjaya_speaker_label_extension`

- Observed forms: `सञ्जय उवाच / संजय उवाच`
- Affected Verses: `1.24`
- Frequency: `1`
- Description: Approved संजय↔सञ्जय pair appearing in speaker labels.
- Changes lexical identity: `False`
- Already covered by policy: `True`
- Proposed policy action: Extend existing orthography_sanjaya_equivalence application to speaker-label comparison (policy already lists the pair).
- Risk of over-normalization: Low if limited to the approved pair.

## Non-cluster / editorial attention

References that remain more than a repeated orthographic cluster (or lack a safe narrow rule): `1.20, 1.22`
