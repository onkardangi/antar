package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
class ChapterRepositoryAdapter implements ChapterRepository {

    private final ChapterSpringDataRepository springDataRepository;

    ChapterRepositoryAdapter(ChapterSpringDataRepository springDataRepository) {
        this.springDataRepository = springDataRepository;
    }

    @Override
    public List<Chapter> findAllByPublicationStatusOrderByChapterNumberAsc(
            PublicationStatus publicationStatus) {
        return springDataRepository
                .findAllByPublicationStatusOrderByChapterNumberAsc(publicationStatus)
                .stream()
                .map(ChapterPersistenceMapper::toDomain)
                .toList();
    }

    @Override
    public Optional<Chapter> findByIdAndPublicationStatus(
            ChapterId chapterId, PublicationStatus publicationStatus) {
        return springDataRepository
                .findByIdAndPublicationStatus(chapterId.value(), publicationStatus)
                .map(ChapterPersistenceMapper::toDomain);
    }

    @Override
    public Optional<Chapter> findByChapterNumberAndPublicationStatus(
            ChapterNumber chapterNumber, PublicationStatus publicationStatus) {
        return springDataRepository
                .findByChapterNumberAndPublicationStatus((short) chapterNumber.value(), publicationStatus)
                .map(ChapterPersistenceMapper::toDomain);
    }

    @Override
    public Chapter save(Chapter chapter) {
        ChapterJpaEntity entity = springDataRepository
                .findById(chapter.id().value())
                .orElseGet(ChapterJpaEntity::new);

        if (entity.getId() == null) {
            entity = ChapterPersistenceMapper.toEntity(chapter);
        } else {
            ChapterPersistenceMapper.copyToEntity(chapter, entity);
        }

        return ChapterPersistenceMapper.toDomain(springDataRepository.save(entity));
    }
}
