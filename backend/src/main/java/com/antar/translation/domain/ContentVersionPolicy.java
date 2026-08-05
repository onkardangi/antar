package com.antar.translation.domain;

import java.util.Objects;

/**
 * Content-version and package-identity policy for Translation package import.
 */
public final class ContentVersionPolicy {

    public ContentVersionPolicy() {
    }

    public void assertCompatible(
            String incomingPackageId,
            String incomingPackageChecksum,
            long incomingContentVersion,
            Translation existing) {
        Objects.requireNonNull(incomingPackageId, "incomingPackageId is required");
        Objects.requireNonNull(incomingPackageChecksum, "incomingPackageChecksum is required");
        Objects.requireNonNull(existing, "existing is required");
        if (incomingContentVersion <= 0) {
            throw new IllegalArgumentException("incomingContentVersion must be positive");
        }

        long currentVersion = existing.contentVersion().value();
        boolean hasImportedContent = existing.sourcePackageId().isPresent();

        if (!hasImportedContent) {
            return;
        }

        if (incomingContentVersion < currentVersion) {
            throw new ContentVersionPolicyException(
                    ImportFailureCode.CONTENT_VERSION_DOWNGRADE,
                    "package contentVersion "
                            + incomingContentVersion
                            + " is lower than current Translation contentVersion "
                            + currentVersion);
        }

        if (incomingContentVersion == currentVersion) {
            String currentChecksum = existing.sourcePackageChecksum().orElse(null);
            boolean samePackage =
                    existing.sourcePackageId().map(incomingPackageId::equals).orElse(false)
                            && incomingPackageChecksum.equals(currentChecksum);
            if (samePackage) {
                return;
            }
            throw new ContentVersionPolicyException(
                    ImportFailureCode.CONTENT_VERSION_CONFLICT,
                    "same contentVersion with different package/content is not allowed");
        }

        if (existing
                .sourcePackageId()
                .map(id -> id.equals(incomingPackageId)
                        && !incomingPackageChecksum.equals(
                                existing.sourcePackageChecksum().orElse(null)))
                .orElse(false)) {
            throw new ContentVersionPolicyException(
                    ImportFailureCode.PACKAGE_IDENTITY_CONFLICT,
                    "package identity conflict for packageId " + incomingPackageId);
        }
    }

    public void assertPackageIdentity(
            String packageId, String packageChecksum, String existingPackageId, String existingChecksum) {
        Objects.requireNonNull(packageId, "packageId is required");
        Objects.requireNonNull(packageChecksum, "packageChecksum is required");
        if (existingPackageId == null) {
            return;
        }
        if (packageId.equals(existingPackageId) && !packageChecksum.equals(existingChecksum)) {
            throw new ContentVersionPolicyException(
                    ImportFailureCode.PACKAGE_IDENTITY_CONFLICT,
                    "same packageId with different packageChecksum");
        }
        if (!packageId.equals(existingPackageId) && packageChecksum.equals(existingChecksum)) {
            throw new ContentVersionPolicyException(
                    ImportFailureCode.PACKAGE_IDENTITY_CONFLICT,
                    "different packageId with identical packageChecksum");
        }
    }
}
