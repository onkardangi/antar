package com.antar.translation.domain;

public final class InvalidVerseIdException extends RuntimeException {

    public InvalidVerseIdException(String value) {
        super("Invalid verse id: " + value);
    }
}
