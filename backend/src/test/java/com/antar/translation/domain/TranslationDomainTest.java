package com.antar.translation.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class TranslationDomainTest {

    @Test
    void createsPublishedTranslationWithLineage() {
        Instant now = Instant.parse("2026-08-04T00:00:00Z");
        Translation translation = Translation.create(
                VerseId.of(UUID.fromString("01900000-0000-7000-8000-000000000001")),
                TranslationSourceId.generate(),
                TranslationLanguage.of("en"),
                TranslationProvider.of("FIXTURE_PROVIDER"),
                TranslationText.of("FIXTURE_TRANSLATION_VERSE_1"),
                TranslationStatus.PUBLISHED,
                TranslationVersion.of(1),
                "fixture-package",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                now);

        assertThat(translation.isPublished()).isTrue();
        assertThat(translation.translationText().value()).isEqualTo("FIXTURE_TRANSLATION_VERSE_1");
        assertThat(translation.sourcePackageId()).contains("fixture-package");
    }

    @Test
    void rejectsBlankTranslationText() {
        assertThatThrownBy(() -> TranslationText.of("  "))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void rejectsNonPositiveVersion() {
        assertThatThrownBy(() -> TranslationVersion.of(0))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
