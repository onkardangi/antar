package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
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
    public List<Verse> findAllByChapterIdOrderByVerseNumberAsc(ChapterId chapterId) {
        return springDataRepository.findAllByChapterIdOrderByVerseNumberAsc(chapterId.value()).stream()
                .map(VersePersistenceMapper::toDomain)
                .toList();
    }

    @Override
    public List<Verse> findAllByCanonicalReferences(Collection<String> canonicalReferences) {
        if (canonicalReferences == null || canonicalReferences.isEmpty()) {
            return List.of();
        }
        return springDataRepository.findAllByCanonicalReferenceIn(canonicalReferences).stream()
                .map(VersePersistenceMapper::toDomain)
                .toList();
    }

    @Override
    public Optional<Verse> findByCanonicalReference(String canonicalReference) {
        return springDataRepository
                .findByCanonicalReference(canonicalReference)
                .map(VersePersistenceMapper::toDomain);
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

    @Override
    public void saveAll(Collection<Verse> verses) {
        for (Verse verse : verses) {
            save(verse);
        }
    }
}
