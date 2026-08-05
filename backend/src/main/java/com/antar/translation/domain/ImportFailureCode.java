package com.antar.translation.domain;

/**
 * Stable failure codes for Translation package import.
 *
 * <p>Safe for logs and audit rows. Never encode translation text.
 */
public enum ImportFailureCode {
    INVALID_PACKAGE_PATH,
    PACKAGE_VALIDATION_FAILED,
    PACKAGE_NOT_IMPORTABLE,
    PACKAGE_HAS_WARNINGS,
    PACKAGE_READ_FAILED,
    VERSE_IDENTITY_MISSING,
    RECORD_COUNT_MISMATCH,
    PACKAGE_IDENTITY_CONFLICT,
    CONTENT_VERSION_DOWNGRADE,
    CONTENT_VERSION_CONFLICT,
    IMPORT_MUTATION_FAILED
}
