package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import java.util.List;
import org.springframework.stereotype.Component;

@Component
class VerseRepositoryAdapter implements VerseRepository {

    private final VerseSpringDataRepository springDataRepository;

    VerseRepositoryAdapter(VerseSpringDataRepository springDataRepository) {
        this.springDataRepository = springDataRepository;
    }

    @Override
    public List<Verse> findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
            ChapterId chapterId, PublicationStatus publicationStatus) {
        return springDataRepository
                .findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
                        chapterId.value(), publicationStatus)
                .stream()
                .map(VersePersistenceMapper::toDomain)
                .toList();
    }

    @Override
    public long countByChapterIdAndPublicationStatus(
            ChapterId chapterId, PublicationStatus publicationStatus) {
        return springDataRepository.countByChapterIdAndPublicationStatus(
                chapterId.value(), publicationStatus);
    }

    @Override
    public Verse save(Verse verse) {
        VerseJpaEntity entity = springDataRepository
                .findById(verse.id().value())
                .orElseGet(VerseJpaEntity::new);

        if (entity.getId() == null) {
            entity = VersePersistenceMapper.toEntity(verse);
        } else {
            VersePersistenceMapper.copyToEntity(verse, entity);
        }

        return VersePersistenceMapper.toDomain(springDataRepository.save(entity));
    }
}
