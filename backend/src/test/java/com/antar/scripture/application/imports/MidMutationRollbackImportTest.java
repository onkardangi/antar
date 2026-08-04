package com.antar.scripture.application.imports;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.ResolvedScripturePackage;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import com.antar.scripture.domain.Verse;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;
import org.springframework.jdbc.core.JdbcTemplate;

/**
 * Forces failure after Verse mutation writes begin; proves TX rollback + REQUIRES_NEW FAILED audit.
 */
@SpringBootTest
@SkipInfrastructureTestsIfRequested
@Import(MidMutationRollbackImportTest.FailingProbeConfig.class)
class MidMutationRollbackImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;
    private static final AtomicBoolean FAIL_NEXT = new AtomicBoolean(false);

    @TempDir
    Path tempDir;

    @Autowired
    ImportScripturePackageUseCase useCase;

    @Autowired
    ContentPackageRepository contentPackageRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    private SyntheticPackageFixtureBuilder fixtures;
    private Path sourcesRegistry;

    @BeforeEach
    void setUp() throws Exception {
        FAIL_NEXT.set(false);
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
        resetChapter12();
    }

    @org.junit.jupiter.api.AfterEach
    void tearDown() {
        FAIL_NEXT.set(false);
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
    void midMutationFailureRollsBackAndWritesSanitizedFailedAudit() throws Exception {
        Path prior = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-prior-ok",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_PRIOR_");
        assertThat(useCase.execute(command(prior, false)).succeeded()).isTrue();

        Path next = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("next"),
                "fixture-chapter-12-mid-fail",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_NON_SCRIPTURAL_NEXT_");

        FAIL_NEXT.set(true);
        ImportScripturePackageResult failed = useCase.execute(command(next, false));
        FAIL_NEXT.set(false);

        assertThat(failed.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(failed.failureCode()).isEqualTo(ImportFailureCode.IMPORT_MUTATION_FAILED);
        assertThat(failed.failureMessageOptional().orElse(""))
                .doesNotContain("/Users/")
                .doesNotContain("/tmp/")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL_NEXT_")
                .doesNotContain("Exception")
                .doesNotContain("at com.antar");

        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages WHERE package_id = ?",
                        Integer.class,
                        "fixture-chapter-12-mid-fail"))
                .isZero();
        assertThat(contentPackageRepository
                        .findActiveApprovedByScriptureAndChapter("bhagavad-gita", CHAPTER)
                        .map(ContentPackageRepository.ContentPackageRecord::packageId))
                .contains("fixture-chapter-12-prior-ok");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM scripture.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-chapter-12-prior-ok"))
                .isEqualTo("APPROVED");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT sanskrit_text FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_NON_SCRIPTURAL_PRIOR_1");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports WHERE import_status = 'FAILED'",
                        Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_id FROM scripture.content_package_imports WHERE import_status = 'FAILED'",
                        String.class))
                .isNull();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT attempted_package_id FROM scripture.content_package_imports WHERE import_status = 'FAILED'",
                        String.class))
                .isEqualTo("fixture-chapter-12-mid-fail");
        String failedMessage = jdbcTemplate.queryForObject(
                "SELECT failure_message FROM scripture.content_package_imports WHERE import_status = 'FAILED'",
                String.class);
        assertThat(failedMessage)
                .doesNotContain("/Users/")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL")
                .doesNotContain("Exception");

        // Later valid retry succeeds.
        ImportScripturePackageResult retry = useCase.execute(command(next, false));
        assertThat(retry.succeeded()).isTrue();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM scripture.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-chapter-12-prior-ok"))
                .isEqualTo("SUPERSEDED");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT source_package_id FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("fixture-chapter-12-mid-fail");
    }

    private ImportScripturePackageCommand command(Path pkg, boolean dryRun) {
        return new ImportScripturePackageCommand(
                pkg, dryRun, PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry));
    }

    @TestConfiguration
    static class FailingProbeConfig {
        @Bean
        @Primary
        ImportMutationProbe failingImportMutationProbe() {
            return (ResolvedScripturePackage pkg, List<Verse> updatedVerses) -> {
                if (FAIL_NEXT.get() && !updatedVerses.isEmpty()) {
                    throw new IllegalStateException(
                            "forced mid-mutation failure for " + pkg.packageId()
                                    + " at /Users/example/secret/path with "
                                    + updatedVerses.getFirst().sanskritText());
                }
            };
        }
    }
}
