package com.antar.scripture.infrastructure.importcmd;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class ScripturePackageImportMainCliArgsTest {

    @Test
    void parsesPackagePathAndDryRun() {
        ScripturePackageImportMain.CliArgs args = ScripturePackageImportMain.CliArgs.parse(
                new String[] {"--package-path", "/tmp/pkg", "--dry-run"});
        assertThat(args.packagePath()).isEqualTo(Path.of("/tmp/pkg"));
        assertThat(args.dryRun()).isTrue();
    }

    @Test
    void requiresPackagePath() {
        assertThatThrownBy(() -> ScripturePackageImportMain.CliArgs.parse(new String[] {"--dry-run"}))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("--package-path");
    }
}
