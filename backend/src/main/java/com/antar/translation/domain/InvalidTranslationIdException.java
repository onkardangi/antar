package com.antar.translation.domain;

public final class InvalidTranslationIdException extends RuntimeException {

    public InvalidTranslationIdException(String value) {
        super("Invalid translation id: " + value);
    }
}
