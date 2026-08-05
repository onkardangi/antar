package com.antar.translation.infrastructure.config;

import com.antar.translation.application.imports.ImportMutationProbe;
import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.domain.ContentVersionPolicy;
import com.antar.translation.domain.Translation;
import java.time.Clock;
import java.util.List;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
class TranslationImportConfiguration {

    @Bean
    @ConditionalOnMissingBean(Clock.class)
    Clock translationClock() {
        return Clock.systemUTC();
    }

    @Bean
    ContentVersionPolicy translationContentVersionPolicy() {
        return new ContentVersionPolicy();
    }

    @Bean
    @ConditionalOnMissingBean(ImportMutationProbe.class)
    ImportMutationProbe noOpTranslationImportMutationProbe() {
        return NoOpImportMutationProbe.INSTANCE;
    }

    static final class NoOpImportMutationProbe implements ImportMutationProbe {
        static final NoOpImportMutationProbe INSTANCE = new NoOpImportMutationProbe();

        private NoOpImportMutationProbe() {
        }

        @Override
        public void afterTranslationsSaved(ResolvedTranslationPackage pkg, List<Translation> updated) {
            // intentional no-op
        }
    }
}
