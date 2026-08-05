package com.antar.translation.domain;

import java.util.Objects;

public final class TranslationProvider {

    private final String value;

    private TranslationProvider(String value) {
        String normalized = Objects.requireNonNull(value, "provider is required").trim();
        if (normalized.isEmpty()) {
            throw new IllegalArgumentException("provider must be non-blank");
        }
        this.value = normalized;
    }

    public static TranslationProvider of(String value) {
        return new TranslationProvider(value);
    }

    public String value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationProvider that)) {
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
