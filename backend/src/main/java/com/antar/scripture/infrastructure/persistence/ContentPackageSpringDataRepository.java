package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.ContentPackageStatus;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

interface ContentPackageSpringDataRepository extends JpaRepository<ContentPackageJpaEntity, String> {

    Optional<ContentPackageJpaEntity> findByPackageChecksum(String packageChecksum);

    Optional<ContentPackageJpaEntity> findByChapterNumberAndPackageStatus(
            int chapterNumber, ContentPackageStatus packageStatus);

    Optional<ContentPackageJpaEntity> findByScriptureIdAndChapterNumberAndPackageStatus(
            String scriptureId, int chapterNumber, ContentPackageStatus packageStatus);
}
