package com.antar.scripture.application.verse.query;

import com.antar.scripture.domain.ChapterId;

public final class ChapterHasNoPublishedVersesException extends RuntimeException {

    private final ChapterId chapterId;

    public ChapterHasNoPublishedVersesException(ChapterId chapterId) {
        super("Chapter " + chapterId.value() + " has no published Verses");
        this.chapterId = chapterId;
    }

    public ChapterId chapterId() {
        return chapterId;
    }
}
