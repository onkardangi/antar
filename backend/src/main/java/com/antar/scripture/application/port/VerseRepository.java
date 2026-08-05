package com.antar.scripture.application.port;

import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import com.antar.scripture.domain.VerseId;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

public interface VerseRepository {

    Optional<Verse> findByIdAndPublicationStatus(VerseId verseId, PublicationStatus publicationStatus);

    List<Verse> findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
            ChapterId chapterId, PublicationStatus publicationStatus);

    long countByChapterIdAndPublicationStatus(ChapterId chapterId, PublicationStatus publicationStatus);

    List<Verse> findAllByChapterIdOrderByVerseNumberAsc(ChapterId chapterId);

    List<Verse> findAllByCanonicalReferences(Collection<String> canonicalReferences);

    Optional<Verse> findByCanonicalReference(String canonicalReference);

    Verse save(Verse verse);

    void saveAll(Collection<Verse> verses);
}
