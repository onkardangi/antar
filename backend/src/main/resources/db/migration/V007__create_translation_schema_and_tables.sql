-- Translation module owns translation.* tables.
-- References scripture.verses by FK for Verse identity only.
-- Does not modify scripture.verses or store commentary.

CREATE SCHEMA IF NOT EXISTS translation;

CREATE TABLE translation.translation_sources (
    id                  UUID            PRIMARY KEY,
    provider            TEXT            NOT NULL,
    name                TEXT            NOT NULL,
    language_code       TEXT            NOT NULL,
    license_type        TEXT            NOT NULL,
    license_reference   TEXT,
    publication_status  VARCHAR(32)     NOT NULL,
    created_at          TIMESTAMPTZ     NOT NULL,
    updated_at          TIMESTAMPTZ     NOT NULL,
    CONSTRAINT uq_translation_sources_provider_language
        UNIQUE (provider, language_code),
    CONSTRAINT chk_translation_sources_publication_status
        CHECK (publication_status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'RETIRED')),
    CONSTRAINT chk_translation_sources_provider_not_blank
        CHECK (length(btrim(provider)) > 0),
    CONSTRAINT chk_translation_sources_name_not_blank
        CHECK (length(btrim(name)) > 0),
    CONSTRAINT chk_translation_sources_language_not_blank
        CHECK (length(btrim(language_code)) > 0),
    CONSTRAINT chk_translation_sources_license_type_not_blank
        CHECK (length(btrim(license_type)) > 0)
);

COMMENT ON TABLE translation.translation_sources IS
    'Identifiable translation edition / provider. Licensing is mandatory before publication.';

