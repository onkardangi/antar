package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.application.port.FailedImportAuditWriter;
import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.domain.ImportExecutionStatus;
import java.util.UUID;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/**
 * Persists FAILED import audits without creating {@code content_packages} rows.
 */
@Component
class FailedImportAuditWriterAdapter implements FailedImportAuditWriter {

    private final ContentPackageRepository contentPackageRepository;

    FailedImportAuditWriterAdapter(ContentPackageRepository contentPackageRepository) {
        this.contentPackageRepository = contentPackageRepository;
    }

    @Override
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordFailedImport(FailedImportAudit audit) {
        contentPackageRepository.saveFailedImport(
                new ContentPackageRepository.ImportExecutionRecord(
                        UUID.randomUUID(),
                        null,
                        audit.attemptedPackageId(),
                        audit.packageChecksum(),
                        audit.chapterNumber(),
                        ImportExecutionStatus.FAILED,
                        audit.recordsRead(),
                        audit.recordsValidated(),
                        audit.recordsUpdated(),
                        audit.recordsUnchanged(),
                        audit.recordsRejected(),
                        audit.failureCode(),
                        audit.failureMessage(),
                        audit.importerVersion(),
                        audit.startedAt(),
                        audit.completedAt(),
                        audit.durationMs()));
    }
}
