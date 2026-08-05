package com.antar.translation.application.query;

import com.antar.translation.application.port.TranslationRepository;
import com.antar.translation.domain.Translation;
import com.antar.translation.domain.VerseId;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class TranslationQueryService {

    private final TranslationRepository translationRepository;

    public TranslationQueryService(TranslationRepository translationRepository) {
        this.translationRepository = translationRepository;
    }

    public TranslationView getPublishedTranslationForVerse(VerseId verseId) {
        Translation translation = translationRepository
                .findPublishedByVerseId(verseId)
                .orElseThrow(() -> new TranslationNotFoundException(verseId));

        return new TranslationView(
                translation.id().value(),
                translation.verseId().value(),
                translation.language().code(),
                translation.provider().value(),
                translation.translationText().value(),
                translation.contentVersion().value());
    }
}
