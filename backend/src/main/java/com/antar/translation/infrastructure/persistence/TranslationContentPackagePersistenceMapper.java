package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.TranslationContentPackageRepository.ContentPackageRecord;
import com.antar.translation.application.port.TranslationContentPackageRepository.ImportExecutionRecord;

final class TranslationContentPackagePersistenceMapper {

    private TranslationContentPackagePersistenceMapper() {
    }

    static ContentPackageRecord toPackageRecord(TranslationContentPackageJpaEntity entity) {
        return new ContentPackageRecord(
                entity.getPackageId(),
                entity.getPackageFormatVersion(),
                entity.getScriptureId(),
                entity.getChapterNumber(),
                entity.getLanguageCode(),
                entity.getProvider(),
                entity.getContentVersion(),
                entity.getPackageStatus(),
                entity.getPackageChecksum(),
                entity.getManifestChecksum(),
                entity.getProvenanceChecksum(),
                entity.getTranslationsChecksum(),
                entity.getSourceRegistryReferences(),
                entity.getImporterVersion(),
                entity.getFirstImportedAt(),
                entity.getLastVerifiedAt(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    static void copyPackage(ContentPackageRecord record, TranslationContentPackageJpaEntity entity) {
        entity.setPackageId(record.packageId());
        entity.setPackageFormatVersion(record.packageFormatVersion());
        entity.setScriptureId(record.scriptureId());
        entity.setChapterNumber(record.chapterNumber());
        entity.setLanguageCode(record.languageCode());
        entity.setProvider(record.provider());
        entity.setContentVersion(record.contentVersion());
        entity.setPackageStatus(record.packageStatus());
        entity.setPackageChecksum(record.packageChecksum());
        entity.setManifestChecksum(record.manifestChecksum());
        entity.setProvenanceChecksum(record.provenanceChecksum());
        entity.setTranslationsChecksum(record.translationsChecksum());
        entity.setSourceRegistryReferences(record.sourceRegistryReferences());
        entity.setImporterVersion(record.importerVersion());
        entity.setFirstImportedAt(record.firstImportedAt());
        entity.setLastVerifiedAt(record.lastVerifiedAt());
        entity.setCreatedAt(record.createdAt());
        entity.setUpdatedAt(record.updatedAt());
    }

    static ImportExecutionRecord toImportRecord(TranslationContentPackageImportJpaEntity entity) {
        return new ImportExecutionRecord(
                entity.getId(),
                entity.getPackageId(),
                entity.getAttemptedPackageId(),
                entity.getPackageChecksum(),
                entity.getChapterNumber(),
                entity.getImportStatus(),
                entity.getRecordsRead(),
                entity.getRecordsValidated(),
                entity.getRecordsUpdated(),
                entity.getRecordsUnchanged(),
                entity.getRecordsRejected(),
                entity.getFailureCode(),
                entity.getFailureMessage(),
                entity.getImporterVersion(),
                entity.getStartedAt(),
                entity.getCompletedAt(),
                entity.getDurationMs());
    }

    static void copyImport(ImportExecutionRecord record, TranslationContentPackageImportJpaEntity entity) {
        entity.setId(record.id());
        entity.setPackageId(record.packageId());
        entity.setAttemptedPackageId(record.attemptedPackageId());
        entity.setPackageChecksum(record.packageChecksum());
        entity.setChapterNumber(record.chapterNumber());
        entity.setImportStatus(record.importStatus());
        entity.setRecordsRead(record.recordsRead());
        entity.setRecordsValidated(record.recordsValidated());
        entity.setRecordsUpdated(record.recordsUpdated());
        entity.setRecordsUnchanged(record.recordsUnchanged());
        entity.setRecordsRejected(record.recordsRejected());
        entity.setFailureCode(record.failureCode());
        entity.setFailureMessage(record.failureMessage());
        entity.setImporterVersion(record.importerVersion());
        entity.setStartedAt(record.startedAt());
        entity.setCompletedAt(record.completedAt());
        entity.setDurationMs(record.durationMs());
    }
}
