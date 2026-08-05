package com.antar.translation.application.query;

import java.util.UUID;

public record TranslationView(
        UUID id,
        UUID verseId,
        String language,
        String provider,
        String translationText,
        long contentVersion) {
}
