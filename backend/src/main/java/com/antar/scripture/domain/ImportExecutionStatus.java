package com.antar.scripture.domain;

/**
 * Durable import execution outcome.
 *
 * <p>Distinct from editorial {@link ContentPackageStatus}. {@code VALIDATED} is transient and is
 * not persisted.
 */
public enum ImportExecutionStatus {
    IMPORTED,
    FAILED,
    REVOKED,
    SUPERSEDED
}
