package com.antar.translation.infrastructure.packageformat;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.translation.application.port.PackageValidationOptions;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.support.SyntheticTranslationPackageFixtureBuilder;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class TranslationPackageFormatV1ValidatorTest {

    @TempDir
    Path tempDir;

    private final TranslationPackageFormatV1Validator validator = new TranslationPackageFormatV1Validator();
    private final SyntheticTranslationPackageFixtureBuilder fixtures =
            new SyntheticTranslationPackageFixtureBuilder();

    @Test
    void acceptsApprovedSyntheticPackage() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "fixture-translation-valid", 12, 3, 1, "FIXTURE_TRANSLATION_VERSE_");

        PackageValidationResult result = validator.validate(pkg, PackageValidationOptions.defaults());

        assertThat(result.structurallyValid()).isTrue();
        assertThat(result.editoriallyValid()).isTrue();
        assertThat(result.importable()).isTrue();
        assertThat(result.errors()).isEmpty();
    }

    @Test
    void draftIsNotImportable() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir, "fixture-translation-draft", 12, 3, 1, "FIXTURE_TRANSLATION_VERSE_");

        PackageValidationResult result = validator.validate(pkg, PackageValidationOptions.defaults());

        assertThat(result.structurallyValid()).isTrue();
        assertThat(result.importable()).isFalse();
        assertThat(result.warnings()).anyMatch(w -> w.contains("DRAFT"));
    }

    @Test
    void rejectsChecksumCorruption() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "fixture-translation-bad-sum", 12, 3, 1, "FIXTURE_TRANSLATION_VERSE_");
        fixtures.corruptChecksums(pkg);

        PackageValidationResult result = validator.validate(pkg, PackageValidationOptions.defaults());

        assertThat(result.structurallyValid()).isFalse();
        assertThat(result.importable()).isFalse();
        assertThat(result.errors()).isNotEmpty();
    }
}
