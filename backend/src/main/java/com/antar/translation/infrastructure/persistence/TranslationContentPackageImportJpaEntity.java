package com.antar.translation.infrastructure.persistence;

import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "content_package_imports", schema = "translation")
public class TranslationContentPackageImportJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "package_id")
    private String packageId;

    @Column(name = "attempted_package_id", nullable = false)
    private String attemptedPackageId;

    @Column(name = "package_checksum", nullable = false, length = 64)
    private String packageChecksum;

    @Column(name = "chapter_number")
    private Integer chapterNumber;

    @Enumerated(EnumType.STRING)
    @Column(name = "import_status", nullable = false, length = 32)
    private ImportExecutionStatus importStatus;

    @Column(name = "records_read", nullable = false)
    private int recordsRead;

    @Column(name = "records_validated", nullable = false)
    private int recordsValidated;

    @Column(name = "records_updated", nullable = false)
    private int recordsUpdated;

    @Column(name = "records_unchanged", nullable = false)
    private int recordsUnchanged;

    @Column(name = "records_rejected", nullable = false)
    private int recordsRejected;

    @Enumerated(EnumType.STRING)
    @Column(name = "failure_code", length = 64)
    private ImportFailureCode failureCode;

    @Column(name = "failure_message")
    private String failureMessage;

    @Column(name = "importer_version", nullable = false)
    private int importerVersion;

    @Column(name = "started_at", nullable = false)
    private Instant startedAt;

    @Column(name = "completed_at", nullable = false)
    private Instant completedAt;

    @Column(name = "duration_ms", nullable = false)
    private long durationMs;

    protected TranslationContentPackageImportJpaEntity() {
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getPackageId() { return packageId; }
    public void setPackageId(String packageId) { this.packageId = packageId; }
    public String getAttemptedPackageId() { return attemptedPackageId; }
    public void setAttemptedPackageId(String attemptedPackageId) { this.attemptedPackageId = attemptedPackageId; }
    public String getPackageChecksum() { return packageChecksum; }
    public void setPackageChecksum(String packageChecksum) { this.packageChecksum = packageChecksum; }
    public Integer getChapterNumber() { return chapterNumber; }
    public void setChapterNumber(Integer chapterNumber) { this.chapterNumber = chapterNumber; }
    public ImportExecutionStatus getImportStatus() { return importStatus; }
    public void setImportStatus(ImportExecutionStatus importStatus) { this.importStatus = importStatus; }
    public int getRecordsRead() { return recordsRead; }
    public void setRecordsRead(int recordsRead) { this.recordsRead = recordsRead; }
    public int getRecordsValidated() { return recordsValidated; }
    public void setRecordsValidated(int recordsValidated) { this.recordsValidated = recordsValidated; }
    public int getRecordsUpdated() { return recordsUpdated; }
    public void setRecordsUpdated(int recordsUpdated) { this.recordsUpdated = recordsUpdated; }
    public int getRecordsUnchanged() { return recordsUnchanged; }
    public void setRecordsUnchanged(int recordsUnchanged) { this.recordsUnchanged = recordsUnchanged; }
    public int getRecordsRejected() { return recordsRejected; }
    public void setRecordsRejected(int recordsRejected) { this.recordsRejected = recordsRejected; }
    public ImportFailureCode getFailureCode() { return failureCode; }
    public void setFailureCode(ImportFailureCode failureCode) { this.failureCode = failureCode; }
    public String getFailureMessage() { return failureMessage; }
    public void setFailureMessage(String failureMessage) { this.failureMessage = failureMessage; }
    public int getImporterVersion() { return importerVersion; }
    public void setImporterVersion(int importerVersion) { this.importerVersion = importerVersion; }
    public Instant getStartedAt() { return startedAt; }
    public void setStartedAt(Instant startedAt) { this.startedAt = startedAt; }
    public Instant getCompletedAt() { return completedAt; }
    public void setCompletedAt(Instant completedAt) { this.completedAt = completedAt; }
    public long getDurationMs() { return durationMs; }
    public void setDurationMs(long durationMs) { this.durationMs = durationMs; }
}
