package com.antar.scripture.application.imports;

import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.application.port.ContentPackageRepository.ContentPackageRecord;
import com.antar.scripture.application.port.ContentPackageRepository.ImportExecutionRecord;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.application.port.ResolvedScripturePackage;
import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.ContentPackageStatus;
import com.antar.scripture.domain.ContentVersionPolicy;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.Verse;
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
 * Single transactional mutation for a successful Scripture package import.
 */
@Service
public class ScripturePackageImportMutationService {

    private final ContentPackageRepository contentPackageRepository;
    private final VerseRepository verseRepository;
    private final ContentVersionPolicy contentVersionPolicy;
    private final ImportMutationProbe importMutationProbe;
    private final Clock clock;

    public ScripturePackageImportMutationService(
            ContentPackageRepository contentPackageRepository,
            VerseRepository verseRepository,
            ContentVersionPolicy contentVersionPolicy,
            ImportMutationProbe importMutationProbe,
            Clock clock) {
        this.contentPackageRepository = contentPackageRepository;
        this.verseRepository = verseRepository;
        this.contentVersionPolicy = contentVersionPolicy;
        this.importMutationProbe = importMutationProbe;
        this.clock = clock;
    }

    @Transactional
    public ImportScripturePackageResult apply(
            ResolvedScripturePackage pkg,
            ImportScripturePackageUseCase.ChangePlan plan,
            PackageValidationResult validation,
            Instant startedAt) {
        contentPackageRepository.acquirePackageImportLock(pkg.packageChecksum());

        Optional<ImportExecutionRecord> raced =
                contentPackageRepository.findSuccessfulImport(pkg.packageId(), pkg.packageChecksum());
        if (raced.isPresent()) {
            ImportExecutionRecord existing = raced.get();
            Duration duration = Duration.between(startedAt, clock.instant());
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

        assertPackageIdentityAgainstStore(pkg);

        Instant now = clock.instant();
        Optional<ContentPackageRecord> priorActive =
                contentPackageRepository.findActiveApprovedByScriptureAndChapter(
                        pkg.scriptureId(), pkg.chapterNumber());
        if (priorActive.isEmpty()) {
            priorActive = contentPackageRepository.findActiveApprovedByChapterNumber(pkg.chapterNumber());
        }
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
                            superseded.contentVersion(),
                            ContentPackageStatus.SUPERSEDED,
                            superseded.packageChecksum(),
                            superseded.manifestChecksum(),
                            superseded.provenanceChecksum(),
                            superseded.versesChecksum(),
                            superseded.sourceRegistryReferences(),
                            superseded.importerVersion(),
                            superseded.firstImportedAt(),
                            now,
                            superseded.createdAt(),
                            now));
            // Flush so the partial unique APPROVED index allows the new package insert.
            contentPackageRepository.flush();
        }

        contentPackageRepository.savePackage(
                new ContentPackageRecord(
                        pkg.packageId(),
                        pkg.packageFormatVersion(),
                        pkg.scriptureId(),
                        pkg.chapterNumber(),
                        pkg.contentVersion(),
                        ContentPackageStatus.APPROVED,
                        pkg.packageChecksum(),
                        pkg.manifestChecksum(),
                        pkg.provenanceChecksum(),
                        pkg.versesChecksum(),
                        pkg.sourceRegistryReferences(),
                        ImportScripturePackageUseCase.IMPORTER_VERSION,
                        now,
                        now,
                        now,
                        now));

        List<Verse> updated = new ArrayList<>();
        for (ImportScripturePackageUseCase.VerseChange change : plan.changes()) {
            if (change.updated()) {
                updated.add(change.verse()
                        .withImportedContent(
                                change.incomingSanskrit(),
                                pkg.contentVersion(),
                                pkg.packageId(),
                                pkg.packageChecksum(),
                                now));
            }
        }
        if (!updated.isEmpty()) {
            verseRepository.saveAll(updated);
        }

        // Deterministic post-save hook for tests to force mid-mutation failure after Verse writes.
        importMutationProbe.afterVersesSaved(pkg, List.copyOf(updated));

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
                        ImportScripturePackageUseCase.IMPORTER_VERSION,
                        startedAt,
                        now,
                        Duration.between(startedAt, now).toMillis()));

        Duration duration = Duration.between(startedAt, now);
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
                false,
                duration,
                validation.warnings(),
                null,
                null);
    }

    private void assertPackageIdentityAgainstStore(ResolvedScripturePackage pkg) {
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
