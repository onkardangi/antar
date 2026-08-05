package com.antar.translation.application.port;

import com.antar.translation.domain.Translation;
import com.antar.translation.domain.TranslationSourceId;
import com.antar.translation.domain.VerseId;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

public interface TranslationRepository {

    Optional<Translation> findPublishedByVerseId(VerseId verseId);

    List<Translation> findAllBySourceIdAndVerseIds(
            TranslationSourceId sourceId, Collection<VerseId> verseIds);

    Optional<Translation> findByVerseIdAndSourceId(VerseId verseId, TranslationSourceId sourceId);

    void saveAll(List<Translation> translations);
}
