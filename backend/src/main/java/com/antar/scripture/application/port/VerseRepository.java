package com.antar.scripture.application.port;

import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.PublicationStatus;
import com.antar.scripture.domain.Verse;
import java.util.List;

public interface VerseRepository {

    List<Verse> findAllByChapterIdAndPublicationStatusOrderByVerseNumberAsc(
            ChapterId chapterId, PublicationStatus publicationStatus);

    long countByChapterIdAndPublicationStatus(ChapterId chapterId, PublicationStatus publicationStatus);

    Verse save(Verse verse);
}
