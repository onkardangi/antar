package com.antar.scripture.application.verse.query;

import com.antar.scripture.application.chapter.query.ChapterNotFoundException;
import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.application.port.VerseRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import com.antar.scripture.domain.VerseId;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class VerseQueryService {

    /**
     * Temporary Chapter-screen preview until Translation content exists.
     * API-derived only — never persisted, never treated as Scripture, and never a substitute
     * for {@code sanskrit_text}.
     */
    public static final String PLACEHOLDER_PREVIEW_TEXT = "Verse preview unavailable";

    private final ChapterRepository chapterRepository;
    private final VerseRepository verseRepository;

    public VerseQueryService(ChapterRepository chapterRepository, VerseRepository verseRepository) {
        this.chapterRepository = chapterRepository;
        this.verseRepository = verseRepository;
    }

    public List<VerseView> listPublishedVersesForChapter(ChapterId chapterId) {
        Chapter chapter = chapterRepository
                .findByIdAndPublicationStatus(chapterId, PublicationStatus.PUBLISHED)
                .orElseThrow(() -> new ChapterNotFoundException(chapterId));

        List<Verse> verses = verseRepository.findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
                chapter.id(), PublicationStatus.PUBLISHED);

        if (verses.isEmpty()) {
            throw new ChapterHasNoPublishedVersesException(chapter.id());
        }

        return verses.stream()
                .peek(verse -> verse.assertBelongsTo(chapter.chapterNumber()))
                .map(this::toView)
                .toList();
    }

    /**
     * Returns a published Verse with imported Sanskrit for Reader display.
     *
     * <p>Unknown, unpublished, or Sanskrit-missing Verses all raise
     * {@link VerseNotFoundException} so the Reader never receives placeholder Scripture.
     */
    public VerseDetailView getPublishedVerseDetail(VerseId verseId) {
        Verse verse = verseRepository
                .findByIdAndPublicationStatus(verseId, PublicationStatus.PUBLISHED)
                .orElseThrow(() -> new VerseNotFoundException(verseId));

        if (!verse.hasSanskritText()) {
            throw new VerseNotFoundException(
                    verseId, "Published verse has no imported Sanskrit");
        }

        Chapter chapter = chapterRepository
                .findByIdAndPublicationStatus(verse.chapterId(), PublicationStatus.PUBLISHED)
                .orElseThrow(() -> new VerseNotFoundException(
                        verseId, "Published verse chapter is unavailable"));

        verse.assertBelongsTo(chapter.chapterNumber());

        return new VerseDetailView(
                verse.id().value(),
                verse.chapterId().value(),
                chapter.chapterNumber().value(),
                verse.verseNumber().value(),
                verse.canonicalReference().value(),
                verse.sanskritText(),
                verse.contentVersion());
    }

    private VerseView toView(Verse verse) {
        return new VerseView(
                verse.id().value(),
                verse.verseNumber().value(),
                verse.canonicalReference().value(),
                PLACEHOLDER_PREVIEW_TEXT);
    }
}
