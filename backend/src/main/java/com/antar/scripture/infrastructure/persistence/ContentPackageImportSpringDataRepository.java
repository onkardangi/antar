package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.ImportExecutionStatus;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface ContentPackageImportSpringDataRepository
        extends JpaRepository<ContentPackageImportJpaEntity, UUID> {

    Optional<ContentPackageImportJpaEntity>
            findFirstByPackageIdAndPackageChecksumAndImportStatusOrderByCompletedAtDesc(
                    String packageId, String packageChecksum, ImportExecutionStatus importStatus);
}
