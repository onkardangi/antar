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
@Table(name = "chapters", schema = "scripture")
public class ChapterJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "chapter_number", nullable = false, unique = true)
    private short chapterNumber;

    @Column(name = "canonical_name", nullable = false)
    private String canonicalName;

    @Column(name = "english_name", nullable = false)
    private String englishName;

    @Column(name = "short_intent", nullable = false)
    private String shortIntent;

    @Column(name = "verse_count", nullable = false)
    private int verseCount;

    @Enumerated(EnumType.STRING)
    @Column(name = "publication_status", nullable = false, length = 32)
    private PublicationStatus publicationStatus;

    @Column(name = "content_version", nullable = false)
    private long contentVersion;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected ChapterJpaEntity() {
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public short getChapterNumber() {
        return chapterNumber;
    }

    public void setChapterNumber(short chapterNumber) {
        this.chapterNumber = chapterNumber;
    }

    public String getCanonicalName() {
        return canonicalName;
    }

    public void setCanonicalName(String canonicalName) {
        this.canonicalName = canonicalName;
    }

    public String getEnglishName() {
        return englishName;
    }

    public void setEnglishName(String englishName) {
        this.englishName = englishName;
    }

    public String getShortIntent() {
        return shortIntent;
    }

    public void setShortIntent(String shortIntent) {
        this.shortIntent = shortIntent;
    }

    public int getVerseCount() {
        return verseCount;
    }

    public void setVerseCount(int verseCount) {
        this.verseCount = verseCount;
    }

    public PublicationStatus getPublicationStatus() {
        return publicationStatus;
    }

    public void setPublicationStatus(PublicationStatus publicationStatus) {
        this.publicationStatus = publicationStatus;
    }

    public long getContentVersion() {
        return contentVersion;
    }

    public void setContentVersion(long contentVersion) {
        this.contentVersion = contentVersion;
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
