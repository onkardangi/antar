package com.antar.scripture.application.port;

import java.util.List;

/**
 * Typed Package Format v1 validation result.
 *
 * <p>Import may proceed only when {@code structurallyValid}, {@code editoriallyValid}, and
 * {@code importable} are all true and {@code warnings} is empty.
 */
public record PackageValidationResult(
        boolean structurallyValid,
        boolean editoriallyValid,
        boolean importable,
        List<String> errors,
        List<String> warnings) {

    public PackageValidationResult {
        errors = List.copyOf(errors);
        warnings = List.copyOf(warnings);
    }

    public boolean mayProceedToImport() {
        return structurallyValid && editoriallyValid && importable && warnings.isEmpty();
    }
}
