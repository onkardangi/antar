package com.antar.translation.application.imports;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import com.antar.translation.application.port.PackageFormatValidator;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import com.antar.translation.support.SyntheticTranslationPackageFixtureBuilder;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

/**
 * Proves importer rejects importable packages that still carry warnings.
 */
@SpringBootTest
@SkipInfrastructureTestsIfRequested
class WarningBearingTranslationImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportTranslationPackageUseCase useCase;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockitoBean
    PackageFormatValidator packageFormatValidator;

    private SyntheticTranslationPackageFixtureBuilder fixtures;

    @BeforeEach
    void setUp() {
        fixtures = new SyntheticTranslationPackageFixtureBuilder();
        resetTranslationState();
        when(packageFormatValidator.validate(any(), any()))
                .thenReturn(new PackageValidationResult(
                        true,
                        true,
                        true,
                        List.of(),
                        List.of("synthetic advisory warning for test")));
    }

    @AfterEach
    void tearDown() {
        resetTranslationState();
    }

    private void resetTranslationState() {
        jdbcTemplate.update("DELETE FROM translation.content_package_imports");
        jdbcTemplate.update("DELETE FROM translation.translations");
        jdbcTemplate.update("DELETE FROM translation.content_packages");
        jdbcTemplate.update("DELETE FROM translation.translation_sources");
    }

    @Test
    void rejectsWarningBearingApprovedPackageWithZeroWrites() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-warn",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ImportTranslationPackageResult result =
                useCase.execute(ImportTranslationPackageCommand.of(pkg, false));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_HAS_WARNINGS);
        assertThat(result.failureMessage())
                .contains("package validation produced warnings; importer rejects warnings");
        assertThat(result.dryRun()).isFalse();
        assertZeroWrites();
    }

    @Test
    void dryRunWarningRejectionReportsDryRunAndWritesNothing() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-warn-dry",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ImportTranslationPackageResult result =
                useCase.execute(ImportTranslationPackageCommand.of(pkg, true));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_HAS_WARNINGS);
        assertThat(result.dryRun()).isTrue();
        assertZeroWrites();
    }

    private void assertZeroWrites() {
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.translations", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.translation_sources", Integer.class))
                .isZero();
    }
}
