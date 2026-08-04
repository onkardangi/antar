package com.antar.scripture.application.imports;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.domain.ImportExecutionStatus;
import com.antar.scripture.domain.ImportFailureCode;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class ImportScripturePackageIntegrationTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportScripturePackageUseCase useCase;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Autowired
    ApplicationContext applicationContext;

    private SyntheticPackageFixtureBuilder fixtures;
    private Path sourcesRegistry;

    @BeforeEach
    void setUp() throws Exception {
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
        resetChapter12();
    }

    @org.junit.jupiter.api.AfterEach
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
    void importsApprovedSyntheticPackage() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-v1",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");

        ImportScripturePackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.succeeded()).isTrue();
        assertThat(result.recordsUpdated()).isEqualTo(VERSE_COUNT);
        assertThat(result.recordsUnchanged()).isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.verses WHERE source_package_id = ?",
                        Integer.class,
                        "fixture-chapter-12-v1"))
                .isEqualTo(VERSE_COUNT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT sanskrit_text FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_NON_SCRIPTURAL_VERSE_1");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages WHERE package_id = ?",
                        Integer.class,
                        "fixture-chapter-12-v1"))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
        assertThat(tableExists("scripture.translations")).isFalse();
        assertThat(tableExists("scripture.commentaries")).isFalse();
    }

    @Test
    void rejectsDraftPackageAndPersistsNothing() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir,
                "fixture-chapter-12-draft",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");

        ImportScripturePackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_NOT_IMPORTABLE);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.verses WHERE sanskrit_text IS NOT NULL AND canonical_reference LIKE '12.%'",
                        Integer.class))
                .isZero();
    }

    @Test
    void rejectsChecksumMismatch() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-bad-sum",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        fixtures.corruptChecksums(pkg);

        ImportScripturePackageResult result = useCase.execute(command(pkg, false));

        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_VALIDATION_FAILED);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isZero();
    }

    @Test
    void dryRunWritesNothing() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-dry",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");

        ImportScripturePackageResult result = useCase.execute(command(pkg, true));

        assertThat(result.dryRun()).isTrue();
        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.IMPORTED);
        assertThat(result.recordsUpdated()).isEqualTo(VERSE_COUNT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports", Integer.class))
                .isZero();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.verses WHERE sanskrit_text IS NOT NULL AND canonical_reference LIKE '12.%'",
                        Integer.class))
                .isZero();
    }

    @Test
    void repeatedImportIsIdempotent() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-idem",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");

        ImportScripturePackageResult first = useCase.execute(command(pkg, false));
        ImportScripturePackageResult second = useCase.execute(command(pkg, false));

        assertThat(first.succeeded()).isTrue();
        assertThat(second.succeeded()).isTrue();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
    }

    @Test
    void samePackageIdDifferentChecksumRejected() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-conflict",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        assertThat(useCase.execute(command(first, false)).succeeded()).isTrue();

        Path secondParent = tempDir.resolve("alt");
        Files.createDirectories(secondParent);
        Path second = fixtures.writeApprovedChapterPackage(
                secondParent,
                "fixture-chapter-12-conflict",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_ALT_");

        ImportScripturePackageResult result = useCase.execute(command(second, false));
        // Same contentVersion with different package checksum/text is rejected before mutation.
        assertThat(result.failureCode())
                .isIn(
                        ImportFailureCode.CONTENT_VERSION_CONFLICT,
                        ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT sanskrit_text FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_NON_SCRIPTURAL_VERSE_1");
    }

    @Test
    void lowerContentVersionRejected() throws Exception {
        Path v2 = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-v2",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_NON_SCRIPTURAL_V2_");
        assertThat(useCase.execute(command(v2, false)).succeeded()).isTrue();

        Path v1 = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("lower"),
                "fixture-chapter-12-v1-lower",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_V1_");
        ImportScripturePackageResult result = useCase.execute(command(v1, false));
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.CONTENT_VERSION_DOWNGRADE);
    }

    @Test
    void sameVersionDifferentContentRejected() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-samever-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_A_");
        assertThat(useCase.execute(command(first, false)).succeeded()).isTrue();

        Path second = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("samever"),
                "fixture-chapter-12-samever-b",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_B_");
        ImportScripturePackageResult result = useCase.execute(command(second, false));
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.CONTENT_VERSION_CONFLICT);
    }

    @Test
    void higherVersionSupersedesAtomically() throws Exception {
        Path v1 = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-super-v1",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_V1_");
        assertThat(useCase.execute(command(v1, false)).succeeded()).isTrue();

        Path v2 = fixtures.writeApprovedChapterPackage(
                tempDir.resolve("super"),
                "fixture-chapter-12-super-v2",
                CHAPTER,
                VERSE_COUNT,
                2,
                "FIXTURE_NON_SCRIPTURAL_V2_");
        ImportScripturePackageResult result = useCase.execute(command(v2, false));

        assertThat(result.succeeded()).isTrue();
        assertThat(result.recordsUpdated()).isEqualTo(VERSE_COUNT);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT package_status FROM scripture.content_packages WHERE package_id = ?",
                        String.class,
                        "fixture-chapter-12-super-v1"))
                .isEqualTo("SUPERSEDED");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT source_package_id FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("fixture-chapter-12-super-v2");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT content_version FROM scripture.verses WHERE canonical_reference = '12.1'",
                        Long.class))
                .isEqualTo(2L);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT sanskrit_text FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_NON_SCRIPTURAL_V2_1");
    }

    @Test
    void rejectsNonNullTransliteration() throws Exception {
        Path pkg = fixtures.writeApprovedWithTransliteration(
                tempDir, "fixture-chapter-12-tl", CHAPTER, VERSE_COUNT, 1);
        ImportScripturePackageResult result = useCase.execute(command(pkg, false));
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.UNSUPPORTED_CONTENT_LAYER);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isZero();
    }

    @Test
    void dryRunTransliterationRejectionReportsDryRunAndWritesNothing() throws Exception {
        Path pkg = fixtures.writeApprovedWithTransliteration(
                tempDir, "fixture-chapter-12-tl-dry", CHAPTER, VERSE_COUNT, 1);
        ImportScripturePackageResult result = useCase.execute(command(pkg, true));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.UNSUPPORTED_CONTENT_LAYER);
        assertThat(result.dryRun()).isTrue();
        assertZeroImportWrites();
        assertPathSafe(result.failureMessage());
    }

    @Test
    void dryRunPlanningFailureReportsDryRunAndWritesNothing() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-planning-dry",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        jdbcTemplate.update(
                "UPDATE scripture.chapters SET publication_status = 'RETIRED' WHERE chapter_number = ?",
                CHAPTER);
        try {
            ImportScripturePackageResult result = useCase.execute(command(pkg, true));

            assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
            assertThat(result.failureCode()).isEqualTo(ImportFailureCode.CHAPTER_NOT_FOUND);
            assertThat(result.dryRun()).isTrue();
            assertZeroImportWrites();
            assertPathSafe(result.failureMessage());
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.chapters SET publication_status = 'PUBLISHED' WHERE chapter_number = ?",
                    CHAPTER);
        }
    }

    @Test
    void dryRunValidationFailureReportsDryRunAndWritesNothing() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir,
                "fixture-chapter-12-draft-dry",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        ImportScripturePackageResult result = useCase.execute(command(pkg, true));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_NOT_IMPORTABLE);
        assertThat(result.dryRun()).isTrue();
        assertZeroImportWrites();
        assertPathSafe(result.failureMessage());
    }

    @Test
    void missingAbsolutePackagePathFailureIsPathSafe() {
        Path missing = tempDir.resolve("missing-abs-pkg").toAbsolutePath().normalize();
        ImportScripturePackageResult result = useCase.execute(command(missing, true));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertThat(result.failureCode()).isEqualTo(ImportFailureCode.INVALID_PACKAGE_PATH);
        assertThat(result.dryRun()).isTrue();
        assertPathSafe(result.failureMessage());
        assertThat(result.failureMessage()).doesNotContain(missing.toString());
        assertZeroImportWrites();
    }

    @Test
    void validationFailureMessagesRemainPathSafeForUnreadableAbsolutePaths() throws Exception {
        Path absMissing = Path.of("/Users/example/secret/package-does-not-exist");
        ImportScripturePackageResult result = useCase.execute(command(absMissing, false));

        assertThat(result.importStatus()).isEqualTo(ImportExecutionStatus.FAILED);
        assertPathSafe(result.failureMessage());
        assertThat(result.failureMessage())
                .doesNotContain("/Users/example")
                .doesNotContain("secret");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports", Integer.class))
                .isZero();
    }

    private void assertZeroImportWrites() {
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

    private static void assertPathSafe(String message) {
        assertThat(message).isNotBlank();
        assertThat(message)
                .doesNotContain("/Users/")
                .doesNotContain("/home/")
                .doesNotContain("file://")
                .doesNotContain("C:\\")
                .doesNotContain("FIXTURE_NON_SCRIPTURAL");
    }

    @Test
    void noPublicImportApiBeansExist() {
        String[] controllers = applicationContext.getBeanNamesForAnnotation(
                org.springframework.web.bind.annotation.RestController.class);
        for (String name : controllers) {
            Object bean = applicationContext.getBean(name);
            String className = bean.getClass().getName();
            if (className.startsWith("com.antar.scripture.api.")) {
                assertThat(className.toLowerCase())
                        .as("Scripture API RestController must not expose import/ingest")
                        .doesNotContain("import")
                        .doesNotContain("ingest")
                        .doesNotContain("packageload");
            }
        }
    }

    @Test
    void sameChecksumDifferentPackageIdRejectedByDatabaseAndApplication() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-checksum-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        ImportScripturePackageResult imported = useCase.execute(command(first, false));
        assertThat(imported.succeeded()).isTrue();
        String checksum = imported.packageChecksum();

        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.content_packages (
                            package_id, package_format_version, scripture_id, chapter_number,
                            content_version, package_status, package_checksum, manifest_checksum,
                            provenance_checksum, verses_checksum, source_registry_references,
                            importer_version, first_imported_at, last_verified_at, created_at, updated_at
                        ) VALUES (
                            'fixture-chapter-12-checksum-b', 1, 'bhagavad-gita', 12, 1, 'APPROVED',
                            ?, ?, ?, ?, '["fixture-antar-importer-v1"]'::jsonb,
                            1, NOW(), NOW(), NOW(), NOW()
                        )
                        """,
                        checksum,
                        checksum,
                        checksum,
                        checksum))
                .hasMessageContaining("uq_scripture_content_packages_checksum");

        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_packages", Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM scripture.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT sanskrit_text FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_NON_SCRIPTURAL_VERSE_1");
    }

    @Test
    void activeApprovedPackageUniquePerChapterIsEnforced() throws Exception {
        Path first = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-active-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_A_");
        assertThat(useCase.execute(command(first, false)).succeeded()).isTrue();

        String otherChecksum = "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd";
        assertThatThrownBy(() -> jdbcTemplate.update(
                        """
                        INSERT INTO scripture.content_packages (
                            package_id, package_format_version, scripture_id, chapter_number,
                            content_version, package_status, package_checksum, manifest_checksum,
                            provenance_checksum, verses_checksum, source_registry_references,
                            importer_version, first_imported_at, last_verified_at, created_at, updated_at
                        ) VALUES (
                            'fixture-chapter-12-active-b', 1, 'bhagavad-gita', 12, 2, 'APPROVED',
                            ?, ?, ?, ?, '["fixture-antar-importer-v1"]'::jsonb,
                            1, NOW(), NOW(), NOW(), NOW()
                        )
                        """,
                        otherChecksum,
                        otherChecksum,
                        otherChecksum,
                        otherChecksum))
                .hasMessageContaining("uq_scripture_content_packages_one_active_approved");
    }

    private ImportScripturePackageCommand command(Path pkg, boolean dryRun) {
        return new ImportScripturePackageCommand(
                pkg, dryRun, PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry));
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
