package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.domain.ContentPackageStatus;
import com.antar.scripture.domain.ImportExecutionStatus;
import jakarta.persistence.EntityManager;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
class ContentPackageRepositoryAdapter implements ContentPackageRepository {

    private final ContentPackageSpringDataRepository packageRepository;
    private final ContentPackageImportSpringDataRepository importRepository;
    private final EntityManager entityManager;

    ContentPackageRepositoryAdapter(
            ContentPackageSpringDataRepository packageRepository,
            ContentPackageImportSpringDataRepository importRepository,
            EntityManager entityManager) {
        this.packageRepository = packageRepository;
        this.importRepository = importRepository;
        this.entityManager = entityManager;
    }

    @Override
    public Optional<ContentPackageRecord> findByPackageId(String packageId) {
        return packageRepository.findById(packageId).map(ContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ContentPackageRecord> findByPackageChecksum(String packageChecksum) {
        return packageRepository
                .findByPackageChecksum(packageChecksum)
                .map(ContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ContentPackageRecord> findActiveApprovedByChapterNumber(int chapterNumber) {
        return packageRepository
                .findByChapterNumberAndPackageStatus(chapterNumber, ContentPackageStatus.APPROVED)
                .map(ContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ContentPackageRecord> findActiveApprovedByScriptureAndChapter(
            String scriptureId, int chapterNumber) {
        return packageRepository
                .findByScriptureIdAndChapterNumberAndPackageStatus(
                        scriptureId, chapterNumber, ContentPackageStatus.APPROVED)
                .map(ContentPackagePersistenceMapper::toPackageRecord);
    }

    @Override
    public Optional<ImportExecutionRecord> findSuccessfulImport(String packageId, String packageChecksum) {
        return importRepository
                .findFirstByPackageIdAndPackageChecksumAndImportStatusOrderByCompletedAtDesc(
                        packageId, packageChecksum, ImportExecutionStatus.IMPORTED)
                .map(ContentPackagePersistenceMapper::toImportRecord);
    }

    @Override
    public void acquirePackageImportLock(String packageChecksum) {
        entityManager
                .createNativeQuery("SELECT pg_advisory_xact_lock(hashtextextended(:checksum, 0))")
                .setParameter("checksum", packageChecksum)
                .getSingleResult();
    }

    @Override
    public ContentPackageRecord savePackage(ContentPackageRecord record) {
        ContentPackageJpaEntity entity = packageRepository
                .findById(record.packageId())
                .orElseGet(ContentPackageJpaEntity::new);
        ContentPackagePersistenceMapper.copyPackage(record, entity);
        return ContentPackagePersistenceMapper.toPackageRecord(packageRepository.save(entity));
    }

    @Override
    public ImportExecutionRecord saveImport(ImportExecutionRecord record) {
        ContentPackageImportJpaEntity entity = new ContentPackageImportJpaEntity();
        ContentPackagePersistenceMapper.copyImport(record, entity);
        return ContentPackagePersistenceMapper.toImportRecord(importRepository.save(entity));
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
