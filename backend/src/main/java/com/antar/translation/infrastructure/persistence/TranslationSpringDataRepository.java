package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.TranslationStatus;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface TranslationSpringDataRepository extends JpaRepository<TranslationJpaEntity, UUID> {

    Optional<TranslationJpaEntity> findFirstByVerseIdAndPublicationStatusOrderByProviderAsc(
            UUID verseId, TranslationStatus publicationStatus);

    List<TranslationJpaEntity> findAllByTranslationSourceIdAndVerseIdIn(
            UUID translationSourceId, Collection<UUID> verseIds);

    Optional<TranslationJpaEntity> findByVerseIdAndTranslationSourceId(
            UUID verseId, UUID translationSourceId);
}
