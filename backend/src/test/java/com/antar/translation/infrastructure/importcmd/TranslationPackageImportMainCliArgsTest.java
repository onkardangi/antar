package com.antar.translation.infrastructure.importcmd;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class TranslationPackageImportMainCliArgsTest {

    @Test
    void parsesDryRunAndPackagePath() {
        TranslationPackageImportMain.CliArgs args = TranslationPackageImportMain.CliArgs.parse(
                new String[] {"--package-path", "/tmp/pkg", "--dry-run"});
        assertThat(args.dryRun()).isTrue();
        assertThat(args.packagePath().toString()).isEqualTo("/tmp/pkg");
    }

    @Test
    void requiresPackagePath() {
        assertThatThrownBy(() -> TranslationPackageImportMain.CliArgs.parse(new String[] {"--dry-run"}))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("--package-path");
    }
}
