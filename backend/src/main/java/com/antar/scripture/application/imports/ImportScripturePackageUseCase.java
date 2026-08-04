package com.antar.scripture.application.imports;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.application.port.ContentPackageRepository.ImportExecutionRecord;
import com.antar.scripture.application.port.FailedImportAuditWriter;
import com.antar.scripture.application.port.FailedImportAuditWriter.FailedImportAudit;
import com.antar.scripture.application.port.PackageFormatValidator;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.application.port.ResolvedScripturePackage;
import com.antar.scripture.application.port.ResolvedScripturePackage.PackageVerseRecord;
import com.antar.scripture.application.port.ScripturePackageReadException;
import com.antar.scripture.application.port.ScripturePackageReader;
import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.ContentVersionPolicy;
import com.antar.scripture.domain.ContentVersionPolicyException;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Orchestrates Package Format v1 validation and transactional import.
 *
 * <p>Successful mutation is one transaction. On mutation failure, all Verse/package changes roll
 * back; a sanitized FAILED audit row may be written afterward in a separate transaction. Dry-run
 * performs zero database writes.
 */
@Service
public class ImportScripturePackageUseCase {

    public static final int IMPORTER_VERSION = 1;

    private static final Logger log = LoggerFactory.getLogger(ImportScripturePackageUseCase.class);

    private final PackageFormatValidator packageFormatValidator;
    private final ScripturePackageReader packageReader;
    private final ChapterRepository chapterRepository;
    private final VerseRepository verseRepository;
    private final ContentPackageRepository contentPackageRepository;
    private final ScripturePackageImportMutationService mutationService;
    private final FailedImportAuditWriter failedImportAuditWriter;
    private final ContentVersionPolicy contentVersionPolicy;
    private final Clock clock;

    public ImportScripturePackageUseCase(
            PackageFormatValidator packageFormatValidator,
            ScripturePackageReader packageReader,
            ChapterRepository chapterRepository,
            VerseRepository verseRepository,
            ContentPackageRepository contentPackageRepository,
            ScripturePackageImportMutationService mutationService,
            FailedImportAuditWriter failedImportAuditWriter,
            ContentVersionPolicy contentVersionPolicy,
            Clock clock) {
        this.packageFormatValidator = packageFormatValidator;
        this.packageReader = packageReader;
        this.chapterRepository = chapterRepository;
        this.verseRepository = verseRepository;
        this.contentPackageRepository = contentPackageRepository;
        this.mutationService = mutationService;
        this.failedImportAuditWriter = failedImportAuditWriter;
        this.contentVersionPolicy = contentVersionPolicy;
        this.clock = clock;
    }

    public ImportScripturePackageResult execute(ImportScripturePackageCommand command) {
        Objects.requireNonNull(command, "command is required");
        Instant startedAt = clock.instant();
        boolean dryRun = command.dryRun();

        Path packagePath;
        try {
            packagePath = resolvePackagePath(command.packagePath(), dryRun, startedAt);
        } catch (ScripturePackageImportException ex) {
            return sanitizeResult(ex.result());
        }

        PackageValidationResult validation =
                packageFormatValidator.validate(packagePath, command.validationOptions());

        if (!validation.mayProceedToImport()) {
            ImportFailureCode code = resolveValidationFailureCode(validation);
            return failureResult(
                    null,
                    null,
                    validation,
                    0,
                    0,
                    0,
                    0,
                    0,
                    dryRun,
                    startedAt,
                    code,
                    summarizeValidationFailure(validation, code),
                    validation.warnings());
        }

        ResolvedScripturePackage pkg;
        try {
            pkg = packageReader.read(packagePath);
        } catch (ScripturePackageReadException ex) {
            return handlePackageReadFailure(validation, dryRun, startedAt);
        }

        try {
            rejectUnsupportedContentLayers(pkg, dryRun, startedAt);
            ChangePlan plan = planChanges(pkg, dryRun, startedAt);

            if (dryRun) {
                Duration duration = Duration.between(startedAt, clock.instant());
                logSafeSummary(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.chapterNumber(),
                        plan,
                        ImportExecutionStatus.IMPORTED,
                        true,
                        duration,
                        null);
                return successResult(pkg, validation, plan, true, duration);
            }

            Optional<ImportExecutionRecord> prior =
                    contentPackageRepository.findSuccessfulImport(
                            pkg.packageId(), pkg.packageChecksum());
            if (prior.isPresent()) {
                ImportExecutionRecord existing = prior.get();
                Duration duration = Duration.between(startedAt, clock.instant());
                logSafeSummary(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.chapterNumber(),
                        plan,
                        ImportExecutionStatus.IMPORTED,
                        false,
                        duration,
                        null);
                return new ImportScripturePackageResult(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        validation,
                        existing.recordsRead(),
                        existing.recordsValidated(),
                        existing.recordsUpdated(),
                        existing.recordsUnchanged(),
                        existing.recordsRejected(),
                        ImportExecutionStatus.IMPORTED,
                        false,
                        duration,
                        validation.warnings(),
                        null,
                        null);
            }

            try {
                ImportScripturePackageResult result =
                        mutationService.apply(pkg, plan, validation, startedAt);
                logSafeSummary(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.chapterNumber(),
                        plan,
                        ImportExecutionStatus.IMPORTED,
                        false,
                        result.duration(),
                        null);
                return result;
            } catch (ContentVersionPolicyException ex) {
                return writeFailedAuditAfterMutation(
                        pkg, plan, validation, startedAt, ex.failureCode(), ex.getMessage());
            } catch (RuntimeException ex) {
                return writeFailedAuditAfterMutation(
                        pkg,
                        plan,
                        validation,
                        startedAt,
                        ImportFailureCode.IMPORT_MUTATION_FAILED,
                        "import mutation failed");
            }
        } catch (ContentVersionPolicyException ex) {
            return handlePreMutationFailure(
                    pkg, validation, dryRun, startedAt, ex.failureCode(), ex.getMessage());
        } catch (ScripturePackageImportException ex) {
            return sanitizeResult(ex.result());
        }
    }

