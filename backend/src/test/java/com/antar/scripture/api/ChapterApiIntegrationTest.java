package com.antar.scripture.api;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

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
class ChapterApiIntegrationTest extends AbstractIntegrationTest {

    private static final String CHAPTER_1_ID = "018f0000-0000-7000-8000-000000000001";

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void listChaptersReturnsPublishedChaptersInCanonicalOrder() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.items", hasSize(18)))
                .andExpect(jsonPath("$.items[0].chapterNumber").value(1))
                .andExpect(jsonPath("$.items[0].canonicalName").value("Arjuna Vishada Yoga"))
                .andExpect(jsonPath("$.items[1].chapterNumber").value(2))
                .andExpect(jsonPath("$.items[17].chapterNumber").value(18));
    }

    @Test
    void getChapterByIdReturnsPublishedChapter() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/{chapterId}", CHAPTER_1_ID))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(CHAPTER_1_ID))
                .andExpect(jsonPath("$.chapterNumber").value(1))
                .andExpect(jsonPath("$.englishName").value("The Yoga of Arjuna's Despair"))
                .andExpect(jsonPath("$.verseCount").value(47));
    }

    @Test
    void getChapterByNumberReturnsPublishedChapter() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/by-number/{chapterNumber}", 2))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.chapterNumber").value(2))
                .andExpect(jsonPath("$.canonicalName").value("Sankhya Yoga"))
                .andExpect(jsonPath("$.verseCount").value(72));
    }

    @Test
    void getChapterByInvalidNumberReturnsProblemDetails() throws Exception {
        mockMvc.perform(get("/api/v1/scripture/chapters/by-number/{chapterNumber}", 19))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors[0].field").value("chapterNumber"))
                .andExpect(jsonPath("$.errors[0].code").value("INVALID_CHAPTER_NUMBER"));
    }

    @Test
    void getMissingChapterReturnsNotFoundProblemDetails() throws Exception {
        mockMvc.perform(get(
                        "/api/v1/scripture/chapters/{chapterId}",
                        "018f0000-0000-7000-8000-00000000dead"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
    }

    @Test
    void unpublishedChapterIsNotVisibleToReaderApis() throws Exception {
        jdbcTemplate.update(
                "UPDATE scripture.chapters SET publication_status = 'DRAFT' WHERE chapter_number = 3");

        try {
            mockMvc.perform(get("/api/v1/scripture/chapters/by-number/{chapterNumber}", 3))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));

            mockMvc.perform(get("/api/v1/scripture/chapters"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.items", hasSize(17)));
        } finally {
            jdbcTemplate.update(
                    "UPDATE scripture.chapters SET publication_status = 'PUBLISHED' WHERE chapter_number = 3");
        }
    }
}
