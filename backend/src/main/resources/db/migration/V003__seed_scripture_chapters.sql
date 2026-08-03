-- Seed the 18 canonical Bhagavad Gita chapters.
-- Verse content is intentionally absent.
--
-- Naming sources:
-- - Chapters 1–2 canonicalName / englishName / shortIntent / verseCount follow
--   docs/architecture/04_API_CONTRACTS.md examples.
-- - Chapters 3–18 canonical Sanskrit yoga titles and traditional verse counts are
--   the widely attested Bhagavad Gita structure (700 verses total).
-- - englishName and shortIntent for chapters 3–18 are provisional editorial
--   placeholders pending an approved Antar content corpus. They are not Verse text.

INSERT INTO scripture.chapters (
    id,
    chapter_number,
    canonical_name,
    english_name,
    short_intent,
    verse_count,
    publication_status,
    content_version,
    created_at,
    updated_at
) VALUES
(
    '018f0000-0000-7000-8000-000000000001',
    1,
    'Arjuna Vishada Yoga',
    'The Yoga of Arjuna''s Despair',
    'A battlefield crisis becomes the beginning of inquiry.',
    47,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000002',
    2,
    'Sankhya Yoga',
    'The Yoga of Knowledge',
    'Action, wisdom, duty, and steadiness.',
    72,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000003',
    3,
    'Karma Yoga',
    'The Yoga of Action',
    'Action offered without attachment becomes a path.',
    43,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000004',
    4,
    'Jnana Karma Sanyasa Yoga',
    'The Yoga of Knowledge and Renunciation of Action',
    'Knowledge clarifies the meaning of action.',
    42,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000005',
    5,
    'Karma Sanyasa Yoga',
    'The Yoga of Renunciation',
    'Renunciation and action are reconciled.',
    29,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000006',
    6,
    'Atma Samyama Yoga',
    'The Yoga of Meditation',
    'Self-discipline steadies the mind.',
    47,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000007',
    7,
    'Jnana Vijnana Yoga',
    'The Yoga of Knowledge and Wisdom',
    'Knowing and realizing are distinguished.',
    30,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000008',
    8,
    'Akshara Brahma Yoga',
    'The Yoga of the Imperishable Absolute',
    'Attention turns toward what does not perish.',
    28,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000009',
    9,
    'Raja Vidya Raja Guhya Yoga',
    'The Yoga of Royal Knowledge and Royal Secret',
    'The most intimate teaching is offered openly.',
    34,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000a',
    10,
    'Vibhuti Yoga',
    'The Yoga of Divine Glories',
    'Manifestations point beyond themselves.',
    42,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000b',
    11,
    'Vishwarupa Darshana Yoga',
    'The Yoga of the Vision of the Universal Form',
    'Vision expands beyond ordinary sight.',
    55,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000c',
    12,
    'Bhakti Yoga',
    'The Yoga of Devotion',
    'Devotion becomes a path of nearness.',
    20,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000d',
    13,
    'Kshetra Kshetrajna Vibhaga Yoga',
    'The Yoga of the Field and the Knower of the Field',
    'The field and its knower are distinguished.',
    34,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000e',
    14,
    'Gunatraya Vibhaga Yoga',
    'The Yoga of the Three Gunas',
    'The qualities that shape nature are named.',
    27,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-00000000000f',
    15,
    'Purushottama Yoga',
    'The Yoga of the Supreme Person',
    'The supreme is described beyond the perishable.',
    20,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000010',
    16,
    'Daivasura Sampad Vibhaga Yoga',
    'The Yoga of the Divine and Demonic Qualities',
    'Contrasting qualities clarify the path.',
    24,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000011',
    17,
    'Shraddhatraya Vibhaga Yoga',
    'The Yoga of the Threefold Faith',
    'Faith itself is examined with care.',
    28,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
),
(
    '018f0000-0000-7000-8000-000000000012',
    18,
    'Moksha Sanyasa Yoga',
    'The Yoga of Liberation and Renunciation',
    'Renunciation and liberation are brought together.',
    78,
    'PUBLISHED',
    1,
    TIMESTAMPTZ '2026-08-01T00:00:00Z',
    TIMESTAMPTZ '2026-08-01T00:00:00Z'
);