    private ImportScripturePackageResult writeFailedAuditAfterMutation(
            ResolvedScripturePackage pkg,
            ChangePlan plan,
            PackageValidationResult validation,
            Instant startedAt,
            ImportFailureCode code,
            String message) {
        Instant completedAt = clock.instant();
        long durationMs = Duration.between(startedAt, completedAt).toMillis();
        String sanitized = sanitizeFailureMessage(message, code);
        failedImportAuditWriter.recordFailedImport(
                new FailedImportAudit(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.chapterNumber(),
                        code,
                        sanitized,
                        IMPORTER_VERSION,
                        plan.recordsRead(),
                        plan.recordsValidated(),
                        0,
                        0,
                        plan.recordsRejected(),
                        startedAt,
                        completedAt,
                        durationMs));
        logSafeSummary(
                pkg.packageId(),
                pkg.packageChecksum(),
                pkg.chapterNumber(),
                plan,
                ImportExecutionStatus.FAILED,
                false,
                Duration.ofMillis(durationMs),
                code);
        return failureResult(
                pkg.packageId(),
                pkg.packageChecksum(),
                validation,
                plan.recordsRead(),
                plan.recordsValidated(),
                0,
                0,
                plan.recordsRejected(),
                false,
                startedAt,
                code,
                sanitized,
                validation.warnings());
    }

    private ChangePlan planChanges(ResolvedScripturePackage pkg, boolean dryRun, Instant startedAt) {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(
                        ChapterNumber.of(pkg.chapterNumber()), PublicationStatus.PUBLISHED)
                .orElseThrow(() -> new ScripturePackageImportException(failureResult(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        emptyPassedValidation(),
                        pkg.recordCount(),
                        0,
                        0,
                        0,
                        pkg.recordCount(),
                        dryRun,
                        startedAt,
                        ImportFailureCode.CHAPTER_NOT_FOUND,
                        "chapter " + pkg.chapterNumber() + " not found",
                        List.of())));

        if (pkg.recordCount() != pkg.verses().size()
                || pkg.canonicalReferenceRange().expectedCount() != pkg.verses().size()) {
            throw new ScripturePackageImportException(failureResult(
                    pkg.packageId(),
                    pkg.packageChecksum(),
                    emptyPassedValidation(),
                    pkg.verses().size(),
                    0,
                    0,
                    0,
                    pkg.verses().size(),
                    dryRun,
                    startedAt,
                    ImportFailureCode.RECORD_COUNT_MISMATCH,
                    "record count mismatch",
                    List.of()));
        }

        List<String> refs =
                pkg.verses().stream().map(PackageVerseRecord::canonicalReference).toList();
        Map<String, Verse> existingByRef = new HashMap<>();
        for (Verse verse : verseRepository.findAllByCanonicalReferences(refs)) {
            existingByRef.put(verse.canonicalReference().value(), verse);
        }

        List<VerseChange> changes = new ArrayList<>();
        int updated = 0;
        int unchanged = 0;
        int rejected = 0;

        for (PackageVerseRecord record : pkg.verses()) {
            Verse existing = existingByRef.get(record.canonicalReference());
            if (existing == null || !existing.chapterId().equals(chapter.id())) {
                rejected++;
                throw new ScripturePackageImportException(failureResult(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        emptyPassedValidation(),
                        pkg.verses().size(),
                        pkg.verses().size(),
                        0,
                        0,
                        rejected,
                        dryRun,
                        startedAt,
                        ImportFailureCode.VERSE_IDENTITY_MISSING,
                        "missing Verse identity for " + record.canonicalReference(),
                        List.of()));
            }

            contentVersionPolicy.assertCompatible(
                    pkg.packageId(), pkg.packageChecksum(), pkg.contentVersion(), existing);

            boolean sameContent = existing.hasSanskritText()
                    && record.sanskritText().equals(existing.sanskritText())
                    && existing.contentVersion() == pkg.contentVersion()
                    && existing.sourcePackageId().map(pkg.packageId()::equals).orElse(false)
                    && existing
                            .sourcePackageChecksum()
                            .map(pkg.packageChecksum()::equals)
                            .orElse(false);

            if (sameContent) {
                unchanged++;
                changes.add(new VerseChange(existing, record.sanskritText(), false));
            } else {
                updated++;
                changes.add(new VerseChange(existing, record.sanskritText(), true));
            }
        }

        return new ChangePlan(
                pkg.verses().size(), pkg.verses().size(), updated, unchanged, rejected, changes);
    }

