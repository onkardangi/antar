package com.antar.scripture.application.port;

import java.nio.file.Path;
import java.util.Objects;
import java.util.Optional;

/**
 * Options for Package Format v1 validation.
 *
 * @param sourcesRegistryPath optional override for source registry JSON; when empty the adapter
 *     default is used
 * @param verseCountsPath optional override for Antar verse-count JSON; when empty the adapter
 *     default is used
 */
public record PackageValidationOptions(Path sourcesRegistryPath, Path verseCountsPath) {

    public static PackageValidationOptions defaults() {
        return new PackageValidationOptions(null, null);
    }

    public PackageValidationOptions {
        // nullable overrides are intentional
    }

    public Optional<Path> sourcesRegistryPathOptional() {
        return Optional.ofNullable(sourcesRegistryPath);
    }

    public Optional<Path> verseCountsPathOptional() {
        return Optional.ofNullable(verseCountsPath);
    }

    public PackageValidationOptions withSourcesRegistry(Path path) {
        return new PackageValidationOptions(Objects.requireNonNull(path), verseCountsPath);
    }

    public PackageValidationOptions withVerseCounts(Path path) {
        return new PackageValidationOptions(sourcesRegistryPath, Objects.requireNonNull(path));
    }
}
