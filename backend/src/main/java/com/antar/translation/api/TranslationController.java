package com.antar.translation.api;

import com.antar.translation.application.query.TranslationQueryService;
import com.antar.translation.domain.VerseId;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/translations/verses")
public class TranslationController {

    private final TranslationQueryService translationQueryService;

    public TranslationController(TranslationQueryService translationQueryService) {
        this.translationQueryService = translationQueryService;
    }

    @GetMapping("/{verseId}")
    public ResponseEntity<TranslationResponse> getTranslation(@PathVariable("verseId") String verseId) {
        TranslationResponse response = TranslationApiMapper.toResponse(
                translationQueryService.getPublishedTranslationForVerse(VerseId.of(verseId)));
        return ResponseEntity.ok().body(response);
    }
}