    private void rejectUnsupportedContentLayers(
            ResolvedScripturePackage pkg, boolean dryRun, Instant startedAt) {
        for (PackageVerseRecord verse : pkg.verses()) {
            if (verse.hasTransliteration()) {
                throw new ScripturePackageImportException(failureResult(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        emptyPassedValidation(),
                        pkg.verses().size(),
                        0,
                        0,
                        0,
                        pkg.verses().size(),
                        dryRun,
                        startedAt,
                        ImportFailureCode.UNSUPPORTED_CONTENT_LAYER,
                        "transliteration persistence is not implemented; non-null transliteration rejected",
                        List.of()));
            }
        }
    }

    private Path resolvePackagePath(Path packagePath, boolean dryRun, Instant startedAt) {
        try {
            Path normalized = packagePath.toAbsolutePath().normalize();
            if (!Files.exists(normalized) || !Files.isDirectory(normalized)) {
                throw new ScripturePackageImportException(failureResult(
                        null,
                        null,
                        new PackageValidationResult(
                                false, false, false, List.of("invalid package path"), List.of()),
                        0,
                        0,
                        0,
                        0,
                        0,
                        dryRun,
                        startedAt,
                        ImportFailureCode.INVALID_PACKAGE_PATH,
                        "package path must be an existing directory",
                        List.of()));
            }
            return normalized;
        } catch (ScripturePackageImportException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new ScripturePackageImportException(failureResult(
                    null,
                    null,
                    new PackageValidationResult(
                            false, false, false, List.of("invalid package path"), List.of()),
                    0,
                    0,
                    0,
                    0,
                    0,
                    dryRun,
                    startedAt,
                    ImportFailureCode.INVALID_PACKAGE_PATH,
                    "package path could not be resolved",
                    List.of()));
        }
    }

    private ImportScripturePackageResult handlePackageReadFailure(
            PackageValidationResult validation, boolean dryRun, Instant startedAt) {
        return failureResult(
                null,
                null,
                validation,
                0,
                0,
                0,
                0,
                0,
                dryRun,
                startedAt,
                ImportFailureCode.PACKAGE_READ_FAILED,
                ScripturePackageReadException.STABLE_MESSAGE,
                validation.warnings());
    }

    private ImportScripturePackageResult handlePreMutationFailure(
            ResolvedScripturePackage pkg,
            PackageValidationResult validation,
            boolean dryRun,
            Instant startedAt,
            ImportFailureCode code,
            String message) {
        Duration duration = Duration.between(startedAt, clock.instant());
        logSafeSummary(
                pkg.packageId(),
                pkg.packageChecksum(),
                pkg.chapterNumber(),
                new ChangePlan(0, 0, 0, 0, 0, List.of()),
                ImportExecutionStatus.FAILED,
                dryRun,
                duration,
                code);
        return failureResult(
                pkg.packageId(),
                pkg.packageChecksum(),
                validation,
                pkg.recordCount(),
                0,
                0,
                0,
                pkg.recordCount(),
                dryRun,
                startedAt,
                code,
                sanitizeFailureMessage(message, code),
                validation.warnings());
    }

    private static PackageValidationResult emptyPassedValidation() {
        return new PackageValidationResult(true, true, true, List.of(), List.of());
    }

