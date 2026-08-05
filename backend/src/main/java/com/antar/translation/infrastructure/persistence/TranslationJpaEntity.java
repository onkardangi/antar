package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.TranslationStatus;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "translations", schema = "translation")
public class TranslationJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "verse_id", nullable = false)
    private UUID verseId;

    @Column(name = "translation_source_id", nullable = false)
    private UUID translationSourceId;

    @Column(name = "language_code", nullable = false)
    private String languageCode;

    @Column(name = "provider", nullable = false)
    private String provider;

    @Column(name = "translation_text", nullable = false)
    private String translationText;

    @Enumerated(EnumType.STRING)
    @Column(name = "publication_status", nullable = false, length = 32)
    private TranslationStatus publicationStatus;

    @Column(name = "content_version", nullable = false)
    private long contentVersion;

    @Column(name = "source_package_id")
    private String sourcePackageId;

    @Column(name = "source_package_checksum", length = 64)
    private String sourcePackageChecksum;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected TranslationJpaEntity() {
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getVerseId() { return verseId; }
    public void setVerseId(UUID verseId) { this.verseId = verseId; }
    public UUID getTranslationSourceId() { return translationSourceId; }
    public void setTranslationSourceId(UUID translationSourceId) { this.translationSourceId = translationSourceId; }
    public String getLanguageCode() { return languageCode; }
    public void setLanguageCode(String languageCode) { this.languageCode = languageCode; }
    public String getProvider() { return provider; }
    public void setProvider(String provider) { this.provider = provider; }
    public String getTranslationText() { return translationText; }
    public void setTranslationText(String translationText) { this.translationText = translationText; }
    public TranslationStatus getPublicationStatus() { return publicationStatus; }
    public void setPublicationStatus(TranslationStatus publicationStatus) { this.publicationStatus = publicationStatus; }
    public long getContentVersion() { return contentVersion; }
    public void setContentVersion(long contentVersion) { this.contentVersion = contentVersion; }
    public String getSourcePackageId() { return sourcePackageId; }
    public void setSourcePackageId(String sourcePackageId) { this.sourcePackageId = sourcePackageId; }
    public String getSourcePackageChecksum() { return sourcePackageChecksum; }
    public void setSourcePackageChecksum(String sourcePackageChecksum) { this.sourcePackageChecksum = sourcePackageChecksum; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}
