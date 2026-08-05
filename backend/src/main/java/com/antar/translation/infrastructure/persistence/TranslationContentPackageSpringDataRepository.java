package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.ContentPackageStatus;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

interface TranslationContentPackageSpringDataRepository
        extends JpaRepository<TranslationContentPackageJpaEntity, String> {

    Optional<TranslationContentPackageJpaEntity> findByPackageChecksum(String packageChecksum);

    Optional<TranslationContentPackageJpaEntity>
            findByLanguageCodeAndProviderAndScriptureIdAndChapterNumberAndPackageStatus(
                    String languageCode,
                    String provider,
                    String scriptureId,
                    int chapterNumber,
                    ContentPackageStatus packageStatus);
}
