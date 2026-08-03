package com.antar.scripture.application.port;

import com.antar.scripture.domain.Chapter;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import com.antar.scripture.domain.PublicationStatus;
import java.util.List;
import java.util.Optional;

public interface ChapterRepository {

    List<Chapter> findAllByPublicationStatusOrderByChapterNumberAsc(PublicationStatus publicationStatus);

    Optional<Chapter> findByIdAndPublicationStatus(ChapterId chapterId, PublicationStatus publicationStatus);

    Optional<Chapter> findByChapterNumberAndPublicationStatus(
            ChapterNumber chapterNumber, PublicationStatus publicationStatus);

    Chapter save(Chapter chapter);
}
