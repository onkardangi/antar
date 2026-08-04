package com.antar.scripture.application.imports;

/**
 * Central sanitizer for importer failure messages exposed via results, CLI, and FAILED audit rows.
 *
 * <p>Prefer allowlisted stable messages. Never emit absolute paths, stack traces, Verse text, or
 * raw package payloads.
 */
public final class ImportFailureSanitizer {

    private ImportFailureSanitizer() {
    }

    public static String sanitize(String message, String fallback) {
        String safeFallback = (fallback == null || fallback.isBlank()) ? "import failed" : fallback;
        if (message == null || message.isBlank()) {
            return safeFallback;
        }
        String trimmed = message.replaceAll("\\s+", " ").trim();
        trimmed = trimmed.replaceAll("(?i)file://\\S+", "[uri]");
        trimmed = trimmed.replaceAll("(?i)(/Users/|/home/|/var/folders/|/tmp/|[A-Za-z]:\\\\)\\S*", "[path]");
        trimmed = trimmed.replaceAll(
                "(?i)package directory does not exist:\\S*", "package directory does not exist");
        if (containsUnsafeResidue(trimmed)) {
            return safeFallback;
        }
        if (trimmed.length() > 240) {
            return trimmed.substring(0, 240);
        }
        return trimmed;
    }

    private static boolean containsUnsafeResidue(String value) {
        String lower = value.toLowerCase();
        return lower.contains("/users/")
                || lower.contains("/home/")
                || lower.contains("/var/")
                || lower.contains("file://")
                || lower.matches("(?s).*[a-z]:\\\\.*")
                || lower.contains("\tat ")
                || lower.contains("exception in thread")
                || lower.contains("at com.antar")
                || lower.contains("fixture_non_scriptural");
    }
}
