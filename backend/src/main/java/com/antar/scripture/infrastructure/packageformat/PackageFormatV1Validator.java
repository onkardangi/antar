package com.antar.scripture.infrastructure.packageformat;

import com.antar.scripture.application.port.PackageFormatValidator;
import com.antar.scripture.application.port.PackageValidationOptions;
import com.antar.scripture.application.port.PackageValidationResult;
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
import java.util.HexFormat;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.regex.Pattern;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Antar Package Format v1 validator.
 *
 * <p>Mirrors the version-controlled Python validator rules for format version 1. This is <strong>not</strong>
 * a standards-compliant JSON Schema engine; required fields, enums, patterns, and package rules are
 * checked explicitly against the v1 contract.
 */
@Component
public class PackageFormatV1Validator implements PackageFormatValidator {

    private static final Set<String> REQUIRED_FILES =
            Set.of("manifest.json", "verses.jsonl", "provenance.json", "SHA256SUMS");
    private static final Set<String> ALLOWED_STATUSES =
            Set.of("DRAFT", "APPROVED", "SUPERSEDED", "REVOKED");
    private static final Set<String> FORBIDDEN_VERSE_KEYS = Set.of(
            "translation",
            "translations",
            "commentary",
            "commentaries",
            "approvalStatus",
            "reviewStatus",
            "status",
            "auditLog",
            "editorialNotes",
            "placeholder");
    private static final Pattern PACKAGE_ID_PATTERN = Pattern.compile("^[a-z0-9]+(-[a-z0-9]+)*$");
    private static final Pattern REF_PATTERN = Pattern.compile("^[1-9][0-9]*\\.[1-9][0-9]*$");
    private static final Pattern SHA256_PATTERN = Pattern.compile("^[a-f0-9]{64}$");
    private static final Pattern CREATED_AT_PATTERN =
            Pattern.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$");
    private static final Pattern APPROVAL_DATE_PATTERN = Pattern.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$");
    private static final Pattern PLACEHOLDER_PATTERN = Pattern.compile(
            "(?i)\\b(TODO|FIXME|placeholder|lorem ipsum|tbd|xxx|insert text here)\\b");

    private final ObjectMapper objectMapper;
    private final Path defaultSourcesRegistry;
    private final Path defaultVerseCounts;

    @org.springframework.beans.factory.annotation.Autowired
    public PackageFormatV1Validator(
            @Value("${antar.scripture.package.sources-registry:}") String sourcesRegistry,
            @Value("${antar.scripture.package.verse-counts:}") String verseCounts) {
        this(new ObjectMapper(), sourcesRegistry, verseCounts);
    }

