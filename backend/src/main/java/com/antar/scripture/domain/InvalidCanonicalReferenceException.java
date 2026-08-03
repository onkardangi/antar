package com.antar.scripture.domain;

public final class InvalidCanonicalReferenceException extends RuntimeException {

    private final String value;

    public InvalidCanonicalReferenceException(String value) {
        super("Canonical reference must be of the form chapter.verse within the Bhagavad Gita range, but was '"
                + value
                + "'");
        this.value = value;
    }

    public String value() {
        return value;
    }
}
