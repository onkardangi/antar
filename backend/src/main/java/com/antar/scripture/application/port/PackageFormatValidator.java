package com.antar.scripture.application.port;

import java.nio.file.Path;
import java.util.List;

/**
 * Package Format v1 validation port.
 *
 * <p>Implementations perform Antar Package Format v1 structural and editorial checks. This is not a
 * standards-compliant JSON Schema engine unless explicitly documented as such.
 */
public interface PackageFormatValidator {

    PackageValidationResult validate(Path packageDirectory, PackageValidationOptions options);
}
