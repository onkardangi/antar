package com.antar.translation.application.imports;

public final class TranslationPackageImportException extends RuntimeException {

    private final ImportTranslationPackageResult result;

    public TranslationPackageImportException(ImportTranslationPackageResult result) {
        super(result.failureMessage());
        this.result = result;
    }

    public ImportTranslationPackageResult result() {
        return result;
    }
}
