package com.antar.translation.domain;

import java.util.List;
import java.util.Objects;

/**
 * Immutable Translation package identity metadata after successful resolution.
 */
public final class TranslationPackage {

    private final String packageId;
    private final int packageFormatVersion;
    private final String scriptureId;
    private final int chapterNumber;
    private final TranslationLanguage language;
    private final TranslationProvider provider;
    private final TranslationVersion contentVersion;
    private final ContentPackageStatus packageStatus;
    private final String packageChecksum;
    private final List<String> sourceRegistryReferences;

    public TranslationPackage(
            String packageId,
            int packageFormatVersion,
            String scriptureId,
            int chapterNumber,
            TranslationLanguage language,
            TranslationProvider provider,
            TranslationVersion contentVersion,
            ContentPackageStatus packageStatus,
            String packageChecksum,
            List<String> sourceRegistryReferences) {
        this.packageId = requireText(packageId, "packageId");
        if (packageFormatVersion < 1) {
            throw new IllegalArgumentException("packageFormatVersion must be >= 1");
        }
        this.packageFormatVersion = packageFormatVersion;
        this.scriptureId = requireText(scriptureId, "scriptureId");
        if (chapterNumber < 1 || chapterNumber > 18) {
            throw new IllegalArgumentException("chapterNumber must be between 1 and 18");
        }
        this.chapterNumber = chapterNumber;
        this.language = Objects.requireNonNull(language, "language is required");
        this.provider = Objects.requireNonNull(provider, "provider is required");
        this.contentVersion = Objects.requireNonNull(contentVersion, "contentVersion is required");
        this.packageStatus = Objects.requireNonNull(packageStatus, "packageStatus is required");
        this.packageChecksum = requireChecksum(packageChecksum);
        this.sourceRegistryReferences = List.copyOf(
                Objects.requireNonNull(sourceRegistryReferences, "sourceRegistryReferences is required"));
    }

    public String packageId() {
        return packageId;
    }

    public int packageFormatVersion() {
        return packageFormatVersion;
    }

    public String scriptureId() {
        return scriptureId;
    }

    public int chapterNumber() {
        return chapterNumber;
    }

    public TranslationLanguage language() {
        return language;
    }

    public TranslationProvider provider() {
        return provider;
    }

    public TranslationVersion contentVersion() {
        return contentVersion;
    }

    public ContentPackageStatus packageStatus() {
        return packageStatus;
    }

    public String packageChecksum() {
        return packageChecksum;
    }

    public List<String> sourceRegistryReferences() {
        return sourceRegistryReferences;
    }

    private static String requireText(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(fieldName + " is required");
        }
        return value.trim();
    }

    private static String requireChecksum(String value) {
        String trimmed = requireText(value, "packageChecksum");
        if (!trimmed.matches("^[a-f0-9]{64}$")) {
            throw new IllegalArgumentException("packageChecksum must be a lowercase SHA-256 hex digest");
        }
        return trimmed;
    }
}