    /** Test/helper constructor. */
    PackageFormatV1Validator(ObjectMapper objectMapper, String sourcesRegistry, String verseCounts) {
        this.objectMapper = objectMapper;
        this.defaultSourcesRegistry = sourcesRegistry == null || sourcesRegistry.isBlank()
                ? null
                : Path.of(sourcesRegistry);
        this.defaultVerseCounts =
                verseCounts == null || verseCounts.isBlank() ? null : Path.of(verseCounts);
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
        List<JsonNode> verses;
        JsonNode provenance;
        Map<String, String> sums;
        byte[] versesBytes;
        byte[] provenanceBytes;
        byte[] manifestBytes;
        try {
            manifestBytes = Files.readAllBytes(dir.resolve("manifest.json"));
            versesBytes = Files.readAllBytes(dir.resolve("verses.jsonl"));
            provenanceBytes = Files.readAllBytes(dir.resolve("provenance.json"));
            manifest = objectMapper.readTree(manifestBytes);
            verses = readJsonl(versesBytes);
            provenance = objectMapper.readTree(provenanceBytes);
            sums = parseSha256Sums(Files.readString(dir.resolve("SHA256SUMS"), StandardCharsets.UTF_8));
        } catch (IOException | RuntimeException ex) {
            errors.add("failed to parse package files");
            return result(false, false, false, errors, warnings);
        }

        validateManifestShape(manifest, errors);
        validateProvenanceShape(provenance, errors);
        for (int i = 0; i < verses.size(); i++) {
            validateVerseShape(verses.get(i), i, errors);
        }

        String packageId = text(manifest, "packageId");
        if (packageId != null && !packageId.equals(dir.getFileName().toString())) {
            errors.add("packageId '" + packageId + "' does not match directory name '"
                    + dir.getFileName() + "'");
        }

        Map<String, String> actual = Map.of(
                "manifest.json", sha256(manifestBytes),
                "verses.jsonl", sha256(versesBytes),
                "provenance.json", sha256(provenanceBytes));
        if (!sums.keySet().equals(Set.of("manifest.json", "provenance.json", "verses.jsonl"))) {
            errors.add(
                    "SHA256SUMS must list exactly manifest.json, provenance.json, verses.jsonl; got "
                            + sums.keySet().stream().sorted().toList());
        }
        for (Map.Entry<String, String> entry : actual.entrySet()) {
            if (!entry.getValue().equals(sums.get(entry.getKey()))) {
                errors.add("checksum mismatch for " + entry.getKey());
            }
        }

        JsonNode fileChecksums = manifest.get("fileChecksums");
        if (fileChecksums != null && fileChecksums.isObject()) {
            for (String name : List.of("verses.jsonl", "provenance.json")) {
                if (!actual.get(name).equals(text(fileChecksums, name))) {
                    errors.add("manifest.fileChecksums mismatch for " + name);
                }
            }
        }
        String expectedPkg = sha256(concat(versesBytes, provenanceBytes));
        if (!expectedPkg.equals(text(manifest, "packageChecksum"))) {
            errors.add("manifest.packageChecksum does not match canonical combined checksum");
        }

        String status = text(manifest, "packageStatus");
        if (status != null && !ALLOWED_STATUSES.contains(status)) {
            errors.add("packageStatus '" + status + "' is not allowed");
        }

        int recordCount = intValue(manifest, "recordCount", -1);
        if (recordCount != verses.size()) {
            errors.add("recordCount " + recordCount + " != verses.jsonl length " + verses.size());
        }

        int chapter = intValue(manifest, "chapterNumber", -1);
        JsonNode refRange = manifest.get("canonicalReferenceRange");
        boolean allowNullTl = booleanValue(manifest, "allowNullTransliteration", false);
        Set<String> seen = new HashSet<>();
        Set<String> sourceIdsUsed = new LinkedHashSet<>();
        List<Integer> verseNumbers = new ArrayList<>();

        for (int i = 0; i < verses.size(); i++) {
            JsonNode row = verses.get(i);
            int ch = intValue(row, "chapterNumber", -1);
            int vn = intValue(row, "verseNumber", -1);
            String ref = text(row, "canonicalReference");
            if (ch != chapter) {
                errors.add("verses.jsonl[" + i + "]: chapterNumber " + ch + " != manifest " + chapter);
            }
            String expectedRef = ch + "." + vn;
            if (ref != null && !ref.equals(expectedRef)) {
                errors.add("verses.jsonl[" + i + "]: canonicalReference '" + ref + "' != '"
                        + expectedRef + "'");
            }
            String sanskrit = text(row, "sanskritText");
            if (sanskrit == null || sanskrit.isBlank()) {
                errors.add("verses.jsonl[" + i + "]: sanskritText must be nonblank");
            } else if (PLACEHOLDER_PATTERN.matcher(sanskrit).find()) {
                errors.add("verses.jsonl[" + i + "]: placeholder text detected in sanskritText");
            }
            JsonNode tlNode = row.get("transliteration");
            if (tlNode == null || tlNode.isNull()) {
                if (!allowNullTl) {
                    errors.add(
                            "verses.jsonl[" + i + "]: transliteration null but policy forbids it");
                }
            } else if (!tlNode.isTextual() || tlNode.asText().isBlank()) {
                errors.add(
                        "verses.jsonl[" + i + "]: transliteration must be nonblank string or null");
            } else if (PLACEHOLDER_PATTERN.matcher(tlNode.asText()).find()) {
                errors.add(
                        "verses.jsonl[" + i + "]: placeholder text detected in transliteration");
            }
            Iterator<String> fields = row.fieldNames();
            while (fields.hasNext()) {
                String field = fields.next();
                if (FORBIDDEN_VERSE_KEYS.contains(field)) {
                    errors.add("verses.jsonl[" + i + "]: forbidden fields present: [" + field + "]");
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
                        errors.add("verses.jsonl[" + i + "]: missing sourceChecksums entry for "
                                + sid.asText());
                    }
                }
            }
        }

