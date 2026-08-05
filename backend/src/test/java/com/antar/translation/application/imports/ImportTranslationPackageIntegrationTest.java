package com.antar.translation.application.imports;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import com.antar.translation.domain.ImportExecutionStatus;
import com.antar.translation.domain.ImportFailureCode;
import com.antar.translation.support.SyntheticTranslationPackageFixtureBuilder;
import java.nio.file.Path;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class ImportTranslationPackageIntegrationTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportTranslationPackageUseCase useCase;

    @Autowired
    JdbcTemplate jdbcTemplate;

    private SyntheticTranslationPackageFixtureBuilder fixtures;

    @BeforeEach
    void setUp() {
        fixtures = new SyntheticTranslationPackageFixtureBuilder();
        resetTranslationState();
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
    void importsApprovedSyntheticPackage() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-v1",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ImportTranslationPackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.succeeded()).isTrue();
        assertThat(result.recordsUpdated()).isEqualTo(VERSE_COUNT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.translations WHERE source_package_id = ?",
                        Integer.class,
                        "fixture-translation-chapter-12-v1"))
                .isEqualTo(VERSE_COUNT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_VERSE_1");
        assertThat(tableExists("scripture.translations")).isFalse();
    }

    @Test
    void importsCheckedInSyntheticFixturePackage() {
        Path pkg = Path.of("")
                .toAbsolutePath()
                .getParent()
                .resolve("content/packages/translation/fixtures/fixture-translation-en-chapter-01-v1");
        if (!pkg.toFile().isDirectory()) {
            pkg = Path.of("content/packages/translation/fixtures/fixture-translation-en-chapter-01-v1")
                    .toAbsolutePath()
                    .normalize();
        }

        ImportTranslationPackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.succeeded()).isTrue();
        assertThat(result.recordsUpdated()).isEqualTo(2);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '1.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_VERSE_1");
    }

    @Test
    void rejectsDraftPackageAndPersistsNothing() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-draft",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ImportTranslationPackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_NOT_IMPORTABLE);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isZero();
    }

    @Test
    void rejectsChecksumMismatch() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-bad-sum",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");
        fixtures.corruptChecksums(pkg);

        ImportTranslationPackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_VALIDATION_FAILED);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isZero();
    }

    @Test
    void dryRunWritesNothing() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-dry",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ImportTranslationPackageResult result = useCase.execute(command(pkg, true));

        assertThat(result.succeeded()).isTrue();
        assertThat(result.dryRun()).isTrue();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports", Integer.class))
                .isZero();
    }

    @Test
    void secondImportIsIdempotent() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-idem",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        assertThat(useCase.execute(command(pkg, false)).succeeded()).isTrue();
        ImportTranslationPackageResult second = useCase.execute(command(pkg, false));

        assertThat(second.succeeded()).isTrue();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
    }

    @Test
    void higherContentVersionSupersedesPriorPackage() throws Exception {
        Path v1 = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-v1-sup",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");
        assertThat(useCase.execute(command(v1, false)).succeeded()).isTrue();

        Path v2 = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-v2-sup",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_TRANSLATION_VERSE_V2_");
        assertThat(useCase.execute(command(v2, false)).succeeded()).isTrue();

        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM translation.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-translation-chapter-12-v1-sup"))
                .isEqualTo("SUPERSEDED");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM translation.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-translation-chapter-12-v2-sup"))
                .isEqualTo("APPROVED");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_VERSE_V2_1");
    }

    @Test
    void lowerContentVersionRejected() throws Exception {
        Path v2 = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-v2",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_TRANSLATION_V2_");
        assertThat(useCase.execute(command(v2, false)).succeeded()).isTrue();

        Path v1 = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("lower"),
                "fixture-translation-chapter-12-v1-lower",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_V1_");
        ImportTranslationPackageResult result = useCase.execute(command(v1, false));

        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.CONTENT_VERSION_DOWNGRADE);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_V2_1");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages WHERE package_id = ?",
                        Integer.class,
                        "fixture-translation-chapter-12-v1-lower"))
                .isZero();
    }

    @Test
    void sameVersionDifferentContentRejected() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-samever-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_A_");
        assertThat(useCase.execute(command(first, false)).succeeded()).isTrue();

        Path second = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("samever"),
                "fixture-translation-chapter-12-samever-b",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_B_");
        ImportTranslationPackageResult result = useCase.execute(command(second, false));

        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.CONTENT_VERSION_CONFLICT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_A_1");
    }

    @Test
    void samePackageIdDifferentChecksumRejected() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-conflict",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");
        assertThat(useCase.execute(command(first, false)).succeeded()).isTrue();

        Path second = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("alt"),
                "fixture-translation-chapter-12-conflict",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_ALT_");
        ImportTranslationPackageResult result = useCase.execute(command(second, false));

        assertThat(result.failureCode())
                .isIn(
                        ImportFailureCode.CONTENT_VERSION_CONFLICT,
                        ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_VERSE_1");
    }

    @Test
    void missingAbsolutePackagePathFailureIsPathSafe() {
        Path missing = tempDir.resolve("missing-abs-pkg").toAbsolutePath().normalize();
        ImportTranslationPackageResult result = useCase.execute(command(missing, true));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.INVALID_PACKAGE_PATH);
        assertThat(result.dryRun()).isTrue();
        assertPathSafe(result.failureMessage());
        assertThat(result.failureMessage()).doesNotContain(missing.toString());
        assertZeroImportWrites();
    }

    @Test
    void validationFailureMessagesRemainPathSafeForUnreadableAbsolutePaths() {
        Path absMissing = Path.of("/Users/example/secret/package-does-not-exist");
        ImportTranslationPackageResult result = useCase.execute(command(absMissing, false));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertPathSafe(result.failureMessage());
        assertThat(result.failureMessage())
                .doesNotContain("/Users/example")
                .doesNotContain("secret");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports", Integer.class))
                .isZero();
    }

    private ImportTranslationPackageCommand command(Path pkg, boolean dryRun) {
        return ImportTranslationPackageCommand.of(pkg, dryRun);
    }

    private void assertZeroImportWrites() {
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.translations", Integer.class))
                .isZero();
    }

    private static void assertPathSafe(String message) {
        assertThat(message).isNotBlank();
        assertThat(message)
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("FIXTURE_TRANSLATION");
    }

    private boolean tableExists(String qualifiedName) {
        String[] parts = qualifiedName.split("\\.");
        Integer count = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?",
                Integer.class,
                parts[0],
                parts[1]);
        return count != null && count > 0;
    }
}
