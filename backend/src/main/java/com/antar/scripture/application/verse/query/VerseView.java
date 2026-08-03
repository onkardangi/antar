package com.antar.scripture.application.verse.query;

import java.util.UUID;

public record VerseView(
        UUID id,
        int verseNumber,
        String canonicalReference,
        String previewText) {
}