    private static ImportFailureCode resolveValidationFailureCode(PackageValidationResult validation) {
        if (!validation.structurallyValid() || !validation.editoriallyValid()) {
            return ImportFailureCode.PACKAGE_VALIDATION_FAILED;
        }
        if (!validation.warnings().isEmpty() && validation.importable()) {
            return ImportFailureCode.PACKAGE_HAS_WARNINGS;
        }
        if (!validation.importable()) {
            return ImportFailureCode.PACKAGE_NOT_IMPORTABLE;
        }
        return ImportFailureCode.PACKAGE_VALIDATION_FAILED;
    }

    private static String summarizeValidationFailure(
            PackageValidationResult validation, ImportFailureCode code) {
        if (code == ImportFailureCode.PACKAGE_HAS_WARNINGS) {
            return "package validation produced warnings; importer rejects warnings";
        }
        if (!validation.errors().isEmpty()) {
            return "package validation failed: "
                    + ImportFailureSanitizer.sanitize(validation.errors().getFirst(), "validation error");
        }
        return "package is not importable";
    }

    private static String sanitizeFailureMessage(String message, ImportFailureCode code) {
        return ImportFailureSanitizer.sanitize(
                message, code == null ? "import failed" : code.name());
    }

    private static ImportScripturePackageResult sanitizeResult(ImportScripturePackageResult result) {
        if (result == null || result.failureMessage() == null) {
            return result;
        }
        String sanitized = sanitizeFailureMessage(result.failureMessage(), result.failureCode());
        if (sanitized.equals(result.failureMessage())) {
            return result;
        }
        return new ImportScripturePackageResult(
                result.packageId(),
                result.packageChecksum(),
                result.validationResult(),
                result.recordsRead(),
                result.recordsValidated(),
                result.recordsUpdated(),
                result.recordsUnchanged(),
                result.recordsRejected(),
                result.importStatus(),
                result.dryRun(),
                result.duration(),
                result.warnings(),
                result.failureCode(),
                sanitized);
    }

    private static ImportScripturePackageResult successResult(
            ResolvedScripturePackage pkg,
            PackageValidationResult validation,
            ChangePlan plan,
            boolean dryRun,
            Duration duration) {
        return new ImportScripturePackageResult(
                pkg.packageId(),
                pkg.packageChecksum(),
                validation,
                plan.recordsRead(),
                plan.recordsValidated(),
                plan.recordsUpdated(),
                plan.recordsUnchanged(),
                plan.recordsRejected(),
                ImportExecutionStatus.IMPORTED,
                dryRun,
                duration,
                validation.warnings(),
                null,
                null);
    }

    private ImportScripturePackageResult failureResult(
            String packageId,
            String packageChecksum,
            PackageValidationResult validation,
            int read,
            int validated,
            int updated,
            int unchanged,
            int rejected,
            boolean dryRun,
            Instant startedAt,
            ImportFailureCode code,
            String message,
            List<String> warnings) {
        Duration duration = Duration.between(startedAt, clock.instant());
        return new ImportScripturePackageResult(
                packageId,
                packageChecksum,
                validation,
                read,
                validated,
                updated,
                unchanged,
                rejected,
                ImportExecutionStatus.FAILED,
                dryRun,
                duration,
                warnings,
                code,
                sanitizeFailureMessage(message, code));
    }

    private void logSafeSummary(
            String packageId,
            String packageChecksum,
            int chapterNumber,
            ChangePlan plan,
            ImportExecutionStatus status,
            boolean dryRun,
            Duration duration,
            ImportFailureCode failureCode) {
        log.info(
                "scripture_package_import packageId={} checksumPrefix={} chapter={} read={} updated={} unchanged={} rejected={} status={} dryRun={} durationMs={} failureCode={}",
                packageId,
                checksumPrefix(packageChecksum),
                chapterNumber,
                plan.recordsRead(),
                plan.recordsUpdated(),
                plan.recordsUnchanged(),
                plan.recordsRejected(),
                status,
                dryRun,
                duration.toMillis(),
                failureCode);
    }

    private static String checksumPrefix(String checksum) {
        if (checksum == null || checksum.length() < 12) {
            return checksum;
        }
        return checksum.substring(0, 12);
    }

    public record VerseChange(Verse verse, String incomingSanskrit, boolean updated) {
    }

    public record ChangePlan(
            int recordsRead,
            int recordsValidated,
            int recordsUpdated,
            int recordsUnchanged,
            int recordsRejected,
            List<VerseChange> changes) {

        public ChangePlan {
            changes = List.copyOf(changes);
        }
    }
}
