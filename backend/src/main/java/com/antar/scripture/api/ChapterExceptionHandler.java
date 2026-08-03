package com.antar.scripture.api;

import com.antar.platform.web.ProblemDetailsResponse;
import com.antar.scripture.application.chapter.query.ChapterNotFoundException;
import com.antar.scripture.application.verse.query.ChapterHasNoPublishedVersesException;
import com.antar.scripture.domain.InvalidChapterIdException;
import com.antar.scripture.domain.InvalidChapterNumberException;
import jakarta.servlet.http.HttpServletRequest;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice(assignableTypes = ChapterController.class)
public class ChapterExceptionHandler {

    private static final String PROBLEM_BASE = "https://antar.app/problems/";

    @ExceptionHandler(ChapterNotFoundException.class)
    public ResponseEntity<ProblemDetailsResponse> handleChapterNotFound(
            ChapterNotFoundException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.NOT_FOUND,
                "resource-not-found",
                "Resource not found",
                "RESOURCE_NOT_FOUND",
                exception.getMessage(),
                request,
                List.of());
    }

    @ExceptionHandler(ChapterHasNoPublishedVersesException.class)
    public ResponseEntity<ProblemDetailsResponse> handleChapterHasNoPublishedVerses(
            ChapterHasNoPublishedVersesException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.NOT_FOUND,
                "content-not-published",
                "Published verses unavailable",
                "CONTENT_NOT_PUBLISHED",
                exception.getMessage(),
                request,
                List.of());
    }

    @ExceptionHandler(InvalidChapterNumberException.class)
    public ResponseEntity<ProblemDetailsResponse> handleInvalidChapterNumber(
            InvalidChapterNumberException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.BAD_REQUEST,
                "validation-error",
                "Request validation failed",
                "VALIDATION_ERROR",
                exception.getMessage(),
                request,
                List.of(new ProblemDetailsResponse.FieldError(
                        "chapterNumber",
                        "INVALID_CHAPTER_NUMBER",
                        exception.getMessage())));
    }

    @ExceptionHandler(InvalidChapterIdException.class)
    public ResponseEntity<ProblemDetailsResponse> handleInvalidChapterId(
            InvalidChapterIdException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.BAD_REQUEST,
                "validation-error",
                "Request validation failed",
                "VALIDATION_ERROR",
                exception.getMessage(),
                request,
                List.of(new ProblemDetailsResponse.FieldError(
                        "chapterId",
                        "INVALID_CHAPTER_ID",
                        exception.getMessage())));
    }

    private ResponseEntity<ProblemDetailsResponse> problem(
            HttpStatus status,
            String typeSuffix,
            String title,
            String code,
            String detail,
            HttpServletRequest request,
            List<ProblemDetailsResponse.FieldError> errors) {
        String requestId = resolveRequestId(request);
        ProblemDetailsResponse body = new ProblemDetailsResponse(
                PROBLEM_BASE + typeSuffix,
                title,
                status.value(),
                code,
                detail,
                request.getRequestURI(),
                requestId,
                errors);

        return ResponseEntity.status(status)
                .contentType(MediaType.APPLICATION_PROBLEM_JSON)
                .header("X-Request-Id", requestId)
                .body(body);
    }

    private static String resolveRequestId(HttpServletRequest request) {
        String incoming = request.getHeader("X-Request-Id");
        if (incoming != null && !incoming.isBlank()) {
            return incoming.trim();
        }
        return "req_" + UUID.randomUUID();
    }
}
