package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;

final class ChapterPersistenceMapper {

    private ChapterPersistenceMapper() {
    }

    static Chapter toDomain(ChapterJpaEntity entity) {
        return Chapter.rehydrate(
                ChapterId.of(entity.getId()),
                ChapterNumber.of(entity.getChapterNumber()),
                entity.getCanonicalName(),
                entity.getEnglishName(),
                entity.getShortIntent(),
                entity.getVerseCount(),
                entity.getPublicationStatus(),
                entity.getContentVersion(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    static ChapterJpaEntity toEntity(Chapter chapter) {
        ChapterJpaEntity entity = new ChapterJpaEntity();
        entity.setId(chapter.id().value());
        entity.setChapterNumber((short) chapter.chapterNumber().value());
        entity.setCanonicalName(chapter.canonicalName());
        entity.setEnglishName(chapter.englishName());
        entity.setShortIntent(chapter.shortIntent());
        entity.setVerseCount(chapter.verseCount());
        entity.setPublicationStatus(chapter.publicationStatus());
        entity.setContentVersion(chapter.contentVersion());
        entity.setCreatedAt(chapter.createdAt());
        entity.setUpdatedAt(chapter.updatedAt());
        return entity;
    }

    static void copyToEntity(Chapter chapter, ChapterJpaEntity entity) {
        entity.setChapterNumber((short) chapter.chapterNumber().value());
        entity.setCanonicalName(chapter.canonicalName());
        entity.setEnglishName(chapter.englishName());
        entity.setShortIntent(chapter.shortIntent());
        entity.setVerseCount(chapter.verseCount());
        entity.setPublicationStatus(chapter.publicationStatus());
        entity.setContentVersion(chapter.contentVersion());
        entity.setUpdatedAt(chapter.updatedAt());
    }
}
