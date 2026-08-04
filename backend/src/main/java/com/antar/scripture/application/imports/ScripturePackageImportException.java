package com.antar.scripture.application.imports;

/**
 * Raised when package import cannot complete successfully.
 */
public final class ScripturePackageImportException extends RuntimeException {

    private final ImportScripturePackageResult result;

    public ScripturePackageImportException(ImportScripturePackageResult result) {
        super(sanitizeMessage(result));
        this.result = result;
    }

    public ImportScripturePackageResult result() {
        return result;
    }

    private static String sanitizeMessage(ImportScripturePackageResult result) {
        String code =
                result.failureCodeOptional().map(Enum::name).orElse("IMPORT_FAILED");
        String message = result.failureMessageOptional().orElse("Scripture package import failed");
        return code + ": " + message;
    }
}
