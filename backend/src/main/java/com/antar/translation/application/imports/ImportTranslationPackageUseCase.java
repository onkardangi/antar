package com.antar.translation.application.imports;

import com.antar.translation.application.port.FailedImportAuditWriter;
import com.antar.translation.application.port.FailedImportAuditWriter.FailedImportAudit;
import com.antar.translation.application.port.PackageFormatValidator;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.application.port.ResolvedTranslationPackage.PackageTranslationRecord;
import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.application.port.TranslationContentPackageRepository.ImportExecutionRecord;
import com.antar.translation.application.port.TranslationPackageReadException;
import com.antar.translation.application.port.TranslationPackageReader;
import com.antar.translation.application.port.TranslationRepository;
import com.antar.translation.application.port.TranslationSourceRepository;
import com.antar.translation.application.port.VerseIdentityLookup;
import com.antar.translation.domain.ContentVersionPolicy;
import com.antar.translation.domain.ContentVersionPolicyException;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import com.antar.translation.domain.Translation;
import com.antar.translation.domain.TranslationLanguage;
import com.antar.translation.domain.TranslationProvider;
import com.antar.translation.domain.TranslationSource;
import com.antar.translation.domain.TranslationStatus;
import com.antar.translation.domain.TranslationText;
import com.antar.translation.domain.TranslationVersion;
import com.antar.translation.domain.VerseId;
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
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Orchestrates Translation Package Format v1 validation and transactional import.
 */
@Service
public class ImportTranslationPackageUseCase {

    public static final int IMPORTER_VERSION = 1;

    private static final Logger log = LoggerFactory.getLogger(ImportTranslationPackageUseCase.class);

    private final PackageFormatValidator packageFormatValidator;
    private final TranslationPackageReader packageReader;
    private final VerseIdentityLookup verseIdentityLookup;
    private final TranslationSourceRepository translationSourceRepository;
    private final TranslationRepository translationRepository;
    private final TranslationContentPackageRepository contentPackageRepository;
    private final TranslationPackageImportMutationService mutationService;
    private final FailedImportAuditWriter failedImportAuditWriter;
    private final ContentVersionPolicy contentVersionPolicy;
    private final Clock clock;

    public ImportTranslationPackageUseCase(
            PackageFormatValidator packageFormatValidator,
            TranslationPackageReader packageReader,
            VerseIdentityLookup verseIdentityLookup,
            TranslationSourceRepository translationSourceRepository,
            TranslationRepository translationRepository,
            TranslationContentPackageRepository contentPackageRepository,
            TranslationPackageImportMutationService mutationService,
            FailedImportAuditWriter failedImportAuditWriter,
            ContentVersionPolicy contentVersionPolicy,
            Clock clock) {
        this.packageFormatValidator = packageFormatValidator;
        this.packageReader = packageReader;
        this.verseIdentityLookup = verseIdentityLookup;
        this.translationSourceRepository = translationSourceRepository;
        this.translationRepository = translationRepository;
        this.contentPackageRepository = contentPackageRepository;
        this.mutationService = mutationService;
        this.failedImportAuditWriter = failedImportAuditWriter;
        this.contentVersionPolicy = contentVersionPolicy;
        this.clock = clock;
    }

