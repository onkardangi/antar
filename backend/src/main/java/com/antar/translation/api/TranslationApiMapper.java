package com.antar.translation.api;

import com.antar.translation.application.query.TranslationView;

final class TranslationApiMapper {

    private TranslationApiMapper() {
    }

    static TranslationResponse toResponse(TranslationView view) {
        return new TranslationResponse(
                view.id(),
                view.verseId(),
                view.language(),
                view.provider(),
                view.translationText(),
                view.contentVersion());
    }
}
