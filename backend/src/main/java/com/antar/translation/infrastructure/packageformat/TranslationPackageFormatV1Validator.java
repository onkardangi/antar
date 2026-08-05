package com.antar.translation.infrastructure.packageformat;

import com.antar.translation.application.port.PackageFormatValidator;
import com.antar.translation.application.port.PackageValidationOptions;
import com.antar.translation.application.port.PackageValidationResult;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.HexFormat;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;
import org.springframework.stereotype.Component;

/**
 * Translation Package Format v1 validator.
 *
 * <p>Mirrors the version-controlled Python validator rules. Not a full JSON Schema engine.
 */
@Component
public class TranslationPackageFormatV1Validator implements PackageFormatValidator {

    private static final Set<String> REQUIRED_FILES =
            Set.of("manifest.json", "translations.jsonl", "provenance.json", "SHA256SUMS");
    private static final Set<String> ALLOWED_STATUSES =
            Set.of("DRAFT", "APPROVED", "SUPERSEDED", "REVOKED");
    private static final Set<String> FORBIDDEN_RECORD_KEYS = Set.of(
            "sanskrit",
            "sanskritText",
            "commentary",
            "commentaries",
            "notes",
            "approvalStatus",
            "reviewStatus",
            "status",
            "auditLog",
            "editorialNotes");
    private static final Pattern PACKAGE_ID_PATTERN = Pattern.compile("^[a-z0-9]+(-[a-z0-9]+)*$");
    private static final Pattern REF_PATTERN = Pattern.compile("^[1-9][0-9]*\\.[1-9][0-9]*$");
    private static final Pattern SHA256_PATTERN = Pattern.compile("^[a-f0-9]{64}$");
    private static final Pattern CREATED_AT_PATTERN =
            Pattern.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$");
    private static final Pattern UNSAFE_TEXT_PATTERN = Pattern.compile(
            "(?i)\\b(TODO|FIXME|lorem ipsum|tbd|xxx|insert text here)\\b");

    private final ObjectMapper objectMapper;

    public TranslationPackageFormatV1Validator() {
        this(new ObjectMapper());
    }

