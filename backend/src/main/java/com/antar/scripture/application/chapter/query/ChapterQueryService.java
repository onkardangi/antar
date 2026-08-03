package com.antar.scripture.application.chapter.query;

import com.antar.scripture.application.port.ChapterRepository;
import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class ChapterQueryService {

    private final ChapterRepository chapterRepository;

    public ChapterQueryService(ChapterRepository chapterRepository) {
        this.chapterRepository = chapterRepository;
    }

    public List<ChapterView> listPublishedChapters() {
        return chapterRepository
                .findAllByPublicationStatusOrderByChapterNumberAsc(PublicationStatus.PUBLISHED)
                .stream()
                .map(this::toView)
                .toList();
    }

    public ChapterView getPublishedChapter(ChapterId chapterId) {
        return chapterRepository
                .findByIdAndPublicationStatus(chapterId, PublicationStatus.PUBLISHED)
                .map(this::toView)
                .orElseThrow(() -> new ChapterNotFoundException(chapterId));
    }

    public ChapterView getPublishedChapterByNumber(ChapterNumber chapterNumber) {
        return chapterRepository
                .findByChapterNumberAndPublicationStatus(chapterNumber, PublicationStatus.PUBLISHED)
                .map(this::toView)
                .orElseThrow(() -> new ChapterNotFoundException(chapterNumber));
    }

    private ChapterView toView(Chapter chapter) {
        return new ChapterView(
                chapter.id().value(),
                chapter.chapterNumber().value(),
                chapter.canonicalName(),
                chapter.englishName(),
                chapter.shortIntent(),
                chapter.verseCount());
    }
}
