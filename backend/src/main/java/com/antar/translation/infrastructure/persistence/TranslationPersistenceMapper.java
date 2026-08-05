package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.Translation;
import com.antar.translation.domain.TranslationId;
import com.antar.translation.domain.TranslationLanguage;
import com.antar.translation.domain.TranslationProvider;
import com.antar.translation.domain.TranslationSourceId;
import com.antar.translation.domain.TranslationText;
import com.antar.translation.domain.TranslationVersion;
import com.antar.translation.domain.VerseId;

final class TranslationPersistenceMapper {

    private TranslationPersistenceMapper() {
    }

    static Translation toDomain(TranslationJpaEntity entity) {
        return Translation.rehydrate(
                TranslationId.of(entity.getId()),
                VerseId.of(entity.getVerseId()),
                TranslationSourceId.of(entity.getTranslationSourceId()),
                TranslationLanguage.of(entity.getLanguageCode()),
                TranslationProvider.of(entity.getProvider()),
                TranslationText.of(entity.getTranslationText()),
                entity.getPublicationStatus(),
                TranslationVersion.of(entity.getContentVersion()),
                entity.getSourcePackageId(),
                entity.getSourcePackageChecksum(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    static void copyToEntity(Translation translation, TranslationJpaEntity entity) {
        entity.setId(translation.id().value());
        entity.setVerseId(translation.verseId().value());
        entity.setTranslationSourceId(translation.translationSourceId().value());
        entity.setLanguageCode(translation.language().code());
        entity.setProvider(translation.provider().value());
        entity.setTranslationText(translation.translationText().value());
        entity.setPublicationStatus(translation.publicationStatus());
        entity.setContentVersion(translation.contentVersion().value());
        entity.setSourcePackageId(translation.sourcePackageId().orElse(null));
        entity.setSourcePackageChecksum(translation.sourcePackageChecksum().orElse(null));
        entity.setCreatedAt(translation.createdAt());
        entity.setUpdatedAt(translation.updatedAt());
    }
}
