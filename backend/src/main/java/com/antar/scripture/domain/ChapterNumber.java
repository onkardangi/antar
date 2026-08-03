package com.antar.scripture.domain;

public final class ChapterNumber {

    public static final int MIN = 1;
    public static final int MAX = 18;

    private final int value;

    private ChapterNumber(int value) {
        if (value < MIN || value > MAX) {
            throw new InvalidChapterNumberException(value);
        }
        this.value = value;
    }

    public static ChapterNumber of(int value) {
        return new ChapterNumber(value);
    }

    public int value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof ChapterNumber chapterNumber)) {
            return false;
        }
        return value == chapterNumber.value;
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
