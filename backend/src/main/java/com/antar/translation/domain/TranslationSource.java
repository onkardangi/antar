package com.antar.translation.domain;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

/**
 * Identifiable translation edition / provider.
 */
public final class TranslationSource {

    private final TranslationSourceId id;
    private final TranslationProvider provider;
    private final String name;
    private final TranslationLanguage language;
    private final String licenseType;
    private final String licenseReference;
    private final TranslationStatus publicationStatus;
    private final Instant createdAt;
    private final Instant updatedAt;

    private TranslationSource(
            TranslationSourceId id,
            TranslationProvider provider,
            String name,
            TranslationLanguage language,
            String licenseType,
            String licenseReference,
            TranslationStatus publicationStatus,
            Instant createdAt,
            Instant updatedAt) {
        this.id = Objects.requireNonNull(id, "id is required");
        this.provider = Objects.requireNonNull(provider, "provider is required");
        this.name = requireText(name, "name");
        this.language = Objects.requireNonNull(language, "language is required");
        this.licenseType = requireText(licenseType, "licenseType");
        this.licenseReference = licenseReference == null || licenseReference.isBlank()
                ? null
                : licenseReference.trim();
        this.publicationStatus =
                Objects.requireNonNull(publicationStatus, "publicationStatus is required");
        this.createdAt = Objects.requireNonNull(createdAt, "createdAt is required");
        this.updatedAt = Objects.requireNonNull(updatedAt, "updatedAt is required");
    }

    public static TranslationSource create(
            TranslationProvider provider,
            String name,
            TranslationLanguage language,
            String licenseType,
            String licenseReference,
            TranslationStatus publicationStatus,
            Instant now) {
        return new TranslationSource(
                TranslationSourceId.generate(),
                provider,
                name,
                language,
                licenseType,
                licenseReference,
                publicationStatus,
                now,
                now);
    }

    public static TranslationSource rehydrate(
            TranslationSourceId id,
            TranslationProvider provider,
            String name,
            TranslationLanguage language,
            String licenseType,
            String licenseReference,
            TranslationStatus publicationStatus,
            Instant createdAt,
            Instant updatedAt) {
        return new TranslationSource(
                id,
                provider,
                name,
                language,
                licenseType,
                licenseReference,
                publicationStatus,
                createdAt,
                updatedAt);
    }

    public TranslationSourceId id() {
        return id;
    }

    public TranslationProvider provider() {
        return provider;
    }

    public String name() {
        return name;
    }

    public TranslationLanguage language() {
        return language;
    }

    public String licenseType() {
        return licenseType;
    }

    public String licenseReference() {
        return licenseReference;
    }

    public TranslationStatus publicationStatus() {
        return publicationStatus;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public Instant updatedAt() {
        return updatedAt;
    }

    public UUID idValue() {
        return id.value();
    }

    private static String requireText(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(fieldName + " is required");
        }
        return value.trim();
    }
}
