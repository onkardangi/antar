package com.antar.translation.application.port;

import com.antar.translation.domain.ImportFailureCode;
import java.time.Instant;

public interface FailedImportAuditWriter {

    void recordFailedImport(FailedImportAudit audit);

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
