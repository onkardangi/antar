package com.antar.scripture.application.chapter.query;

import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;

public final class ChapterNotFoundException extends RuntimeException {

    private final String resource;

    public ChapterNotFoundException(ChapterId chapterId) {
        super("Published chapter not found: " + chapterId);
        this.resource = "chapterId=" + chapterId;
    }

    public ChapterNotFoundException(ChapterNumber chapterNumber) {
        super("Published chapter not found for number: " + chapterNumber.value());
        this.resource = "chapterNumber=" + chapterNumber.value();
    }

    public String resource() {
        return resource;
    }
}
