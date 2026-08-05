package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.TranslationSourceRepository;
import com.antar.translation.domain.TranslationLanguage;
import com.antar.translation.domain.TranslationProvider;
import com.antar.translation.domain.TranslationSource;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
class TranslationSourceRepositoryAdapter implements TranslationSourceRepository {

    private final TranslationSourceSpringDataRepository repository;

    TranslationSourceRepositoryAdapter(TranslationSourceSpringDataRepository repository) {
        this.repository = repository;
    }

    @Override
    public Optional<TranslationSource> findByProviderAndLanguage(
            TranslationProvider provider, TranslationLanguage language) {
        return repository
                .findByProviderAndLanguageCode(provider.value(), language.code())
                .map(TranslationSourcePersistenceMapper::toDomain);
    }

    @Override
    public TranslationSource save(TranslationSource source) {
        TranslationSourceJpaEntity entity = repository
                .findById(source.id().value())
                .orElseGet(TranslationSourceJpaEntity::new);
        TranslationSourcePersistenceMapper.copyToEntity(source, entity);
        return TranslationSourcePersistenceMapper.toDomain(repository.save(entity));
    }
}
