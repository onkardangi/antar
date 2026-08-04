package com.antar.scripture.infrastructure.packageformat;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.antar.scripture.application.port.ScripturePackageReadException;
import com.antar.scripture.support.SyntheticPackageFixtureBuilder;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class FilesystemScripturePackageReaderTest {

    @TempDir
    Path tempDir;

    private SyntheticPackageFixtureBuilder fixtures;
    private FilesystemScripturePackageReader reader;

    @BeforeEach
    void setUp() {
        fixtures = new SyntheticPackageFixtureBuilder();
        reader = new FilesystemScripturePackageReader();
    }

    @Test
    void ioFailureUsesStablePathFreeMessage() throws Exception {
        Path pkg = fixtures.writeApprovedChapterPackage(
                tempDir,
                "fixture-chapter-12-reader-io",
                12,
                20,
                1,
                "FIXTURE_NON_SCRIPTURAL_VERSE_");
        Files.delete(pkg.resolve("manifest.json"));

        assertThatThrownBy(() -> reader.read(pkg))
                .isInstanceOf(ScripturePackageReadException.class)
                .hasMessage(ScripturePackageReadException.STABLE_MESSAGE)
                .satisfies(ex -> assertThat(ex.getMessage())
                        .doesNotContain("/Users/")
                        .doesNotContain("/home/")
                        .doesNotContain(pkg.toAbsolutePath().toString())
                        .doesNotContain("FIXTURE_NON_SCRIPTURAL"));
    }
}
