package com.antar.translation.domain;

import java.util.Objects;

public final class TranslationText {

    private final String value;

    private TranslationText(String value) {
        String normalized = Objects.requireNonNull(value, "translation text is required").trim();
        if (normalized.isEmpty()) {
            throw new IllegalArgumentException("translation text must be non-blank");
        }
        this.value = normalized;
    }

    public static TranslationText of(String value) {
        return new TranslationText(value);
    }

    public String value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationText that)) {
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
        return value;
    }
}
