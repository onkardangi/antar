package com.antar.translation.application.imports;

import com.antar.translation.application.port.PackageValidationOptions;
import java.nio.file.Path;
import java.util.Objects;

public record ImportTranslationPackageCommand(
        Path packagePath, boolean dryRun, PackageValidationOptions validationOptions) {

    public ImportTranslationPackageCommand {
        Objects.requireNonNull(packagePath, "packagePath is required");
        Objects.requireNonNull(validationOptions, "validationOptions is required");
    }

    public static ImportTranslationPackageCommand of(Path packagePath, boolean dryRun) {
        return new ImportTranslationPackageCommand(packagePath, dryRun, PackageValidationOptions.defaults());
    }
}
