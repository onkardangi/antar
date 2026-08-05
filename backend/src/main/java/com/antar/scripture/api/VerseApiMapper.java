package com.antar.scripture.api;

import com.antar.scripture.application.verse.query.VerseDetailView;
import com.antar.scripture.application.verse.query.VerseView;

final class VerseApiMapper {

    private VerseApiMapper() {
    }

    static VerseResponse toResponse(VerseView view) {
        return new VerseResponse(
                view.id(),
                view.verseNumber(),
                view.canonicalReference(),
                view.previewText());
    }

    static VerseDetailResponse toDetailResponse(VerseDetailView view) {
        return new VerseDetailResponse(
                view.id(),
                view.chapterId(),
                view.chapterNumber(),
                view.verseNumber(),
                view.canonicalReference(),
                view.sanskritText(),
                view.contentVersion());
    }
}
