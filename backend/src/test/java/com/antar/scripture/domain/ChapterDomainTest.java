package com.antar.scripture.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class ChapterDomainTest {

    @Test
    void chapterNumberAcceptsCanonicalRange() {
        assertThat(ChapterNumber.of(1).value()).isEqualTo(1);
        assertThat(ChapterNumber.of(18).value()).isEqualTo(18);
    }

    @Test
    void chapterNumberRejectsValuesOutsideCanonicalRange() {
        assertThatThrownBy(() -> ChapterNumber.of(0))
                .isInstanceOf(InvalidChapterNumberException.class);
        assertThatThrownBy(() -> ChapterNumber.of(19))
                .isInstanceOf(InvalidChapterNumberException.class);
    }

    @Test
    void chapterRejectsNonPositiveVerseCount() {
        assertThatThrownBy(() -> Chapter.rehydrate(
                        ChapterId.of(UUID.randomUUID()),
                        ChapterNumber.of(1),
                        "Arjuna Vishada Yoga",
                        "The Yoga of Arjuna's Despair",
                        "A battlefield crisis becomes the beginning of inquiry.",
                        0,
                        PublicationStatus.PUBLISHED,
                        1,
                        Instant.parse("2026-08-01T00:00:00Z"),
                        Instant.parse("2026-08-01T00:00:00Z")))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("verseCount");
    }

    @Test
    void publishedChapterReportsPublished() {
        Chapter chapter = Chapter.rehydrate(
                ChapterId.of(UUID.randomUUID()),
                ChapterNumber.of(2),
                "Sankhya Yoga",
                "The Yoga of Knowledge",
                "Action, wisdom, duty, and steadiness.",
                72,
                PublicationStatus.PUBLISHED,
                1,
                Instant.parse("2026-08-01T00:00:00Z"),
                Instant.parse("2026-08-01T00:00:00Z"));

        assertThat(chapter.isPublished()).isTrue();
    }

    @Test
    void chapterIdRejectsInvalidUuid() {
        assertThatThrownBy(() -> ChapterId.of("not-a-uuid"))
                .isInstanceOf(InvalidChapterIdException.class);
    }
}
