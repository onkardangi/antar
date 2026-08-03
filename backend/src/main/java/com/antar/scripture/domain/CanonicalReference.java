package com.antar.scripture.domain;

import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Stable human-readable Verse identity of the form {@code chapter.verse}, e.g. {@code 2.47}.
 */
public final class CanonicalReference {

    private static final Pattern PATTERN = Pattern.compile("^(\\d{1,2})\\.(\\d{1,3})$");

    private final ChapterNumber chapterNumber;
    private final VerseNumber verseNumber;
    private final String value;

    private CanonicalReference(ChapterNumber chapterNumber, VerseNumber verseNumber) {
        this.chapterNumber = Objects.requireNonNull(chapterNumber, "chapterNumber is required");
        this.verseNumber = Objects.requireNonNull(verseNumber, "verseNumber is required");
        this.value = chapterNumber.value() + "." + verseNumber.value();
    }

    public static CanonicalReference of(ChapterNumber chapterNumber, VerseNumber verseNumber) {
        return new CanonicalReference(chapterNumber, verseNumber);
    }

    public static CanonicalReference parse(String raw) {
        if (raw == null || raw.isBlank()) {
            throw new InvalidCanonicalReferenceException(raw);
        }
        Matcher matcher = PATTERN.matcher(raw.trim());
        if (!matcher.matches()) {
            throw new InvalidCanonicalReferenceException(raw);
        }
        int chapter = Integer.parseInt(matcher.group(1));
        int verse = Integer.parseInt(matcher.group(2));
        try {
            return of(ChapterNumber.of(chapter), VerseNumber.of(verse));
        } catch (InvalidChapterNumberException | InvalidVerseNumberException ex) {
            throw new InvalidCanonicalReferenceException(raw);
        }
    }

    public ChapterNumber chapterNumber() {
        return chapterNumber;
    }

    public VerseNumber verseNumber() {
        return verseNumber;
    }

    public String value() {
        return value;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof CanonicalReference that)) {
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
