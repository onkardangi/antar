package com.antar.scripture.infrastructure.persistence;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.sql.SQLException;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.NestedExceptionUtils;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class ChapterPersistenceIntegrationTest extends AbstractIntegrationTest {

    /**
     * Canonical seed matrix from V003__seed_scripture_chapters.sql.
     * Asserts chapterNumber, canonicalName, and verseCount only — not provisional
     * englishName / shortIntent editorial placeholders.
     */
    private static final List<CanonicalChapterExpectation> CANONICAL_CHAPTERS = List.of(
            new CanonicalChapterExpectation(1, "Arjuna Vishada Yoga", 47),
            new CanonicalChapterExpectation(2, "Sankhya Yoga", 72),
            new CanonicalChapterExpectation(3, "Karma Yoga", 43),
            new CanonicalChapterExpectation(4, "Jnana Karma Sanyasa Yoga", 42),
            new CanonicalChapterExpectation(5, "Karma Sanyasa Yoga", 29),
            new CanonicalChapterExpectation(6, "Atma Samyama Yoga", 47),
            new CanonicalChapterExpectation(7, "Jnana Vijnana Yoga", 30),
            new CanonicalChapterExpectation(8, "Akshara Brahma Yoga", 28),
            new CanonicalChapterExpectation(9, "Raja Vidya Raja Guhya Yoga", 34),
            new CanonicalChapterExpectation(10, "Vibhuti Yoga", 42),
            new CanonicalChapterExpectation(11, "Vishwarupa Darshana Yoga", 55),
            new CanonicalChapterExpectation(12, "Bhakti Yoga", 20),
            new CanonicalChapterExpectation(13, "Kshetra Kshetrajna Vibhaga Yoga", 34),
            new CanonicalChapterExpectation(14, "Gunatraya Vibhaga Yoga", 27),
            new CanonicalChapterExpectation(15, "Purushottama Yoga", 20),
            new CanonicalChapterExpectation(16, "Daivasura Sampad Vibhaga Yoga", 24),
            new CanonicalChapterExpectation(17, "Shraddhatraya Vibhaga Yoga", 28),
            new CanonicalChapterExpectation(18, "Moksha Sanyasa Yoga", 78));

    @Autowired
    private ChapterRepository chapterRepository;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void seededPublishedChaptersAreReturnedInCanonicalOrder() {
        List<Chapter> chapters = chapterRepository.findAllByPublicationStatusOrderByChapterNumberAsc(
                PublicationStatus.PUBLISHED);

        assertThat(chapters).hasSize(18);
        assertThat(chapters)
                .extracting(chapter -> chapter.chapterNumber().value())
                .containsExactly(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18);
    }

    @Test
    void seededChaptersMatchFullCanonicalMatrix() {
        List<Chapter> chapters = chapterRepository.findAllByPublicationStatusOrderByChapterNumberAsc(
                PublicationStatus.PUBLISHED);

        assertThat(chapters).hasSize(18);
        assertThat(chapters)
                .extracting(chapter -> chapter.chapterNumber().value())
                .containsExactly(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18);

        for (int index = 0; index < CANONICAL_CHAPTERS.size(); index++) {
            CanonicalChapterExpectation expected = CANONICAL_CHAPTERS.get(index);
            Chapter actual = chapters.get(index);
            assertThat(actual.chapterNumber().value()).isEqualTo(expected.chapterNumber());
            assertThat(actual.canonicalName()).isEqualTo(expected.canonicalName());
            assertThat(actual.verseCount()).isEqualTo(expected.verseCount());
        }

        int totalVerses = chapters.stream().mapToInt(Chapter::verseCount).sum();
        assertThat(totalVerses).isEqualTo(700);
    }

    @Test
    void unpublishedChaptersAreExcludedFromPublishedQueries() {
        jdbcTemplate.update(
                "UPDATE scripture.chapters SET publication_status = 'DRAFT' WHERE chapter_number = 18");

        try {
            List<Chapter> published = chapterRepository.findAllByPublicationStatusOrderByChapterNumberAsc(
                    PublicationStatus.PUBLISHED);
            assertThat(published).hasSize(17);
            assertThat(published)
                    .noneMatch(chapter -> chapter.chapterNumber().value() == 18);

            assertThat(chapterRepository.findByChapterNumberAndPublicationStatus(
                            ChapterNumber.of(18), PublicationStatus.PUBLISHED))
                    .isEmpty();
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.chapters SET publication_status = 'PUBLISHED' WHERE chapter_number = 18");
        }
    }

    @Test
    void chapterNumberUniquenessIsEnforced() {
        Chapter duplicate = Chapter.rehydrate(
                ChapterId.of(UUID.fromString("018f0000-0000-7000-8000-00000000d002")),
                ChapterNumber.of(1),
                "Duplicate",
                "Duplicate",
                "Duplicate chapter number must fail.",
                10,
                PublicationStatus.DRAFT,
                1,
                Instant.parse("2026-08-02T00:00:00Z"),
                Instant.parse("2026-08-02T00:00:00Z"));

        assertThatThrownBy(() -> chapterRepository.save(duplicate))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    @Transactional
    void verseCountMustBePositiveAtDatabaseLevel() {
        assertThatThrownBy(() -> jdbcTemplate.update(
                        "UPDATE scripture.chapters SET verse_count = 0 WHERE chapter_number = 1"))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> {
                    Throwable root = NestedExceptionUtils.getMostSpecificCause(ex);
                    assertThat(root).isInstanceOf(SQLException.class);
                    assertThat(((SQLException) root).getSQLState()).isEqualTo("23514");
                    assertThat(ex.getMessage()).containsIgnoringCase("verse_count");
                });
    }

    private record CanonicalChapterExpectation(int chapterNumber, String canonicalName, int verseCount) {}
}
