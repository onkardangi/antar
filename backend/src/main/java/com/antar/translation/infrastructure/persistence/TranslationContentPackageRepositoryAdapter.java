package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.domain.ContentPackageStatus;
import com.antar.translation.domain.ImportExecutionStatus;
import jakarta.persistence.EntityManager;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
class TranslationContentPackageRepositoryAdapter implements TranslationContentPackageRepository {

    private final TranslationContentPackageSpringDataRepository packageRepository;
    private final TranslationContentPackageImportSpringDataRepository importRepository;
    private final EntityManager entityManager;

    TranslationContentPackageRepositoryAdapter(
            TranslationContentPackageSpringDataRepository packageRepository,
            TranslationContentPackageImportSpringDataRepository importRepository,
            EntityManager entityManager) {
        this.packageRepository = packageRepository;
        this.importRepository = importRepository;
        this.entityManager = entityManager;
    }

    @Override
    public Optional<ContentPackageRecord> findByPackageId(String packageId) {
        return packageRepository.findById(packageId).map(TranslationContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ContentPackageRecord> findByPackageChecksum(String packageChecksum) {
        return packageRepository
                .findByPackageChecksum(packageChecksum)
                .map(TranslationContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ContentPackageRecord> findActiveApproved(
            String languageCode, String provider, String scriptureId, int chapterNumber) {
        return packageRepository
                .findByLanguageCodeAndProviderAndScriptureIdAndChapterNumberAndPackageStatus(
                        languageCode, provider, scriptureId, chapterNumber, ContentPackageStatus.APPROVED)
                .map(TranslationContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ImportExecutionRecord> findSuccessfulImport(String packageId, String packageChecksum) {
        return importRepository
                .findFirstByPackageIdAndPackageChecksumAndImportStatusOrderByCompletedAtDesc(
                        packageId, packageChecksum, ImportExecutionStatus.IMPORTED)
                .map(TranslationContentPackagePersistenceMapper::toImportRecord);
    }

    @Override
    public void acquirePackageImportLock(String packageChecksum) {
        entityManager
                .createNativeQuery("SELECT pg_advisory_xact_lock(hashtextextended(:checksum, 1))")
                .setParameter("checksum", "translation:" + packageChecksum)
                .getSingleResult();
    }

    @Override
    public ContentPackageRecord savePackage(ContentPackageRecord record) {
        TranslationContentPackageJpaEntity entity = packageRepository
                .findById(record.packageId())
                .orElseGet(TranslationContentPackageJpaEntity::new);
        TranslationContentPackagePersistenceMapper.copyPackage(record, entity);
        return TranslationContentPackagePersistenceMapper.toPackageRecord(packageRepository.save(entity));
    }

    @Override
    public ImportExecutionRecord saveImport(ImportExecutionRecord record) {
        TranslationContentPackageImportJpaEntity entity = new TranslationContentPackageImportJpaEntity();
        TranslationContentPackagePersistenceMapper.copyImport(record, entity);
        return TranslationContentPackagePersistenceMapper.toImportRecord(importRepository.save(entity));
    }

    @Override
    public ImportExecutionRecord saveFailedImport(ImportExecutionRecord record) {
        if (record.packageId() != null) {
            throw new IllegalArgumentException("FAILED import audit must not reference content_packages");
        }
        return saveImport(record);
    }

    @Override
    public void flush() {
        entityManager.flush();
    }
}
