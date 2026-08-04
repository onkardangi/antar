package com.antar.scripture.infrastructure.packageformat;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.PackageValidationResult;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * Fail-closed Java/Python Package Format v1 parity gate.
 *
 * <p>Requires {@code python3} and {@code content/packages/tools/validate_package.py}. Runtime
 * importer execution does not spawn Python.
 */
class PackageFormatV1PythonParityTest {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static Path sourcesRegistry;
    private static Path validatePackageScript;
    private static PythonPackageValidatorParityGate gate;

    @TempDir
    Path tempDir;

    private SyntheticPackageFixtureBuilder fixtures;

    @BeforeAll
    static void resolveTools() {
        Path moduleDir = Path.of("").toAbsolutePath().normalize();
        Path repoRoot = moduleDir.getFileName().toString().equals("backend")
                ? moduleDir.getParent()
                : moduleDir;
        validatePackageScript = repoRoot.resolve("content/packages/tools/validate_package.py");
        gate = new PythonPackageValidatorParityGate();
    }

    @BeforeEach
    void setUp() throws Exception {
        fixtures = new SyntheticPackageFixtureBuilder();
        sourcesRegistry = fixtures.writeSourcesRegistry(tempDir.resolve("sources.json"));
    }

    @Test
    void approvedChapterTwelveFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-approved", 12, 20, 1, "FIXTURE_NON_SCRIPTURAL_VERSE_");
        assertParity(pkg);
    }

    @Test
    void draftStatusFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeDraftChapterPackage(
                tempDir, "parity-draft", 12, 20, 1, "FIXTURE_NON_SCRIPTURAL_VERSE_");
        assertParity(pkg);
    }

    @Test
    void missingSanskritFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-missing-sanskrit", 12, 20, 1, "FIXTURE_NON_SCRIPTURAL_VERSE_");
        fixtures.omitSanskritForFirstVerse(pkg);
        assertParity(pkg);
    }

    @Test
    void badCanonicalReferenceFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-bad-ref", 12, 20, 1, "FIXTURE_NON_SCRIPTURAL_VERSE_");
        fixtures.badCanonicalReferenceForFirstVerse(pkg);
        assertParity(pkg);
    }

    @Test
    void wrongVerseCountFixtureMatchesPython() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir, "parity-wrong-count", 12, 20, 1, "FIXTURE_NON_SCRIPTURAL_VERSE_");
        fixtures.wrongRecordCountInManifest(pkg);
        assertParity(pkg);
    }

    @Test
    void missingPython3FailsClosed() {
        PythonPackageValidatorParityGate missingPython = new PythonPackageValidatorParityGate(
                MAPPER,
                (cmd, timeout, unit) -> {
                    throw new AssertionError("process should not launch when python3 is missing");
                },
                () -> false,
                5);

        assertThatThrownBy(() -> missingPython.validate(tempDir, sourcesRegistry, validatePackageScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("python3")
                .hasMessageNotContaining("/Users/")
                .hasMessageNotContaining("/home/");
    }

    @Test
    void missingValidatePackageScriptFailsClosed() {
        Path missingScript = tempDir.resolve("missing-validate_package.py");
        assertThatThrownBy(() -> gate.validate(tempDir, sourcesRegistry, missingScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("validate_package.py")
                .hasMessageNotContaining("/Users/")
                .hasMessageNotContaining("/home/");
    }

    @Test
    void timeoutFailsClosed() throws Exception {
        PythonPackageValidatorParityGate timingOut = new PythonPackageValidatorParityGate(
                MAPPER,
                (cmd, timeout, unit) -> new PythonPackageValidatorParityGate.ProcessResult(false, -1, ""),
                () -> true,
                1);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> timingOut.validate(tempDir, sourcesRegistry, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("timed out")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void unexpectedExitCodeFailsClosed() throws Exception {
        PythonPackageValidatorParityGate badExit = new PythonPackageValidatorParityGate(
                MAPPER,
                (cmd, timeout, unit) ->
                        new PythonPackageValidatorParityGate.ProcessResult(true, 2, "{\"unexpected\":true}"),
                () -> true,
                5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> badExit.validate(tempDir, sourcesRegistry, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("unexpected code")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void malformedJsonFailsClosed() throws Exception {
        PythonPackageValidatorParityGate malformed = new PythonPackageValidatorParityGate(
                MAPPER,
                (cmd, timeout, unit) ->
                        new PythonPackageValidatorParityGate.ProcessResult(true, 0, "not-json"),
                () -> true,
                5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> malformed.validate(tempDir, sourcesRegistry, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("malformed JSON")
                .hasMessageNotContaining("/Users/");
    }

    @Test
    void emptyOutputFailsClosed() throws Exception {
        PythonPackageValidatorParityGate empty = new PythonPackageValidatorParityGate(
                MAPPER,
                (cmd, timeout, unit) ->
                        new PythonPackageValidatorParityGate.ProcessResult(true, 0, "   "),
                () -> true,
                5);

        Path fakeScript = tempDir.resolve("validate_package.py");
        Files.writeString(fakeScript, "# fake");

        assertThatThrownBy(() -> empty.validate(tempDir, sourcesRegistry, fakeScript))
                .isInstanceOf(AssertionError.class)
                .hasMessageContaining("empty output");
    }

    private void assertParity(Path pkg) throws Exception {
        PackageFormatV1Validator javaValidator = new PackageFormatV1Validator(MAPPER, "", "");
        PackageValidationResult javaResult =
                javaValidator.validate(pkg, PackageValidationOptions.defaults().withSourcesRegistry(sourcesRegistry));
        JsonNode python = gate.validate(pkg, sourcesRegistry, validatePackageScript);

        assertThat(javaResult.structurallyValid()).isEqualTo(python.path("structurallyValid").asBoolean());
        assertThat(javaResult.editoriallyValid()).isEqualTo(python.path("editoriallyValid").asBoolean());
        assertThat(javaResult.mayProceedToImport()).isEqualTo(python.path("importable").asBoolean());
        assertThat(javaResult.warnings()).hasSize(python.path("warnings").size());
    }
}
