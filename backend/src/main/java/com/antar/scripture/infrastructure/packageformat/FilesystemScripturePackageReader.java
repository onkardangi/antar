package com.antar.scripture.infrastructure.packageformat;

import com.antar.scripture.application.port.ResolvedScripturePackage;
import com.antar.scripture.application.port.ResolvedScripturePackage.CanonicalReferenceRange;
import com.antar.scripture.application.port.ResolvedScripturePackage.PackageProvenance;
import com.antar.scripture.application.port.ResolvedScripturePackage.PackageVerseRecord;
import com.antar.scripture.application.port.ScripturePackageReadException;
import com.antar.scripture.application.port.ScripturePackageReader;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;

@Component
public class FilesystemScripturePackageReader implements ScripturePackageReader {

    private final ObjectMapper objectMapper;

    public FilesystemScripturePackageReader() {
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public ResolvedScripturePackage read(Path packageDirectory) {
        Path dir = packageDirectory.toAbsolutePath().normalize();
        try {
            byte[] manifestBytes = Files.readAllBytes(dir.resolve("manifest.json"));
            byte[] versesBytes = Files.readAllBytes(dir.resolve("verses.jsonl"));
            byte[] provenanceBytes = Files.readAllBytes(dir.resolve("provenance.json"));
            JsonNode manifest = objectMapper.readTree(manifestBytes);
            JsonNode provenance = objectMapper.readTree(provenanceBytes);
            List<PackageVerseRecord> verses = new ArrayList<>();
            for (String line : new String(versesBytes, StandardCharsets.UTF_8).split("\\R")) {
                if (line.isBlank()) {
                    continue;
                }
                verses.add(toVerse(objectMapper.readTree(line)));
            }
            JsonNode range = manifest.get("canonicalReferenceRange");
            List<String> sourceRefs = new ArrayList<>();
            for (JsonNode ref : manifest.get("sourceRegistryReferences")) {
                sourceRefs.add(ref.asText());
            }
            return new ResolvedScripturePackage(
                    manifest.get("packageId").asText(),
                    manifest.get("scriptureId").asText(),
                    manifest.get("chapterNumber").asInt(),
                    manifest.get("contentVersion").asLong(),
                    manifest.get("recordCount").asInt(),
                    manifest.get("packageStatus").asText(),
                    manifest.get("packageFormatVersion").asInt(),
                    manifest.get("packageChecksum").asText(),
                    sha256(manifestBytes),
                    sha256(provenanceBytes),
                    sha256(versesBytes),
                    sourceRefs,
                    manifest.get("editorialApprovalManifestChecksum").asText(),
                    manifest.get("allowNullTransliteration").asBoolean(),
                    new CanonicalReferenceRange(
                            range.get("from").asText(),
                            range.get("to").asText(),
                            range.get("expectedCount").asInt()),
                    verses,
                    toProvenance(provenance));
        } catch (IOException ex) {
            throw new ScripturePackageReadException(ex);
        } catch (RuntimeException ex) {
            throw new ScripturePackageReadException(ex);
        }
    }

    private static PackageVerseRecord toVerse(JsonNode row) {
        List<String> sourceIds = new ArrayList<>();
        for (JsonNode sid : row.get("sourceIds")) {
            sourceIds.add(sid.asText());
        }
        Map<String, String> checksums = new LinkedHashMap<>();
        row.get("sourceChecksums")
                .fields()
                .forEachRemaining(e -> checksums.put(e.getKey(), e.getValue().asText()));
        String transliteration =
                row.has("transliteration") && !row.get("transliteration").isNull()
                        ? row.get("transliteration").asText()
                        : null;
        return new PackageVerseRecord(
                row.get("chapterNumber").asInt(),
                row.get("verseNumber").asInt(),
                row.get("canonicalReference").asText(),
                row.get("sanskritText").asText(),
                transliteration,
                row.get("contentVersion").asLong(),
                sourceIds,
                checksums,
                row.get("editorialDecisionId").asText(),
                row.get("editorialApprovalChecksum").asText());
    }

    private static PackageProvenance toProvenance(JsonNode provenance) {
        List<String> sourceIds = new ArrayList<>();
        for (JsonNode sid : provenance.get("sourceIds")) {
            sourceIds.add(sid.asText());
        }
        Map<String, String> roles = new LinkedHashMap<>();
        provenance
                .get("sourceRoles")
                .fields()
                .forEachRemaining(e -> roles.put(e.getKey(), e.getValue().asText()));
        Map<String, String> checksums = new LinkedHashMap<>();
        provenance
                .get("sourceChecksums")
                .fields()
                .forEachRemaining(e -> checksums.put(e.getKey(), e.getValue().asText()));
        List<String> reviewers = new ArrayList<>();
        for (JsonNode id : provenance.get("editorialReviewerIds")) {
            reviewers.add(id.asText());
        }
        List<String> second = new ArrayList<>();
        for (JsonNode id : provenance.get("secondReviewerIds")) {
            second.add(id.asText());
        }
        List<String> dates = new ArrayList<>();
        for (JsonNode id : provenance.get("approvalDates")) {
            dates.add(id.asText());
        }
        return new PackageProvenance(
                provenance.get("packageId").asText(),
                sourceIds,
                roles,
                checksums,
                reviewers,
                second,
                dates);
    }

    private static String sha256(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data));
        } catch (NoSuchAlgorithmException ex) {
            throw new IllegalStateException("SHA-256 not available", ex);
        }
    }
}
