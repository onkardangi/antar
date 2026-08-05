package com.antar.translation.domain;

import java.util.Objects;
import java.util.UUID;

/**
 * Verse identity reference held by Translation. UUID only — no Scripture aggregate dependency.
 */
public final class VerseId {

    private final UUID value;

    private VerseId(UUID value) {
        this.value = Objects.requireNonNull(value, "VerseId value is required");
    }

    public static VerseId of(UUID value) {
        return new VerseId(value);
    }

    public static VerseId of(String value) {
        try {
            return new VerseId(UUID.fromString(value));
        } catch (IllegalArgumentException | NullPointerException ex) {
            throw new InvalidVerseIdException(value);
        }
    }

    public UUID value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof VerseId that)) {
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
