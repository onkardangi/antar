package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.PublicationStatus;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface VerseSpringDataRepository extends JpaRepository<VerseJpaEntity, UUID> {

    List<VerseJpaEntity> findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
            UUID chapterId, PublicationStatus publicationStatus);

    long countByChapterIdAndPublicationStatus(UUID chapterId, PublicationStatus publicationStatus);

    List<VerseJpaEntity> findAllByChapterIdOrderByVerseNumberAsc(UUID chapterId);

    List<VerseJpaEntity> findAllByCanonicalReferenceIn(Collection<String> canonicalReferences);

    Optional<VerseJpaEntity> findByCanonicalReference(String canonicalReference);
}
