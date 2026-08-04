package com.antar.scripture.application.imports;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.ScripturePackageReadException;
import com.antar.scripture.application.port.ScripturePackageReader;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

/**
 * Post-validation package-read failures must become structured, path-safe results (no audit write).
 */
@SpringBootTest
@SkipInfrastructureTestsIfRequested
class PackageReadFailureImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportScripturePackageUseCase useCase;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockitoBean
    ScripturePackageReader scripturePackageReader;

    private SyntheticPackageFixtureBuilder fixtures;
    private Path sourcesRegistry;
    private Path approvedPackage;

    @BeforeEach
    void setUp() throws Exception {
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
        approvedPackage = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-read-fail",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        resetChapter12();
    }

    @AfterEach
    void tearDown() {
        resetChapter12();
    }

    private void resetChapter12() {
        jdbcTemplate.update(
                "UPDATE scripture.verses SET sanskrit_text = NULL, content_version = 1, "
                        + "source_package_id = NULL, source_package_checksum = NULL, "
                        + "updated_at = TIMESTAMPTZ '2026-08-01T00:00:00Z' "
                        + "WHERE canonical_reference LIKE '12.%'");
        jdbcTemplate.update("DELETE FROM scripture.content_package_imports");
        jdbcTemplate.update("DELETE FROM scripture.content_packages");
    }

    @Test
    void unixPathInReadFailureIsSanitizedAndWriteFree() {
        when(scripturePackageReader.read(any()))
                .thenThrow(new ScripturePackageReadException(new IOException(
                        "/Users/example/secret/pkg/manifest.json (Permission denied)")));

        ImportScripturePackageResult result = useCase.execute(command(true));

        assertStructuredReadFailure(result, true);
        assertThat(result.failureMessage())
                .isEqualTo(ScripturePackageReadException.STABLE_MESSAGE)
                .doesNotContain("/Users/")
                .doesNotContain("example")
                .doesNotContain("secret");
        assertCliSummaryPathSafe(result);
    }

    @Test
    void windowsPathInReadFailureIsSanitizedAndWriteFree() {
        when(scripturePackageReader.read(any()))
                .thenThrow(new ScripturePackageReadException(new IOException(
                        "C:\\Users\\example\\secret\\pkg\\manifest.json")));

        ImportScripturePackageResult result = useCase.execute(command(true));

        assertStructuredReadFailure(result, true);
        assertThat(result.failureMessage())
                .isEqualTo(ScripturePackageReadException.STABLE_MESSAGE)
                .doesNotContain("C:\\")
                .doesNotContain("Users\\example");
        assertCliSummaryPathSafe(result);
    }

    @Test
    void dryRunFalseReadFailureStillWriteFreeAndStructured() {
        when(scripturePackageReader.read(any()))
                .thenThrow(new ScripturePackageReadException(new IOException(
                        "file:///Users/example/pkg/verses.jsonl")));

        ImportScripturePackageResult result = useCase.execute(command(false));

        assertStructuredReadFailure(result, false);
        assertThat(result.failureMessage())
                .doesNotContain("file://")
                .doesNotContain("/Users/");
    }

    private ImportScripturePackageCommand command(boolean dryRun) {
        return new ImportScripturePackageCommand(
                approvedPackage,
                dryRun,
                PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry));
    }

    private void assertStructuredReadFailure(ImportScripturePackageResult result, boolean dryRun) {
        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_READ_FAILED);
        assertThat(result.dryRun()).isEqualTo(dryRun);
        assertThat(result.succeeded()).isFalse();
        assertThat(result.failureMessage())
                .doesNotContain("Exception")
                .doesNotContain("at com.antar")
                .doesNotContain("\tat ")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.verses WHERE sanskrit_text IS NOT NULL "
                                + "AND canonical_reference LIKE '12.%'",
                        Integer.class))
                .isZero();
    }

    private static void assertCliSummaryPathSafe(ImportScripturePackageResult result) {
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
                .contains("importStatus=FAILED")
                .contains("failureCode=PACKAGE_READ_FAILED")
                .contains("failureMessage=failed to read package")
                .contains("dryRun=" + result.dryRun())
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("Exception")
                .doesNotContain("at com.antar")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL");
    }
}
