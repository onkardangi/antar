package com.antar.translation.infrastructure.importcmd;

import com.antar.AntarApplication;
import com.antar.translation.application.imports.ImportTranslationPackageCommand;
import com.antar.translation.application.imports.ImportTranslationPackageResult;
import com.antar.translation.application.imports.ImportTranslationPackageUseCase;
import com.antar.translation.domain.ImportExecutionStatus;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * Controlled administrative entry point for Translation package import.
 *
 * <p>Never runs during normal {@code AntarApplication} startup.
 */
public final class TranslationPackageImportMain {

    private TranslationPackageImportMain() {
    }

    public static void main(String[] args) {
        System.exit(run(args));
    }

    public static int run(String[] args) {
        CliArgs parsed;
        try {
            parsed = CliArgs.parse(args);
        } catch (IllegalArgumentException ex) {
            System.err.println(ex.getMessage());
            printUsage();
            return 2;
        }

        try (ConfigurableApplicationContext context = new SpringApplicationBuilder(AntarApplication.class)
                .web(WebApplicationType.NONE)
                .run(toSpringArgs(args))) {
            ImportTranslationPackageUseCase useCase = context.getBean(ImportTranslationPackageUseCase.class);
            ImportTranslationPackageResult result = useCase.execute(
                    ImportTranslationPackageCommand.of(parsed.packagePath(), parsed.dryRun()));
            printSummary(result);
            boolean ok = result.importStatus() == ImportExecutionStatus.IMPORTED && result.failureCode() == null;
            return ok ? 0 : 1;
        }
    }

    private static String[] toSpringArgs(String[] original) {
        List<String> springArgs = new ArrayList<>();
        for (String arg : original) {
            if (arg.startsWith("--spring.")
                    || arg.startsWith("--antar.")
                    || arg.startsWith("--server.")
                    || arg.startsWith("--logging.")) {
                springArgs.add(arg);
            }
        }
        return springArgs.toArray(String[]::new);
    }

    static void printSummaryForTest(ImportTranslationPackageResult result) {
        printSummary(result);
    }

    private static void printSummary(ImportTranslationPackageResult result) {
        System.out.println("packageId=" + result.packageId());
        System.out.println("packageChecksumPrefix="
                + (result.packageChecksum() == null || result.packageChecksum().length() < 12
                        ? result.packageChecksum()
                        : result.packageChecksum().substring(0, 12)));
        System.out.println("importStatus=" + result.importStatus());
        System.out.println("dryRun=" + result.dryRun());
        System.out.println("recordsRead=" + result.recordsRead());
        System.out.println("recordsValidated=" + result.recordsValidated());
        System.out.println("recordsUpdated=" + result.recordsUpdated());
        System.out.println("recordsUnchanged=" + result.recordsUnchanged());
        System.out.println("recordsRejected=" + result.recordsRejected());
        System.out.println("durationMs=" + result.duration().toMillis());
        result.failureCodeOptional().ifPresent(code -> System.out.println("failureCode=" + code));
        result.failureMessageOptional().ifPresent(msg -> System.out.println("failureMessage=" + msg));
        if (result.validationResult() != null) {
            System.out.println("structurallyValid=" + result.validationResult().structurallyValid());
            System.out.println("editoriallyValid=" + result.validationResult().editoriallyValid());
            System.out.println("importable=" + result.validationResult().importable());
            System.out.println("warningCount=" + result.validationResult().warnings().size());
        }
    }

    private static void printUsage() {
        System.err.println("Usage: TranslationPackageImportMain --package-path <dir> [--dry-run]");
    }

    record CliArgs(Path packagePath, boolean dryRun) {

        static CliArgs parse(String[] args) {
            Path packagePath = null;
            boolean dryRun = false;
            for (int i = 0; i < args.length; i++) {
                String arg = args[i];
                if ("--dry-run".equals(arg)) {
                    dryRun = true;
                } else if ("--package-path".equals(arg)) {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("--package-path requires a value");
                    }
                    packagePath = Path.of(args[++i]);
                } else if (arg.startsWith("--package-path=")) {
                    packagePath = Path.of(arg.substring("--package-path=".length()));
                } else if (arg.startsWith("--spring.")
                        || arg.startsWith("--antar.")
                        || arg.startsWith("--server.")
                        || arg.startsWith("--logging.")) {
                    // forwarded to Spring
                } else {
                    throw new IllegalArgumentException("unknown argument: " + arg);
                }
            }
            if (packagePath == null) {
                throw new IllegalArgumentException("--package-path is required");
            }
            return new CliArgs(packagePath, dryRun);
        }
    }
}
