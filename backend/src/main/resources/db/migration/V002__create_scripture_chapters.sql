-- Scripture module owns scripture.chapters.
-- Creates Chapter persistence only. No Verse tables in this migration.

CREATE TABLE scripture.chapters (
    id                  UUID            PRIMARY KEY,
    chapter_number      SMALLINT        NOT NULL,
    canonical_name      TEXT            NOT NULL,
    english_name        TEXT            NOT NULL,
    short_intent        TEXT            NOT NULL,
    verse_count         INTEGER         NOT NULL,
    publication_status  VARCHAR(32)     NOT NULL,
    content_version     BIGINT          NOT NULL DEFAULT 1,
    created_at          TIMESTAMPTZ     NOT NULL,
    updated_at          TIMESTAMPTZ     NOT NULL,
    CONSTRAINT uq_scripture_chapters_chapter_number UNIQUE (chapter_number),
    CONSTRAINT chk_scripture_chapters_chapter_number
        CHECK (chapter_number BETWEEN 1 AND 18),
    CONSTRAINT chk_scripture_chapters_verse_count
        CHECK (verse_count > 0),
    CONSTRAINT chk_scripture_chapters_publication_status
        CHECK (publication_status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'RETIRED')),
    CONSTRAINT chk_scripture_chapters_content_version
        CHECK (content_version >= 0)
);

CREATE INDEX idx_scripture_chapters_chapter_number
    ON scripture.chapters (chapter_number);

CREATE INDEX idx_scripture_chapters_publication_status
    ON scripture.chapters (publication_status);
