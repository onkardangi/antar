package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.PublicationStatus;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface ChapterSpringDataRepository extends JpaRepository<ChapterJpaEntity, UUID> {

    List<ChapterJpaEntity> findAllByPublicationStatusOrderByChapterNumberAsc(
            PublicationStatus publicationStatus);

    Optional<ChapterJpaEntity> findByIdAndPublicationStatus(UUID id, PublicationStatus publicationStatus);

    Optional<ChapterJpaEntity> findByChapterNumberAndPublicationStatus(
            short chapterNumber, PublicationStatus publicationStatus);
}
