package com.antar.platform.web;

import java.util.List;

/**
 * Antar Problem Details payload aligned with docs/architecture/04_API_CONTRACTS.md.
 */
public record ProblemDetailsResponse(
        String type,
        String title,
        int status,
        String code,
        String detail,
        String instance,
        String requestId,
        List<FieldError> errors) {

    public record FieldError(String field, String code, String message) {
    }
}
