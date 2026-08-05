package com.antar.scripture.api;

import java.util.UUID;

/**
 * Reader Verse detail payload for {@code GET /api/v1/scripture/verses/{verseId}}.
 *
 * <p>MVP Sanskrit-only response. Translation, commentary, transliteration, and personalization
 * are intentionally absent.
 */
public record VerseDetailResponse(
        UUID id,
        UUID chapterId,
        int chapterNumber,
        int verseNumber,
        String canonicalReference,
        String sanskritText,
        long contentVersion) {
}
