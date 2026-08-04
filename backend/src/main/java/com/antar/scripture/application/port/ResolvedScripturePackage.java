package com.antar.scripture.application.port;

import java.util.List;
import java.util.Map;

/**
 * Parsed Package Format v1 package (in-memory). Does not include raw filesystem secrets beyond
 * declared metadata fields.
 */
public record ResolvedScripturePackage(
        String packageId,
        String scriptureId,
        int chapterNumber,
        long contentVersion,
        int recordCount,
        String packageStatus,
        int packageFormatVersion,
        String packageChecksum,
        String manifestChecksum,
        String provenanceChecksum,
        String versesChecksum,
        List<String> sourceRegistryReferences,
        String editorialApprovalManifestChecksum,
        boolean allowNullTransliteration,
        CanonicalReferenceRange canonicalReferenceRange,
        List<PackageVerseRecord> verses,
        PackageProvenance provenance) {

    public ResolvedScripturePackage {
        sourceRegistryReferences = List.copyOf(sourceRegistryReferences);
        verses = List.copyOf(verses);
    }

    public record CanonicalReferenceRange(String from, String to, int expectedCount) {
    }

    public record PackageVerseRecord(
            int chapterNumber,
            int verseNumber,
            String canonicalReference,
            String sanskritText,
            String transliteration,
            long contentVersion,
            List<String> sourceIds,
            Map<String, String> sourceChecksums,
            String editorialDecisionId,
            String editorialApprovalChecksum) {

        public PackageVerseRecord {
            sourceIds = List.copyOf(sourceIds);
            sourceChecksums = Map.copyOf(sourceChecksums);
        }

        public boolean hasTransliteration() {
            return transliteration != null;
        }
    }

    public record PackageProvenance(
            String packageId,
            List<String> sourceIds,
            Map<String, String> sourceRoles,
            Map<String, String> sourceChecksums,
            List<String> editorialReviewerIds,
            List<String> secondReviewerIds,
            List<String> approvalDates) {

        public PackageProvenance {
            sourceIds = List.copyOf(sourceIds);
            sourceRoles = Map.copyOf(sourceRoles);
            sourceChecksums = Map.copyOf(sourceChecksums);
            editorialReviewerIds = List.copyOf(editorialReviewerIds);
            secondReviewerIds = List.copyOf(secondReviewerIds);
            approvalDates = List.copyOf(approvalDates);
        }
    }
}
