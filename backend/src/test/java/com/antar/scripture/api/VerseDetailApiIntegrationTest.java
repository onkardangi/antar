package com.antar.scripture.api;

import static org.hamcrest.Matchers.nullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.util.UUID;
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
class VerseDetailApiIntegrationTest extends AbstractIntegrationTest {

    private static final String CHAPTER_1_ID = "018f0000-0000-7000-8000-000000000001";
    private static final String SANSKRIT_SAMPLE = "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।";

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void getVerseReturnsPublishedVerseWithSanskrit() throws Exception {
        UUID verseId = verseIdForChapterOne(1);
        jdbcTemplate.update(
                "UPDATE scripture.verses SET sanskrit_text = ?, content_version = 3 WHERE id = ?",
                SANSKRIT_SAMPLE,
                verseId);

        try {
            mockMvc.perform(get("/api/v1/scripture/verses/{verseId}", verseId))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").value(verseId.toString()))
                    .andExpect(jsonPath("$.chapterId").value(CHAPTER_1_ID))
                    .andExpect(jsonPath("$.chapterNumber").value(1))
                    .andExpect(jsonPath("$.verseNumber").value(1))
                    .andExpect(jsonPath("$.canonicalReference").value("1.1"))
                    .andExpect(jsonPath("$.sanskritText").value(SANSKRIT_SAMPLE))
                    .andExpect(jsonPath("$.contentVersion").value(3));
        } finally {
            clearSanskrit(verseId);
        }
    }

    @Test
    void getVerseExposesOnlyApprovedDetailFields() throws Exception {
        UUID verseId = verseIdForChapterOne(2);
        jdbcTemplate.update(
                "UPDATE scripture.verses SET sanskrit_text = ?, content_version = 2 WHERE id = ?",
                SANSKRIT_SAMPLE,
                verseId);

        try {
            mockMvc.perform(get("/api/v1/scripture/verses/{verseId}", verseId))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").exists())
                    .andExpect(jsonPath("$.chapterId").exists())
                    .andExpect(jsonPath("$.chapterNumber").exists())
                    .andExpect(jsonPath("$.verseNumber").exists())
                    .andExpect(jsonPath("$.canonicalReference").exists())
                    .andExpect(jsonPath("$.sanskritText").exists())
                    .andExpect(jsonPath("$.contentVersion").exists())
                    .andExpect(jsonPath("$.publicationStatus").doesNotExist())
                    .andExpect(jsonPath("$.sourcePackageId").doesNotExist())
                    .andExpect(jsonPath("$.sourcePackageChecksum").doesNotExist())
                    .andExpect(jsonPath("$.createdAt").doesNotExist())
                    .andExpect(jsonPath("$.updatedAt").doesNotExist())
                    .andExpect(jsonPath("$.previewText").doesNotExist())
                    .andExpect(jsonPath("$.translation").doesNotExist())
                    .andExpect(jsonPath("$.commentary").doesNotExist())
                    .andExpect(jsonPath("$.transliterations").doesNotExist())
                    .andExpect(jsonPath("$.navigation").doesNotExist());
        } finally {
            clearSanskrit(verseId);
        }
    }

    @Test
    void getVerseReturnsNotFoundWhenSanskritIsMissing() throws Exception {
        UUID verseId = verseIdForChapterOne(3);

        mockMvc.perform(get("/api/v1/scripture/verses/{verseId}", verseId))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.type").value("https://antar.app/problems/resource-not-found"))
                .andExpect(jsonPath("$.title").value("Resource not found"))
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"))
                .andExpect(jsonPath("$.detail").exists())
                .andExpect(jsonPath("$.instance")
                        .value("/api/v1/scripture/verses/" + verseId))
                .andExpect(jsonPath("$.requestId").exists())
                .andExpect(header().exists("X-Request-Id"));
    }

    @Test
    void getVerseReturnsNotFoundForUnknownVerse() throws Exception {
        mockMvc.perform(get(
                        "/api/v1/scripture/verses/{verseId}",
                        "018f0000-0000-7000-8000-00000000dead"))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
    }

    @Test
    void getVerseReturnsNotFoundForUnpublishedVerse() throws Exception {
        UUID verseId = verseIdForChapterOne(4);
        jdbcTemplate.update(
                "UPDATE scripture.verses SET publication_status = 'DRAFT', sanskrit_text = ? WHERE id = ?",
                SANSKRIT_SAMPLE,
                verseId);

        try {
            mockMvc.perform(get("/api/v1/scripture/verses/{verseId}", verseId))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.verses SET publication_status = 'PUBLISHED', sanskrit_text = NULL"
                            + " WHERE id = ?",
                    verseId);
        }
    }

    @Test
    void getVerseForMalformedVerseIdReturnsValidationError() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/verses/{verseId}", "not-a-uuid"))
                .andExpect(status().isBadRequest())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors[0].field").value("verseId"))
                .andExpect(jsonPath("$.errors[0].code").value("INVALID_VERSE_ID"))
                .andExpect(jsonPath("$.errors").value(org.hamcrest.Matchers.not(nullValue())));
    }

    private UUID verseIdForChapterOne(int verseNumber) {
        return jdbcTemplate.queryForObject(
                "SELECT id FROM scripture.verses WHERE chapter_id = ?::uuid AND verse_number = ?",
                UUID.class,
                CHAPTER_1_ID,
                verseNumber);
    }

    private void clearSanskrit(UUID verseId) {
        jdbcTemplate.update(
                "UPDATE scripture.verses SET sanskrit_text = NULL, content_version = 1 WHERE id = ?",
                verseId);
    }
}
