package com.antar.translation.application.port;

import java.util.List;

public record ResolvedTranslationPackage(
        String packageId,
        int packageFormatVersion,
        String scriptureId,
        int chapterNumber,
        String language,
        String provider,
        String sourceName,
        String licenseType,
        String licenseReference,
        long contentVersion,
        String packageStatus,
        String packageChecksum,
        String manifestChecksum,
        String provenanceChecksum,
        String translationsChecksum,
        List<String> sourceRegistryReferences,
        int recordCount,
        CanonicalReferenceRange canonicalReferenceRange,
        List<PackageTranslationRecord> translations) {

    public ResolvedTranslationPackage {
        sourceRegistryReferences = List.copyOf(sourceRegistryReferences);
        translations = List.copyOf(translations);
    }

    public record CanonicalReferenceRange(String from, String to, int expectedCount) {
    }

    public record PackageTranslationRecord(
            String canonicalReference,
            int chapterNumber,
            int verseNumber,
            String translationText,
            long contentVersion) {
    }
}
