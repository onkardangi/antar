package com.antar.translation.application.port;

import java.util.List;

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
