package com.antar.translation.application.imports;

import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.application.port.TranslationContentPackageRepository.ContentPackageRecord;
import com.antar.translation.application.port.TranslationContentPackageRepository.ImportExecutionRecord;
import com.antar.translation.application.port.TranslationRepository;
import com.antar.translation.application.port.TranslationSourceRepository;
import com.antar.translation.domain.ContentPackageStatus;
import com.antar.translation.domain.ContentVersionPolicy;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.Translation;
import com.antar.translation.domain.TranslationText;
import com.antar.translation.domain.TranslationVersion;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Single transactional mutation for a successful Translation package import.
 */
@Service
public class TranslationPackageImportMutationService {

    private final TranslationContentPackageRepository contentPackageRepository;
    private final TranslationSourceRepository translationSourceRepository;
    private final TranslationRepository translationRepository;
    private final ContentVersionPolicy contentVersionPolicy;
    private final ImportMutationProbe importMutationProbe;
    private final Clock clock;

    public TranslationPackageImportMutationService(
            TranslationContentPackageRepository contentPackageRepository,
            TranslationSourceRepository translationSourceRepository,
            TranslationRepository translationRepository,
            ContentVersionPolicy contentVersionPolicy,
            ImportMutationProbe importMutationProbe,
            Clock clock) {
        this.contentPackageRepository = contentPackageRepository;
        this.translationSourceRepository = translationSourceRepository;
        this.translationRepository = translationRepository;
        this.contentVersionPolicy = contentVersionPolicy;
        this.importMutationProbe = importMutationProbe;
        this.clock = clock;
    }

    @Transactional
    public ImportTranslationPackageResult apply(
            ResolvedTranslationPackage pkg,
            ImportTranslationPackageUseCase.ChangePlan plan,
            PackageValidationResult validation,
            Instant startedAt) {
        contentPackageRepository.acquirePackageImportLock(pkg.packageChecksum());

        Optional<ImportExecutionRecord> raced =
                contentPackageRepository.findSuccessfulImport(pkg.packageId(), pkg.packageChecksum());
        if (raced.isPresent()) {
            ImportExecutionRecord existing = raced.get();
            Duration duration = Duration.between(startedAt, clock.instant());
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

        assertPackageIdentityAgainstStore(pkg);

        Instant now = clock.instant();
        Optional<ContentPackageRecord> priorActive = contentPackageRepository.findActiveApproved(
                pkg.language(), pkg.provider(), pkg.scriptureId(), pkg.chapterNumber());
        if (priorActive.isPresent()
                && !priorActive.get().packageId().equals(pkg.packageId())
                && priorActive.get().contentVersion() < pkg.contentVersion()) {
            ContentPackageRecord superseded = priorActive.get();
            contentPackageRepository.savePackage(
                    new ContentPackageRecord(
                            superseded.packageId(),
                            superseded.packageFormatVersion(),
                            superseded.scriptureId(),
                            superseded.chapterNumber(),
                            superseded.languageCode(),
                            superseded.provider(),
                            superseded.contentVersion(),
                            ContentPackageStatus.SUPERSEDED,
                            superseded.packageChecksum(),
                            superseded.manifestChecksum(),
                            superseded.provenanceChecksum(),
                            superseded.translationsChecksum(),
                            superseded.sourceRegistryReferences(),
                            superseded.importerVersion(),
                            superseded.firstImportedAt(),
                            now,
                            superseded.createdAt(),
                            now));
            contentPackageRepository.flush();
        }

        if (plan.sourceIsNew()) {
            translationSourceRepository.save(plan.source());
        }

        contentPackageRepository.savePackage(
                new ContentPackageRecord(
                        pkg.packageId(),
                        pkg.packageFormatVersion(),
                        pkg.scriptureId(),
                        pkg.chapterNumber(),
                        pkg.language(),
                        pkg.provider(),
                        pkg.contentVersion(),
                        ContentPackageStatus.APPROVED,
                        pkg.packageChecksum(),
                        pkg.manifestChecksum(),
                        pkg.provenanceChecksum(),
                        pkg.translationsChecksum(),
                        pkg.sourceRegistryReferences(),
                        ImportTranslationPackageUseCase.IMPORTER_VERSION,
                        now,
                        now,
                        now,
                        now));

        List<Translation> toSave = new ArrayList<>();
        for (ImportTranslationPackageUseCase.TranslationChange change : plan.changes()) {
            if (!change.updated()) {
                continue;
            }
            if (change.created()) {
                toSave.add(change.translation());
            } else {
                toSave.add(change.translation()
                        .withImportedContent(
                                TranslationText.of(change.incomingText()),
                                TranslationVersion.of(pkg.contentVersion()),
                                pkg.packageId(),
                                pkg.packageChecksum(),
                                now));
            }
        }
        if (!toSave.isEmpty()) {
            translationRepository.saveAll(toSave);
        }

        importMutationProbe.afterTranslationsSaved(pkg, List.copyOf(toSave));

        contentPackageRepository.saveImport(
                new ImportExecutionRecord(
                        UUID.randomUUID(),
                        pkg.packageId(),
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        pkg.chapterNumber(),
                        ImportExecutionStatus.IMPORTED,
                        plan.recordsRead(),
                        plan.recordsValidated(),
                        plan.recordsUpdated(),
                        plan.recordsUnchanged(),
                        plan.recordsRejected(),
                        null,
                        null,
                        ImportTranslationPackageUseCase.IMPORTER_VERSION,
                        startedAt,
                        now,
                        Duration.between(startedAt, now).toMillis()));

        Duration duration = Duration.between(startedAt, now);
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
                false,
                duration,
                validation.warnings(),
                null,
                null);
    }

    private void assertPackageIdentityAgainstStore(ResolvedTranslationPackage pkg) {
        contentPackageRepository
                .findByPackageId(pkg.packageId())
                .ifPresent(existing -> contentVersionPolicy.assertPackageIdentity(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        existing.packageId(),
                        existing.packageChecksum()));
        contentPackageRepository
                .findByPackageChecksum(pkg.packageChecksum())
                .ifPresent(existing -> contentVersionPolicy.assertPackageIdentity(
                        pkg.packageId(),
                        pkg.packageChecksum(),
                        existing.packageId(),
                        existing.packageChecksum()));
    }
}
