package com.antar.scripture.domain;

import java.util.Objects;
import java.util.UUID;

public final class ChapterId {

    private final UUID value;

    private ChapterId(UUID value) {
        this.value = Objects.requireNonNull(value, "ChapterId value is required");
    }

    public static ChapterId of(UUID value) {
        return new ChapterId(value);
    }

    public static ChapterId of(String value) {
        try {
            return new ChapterId(UUID.fromString(value));
        } catch (IllegalArgumentException | NullPointerException ex) {
            throw new InvalidChapterIdException(value);
        }
    }

    public static ChapterId generate() {
        return new ChapterId(UUID.randomUUID());
    }

    public UUID value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof ChapterId chapterId)) {
            return false;
        }
        return value.equals(chapterId.value);
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
