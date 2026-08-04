-- Scripture content package provenance and import audit.
-- Packages are immutable release artifacts; this migration records import lineage only.
-- Does not store package blobs, Scripture text, local paths, or raw exception output.
--
-- V006 is revised in-branch before commit: FAILED execution rows do not register
-- content_packages, and at most one APPROVED package may be active per scripture/chapter.

CREATE TABLE scripture.content_packages (
    package_id                   TEXT            NOT NULL,
    package_format_version       INTEGER         NOT NULL,
    scripture_id                 TEXT            NOT NULL,
    chapter_number               INTEGER         NOT NULL,
    content_version              BIGINT          NOT NULL,
    package_status               VARCHAR(32)     NOT NULL,
    package_checksum             VARCHAR(64)     NOT NULL,
    manifest_checksum            VARCHAR(64)     NOT NULL,
    provenance_checksum          VARCHAR(64)     NOT NULL,
    verses_checksum              VARCHAR(64)     NOT NULL,
    source_registry_references   JSONB           NOT NULL,
    importer_version             INTEGER         NOT NULL,
    first_imported_at            TIMESTAMPTZ,
    last_verified_at             TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ     NOT NULL,
    updated_at                   TIMESTAMPTZ     NOT NULL,
    CONSTRAINT pk_scripture_content_packages
        PRIMARY KEY (package_id),
    CONSTRAINT uq_scripture_content_packages_checksum
        UNIQUE (package_checksum),
    CONSTRAINT chk_scripture_content_packages_format_version
        CHECK (package_format_version >= 1),
    CONSTRAINT chk_scripture_content_packages_chapter_number
        CHECK (chapter_number BETWEEN 1 AND 18),
    CONSTRAINT chk_scripture_content_packages_content_version
        CHECK (content_version > 0),
    CONSTRAINT chk_scripture_content_packages_package_status
        CHECK (package_status IN ('APPROVED', 'SUPERSEDED', 'REVOKED')),
    CONSTRAINT chk_scripture_content_packages_package_checksum
        CHECK (package_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_scripture_content_packages_manifest_checksum
        CHECK (manifest_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_scripture_content_packages_provenance_checksum
        CHECK (provenance_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_scripture_content_packages_verses_checksum
        CHECK (verses_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_scripture_content_packages_importer_version
        CHECK (importer_version >= 1)
);

COMMENT ON TABLE scripture.content_packages IS
    'Successfully imported package identity and editorial lifecycle. DRAFT and failed '
    'attempts are never stored here. Does not store package blobs or Scripture text.';

COMMENT ON COLUMN scripture.content_packages.package_status IS
    'Editorial package lifecycle after successful import: APPROVED, SUPERSEDED, or REVOKED. '
    'Separate from content_package_imports.import_status.';

CREATE INDEX idx_scripture_content_packages_chapter_content_version
    ON scripture.content_packages (chapter_number, content_version);

-- At most one active APPROVED package per scripture + Chapter.
CREATE UNIQUE INDEX uq_scripture_content_packages_one_active_approved
    ON scripture.content_packages (scripture_id, chapter_number)
    WHERE package_status = 'APPROVED';

CREATE TABLE scripture.content_package_imports (
    id                      UUID            PRIMARY KEY,
    package_id              TEXT,
    attempted_package_id    TEXT            NOT NULL,
    package_checksum        VARCHAR(64)     NOT NULL,
    chapter_number          INTEGER,
    import_status           VARCHAR(32)     NOT NULL,
    records_read            INTEGER         NOT NULL,
    records_validated       INTEGER         NOT NULL,
    records_updated         INTEGER         NOT NULL,
    records_unchanged       INTEGER         NOT NULL,
    records_rejected        INTEGER         NOT NULL,
    failure_code            VARCHAR(64),
    failure_message         TEXT,
    importer_version        INTEGER         NOT NULL,
    started_at              TIMESTAMPTZ     NOT NULL,
    completed_at            TIMESTAMPTZ     NOT NULL,
    duration_ms             BIGINT          NOT NULL,
    CONSTRAINT fk_scripture_content_package_imports_package
        FOREIGN KEY (package_id) REFERENCES scripture.content_packages (package_id),
    CONSTRAINT chk_scripture_content_package_imports_status
        CHECK (import_status IN ('IMPORTED', 'FAILED', 'REVOKED', 'SUPERSEDED')),
    CONSTRAINT chk_scripture_content_package_imports_package_checksum
        CHECK (package_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_scripture_content_package_imports_counts
        CHECK (
            records_read >= 0
            AND records_validated >= 0
            AND records_updated >= 0
            AND records_unchanged >= 0
            AND records_rejected >= 0
        ),
    CONSTRAINT chk_scripture_content_package_imports_importer_version
        CHECK (importer_version >= 1),
    CONSTRAINT chk_scripture_content_package_imports_duration
        CHECK (duration_ms >= 0),
    CONSTRAINT chk_scripture_content_package_imports_chapter_number
        CHECK (chapter_number IS NULL OR chapter_number BETWEEN 1 AND 18),
    CONSTRAINT chk_scripture_content_package_imports_success_fk
        CHECK (
            (import_status = 'IMPORTED' AND package_id IS NOT NULL
                AND package_id = attempted_package_id)
            OR (import_status = 'FAILED' AND package_id IS NULL)
            OR (import_status IN ('REVOKED', 'SUPERSEDED'))
        ),
    CONSTRAINT chk_scripture_content_package_imports_failure_fields
        CHECK (
            (import_status = 'FAILED' AND failure_code IS NOT NULL)
            OR (import_status <> 'FAILED' AND failure_code IS NULL AND failure_message IS NULL)
        )
);

COMMENT ON TABLE scripture.content_package_imports IS
    'Durable import execution outcomes. VALIDATED is transient and not stored. '
    'FAILED rows do not register content_packages (package_id stays NULL). '
    'Dry-run never writes rows. failure_message must be sanitized metadata only.';

COMMENT ON COLUMN scripture.content_package_imports.package_id IS
    'FK to content_packages for successful (and later revoked/superseded) imports. '
    'NULL for FAILED attempts so failures never create active packages.';

COMMENT ON COLUMN scripture.content_package_imports.attempted_package_id IS
    'Package ID that was attempted. Always set; used for FAILED rows without an FK.';

COMMENT ON COLUMN scripture.content_package_imports.import_status IS
    'Import execution status: IMPORTED, FAILED, REVOKED, or SUPERSEDED. '
    'Not the editorial packageStatus from the package manifest.';

CREATE INDEX idx_scripture_content_package_imports_package_id
    ON scripture.content_package_imports (package_id)
    WHERE package_id IS NOT NULL;

CREATE INDEX idx_scripture_content_package_imports_attempted_package_id
    ON scripture.content_package_imports (attempted_package_id);

CREATE INDEX idx_scripture_content_package_imports_checksum_status
    ON scripture.content_package_imports (package_checksum, import_status);

-- Verse lineage: current content traces to an imported package.
ALTER TABLE scripture.verses
    ADD COLUMN source_package_id TEXT,
    ADD COLUMN source_package_checksum VARCHAR(64);

ALTER TABLE scripture.verses
    ADD CONSTRAINT fk_scripture_verses_source_package
        FOREIGN KEY (source_package_id) REFERENCES scripture.content_packages (package_id);

ALTER TABLE scripture.verses
    ADD CONSTRAINT chk_scripture_verses_source_package_checksum
        CHECK (
            source_package_checksum IS NULL
            OR source_package_checksum ~ '^[a-f0-9]{64}$'
        );

ALTER TABLE scripture.verses
    ADD CONSTRAINT chk_scripture_verses_source_package_pair
        CHECK (
            (source_package_id IS NULL AND source_package_checksum IS NULL)
            OR (source_package_id IS NOT NULL AND source_package_checksum IS NOT NULL)
        );

COMMENT ON COLUMN scripture.verses.source_package_id IS
    'Package that currently populates this Verse Sanskrit content. Null until first successful import.';

COMMENT ON COLUMN scripture.verses.source_package_checksum IS
    'Checksum of the package that currently populates this Verse. Must update with source_package_id and content_version.';

CREATE INDEX idx_scripture_verses_source_package_id
    ON scripture.verses (source_package_id);
