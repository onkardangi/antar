package com.antar.scripture.api;

import com.antar.scripture.application.chapter.query.ChapterView;

final class ChapterApiMapper {

    private ChapterApiMapper() {
    }

    static ChapterResponse toResponse(ChapterView view) {
        return new ChapterResponse(
                view.id(),
                view.chapterNumber(),
                view.canonicalName(),
                view.englishName(),
                view.shortIntent(),
                view.verseCount());
    }
}
