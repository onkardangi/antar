package com.antar.scripture.domain;

import java.time.Instant;
import java.util.Objects;

/**
 * Scripture Chapter aggregate root.
 *
 * <p>Owns chapter metadata and canonical ordering. Verses belong to exactly one Chapter.
 */
public final class Chapter {

    private final ChapterId id;
    private final ChapterNumber chapterNumber;
    private final String canonicalName;
    private final String englishName;
    private final String shortIntent;
    private final int verseCount;
    private final PublicationStatus publicationStatus;
    private final long contentVersion;
    private final Instant createdAt;
    private final Instant updatedAt;

    private Chapter(
            ChapterId id,
            ChapterNumber chapterNumber,
            String canonicalName,
            String englishName,
            String shortIntent,
            int verseCount,
            PublicationStatus publicationStatus,
            long contentVersion,
            Instant createdAt,
            Instant updatedAt) {
        this.id = Objects.requireNonNull(id, "id is required");
        this.chapterNumber = Objects.requireNonNull(chapterNumber, "chapterNumber is required");
        this.canonicalName = requireText(canonicalName, "canonicalName");
        this.englishName = requireText(englishName, "englishName");
        this.shortIntent = requireText(shortIntent, "shortIntent");
        if (verseCount <= 0) {
            throw new IllegalArgumentException("verseCount must be positive");
        }
        this.verseCount = verseCount;
        this.publicationStatus = Objects.requireNonNull(publicationStatus, "publicationStatus is required");
        if (contentVersion < 0) {
            throw new IllegalArgumentException("contentVersion must not be negative");
        }
        this.contentVersion = contentVersion;
        this.createdAt = Objects.requireNonNull(createdAt, "createdAt is required");
        this.updatedAt = Objects.requireNonNull(updatedAt, "updatedAt is required");
    }

    public static Chapter rehydrate(
            ChapterId id,
            ChapterNumber chapterNumber,
            String canonicalName,
            String englishName,
            String shortIntent,
            int verseCount,
            PublicationStatus publicationStatus,
            long contentVersion,
            Instant createdAt,
            Instant updatedAt) {
        return new Chapter(
                id,
                chapterNumber,
                canonicalName,
                englishName,
                shortIntent,
                verseCount,
                publicationStatus,
                contentVersion,
                createdAt,
                updatedAt);
    }

    public boolean isPublished() {
        return publicationStatus == PublicationStatus.PUBLISHED;
    }

    public ChapterId id() {
        return id;
    }

    public ChapterNumber chapterNumber() {
        return chapterNumber;
    }

    public String canonicalName() {
        return canonicalName;
    }

    public String englishName() {
        return englishName;
    }

    public String shortIntent() {
        return shortIntent;
    }

    public int verseCount() {
        return verseCount;
    }

    public PublicationStatus publicationStatus() {
        return publicationStatus;
    }

    public long contentVersion() {
        return contentVersion;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public Instant updatedAt() {
        return updatedAt;
    }

    private static String requireText(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(fieldName + " is required");
        }
        return value.trim();
    }
}
