package com.antar.scripture.infrastructure.config;

import com.antar.scripture.application.imports.ImportMutationProbe;
import com.antar.scripture.domain.ContentVersionPolicy;
import java.time.Clock;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
class ScriptureImportConfiguration {

    @Bean
    Clock scriptureClock() {
        return Clock.systemUTC();
    }

    @Bean
    ContentVersionPolicy contentVersionPolicy() {
        return new ContentVersionPolicy();
    }

    /**
     * Production always registers a no-op probe. Tests may supply a {@code @Primary} replacement
     * for mid-mutation rollback proofs. No production property enables a crashing probe.
     */
    @Bean
    @ConditionalOnMissingBean(ImportMutationProbe.class)
    ImportMutationProbe noOpImportMutationProbe() {
        return NoOpImportMutationProbe.INSTANCE;
    }

    /** Final no-op implementation — not overridable except by replacing the Spring bean in tests. */
    static final class NoOpImportMutationProbe implements ImportMutationProbe {
        static final NoOpImportMutationProbe INSTANCE = new NoOpImportMutationProbe();

        private NoOpImportMutationProbe() {
        }

        @Override
        public void afterVersesSaved(
                com.antar.scripture.application.port.ResolvedScripturePackage pkg,
                java.util.List<com.antar.scripture.domain.Verse> updatedVerses) {
            // intentional no-op
        }
    }
}
