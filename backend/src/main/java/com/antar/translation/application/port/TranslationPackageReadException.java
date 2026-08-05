package com.antar.translation.application.port;

/**
 * Raised when a structurally validated package cannot be read into domain records.
 */
public final class TranslationPackageReadException extends RuntimeException {

    public static final String STABLE_MESSAGE = "translation package could not be read";

    public TranslationPackageReadException() {
        super(STABLE_MESSAGE);
    }

    public TranslationPackageReadException(Throwable cause) {
        super(STABLE_MESSAGE, cause);
    }
}
