package com.antar.scripture.support;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

/**
 * Builds synthetic Package Format v1 directories for tests. Uses non-scriptural fixture text only.
 */
public final class SyntheticPackageFixtureBuilder {

    public static final String FIXTURE_SOURCE_ID = "fixture-antar-importer-v1";
    public static final String FIXTURE_SOURCE_CHECKSUM =
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
    public static final String APPROVAL_CHECKSUM =
            "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc";

    private final ObjectMapper objectMapper =
            new ObjectMapper().configure(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS, true);

    public Path writeApprovedChapterPackage(
            Path parent,
            String packageId,
            int chapterNumber,
            int verseCount,
            long contentVersion,
            String textPrefix)
            throws IOException {
        return writePackage(
                parent,
                packageId,
                chapterNumber,
                verseCount,
                contentVersion,
                "APPROVED",
                textPrefix,
                true,
                null);
    }

    public Path writeDraftChapterPackage(
            Path parent,
            String packageId,
            int chapterNumber,
            int verseCount,
            long contentVersion,
            String textPrefix)
            throws IOException {
        return writePackage(
                parent,
                packageId,
                chapterNumber,
                verseCount,
                contentVersion,
                "DRAFT",
                textPrefix,
                true,
                null);
    }

    public Path writeApprovedWithTransliteration(
            Path parent, String packageId, int chapterNumber, int verseCount, long contentVersion)
            throws IOException {
        return writePackage(
                parent,
                packageId,
                chapterNumber,
                verseCount,
                contentVersion,
                "APPROVED",
                "FIXTURE_NON_SCRIPTURAL_VERSE_",
                false,
                "fixture-transliteration");
    }

