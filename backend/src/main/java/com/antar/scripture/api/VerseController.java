package com.antar.scripture.api;

import com.antar.scripture.application.verse.query.VerseQueryService;
import com.antar.scripture.domain.VerseId;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/scripture/verses")
public class VerseController {

    private final VerseQueryService verseQueryService;

    public VerseController(VerseQueryService verseQueryService) {
        this.verseQueryService = verseQueryService;
    }

    @GetMapping("/{verseId}")
    public ResponseEntity<VerseDetailResponse> getVerse(@PathVariable("verseId") String verseId) {
        VerseDetailResponse response =
                VerseApiMapper.toDetailResponse(verseQueryService.getPublishedVerseDetail(VerseId.of(verseId)));
        return ResponseEntity.ok().body(response);
    }
}
