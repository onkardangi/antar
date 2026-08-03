package com.antar.scripture.domain;

public final class InvalidVerseNumberException extends RuntimeException {

    private final int verseNumber;

    public InvalidVerseNumberException(int verseNumber) {
        super("Verse number must be positive, but was " + verseNumber);
        this.verseNumber = verseNumber;
    }

    public int verseNumber() {
        return verseNumber;
    }
}
