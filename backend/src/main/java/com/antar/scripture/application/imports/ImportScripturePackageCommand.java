package com.antar.scripture.application.imports;

import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.PackageValidationResult;
import java.nio.file.Path;
import java.util.Objects;

/**
 * Command for {@link ImportScripturePackageUseCase}.
 *
 * @param packagePath filesystem path to a Package Format v1 directory
 * @param dryRun when true, validate and compute counts with zero database writes
 * @param validationOptions optional validator path overrides (tests)
 */
public record ImportScripturePackageCommand(
        Path packagePath, boolean dryRun, PackageValidationOptions validationOptions) {

    public ImportScripturePackageCommand {
        Objects.requireNonNull(packagePath, "packagePath is required");
        if (validationOptions == null) {
            validationOptions = PackageValidationOptions.defaults();
        }
    }

    public static ImportScripturePackageCommand of(Path packagePath, boolean dryRun) {
        return new ImportScripturePackageCommand(packagePath, dryRun, PackageValidationOptions.defaults());
    }
}
