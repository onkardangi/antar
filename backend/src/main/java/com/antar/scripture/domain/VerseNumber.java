package com.antar.scripture.domain;

public final class VerseNumber {

    private final int value;

    private VerseNumber(int value) {
        if (value <= 0) {
            throw new InvalidVerseNumberException(value);
        }
        this.value = value;
    }

    public static VerseNumber of(int value) {
        return new VerseNumber(value);
    }

    public int value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof VerseNumber verseNumber)) {
            return false;
        }
        return value == verseNumber.value;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(value);
    }

    @Override
    public String toString() {
        return Integer.toString(value);
    }
}
