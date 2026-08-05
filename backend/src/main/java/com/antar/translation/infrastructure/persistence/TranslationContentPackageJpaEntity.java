package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.ContentPackageStatus;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.List;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "content_packages", schema = "translation")
public class TranslationContentPackageJpaEntity {

    @Id
    @Column(name = "package_id", nullable = false, updatable = false)
    private String packageId;

    @Column(name = "package_format_version", nullable = false)
    private int packageFormatVersion;

    @Column(name = "scripture_id", nullable = false)
    private String scriptureId;

    @Column(name = "chapter_number", nullable = false)
    private int chapterNumber;

    @Column(name = "language_code", nullable = false)
    private String languageCode;

    @Column(name = "provider", nullable = false)
    private String provider;

    @Column(name = "content_version", nullable = false)
    private long contentVersion;

    @Enumerated(EnumType.STRING)
    @Column(name = "package_status", nullable = false, length = 32)
    private ContentPackageStatus packageStatus;

    @Column(name = "package_checksum", nullable = false, unique = true, length = 64)
    private String packageChecksum;

    @Column(name = "manifest_checksum", nullable = false, length = 64)
    private String manifestChecksum;

    @Column(name = "provenance_checksum", nullable = false, length = 64)
    private String provenanceChecksum;

    @Column(name = "translations_checksum", nullable = false, length = 64)
    private String translationsChecksum;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "source_registry_references", nullable = false, columnDefinition = "jsonb")
    private List<String> sourceRegistryReferences;

    @Column(name = "importer_version", nullable = false)
    private int importerVersion;

    @Column(name = "first_imported_at")
    private Instant firstImportedAt;

    @Column(name = "last_verified_at")
    private Instant lastVerifiedAt;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected TranslationContentPackageJpaEntity() {
    }

    public String getPackageId() { return packageId; }
    public void setPackageId(String packageId) { this.packageId = packageId; }
    public int getPackageFormatVersion() { return packageFormatVersion; }
    public void setPackageFormatVersion(int packageFormatVersion) { this.packageFormatVersion = packageFormatVersion; }
    public String getScriptureId() { return scriptureId; }
    public void setScriptureId(String scriptureId) { this.scriptureId = scriptureId; }
    public int getChapterNumber() { return chapterNumber; }
    public void setChapterNumber(int chapterNumber) { this.chapterNumber = chapterNumber; }
    public String getLanguageCode() { return languageCode; }
    public void setLanguageCode(String languageCode) { this.languageCode = languageCode; }
    public String getProvider() { return provider; }
    public void setProvider(String provider) { this.provider = provider; }
    public long getContentVersion() { return contentVersion; }
    public void setContentVersion(long contentVersion) { this.contentVersion = contentVersion; }
    public ContentPackageStatus getPackageStatus() { return packageStatus; }
    public void setPackageStatus(ContentPackageStatus packageStatus) { this.packageStatus = packageStatus; }
    public String getPackageChecksum() { return packageChecksum; }
    public void setPackageChecksum(String packageChecksum) { this.packageChecksum = packageChecksum; }
    public String getManifestChecksum() { return manifestChecksum; }
    public void setManifestChecksum(String manifestChecksum) { this.manifestChecksum = manifestChecksum; }
    public String getProvenanceChecksum() { return provenanceChecksum; }
    public void setProvenanceChecksum(String provenanceChecksum) { this.provenanceChecksum = provenanceChecksum; }
    public String getTranslationsChecksum() { return translationsChecksum; }
    public void setTranslationsChecksum(String translationsChecksum) { this.translationsChecksum = translationsChecksum; }
    public List<String> getSourceRegistryReferences() { return sourceRegistryReferences; }
    public void setSourceRegistryReferences(List<String> sourceRegistryReferences) { this.sourceRegistryReferences = sourceRegistryReferences; }
    public int getImporterVersion() { return importerVersion; }
    public void setImporterVersion(int importerVersion) { this.importerVersion = importerVersion; }
    public Instant getFirstImportedAt() { return firstImportedAt; }
    public void setFirstImportedAt(Instant firstImportedAt) { this.firstImportedAt = firstImportedAt; }
    public Instant getLastVerifiedAt() { return lastVerifiedAt; }
    public void setLastVerifiedAt(Instant lastVerifiedAt) { this.lastVerifiedAt = lastVerifiedAt; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}
