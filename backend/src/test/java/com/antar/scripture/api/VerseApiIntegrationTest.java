package com.antar.scripture.api;

import static org.hamcrest.Matchers.everyItem;
import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.notNullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.antar.scripture.application.verse.query.VerseQueryService;
import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@SkipInfrastructureTestsIfRequested
class VerseApiIntegrationTest extends AbstractIntegrationTest {

    private static final String CHAPTER_1_ID = "018f0000-0000-7000-8000-000000000001";
    private static final String CHAPTER_2_ID = "018f0000-0000-7000-8000-000000000002";

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void listChapterVersesReturnsPublishedVersesInCanonicalOrder() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_2_ID))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items", hasSize(72)))
                .andExpect(jsonPath("$.items[0].verseNumber").value(1))
                .andExpect(jsonPath("$.items[0].canonicalReference").value("2.1"))
                .andExpect(jsonPath("$.items[0].previewText")
                        .value(VerseQueryService.PLACEHOLDER_PREVIEW_TEXT))
                .andExpect(jsonPath("$.items[71].verseNumber").value(72))
                .andExpect(jsonPath("$.items[71].canonicalReference").value("2.72"));
    }

    @Test
    void listChapterVersesMatchesSeededChapterOneCount() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_1_ID))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items", hasSize(47)))
                .andExpect(jsonPath("$.items[0].id", notNullValue()))
                .andExpect(jsonPath("$.items[*].previewText")
                        .value(everyItem(is(VerseQueryService.PLACEHOLDER_PREVIEW_TEXT))));
    }

    @Test
    void listChapterVersesExposesOnlyApprovedResponseFields() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_1_ID))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items[0].id").exists())
                .andExpect(jsonPath("$.items[0].verseNumber").exists())
                .andExpect(jsonPath("$.items[0].canonicalReference").exists())
                .andExpect(jsonPath("$.items[0].previewText")
                        .value(VerseQueryService.PLACEHOLDER_PREVIEW_TEXT))
                .andExpect(jsonPath("$.items[0].publicationStatus").doesNotExist())
                .andExpect(jsonPath("$.items[0].contentVersion").doesNotExist())
                .andExpect(jsonPath("$.items[0].createdAt").doesNotExist())
                .andExpect(jsonPath("$.items[0].updatedAt").doesNotExist())
                .andExpect(jsonPath("$.items[0].sanskritText").doesNotExist())
                .andExpect(jsonPath("$.items[0].chapterId").doesNotExist());
    }

    @Test
    void listChapterVersesNeverExposesSanskritTextEvenWhenPresentInDatabase() throws Exception {
        jdbcTemplate.update(
                "UPDATE scripture.verses SET sanskrit_text = ? WHERE chapter_id = ?::uuid AND verse_number = 1",
                "कर्मण्येवाधिकारस्ते",
                CHAPTER_1_ID);

        try {
            mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_1_ID))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.items[0].verseNumber").value(1))
                    .andExpect(jsonPath("$.items[0].previewText")
                            .value(VerseQueryService.PLACEHOLDER_PREVIEW_TEXT))
                    .andExpect(jsonPath("$.items[0].sanskritText").doesNotExist())
                    .andExpect(jsonPath("$.items[0].sanskrit").doesNotExist());
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.verses SET sanskrit_text = NULL WHERE chapter_id = ?::uuid AND verse_number = 1",
                    CHAPTER_1_ID);
        }
    }

    @Test
    void listChapterVersesFiltersUnpublishedVerses() throws Exception {
        jdbcTemplate.update(
                "UPDATE scripture.verses SET publication_status = 'DRAFT' WHERE chapter_id = ?::uuid AND verse_number = 1",
                CHAPTER_1_ID);

        try {
            mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_1_ID))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.items", hasSize(46)))
                    .andExpect(jsonPath("$.items[0].verseNumber").value(2));
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.verses SET publication_status = 'PUBLISHED' WHERE chapter_id = ?::uuid AND verse_number = 1",
                    CHAPTER_1_ID);
        }
    }

    @Test
    void listChapterVersesReturnsContentNotPublishedWhenNoPublishedVersesRemain() throws Exception {
        jdbcTemplate.update(
                "UPDATE scripture.verses SET publication_status = 'DRAFT' WHERE chapter_id = ?::uuid",
                CHAPTER_1_ID);

        try {
            mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", CHAPTER_1_ID))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.code").value("CONTENT_NOT_PUBLISHED"));
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.verses SET publication_status = 'PUBLISHED' WHERE chapter_id = ?::uuid",
                    CHAPTER_1_ID);
        }
    }

    @Test
    void listChapterVersesForMissingChapterReturnsNotFound() throws Exception {
        mockMvc.perform(get(
                        "/api/v1/scripture/chapters/{chapterId}/verses",
                        "018f0000-0000-7000-8000-00000000dead"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
    }

    @Test
    void listChapterVersesForMalformedChapterIdReturnsValidationError() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}/verses", "not-a-uuid"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors[0].field").value("chapterId"))
                .andExpect(jsonPath("$.errors[0].code").value("INVALID_CHAPTER_ID"));
    }

    @Test
    void chapterDetailStillExposesShortIntentRatherThanThematicIntroduction() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}", CHAPTER_1_ID))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.chapterNumber").value(1))
                .andExpect(jsonPath("$.canonicalName").value("Arjuna Vishada Yoga"))
                .andExpect(jsonPath("$.shortIntent").exists())
                .andExpect(jsonPath("$.thematicIntroduction").doesNotExist());
    }
}
