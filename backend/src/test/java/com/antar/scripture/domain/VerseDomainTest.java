package com.antar.scripture.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class VerseDomainTest {

    private static final Instant TIMESTAMP = Instant.parse("2026-08-01T00:00:00Z");

    @Test
    void verseNumberRejectsNonPositiveValues() {
        assertThatThrownBy(() -> VerseNumber.of(0))
                .isInstanceOf(InvalidVerseNumberException.class);
        assertThatThrownBy(() -> VerseNumber.of(-1))
                .isInstanceOf(InvalidVerseNumberException.class);
    }

    @Test
    void verseNumberAcceptsPositiveValues() {
        assertThat(VerseNumber.of(1).value()).isEqualTo(1);
        assertThat(VerseNumber.of(47).value()).isEqualTo(47);
    }

    @Test
    void canonicalReferenceParsesValidReference() {
        CanonicalReference reference = CanonicalReference.parse("2.47");

        assertThat(reference.value()).isEqualTo("2.47");
        assertThat(reference.chapterNumber().value()).isEqualTo(2);
        assertThat(reference.verseNumber().value()).isEqualTo(47);
    }

    @Test
    void canonicalReferenceRejectsInvalidFormats() {
        assertThatThrownBy(() -> CanonicalReference.parse("BG 2.47"))
                .isInstanceOf(InvalidCanonicalReferenceException.class);
        assertThatThrownBy(() -> CanonicalReference.parse("2"))
                .isInstanceOf(InvalidCanonicalReferenceException.class);
        assertThatThrownBy(() -> CanonicalReference.parse(""))
                .isInstanceOf(InvalidCanonicalReferenceException.class);
        assertThatThrownBy(() -> CanonicalReference.parse("19.1"))
                .isInstanceOf(InvalidCanonicalReferenceException.class);
        assertThatThrownBy(() -> CanonicalReference.parse("2.0"))
                .isInstanceOf(InvalidCanonicalReferenceException.class);
    }

    @Test
    void verseRejectsMismatchedCanonicalReferenceVerseNumber() {
        assertThatThrownBy(() -> Verse.rehydrate(
                        VerseId.of(UUID.randomUUID()),
                        ChapterId.of(UUID.randomUUID()),
                        VerseNumber.of(1),
                        CanonicalReference.parse("2.47"),
                        null,
                        PublicationStatus.PUBLISHED,
                        1,
                        TIMESTAMP,
                        TIMESTAMP))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("canonicalReference");
    }

    @Test
    void verseRejectsNonPositiveContentVersion() {
        assertThatThrownBy(() -> Verse.rehydrate(
                        VerseId.of(UUID.randomUUID()),
                        ChapterId.of(UUID.randomUUID()),
                        VerseNumber.of(1),
                        CanonicalReference.parse("1.1"),
                        null,
                        PublicationStatus.PUBLISHED,
                        0,
                        TIMESTAMP,
                        TIMESTAMP))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("contentVersion");
    }

    @Test
    void verseAllowsAbsentSanskritUntilCorpusImport() {
        Verse verse = Verse.rehydrate(
                VerseId.of(UUID.randomUUID()),
                ChapterId.of(UUID.randomUUID()),
                VerseNumber.of(1),
                CanonicalReference.parse("1.1"),
                null,
                PublicationStatus.PUBLISHED,
                1,
                TIMESTAMP,
                TIMESTAMP);

        assertThat(verse.hasSanskritText()).isFalse();
        assertThat(verse.sanskritText()).isNull();
        assertThat(verse.sanskritTextOptional()).isEmpty();
    }

    @Test
    void verseRejectsBlankSanskritText() {
        assertThatThrownBy(() -> Verse.rehydrate(
                        VerseId.of(UUID.randomUUID()),
                        ChapterId.of(UUID.randomUUID()),
                        VerseNumber.of(1),
                        CanonicalReference.parse("1.1"),
                        "   ",
                        PublicationStatus.PUBLISHED,
                        1,
                        TIMESTAMP,
                        TIMESTAMP))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("sanskritText");
    }

    @Test
    void verseAssertsChapterOwnership() {
        Verse verse = Verse.rehydrate(
                VerseId.of(UUID.randomUUID()),
                ChapterId.of(UUID.randomUUID()),
                VerseNumber.of(1),
                CanonicalReference.parse("2.1"),
                null,
                PublicationStatus.PUBLISHED,
                1,
                TIMESTAMP,
                TIMESTAMP);

        verse.assertBelongsTo(ChapterNumber.of(2));

        assertThatThrownBy(() -> verse.assertBelongsTo(ChapterNumber.of(1)))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("does not belong");
    }

    @Test
    void publishedVerseReportsPublished() {
        Verse verse = Verse.rehydrate(
                VerseId.of(UUID.randomUUID()),
                ChapterId.of(UUID.randomUUID()),
                VerseNumber.of(47),
                CanonicalReference.parse("2.47"),
                null,
                PublicationStatus.PUBLISHED,
                1,
                TIMESTAMP,
                TIMESTAMP);

        assertThat(verse.isPublished()).isTrue();
    }

    @Test
    void verseIdRejectsInvalidUuid() {
        assertThatThrownBy(() -> VerseId.of("not-a-uuid"))
                .isInstanceOf(InvalidVerseIdException.class);
    }
}
