package com.antar.scripture.infrastructure.importcmd;

import com.antar.AntarApplication;
import com.antar.scripture.application.imports.ImportScripturePackageCommand;
import com.antar.scripture.application.imports.ImportScripturePackageResult;
import com.antar.scripture.application.imports.ImportScripturePackageUseCase;
import com.antar.scripture.domain.ImportExecutionStatus;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * Controlled administrative entry point for Scripture package import.
 *
 * <p>Never runs during normal {@code AntarApplication} startup. Uses {@link WebApplicationType#NONE},
 * closes its context, and leaves {@link System#exit} to {@link #main(String[])} only.
 */
public final class ScripturePackageImportMain {

    private ScripturePackageImportMain() {
    }

    public static void main(String[] args) {
        int code = run(args);
        System.exit(code);
    }

    /**
     * Testable entry that does not call {@link System#exit(int)}.
     *
     * @return process exit code (0 success, non-zero failure)
     */
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
            ImportScripturePackageUseCase useCase = context.getBean(ImportScripturePackageUseCase.class);
            ImportScripturePackageResult result = useCase.execute(
                    ImportScripturePackageCommand.of(parsed.packagePath(), parsed.dryRun()));
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

    /** Visible for path-safety unit tests; does not call {@link System#exit(int)}. */
    public static void printSummaryForTest(ImportScripturePackageResult result) {
        printSummary(result);
    }

    private static void printSummary(ImportScripturePackageResult result) {
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
        System.err.println("Usage: ScripturePackageImportMain --package-path <dir> [--dry-run]");
    }

    record CliArgs(Path packagePath, boolean dryRun) {

        static CliArgs parse(String[] args) {
            Path packagePath = null;
            boolean dryRun = false;
            List<String> unknown = new ArrayList<>();
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
                } else if (arg.startsWith("-")) {
                    unknown.add(arg);
                }
            }
            if (!unknown.isEmpty()) {
                throw new IllegalArgumentException("unknown arguments: " + unknown);
            }
            if (packagePath == null) {
                throw new IllegalArgumentException("--package-path is required");
            }
            return new CliArgs(packagePath, dryRun);
        }
    }
}
