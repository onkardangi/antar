package com.antar.translation.api;

import java.util.UUID;

public record TranslationResponse(
        UUID id,
        UUID verseId,
        String language,
        String provider,
        String translationText,
        long contentVersion) {
}
