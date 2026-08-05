package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.FailedImportAuditWriter;
import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.domain.ImportExecutionStatus;
import java.util.UUID;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Component
class TranslationFailedImportAuditWriterAdapter implements FailedImportAuditWriter {

    private final TranslationContentPackageRepository contentPackageRepository;

    TranslationFailedImportAuditWriterAdapter(TranslationContentPackageRepository contentPackageRepository) {
        this.contentPackageRepository = contentPackageRepository;
    }

    @Override
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordFailedImport(FailedImportAudit audit) {
        contentPackageRepository.saveFailedImport(
                new TranslationContentPackageRepository.ImportExecutionRecord(
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
