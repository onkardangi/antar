package com.antar.scripture.application.imports;

/**
 * Deterministic seam invoked inside the import mutation transaction after Verse updates are
 * prepared and saved, before the successful import audit row is written.
 *
 * <p>Production always uses the no-op implementation from {@code ScriptureImportConfiguration}.
 * Tests may replace it with a {@code @Primary} bean to prove mid-mutation rollback. There is no
 * runtime property that intentionally crashes production imports.
 */
@FunctionalInterface
public interface ImportMutationProbe {

    void afterVersesSaved(
            com.antar.scripture.application.port.ResolvedScripturePackage pkg,
            java.util.List<com.antar.scripture.domain.Verse> updatedVerses);
}
