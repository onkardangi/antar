package com.antar.translation.domain;

import java.util.Objects;

public final class TranslationLanguage {

    private final String code;

    private TranslationLanguage(String code) {
        String normalized = Objects.requireNonNull(code, "language code is required").trim();
        if (normalized.isEmpty()) {
            throw new IllegalArgumentException("language code must be non-blank");
        }
        this.code = normalized.toLowerCase();
    }

    public static TranslationLanguage of(String code) {
        return new TranslationLanguage(code);
    }

    public String code() {
        return code;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationLanguage that)) {
            return false;
        }
        return code.equals(that.code);
    }

    @Override
    public int hashCode() {
        return code.hashCode();
    }

    @Override
    public String toString() {
        return code;
    }
}
