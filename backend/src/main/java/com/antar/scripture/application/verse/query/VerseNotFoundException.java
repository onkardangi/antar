package com.antar.scripture.application.verse.query;

import com.antar.scripture.domain.VerseId;

/**
 * Raised when a published Verse with readable Sanskrit is unavailable to the Reader.
 *
 * <p>Covers unknown ids, unpublished Verses, missing Chapter publication, and Verses whose
 * Sanskrit has not yet been imported. All map to HTTP 404 so Readers never see placeholder
 * Scripture.
 */
public final class VerseNotFoundException extends RuntimeException {

    private final String resource;

    public VerseNotFoundException(VerseId verseId) {
        super("Published verse not found: " + verseId);
        this.resource = "verseId=" + verseId;
    }

    public VerseNotFoundException(VerseId verseId, String reason) {
        super(reason + ": " + verseId);
        this.resource = "verseId=" + verseId;
    }

    public String resource() {
        return resource;
    }
}
