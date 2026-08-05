package com.antar.translation.infrastructure.importcmd;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.translation.application.imports.ImportTranslationPackageResult;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

class TranslationPackageImportMainPathSafetyTest {

    @Test
    void printedFailureSummaryDoesNotLeakAbsolutePathsOrTranslationText() {
        ImportTranslationPackageResult result = new ImportTranslationPackageResult(
                "fixture-pkg",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                new PackageValidationResult(
                        false, false, false, List.of("package directory does not exist"), List.of()),
                0,
                0,
                0,
                0,
                0,
                ImportExecutionStatus.FAILED,
                true,
                Duration.ofMillis(12),
                List.of(),
                ImportFailureCode.INVALID_PACKAGE_PATH,
                "package path must be an existing directory");

        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        PrintStream original = System.out;
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        try {
            TranslationPackageImportMain.printSummaryForTest(result);
        } finally {
            System.setOut(original);
        }

        String output = buffer.toString(StandardCharsets.UTF_8);
        assertThat(output)
                .contains("dryRun=true")
                .contains("failureCode=INVALID_PACKAGE_PATH")
                .contains("failureMessage=package path must be an existing directory")
                .contains("importStatus=FAILED")
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("FIXTURE_TRANSLATION")
                .doesNotContain("Exception")
                .doesNotContain("\tat ");
    }
}
