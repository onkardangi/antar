package com.antar.scripture.domain;

public final class InvalidChapterIdException extends RuntimeException {

    private final String chapterId;

    public InvalidChapterIdException(String chapterId) {
        super("Chapter id is not a valid UUID: " + chapterId);
        this.chapterId = chapterId;
    }

    public String chapterId() {
        return chapterId;
    }
}
