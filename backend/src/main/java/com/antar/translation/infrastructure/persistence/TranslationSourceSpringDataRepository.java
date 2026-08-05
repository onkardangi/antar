package com.antar.translation.infrastructure.persistence;

import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface TranslationSourceSpringDataRepository extends JpaRepository<TranslationSourceJpaEntity, UUID> {

    Optional<TranslationSourceJpaEntity> findByProviderAndLanguageCode(String provider, String languageCode);
}
