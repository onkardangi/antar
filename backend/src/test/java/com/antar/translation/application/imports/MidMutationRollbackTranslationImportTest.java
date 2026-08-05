package com.antar.translation.application.imports;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import com.antar.translation.domain.Translation;
import com.antar.translation.support.SyntheticTranslationPackageFixtureBuilder;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import org.junit.jupiter.api.AfterEach;
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

@SpringBootTest
@SkipInfrastructureTestsIfRequested
@Import(MidMutationRollbackTranslationImportTest.FailingProbeConfig.class)
class MidMutationRollbackTranslationImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;
    private static final AtomicBoolean FAIL_NEXT = new AtomicBoolean(false);

    @TempDir
    Path tempDir;

    @Autowired
    ImportTranslationPackageUseCase useCase;

    @Autowired
    TranslationContentPackageRepository contentPackageRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    private SyntheticTranslationPackageFixtureBuilder fixtures;

    @BeforeEach
    void setUp() {
        FAIL_NEXT.set(false);
        fixtures = new SyntheticTranslationPackageFixtureBuilder();
        reset();
    }

    @AfterEach
    void tearDown() {
        FAIL_NEXT.set(false);
        reset();
    }

    private void reset() {
        jdbcTemplate.update("DELETE FROM translation.content_package_imports");
        jdbcTemplate.update("DELETE FROM translation.translations");
        jdbcTemplate.update("DELETE FROM translation.content_packages");
        jdbcTemplate.update("DELETE FROM translation.translation_sources");
    }

    @Test
    void midMutationFailureRollsBackAndWritesSanitizedFailedAudit() throws Exception {
        Path prior = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-prior-ok",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_PRIOR_");
        assertThat(useCase.execute(ImportTranslationPackageCommand.of(prior, false)).succeeded())
                .isTrue();

        Path next = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("next"),
                "fixture-translation-chapter-12-mid-fail",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_TRANSLATION_NEXT_");

        FAIL_NEXT.set(true);
        ImportTranslationPackageResult failed =
                useCase.execute(ImportTranslationPackageCommand.of(next, false));
        FAIL_NEXT.set(false);

        assertThat(failed.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(failed.failureCode()).isEqualTo(ImportFailureCode.IMPORT_MUTATION_FAILED);
        assertThat(failed.failureMessageOptional().orElse(""))
                .doesNotContain("/Users/")
                .doesNotContain("FIXTURE_TRANSLATION_NEXT_")
                .doesNotContain("Exception");

        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages WHERE package_id = ?",
                        Integer.class,
                        "fixture-translation-chapter-12-mid-fail"))
                .isZero();
        assertThat(contentPackageRepository
                        .findActiveApproved("en", "FIXTURE_PROVIDER", "bhagavad-gita", CHAPTER)
                        .map(TranslationContentPackageRepository.ContentPackageRecord::packageId))
                .contains("fixture-translation-chapter-12-prior-ok");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_PRIOR_1");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports WHERE import_status = 'FAILED'",
                        Integer.class))
                .isEqualTo(1);

        ImportTranslationPackageResult retry =
                useCase.execute(ImportTranslationPackageCommand.of(next, false));
        assertThat(retry.succeeded()).isTrue();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM translation.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-translation-chapter-12-prior-ok"))
                .isEqualTo("SUPERSEDED");
    }

    @TestConfiguration
    static class FailingProbeConfig {
        @Bean
        @Primary
        ImportMutationProbe failingTranslationImportMutationProbe() {
            return (ResolvedTranslationPackage pkg, List<Translation> updated) -> {
                if (FAIL_NEXT.get() && !updated.isEmpty()) {
                    throw new IllegalStateException(
                            "forced mid-mutation failure for " + pkg.packageId()
                                    + " at /Users/example/secret/path with "
                                    + updated.getFirst().translationText().value());
                }
            };
        }
    }
}
