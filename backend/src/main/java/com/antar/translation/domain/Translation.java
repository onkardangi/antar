package com.antar.translation.domain;

import java.time.Instant;
import java.util.Objects;
import java.util.Optional;

/**
 * Per-Verse translation aggregate root owned by the Translation module.
 */
public final class Translation {

    private final TranslationId id;
    private final VerseId verseId;
    private final TranslationSourceId translationSourceId;
    private final TranslationLanguage language;
    private final TranslationProvider provider;
    private final TranslationText translationText;
    private final TranslationStatus publicationStatus;
    private final TranslationVersion contentVersion;
    private final String sourcePackageId;
    private final String sourcePackageChecksum;
    private final Instant createdAt;
    private final Instant updatedAt;

    private Translation(
            TranslationId id,
            VerseId verseId,
            TranslationSourceId translationSourceId,
            TranslationLanguage language,
            TranslationProvider provider,
            TranslationText translationText,
            TranslationStatus publicationStatus,
            TranslationVersion contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant createdAt,
            Instant updatedAt) {
        this.id = Objects.requireNonNull(id, "id is required");
        this.verseId = Objects.requireNonNull(verseId, "verseId is required");
        this.translationSourceId =
                Objects.requireNonNull(translationSourceId, "translationSourceId is required");
        this.language = Objects.requireNonNull(language, "language is required");
        this.provider = Objects.requireNonNull(provider, "provider is required");
        this.translationText = Objects.requireNonNull(translationText, "translationText is required");
        this.publicationStatus =
                Objects.requireNonNull(publicationStatus, "publicationStatus is required");
        this.contentVersion = Objects.requireNonNull(contentVersion, "contentVersion is required");
        validatePackageLineage(sourcePackageId, sourcePackageChecksum);
        this.sourcePackageId = sourcePackageId;
        this.sourcePackageChecksum = sourcePackageChecksum;
        this.createdAt = Objects.requireNonNull(createdAt, "createdAt is required");
        this.updatedAt = Objects.requireNonNull(updatedAt, "updatedAt is required");
    }

    public static Translation create(
            VerseId verseId,
            TranslationSourceId translationSourceId,
            TranslationLanguage language,
            TranslationProvider provider,
            TranslationText translationText,
            TranslationStatus publicationStatus,
            TranslationVersion contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant now) {
        return new Translation(
                TranslationId.generate(),
                verseId,
                translationSourceId,
                language,
                provider,
                translationText,
                publicationStatus,
                contentVersion,
                requireText(sourcePackageId, "sourcePackageId"),
                requireChecksum(sourcePackageChecksum, "sourcePackageChecksum"),
                now,
                now);
    }

    public static Translation rehydrate(
            TranslationId id,
            VerseId verseId,
            TranslationSourceId translationSourceId,
            TranslationLanguage language,
            TranslationProvider provider,
            TranslationText translationText,
            TranslationStatus publicationStatus,
            TranslationVersion contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant createdAt,
            Instant updatedAt) {
        return new Translation(
                id,
                verseId,
                translationSourceId,
                language,
                provider,
                translationText,
                publicationStatus,
                contentVersion,
                sourcePackageId,
                sourcePackageChecksum,
                createdAt,
                updatedAt);
    }

    public Translation withImportedContent(
            TranslationText translationText,
            TranslationVersion contentVersion,
            String sourcePackageId,
            String sourcePackageChecksum,
            Instant updatedAt) {
        return new Translation(
                id,
                verseId,
                translationSourceId,
                language,
                provider,
                Objects.requireNonNull(translationText, "translationText is required"),
                publicationStatus,
                Objects.requireNonNull(contentVersion, "contentVersion is required"),
                requireText(sourcePackageId, "sourcePackageId"),
                requireChecksum(sourcePackageChecksum, "sourcePackageChecksum"),
                createdAt,
                Objects.requireNonNull(updatedAt, "updatedAt is required"));
    }

    public boolean isPublished() {
        return publicationStatus == TranslationStatus.PUBLISHED;
    }

    public TranslationId id() {
        return id;
    }

    public VerseId verseId() {
        return verseId;
    }

    public TranslationSourceId translationSourceId() {
        return translationSourceId;
    }

    public TranslationLanguage language() {
        return language;
    }

    public TranslationProvider provider() {
        return provider;
    }

    public TranslationText translationText() {
        return translationText;
    }

    public TranslationStatus publicationStatus() {
        return publicationStatus;
    }

    public TranslationVersion contentVersion() {
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
}
