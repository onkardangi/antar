package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.ImportExecutionStatus;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface TranslationContentPackageImportSpringDataRepository
        extends JpaRepository<TranslationContentPackageImportJpaEntity, UUID> {

    Optional<TranslationContentPackageImportJpaEntity>
            findFirstByPackageIdAndPackageChecksumAndImportStatusOrderByCompletedAtDesc(
                    String packageId, String packageChecksum, ImportExecutionStatus importStatus);
}