CREATE TABLE translation.content_packages (
    package_id                   TEXT            NOT NULL,
    package_format_version       INTEGER         NOT NULL,
    scripture_id                 TEXT            NOT NULL,
    chapter_number               INTEGER         NOT NULL,
    language_code                TEXT            NOT NULL,
    provider                     TEXT            NOT NULL,
    content_version              BIGINT          NOT NULL,
    package_status               VARCHAR(32)     NOT NULL,
    package_checksum             VARCHAR(64)     NOT NULL,
    manifest_checksum            VARCHAR(64)     NOT NULL,
    provenance_checksum          VARCHAR(64)     NOT NULL,
    translations_checksum        VARCHAR(64)     NOT NULL,
    source_registry_references   JSONB           NOT NULL,
    importer_version             INTEGER         NOT NULL,
    first_imported_at            TIMESTAMPTZ,
    last_verified_at             TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ     NOT NULL,
    updated_at                   TIMESTAMPTZ     NOT NULL,
    CONSTRAINT pk_translation_content_packages
        PRIMARY KEY (package_id),
    CONSTRAINT uq_translation_content_packages_checksum
        UNIQUE (package_checksum),
    CONSTRAINT chk_translation_content_packages_format_version
        CHECK (package_format_version >= 1),
    CONSTRAINT chk_translation_content_packages_chapter_number
        CHECK (chapter_number BETWEEN 1 AND 18),
    CONSTRAINT chk_translation_content_packages_content_version
        CHECK (content_version > 0),
    CONSTRAINT chk_translation_content_packages_package_status
        CHECK (package_status IN ('APPROVED', 'SUPERSEDED', 'REVOKED')),
    CONSTRAINT chk_translation_content_packages_package_checksum
        CHECK (package_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_translation_content_packages_manifest_checksum
        CHECK (manifest_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_translation_content_packages_provenance_checksum
        CHECK (provenance_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_translation_content_packages_translations_checksum
        CHECK (translations_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_translation_content_packages_importer_version
        CHECK (importer_version >= 1),
    CONSTRAINT chk_translation_content_packages_language_not_blank
        CHECK (length(btrim(language_code)) > 0),
    CONSTRAINT chk_translation_content_packages_provider_not_blank
        CHECK (length(btrim(provider)) > 0)
);

COMMENT ON TABLE translation.content_packages IS
    'Successfully imported Translation package identity and editorial lifecycle. '
    'DRAFT and failed attempts are never stored here.';

CREATE INDEX idx_translation_content_packages_chapter_content_version
    ON translation.content_packages (chapter_number, content_version);

-- At most one active APPROVED package per language + provider + scripture + Chapter.
CREATE UNIQUE INDEX uq_translation_content_packages_one_active_approved
    ON translation.content_packages (language_code, provider, scripture_id, chapter_number)
    WHERE package_status = 'APPROVED';

CREATE TABLE translation.content_package_imports (
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
    CONSTRAINT fk_translation_content_package_imports_package
        FOREIGN KEY (package_id) REFERENCES translation.content_packages (package_id),
    CONSTRAINT chk_translation_content_package_imports_status
        CHECK (import_status IN ('IMPORTED', 'FAILED', 'REVOKED', 'SUPERSEDED')),
    CONSTRAINT chk_translation_content_package_imports_package_checksum
        CHECK (package_checksum ~ '^[a-f0-9]{64}$'),
    CONSTRAINT chk_translation_content_package_imports_counts
        CHECK (
            records_read >= 0
            AND records_validated >= 0
            AND records_updated >= 0
            AND records_unchanged >= 0
            AND records_rejected >= 0
        ),
    CONSTRAINT chk_translation_content_package_imports_importer_version
        CHECK (importer_version >= 1),
    CONSTRAINT chk_translation_content_package_imports_duration
        CHECK (duration_ms >= 0),
    CONSTRAINT chk_translation_content_package_imports_chapter_number
        CHECK (chapter_number IS NULL OR chapter_number BETWEEN 1 AND 18),
    CONSTRAINT chk_translation_content_package_imports_success_fk
        CHECK (
            (import_status = 'IMPORTED' AND package_id IS NOT NULL
                AND package_id = attempted_package_id)
            OR (import_status = 'FAILED' AND package_id IS NULL)
            OR (import_status IN ('REVOKED', 'SUPERSEDED'))
        ),
    CONSTRAINT chk_translation_content_package_imports_failure_fields
        CHECK (
            (import_status = 'FAILED' AND failure_code IS NOT NULL)
            OR (import_status <> 'FAILED' AND failure_code IS NULL AND failure_message IS NULL)
        )
);

COMMENT ON TABLE translation.content_package_imports IS
    'Durable Translation import execution outcomes. VALIDATED is transient and not stored. '
    'FAILED rows do not register content_packages. Dry-run never writes rows.';

CREATE INDEX idx_translation_content_package_imports_package_id
    ON translation.content_package_imports (package_id)
    WHERE package_id IS NOT NULL;

CREATE INDEX idx_translation_content_package_imports_attempted_package_id
    ON translation.content_package_imports (attempted_package_id);

CREATE INDEX idx_translation_content_package_imports_checksum_status
    ON translation.content_package_imports (package_checksum, import_status);

CREATE TABLE translation.translations (
    id                          UUID            PRIMARY KEY,
    verse_id                    UUID            NOT NULL,
    translation_source_id       UUID            NOT NULL,
    language_code               TEXT            NOT NULL,
    provider                    TEXT            NOT NULL,
    translation_text            TEXT            NOT NULL,
    publication_status          VARCHAR(32)     NOT NULL,
    content_version             BIGINT          NOT NULL DEFAULT 1,
    source_package_id           TEXT,
    source_package_checksum     VARCHAR(64),
    created_at                  TIMESTAMPTZ     NOT NULL,
    updated_at                  TIMESTAMPTZ     NOT NULL,
    CONSTRAINT fk_translation_translations_verse
        FOREIGN KEY (verse_id) REFERENCES scripture.verses (id),
    CONSTRAINT fk_translation_translations_source
        FOREIGN KEY (translation_source_id) REFERENCES translation.translation_sources (id),
    CONSTRAINT fk_translation_translations_source_package
        FOREIGN KEY (source_package_id) REFERENCES translation.content_packages (package_id),
    CONSTRAINT uq_translation_translations_verse_source
        UNIQUE (verse_id, translation_source_id),
    CONSTRAINT chk_translation_translations_publication_status
        CHECK (publication_status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'RETIRED')),
    CONSTRAINT chk_translation_translations_content_version
        CHECK (content_version > 0),
    CONSTRAINT chk_translation_translations_text_not_blank
        CHECK (length(btrim(translation_text)) > 0),
    CONSTRAINT chk_translation_translations_language_not_blank
        CHECK (length(btrim(language_code)) > 0),
    CONSTRAINT chk_translation_translations_provider_not_blank
        CHECK (length(btrim(provider)) > 0),
    CONSTRAINT chk_translation_translations_source_package_checksum
        CHECK (
            source_package_checksum IS NULL
            OR source_package_checksum ~ '^[a-f0-9]{64}$'
        ),
    CONSTRAINT chk_translation_translations_source_package_pair
        CHECK (
            (source_package_id IS NULL AND source_package_checksum IS NULL)
            OR (source_package_id IS NOT NULL AND source_package_checksum IS NOT NULL)
        )
);

COMMENT ON TABLE translation.translations IS
    'Per-Verse translation text owned by the Translation module. No commentary or notes.';

CREATE INDEX idx_translation_translations_verse_id
    ON translation.translations (verse_id);

CREATE INDEX idx_translation_translations_verse_published
    ON translation.translations (verse_id)
    WHERE publication_status = 'PUBLISHED';

CREATE INDEX idx_translation_translations_source_package_id
    ON translation.translations (source_package_id);
