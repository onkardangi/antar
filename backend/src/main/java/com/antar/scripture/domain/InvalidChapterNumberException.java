package com.antar.scripture.domain;

public final class InvalidChapterNumberException extends RuntimeException {

    private final int chapterNumber;

    public InvalidChapterNumberException(int chapterNumber) {
        super("Chapter number must be between "
                + ChapterNumber.MIN
                + " and "
                + ChapterNumber.MAX
                + ", but was "
                + chapterNumber);
        this.chapterNumber = chapterNumber;
    }

    public int chapterNumber() {
        return chapterNumber;
    }
}
