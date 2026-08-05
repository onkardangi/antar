package com.antar.translation.domain;

/**
 * Content version for Translation text and packages. Positive monotonic integer.
 */
public final class TranslationVersion {

    private final long value;

    private TranslationVersion(long value) {
        if (value <= 0) {
            throw new IllegalArgumentException("contentVersion must be positive");
        }
        this.value = value;
    }

    public static TranslationVersion of(long value) {
        return new TranslationVersion(value);
    }

    public long value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof TranslationVersion that)) {
            return false;
        }
        return value == that.value;
    }

    @Override
    public int hashCode() {
        return Long.hashCode(value);
    }

    @Override
    public String toString() {
        return Long.toString(value);
    }
}
