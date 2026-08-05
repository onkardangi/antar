package com.antar.translation.domain;

import java.util.Objects;
import java.util.UUID;

public final class TranslationId {

    private final UUID value;

    private TranslationId(UUID value) {
        this.value = Objects.requireNonNull(value, "TranslationId value is required");
    }

    public static TranslationId of(UUID value) {
        return new TranslationId(value);
    }

    public static TranslationId of(String value) {
        try {
            return new TranslationId(UUID.fromString(value));
        } catch (IllegalArgumentException | NullPointerException ex) {
            throw new InvalidTranslationIdException(value);
        }
    }

    public static TranslationId generate() {
        return new TranslationId(UUID.randomUUID());
    }

    public UUID value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationId that)) {
            return false;
        }
        return value.equals(that.value);
    }

    @Override
    public int hashCode() {
        return value.hashCode();
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
