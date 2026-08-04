package com.antar.scripture.infrastructure.packageformat;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class PackageFormatV1ValidatorTest {

    @TempDir
    Path tempDir;

    private PackageFormatV1Validator validator;
    private SyntheticPackageFixtureBuilder fixtures;
    private Path sourcesRegistry;

    @BeforeEach
    void setUp() throws Exception {
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
        validator = new PackageFormatV1Validator(new ObjectMapper(), "", "");
    }

    @Test
    void approvedFullChapterIsImportableWithoutWarnings() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-v1",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        PackageValidationResult result = validator.validate(pkg, options());
        assertThat(result.structurallyValid()).isTrue();
        assertThat(result.editoriallyValid()).isTrue();
        assertThat(result.importable()).isTrue();
        assertThat(result.warnings()).isEmpty();
        assertThat(result.mayProceedToImport()).isTrue();
    }

    @Test
    void draftIsNeverImportable() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir,
                "fixture-chapter-12-draft",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        PackageValidationResult result = validator.validate(pkg, options());
        assertThat(result.importable()).isFalse();
        assertThat(result.mayProceedToImport()).isFalse();
        assertThat(result.warnings()).anyMatch(w -> w.contains("DRAFT"));
    }

    @Test
    void checksumMismatchFailsClosed() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-bad-sum",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        fixtures.corruptChecksums(pkg);
        PackageValidationResult result = validator.validate(pkg, options());
        assertThat(result.structurallyValid()).isFalse();
        assertThat(result.importable()).isFalse();
        assertThat(result.errors()).anyMatch(e -> e.contains("checksum mismatch"));
    }

    @Test
    void invalidPathErrorsDoNotIncludeAbsoluteFilesystemPaths() {
        PackageValidationResult result =
                validator.validate(tempDir.resolve("does-not-exist"), options());
        assertThat(result.errors())
                .containsExactly("package directory does not exist")
                .allSatisfy(err -> assertThat(err)
                        .doesNotContain("/Users/")
                        .doesNotContain("/home/")
                        .doesNotContain("file://")
                        .doesNotContain("C:\\")
                        .doesNotContain(tempDir.toAbsolutePath().normalize().toString()));
    }

    @Test
    void parseFailuresUseStablePathFreeMessages() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-corrupt-json",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        Files.writeString(pkg.resolve("manifest.json"), "{not-json");
        PackageValidationResult result = validator.validate(pkg, options());
        assertThat(result.structurallyValid()).isFalse();
        assertThat(result.errors())
                .contains("failed to parse package files")
                .allSatisfy(err -> assertThat(err)
                        .doesNotContain("/Users/")
                        .doesNotContain("/home/")
                        .doesNotContain(pkg.toAbsolutePath().toString())
                        .doesNotContain("FIXTURE_NON_SCRIPTURAL"));
    }

    @Test
    void sourceRegistryLoadFailuresUseStablePathFreeMessages() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-bad-registry",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        Path missingRegistry = tempDir.resolve("missing-sources.json").toAbsolutePath();
        PackageValidationResult result = validator.validate(
                pkg, PackageValidationOptions.defaults().withSourcesRegistry(missingRegistry));
        assertThat(result.errors())
                .anyMatch(e -> e.equals("failed to load source registry"))
                .allSatisfy(err -> assertThat(err)
                        .doesNotContain("/Users/")
                        .doesNotContain(missingRegistry.toString())
                        .doesNotContain("FIXTURE_NON_SCRIPTURAL"));
    }

    @Test
    void committedDraftExampleIsNotImportable() {
        Path example = resolveExamplePackage();
        assertThat(Files.isDirectory(example))
                .as("committed package example must exist")
                .isTrue();
        Path registry = resolveRepoFile("content/registry/sources.json");
        PackageValidationResult result = validator.validate(
                example, PackageValidationOptions.defaults().withSourcesRegistry(registry));
        assertThat(result.importable()).isFalse();
        assertThat(result.mayProceedToImport()).isFalse();
    }

    private PackageValidationOptions options() {
        return PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry);
    }

    private static Path resolveExamplePackage() {
        return resolveRepoFile("content/packages/examples/bhagavad-gita-chapter-01-v1-example");
    }

    private static Path resolveRepoFile(String relative) {
        Path cwd = Path.of("").toAbsolutePath().normalize();
        Path direct = cwd.resolve(relative);
        if (Files.exists(direct)) {
            return direct;
        }
        return cwd.resolve("..").resolve(relative).normalize();
    }
}
