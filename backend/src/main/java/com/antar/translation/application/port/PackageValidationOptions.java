package com.antar.translation.application.port;

import java.nio.file.Path;
import java.util.Objects;
import java.util.Optional;

public record PackageValidationOptions(Path sourcesRegistryPath) {

    public static PackageValidationOptions defaults() {
        return new PackageValidationOptions(null);
    }

    public Optional<Path> sourcesRegistryPathOptional() {
        return Optional.ofNullable(sourcesRegistryPath);
    }

    public PackageValidationOptions withSourcesRegistry(Path path) {
        return new PackageValidationOptions(Objects.requireNonNull(path));
    }
}
