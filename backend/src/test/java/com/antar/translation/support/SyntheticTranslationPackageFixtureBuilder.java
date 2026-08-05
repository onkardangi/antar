package com.antar.translation.support;

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
import java.util.Map;
import java.util.TreeMap;

/**
 * Builds synthetic Translation Package Format v1 directories for tests.
 */
public final class SyntheticTranslationPackageFixtureBuilder {

    public static final String FIXTURE_SOURCE_ID = "fixture-antar-translation-v1";
    public static final String FIXTURE_SOURCE_CHECKSUM =
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    public static final String APPROVAL_CHECKSUM =
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";

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
                parent, packageId, chapterNumber, verseCount, contentVersion, "APPROVED", textPrefix);
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
                parent, packageId, chapterNumber, verseCount, contentVersion, "DRAFT", textPrefix);
    }

    public Path writePackage(
            Path parent,
            String packageId,
            int chapterNumber,
            int verseCount,
            long contentVersion,
            String packageStatus,
            String textPrefix)
            throws IOException {
        Path dir = parent.resolve(packageId);
        Files.createDirectories(dir);

        StringBuilder jsonl = new StringBuilder();
        for (int vn = 1; vn <= verseCount; vn++) {
            ObjectNode row = objectMapper.createObjectNode();
            row.put("chapterNumber", chapterNumber);
            row.put("verseNumber", vn);
            row.put("canonicalReference", chapterNumber + "." + vn);
            row.put("translationText", textPrefix + vn);
            row.put("contentVersion", contentVersion);
            ArrayNode sourceIds = row.putArray("sourceIds");
            sourceIds.add(FIXTURE_SOURCE_ID);
            ObjectNode checksums = row.putObject("sourceChecksums");
            checksums.put(FIXTURE_SOURCE_ID, FIXTURE_SOURCE_CHECKSUM);
            row.put("editorialDecisionId", "fixture-translation-decision-" + chapterNumber + "." + vn);
            row.put("editorialApprovalChecksum", hexPad(vn));
            jsonl.append(objectMapper.writeValueAsString(row)).append('\n');
        }
        byte[] translationsBytes = jsonl.toString().getBytes(StandardCharsets.UTF_8);

        Map<String, Object> provenance = new TreeMap<>();
        provenance.put("packageId", packageId);
        provenance.put("sourceIds", List.of(FIXTURE_SOURCE_ID));
        provenance.put("sourceRoles", Map.of(FIXTURE_SOURCE_ID, "FIXTURE"));
        provenance.put("sourceChecksums", Map.of(FIXTURE_SOURCE_ID, FIXTURE_SOURCE_CHECKSUM));
        provenance.put(
                "licenses",
                Map.of(FIXTURE_SOURCE_ID, Map.of("licenseDisplayed", "CC0 fixture", "licenseCatalogId", "cc0-1.0")));
        provenance.put(
                "retrievalMetadata",
                Map.of("sourceRegistryPath", "fixture", "editorialApprovalManifestPath", "fixture"));
        provenance.put("editorialReviewerIds", List.of("fixture-reviewer-a"));
        provenance.put("secondReviewerIds", List.of("fixture-reviewer-b"));
        provenance.put("approvalDates", List.of("2026-08-04"));
        provenance.put("normalizationPolicyVersion", 1);
        provenance.put("comparisonEngineVersion", 1);
        provenance.put("packageBuilderVersion", 1);
        provenance.put("knownCaveats", List.of("Synthetic Translation fixture only."));
        provenance.put("sourceSelectionRationale", "Synthetic Translation foundation fixture only.");
        byte[] provenanceBytes = (objectMapper.writerWithDefaultPrettyPrinter()
                        .writeValueAsString(provenance)
                        + "\n")
                .getBytes(StandardCharsets.UTF_8);

        String packageChecksum = sha256(concat(translationsBytes, provenanceBytes));
        Map<String, Object> manifest = new TreeMap<>();
        manifest.put("packageId", packageId);
        manifest.put("scriptureId", "bhagavad-gita");
        manifest.put("chapterNumber", chapterNumber);
        manifest.put("language", "en");
        manifest.put("provider", "FIXTURE_PROVIDER");
        manifest.put("sourceName", "Antar Fixture Translation");
        manifest.put("licenseType", "CC0");
        manifest.put("licenseReference", "CC0 fixture");
        manifest.put("contentVersion", contentVersion);
        manifest.put("recordCount", verseCount);
        manifest.put(
                "canonicalReferenceRange",
                Map.of(
                        "from",
                        chapterNumber + ".1",
                        "to",
                        chapterNumber + "." + verseCount,
                        "expectedCount",
                        verseCount));
        manifest.put("createdAt", "2026-08-04T00:00:00Z");
        manifest.put("packageStatus", packageStatus);
        manifest.put("sourceRegistryReferences", List.of(FIXTURE_SOURCE_ID));
        manifest.put("editorialApprovalManifestChecksum", APPROVAL_CHECKSUM);
        manifest.put("packageFormatVersion", 1);
        manifest.put("checksumAlgorithm", "SHA-256");
        manifest.put("packageChecksum", packageChecksum);
        manifest.put(
                "fileChecksums",
                Map.of(
                        "translations.jsonl",
                        sha256(translationsBytes),
                        "provenance.json",
                        sha256(provenanceBytes)));

        byte[] manifestBytes = (objectMapper.writerWithDefaultPrettyPrinter()
                        .writeValueAsString(manifest)
                        + "\n")
                .getBytes(StandardCharsets.UTF_8);

        Files.write(dir.resolve("translations.jsonl"), translationsBytes);
        Files.write(dir.resolve("provenance.json"), provenanceBytes);
        Files.write(dir.resolve("manifest.json"), manifestBytes);
        String sums = sha256(manifestBytes) + "  manifest.json\n"
                + sha256(provenanceBytes) + "  provenance.json\n"
                + sha256(translationsBytes) + "  translations.jsonl\n";
        Files.writeString(dir.resolve("SHA256SUMS"), sums, StandardCharsets.UTF_8);
        return dir;
    }

    public void corruptChecksums(Path packageDir) throws IOException {
        Path sums = packageDir.resolve("SHA256SUMS");
        Files.writeString(
                sums,
                "0000000000000000000000000000000000000000000000000000000000000000  manifest.json\n"
                        + "0000000000000000000000000000000000000000000000000000000000000000  provenance.json\n"
                        + "0000000000000000000000000000000000000000000000000000000000000000  translations.jsonl\n",
                StandardCharsets.UTF_8);
    }

    /** Rewrites package checksums after intentional record/manifest mutations for parity fixtures. */
    public Path recomputeChecksums(Path packageDir) throws IOException {
        byte[] translationsBytes = Files.readAllBytes(packageDir.resolve("translations.jsonl"));
        byte[] provenanceBytes = Files.readAllBytes(packageDir.resolve("provenance.json"));
        String translationsDigest = sha256(translationsBytes);
        String provenanceDigest = sha256(provenanceBytes);
        String packageChecksum = sha256(concat(translationsBytes, provenanceBytes));

        ObjectNode manifest =
                (ObjectNode) objectMapper.readTree(Files.readAllBytes(packageDir.resolve("manifest.json")));
        manifest.put("packageChecksum", packageChecksum);
        ObjectNode fileChecksums = manifest.with("fileChecksums");
        fileChecksums.put("translations.jsonl", translationsDigest);
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
                        + translationsDigest
                        + "  translations.jsonl\n",
                StandardCharsets.UTF_8);
        return packageDir;
    }

    public Path blankTranslationTextForFirstVerse(Path packageDir) throws IOException {
        java.util.List<String> lines =
                Files.readAllLines(packageDir.resolve("translations.jsonl"), StandardCharsets.UTF_8);
        ObjectNode first = (ObjectNode) objectMapper.readTree(lines.getFirst());
        first.put("translationText", "   ");
        lines.set(0, objectMapper.writeValueAsString(first));
        Files.writeString(
                packageDir.resolve("translations.jsonl"),
                String.join("\n", lines) + "\n",
                StandardCharsets.UTF_8);
        return recomputeChecksums(packageDir);
    }

    public Path badCanonicalReferenceForFirstVerse(Path packageDir) throws IOException {
        java.util.List<String> lines =
                Files.readAllLines(packageDir.resolve("translations.jsonl"), StandardCharsets.UTF_8);
        ObjectNode first = (ObjectNode) objectMapper.readTree(lines.getFirst());
        first.put("canonicalReference", "bad-ref");
        lines.set(0, objectMapper.writeValueAsString(first));
        Files.writeString(
                packageDir.resolve("translations.jsonl"),
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

    private static String hexPad(int vn) {
        return String.format("%064x", vn);
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
            throw new IllegalStateException(ex);
        }
    }
}