    TranslationPackageFormatV1Validator(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override
    public PackageValidationResult validate(Path packageDirectory, PackageValidationOptions options) {
        Objects.requireNonNull(packageDirectory, "packageDirectory is required");
        Objects.requireNonNull(options, "options is required");

        List<String> errors = new ArrayList<>();
        List<String> warnings = new ArrayList<>();

        Path dir = packageDirectory.toAbsolutePath().normalize();
        if (!Files.isDirectory(dir)) {
            errors.add("package directory does not exist");
            return result(false, false, false, errors, warnings);
        }

        Set<String> present = listFiles(dir, errors);
        if (!errors.isEmpty()) {
            return result(false, false, false, errors, warnings);
        }
        for (String required : REQUIRED_FILES) {
            if (!present.contains(required)) {
                errors.add("missing required file: " + required);
            }
        }
        for (String name : present) {
            if (!REQUIRED_FILES.contains(name)) {
                errors.add("unexpected file: " + name);
            }
        }
        if (!errors.isEmpty()) {
            return result(false, false, false, errors, warnings);
        }

        JsonNode manifest;
        List<JsonNode> translations;
        JsonNode provenance;
        Map<String, String> sums;
        byte[] translationsBytes;
        byte[] provenanceBytes;
        byte[] manifestBytes;
        try {
            manifestBytes = Files.readAllBytes(dir.resolve("manifest.json"));
            translationsBytes = Files.readAllBytes(dir.resolve("translations.jsonl"));
            provenanceBytes = Files.readAllBytes(dir.resolve("provenance.json"));
            manifest = objectMapper.readTree(manifestBytes);
            translations = readJsonl(translationsBytes);
            provenance = objectMapper.readTree(provenanceBytes);
            sums = parseSha256Sums(Files.readString(dir.resolve("SHA256SUMS"), StandardCharsets.UTF_8));
        } catch (IOException | RuntimeException ex) {
            errors.add("failed to parse package files");
            return result(false, false, false, errors, warnings);
        }

        validateManifestShape(manifest, errors);
        validateProvenanceShape(provenance, errors);
        for (int i = 0; i < translations.size(); i++) {
            validateRecordShape(translations.get(i), i, errors);
        }

        String packageId = text(manifest, "packageId");
        if (packageId != null && !packageId.equals(dir.getFileName().toString())) {
            errors.add("packageId '" + packageId + "' does not match directory name '"
                    + dir.getFileName() + "'");
        }

        Map<String, String> actual = Map.of(
                "manifest.json", sha256(manifestBytes),
                "translations.jsonl", sha256(translationsBytes),
                "provenance.json", sha256(provenanceBytes));
        if (!sums.keySet().equals(Set.of("manifest.json", "provenance.json", "translations.jsonl"))) {
            errors.add(
                    "SHA256SUMS must list exactly manifest.json, provenance.json, translations.jsonl; got "
                            + sums.keySet().stream().sorted().toList());
        }
        for (Map.Entry<String, String> entry : actual.entrySet()) {
            if (!entry.getValue().equals(sums.get(entry.getKey()))) {
                errors.add("checksum mismatch for " + entry.getKey());
            }
        }

        JsonNode fileChecksums = manifest.get("fileChecksums");
        if (fileChecksums != null && fileChecksums.isObject()) {
            for (String name : List.of("translations.jsonl", "provenance.json")) {
                if (!actual.get(name).equals(text(fileChecksums, name))) {
                    errors.add("manifest.fileChecksums mismatch for " + name);
                }
            }
        }
        String expectedPkg = sha256(concat(translationsBytes, provenanceBytes));
        if (!expectedPkg.equals(text(manifest, "packageChecksum"))) {
            errors.add("manifest.packageChecksum does not match canonical combined checksum");
        }

        String status = text(manifest, "packageStatus");
        if (status != null && !ALLOWED_STATUSES.contains(status)) {
            errors.add("packageStatus '" + status + "' is not allowed");
        }

        int recordCount = intValue(manifest, "recordCount", -1);
        if (recordCount != translations.size()) {
            errors.add("recordCount " + recordCount + " != translations.jsonl length " + translations.size());
        }

        int chapter = intValue(manifest, "chapterNumber", -1);
        JsonNode refRange = manifest.get("canonicalReferenceRange");
        Set<String> seen = new HashSet<>();
        Set<String> sourceIdsUsed = new LinkedHashSet<>();
        List<Integer> verseNumbers = new ArrayList<>();

        for (int i = 0; i < translations.size(); i++) {
            JsonNode row = translations.get(i);
            int ch = intValue(row, "chapterNumber", -1);
            int vn = intValue(row, "verseNumber", -1);
            String ref = text(row, "canonicalReference");
            if (ch != chapter) {
                errors.add("translations.jsonl[" + i + "]: chapterNumber " + ch + " != manifest " + chapter);
            }
            String expectedRef = ch + "." + vn;
            if (ref != null && !ref.equals(expectedRef)) {
                errors.add("translations.jsonl[" + i + "]: canonicalReference '" + ref + "' != '"
                        + expectedRef + "'");
            }
            String body = text(row, "translationText");
            if (body == null || body.isBlank()) {
                errors.add("translations.jsonl[" + i + "]: translationText must be nonblank");
            } else if (UNSAFE_TEXT_PATTERN.matcher(body).find()) {
                errors.add("translations.jsonl[" + i + "]: unsafe placeholder markers in translationText");
            }
            Iterator<String> fields = row.fieldNames();
            while (fields.hasNext()) {
                String field = fields.next();
                if (FORBIDDEN_RECORD_KEYS.contains(field)) {
                    errors.add("translations.jsonl[" + i + "]: forbidden fields present: [" + field + "]");
                }
            }
            if (ref != null) {
                if (!seen.add(ref)) {
                    errors.add("duplicate Verse canonicalReference: " + ref);
                } else {
                    verseNumbers.add(vn);
                }
            }
            JsonNode sourceIds = row.get("sourceIds");
            JsonNode sourceChecksums = row.get("sourceChecksums");
            if (sourceIds != null && sourceIds.isArray()) {
                for (JsonNode sid : sourceIds) {
                    sourceIdsUsed.add(sid.asText());
                    if (sourceChecksums == null || !sourceChecksums.has(sid.asText())) {
                        errors.add("translations.jsonl[" + i + "]: missing sourceChecksums entry for "
                                + sid.asText());
                    }
                }
            }
        }

        if (!verseNumbers.isEmpty() && refRange != null && refRange.isObject()) {
            List<Integer> sorted = verseNumbers.stream().sorted().toList();
            String expectedFrom = chapter + "." + sorted.getFirst();
            String expectedTo = chapter + "." + sorted.getLast();
            if (!expectedFrom.equals(text(refRange, "from"))
                    || !expectedTo.equals(text(refRange, "to"))) {
                errors.add("canonicalReferenceRange mismatch: manifest vs data " + expectedFrom
                        + ".." + expectedTo);
            }
            if (intValue(refRange, "expectedCount", -1) != verseNumbers.size()) {
                errors.add("canonicalReferenceRange.expectedCount != record count");
            }
            List<Integer> contiguous = new ArrayList<>();
            for (int n = sorted.getFirst(); n < sorted.getFirst() + sorted.size(); n++) {
                contiguous.add(n);
            }
            if (!sorted.equals(contiguous)) {
                errors.add("Verse numbers are not contiguous: " + sorted);
            }
        }

        Path registryPath = options.sourcesRegistryPathOptional().orElse(null);
        if (registryPath != null) {
            Set<String> registryIds;
            try {
                registryIds = loadSourceIds(registryPath);
            } catch (IOException | RuntimeException ex) {
                errors.add("failed to load source registry");
                registryIds = Set.of();
            }
            Set<String> requiredSources = new LinkedHashSet<>(sourceIdsUsed);
            JsonNode refs = manifest.get("sourceRegistryReferences");
            if (refs != null && refs.isArray()) {
                for (JsonNode ref : refs) {
                    requiredSources.add(ref.asText());
                }
            }
            for (String sid : requiredSources) {
                if (!registryIds.contains(sid)) {
                    errors.add("unresolved source ID: " + sid);
                }
            }
        }

        if (packageId != null && !packageId.equals(text(provenance, "packageId"))) {
            errors.add("provenance.packageId does not match manifest.packageId");
        }

        if ("APPROVED".equals(status)) {
            if (isEmptyArray(provenance.get("editorialReviewerIds"))) {
                errors.add("APPROVED package missing editorialReviewerIds");
            }
            if (isEmptyArray(provenance.get("approvalDates"))) {
                errors.add("APPROVED package missing approvalDates");
            }
            String approvalChecksum = text(manifest, "editorialApprovalManifestChecksum");
            if (approvalChecksum == null || approvalChecksum.isBlank()) {
                errors.add("APPROVED package missing editorialApprovalManifestChecksum");
            }
            for (int i = 0; i < translations.size(); i++) {
                JsonNode row = translations.get(i);
                if (blank(text(row, "editorialDecisionId"))) {
                    errors.add("translations.jsonl[" + i + "]: APPROVED package missing editorialDecisionId");
                }
                if (blank(text(row, "editorialApprovalChecksum"))) {
                    errors.add(
                            "translations.jsonl[" + i + "]: APPROVED package missing editorialApprovalChecksum");
                }
            }
        }

        boolean structurallyValid = errors.stream().noneMatch(TranslationPackageFormatV1Validator::isEditorialError);
        boolean editoriallyValid =
                structurallyValid && errors.stream().noneMatch(TranslationPackageFormatV1Validator::isEditorialError);
        // Recompute after editorial appends
        structurallyValid = errors.stream().noneMatch(e -> !isEditorialError(e));
        editoriallyValid = structurallyValid && errors.stream().noneMatch(TranslationPackageFormatV1Validator::isEditorialError);

        boolean importable = "APPROVED".equals(status) && structurallyValid && editoriallyValid;
        if (!"APPROVED".equals(status)) {
            importable = false;
            if ("DRAFT".equals(status)) {
                warnings.add("DRAFT package is never importable");
            }
        }

        return result(structurallyValid, editoriallyValid, importable, errors, warnings);
    }

    private void validateManifestShape(JsonNode manifest, List<String> errors) {
        requireText(manifest, "packageId", PACKAGE_ID_PATTERN, errors);
        requireText(manifest, "scriptureId", null, errors);
        requireText(manifest, "language", null, errors);
        requireText(manifest, "provider", null, errors);
        requireText(manifest, "sourceName", null, errors);
        requireText(manifest, "licenseType", null, errors);
        if (intValue(manifest, "chapterNumber", -1) < 1 || intValue(manifest, "chapterNumber", -1) > 18) {
            errors.add("chapterNumber must be between 1 and 18");
        }
        if (intValue(manifest, "contentVersion", -1) < 1) {
            errors.add("contentVersion must be positive");
        }
        if (intValue(manifest, "recordCount", -1) < 1) {
            errors.add("recordCount must be positive");
        }
        if (intValue(manifest, "packageFormatVersion", -1) != 1) {
            errors.add("packageFormatVersion must be 1");
        }
        if (!"SHA-256".equals(text(manifest, "checksumAlgorithm"))) {
            errors.add("checksumAlgorithm must be SHA-256");
        }
        String createdAt = text(manifest, "createdAt");
        if (createdAt == null || !CREATED_AT_PATTERN.matcher(createdAt).matches()) {
            errors.add("createdAt must be UTC Zulu timestamp");
        }
        String status = text(manifest, "packageStatus");
        if (status == null || !ALLOWED_STATUSES.contains(status)) {
            errors.add("packageStatus is required");
        }
        String pkgChecksum = text(manifest, "packageChecksum");
        if (pkgChecksum == null || !SHA256_PATTERN.matcher(pkgChecksum).matches()) {
            errors.add("packageChecksum must be sha256 hex");
        }
        String approval = text(manifest, "editorialApprovalManifestChecksum");
        if (approval == null || !SHA256_PATTERN.matcher(approval).matches()) {
            errors.add("editorialApprovalManifestChecksum must be sha256 hex");
        }
        JsonNode refs = manifest.get("sourceRegistryReferences");
        if (refs == null || !refs.isArray() || refs.isEmpty()) {
            errors.add("sourceRegistryReferences must be a non-empty array");
        }
        JsonNode range = manifest.get("canonicalReferenceRange");
        if (range == null || !range.isObject()) {
            errors.add("canonicalReferenceRange is required");
        } else {
            String from = text(range, "from");
            String to = text(range, "to");
            if (from == null || !REF_PATTERN.matcher(from).matches()) {
                errors.add("canonicalReferenceRange.from invalid");
            }
            if (to == null || !REF_PATTERN.matcher(to).matches()) {
                errors.add("canonicalReferenceRange.to invalid");
            }
            if (intValue(range, "expectedCount", -1) < 1) {
                errors.add("canonicalReferenceRange.expectedCount must be positive");
            }
        }
        JsonNode fileChecksums = manifest.get("fileChecksums");
        if (fileChecksums == null || !fileChecksums.isObject()) {
            errors.add("fileChecksums is required");
        }
    }

    private void validateProvenanceShape(JsonNode provenance, List<String> errors) {
        requireText(provenance, "packageId", PACKAGE_ID_PATTERN, errors);
        if (isEmptyArray(provenance.get("sourceIds"))) {
            errors.add("provenance.sourceIds must be non-empty");
        }
        if (provenance.get("sourceRoles") == null || !provenance.get("sourceRoles").isObject()) {
            errors.add("provenance.sourceRoles is required");
        }
        if (provenance.get("sourceChecksums") == null || !provenance.get("sourceChecksums").isObject()) {
            errors.add("provenance.sourceChecksums is required");
        }
        if (provenance.get("licenses") == null || !provenance.get("licenses").isObject()) {
            errors.add("provenance.licenses is required");
        }
    }

    private void validateRecordShape(JsonNode row, int index, List<String> errors) {
        String prefix = "translations.jsonl[" + index + "]: ";
        if (intValue(row, "chapterNumber", -1) < 1) {
            errors.add(prefix + "chapterNumber invalid");
        }
        if (intValue(row, "verseNumber", -1) < 1) {
            errors.add(prefix + "verseNumber invalid");
        }
        String ref = text(row, "canonicalReference");
        if (ref == null || !REF_PATTERN.matcher(ref).matches()) {
            errors.add(prefix + "canonicalReference invalid");
        }
        if (blank(text(row, "translationText"))) {
            errors.add(prefix + "translationText required");
        }
        if (intValue(row, "contentVersion", -1) < 1) {
            errors.add(prefix + "contentVersion invalid");
        }
        if (row.get("sourceIds") == null || !row.get("sourceIds").isArray() || row.get("sourceIds").isEmpty()) {
            errors.add(prefix + "sourceIds required");
        }
        if (row.get("sourceChecksums") == null || !row.get("sourceChecksums").isObject()) {
            errors.add(prefix + "sourceChecksums required");
        }
    }

    private static void requireText(JsonNode node, String field, Pattern pattern, List<String> errors) {
        String value = text(node, field);
        if (blank(value)) {
            errors.add(field + " is required");
            return;
        }
        if (pattern != null && !pattern.matcher(value).matches()) {
            errors.add(field + " has invalid format");
        }
    }

    private static boolean isEditorialError(String error) {
        return error.contains("APPROVED package missing")
                || error.contains("unresolved source")
                || error.contains("editorialDecisionId")
                || error.contains("editorialApprovalChecksum");
    }

    private static boolean blank(String value) {
        return value == null || value.isBlank();
    }

    private static boolean isEmptyArray(JsonNode node) {
        return node == null || !node.isArray() || node.isEmpty();
    }

    private static PackageValidationResult result(
            boolean structurallyValid,
            boolean editoriallyValid,
            boolean importable,
            List<String> errors,
            List<String> warnings) {
        return new PackageValidationResult(
                structurallyValid, editoriallyValid, importable, errors, warnings);
    }

    private static Set<String> listFiles(Path dir, List<String> errors) {
        Set<String> names = new HashSet<>();
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
            for (Path path : stream) {
                if (Files.isRegularFile(path)) {
                    names.add(path.getFileName().toString());
                } else {
                    errors.add("unexpected non-file entry: " + path.getFileName());
                }
            }
        } catch (IOException ex) {
            errors.add("failed to list package directory");
        }
        return names;
    }

