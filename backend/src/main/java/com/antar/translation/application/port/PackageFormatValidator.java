package com.antar.translation.application.port;

import java.nio.file.Path;

public interface PackageFormatValidator {

    PackageValidationResult validate(Path packageDirectory, PackageValidationOptions options);
}
