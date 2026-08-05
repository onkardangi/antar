package com.antar.translation.application.imports;

import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import java.time.Duration;
import java.util.List;
import java.util.Optional;

public record ImportTranslationPackageResult(
        String packageId,
        String packageChecksum,
        PackageValidationResult validationResult,
        int recordsRead,
        int recordsValidated,
        int recordsUpdated,
        int recordsUnchanged,
        int recordsRejected,
        ImportExecutionStatus importStatus,
        boolean dryRun,
        Duration duration,
        List<String> warnings,
        ImportFailureCode failureCode,
        String failureMessage) {

    public ImportTranslationPackageResult {
        warnings = warnings == null ? List.of() : List.copyOf(warnings);
        duration = duration == null ? Duration.ZERO : duration;
    }

    public boolean succeeded() {
        return importStatus == ImportExecutionStatus.IMPORTED && failureCode == null;
    }

    public Optional<ImportFailureCode> failureCodeOptional() {
        return Optional.ofNullable(failureCode);
    }

    public Optional<String> failureMessageOptional() {
        return Optional.ofNullable(failureMessage);
    }
}
