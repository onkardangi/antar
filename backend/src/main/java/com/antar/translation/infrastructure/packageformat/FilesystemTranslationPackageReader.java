package com.antar.translation.infrastructure.packageformat;

import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.application.port.ResolvedTranslationPackage.CanonicalReferenceRange;
import com.antar.translation.application.port.ResolvedTranslationPackage.PackageTranslationRecord;
import com.antar.translation.application.port.TranslationPackageReadException;
import com.antar.translation.application.port.TranslationPackageReader;
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
import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class FilesystemTranslationPackageReader implements TranslationPackageReader {

    private final ObjectMapper objectMapper;

    public FilesystemTranslationPackageReader() {
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public ResolvedTranslationPackage read(Path packageDirectory) {
        Path dir = packageDirectory.toAbsolutePath().normalize();
        try {
            byte[] manifestBytes = Files.readAllBytes(dir.resolve("manifest.json"));
            byte[] translationsBytes = Files.readAllBytes(dir.resolve("translations.jsonl"));
            byte[] provenanceBytes = Files.readAllBytes(dir.resolve("provenance.json"));
            JsonNode manifest = objectMapper.readTree(manifestBytes);
            List<PackageTranslationRecord> translations = new ArrayList<>();
            for (String line : new String(translationsBytes, StandardCharsets.UTF_8).split("\\R")) {
                if (line.isBlank()) {
                    continue;
                }
                JsonNode row = objectMapper.readTree(line);
                translations.add(new PackageTranslationRecord(
                        row.get("canonicalReference").asText(),
                        row.get("chapterNumber").asInt(),
                        row.get("verseNumber").asInt(),
                        row.get("translationText").asText(),
                        row.get("contentVersion").asLong()));
            }
            JsonNode range = manifest.get("canonicalReferenceRange");
            List<String> sourceRefs = new ArrayList<>();
            for (JsonNode ref : manifest.get("sourceRegistryReferences")) {
                sourceRefs.add(ref.asText());
            }
            String licenseReference = manifest.has("licenseReference") && !manifest.get("licenseReference").isNull()
                    ? manifest.get("licenseReference").asText()
                    : null;
            return new ResolvedTranslationPackage(
                    manifest.get("packageId").asText(),
                    manifest.get("packageFormatVersion").asInt(),
                    manifest.get("scriptureId").asText(),
                    manifest.get("chapterNumber").asInt(),
                    manifest.get("language").asText(),
                    manifest.get("provider").asText(),
                    manifest.get("sourceName").asText(),
                    manifest.get("licenseType").asText(),
                    licenseReference,
                    manifest.get("contentVersion").asLong(),
                    manifest.get("packageStatus").asText(),
                    manifest.get("packageChecksum").asText(),
                    sha256(manifestBytes),
                    sha256(provenanceBytes),
                    sha256(translationsBytes),
                    sourceRefs,
                    manifest.get("recordCount").asInt(),
                    new CanonicalReferenceRange(
                            range.get("from").asText(),
                            range.get("to").asText(),
                            range.get("expectedCount").asInt()),
                    translations);
        } catch (IOException | RuntimeException ex) {
            throw new TranslationPackageReadException(ex);
        }
    }

    private static String sha256(byte[] data) {
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(data));
        } catch (NoSuchAlgorithmException ex) {
            throw new IllegalStateException("SHA-256 unavailable", ex);
        }
    }
}
