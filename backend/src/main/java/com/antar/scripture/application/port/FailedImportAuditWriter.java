package com.antar.scripture.application.port;

import com.antar.scripture.domain.ImportFailureCode;
import java.time.Instant;

/**
 * Writes sanitized FAILED import audit rows in an independent transaction after a rolled-back
 * mutation attempt. Never used for dry-run. Never creates {@code content_packages} rows.
 */
public interface FailedImportAuditWriter {

    void recordFailedImport(FailedImportAudit audit);

    /**
     * Safe failure metadata only. No local paths, Verse text, stack traces, or raw payloads.
     */
    record FailedImportAudit(
            String attemptedPackageId,
            String packageChecksum,
            Integer chapterNumber,
            ImportFailureCode failureCode,
            String failureMessage,
            int importerVersion,
            int recordsRead,
            int recordsValidated,
            int recordsUpdated,
            int recordsUnchanged,
            int recordsRejected,
            Instant startedAt,
            Instant completedAt,
            long durationMs) {
    }
}