        boolean declaredFullChapter = false;
        Integer antarCount = expectedVerseCount(chapter, options);
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
            declaredFullChapter = antarCount != null
                    && (chapter + ".1").equals(text(refRange, "from"))
                    && (chapter + "." + antarCount).equals(text(refRange, "to"))
                    && intValue(refRange, "expectedCount", -1) == antarCount;
        }

        if (antarCount != null && verses.size() != antarCount) {
            if ("APPROVED".equals(status) && declaredFullChapter) {
                errors.add("APPROVED full-chapter package for chapter " + chapter
                        + " must contain " + antarCount + " Verses, found " + verses.size());
            } else {
                warnings.add("chapter " + chapter + " Antar full count is " + antarCount
                        + "; package has " + verses.size());
            }
        }

        Path registryPath = options.sourcesRegistryPathOptional()
                .orElse(defaultSourcesRegistry);
        Set<String> registryIds = Set.of();
        if (registryPath != null) {
            try {
                registryIds = loadSourceIds(registryPath);
            } catch (IOException | RuntimeException ex) {
                errors.add("failed to load source registry");
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
            JsonNode provenanceSources = provenance.get("sourceIds");
            if (provenanceSources != null && provenanceSources.isArray()) {
                for (JsonNode sid : provenanceSources) {
                    if (!registryIds.contains(sid.asText())) {
                        errors.add("provenance unresolved source ID: " + sid.asText());
                    }
                }
            }
        }

        if (packageId != null && !packageId.equals(text(provenance, "packageId"))) {
            errors.add("provenance.packageId does not match manifest.packageId");
        }

        boolean structurallyValid = errors.stream().noneMatch(PackageFormatV1Validator::isEditorialError);

        boolean editorialOk = structurallyValid;
        if ("APPROVED".equals(status)) {
            if (isEmptyArray(provenance.get("editorialReviewerIds"))) {
                errors.add("APPROVED package missing editorialReviewerIds");
                editorialOk = false;
            }
            if (isEmptyArray(provenance.get("approvalDates"))) {
                errors.add("APPROVED package missing approvalDates");
                editorialOk = false;
            }
            String approvalChecksum = text(manifest, "editorialApprovalManifestChecksum");
            if (approvalChecksum == null || approvalChecksum.isBlank()) {
                errors.add("APPROVED package missing editorialApprovalManifestChecksum");
                editorialOk = false;
            }
            for (int i = 0; i < verses.size(); i++) {
                JsonNode row = verses.get(i);
                if (text(row, "editorialDecisionId") == null
                        || text(row, "editorialDecisionId").isBlank()) {
                    errors.add("verses.jsonl[" + i + "]: APPROVED package missing editorialDecisionId");
                    editorialOk = false;
                }
                if (text(row, "editorialApprovalChecksum") == null
                        || text(row, "editorialApprovalChecksum").isBlank()) {
                    errors.add("verses.jsonl[" + i + "]: APPROVED package missing editorialApprovalChecksum");
                    editorialOk = false;
                }
            }
            if (declaredFullChapter && antarCount != null && verses.size() != antarCount) {
                editorialOk = false;
            }
        }
        if (errors.stream().anyMatch(e -> e.contains("unresolved source"))) {
            editorialOk = false;
        }

        boolean editoriallyValid = structurallyValid
                && editorialOk
                && errors.stream().noneMatch(PackageFormatV1Validator::isEditorialError);

        // Recompute structural after editorial errors were appended
        structurallyValid = errors.stream().noneMatch(e -> !isEditorialError(e));
        editoriallyValid = structurallyValid
                && errors.stream().noneMatch(PackageFormatV1Validator::isEditorialError);

        boolean importable = "APPROVED".equals(status) && structurallyValid && editoriallyValid;
        if (!"APPROVED".equals(status)) {
            importable = false;
            if ("DRAFT".equals(status)) {
                warnings.add("DRAFT package is never importable");
            }
        }

        return result(structurallyValid, editoriallyValid, importable, errors, warnings);
    }

    private Integer expectedVerseCount(int chapter, PackageValidationOptions options) {
        Path path = options.verseCountsPathOptional().orElse(defaultVerseCounts);
        if (path == null || !Files.isRegularFile(path)) {
            path = resolveRepoRelative("content/validation/antar_verse_counts.json");
        }
        if (path == null || !Files.isRegularFile(path)) {
            return null;
        }
        try {
            JsonNode root = objectMapper.readTree(Files.readAllBytes(path));
            JsonNode counts = root.get("verse_counts");
            if (counts == null || !counts.has(String.valueOf(chapter))) {
                return null;
            }
            return counts.get(String.valueOf(chapter)).asInt();
        } catch (IOException ex) {
            return null;
        }
    }

    private Set<String> loadSourceIds(Path registryPath) throws IOException {
        JsonNode root = objectMapper.readTree(Files.readAllBytes(registryPath));
        JsonNode sources = root.isArray() ? root : root.get("sources");
        Set<String> ids = new HashSet<>();
        if (sources != null && sources.isArray()) {
            for (JsonNode source : sources) {
                if (source.has("id")) {
                    ids.add(source.get("id").asText());
                }
            }
        }
        return ids;
    }

    private static Path resolveRepoRelative(String relative) {
        Path cwd = Path.of("").toAbsolutePath().normalize();
        Path direct = cwd.resolve(relative);
        if (Files.isRegularFile(direct)) {
            return direct;
        }
        Path fromBackend = cwd.resolve("..").resolve(relative).normalize();
        if (Files.isRegularFile(fromBackend)) {
            return fromBackend;
        }
        return null;
    }

    private void validateManifestShape(JsonNode manifest, List<String> errors) {
        requireObject(manifest, "manifest", errors);
        requireFields(
                manifest,
                "manifest",
                errors,
                "packageId",
                "scriptureId",
                "chapterNumber",
                "contentVersion",
                "recordCount",
                "canonicalReferenceRange",
                "createdAt",
                "packageStatus",
                "sourceRegistryReferences",
                "editorialApprovalManifestChecksum",
                "packageFormatVersion",
                "checksumAlgorithm",
                "packageChecksum",
                "fileChecksums",
                "allowNullTransliteration");
        if (text(manifest, "packageId") != null
                && !PACKAGE_ID_PATTERN.matcher(text(manifest, "packageId")).matches()) {
            errors.add("manifest schema: packageId pattern mismatch");
        }
        int chapter = intValue(manifest, "chapterNumber", -1);
        if (chapter < 1 || chapter > 18) {
            errors.add("manifest schema: chapterNumber out of range");
        }
        if (intValue(manifest, "packageFormatVersion", -1) != 1) {
            errors.add("manifest schema: packageFormatVersion must be 1");
        }
        if (!"SHA-256".equals(text(manifest, "checksumAlgorithm"))) {
            errors.add("manifest schema: checksumAlgorithm must be SHA-256");
        }
        if (text(manifest, "packageChecksum") != null
                && !SHA256_PATTERN.matcher(text(manifest, "packageChecksum")).matches()) {
            errors.add("manifest schema: packageChecksum pattern mismatch");
        }
        if (text(manifest, "createdAt") != null
                && !CREATED_AT_PATTERN.matcher(text(manifest, "createdAt")).matches()) {
            errors.add("manifest schema: createdAt pattern mismatch");
        }
        rejectAdditional(
                manifest,
                "manifest",
                errors,
                "packageId",
                "scriptureId",
                "chapterNumber",
                "contentVersion",
                "recordCount",
                "canonicalReferenceRange",
                "createdAt",
                "packageStatus",
                "sourceRegistryReferences",
                "editorialApprovalManifestChecksum",
                "packageFormatVersion",
                "checksumAlgorithm",
                "packageChecksum",
                "fileChecksums",
                "allowNullTransliteration");
    }

    private void validateProvenanceShape(JsonNode provenance, List<String> errors) {
        requireObject(provenance, "provenance", errors);
        requireFields(
                provenance,
                "provenance",
                errors,
                "packageId",
                "sourceIds",
                "sourceRoles",
                "sourceChecksums",
                "licenses",
                "retrievalMetadata",
                "editorialReviewerIds",
                "secondReviewerIds",
                "approvalDates",
                "normalizationPolicyVersion",
                "comparisonEngineVersion",
                "packageBuilderVersion",
                "knownCaveats",
                "sourceSelectionRationale");
        JsonNode approvalDates = provenance.get("approvalDates");
        if (approvalDates != null && approvalDates.isArray()) {
            for (JsonNode date : approvalDates) {
                if (!date.isTextual()
                        || !APPROVAL_DATE_PATTERN.matcher(date.asText()).matches()) {
                    errors.add("provenance schema: approvalDates pattern mismatch");
                }
            }
        }
    }

    private void validateVerseShape(JsonNode row, int index, List<String> errors) {
        requireObject(row, "verses.jsonl[" + index + "]", errors);
        requireFields(
                row,
                "verses.jsonl[" + index + "]",
                errors,
                "chapterNumber",
                "verseNumber",
                "canonicalReference",
                "sanskritText",
                "transliteration",
                "contentVersion",
                "sourceIds",
                "sourceChecksums",
                "editorialDecisionId",
                "editorialApprovalChecksum");
        String ref = text(row, "canonicalReference");
        if (ref != null && !REF_PATTERN.matcher(ref).matches()) {
            errors.add("verses.jsonl[" + index + "] schema: canonicalReference pattern mismatch");
        }
    }

    private static boolean isEditorialError(String error) {
        return error.contains("unresolved source")
                || error.contains("APPROVED package")
                || error.contains("editorial evidence")
                || error.contains("missing reviewer")
                || error.contains("importable");
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
                }
            }
        } catch (IOException ex) {
            errors.add("failed to parse package files");
        }
        return names;
    }

    private List<JsonNode> readJsonl(byte[] bytes) throws IOException {
        String text = new String(bytes, StandardCharsets.UTF_8);
        List<JsonNode> rows = new ArrayList<>();
        int lineNo = 0;
        for (String line : text.split("\\R", -1)) {
            lineNo++;
            if (line.isBlank()) {
                continue;
            }
            try {
                rows.add(objectMapper.readTree(line));
            } catch (IOException ex) {
                throw new IOException("verses.jsonl line " + lineNo + " is not valid JSON", ex);
            }
        }
        return rows;
    }

    private static Map<String, String> parseSha256Sums(String text) {
        Map<String, String> mapping = new HashMap<>();
        int lineNo = 0;
        for (String line : text.split("\\R")) {
            lineNo++;
            if (line.isBlank() || line.stripLeading().startsWith("#")) {
                continue;
            }
            String[] parts = line.trim().split("\\s+", 2);
            if (parts.length != 2) {
                throw new IllegalArgumentException(
                        "SHA256SUMS line " + lineNo + ": expected '<hash>  <filename>'");
            }
            String digest = parts[0].trim().toLowerCase(Locale.ROOT);
            String name = parts[1].trim();
            if (!SHA256_PATTERN.matcher(digest).matches()) {
                throw new IllegalArgumentException(
                        "SHA256SUMS line " + lineNo + ": invalid sha256 digest");
            }
            if (mapping.containsKey(name)) {
                throw new IllegalArgumentException("SHA256SUMS duplicate filename '" + name + "'");
            }
            mapping.put(name, digest);
        }
        return mapping;
    }

    private static String sha256(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data));
        } catch (NoSuchAlgorithmException ex) {
            throw new IllegalStateException("SHA-256 not available", ex);
        }
    }

    private static byte[] concat(byte[] left, byte[] right) {
        byte[] out = new byte[left.length + right.length];
        System.arraycopy(left, 0, out, 0, left.length);
        System.arraycopy(right, 0, out, left.length, right.length);
        return out;
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

    private static boolean booleanValue(JsonNode node, String field, boolean defaultValue) {
        if (node == null || !node.has(field) || !node.get(field).isBoolean()) {
            return defaultValue;
        }
        return node.get(field).asBoolean();
    }

    private static boolean isEmptyArray(JsonNode node) {
        return node == null || !node.isArray() || node.isEmpty();
    }

    private static void requireObject(JsonNode node, String label, List<String> errors) {
        if (node == null || !node.isObject()) {
            errors.add(label + " schema: expected object");
        }
    }

    private static void requireFields(JsonNode node, String label, List<String> errors, String... fields) {
        if (node == null || !node.isObject()) {
            return;
        }
        for (String field : fields) {
            if (!node.has(field)) {
                errors.add(label + " schema: missing required field " + field);
            }
        }
    }

    private static void rejectAdditional(
            JsonNode node, String label, List<String> errors, String... allowed) {
        if (node == null || !node.isObject()) {
            return;
        }
        Set<String> allow = Set.of(allowed);
        Iterator<String> names = node.fieldNames();
        while (names.hasNext()) {
            String name = names.next();
            if (!allow.contains(name)) {
                errors.add(label + " schema: unexpected field " + name);
            }
        }
    }
}