    private List<JsonNode> readJsonl(byte[] bytes) throws IOException {
        List<JsonNode> rows = new ArrayList<>();
        for (String line : new String(bytes, StandardCharsets.UTF_8).split("\\R")) {
            if (line.isBlank()) {
                continue;
            }
            rows.add(objectMapper.readTree(line));
        }
        return rows;
    }

    private static Map<String, String> parseSha256Sums(String content) {
        Map<String, String> sums = new HashMap<>();
        for (String line : content.split("\\R")) {
            if (line.isBlank()) {
                continue;
            }
            String[] parts = line.trim().split("\\s+", 2);
            if (parts.length == 2) {
                sums.put(parts[1].trim(), parts[0].trim().toLowerCase());
            }
        }
        return sums;
    }

    private Set<String> loadSourceIds(Path registryPath) throws IOException {
        JsonNode root = objectMapper.readTree(Files.readAllBytes(registryPath));
        Set<String> ids = new HashSet<>();
        JsonNode sources = root.isArray() ? root : root.get("sources");
        if (sources != null && sources.isArray()) {
            for (JsonNode source : sources) {
                String id = text(source, "id");
                if (id != null) {
                    ids.add(id);
                }
            }
        }
        return ids;
    }

    private static String text(JsonNode node, String field) {
        if (node == null || !node.has(field) || node.get(field).isNull()) {
            return null;
        }
        return node.get(field).asText();
    }

    private static int intValue(JsonNode node, String field, int defaultValue) {
        if (node == null || !node.has(field) || !node.get(field).canConvertToInt()) {
            return defaultValue;
        }
        return node.get(field).asInt();
    }

    private static byte[] concat(byte[] a, byte[] b) {
        byte[] out = new byte[a.length + b.length];
        System.arraycopy(a, 0, out, 0, a.length);
        System.arraycopy(b, 0, out, a.length, b.length);
        return out;
    }

    private static String sha256(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data));
        } catch (NoSuchAlgorithmException ex) {
            throw new IllegalStateException("SHA-256 unavailable", ex);
        }
    }
}
