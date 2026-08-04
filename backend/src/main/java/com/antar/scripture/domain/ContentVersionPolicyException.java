package com.antar.scripture.domain;

/**
 * Raised when package identity or content-version policy rejects an import.
 */
public final class ContentVersionPolicyException extends RuntimeException {

    private final ImportFailureCode failureCode;

    public ContentVersionPolicyException(ImportFailureCode failureCode, String message) {
        super(message);
        this.failureCode = failureCode;
    }

    public ImportFailureCode failureCode() {
        return failureCode;
    }
}
