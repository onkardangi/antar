package com.antar.translation.application.port;

import com.antar.translation.domain.ContentPackageStatus;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface TranslationContentPackageRepository {

    Optional<ContentPackageRecord> findByPackageId(String packageId);

    Optional<ContentPackageRecord> findByPackageChecksum(String packageChecksum);

    Optional<ContentPackageRecord> findActiveApproved(
            String languageCode, String provider, String scriptureId, int chapterNumber);

    Optional<ImportExecutionRecord> findSuccessfulImport(String packageId, String packageChecksum);

    void acquirePackageImportLock(String packageChecksum);

    ContentPackageRecord savePackage(ContentPackageRecord record);

    ImportExecutionRecord saveImport(ImportExecutionRecord record);

    ImportExecutionRecord saveFailedImport(ImportExecutionRecord record);

    void flush();

    record ContentPackageRecord(
            String packageId,
            int packageFormatVersion,
            String scriptureId,
            int chapterNumber,
            String languageCode,
            String provider,
            long contentVersion,
            ContentPackageStatus packageStatus,
            String packageChecksum,
            String manifestChecksum,
            String provenanceChecksum,
            String translationsChecksum,
            List<String> sourceRegistryReferences,
            int importerVersion,
            Instant firstImportedAt,
            Instant lastVerifiedAt,
            Instant createdAt,
            Instant updatedAt) {

        public ContentPackageRecord {
            sourceRegistryReferences = List.copyOf(sourceRegistryReferences);
        }
    }

    record ImportExecutionRecord(
            UUID id,
            String packageId,
            String attemptedPackageId,
            String packageChecksum,
            Integer chapterNumber,
            ImportExecutionStatus importStatus,
            int recordsRead,
            int recordsValidated,
            int recordsUpdated,
            int recordsUnchanged,
            int recordsRejected,
            ImportFailureCode failureCode,
            String failureMessage,
            int importerVersion,
            Instant startedAt,
            Instant completedAt,
            long durationMs) {
    }
}
