package com.antar.translation.application.imports;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import com.antar.translation.application.port.PackageFormatValidator;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.application.port.ResolvedTranslationPackage.CanonicalReferenceRange;
import com.antar.translation.application.port.ResolvedTranslationPackage.PackageTranslationRecord;
import com.antar.translation.application.port.TranslationContentPackageRepository;
import com.antar.translation.application.port.TranslationPackageReader;
import com.antar.translation.domain.ImportFailureCode;
import com.antar.translation.infrastructure.packageformat.FilesystemTranslationPackageReader;
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
 * Forces package-identity conflict: different packageId, identical packageChecksum.
 */
@SpringBootTest
@SkipInfrastructureTestsIfRequested
class SameChecksumDifferentPackageIdTranslationImportTest extends AbstractIntegrationTest {

    private static final int CHAPTER = 12;
    private static final int VERSE_COUNT = 20;

    @TempDir
    Path tempDir;

    @Autowired
    ImportTranslationPackageUseCase useCase;

    @Autowired
    TranslationContentPackageRepository contentPackageRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockitoBean
    PackageFormatValidator packageFormatValidator;

    @MockitoBean
    TranslationPackageReader translationPackageReader;

    private SyntheticTranslationPackageFixtureBuilder fixtures;

    @BeforeEach
    void setUp() {
        fixtures = new SyntheticTranslationPackageFixtureBuilder();
        resetTranslationState();
        when(packageFormatValidator.validate(any(), any()))
                .thenReturn(new PackageValidationResult(true, true, true, List.of(), List.of()));
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
    void rejectsDifferentPackageIdWithSameChecksumWithoutRewritingTranslations() throws Exception {
        Path firstDir = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-translation-chapter-12-same-checksum-a",
                CHAPTER,
                VERSE_COUNT,
                1,
                "FIXTURE_TRANSLATION_VERSE_");

        ResolvedTranslationPackage firstPkg = new FilesystemTranslationPackageReader().read(firstDir);
        when(translationPackageReader.read(any())).thenReturn(firstPkg);

        ImportTranslationPackageResult first =
                useCase.execute(ImportTranslationPackageCommand.of(firstDir, false));
        assertThat(first.succeeded()).isTrue();

        ResolvedTranslationPackage conflicting =
                withPackageIdAndVersion(firstPkg, "fixture-translation-chapter-12-same-checksum-b", 2);
        when(translationPackageReader.read(any())).thenReturn(conflicting);

        ImportTranslationPackageResult second =
                useCase.execute(ImportTranslationPackageCommand.of(firstDir, false));

        assertThat(second.failureCode()).isEqualTo(ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
        assertThat(contentPackageRepository.findByPackageId(
                        "fixture-translation-chapter-12-same-checksum-b"))
                .isEmpty();
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_packages", Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT COUNT(*) FROM translation.content_package_imports WHERE import_status = 'IMPORTED'",
                        Integer.class))
                .isEqualTo(1);
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT translation_text FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("FIXTURE_TRANSLATION_VERSE_1");
        assertThat(jdbcTemplate.queryForObject(
                        "SELECT t.source_package_id FROM translation.translations t "
                                + "JOIN scripture.verses v ON v.id = t.verse_id "
                                + "WHERE v.canonical_reference = '12.1'",
                        String.class))
                .isEqualTo("fixture-translation-chapter-12-same-checksum-a");
    }

    private static ResolvedTranslationPackage withPackageIdAndVersion(
            ResolvedTranslationPackage original, String newId, long contentVersion) {
        List<PackageTranslationRecord> translations = original.translations().stream()
                .map(t -> new PackageTranslationRecord(
                        t.canonicalReference(),
                        t.chapterNumber(),
                        t.verseNumber(),
                        t.translationText(),
                        contentVersion))
                .toList();
        return new ResolvedTranslationPackage(
                newId,
                original.packageFormatVersion(),
                original.scriptureId(),
                original.chapterNumber(),
                original.language(),
                original.provider(),
                original.sourceName(),
                original.licenseType(),
                original.licenseReference(),
                contentVersion,
                original.packageStatus(),
                original.packageChecksum(),
                original.manifestChecksum(),
                original.provenanceChecksum(),
                original.translationsChecksum(),
                original.sourceRegistryReferences(),
                original.recordCount(),
                new CanonicalReferenceRange(
                        original.canonicalReferenceRange().from(),
                        original.canonicalReferenceRange().to(),
                        original.canonicalReferenceRange().expectedCount()),
                translations);
    }
}
