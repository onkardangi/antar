package com.antar.scripture.application.imports;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.scripture.domain.ImportFailureCode;
import org.junit.jupiter.api.Test;

class ImportFailureSanitizerTest {

    @Test
    void stripsUnixAndMacUserPaths() {
        String sanitized = ImportFailureSanitizer.sanitize(
                "failed under /Users/example/secret/pkg and /home/runner/work",
                ImportFailureCode.IMPORT_MUTATION_FAILED.name());
        assertThat(sanitized)
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("example")
                .doesNotContain("secret");
    }

    @Test
    void stripsWindowsDriveAndFileUrls() {
        String sanitized = ImportFailureSanitizer.sanitize(
                "saw file:///C:/Users/x/pkg and C:\\Users\\x\\pkg",
                "import failed");
        assertThat(sanitized)
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("C:/Users");
    }

    @Test
    void rejectsVerseFixtureResidue() {
        String sanitized = ImportFailureSanitizer.sanitize(
                "mismatch FIXTURE_NON_SCRIPTURAL_VERSE_1",
                ImportFailureCode.IMPORT_MUTATION_FAILED.name());
        assertThat(sanitized).isEqualTo(ImportFailureCode.IMPORT_MUTATION_FAILED.name());
    }

    @Test
    void preservesStableAllowlistedMessages() {
        assertThat(ImportFailureSanitizer.sanitize("package directory does not exist", "fallback"))
                .isEqualTo("package directory does not exist");
        assertThat(ImportFailureSanitizer.sanitize("failed to parse package files", "fallback"))
                .isEqualTo("failed to parse package files");
    }
}
