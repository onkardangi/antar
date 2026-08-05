package com.antar.translation.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@SkipInfrastructureTestsIfRequested
class TranslationApiIntegrationTest extends AbstractIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @AfterEach
    void tearDown() {
        jdbcTemplate.update("DELETE FROM translation.translations");
        jdbcTemplate.update("DELETE FROM translation.content_package_imports");
        jdbcTemplate.update("DELETE FROM translation.content_packages");
        jdbcTemplate.update("DELETE FROM translation.translation_sources");
    }

    @Test
    void getTranslationReturnsPublishedTranslation() throws Exception {
        UUID verseId = verseIdFor(1, 1);
        UUID sourceId = UUID.fromString("01910000-0000-7000-8000-000000000001");
        UUID translationId = UUID.fromString("01910000-0000-7000-8000-000000000011");
        insertSource(sourceId);
        insertTranslation(translationId, verseId, sourceId, "FIXTURE_TRANSLATION_VERSE_1", 1);

        mockMvc.perform(get("/api/v1/translations/verses/{verseId}", verseId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(translationId.toString()))
                .andExpect(jsonPath("$.verseId").value(verseId.toString()))
                .andExpect(jsonPath("$.language").value("en"))
                .andExpect(jsonPath("$.provider").value("FIXTURE_PROVIDER"))
                .andExpect(jsonPath("$.translationText").value("FIXTURE_TRANSLATION_VERSE_1"))
                .andExpect(jsonPath("$.contentVersion").value(1))
                .andExpect(jsonPath("$.sanskritText").doesNotExist())
                .andExpect(jsonPath("$.commentary").doesNotExist());
    }

    @Test
    void getTranslationReturnsNotFoundWhenMissing() throws Exception {
        UUID verseId = verseIdFor(1, 2);

        mockMvc.perform(get("/api/v1/translations/verses/{verseId}", verseId))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.type").value("https://antar.app/problems/resource-not-found"))
                .andExpect(jsonPath("$.title").value("Resource not found"))
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"))
                .andExpect(jsonPath("$.detail").exists())
                .andExpect(jsonPath("$.instance").exists());
    }

    @Test
    void getTranslationReturnsNotFoundWhenUnpublished() throws Exception {
        UUID verseId = verseIdFor(1, 3);
        UUID sourceId = UUID.fromString("01910000-0000-7000-8000-000000000002");
        UUID translationId = UUID.fromString("01910000-0000-7000-8000-000000000012");
        insertSource(sourceId);
        insertTranslation(
                translationId, verseId, sourceId, "FIXTURE_TRANSLATION_DRAFT", 1, "DRAFT");

        mockMvc.perform(get("/api/v1/translations/verses/{verseId}", verseId))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"))
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.type").value("https://antar.app/problems/resource-not-found"));
    }

    @Test
    void getTranslationReturnsProviderAscendingWhenMultiplePublished() throws Exception {
        UUID verseId = verseIdFor(1, 1);
        UUID zebraSourceId = UUID.fromString("01910000-0000-7000-8000-000000000021");
        UUID alphaSourceId = UUID.fromString("01910000-0000-7000-8000-000000000022");
        UUID zebraTranslationId = UUID.fromString("01910000-0000-7000-8000-000000000031");
        UUID alphaTranslationId = UUID.fromString("01910000-0000-7000-8000-000000000032");

        insertSource(zebraSourceId, "ZEBRA_PROVIDER", "Zebra Fixture Translation");
        insertSource(alphaSourceId, "ALPHA_PROVIDER", "Alpha Fixture Translation");
        insertTranslation(
                zebraTranslationId,
                verseId,
                zebraSourceId,
                "ZEBRA_PROVIDER",
                "FIXTURE_TRANSLATION_ZEBRA",
                1,
                "PUBLISHED");
        insertTranslation(
                alphaTranslationId,
                verseId,
                alphaSourceId,
                "ALPHA_PROVIDER",
                "FIXTURE_TRANSLATION_ALPHA",
                1,
                "PUBLISHED");

        mockMvc.perform(get("/api/v1/translations/verses/{verseId}", verseId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(alphaTranslationId.toString()))
                .andExpect(jsonPath("$.provider").value("ALPHA_PROVIDER"))
                .andExpect(jsonPath("$.translationText").value("FIXTURE_TRANSLATION_ALPHA"));
    }

    @Test
    void getTranslationReturnsBadRequestForInvalidVerseId() throws Exception {
        mockMvc.perform(get("/api/v1/translations/verses/{verseId}", "not-a-uuid"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"));
    }

    private void insertSource(UUID sourceId) {
        insertSource(sourceId, "FIXTURE_PROVIDER", "Antar Fixture Translation");
    }

    private void insertSource(UUID sourceId, String provider, String name) {
        jdbcTemplate.update(
                """
                INSERT INTO translation.translation_sources (
                    id, provider, name, language_code, license_type, license_reference,
                    publication_status, created_at, updated_at
                ) VALUES (?, ?, ?, 'en', 'CC0', 'CC0 fixture',
                    'PUBLISHED', TIMESTAMPTZ '2026-08-04T00:00:00Z', TIMESTAMPTZ '2026-08-04T00:00:00Z')
                """,
                sourceId,
                provider,
                name);
    }

    private void insertTranslation(
            UUID translationId, UUID verseId, UUID sourceId, String text, long version) {
        insertTranslation(translationId, verseId, sourceId, "FIXTURE_PROVIDER", text, version, "PUBLISHED");
    }

    private void insertTranslation(
            UUID translationId,
            UUID verseId,
            UUID sourceId,
            String text,
            long version,
            String publicationStatus) {
        insertTranslation(
                translationId, verseId, sourceId, "FIXTURE_PROVIDER", text, version, publicationStatus);
    }

    private void insertTranslation(
            UUID translationId,
            UUID verseId,
            UUID sourceId,
            String provider,
            String text,
            long version,
            String publicationStatus) {
        jdbcTemplate.update(
                """
                INSERT INTO translation.translations (
                    id, verse_id, translation_source_id, language_code, provider, translation_text,
                    publication_status, content_version, created_at, updated_at
                ) VALUES (?, ?, ?, 'en', ?, ?, ?, ?,
                    TIMESTAMPTZ '2026-08-04T00:00:00Z', TIMESTAMPTZ '2026-08-04T00:00:00Z')
                """,
                translationId,
                verseId,
                sourceId,
                provider,
                text,
                publicationStatus,
                version);
    }

    private UUID verseIdFor(int chapter, int verse) {
        return jdbcTemplate.queryForObject(
                "SELECT id FROM scripture.verses WHERE canonical_reference = ?",
                UUID.class,
                chapter + "." + verse);
    }
}