    public Path writePackage(
            Path parent,
            String packageId,
            int chapterNumber,
            int verseCount,
            long contentVersion,
            String packageStatus,
            String textPrefix,
            boolean allowNullTransliteration,
            String transliteration)
            throws IOException {
        Path dir = parent.resolve(packageId);
        Files.createDirectories(dir);

        StringBuilder versesJsonl = new StringBuilder();
        for (int vn = 1; vn <= verseCount; vn++) {
            ObjectNode row = objectMapper.createObjectNode();
            row.put("chapterNumber", chapterNumber);
            row.put("verseNumber", vn);
            row.put("canonicalReference", chapterNumber + "." + vn);
            row.put("sanskritText", textPrefix + vn);
            if (transliteration == null) {
                row.putNull("transliteration");
            } else {
                row.put("transliteration", transliteration + "_" + vn);
            }
            row.put("contentVersion", contentVersion);
            ArrayNode sourceIds = row.putArray("sourceIds");
            sourceIds.add(FIXTURE_SOURCE_ID);
            ObjectNode checksums = row.putObject("sourceChecksums");
            checksums.put(FIXTURE_SOURCE_ID, FIXTURE_SOURCE_CHECKSUM);
            row.put("editorialDecisionId", "fixture-decision-" + chapterNumber + "." + vn);
            row.put("editorialApprovalChecksum", hexPad(vn));
            versesJsonl.append(objectMapper.writeValueAsString(row)).append('\n');
        }
        byte[] versesBytes = versesJsonl.toString().getBytes(StandardCharsets.UTF_8);

        Map<String, Object> provenance = new TreeMap<>();
        provenance.put("packageId", packageId);
        provenance.put("sourceIds", List.of(FIXTURE_SOURCE_ID));
        provenance.put("sourceRoles", Map.of(FIXTURE_SOURCE_ID, "FIXTURE"));
        provenance.put("sourceChecksums", Map.of(FIXTURE_SOURCE_ID, FIXTURE_SOURCE_CHECKSUM));
        Map<String, Object> license = new TreeMap<>();
        license.put("licenseDisplayed", "CC0 fixture");
        license.put("licenseCatalogId", null);
        provenance.put("licenses", Map.of(FIXTURE_SOURCE_ID, license));
        provenance.put(
                "retrievalMetadata",
                Map.of(
                        "sourceRegistryPath",
                        "test-sources.json",
                        "editorialApprovalManifestPath",
                        "test-approval.json"));
        provenance.put("editorialReviewerIds", List.of("fixture-reviewer-a"));
        provenance.put("secondReviewerIds", List.of("fixture-reviewer-b"));
        provenance.put("approvalDates", List.of("2026-08-04"));
        provenance.put("normalizationPolicyVersion", 1);
        provenance.put("comparisonEngineVersion", 1);
        provenance.put("packageBuilderVersion", 1);
        provenance.put(
                "knownCaveats", List.of("Synthetic non-scriptural fixture for importer tests only."));
        provenance.put(
                "sourceSelectionRationale",
                "Synthetic fixture package for Antar importer tests; never Scripture.");

        byte[] provenanceBytes =
                (objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(provenance) + "\n")
                        .getBytes(StandardCharsets.UTF_8);

        String versesDigest = sha256(versesBytes);
        String provenanceDigest = sha256(provenanceBytes);
        String packageChecksum = sha256(concat(versesBytes, provenanceBytes));

        Map<String, Object> manifest = new TreeMap<>();
        manifest.put("allowNullTransliteration", allowNullTransliteration);
        manifest.put(
                "canonicalReferenceRange",
                Map.of(
                        "expectedCount",
                        verseCount,
                        "from",
                        chapterNumber + ".1",
                        "to",
                        chapterNumber + "." + verseCount));
        manifest.put("chapterNumber", chapterNumber);
        manifest.put("checksumAlgorithm", "SHA-256");
        manifest.put("contentVersion", contentVersion);
        manifest.put("createdAt", "2026-08-04T00:00:00Z");
        manifest.put("editorialApprovalManifestChecksum", APPROVAL_CHECKSUM);
        manifest.put(
                "fileChecksums",
                Map.of("provenance.json", provenanceDigest, "verses.jsonl", versesDigest));
        manifest.put("packageChecksum", packageChecksum);
        manifest.put("packageFormatVersion", 1);
        manifest.put("packageId", packageId);
        manifest.put("packageStatus", packageStatus);
        manifest.put("recordCount", verseCount);
        manifest.put("scriptureId", "bhagavad-gita");
        manifest.put("sourceRegistryReferences", List.of(FIXTURE_SOURCE_ID));

        byte[] manifestBytes =
                (objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(manifest) + "\n")
                        .getBytes(StandardCharsets.UTF_8);
        String manifestDigest = sha256(manifestBytes);

        Files.write(dir.resolve("verses.jsonl"), versesBytes);
        Files.write(dir.resolve("provenance.json"), provenanceBytes);
        Files.write(dir.resolve("manifest.json"), manifestBytes);

        String shaFile = manifestDigest
                + "  manifest.json\n"
                + provenanceDigest
                + "  provenance.json\n"
                + versesDigest
                + "  verses.jsonl\n";
        Files.writeString(dir.resolve("SHA256SUMS"), shaFile, StandardCharsets.UTF_8);
        return dir;
    }

    public Path writeSourcesRegistry(Path file) throws IOException {
        Map<String, Object> root = new TreeMap<>();
        root.put(
                "sources",
                List.of(Map.of("id", FIXTURE_SOURCE_ID, "status", "APPROVED_FOR_IMPORT")));
        Files.writeString(
                file,
                objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(root) + "\n",
                StandardCharsets.UTF_8);
        return file;
    }

    public Path corruptChecksums(Path packageDir) throws IOException {
        Files.writeString(
                packageDir.resolve("SHA256SUMS"),
                "0000000000000000000000000000000000000000000000000000000000000000  manifest.json\n"
                        + "0000000000000000000000000000000000000000000000000000000000000000  provenance.json\n"
                        + "0000000000000000000000000000000000000000000000000000000000000000  verses.jsonl\n",
                StandardCharsets.UTF_8);
        return packageDir;
    }

