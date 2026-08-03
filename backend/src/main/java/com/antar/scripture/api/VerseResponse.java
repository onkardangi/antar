package com.antar.scripture.api;

import java.util.UUID;

public record VerseResponse(
        UUID id,
        int verseNumber,
        String canonicalReference,
        String previewText) {
}