    public ImportTranslationPackageResult execute(ImportTranslationPackageCommand command) {
        Objects.requireNonNull(command, "command is required");
        Instant startedAt = clock.instant();
        boolean dryRun = command.dryRun();

        Path packagePath;
        try {
            packagePath = resolvePackagePath(command.packagePath(), dryRun, startedAt);
        } catch (TranslationPackageImportException ex) {
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

        ResolvedTranslationPackage pkg;
        try {
            pkg = packageReader.read(packagePath);
        } catch (TranslationPackageReadException ex) {
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
                    TranslationPackageReadException.STABLE_MESSAGE,
                    validation.warnings());
        }

        try {
            ChangePlan plan = planChanges(pkg, dryRun, startedAt);

            if (dryRun) {
                Duration duration = Duration.between(startedAt, clock.instant());
                logSafeSummary(pkg, plan, ImportExecutionStatus.IMPORTED, true, duration, null);
                return successResult(pkg, validation, plan, true, duration);
            }

            Optional<ImportExecutionRecord> prior =
                    contentPackageRepository.findSuccessfulImport(
                            pkg.packageId(), pkg.packageChecksum());
            if (prior.isPresent()) {
                ImportExecutionRecord existing = prior.get();
                Duration duration = Duration.between(startedAt, clock.instant());
                logSafeSummary(pkg, plan, ImportExecutionStatus.IMPORTED, false, duration, null);
                return new ImportTranslationPackageResult(
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
                ImportTranslationPackageResult result =
                        mutationService.apply(pkg, plan, validation, startedAt);
                logSafeSummary(
                        pkg, plan, ImportExecutionStatus.IMPORTED, false, result.duration(), null);
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
        } catch (TranslationPackageImportException ex) {
            return sanitizeResult(ex.result());
        }
    }

    private ChangePlan planChanges(
            ResolvedTranslationPackage pkg, boolean dryRun, Instant startedAt) {
        if (pkg.recordCount() != pkg.translations().size()
                || pkg.canonicalReferenceRange().expectedCount() != pkg.translations().size()) {
            throw new TranslationPackageImportException(failureResult(
                    pkg.packageId(),
                    pkg.packageChecksum(),
                    emptyPassedValidation(),
                    pkg.translations().size(),
                    0,
                    0,
                    0,
                    pkg.translations().size(),
                    dryRun,
                    startedAt,
                    ImportFailureCode.RECORD_COUNT_MISMATCH,
                    "record count mismatch",
                    List.of()));
        }

        List<String> refs =
                pkg.translations().stream().map(PackageTranslationRecord::canonicalReference).toList();
        Map<String, UUID> verseIds = verseIdentityLookup.findVerseIdsByCanonicalReferences(refs);

        TranslationLanguage language = TranslationLanguage.of(pkg.language());
        TranslationProvider provider = TranslationProvider.of(pkg.provider());
        Instant now = clock.instant();

        Optional<TranslationSource> existingSource =
                translationSourceRepository.findByProviderAndLanguage(provider, language);
        boolean sourceIsNew = existingSource.isEmpty();
        TranslationSource source = existingSource.orElseGet(() -> TranslationSource.create(
                provider,
                pkg.sourceName(),
                language,
                pkg.licenseType(),
                pkg.licenseReference(),
                TranslationStatus.PUBLISHED,
                now));

        List<VerseId> verseIdList = new ArrayList<>();
        for (PackageTranslationRecord record : pkg.translations()) {
            UUID verseUuid = verseIds.get(record.canonicalReference());
            if (verseUuid == null) {
                throw new TranslationPackageImportException(failureResult(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        emptyPassedValidation(),
                        pkg.translations().size(),
                        pkg.translations().size(),
                        0,
                        0,
                        1,
                        dryRun,
                        startedAt,
                        ImportFailureCode.VERSE_IDENTITY_MISSING,
                        "missing Verse identity for " + record.canonicalReference(),
                        List.of()));
            }
            verseIdList.add(VerseId.of(verseUuid));
        }

        Map<VerseId, Translation> existingByVerse = new HashMap<>();
        if (!sourceIsNew) {
            for (Translation existing :
                    translationRepository.findAllBySourceIdAndVerseIds(source.id(), verseIdList)) {
                existingByVerse.put(existing.verseId(), existing);
            }
        }

        List<TranslationChange> changes = new ArrayList<>();
        int updated = 0;
        int unchanged = 0;
        int rejected = 0;

        for (int i = 0; i < pkg.translations().size(); i++) {
            PackageTranslationRecord record = pkg.translations().get(i);
            VerseId verseId = verseIdList.get(i);
            Translation existing = existingByVerse.get(verseId);

            if (existing != null) {
                contentVersionPolicy.assertCompatible(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.contentVersion(),
                        existing);

                boolean sameContent = record.translationText().equals(existing.translationText().value())
                        && existing.contentVersion().value() == pkg.contentVersion()
                        && existing.sourcePackageId().map(pkg.packageId()::equals).orElse(false)
                        && existing
                                .sourcePackageChecksum()
                                .map(pkg.packageChecksum()::equals)
                                .orElse(false);

                if (sameContent) {
                    unchanged++;
                    changes.add(new TranslationChange(existing, record.translationText(), false, false));
                } else {
                    updated++;
                    changes.add(new TranslationChange(existing, record.translationText(), true, false));
                }
            } else {
                updated++;
                Translation created = Translation.create(
                        verseId,
                        source.id(),
                        language,
                        provider,
                        TranslationText.of(record.translationText()),
                        TranslationStatus.PUBLISHED,
                        TranslationVersion.of(pkg.contentVersion()),
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        now);
                changes.add(new TranslationChange(created, record.translationText(), true, true));
            }
        }

        return new ChangePlan(
                pkg.translations().size(),
                pkg.translations().size(),
                updated,
                unchanged,
                rejected,
                source,
                sourceIsNew,
                changes);
    }

    private ImportTranslationPackageResult writeFailedAuditAfterMutation(
            ResolvedTranslationPackage pkg,
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
                pkg, plan, ImportExecutionStatus.FAILED, false, Duration.ofMillis(durationMs), code);
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

    private Path resolvePackagePath(Path packagePath, boolean dryRun, Instant startedAt) {
        try {
            Path normalized = packagePath.toAbsolutePath().normalize();
            if (!Files.exists(normalized) || !Files.isDirectory(normalized)) {
                throw new TranslationPackageImportException(failureResult(
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
        } catch (TranslationPackageImportException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new TranslationPackageImportException(failureResult(
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

    private ImportTranslationPackageResult handlePreMutationFailure(
            ResolvedTranslationPackage pkg,
            PackageValidationResult validation,
            boolean dryRun,
            Instant startedAt,
            ImportFailureCode code,
            String message) {
        Duration duration = Duration.between(startedAt, clock.instant());
        logSafeSummary(
                pkg,
                new ChangePlan(0, 0, 0, 0, 0, null, false, List.of()),
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

    private static ImportTranslationPackageResult sanitizeResult(ImportTranslationPackageResult result) {
        if (result == null || result.failureMessage() == null) {
            return result;
        }
        String sanitized = sanitizeFailureMessage(result.failureMessage(), result.failureCode());
        if (sanitized.equals(result.failureMessage())) {
            return result;
        }
        return new ImportTranslationPackageResult(
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

    private static ImportTranslationPackageResult successResult(
            ResolvedTranslationPackage pkg,
            PackageValidationResult validation,
            ChangePlan plan,
            boolean dryRun,
            Duration duration) {
        return new ImportTranslationPackageResult(
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

    private ImportTranslationPackageResult failureResult(
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
        return new ImportTranslationPackageResult(
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
            ResolvedTranslationPackage pkg,
            ChangePlan plan,
            ImportExecutionStatus status,
            boolean dryRun,
            Duration duration,
            ImportFailureCode failureCode) {
        log.info(
                "translation_package_import packageId={} checksumPrefix={} chapter={} language={} provider={} read={} updated={} unchanged={} rejected={} status={} dryRun={} durationMs={} failureCode={}",
                pkg.packageId(),
                checksumPrefix(pkg.packageChecksum()),
                pkg.chapterNumber(),
                pkg.language(),
                pkg.provider(),
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

    public record TranslationChange(
            Translation translation, String incomingText, boolean updated, boolean created) {
    }

    public record ChangePlan(
            int recordsRead,
            int recordsValidated,
            int recordsUpdated,
            int recordsUnchanged,
            int recordsRejected,
            TranslationSource source,
            boolean sourceIsNew,
            List<TranslationChange> changes) {

        public ChangePlan {
            changes = List.copyOf(changes);
        }
    }
}
