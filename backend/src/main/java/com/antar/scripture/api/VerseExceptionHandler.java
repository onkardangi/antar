package com.antar.scripture.api;

import com.antar.platform.web.ProblemDetailsResponse;
import com.antar.scripture.application.verse.query.VerseNotFoundException;
import com.antar.scripture.domain.InvalidVerseIdException;
import jakarta.servlet.http.HttpServletRequest;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice(assignableTypes = VerseController.class)
public class VerseExceptionHandler {

    private static final String PROBLEM_BASE = "https://antar.app/problems/";

    @ExceptionHandler(VerseNotFoundException.class)
    public ResponseEntity<ProblemDetailsResponse> handleVerseNotFound(
            VerseNotFoundException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.NOT_FOUND,
                "resource-not-found",
                "Resource not found",
                "RESOURCE_NOT_FOUND",
                exception.getMessage(),
                request,
                List.of());
    }

    @ExceptionHandler(InvalidVerseIdException.class)
    public ResponseEntity<ProblemDetailsResponse> handleInvalidVerseId(
            InvalidVerseIdException exception, HttpServletRequest request) {
        return problem(
                HttpStatus.BAD_REQUEST,
                "validation-error",
                "Request validation failed",
                "VALIDATION_ERROR",
                exception.getMessage(),
                request,
                List.of(new ProblemDetailsResponse.FieldError(
                        "verseId",
                        "INVALID_VERSE_ID",
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
