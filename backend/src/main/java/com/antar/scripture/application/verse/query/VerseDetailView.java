package com.antar.scripture.application.verse.query;

import java.util.UUID;

/**
 * Reader-facing Verse detail projection.
 *
 * <p>Contains only approved canonical Scripture fields. Package checksum, source ids,
 * review metadata, and editorial history are intentionally excluded.
 */
public record VerseDetailView(
        UUID id,
        UUID chapterId,
        int chapterNumber,
        int verseNumber,
        String canonicalReference,
        String sanskritText,
        long contentVersion) {
}
