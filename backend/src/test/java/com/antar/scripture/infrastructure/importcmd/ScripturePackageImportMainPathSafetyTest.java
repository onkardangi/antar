package com.antar.scripture.infrastructure.importcmd;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.scripture.application.imports.ImportScripturePackageResult;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

class ScripturePackageImportMainPathSafetyTest {

    @Test
    void printedFailureSummaryDoesNotLeakAbsolutePathsOrVerseText() {
        ImportScripturePackageResult result = new ImportScripturePackageResult(
                "fixture-pkg",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                new PackageValidationResult(false, false, false, List.of("package directory does not exist"), List.of()),
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
            ScripturePackageImportMain.printSummaryForTest(result);
        } finally {
            System.setOut(original);
        }

        String output = buffer.toString(StandardCharsets.UTF_8);
        assertThat(output)
                .contains("dryRun=true")
                .contains("failureMessage=package path must be an existing directory")
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL");
    }
}
