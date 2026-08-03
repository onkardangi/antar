-- Seed Verse identities for all 18 Chapters.
--
-- Counts: derived from scripture.chapters.verse_count seeded in V003
-- (canonical Bhagavad Gita structure; 700 verses total).
--
-- Content:
-- - sanskrit_text is NULL. NULL means the approved Sanskrit corpus has not yet been
--   imported. Engineering placeholder prose must never be stored in this column.
-- - Chapter-screen previewText is not stored here; the Reader API returns a temporary
--   product placeholder ("Verse preview unavailable") until Translation content exists.
-- - The future Verse Reader slice requires approved Sanskrit (and licensed Translation /
--   Transliteration where applicable) before displaying full Verse content.

INSERT INTO scripture.verses (
    id,
    chapter_id,
    verse_number,
    canonical_reference,
    sanskrit_text,
    content_version,
    publication_status,
    created_at,
    updated_at
)
SELECT
    md5('scripture.verse.' || c.chapter_number || '.' || v.verse_number)::uuid,
    c.id,
    v.verse_number,
    c.chapter_number || '.' || v.verse_number,
    NULL,
    1,
    'PUBLISHED',
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
FROM scripture.chapters c
CROSS JOIN LATERAL generate_series(1, c.verse_count) AS v(verse_number);
