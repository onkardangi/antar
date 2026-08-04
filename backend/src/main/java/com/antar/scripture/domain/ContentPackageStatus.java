package com.antar.scripture.domain;

/**
 * Editorial lifecycle of an imported content package.
 *
 * <p>Distinct from {@link ImportExecutionStatus}. DRAFT packages are never persisted.
 */
public enum ContentPackageStatus {
    APPROVED,
    SUPERSEDED,
    REVOKED
}