    /** Rewrites package checksums after intentional verse/manifest mutations for parity fixtures. */
    public Path recomputeChecksums(Path packageDir) throws IOException {
        byte[] versesBytes = Files.readAllBytes(packageDir.resolve("verses.jsonl"));
        byte[] provenanceBytes = Files.readAllBytes(packageDir.resolve("provenance.json"));
        String versesDigest = sha256(versesBytes);
        String provenanceDigest = sha256(provenanceBytes);
        String packageChecksum = sha256(concat(versesBytes, provenanceBytes));

        ObjectNode manifest =
                (ObjectNode) objectMapper.readTree(Files.readAllBytes(packageDir.resolve("manifest.json")));
        manifest.put("packageChecksum", packageChecksum);
        ObjectNode fileChecksums = manifest.with("fileChecksums");
        fileChecksums.put("verses.jsonl", versesDigest);
        fileChecksums.put("provenance.json", provenanceDigest);
        byte[] manifestBytes =
                (objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(manifest) + "\n")
                        .getBytes(StandardCharsets.UTF_8);
        String manifestDigest = sha256(manifestBytes);
        Files.write(packageDir.resolve("manifest.json"), manifestBytes);
        Files.writeString(
                packageDir.resolve("SHA256SUMS"),
                manifestDigest
                        + "  manifest.json\n"
                        + provenanceDigest
                        + "  provenance.json\n"
                        + versesDigest
                        + "  verses.jsonl\n",
                StandardCharsets.UTF_8);
        return packageDir;
    }

    public Path omitSanskritForFirstVerse(Path packageDir) throws IOException {
        List<String> lines = Files.readAllLines(packageDir.resolve("verses.jsonl"), StandardCharsets.UTF_8);
        ObjectNode first = (ObjectNode) objectMapper.readTree(lines.getFirst());
        first.putNull("sanskritText");
        lines.set(0, objectMapper.writeValueAsString(first));
        Files.writeString(
                packageDir.resolve("verses.jsonl"),
                String.join("\n", lines) + "\n",
                StandardCharsets.UTF_8);
        return recomputeChecksums(packageDir);
    }

    public Path badCanonicalReferenceForFirstVerse(Path packageDir) throws IOException {
        List<String> lines = Files.readAllLines(packageDir.resolve("verses.jsonl"), StandardCharsets.UTF_8);
        ObjectNode first = (ObjectNode) objectMapper.readTree(lines.getFirst());
        first.put("canonicalReference", "bad-ref");
        lines.set(0, objectMapper.writeValueAsString(first));
        Files.writeString(
                packageDir.resolve("verses.jsonl"),
                String.join("\n", lines) + "\n",
                StandardCharsets.UTF_8);
        return recomputeChecksums(packageDir);
    }

    public Path wrongRecordCountInManifest(Path packageDir) throws IOException {
        ObjectNode manifest =
                (ObjectNode) objectMapper.readTree(Files.readAllBytes(packageDir.resolve("manifest.json")));
        manifest.put("recordCount", 999);
        Files.write(
                packageDir.resolve("manifest.json"),
                (objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(manifest) + "\n")
                        .getBytes(StandardCharsets.UTF_8));
        return recomputeChecksums(packageDir);
    }

    private static String hexPad(int value) {
        return String.format(Locale.ROOT, "%064x", value);
    }

    private static String sha256(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data));
        } catch (NoSuchAlgorithmException ex) {
            throw new IllegalStateException(ex);
        }
    }

    private static byte[] concat(byte[] left, byte[] right) {
        byte[] out = new byte[left.length + right.length];
        System.arraycopy(left, 0, out, 0, left.length);
        System.arraycopy(right, 0, out, left.length, right.length);
        return out;
    }
}
