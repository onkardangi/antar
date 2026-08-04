package com.antar.scripture.domain;

/**
 * Stable failure codes for Scripture package import.
 *
 * <p>Safe for logs and audit rows. Never encode Scripture text.
 */
public enum ImportFailureCode {
    INVALID_PACKAGE_PATH,
    PACKAGE_VALIDATION_FAILED,
    PACKAGE_NOT_IMPORTABLE,
    PACKAGE_HAS_WARNINGS,
    PACKAGE_READ_FAILED,
    UNSUPPORTED_CONTENT_LAYER,
    CHAPTER_NOT_FOUND,
    VERSE_IDENTITY_MISSING,
    RECORD_COUNT_MISMATCH,
    PACKAGE_IDENTITY_CONFLICT,
    CONTENT_VERSION_DOWNGRADE,
    CONTENT_VERSION_CONFLICT,
    IMPORT_MUTATION_FAILED
}
