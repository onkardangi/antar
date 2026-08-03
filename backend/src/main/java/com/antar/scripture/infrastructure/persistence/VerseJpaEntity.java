package com.antar.scripture.infrastructure.persistence;

import com.antar.scripture.domain.PublicationStatus;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "verses", schema = "scripture")
public class VerseJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "chapter_id", nullable = false)
    private UUID chapterId;

    @Column(name = "verse_number", nullable = false)
    private int verseNumber;

    @Column(name = "canonical_reference", nullable = false, unique = true)
    private String canonicalReference;

    /**
     * Canonical Sanskrit. Null means the approved corpus has not yet been imported.
     * Must never hold engineering placeholder prose.
     */
    @Column(name = "sanskrit_text")
    private String sanskritText;

    @Column(name = "content_version", nullable = false)
    private long contentVersion;

    @Enumerated(EnumType.STRING)
    @Column(name = "publication_status", nullable = false, length = 32)
    private PublicationStatus publicationStatus;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected VerseJpaEntity() {
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public UUID getChapterId() {
        return chapterId;
    }

    public void setChapterId(UUID chapterId) {
        this.chapterId = chapterId;
    }

    public int getVerseNumber() {
        return verseNumber;
    }

    public void setVerseNumber(int verseNumber) {
        this.verseNumber = verseNumber;
    }

    public String getCanonicalReference() {
        return canonicalReference;
    }

    public void setCanonicalReference(String canonicalReference) {
        this.canonicalReference = canonicalReference;
    }

    public String getSanskritText() {
        return sanskritText;
    }

    public void setSanskritText(String sanskritText) {
        this.sanskritText = sanskritText;
    }

    public long getContentVersion() {
        return contentVersion;
    }

    public void setContentVersion(long contentVersion) {
        this.contentVersion = contentVersion;
    }

    public PublicationStatus getPublicationStatus() {
        return publicationStatus;
    }

    public void setPublicationStatus(PublicationStatus publicationStatus) {
        this.publicationStatus = publicationStatus;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }
}
