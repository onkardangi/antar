package com.antar.scripture.application.chapter.query;

import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import java.util.UUID;

public record ChapterView(
        UUID id,
        int chapterNumber,
        String canonicalName,
        String englishName,
        String shortIntent,
        int verseCount) {

    public ChapterId chapterId() {
        return ChapterId.of(id);
    }

    public ChapterNumber number() {
        return ChapterNumber.of(chapterNumber);
    }
}
