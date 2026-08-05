package com.antar.translation.domain;

import java.util.Objects;
import java.util.UUID;

public final class TranslationSourceId {

    private final UUID value;

    private TranslationSourceId(UUID value) {
        this.value = Objects.requireNonNull(value, "TranslationSourceId value is required");
    }

    public static TranslationSourceId of(UUID value) {
        return new TranslationSourceId(value);
    }

    public static TranslationSourceId generate() {
        return new TranslationSourceId(UUID.randomUUID());
    }

    public UUID value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationSourceId that)) {
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
