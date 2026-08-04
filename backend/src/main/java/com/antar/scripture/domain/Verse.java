package com.antar.scripture.domain;

import java.time.Instant;
import java.util.Objects;
import java.util.Optional;

/**
 * Scripture Verse aggregate root.
 *
 * <p>Belongs to exactly one Chapter. Canonical Sanskrit is required by the approved data model once
 * imported; until then {@code sanskritText} may be absent so Verse identity records can exist for
 * Chapter listing. Absent Sanskrit must never be treated as Scripture content.
 *
 * <p>When Sanskrit is imported, {@code contentVersion}, {@code sourcePackageId}, and
 * {@code sourcePackageChecksum} update together.
 */
public final class Verse {

    private final VerseId id;
    private final ChapterId chapterId;
    private final VerseNumber verseNumber;
    private final CanonicalReference canonicalReference;
    private final String sanskritText;
    private final PublicationStatus publicationStatus;
    private final long contentVersion;
    private final String sourcePackageId;
    private final String sourcePackageChecksum;
    private final Instant createdAt;
    private final Instant updatedAt;

    private Verse(
            VerseId id,
            ChapterId chapterId,
            VerseNumber verseNumber,
            CanonicalReference canonicalReference,
            String sanskritText,
            PublicationStatus publicationStatus,
            long contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant createdAt,
            Instant updatedAt) {
        this.id = Objects.requireNonNull(id, "id is required");
        this.chapterId = Objects.requireNonNull(chapterId, "chapterId is required");
        this.verseNumber = Objects.requireNonNull(verseNumber, "verseNumber is required");
        this.canonicalReference =
                Objects.requireNonNull(canonicalReference, "canonicalReference is required");
        if (!canonicalReference.verseNumber().equals(verseNumber)) {
            throw new IllegalArgumentException(
                    "canonicalReference verse number must match verseNumber");
        }
        this.sanskritText = normalizeOptionalSanskrit(sanskritText);
        this.publicationStatus =
                Objects.requireNonNull(publicationStatus, "publicationStatus is required");
        if (contentVersion <= 0) {
            throw new IllegalArgumentException("contentVersion must be positive");
        }
        this.contentVersion = contentVersion;
        validatePackageLineage(sourcePackageId, sourcePackageChecksum);
        this.sourcePackageId = sourcePackageId;
        this.sourcePackageChecksum = sourcePackageChecksum;
        this.createdAt = Objects.requireNonNull(createdAt, "createdAt is required");
        this.updatedAt = Objects.requireNonNull(updatedAt, "updatedAt is required");
    }

    public static Verse rehydrate(
            VerseId id,
            ChapterId chapterId,
            VerseNumber verseNumber,
            CanonicalReference canonicalReference,
            String sanskritText,
            PublicationStatus publicationStatus,
            long contentVersion,
            Instant createdAt,
            Instant updatedAt) {
        return rehydrate(
                id,
                chapterId,
                verseNumber,
                canonicalReference,
                sanskritText,
                publicationStatus,
                contentVersion,
                null,
                null,
                createdAt,
                updatedAt);
    }

    public static Verse rehydrate(
            VerseId id,
            ChapterId chapterId,
            VerseNumber verseNumber,
            CanonicalReference canonicalReference,
            String sanskritText,
            PublicationStatus publicationStatus,
            long contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant createdAt,
            Instant updatedAt) {
        return new Verse(
                id,
                chapterId,
                verseNumber,
                canonicalReference,
                sanskritText,
                publicationStatus,
                contentVersion,
                sourcePackageId,
                sourcePackageChecksum,
                createdAt,
                updatedAt);
    }

    /**
     * Applies imported Sanskrit content and package lineage atomically.
     *
     * @throws IllegalArgumentException when lineage fields are incomplete or contentVersion invalid
     */
    public Verse withImportedContent(
            String sanskritText,
            long contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant updatedAt) {
        String normalized = normalizeOptionalSanskrit(sanskritText);
        if (normalized == null) {
            throw new IllegalArgumentException("imported sanskritText must be non-blank");
        }
        return new Verse(
                id,
                chapterId,
                verseNumber,
                canonicalReference,
                normalized,
                publicationStatus,
                contentVersion,
                requireText(sourcePackageId, "sourcePackageId"),
                requireChecksum(sourcePackageChecksum, "sourcePackageChecksum"),
                createdAt,
                Objects.requireNonNull(updatedAt, "updatedAt is required"));
    }

    /**
     * Ensures the Verse's canonical reference chapter matches the owning Chapter number.
     *
     * @throws IllegalArgumentException when chapter ownership is inconsistent
     */
    public void assertBelongsTo(ChapterNumber chapterNumber) {
        Objects.requireNonNull(chapterNumber, "chapterNumber is required");
        if (!canonicalReference.chapterNumber().equals(chapterNumber)) {
            throw new IllegalArgumentException(
                    "Verse "
                            + canonicalReference.value()
                            + " does not belong to Chapter "
                            + chapterNumber.value());
        }
    }

    public boolean isPublished() {
        return publicationStatus == PublicationStatus.PUBLISHED;
    }

    public boolean hasSanskritText() {
        return sanskritText != null;
    }

    public VerseId id() {
        return id;
    }

    public ChapterId chapterId() {
        return chapterId;
    }

    public VerseNumber verseNumber() {
        return verseNumber;
    }

    public CanonicalReference canonicalReference() {
        return canonicalReference;
    }

    /**
     * Canonical Sanskrit when imported; {@code null} when the approved corpus is not yet present.
     */
    public String sanskritText() {
        return sanskritText;
    }

    public Optional<String> sanskritTextOptional() {
        return Optional.ofNullable(sanskritText);
    }

    public PublicationStatus publicationStatus() {
        return publicationStatus;
    }

    public long contentVersion() {
        return contentVersion;
    }

    public Optional<String> sourcePackageId() {
        return Optional.ofNullable(sourcePackageId);
    }

    public Optional<String> sourcePackageChecksum() {
        return Optional.ofNullable(sourcePackageChecksum);
    }

    public Instant createdAt() {
        return createdAt;
    }

    public Instant updatedAt() {
        return updatedAt;
    }

    private static void validatePackageLineage(String packageId, String packageChecksum) {
        if (packageId == null && packageChecksum == null) {
            return;
        }
        if (packageId == null || packageChecksum == null) {
            throw new IllegalArgumentException(
                    "sourcePackageId and sourcePackageChecksum must both be present or both absent");
        }
        requireText(packageId, "sourcePackageId");
        requireChecksum(packageChecksum, "sourcePackageChecksum");
    }

    private static String requireText(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(fieldName + " is required");
        }
        return value.trim();
    }

    private static String requireChecksum(String value, String fieldName) {
        String trimmed = requireText(value, fieldName);
        if (!trimmed.matches("^[a-f0-9]{64}$")) {
            throw new IllegalArgumentException(fieldName + " must be a lowercase SHA-256 hex digest");
        }
        return trimmed;
    }

    private static String normalizeOptionalSanskrit(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        if (trimmed.isEmpty()) {
            throw new IllegalArgumentException("sanskritText must be null or non-blank");
        }
        return trimmed;
    }
}
