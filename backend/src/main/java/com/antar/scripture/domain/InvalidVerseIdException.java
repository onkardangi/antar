package com.antar.scripture.domain;

public final class InvalidVerseIdException extends RuntimeException {

    private final String value;

    public InvalidVerseIdException(String value) {
        super("Verse id must be a valid UUID, but was '" + value + "'");
        this.value = value;
    }

    public String value() {
        return value;
    }
}
