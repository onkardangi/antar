package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.CanonicalReference;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.Verse;
import com.antar.scripture.domain.VerseId;
import com.antar.scripture.domain.VerseNumber;

final class VersePersistenceMapper {

    private VersePersistenceMapper() {
    }

    static Verse toDomain(VerseJpaEntity entity) {
        VerseNumber verseNumber = VerseNumber.of(entity.getVerseNumber());
        return Verse.rehydrate(
                VerseId.of(entity.getId()),
                ChapterId.of(entity.getChapterId()),
                verseNumber,
                CanonicalReference.parse(entity.getCanonicalReference()),
                entity.getSanskritText(),
                entity.getPublicationStatus(),
                entity.getContentVersion(),
                entity.getSourcePackageId(),
                entity.getSourcePackageChecksum(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    static VerseJpaEntity toEntity(Verse verse) {
        VerseJpaEntity entity = new VerseJpaEntity();
        copyToEntity(verse, entity);
        return entity;
    }

    static void copyToEntity(Verse verse, VerseJpaEntity entity) {
        entity.setId(verse.id().value());
        entity.setChapterId(verse.chapterId().value());
        entity.setVerseNumber(verse.verseNumber().value());
        entity.setCanonicalReference(verse.canonicalReference().value());
        entity.setSanskritText(verse.sanskritText());
        entity.setContentVersion(verse.contentVersion());
        entity.setSourcePackageId(verse.sourcePackageId().orElse(null));
        entity.setSourcePackageChecksum(verse.sourcePackageChecksum().orElse(null));
        entity.setPublicationStatus(verse.publicationStatus());
        entity.setCreatedAt(verse.createdAt());
        entity.setUpdatedAt(verse.updatedAt());
    }
}
