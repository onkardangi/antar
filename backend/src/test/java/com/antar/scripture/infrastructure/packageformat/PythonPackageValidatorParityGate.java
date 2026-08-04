package com.antar.scripture.infrastructure.packageformat;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Objects;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

/**
 * Fail-closed bridge to the version-controlled Python Package Format v1 validator.
 *
 * <p>Used only by the verification parity gate. The runtime importer never spawns Python.
 */
final class PythonPackageValidatorParityGate {

    private static final long DEFAULT_TIMEOUT_SECONDS = 60;

    private final ObjectMapper objectMapper;
    private final ProcessLauncher processLauncher;
    private final Supplier<Boolean> python3Available;
    private final long timeoutSeconds;

    PythonPackageValidatorParityGate() {
        this(new ObjectMapper(), new DefaultProcessLauncher(), PythonPackageValidatorParityGate::detectPython3, DEFAULT_TIMEOUT_SECONDS);
    }

    PythonPackageValidatorParityGate(
            ObjectMapper objectMapper,
            ProcessLauncher processLauncher,
            Supplier<Boolean> python3Available,
            long timeoutSeconds) {
        this.objectMapper = Objects.requireNonNull(objectMapper);
        this.processLauncher = Objects.requireNonNull(processLauncher);
        this.python3Available = Objects.requireNonNull(python3Available);
        this.timeoutSeconds = timeoutSeconds;
    }

    JsonNode validate(Path packageDir, Path sourcesRegistry, Path validatePackageScript) {
        Objects.requireNonNull(packageDir, "packageDir is required");
        Objects.requireNonNull(sourcesRegistry, "sourcesRegistry is required");
        Objects.requireNonNull(validatePackageScript, "validatePackageScript is required");

        if (!Boolean.TRUE.equals(python3Available.get())) {
            throw new AssertionError("python3 is required for Package Format v1 parity gate");
        }
        if (!Files.isRegularFile(validatePackageScript)) {
            throw new AssertionError("validate_package.py is required for Package Format v1 parity gate");
        }

        ProcessResult result;
        try {
            result = processLauncher.launch(
                    new String[] {
                        "python3",
                        validatePackageScript.toString(),
                        packageDir.toString(),
                        "--sources-registry",
                        sourcesRegistry.toString(),
                        "--json"
                    },
                    timeoutSeconds,
                    TimeUnit.SECONDS);
        } catch (IOException ex) {
            throw new AssertionError("failed to start python3 validate_package.py for parity gate", ex);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
            throw new AssertionError("parity gate interrupted while waiting for validate_package.py");
        }

        if (!result.finished()) {
            throw new AssertionError("validate_package.py timed out during Package Format v1 parity gate");
        }
        if (result.exitCode() != 0 && result.exitCode() != 1) {
            // Python validator returns 0 when structurally valid, 1 when structurally invalid.
            // Other codes are unexpected process failures.
            throw new AssertionError(
                    "validate_package.py exited with unexpected code " + result.exitCode());
        }

        String output = result.stdout();
        if (output == null || output.isBlank()) {
            throw new AssertionError(
                    result.exitCode() == 0 || result.exitCode() == 1
                            ? "validate_package.py produced empty output"
                            : "validate_package.py produced empty output after exit "
                                    + result.exitCode());
        }
        try {
            JsonNode node = objectMapper.readTree(output);
            if (!node.has("structurallyValid")
                    || !node.has("editoriallyValid")
                    || !node.has("importable")
                    || !node.has("warnings")) {
                throw new AssertionError("validate_package.py JSON missing required parity fields");
            }
            return node;
        } catch (IOException ex) {
            throw new AssertionError("validate_package.py produced malformed JSON", ex);
        }
    }

    static boolean detectPython3() {
        try {
            Process process = new ProcessBuilder("python3", "--version").start();
            boolean finished = process.waitFor(10, TimeUnit.SECONDS);
            return finished && process.exitValue() == 0;
        } catch (Exception ex) {
            return false;
        }
    }

    interface ProcessLauncher {
        ProcessResult launch(String[] command, long timeout, TimeUnit unit)
                throws IOException, InterruptedException;
    }

    record ProcessResult(boolean finished, int exitCode, String stdout) {
    }

    static final class DefaultProcessLauncher implements ProcessLauncher {
        @Override
        public ProcessResult launch(String[] command, long timeout, TimeUnit unit)
                throws IOException, InterruptedException {
            Process process = new ProcessBuilder(command).start();
            boolean finished = process.waitFor(timeout, unit);
            if (!finished) {
                process.destroyForcibly();
                return new ProcessResult(false, -1, "");
            }
            String stdout;
            try (InputStream in = process.getInputStream()) {
                stdout = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            }
            // Drain stderr without merging into JSON stdout (path-safe: do not surface contents).
            try (InputStream err = process.getErrorStream()) {
                err.readAllBytes();
            }
            return new ProcessResult(true, process.exitValue(), stdout);
        }
    }
}
