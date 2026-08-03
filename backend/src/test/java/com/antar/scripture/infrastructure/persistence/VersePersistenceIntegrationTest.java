package com.antar.scripture.infrastructure.persistence;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.NestedExceptionUtils;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class VersePersistenceIntegrationTest extends AbstractIntegrationTest {

    private static final Instant TIMESTAMP = Instant.parse("2026-08-03T00:00:00Z");

    private static final List<CanonicalChapterExpectation> CANONICAL_CHAPTERS = List.of(
            new CanonicalChapterExpectation(1, 47),
            new CanonicalChapterExpectation(2, 72),
            new CanonicalChapterExpectation(3, 43),
            new CanonicalChapterExpectation(4, 42),
            new CanonicalChapterExpectation(5, 29),
            new CanonicalChapterExpectation(6, 47),
            new CanonicalChapterExpectation(7, 30),
            new CanonicalChapterExpectation(8, 28),
            new CanonicalChapterExpectation(9, 34),
            new CanonicalChapterExpectation(10, 42),
            new CanonicalChapterExpectation(11, 55),
            new CanonicalChapterExpectation(12, 20),
            new CanonicalChapterExpectation(13, 34),
            new CanonicalChapterExpectation(14, 27),
            new CanonicalChapterExpectation(15, 20),
            new CanonicalChapterExpectation(16, 24),
            new CanonicalChapterExpectation(17, 28),
            new CanonicalChapterExpectation(18, 78));

    @Autowired
    private VerseRepository verseRepository;

    @Autowired
    private ChapterRepository chapterRepository;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void seededVerseCountsMatchChapterVerseCount() {
        List<Chapter> chapters = chapterRepository.findAllByPublicationStatusOrderByChapterNumberAsc(
                PublicationStatus.PUBLISHED);
        assertThat(chapters).hasSize(18);

        Map<Integer, Integer> expectedByChapter = CANONICAL_CHAPTERS.stream()
                .collect(Collectors.toMap(
                        CanonicalChapterExpectation::chapterNumber,
                        CanonicalChapterExpectation::verseCount));

        int totalVerses = 0;
        for (Chapter chapter : chapters) {
            long count = verseRepository.countByChapterIdAndPublicationStatus(
                    chapter.id(), PublicationStatus.PUBLISHED);
            int expected = expectedByChapter.get(chapter.chapterNumber().value());
            assertThat(count)
                    .as("Chapter %s", chapter.chapterNumber().value())
                    .isEqualTo((long) expected);
            assertThat(count).isEqualTo((long) chapter.verseCount());
            totalVerses += (int) count;
        }

        assertThat(totalVerses).isEqualTo(700);
        Integer databaseTotal = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM scripture.verses", Integer.class);
        assertThat(databaseTotal).isEqualTo(700);
    }

    @Test
    void seededSanskritTextIsNullUntilApprovedCorpusImport() {
        Integer nullSanskritCount = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM scripture.verses WHERE sanskrit_text IS NULL", Integer.class);
        Integer nonNullSanskritCount = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM scripture.verses WHERE sanskrit_text IS NOT NULL", Integer.class);

        assertThat(nullSanskritCount).isEqualTo(700);
        assertThat(nonNullSanskritCount).isEqualTo(0);

        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();
        List<Verse> verses = verseRepository.findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
                chapter.id(), PublicationStatus.PUBLISHED);
        assertThat(verses).isNotEmpty();
        assertThat(verses).allSatisfy(verse -> {
            assertThat(verse.hasSanskritText()).isFalse();
            assertThat(verse.sanskritText()).isNull();
        });
    }

    @Test
    void publishedVersesAreReturnedInCanonicalOrder() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(2), PublicationStatus.PUBLISHED)
                .orElseThrow();

        List<Verse> verses = verseRepository.findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
                chapter.id(), PublicationStatus.PUBLISHED);

        assertThat(verses).hasSize(72);
        assertThat(verses)
                .extracting(verse -> verse.verseNumber().value())
                .containsExactlyElementsOf(IntStream.rangeClosed(1, 72).boxed().toList());
        assertThat(verses.getFirst().canonicalReference().value()).isEqualTo("2.1");
        assertThat(verses.getLast().canonicalReference().value()).isEqualTo("2.72");
    }

    @Test
    void unpublishedVersesAreExcludedFromPublishedQueries() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();

        jdbcTemplate.update(
                "UPDATE scripture.verses SET publication_status = 'DRAFT' WHERE chapter_id = ? AND verse_number = 1",
                chapter.id().value());

        try {
            List<Verse> published = verseRepository.findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
                    chapter.id(), PublicationStatus.PUBLISHED);
            assertThat(published).hasSize(46);
            assertThat(published.getFirst().verseNumber().value()).isEqualTo(2);
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.verses SET publication_status = 'PUBLISHED' WHERE chapter_id = ? AND verse_number = 1",
                    chapter.id().value());
        }
    }

    @Test
    void chapterAndVerseNumberMustBeUnique() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 1, '1.900', NULL, 1, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        chapter.id().value(),
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> assertThat(ex.getMessage())
                        .containsIgnoringCase("chapter_verse_number"));
    }

    @Test
    void canonicalReferenceMustBeUnique() {
        Chapter chapterTwo = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(2), PublicationStatus.PUBLISHED)
                .orElseThrow();

        // Bypass domain validation to assert the database unique constraint alone.
        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 100, '1.1', NULL, 1, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        chapterTwo.id().value(),
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> assertThat(ex.getMessage())
                        .containsIgnoringCase("canonical_reference"));
    }

    @Test
    void verseNumberMustBePositiveAtDatabaseLevel() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 0, '1.999', NULL, 1, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        chapter.id().value(),
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> {
                    Throwable root = NestedExceptionUtils.getMostSpecificCause(ex);
                    assertThat(root).isInstanceOf(SQLException.class);
                    assertThat(ex.getMessage()).containsIgnoringCase("verse_number");
                });
    }

    @Test
    void foreignKeyToChapterIsEnforced() {
        UUID missingChapterId = UUID.fromString("018f0000-0000-7000-8000-00000000dead");

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 1, '99.1', NULL, 1, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        missingChapterId,
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> assertThat(ex.getMessage()).containsIgnoringCase("fk_scripture_verses_chapter"));
    }

    @Test
    void contentVersionMustBePositiveAtDatabaseLevel() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 200, '1.200', NULL, 0, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        chapter.id().value(),
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> assertThat(ex.getMessage()).containsIgnoringCase("content_version"));
    }

    @Test
    void blankSanskritTextIsRejectedAtDatabaseLevel() {
        Chapter chapter = chapterRepository
                .findByChapterNumberAndPublicationStatus(ChapterNumber.of(1), PublicationStatus.PUBLISHED)
                .orElseThrow();

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.verses (
                            id, chapter_id, verse_number, canonical_reference, sanskrit_text,
                            content_version, publication_status, created_at, updated_at
                        ) VALUES (?, ?, 201, '1.201', '   ', 1, 'PUBLISHED', ?, ?)
                        """,
                        UUID.randomUUID(),
                        chapter.id().value(),
                        Timestamp.from(TIMESTAMP),
                        Timestamp.from(TIMESTAMP)))
                .isInstanceOf(DataIntegrityViolationException.class)
                .satisfies(ex -> assertThat(ex.getMessage()).containsIgnoringCase("sanskrit_text"));
    }

    private record CanonicalChapterExpectation(int chapterNumber, int verseCount) {}
}
