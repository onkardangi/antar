package com.antar.translation.application.query;

import com.antar.translation.domain.VerseId;

public final class TranslationNotFoundException extends RuntimeException {

    public TranslationNotFoundException(VerseId verseId) {
        super("Published translation not found for verse " + verseId);
    }
}
