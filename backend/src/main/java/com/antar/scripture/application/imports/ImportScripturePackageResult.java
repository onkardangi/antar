package com.antar.scripture.application.imports;

import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import java.time.Duration;
import java.util.List;
import java.util.Optional;

/**
 * Result of a Scripture package import attempt.
 *
 * <p>Never includes Verse Sanskrit text.
 */
public record ImportScripturePackageResult(
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

    public ImportScripturePackageResult {
        warnings = warnings == null ? List.of() : List.copyOf(warnings);
    }

    public Optional<ImportFailureCode> failureCodeOptional() {
        return Optional.ofNullable(failureCode);
    }

    public Optional<String> failureMessageOptional() {
        return Optional.ofNullable(failureMessage);
    }

    public boolean succeeded() {
        return importStatus == ImportExecutionStatus.IMPORTED && failureCode == null;
    }
}
