package com.antar.scripture.application.imports;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.antar.scripture.application.port.ContentPackageRepository;
import com.antar.scripture.application.port.PackageFormatValidator;
import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.application.port.ResolvedScripturePackage;
import com.antar.scripture.application.port.ResolvedScripturePackage.CanonicalReferenceRange;
import com.antar.scripture.application.port.ResolvedScripturePackage.PackageProvenance;
import com.antar.scripture.application.port.ResolvedScripturePackage.PackageVerseRecord;
import com.antar.scripture.application.port.ScripturePackageReader;
import com.antar.scripture.domain.ImportFailureCode;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

/**
 * Forces package-identity conflict: different packageId, identical packageChecksum.
 */
@SpringBootTest
@SkipInfrastructureTestsIfRequested
class SameChecksumDifferentPackageIdImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportScripturePackageUseCase useCase;

    @Autowired
    ContentPackageRepository contentPackageRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockitoBean
    PackageFormatValidator packageFormatValidator;

    @MockitoBean
    ScripturePackageReader scripturePackageReader;

    private SyntheticPackageFixtureBuilder fixtures;
    private Path sourcesRegistry;

    @BeforeEach
    void setUp() throws Exception {
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
        resetChapter12();

        when(packageFormatValidator.validate(any(), any()))
                .thenReturn(new PackageValidationResult(true, true, true, List.of(), List.of()));
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
    void rejectsDifferentPackageIdWithSameChecksumWithoutRewritingVerses() throws Exception {
        Path firstDir = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-same-checksum-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");

        ResolvedScripturePackage firstPkg = new com.antar.scripture.infrastructure.packageformat
                .FilesystemScripturePackageReader()
                .read(firstDir);
        when(scripturePackageReader.read(any())).thenReturn(firstPkg);

        ImportScripturePackageResult first = useCase.execute(new ImportScripturePackageCommand(
                firstDir, false, PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry)));
        assertThat(first.succeeded()).isTrue();

        ResolvedScripturePackage conflicting =
                withPackageIdAndVersion(firstPkg, "fixture-chapter-12-same-checksum-b", 2);
        when(scripturePackageReader.read(any())).thenReturn(conflicting);

        ImportScripturePackageResult second = useCase.execute(new ImportScripturePackageCommand(
                firstDir, false, PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry)));

        assertThat(second.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
        assertThat(contentPackageRepository.findByPackageId("fixture-chapter-12-same-checksum-b")).isEmpty();
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
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT source_package_id FROM scripture.verses WHERE canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("fixture-chapter-12-same-checksum-a");
    }

    private static ResolvedScripturePackage withPackageIdAndVersion(
            ResolvedScripturePackage original, String newId, long contentVersion) {
        List<PackageVerseRecord> verses = original.verses().stream()
                .map(v -> new PackageVerseRecord(
                        v.chapterNumber(),
                        v.verseNumber(),
                        v.canonicalReference(),
                        v.sanskritText(),
                        v.transliteration(),
                        contentVersion,
                        v.sourceIds(),
                        v.sourceChecksums(),
                        v.editorialDecisionId(),
                        v.editorialApprovalChecksum()))
                .toList();
        PackageProvenance provenance = new PackageProvenance(
                newId,
                original.provenance().sourceIds(),
                original.provenance().sourceRoles(),
                original.provenance().sourceChecksums(),
                original.provenance().editorialReviewerIds(),
                original.provenance().secondReviewerIds(),
                original.provenance().approvalDates());
        return new ResolvedScripturePackage(
                newId,
                original.scriptureId(),
                original.chapterNumber(),
                contentVersion,
                original.recordCount(),
                original.packageStatus(),
                original.packageFormatVersion(),
                original.packageChecksum(),
                original.manifestChecksum(),
                original.provenanceChecksum(),
                original.versesChecksum(),
                original.sourceRegistryReferences(),
                original.editorialApprovalManifestChecksum(),
                original.allowNullTransliteration(),
                new CanonicalReferenceRange(
                        original.canonicalReferenceRange().from(),
                        original.canonicalReferenceRange().to(),
                        original.canonicalReferenceRange().expectedCount()),
                verses,
                provenance);
    }
}
