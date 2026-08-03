package com.antar.scripture.api;

import com.antar.scripture.application.chapter.query.ChapterQueryService;
import com.antar.scripture.domain.ChapterId;
import com.antar.scripture.domain.ChapterNumber;
import java.util.List;
import org.springframework.http.CacheControl;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/scripture/chapters")
public class ChapterController {

    private final ChapterQueryService chapterQueryService;

    public ChapterController(ChapterQueryService chapterQueryService) {
        this.chapterQueryService = chapterQueryService;
    }

    @GetMapping
    public ResponseEntity<ChapterListResponse> listChapters() {
        List<ChapterResponse> items = chapterQueryService.listPublishedChapters().stream()
                .map(ChapterApiMapper::toResponse)
                .toList();
        return ResponseEntity.ok()
                .cacheControl(CacheControl.noCache())
                .body(new ChapterListResponse(items));
    }

    @GetMapping("/by-number/{chapterNumber}")
    public ResponseEntity<ChapterResponse> getChapterByNumber(
            @PathVariable("chapterNumber") int chapterNumber) {
        ChapterResponse response = ChapterApiMapper.toResponse(
                chapterQueryService.getPublishedChapterByNumber(ChapterNumber.of(chapterNumber)));
        return ResponseEntity.ok().body(response);
    }

    @GetMapping("/{chapterId}")
    public ResponseEntity<ChapterResponse> getChapter(@PathVariable("chapterId") String chapterId) {
        ChapterResponse response =
                ChapterApiMapper.toResponse(chapterQueryService.getPublishedChapter(ChapterId.of(chapterId)));
        return ResponseEntity.ok().body(response);
    }
}
