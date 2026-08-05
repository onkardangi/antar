package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.TranslationLanguage;
import com.antar.translation.domain.TranslationProvider;
import com.antar.translation.domain.TranslationSource;
import com.antar.translation.domain.TranslationSourceId;

final class TranslationSourcePersistenceMapper {

    private TranslationSourcePersistenceMapper() {
    }

    static TranslationSource toDomain(TranslationSourceJpaEntity entity) {
        return TranslationSource.rehydrate(
                TranslationSourceId.of(entity.getId()),
                TranslationProvider.of(entity.getProvider()),
                entity.getName(),
                TranslationLanguage.of(entity.getLanguageCode()),
                entity.getLicenseType(),
                entity.getLicenseReference(),
                entity.getPublicationStatus(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    static void copyToEntity(TranslationSource source, TranslationSourceJpaEntity entity) {
        entity.setId(source.id().value());
        entity.setProvider(source.provider().value());
        entity.setName(source.name());
        entity.setLanguageCode(source.language().code());
        entity.setLicenseType(source.licenseType());
        entity.setLicenseReference(source.licenseReference());
        entity.setPublicationStatus(source.publicationStatus());
        entity.setCreatedAt(source.createdAt());
        entity.setUpdatedAt(source.updatedAt());
    }
}
