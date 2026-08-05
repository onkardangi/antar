package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.TranslationRepository;
import com.antar.translation.domain.Translation;
import com.antar.translation.domain.TranslationSourceId;
import com.antar.translation.domain.TranslationStatus;
import com.antar.translation.domain.VerseId;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Component;

@Component
class TranslationRepositoryAdapter implements TranslationRepository {

    private final TranslationSpringDataRepository repository;

    TranslationRepositoryAdapter(TranslationSpringDataRepository repository) {
        this.repository = repository;
    }

    @Override
    public Optional<Translation> findPublishedByVerseId(VerseId verseId) {
        // V1 limitation: when multiple published translations exist for one Verse,
        // return the first row ordered by provider ascending. Explicit
        // language/provider selection is deferred (ADR-012).
        return repository
                .findFirstByVerseIdAndPublicationStatusOrderByProviderAsc(
                        verseId.value(), TranslationStatus.PUBLISHED)
                .map(TranslationPersistenceMapper::toDomain);
    }

    @Override
    public List<Translation> findAllBySourceIdAndVerseIds(
            TranslationSourceId sourceId, Collection<VerseId> verseIds) {
        List<UUID> ids = verseIds.stream().map(VerseId::value).toList();
        return repository.findAllByTranslationSourceIdAndVerseIdIn(sourceId.value(), ids).stream()
                .map(TranslationPersistenceMapper::toDomain)
                .toList();
    }

    @Override
    public Optional<Translation> findByVerseIdAndSourceId(VerseId verseId, TranslationSourceId sourceId) {
        return repository
                .findByVerseIdAndTranslationSourceId(verseId.value(), sourceId.value())
                .map(TranslationPersistenceMapper::toDomain);
    }

    @Override
    public void saveAll(List<Translation> translations) {
        for (Translation translation : translations) {
            TranslationJpaEntity entity = repository
                    .findById(translation.id().value())
                    .orElseGet(TranslationJpaEntity::new);
            TranslationPersistenceMapper.copyToEntity(translation, entity);
            repository.save(entity);
        }
    }
}
