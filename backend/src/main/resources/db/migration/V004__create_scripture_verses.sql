-- Scripture module owns scripture.verses.
-- Creates Verse identity persistence for the Chapter slice.
--
-- sanskrit_text is nullable in this phase so Verse identity records may exist before
-- an approved Sanskrit corpus is imported. NULL means the approved Sanskrit corpus
-- has not yet been imported for that Verse. It must never hold engineering placeholder
-- prose, and NULL must never be treated as Scripture content.
--
-- Preview text for the Chapter screen is not a persisted column; it is supplied as a
-- temporary API placeholder until Translation content exists.

CREATE TABLE scripture.verses (
    id                  UUID            PRIMARY KEY,
    chapter_id          UUID            NOT NULL,
    verse_number        INTEGER         NOT NULL,
    canonical_reference TEXT            NOT NULL,
    sanskrit_text       TEXT,
    content_version     BIGINT          NOT NULL DEFAULT 1,
    publication_status  VARCHAR(32)     NOT NULL,
    created_at          TIMESTAMPTZ     NOT NULL,
    updated_at          TIMESTAMPTZ     NOT NULL,
    CONSTRAINT fk_scripture_verses_chapter
        FOREIGN KEY (chapter_id) REFERENCES scripture.chapters (id),
    CONSTRAINT uq_scripture_verses_chapter_verse_number
        UNIQUE (chapter_id, verse_number),
    CONSTRAINT uq_scripture_verses_canonical_reference
        UNIQUE (canonical_reference),
    CONSTRAINT chk_scripture_verses_verse_number
        CHECK (verse_number > 0),
    CONSTRAINT chk_scripture_verses_publication_status
        CHECK (publication_status IN ('DRAFT', 'IN_REVIEW', 'APPROVED', 'PUBLISHED', 'RETIRED')),
    CONSTRAINT chk_scripture_verses_content_version
        CHECK (content_version > 0),
    CONSTRAINT chk_scripture_verses_sanskrit_text_not_blank
        CHECK (sanskrit_text IS NULL OR length(btrim(sanskrit_text)) > 0)
);

COMMENT ON COLUMN scripture.verses.sanskrit_text IS
    'Canonical Sanskrit. NULL means the approved Sanskrit corpus has not yet been imported. '
    'Do not store engineering placeholders. Future Verse Reader queries must require non-NULL '
    'approved content before exposing Sanskrit as Scripture.';

-- Canonical listing within a Chapter.
CREATE INDEX idx_scripture_verses_chapter_id_verse_number
    ON scripture.verses (chapter_id, verse_number);

-- Exact reference lookup.
CREATE INDEX idx_scripture_verses_canonical_reference
    ON scripture.verses (canonical_reference);

-- Published Verse listing by Chapter in canonical order.
CREATE INDEX idx_scripture_verses_chapter_published_verse_number
    ON scripture.verses (chapter_id, verse_number)
    WHERE publication_status = 'PUBLISHED';
