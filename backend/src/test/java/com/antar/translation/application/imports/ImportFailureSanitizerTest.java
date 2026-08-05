package com.antar.translation.application.imports;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class ImportFailureSanitizerTest {

    @Test
    void stripsAbsolutePaths() {
        String sanitized = ImportFailureSanitizer.sanitize(
                "failed at /Users/onkardangi/Desktop/Projects/antar/pkg", "fallback");
        assertThat(sanitized).doesNotContain("/Users/");
        assertThat(sanitized).contains("[path]");
    }

    @Test
    void replacesUnsafeFixtureResidue() {
        String sanitized = ImportFailureSanitizer.sanitize(
                "saw FIXTURE_TRANSLATION text", "fallback");
        assertThat(sanitized).isEqualTo("fallback");
    }
}
