package com.antar.scripture.api;

import java.util.UUID;

public record ChapterResponse(
        UUID id,
        int chapterNumber,
        String canonicalName,
        String englishName,
        String shortIntent,
        int verseCount) {
}
