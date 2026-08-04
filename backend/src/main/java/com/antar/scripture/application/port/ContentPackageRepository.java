package com.antar.scripture.application.port;

import com.antar.scripture.domain.ContentPackageStatus;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Persistence for imported package identity and import execution audit.
 */
public interface ContentPackageRepository {

    Optional<ContentPackageRecord> findByPackageId(String packageId);

    Optional<ContentPackageRecord> findByPackageChecksum(String packageChecksum);

    Optional<ContentPackageRecord> findActiveApprovedByChapterNumber(int chapterNumber);

    Optional<ContentPackageRecord> findActiveApprovedByScriptureAndChapter(
            String scriptureId, int chapterNumber);

    Optional<ImportExecutionRecord> findSuccessfulImport(String packageId, String packageChecksum);

    void acquirePackageImportLock(String packageChecksum);

    ContentPackageRecord savePackage(ContentPackageRecord record);

    ImportExecutionRecord saveImport(ImportExecutionRecord record);

    ImportExecutionRecord saveFailedImport(ImportExecutionRecord record);

    /** Flushes pending persistence work (needed before inserting a new APPROVED package). */
    void flush();

    record ContentPackageRecord(
            String packageId,
            int packageFormatVersion,
            String scriptureId,
            int chapterNumber,
            long contentVersion,
            ContentPackageStatus packageStatus,
            String packageChecksum,
            String manifestChecksum,
            String provenanceChecksum,
            String versesChecksum,
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

        public Optional<String> packageIdOptional() {
            return Optional.ofNullable(packageId);
        }

        public Optional<ImportFailureCode> failureCodeOptional() {
            return Optional.ofNullable(failureCode);
        }

        public Optional<String> failureMessageOptional() {
            return Optional.ofNullable(failureMessage);
        }
    }
}
