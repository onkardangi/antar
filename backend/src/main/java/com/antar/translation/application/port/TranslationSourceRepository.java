package com.antar.translation.application.port;

import com.antar.translation.domain.TranslationLanguage;
import com.antar.translation.domain.TranslationProvider;
import com.antar.translation.domain.TranslationSource;
import java.util.Optional;

public interface TranslationSourceRepository {

    Optional<TranslationSource> findByProviderAndLanguage(
            TranslationProvider provider, TranslationLanguage language);

    TranslationSource save(TranslationSource source);
}
