package com.antar.scripture.application.port;

/**
 * Thrown when an on-disk package cannot be read after validation.
 *
 * <p>Message must be stable and path-free. Preserve the cause for diagnostics only; never surface
 * {@code cause.getMessage()} to CLI, results, or audit rows.
 */
public final class ScripturePackageReadException extends RuntimeException {

    public static final String STABLE_MESSAGE = "failed to read package";

    public ScripturePackageReadException(Throwable cause) {
        super(STABLE_MESSAGE, cause);
    }

    public ScripturePackageReadException() {
        super(STABLE_MESSAGE);
    }
}
