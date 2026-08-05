package com.antar.scripture.application.verse.query;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.CanonicalReference;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import com.antar.scripture.domain.VerseId;
import com.antar.scripture.domain.VerseNumber;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class VerseQueryServiceTest {

    private static final Instant TIMESTAMP = Instant.parse("2026-08-01T00:00:00Z");
    private static final ChapterId CHAPTER_ID =
            ChapterId.of(UUID.fromString("018f0000-0000-7000-8000-000000000001"));
    private static final VerseId VERSE_ID =
            VerseId.of(UUID.fromString("018f0000-0000-7000-8000-000000000101"));

    @Mock
    private ChapterRepository chapterRepository;

    @Mock
    private VerseRepository verseRepository;

    private VerseQueryService verseQueryService;

    @BeforeEach
    void setUp() {
        verseQueryService = new VerseQueryService(chapterRepository, verseRepository);
    }

    @Test
    void getPublishedVerseDetailReturnsCanonicalFieldsWhenSanskritIsPresent() {
        when(verseRepository.findByIdAndPublicationStatus(VERSE_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.of(verseWithSanskrit("धर्मक्षेत्रे कुरुक्षेत्रे")));
        when(chapterRepository.findByIdAndPublicationStatus(CHAPTER_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.of(publishedChapter()));

        VerseDetailView view = verseQueryService.getPublishedVerseDetail(VERSE_ID);

        assertThat(view.id()).isEqualTo(VERSE_ID.value());
        assertThat(view.chapterId()).isEqualTo(CHAPTER_ID.value());
        assertThat(view.chapterNumber()).isEqualTo(1);
        assertThat(view.verseNumber()).isEqualTo(1);
        assertThat(view.canonicalReference()).isEqualTo("1.1");
        assertThat(view.sanskritText()).isEqualTo("धर्मक्षेत्रे कुरुक्षेत्रे");
        assertThat(view.contentVersion()).isEqualTo(2L);
    }

    @Test
    void getPublishedVerseDetailThrowsWhenVerseIsUnknown() {
        when(verseRepository.findByIdAndPublicationStatus(VERSE_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.empty());

        assertThatThrownBy(() -> verseQueryService.getPublishedVerseDetail(VERSE_ID))
                .isInstanceOf(VerseNotFoundException.class)
                .hasMessageContaining(VERSE_ID.toString());

        verifyNoInteractions(chapterRepository);
    }

    @Test
    void getPublishedVerseDetailThrowsWhenSanskritIsMissing() {
        when(verseRepository.findByIdAndPublicationStatus(VERSE_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.of(verseWithoutSanskrit()));

        assertThatThrownBy(() -> verseQueryService.getPublishedVerseDetail(VERSE_ID))
                .isInstanceOf(VerseNotFoundException.class)
                .hasMessageContaining("no imported Sanskrit");

        verifyNoInteractions(chapterRepository);
    }

    @Test
    void getPublishedVerseDetailThrowsWhenChapterIsUnavailable() {
        when(verseRepository.findByIdAndPublicationStatus(VERSE_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.of(verseWithSanskrit("धर्मक्षेत्रे कुरुक्षेत्रे")));
        when(chapterRepository.findByIdAndPublicationStatus(CHAPTER_ID, PublicationStatus.PUBLISHED))
                .thenReturn(Optional.empty());

        assertThatThrownBy(() -> verseQueryService.getPublishedVerseDetail(VERSE_ID))
                .isInstanceOf(VerseNotFoundException.class)
                .hasMessageContaining("chapter is unavailable");
    }

    private static Verse verseWithSanskrit(String sanskrit) {
        return Verse.rehydrate(
                VERSE_ID,
                CHAPTER_ID,
                VerseNumber.of(1),
                CanonicalReference.parse("1.1"),
                sanskrit,
                PublicationStatus.PUBLISHED,
                2L,
                TIMESTAMP,
                TIMESTAMP);
    }

    private static Verse verseWithoutSanskrit() {
        return Verse.rehydrate(
                VERSE_ID,
                CHAPTER_ID,
                VerseNumber.of(1),
                CanonicalReference.parse("1.1"),
                null,
                PublicationStatus.PUBLISHED,
                1L,
                TIMESTAMP,
                TIMESTAMP);
    }

    private static Chapter publishedChapter() {
        return Chapter.rehydrate(
                CHAPTER_ID,
                ChapterNumber.of(1),
                "Arjuna Vishada Yoga",
                "The Yoga of Arjuna's Despair",
                "Grief, conflict, and the beginning of inquiry.",
                47,
                PublicationStatus.PUBLISHED,
                1L,
                TIMESTAMP,
                TIMESTAMP);
    }
}
