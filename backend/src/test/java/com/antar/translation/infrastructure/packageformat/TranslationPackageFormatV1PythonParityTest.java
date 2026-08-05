package com.antar.translation.infrastructure.packageformat;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.translation.application.port.PackageValidationOptions;
import com.antar.translation.application.port.PackageValidationResult;
import com.antar.translation.support.SyntheticTranslationPackageFixtureBuilder;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * Fail-closed Java/Python Translation Package Format v1 parity gate.
 *
 * <p>Requires {@code python3} and {@code content/packages/translation/tools/validate_package.py}.
 * Runtime importer execution does not spawn Python.
 */
class TranslationPackageFormatV1PythonParityTest {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static Path validatePackageScript;
    private static TranslationPythonPackageValidatorParityGate gate;

    @TempDir
    Path tempDir;

    private SyntheticTranslationPackageFixtureBuilder fixtures;

    @BeforeAll
    static void resolveTools() {
        Path moduleDir = Path.of("").toAbsolutePath().normalize();
        Path repoRoot = moduleDir.getFileName().toString().equals("backend")
                ? moduleDir.getParent()
                : moduleDir;
        validatePackageScript =
                repoRoot.resolve("content/packages/translation/tools/validate_package.py");
        gate = new TranslationPythonPackageValidatorParityGate();
    }

    @BeforeEach
    void setUp() {
        fixtures = new SyntheticTranslationPackageFixtureBuilder();
    }

    @Test
    void approvedChapterTwelveFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-translation-approved", 12, 20, 1, "FIXTURE_TRANSLATION_VERSE_");
        assertParity(pkg);
    }

    @Test
    void draftStatusFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir, "parity-translation-draft", 12, 20, 1, "FIXTURE_TRANSLATION_VERSE_");
        assertParity(pkg);
    }

    @Test
    void blankTranslationTextFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-translation-blank", 12, 20, 1, "FIXTURE_TRANSLATION_VERSE_");
        fixtures.blankTranslationTextForFirstVerse(pkg);
        assertParity(pkg);
    }

    @Test
    void badCanonicalReferenceFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-translation-bad-ref", 12, 20, 1, "FIXTURE_TRANSLATION_VERSE_");
        fixtures.badCanonicalReferenceForFirstVerse(pkg);
        assertParity(pkg);
    }

    @Test
    void wrongVerseCountFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-translation-wrong-count", 12, 20, 1, "FIXTURE_TRANSLATION_VERSE_");
        fixtures.wrongRecordCountInManifest(pkg);
        assertParity(pkg);
    }

    @Test
    void missingPython3FailsClosed() {
        TranslationPythonPackageValidatorParityGate missingPython =
                new TranslationPythonPackageValidatorParityGate(
                        MAPPER,
                        (cmd, timeout, unit) -> {
                            throw new AssertionError("process should not launch when python3 is missing");
                        },
                        () -> false,
                        5);

        assertThatThrownBy(() -> missingPython.validate(tempDir, validatePackageScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("python3")
                .hasMessageNotContaining("/Users/")
                .hasMessageNotContaining("/home/");
    }

    @Test
    void missingValidatePackageScriptFailsClosed() {
        Path missingScript = tempDir.resolve("missing-validate_package.py");
        assertThatThrownBy(() -> gate.validate(tempDir, missingScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("validate_package.py")
                .hasMessageNotContaining("/Users/")
                .hasMessageNotContaining("/home/");
    }

    @Test
    void timeoutFailsClosed() throws Exception {
        TranslationPythonPackageValidatorParityGate timingOut =
                new TranslationPythonPackageValidatorParityGate(
                        MAPPER,
                        (cmd, timeout, unit) ->
                                new TranslationPythonPackageValidatorParityGate.ProcessResult(false, -1, ""),
                        () -> true,
                        1);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> timingOut.validate(tempDir, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("timed out")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void unexpectedExitCodeFailsClosed() throws Exception {
        TranslationPythonPackageValidatorParityGate badExit =
                new TranslationPythonPackageValidatorParityGate(
                        MAPPER,
                        (cmd, timeout, unit) ->
                                new TranslationPythonPackageValidatorParityGate.ProcessResult(
                                        true, 2, "{\"unexpected\":true}"),
                        () -> true,
                        5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> badExit.validate(tempDir, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("unexpected code")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void malformedJsonFailsClosed() throws Exception {
        TranslationPythonPackageValidatorParityGate malformed =
                new TranslationPythonPackageValidatorParityGate(
                        MAPPER,
                        (cmd, timeout, unit) ->
                                new TranslationPythonPackageValidatorParityGate.ProcessResult(true, 0, "not-json"),
                        () -> true,
                        5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> malformed.validate(tempDir, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("malformed JSON")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void emptyOutputFailsClosed() throws Exception {
        TranslationPythonPackageValidatorParityGate empty =
                new TranslationPythonPackageValidatorParityGate(
                        MAPPER,
                        (cmd, timeout, unit) ->
                                new TranslationPythonPackageValidatorParityGate.ProcessResult(true, 0, "   "),
                        () -> true,
                        5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> empty.validate(tempDir, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("empty output");
    }

    private void assertParity(Path pkg) throws Exception {
        TranslationPackageFormatV1Validator javaValidator = new TranslationPackageFormatV1Validator(MAPPER);
        PackageValidationResult javaResult =
                javaValidator.validate(pkg, PackageValidationOptions.defaults());
        JsonNode python = gate.validate(pkg, validatePackageScript);

        assertThat(javaResult.structurallyValid()).isEqualTo(python.path("structurallyValid").asBoolean());
        assertThat(javaResult.editoriallyValid()).isEqualTo(python.path("editoriallyValid").asBoolean());
        assertThat(javaResult.importable()).isEqualTo(python.path("importable").asBoolean());
        assertThat(javaResult.mayProceedToImport())
                .isEqualTo(python.path("importable").asBoolean() && python.path("warnings").isEmpty());
        assertThat(javaResult.warnings()).hasSize(python.path("warnings").size());
    }
}
